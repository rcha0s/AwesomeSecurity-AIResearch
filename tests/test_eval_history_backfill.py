"""Backfill rows in data/evals/history.json (issue #52): marked, kept out of the
7-run gate and its trend table, and the mark is checked against the ledger so it
can neither make nor break the gate."""

from __future__ import annotations

import argparse

import content_checks as cc
import eval_history as eh
import pytest
from test_eval_forgery import RESERVE, check, new_row, pr
from test_eval_history import CFG, row

WIN = "2026-09-09..2026-09-16"


def bf(i: int, **over) -> dict:
    return row(i, backfill=WIN, run_id=f"b{i}", **over)


def test_a_failing_backfill_row_cannot_break_the_gate():
    rows = [row(i) for i in range(7)]
    rows.insert(3, bf(3, integrity={"passed": False, "problems": 4}, recall=None))
    result = eh.gate(rows, CFG)
    assert result["passed"] and result["streak"] == 7 and result["runs"] == 7
    assert all(not r["run_id"].startswith("b") for r in result["window"])


def test_passing_backfill_rows_cannot_make_the_gate():
    rows = [row(i) for i in range(5)] + [bf(i) for i in range(5, 10)]
    result = eh.gate(rows, CFG)
    assert not result["passed"] and result["runs"] == 5


def test_a_newest_backfill_row_does_not_reset_the_streak():
    rows = [row(i) for i in range(7)] + [bf(7, cost_usd=99.0)]
    assert eh.gate(rows, CFG)["streak"] == 7


def test_the_trend_table_skips_backfill_rows_and_lists_them_apart():
    rows = [row(i) for i in range(3)] + [bf(3, stories=9, kept=4)]
    text = eh.body(rows, "b3", CFG)
    table = [line for line in text.splitlines() if line.startswith("| 2026")]
    assert len(table) == 3  # the daily runs only
    assert f"Backfill {WIN}: not counted in the gate." in text
    assert f"**Backfill runs** (not in the gate): {WIN} (9 stories, 4 kept, $3.55)" in text
    assert "Backfill runs" not in eh.body([row(i) for i in range(3)], "r2", CFG)


def test_append_marks_the_row(monkeypatch, sandbox):
    monkeypatch.setattr(eh.eval_integrity, "run", lambda: {"passed": True, "problems": []})
    args = argparse.Namespace(config=eh.c.CONFIG_FILE, run_id="b1", runner="local", stories=2,
                              candidates=9, ledger=None, recall=None, backfill=WIN)  # fmt: skip
    assert eh.build_row(args)["backfill"] == WIN
    assert "backfill" not in eh.build_row(argparse.Namespace(**{**vars(args), "backfill": None}))


# --- merge_gate: the mark must be its reservation's ------------------------------------
BF_RESERVE = {**RESERVE, "backfill": WIN}


def test_an_honest_backfill_row_passes():
    assert check(pr(new_row(backfill=WIN)), ledger=(BF_RESERVE,)) == []


def test_a_daily_row_cannot_claim_a_backfill_mark_to_leave_the_gate():
    problems = check(pr(new_row(backfill=WIN)))  # its reservation is a daily one
    assert problems == ["history: run C9's backfill mark is not its reservation's"]


def test_a_backfill_row_cannot_drop_its_mark_to_join_the_gate():
    problems = check(pr(new_row()), ledger=(BF_RESERVE,))
    assert problems == ["history: run C9's backfill mark is not its reservation's"]


@pytest.mark.parametrize("mark", ["2026-09-09", "<b>x</b>", 7, True, "", WIN + "\n"])
def test_a_malformed_mark_is_refused(mark):
    problems = check(pr(new_row(backfill=mark)), ledger=({**RESERVE, "backfill": mark},))
    assert problems == ["history: run C9's backfill mark is not a FROM..TO window"]


def test_the_window_pattern_is_anchored():
    assert cc.BACKFILL_WINDOW.match(WIN)
    assert not cc.BACKFILL_WINDOW.match(WIN + "\n| x |")
