#!/usr/bin/env python3
"""
automerge.py — drives gated auto-merge of scan PRs (.github/workflows/automerge.yml).

Always runs MAIN's code from a checkout of main; it never imports, installs or
executes anything from a PR. PR content is fetched as git objects and diffed, which
reads trees but runs nothing. The decision itself is `merge_guard.evaluate`.

  select   (read-only job)  evaluate every open claude/scan-* PR; write a step
                            summary; emit `number`/`sha` of the oldest that passes
                            the path guard, for the read-only test job to test,
                            skipping a head the gate already refused; and the
                            `rebuild_*` of the oldest that conflicts with main, for
                            the rebuild job (scripts/rebuild_pr.py).
  decide   (write job)      re-fetch and re-evaluate everything (the head must still
                            be the SHA that was tested), report each verdict, and in
                            `merge` mode merge the tested PR with `sha=<that SHA>`.

GitHub calls are REST via `gh api` (cloud sessions 403 on GraphQL; see lib.sh).
The mode comes from config.yaml in this checkout of main, never the PR head.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import merge_guard as mg
import yaml

ROOT = Path(__file__).resolve().parent.parent
MODES = ("shadow", "merge")
MERGE_METHODS = ("squash", "merge", "rebase")
PYTEST_APP_ID = 15368  # GitHub Actions: main's required `pytest` check
MARKER = "<!-- automerge-gate"
MAX_PAGES = 30  # 30 x 100 = the files API's 3000-file ceiling


def settings(config_path: Path) -> dict:
    """automerge settings from main's config. Anything unexpected reads as shadow."""
    try:
        cfg = (yaml.safe_load(config_path.read_text()) or {}).get("automerge") or {}
    except (OSError, yaml.YAMLError, AttributeError):
        cfg = {}
    if not isinstance(cfg, dict):
        cfg = {}
    mode = cfg.get("mode") if cfg.get("mode") in MODES else "shadow"
    method = cfg.get("merge_method") if cfg.get("merge_method") in MERGE_METHODS else "squash"
    # Rebuilding a conflicting scan PR writes to its branch: merge mode and an explicit true.
    return {
        "mode": mode,
        "merge_method": method,
        "rebuild": mode == "merge" and cfg.get("rebuild_conflicts") is True,
    }


# ---------------------------------------------------------------- GitHub / git I/O


def gh(path: str, *args: str) -> object:
    out = subprocess.run(["gh", "api", path, *args], check=True, capture_output=True, text=True)
    return json.loads(out.stdout) if out.stdout.strip() else None


def gh_pages(path: str) -> list:
    """GET a list endpoint page by page (REST, no --paginate/--slurp dependency)."""
    items: list = []
    sep = "&" if "?" in path else "?"
    for page in range(1, MAX_PAGES + 1):
        batch = gh(f"{path}{sep}per_page=100&page={page}")
        if not isinstance(batch, list):
            raise RuntimeError(f"expected a list from {path}")
        items += batch
        if len(batch) < 100:
            break
    return items


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return out.stdout.decode("utf-8", errors="replace")


def raw_changes(number: int, head_sha: str, main_sha: str) -> list[mg.Change]:
    """The PR's changes vs its merge base with main, as git sees them (no renames)."""
    git("fetch", "--no-tags", "--quiet", "origin", f"+refs/pull/{number}/head:refs/pr/{number}")
    if git("rev-parse", f"refs/pr/{number}").strip() != head_sha:
        raise RuntimeError("fetched PR head differs from the API's head SHA")
    base = git("merge-base", main_sha, head_sha).strip()
    raw = git("diff", "--raw", "-z", "--no-renames", "--no-ext-diff", base, head_sha)
    return mg.parse_raw_diff(raw)


def scan_prs(repo: str) -> list[dict]:
    """Open PRs into main whose head is named like a scan branch, oldest first."""
    prs = gh_pages(f"repos/{repo}/pulls?state=open&base=main&sort=created&direction=asc")
    return [p for p in prs if ((p.get("head") or {}).get("ref") or "").startswith("claude/scan-")]


def judge(repo: str, number: int, expected_sha: str, main_sha: str) -> mg.Verdict:
    """Fetch everything fresh for one PR and run the guard. Errors refuse."""
    try:
        pr = gh(f"repos/{repo}/pulls/{number}")
        files = gh_pages(f"repos/{repo}/pulls/{number}/files")
        changes = raw_changes(number, (pr or {}).get("head", {}).get("sha", ""), main_sha)
    except (subprocess.CalledProcessError, RuntimeError, ValueError, json.JSONDecodeError) as e:
        return mg.Verdict(ok=False, reasons=[f"could not evaluate: {type(e).__name__}"])
    return mg.evaluate(pr or {}, files, changes, repo, expected_sha)


# ---------------------------------------------------------------- reporting


def comment_body(sha: str, outcome: str, mode: str, reasons: list[str]) -> str:
    """A PR comment. Reasons are already display()-sanitised; still fenced."""
    key = hashlib.sha256(f"{sha}|{outcome}|{mode}|{reasons}".encode()).hexdigest()[:16]
    lines = [f"{MARKER} {key} -->", f"**Auto-merge gate** ({mode} mode): {outcome}", ""]
    lines.append(f"Evaluated head `{sha[:12]}`.")
    if reasons:
        lines += ["", "```text", *[r.replace("`", "'") for r in reasons[:25]], "```"]
        if len(reasons) > 25:
            lines.append(f"... and {len(reasons) - 25} more.")
    return "\n".join(lines)


def already_posted(repo: str, number: int, body: str) -> bool:
    marker = body.splitlines()[0]
    comments = gh_pages(f"repos/{repo}/issues/{number}/comments")
    return any(marker in (c.get("body") or "") for c in comments)


def post_once(repo: str, number: int, body: str) -> None:
    if not already_posted(repo, number, body):
        gh(f"repos/{repo}/issues/{number}/comments", "-X", "POST", "-f", f"body={body}")


def summary(lines: list[str]) -> None:
    text = "\n".join(lines) + "\n"
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


def output(**values: str) -> None:
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as fh:
            fh.writelines(f"{k}={v}\n" for k, v in values.items())


# ---------------------------------------------------------------- select


def conflicts_with_main(repo: str, number: int) -> bool:
    """True only when GitHub reports the PR unmergeable. `mergeable` is null while
    GitHub computes it, and an error is unknown too: both are tested as before."""
    try:
        return (gh(f"repos/{repo}/pulls/{number}") or {}).get("mergeable") is False
    except (subprocess.CalledProcessError, RuntimeError, ValueError, json.JSONDecodeError):
        return False


GATE_AUTHOR = "github-actions[bot]"
BRANCH = re.compile(r"claude/scan-[A-Za-z0-9._-]{1,100}")
REBUILT = re.compile(r"-rebuilt-[0-9a-f]{8}$")
TESTS_FAILED = "in-workflow tests or integrity checks failed"


def rebuild_failed(main_sha: str) -> str:
    return f"rebuild on main {main_sha[:12]} failed"


def refusals(repo: str, number: int, sha: str) -> set[str]:
    """The reasons this workflow already gave when it refused this exact head. Only
    its own comments count; an error reads as none."""
    try:
        comments = gh_pages(f"repos/{repo}/issues/{number}/comments")
    except (subprocess.CalledProcessError, RuntimeError, ValueError, json.JSONDecodeError):
        return set()
    found: set[str] = set()
    for c in comments:
        body = c.get("body") or ""
        if (
            (c.get("user") or {}).get("login") == GATE_AUTHOR
            and body.startswith(MARKER)
            and f"Evaluated head `{sha[:12]}`" in body
            and "): refused" in body
        ):
            found.update(line.strip() for line in body.splitlines())
    return found


def triage(repo: str, pr: dict, verdict: mg.Verdict, main_sha: str) -> str:
    """What select does with one PR: test, rebuild, skip, or nothing (refused).

    A head that conflicts with main fails the test job's merge every run, and a
    head whose tests failed fails them again: testing either first starved every
    newer scan PR behind it (#165, 11-06). Guard refusals (a hold label, a draft)
    are re-judged every run, so removing the label is enough to retry."""
    if not verdict.ok:
        return "refused"
    seen = refusals(repo, pr["number"], pr["head"]["sha"])
    if conflicts_with_main(repo, pr["number"]):
        return "skip-rebuild" if rebuild_failed(main_sha) in seen else "rebuild"
    return "skip" if TESTS_FAILED in seen else "test"


STATES = {
    "refused": "refused",
    "test": "passes the path guard",
    "rebuild": "passes the path guard; conflicts with main, to be rebuilt on main",
    "skip": "passes the path guard; its tests already failed on this head, skipped",
    "skip-rebuild": "passes the path guard; conflicts with main; rebuild already failed",
    "no-rebuild": "passes the path guard; conflicts with main, skipped (rebuild is off)",
}


def rebuilt_ref(ref: str, main_sha: str) -> str:
    """claude/scan-2026-11-04-local -> claude/scan-2026-11-04-local-rebuilt-<main>."""
    return f"{REBUILT.sub('', ref)}-rebuilt-{main_sha[:8]}"


def cmd_select(repo: str, main_sha: str) -> int:
    conf = settings(ROOT / "config.yaml")
    lines = [f"## Auto-merge gate: select ({conf['mode']} mode)", ""]
    picks: dict[str, dict] = {}
    for pr in scan_prs(repo):
        number, sha, ref = pr["number"], pr["head"]["sha"], pr["head"]["ref"]
        verdict = judge(repo, number, sha, main_sha)
        action = triage(repo, pr, verdict, main_sha)
        new_ref = rebuilt_ref(ref, main_sha)
        if action == "rebuild" and not (conf["rebuild"] and BRANCH.fullmatch(new_ref)):
            action = "no-rebuild"
        lines.append(f"- #{number} `{sha[:12]}`: {STATES[action]}")
        lines += [f"  - {r}" for r in verdict.reasons[:10]]
        if action in ("test", "rebuild"):
            picks.setdefault(action, {"number": str(number), "sha": sha, "ref": new_ref})
    if "test" not in picks:
        lines.append("- nothing to test")
    summary(lines)
    test, rb = picks.get("test", {}), picks.get("rebuild", {})
    output(number=test.get("number", ""), sha=test.get("sha", ""),
           rebuild_number=rb.get("number", ""), rebuild_sha=rb.get("sha", ""),
           rebuild_ref=rb.get("ref", ""))  # fmt: skip
    return 0


# ---------------------------------------------------------------- rebuild (write job)


def tree_reasons(main_sha: str, commit: str) -> list[str]:
    """The rebuilt commit must sit directly on main and change only content."""
    reasons = []
    if git("rev-parse", f"{commit}^@").split() != [main_sha]:
        reasons.append("rebuilt commit's only parent is not main")
    raw = git("diff", "--raw", "-z", "--no-renames", "--no-ext-diff", main_sha, commit)
    changes = mg.parse_raw_diff(raw)
    if not changes:
        reasons.append("no changes")
    for change in changes:
        bad = mg.mode_reason(change) or mg.path_reason(change.path)
        if bad:
            reasons.append(f"{mg.display(change.path)}: {bad}")
    return reasons


def cmd_check_tree(main_sha: str, commit: str) -> int:
    if not mg.SHA.fullmatch(commit):
        print("check-tree: --commit must be a 40-hex SHA", file=sys.stderr)
        return 1
    reasons = tree_reasons(main_sha, commit)
    for r in reasons:
        print(f"check-tree: {r}", file=sys.stderr)
    return 1 if reasons else 0


def cmd_replace(repo: str, main_sha: str, number: str, sha: str, new_ref: str) -> int:
    """Open the rebuilt branch as a PR and close the one it replaces (its branch is
    kept). If the old head moved since select, nothing is opened: the rebuilt
    content is superseded, and the orphan branch is harmless."""
    old = gh(f"repos/{repo}/pulls/{number}") or {}
    if old.get("state") != "open" or (old.get("head") or {}).get("sha") != sha:
        summary([f"- #{number} moved or closed since select; rebuilt PR not opened"])
        return 0
    title = f"{old.get('title') or 'chore: daily scan'} (rebuilt on main)"[:250]
    body = (f"Rebuilt from #{number} (head `{sha[:12]}`) onto main `{main_sha[:12]}` by "
            "`scripts/rebuild_pr.py`: data merged three ways, site re-rendered by main's "
            "renderers. The auto-merge gate judges this PR like any other.")  # fmt: skip
    new = gh(f"repos/{repo}/pulls", "-X", "POST", "-f", f"title={title}", "-f", f"head={new_ref}",
             "-f", "base=main", "-f", f"body={body}") or {}  # fmt: skip
    summary([f"- #{number} rebuilt on main as #{new.get('number')} (`{new_ref}`)"])
    note = f"Replaced by #{new.get('number')}: rebuilt on main `{main_sha[:12]}` by code."
    gh(f"repos/{repo}/issues/{number}/comments", "-X", "POST", "-f", f"body={note}")
    gh(f"repos/{repo}/pulls/{number}", "-X", "PATCH", "-f", "state=closed")
    return 0


def cmd_rebuild_failed(repo: str, main_sha: str, number: str, sha: str) -> int:
    """Record the failure on the PR so select stops retrying this (head, main) pair
    and moves to the next conflicting PR; the watchdog reports it as stuck."""
    mode = settings(ROOT / "config.yaml")["mode"]
    post_once(repo, int(number), comment_body(sha, "refused", mode, [rebuild_failed(main_sha)]))
    return 0


# ---------------------------------------------------------------- decide


def required_check_ok(repo: str, sha: str) -> bool:
    runs = gh(f"repos/{repo}/commits/{sha}/check-runs?check_name=pytest&per_page=100") or {}
    return any(
        r.get("conclusion") == "success" and (r.get("app") or {}).get("id") == PYTEST_APP_ID
        for r in runs.get("check_runs", [])
    )


def behind_main(repo: str, sha: str) -> bool:
    cmp = gh(f"repos/{repo}/compare/main...{sha}") or {}
    return int(cmp.get("behind_by", 1)) > 0


def blockers(repo: str, sha: str) -> dict[str, str]:
    """What stops GitHub accepting a merge of a tested, guard-passing head."""
    out = {}
    if behind_main(repo, sha):
        out["behind"] = "behind main (main requires up-to-date branches)"
    if not required_check_ok(repo, sha):
        out["check"] = "main's required `pytest` check has not passed on this head"
    return out


def unblock(repo: str, pr: dict, problems: dict[str, str]) -> str:
    """merge mode: start whatever clears a blocker; the next scheduled run re-checks."""
    sha, ref = pr["head"]["sha"], pr["head"]["ref"]
    try:
        if "behind" in problems:
            # The new head is unjudged: the next run judges it before any dispatch.
            gh(f"repos/{repo}/pulls/{pr['number']}/update-branch", "-X", "PUT", "-f",
               f"expected_head_sha={sha}")  # fmt: skip
            return "waiting (branch update requested)"
        # A dispatch runs the BRANCH's tests.yml, so only at the head we judged:
        # re-confirm it right before (a moved head may carry a rewritten workflow).
        current = (gh(f"repos/{repo}/pulls/{pr['number']}") or {}).get("head", {}).get("sha")
        if current != sha:
            return "waiting (head moved; not dispatching)"
        gh(f"repos/{repo}/actions/workflows/tests.yml/dispatches", "-X", "POST", "-f", f"ref={ref}")
    except subprocess.CalledProcessError:
        return "waiting (unblock request FAILED)"
    return "waiting (required check dispatched)"


def merge(repo: str, number: int, sha: str, method: str) -> str:
    """Merge exactly the evaluated head; GitHub answers 409 if the head moved."""
    try:
        gh(f"repos/{repo}/pulls/{number}/merge", "-X", "PUT", "-f", f"sha={sha}",
           "-f", f"merge_method={method}")  # fmt: skip
    except subprocess.CalledProcessError:
        return "merge FAILED (GitHub refused it; see the job log)"
    notes = ["merged"]
    # Pushes made with GITHUB_TOKEN start no push-triggered workflow and no
    # branch Pages build, so ask for both explicitly.
    for label, path, args in (
        ("render", f"repos/{repo}/actions/workflows/update.yml/dispatches", ["-f", "ref=main"]),
        ("pages build", f"repos/{repo}/pages/builds", []),
    ):
        try:
            gh(path, "-X", "POST", *args)
            notes.append(f"{label} requested")
        except subprocess.CalledProcessError:
            notes.append(f"{label} request FAILED")
    return "; ".join(notes)


def outcome_for(
    repo: str, pr: dict, verdict: mg.Verdict, tests: str, conf: dict
) -> tuple[str, list[str]]:
    """(outcome, reasons) for one PR; acts (unblock/merge) only in merge mode."""
    sha = pr["head"]["sha"]
    if not verdict.ok:
        return "refused", verdict.reasons
    if tests == "failure":
        return "refused", [TESTS_FAILED]
    if tests != "success":
        return "not tested this run", []
    problems = blockers(repo, sha)
    if problems and conf["mode"] == "shadow":
        return "would wait (shadow mode)", list(problems.values())
    if problems:
        return unblock(repo, pr, problems), list(problems.values())
    if conf["mode"] == "shadow":
        return "would merge (shadow mode: not merged)", []
    return merge(repo, pr["number"], sha, conf["merge_method"]), []


REPORTED = ("refused", "would merge", "merged", "merge FAILED")


def decide_one(repo: str, pr: dict, main_sha: str, tested: tuple[str, str], tests: str) -> None:
    conf = settings(ROOT / "config.yaml")
    number, sha = pr["number"], pr["head"]["sha"]
    is_tested = tested == (str(number), sha)
    # Re-fetched and re-judged against the listed head, which for the tested PR
    # is the tested SHA: a head that moved since is refused, and merge() pins it.
    verdict = judge(repo, number, sha, main_sha)
    outcome, reasons = outcome_for(repo, pr, verdict, tests if is_tested else "", conf)
    summary([f"- #{number} `{sha[:12]}`: {outcome}", *[f"  - {r}" for r in reasons[:10]]])
    if outcome.startswith(REPORTED):
        post_once(repo, number, comment_body(sha, outcome, conf["mode"], reasons))


def cmd_decide(repo: str, main_sha: str, number: str, sha: str, tests: str) -> int:
    if number and not (number.isdigit() and mg.SHA.fullmatch(sha)):
        print("decide: malformed tested PR number/SHA", file=sys.stderr)
        return 1
    summary([f"## Auto-merge gate: decide ({settings(ROOT / 'config.yaml')['mode']} mode)", ""])
    for pr in scan_prs(repo):
        decide_one(repo, pr, main_sha, (number, sha), tests)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    commands = ("select", "decide", "check-tree", "replace", "rebuild-failed")
    ap.add_argument("command", choices=commands)
    ap.add_argument("--repo", default="")
    ap.add_argument("--main-sha", required=True)
    ap.add_argument("--number", default="")
    ap.add_argument("--sha", default="")
    ap.add_argument("--tests", default="")
    ap.add_argument("--commit", default="")
    ap.add_argument("--new-ref", default="")
    a = ap.parse_args(argv)
    if not mg.SHA.fullmatch(a.main_sha):
        print("automerge: --main-sha must be a 40-hex SHA", file=sys.stderr)
        return 1
    if a.command == "check-tree":
        return cmd_check_tree(a.main_sha, a.commit)
    if not a.repo:
        print("automerge: --repo is required", file=sys.stderr)
        return 1
    if a.command == "select":
        return cmd_select(a.repo, a.main_sha)
    if a.command in ("replace", "rebuild-failed"):
        if not (a.number.isdigit() and mg.SHA.fullmatch(a.sha)):
            print(f"{a.command}: malformed PR number/SHA", file=sys.stderr)
            return 1
        if a.command == "rebuild-failed":
            return cmd_rebuild_failed(a.repo, a.main_sha, a.number, a.sha)
        if not BRANCH.fullmatch(a.new_ref) or not REBUILT.search(a.new_ref):
            print(
                "replace: --new-ref must be a claude/scan-*-rebuilt-<sha8> branch", file=sys.stderr
            )
            return 1
        return cmd_replace(a.repo, a.main_sha, a.number, a.sha, a.new_ref)
    return cmd_decide(a.repo, a.main_sha, a.number, a.sha, a.tests)


if __name__ == "__main__":
    sys.exit(main())
