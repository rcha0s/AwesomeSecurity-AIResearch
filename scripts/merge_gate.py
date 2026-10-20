#!/usr/bin/env python3
"""
merge_gate.py — the checks a scan PR must pass before it can auto-merge.

Runs in automerge.yml's read-only `test` job, on main merged with the PR head
(the tree that would land). The path guard has already confirmed the PR changes
content only, so the code and config here are main's.

This is THE hook for Phase 3 evals: list a script under `automerge.evals` in
config.yaml. An eval whose script is missing is skipped with a notice until it is
declared `required: true`; from then on a missing script fails the gate (closed).

Usage: python scripts/merge_gate.py [--dry-run]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Always run. Each is a command, from the repo root.
BUILTIN = (
    ("pytest", [sys.executable, "-m", "pytest", "-q"]),
    ("claim ledger", [sys.executable, "scripts/add_claim.py", "validate"]),
    ("analysis eval", [sys.executable, "scripts/eval_analysis.py"]),
)


def declared_evals(config: dict) -> list[tuple[str, bool]]:
    """(script, required) pairs from `automerge.evals`. Malformed config raises."""
    entries = ((config or {}).get("automerge") or {}).get("evals") or []
    if not isinstance(entries, list):
        raise ValueError("automerge.evals must be a list")
    out = []
    for e in entries:
        script = e.get("script") if isinstance(e, dict) else None
        if not isinstance(script, str) or not script.startswith("scripts/") or ".." in script:
            raise ValueError(f"automerge.evals: bad entry {e!r}")
        out.append((script, e.get("required") is True))
    return out


def plan(config: dict, root: Path = ROOT) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """(steps to run, problems). A problem is a required eval with no script."""
    steps = list(BUILTIN)
    problems: list[str] = []
    for script, required in declared_evals(config):
        if (root / script).is_file():
            steps.append((script, [sys.executable, script]))
        elif required:
            problems.append(f"required eval {script} is missing")
        else:
            print(f"merge_gate: optional eval {script} not present yet; skipped")
    return steps, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="scan-PR merge gate")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    args = ap.parse_args(argv)
    config = yaml.safe_load((ROOT / "config.yaml").read_text()) or {}
    steps, problems = plan(config)
    for p in problems:
        print(f"merge_gate: FAIL {p}")
    failed = bool(problems)
    for name, cmd in steps:
        print(f"merge_gate: {name}: {' '.join(cmd)}", flush=True)
        if args.dry_run:
            continue
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            print(f"merge_gate: FAIL {name}")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
