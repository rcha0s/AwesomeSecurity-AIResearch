"""End-to-end test of scripts/run_scan_local.sh with a fake `claude` (ISC-7/8).

The wrapper, not the model, must run check -> pre -> analysis -> post ->
actual, launch the session locked down, and record the measured cost even
when the session fails.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from test_run_scan import ledger_rows, open_budget, scan_repo  # noqa: F401  (fixture)

FAKE_CLAUDE = """#!/bin/sh
printf '%s\\n' "$@" > "$CLAUDE_ARGS"
echo '{"total_cost_usd": 0.42}'
exit "${FAKE_CLAUDE_RC:-0}"
"""


def run_local(work: Path, env: dict, tmp: Path, rc: int = 0):
    fake = tmp / "fake-claude"
    fake.write_text(FAKE_CLAUDE)
    fake.chmod(0o755)
    extra = {
        "CLAUDE_BIN": str(fake),
        "CLAUDE_ARGS": str(tmp / "claude-args"),
        "FAKE_CLAUDE_RC": str(rc),
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
    res, args = run_local(work, env, tmp_path, rc=claude_rc)
    assert (res.returncode == 0) == (claude_rc == 0), res.stdout + res.stderr
    assert args[:2] == ["-p", "/daily-scan wrapped"]
    flag = dict(zip(args, args[1:]))
    assert flag["--permission-mode"] == "dontAsk"
    assert flag["--setting-sources"] == "local"
    assert "--strict-mcp-config" in args and flag["--disallowedTools"] == "mcp__*"
    assert flag["--max-budget-usd"] == "1.60"  # 80% of the $2.00 reservation
    assert not any("run_scan.sh" in a for a in args)  # phases stay out of the model's reach
    assert "acceptEdits" not in args and "--dangerously-skip-permissions" not in args
    rows = [(r["kind"], r["cost_usd"]) for r in ledger_rows(origin)]
    assert rows == [("reserve", 2.0), ("actual", 0.42)]


def test_wrapper_skips_without_launching_claude_when_budget_closed(scan_repo, tmp_path):
    work, _, env = scan_repo  # main ships monthly_cap_usd: null
    res, args = run_local(work, env, tmp_path)
    assert res.returncode == 0 and "skip" in res.stdout
    assert args == []
