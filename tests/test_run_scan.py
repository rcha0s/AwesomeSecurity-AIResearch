"""End-to-end tests for scripts/run_scan.sh in a throwaway repo (ISC-8, ISC-9).

Each test copies scripts/ + config.yaml into a temp git repo whose origin is a
local bare repo, and puts a fake `gh` first on PATH that logs every call. No
network, no LLM, no real GitHub.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FAKE_GH = """#!/bin/sh
echo "$*" >> "$GH_LOG"
case "$*" in
  *"issues?state=open"*|*"pulls?state=open"*) echo 0 ;;
  *"-X POST"*) echo https://github.com/o/r/issues/1 ;;
esac
"""


def git(cwd: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return out.stdout.strip()


@pytest.fixture
def scan_repo(tmp_path: Path):
    origin, work, bin_dir = tmp_path / "origin.git", tmp_path / "work", tmp_path / "bin"
    git(tmp_path, "init", "-q", "--bare", str(origin))
    work.mkdir()
    shutil.copytree(REPO / "scripts", work / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(REPO / "config.yaml", work / "config.yaml")
    (work / "data").mkdir()
    git(work, "init", "-q", "-b", "main")
    git(work, "remote", "add", "origin", f"file://{origin}")
    git(work, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "init")
    bin_dir.mkdir()
    (bin_dir / "gh").write_text(FAKE_GH)
    (bin_dir / "gh").chmod(0o755)
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
    env.pop("GITHUB_REPOSITORY", None)
    env.pop("GITHUB_ACTIONS", None)
    return work, origin, env


def run_scan(work: Path, env: dict, *args: str, runner: str = "cloud"):
    return subprocess.run(
        ["/bin/bash", "scripts/run_scan.sh", *args],
        cwd=work,
        env={**env, "SCAN_RUNNER": runner},
        capture_output=True,
        text=True,
    )


def set_cap(work: Path, cap: str) -> None:
    cfg = work / "config.yaml"
    cfg.write_text(cfg.read_text().replace("monthly_cap_usd: null", f"monthly_cap_usd: {cap}"))


def gh_calls(env: dict) -> str:
    log = Path(env["GH_LOG"])
    return log.read_text() if log.exists() else ""


def test_pre_skips_before_any_ingest_when_no_cap(scan_repo):
    work, _, env = scan_repo
    res = run_scan(work, env, "pre")
    assert res.returncode == 0, res.stderr
    assert "SCAN_SKIP" in res.stdout and "monthly_cap_usd" in res.stdout
    assert (work / "data/_scan_skip").exists()
    assert "ingest" not in (work / "data/_scan.log").read_text()


def test_pre_skips_when_month_is_spent(scan_repo):
    work, _, env = scan_repo
    set_cap(work, "1.0")
    month = subprocess.run(["date", "-u", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    ledger = {"runs": [{"date": month, "runner": "local", "stories": 4, "cost_usd": 1.0, "measured": True}]}
    (work / "data/_budget_ledger.json").write_text(json.dumps(ledger))
    assert run_scan(work, env, "ledger-push").returncode == 0
    (work / "data/_budget_ledger.json").unlink()
    res = run_scan(work, env, "pre", runner="local")
    assert res.returncode == 0, res.stderr
    assert "exhausted" in res.stdout and (work / "data/_scan_skip").exists()


def test_ledger_push_creates_then_appends_branch(scan_repo):
    work, origin, env = scan_repo
    (work / "data/_budget_ledger.json").write_text('{"runs": []}')
    assert run_scan(work, env, "ledger-push").returncode == 0
    assert run_scan(work, env, "ledger-push").returncode == 0
    assert git(origin, "rev-list", "--count", "budget-ledger") == "2"
    assert git(origin, "show", "budget-ledger:budget.json") == '{"runs": []}'
    assert git(work, "branch", "--show-current") == "main"  # checkout untouched


def test_fail_opens_scan_failure_issue(scan_repo):
    work, _, env = scan_repo
    res = run_scan(work, env, "fail", "analysis")
    assert res.returncode == 0, res.stderr
    calls = gh_calls(env)
    assert "issues?state=open&labels=scan-failure" in calls
    assert "-X POST repos/" in calls and "/issues -f title=Daily scan failing (cloud, analysis)" in calls


def test_post_over_story_cap_fails_and_alerts(scan_repo):
    work, _, env = scan_repo
    entries = [{"title": f"t{i}"} for i in range(9)]  # default cap is 8
    (work / "data/analysis_out.json").write_text(json.dumps(entries))
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    assert "over the per-run cap of 8" in (work / "data/_scan.log").read_text()
    assert "labels=scan-failure" in gh_calls(env)
