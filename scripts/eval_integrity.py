#!/usr/bin/env python3
"""
eval_integrity.py — Deterministic integrity eval over the pools and the site (ISA ISC-24).

No network and no LLM: it runs in the Tests workflow on every PR, and
scripts/merge_gate.py runs it before a scan PR can auto-merge.

Published stories (the site's research findings + news lane, read from the data
block in docs/index.html and joined back to their pool entries) must be clean:

  grounded  no lesson is marked `grounded: false`, no `grounding_score` is below
            1.0, and where the raw source text is on disk (data/_raw/, i.e. a
            scan's own candidates) every excerpt is re-checked against it with
            verify_citations.ground_entry
  article   the citation is an article, not a homepage or site root
  domain    the domain is a taxonomy ID of the entry's own topic
  unique    every rendered row carries a story_id and no story is rendered twice,
            across both lanes (content_checks.site_story_problems, the story ledger's
            own check)

Every pool and archive entry must have a valid domain ID and http(s) URLs
(content_checks.url_problems, shared with the merge gate), and
no id may repeat inside the live pools. Warnings never fail the eval: a held
entry citing a homepage, an id in both a pool and the archive, an entry with no id.

Usage:
    python scripts/eval_integrity.py            # problems, then the summary line
    python scripts/eval_integrity.py --verbose  # warnings too
    python scripts/eval_integrity.py --json     # the full report
Exit 0 = no problems, 1 = problems.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from collections import Counter
from urllib.parse import urlparse

import common as c
import content_checks as cc
import eval_lib as el
import taxonomy as tx
import verify_citations as vc
from content_checks import url_problems as bad_urls  # the one http(s)-only URL rule

SITE = "docs/index.html"
# Paths that are a site's front page, not an article.
ROOT_PATHS = re.compile(r"^/?((index|default|home)(\.html?|\.php)?|[a-z]{2}(-[a-z]{2})?)?/?$", re.I)
LANES = ("findings", "editorial")


# --- Rules -------------------------------------------------------------------
def is_homepage(url: str) -> bool:
    """True for a site root ('https://blog.example.com/', '/en/', '/index.html')."""
    parsed = urlparse(url or "")
    return bool(parsed.netloc) and not parsed.query and bool(ROOT_PATHS.match(parsed.path))


def citation(entry: dict) -> str:
    return entry.get("article_url") or entry.get("source_url") or entry.get("url") or ""


def grounding_problems(entry: dict) -> list[str]:
    """Persisted verdicts first; then a re-check against raw text if it's on disk."""
    out = [
        f"lesson {i} excerpt marked ungrounded"
        for i, le in enumerate(entry.get("lessons") or [])
        if isinstance(le, dict) and le.get("grounded") is False
    ]
    if not vc.fully_grounded(entry):
        out.append(f"grounding_score {entry.get('grounding_score')} < 1.0")
    raw = c.raw_file(entry.get("raw_path"))
    if raw is not None and raw.exists():
        fresh = vc.ground_entry(
            copy.deepcopy(entry), raw.read_text(encoding="utf-8", errors="replace")
        )
        if not vc.fully_grounded(fresh):
            out.append(f"excerpt not found in its raw source text ({entry['raw_path']})")
    return out


# --- Loading -----------------------------------------------------------------
def site_payload(page: str) -> dict:
    """The site's data block. Raises on a missing or repeated block."""
    blocks = cc.PAYLOAD.findall(page)
    if len(blocks) != 1:
        raise ValueError(f"{SITE}: expected one site-data block, found {len(blocks)}")
    return json.loads(blocks[0])


def site_rows(payload: dict) -> list[tuple[str, dict]]:
    """(lane, row) for every story the site renders."""
    return [(lane, row) for lane in LANES for row in payload.get(lane) or []]


def load_entries() -> tuple[list[tuple[str, dict]], list[dict]]:
    """([(topic, entry)] for the live pools, archive entries)."""
    pools = [(t, e) for t in c.TOPICS for e in c.load_pool(t)["entries"]]
    return pools, c.load_json(c.ARCHIVE_FILE, default=[]) or []


# --- Checks ------------------------------------------------------------------
def label(entry: dict) -> str:
    return entry.get("id") or (entry.get("title") or "?")[:50]


def entry_problems(entry: dict, tax: tx.Taxonomy) -> list[str]:
    """Invariants for every pool and archive entry."""
    out = (
        []
        if tax.is_valid(entry.get("domain"), entry.get("topic"))
        else [f"domain {entry.get('domain')!r} is not a {entry.get('topic')} taxonomy ID"]
    )
    return out + bad_urls(entry)


def published_problems(lane: str, row: dict, entry: dict | None, tax: tx.Taxonomy) -> list[str]:
    """Invariants for a story the site shows."""
    if entry is None:
        return [f"{lane}: rendered story {row.get('id')} is in no pool"]
    out = grounding_problems(entry)
    url = citation(entry)
    if not url or is_homepage(url):
        out.append(f"citation {url!r} is a homepage, not an article")
    if row.get("url") and is_homepage(row["url"]):
        out.append(f"rendered link {row['url']!r} is a homepage")
    if not tax.is_valid(row.get("domain_id"), row.get("topic")):
        out.append(f"rendered domain {row.get('domain_id')!r} is not a {row.get('topic')} ID")
    return out


def data_warnings(pools: list[tuple[str, dict]], archive: list[dict]) -> list[str]:
    live = {e.get("id") for _, e in pools}
    out = [f"{label(e)}: in a pool and in the archive" for e in archive if e.get("id") in live]
    out += [
        f"{label(e)}: entry has no id" for e in [e for _, e in pools] + archive if not e.get("id")
    ]
    out += [
        f"{label(e)}: held entry cites a homepage ({citation(e)})"
        for _, e in pools
        if is_homepage(citation(e))
    ]
    return out


def run(page: str | None = None) -> dict:
    tax = tx.get()
    pools, archive = load_entries()
    problems: list[str] = []
    for where, e in [(t, e) for t, e in pools] + [("archive", e) for e in archive]:
        problems += [f"[{where}] {label(e)}: {p}" for p in entry_problems(e, tax)]
    ids = Counter(e.get("id") for _, e in pools)
    problems += [f"[pools] id {i} appears {n} times" for i, n in ids.items() if i and n > 1]
    page = page if page is not None else (c.ROOT / SITE).read_text(encoding="utf-8")
    payload = site_payload(page)
    rows = site_rows(payload)
    by_id = {e.get("id"): e for _, e in pools}
    for lane, row in rows:
        found = published_problems(lane, row, by_id.get(row.get("id")), tax)
        problems += [f"[site] {row.get('id')}: {p}" for p in found]
    problems += [f"[site] {p}" for p in cc.site_story_problems(payload)]
    warnings = data_warnings(pools, archive)
    return {
        "passed": not problems,
        "published": len(rows),
        "entries": len(pools) + len(archive),
        "problems": problems,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--json", action="store_true", help="print the full report")
    ap.add_argument("--verbose", action="store_true", help="print warnings too")
    args = ap.parse_args(argv)
    try:
        report = run()
    except (OSError, ValueError) as exc:
        report = {"passed": False, "published": 0, "entries": 0, "warnings": [],
                  "problems": [f"could not run: {type(exc).__name__}: {exc}"]}  # fmt: skip
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for p in report["problems"]:
            print(f"PROBLEM {p}")
        for w in report["warnings"] if args.verbose else []:
            print(f"WARN {w}")
    print(
        el.summary_line(
            "integrity",
            report["passed"],
            published=report["published"],
            entries=report["entries"],
            problems=len(report["problems"]),
            warnings=len(report["warnings"]),
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
