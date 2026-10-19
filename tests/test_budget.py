"""Tests for scripts/budget.py — the spend guard runs before any LLM work (ISC-8)."""

from __future__ import annotations

import budget
import common
import pytest

MONTH = "2026-07"  # conftest pins the clock to 2026-07-15


def settings(cap=10.0, per_story=None, max_stories=8) -> dict:
    return {"monthly_cap_usd": cap, "usd_per_story": per_story, "max_stories_per_run": max_stories}


def run(date="2026-07-02", cost=1.0, stories=4, measured=True, runner="local") -> dict:
    return {
        "date": date,
        "runner": runner,
        "stories": stories,
        "cost_usd": cost,
        "measured": measured,
    }


def test_no_cap_configured_skips():
    ok, reason = budget.check([], settings(cap=None), "local", MONTH)
    assert not ok and "monthly_cap_usd" in reason


def test_exhausted_month_skips_both_runners():
    runs = [run(cost=6.0), run(cost=4.0)]
    for runner in budget.RUNNERS:
        ok, reason = budget.check(runs, settings(cap=10.0), runner, MONTH)
        assert not ok and "exhausted" in reason


def test_previous_months_spend_does_not_count():
    runs = [run(date="2026-06-30", cost=50.0, stories=500)]
    ok, _ = budget.check(runs, settings(cap=10.0), "local", MONTH)
    assert ok


def test_cloud_needs_a_measured_per_story_cost():
    ok, reason = budget.check([], settings(), "cloud", MONTH)
    assert not ok and "local scan first" in reason
    ok, _ = budget.check([], settings(), "local", MONTH)
    assert ok  # the uncalibrated local run is the calibration run


def test_ceiling_must_fit_the_remaining_budget():
    runs = [run(cost=8.0, stories=8)]  # $1/story measured, $2 left
    ok, reason = budget.check(runs, settings(cap=10.0, max_stories=3), "cloud", MONTH)
    assert not ok and "ceiling $3.00" in reason
    ok, reason = budget.check(runs, settings(cap=10.0, max_stories=2), "cloud", MONTH)
    assert ok and "at most $2.00" in reason


def test_per_story_mean_uses_measured_runs_only():
    runs = [run(cost=2.0, stories=4), run(cost=99.0, stories=1, measured=False)]
    assert budget.usd_per_story(runs) == pytest.approx(0.5)
    assert budget.usd_per_story(runs, override=0.25) == 0.25


def test_cli_check_exit_codes(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    monkeypatch.setattr(budget, "budget_settings", lambda: settings(cap=None))
    assert budget.main(["check", "--runner", "cloud"]) == budget.SKIP_EXIT
    monkeypatch.setattr(budget, "budget_settings", lambda: settings(cap=5.0))
    assert budget.main(["check", "--runner", "local"]) == 0


def test_cli_record_measured_then_estimated(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    monkeypatch.setattr(budget, "budget_settings", lambda: settings(cap=5.0))
    budget.main(["record", "--runner", "local", "--stories", "4", "--cost-usd", "2.0"])
    budget.main(["record", "--runner", "cloud", "--stories", "3"])
    rows = common.load_json(ledger)["runs"]
    assert rows[0] == run(date="2026-07-15", cost=2.0, stories=4, measured=True)
    assert rows[1]["cost_usd"] == pytest.approx(1.5) and rows[1]["measured"] is False


def test_cli_record_without_cost_or_calibration_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("BUDGET_LEDGER", str(tmp_path / "ledger.json"))
    monkeypatch.setattr(budget, "budget_settings", lambda: settings(cap=5.0))
    with pytest.raises(SystemExit):
        budget.main(["record", "--runner", "cloud", "--stories", "3"])


def test_real_config_declares_the_guard_keys():
    s = budget.budget_settings()
    assert "monthly_cap_usd" in s and "usd_per_story" in s
    assert s["max_stories_per_run"] > 0


def test_cli_ran_today(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": [run(date="2026-07-15", runner="cloud")]})
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    assert budget.main(["ran-today", "--runner", "cloud"]) == 0
    assert budget.main(["ran-today", "--runner", "local"]) == 1
