#!/usr/bin/env bash
# ensure_pr.sh - Open a PR for an already-pushed bot branch unless one is open.
#
# The one sanctioned way the pipeline opens its PRs (render, source-scout,
# research-scan). Never `gh pr view <branch>`: it also matches merged/closed
# PRs, so after the first merge the create step was skipped silently and
# render drift had no PR from 2026-07-31 to 2026-10-19.
#
# In GitHub Actions the PR is made with GITHUB_TOKEN, which does not fire
# pull_request workflows, so the Tests check would never run on it. A
# workflow_dispatch IS allowed from GITHUB_TOKEN, and its check run lands on
# the branch head, so the PR shows it. Callers need `actions: write`.
#
# Usage: scripts/ensure_pr.sh <branch> <title> <body>
set -euo pipefail

branch="$1"
title="$2"
body="$3"

open_prs="$(gh pr list --state open --head "$branch" --json number --jq length)"
if [[ ! "$open_prs" =~ ^[0-9]+$ ]]; then
  echo "ensure_pr: unexpected 'gh pr list' output: $open_prs" >&2
  exit 1
fi

if [[ "$open_prs" == "0" ]]; then
  gh pr create --base main --head "$branch" --title "$title" --body "$body"
else
  echo "ensure_pr: PR already open for $branch; it picks up the new head."
fi

if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
  gh workflow run tests.yml --ref "$branch"
fi
