#!/usr/bin/env bash
# scan_alert.sh - A failed scan opens (or comments on) a GitHub issue (ISC-9).
#
# One open `scan-failure` issue collects every failure until someone closes
# it, so a dead pipeline is loud without opening an issue per day. REST only
# (see lib.sh). The public issue carries the runner, phase and time, never log
# text: logs hold model-written and ingested content, so a prompt injection
# could use them to publish secrets. The log stays on the runner
# (the scan worktree's data/_scan.log locally, the session transcript in the cloud).
#
# Usage: scripts/scan_alert.sh <runner> <phase>
set -euo pipefail
source "$(dirname "$0")/lib.sh"

runner="$1"
phase="$2"
[[ "$runner" =~ ^(cloud|local)$ ]] || runner="unknown"
[[ "$phase" =~ ^[A-Za-z0-9_-]{1,40}$ ]] || phase="unknown"
repo="$(repo_slug)"
label="scan-failure"
when="$(date -u +%Y-%m-%dT%H:%MZ)"
where="the session transcript of the cloud run"
[[ "$runner" == local ]] && where="data/_scan.log in the Mac scan worktree"
body="Scan failed: runner \`$runner\`, phase \`$phase\`, at $when. Details: $where."

# Only "already exists" is expected here; any other failure is real.
if ! out="$(gh api -X POST "repos/$repo/labels" -f name="$label" -f color=d73a4a \
  -f description="Daily scan failed" 2>&1)"; then
  [[ "$out" == *already_exists* ]] || {
    echo "scan_alert: cannot create label: $out" >&2
    exit 1
  }
fi

open_issue="$(gh api "repos/$repo/issues?state=open&labels=$label" --jq '.[0].number // 0')"
require_int "$open_issue" "scan_alert: open issue number"

if [[ "$open_issue" != "0" ]]; then
  gh api -X POST "repos/$repo/issues/$open_issue/comments" -f body="$body" --jq .html_url
else
  gh api -X POST "repos/$repo/issues" -f title="Daily scan failing ($runner, $phase)" \
    -f body="$body" -f "labels[]=$label" --jq .html_url
fi
