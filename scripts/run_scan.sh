#!/usr/bin/env bash
# run_scan.sh - The one entrypoint for the daily scan (ISA F1).
#
# Both runners drive the same /daily-scan skill, which calls these phases
# around its LLM analysis, so a cloud run and a local run open a scan PR of
# the same shape:
#
#   check        budget guard only (the local wrapper runs it before it pays
#                for a `claude` session). Exit 0 = go, 3 = skip.
#   session-limits  print "<max_budget_usd> <max_turns>" for the local session.
#   pre          budget guard, then RESERVE the run's ceiling on the ledger
#                BEFORE any LLM work, then every ingestor. A refusal prints
#                SCAN_SKIP and writes data/_scan_skip; the skill stops there.
#   post         per-run story cap, render everything, push
#                claude/scan-<date>-<runner> and open its PR.
#   actual <stories> <cost_usd>   record a local run's measured cost.
#   fail <phase> open or comment on the scan-failure issue.
#   status       print this month's spend report (also kept as SPEND.md on the
#                budget-ledger branch, rewritten on every ledger write).
#
# Trust boundary: the model shares this working tree, so nothing that guards
# spend is read from it. The budget settings come from origin/main's
# config.yaml, and every ledger write appends one row to a fresh copy of the
# `budget-ledger` branch in a temp dir, never to a file under data/.
#
# Runner: SCAN_RUNNER=cloud (default) or local. Python: $PYTHON or python3.
set -Eeuo pipefail # -E: the ERR trap fires inside functions too
cd "$(dirname "$0")/.."
source scripts/lib.sh

RUNNER="${SCAN_RUNNER:-cloud}"
PY="${PYTHON:-python3}"
LOG="${SCAN_LOG:-data/_scan.log}" # the Mac wrapper keeps it outside its worktree
LEDGER_BRANCH="budget-ledger"
SKIP_MARKER="data/_scan_skip"
RESULT="data/_scan_result.json"
SUMMARY="data/_summary.md"
RUN_ID_FILE="data/_scan_run_id"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

INGESTORS=(aggregate ingest_sitemap ingest_github ingest_ghsa ingest_hn ingest_conferences)
RENDERERS=(rerank generate_site generate_claims generate_html generate_og trends
  generate_newsletter generate_review)
# What a scan commits. data/ is staged with `-u` (tracked files only), so a
# file the model invents under data/ never ships; rendered paths take new
# files because the renderers create pages. Directories, not globs: a glob
# would name gitignored files, and `git add` exits 1 on those.
DATA_DIR="data"
RENDERED=(README.md NEWSLETTER.md TRENDS.md REVIEW.md
  ai-security product-security ai-research claims docs)

# The published paths that exist or are tracked; git rejects a pathspec that
# matches neither.
published() {
  local p
  for p in "${RENDERED[@]}"; do
    if [[ -e "$p" ]] || git ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then echo "$p"; fi
  done
}

log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

on_error() {
  log "FAILED in phase '$1' (line $2)"
  scripts/scan_alert.sh "$RUNNER" "$1" || log "alert itself failed"
}

# Every step in these helpers checks its own exit status: they are called
# from `||` and `if` contexts, where bash turns errexit off, and a git failure
# that slipped through would let the guard read a stale or empty ledger as GO.

# Budget settings from origin/main: a branch the model can't push to.
main_config() {
  git fetch -q origin main || return 1
  git show origin/main:config.yaml >"$WORK/config.yaml" || return 1
}

# A fresh copy of the remote ledger in $WORK/ledger.json. A missing branch
# means the first run; any other git error fails, because starting from an
# empty ledger would overspend.
ledger_fetch() {
  local rc=0
  rm -f "$WORK/ledger.json"
  git ls-remote --exit-code --heads origin "$LEDGER_BRANCH" >/dev/null || rc=$?
  if [[ "$rc" == 2 ]]; then
    echo '{"runs": []}' >"$WORK/ledger.json" || return 1
    LEDGER_PARENT=""
  elif [[ "$rc" == 0 ]]; then
    git fetch -q origin "$LEDGER_BRANCH" || return 1
    LEDGER_PARENT="$(git rev-parse FETCH_HEAD)" || return 1
    git show "$LEDGER_PARENT:budget.json" >"$WORK/ledger.json" || return 1
  else
    log "cannot reach origin to read the budget ledger (git exit $rc)"
    return 1
  fi
}

budget() {
  BUDGET_LEDGER="$WORK/ledger.json" "$PY" scripts/budget.py --config "$WORK/config.yaml" "$@"
}

# Commit the temp ledger onto its branch with plumbing: no worktree, and the
# scan's own checkout is never touched. Not a force push: a concurrent writer
# makes it fail, and the callers retry from a fresh fetch.
ledger_commit() {
  local blob report tree commit
  local parent=()
  [[ -n "$LEDGER_PARENT" ]] && parent=(-p "$LEDGER_PARENT")
  blob="$(git hash-object -w "$WORK/ledger.json")" || return 1
  # SPEND.md rides along so the month's spend is readable on GitHub.
  budget status >"$WORK/SPEND.md" || return 1
  report="$(git hash-object -w "$WORK/SPEND.md")" || return 1
  tree="$(printf '100644 blob %s\tSPEND.md\n100644 blob %s\tbudget.json\n' "$report" "$blob" |
    git mktree)" || return 1
  commit="$(git commit-tree "$tree" ${parent[@]+"${parent[@]}"} -m "budget: $1")" || return 1
  git push -q origin "$commit:refs/heads/$LEDGER_BRANCH"
}

# Append one row (budget.py actual|done ...) to the remote ledger.
ledger_append() {
  local run_id="$1" try
  shift
  for try in 1 2; do
    ledger_fetch || return 1
    budget "$@" | tee -a "$LOG" || return 1
    if ledger_commit "$run_id"; then
      log "ledger: $1 recorded for $run_id"
      return 0
    fi
    log "ledger push raced another writer; retrying ($try)"
  done
  return 1
}

# The spend check alone (exit 0 go, 3 skip, else error).
guard() {
  local repeat=() rc=0
  [[ "${SCAN_ALLOW_REPEAT:-}" == 1 ]] && repeat=(--allow-repeat)
  main_config || return 1
  ledger_fetch || return 1
  budget check --runner "$RUNNER" ${repeat[@]+"${repeat[@]}"} | tee -a "$LOG" || rc=$?
  return "$rc"
}

# Check and reserve against the same fetched ledger. If the push loses a race,
# the retry re-runs the check on the newer ledger, so two runners can't both
# reserve the last of the budget or the same day.
check_and_reserve() {
  local run_id="$1" try rc
  for try in 1 2; do
    rc=0
    guard || rc=$?
    [[ "$rc" == 0 ]] || return "$rc"
    budget reserve --runner "$RUNNER" --run-id "$run_id" | tee -a "$LOG" || return 1
    if ledger_commit "$run_id"; then
      log "ledger: reserve recorded for $run_id"
      return 0
    fi
    log "ledger push raced another writer; re-checking ($try)"
  done
  return 1
}

phase_pre() {
  rm -f "$SKIP_MARKER" "$RESULT" "$SUMMARY" "$RUN_ID_FILE" \
    data/analysis_out.json data/editorial_out.json
  local rc=0 run_id
  run_id="${SCAN_RUN_ID:-$RUNNER-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
  check_and_reserve "$run_id" || rc=$?
  if [[ "$rc" == 3 ]]; then
    touch "$SKIP_MARKER"
    log "SCAN_SKIP: budget guard refused; no LLM work this run"
    return 0
  fi
  [[ "$rc" == 0 ]] || return "$rc"
  echo "$run_id" >"$RUN_ID_FILE"
  local failed=0
  for ing in "${INGESTORS[@]}"; do
    if "$PY" "scripts/$ing.py" >>"$LOG" 2>&1; then log "ingest ok: $ing"; else
      log "ingest WARN: $ing failed"
      failed=$((failed + 1))
    fi
  done
  if [[ "$failed" == "${#INGESTORS[@]}" ]]; then
    log "every ingestor failed"
    return 1
  fi
  "$PY" scripts/fetch_raw.py --snapshot | tee -a "$LOG"
  log "SCAN_READY: $("$PY" -c 'import sys;sys.path.insert(0,"scripts");import common;print(len(common.load_candidates()))') candidates"
}

phase_post() {
  local stories cap day branch body run_id
  run_id="$(cat "$RUN_ID_FILE")"
  main_config
  # The larger of analysis_out.json and entries new since main: the model
  # could merge several capped batches before post sees only the last.
  stories="$("$PY" scripts/scan_count.py)"
  cap="$("$PY" -c 'import sys;sys.path.insert(0,"scripts");import budget;print(budget.budget_settings(sys.argv[1])["max_stories_per_run"])' "$WORK/config.yaml")"
  require_int "$stories" "story count"
  require_int "$cap" "story cap"
  if ((stories > cap)); then
    log "analyzed $stories stories, over the per-run cap of $cap"
    return 1
  fi
  "$PY" scripts/add_claim.py validate >>"$LOG"
  for r in "${RENDERERS[@]}"; do "$PY" "scripts/$r.py" >>"$LOG"; done
  echo "{\"runner\": \"$RUNNER\", \"stories\": $stories}" >"$RESULT"
  local paths=()
  while IFS= read -r p; do paths+=("$p"); done < <(published)
  local changes
  changes="$(git status --porcelain --untracked-files=no -- "$DATA_DIR")"
  if [[ ${#paths[@]} -gt 0 ]]; then changes+="$(git status --porcelain -- "${paths[@]}")"; fi
  if [[ -z "$changes" ]]; then
    log "SCAN_RESULT: no changes; no PR"
    ledger_append "$run_id" done --run-id "$run_id" --stories "$stories"
    return 0
  fi
  day="$(date -u +%Y-%m-%d)"
  branch="claude/scan-$day-$RUNNER"
  git checkout -q -B "$branch"
  git add -u -- "$DATA_DIR"
  [[ ${#paths[@]} == 0 ]] || git add -A -- "${paths[@]}"
  if ! git diff --cached -U0 | "$PY" scripts/scrub.py --diff; then
    log "staged diff has secret-like content; not pushing"
    return 1
  fi
  git commit -qm "chore: daily scan ($RUNNER, $day, $stories stories)"
  git push -q --force origin "HEAD:refs/heads/$branch"
  body="$("$PY" scripts/scrub.py "$SUMMARY" "Daily scan, runner \`$RUNNER\`, $stories stories analyzed.")"
  body+="$(spend_line)"
  scripts/ensure_pr.sh "$branch" "chore: daily scan ($RUNNER, $day)" "$body" | tee -a "$LOG"
  ledger_append "$run_id" done --run-id "$run_id" --stories "$stories"
}

# One line for the PR body: the month so far, and where the full report lives.
spend_line() {
  local month
  ledger_fetch || return 0 # the PR still opens; the report is on the branch
  month="$(budget status | sed -n 's/^\*\*\(.* charged of .*\)\.\*\* .*/\1/p')"
  printf '\n\n**Spend this month:** %s (this run reserved its ceiling; local runs settle to measured cost). Full report: [SPEND.md](../blob/%s/SPEND.md)' \
    "${month:-unavailable}" "$LEDGER_BRANCH"
}

# The local wrapper passes the run id it set, so the row can't be redirected
# by an edited data/_scan_run_id.
phase_actual() {
  local run_id="$1" stories="$2" cost="$3"
  require_int "$stories" "actual: stories"
  main_config
  ledger_append "$run_id" actual --run-id "$run_id" --stories "$stories" --cost-usd "$cost"
}

main() {
  local phase="${1:-}"
  mkdir -p data
  case "$phase" in
    check) guard ;;
    session-limits)
      main_config
      ledger_fetch
      budget session-limits --runner "$RUNNER"
      ;;
    pre | post)
      trap "on_error $phase \$LINENO" ERR
      "phase_$phase"
      ;;
    actual) phase_actual "$2" "$3" "$4" ;;
    status)
      main_config
      ledger_fetch
      budget status
      ;;
    fail) on_error "${2:-unknown}" 0 ;;
    *)
      echo "usage: $0 check|session-limits|pre|post|status|actual <run_id> <stories> <cost>|fail <phase>" >&2
      exit 2
      ;;
  esac
}

main "$@"
