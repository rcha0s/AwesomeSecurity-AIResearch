#!/usr/bin/env python3
"""
briefing.py - what leads the front page, decided once for README and site.

The README teaser and the site's Briefing both show "this week's top stories"
and the ledger's "claim changes". They are picked here, from the same site
rows, so the two surfaces can never disagree.

  top_stories   rows active in the last `days` (a fresh Updated line counts),
                newest activity first, then most covering sources, then
                composite (Rohan, 2026-10-27: the briefing reads latest first). Fewer than `n_min` in the window -> topped up with
                the most recent stories outside it (and the caller says so).
  claim_changes what the ledger changed in the last `days`: claims added,
                newly contested, and overturned (superseded or refuted, shown
                as the claim that replaced them). Fewer than `n_min` in the
                window -> topped up with the most recent earlier changes; the
                latest reversal is always included when there is one.
  claim_domain  a claim's free-text domain label as a taxonomy ID, or "".

Pure functions over payload rows; generate_html.py and generate_site.py do I/O.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import taxonomy

TOP_STORIES_MAX = 8
TOP_STORIES_MIN = 5
# A label resolved by these rules is trusted on a topic page; a bare default is not.
_TRUSTED_RESOLUTION = frozenset({"id", "alias", "name", "keywords"})


def last_activity(row: dict) -> str:
    """The later of a story's publish date and its newest Updated line."""
    return max(str(row.get("published") or ""), str(row.get("updated") or ""))


def source_count(row: dict) -> int:
    """The story's own source plus every other outlet that covered it."""
    return 1 + len(row.get("corroborators") or [])


def _ranked(rows, *keys) -> list[dict]:
    """`rows` sorted descending by each key in turn (first key is primary)."""
    out = list(rows)
    for key in reversed(keys):  # stable sorts: the last pass decides first
        out.sort(key=key, reverse=True)
    return out


def _composite(row: dict) -> float:
    try:
        return float(row.get("composite") or 0)
    except (TypeError, ValueError):
        return 0.0


def top_stories(
    rows: list[dict],
    now: str,
    days: int,
    n_max: int = TOP_STORIES_MAX,
    n_min: int = TOP_STORIES_MIN,
) -> tuple[list[dict], bool]:
    """(the front page's top stories, whether the window had to be topped up)."""
    cutoff = _cutoff(now, days)
    fresh = [r for r in rows if last_activity(r) >= cutoff]
    picked = _ranked(fresh, last_activity, source_count, _composite)[:n_max]
    if len(picked) >= n_min:
        return picked, False
    older = _ranked([r for r in rows if last_activity(r) < cutoff], last_activity, source_count)
    return picked + older[: n_min - len(picked)], True


def _cutoff(now: str, days: int) -> str:
    return (datetime.strptime(now, "%Y-%m-%d") - timedelta(days=days)).strftime("%Y-%m-%d")


def fresh_count(rows: list[dict], now: str, days: int) -> int:
    """How many of `rows` were active in the last `days` (the rest topped up)."""
    cutoff = _cutoff(now, days)
    return sum(1 for r in rows if last_activity(r) >= cutoff)


def window_note(fresh: int, total: int, days: int) -> str:
    """The one sentence README and site both print above the top stories."""
    if not total:
        return "No stories yet."
    if fresh == 0:
        return f"Nothing new in the last {days} days, so these are the latest top stories."
    if fresh < total:
        return (
            f"Fewer than five stories in the last {days} days, so the most recent ones "
            "before it fill in."
        )
    return f"The last {days} days, newest first."


# --- Claim changes: the ledger's job is to call claims out, not to-do lists ---
CHANGES_MAX = 6
CHANGES_MIN = 3
CHANGE_KINDS = ("added", "contested", "overturned")
_CONTESTING = ("contests", "refutes")


def added_on(claim: dict) -> str:
    """When the claim entered the ledger. `added_on` is the ledger's own record;
    an older claim without one falls back to `first_seen` (when the belief dates
    from). Never `last_reviewed`: every review bumps it, so it says nothing changed."""
    return str(claim.get("added_on") or claim.get("first_seen") or "")


def _contested_on(claim: dict) -> str:
    """When a contested claim became contested: the ledger's `changed_on`, else
    its newest contesting evidence, else the day it entered the ledger."""
    if claim.get("changed_on"):
        return str(claim["changed_on"])
    dates = [
        str(e.get("published") or "")
        for e in claim.get("evidence") or []
        if isinstance(e, dict) and e.get("stance") in _CONTESTING
    ]
    return max(dates, default="") or added_on(claim)


def _first(value) -> str:
    ids = value if isinstance(value, list) else [value] if value else []
    return str(ids[0]) if ids else ""


def _change_of(claim: dict) -> dict | None:
    """The one change a claim stands for, or None.

    overturned  a retired claim: headlined by the claim that replaced it
    contested   a live claim with evidence on both sides
    added       a current claim; one that replaced another is told by the
                overturned change instead, so a reversal shows once"""
    cid, status = str(claim.get("id") or ""), claim.get("status")
    if status in ("superseded", "refuted"):
        when = claim.get("changed_on") or claim.get("superseded_on") or ""
        change = {"kind": "overturned", "date": str(when)}
        change |= {"claim": _first(claim.get("superseded_by")) or cid, "replaced": cid}
    elif status == "contested":
        change = {"kind": "contested", "date": _contested_on(claim), "claim": cid}
    elif status == "current" and not claim.get("supersedes"):
        change = {"kind": "added", "date": added_on(claim), "claim": cid}
    else:
        return None
    return change if change["date"] and cid else None


def all_changes(claims: list[dict]) -> list[dict]:
    """Every claim change, newest first (ties: kind, then claim id)."""
    out = [ch for ch in map(_change_of, claims) if ch]
    out.sort(key=lambda ch: (ch["kind"], ch["claim"]))
    out.sort(key=lambda ch: ch["date"], reverse=True)
    return out


def claim_changes(
    claims: list[dict],
    now: str,
    days: int,
    n_max: int = CHANGES_MAX,
    n_min: int = CHANGES_MIN,
) -> tuple[list[dict], int]:
    """(the front page's claim changes, how many changes fall in the last `days`).

    At most `n_max` are shown. The window's changes come first, then the
    n_min top-up; the newest reversal is added after those only when a slot is
    still free, so an old one never pushes a change from the window off the
    list. A reversal older than the window carries `"pinned": True`. The count
    is of every change in the window, not just the ones shown."""
    cutoff = _cutoff(now, days)
    changes = all_changes(claims)
    fresh = [ch for ch in changes if ch["date"] >= cutoff]
    older = [ch for ch in changes if ch["date"] < cutoff]
    picked = fresh[:n_max] + older[: max(0, n_min - len(fresh))]
    reversal = next((ch for ch in changes if ch["kind"] == "overturned"), None)
    if reversal is not None:
        if reversal in picked:
            picked = [_pin(ch, cutoff) if ch is reversal else ch for ch in picked]
        elif len(picked) < n_max:
            picked.append(_pin(reversal, cutoff))
    return _by_date(picked), len(fresh)


def _pin(change: dict, cutoff: str) -> dict:
    """The newest reversal, marked `pinned` when it is older than the window."""
    return {**change, "pinned": True} if change["date"] < cutoff else change


def _by_date(changes: list[dict]) -> list[dict]:
    """Newest first, in all_changes' order within a date (stable sort)."""
    return sorted(changes, key=lambda ch: ch["date"], reverse=True)


def changes_note(fresh: int, total: int, days: int, last: str = "") -> str:
    """The one sentence README and site both print above the claim changes.
    `last` is the newest change's date (shown when the window had none)."""
    if not total:
        return "No claim has changed yet."
    if fresh == 0:
        return f"No claim changed in the last {days} days; the last change was {last}."
    if fresh > total:
        return f"The {total} newest of {fresh} changes in the last {days} days."
    if fresh < total:
        return (
            f"{fresh} change{'s' if fresh > 1 else ''} in the last {days} days; "
            "earlier ones fill in, each with its date."
        )
    return f"Every claim added, contested or overturned in the last {days} days."


def claim_domain(claim: dict, tax: taxonomy.Taxonomy) -> str:
    """The taxonomy ID a claim's domain label names, or "" if only a default fits."""
    topic, label = claim.get("topic") or "", claim.get("domain") or ""
    if topic not in tax.defaults or not label:
        return ""
    did, how = taxonomy.resolve(tax, topic, label)
    return did if how in _TRUSTED_RESOLUTION else ""
