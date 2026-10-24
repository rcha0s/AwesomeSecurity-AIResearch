#!/usr/bin/env python3
"""
rerank.py — Deterministic (re)ranking of the research pools.

Recomputes time-decayed newness for every entry, folds it with the LLM-provided
novelty/relevance into a weighted composite, and re-sorts each pool. This is
cheap (no LLM) and runs after every ingest/merge and in CI, so ordering stays
fresh as findings age and as new ones arrive.

Every pass also normalizes `domain` to a taxonomy ID (pool and archive), with the
same rules as scripts/migrate_taxonomy.py, so a branch carrying pre-taxonomy
pool data converges the next time it re-renders. Every pass also ledgers any
pool or archive entry the story ledger (story_ledger.py) has not seen yet.

Usage:
    python scripts/rerank.py            # rerank both pools in place
    python scripts/rerank.py --track ai
"""

from __future__ import annotations

import argparse

import common as c
import readability as rd
import story_ledger as sl
import taxonomy as tx


def score_entry(entry: dict, conf: c.Config, now=None) -> dict:
    """Return a new entry with refreshed scores.{newness,composite,scored_at}.

    `scored_at` is when the scores last CHANGED, not when the last pass ran: if a
    re-score leaves every axis as it was, the old stamp is kept, so a pure
    re-render is byte-identical and the render job opens no PR."""
    old = entry.get("scores") or {}
    scores = dict(old)
    scores["newness"] = c.newness_score(entry.get("date") or "", conf.half_life_days, now=now)
    scores.setdefault("novelty", 0)
    scores.setdefault("relevance", 0)
    scores["credibility"] = c.credibility_of(entry)  # from the source registry rank
    scores["composite"] = c.composite_score(scores, conf.weights)
    unchanged = old.get("scored_at") and all(
        scores.get(k) == old.get(k) for k in set(scores) | set(old) if k != "scored_at"
    )
    scores["scored_at"] = old["scored_at"] if unchanged else c.utcnow_iso()
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


def kept_for(is_news):
    """What the prune never archives: news stories, and in a backfill scan
    (issue #52) the entries this run merged (not on origin/main), so they are
    not archived on arrival. Scores stay on the wall clock, so the live ranking
    is untouched. The next normal rerank (the next daily scan, or update.yml on
    main) archives backfilled findings past max_age_days, still vetted; news
    stays."""
    if c.backfill_window() is None:
        return is_news
    on_main = c.main_entry_ids()
    return lambda e: is_news(e) or e.get("id") not in on_main


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
    fresh, stale = prune_stale(pool["entries"], conf, now=now, keep=kept_for(is_news))
    archived = c.archive_entries(stale)
    if stale:
        print(f"  pruned {len(stale)} stale from {track} (archived {archived})")
    released = release_holds(fresh)
    if released:
        print(f"  released {released} readability hold(s) the current config no longer supports")
    pool["entries"] = sorted((score_entry(e, conf, now=now) for e in fresh), key=sort_key)
    c.save_pool(track, pool)
    return pool


def release_holds(entries: list[dict]) -> int:
    """Re-judge every readability hold under the current config (tuning a
    threshold releases what it no longer supports; rerank never adds a hold)."""
    cfg = rd.settings()
    return sum(rd.release(e, cfg) for e in entries)


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
    merges = sl.sync_and_save()  # the story ledger never prunes; it only grows
    if merges:
        print(f"  story ledger: {len(merges)} entr(y/ies) joined an existing story")


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
