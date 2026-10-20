#!/usr/bin/env python3
"""
rerank.py — Deterministic (re)ranking of the research pools.

Recomputes time-decayed newness for every entry, folds it with the LLM-provided
novelty/relevance into a weighted composite, and re-sorts each pool. This is
cheap (no LLM) and runs after every ingest/merge and in CI, so ordering stays
fresh as findings age and as new ones arrive.

Every pass also normalizes `domain` to a taxonomy ID (pool and archive), with the
same rules as scripts/migrate_taxonomy.py, so a branch carrying pre-taxonomy
pool data converges the next time it re-renders.

Usage:
    python scripts/rerank.py            # rerank both pools in place
    python scripts/rerank.py --track ai
"""

from __future__ import annotations

import argparse

import common as c
import taxonomy as tx


def score_entry(entry: dict, conf: c.Config, now=None) -> dict:
    """Return a new entry with refreshed scores.{newness,composite,scored_at}."""
    scores = dict(entry.get("scores") or {})
    scores["newness"] = c.newness_score(entry.get("date") or "", conf.half_life_days, now=now)
    scores.setdefault("novelty", 0)
    scores.setdefault("relevance", 0)
    scores["credibility"] = c.credibility_of(entry)  # from the source registry rank
    scores["composite"] = c.composite_score(scores, conf.weights)
    scores["scored_at"] = c.utcnow_iso()
    return {**entry, "scores": scores}


def sort_key(entry: dict) -> tuple:
    scores = entry.get("scores") or {}
    return (-float(scores.get("composite", 0)), entry.get("date") or "", entry.get("title", ""))


def prune_stale(
    entries: list[dict], conf: c.Config, now=None, keep=lambda e: False
) -> tuple[list[dict], list[dict]]:
    """Split entries into (fresh, stale) by the hard freshness window.

    `keep` exempts entries that never age out (news stories, like claims)."""
    fresh, stale = [], []
    for e in entries:
        (fresh if keep(e) or c.is_fresh(e, conf.max_age_days, now=now) else stale).append(e)
    return fresh, stale


def rerank_pool(track: str, conf: c.Config | None = None, now=None) -> dict:
    conf = conf or c.load_config()
    pool = c.load_pool(track)
    sources = c.load_sources_by_id()

    def is_news(e: dict) -> bool:
        return c.is_news_story(e, conf, sources)

    live = {e.get("id") for e in pool["entries"]}
    restored = c.unarchive(lambda e: e.get("topic") == track and is_news(e))
    pool["entries"] += [e for e in restored if e.get("id") not in live]
    if restored:
        print(f"  restored {len(restored)} archived news stories to {track}")
    migrated = tx.normalize_entries(pool["entries"], tx.get(), tx.load_overrides())
    if migrated:
        print(f"  normalized {migrated} free-text domain(s) in {track} to taxonomy IDs")
    pool["domains"] = c.TOPICS[track]["domains"]
    fresh, stale = prune_stale(pool["entries"], conf, now=now, keep=is_news)
    archived = c.archive_entries(stale)
    if stale:
        print(f"  pruned {len(stale)} stale from {track} (archived {archived})")
    pool["entries"] = sorted((score_entry(e, conf, now=now) for e in fresh), key=sort_key)
    c.save_pool(track, pool)
    return pool


def normalize_archive() -> int:
    """Give archived entries taxonomy IDs too (rewrites the file only on change)."""
    archive = c.load_json(c.ARCHIVE_FILE, default=[]) or []
    changed = tx.normalize_entries(archive, tx.get(), tx.load_overrides())
    if changed:
        c.save_json(c.ARCHIVE_FILE, archive)
        print(f"  normalized {changed} free-text domain(s) in the archive")
    return changed


def rerank_all(conf: c.Config | None = None, now=None) -> None:
    conf = conf or c.load_config()
    normalize_archive()
    for track in c.TOPICS:
        pool = rerank_pool(track, conf, now=now)
        print(f"reranked {track}: {len(pool['entries'])} entries")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", choices=list(c.TOPICS), default=None)
    args = ap.parse_args()
    if args.topic:
        rerank_pool(args.topic)
    else:
        rerank_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
