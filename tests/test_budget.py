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


def test_a_calibration_window_retires_an_old_outlier_but_not_to_padding():
    # 2026-10: the first run (3 stories, $0.44 each) set every later ceiling.
    first = row("a", cost=1.32, stories=3)  # $0.44/story
    honest = [row(f"h{i}", cost=1.68, stories=8) for i in range(5)]  # $0.21/story
    assert budget.usd_per_story([first, *honest]) == pytest.approx(0.44)  # no window
    assert budget.usd_per_story([first, *honest], window=5) == pytest.approx(0.21)
    assert budget.usd_per_story([first, *honest[:4]], window=5) == pytest.approx(0.44)
    padded = [first, *[row(f"p{i}", cost=0.8, stories=8) for i in range(4)]]  # $0.10/story
    assert budget.usd_per_story(padded, window=5) == pytest.approx(0.44)  # 4 pads aren't enough
    for off in (None, 0, -1):
        assert budget.usd_per_story([first, *honest], window=off) == pytest.approx(0.44)
    assert budget.usd_per_story([first], override=0.1, window=5) == 0.1


def test_headroom_scales_a_measured_rate_never_an_override_and_never_down():
    runs = [row("a", cost=2.0, stories=4)]  # $0.50/story
    s = {**settings(cap=100.0, max_stories=10), "ceiling_headroom": 1.5}
    assert budget.run_ceiling(runs, s, "cloud") == (7.5, "calibrated")
    assert budget.run_ceiling(runs, {**s, "usd_per_story": 0.25}, "cloud")[0] == 2.5
    assert budget.run_ceiling(runs, {**s, "ceiling_headroom": 0.5}, "cloud")[0] == 5.0
    assert budget.run_ceiling(runs, {**s, "ceiling_headroom": None}, "cloud")[0] == 5.0
    later = [*runs, row("b", cost=1.0, stories=4)]  # $0.25/story, the newest
    assert budget.run_ceiling(later, {**s, "calibration_runs": 1}, "cloud")[0] == 3.75
    assert budget.run_ceiling(later, s, "cloud")[0] == 7.5  # no window: the old worst


def test_real_config_fits_a_month_of_cloud_runs_at_the_measured_rate():
    """The 2026-10-22 run: 8 stories for $1.67. Cloud runs are charged the
    ceiling, one a day, so 31 of them must fit the monthly cap."""
    s = budget.budget_settings()
    assert s["calibration_runs"] >= 3  # padding has to repeat to move the ceiling
    assert s["ceiling_headroom"] * s["session_cap_fraction"] > 1  # a worst-rate run fits
    ceiling, _ = budget.run_ceiling([row("m", cost=1.6749, stories=8)], s, "cloud")
    assert 31 * ceiling <= s["monthly_cap_usd"]


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
        {"run_id": "a|b"},
        {"run_id": "a\nb"},
    ],
)
def test_invalid_rows_fail_closed(tmp_path, bad):
    ledger = tmp_path / "ledger.json"
    common.save_json(ledger, {"runs": [{**row(), **bad}]})
    with pytest.raises(budget.LedgerError):
        budget.load_ledger(ledger)


def test_spend_report_shows_each_run_and_what_it_was_charged():
    runs = [
        row("L1", kind="reserve", cost=5.0, stories=0),
        row("L1", kind="actual", cost=1.8, stories=6),
        {**row("L1", kind="done", cost=0, stories=6)},
        row("C1", date="2026-07-03", kind="reserve", runner="cloud", cost=2.4, stories=0),
        row("old", date="2026-06-30", cost=40.0),
    ]
    report = budget.spend_report(runs, settings(cap=100.0), MONTH)
    assert "**$4.20 charged of $100.00.**" in report
    assert "| 2026-07-02 | local | `L1` | 6 | $1.80 | measured | yes |" in report
    assert "| 2026-07-03 | cloud | `C1` | 0 | $2.40 | reserved ceiling | no |" in report
    assert "`old`" not in report
    assert "no cap set" in budget.spend_report([], settings(cap=None), MONTH)


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
    assert 0 < s["retry_max_usd"] <= 2  # a small, named allowance


def failed_empty(run_id="L1", cost=0.4, runner="local", outcome="analysis-empty") -> list[dict]:
    reserve = row(run_id, date=TODAY, kind="reserve", cost=2.0, stories=0, runner=runner)
    actual = {**reserve, "kind": "actual", "cost_usd": cost}
    if outcome:
        actual["outcome"] = outcome
    return [reserve, actual]


RETRY = {**settings(per_story=0.1), "retry_max_usd": 1.0}


def test_one_local_retry_after_a_cheap_analysis_empty_failure():
    ok, reason = budget.check(failed_empty(), RETRY, "local", TODAY)
    assert ok, reason
    # The retry's own reservation is the record: a second retry is blocked.
    second = failed_empty() + failed_empty("L2")[:1]
    ok, reason = budget.check(second, RETRY, "local", TODAY)
    assert not ok and "already tried" in reason
    second += failed_empty("L2")[1:]  # even when the retry also came back empty
    assert not budget.check(second, RETRY, "local", TODAY)[0]


@pytest.mark.parametrize(
    "runs, settings_",
    [
        (failed_empty(cost=1.0), RETRY),  # cost not below the limit
        (failed_empty(), {**RETRY, "retry_max_usd": None}),  # no allowance configured
        (failed_empty()[:1], RETRY),  # no actual row: outcome unknown
        (failed_empty(outcome=None), RETRY),  # failed some other way
        (failed_empty(runner="cloud"), RETRY),  # the cloud never retries
    ],
)
def test_no_retry_unless_local_cheap_and_analysis_empty(runs, settings_):
    runner = runs[0]["runner"]
    assert not budget.check(runs, settings_, runner, TODAY)[0]


def test_actual_rows_carry_only_known_outcomes():
    budget.validate_row(failed_empty()[1])
    with pytest.raises(budget.LedgerError):
        budget.validate_row({**failed_empty()[1], "outcome": "whatever"})
