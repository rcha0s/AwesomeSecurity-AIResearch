#!/usr/bin/env python3
"""
content_checks.py — content invariants a scan PR must keep (scripts/merge_gate.py).

The path guard (merge_guard.py) proves a PR touches content only. These checks
bound what that content can do once published:

  url_problems          every `url` / `*_url` field is an http(s) URL, so no
                        `javascript:` or quote-breakout link reaches the site.
  render_problems       docs/index.html is byte-equal to main's renderer applied
                        to the payload and stamp it carries: the page is main's
                        template plus data, never hand-written HTML or script.
  claim_history_problems no claim on main disappears, and an existing claim
                        (live or retired) only gains evidence; any other change
                        is refused as "claim change needs human review".

Pure functions over parsed data; merge_gate.py does the I/O.
"""

from __future__ import annotations

import html
import json
import re

# Same rule as safeUrl() in scripts/templates/site.html: keep them in step.
HTTP_URL = re.compile(r"https?://[^\s\"<>`]+", re.IGNORECASE)

PAYLOAD = re.compile(r'<script id="site-data" type="application/json">(.*?)</script>', re.S)
STAMP = re.compile(r"<span>Generated <b>([^<]*)</b></span>")

# Policy (coordinator, 2026-10-20): a scan PR may ADD claims and APPEND evidence
# to existing ones (bumping `last_reviewed`), which is all a scan does (#68).
# Any other change to an existing claim, live or retired (status, statement,
# title, guidance, supersession edges, confidence, scope, ...), means the PR does
# not auto-merge: it stays open for a human.
CLAIM_MUTABLE = frozenset({"evidence", "last_reviewed"})
NEEDS_REVIEW = "claim change needs human review"


def _is_url_key(key: object) -> bool:
    return isinstance(key, str) and (key == "url" or key.endswith("_url"))


def url_problems(obj: object, where: str = "") -> list[str]:
    """Every non-empty `url` / `*_url` value anywhere in `obj` must be http(s)."""
    out: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            here = f"{where}.{key}" if where else str(key)
            if _is_url_key(key) and value not in (None, ""):
                if not (isinstance(value, str) and HTTP_URL.fullmatch(value)):
                    out.append(f"{here}: not an http(s) URL")
                continue
            out += url_problems(value, here)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            out += url_problems(value, f"{where}[{i}]")
    return out


def render_problems(page: str, render) -> list[str]:
    """`render(payload, stamp)` (main's generate_html.render) must reproduce `page`."""
    payloads, stamps = PAYLOAD.findall(page), STAMP.findall(page)
    if len(payloads) != 1 or len(stamps) != 1:
        return ["docs/index.html: expected exactly one data block and one generated stamp"]
    try:
        payload = json.loads(payloads[0])
    except json.JSONDecodeError:
        return ["docs/index.html: the data block is not JSON"]
    if render(payload, html.unescape(stamps[0])) != page:
        return ["docs/index.html: not what main's renderer makes from its own data"]
    return []


def _claims_by_id(ledger: object) -> dict[str, dict]:
    claims = ledger.get("claims") if isinstance(ledger, dict) else None
    return {c["id"]: c for c in claims or [] if isinstance(c, dict) and "id" in c}


def _claim_change_problems(cid: str, old: dict, new: dict) -> list[str]:
    out = []
    for key in sorted((set(old) | set(new)) - CLAIM_MUTABLE):
        if old.get(key) != new.get(key):
            out.append(f"{NEEDS_REVIEW}: {cid} `{key}` changed")
    old_ev, new_ev = old.get("evidence") or [], new.get("evidence") or []
    if not isinstance(new_ev, list) or new_ev[: len(old_ev)] != old_ev:
        out.append(f"{NEEDS_REVIEW}: {cid} evidence was rewritten, not appended to")
    return out


def claim_history_problems(main_ledger: object, pr_ledger: object) -> list[str]:
    """Scan PRs may add claims and append evidence; nothing else about a claim."""
    old, new = _claims_by_id(main_ledger), _claims_by_id(pr_ledger)
    out = [f"claim {cid} on main is missing from the PR" for cid in sorted(set(old) - set(new))]
    for cid in sorted(set(old) & set(new)):
        out += _claim_change_problems(cid, old[cid], new[cid])
    return out
