#!/usr/bin/env python3
"""
generate_stream.py - render each research stream (data/streams.yaml).

For every stream it writes, under docs/streams/:
  <id>.md    the stream as one Markdown page a harness can fetch, at
             <site>/streams/<id>.md: per sub-category its live claims (Do this,
             Conditions, evidence) and findings (Try:), in efficiency_feed.py's blocks
  <id>.json  the same as a JSON Feed 1.1 document (https://jsonfeed.org/version/1.1),
             served by GitHub Pages at <site>/streams/<id>.json, so a harness or a
             feed reader can poll it. Each item carries a `_stream` extension with
             its sub-category, domain, takeaway, action and related claims; the
             top level carries `_stream.claims`, the standing answers.

What enters: findings from every pool and the archive whose domain a
sub-category takes (streams.classify), dated inside the stream's
`library_days`, that pass the same integrity bar as the curated view
(common.is_curated) judged as if they were fresh. The site prunes after
`max_age_days` and its composite decays with age; a stream is a library, so a
finding is not dropped for being a month old. One entry per story
(story_ledger), the best composite first. Claims enter when live (current or
contested) and classified into the stream.

Pure rendering over committed data: no network, no LLM. Do not hand-edit the
outputs; edit data/streams.yaml or the pools and regenerate.

Usage:
    python scripts/generate_stream.py            # every stream
    python scripts/generate_stream.py --check    # exit 1 if an output is stale
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict

import briefing
import common as c
import efficiency_feed as ef
import story_ledger as sl
import streams as st
import taxonomy as tx

import claims as cl

OUT_DIR = c.ROOT / "docs" / "streams"
REPO_NAME = "AwesomeSecurity-AIResearch"
REPO_URL = f"https://github.com/rcha0s/{REPO_NAME}"
SITE_URL = f"https://rcha0s.github.io/{REPO_NAME}/"
LIVE_CLAIM = ("current", "contested")
MD_PER_SUBCATEGORY = 12  # findings listed per sub-category on the GitHub page
TEXT_MAX = 400


def library_vetted(entry: dict, conf: c.Config) -> bool:
    """common.is_curated with age taken out: the same integrity checks and score
    floors, newness counted as fresh. A finding the curated view held stays out."""
    fresh = dict(entry)
    scores = dict(entry.get("scores") or {})
    scores.pop("composite", None)
    scores["newness"] = 100.0
    fresh["scores"] = scores
    return c.is_curated(fresh, conf)


def watch_eligible(entry: dict, conf: c.Config, min_relevance: float | None) -> bool:
    """A finding held only for its scores, still worth a harness builder's look:
    scored, not refuted, every checked excerpt grounded, not held for its domain
    or its readability, and relevance at least `min_relevance`."""
    if min_relevance is None or not c.is_scored(entry):
        return False
    if entry.get("verified") is False or c.domain_held(entry) or c.readability_held(entry):
        return False
    if c.reddit_only(entry):
        return False
    grounding = entry.get("grounding_score")
    if grounding is not None and grounding < 1.0:
        return False
    return float((entry.get("scores") or {}).get("relevance") or 0) >= min_relevance


def tier_of(entry: dict, conf: c.Config, stream: st.Stream) -> str | None:
    """`vetted`, `watch` or None (not in the stream)."""
    if library_vetted(entry, conf):
        return "vetted"
    if watch_eligible(entry, conf, stream.watch_min_relevance):
        return "watch"
    return None


def _clip(text: str, limit: int = TEXT_MAX) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def entry_url(entry: dict) -> str:
    return entry.get("article_url") or entry.get("source_url") or entry.get("tweet_url") or ""


def detail_path(entry: dict, curated_ids: set[str]) -> str | None:
    """The repo page generate_site.py writes for a curated pool entry, if any."""
    if entry.get("id") not in curated_ids:
        return None
    date = entry.get("date") or "undated"
    name = f"{date}-{c.slugify(entry.get('title', ''), 60)}.md"
    return f"{entry.get('topic')}/{c.domain_slug(entry.get('domain') or 'General')}/{name}"


def collect(stream: st.Stream, conf: c.Config, now, pools: dict, archive: list, index: dict) -> list[dict]:
    """The stream's findings: classified, in the library window, vetted, one per story."""
    rows: list[tuple[dict, str, bool]] = []
    for topic, pool in pools.items():
        for entry in pool:
            rows.append((entry, topic, True))
    for entry in archive:
        rows.append((entry, entry.get("topic") or "", False))

    best: dict[str, dict] = {}
    # Vetted before watch, then the best composite: the story's best entry speaks for it.
    def order(row):
        return (0 if library_vetted(row[0], conf) else 1, -c.entry_composite(row[0], conf))

    for entry, topic, in_pool in sorted(rows, key=order):
        sub = st.classify(entry, stream)
        if not sub or not st.in_library(entry, now, stream.library_days):
            continue
        tier = tier_of(entry, conf, stream)
        if not tier:
            continue
        url = c.normalize_url(entry_url(entry)) or ""
        key = index.get(entry.get("id") or "") or (f"u-{url}" if url else f"e-{entry.get('id')}")
        if key in best:
            continue
        best[key] = {**entry, "topic": entry.get("topic") or topic, "_sub": sub, "_tier": tier, "_in_pool": in_pool}
    # A story already taken under another key (same URL, different story id) is dropped too.
    seen_urls: set[str] = set()
    out = []
    for row in best.values():
        url = c.normalize_url(entry_url(row)) or ""
        if url and url in seen_urls:
            continue
        seen_urls.add(url)
        out.append(row)
    out.sort(key=lambda r: (st.item_date(r), r.get("title") or ""), reverse=True)
    return out


def stream_claims(stream: st.Stream, ledger: dict) -> list[dict]:
    live = [cl_ for cl_ in ledger.get("claims") or [] if cl_.get("status") in LIVE_CLAIM]
    out = []
    for claim in live:
        sub = st.classify(claim, stream)
        if sub:
            out.append({**claim, "_sub": sub})
    order = {s.id: i for i, s in enumerate(stream.subcategories)}
    out.sort(key=lambda x: (order[x["_sub"]], x.get("id") or ""))
    return out


def feed_item(row: dict, stream: st.Stream, curated_ids: set[str]) -> dict:
    sub = stream.subcategory(row["_sub"])
    path = detail_path(row, curated_ids)
    action = row.get("actionable") or {}
    item = {
        "id": row.get("id"),
        "url": entry_url(row),
        "title": row.get("title") or "",
        "summary": _clip(row.get("takeaway") or row.get("summary")),
        "content_text": _clip(row.get("summary"), 1200),
        "date_published": st.item_date(row) or None,
        "tags": [sub.name] + [str(t) for t in row.get("tags") or []][:8],
        "_stream": {
            "subcategory": sub.id,
            "tier": row["_tier"],
            "domain": row.get("domain"),
            "source": row.get("source_name"),
            "takeaway": row.get("takeaway") or "",
            "action": {k: action.get(k) for k in ("type", "title", "detail") if action.get(k)} or None,
            "related_claims": list(row.get("related_claims") or []),
            "detail": f"{REPO_URL}/blob/main/{path}" if path else None,
            "on_site": bool(row.get("_in_pool") and path),
        },
    }
    if path and row.get("_in_pool"):
        item["external_url"] = f"{SITE_URL}?finding={row.get('id')}#week"
    return item


def claim_item(claim: dict) -> dict:
    return {
        "id": claim.get("id"),
        "title": claim.get("title"),
        "statement": _clip(claim.get("statement"), 600),
        "guidance": _clip(claim.get("guidance"), 600) or None,
        "status": claim.get("status"),
        "subcategory": claim["_sub"],
        "domain": claim.get("domain"),
        "changed_on": claim.get("changed_on") or claim.get("added_on"),
        "url": f"{SITE_URL}?claim={claim.get('id')}#claims",
    }


def render_feed(stream: st.Stream, rows: list[dict], claims: list[dict], curated_ids: set[str], now: str) -> str:
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": f"{stream.name} - Awesome Security & AI Research",
        "home_page_url": f"{REPO_URL}/blob/main/docs/streams/{stream.id}.md",
        "feed_url": f"{SITE_URL}streams/{stream.id}.json",
        "description": stream.blurb,
        "language": "en",
        "_stream": {
            "id": stream.id,
            "generated": now,
            "library_days": stream.library_days,
            "subcategories": [{"id": s.id, "name": s.name, "scope": s.scope} for s in stream.subcategories],
            "watch_min_relevance": stream.watch_min_relevance,
            "counts": {s.id: sum(1 for r in rows if r["_sub"] == s.id) for s in stream.subcategories},
            "claims": [claim_item(x) for x in claims],
        },
        "items": [feed_item(r, stream, curated_ids) for r in rows[: stream.feed_max]],
    }
    return json.dumps(feed, indent=2, ensure_ascii=False) + "\n"


def _finding_row(row: dict) -> dict:
    """A stream finding in the row shape efficiency_feed._finding_line reads."""
    return {
        "title": row.get("title"),
        "url": entry_url(row),
        "published": st.item_date(row),
        "source_name": row.get("source_name"),
        "takeaway": row.get("takeaway"),
        "actionable": row.get("actionable") or {},
    }


def _claim_sort_key(claim: dict) -> tuple:
    return (briefing.claim_updated(claim), str(claim.get("id") or ""))


def render_md(stream: st.Stream, rows: list[dict], claims: list[dict], curated_ids: set[str], now: str) -> str:
    """The stream as one Markdown page a harness can fetch, in the same claim and
    finding blocks as docs/efficiency.md (efficiency_feed.py): each claim with
    **Do this**, **Conditions** and evidence newest first, each finding with a
    "Try:" line. `curated_ids` is unused here (the JSON feed links writeups)."""
    by_sub: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_sub[row["_sub"]].append(row)
    claims_by_sub: dict[str, list[dict]] = defaultdict(list)
    for claim in sorted(claims, key=_claim_sort_key, reverse=True):
        claims_by_sub[claim["_sub"]].append(claim)
    vetted = sum(1 for r in rows if r["_tier"] == "vetted")
    watch = len(rows) - vetted
    feed_url = f"{SITE_URL}streams/{stream.id}.json"
    out = [
        f"# {ef._md(stream.name)}",
        "",
        f"_{ef._md(stream.blurb)}_",
        "",
        f"_Generated {now} from the claim ledger, the pools and the archive of "
        f"[Awesome Security & AI Research]({SITE_URL}) by the rules in `data/streams.yaml`. "
        "Generated - do not hand-edit._",
        "",
        "This page is meant to be fetched by an agent harness, like "
        f"[efficiency.md]({SITE_URL}efficiency.md), which covers the first two sub-categories. "
        "Each claim is a standing answer: **Do this** is the change to make, **Conditions** is "
        "where it does not hold, and the evidence is newest first. Findings are research from "
        f"the last {stream.library_days} days, newest first; **Worth a look** findings passed "
        "every fact check but sat below the Briefing's novelty bar. "
        f"The same data as JSON Feed 1.1: [{stream.id}.json]({feed_url}) "
        "(filter items by `_stream.subcategory`).",
        "",
        f"{len(claims)} live claims, {vetted} vetted findings, {watch} worth a look.",
        "",
    ]
    for sub in stream.subcategories:
        n_claims, n_rows = len(claims_by_sub[sub.id]), len(by_sub[sub.id])
        out.append(f"- [{ef._md(sub.name)}](#{sub.id}): {n_claims} claims, {n_rows} findings")
    for sub in stream.subcategories:
        out += ["", f'<a id="{sub.id}"></a>', "", f"## {ef._md(sub.name)}", "", f"_{ef._md(sub.scope)}_", ""]
        for claim in claims_by_sub[sub.id]:
            out += ef._claim_block(claim, SITE_URL)
        sub_rows = by_sub[sub.id]
        for tier, label in (("vetted", "New research"), ("watch", "Worth a look")):
            tier_rows = [r for r in sub_rows if r["_tier"] == tier]
            if not tier_rows:
                continue
            out += [f"**{label}** ({len(tier_rows)})", ""]
            for row in tier_rows[:MD_PER_SUBCATEGORY]:
                out += ef._finding_line(_finding_row(row))
            if len(tier_rows) > MD_PER_SUBCATEGORY:
                out.append(f"- _{len(tier_rows) - MD_PER_SUBCATEGORY} more in the JSON feed._")
            out.append("")
        if not claims_by_sub[sub.id] and not sub_rows:
            out += ["_Nothing yet: no live claim or finding in the window._", ""]
    return "\n".join(out).rstrip() + "\n"


def build(conf: c.Config | None = None, now=None) -> dict[str, str]:
    """{relative output path: text} for every stream."""
    conf = conf or c.load_config()
    now = now or c.utcnow()
    stamp = now.strftime("%Y-%m-%d")
    known = set(tx.get().domains)
    all_streams = st.load(known_domains=known)
    pools = {topic: c.load_pool(topic)["entries"] for topic in c.TOPICS}
    archive = c.load_json(c.ARCHIVE_FILE, default=[]) or []
    _, index = sl.render_context()
    curated_ids = {e.get("id") for entries in pools.values() for e in entries if c.is_curated(e, conf)}
    ledger = cl.load_ledger()
    out: dict[str, str] = {}
    for stream in all_streams.values():
        rows = collect(stream, conf, now, pools, archive, index)
        claims = stream_claims(stream, ledger)
        out[f"docs/streams/{stream.id}.md"] = render_md(stream, rows, claims, curated_ids, stamp)
        out[f"docs/streams/{stream.id}.json"] = render_feed(stream, rows, claims, curated_ids, stamp)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if a rendered stream differs from disk")
    args = ap.parse_args(argv)
    outputs = build()
    stale = []
    for rel, text in outputs.items():
        path = c.ROOT / rel
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(rel)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if args.check:
        for rel in stale:
            print(f"STALE {rel}")
        return 1 if stale else 0
    print(f"Rendered {len(outputs)} stream files under docs/streams/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
