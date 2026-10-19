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

import json
import subprocess
import sys

import common as c


def main_pool_ids(topic: str) -> set[str]:
    rel = c.POOL_FILES[topic].relative_to(c.ROOT).as_posix()
    out = subprocess.run(
        ["git", "show", f"origin/main:{rel}"], cwd=c.ROOT, capture_output=True, text=True
    )
    if out.returncode != 0:  # a pool new on this branch: nothing on main yet
        return set()
    return {e.get("id") for e in json.loads(out.stdout).get("entries", [])}


def new_entries() -> int:
    count = 0
    for topic in c.TOPICS:
        before = main_pool_ids(topic)
        count += sum(1 for e in c.load_pool(topic)["entries"] if e.get("id") not in before)
    return count


def analysis_count() -> int:
    data = c.load_json(c.ANALYSIS_OUT, default=[]) or []
    return len(data if isinstance(data, list) else data.get("entries", []))


def main() -> int:
    print(max(new_entries(), analysis_count()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
