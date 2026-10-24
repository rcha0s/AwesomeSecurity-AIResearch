#!/usr/bin/env python3
"""
scan_count.py — How many stories this scan analyzed, and whether it did any work.

`post` can't trust data/analysis_out.json alone: the model runs
merge_analysis.py itself and could merge several capped batches before `post`
sees only the last one. The count is the larger of analysis_out.json's length
and the pool entries absent from origin/main's pools AND archive. The archive
matters: rerank pulls archived news stories back into the pools, and those are
main's own entries, not this run's analysis (the 2026-10-20 run analyzed
nothing, yet counted the 19 it restored).

`--work` exits 3 when the session produced nothing to ship: no entry that
merge_analysis.py merged and no `same`/`update` story verdict it applied. Both
come from its code-owned records (data/_merge_outcomes.json and
data/_story_outcomes.md), never from the model's analysis_out.json. `post`
fails such a run.

Two tiers (select_batch.py): deep analyses count as stories, against
`limits.max_stories_per_run`; news briefs (`news_brief` on a pool entry,
`brief: "news"` in analysis_out.json) count separately, against
`limits.max_news_per_run`. A brief is never a story, and a story never a brief.

Usage:
    python scripts/scan_count.py          # print the (deep) story count
    python scripts/scan_count.py --news   # print the news-brief count
    python scripts/scan_count.py --work   # print the counts; exit 3 if no work
"""

from __future__ import annotations

import json
import subprocess
import sys

import common as c
import story_ledger as sl

NO_WORK = 3  # distinct from a crash's exit 1


def main_archive_ids() -> set[str]:
    """Ids of every archived entry on origin/main ({} if main has no archive)."""
    rel = c.ARCHIVE_FILE.relative_to(c.ROOT).as_posix()
    out = subprocess.run(
        ["git", "show", f"origin/main:{rel}"], cwd=c.ROOT, capture_output=True, text=True
    )
    if out.returncode != 0:
        return set()
    data = json.loads(out.stdout)
    entries = data if isinstance(data, list) else data.get("entries", [])
    return {e.get("id") for e in entries if isinstance(e, dict)}


def new_entries(news: bool = False) -> int:
    """Pool entries absent from main's pools and archive: deep ones, or (news)
    the news briefs."""
    on_main = c.main_entry_ids() | main_archive_ids()
    return sum(
        1
        for topic in c.TOPICS
        for e in c.load_pool(topic)["entries"]
        if e.get("id") not in on_main and c.is_news_brief(e) == news
    )


def analysis_count(news: bool = False) -> int:
    data = c.load_json(c.ANALYSIS_OUT, default=[]) or []
    rows = data if isinstance(data, list) else data.get("entries", [])
    return sum(1 for e in rows if isinstance(e, dict) and is_brief(e) == news)


def is_brief(row: dict) -> bool:
    return row.get("brief") == c.NEWS_BRIEF or c.is_news_brief(row)


def settled_verdicts() -> int:
    path = c.DATA_DIR / sl.OUTCOMES_FILE.name
    return sl.settled_count(path.read_text(encoding="utf-8")) if path.exists() else 0


def counts() -> tuple[int, int]:
    """(deep stories, news briefs) this run produced."""
    return (
        max(new_entries(), analysis_count()),
        max(new_entries(news=True), analysis_count(news=True)),
    )


def main(argv: list[str]) -> int:
    stories, briefs = counts()
    if argv == ["--work"]:
        merged, settled = c.merge_record()["merged"], settled_verdicts()
        print(f"analyzed={stories} news_briefs={briefs} merged={merged} settled_verdicts={settled}")
        return 0 if merged or settled else NO_WORK
    print(briefs if argv == ["--news"] else stories)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
