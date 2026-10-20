"""Tests for scripts/eval_history.py + eval_lib.py (ISC-25, ISC-26): the 7-run gate."""

from __future__ import annotations

import json
from datetime import timedelta

import common
import eval_history as eh
import eval_lib as el
import pytest

CFG = el.DEFAULTS


def row(i: int = 0, **over) -> dict:
    """A run that passes every bar."""
    out = {
        "run_id": f"r{i}",
        "date": f"2026-07-{i + 1:02d}",
        "runner": "cloud",
        "candidates": 40,
        "stories": 6,
        "kept": 3,
        "kept_ratio": 0.5,
        "recall": {"recall": 0.9, "stale": False},
        "golden": {"score": 0.95, "off_topic_rate": 0.05, "stale": False},
        "integrity": {"passed": True, "problems": 0},
        "cost_usd": 2.0,
        "cap_usd": 3.33,
    }
    out.update(over)
    return out


@pytest.mark.parametrize(
    "over,reason",
    [
        ({"recall": {"recall": 0.84, "stale": False}}, "recall 0.84 < 0.85"),
        ({"recall": {"recall": 0.99, "stale": True}}, "no fresh recall result"),
        ({"recall": None}, "no fresh recall result"),
        ({"golden": {"score": 0.89, "off_topic_rate": 0.0, "stale": False}}, "golden 0.89 < 0.9"),
        (
            {"golden": {"score": 0.95, "off_topic_rate": 0.11, "stale": False}},
            "off-topic 0.11 > 0.1",
        ),
        ({"golden": None}, "no fresh golden result"),
        (
            {"golden": {"score": 0.99, "off_topic_rate": 0.0, "stale": True}},
            "no fresh golden result",
        ),
        ({"integrity": {"passed": False, "problems": 2}}, "integrity failed (2 problems)"),
        ({"cost_usd": 3.34}, "cost $3.34 > cap $3.33"),
        ({"cost_usd": None}, "cost or per-run cap unknown"),
        ({"cap_usd": None}, "cost or per-run cap unknown"),
    ],
)
def test_each_bar_fails_a_run_on_its_own(over, reason):
    assert eh.verdict(row(**over), CFG["thresholds"]) == [reason]


def test_a_run_exactly_at_every_bar_passes():
    exact = row(recall={"recall": 0.85, "stale": False}, cost_usd=3.33,
                golden={"score": 0.9, "off_topic_rate": 0.1, "stale": False})  # fmt: skip
    assert eh.verdict(exact, CFG["thresholds"]) == []


def test_the_gate_needs_seven_consecutive_passing_runs():
    assert eh.gate([row(i) for i in range(7)], CFG)["passed"]
    assert not eh.gate([row(i) for i in range(6)], CFG)["passed"]  # too few
    broken = [row(i) for i in range(7)]
    broken[3] = row(3, cost_usd=9.0)
    result = eh.gate(broken, CFG)
    assert not result["passed"] and result["streak"] == 3
    healed = broken + [row(i) for i in range(7, 14)]  # an old failure outside the window
    assert eh.gate(healed, CFG)["passed"] and eh.gate(healed, CFG)["streak"] == 10


def test_per_run_cap_defaults_to_a_thirtieth_of_the_monthly_cap(tmp_path):
    cfg = tmp_path / "c.yaml"
    cfg.write_text("budget:\n  monthly_cap_usd: 100\n")
    assert el.per_run_cap(cfg) == 3.3333
    cfg.write_text("budget:\n  monthly_cap_usd: 100\nevals:\n  thresholds:\n    max_run_usd: 2.5\n")
    assert el.per_run_cap(cfg) == 2.5
    assert el.settings(cfg)["thresholds"]["recall_min"] == 0.85  # defaults fill the rest
    cfg.write_text("budget:\n  monthly_cap_usd: null\n")
    assert el.per_run_cap(cfg) is None


def test_results_go_stale_and_the_newest_file_wins(sandbox):
    now = common.utcnow()
    assert not el.is_stale({"generated": (now - timedelta(days=8)).isoformat()}, 8)
    assert el.is_stale({"generated": (now - timedelta(days=9)).isoformat()}, 8)
    assert el.is_stale({}, 8) and el.is_stale({"generated": "2026-07-15T00:00:00"}, 8)
    d = sandbox / "data" / "evals"
    d.mkdir()
    for week in ("2026-W27", "2026-W29", "2026-W28"):
        (d / f"recall-{week}.json").write_text(json.dumps({"week": week}))
    assert el.latest_result("recall")[1]["week"] == "2026-W29"
    assert el.latest_result("golden") is None


def test_summary_line_is_one_parseable_line():
    line = el.summary_line("recall", False, recall=0.8333, week="2026-W29", note="two words")
    assert line == "EVAL recall FAIL recall=0.833 week=2026-W29 note=two_words"


def write_ledger(path, run_id: str, cost: float) -> None:
    rows = [{"run_id": run_id, "date": "2026-07-15", "runner": "cloud", "kind": "reserve",
             "stories": 0, "cost_usd": cost}]  # fmt: skip
    path.write_text(json.dumps({"runs": rows}))


def test_append_builds_the_row_and_body_renders_numbers_and_trend(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(common, "_MAIN_IDS", set())  # every pool entry is this run's
    monkeypatch.setattr(eh.eval_integrity, "run", lambda: {"passed": True, "problems": []})
    d = sandbox / "data" / "evals"
    d.mkdir()
    fresh = common.utcnow_iso()
    (d / "recall-2026-W29.json").write_text(
        json.dumps({"recall": 0.9, "week": "2026-W29", "generated": fresh})
    )
    (d / "golden-2026-07-14.json").write_text(
        json.dumps({"score": 0.95, "off_topic_rate": 0.0, "generated": fresh})
    )
    from conftest import make_entry

    pool = common.empty_pool("ai-research")
    pool["entries"] = [
        make_entry(id="k"),
        make_entry(id="h", needs_review=True, title="Other thing"),
    ]
    common.save_pool("ai-research", pool)
    ledger = sandbox / "ledger.json"
    write_ledger(ledger, "C1", 2.0)
    common.save_json(d / "history.json", {"runs": [row(i) for i in range(7)]})
    args = ["append", "--run-id", "C1", "--runner", "cloud", "--stories", "2",
            "--candidates", "41", "--ledger", str(ledger)]  # fmt: skip
    assert eh.main(args) == 0
    assert capsys.readouterr().out.strip() == "EVAL run PASS run_id=C1 fails=0"
    last = eh.load_rows()[-1]
    assert (last["kept"], last["kept_ratio"], last["cost_usd"]) == (1, 0.5, 2.0)
    assert last["recall"]["file"] == "recall-2026-W29.json" and not last["golden"]["stale"]
    assert eh.main(args) == 0 and len(eh.load_rows()) == 8  # re-running post replaces its row
    eh.main(["body", "--run-id", "C1"])
    body = capsys.readouterr().out
    assert "**Run numbers:** 41 candidates staged · 2 stories analyzed · 1 kept (50% of new" in body
    assert "charged $2.00 of a $3.33 per-run cap" in body
    assert body.count("| cloud |") == 7  # the 7-run trend
    assert eh.main(["gate"]) == 0
    assert (
        capsys.readouterr().out.strip().splitlines()[-1] == "EVAL gate PASS streak=8 need=7 runs=8"
    )


def test_gate_cli_fails_without_enough_history(sandbox, capsys):
    (sandbox / "data" / "evals").mkdir()
    assert eh.main(["gate"]) == 1
    assert capsys.readouterr().out.strip() == "EVAL gate FAIL streak=0 need=7 runs=0"


def test_body_without_a_row_says_so():
    assert "unavailable" in eh.body([], "nope", CFG)
