#!/usr/bin/env python3
"""
automerge.py — drives gated auto-merge of scan PRs (.github/workflows/automerge.yml).

Always runs MAIN's code from a checkout of main; it never imports, installs or
executes anything from a PR. PR content is fetched as git objects and diffed, which
reads trees but runs nothing. The decision itself is `merge_guard.evaluate`.

  select   (read-only job)  evaluate every open claude/scan-* PR; write a step
                            summary; emit `number`/`sha` of the oldest that passes
                            the path guard, for the read-only test job to test.
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
    return {"mode": mode, "merge_method": method}


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


def cmd_select(repo: str, main_sha: str) -> int:
    conf = settings(ROOT / "config.yaml")
    lines = [f"## Auto-merge gate: select ({conf['mode']} mode)", ""]
    chosen: dict | None = None
    for pr in scan_prs(repo):
        number, sha = pr["number"], pr["head"]["sha"]
        verdict = judge(repo, number, sha, main_sha)
        state = "passes the path guard" if verdict.ok else "refused"
        lines.append(f"- #{number} `{sha[:12]}`: {state}")
        lines += [f"  - {r}" for r in verdict.reasons[:10]]
        if verdict.ok and chosen is None:
            chosen = {"number": str(number), "sha": sha}
    if not chosen:
        lines.append("- nothing to test")
    summary(lines)
    output(**(chosen or {"number": "", "sha": ""}))
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
            gh(f"repos/{repo}/pulls/{pr['number']}/update-branch", "-X", "PUT", "-f",
               f"expected_head_sha={sha}")  # fmt: skip
        # Either blocker needs a fresh `pytest` run: update-branch makes a new head.
        gh(f"repos/{repo}/actions/workflows/tests.yml/dispatches", "-X", "POST", "-f", f"ref={ref}")
    except subprocess.CalledProcessError:
        return "waiting (unblock request FAILED)"
    return "waiting (unblock requested)"


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
        return "refused", ["in-workflow tests or integrity checks failed"]
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
    ap.add_argument("command", choices=("select", "decide"))
    ap.add_argument("--repo", required=True)
    ap.add_argument("--main-sha", required=True)
    ap.add_argument("--number", default="")
    ap.add_argument("--sha", default="")
    ap.add_argument("--tests", default="")
    a = ap.parse_args(argv)
    if not mg.SHA.fullmatch(a.main_sha):
        print("automerge: --main-sha must be a 40-hex SHA", file=sys.stderr)
        return 1
    if a.command == "select":
        return cmd_select(a.repo, a.main_sha)
    return cmd_decide(a.repo, a.main_sha, a.number, a.sha, a.tests)


if __name__ == "__main__":
    sys.exit(main())
