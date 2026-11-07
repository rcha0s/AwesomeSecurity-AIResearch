"""Tests for scripts/watchdog.py: it reports a day with no finished scan and a stuck scan PR."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import watchdog as wd

NOW = datetime(2026, 11, 7, 23, 30, tzinfo=UTC)


def run(kind, date="2026-11-07", **more):
    return {"run_id": "r", "date": date, "runner": "local", "kind": kind, **more}


def pr(number, created, ref="claude/scan-2026-11-04-local"):
    return {"number": number, "created_at": created, "head": {"ref": ref}}


def test_a_day_with_only_a_killed_reservation_is_reported():
    # 11-06: reserved, then killed in aggregate; no done row
    assert wd.problems([run("reserve")], [], NOW, True, 8) == ["no-finished-scan"]


def test_a_finished_day_is_quiet_and_a_backfill_does_not_count():
    assert wd.problems([run("reserve"), run("done")], [], NOW, True, 8) == []
    backfill = run("done", backfill="2026-10-01..2026-10-05")
    assert wd.problems([backfill], [], NOW, True, 8) == ["no-finished-scan"]


def test_yesterdays_scan_does_not_cover_today_and_a_paused_budget_is_quiet():
    assert wd.no_finished_scan([run("done", date="2026-11-06")], "2026-11-07", True)
    assert not wd.no_finished_scan([], "2026-11-07", cap_set=False)


def test_only_scan_prs_open_past_the_limit_are_stuck():
    prs = [
        pr(165, "2026-11-04T21:59:00Z"),  # three days: #165
        pr(170, "2026-11-07T20:00:00Z"),  # 3.5 hours: still normal
        pr(160, "2026-11-01T11:42:00Z", ref="chore/source-proposals"),  # not a scan PR
    ]
    assert wd.stuck_prs(prs, NOW, 8) == [165]


def test_cli_prints_one_phase_per_line(tmp_path, capsys):
    (tmp_path / "l.json").write_text(json.dumps({"runs": [run("reserve")]}))
    (tmp_path / "p.json").write_text(json.dumps([pr(165, "2026-11-04T21:59:00Z")]))
    argv = ["--ledger", str(tmp_path / "l.json"), "--prs", str(tmp_path / "p.json")]
    assert wd.main([*argv, "--now", NOW.isoformat()]) == 0
    assert capsys.readouterr().out.split() == ["no-finished-scan", "stuck-pr-165"]
