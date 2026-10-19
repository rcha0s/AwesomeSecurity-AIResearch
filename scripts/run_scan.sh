#!/usr/bin/env bash
# run_scan.sh - The one entrypoint for the daily scan (ISA F1).
#
# Both runners drive the same /daily-scan skill, which calls these phases
# around its LLM analysis, so a cloud run and a local run open a scan PR of
# the same shape:
#
#   pre          sync the budget ledger, run the spend guard BEFORE any LLM
#                work, then run every ingestor. A refused budget prints
#                SCAN_SKIP and writes data/_scan_skip; the skill stops there.
#   post         enforce the per-run story cap, render everything, record the
#                cloud run's estimated spend, push claude/scan-<date>-<runner>
#                and open its PR.
#   ledger-sync  pull the budget-ledger branch into data/_budget_ledger.json.
#   ledger-push  push data/_budget_ledger.json to the budget-ledger branch.
#   fail <phase> open or comment on the scan-failure issue.
#
# Runner: SCAN_RUNNER=cloud (default) or local. Python: $PYTHON or python3.
set -Eeuo pipefail # -E: the ERR trap fires inside functions too
cd "$(dirname "$0")/.."
source scripts/lib.sh

RUNNER="${SCAN_RUNNER:-cloud}"
PY="${PYTHON:-python3}"
LOG="data/_scan.log"
LEDGER="data/_budget_ledger.json"
LEDGER_BRANCH="budget-ledger"
SKIP_MARKER="data/_scan_skip"
RESULT="data/_scan_result.json"
SUMMARY="data/_scan_summary.md"
export BUDGET_LEDGER="$LEDGER"

INGESTORS=(aggregate ingest_sitemap ingest_github ingest_ghsa ingest_hn ingest_conferences)
RENDERERS=(rerank generate_site generate_claims generate_html generate_og trends
  generate_newsletter generate_review)
PUBLISHED=(data/*.json README.md NEWSLETTER.md TRENDS.md REVIEW.md
  ai-security product-security ai-research claims docs)

log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

on_error() {
  log "FAILED in phase '$1' (line $2)"
  scripts/scan_alert.sh "$RUNNER" "$1" "$LOG" || log "alert itself failed"
}

# Missing branch = first run, start empty. Any other git error must fail:
# silently starting from an empty ledger would overspend.
ledger_sync() {
  local rc=0
  git ls-remote --exit-code --heads origin "$LEDGER_BRANCH" >/dev/null || rc=$?
  if [[ "$rc" == 2 ]]; then
    echo '{"runs": []}' >"$LEDGER"
  elif [[ "$rc" == 0 ]]; then
    git fetch -q origin "$LEDGER_BRANCH"
    git show "FETCH_HEAD:budget.json" >"$LEDGER"
  else
    log "cannot reach origin to read the budget ledger (git exit $rc)"
    return 1
  fi
}

# Commit budget.json onto the ledger branch with plumbing: no worktree, and
# the scan's own checkout is never touched.
ledger_push() {
  local blob tree commit
  local parent=()
  blob="$(git hash-object -w "$LEDGER")"
  tree="$(printf '100644 blob %s\tbudget.json\n' "$blob" | git mktree)"
  if git ls-remote --exit-code --heads origin "$LEDGER_BRANCH" >/dev/null; then
    git fetch -q origin "$LEDGER_BRANCH"
    parent=(-p FETCH_HEAD)
  fi
  commit="$(git commit-tree "$tree" ${parent[@]+"${parent[@]}"} -m "budget: $RUNNER run $(date -u +%Y-%m-%d)")"
  git push -q origin "$commit:refs/heads/$LEDGER_BRANCH"
  log "ledger pushed to $LEDGER_BRANCH"
}

phase_pre() {
  rm -f "$SKIP_MARKER" "$RESULT" "$SUMMARY"
  ledger_sync
  local rc=0
  "$PY" scripts/budget.py check --runner "$RUNNER" | tee -a "$LOG" || rc=$?
  if [[ "$rc" == 3 ]]; then
    touch "$SKIP_MARKER"
    log "SCAN_SKIP: budget guard refused; no LLM work this run"
    return 0
  fi
  [[ "$rc" == 0 ]] || return "$rc"
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
  log "SCAN_READY: $("$PY" -c 'import json;print(len(json.load(open("data/candidates.json"))))') candidates"
}

story_count() {
  [[ -f data/analysis_out.json ]] || { echo 0; return; }
  "$PY" -c 'import json;d=json.load(open("data/analysis_out.json"));print(len(d if isinstance(d,list) else d.get("entries",[])))'
}

phase_post() {
  local stories cap
  stories="$(story_count)"
  cap="$("$PY" -c 'import sys;sys.path.insert(0,"scripts");import budget;print(budget.budget_settings()["max_stories_per_run"])')"
  require_int "$stories" "story count"
  require_int "$cap" "story cap"
  if ((stories > cap)); then
    log "analyzed $stories stories, over the per-run cap of $cap"
    return 1
  fi
  "$PY" scripts/add_claim.py validate >>"$LOG"
  for r in "${RENDERERS[@]}"; do "$PY" "scripts/$r.py" >>"$LOG"; done
  echo "{\"runner\": \"$RUNNER\", \"stories\": $stories}" >"$RESULT"
  if [[ "$RUNNER" == "cloud" ]]; then
    "$PY" scripts/budget.py record --runner cloud --stories "$stories" | tee -a "$LOG"
    ledger_push
  fi
  if [[ -z "$(git status --porcelain -- "${PUBLISHED[@]}")" ]]; then
    log "SCAN_RESULT: no changes; no PR"
    return 0
  fi
  local branch="claude/scan-$(date -u +%Y-%m-%d)-$RUNNER"
  git checkout -q -B "$branch"
  git add -- "${PUBLISHED[@]}"
  git commit -qm "chore: daily scan ($RUNNER, $(date -u +%Y-%m-%d), $stories stories)"
  git push -q --force origin "HEAD:refs/heads/$branch"
  local body="Daily scan, runner \`$RUNNER\`, $stories stories analyzed."
  [[ -f "$SUMMARY" ]] && body="$(cat "$SUMMARY")"
  scripts/ensure_pr.sh "$branch" "chore: daily scan ($RUNNER, $(date -u +%Y-%m-%d))" "$body" | tee -a "$LOG"
}

main() {
  local phase="${1:-}"
  mkdir -p data
  case "$phase" in
    pre | post)
      trap "on_error $phase \$LINENO" ERR
      "phase_$phase"
      ;;
    ledger-sync) ledger_sync ;;
    ledger-push) ledger_push ;;
    fail) on_error "${2:-unknown}" 0 ;;
    *)
      echo "usage: $0 pre|post|ledger-sync|ledger-push|fail <phase>" >&2
      exit 2
      ;;
  esac
}

main "$@"
