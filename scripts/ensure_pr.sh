#!/usr/bin/env bash
# ensure_pr.sh - Open a PR for an already-pushed bot branch unless one is open.
#
# The one sanctioned way the pipeline opens its PRs (render, source-scout,
# scan). Never `gh pr view <branch>`: it also matches merged/closed PRs, so
# after the first merge the create step was skipped silently and render drift
# had no PR from 2026-07-31 to 2026-10-19. REST only (see lib.sh): `gh pr`
# is GraphQL and gets a 403 in cloud sessions.
#
# In GitHub Actions the PR is made with GITHUB_TOKEN, which does not fire
# pull_request workflows, so the Tests check would never run on it. A
# workflow_dispatch IS allowed from GITHUB_TOKEN, and its check run lands on
# the branch head. Callers need `actions: write`.
#
# Usage: scripts/ensure_pr.sh <branch> <title> <body>
set -euo pipefail
source "$(dirname "$0")/lib.sh"

branch="$1"
title="$2"
body="$3"
repo="$(repo_slug)"

open_prs="$(gh api "repos/$repo/pulls?state=open&head=${repo%%/*}:$branch" --jq length)"
require_int "$open_prs" "ensure_pr: open-PR count"

if [[ "$open_prs" == "0" ]]; then
  gh api -X POST "repos/$repo/pulls" -f title="$title" -f head="$branch" \
    -f base=main -f body="$body" --jq .html_url
else
  echo "ensure_pr: PR already open for $branch; it picks up the new head."
fi

if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
  gh workflow run tests.yml --ref "$branch"
fi
