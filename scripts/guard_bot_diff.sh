#!/usr/bin/env bash
# guard_bot_diff.sh - Refuse a bot branch whose diff against main strays.
#
# A bot PR must contain only that bot's own output. The 2026-10-23 incident
# (PR #98) was a branch built on an old main: its diff reverted 41 unrelated
# files. Comparing the branch TIP to main (two-dot, not merge-base) catches
# exactly that, because a stale base shows up as reverted files.
#
# Usage: scripts/guard_bot_diff.sh <profile> [base-ref]   (run on the branch)
#   profile   source-scout | render-refresh
#   base-ref  default origin/main
# Exit 0 = every changed path is allowed. Exit 1 = stray paths (listed on
# stderr, GitHub error annotation). Exit 2 = usage/unknown profile.
set -euo pipefail

profile="${1:-}"
base="${2:-origin/main}"

# allowed <path>: succeed if the profile may touch it.
case "$profile" in
  source-scout)
    allowed() { [[ "$1" == "data/source_proposals.json" ]]; }
    ;;
  render-refresh)
    # Mirror the `paths` staged in update.yml: top-level data/*.json (no
    # subdirs, so data/evals/ and data/_raw/ are out), the four root reports,
    # and the generated trees.
    allowed() {
      [[ "$1" =~ ^data/[^/]+\.json$ ]] && return 0
      case "$1" in
        README.md | NEWSLETTER.md | TRENDS.md | REVIEW.md) return 0 ;;
        ai-security/* | product-security/* | ai-research/* | claims/* | docs/*) return 0 ;;
      esac
      return 1
    }
    ;;
  *)
    echo "guard_bot_diff: unknown profile '$profile' (source-scout|render-refresh)" >&2
    exit 2
    ;;
esac

# Two-dot on purpose: tip vs base. -z keeps odd filenames intact; --no-renames
# reports both sides of a rename, so a move out of a protected path is seen.
stray=()
while IFS= read -r -d '' f; do
  allowed "$f" || stray+=("$f")
done < <(git diff --name-only --no-renames -z "$base" HEAD)

if ((${#stray[@]} > 0)); then
  echo "::error::guard_bot_diff[$profile]: ${#stray[@]} path(s) outside the allowed set; refusing to push/open a PR" >&2
  printf '  stray: %s\n' "${stray[@]:0:50}" >&2
  exit 1
fi
echo "guard_bot_diff[$profile]: diff vs $base is within the allowed set."
