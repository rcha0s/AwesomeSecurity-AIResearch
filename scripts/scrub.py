#!/usr/bin/env python3
"""
scrub.py — Print a scan's PR body, or a safe default if it looks like it leaks.

The run summary is written by the model, and the model reads attacker-
controlled text, so a prompt injection could try to smuggle a secret into the
public PR body. This prints the summary only when it has no secret-shaped
string and no exact copy of a secret-named environment variable's value;
otherwise it prints the default body and says why on stderr. It never fails
the run: publishing the plain default is always safe.

Usage:
    python scripts/scrub.py data/_summary.md "<default body>"
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

MAX_CHARS = 20_000
MIN_SECRET_LEN = 8
SECRET_ENV_NAME = re.compile(r"TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|AUTH|CREDENTIAL", re.I)
NOT_SECRETS = {"proxy-injected"}
SECRET_PATTERNS = (
    re.compile(r"\b(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{32,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
)


def env_secrets(environ: dict[str, str]) -> set[str]:
    return {
        v
        for k, v in environ.items()
        if SECRET_ENV_NAME.search(k) and len(v) >= MIN_SECRET_LEN and v not in NOT_SECRETS
    }


def leak_reason(text: str, environ: dict[str, str]) -> str | None:
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            return f"matches secret pattern {pat.pattern[:24]}…"
    if any(secret in text for secret in env_secrets(environ)):
        return "contains a secret environment value"
    return None


def safe_body(path: Path, default: str, environ: dict[str, str]) -> str:
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8", errors="replace")
    reason = leak_reason(text, environ)
    if reason:
        print(f"scrub: summary withheld ({reason}); using the default body", file=sys.stderr)
        return default + "\n\n_Run summary withheld: it contained secret-like text._"
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n_(summary truncated)_"
    return text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    print(safe_body(Path(argv[0]), argv[1], dict(os.environ)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
