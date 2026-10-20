#!/usr/bin/env python3
"""
taxonomy_proposals.py — record verified new-domain proposals; escalate recurring ones.

When no domain fits, the analyzer still files the entry under the nearest ID and
adds `proposed_domain: {name, scope, nearest, why_different}`. A separate small-
model verifier (research-scan skill, step 4b) must then name the nearest EXISTING
domain and say why the proposal is really different, writing
`proposed_domain.verifier: {verdict, nearest, reason}`.

This module is the deterministic part (ISC-18):
  - `record`   append each proposal that passes verification to
               data/taxonomy_proposals.json (one row per entry, idempotent);
  - `recurring` proposals seen on >= `proposal_min_count` distinct entries
               within `proposal_window_days`;
  - `notify`   open — or comment on — one GitHub issue labelled `taxonomy` per
               recurring proposal, via `gh api` REST only (cloud sessions block
               GraphQL; same pattern as scan_alert.sh).

The verifier is injectable (`verify=`), so tests stub it. The issue body carries
model-written text, so it passes scrub.leak_reason first and falls back to a
plain body on a hit, like the scan PR body.

Usage:
    python scripts/taxonomy_proposals.py notify [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

import common as c
import scrub
import taxonomy as tx

PROPOSALS_NAME = "taxonomy_proposals.json"
MAX_TEXT = 300  # chars of model-written text per field that reach a public issue
MARKER = "<!-- taxonomy-proposal:{key} -->"


def proposals_file():
    """The proposal ledger (resolved per call so tests can sandbox DATA_DIR)."""
    return c.DATA_DIR / PROPOSALS_NAME


@dataclass(frozen=True)
class Verdict:
    passed: bool
    nearest: str
    reason: str


def settings() -> dict:
    """`taxonomy:` block of config.yaml (window, threshold, issue label)."""
    raw = (c.load_yaml(c.CONFIG_FILE) or {}).get("taxonomy") or {}
    return {
        "window_days": int(raw.get("proposal_window_days", 30)),
        "min_count": int(raw.get("proposal_min_count", 3)),
        "label": str(raw.get("issue_label", "taxonomy")),
    }


def skill_verdict(proposal: dict) -> Verdict:
    """The verdict the skill's verifier subagent wrote onto the proposal."""
    v = proposal.get("verifier") or {}
    return Verdict(
        passed=str(v.get("verdict") or "").lower() == "pass",
        nearest=str(v.get("nearest") or ""),
        reason=str(v.get("reason") or "").strip(),
    )


def accepted(entry: dict, tax: tx.Taxonomy, verify: Callable[[dict], Verdict]) -> Verdict | None:
    """The verdict if the entry's proposal passes, else None. A pass must name
    an existing domain of the entry's topic and give a reason, whatever the
    verifier claims."""
    proposal = entry.get("proposed_domain")
    if not isinstance(proposal, dict) or not str(proposal.get("name") or "").strip():
        return None
    verdict = verify(proposal)
    if not (verdict.passed and verdict.reason and tax.is_valid(verdict.nearest, entry["topic"])):
        return None
    return verdict


def proposal_key(topic: str, name: str) -> str:
    return f"{topic}/{tx.label_tag(name)}"


def _row(entry: dict, verdict: Verdict, now: datetime) -> dict:
    proposal = entry["proposed_domain"]
    return {
        "key": proposal_key(entry["topic"], proposal["name"]),
        "name": str(proposal["name"]).strip(),
        "scope": str(proposal.get("scope") or "").strip(),
        "topic": entry["topic"],
        "entry": tx.entry_key(entry),
        "title": entry.get("title", ""),
        "source_url": entry.get("source_url", ""),
        "filed_under": entry.get("domain", ""),
        "verifier_nearest": verdict.nearest,
        "verifier_reason": verdict.reason,
        "recorded_at": now.isoformat(),
    }


def record(
    entries: list[dict],
    now: datetime | None = None,
    verify: Callable[[dict], Verdict] = skill_verdict,
) -> list[dict]:
    """Append every newly passing proposal to the ledger; return the new rows.
    One row per (proposal, entry): re-merging the same entry never re-counts."""
    tax, now = tx.get(), now or c.utcnow()
    rows = c.load_json(proposals_file(), default=[]) or []
    seen = {(r["key"], r["entry"]) for r in rows}
    added = []
    for entry in entries:
        verdict = accepted(entry, tax, verify)
        if verdict is None:
            continue
        row = _row(entry, verdict, now)
        if (row["key"], row["entry"]) not in seen:
            seen.add((row["key"], row["entry"]))
            added.append(row)
    if added:
        c.save_json(proposals_file(), rows + added)
    return added


def recurring(
    rows: list[dict], now: datetime, window_days: int, min_count: int
) -> dict[str, list[dict]]:
    """Proposal key -> its rows inside the window, for keys on >= min_count entries."""
    cutoff = now - timedelta(days=window_days)
    by_key: dict[str, list[dict]] = {}
    for row in rows:
        if datetime.fromisoformat(row["recorded_at"]) >= cutoff:
            by_key.setdefault(row["key"], []).append(row)
    return {k: v for k, v in by_key.items() if len({r["entry"] for r in v}) >= min_count}


# --- GitHub (REST only) ------------------------------------------------------
def gh_api(*args: str) -> str:
    """Run `gh api` and return stdout; raises on failure."""
    out = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=True)
    return out.stdout


def repo_slug() -> str:
    """owner/repo: GITHUB_REPOSITORY, else origin's last two path segments."""
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"]
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True
    ).stdout.strip()
    match = re.search(r"([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    if not match:
        raise ValueError(f"cannot parse origin URL: {url}")
    return f"{match.group(1)}/{match.group(2)}"


def _clip(text: str) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= MAX_TEXT else text[: MAX_TEXT - 1] + "…"


def entry_line(row: dict) -> str:
    """One evidence line; `entry:<key>` is what makes re-comments idempotent."""
    return (
        f"- `entry:{row['entry']}` [{_clip(row['title'])}]({row['source_url']}) — filed under "
        f"`{row['filed_under']}`; verifier: nearest `{row['verifier_nearest']}`, "
        f"different because {_clip(row['verifier_reason'])}"
    )


def issue_body(key: str, rows: list[dict], conf: dict) -> str:
    first = rows[0]
    lines = [
        MARKER.format(key=key),
        f"The analyzer proposed a new **{first['topic']}** domain, "
        f"**{_clip(first['name'])}**, on {len(rows)} entries in {conf['window_days']} days, "
        "and the verifier passed each one.",
        "",
        f"Proposed scope: {_clip(first['scope'])}",
        "",
        "Decide: add it to `data/taxonomy.yaml` (then re-file these entries), "
        "or widen the nearest domain's scope and close this.",
        "",
        *[entry_line(r) for r in rows],
    ]
    return "\n".join(lines)


def safe(body: str, key: str) -> str:
    """The body, or a plain one if it looks like it leaks a secret."""
    if scrub.leak_reason(body, dict(os.environ)) is None:
        return body
    return f"{MARKER.format(key=key)}\nA new-domain proposal `{key}` recurred (details withheld)."


def _open_issues(repo: str, label: str) -> list[dict]:
    raw = gh_api(f"repos/{repo}/issues?state=open&labels={label}&per_page=100")
    return [i for i in json.loads(raw or "[]") if "pull_request" not in i]


def _ensure_label(repo: str, label: str) -> None:
    try:
        gh_api("-X", "POST", f"repos/{repo}/labels", "-f", f"name={label}", "-f", "color=5319e7")
    except subprocess.CalledProcessError as err:  # "already_exists" is the normal case
        if "already_exists" not in (err.stderr or "") + (err.stdout or ""):
            raise


def _already_listed(repo: str, issue: dict) -> str:
    raw = gh_api(f"repos/{repo}/issues/{issue['number']}/comments?per_page=100")
    return (issue.get("body") or "") + "".join(x.get("body") or "" for x in json.loads(raw))


def notify_one(repo: str, key: str, rows: list[dict], conf: dict, issues: list[dict]) -> str:
    """Open an issue for `key`, or comment the entries it doesn't list yet.
    Returns 'opened', 'commented' or 'unchanged'."""
    marker = MARKER.format(key=key)
    issue = next((i for i in issues if marker in (i.get("body") or "")), None)
    if issue is None:
        title = f"Taxonomy: proposed {rows[0]['topic']} domain '{_clip(rows[0]['name'])[:60]}'"
        body = safe(issue_body(key, rows, conf), key)
        gh_api(
            "-X",
            "POST",
            f"repos/{repo}/issues",
            "-f",
            f"title={title}",
            "-f",
            f"body={body}",
            "-f",
            f"labels[]={conf['label']}",
        )
        return "opened"
    listed = _already_listed(repo, issue)
    new = [r for r in rows if f"entry:{r['entry']}`" not in listed]
    if not new:
        return "unchanged"
    body = safe("\n".join(["Seen again:", *[entry_line(r) for r in new]]), key)
    gh_api("-X", "POST", f"repos/{repo}/issues/{issue['number']}/comments", "-f", f"body={body}")
    return "commented"


def notify(now: datetime | None = None, dry_run: bool = False) -> dict[str, str]:
    """Escalate every recurring proposal. Returns key -> action."""
    conf, now = settings(), now or c.utcnow()
    rows = c.load_json(proposals_file(), default=[]) or []
    due = recurring(rows, now, conf["window_days"], conf["min_count"])
    if dry_run or not due:
        return {key: "due" for key in due}
    repo = repo_slug()
    _ensure_label(repo, conf["label"])
    issues = _open_issues(repo, conf["label"])
    return {key: notify_one(repo, key, kr, conf, issues) for key, kr in sorted(due.items())}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["notify"])
    ap.add_argument("--dry-run", action="store_true", help="list due proposals; touch nothing")
    args = ap.parse_args(argv)
    actions = notify(dry_run=args.dry_run)
    for key, action in actions.items():
        print(f"taxonomy proposal {key}: {action}")
    if not actions:
        print("taxonomy proposals: none recurring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
