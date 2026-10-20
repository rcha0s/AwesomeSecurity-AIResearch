#!/usr/bin/env python3
"""
replay_stories.py — Replay a window of pool history through the story matcher.

Builds a FRESH ledger in memory (the real data/news_stories.json is never
written) by feeding every pool + archive entry published in [--since, --until]
through the same path a scan uses, oldest first:

    shortlist (deterministic, over-matching)  ->  judge verdict  ->  apply

The judge is the scan's small model; a replay can't call it, so its verdicts
come from a recorded file (`--verdicts`, keyed by entry id). An entry with a
shortlist but no recorded verdict falls back to the conservative
deterministic rule (clear duplicate -> same, else new), so the replay only
merges what the deterministic rule or a recorded verdict says to.

`--tasks` prints the judge's input for every entry that has a shortlist, which
is how a verdict file is recorded. `--expect-one id,id,...` exits 1 unless all
those entries end up in one story (the ISC-21 probe).

Usage:
    python scripts/replay_stories.py --since 2026-07-01 --until 2026-08-31 \\
        --verdicts tests/fixtures/replay_2026-08_judge.json --expect-one <ids>
"""

from __future__ import annotations

import argparse
import json
import sys

import common as c
import story_ledger as sl


def window_entries(since: str, until: str) -> list[dict]:
    """Every pool + archive entry dated inside the window, one per id, oldest first."""
    seen: dict[str, dict] = {}
    for entry in sl.all_entries():
        day = sl.entry_day(entry)
        if entry.get("id") and since <= day <= until:
            seen.setdefault(entry["id"], entry)
    return sorted(seen.values(), key=lambda e: (sl.entry_day(e), e["id"]))


def judge_task(entry: dict, shortlist: list[dict]) -> dict:
    return {
        "candidate_id": entry["id"],
        "title": entry.get("title", ""),
        "source": entry.get("source_name") or entry.get("source_url", ""),
        "date": sl.entry_day(entry),
        "text": (entry.get("summary") or "")[:600],
        "shortlist": shortlist,
    }


def replay_one(ledger: dict, entry: dict, shortlist: list[dict], verdict: dict | None) -> str:
    """Route one entry; returns the action taken (new | same | update | fallback-*)."""
    if not shortlist:
        sl.create_story(ledger, entry)
        return "new"
    allowed = [row["story_id"] for row in shortlist]
    if verdict is None:
        sid = sl.find_clear_duplicate(ledger, entry, sl.DEFAULT_WINDOW_DAYS)
        if sid in allowed:
            sl.attach_entry(ledger, sid, entry)
            return "fallback-same"
        sl.create_story(ledger, entry)
        return "fallback-new"
    out = sl.apply_verdict(ledger, entry, verdict, allowed=allowed)
    if out["action"] in ("same", "update"):
        sl.attach_entry(ledger, out["story_id"], entry)  # the entry stays reachable
        return out["action"]
    sl.create_story(ledger, entry)
    return "new" if out["action"] == "new" else "rejected-new"


def replay(entries: list[dict], verdicts: dict[str, dict], window: int, k: int):
    """(ledger, {entry_id: action}, [judge tasks])."""
    ledger, actions, tasks = sl.empty_ledger(), {}, []
    by_id: dict[str, dict] = {}
    for entry in entries:
        shortlist = sl.shortlist_many([entry], ledger, by_id, window_days=window, k=k)[entry["id"]]
        if shortlist:
            tasks.append(judge_task(entry, shortlist))
        actions[entry["id"]] = replay_one(ledger, entry, shortlist, verdicts.get(entry["id"]))
        by_id[entry["id"]] = entry
    return ledger, actions, tasks


def report(ledger: dict, actions: dict[str, str], entries: list[dict]) -> list[str]:
    counts: dict[str, int] = {}
    for action in actions.values():
        counts[action] = counts.get(action, 0) + 1
    lines = [
        f"replayed {len(entries)} entries -> {len(ledger['stories'])} stories",
        "actions: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())),
    ]
    titles = {e["id"]: e.get("title", "") for e in entries}
    multi = [(sid, s) for sid, s in ledger["stories"].items() if len(s["entry_ids"]) > 1]
    lines.append(f"stories with more than one entry: {len(multi)}")
    for sid, story in multi:
        lines.append(
            f"- {sid} first seen {story['first_seen']}, last updated "
            f"{story['last_updated']}: {story['title'][:90]}"
        )
        for eid in story["entry_ids"]:
            lines.append(f"    [{actions.get(eid, '?')}] {eid}: {titles.get(eid, '')[:80]}")
        for upd in story["updates"]:
            lines.append(f"    Updated {upd['date']}: {upd['note'][:110]}")
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", required=True)
    ap.add_argument("--until", required=True)
    ap.add_argument("--verdicts", default=None, help="recorded judge verdicts (JSON list)")
    ap.add_argument("--tasks", action="store_true", help="print the judge tasks and stop")
    ap.add_argument("--expect-one", default="", help="comma-separated entry ids")
    args = ap.parse_args(argv)
    recorded = c.load_json(c.ROOT / args.verdicts, default=[]) if args.verdicts else []
    verdicts = {v["candidate_id"]: v for v in recorded}
    conf = sl.settings()
    entries = window_entries(args.since, args.until)
    ledger, actions, tasks = replay(
        entries, verdicts, conf["match_window_days"], conf["shortlist_max"]
    )
    if args.tasks:
        print(json.dumps(tasks, indent=2, ensure_ascii=False))
        return 0
    print("\n".join(report(ledger, actions, entries)))
    return expect_one(ledger, [i for i in args.expect_one.split(",") if i])


def expect_one(ledger: dict, ids: list[str]) -> int:
    if not ids:
        return 0
    index = sl.entry_index(ledger)
    stories = {index.get(i, f"missing:{i}") for i in ids}
    ok = len(stories) == 1 and not any(s.startswith("missing:") for s in stories)
    print(
        f"\nexpect-one: {len(ids)} entries -> {len(stories)} story(ies): "
        f"{'PASS' if ok else 'FAIL'} {sorted(stories)}"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
