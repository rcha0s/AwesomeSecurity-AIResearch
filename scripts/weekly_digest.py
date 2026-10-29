#!/usr/bin/env python3
"""
weekly_digest.py - the last week's focus items as a short markdown digest (ISC-56).

Writes docs/digest.md: the stories and claim changes of the last `focus.digest_days`
days that match one of Rohan's focus areas (config.yaml `focus:`), each with its
title, a one-line takeaway and a link. The picks come from briefing.py, the same
rules the Briefing's "Your focus" lane uses, and nothing here reads the clock, so
a re-run on the same data writes the same file.

    python scripts/weekly_digest.py            write docs/digest.md, print a one-line message
    python scripts/weekly_digest.py --due      exit 0 when today is the digest weekday, else 1

The Mac wrapper (run_scan_local.sh) calls --due, then the bare form, and posts the
message to $DIGEST_NOTIFY_URL when that is set.
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import briefing
import common as c
import focus as focus_mod
import generate_html as gh

import claims as cl

DIGEST_FILE = "digest.md"
TAKEAWAY_CHARS = 200
DEFAULT_WEEKDAY = 6  # Sunday; config.yaml focus.digest_weekday decides
DEFAULT_DAYS = 7
DEFAULT_MAX = 15


def is_due(focus: dict, today: datetime | None = None, override: str | None = None) -> bool:
    """True on the digest weekday. `override` (env DIGEST_WEEKDAY) is 0-6 or `any`."""
    override = os.environ.get("DIGEST_WEEKDAY", "") if override is None else override
    if override.strip().lower() == "any":
        return True
    want = (
        int(override)
        if override.strip().isdigit()
        else int(focus.get("digest_weekday", DEFAULT_WEEKDAY))
    )
    return (today or datetime.now(UTC)).weekday() == want


def _one_line(text: str, limit: int = TAKEAWAY_CHARS) -> str:
    """The first sentence of `text`, cut to `limit`, safe inside a markdown list item."""
    return gh.sentence_cut(" ".join(str(text or "").split()), limit)


def _link_label(title: str) -> str:
    return " ".join(str(title or "").split()).replace("[", "(").replace("]", ")")


def pick(payload_rows: list[dict], claims: list[dict], focus: dict, now: str) -> tuple[list, list]:
    """(stories, claim changes) of the digest window; no top-up, so a quiet week is empty."""
    days = int(focus.get("digest_days") or DEFAULT_DAYS)
    cap = int(focus.get("digest_max") or DEFAULT_MAX)
    stories, _ = briefing.focus_stories(
        payload_rows, {**focus, "lane_min": 0, "lane_max": cap}, now, days
    )
    cutoff = briefing._cutoff(now, days)
    stories = [r for r in stories if briefing.last_activity(r) >= cutoff]
    changes = briefing.focus_claim_changes(claims, {**focus, "claim_changes_max": cap}, now, days)
    return stories, changes


def _story_line(row: dict, focus: dict) -> str:
    tags = focus_mod.names(focus_mod.areas(row, focus), focus)
    line = f"- [{_link_label(row['title'])}]({row['url']})"
    if row.get("takeaway"):
        line += f" - {_one_line(row['takeaway'])}"
    return line + (f" _({', '.join(tags)})_" if tags else "")


def _change_line(change: dict, claims: dict, focus: dict) -> str | None:
    claim = claims.get(change["claim"])
    if claim is None:
        return None
    label = _link_label(claim.get("title") or claim.get("statement") or claim["id"])
    link = f"{gh.SITE_URL}?claim={claim['id']}#claims"
    line = f"- {change['kind'].capitalize()}: [{label}]({link})"
    statement = claim.get("statement")
    if statement and statement != claim.get("title"):
        line += f" - {_one_line(statement)}"
    return line


def render(
    stories: list[dict], changes: list[dict], claims: list[dict], focus: dict, now: str
) -> str:
    """The digest's markdown. Plain sentences, no marketing."""
    days = int(focus.get("digest_days") or DEFAULT_DAYS)
    by_id = {str(cl_["id"]): cl_ for cl_ in claims}
    names = ", ".join(a["name"] for a in focus.get("areas") or [])
    out = [
        "# Weekly focus digest",
        "",
        f"The last {days} days up to {now}, in your focus areas: {names}.",
        "",
        "## Stories",
        "",
    ]
    out += [_story_line(r, focus) for r in stories] or [
        "Nothing new in your focus areas this week."
    ]
    lines = [ln for ln in (_change_line(ch, by_id, focus) for ch in changes) if ln]
    if lines:
        out += ["", "## Claim changes", ""] + lines
    return "\n".join(out) + "\n"


def message(n_stories: int, n_changes: int) -> str:
    """The one-line notification: counts and where the digest lives once merged."""
    stories = f"{n_stories} {'story' if n_stories == 1 else 'stories'}"
    changes = f"{n_changes} claim change{'' if n_changes == 1 else 's'}"
    return f"Weekly focus digest: {stories}, {changes}. {gh.SITE_URL}{DIGEST_FILE}"


def build(now: str | None = None) -> tuple[str, int, int]:
    """(markdown, story count, claim-change count) from the current pools and ledger."""
    conf = c.load_config()
    ledger = cl.load_ledger()
    now = now or c.utcnow().strftime("%Y-%m-%d")
    payload = gh.build_payload(ledger, conf, now)
    claims = payload["claims"]
    stories, changes = pick(payload["findings"] + payload["editorial"], claims, conf.focus, now)
    return render(stories, changes, claims, conf.focus, now), len(stories), len(changes)


def main(argv: list[str]) -> int:
    conf = c.load_config()
    if "--due" in argv:
        return 0 if is_due(conf.focus) else 1
    text, n_stories, n_changes = build()
    docs = Path(c.ROOT) / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / DIGEST_FILE).write_text(text, encoding="utf-8")
    print(message(n_stories, n_changes))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
