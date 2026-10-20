"""End-to-end tests for scripts/run_scan.sh in a throwaway repo (ISC-8, ISC-9).

Each test copies scripts/ + config.yaml + .gitignore into a temp git repo
whose origin is a local bare repo, stubs out the ingestors and renderers, and
puts a fake `gh` first on PATH that logs every call. Runs under /bin/bash,
which is bash 3.2 on macOS, the shell launchd uses. No network, no LLM.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
STUBBED = (
    "aggregate ingest_sitemap ingest_github ingest_ghsa ingest_hn ingest_conferences ingest_json_feeds "
    "rerank generate_site generate_claims generate_html generate_og trends "
    "generate_newsletter generate_review add_claim"
).split()
FAKE_GH = """#!/bin/sh
echo "$*" >> "$GH_LOG"
case "$*" in
  *"issues?state=open"*|*"pulls?state=open"*) echo 0 ;;
  *"/labels"*) echo '{"errors":[{"code":"already_exists"}]}'; exit 1 ;;
  *"-X POST"*) echo https://github.com/o/r/pull/1 ;;
esac
"""
SECRET = "ghp_" + "A" * 36


def git(cwd: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return out.stdout.strip()


def set_budget(cfg: Path, **values: str) -> None:
    text = cfg.read_text()
    for key, val in values.items():
        text = re.sub(rf"(?m)^  {key}: \S+", f"  {key}: {val}", text, count=1)
    cfg.write_text(text)


# Every test starts from a closed budget, whatever the real config ships.
CLOSED = {"monthly_cap_usd": "null", "usd_per_story": "null", "uncalibrated_run_usd": "null"}


def commit_main(work: Path, msg: str) -> None:
    git(work, "add", "-A")
    git(work, "commit", "-qm", msg)
    git(work, "push", "-q", "origin", "main")


@pytest.fixture
def scan_repo(tmp_path: Path):
    origin, work, bin_dir = tmp_path / "origin.git", tmp_path / "work", tmp_path / "bin"
    git(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    work.mkdir()
    shutil.copytree(
        REPO / "scripts", work / "scripts", ignore=shutil.ignore_patterns("__pycache__")
    )
    for name in STUBBED:
        (work / "scripts" / f"{name}.py").write_text("print('stub')\n")
    shutil.copy(REPO / "config.yaml", work / "config.yaml")
    set_budget(work / "config.yaml", **CLOSED)
    shutil.copy(REPO / ".gitignore", work / ".gitignore")
    (work / "data").mkdir()
    (work / "data" / "pool.json").write_text("[]")
    (work / "README.md").write_text("v1\n")
    env = {
        **os.environ,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "GH_LOG": str(tmp_path / "gh.log"),
        "PYTHON": sys.executable,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
    }
    for var in ("GITHUB_REPOSITORY", "GITHUB_ACTIONS", "SCAN_ALLOW_REPEAT", "SCAN_RUN_ID"):
        env.pop(var, None)
    os.environ.update({k: env[k] for k in env if k.startswith("GIT_")})
    git(work, "init", "-q", "-b", "main")
    git(work, "remote", "add", "origin", f"file://{origin}")
    commit_main(work, "init")
    bin_dir.mkdir()
    (bin_dir / "gh").write_text(FAKE_GH)
    (bin_dir / "gh").chmod(0o755)
    return work, origin, env


def run_scan(work: Path, env: dict, *args: str, runner: str = "cloud", **extra: str):
    return subprocess.run(
        ["/bin/bash", "scripts/run_scan.sh", *args],
        cwd=work,
        env={**env, "SCAN_RUNNER": runner, **extra},
        capture_output=True,
        text=True,
    )


def ledger_rows(origin: Path) -> list[dict]:
    return json.loads(git(origin, "show", "budget-ledger:budget.json"))["runs"]


def gh_calls(env: dict) -> str:
    log = Path(env["GH_LOG"])
    return log.read_text() if log.exists() else ""


def open_budget(work: Path, **values: str) -> None:
    set_budget(work / "config.yaml", **values)
    commit_main(work, "open budget")


def reserved_run(work: Path, env: dict, run_id: str = "C1") -> None:
    """Open the budget on main and run `pre`, so a reservation exists."""
    open_budget(work, monthly_cap_usd="10.0", usd_per_story="0.25")
    res = run_scan(work, env, "pre", SCAN_RUN_ID=run_id)
    assert res.returncode == 0, res.stdout + res.stderr


def test_pre_skips_before_any_ingest_when_no_cap(scan_repo):
    work, origin, env = scan_repo
    res = run_scan(work, env, "pre")
    assert res.returncode == 0, res.stderr
    assert "SCAN_SKIP" in res.stdout and "monthly_cap_usd" in res.stdout
    assert (work / "data/_scan_skip").exists()
    assert "ingest" not in (work / "data/_scan.log").read_text()
    assert "budget-ledger" not in git(origin, "branch")


def test_working_tree_config_cannot_open_the_budget(scan_repo):
    work, _, env = scan_repo
    set_budget(work / "config.yaml", monthly_cap_usd="100.0", uncalibrated_run_usd="1.0")
    res = run_scan(work, env, "pre", runner="local")  # main still has cap: null
    assert "SCAN_SKIP" in res.stdout and "monthly_cap_usd" in res.stdout


def test_pre_reserves_before_ingest_and_ignores_a_tampered_local_ledger(scan_repo):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    fake = {
        "runs": [
            {
                "run_id": "x",
                "date": "2026-01-01",
                "runner": "local",
                "kind": "actual",
                "stories": 0,
                "cost_usd": -1000,
            }
        ]
    }
    (work / "data/_budget_ledger.json").write_text(json.dumps(fake))
    res = run_scan(work, env, "pre", runner="local", SCAN_RUN_ID="L1")
    assert res.returncode == 0, res.stderr + res.stdout
    rows = ledger_rows(origin)
    assert rows == [{**rows[0], "run_id": "L1", "kind": "reserve", "cost_usd": 2.0}]
    log = (work / "data/_scan.log").read_text()
    assert log.index("ledger: reserve recorded") < log.index("ingest ok")


def test_a_runner_does_not_retry_its_own_day(scan_repo):
    work, _, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    assert run_scan(work, env, "pre", runner="local", SCAN_RUN_ID="L1").returncode == 0
    res = run_scan(work, env, "check", runner="local")
    assert res.returncode == 3 and "already tried" in res.stdout


def test_check_fails_closed_when_the_ledger_is_unreachable(scan_repo, tmp_path):
    work, _, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    git(work, "remote", "set-url", "origin", f"file://{tmp_path}/gone.git")
    res = run_scan(work, env, "check", runner="local")
    assert res.returncode not in (0, 3) and "GO" not in res.stdout


def test_actual_replaces_the_reservation_on_the_remote_ledger(scan_repo):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    assert run_scan(work, env, "pre", runner="local", SCAN_RUN_ID="L1").returncode == 0
    res = run_scan(work, env, "actual", "L1", "3", "1.25", runner="local")
    assert res.returncode == 0, res.stderr
    kinds = [(r["kind"], r["cost_usd"]) for r in ledger_rows(origin)]
    assert kinds == [("reserve", 2.0), ("actual", 1.25)]
    assert git(origin, "rev-list", "--count", "budget-ledger") == "2"
    assert git(work, "branch", "--show-current") == "main"
    report = git(origin, "show", "budget-ledger:SPEND.md")
    assert "$1.25 charged of $10.00" in report and "| measured |" in report
    status = run_scan(work, env, "status", runner="local")
    assert status.returncode == 0 and "$1.25 charged of $10.00" in status.stdout


def test_fail_alert_never_publishes_log_text(scan_repo):
    work, _, env = scan_repo
    (work / "data/_scan.log").write_text(f"leaked {SECRET}\n")
    res = run_scan(work, env, "fail", "analysis")
    assert res.returncode == 0, res.stderr
    calls = gh_calls(env)
    assert "/issues -f title=Daily scan failing (cloud, analysis)" in calls
    assert SECRET not in calls


def test_post_over_story_cap_fails_and_alerts(scan_repo):
    work, _, env = scan_repo
    reserved_run(work, env)
    (work / "data/analysis_out.json").write_text(json.dumps([{"t": i} for i in range(9)]))
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    assert "over the per-run cap of 8" in (work / "data/_scan.log").read_text()
    assert "labels=scan-failure" in gh_calls(env)


def test_post_counts_entries_merged_past_the_last_analysis_out(scan_repo):
    work, _, env = scan_repo
    reserved_run(work, env)
    (work / "data/analysis_out.json").write_text("[]")
    pool = {"topic": "ai-security", "entries": [{"id": f"e{i}"} for i in range(9)]}
    (work / "data/ai-security.json").write_text(json.dumps(pool))
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    assert "analyzed 9 stories, over the per-run cap of 8" in (work / "data/_scan.log").read_text()


def test_post_commits_with_ignored_files_present_and_scrubs_the_body(scan_repo):
    work, origin, env = scan_repo
    reserved_run(work, env)
    for ignored in ("candidates.json", "analysis_out.json", "_budget_ledger.json"):
        (work / "data" / ignored).write_text("[]")
    (work / "data/_summary.md").write_text(f"Summary with {SECRET}")
    (work / "README.md").write_text("v2\n")
    res = run_scan(work, env, "post")
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    branch = f"claude/scan-{day}-cloud"
    assert git(origin, "show", f"{branch}:README.md") == "v2"
    files = git(origin, "ls-tree", "-r", "--name-only", branch)
    assert "data/candidates.json" not in files and "data/_summary.md" not in files
    calls = gh_calls(env)
    assert "-X POST repos/" in calls and "/pulls" in calls
    assert SECRET not in calls and "withheld" in calls
    assert "Spend this month:** $2.00 charged of $10.00" in calls  # 8 stories x $0.25 reserved
    assert "/blob/budget-ledger/SPEND.md" in calls and "https://github.com/" in calls
    assert [r["kind"] for r in ledger_rows(origin)] == ["reserve", "done"]
