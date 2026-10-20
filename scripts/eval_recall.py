#!/usr/bin/env python3
"""
eval_recall.py — Did we catch what the reference curators led with? (ISA ISC-22)

Each week, pull the headline story links from four reference curators:

  tldrsec   tl;dr sec issues (tldrsec.com sitemap -> /p/tldr-sec-<n> pages): the
            first link of each paragraph in the security sections, not Misc
  simon     Simon Willison's weblog, the `security` and `prompt-injection` tag feeds:
            the post and the story it links to
  ghsa      GitHub reviewed advisories, severity critical (`gh api`, REST)
  kev       CISA Known Exploited Vulnerabilities, recently added

keep the on-thesis ones (a taxonomy keyword hint fires and no excluded term
does), and score the fraction we already hold anywhere in the pools or the
archive. A headline is held when an entry shares its canonical URL, a CVE or
GHSA id, or (dedupe_stories.is_collision) its title and entities.

The misses are the source-tuning signal: the report lists them and their hosts.

Usage:
    python scripts/eval_recall.py --live [--write] [--if-missing]   # fetch the curators (network)
    python scripts/eval_recall.py --fixtures DIR     # recorded responses (tests)
Exit 0 = recall >= evals.thresholds.recall_min, 1 = below, 2 = could not run.
--write saves data/evals/recall-<ISO week>.json.

Only the curator hosts in CURATOR_HOSTS are fetched (also printed by
scripts/allowlist.py); GitHub goes through the authed `gh` CLI.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote, urlparse

import common as c
import dedupe_stories as ds
import eval_lib as el
import taxonomy as tx

TLDRSEC_SITEMAP = "https://tldrsec.com/sitemap.xml"
SIMON_FEEDS = (
    "https://simonwillison.net/tags/security.atom",
    "https://simonwillison.net/tags/prompt-injection.atom",
)
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NVD_URL = "https://nvd.nist.gov/vuln/detail/"
CURATOR_HOSTS = ("tldrsec.com", "simonwillison.net", "www.cisa.gov")
ISSUE_URL = re.compile(r"^https://tldrsec\.com/p/tldr-sec-\d+$")
# tl;dr sec sections that aren't security headlines.
SKIP_SECTIONS = ("misc", "wrapping up", "advice", "sponsor", "")
# Paragraph links to people and social posts are credits, not stories.
PEOPLE_HOSTS = ("linkedin.com", "x.com", "twitter.com", "bsky.app", "youtube.com", "mastodon")
VULN_ID = re.compile(r"\b(CVE-\d{4}-\d{4,7}|GHSA(?:-[23456789cfghjmpqrvwx]{4}){3})\b", re.I)
TAG = re.compile(r"<[^>]+>")
LINK = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S | re.I)
PARA = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
H2 = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.S | re.I)
SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def item(curator: str, title: str, url: str, published: str, text: str = "", urls=()) -> dict:
    blob = f"{title} {text}"
    return {
        "curator": curator,
        "title": html.unescape(title).strip(),
        "url": url,
        "urls": sorted({u for u in (url, *urls) if u}),
        "published": published,
        "text": html.unescape(TAG.sub(" ", blob)),
        "ids": sorted({m.upper() for m in VULN_ID.findall(blob)}),
    }


# --- Parsers (pure: tests feed them recorded responses) -----------------------
def parse_tldrsec_sitemap(xml: str, since: str) -> list[tuple[str, str]]:
    """(issue URL, lastmod) for issues modified on or after `since` (YYYY-MM-DD)."""
    out = []
    for node in ET.fromstring(xml).iter(f"{SM}url"):
        loc = (node.findtext(f"{SM}loc") or "").strip()
        mod = (node.findtext(f"{SM}lastmod") or "")[:10]
        if ISSUE_URL.match(loc) and mod >= since:
            out.append((loc, mod))
    return out


def _is_story_link(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return url.startswith("http") and not any(p in host for p in PEOPLE_HOSTS + ("tldrsec.com",))


def parse_tldrsec_issue(page: str, issue_url: str, published: str) -> list[dict]:
    """The first story link of every paragraph in the issue's security sections."""
    out = []
    parts = H2.split(page)  # [preamble, heading, body, heading, body, ...]
    for heading, body in zip(parts[1::2], parts[2::2], strict=False):
        name = TAG.sub("", html.unescape(heading)).strip().lower()
        name = re.sub(r"^[^a-z0-9]+", "", name)
        if any(name.startswith(s) for s in SKIP_SECTIONS if s) or not name:
            continue
        for para in PARA.findall(body):
            links = [(h, t) for h, t in LINK.findall(para) if _is_story_link(html.unescape(h))]
            if links:
                href, anchor = links[0]
                url = ds.canonical_url(html.unescape(href))
                out.append(item("tldrsec", TAG.sub("", anchor), url, published, para, (issue_url,)))
    return out


def parse_atom(feed: str, since: str, curator: str = "simon") -> list[dict]:
    """Feed entries published on or after `since`; urls = the post + its first link."""
    import feedparser

    out = []
    for e in feedparser.parse(feed).entries:
        published = (e.get("published") or e.get("updated") or "")[:10]
        if published < since:
            continue
        body = e.get("summary") or ""
        first = next((h for h, _ in LINK.findall(body) if h.startswith("http")), "")
        out.append(item(curator, e.get("title", ""), e.get("link", ""), published, body, (first,)))
    return out


def parse_ghsa(advisories: list[dict]) -> list[dict]:
    out = []
    for adv in advisories if isinstance(advisories, list) else []:
        ids = " ".join(filter(None, [adv.get("ghsa_id"), adv.get("cve_id")]))
        text = f"{ids} {adv.get('description') or ''}"[:1500]
        published = (adv.get("published_at") or "")[:10]
        out.append(
            item("ghsa", adv.get("summary") or ids, adv.get("html_url") or "", published, text)
        )
    return out


def parse_kev(data: dict, since: str) -> list[dict]:
    out = []
    for v in (data or {}).get("vulnerabilities") or []:
        added = v.get("dateAdded") or ""
        if added < since:
            continue
        cve = v.get("cveID") or ""
        text = f"{cve} {v.get('vendorProject')} {v.get('product')} {v.get('shortDescription')}"
        out.append(item("kev", v.get("vulnerabilityName") or cve, NVD_URL + cve, added, text))
    return out


# --- Fetching (live mode only) ------------------------------------------------
def http_get(url: str) -> str:
    """GET a curator URL. Refuses any host outside CURATOR_HOSTS."""
    import requests

    if (urlparse(url).hostname or "") not in CURATOR_HOSTS:
        raise ValueError(f"recall: {url} is not a curator host")
    resp = requests.get(url, timeout=45, headers={"User-Agent": c.HTTP_USER_AGENT})
    resp.raise_for_status()
    return resp.text


def gh_advisories(since: str, today: str) -> list[dict]:
    query = f"type=reviewed&severity=critical&per_page=100&published={quote(since + '..' + today)}"
    out = subprocess.run(
        ["gh", "api", f"/advisories?{query}"], capture_output=True, text=True, timeout=90
    )
    if out.returncode != 0:
        raise RuntimeError(f"gh api /advisories failed: {out.stderr.strip()[:200]}")
    return json.loads(out.stdout)


def live_source(since: str, today: str) -> Callable[[str], object]:
    def get(name: str) -> object:
        if name == "tldrsec":
            issues = parse_tldrsec_sitemap(http_get(TLDRSEC_SITEMAP), since)
            return [(u, mod, http_get(u)) for u, mod in issues]
        if name == "simon":
            return [http_get(u) for u in SIMON_FEEDS]
        if name == "ghsa":
            return gh_advisories(since, today)
        return json.loads(http_get(KEV_URL))

    return get


def fixture_source(directory: Path, since: str) -> Callable[[str], object]:
    """Recorded responses: tldrsec_sitemap.xml + tldrsec-<n>.html, simon-*.atom,
    ghsa.json, kev.json. A missing file is an empty curator."""

    def get(name: str) -> object:
        if name == "tldrsec":
            sm = directory / "tldrsec_sitemap.xml"
            urls = parse_tldrsec_sitemap(sm.read_text(), since) if sm.exists() else []
            pages = [(u, mod, directory / f"{u.rsplit('/', 1)[1]}.html") for u, mod in urls]
            return [(u, mod, p.read_text()) for u, mod, p in pages if p.exists()]
        if name == "simon":
            return [p.read_text() for p in sorted(directory.glob("simon-*.atom"))]
        path = directory / f"{name}.json"
        return json.loads(path.read_text()) if path.exists() else ([] if name == "ghsa" else {})

    return get


def collect(get: Callable[[str], object], since: str) -> tuple[list[dict], list[str]]:
    """(headlines, errors). One curator failing never sinks the others."""
    items: list[dict] = []
    errors: list[str] = []
    for name in ("tldrsec", "simon", "ghsa", "kev"):
        try:
            raw = get(name)
            if name == "tldrsec":
                for url, published, page in raw:
                    items += parse_tldrsec_issue(page, url, published)
            elif name == "simon":
                for feed in raw:
                    items += parse_atom(feed, since)
            elif name == "ghsa":
                items += parse_ghsa(raw)
            else:
                items += parse_kev(raw, since)
        except Exception as exc:  # noqa: BLE001 - a curator outage is a reported error
            errors.append(f"{name}: {type(exc).__name__}: {str(exc)[:160]}")
    return dedupe(items), errors


def dedupe(items: list[dict]) -> list[dict]:
    """One row per story: the same link from two curators counts once."""
    seen, out = set(), []
    for it in items:
        key = ds.canonical_url(it["url"]) or it["title"].lower()
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


# --- Scoring ------------------------------------------------------------------
def on_thesis(it: dict, tax: tx.Taxonomy) -> bool:
    text = f"{it['title']} {it['text']}".lower()
    if any(term in text for term in tax.excluded_terms):
        return False
    return max(tx.keyword_scores(text, list(tax.domains.values())).values(), default=0) > 0


def entry_index(entries: list[dict]) -> dict:
    """Lookups for matching: canonical URLs, vuln ids, and story fingerprints."""
    urls, ids, prints = {}, {}, []
    for e in entries:
        for k in ("source_url", "article_url", "tweet_url"):
            if e.get(k):
                urls[ds.canonical_url(e[k])] = e
        for corr in e.get("corroborating_sources") or []:
            if isinstance(corr, dict) and corr.get("url"):
                urls[ds.canonical_url(corr["url"])] = e
        blob = " ".join(
            str(e.get(k) or "") for k in ("title", "summary", "source_url", "article_url")
        )
        for vid in VULN_ID.findall(blob):
            ids[vid.upper()] = e
        prints.append((ds.story_fingerprint(e), e))
    return {"urls": urls, "ids": ids, "prints": prints}


def find_match(it: dict, index: dict) -> tuple[dict, str] | None:
    for u in it["urls"]:
        if ds.canonical_url(u) in index["urls"]:
            return index["urls"][ds.canonical_url(u)], "url"
    for vid in it["ids"]:
        if vid in index["ids"]:
            return index["ids"][vid], "id"
    fp = ds.story_fingerprint({"title": it["title"], "summary": it["text"][:200], "source_url": ""})
    for other, e in index["prints"]:
        if ds.is_collision(fp, other):
            return e, "title+entities"
    return None


def score(items: list[dict], entries: list[dict], tax: tx.Taxonomy) -> dict:
    index = entry_index(entries)
    scored, misses = [], []
    for it in (i for i in items if on_thesis(i, tax)):
        hit = find_match(it, index)
        row = {k: it[k] for k in ("curator", "title", "url", "published")}
        if hit:
            row.update(matched=hit[0].get("id"), how=hit[1])
        else:
            misses.append(row)
        scored.append(row)
    hosts = Counter((urlparse(m["url"]).hostname or "?").removeprefix("www.") for m in misses)
    by_curator = Counter(r["curator"] for r in scored)
    return {
        "headlines": len(items),
        "on_thesis": len(scored),
        "matched": len(scored) - len(misses),
        "recall": round((len(scored) - len(misses)) / len(scored), 3) if scored else None,
        "by_curator": dict(by_curator),
        "misses": misses,
        "miss_hosts": dict(hosts.most_common()),
        "matched_rows": [r for r in scored if "matched" in r],
    }


def run(get: Callable[[str], object], now: datetime, lookback_days: int) -> dict:
    since = (now - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    items, errors = collect(get, since)
    entries = c.all_pool_entries() + (c.load_json(c.ARCHIVE_FILE, default=[]) or [])
    result = score(items, entries, tx.get())
    return {"generated": c.utcnow_iso(), "week": el.iso_week(now), "since": since,
            "errors": errors, **result}  # fmt: skip


def print_report(result: dict) -> None:
    for err in result["errors"]:
        print(f"ERROR {err}")
    for m in result["misses"]:
        print(f"MISS [{m['curator']}] {m['title'][:90]} <{m['url']}>")
    if result["miss_hosts"]:
        hosts = ", ".join(f"{h} ({n})" for h, n in result["miss_hosts"].items())
        print(f"Miss hosts: {hosts}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true", help="fetch the curators (network)")
    mode.add_argument("--fixtures", type=Path, help="read recorded responses from DIR")
    ap.add_argument("--write", action="store_true", help="save data/evals/recall-<week>.json")
    ap.add_argument("--json", action="store_true", help="print the full result")
    ap.add_argument("--if-missing", action="store_true", help="skip if this week's file exists")
    args = ap.parse_args(argv)
    cfg, now = el.settings(), c.utcnow()
    existing = el.evals_dir() / f"recall-{el.iso_week(now)}.json"
    if args.if_missing and existing.exists():
        print(f"recall: {existing.name} already exists; not re-fetching")
        return 0
    since = (now - timedelta(days=int(cfg["recall"]["lookback_days"]))).strftime("%Y-%m-%d")
    get = (
        live_source(since, now.strftime("%Y-%m-%d"))
        if args.live
        else fixture_source(args.fixtures, since)
    )
    result = run(get, now, int(cfg["recall"]["lookback_days"]))
    print(json.dumps(result, indent=2)) if args.json else print_report(result)
    recall, floor = result["recall"], float(cfg["thresholds"]["recall_min"])
    passed = recall is not None and recall >= floor and not result["errors"]
    if args.write:
        path = el.evals_dir() / f"recall-{result['week']}.json"
        c.save_json(path, {**result, "passed": passed})
        print(f"wrote {path.relative_to(c.ROOT)}", file=sys.stderr)
    print(
        el.summary_line(
            "recall", passed, recall=recall if recall is not None else "none", matched=result["matched"],
            on_thesis=result["on_thesis"], headlines=result["headlines"],
            misses=len(result["misses"]), errors=len(result["errors"]), week=result["week"],
        )
    )  # fmt: skip
    if recall is None and result["errors"]:
        return 2
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
