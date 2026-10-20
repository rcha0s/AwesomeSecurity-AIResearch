#!/usr/bin/env python3
"""
briefing.py - what leads the front page, decided once for README and site.

The README teaser and the site's Briefing both show "this week's top stories"
and the top "what to do now" claims. They are picked here, from the same site
rows, so the two surfaces can never disagree.

  top_stories   rows active in the last `days` (a fresh Updated line counts),
                most covering sources first, then most recent activity, then
                composite. Fewer than `n_min` in the window -> topped up with
                the most recent stories outside it (and the caller says so).
  top_claims    live `current` claims that carry guidance, most recently
                reviewed first, then highest confidence.
  claim_domain  a claim's free-text domain label as a taxonomy ID, or "".

Pure functions over payload rows; generate_html.py and generate_site.py do I/O.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import taxonomy

TOP_STORIES_MAX = 8
TOP_STORIES_MIN = 5
TOP_CLAIMS = 3
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
    picked = _ranked(fresh, source_count, last_activity, _composite)[:n_max]
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
    return f"The last {days} days: the stories with the most covering sources first."


def top_claims(claims: list[dict], n: int = TOP_CLAIMS) -> list[dict]:
    """The standing answers to act on now: current, with guidance, freshest first."""
    live = [c for c in claims if c.get("status") == "current" and c.get("guidance")]
    live.sort(key=lambda c: c.get("id", ""))
    return _ranked(live, lambda c: str(c.get("last_reviewed") or ""), _conf)[:n]


def _conf(claim: dict) -> float:
    try:
        return float(claim.get("confidence") or 0)
    except (TypeError, ValueError):
        return 0.0


def claim_domain(claim: dict, tax: taxonomy.Taxonomy) -> str:
    """The taxonomy ID a claim's domain label names, or "" if only a default fits."""
    topic, label = claim.get("topic") or "", claim.get("domain") or ""
    if topic not in tax.defaults or not label:
        return ""
    did, how = taxonomy.resolve(tax, topic, label)
    return did if how in _TRUSTED_RESOLUTION else ""
