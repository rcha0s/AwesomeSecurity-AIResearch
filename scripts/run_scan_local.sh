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
#   - Edits only under data/, never data/_scan*, data/_raw/ (fetch_raw.py is its
#     only writer, so quotes ground against fetched text) or candidates.json; file reads
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
#   - --max-budget-usd (the reservation x budget.session_cap_fraction, since
#     spend can overshoot the cap) and --max-turns (limits.max_turns), both
#     read from origin/main's config by `run_scan.sh session-limits`.
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
# The scan runs in its own worktree, reset to origin/main every run: a failed
# run can't leave a dirty tree behind, and Rohan's checkout is never touched.
WT="${SCAN_WORKTREE:-$HOME/.local/share/awesomesec-worktree}"
SCAN_DIR="$REPO" # where `fail` finds run_scan.sh; the worktree once it's ready
OUT="$(mktemp)"
# Outside the worktree, which every run cleans: the log an alert points to
# survives, and the model session (confined to the worktree) can't read it.
export SCAN_LOG="$REPO/data/_scan.log"
LOG="$SCAN_LOG"
trap 'rm -f "$OUT"' EXIT

# TOOLS, ALLOWED_TOOLS, SETTINGS and contained_claude: one lockdown, shared
# with the weekly golden-set run (run_golden_local.sh).
source scripts/scan_containment.sh

fail() {
  echo "[local] $1" | tee -a "$LOG"
  "$SCAN_DIR/scripts/run_scan.sh" fail "$1"
  exit 1
}

reset_worktree() {
  git -C "$REPO" fetch -q origin main || return 1
  if [[ ! -e "$WT/.git" ]]; then
    # A worktree deleted from disk stays registered and blocks `worktree add`.
    git -C "$REPO" worktree prune || return 1
    mkdir -p "$(dirname "$WT")" || return 1
    git -C "$REPO" worktree add -q --detach "$WT" origin/main || return 1
  fi
  git -C "$WT" checkout -q -f --detach origin/main || return 1
  git -C "$WT" clean -ffdxq || return 1
}

mkdir -p "$REPO/data"
reset_worktree || fail "local-worktree"
cd "$WT"
SCAN_DIR="$WT"
mkdir -p data

rc=0
scripts/run_scan.sh check >/dev/null || rc=$?
if [[ "$rc" == 3 ]]; then
  echo "[local] budget guard says skip (a scan finished today, no cap, or no budget left)"
  exit 0
fi
[[ "$rc" == 0 ]] || fail "local-budget-check"
limits="$(scripts/run_scan.sh session-limits)" || fail "local-session-limits"
cap_usd="${limits% *}"
max_turns="${limits#* }"

scripts/run_scan.sh pre || exit 1 # pre raises its own alert
[[ -f data/_scan_skip ]] && exit 0 # raced: the guard refused at pre time

claude_rc=0
contained_claude \
  "Run the daily scan in wrapped mode, following the daily-scan instructions appended to your system prompt." \
  .claude/skills/daily-scan/SKILL.md "$cap_usd" "$max_turns" >"$OUT" || claude_rc=$?

post_rc=0
if [[ "$claude_rc" == 0 ]]; then
  scripts/run_scan.sh post || post_rc=$?
fi

# Record what the session really cost on every outcome. Without a readable
# cost, the reservation pre made stays as the charge.
cost="$("$PYTHON" -c 'import json,sys;print(json.load(open(sys.argv[1])).get("total_cost_usd",""))' "$OUT" 2>/dev/null || true)"
# Counted here, not read from post's result: a run that fails in post still
# analyzed its stories, and calibration needs that count.
stories="$("$PYTHON" scripts/scan_count.py 2>/dev/null || echo 0)"
[[ "$stories" =~ ^[0-9]+$ ]] || stories=0
if [[ -n "$cost" ]]; then
  scripts/run_scan.sh actual "$SCAN_RUN_ID" "$stories" "$cost" || fail "local-ledger-actual"
else
  echo "[local] no total_cost_usd in claude output; the reservation stands" | tee -a "$LOG"
fi

[[ "$claude_rc" == 0 ]] || fail "local-claude"
[[ "$post_rc" == 0 ]] || exit 1 # post already raised its own alert
