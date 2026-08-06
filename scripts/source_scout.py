#!/usr/bin/env python3
"""
source_scout.py — Discover trending stories from unindexed publishers and
propose the ones worth adding to data/sources.json.

Loop shape (see also the PR-7 design in the project notes):

  1. Trending signal: pull recent high-scoring HN stories that pass the
     shared topic classifier. (Reddit / Google News / X are drop-in
     extensions later — same interface: return a list of (title, url,
     signal) tuples.)

  2. For each trending story, extract the publisher domain. Skip if the
     publisher is already in sources.json or on the blocklist.

  3. For each candidate publisher, run a back-catalog check: fetch its
     RSS/Atom feed if discoverable, run every recent article's title +
     summary through the shared classifier + news deny list. Publisher
     qualifies if >= HIT_RATE_THRESHOLD of recent items clear both.

  4. Write proposals to data/source_proposals.json. The workflow opens
     a PR against main; a human merges (or ignores + optionally adds
     to blocklist).

Idempotent. Runs headless (no auth beyond HN Algolia's keyless API +
public RSS fetches).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import aggregate as agg  # noqa: E402
import common as c  # noqa: E402

SOURCES = ROOT / "data" / "sources.json"
BLOCKLIST = ROOT / "data" / "source_blocklist.json"
PROPOSALS = ROOT / "data" / "source_proposals.json"

# Publisher qualifies if >= this fraction of its recent articles pass our
# classifier + news deny list. Chosen for the ~40% threshold discussed in
# the design; tune down as scout gains history to compare against.
HIT_RATE_THRESHOLD = 0.4
# How many recent items to sample from a publisher's feed for the check.
BACK_CATALOG_SAMPLE = 25
# HN top-of-window trending threshold; matches the news lane's standalone
# points floor for consistency.
HN_TRENDING_POINTS = 100
HN_WINDOW_DAYS = 3

# Big-media hosts we never want as ingestion sources, even if they trend
# once. Prevents the scout from proposing Bloomberg for a spot AI story.
_PERMANENT_BLOCK_HOSTS = frozenset({
    "bloomberg.com", "cnbc.com", "reuters.com", "wsj.com",
    "ft.com", "nytimes.com", "washingtonpost.com",
    "businessinsider.com", "forbes.com",
})


# ---------------------------------------------------------------------------
# Signals: pull trending stories from HN
# ---------------------------------------------------------------------------
def _hn_trending() -> list[dict]:
    """Return recent high-scoring HN stories with (title, url, points)."""
    import requests

    cutoff = int((datetime.now(UTC) - timedelta(days=HN_WINDOW_DAYS)).timestamp())
    params = {
        "tags": "story",
        "numericFilters": f"created_at_i>={cutoff},points>={HN_TRENDING_POINTS}",
        "hitsPerPage": "50",
    }
    try:
        r = requests.get(
            "http://hn.algolia.com/api/v1/search_by_date",
            params=params, timeout=30,
            headers={"User-Agent": "SourceScout/1.0"},
        )
        r.raise_for_status()
        hits = r.json().get("hits", []) or []
    except Exception as exc:  # noqa: BLE001
        print(f"HN trending fetch failed: {exc}", file=sys.stderr)
        return []
    out = []
    for h in hits:
        url = (h.get("url") or "").strip()
        title = (h.get("title") or "").strip()
        if not url or not title:
            continue
        out.append({
            "title": title,
            "url": url,
            "points": int(h.get("points") or 0),
            "signal": "hackernews",
        })
    return out


# ---------------------------------------------------------------------------
# Publisher-level qualification
# ---------------------------------------------------------------------------
def _host(url: str) -> str:
    try:
        h = urlparse(url).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except (ValueError, TypeError):
        return ""


def _discover_feed(host: str) -> str | None:
    """Try well-known feed paths for a host. Returns the first one that
    responds 200 with an XML content-type-ish body."""
    import requests

    for path in ("/feed", "/feed.xml", "/rss", "/rss.xml", "/atom.xml", "/index.xml"):
        url = f"https://{host}{path}"
        try:
            r = requests.get(url, timeout=15,
                             headers={"User-Agent": "SourceScout/1.0"})
            if r.status_code != 200:
                continue
            ct = (r.headers.get("Content-Type") or "").lower()
            body = r.text[:512].lower()
            if "xml" in ct or "<rss" in body or "<feed" in body:
                return url
        except Exception:  # noqa: BLE001
            continue
    return None


def _classifier_hit_rate(feed_url: str, rules: dict) -> tuple[int, int]:
    """Fetch the feed, classify each recent item, return (hits, total)."""
    import feedparser

    try:
        parsed = feedparser.parse(feed_url)
    except Exception as exc:  # noqa: BLE001
        print(f"  feedparser error {feed_url}: {exc}", file=sys.stderr)
        return 0, 0

    entries = list(parsed.entries or [])[:BACK_CATALOG_SAMPLE]
    total = 0
    hits = 0
    for entry in entries:
        title = (entry.get("title") or "").strip()
        summary = c.clean_summary(entry.get("summary") or "", 320)
        if not title:
            continue
        total += 1
        blob = f"{title} {summary}"
        # Same classifier the pool uses; strict on-topic.
        if agg.classify_domain(blob, rules, []) is None:
            continue
        # And the news deny list — puff-only feeds get filtered.
        pseudo = {"title": title, "summary": summary, "takeaway": ""}
        if c.news_denylist_hit(pseudo):
            continue
        hits += 1
    return hits, total


# ---------------------------------------------------------------------------
# Blocklist + registry lookup
# ---------------------------------------------------------------------------
@dataclass
class Context:
    sources: list[dict]
    blocklist: list[dict]
    rules: dict
    known_hosts: set[str] = field(default_factory=set)
    blocked_hosts: set[str] = field(default_factory=set)

    def already_registered(self, host: str) -> bool:
        return host in self.known_hosts

    def blocked(self, host: str) -> bool:
        return host in self.blocked_hosts or host in _PERMANENT_BLOCK_HOSTS


def _load(p: Path, default):
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _save(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _ctx() -> Context:
    sources = _load(SOURCES, [])
    blocklist = _load(BLOCKLIST, [])
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    known: set[str] = set()
    for s in sources:
        host = _host(s.get("url") or s.get("handle") or "")
        if host:
            known.add(host)
    blocked = {b.get("domain") for b in blocklist if b.get("domain")}
    return Context(sources=sources, blocklist=blocklist, rules=rules,
                   known_hosts=known, blocked_hosts=blocked)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def _propose(ctx: Context, story: dict) -> dict | None:
    """Given one trending story, decide if its publisher is a candidate
    source. Returns a proposal dict or None."""
    host = _host(story["url"])
    if not host:
        return None
    if ctx.already_registered(host):
        return None
    if ctx.blocked(host):
        return None

    feed_url = _discover_feed(host)
    if not feed_url:
        return {
            "domain": host,
            "surfaced_by": story["signal"],
            "trending_story": {"title": story["title"], "url": story["url"],
                               "points": story.get("points")},
            "status": "skipped",
            "reason": "No RSS/Atom feed discoverable via well-known paths.",
        }

    hits, total = _classifier_hit_rate(feed_url, ctx.rules)
    if total == 0:
        return {
            "domain": host,
            "surfaced_by": story["signal"],
            "trending_story": {"title": story["title"], "url": story["url"]},
            "feed_url": feed_url,
            "status": "skipped",
            "reason": "Feed had 0 usable entries in back-catalog sample.",
        }

    rate = hits / total
    if rate < HIT_RATE_THRESHOLD:
        return {
            "domain": host,
            "surfaced_by": story["signal"],
            "trending_story": {"title": story["title"], "url": story["url"]},
            "feed_url": feed_url,
            "hit_rate": round(rate, 3),
            "hits": hits, "sampled": total,
            "status": "skipped",
            "reason": (
                f"Back-catalog hit-rate {rate:.0%} < threshold "
                f"{HIT_RATE_THRESHOLD:.0%}."
            ),
        }

    return {
        "domain": host,
        "surfaced_by": story["signal"],
        "trending_story": {"title": story["title"], "url": story["url"],
                           "points": story.get("points")},
        "feed_url": feed_url,
        "hit_rate": round(rate, 3),
        "hits": hits, "sampled": total,
        "status": "proposed",
        "suggested_tier": "medium",   # scout never proposes high on its own
        "suggested_track": "news",
        "suggested_scope": "both",
    }


def scout(ctx: Context, trending: list[dict]) -> dict:
    """Given a fresh Context and a list of trending stories, return a
    proposals doc. Deterministic — same input → same output."""
    proposals: list[dict] = []
    considered_domains: set[str] = set()
    for story in trending:
        host = _host(story["url"])
        if not host or host in considered_domains:
            continue
        considered_domains.add(host)
        p = _propose(ctx, story)
        if p is not None:
            proposals.append(p)

    proposed = [p for p in proposals if p["status"] == "proposed"]
    skipped = [p for p in proposals if p["status"] == "skipped"]

    return {
        "generated": datetime.now(UTC).strftime("%Y-%m-%d"),
        "proposed": proposed,
        "skipped": skipped,
        "summary": {
            "trending_stories": len(trending),
            "candidate_domains": len(considered_domains),
            "proposed": len(proposed),
            "skipped": len(skipped),
        },
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the proposals doc; do not write.")
    ap.add_argument("--offline", action="store_true",
                    help="Skip network calls (for tests).")
    args = ap.parse_args(argv)

    ctx = _ctx()
    trending = [] if args.offline else _hn_trending()
    doc = scout(ctx, trending)

    print(f"trending stories: {doc['summary']['trending_stories']}")
    print(f"candidate domains: {doc['summary']['candidate_domains']}")
    print(f"proposed: {doc['summary']['proposed']}")
    print(f"skipped: {doc['summary']['skipped']}")

    if args.dry_run:
        print(json.dumps(doc, indent=2))
        return 0

    _save(PROPOSALS, doc)
    print(f"wrote {PROPOSALS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
