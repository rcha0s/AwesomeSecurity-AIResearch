# lib.sh - Shared helpers for the scan's shell scripts. Source, don't run.
#
# GitHub calls go through `gh api` (REST) only. In Claude Code cloud sessions
# the GitHub proxy rejects GraphQL, so `gh pr` and `gh issue` get a 403
# (cloud-environments.md § GitHub proxy).

# owner/repo of origin: GITHUB_REPOSITORY in Actions, else the remote URL's
# last two path segments (works for github.com and the cloud's proxy remote).
repo_slug() {
  if [[ -n "${GITHUB_REPOSITORY:-}" ]]; then
    echo "$GITHUB_REPOSITORY"
    return
  fi
  local url
  url="$(git remote get-url origin)"
  url="${url%/}"
  url="${url%.git}"
  if [[ ! "$url" =~ ([^/:]+)/([^/]+)$ ]]; then
    echo "repo_slug: cannot parse origin URL: $url" >&2
    return 1
  fi
  echo "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
}

# Fail loudly on anything that isn't a non-negative integer.
require_int() {
  if [[ ! "$1" =~ ^[0-9]+$ ]]; then
    echo "$2: expected a number, got: $1" >&2
    return 1
  fi
}
