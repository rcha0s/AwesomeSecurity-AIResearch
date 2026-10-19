"""Tests for scripts/budget.py — reserve before spend; the guard runs before LLM work (ISC-8)."""

from __future__ import annotations

import budget
import common
import pytest

TODAY = "2026-07-15"  # conftest pins the clock
MONTH = TODAY[:7]


def settings(cap=10.0, per_story=None, max_stories=8, uncalibrated=None) -> dict:
    return {
        "monthly_cap_usd": cap,
        "usd_per_story": per_story,
        "uncalibrated_run_usd": uncalibrated,
        "max_stories_per_run": max_stories,
    }


def row(run_id="r1", date="2026-07-02", kind="actual", cost=1.0, stories=4, runner="local"):
    return {
        "run_id": run_id,
        "date": date,
        "runner": runner,
        "kind": kind,
        "stories": stories,
        "cost_usd": cost,
    }


def test_no_cap_configured_skips():
    ok, reason = budget.check([], settings(cap=None), "local", TODAY)
    assert not ok and "monthly_cap_usd" in reason


def test_exhausted_month_skips_both_runners():
    runs = [row("a", cost=6.0), row("b", cost=4.0)]
    for runner in budget.RUNNERS:
        ok, reason = budget.check(runs, settings(cap=10.0), runner, TODAY)
        assert not ok and "exhausted" in reason


def test_reservation_counts_until_an_actual_replaces_it():
    reserved = [row("a", kind="reserve", cost=5.0, stories=0)]
    assert budget.month_spend(reserved, MONTH) == 5.0
    settled = reserved + [row("a", kind="actual", cost=1.5)]
    assert budget.month_spend(settled, MONTH) == 1.5


def test_failed_run_is_still_charged_its_reservation():
    runs = [row("a", kind="reserve", cost=10.0, stories=0, date="2026-07-02")]
    ok, reason = budget.check(runs, settings(cap=10.0, per_story=1.0), "cloud", TODAY)
    assert not ok and "exhausted" in reason


def test_previous_months_spend_does_not_count():
    runs = [row(date="2026-06-30", cost=50.0, stories=500)]
    ok, _ = budget.check(runs, settings(cap=10.0), "local", TODAY)
    assert ok


def test_a_finished_day_blocks_both_runners_unless_allowed():
    runs = [row("a", date=TODAY, kind="reserve", runner="cloud", cost=0.5, stories=0)]
    runs.append({**runs[0], "kind": "done", "cost_usd": 0, "stories": 5})
    for runner in budget.RUNNERS:
        ok, reason = budget.check(runs, settings(per_story=0.1), runner, TODAY)
        assert not ok and "finished" in reason
    ok, _ = budget.check(runs, settings(per_story=0.1), "local", TODAY, allow_repeat=True)
    assert ok


def test_a_failed_cloud_run_does_not_block_the_mac_fallback():
    failed_cloud = [row("c", date=TODAY, kind="reserve", runner="cloud", cost=0.5, stories=0)]
    ok, reason = budget.check(failed_cloud, settings(per_story=0.1), "local", TODAY)
    assert ok, reason
    ok, reason = budget.check(failed_cloud, settings(per_story=0.1), "cloud", TODAY)
    assert not ok and "already tried" in reason


def test_done_rows_cost_nothing_and_keep_the_reservation_charged():
    runs = [row("a", kind="reserve", cost=3.0, stories=0)]
    runs.append({**runs[0], "kind": "done", "cost_usd": 0, "stories": 2})
    assert budget.month_spend(runs, MONTH) == 3.0


def test_cloud_needs_calibration_and_local_needs_a_reserve():
    ok, reason = budget.check([], settings(uncalibrated=2.0), "cloud", TODAY)
    assert not ok and "local scan first" in reason
    ok, reason = budget.check([], settings(), "local", TODAY)
    assert not ok and "uncalibrated_run_usd" in reason
    ok, reason = budget.check([], settings(uncalibrated=2.0), "local", TODAY)
    assert ok and "reserves $2.00" in reason


def test_uncalibrated_reserve_must_fit_too():
    ok, reason = budget.check([], settings(cap=1.0, uncalibrated=2.0), "local", TODAY)
    assert not ok and "ceiling $2.00" in reason


def test_ceiling_must_fit_the_remaining_budget():
    runs = [row(cost=8.0, stories=8)]  # $1/story measured, $2 left
    ok, reason = budget.check(runs, settings(cap=10.0, max_stories=3), "cloud", TODAY)
    assert not ok and "ceiling $3.00" in reason
    ok, reason = budget.check(runs, settings(cap=10.0, max_stories=2), "cloud", TODAY)
    assert ok and "reserves $2.00" in reason


def test_per_story_is_the_worst_actual_run_so_padding_cannot_lower_it():
    runs = [row("a", cost=2.0, stories=4), row("b", kind="reserve", cost=99.0, stories=1)]
    assert budget.usd_per_story(runs) == pytest.approx(0.5)
    padded = runs + [row("c", cost=0.8, stories=8)]  # $0.10/story padding run
    assert budget.usd_per_story(padded) == pytest.approx(0.5)
    assert budget.usd_per_story(runs, override=0.25) == 0.25


@pytest.mark.parametrize(
    "bad",
    [
        {"cost_usd": -1000},
        {"cost_usd": float("nan")},
        {"cost_usd": True},
        {"stories": -1},
        {"date": "yesterday"},
        {"runner": "evil"},
        {"kind": "refund"},
        {"run_id": ""},
    ],
)
def test_invalid_rows_fail_closed(tmp_path, bad):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": [{**row(), **bad}]})
    with pytest.raises(budget.LedgerError):
        budget.load_ledger(ledger)


def write_config(tmp_path, cap="5.0", uncalibrated="2.0", per_story="null"):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "limits:\n  max_stories_per_run: 4\n"
        f"budget:\n  monthly_cap_usd: {cap}\n  usd_per_story: {per_story}\n"
        f"  uncalibrated_run_usd: {uncalibrated}\n"
    )
    return str(cfg)


def test_cli_refuses_a_missing_ledger_file(tmp_path, monkeypatch):
    monkeypatch.setenv("BUDGET_LEDGER", str(tmp_path / "never-fetched.json"))
    with pytest.raises(budget.LedgerError):
        budget.main(["--config", write_config(tmp_path), "check", "--runner", "local"])


def test_cli_session_limits(tmp_path, monkeypatch, capsys):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": []})
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    budget.main(["--config", write_config(tmp_path), "session-limits", "--runner", "local"])
    assert capsys.readouterr().out.strip() == "1.60 150"  # $2.00 reserve x 0.8; default turns


def test_cli_check_reserve_actual_cycle(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": []})
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    cfg = write_config(tmp_path)
    assert budget.main(["--config", cfg, "check", "--runner", "local"]) == 0
    budget.main(["--config", cfg, "reserve", "--runner", "local", "--run-id", "L1"])
    budget.main(
        ["--config", cfg, "actual", "--run-id", "L1", "--stories", "4", "--cost-usd", "1.2"]
    )
    rows = common.load_json(ledger)["runs"]
    assert [r["kind"] for r in rows] == ["reserve", "actual"]
    assert rows[0]["cost_usd"] == 2.0 and rows[1]["cost_usd"] == 1.2
    # unfinished local run (no done row): the other runner may still go, calibrated
    assert budget.main(["--config", cfg, "check", "--runner", "cloud"]) == 0
    assert budget.main(["--config", cfg, "check", "--runner", "local"]) == budget.SKIP_EXIT


def test_cli_cloud_reserves_calibrated_ceiling(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": [row("L0", date="2026-07-01", cost=2.0, stories=4)]})
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    cfg = write_config(tmp_path, cap="10.0")
    assert budget.main(["--config", cfg, "check", "--runner", "cloud"]) == 0
    budget.main(["--config", cfg, "reserve", "--runner", "cloud", "--run-id", "C1"])
    assert common.load_json(ledger)["runs"][-1]["cost_usd"] == 2.0  # 4 stories x $0.50


def test_cli_actual_needs_a_reservation(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": []})
    monkeypatch.setenv("BUDGET_LEDGER", str(ledger))
    cfg = write_config(tmp_path)
    with pytest.raises(SystemExit):
        budget.main(
            ["--config", cfg, "actual", "--run-id", "nope", "--stories", "1", "--cost-usd", "1"]
        )


def test_real_config_declares_the_guard_keys():
    s = budget.budget_settings()
    assert {"monthly_cap_usd", "usd_per_story", "uncalibrated_run_usd"} <= s.keys()
    assert s["max_stories_per_run"] > 0
