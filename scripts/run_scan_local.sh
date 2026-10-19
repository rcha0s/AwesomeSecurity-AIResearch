#!/usr/bin/env bash
# run_scan_local.sh - The Mac fallback runner for /daily-scan (launchd calls it).
#
# Idle when the cloud routine already ran today. Otherwise it runs the same
# skill headless via `claude -p` and records the run's measured cost
# (`total_cost_usd`), which also calibrates the per-story estimate cloud runs use.
#
# Subscription billing: ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN are unset so
# `claude` never falls back to API-key billing. Never --dangerously-skip-permissions:
# acceptEdits + an explicit tool allowlist. If a tool prompt stalls a run,
# widen ALLOWED_TOOLS rather than skipping permissions.
set -Eeuo pipefail
cd "$(dirname "$0")/.."
export SCAN_RUNNER=local
export PYTHON="${PYTHON:-$PWD/.venv/bin/python}"
export BUDGET_LEDGER="data/_budget_ledger.json"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
OUT="data/_scan_claude.json"
LOG="data/_scan.log"

ALLOWED_TOOLS=(
  "Read" "Write" "Edit" "Glob" "Grep" "Task"
  "Bash(scripts/run_scan.sh:*)"
  "Bash(python scripts/:*)" "Bash($PYTHON scripts/:*)"
  "Bash(curl -s https://r.jina.ai/:*)"
)

fail() {
  echo "[local] $1" | tee -a "$LOG"
  scripts/run_scan.sh fail "$1"
  exit 1
}

[[ -z "$(git status --porcelain --untracked-files=no)" ]] || fail "local-dirty-tree"
git checkout -q main && git pull -q --ff-only || fail "local-git-sync"

# The ledger is the shared record of which runner ran today.
scripts/run_scan.sh ledger-sync || fail "local-ledger-sync"
if "$PYTHON" scripts/budget.py ran-today --runner cloud >/dev/null 2>&1; then
  echo "[local] cloud routine already ran today; nothing to do"
  exit 0
fi

env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN claude -p "/daily-scan" \
  --output-format json --permission-mode acceptEdits \
  --allowedTools "${ALLOWED_TOOLS[@]}" >"$OUT" || fail "local-claude"

[[ -f data/_scan_skip ]] && { echo "[local] budget guard skipped this run"; exit 0; }
[[ -f data/_scan_result.json ]] || fail "local-no-result"

cost="$("$PYTHON" -c 'import json,sys;print(json.load(open(sys.argv[1]))["total_cost_usd"])' "$OUT")"
stories="$("$PYTHON" -c 'import json;print(json.load(open("data/_scan_result.json"))["stories"])')"
"$PYTHON" scripts/budget.py record --runner local --stories "$stories" --cost-usd "$cost"
scripts/run_scan.sh ledger-push
git checkout -q main
