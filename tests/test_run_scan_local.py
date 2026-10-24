"""End-to-end test of scripts/run_scan_local.sh with a fake `claude` (ISC-7/8).

The wrapper, not the model, must run check -> pre -> analysis -> post ->
actual, launch the session locked down, and record the measured cost even
when the session fails.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import content_checks
import pytest
from test_run_scan import SECRET, gh_calls, git, ledger_rows, open_budget

FAKE_CLAUDE = """#!/bin/sh
printf '%s\\n' "$@" > "$CLAUDE_ARGS"
echo "SCAN_LOCKED=$SCAN_LOCKED" >> "$CLAUDE_ARGS.env"
echo call >> "$CLAUDE_ARGS.calls"
# FAKE_ANALYSIS_ON_RETRY: analyze only on the second session of the day.
if [ -n "$FAKE_ANALYSIS_ON_RETRY" ] && [ "$(wc -l < "$CLAUDE_ARGS.calls")" -ge 2 ]; then
  FAKE_ANALYSIS=1
fi
if [ -n "$FAKE_ANALYSIS" ]; then
  echo '[{"id": "a"}, {"id": "b"}]' > data/analysis_out.json
  echo '{"merged": 2, "new": 2}' > data/_merge_outcomes.json  # as merge_analysis.py writes
fi
# FAKE_TOUCH: change a published file, so post has something to open a PR for.
if [ -n "$FAKE_TOUCH" ]; then echo changed >> README.md; fi
printf '{"total_cost_usd": 0.42, "subtype": "%s", "num_turns": 7, "result": "%s"}' \\
  "${FAKE_SUBTYPE:-success}" "${FAKE_RESULT:-Analyzed the batch.}"
exit "${FAKE_CLAUDE_RC:-0}"
"""


def run_local(work: Path, env: dict, tmp: Path, rc: int = 0, **more: str):
    fake = tmp / "fake-claude"
    fake.write_text(FAKE_CLAUDE)
    fake.chmod(0o755)
    extra = {
        "CLAUDE_BIN": str(fake),
        "CLAUDE_ARGS": str(tmp / "claude-args"),
        "FAKE_CLAUDE_RC": str(rc),
        "SCAN_WORKTREE": str(tmp / "scan-worktree"),
        "HOME": str(tmp / "home"),  # nothing a test runs may touch the real home
        **more,
    }
    res = subprocess.run(
        ["/bin/bash", "scripts/run_scan_local.sh"],
        cwd=work,
        env={**env, **extra},
        capture_output=True,
        text=True,
    )
    args_file = tmp / "claude-args"
    return res, (args_file.read_text().splitlines() if args_file.exists() else [])


@pytest.mark.parametrize("claude_rc", [0, 1])
def test_wrapper_owns_the_phases_and_records_cost_on_every_outcome(scan_repo, tmp_path, claude_rc):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, args = run_local(work, env, tmp_path, rc=claude_rc, FAKE_ANALYSIS="1")
    assert (res.returncode == 0) == (claude_rc == 0), res.stdout + res.stderr
    assert args[0] == "-p" and "wrapped mode" in args[1]
    assert (tmp_path / "claude-args.env").read_text().strip() == "SCAN_LOCKED=1"
    flag = dict(zip(args, args[1:], strict=False))
    assert flag["--permission-mode"] == "dontAsk"
    assert '"Edit(data/_raw/**)"' in "\n".join(args)  # model can't forge source text
    assert '"Edit(data/evals/**)"' in "\n".join(args)  # nor its own eval results
    assert "Read(data/evals/**)" not in "\n".join(args)  # golden-only tightening
    assert '"Edit(data/_scan*)"' in "\n".join(args)  # the batch cut + backlog
    assert '"Read(data/_scan_backlog.json)"' in "\n".join(args)  # the batch is the job
    assert '"Edit(data/_curator_arxiv.json)"' in "\n".join(args)  # the paper gate's input
    # what post's --work reads, and the editorial record post puts in the PR body
    code_owned = ("_story_outcomes.md", "_merge_outcomes.json", "_editorial_outcomes.md")
    for denied in ("news_stories.json", "story_shortlist.json", *code_owned):
        assert f'"Edit(data/{denied})"' in "\n".join(args)  # the story guard's inputs
    assert flag["--append-system-prompt-file"] == ".claude/skills/daily-scan/SKILL.md"
    assert flag["--setting-sources"] == "local"
    assert "--strict-mcp-config" in args and flag["--disallowedTools"] == "mcp__*"
    assert flag["--max-budget-usd"] == "1.60"  # 80% of the $2.00 reservation
    assert not any("run_scan.sh" in a for a in args)  # phases stay out of the model's reach
    assert "acceptEdits" not in args and "--dangerously-skip-permissions" not in args
    rows = [(r["kind"], r["cost_usd"]) for r in ledger_rows(origin)]
    finished = [("done", 0)] if claude_rc == 0 else []  # post ran only on success
    assert rows == [("reserve", 2.0), ("actual", 0.42), *finished]  # measured before post
    # the scan ran in its own worktree; Rohan's checkout is untouched
    assert git(work, "status", "--porcelain", "--untracked-files=no") == ""
    assert git(work, "branch", "--show-current") == "main"


def test_the_local_pr_body_and_history_row_show_the_measured_charge(scan_repo, tmp_path):
    """The session cost $0.42 against a $2.00 reservation: the PR says $0.42."""
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, _ = run_local(work, env, tmp_path, FAKE_ANALYSIS="1", FAKE_TOUCH="1")
    assert res.returncode == 0, res.stdout + res.stderr
    calls = gh_calls(env)
    assert "charged $0.42 (measured; reserved ceiling $2.00" in calls
    assert "(reserved;" not in calls
    branch = next(b for b in git(origin, "branch", "--list", "claude/scan-*").split() if b != "*")
    row = json.loads(git(origin, "show", f"{branch}:data/evals/history.json"))["runs"][-1]
    assert (row["cost_usd"], row["cost_basis"], row["ceiling_usd"]) == (0.42, "measured", 2.0)
    # ...and the merge gate's anti-forgery check accepts it against the real ledger.
    ledger = ledger_rows(origin)
    assert content_checks.history_problems({}, {"runs": [row]}, ledger, {
        "integrity": row["integrity"]["passed"], "golden": row["golden"],
        "cap_usd": row["cap_usd"]}) == []  # fmt: skip


def test_a_run_that_fails_in_post_still_records_its_story_count(scan_repo, tmp_path):
    work, origin, env = scan_repo
    (work / "scripts/generate_review.py").write_text("raise SystemExit(1)\n")
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, _ = run_local(work, env, tmp_path, FAKE_ANALYSIS="1")
    assert res.returncode != 0
    actual = [r for r in ledger_rows(origin) if r["kind"] == "actual"]
    assert [(r["stories"], r["cost_usd"]) for r in actual] == [(2, 0.42)]  # calibrates


def test_wrapper_skips_without_launching_claude_when_budget_closed(scan_repo, tmp_path):
    work, _, env = scan_repo  # main ships monthly_cap_usd: null
    res, args = run_local(work, env, tmp_path)
    assert res.returncode == 0 and "skip" in res.stdout
    assert args == []


def sessions(tmp: Path) -> int:
    calls = tmp / "claude-args.calls"
    return len(calls.read_text().splitlines()) if calls.exists() else 0


def attempts(origin: Path) -> list[tuple]:
    return [(r["kind"], r["stories"], r.get("outcome")) for r in ledger_rows(origin)]


EMPTY = [("reserve", 0, None), ("actual", 0, "analysis-empty")]


def test_a_session_with_no_analysis_fails_without_a_pr_and_logs_why(scan_repo, tmp_path):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0", retry_max_usd="0.1")
    res, _ = run_local(work, env, tmp_path, FAKE_RESULT="I stopped before analyzing anything")
    assert res.returncode != 0
    rows = [(r["kind"], r["stories"], r["cost_usd"]) for r in ledger_rows(origin)]
    assert rows == [("reserve", 0, 2.0), ("actual", 0, 0.42)]  # no done row, no fake count
    assert sessions(tmp_path) == 1  # $0.42 is not below retry_max_usd: no retry
    calls = gh_calls(env)
    assert "Daily scan failing (local, analysis-empty)" in calls and "/pulls" not in calls
    assert "I stopped" not in calls  # the session's words stay out of public issues
    log = (work / "data/_scan.log").read_text()
    assert "session result (subtype=success, turns=7):" in log
    assert "I stopped before analyzing anything" in log


def test_the_logged_session_result_is_scrubbed(scan_repo, tmp_path):
    work, _, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, _ = run_local(work, env, tmp_path, FAKE_ANALYSIS="1", FAKE_RESULT=f"leak {SECRET}")
    assert res.returncode == 0, res.stdout + res.stderr
    log = (work / "data/_scan.log").read_text()
    assert "session result withheld" in log and SECRET not in log
    assert SECRET not in gh_calls(env)


def test_a_cheap_analysis_empty_day_gets_exactly_one_retry(scan_repo, tmp_path):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0", retry_max_usd="1.0")
    res, _ = run_local(work, env, tmp_path)  # every session comes back empty
    assert res.returncode != 0
    assert sessions(tmp_path) == 2
    assert attempts(origin) == EMPTY + EMPTY
    run_ids = [r["run_id"] for r in ledger_rows(origin) if r["kind"] == "reserve"]
    assert run_ids[1] == run_ids[0] + "-retry"
    assert "/pulls" not in gh_calls(env)
    # The same day again (launchd, or by hand): the ledger blocks a third session.
    res, _ = run_local(work, env, tmp_path)
    assert res.returncode == 0 and "skip" in res.stdout
    assert sessions(tmp_path) == 2 and attempts(origin) == EMPTY + EMPTY


def test_the_retry_ships_when_its_session_analyzes(scan_repo, tmp_path):
    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0", retry_max_usd="1.0")
    res, _ = run_local(work, env, tmp_path, FAKE_ANALYSIS_ON_RETRY="1")
    assert res.returncode == 0, res.stdout + res.stderr
    assert sessions(tmp_path) == 2
    assert attempts(origin) == [
        *EMPTY,
        ("reserve", 0, None),
        ("actual", 2, None),
        ("done", 2, None),
    ]
    log = (work / "data/_scan.log").read_text()
    assert log.count("FAILED in phase 'analysis-empty'") == 1  # only the first attempt
    assert "SCAN_RESULT" in log  # the retry's post ran to the end
