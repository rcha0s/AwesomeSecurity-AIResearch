#!/usr/bin/env bash
# scan_alert.sh - A failed scan opens (or comments on) a GitHub issue (ISC-9).
#
# One open `scan-failure` issue collects every failure until someone closes
# it, so a dead pipeline is loud without opening an issue per day. REST only
# (see lib.sh). If even the alert fails, it exits non-zero so the runner's
# own log shows it.
#
# Usage: scripts/scan_alert.sh <runner> <phase> [logfile]
set -euo pipefail
source "$(dirname "$0")/lib.sh"

runner="$1"
phase="$2"
log="${3:-}"
repo="$(repo_slug)"
label="scan-failure"
when="$(date -u +%Y-%m-%dT%H:%MZ)"

tail_text="(no log)"
if [[ -n "$log" && -f "$log" ]]; then
  tail_text="$(tail -n 40 "$log")"
fi
body="Scan failed: runner \`$runner\`, phase \`$phase\`, at $when.

<details><summary>Last 40 log lines</summary>

\`\`\`
$tail_text
\`\`\`
</details>"

# 422 = the label already exists; anything else is a real error.
gh api -X POST "repos/$repo/labels" -f name="$label" -f color=d73a4a \
  -f description="Daily scan failed" >/dev/null 2>&1 || true

open_issue="$(gh api "repos/$repo/issues?state=open&labels=$label" --jq '.[0].number // 0')"
require_int "$open_issue" "scan_alert: open issue number"

if [[ "$open_issue" != "0" ]]; then
  gh api -X POST "repos/$repo/issues/$open_issue/comments" -f body="$body" --jq .html_url
else
  gh api -X POST "repos/$repo/issues" -f title="Daily scan failing ($runner, $phase)" \
    -f body="$body" -f "labels[]=$label" --jq .html_url
fi
