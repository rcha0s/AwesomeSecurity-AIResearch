#!/usr/bin/env python3
"""
merge_gate.py — the checks a scan PR must pass before it can auto-merge.

Runs in automerge.yml's read-only `test` job, on main merged with the PR head
(the tree that would land). The path guard has already confirmed the PR changes
content only, so the code and config here are main's.

This is THE hook for Phase 3 evals: list a script under `automerge.evals` in
config.yaml. An eval whose script is missing is skipped with a notice until it is
declared `required: true`; from then on a missing script fails the gate (closed).

It also runs content_checks.py in-process: URL schemes in data/*.json, render
equality of docs/index.html (raw bytes, so line endings count) and of
docs/feed.xml (main's render_feed of that page's data), claim-ledger history against main (`--base`),
sticky editorial promotions (a removal needs a human unless main had already lost integrity),
and the eval history: main's rows untouched, at most one new row, and that row's
charge, integrity, golden result and cap checked against the budget ledger
(origin/budget-ledger) and recomputed on this tree.

Usage: python scripts/merge_gate.py [--base <main sha or ref>] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import content_checks as cc
import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER_REF = "origin/budget-ledger"  # where run_scan.sh keeps the spend ledger

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


def main_ledger(base: str) -> object:
    """main's claim ledger, straight from git (never from the PR's tree)."""
    cmd = ["git", "show", f"{base}:data/claims.json"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, check=True)
    return json.loads(out.stdout)


def main_stories(base: str) -> object:
    """main's story ledger, straight from git ({} if main has none yet)."""
    cmd = ["git", "show", f"{base}:data/news_stories.json"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    return json.loads(out.stdout) if out.returncode == 0 else {}


def content_problems(base: str, root: Path = ROOT) -> list[str]:
    """URL schemes, render equality and claim history for the tree at `root`."""
    import generate_html  # main's renderer (import is slow; only when checking)

    out: list[str] = []
    for path in sorted((root / "data").glob("*.json")):
        found = cc.url_problems(json.loads(path.read_text(encoding="utf-8")))
        out += [f"{path.name}: {p}" for p in found]
    page = root / "docs" / "index.html"
    if page.is_file():
        out += cc.render_problems(read_exact(page), generate_html.render)
    else:
        out.append("docs/index.html is missing")
    out += feed_check(base, root)
    pr_ledger = json.loads((root / "data" / "claims.json").read_text(encoding="utf-8"))
    out += cc.claim_history_problems(main_ledger(base), pr_ledger)
    stories = root / "data" / "news_stories.json"
    pr_stories = json.loads(stories.read_text(encoding="utf-8")) if stories.is_file() else {}
    out += cc.story_membership_problems(main_stories(base), pr_stories)
    out += editorial_check(base, root)
    out += readability_check(base, root)
    out += history_check(base, root)
    return out


def read_exact(path: Path) -> str:
    """A file's text with its line endings untouched (read_text would turn CRLF and
    CR into LF, so a CRLF copy would pass byte-equality). Invalid UTF-8 raises."""
    return path.read_bytes().decode("utf-8")


def main_has_feed(base: str) -> bool:
    """Whether main already publishes docs/feed.xml. Fails closed: an unknown base
    or any git error raises, it never reads as "no feed"."""
    ok = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
    )
    if ok.returncode != 0:
        raise RuntimeError(f"base {base!r} is not a commit; cannot tell if main has a feed")
    found = subprocess.run(
        ["git", "ls-tree", "--name-only", base, "docs/feed.xml"], cwd=ROOT, capture_output=True
    )
    if found.returncode != 0:
        raise RuntimeError(f"git ls-tree failed ({found.returncode}): {found.stderr[:200]!r}")
    return found.stdout.strip() == b"docs/feed.xml"  # empty output: no such path on main


def feed_check(base: str, root: Path = ROOT) -> list[str]:
    """docs/feed.xml is main's render_feed() of the payload the PR's index.html carries."""
    import generate_html

    page, feed = root / "docs" / "index.html", root / "docs" / "feed.xml"
    if not page.is_file():
        return []  # already reported as "docs/index.html is missing"
    text = read_exact(feed) if feed.is_file() else None
    return cc.feed_problems(text, read_exact(page), generate_html.render_feed, main_has_feed(base))


def pool_docs(base: str, root: Path = ROOT) -> tuple[list, list]:
    """(main's pools + archive from git, this tree's pools + archive)."""
    import common as c

    names = [f"{t}.json" for t in c.TOPICS] + ["archive.json"]
    main_docs = [git_json(f"{base}:data/{n}", {}) for n in names]
    pr_docs = []
    for n in names:
        path = root / "data" / n
        pr_docs.append(json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {})
    return main_docs, pr_docs


def editorial_check(base: str, root: Path = ROOT) -> list[str]:
    """Promotions on main stay promoted unless main's copy had already lost integrity."""
    return cc.editorial_problems(*pool_docs(base, root))


def readability_check(base: str, root: Path = ROOT) -> list[str]:
    """An entry main shows may not gain a readability hold without a human."""
    import common as c

    main_docs, pr_docs = pool_docs(base, root)
    # Pools only: an archived finding is not on the site.
    shown = cc.shown_ids(main_docs[:-1], c.load_config(), c.load_sources_by_id())
    return cc.readability_problems(shown, pr_docs)


def git_json(ref_path: str, default: object) -> object:
    """A JSON file from a git ref (`<ref>:<path>`), or `default` if it isn't there."""
    out = subprocess.run(["git", "show", ref_path], cwd=ROOT, capture_output=True)
    return json.loads(out.stdout) if out.returncode == 0 else default


def history_check(base: str, root: Path = ROOT, ledger_ref: str = LEDGER_REF) -> list[str]:
    """The eval history (ISC-26) only grows by one row that the gate can vouch for:
    its ledger charge, and the integrity, golden result and cap recomputed here."""
    import eval_history as eh
    import eval_integrity
    import eval_lib as el

    path = root / "data" / "evals" / "history.json"
    pr_history = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    main_history = git_json(f"{base}:data/evals/history.json", {})
    if pr_history == main_history:
        return []
    ledger = git_json(f"{ledger_ref}:budget.json", {}) or {}
    cfg = el.settings(root / "config.yaml")
    recomputed = {
        "integrity": eval_integrity.run()["passed"],
        "golden": eh.weekly("golden", eh.GOLDEN_KEYS, int(cfg["max_result_age_days"])),
        "cap_usd": el.per_run_cap(root / "config.yaml"),
    }
    return cc.history_problems(main_history, pr_history, ledger.get("runs") or [], recomputed)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="scan-PR merge gate")
    ap.add_argument("--base", default="origin/main", help="main's commit, for claim history")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    args = ap.parse_args(argv)
    config = yaml.safe_load((ROOT / "config.yaml").read_text()) or {}
    steps, problems = plan(config)
    if not args.dry_run:
        try:
            problems += content_problems(args.base)
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            problems.append(f"content checks could not run: {type(exc).__name__}")
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
