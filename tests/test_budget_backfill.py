"""Backfill on the spend ledger (issue #52): rows labelled with their window,
never the day's scan, and a whole campaign capped (budget.check_backfill)."""

from __future__ import annotations

import json

import budget
import pytest
from test_budget import TODAY, row, settings

CAMPAIGN = {"from": "2026-06-01", "to": "2026-06-30", "max_chunk_days": 10,
            "max_runs": 3, "max_usd": 6.0}  # fmt: skip
W1, W2, W3 = "2026-06-01..2026-06-08", "2026-06-09..2026-06-16", "2026-06-17..2026-06-24"


def bf_settings(**over) -> dict:
    return {**settings(cap=100.0, per_story=0.25), "backfill": {**CAMPAIGN, **over}}  # $2 ceiling


def bf(run_id: str, window: str, kind: str, cost: float = 0.0, date: str = TODAY) -> dict:
    return {**row(run_id, date=date, kind=kind, cost=cost, stories=0), "backfill": window}


def chunk(runs, window=W2, s=None, runner="local"):
    return budget.check_backfill(runs, s or bf_settings(), runner, window, TODAY)


# --- Not the day's scan -------------------------------------------------------------
def test_a_finished_backfill_today_does_not_finish_the_day():
    runs = [bf("b1", W1, "reserve", 2.0), bf("b1", W1, "actual", 1.0), bf("b1", W1, "done")]
    for runner in ("local", "cloud"):
        ok, reason = budget.check(runs, settings(cap=100.0, per_story=0.25), runner, TODAY)
        assert ok, reason


def test_a_backfill_attempt_today_is_not_the_local_runners_try():
    runs = [bf("b1", W1, "reserve", 2.0)]
    ok, reason = budget.check(runs, settings(cap=100.0, per_story=0.25), "local", TODAY)
    assert ok, reason


def test_a_daily_scan_today_does_not_block_a_backfill():
    runs = [row("d1", date=TODAY, kind="reserve", cost=2.0), row("d1", date=TODAY, kind="done")]
    ok, reason = chunk(runs)
    assert ok, reason
    assert budget.check(runs, settings(cap=100.0, per_story=0.25), "local", TODAY)[0] is False


def test_backfill_spend_still_counts_against_the_month():
    runs = [bf("b1", W1, "reserve", 2.0), bf("b1", W1, "actual", 99.0)]
    ok, reason = budget.check(runs, settings(cap=100.0, per_story=0.25), "local", TODAY)
    assert not ok and "exceeds" in reason


# --- The campaign and its caps --------------------------------------------------------
def test_a_chunk_inside_the_campaign_goes():
    ok, reason = chunk([])
    assert ok and "run 1 of 3" in reason


@pytest.mark.parametrize(
    "window,why",
    [
        ("2026-05-25..2026-06-02", "outside the approved"),
        ("2026-06-01..2026-06-15", "over backfill.max_chunk_days"),
        ("2026-06-08..2026-06-01", "ends before it starts"),
        ("2026-06-01", "YYYY-MM-DD..YYYY-MM-DD"),
        ("2026-07-10..2026-07-16", "ends in the future"),
    ],
)
def test_a_bad_or_unapproved_window_is_refused(window, why):
    ok, reason = chunk([], window=window)
    assert not ok and why in reason


def test_no_approved_campaign_refuses():
    s = {**settings(cap=100.0, per_story=0.25), "backfill": {}}
    ok, reason = chunk([], s=s)
    assert not ok and "no backfill approved" in reason


def test_only_the_local_runner_backfills():
    ok, reason = chunk([], runner="cloud")
    assert not ok and "local runner" in reason


def test_a_finished_window_is_never_run_again():
    runs = [bf("b1", W2, "reserve", 2.0), bf("b1", W2, "actual", 0.5), bf("b1", W2, "done")]
    ok, reason = chunk(runs, window="2026-06-12..2026-06-14")
    assert not ok and "already finished" in reason
    assert chunk(runs, window=W3)[0]


def test_a_window_that_failed_may_be_tried_again_within_the_caps():
    runs = [bf("b1", W2, "reserve", 2.0), bf("b1", W2, "actual", 0.3)]
    ok, reason = chunk(runs)
    assert ok and "run 2 of 3" in reason


def test_the_run_cap_counts_every_started_run():
    runs = [bf(f"b{i}", w, "reserve", 0.1) for i, w in enumerate((W1, W2, W3))]
    ok, reason = chunk(runs, s=bf_settings(max_usd=100.0), window="2026-06-25..2026-06-30")
    assert not ok and "3 of 3 runs started" in reason


def test_the_run_cap_allows_the_last_permitted_run():
    runs = [bf(f"b{i}", w, "reserve", 0.1) for i, w in enumerate((W1, W2))]
    ok, reason = chunk(runs, s=bf_settings(max_usd=100.0), window=W3)
    assert ok and "run 3 of 3" in reason


def test_the_dollar_cap_counts_this_runs_ceiling():
    runs = [bf("b1", W1, "reserve", 2.0), bf("b1", W1, "actual", 4.0)]
    ok, reason = chunk(runs)  # $4 + $2 ceiling = $6: fits exactly
    assert ok, reason
    runs.append(bf("b1", W1, "actual", 4.01))
    ok, reason = chunk(runs)
    assert not ok and "backfill.max_usd" in reason


def test_an_in_flight_reservation_counts_against_the_dollar_cap():
    ok, reason = chunk([bf("b1", W1, "reserve", 4.5)])
    assert not ok and "backfill.max_usd" in reason


def test_rows_of_another_campaign_do_not_count():
    old = [
        bf(f"x{i}", "2026-03-01..2026-03-05", "reserve", 5.0, date="2026-03-06") for i in range(5)
    ]
    ok, reason = chunk(old)
    assert ok and "run 1 of 3" in reason


def test_the_month_cap_still_applies():
    s = {**bf_settings(), "monthly_cap_usd": 1.0}
    ok, reason = chunk([], s=s)
    assert not ok and "exceeds" in reason


# --- Labelling ------------------------------------------------------------------------
def test_a_malformed_window_label_fails_the_ledger_closed():
    with pytest.raises(budget.LedgerError):
        budget.validate_row(bf("b1", "2026-06-01 to 2026-06-08", "reserve"))


def cli(tmp_path, monkeypatch, *args: str) -> int:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "budget:\n  monthly_cap_usd: 100\n  usd_per_story: 0.25\nlimits:\n  max_stories_per_run: 8\n"
        "backfill:\n" + "".join(f"  {k}: \"{v}\"\n" if k in ("from", "to") else f"  {k}: {v}\n"
                                for k, v in CAMPAIGN.items())
    )  # fmt: skip
    monkeypatch.setenv("BUDGET_LEDGER", str(tmp_path / "ledger.json"))
    return budget.main(["--config", str(cfg), *args])


def test_reserve_actual_and_done_rows_all_carry_the_window(tmp_path, monkeypatch, capsys):
    (tmp_path / "ledger.json").write_text('{"runs": []}')
    assert cli(tmp_path, monkeypatch, "reserve", "--runner", "local", "--run-id", "b1",
               "--backfill", W1) == 0  # fmt: skip
    cli(tmp_path, monkeypatch, "actual", "--run-id", "b1", "--stories", "4", "--cost-usd", "1.1")
    cli(tmp_path, monkeypatch, "done", "--run-id", "b1", "--stories", "4")
    rows = json.loads((tmp_path / "ledger.json").read_text())["runs"]
    assert [r["kind"] for r in rows] == ["reserve", "actual", "done"]
    assert {r["backfill"] for r in rows} == {W1}
    capsys.readouterr()
    cli(tmp_path, monkeypatch, "status")
    report = capsys.readouterr().out
    assert f"| local backfill {W1} | `b1` |" in report
    assert "**Backfill 2026-06-01..2026-06-30:** $1.10 charged of $6.00, 1 of 3 runs" in report
    assert f"Finished windows: {W1}." in report


def test_reserve_rechecks_the_campaign(tmp_path, monkeypatch):
    (tmp_path / "ledger.json").write_text('{"runs": []}')
    with pytest.raises(SystemExit, match="outside the approved"):
        cli(tmp_path, monkeypatch, "reserve", "--runner", "local", "--run-id", "b1",
            "--backfill", "2026-07-01..2026-07-05")  # fmt: skip
    assert json.loads((tmp_path / "ledger.json").read_text())["runs"] == []


def test_check_cli_exits_skip_on_refusal(tmp_path, monkeypatch, capsys):
    (tmp_path / "ledger.json").write_text('{"runs": []}')
    assert cli(tmp_path, monkeypatch, "check", "--runner", "local", "--backfill", W1) == 0
    assert cli(tmp_path, monkeypatch, "check", "--runner", "cloud", "--backfill", W1) == 3
    assert "SKIP" in capsys.readouterr().out


# --- Chunking ---------------------------------------------------------------------------
def test_the_gap_splits_into_five_eight_day_chunks():
    got = budget.chunk_windows("2026-09-09", "2026-10-18", 8)
    assert got == [
        ("2026-09-09", "2026-09-16"),
        ("2026-09-17", "2026-09-24"),
        ("2026-09-25", "2026-10-02"),
        ("2026-10-03", "2026-10-10"),
        ("2026-10-11", "2026-10-18"),
    ]


def test_chunks_cover_the_window_exactly_once():
    got = budget.chunk_windows("2026-01-30", "2026-03-02", 7)
    assert got[0][0] == "2026-01-30" and got[-1] == ("2026-02-27", "2026-03-02")
    assert all(a[1] < b[0] for a, b in zip(got, got[1:], strict=False))
    assert budget.chunk_windows("2026-01-01", "2026-01-01", 8) == [("2026-01-01", "2026-01-01")]


@pytest.mark.parametrize("days", [0, 32])
def test_chunk_size_is_bounded(days):
    with pytest.raises(ValueError):
        budget.chunk_windows("2026-01-01", "2026-01-31", days)


def test_the_shipped_campaign_fits_its_chunks():
    """config.yaml's approved campaign: issue #52's gap in 8-day chunks."""
    s = budget.budget_settings()
    cfg = s["backfill"]
    plan = budget.chunk_windows(cfg["from"], cfg["to"], 8)
    assert (cfg["from"], cfg["to"]) == ("2026-09-09", "2026-10-18")
    assert len(plan) < cfg["max_runs"]  # one spare for a failed chunk
    for frm, to in plan:
        assert budget.backfill_window_problem(cfg, f"{frm}..{to}", "2026-10-22") is None
