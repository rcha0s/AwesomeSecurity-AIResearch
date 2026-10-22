"""Backfill end to end in a throwaway repo (issue #52): run_scan.sh labels and
ships a backfill chunk like a scan, run_scan_local.sh never retries one, and
scripts/backfill.sh drives the chunks in order, once each, waiting for each
PR. Fake gh, claude and launchctl; no network, no LLM. Runs under /bin/bash."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from test_run_scan import analyzed, git, ledger_rows, open_budget, run_scan
from test_run_scan_local import run_local

WINDOW = {"SCAN_BACKFILL_FROM": "2026-09-09", "SCAN_BACKFILL_TO": "2026-09-16"}
LABEL = "2026-09-09..2026-09-16"


def backfill_pre(work: Path, env: dict, runner: str = "local", run_id: str = "B1"):
    return run_scan(work, env, "pre", runner=runner, SCAN_RUN_ID=run_id, **WINDOW)


def test_a_backfill_chunk_is_reserved_labelled_and_ships_its_own_branch(scan_repo):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="100.0", uncalibrated_run_usd="2.0")
    res = backfill_pre(work, env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert (
        "SCAN_SKIP" not in res.stdout and "backfill 2026-09-09..2026-09-16, run 1 of" in res.stdout
    )
    assert [r.get("backfill") for r in ledger_rows(origin)] == [LABEL]
    analyzed(work)
    (work / "README.md").write_text("v2\n")
    res = run_scan(work, env, "post", runner="local", **WINDOW)
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    branch = f"claude/scan-{day}-backfill-2026-09-09-2026-09-16"
    assert git(origin, "show", f"{branch}:README.md") == "v2"
    assert "chore: backfill scan (local, " in git(origin, "log", "-1", "--format=%s", branch)
    calls = Path(env["GH_LOG"]).read_text()
    assert (
        "title=chore: backfill scan (local, " in calls and "**Backfill:** items published" in calls
    )
    assert [(r["kind"], r.get("backfill")) for r in ledger_rows(origin)] == [
        ("reserve", LABEL),
        ("done", LABEL),
    ]
    # Not the day's scan: the daily local check still says GO today ...
    assert run_scan(work, env, "check", runner="local").returncode == 0
    # ... and the finished window can't run again.
    again = backfill_pre(work, env, run_id="B2")
    assert "SCAN_SKIP" in again.stdout and "already finished" in again.stdout


def test_a_cloud_backfill_is_refused_before_any_ingest(scan_repo):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="100.0", usd_per_story="0.25")
    res = backfill_pre(work, env, runner="cloud")
    assert "SCAN_SKIP" in res.stdout and "local runner" in res.stdout
    assert "ingest" not in (work / "data/_scan.log").read_text()


def test_a_bad_window_is_refused_before_any_ingest(scan_repo):
    work, _, env = scan_repo
    open_budget(work, monthly_cap_usd="100.0", uncalibrated_run_usd="2.0")
    res = run_scan(
        work, env, "pre", runner="local", SCAN_BACKFILL_FROM="2026-09-09", SCAN_BACKFILL_TO="x"
    )
    assert "SCAN_SKIP" in res.stdout and "YYYY-MM-DD" in res.stdout
    assert "ingest" not in (work / "data/_scan.log").read_text()


def test_the_local_wrapper_never_retries_a_backfill_chunk(scan_repo, tmp_path):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="100.0", uncalibrated_run_usd="0.5", retry_max_usd="5.0")
    res, _ = run_local(work, env, tmp_path, **WINDOW)  # no analysis: post says analysis-empty
    assert res.returncode == 1, res.stdout + res.stderr
    assert (tmp_path / "claude-args.calls").read_text().count("call") == 1
    ids = {r["run_id"] for r in ledger_rows(origin)}
    assert len(ids) == 1 and next(iter(ids)).startswith("local-backfill-20260909-20260916-")
    assert {r.get("backfill") for r in ledger_rows(origin)} == {LABEL}


def test_the_local_wrapper_exits_3_when_the_guard_skips_a_chunk(scan_repo, tmp_path):
    work, _, env = scan_repo  # closed budget
    res, args = run_local(work, env, tmp_path, **WINDOW)
    assert res.returncode == 3 and args == []
    assert "skip backfill 2026-09-09..2026-09-16" in (work / "data/_scan.log").read_text()


# --- scripts/backfill.sh -----------------------------------------------------------------
FAKE_SCAN = """#!/bin/bash
# Stands in for run_scan_local.sh: logs the chunk, proves stdin is empty, and
# exits with the next code from FAKE_RCS (one per call).
touch "$CALLS"; n=$(( $(wc -l < "$CALLS") + 1 ))
echo "$SCAN_BACKFILL_FROM $SCAN_BACKFILL_TO stdin=$(cat | wc -c | tr -d ' ')" >> "$CALLS"
set -- $FAKE_RCS
eval "exit \\${$n:-0}"
"""
FAKE_GH = """#!/bin/sh
# Open PR refs: chunk 1's branch while the poll count is under OPEN_POLLS.
echo "$*" >> "$GH_LOG"
case "$*" in
  *"pulls?state=open"*)
    n=$(( $(cat "$POLLS" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$POLLS"
    if [ "$n" -le "${OPEN_POLLS:-0}" ]; then echo "claude/scan-2026-10-22-backfill-2026-09-09-2026-09-16"; fi
    echo "claude/scan-2026-10-22-local" ;;
esac
"""
FAKE_LAUNCHCTL = """#!/bin/sh
echo "$*" >> "$LAUNCHCTL_LOG"
case "$1" in print) exit "${LOADED:-1}" ;; esac
"""


def driver_env(work: Path, env: dict, tmp: Path, **more: str) -> dict:
    for name, body in (("run_scan_local.sh", FAKE_SCAN),):
        (work / "scripts" / name).write_text(body)
    fakes = tmp / "fakes"
    fakes.mkdir(exist_ok=True)
    for name, body in (("gh", FAKE_GH), ("launchctl", FAKE_LAUNCHCTL)):
        (fakes / name).write_text(body)
        (fakes / name).chmod(0o755)
    return {
        **env,
        "PATH": f"{fakes}:{env['PATH']}",
        "PYTHON": sys.executable,
        "HOME": str(tmp / "home"),
        "CALLS": str(tmp / "calls"),
        "POLLS": str(tmp / "polls"),
        "LAUNCHCTL": str(fakes / "launchctl"),
        "LAUNCHCTL_LOG": str(tmp / "launchctl.log"),
        "BACKFILL_PLIST": str(tmp / "job.plist"),
        "BACKFILL_POLL_SECONDS": "1",
        **more,
    }


def drive(work: Path, denv: dict, *args: str):
    return subprocess.run(
        ["/bin/bash", "scripts/backfill.sh", *args],
        cwd=work,
        env=denv,
        capture_output=True,
        text=True,
        timeout=60,
    )


def chunks_run(tmp: Path) -> list[str]:
    path = tmp / "calls"
    return path.read_text().splitlines() if path.exists() else []


def test_the_driver_runs_every_chunk_once_in_order_then_unloads_itself(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path)
    (tmp_path / "job.plist").write_text("<plist/>")
    res = drive(work, denv, "run", "2026-09-09", "2026-10-18", "8")
    assert res.returncode == 0, res.stdout + res.stderr
    assert chunks_run(tmp_path) == [
        "2026-09-09 2026-09-16 stdin=0",  # stdin=0: the session can't eat the plan
        "2026-09-17 2026-09-24 stdin=0",
        "2026-09-25 2026-10-02 stdin=0",
        "2026-10-03 2026-10-10 stdin=0",
        "2026-10-11 2026-10-18 stdin=0",
    ]
    log = (work / "data/_scan.log").read_text()
    assert "[backfill] finished 2026-09-09..2026-10-18" in log
    assert (
        f"bootout gui/{os.getuid()}/com.rcha0s.awesomesecurity.backfill"
        in (tmp_path / "launchctl.log").read_text()
    )
    assert not (tmp_path / "job.plist").exists()
    assert not (work / "data/_backfill.lock").exists()


def test_a_skipped_chunk_is_passed_over_and_a_failure_stops_the_driver(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path, FAKE_RCS="0 3 1 0 0")
    res = drive(work, denv, "run", "2026-09-09", "2026-10-18", "8")
    assert res.returncode == 1
    assert [x.split()[0] for x in chunks_run(tmp_path)] == [
        "2026-09-09",
        "2026-09-17",
        "2026-09-25",
    ]
    log = (work / "data/_scan.log").read_text()
    assert "chunk 2026-09-17..2026-09-24: skipped by the budget guard" in log
    assert "chunk 2026-09-25..2026-10-02: FAILED (exit 1); stopping" in log
    assert "bootout" in (tmp_path / "launchctl.log").read_text()  # one-shot even on failure


def test_the_next_chunk_waits_for_the_previous_pr(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path, OPEN_POLLS="2")
    res = drive(work, denv, "run", "2026-09-09", "2026-09-24", "8")
    assert res.returncode == 0, res.stdout + res.stderr
    assert len(chunks_run(tmp_path)) == 2
    assert int((tmp_path / "polls").read_text()) == 4  # 3 for chunk 1 (2 open), 1 for chunk 2
    assert "waiting for its PR to be merged or closed" in (work / "data/_scan.log").read_text()


def test_a_pr_left_open_past_the_wait_stops_the_driver(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path, OPEN_POLLS="999", BACKFILL_WAIT_SECONDS="2")
    res = drive(work, denv, "run", "2026-09-09", "2026-09-24", "8")
    assert res.returncode == 1
    assert len(chunks_run(tmp_path)) == 1
    assert "still open after 2s; stopping" in (work / "data/_scan.log").read_text()


def test_an_unreadable_pr_list_is_not_read_as_merged(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path, BACKFILL_WAIT_SECONDS="2")
    (Path(denv["PATH"].split(":")[0]) / "gh").write_text("#!/bin/sh\nexit 1\n")
    res = drive(work, denv, "run", "2026-09-09", "2026-09-24", "8")
    assert res.returncode == 1 and len(chunks_run(tmp_path)) == 1


def test_a_second_driver_is_refused_while_one_runs(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path)
    (work / "data/_backfill.lock").mkdir(parents=True)
    (work / "data/_backfill.lock/pid").write_text(str(os.getpid()))  # alive
    res = drive(work, denv, "run", "2026-09-09", "2026-09-16", "8")
    assert res.returncode == 1 and "another backfill driver is running" in res.stderr
    assert chunks_run(tmp_path) == []


def test_a_dead_drivers_lock_is_taken_over(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path)
    (work / "data/_backfill.lock").mkdir(parents=True)
    (work / "data/_backfill.lock/pid").write_text("999999")
    assert drive(work, denv, "run", "2026-09-09", "2026-09-16", "8").returncode == 0
    assert len(chunks_run(tmp_path)) == 1


def test_plan_prints_the_chunks_and_rejects_bad_arguments(scan_repo, tmp_path):
    work, _, env = scan_repo
    denv = driver_env(work, env, tmp_path)
    res = drive(work, denv, "plan", "2026-09-09", "2026-10-18")
    assert (
        res.stdout.splitlines()[0] == "2026-09-09 2026-09-16" and len(res.stdout.splitlines()) == 5
    )
    for bad in (("2026-9-9", "2026-10-18"), ("2026-09-09", "2026-10-18", "x"), ("2026-09-09",)):
        assert drive(work, denv, "plan", *bad).returncode != 0


def test_start_boots_a_one_shot_job_from_the_runner_clone(scan_repo, tmp_path):
    work, origin, env = scan_repo
    runner = tmp_path / "runner"
    git(tmp_path, "clone", "-q", f"file://{origin}", str(runner))
    denv = driver_env(work, env, tmp_path, SCAN_RUNNER_HOME=str(runner))
    res = drive(work, denv, "start", "2026-09-09", "2026-10-18", "8")
    assert res.returncode == 0, res.stdout + res.stderr
    plist = (tmp_path / "job.plist").read_text()
    assert "<key>RunAtLoad</key><true/>" in plist and "<key>KeepAlive</key><false/>" in plist
    assert "StartCalendarInterval" not in plist  # no schedule: it never runs again
    assert (
        f"cd '{runner}' || exit 1; exec /bin/bash scripts/backfill.sh run 2026-09-09 2026-10-18 8"
        in plist
    )
    calls = (tmp_path / "launchctl.log").read_text()
    assert f"bootstrap gui/{os.getuid()} {tmp_path / 'job.plist'}" in calls
    assert "Guard for the first chunk (2026-09-09..2026-09-16)" in res.stdout
    # Already loaded: refuse, never a second job.
    again = drive(work, {**denv, "LOADED": "0"}, "start", "2026-09-09", "2026-10-18", "8")
    assert again.returncode == 1 and "already running" in again.stderr


def test_stop_unloads_the_job_and_clears_the_lock(scan_repo, tmp_path):
    work, _, env = scan_repo
    runner = tmp_path / "runner"
    (runner / "data/_backfill.lock").mkdir(parents=True)
    denv = driver_env(work, env, tmp_path, SCAN_RUNNER_HOME=str(runner))
    (tmp_path / "job.plist").write_text("<plist/>")
    res = drive(work, denv, "stop")
    assert res.returncode == 0
    assert "bootout" in (tmp_path / "launchctl.log").read_text()
    assert not (tmp_path / "job.plist").exists() and not (runner / "data/_backfill.lock").exists()


def test_the_shipped_config_approves_issue_52s_gap():
    cfg = json.loads(
        subprocess.run(
            [sys.executable, "-c", "import sys,json;sys.path.insert(0,'scripts');import budget;"
             "print(json.dumps(budget.budget_settings()['backfill']))"],  # fmt: skip
            capture_output=True,
            text=True,
            check=True,
            cwd=Path(__file__).resolve().parent.parent,
        ).stdout
    )
    assert cfg["from"] == "2026-09-09" and cfg["to"] == "2026-10-18"
