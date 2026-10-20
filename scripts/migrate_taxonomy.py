#!/usr/bin/env python3
"""
migrate_taxonomy.py — give every pool and archive entry a taxonomy domain ID.

The one-time migration off free-text `domain` labels (ISC-17). The decisions
live in `data/taxonomy_migration.json` (every pre-migration label → ID, plus
per-entry overrides where a label was ambiguous); this script applies them.
Idempotent: an entry that already carries a valid ID is never touched, so a
second run changes nothing. `rerank.py` runs the same normalization on every
pass, so a branch with older pool data converges when it re-renders.

Usage:
    python scripts/migrate_taxonomy.py           # rewrite the pools + archive
    python scripts/migrate_taxonomy.py --check   # exit 1 if anything would change
"""

from __future__ import annotations

import argparse
import copy

import common as c
import taxonomy as tx


def migrate_pools(tax: tx.Taxonomy, overrides: dict[str, str], write: bool) -> dict[str, int]:
    """Normalize each pool's entries and its header's domain list (a stale
    header counts as one change). Returns changes per pool."""
    changed: dict[str, int] = {}
    for topic in c.TOPICS:
        pool = c.load_pool(topic)
        ids = [d.id for d in tax.for_topic(topic)]
        entries = copy.deepcopy(pool["entries"])
        changed[topic] = tx.normalize_entries(entries, tax, overrides)
        changed[topic] += int(pool.get("domains") != ids)
        if write and changed[topic]:
            c.save_pool(topic, {**pool, "domains": ids, "entries": entries})
    return changed


def migrate_archive(tax: tx.Taxonomy, overrides: dict[str, str], write: bool) -> int:
    archive = c.load_json(c.ARCHIVE_FILE, default=[]) or []
    n = tx.normalize_entries(archive, tax, overrides)
    if write and n:
        c.save_json(c.ARCHIVE_FILE, archive)
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only; exit 1 on pending changes")
    args = ap.parse_args(argv)
    tax, overrides = tx.get(), tx.load_overrides()
    changed = migrate_pools(tax, overrides, write=not args.check)
    changed["archive"] = migrate_archive(tax, overrides, write=not args.check)
    for name, n in changed.items():
        print(f"  {name}: {n} change(s) {'pending' if args.check else 'written'}")
    return 1 if args.check and any(changed.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
