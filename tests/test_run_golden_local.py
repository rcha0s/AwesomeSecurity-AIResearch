"""End-to-end test of scripts/run_golden_local.sh with a fake `claude` (ISC-23).

The weekly golden run must stage the cases in its own worktree, hide their
entries there, run the session under the daily scan's lockdown, score the
output, and open a PR carrying only the result file.
"""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime

from test_run_scan import commit_main, gh_calls, git

FAKE_CLAUDE = """#!/bin/sh
printf '%s\\n' "$@" > "$CLAUDE_ARGS"
cp data/candidates.json "$CLAUDE_ARGS.candidates"
cp data/ai-research.json "$CLAUDE_ARGS.pool"
prev=""
for a in "$@"; do
  [ "$prev" = "--settings" ] && printf '%s' "$a" > "$CLAUDE_ARGS.settings"
  prev="$a"
done
grep -rIl --exclude-dir=.git -e "Harness escalation story" -e "example.com/a" . | sort > "$CLAUDE_ARGS.traces"
cat > data/analysis_out.json <<'JSON'
[{"topic": "ai-research", "domain": "air.agents", "title": "Harness escalation story",
  "source_url": "https://example.com/a", "summary": "All 13 attack objectives worked.",
  "scores": {"novelty": 80, "relevance": 85}, "verified": true,
  "lessons": [{"point": "p", "excerpt": "e", "confidence": 0.9}]}]
JSON
echo '{"total_cost_usd": 0.5}'
"""

CASES = [
    {"id": "a", "title": "Harness escalation story", "url": "https://example.com/a",
     "keep": True, "on_topic": True, "domain": "air.agents", "reason": "curated",
     "facts": [{"fact": "13 objectives", "any": ["13 attack"]}]},
    {"id": "b", "title": "Sourdough for engineers", "url": "https://example.com/b",
     "keep": False, "on_topic": False, "domain": "air.ml-research", "reason": "off-thesis",
     "facts": []},
]  # fmt: skip


def test_golden_run_stages_in_its_worktree_and_opens_a_result_pr(scan_repo, tmp_path):
    work, origin, env = scan_repo
    (work / "scripts" / "fetch_raw.py").write_text("print('stub')\n")  # no network
    (work / "data" / "evals").mkdir()
    (work / "data" / "evals" / "golden.json").write_text(json.dumps({"cases": CASES}))
    entries = [
        {"id": "a", "title": "Harness escalation story", "source_url": "https://example.com/a"},
        {"id": "keep-me", "title": "Other", "prior_art": "Harness escalation story (2026)"},
    ]
    pool = {"topic": "ai-research", "entries": entries}
    (work / "data" / "ai-research.json").write_text(json.dumps(pool))
    # The old answer, rendered and cited: all of it must be gone before the session.
    (work / "docs").mkdir()
    (work / "docs" / "index.html").write_text("<p>Harness escalation story</p>")
    (work / "README.md").write_text("- Harness escalation story\n")
    claims = {"claims": [{"id": "c", "evidence": [{"url": "https://example.com/a", "title": "t"}]}]}
    (work / "data" / "claims.json").write_text(json.dumps(claims))
    commit_main(work, "golden set")
    fake = tmp_path / "fake-claude"
    fake.write_text(FAKE_CLAUDE)
    fake.chmod(0o755)
    args_file = tmp_path / "claude-args"
    res = subprocess.run(
        ["/bin/bash", "scripts/run_golden_local.sh"],
        cwd=work,
        env={**env, "CLAUDE_BIN": str(fake), "CLAUDE_ARGS": str(args_file),
             "GOLDEN_WORKTREE": str(tmp_path / "golden-wt"), "HOME": str(tmp_path / "home")},
        capture_output=True,
        text=True,
    )  # fmt: skip
    assert res.returncode == 0, res.stdout + res.stderr
    args = args_file.read_text().splitlines()
    flag = dict(zip(args, args[1:], strict=False))
    assert args[0] == "-p" and "Golden eval run" in args[1]
    assert flag["--append-system-prompt-file"] == ".claude/skills/research-scan/SKILL.md"
    assert flag["--permission-mode"] == "dontAsk" and flag["--max-budget-usd"] == "4"
    assert '"Edit(data/evals/**)"' in "\n".join(args)  # the session can't forge a result
    staged = json.loads((tmp_path / "claude-args.candidates").read_text())
    assert [c["id"] for c in staged] == ["a", "b"] and "domain" not in staged[0]
    hidden = json.loads((tmp_path / "claude-args.pool").read_text())
    assert hidden["entries"] == [{"id": "keep-me", "title": "Other"}]  # prior_art naming it cut
    assert (tmp_path / "claude-args.traces").read_text().split() == ["./data/candidates.json"]
    deny = json.loads((tmp_path / "claude-args.settings").read_text())["permissions"]["deny"]
    assert {"Read(data/evals/**)", "Read(data/_golden*)", "Read(.git/**)"} <= set(deny)
    assert "Edit(data/evals/**)" in deny and "Bash(git *)" in deny  # the daily lockdown kept
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    branch = f"claude/golden-{day}"
    assert git(origin, "diff", "--name-only", "main", branch) == f"data/evals/golden-{day}.json"
    result = json.loads(git(origin, "show", f"{branch}:data/evals/golden-{day}.json"))
    assert result["score"] == 1.0 and result["cases"] == 2
    assert "-X POST repos/" in gh_calls(env) and "EVAL golden PASS score=1.000" in gh_calls(env)
    assert git(work, "status", "--porcelain", "--untracked-files=no") == ""  # checkout untouched
