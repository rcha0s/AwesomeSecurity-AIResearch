# go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)

**Published:** Aug 7, 2026

> **Takeaway:** A path-string allowlist is not a symlink-safe boundary; you have to make the filesystem wrapper itself reject symlink escapes at open time.

## TL;DR

go-git's worktreeFilesystem wrapper rejected obviously dangerous path strings (containing .git, parent components, or control characters) but did not stop filesystem operations from following symlinks that were already present in the worktree. An attacker who can plant a symlink inside a worktree can therefore cause writes to land in .git/config or any other target, escaping the wrapper's string-level checks.

## What to learn

- String-level path filtering is insufficient when the filesystem below the wrapper honors existing symlinks. - _"The `worktreeFilesystem` wrapper rejected dangerous path strings, including paths containing `.git`, parent-directory components, or control characters. However, it did not prevent filesystem operations from following symbolic links that were already present in the worktree."_
- A symlink placed anywhere in the path, including the final component, converts a benign-looking write into a write into repository metadata. - _"As a result, a path that is safe when evaluated as a string could still resolve into the repository's Git metadata directory. For example, if `s` is a symbolic link to `.git`, writing to `s/config` would modify `.git/config`."_
- The fix reframes the wrapper as a symlink-safe boundary, checking every path component at operation time, not the input string. - _"The issue has been addressed by making the worktree filesystem wrapper a symlink-safe boundary. Worktree operations now reject paths where an existing symbolic link in any path component could cause the operation to escape the intended worktree location, including symbolic links at the final component."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker who can plant or modify a symlink inside a worktree (via a crafted commit, an unpacked tarball, or a prior filesystem write) can cause go-git worktree operations to overwrite .git/config or other sensitive files. Modifying .git/config can redirect hooks, change remote URLs, or set core.sshCommand to attacker-controlled code, giving code execution on the next Git operation.
- **Conditions:** Application uses go-git v5 <= 5.19.1 or v6 <= 6.0.0-alpha.4 with a filesystem-backed worktree, and processes content from which an attacker can introduce symlinks inside the worktree.
- **Mitigations:** Upgrade to go-git v5.19.2 or v6.0.0-alpha.5. Where infeasible, switch the storer/worktree to storage/memory or go-billy/memfs (not affected). Do not treat string-level path validation as a substitute for symlink-aware resolution.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [source](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm)  ·  **Retrieved:** 2026-08-10  
**Scores:** Newness 20 · Novelty 60 · Relevance 75 · Credibility 70 · **Composite 56.0**  
**Tags:** `symlink`, `path-traversal`, `cwe-59`, `go`, `git`

_Source: [https://github.com/advisories/GHSA-hc8v-wwc9-vgxm](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm)_  ·  [← back to index](../README.md)
