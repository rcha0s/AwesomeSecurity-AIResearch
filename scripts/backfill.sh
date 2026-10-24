#!/usr/bin/env bash
# backfill.sh - Backfill a gap in the scan history (issue #52), one chunk at a time.
#
# A backfill chunk is a normal local scan (run_scan_local.sh: same lockdown,
# same skill, same story ledger, same PR shape and merge gate) with
# SCAN_BACKFILL_FROM/TO set, so ingest pulls items published inside the chunk
# instead of "recent" (see run_scan.sh). budget.py refuses any chunk outside
# the campaign config.yaml `backfill:` approves on main, over its caps, or
# overlapping a chunk that already finished; backfill rows never count as the
# day's scan.
#
#   scripts/backfill.sh plan  FROM TO [CHUNK_DAYS]   print the chunks (default 8 days)
#   scripts/backfill.sh start FROM TO [CHUNK_DAYS]   launch the one-shot launchd job
#   scripts/backfill.sh status                       is it running, recent log lines, spend
#   scripts/backfill.sh stop                         unload the job, kill the run in flight
#   scripts/backfill.sh run   FROM TO [CHUNK_DAYS]   the driver itself (the job runs this)
#
# `start` exists because a Claude session can't run `claude` inline: it pulls
# the runner clone (~/.local/share/awesomesec-runner, made by install_launchd.sh)
# to origin/main, prints the guard's verdict for the first chunk, and boots a
# launchd job from a plist outside ~/Library/LaunchAgents: RunAtLoad, no
# schedule, no KeepAlive, so it runs once and never comes back after a reboot.
# The driver runs the chunks in order. After a chunk opens its PR it waits
# (BACKFILL_WAIT_HOURS, default 48; 0 = don't wait) for that PR to be merged or
# closed, so the next chunk starts from a main that holds it: its story ledger
# dedupes against it, and the PRs never conflict with each other. A chunk the
# guard skips is passed over; any failure stops the driver. When it ends it
# unloads its own job. Logs: <runner>/data/_scan.log (grep "[backfill]").
set -euo pipefail

LABEL="com.rcha0s.awesomesecurity.backfill"
RUNNER="${SCAN_RUNNER_HOME:-$HOME/.local/share/awesomesec-runner}"
PLIST="${BACKFILL_PLIST:-$HOME/.local/share/awesomesec-backfill.plist}"
LAUNCHCTL="${LAUNCHCTL:-launchctl}" # tests point these at fakes
DOMAIN="gui/$(id -u)"
DEFAULT_CHUNK_DAYS=8
LOCK="data/_backfill.lock" # relative to the clone: cmd_run cds there first
WAIT_SECONDS="${BACKFILL_WAIT_SECONDS:-$((${BACKFILL_WAIT_HOURS:-48} * 3600))}"
POLL_SECONDS="${BACKFILL_POLL_SECONDS:-600}"
OTHER_DRIVER=0
((POLL_SECONDS >= 1)) || POLL_SECONDS=1 # a zero poll would never time out

die() {
  echo "backfill: $*" >&2
  exit 1
}

# Strict shapes only: these go into a plist and a shell string.
check_args() {
  [[ "${1:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "FROM must be YYYY-MM-DD, got '${1:-}'"
  [[ "${2:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "TO must be YYYY-MM-DD, got '${2:-}'"
  [[ "${3:-}" =~ ^[0-9]{1,2}$ ]] || die "CHUNK_DAYS must be a number, got '${3:-}'"
}

# The repo's own venv, else the runner clone's, else python3 (budget.py needs PyYAML).
py() {
  local here
  here="$(cd "$(dirname "$0")/.." && pwd)"
  if [[ -n "${PYTHON:-}" ]]; then "$PYTHON" "$@"
  elif [[ -x "$here/.venv/bin/python" ]]; then "$here/.venv/bin/python" "$@"
  elif [[ -x "$RUNNER/.venv/bin/python" ]]; then "$RUNNER/.venv/bin/python" "$@"
  else python3 "$@"; fi
}

chunks() { py "$(dirname "$0")/budget.py" chunks "$1" "$2" "$3"; }

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [backfill] $*" | tee -a "${SCAN_LOG:-data/_scan.log}"; }

# How many open PRs have this chunk's branch (claude/scan-<day>-backfill-FROM-TO).
# Fails when GitHub can't be read: an unreadable list is not "merged".
open_chunk_prs() {
  local slug refs
  slug="$(source scripts/lib.sh && repo_slug)" || return 1
  refs="$(gh api "repos/$slug/pulls?state=open&per_page=100" --jq '.[].head.ref')" || return 1
  printf '%s\n' "$refs" | grep -c -- "-backfill-$1-$2\$" || true
}

# Wait until the chunk's PR is merged or closed. 1 on timeout.
wait_for_pr() {
  local waited=0 limit="$WAIT_SECONDS" n
  ((limit > 0)) || return 0
  while :; do
    n="$(open_chunk_prs "$1" "$2" 2>/dev/null || echo unknown)"
    [[ "$n" == 0 ]] && return 0
    if ((waited >= limit)); then
      log "chunk $1..$2: its PR is still open after ${WAIT_SECONDS}s; stopping (start again to resume)"
      return 1
    fi
    ((waited == 0)) && log "chunk $1..$2: waiting for its PR to be merged or closed"
    sleep "$POLL_SECONDS"
    waited=$((waited + POLL_SECONDS))
  done
}

# The driver: every chunk in order, never twice in one run, never retried here.
drive() {
  local from to rc plan
  mkdir -p data
  if ! mkdir "$LOCK" 2>/dev/null; then
    if kill -0 "$(cat "$LOCK/pid" 2>/dev/null || echo 0)" 2>/dev/null; then
      OTHER_DRIVER=1 # finish must leave that driver's job and lock alone
      die "another backfill driver is running (pid $(cat "$LOCK/pid"))"
    fi
    rm -rf "$LOCK" && mkdir "$LOCK" # its driver died without cleaning up
  fi
  echo $$ >"$LOCK/pid"
  plan="$(chunks "$1" "$2" "$3")" || return 1
  log "start $1..$2 in chunks of $3 days (driver pid $$)"
  # A here-string, and the scan's stdin is /dev/null: the session must not
  # read the rest of the plan.
  while read -r from to; do
    rc=0
    log "chunk $from..$to: running"
    SCAN_BACKFILL_FROM="$from" SCAN_BACKFILL_TO="$to" /bin/bash scripts/run_scan_local.sh \
      </dev/null || rc=$?
    if [[ "$rc" == 3 ]]; then
      log "chunk $from..$to: skipped by the budget guard"
      continue
    fi
    if [[ "$rc" != 0 ]]; then
      log "chunk $from..$to: FAILED (exit $rc); stopping. See the scan-failure issue."
      return 1
    fi
    log "chunk $from..$to: done"
    wait_for_pr "$from" "$to" || return 1
  done <<<"$plan"
  log "finished $1..$2"
}

# One-shot: however the driver ends (finished, failed, or a `die`), drop our
# lock and the plist and unload our own job, so nothing can rerun it. bootout
# signals this process too, so it goes last. A driver refused because another
# one runs touches nothing.
finish() {
  [[ "$OTHER_DRIVER" == 1 ]] && return 0
  if [[ "$(cat "$LOCK/pid" 2>/dev/null)" == "$$" ]]; then rm -rf "$LOCK"; fi
  rm -f "$PLIST"
  "$LAUNCHCTL" bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
}

cmd_run() {
  cd "$(dirname "$0")/.."
  export SCAN_LOG="$PWD/data/_scan.log"
  trap finish EXIT
  check_args "$1" "$2" "$3"
  local rc=0
  drive "$@" || rc=$?
  return "$rc"
}

cmd_start() {
  check_args "$1" "$2" "$3"
  local first
  [[ -d "$RUNNER/.git" ]] || die "no runner clone at $RUNNER: run scripts/install_launchd.sh first"
  [[ "$RUNNER" != *[\'\&\<\>]* ]] || die "runner path can't contain ' & < >: $RUNNER"
  if "$LAUNCHCTL" print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
    die "already running ($LABEL); 'scripts/backfill.sh status', or 'stop' first"
  fi
  git -C "$RUNNER" fetch -q origin main
  git -C "$RUNNER" reset -q --hard origin/main
  [[ -f "$RUNNER/scripts/backfill.sh" ]] || die "origin/main has no scripts/backfill.sh yet"
  echo "Chunks:"
  chunks "$1" "$2" "$3" | sed 's/^/  /'
  first="$(chunks "$1" "$2" "$3" | head -n 1)"
  echo "Guard for the first chunk (${first/ /..}):"
  (cd "$RUNNER" && SCAN_RUNNER=local SCAN_BACKFILL_FROM="${first% *}" SCAN_BACKFILL_TO="${first#* }" \
    PYTHON="$RUNNER/.venv/bin/python" scripts/run_scan.sh check) || true
  write_plist "$@"
  "$LAUNCHCTL" bootstrap "$DOMAIN" "$PLIST"
  echo "Started $LABEL: $1..$2 in chunks of $3 days. Watch: scripts/backfill.sh status"
}

write_plist() {
  local run="cd '$RUNNER' || exit 1; exec /bin/bash scripts/backfill.sh run $1 $2 $3"
  mkdir -p "$(dirname "$PLIST")" "$RUNNER/data"
  cat >"$PLIST.new" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>-c</string><string>$run</string></array>
  <key>WorkingDirectory</key><string>$RUNNER</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><false/>
  <key>StandardOutPath</key><string>$RUNNER/data/_backfill_launchd.log</string>
  <key>StandardErrorPath</key><string>$RUNNER/data/_backfill_launchd.log</string>
</dict>
</plist>
EOF
  if command -v plutil >/dev/null; then plutil -lint "$PLIST.new" >/dev/null; fi
  mv "$PLIST.new" "$PLIST"
}

cmd_status() {
  if "$LAUNCHCTL" print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
    echo "$LABEL: loaded (running or finishing)"
  else
    echo "$LABEL: not loaded"
  fi
  echo "Last driver lines ($RUNNER/data/_scan.log):"
  grep -F "[backfill]" "$RUNNER/data/_scan.log" 2>/dev/null | tail -n 15 || echo "  (none)"
  echo "Spend (budget-ledger SPEND.md):"
  (cd "$RUNNER" && PYTHON="$RUNNER/.venv/bin/python" scripts/run_scan.sh status) || true
}

cmd_stop() {
  "$LAUNCHCTL" bootout "$DOMAIN/$LABEL" 2>/dev/null || echo "$LABEL was not loaded"
  rm -f "$PLIST"
  rm -rf "$RUNNER/data/_backfill.lock"
  echo "Stopped. A chunk cut off mid-run stays charged its reservation; start again to resume."
}

main() {
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    plan)
      check_args "${1:-}" "${2:-}" "${3:-$DEFAULT_CHUNK_DAYS}"
      chunks "$1" "$2" "${3:-$DEFAULT_CHUNK_DAYS}"
      ;;
    start) cmd_start "${1:-}" "${2:-}" "${3:-$DEFAULT_CHUNK_DAYS}" ;;
    run) cmd_run "${1:-}" "${2:-}" "${3:-$DEFAULT_CHUNK_DAYS}" ;;
    status) cmd_status ;;
    stop) cmd_stop ;;
    *)
      echo "usage: $0 plan|start|run FROM TO [CHUNK_DAYS] | status | stop" >&2
      exit 2
      ;;
  esac
}

main "$@"
