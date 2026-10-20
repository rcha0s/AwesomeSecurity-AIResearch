#!/usr/bin/env python3
"""
merge_guard.py — the security boundary of scan-PR auto-merge (ISA ISC-27, Anti ISC-A3).

Scan PRs are written by a model that reads attacker-controlled text. A prompt
injection may change content; it must never be able to change the pipeline. This
module decides, from data alone, whether a PR is content-only. It is pure: no
network, no git, no clock. `automerge.py` gathers the inputs and acts on the verdict.

A PR passes only if ALL of these hold (anything unrecognised is refused):
  - it is open, not a draft, not labelled `automerge:hold`, targets `main` of this
    repo, comes from a branch of this repo (no forks) named `claude/scan-*`, and its
    head is exactly the SHA that was evaluated;
  - every path git reports (`git diff --raw -z --no-renames`, so a rename is a
    delete + add and both sides are checked) and every path the files API reports
    (filename and previous_filename) is on the allowlist, the two sets agree, and
    the API list isn't truncated;
  - every added/modified file is a regular non-executable file (mode 100644): no
    symlinks, submodules, executables or type changes.

Usage (debugging): python scripts/merge_guard.py <pr.json> <files.json> <raw.diff> <repo> <sha>
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Content the pipeline renders or stores. Everything else (scripts/, .github/,
# .claude/, tests/, evals/, config, requirements, agent docs, ...) never auto-merges.
ALLOWED_DIRS = ("data/", "docs/", "ai-security/", "product-security/", "ai-research/", "claims/")
ALLOWED_ROOT_FILES = frozenset({"README.md", "NEWSLETTER.md", "TRENDS.md", "REVIEW.md"})
# Pipeline tuning that lives under data/ but steers the code: never via a scan PR.
DENIED_FILES = frozenset(
    {"data/cluster_keywords.yaml", "data/interests.yaml", "data/source_blocklist.json"}
)
# Transient staging (gitignored): its appearance in a PR is itself an anomaly.
DENIED_PREFIXES = ("data/_",)
DENIED_NAMES = frozenset(
    {"candidates.json", "candidates.filtered.json", "analysis_out.json", "editorial_out.json"}
)
ALLOWED_SUFFIXES = (".json", ".md", ".html", ".png")
ALLOWED_DOTFILES = frozenset({"docs/.nojekyll"})
SAFE_PATH = re.compile(r"[A-Za-z0-9._/-]+")
MAX_PATH_LEN = 300

REGULAR_FILE = "100644"
ABSENT = "000000"
GIT_STATUSES = frozenset({"A", "D", "M"})
API_STATUSES = frozenset({"added", "removed", "modified", "renamed"})
API_FILE_CAP = 3000  # the PR files API stops listing at 3000 files

SCAN_BRANCH = re.compile(r"claude/scan-[A-Za-z0-9._-]+")
BASE_BRANCH = "main"
HOLD_LABEL = "automerge:hold"
SHA = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True)
class Change:
    """One record of `git diff --raw -z --no-renames`."""

    old_mode: str
    new_mode: str
    status: str
    path: str


@dataclass
class Verdict:
    ok: bool
    reasons: list[str] = field(default_factory=list)
    paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"ok": self.ok, "reasons": self.reasons, "paths": self.paths}


def display(path: str) -> str:
    """A path made safe to echo into a PR comment or log (attacker-controlled text)."""
    shown = "".join(ch if SAFE_PATH.fullmatch(ch) else "?" for ch in path[:120])
    return shown + ("..." if len(path) > 120 else "")


def _segment_reason(path: str) -> str | None:
    if not path or len(path) > MAX_PATH_LEN:
        return "empty or overlong path"
    if not SAFE_PATH.fullmatch(path):
        return "path has characters outside [A-Za-z0-9._/-]"
    segments = path.split("/")
    if any(s in ("", ".", "..") for s in segments):
        return "path has an empty, '.' or '..' segment"
    if any(s.startswith(".") for s in segments) and path not in ALLOWED_DOTFILES:
        return "dotfile or dot-directory"
    return None


def path_reason(path: str) -> str | None:
    """None if `path` is allowlisted content, else why it is refused."""
    bad = _segment_reason(path)
    if bad:
        return bad
    name = path.rsplit("/", 1)[-1]
    if path in DENIED_FILES or name in DENIED_NAMES or path.startswith(DENIED_PREFIXES):
        return "pipeline config or transient staging file"
    in_dir = path.startswith(ALLOWED_DIRS)
    if not in_dir and path not in ALLOWED_ROOT_FILES:
        return "outside the content allowlist"
    if in_dir and path not in ALLOWED_DOTFILES and not path.endswith(ALLOWED_SUFFIXES):
        return "file type not allowed in content directories"
    return None


def mode_reason(change: Change) -> str | None:
    """None if the change is a plain-file add/modify or a delete, else why not."""
    if change.status not in GIT_STATUSES:
        return f"git status {change.status!r} (type change, unmerged or unknown)"
    if change.status == "D":
        return None if change.new_mode == ABSENT else "delete with a non-empty new mode"
    if change.new_mode != REGULAR_FILE:
        return f"mode {change.new_mode} (symlink, submodule or executable)"
    return None


def parse_raw_diff(raw: str) -> list[Change]:
    """Parse `git diff --raw -z --no-renames` output. Raises ValueError if malformed."""
    tokens = raw.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    changes: list[Change] = []
    i = 0
    while i < len(tokens):
        header = tokens[i]
        fields = header[1:].split(" ") if header.startswith(":") else []
        if len(fields) != 5 or i + 1 >= len(tokens):
            raise ValueError("malformed raw diff record")
        old_mode, new_mode, _old, _new, status = fields
        changes.append(Change(old_mode, new_mode, status, tokens[i + 1]))
        # A rename/copy record carries two paths; --no-renames should never emit one.
        i += 3 if status[:1] in ("R", "C") else 2
    return changes


def _api_reasons(files: list[dict]) -> tuple[set[str], list[str]]:
    paths: set[str] = set()
    reasons: list[str] = []
    if len(files) >= API_FILE_CAP:
        reasons.append(f"files API list may be truncated ({len(files)} files)")
    for f in files:
        status = f.get("status")
        name = f.get("filename")
        if not isinstance(name, str):
            reasons.append("files API entry without a filename")
            continue
        paths.add(name)
        prev = f.get("previous_filename")
        if isinstance(prev, str):
            paths.add(prev)
        if status not in API_STATUSES:
            reasons.append(f"{display(name)}: files API status {status!r}")
    return paths, reasons


def _label_names(pr: dict) -> set[str]:
    return {lab.get("name") for lab in pr.get("labels") or [] if isinstance(lab, dict)}


def pr_reasons(pr: dict, repo: str, expected_sha: str) -> list[str]:
    """Why this PR's metadata disqualifies it (empty list = eligible)."""
    head, base = pr.get("head") or {}, pr.get("base") or {}
    head_repo = (head.get("repo") or {}).get("full_name")
    checks = [
        (pr.get("state") == "open", "PR is not open"),
        (pr.get("draft") is False, "PR is a draft"),
        (HOLD_LABEL not in _label_names(pr), f"PR is labelled {HOLD_LABEL}"),
        (base.get("ref") == BASE_BRANCH, "base branch is not main"),
        ((base.get("repo") or {}).get("full_name") == repo, "base is another repository"),
        (head_repo == repo, "head is a fork or a deleted repository"),
        (bool(SCAN_BRANCH.fullmatch(head.get("ref") or "")), "head branch is not claude/scan-*"),
        (bool(SHA.fullmatch(expected_sha or "")), "no evaluated head SHA"),
        (head.get("sha") == expected_sha, "head moved since it was evaluated"),
    ]
    return [msg for ok, msg in checks if not ok]


def evaluate(
    pr: dict, files: list[dict], changes: list[Change], repo: str, expected_sha: str
) -> Verdict:
    """The merge decision. Fails closed: any doubt is a refusal."""
    reasons = pr_reasons(pr, repo, expected_sha)
    api_paths, api_problems = _api_reasons(files)
    reasons += api_problems
    git_paths = {c.path for c in changes}
    if not git_paths:
        reasons.append("no changes")
    if api_paths != git_paths:
        reasons.append("git and the files API disagree on the changed paths")
    for change in changes:
        bad = mode_reason(change)
        if bad:
            reasons.append(f"{display(change.path)}: {bad}")
    for path in sorted(api_paths | git_paths):
        bad = path_reason(path)
        if bad:
            reasons.append(f"{display(path)}: {bad}")
    return Verdict(ok=not reasons, reasons=reasons, paths=sorted(api_paths | git_paths))


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__, file=sys.stderr)
        return 2
    pr = json.loads(Path(argv[1]).read_text())
    files = json.loads(Path(argv[2]).read_text())
    changes = parse_raw_diff(Path(argv[3]).read_text(encoding="utf-8", errors="replace"))
    verdict = evaluate(pr, files, changes, argv[4], argv[5])
    print(json.dumps(verdict.to_dict(), indent=2))
    return 0 if verdict.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
