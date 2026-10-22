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
  editorial_problems    an entry promoted on main keeps its promotion (every
                        copy) unless main's copy already failed integrity;
                        any other removal is refused as "editorial demotion
                        needs human review".
  story_membership_problems every entry in main's story ledger stays in the
                        same story in the PR, and no story disappears: a PR can
                        only add stories, or add NEW entries to existing ones
                        (what a judge verdict does), never re-collapse old ones.
  story_id_problems     every rendered story row (findings + news lane) carries
                        a story id and no story renders twice (ISC-21; the
                        Phase 3 integrity eval and generate_html.py call it).
  history_problems      data/evals/history.json only grows by this run's one
                        row, and that row agrees with the budget ledger (its
                        charge is the run's effective charge there; measured
                        only for a local run) and with what the gate recomputes
                        (integrity, golden, the cap).

Pure functions over parsed data; merge_gate.py does the I/O.
"""

from __future__ import annotations

import html
import json
import re

from common import integrity_lost  # the one definition of the integrity floor

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
DEMOTION_REVIEW = "editorial demotion needs human review"


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


def _entries(doc: object) -> list:
    """Entries of a pool ({"entries": [...]}) or the archive (a bare list)."""
    rows = doc.get("entries") if isinstance(doc, dict) else doc
    return [e for e in rows if isinstance(e, dict)] if isinstance(rows, list) else []


def _promoted(entry: dict) -> bool:
    return isinstance(entry.get("editorial"), dict) and bool(entry["editorial"].get("promoted"))


def editorial_problems(main_docs: list, pr_docs: list) -> list[str]:
    """Promotions are sticky (news is kept like claims). A scan PR may drop one
    only when main's copy had already failed integrity (refuted or ungrounded:
    the same c.integrity_lost promote_editorial.py removes on). `verified` and
    `grounding_score` are session-writable, so integrity that fails inside this
    PR is not evidence: that removal, an explicit demotion, or an entry that
    vanished waits for a human. An id counts as kept only if every copy of it
    in the PR is still promoted. `*_docs` are pools + archive."""
    before = {e.get("id"): e for d in main_docs for e in _entries(d) if _promoted(e)}
    after: dict = {}
    for d in pr_docs:
        for e in _entries(d):
            after.setdefault(e.get("id"), []).append(e)
    out = []
    for eid in sorted(i for i in before if isinstance(i, str)):
        copies = after.get(eid) or []
        if not copies:
            out.append(f"{DEMOTION_REVIEW}: promoted entry {eid} is gone")
        elif not all(_promoted(e) for e in copies) and not integrity_lost(before[eid]):
            out.append(f"{DEMOTION_REVIEW}: {eid} lost its promotion with main's integrity intact")
    return out


def duplicate_story_ids(rows: list[dict]) -> list[str]:
    """Story ids that appear on more than one rendered row (sorted)."""
    seen: dict[str, int] = {}
    for row in rows:
        sid = row.get("story_id") or ""
        seen[sid] = seen.get(sid, 0) + 1
    return sorted(sid for sid, n in seen.items() if sid and n > 1)


def story_id_problems(rows: list[dict]) -> list[str]:
    """A rendered row with no story id, or a story rendered twice. [] = clean."""
    out = [
        f"row without story_id: {r.get('id') or r.get('title', '?')}"
        for r in rows
        if not r.get("story_id")
    ]
    out += [f"duplicate story id on the site: {sid}" for sid in duplicate_story_ids(rows)]
    return out


def site_story_problems(payload: dict) -> list[str]:
    """story_id_problems over a site payload's findings + news-lane rows."""
    return story_id_problems((payload.get("findings") or []) + (payload.get("editorial") or []))


def _stories(ledger: object) -> dict:
    if not isinstance(ledger, dict) or ledger.get("version") != 2:
        return {}  # main still on the pre-ledger index: nothing to hold steady
    stories = ledger.get("stories")
    return stories if isinstance(stories, dict) else {}


def story_membership_problems(main_ledger: object, pr_ledger: object) -> list[str]:
    """A scan PR may add stories and add new entries to stories; it may not move
    an entry main already placed, or drop a story."""
    old, new = _stories(main_ledger), _stories(pr_ledger)
    if old and not isinstance(pr_ledger, dict):
        return ["story ledger is not a ledger"]
    where = {e: sid for sid, row in new.items() for e in (row or {}).get("entry_ids") or []}
    out = [f"story {sid} on main is missing from the PR" for sid in sorted(set(old) - set(new))]
    for sid, row in sorted(old.items()):
        for eid in (row or {}).get("entry_ids") or []:
            if where.get(eid) != sid:
                out.append(f"entry {eid} moved from story {sid} to {where.get(eid) or 'nowhere'}")
    return out


def _history_rows(history: object) -> list:
    rows = history.get("runs") if isinstance(history, dict) else None
    return rows if isinstance(rows, list) else []


def _ledger_problems(row: dict, ledger_runs: list[dict]) -> list[str]:
    """The new row's run reserved on the ledger, and its cost is what the ledger says."""
    rid = row.get("run_id")
    mine = [r for r in ledger_runs if r.get("run_id") == rid]
    held = [r for r in mine if r.get("kind") == "reserve"]
    if not held:
        return [f"history: run {rid!r} has no reservation on the budget ledger"]
    out = []
    if (row.get("runner"), row.get("date")) != (held[0].get("runner"), held[0].get("date")):
        out.append(f"history: run {rid}'s runner/date disagree with its reservation")
    if row.get("ceiling_usd") != held[0].get("cost_usd"):
        out.append(f"history: run {rid}'s ceiling is not its reservation")
    return out + _charge_problems(row, mine, held[0])


def _charge_problems(row: dict, mine: list[dict], held: dict) -> list[str]:
    """The row's charge is exactly what the ledger charges the run: its latest
    `actual` row if it has one, else its reservation (budget.effective_runs).
    A measured charge needs a local reservation: a cloud run can't measure its
    cost, so an `actual` row on one is not evidence of anything."""
    rid, basis = row.get("run_id"), row.get("cost_basis")
    actuals = [r for r in mine if r.get("kind") == "actual"]
    charge = actuals[-1] if actuals else held
    want = "measured" if actuals else "reserved"
    if basis == "measured" and held.get("runner") != "local":
        return [f"history: run {rid} claims a measured cost but is not a local run"]
    if basis != want or row.get("cost_usd") != charge.get("cost_usd"):
        return [f"history: run {rid}'s cost is not its {want} charge on the ledger"]
    return []


GOLDEN_FIELDS = ("score", "off_topic_rate", "cases", "generated", "file")


def _golden_key(golden: object) -> tuple | None:
    """The fields of a golden summary that identify the result (not its staleness,
    which depends on when you look)."""
    return tuple(golden.get(k) for k in GOLDEN_FIELDS) if isinstance(golden, dict) else None


def history_problems(
    main_history: object, pr_history: object, ledger_runs: list[dict], recomputed: dict
) -> list[str]:
    """data/evals/history.json in a scan PR: main's rows are an exact prefix, at
    most one row is new, and that row matches what the gate can check itself.

    `recomputed` is what merge_gate derives from the merged tree and main's
    config: {"integrity": bool, "golden": dict | None, "cap_usd": float | None}.
    The recall score needs the network, so it is the one value taken on trust."""
    old, new = _history_rows(main_history), _history_rows(pr_history)
    if new[: len(old)] != old:
        return ["history: rows on main were rewritten or removed"]
    added = new[len(old) :]
    if len(added) > 1:
        return [f"history: {len(added)} new rows; a scan adds at most one"]
    if not added:
        return []
    row = added[0] if isinstance(added[0], dict) else {}
    out = _ledger_problems(row, ledger_runs)
    if (row.get("integrity") or {}).get("passed") is not recomputed.get("integrity"):
        out.append("history: the new row's integrity disagrees with the merged tree")
    if _golden_key(row.get("golden")) != _golden_key(recomputed.get("golden")):
        out.append("history: the new row's golden result is not the newest on the tree")
    if row.get("cap_usd") != recomputed.get("cap_usd"):
        out.append("history: the new row's per-run cap is not main's")
    return out
