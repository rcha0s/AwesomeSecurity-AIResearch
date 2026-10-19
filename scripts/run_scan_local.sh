#!/usr/bin/env bash
# run_scan_local.sh - The Mac fallback runner for /daily-scan (launchd calls it).
#
# The wrapper, not the model, runs every phase that guards spend or publishes:
# check -> pre (reserve + ingest) -> a `claude -p` session running the
# daily-scan skill in wrapped mode (analysis only) -> post (render + PR) ->
# actual (measured cost). The model can't skip,
# re-run or fake any of them, and the measured cost is recorded on every
# outcome because the wrapper itself made the reservation.
#
# Containment: this runs as Rohan on his Mac over attacker-controlled text.
#   - dontAsk mode: only allowlisted tools run, everything else is denied.
#     (acceptEdits would approve edits anywhere in the repo, e.g. .venv.)
#   - Edits only under data/, never data/_scan* or candidates.json; file reads
#     only inside the repo; Bash only the named analysis scripts; no curl, git,
#     gh, WebFetch or WebSearch. fetch_raw.py fetches URLs from pre's snapshot.
#   - No outside settings or tools: --setting-sources local keeps the user's
#     and the repo's broad allow rules out, and every MCP server and connector
#     is off (--strict-mcp-config with none, plus a deny on mcp__*). Without the
#     project source the skill isn't auto-loaded, so its text goes in through
#     --append-system-prompt-file.
#   - SCAN_LOCKED=1 in the session's environment: every script may fetch only
#     a staged candidate's own URL (common.check_scan_lock), and model-written
#     raw_path values can't point outside data/_raw/ (common.raw_file). The
#     model can't clear it: a Bash command prefixed with an env assignment no
#     longer matches its allow rules.
#   - --max-budget-usd at 80% of the reserved ceiling (spend can overshoot the
#     cap) and --max-turns bound the session's spend.
# Never --dangerously-skip-permissions. If a needed tool is denied, add it to
# ALLOWED_TOOLS deliberately.
#
# Subscription billing: ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN are unset so
# `claude` never falls back to API-key billing.
set -Eeuo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"
export SCAN_RUNNER=local
export SCAN_RUN_ID="local-$(date -u +%Y%m%dT%H%M%SZ)-$$"
# Appended, not prepended: launchd starts with a bare PATH, and a caller's own
# PATH (tests use fake gh/claude) must win.
export PATH="$REPO/.venv/bin:$PATH:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin"
export PYTHON="${PYTHON:-$REPO/.venv/bin/python}"
CLAUDE="${CLAUDE_BIN:-claude}" # tests point this at a fake
MAX_TURNS=150
OUT="$(mktemp)"
LOG="data/_scan.log"
trap 'rm -f "$OUT"' EXIT

TOOLS="Read,Edit,Write,Glob,Grep,Bash,Task"
ALLOWED_TOOLS=(
  "Read" "Glob" "Grep" "Task" "Edit(data/**)"
  "Bash(python scripts/fetch_raw.py *)"
  "Bash(python scripts/merge_analysis.py)" "Bash(python scripts/verify_citations.py)"
  "Bash(python scripts/importance.py *)" "Bash(python scripts/promote_editorial.py)"
)
SETTINGS='{"permissions": {
  "blockReadsOutsideWorkingDirectories": true,
  "deny": [
    "Edit(scripts/**)", "Edit(.claude/**)", "Edit(.github/**)", "Edit(.git/**)",
    "Edit(.venv/**)", "Edit(tests/**)", "Edit(**/*.pth)", "Edit(*.toml)", "Edit(*.cfg)",
    "Edit(config.yaml)", "Edit(ISA.md)", "Edit(CLAUDE.md)", "Edit(AGENTS.md)",
    "Edit(data/_scan*)", "Edit(data/candidates.json)",
    "Read(~/.ssh/**)", "Read(~/.claude/**)", "Read(~/.config/**)", "Read(~/.aws/**)",
    "Read(~/.gnupg/**)", "Read(.env)", "Read(.env.*)",
    "Bash(curl *)", "Bash(wget *)", "Bash(git *)", "Bash(gh *)",
    "Bash(scripts/*)", "Bash(bash *)", "Bash(sh *)",
    "WebFetch", "WebSearch", "mcp__*"
  ]
}}'

fail() {
  echo "[local] $1" | tee -a "$LOG"
  scripts/run_scan.sh fail "$1"
  exit 1
}

mkdir -p data
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || fail "local-dirty-tree"
{ git checkout -q main && git pull -q --ff-only origin main; } || fail "local-git-sync"

rc=0
scripts/run_scan.sh check >/dev/null || rc=$?
if [[ "$rc" == 3 ]]; then
  echo "[local] budget guard says skip (already ran today, no cap, or no budget left)"
  exit 0
fi
[[ "$rc" == 0 ]] || fail "local-budget-check"
ceiling="$(scripts/run_scan.sh ceiling)" || fail "local-ceiling"
cap_usd="$("$PYTHON" -c 'import sys;print(f"{float(sys.argv[1])*0.8:.2f}")' "$ceiling")"

scripts/run_scan.sh pre || fail "local-pre"
[[ -f data/_scan_skip ]] && exit 0 # raced: the guard refused at pre time

claude_rc=0
env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN SCAN_LOCKED=1 "$CLAUDE" -p \
  "Run the daily scan in wrapped mode, following the daily-scan instructions appended to your system prompt." \
  --append-system-prompt-file .claude/skills/daily-scan/SKILL.md \
  --output-format json --permission-mode dontAsk \
  --setting-sources local --strict-mcp-config --mcp-config '{"mcpServers": {}}' \
  --tools "$TOOLS" --settings "$SETTINGS" --allowedTools "${ALLOWED_TOOLS[@]}" \
  --disallowedTools "mcp__*" \
  --max-budget-usd "$cap_usd" --max-turns "$MAX_TURNS" >"$OUT" || claude_rc=$?

post_rc=0
if [[ "$claude_rc" == 0 ]]; then
  scripts/run_scan.sh post || post_rc=$?
fi

# Record what the session really cost on every outcome. Without a readable
# cost, the reservation pre made stays as the charge.
cost="$("$PYTHON" -c 'import json,sys;print(json.load(open(sys.argv[1])).get("total_cost_usd",""))' "$OUT" 2>/dev/null || true)"
stories="$("$PYTHON" -c 'import json;print(json.load(open("data/_scan_result.json"))["stories"])' 2>/dev/null || echo 0)"
if [[ -n "$cost" ]]; then
  scripts/run_scan.sh actual "$SCAN_RUN_ID" "$stories" "$cost" || fail "local-ledger-actual"
else
  echo "[local] no total_cost_usd in claude output; the reservation stands" | tee -a "$LOG"
fi

git checkout -q main
[[ "$claude_rc" == 0 ]] || fail "local-claude"
[[ "$post_rc" == 0 ]] || exit 1 # post already raised its own alert
