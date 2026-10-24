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
# stderr, GitHub error annotation). Exit 2 = usage error, unknown profile,
# unresolvable base, or git diff failure. Fails closed: never exit 0 unless
# the diff was actually read.
set -euo pipefail

profile="${1:-}"
base="${2:-origin/main}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# allowed <path>: succeed if the profile may touch it.
case "$profile" in
  source-scout)
    allowed() { [[ "$1" == "data/source_proposals.json" ]]; }
    ;;
  render-refresh)
    # The exact list update.yml stages (shared file). Trailing / = directory.
    list="$here/bot_paths/render-refresh.txt"
    [[ -r "$list" ]] || { echo "guard_bot_diff: cannot read $list" >&2; exit 2; }
    entries=()
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == \#* ]] && continue
      entries+=("$line")
    done <"$list"
    ((${#entries[@]} > 0)) || { echo "guard_bot_diff: empty path list $list" >&2; exit 2; }
    allowed() {
      local e
      for e in "${entries[@]}"; do
        if [[ "$e" == */ ]]; then
          [[ "$1" == "$e"* ]] && return 0
        else
          [[ "$1" == "$e" ]] && return 0
        fi
      done
      return 1
    }
    ;;
  *)
    echo "guard_bot_diff: unknown profile '$profile' (source-scout|render-refresh)" >&2
    exit 2
    ;;
esac

if ! git rev-parse --verify --quiet "${base}^{commit}" >/dev/null; then
  echo "::error::guard_bot_diff: base '$base' does not resolve to a commit; refusing (fail closed)" >&2
  exit 2
fi

# Two-dot on purpose: tip vs base. -z keeps odd filenames intact; --no-renames
# reports both sides of a rename, so a move out of a protected path is seen.
# Written to a file so a git failure is seen (process substitution hides it).
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
if ! git diff --name-only --no-renames -z "$base" HEAD >"$tmp"; then
  echo "::error::guard_bot_diff: git diff failed; refusing (fail closed)" >&2
  exit 2
fi

stray=()
while IFS= read -r -d '' f; do
  allowed "$f" || stray+=("$f")
done <"$tmp"

if ((${#stray[@]} > 0)); then
  echo "::error::guard_bot_diff[$profile]: ${#stray[@]} path(s) outside the allowed set; refusing to push/open a PR" >&2
  printf '  stray: %s\n' "${stray[@]:0:50}" >&2
  exit 1
fi
echo "guard_bot_diff[$profile]: diff vs $base is within the allowed set."
