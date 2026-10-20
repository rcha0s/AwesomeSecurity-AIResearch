"""A scan PR must not be able to forge the Phase 3 gate (ISC-26 / ISC-28).

content_checks.history_problems + merge_gate.history_check are what stop it:
main's history rows are an exact prefix, at most one row is new, and that row's
ledger charge, integrity, golden result and cap are re-derived, not trusted.
merge_guard keeps every other data/evals/ file out of scan PRs.
"""

from __future__ import annotations

import copy
import json

import content_checks as cc
import merge_gate
import merge_guard
import pytest

GOLDEN = {"score": 0.95, "off_topic_rate": 0.0, "cases": 8,
          "generated": "2026-07-14T00:00:00+00:00", "file": "golden-2026-07-14.json"}  # fmt: skip
RESERVE = {"run_id": "C9", "date": "2026-07-15", "runner": "cloud", "kind": "reserve",
           "stories": 0, "cost_usd": 3.554}  # fmt: skip
RECOMPUTED = {"integrity": True, "golden": {**GOLDEN, "stale": False}, "cap_usd": 3.3333}


def old_row(i: int, passed: bool = True) -> dict:
    return {"run_id": f"r{i}", "date": f"2026-07-0{i + 1}", "integrity": {"passed": passed}}


MAIN = {"runs": [old_row(0), old_row(1, passed=False), old_row(2)]}


def new_row(**over) -> dict:
    row = {
        "run_id": "C9", "date": "2026-07-15", "runner": "cloud",
        "integrity": {"passed": True, "problems": 0}, "golden": {**GOLDEN, "stale": False},
        "cost_usd": 3.554, "cost_basis": "reserved", "ceiling_usd": 3.554, "cap_usd": 3.3333,
    }  # fmt: skip
    row.update(over)
    return row


def pr(*rows, base=MAIN) -> dict:
    return {"runs": copy.deepcopy(base["runs"]) + list(rows)}


def check(pr_history, ledger=(RESERVE,), recomputed=RECOMPUTED) -> list[str]:
    return cc.history_problems(MAIN, pr_history, list(ledger), recomputed)


def test_an_honest_row_passes():
    assert check(pr(new_row())) == []
    assert check(copy.deepcopy(MAIN)) == []  # no new row is fine too
    actual = {**RESERVE, "kind": "actual", "cost_usd": 1.2}
    measured = new_row(cost_usd=1.2, cost_basis="measured")
    assert check(pr(measured), ledger=(RESERVE, actual)) == []


def test_rewriting_or_deleting_main_rows_fails():
    rewritten = pr(new_row())
    rewritten["runs"][1]["integrity"]["passed"] = True  # whitewash a failing run
    assert check(rewritten) == ["history: rows on main were rewritten or removed"]
    deleted = {"runs": [MAIN["runs"][0], MAIN["runs"][2], new_row()]}  # drop the failure
    assert check(deleted) == ["history: rows on main were rewritten or removed"]
    assert check({"runs": []}) == ["history: rows on main were rewritten or removed"]


def test_more_than_one_new_row_fails():
    second = new_row(run_id="C10")
    assert check(pr(new_row(), second)) == ["history: 2 new rows; a scan adds at most one"]


@pytest.mark.parametrize(
    "over,ledger,needle",
    [
        ({"run_id": "invented"}, (RESERVE,), "has no reservation on the budget ledger"),
        ({}, (), "has no reservation on the budget ledger"),
        ({"runner": "local"}, (RESERVE,), "runner/date disagree"),
        ({"date": "2026-07-16"}, (RESERVE,), "runner/date disagree"),
        ({"cost_usd": 0.5}, (RESERVE,), "cost is not a reserved charge"),
        ({"cost_usd": 0.5, "cost_basis": "measured"}, (RESERVE,), "cost is not a measured charge"),
        ({"ceiling_usd": 99.0}, (RESERVE,), "ceiling is not its reservation"),
        ({"integrity": {"passed": False}}, (RESERVE,), "integrity disagrees"),
        ({"golden": {**GOLDEN, "score": 1.0}}, (RESERVE,), "golden result is not the newest"),
        ({"golden": None}, (RESERVE,), "golden result is not the newest"),
        ({"cap_usd": 99.0}, (RESERVE,), "per-run cap is not main's"),
    ],
)
def test_a_forged_new_row_fails(over, ledger, needle):
    problems = check(pr(new_row(**over)), ledger=ledger)
    assert any(needle in p for p in problems), problems


def test_a_row_claiming_integrity_the_tree_does_not_have_fails():
    assert check(pr(new_row()), recomputed={**RECOMPUTED, "integrity": False})


def test_golden_staleness_alone_is_not_a_mismatch():
    assert (
        check(pr(new_row()), recomputed={**RECOMPUTED, "golden": {**GOLDEN, "stale": True}}) == []
    )


def test_merge_gate_history_check_reads_main_and_the_ledger(tmp_path, monkeypatch):
    evals = tmp_path / "data" / "evals"
    evals.mkdir(parents=True)
    (evals / "history.json").write_text(json.dumps(pr(new_row(integrity={"passed": False}))))
    (tmp_path / "config.yaml").write_text("budget:\n  monthly_cap_usd: 100\n")
    refs = {"BASE:data/evals/history.json": MAIN, "LEDGER:budget.json": {"runs": [RESERVE]}}
    monkeypatch.setattr(merge_gate, "git_json", lambda ref, default: refs.get(ref, default))
    import eval_history
    import eval_integrity

    monkeypatch.setattr(eval_integrity, "run", lambda: {"passed": True})
    monkeypatch.setattr(eval_history, "weekly", lambda *a: {**GOLDEN, "stale": False})
    problems = merge_gate.history_check("BASE", tmp_path, ledger_ref="LEDGER")
    assert problems == ["history: the new row's integrity disagrees with the merged tree"]
    refs["BASE:data/evals/history.json"] = pr(new_row(integrity={"passed": False}))
    assert merge_gate.history_check("BASE", tmp_path, ledger_ref="LEDGER") == []  # unchanged


@pytest.mark.parametrize(
    "path,ok",
    [
        ("data/evals/history.json", True),
        ("data/evals/golden.json", False),
        ("data/evals/golden-2026-07-14.json", False),
        ("data/evals/recall-2026-W29.json", False),  # a current-week file to block a refetch
        ("data/evals/recall-2099-W01.json", False),  # a future-dated score
    ],
)
def test_scan_prs_may_touch_only_the_history_file_under_evals(path, ok):
    assert (merge_guard.path_reason(path) is None) is ok
