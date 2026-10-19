#!/usr/bin/env python3
"""
scan_count.py — How many stories this scan added, for the per-run cap.

`post` can't trust data/analysis_out.json alone: the model runs
merge_analysis.py itself and could merge several capped batches before `post`
sees only the last one. This counts pool entries whose id isn't in
origin/main's pools, and prints the larger of that and analysis_out.json's
length.

Usage:
    python scripts/scan_count.py
"""

from __future__ import annotations

import sys

import common as c


def new_entries() -> int:
    on_main = c.main_entry_ids()
    return sum(
        1 for topic in c.TOPICS for e in c.load_pool(topic)["entries"] if e.get("id") not in on_main
    )


def analysis_count() -> int:
    data = c.load_json(c.ANALYSIS_OUT, default=[]) or []
    return len(data if isinstance(data, list) else data.get("entries", []))


def main() -> int:
    print(max(new_entries(), analysis_count()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
