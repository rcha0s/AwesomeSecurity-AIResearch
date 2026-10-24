"""Tests for scripts/eval_history.py + eval_lib.py (ISC-25, ISC-26): the 7-run gate."""

from __future__ import annotations

import json
from datetime import timedelta

import budget
import common
import eval_history as eh
import eval_lib as el
import pytest

CFG = el.DEFAULTS
FRESH = "2026-07-01T06:00:00+00:00"


def row(i: int = 0, **over) -> dict:
    """A run that passes every bar; results generated the morning of 2026-07-01."""
    out = {
        "run_id": f"r{i}",
        "date": f"2026-07-{i + 1:02d}",
        "runner": "cloud",
        "candidates": 40,
        "stories": 6,
        "kept": 3,
        "kept_ratio": 0.5,
        "recall": {"recall": 0.9, "passed": True, "errors": 0, "stale": False, "generated": FRESH},
        "golden": {"score": 0.95, "off_topic_rate": 0.05, "stale": False, "generated": FRESH},
        "integrity": {"passed": True, "problems": 0},
        "cost_usd": 3.554,
        "cost_basis": "reserved",
        "ceiling_usd": 3.554,
        "cap_usd": 3.3333,
    }
    out.update(over)
    return out


def rec(**over) -> dict:
    return {**row()["recall"], **over}


def gold(**over) -> dict:
    return {**row()["golden"], **over}


@pytest.mark.parametrize(
    "over,reason",
    [
        ({"recall": rec(recall=0.84)}, "recall 0.84 < 0.85"),
        ({"recall": rec(stale=True)}, "no fresh recall result"),
        ({"recall": None}, "no fresh recall result"),
        ({"recall": rec(generated="2026-06-01T00:00:00+00:00")}, "no fresh recall result"),
        ({"recall": rec(generated="2026-07-09T00:00:00+00:00")}, "no fresh recall result"),
        ({"recall": rec(errors=1)}, "recall result is not clean (curator errors or not passed)"),
        (
            {"recall": rec(passed=False)},
            "recall result is not clean (curator errors or not passed)",
        ),
        ({"golden": gold(score=0.89)}, "golden 0.89 < 0.9"),
        ({"golden": gold(off_topic_rate=0.11)}, "off-topic 0.11 > 0.1"),
        ({"golden": None}, "no fresh golden result"),
        ({"golden": gold(stale=True)}, "no fresh golden result"),
        ({"golden": gold(generated="2026-05-01T00:00:00+00:00")}, "no fresh golden result"),
        ({"integrity": {"passed": False, "problems": 2}}, "integrity failed (2 problems)"),
        ({"cost_usd": 3.6}, "cost $3.60 > reserved ceiling $3.55"),
        ({"cost_usd": 3.4, "cost_basis": "measured"}, "cost $3.40 > per-run cap $3.33"),
        ({"cost_usd": None}, "cost, basis or cap unknown"),
        ({"cost_basis": None}, "cost, basis or cap unknown"),
        ({"ceiling_usd": None}, "cost, basis or cap unknown"),
    ],
)
def test_each_bar_fails_a_run_on_its_own(over, reason):
    assert eh.verdict(row(**over), CFG["thresholds"]) == [reason]


def test_a_cloud_reservation_above_the_per_run_cap_still_passes():
    """Live numbers (2026-10-20): the cloud ceiling is 8 x $0.444 = $3.554, above the
    $3.333 per-run cap. A reservation is judged against its own ceiling."""
    assert eh.verdict(row(), CFG["thresholds"]) == []
    measured = row(cost_usd=3.2, cost_basis="measured")
    assert eh.verdict(measured, CFG["thresholds"]) == []


def test_a_run_exactly_at_every_bar_passes():
    exact = row(recall=rec(recall=0.85), golden=gold(score=0.9, off_topic_rate=0.1),
                cost_usd=3.3333, cost_basis="measured")  # fmt: skip
    assert eh.verdict(exact, CFG["thresholds"]) == []


def test_staleness_is_judged_at_the_run_date_not_taken_from_the_row():
    late = row(6, recall=rec(generated="2026-06-20T00:00:00+00:00", stale=False))
    assert eh.verdict(late, CFG["thresholds"]) == ["no fresh recall result"]


def test_the_gate_needs_seven_consecutive_passing_runs():
    assert eh.gate([row(i) for i in range(7)], CFG)["passed"]
    assert not eh.gate([row(i) for i in range(6)], CFG)["passed"]  # too few
    broken = [row(i) for i in range(7)]
    broken[3] = row(3, cost_usd=9.0)
    result = eh.gate(broken, CFG)
    assert not result["passed"] and result["streak"] == 3
    healed = broken + [row(i, date="2026-07-08") for i in range(7, 14)]
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


def stamp(delta: timedelta) -> str:
    return (common.utcnow() + delta).isoformat()


def test_results_go_stale_including_future_dated_ones():
    assert not el.is_stale({"generated": stamp(-timedelta(days=8))}, 8)
    assert el.is_stale({"generated": stamp(-timedelta(days=9))}, 8)
    assert el.is_stale({"generated": stamp(timedelta(days=3))}, 8)  # forged freshness
    assert not el.is_stale({"generated": stamp(timedelta(minutes=30))}, 8)  # clock skew
    assert el.is_stale({}, 8) and el.is_stale({"generated": "2026-07-15T00:00:00"}, 8)


def test_the_newest_result_is_picked_by_its_stamp_not_its_name(sandbox):
    d = sandbox / "data" / "evals"
    d.mkdir()
    files = {
        "recall-2026-W28.json": stamp(-timedelta(days=1)),  # the real newest
        "recall-2026-W52.json": stamp(-timedelta(days=30)),  # a later name, older result
        "recall-2099-W01.json": stamp(timedelta(days=400)),  # future-dated: never wins
        "recall-2026-W29.json": "not a date",
    }
    for name, generated in files.items():
        (d / name).write_text(json.dumps({"generated": generated, "name": name}))
    assert el.latest_result("recall")[1]["name"] == "recall-2026-W28.json"
    assert el.latest_result("golden") is None


def test_summary_line_is_one_parseable_line():
    line = el.summary_line("recall", False, recall=0.8333, week="2026-W29", note="two words")
    assert line == "EVAL recall FAIL recall=0.833 week=2026-W29 note=two_words"


def write_ledger(path, run_id: str, *rows) -> None:
    base = {"run_id": run_id, "date": "2026-07-15", "runner": "cloud", "stories": 0}
    path.write_text(json.dumps({"runs": [{**base, **r} for r in rows]}))


def test_run_charge_reports_basis_and_ceiling(tmp_path):
    ledger = tmp_path / "l.json"
    write_ledger(ledger, "C1", {"kind": "reserve", "cost_usd": 3.554})
    assert eh.run_charge(ledger, "C1") == {
        "cost_usd": 3.554, "cost_basis": "reserved", "ceiling_usd": 3.554,
    }  # fmt: skip
    write_ledger(ledger, "C1", {"kind": "reserve", "cost_usd": 2.0},
                 {"kind": "actual", "cost_usd": 0.9})  # fmt: skip
    assert eh.run_charge(ledger, "C1")["cost_basis"] == "measured"
    assert eh.run_charge(ledger, "nope")["cost_usd"] is None
    assert eh.run_charge(None, "C1")["cost_basis"] is None


def setup_append(sandbox, monkeypatch):
    monkeypatch.setattr(common, "_MAIN_IDS", set())  # every pool entry is this run's
    monkeypatch.setattr(eh.eval_integrity, "run", lambda: {"passed": True, "problems": []})
    d = sandbox / "data" / "evals"
    d.mkdir()
    fresh = common.utcnow_iso()
    golden = {"score": 0.95, "off_topic_rate": 0.0, "generated": fresh}
    (d / "golden-2026-07-14.json").write_text(json.dumps(golden))
    from conftest import make_entry

    pool = common.empty_pool("ai-research")
    pool["entries"] = [make_entry(id="k"), make_entry(id="h", needs_review=True, title="Other")]
    common.save_pool("ai-research", pool)
    ledger = sandbox / "ledger.json"
    write_ledger(ledger, "C1", {"kind": "reserve", "cost_usd": 2.0})
    recall = sandbox / "recall.json"
    recall.write_text(json.dumps({"recall": 0.9, "passed": True, "errors": [], "generated": fresh}))
    common.save_json(d / "history.json", {"runs": [row(i) for i in range(7)]})
    args = ["append", "--run-id", "C1", "--runner", "cloud", "--stories", "2", "--candidates",
            "41", "--ledger", str(ledger), "--recall", str(recall)]  # fmt: skip
    return d, args


def test_append_builds_the_row_and_body_renders_numbers_and_trend(sandbox, monkeypatch, capsys):
    d, args = setup_append(sandbox, monkeypatch)
    assert eh.main(args) == 0
    assert capsys.readouterr().out.strip() == "EVAL run PASS run_id=C1 fails=0"
    last = eh.load_rows()[-1]
    assert (last["kept"], last["kept_ratio"], last["cost_usd"]) == (1, 0.5, 2.0)
    assert (last["cost_basis"], last["ceiling_usd"]) == ("reserved", 2.0)
    assert last["recall"]["file"] == "recall.json" and last["recall"]["errors"] == 0
    assert not last["golden"]["stale"]
    assert eh.main(args) == 0 and len(eh.load_rows()) == 8  # re-running post replaces its row
    eh.main(["body", "--run-id", "C1"])
    body = capsys.readouterr().out
    assert "**Run numbers:** 41 candidates staged · 2 stories analyzed · 1 kept (50% of new" in body
    cap = budget.budget_settings()["monthly_cap_usd"] / 30  # config.yaml's cap, a month of runs
    assert f"charged $2.00 (reserved; reserved ceiling $2.00, per-run cap ${cap:.2f})" in body
    assert body.count("| cloud |") == 7  # the 7-run trend
    assert eh.main(["gate"]) == 0
    assert (
        capsys.readouterr().out.strip().splitlines()[-1] == "EVAL gate PASS streak=8 need=7 runs=8"
    )


def test_append_ignores_recall_files_in_the_tree_when_given_its_own(sandbox, monkeypatch):
    """A current-week recall file planted under data/evals can't stand in for the
    run's own fetch: post passes --recall, and a missing fetch means no recall."""
    d, args = setup_append(sandbox, monkeypatch)
    planted = {"recall": 1.0, "passed": True, "errors": [], "generated": common.utcnow_iso()}
    (d / "recall-2026-W29.json").write_text(json.dumps(planted))
    (sandbox / "recall.json").unlink()  # this run's fetch errored, so it wrote nothing
    assert eh.main(args) == 0
    assert eh.load_rows()[-1]["recall"] is None


def test_gate_cli_fails_without_enough_history(sandbox, capsys):
    (sandbox / "data" / "evals").mkdir()
    assert eh.main(["gate"]) == 1
    assert capsys.readouterr().out.strip() == "EVAL gate FAIL streak=0 need=7 runs=0"


def test_the_row_keeps_independent_and_per_curator_recall_and_the_body_shows_them(
    sandbox, monkeypatch, capsys
):
    d, args = setup_append(sandbox, monkeypatch)
    result = json.loads((sandbox / "recall.json").read_text())
    per = {"tldrsec": {"recall": 0.5, "independent_recall": 0.25}}
    result.update(independent_recall=0.3, curator_recall=per, misses=[{"title": "x"}])
    (sandbox / "recall.json").write_text(json.dumps(result))
    assert eh.main(args) == 0
    last = eh.load_rows()[-1]["recall"]
    assert last["independent_recall"] == 0.3 and last["curator_recall"] == per
    assert "misses" not in last  # only RECALL_KEYS
    assert eh.verdict(eh.load_rows()[-1], CFG["thresholds"]) == []  # the gate reads `recall`
    capsys.readouterr()
    eh.main(["body", "--run-id", "C1"])
    body = capsys.readouterr().out
    assert "| Recall (independent) |" in body and "| 90% (30%) |" in body
    assert "**Recall by curator** (this run): tldrsec 50% (25% independent)" in body
    assert "| 90% (n/a) |" in body  # older rows without the new key still render


def test_body_without_a_row_says_so():
    assert "unavailable" in eh.body([], "nope", CFG)
