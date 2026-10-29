#!/usr/bin/env python3
"""
focus.py - which of Rohan's focus areas an item belongs to (ISA ISC-56).

The areas live in config.yaml under `focus:`. An item (a site story row, a pool
entry or a claim) matches an area when its taxonomy domain ID is one of the
area's `domains`, or one of its `keywords` appears as whole words, in any case,
in the item's title, takeaway, summary or statement. Pure: no I/O, so
briefing.py, common.py (rerank keeps matching news) and the digest agree.
"""

from __future__ import annotations

import re

TEXT_FIELDS = ("title", "takeaway", "summary", "statement")


def _domain_id(item: dict) -> str:
    """Rows carry `domain_id`; a raw pool entry carries the ID in `domain`."""
    return str(item.get("domain_id") or item.get("domain") or "")


def _text(item: dict) -> str:
    return " ".join(str(item.get(f) or "") for f in TEXT_FIELDS).lower()


def _has_phrase(text: str, phrase: str) -> bool:
    phrase = phrase.strip().lower()
    if not phrase:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text) is not None


def areas(item: dict, focus: dict | None) -> list[str]:
    """IDs of the focus areas `item` matches, in config order (empty: none)."""
    out = []
    domain, text = _domain_id(item), _text(item)
    for area in (focus or {}).get("areas") or []:
        if domain and domain in (area.get("domains") or []):
            out.append(area["id"])
        elif any(_has_phrase(text, kw) for kw in area.get("keywords") or []):
            out.append(area["id"])
    return out


def matches(item: dict, focus: dict | None) -> bool:
    return bool(areas(item, focus))


def names(area_ids: list[str], focus: dict | None) -> list[str]:
    """Display names for area IDs, in the order given."""
    by_id = {a["id"]: a.get("name") or a["id"] for a in (focus or {}).get("areas") or []}
    return [by_id[i] for i in area_ids if i in by_id]
