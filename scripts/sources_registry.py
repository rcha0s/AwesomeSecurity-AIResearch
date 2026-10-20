#!/usr/bin/env python3
"""
sources_registry.py — The rankable registry of approved sources to scan.

A source is anything we harvest recurringly: an X account, a blog/RSS feed, a
GitHub user, a GitHub search query, a YouTube channel, or a newsletter. The
registry (data/sources.json) is the growing, committed list; `add_source.py`
appends to it and the ingestors read from it.

Ranking is hybrid and self-adjusting:
    rank = 0.50 * tier      (your manual authority call: high/medium/low)
         + 0.25 * signal    (followers / stars / subscribers, log-scaled)
         + 0.25 * hit_rate  (curated / ingested, Bayesian-smoothed)
So a source you trust starts high, a big account gets a bump, and every source
rises or falls over time by how many *curated* findings it actually yields.
"""

from __future__ import annotations

import math

import common as c

REGISTRY_FILE = c.DATA_DIR / "sources.json"
STATS_FILE = c.DATA_DIR / "source_stats.json"
STAT_KEYS = ("ingested", "curated")
MAX_STAT = 10**9  # far above any real count; bounds what a scan-written file can claim

SOURCE_TYPES = (
    "x_account",
    "rss",
    "github_user",
    "github_query",
    "youtube",
    "newsletter",
    "conference",
    "research_index",
    "kev_json",  # CISA Known Exploited Vulnerabilities JSON catalog
    "hf_papers",  # Hugging Face Daily Papers API (a paper quality signal)
)

# The three tracked topics (Pass 2 restructures the pools to match these).
TOPIC_SLUGS = ("ai-security", "product-security", "ai-research")

TIER_SCORE = {"high": 100, "medium": 60, "low": 30}
# Weights for the hybrid rank (sum to 1.0).
RANK_WEIGHTS = {"tier": 0.50, "signal": 0.25, "hit_rate": 0.25}
# Bayesian prior so a brand-new source starts at a neutral hit-rate (~50).
HITRATE_PRIOR_CURATED = 2
HITRATE_PRIOR_TOTAL = 4


def load_stats() -> dict[str, dict]:
    """Per-source hit-rate counts written by scans (data/source_stats.json).

    Kept apart from the registry so a scan PR never edits data/sources.json:
    the registry says WHAT gets fetched and changes only in reviewed PRs, while
    these counts may change on every scan (and can auto-merge)."""
    stats = c.load_json(STATS_FILE, default={}) or {}
    if not isinstance(stats, dict):
        return {}
    # Scan-written, so untrusted: an id whose counts aren't sane ints is ignored
    # (its registry baseline stands) rather than crashing every ingestor.
    return {sid: counts for sid, counts in stats.items() if _sane_counts(counts)}


def _sane_counts(counts: object) -> bool:
    if not isinstance(counts, dict):
        return False
    values = [counts.get(k, 0) for k in STAT_KEYS]
    return all(
        isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= MAX_STAT for v in values
    )


def load_sources() -> list[dict]:
    """The registry, with scan-written stats laid over it and ranks recomputed."""
    sources = c.load_json(REGISTRY_FILE, default=[]) or []
    stats = load_stats()
    for s in sources:
        counts = stats.get(s.get("id"))
        if counts is not None:
            s["stats"] = {k: counts.get(k, 0) for k in STAT_KEYS}
            s["rank"] = compute_rank(s)
    return sources


def save_sources(sources: list[dict]) -> None:
    c.save_json(REGISTRY_FILE, sources)


def source_id(stype: str, handle: str) -> str:
    return f"{stype}:{c.slugify(handle, 48)}"


def tier_score(tier: str) -> float:
    return TIER_SCORE.get((tier or "medium").lower(), 60)


def signal_score(source: dict) -> float:
    """Log-scaled 0-100 from the best available reach signal; 50 (neutral) if none.
    Reach is only ever a *bump*: a known-but-small following is floored at the
    neutral 50, never scored below an unknown source (log10 of a small count is
    tiny — a single follower would otherwise score 0, worse than 'no signal')."""
    sig = source.get("signals") or {}
    best = max([int(sig.get(k, 0) or 0) for k in ("followers", "stars", "subscribers")] or [0])
    if best <= 0:
        return 50.0
    return max(50.0, min(100.0, 20.0 * math.log10(best)))


def hit_rate_score(source: dict) -> float:
    stats = source.get("stats") or {}
    curated = int(stats.get("curated", 0) or 0)
    ingested = int(stats.get("ingested", 0) or 0)
    return 100.0 * ((curated + HITRATE_PRIOR_CURATED) / (ingested + HITRATE_PRIOR_TOTAL))


def compute_rank(source: dict) -> float:
    rank = (
        RANK_WEIGHTS["tier"] * tier_score(source.get("tier", "medium"))
        + RANK_WEIGHTS["signal"] * signal_score(source)
        + RANK_WEIGHTS["hit_rate"] * hit_rate_score(source)
    )
    return round(max(0.0, min(100.0, rank)), 1)


def new_source(
    stype: str,
    handle: str,
    *,
    name: str | None = None,
    url: str | None = None,
    topics: list[str] | None = None,
    domains: list[str] | None = None,
    tier: str = "medium",
    signals: dict | None = None,
    notes: str | None = None,
    strict: bool = False,
) -> dict:
    if stype not in SOURCE_TYPES:
        raise ValueError(f"unknown source type: {stype} (want one of {SOURCE_TYPES})")
    src = {
        "id": source_id(stype, handle),
        "type": stype,
        "handle": handle,
        "name": name or handle,
        "url": url,
        "topics": topics or [],
        # Legacy classifier domains (for aggregate.py's single-domain fallback).
        "domains": domains or [],
        # High-volume feed: only stage items that keyword-match a topic (no fallback).
        "strict": strict,
        "tier": (tier or "medium").lower(),
        "signals": signals or {},
        "stats": {"ingested": 0, "curated": 0},
        "rank": 0.0,
        "added": c.utcnow_iso()[:10],
        "active": True,
        "notes": notes,
    }
    src["rank"] = compute_rank(src)
    return src


def find_source(sources: list[dict], stype: str, handle: str) -> dict | None:
    sid = source_id(stype, handle)
    for s in sources:
        if s.get("id") == sid:
            return s
    return None


def add_source(source: dict) -> tuple[dict, bool]:
    """Append a source (or return the existing one). Returns (source, is_new)."""
    sources = load_sources()
    existing = find_source(sources, source["type"], source["handle"])
    if existing:
        return existing, False
    sources.append(source)
    save_sources(sources)
    return source, True


def sources_of_type(stype: str, active_only: bool = True) -> list[dict]:
    return [
        s
        for s in load_sources()
        if s.get("type") == stype and (s.get("active", True) or not active_only)
    ]


def get_by_id(sid: str) -> dict | None:
    for s in load_sources():
        if s.get("id") == sid:
            return s
    return None


def update_stats(source_id_map: dict[str, tuple[int, int]]) -> None:
    """Bulk-apply (ingested_delta, curated_delta) per source id.

    Writes only data/source_stats.json; ranks are recomputed when loaded."""
    if not source_id_map:
        return
    stats = load_stats()
    changed = False
    for s in load_sources():
        delta = source_id_map.get(s.get("id"))
        if not delta:
            continue
        base = s.get("stats") or {}
        stats[s["id"]] = {
            "ingested": int(base.get("ingested", 0) or 0) + delta[0],
            "curated": int(base.get("curated", 0) or 0) + delta[1],
        }
        changed = True
    if changed:
        c.save_json(STATS_FILE, dict(sorted(stats.items())))
