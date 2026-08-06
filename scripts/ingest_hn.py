#!/usr/bin/env python3
"""
ingest_hn.py — Discover fast-moving security/AI stories from Hacker News.

Queries the keyless HN Algolia API (`search_by_date`) for the topics in
sources.yaml `hackernews:`, keeps stories inside the freshness window that clear
a points floor, classifies each with the shared keyword classifier, and stages
them as candidates in data/candidates.json. HN is a velocity signal — it surfaces
a wave breaking, hours to days before it reaches a curated feed. Novelty is judged
at analysis time (the /research-scan skill); the curation gate holds derivative
items as needs_review.

Runs on Windows or WSL (network, no auth). No LLM here.

Usage:
    python scripts/ingest_hn.py --dry-run
    python scripts/ingest_hn.py --max 6
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime, timedelta

import aggregate as agg
import common as c

HN_SEARCH = "http://hn.algolia.com/api/v1/search_by_date"
HN_ITEM = "https://news.ycombinator.com/item?id="
# HN is an aggregator, not a first-party source: a neutral-medium credibility.
HN_SOURCE_RANK = 55.0


def search_stories(query: str, limit: int, since_ts: int,
                   min_points: int = 0) -> list[dict]:
    """Recent HN stories matching `query`, newest first. [] on any failure.

    When called with query="" and min_points>=100, this is the "top-stories"
    tap — pull every high-scoring story in the window regardless of keyword,
    and let the shared classifier drop off-topic ones downstream."""
    import requests  # local import keeps offline unit tests import-clean

    filters = [f"created_at_i>={since_ts}"]
    if min_points > 0:
        filters.append(f"points>={min_points}")
    params = {
        "query": query,
        "tags": "story",
        "numericFilters": ",".join(filters),
        "hitsPerPage": str(limit),
    }
    try:
        resp = requests.get(
            HN_SEARCH,
            params=params,
            timeout=30,
            headers={"User-Agent": "AwesomeSecurityResearch/1.0"},
        )
        resp.raise_for_status()
        return resp.json().get("hits", []) or []
    except Exception as exc:  # noqa: BLE001 - discovery is best-effort
        label = query or f"top>={min_points}"
        print(f"   ! HN search failed for {label!r}: {exc}", file=sys.stderr)
        return []


def hit_to_candidate(hit: dict, rules: dict) -> dict | None:
    """Map an HN Algolia hit to a candidate; None if it doesn't classify on-topic."""
    title = (hit.get("title") or "").strip()
    # Self/Ask-HN posts have no external url — fall back to the HN discussion.
    external = (hit.get("url") or "").strip()
    hn_url = HN_ITEM + str(hit.get("objectID", ""))
    article_url = external or hn_url
    if not title or not c.normalize_url(article_url):
        return None
    body = c.clean_summary(hit.get("story_text") or "", 320)
    blob = f"{title} {body}"
    # Strict: only stage items that actually keyword-match a topic (no fallback),
    # so the HN firehose stays on-scope.
    domain = agg.classify_domain(blob, rules, [])
    if domain is None:
        return None
    published = (hit.get("created_at") or "")[:10] or None
    cand_id = c.make_id(title, c.normalize_url(article_url))
    return {
        "id": cand_id,
        # Label the origin honestly. Downstream (is_news_curated) uses this
        # to apply the HN-standalone points floor; treating HN as RSS made
        # that rule unreachable.
        "discovered_via": "hackernews",
        "title": title,
        "source_name": (
            f"@{hit.get('author')} via Hacker News" if hit.get("author") else "Hacker News"
        ),
        "source_type": "Hacker News",
        "source_url": article_url,
        "article_url": article_url,
        "tweet_url": None,
        "author": hit.get("author"),
        "published": published,
        "date": published[:7] if published else None,
        "excerpt": body
        or f"HN: {hit.get('points', 0)} points, {hit.get('num_comments', 0)} comments",
        "raw_path": None,
        "guess_topic": c.topic_for_domain(domain),
        "guess_domain": domain,
        "guess_subtype": agg.classify_subtype(blob, domain, rules),
        "source_id": None,
        "source_rank": HN_SOURCE_RANK,
        "source_topics": [],
        "hn_points": hit.get("points", 0),
        # Also under `signals` so the news gate (is_news_curated) can find
        # this without knowing HN-specific field names.
        "signals": {"hn_points": hit.get("points", 0)},
        "retrieved_at": c.utcnow_iso(),
    }


def collect(cfg: dict, rules: dict, per_query: int | None) -> list[dict]:
    hn_cfg = cfg.get("hackernews", {})
    queries = hn_cfg.get("queries", [])
    top_stories_enabled = bool(hn_cfg.get("top_stories", False))
    if not queries and not top_stories_enabled:
        print("   (no hackernews.queries and top_stories disabled in sources.yaml)")
        return []
    min_points = int(hn_cfg.get("min_points", 0))
    top_stories_min = int(hn_cfg.get("top_stories_min_points", 100))
    limit = per_query or hn_cfg.get("per_query", 8)
    top_limit = per_query or hn_cfg.get("top_stories_per_run", 30)
    max_age = c.load_config().max_age_days
    cutoff = datetime.now(UTC) - timedelta(days=max_age)
    since_ts = int(cutoff.timestamp())

    out: list[dict] = []
    seen_ids: set[str] = set()

    def _stage(hits, floor: int, label: str) -> None:
        kept = 0
        for hit in hits:
            if int(hit.get("points", 0) or 0) < floor:
                continue
            cand = hit_to_candidate(hit, rules)
            if not cand or cand["id"] in seen_ids:
                continue
            seen_ids.add(cand["id"])
            out.append(cand)
            kept += 1
        print(f"   ({label}: {kept} kept)")

    for query in queries:
        print(f"-> HN search: {query!r} (>= {min_points} pts, last {max_age}d)")
        _stage(search_stories(query, limit, since_ts, min_points), min_points, "keyword")

    if top_stories_enabled:
        print(f"-> HN top-stories tap (>= {top_stories_min} pts, last {max_age}d)")
        # Empty query + points floor via Algolia numericFilters. The
        # classifier inside hit_to_candidate still enforces topic scope,
        # so this stays on-scope even without a keyword.
        _stage(
            search_stories("", top_limit, since_ts, top_stories_min),
            top_stories_min,
            "top-stories",
        )

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max", type=int, default=None, help="override per-query limit")
    args = ap.parse_args()

    cfg = c.load_yaml(c.SOURCES_FILE)
    rules = cfg["classification"]
    candidates = collect(cfg, rules, args.max)
    print(f"\nFound {len(candidates)} HN candidate(s).")

    if args.dry_run:
        for cand in candidates:
            print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title']}")
        return 0

    added = c.add_candidates(candidates)
    print(f"Staged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
