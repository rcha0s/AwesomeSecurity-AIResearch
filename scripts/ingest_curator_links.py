#!/usr/bin/env python3
"""
ingest_curator_links.py — Stage the stories a trusted curator links to.

tl;dr sec (Clint Gibler's weekly newsletter) links the week's best security
research, much of it on small blogs with no feed of their own: on 2026-W43 the
recall eval missed 12 of its 13 on-thesis headlines, among them Zenity Labs,
enklypesalt.com, rea.tools and vincenzoiozzo.com. Its RSS feed is gone
(tldrsec.com/feed redirects to a 404), so this reads the public issue pages
listed in tldrsec.com/sitemap.xml, the same source the recall eval reads (the
/t/Newsletter archive page left out issue #349 when probed on 2026-10-22; the
sitemap had every issue). Issues are picked by number, the newest
`curator_links.max_issues`, and dated by the page's own publish date: the
sitemap lastmod is an edit date (#126, from 2022, carried 2026-05-28).

For each of those published in the last `curator_links.lookback_days` days:
  * eval_recall's issue parser: security sections only, first story link per
    paragraph, people/social links, sponsor blocks and paid links dropped;
  * lead paragraphs only: the paragraph opens with the linked headline (a
    follow-on paragraph links supporting material, not a story);
  * never a paywalled host (`curator_links.paywall_hosts`): it is never staged,
    so it is never fetched;
  * on-thesis: eval_recall.on_thesis (a taxonomy keyword hint fires and no
    excluded term does) and not on the news deny-list;
  * not already held: pools, archive, story ledger sources, or this run.

Each is staged with the article URL (tracking params stripped) as its citation,
the curator's headline as its title and blurb as its excerpt, `source_id`
`curator:tldrsec`, `curated_by: tldrsec` and the issue URL in `curator_issue`.
Only the curator host is fetched here (eval_recall.http_get refuses others).

It also records every arXiv id the issues link to in data/_curator_arxiv.json,
which paper_gate reads as the trusted-curator signal (aggregate.py runs after
this ingestor in run_scan.sh).

Usage:
    python scripts/ingest_curator_links.py [--dry-run] [--misses RECALL_JSON]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import aggregate as agg
import common as c
import dedupe_stories as ds
import eval_recall as er
import paper_gate as pg
import story_ledger as sl
import taxonomy as tx

CURATOR = "tldrsec"
SOURCE_ID = f"curator:{CURATOR}"
SOURCE_NAME = "tl;dr sec (curator link)"
DEFAULTS = {"max_issues": 2, "lookback_days": 14, "source_rank": 70.0}


def settings() -> dict:
    """sources.yaml `curator_links` (source_rank's rationale is documented there)."""
    cfg = (c.load_yaml(c.SOURCES_FILE) or {}).get("curator_links") or {}
    return {
        "max_issues": int(cfg.get("max_issues", DEFAULTS["max_issues"])),
        "lookback_days": int(cfg.get("lookback_days", DEFAULTS["lookback_days"])),
        "source_rank": float(cfg.get("source_rank", DEFAULTS["source_rank"])),
        "paywall_hosts": tuple(h.lower() for h in cfg.get("paywall_hosts") or ()),
    }


def url_key(url: str) -> str:
    """The comparison key for a story URL: tracking, www., query and case stripped."""
    return c.normalize_url(ds.canonical_url(url or ""))


def host_in(url: str, hosts: tuple[str, ...]) -> bool:
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    return any(host == h or host.endswith("." + h) for h in hosts)


def entry_urls(entry: dict) -> list[str]:
    urls = [entry.get(k) for k in ("source_url", "article_url", "tweet_url")]
    urls += [s.get("url") for s in entry.get("corroborating_sources") or [] if isinstance(s, dict)]
    return [u for u in urls if u]


def held() -> tuple[set[str], list[str]]:
    """(URL keys, titles) of everything already held: pools, archive, story ledger."""
    entries = c.all_pool_entries() + (c.load_json(c.ARCHIVE_FILE, default=[]) or [])
    keys = {url_key(u) for e in entries for u in entry_urls(e)}
    for story in (sl.load_ledger().get("stories") or {}).values():
        keys |= {url_key(s.get("url")) for s in story.get("sources") or [] if s.get("url")}
    return keys - {""}, [e.get("title") or "" for e in entries]


def is_held(it: dict, keys: set[str], titles: list[str]) -> bool:
    if url_key(it["href"]) in keys:
        return True
    return any(c.title_similar(it["title"], t) for t in titles if t)


def keep(it: dict, tax: tx.Taxonomy, paywall: tuple[str, ...]) -> str | None:
    """Why a parsed link is not staged, else None."""
    if not it.get("lead"):
        return "follow-on"
    if host_in(it["href"], paywall):
        return "paywall"
    if not er.on_thesis(it, tax):
        return "off-thesis"
    if c.news_denylist_hit({"title": it["title"], "summary": it["text"]}):
        return "denylist"
    return None


def label_for(blob: str, rules: dict, tax: tx.Taxonomy) -> str:
    """The router class (sources.yaml), else the taxonomy's best domain ID: an
    on-thesis link always has at least one taxonomy hint."""
    label = agg.classify_domain(blob, rules, [])
    if label:
        return label
    scores = tx.keyword_scores(blob, list(tax.domains.values()))
    return max(sorted(scores), key=lambda d: scores[d])


def candidate(it: dict, issue: str, rules: dict, tax: tx.Taxonomy, src_rank: float) -> dict:
    url = c.clean_source_url(it["href"])
    excerpt = c.clean_summary(it["text"], 320)
    blob = f"{it['title']} {excerpt}"
    return {
        "id": c.make_id(it["title"], c.normalize_url(url)),
        "discovered_via": "curator",
        "title": it["title"],
        "source_name": SOURCE_NAME,
        "source_type": f"Curator link: tl;dr sec, {it['section']}",
        "source_url": url,
        "article_url": url,
        "tweet_url": None,
        "author": None,
        "published": it["published"],
        "date": it["published"][:7],
        "excerpt": excerpt,
        "raw_path": None,
        **agg.guess_fields(blob, label_for(blob, rules, tax), rules),
        "source_id": SOURCE_ID,
        "source_rank": src_rank,
        "source_topics": ["ai-security", "product-security"],
        "curated_by": CURATOR,
        "curator_issue": issue,
        "retrieved_at": c.utcnow_iso(),
    }


def from_issues(issues: list[tuple[str, str, str]], cfg: dict, rules: dict) -> dict:
    """Parse issues into {"candidates", "arxiv", "counts", "per_issue"}. An arXiv
    link staged here is admitted by construction: the issue is its curator signal."""
    tax, src_rank = tx.get(), cfg["source_rank"]
    keys, titles = held()
    out: list[dict] = []
    arxiv: dict[str, str] = {}
    counts = {"issues": len(issues), "links": 0, "staged": 0, "held": 0}
    per_issue: dict[str, dict[str, int]] = {}
    for issue_url, published, page in issues:
        arxiv.update({i: published for i in pg.arxiv_ids(page)})
        mine = per_issue.setdefault(issue_url, {"links": 0, "staged": 0})
        for it in er.parse_tldrsec_issue(page, published):
            mine["links"] += 1
            why = keep(it, tax, cfg["paywall_hosts"])
            if why is None and is_held(it, keys, titles):
                why = "held"
            counts[why or "staged"] = counts.get(why or "staged", 0) + 1
            if why:
                continue
            keys.add(url_key(it["href"]))
            titles.append(it["title"])
            out.append(candidate(it, issue_url, rules, tax, src_rank))
            mine["staged"] += 1
        counts["links"] += mine["links"]
    return {"candidates": out, "arxiv": arxiv, "counts": counts, "per_issue": per_issue}


def collect(fetch: Callable[[str], str], cfg: dict, rules: dict) -> dict:
    since = (c.utcnow() - timedelta(days=cfg["lookback_days"])).date().isoformat()
    return from_issues(er.tldrsec_issues(fetch, since, cfg["max_issues"]), cfg, rules)


def would_stage(result: dict, recall_path: Path) -> list[dict]:
    """The recall result's misses this run would stage (matched by URL key)."""
    staged = {url_key(cand["article_url"]) for cand in result["candidates"]}
    misses = json.loads(recall_path.read_text()).get("misses") or []
    return [m for m in misses if url_key(m.get("url", "")) in staged]


def report(result: dict) -> None:
    counts = result["counts"]
    print(f"Curator links ({CURATOR}): " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    for issue, n in result["per_issue"].items():
        print(f"   {issue}: {n['links']} story links, {n['staged']} staged")
    for cand in result["candidates"]:
        print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title'][:80]}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--misses", type=Path, help="a recall result: report which misses we'd stage")
    args = ap.parse_args(argv)
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    result = collect(er.http_get, settings(), rules)
    report(result)
    if args.misses:
        hits = would_stage(result, args.misses)
        print(f"Recall misses this would stage: {len(hits)}")
        for m in hits:
            print(f"   [{m.get('curator')}] {m.get('title', '')[:80]}")
    if args.dry_run:
        return 0
    pg.save_curator_link_ids(result["arxiv"])
    added = c.add_candidates(result["candidates"])
    print(f"Staged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
