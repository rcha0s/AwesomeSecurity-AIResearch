#!/usr/bin/env bash
# run_scan_local.sh - The Mac fallback runner for /daily-scan (launchd calls it).
#
# It checks the budget before paying for a `claude` session, which also makes
# it idle on any day a scan already ran (cloud or local). Then it runs the
# skill headless and records the run's measured `total_cost_usd`, whatever the
# outcome, against the reservation `pre` made. That also calibrates the
# per-story cost cloud runs are charged.
#
# Containment: this runs as Rohan, on his Mac, over attacker-controlled text.
# The session gets exactly the tools the skill needs. File reads stay inside
# the repo (blockReadsOutsideWorkingDirectories plus explicit denies for secret
# directories), edits land only under data/, Bash runs only the named scripts,
# and nothing can fetch an arbitrary URL (fetch_raw.py fetches a staged
# candidate's own URL). Never --dangerously-skip-permissions: if a tool prompt
# stalls a run, widen ALLOWED_TOOLS deliberately.
#
# Subscription billing: ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN are unset so
# `claude` never falls back to API-key billing.
set -Eeuo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"
export SCAN_RUNNER=local
export SCAN_RUN_ID="local-$(date -u +%Y%m%dT%H%M%SZ)-$$"
export PATH="$REPO/.venv/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export PYTHON="$REPO/.venv/bin/python"
OUT="$(mktemp)"
LOG="data/_scan.log"
trap 'rm -f "$OUT"' EXIT

ALLOWED_TOOLS=(
  "Read" "Glob" "Grep" "Task" "Edit(data/**)"
  "Bash(scripts/run_scan.sh pre)" "Bash(scripts/run_scan.sh post)"
  "Bash(scripts/run_scan.sh fail *)"
  "Bash(python scripts/fetch_raw.py *)"
  "Bash(python scripts/merge_analysis.py)" "Bash(python scripts/verify_citations.py)"
  "Bash(python scripts/importance.py *)" "Bash(python scripts/promote_editorial.py)"
)
SETTINGS='{"permissions": {
  "blockReadsOutsideWorkingDirectories": true,
  "deny": [
    "Edit(scripts/**)", "Edit(.claude/**)", "Edit(.github/**)", "Edit(.git/**)",
    "Edit(config.yaml)", "Edit(ISA.md)", "Edit(data/_scan*)",
    "Read(~/.ssh/**)", "Read(~/.claude/**)", "Read(~/.config/**)", "Read(~/.aws/**)",
    "Read(~/.gnupg/**)", "Read(.env)", "Read(.env.*)",
    "Bash(curl *)", "Bash(wget *)", "Bash(git *)", "Bash(gh *)",
    "WebFetch", "WebSearch"
  ]
}}'

fail() {
  echo "[local] $1" | tee -a "$LOG"
  scripts/run_scan.sh fail "$1"
  exit 1
}

mkdir -p data
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || fail "local-dirty-tree"
{ git checkout -q main && git pull -q --ff-only; } || fail "local-git-sync"

rc=0
scripts/run_scan.sh check >/dev/null || rc=$?
if [[ "$rc" == 3 ]]; then
  echo "[local] budget guard says skip (already ran today, no cap, or no budget left)"
  exit 0
fi
[[ "$rc" == 0 ]] || fail "local-budget-check"

claude_rc=0
env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN claude -p "/daily-scan" \
  --output-format json --permission-mode acceptEdits \
  --settings "$SETTINGS" --allowedTools "${ALLOWED_TOOLS[@]}" >"$OUT" || claude_rc=$?

# Record the measured cost whether the run shipped, skipped or failed. Without a
# readable cost the reservation `pre` made stays as the charge.
if [[ ! -f data/_scan_skip ]] && [[ -f data/_scan_run_id ]]; then
  cost="$("$PYTHON" -c 'import json,sys;print(json.load(open(sys.argv[1])).get("total_cost_usd",""))' "$OUT" 2>/dev/null || true)"
  stories="$("$PYTHON" -c 'import json;print(json.load(open("data/_scan_result.json"))["stories"])' 2>/dev/null || echo 0)"
  if [[ -n "$cost" ]]; then
    scripts/run_scan.sh actual "$SCAN_RUN_ID" "$stories" "$cost" || fail "local-ledger-actual"
  else
    echo "[local] no total_cost_usd in claude output; the reservation stands" | tee -a "$LOG"
  fi
fi

git checkout -q main
[[ "$claude_rc" == 0 ]] || fail "local-claude"
[[ -f data/_scan_skip || -f data/_scan_result.json ]] || fail "local-no-result"
