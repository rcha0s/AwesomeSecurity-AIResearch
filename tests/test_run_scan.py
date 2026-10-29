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
    "ingest_curator_links ingest_reddit aggregate ingest_sitemap ingest_github ingest_ghsa ingest_hn "
    "ingest_conferences ingest_json_feeds "
    "rerank generate_site generate_claims generate_html generate_og trends "
    "generate_newsletter generate_review add_claim eval_recall"
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
# ...and from the per-run caps these tests count against (10 stories, the news
# tier off), whatever the real config ships; news-tier tests open it themselves.
PINNED = {"max_stories_per_run": "10", "max_news_per_run": "0"}


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
    set_budget(work / "config.yaml", **CLOSED, **PINNED)
    shutil.copy(REPO / ".gitignore", work / ".gitignore")
    (work / "data").mkdir()
    (work / "data" / "pool.json").write_text("[]")
    # The vocabulary is load-bearing config like config.yaml: common imports it.
    shutil.copy(REPO / "data" / "taxonomy.yaml", work / "data" / "taxonomy.yaml")
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


def merged(work: Path, n: int) -> None:
    """merge_analysis.py's code-owned record: it merged `n` entries."""
    rec = {"merged": n, "new": n, "updated": 0, "skipped_invalid": 0}
    (work / "data/_merge_outcomes.json").write_text(json.dumps(rec))


def analyzed(work: Path, n: int = 1) -> None:
    """The session analyzed and merged `n` stories (what post requires to ship a PR)."""
    (work / "data/analysis_out.json").write_text(json.dumps([{"id": f"a{i}"} for i in range(n)]))
    merged(work, n)


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


def test_actual_refuses_a_cloud_runs_reservation(scan_repo):
    """A cloud run can't read its cost, so it stays charged its ceiling: an
    `actual` row would cut that charge and feed the per-story calibration."""
    work, origin, env = scan_repo
    reserved_run(work, env, "C1")  # cloud reservation, $0.25/story x cap
    for runner in ("cloud", "local"):
        res = run_scan(work, env, "actual", "C1", "10", "0.01", runner=runner)
        assert res.returncode != 0
    assert [r["kind"] for r in ledger_rows(origin)] == ["reserve"]


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
    (work / "data/analysis_out.json").write_text(json.dumps([{"t": i} for i in range(11)]))
    merged(work, 11)
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    assert "over the per-run cap of 10" in (work / "data/_scan.log").read_text()
    assert "labels=scan-failure" in gh_calls(env)


def test_post_counts_entries_merged_past_the_last_analysis_out(scan_repo):
    work, _, env = scan_repo
    reserved_run(work, env)
    (work / "data/analysis_out.json").write_text("[]")
    merged(work, 11)
    pool = {"topic": "ai-security", "entries": [{"id": f"e{i}"} for i in range(11)]}
    (work / "data/ai-security.json").write_text(json.dumps(pool))
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    assert (
        "analyzed 11 stories, over the per-run cap of 10" in (work / "data/_scan.log").read_text()
    )


def test_post_commits_with_ignored_files_present_and_scrubs_the_body(scan_repo):
    work, origin, env = scan_repo
    reserved_run(work, env)
    for ignored in ("candidates.json", "analysis_out.json", "_budget_ledger.json"):
        (work / "data" / ignored).write_text("[]")
    analyzed(work)
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
    assert "Spend this month:** $2.50 charged of $10.00" in calls  # 10 stories x $0.25 reserved
    assert "/blob/budget-ledger/SPEND.md" in calls and "https://github.com/" in calls
    assert [r["kind"] for r in ledger_rows(origin)] == ["reserve", "done"]


def test_post_puts_the_code_owned_story_record_in_the_pr_body(scan_repo):
    work, origin, env = scan_repo
    reserved_run(work, env)
    record = "### Story verdicts (applied by merge_analysis.py)\n\n1 same\n"
    settled = "- `same`: https://x.example/a -> story `s1`\n"  # verdicts alone are work
    (work / "data/_story_outcomes.md").write_text(record + f"- `same`: {SECRET}\n")
    (work / "data/_summary.md").write_text("Model summary.")
    (work / "README.md").write_text("v2\n")
    res = run_scan(work, env, "post")
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    calls = gh_calls(env)
    assert "Model summary." in calls and SECRET not in calls  # scrubbed like the summary
    files = git(
        origin, "ls-tree", "-r", "--name-only", f"claude/scan-{datetime.now(UTC):%Y-%m-%d}-cloud"
    )
    assert "data/_story_outcomes.md" not in files
    (work / "data/_story_outcomes.md").write_text(record + settled)
    (work / "README.md").write_text("v3\n")
    res = run_scan(work, env, "post")
    assert "Story verdicts (applied by merge_analysis.py)" in gh_calls(env)


def test_pre_clears_a_stale_story_record(scan_repo):
    work, origin, env = scan_repo
    (work / "data/_story_outcomes.md").write_text("stale")
    (work / "data/_editorial_outcomes.md").write_text("stale")
    reserved_run(work, env)
    assert not (work / "data/_story_outcomes.md").exists()
    assert not (work / "data/_editorial_outcomes.md").exists()


def test_post_puts_the_editorial_record_in_the_pr_body_and_not_the_commit(scan_repo):
    """Every promotion and removal reaches the reviewer (sticky promotions, #82)."""
    work, origin, env = scan_repo
    reserved_run(work, env)
    record = "### Editorial decisions (applied by promote_editorial.py)\n\n- DEMOTED: X: dup\n"
    (work / "data/_editorial_outcomes.md").write_text(record + f"- promoted: {SECRET}\n")
    (work / "README.md").write_text("v2\n")
    analyzed(work)
    res = run_scan(work, env, "post")
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    assert SECRET not in gh_calls(env)  # scrubbed like the summary
    files = git(
        origin, "ls-tree", "-r", "--name-only", f"claude/scan-{datetime.now(UTC):%Y-%m-%d}-cloud"
    )
    assert "data/_editorial_outcomes.md" not in files
    (work / "data/_editorial_outcomes.md").write_text(record)
    (work / "README.md").write_text("v3\n")
    res = run_scan(work, env, "post")
    calls = gh_calls(env)
    assert "Editorial decisions (applied by promote_editorial.py)" in calls
    assert "- DEMOTED: X: dup" in calls


def test_post_records_the_cost_eval_and_ships_only_its_own_eval_files(scan_repo):
    """ISC-25/26: the PR body carries the run's numbers and trend; data/evals is
    reset to main's before post appends, so files the session wrote never ship."""
    work, origin, env = scan_repo
    evals = work / "data" / "evals"
    evals.mkdir()
    (evals / "history.json").write_text(json.dumps({"runs": []}))
    commit_main(work, "evals dir")
    reserved_run(work, env)
    assert (work / "data/_scan_candidates").read_text().strip() == "0"
    (evals / "history.json").write_text(json.dumps({"runs": [{"run_id": "forged"}]}))
    (evals / "golden-2099-01-01.json").write_text('{"score": 1.0}')
    (work / "README.md").write_text("v2\n")
    analyzed(work)
    res = run_scan(work, env, "post")
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    branch = f"claude/scan-{datetime.now(UTC).strftime('%Y-%m-%d')}-cloud"
    files = git(origin, "ls-tree", "-r", "--name-only", branch)
    assert "data/evals/golden-2099-01-01.json" not in files
    rows = json.loads(git(origin, "show", f"{branch}:data/evals/history.json"))["runs"]
    assert [r["run_id"] for r in rows] == ["C1"]
    assert rows[0]["cost_usd"] == 2.5 and rows[0]["candidates"] == 0
    assert (rows[0]["cost_basis"], rows[0]["ceiling_usd"]) == ("reserved", 2.5)
    assert rows[0]["recall"] is None  # the stubbed fetch wrote nothing; no tree file stands in
    assert [f for f in files.split() if f.startswith("data/evals/")] == ["data/evals/history.json"]
    assert rows[0]["integrity"]["passed"] is False  # no rendered site in this repo
    calls = gh_calls(env)
    assert "**Run numbers:** 0 candidates staged" in calls and "LLM calls:" in calls
    assert (
        "| Date | Runner | Candidates | Stories | Kept | Recall (independent) | Charged | Gate |"
        in calls
    )
    assert "Spend this month:**" in calls
    # The cloud can't measure its cost: the body says reserved, honestly.
    assert "charged $2.50 (reserved; reserved ceiling $2.50" in calls


# An ingestor stub that stages 20 neutral candidates, best source rank last.
STAGE_20 = """import json, datetime
day = datetime.date.today().isoformat()
cands = [{"id": f"c{i:02d}", "title": f"Neutral finding {i} about topic{i}",
          "source_url": f"https://ex{i}.example/p", "article_url": f"https://ex{i}.example/p",
          "published": day, "source_rank": float(i * 3)} for i in range(20)]
json.dump(cands, open("data/candidates.json", "w"))
"""


def test_pre_hands_the_session_only_this_runs_batch(scan_repo):
    work, _, env = scan_repo
    (work / "scripts/aggregate.py").write_text(STAGE_20)
    reserved_run(work, env)
    data = work / "data"
    ids = {c["id"] for c in json.loads((data / "candidates.json").read_text())}
    assert ids == {f"c{i:02d}" for i in range(6, 20)}  # 10 stories + margin 4, best rank
    backlog = json.loads((data / "_scan_backlog.json").read_text())
    assert {c["id"] for c in backlog} == {f"c{i:02d}" for i in range(6)}  # kept, not lost
    assert set(json.loads((data / "_scan_urls.json").read_text())) == ids  # fetchable
    assert set(json.loads((data / "story_shortlist.json").read_text())) == ids  # judged
    assert (data / "_scan_candidates").read_text().strip() == "20"  # ingested, for the eval
    assert (
        "SCAN_READY: 14 candidates in this run's batch (20 ingested)"
        in (data / "_scan.log").read_text()
    )


def test_post_without_analysis_fails_and_opens_no_pr(scan_repo):
    """2026-10-20: the session analyzed nothing and post shipped the rerank's
    prune as a "0 stories" scan PR anyway. An analysis_out.json that never
    merged is not work either: only merge_analysis.py's record counts."""
    work, origin, env = scan_repo
    reserved_run(work, env)
    (work / "data/analysis_out.json").write_text(json.dumps([{"id": "a"}, {"id": "b"}]))
    (work / "README.md").write_text("v2\n")  # a rerank's drift alone
    res = run_scan(work, env, "post")
    assert res.returncode == 4
    calls = gh_calls(env)
    assert "Daily scan failing (cloud, analysis-empty)" in calls
    assert "/pulls" not in calls
    assert "claude/scan-" not in git(origin, "branch", "-a")
    assert [r["kind"] for r in ledger_rows(origin)] == ["reserve"]  # the day isn't done
    assert "SCAN_FAILED" in (work / "data/_scan.log").read_text()


def test_post_does_not_count_archived_entries_rerank_restored(scan_repo):
    work, origin, env = scan_repo
    (work / "data/archive.json").write_text(json.dumps([{"id": "old-news"}]))
    commit_main(work, "archive")
    reserved_run(work, env)
    pool = {"topic": "ai-security", "entries": [{"id": "old-news"}, {"id": "fresh"}]}
    (work / "data/ai-security.json").write_text(json.dumps(pool))
    analyzed(work)
    res = run_scan(work, env, "post")
    assert res.returncode == 0, res.stderr + (work / "data/_scan.log").read_text()
    rows = [(r["kind"], r["stories"]) for r in ledger_rows(origin)]
    assert rows == [("reserve", 0), ("done", 1)]
