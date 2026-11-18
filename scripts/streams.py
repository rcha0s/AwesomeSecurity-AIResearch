#!/usr/bin/env python3
"""
streams.py - the one loader for data/streams.yaml, plus the pure rules that
decide which findings and claims belong to a stream and where.

A stream (Harness Engineering is the first) is a reading list across the
taxonomy: it adds no pool and no analysis. Each sub-category is checked in
order and the first match wins: a finding whose domain is in `domains` always
matches; one whose domain is in `from` matches only when a `keywords` phrase
appears as whole words in its text (scripts/focus.py's matcher).

Pure apart from load(): generate_stream.py and the tests share these rules.

Usage:
    python scripts/streams.py list    # each stream's sub-categories and rules
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import yaml

import focus

STREAMS_FILE = Path(__file__).resolve().parent.parent / "data" / "streams.yaml"
TEXT_FIELDS = ("title", "takeaway", "summary", "statement")


@dataclass(frozen=True)
class Subcategory:
    id: str
    name: str
    scope: str
    domains: tuple[str, ...]
    sources: tuple[str, ...]  # the `from` domains
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class Stream:
    id: str
    name: str
    blurb: str
    library_days: int
    feed_max: int
    watch_min_relevance: float | None
    subcategories: tuple[Subcategory, ...]

    def domains(self) -> set[str]:
        """Every domain ID a finding of this stream can carry."""
        out: set[str] = set()
        for sub in self.subcategories:
            out |= set(sub.domains) | set(sub.sources)
        return out

    def subcategory(self, sid: str) -> Subcategory | None:
        return next((s for s in self.subcategories if s.id == sid), None)


def _subcategory(raw: dict) -> Subcategory:
    sid = str(raw.get("id") or "").strip()
    if not sid:
        raise ValueError("streams.yaml: a sub-category has no id")
    domains = tuple(raw.get("domains") or ())
    sources = tuple(raw.get("from") or ())
    keywords = tuple(str(k).strip().lower() for k in raw.get("keywords") or () if str(k).strip())
    if sources and not keywords:
        raise ValueError(f"streams.yaml: sub-category {sid!r} has `from` but no keywords")
    if not domains and not sources:
        raise ValueError(f"streams.yaml: sub-category {sid!r} matches nothing")
    return Subcategory(sid, str(raw.get("name") or sid), str(raw.get("scope") or ""), domains, sources, keywords)


def parse(data: dict, known_domains: set[str] | None = None) -> dict[str, Stream]:
    """Streams from the parsed YAML. With `known_domains`, every domain a rule
    names must be a taxonomy ID (a typo would silently empty a sub-category)."""
    out: dict[str, Stream] = {}
    for sid, body in (data.get("streams") or {}).items():
        subs = tuple(_subcategory(s) for s in body.get("subcategories") or ())
        ids = [s.id for s in subs]
        if len(set(ids)) != len(ids):
            raise ValueError(f"streams.yaml: stream {sid!r} repeats a sub-category id")
        stream = Stream(
            id=sid,
            name=str(body.get("name") or sid),
            blurb=" ".join(str(body.get("blurb") or "").split()),
            library_days=int(body.get("library_days") or 120),
            feed_max=int(body.get("feed_max") or 80),
            watch_min_relevance=(
                float(body["watch_min_relevance"]) if body.get("watch_min_relevance") is not None else None
            ),
            subcategories=subs,
        )
        if known_domains is not None:
            unknown = sorted(stream.domains() - known_domains)
            if unknown:
                raise ValueError(f"streams.yaml: stream {sid!r} names unknown domains {unknown}")
        out[sid] = stream
    return out


def load(path: Path | None = None, known_domains: set[str] | None = None) -> dict[str, Stream]:
    with open(path or STREAMS_FILE, encoding="utf-8") as fh:
        return parse(yaml.safe_load(fh) or {}, known_domains)


def item_text(item: dict) -> str:
    """Title, takeaway, summary, statement and tags, lowercased, for keyword rules."""
    parts = [str(item.get(f) or "") for f in TEXT_FIELDS]
    parts += [str(t).replace("-", " ") for t in item.get("tags") or ()]
    return " ".join(parts).lower()


def classify(item: dict, stream: Stream) -> str | None:
    """The id of the first sub-category `item` (a pool entry or a claim) matches,
    or None when it is not in the stream."""
    domain = str(item.get("domain_id") or item.get("domain") or "")
    if not domain:
        return None
    text = None
    for sub in stream.subcategories:
        if domain in sub.domains:
            return sub.id
        if domain in sub.sources:
            text = item_text(item) if text is None else text
            if any(focus._has_phrase(text, kw) for kw in sub.keywords):
                return sub.id
    return None


def item_date(item: dict) -> str:
    """The finding's own date (YYYY-MM-DD where known): published, else its month."""
    for key in ("published", "date", "added_on", "first_seen"):
        value = str(item.get(key) or "").strip()
        if value:
            return value[:10]
    return ""


def in_library(item: dict, now: datetime, days: int) -> bool:
    """True if the finding's date is inside the stream's library window. A
    month-only date (YYYY-MM) counts from the first of that month."""
    date = item_date(item)
    if not date:
        return False
    if len(date) == 7:
        date += "-01"
    try:
        when = datetime.strptime(date[:10], "%Y-%m-%d")
    except ValueError:
        return False
    return when >= now.replace(tzinfo=None) - timedelta(days=days)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args[:1] != ["list"]:
        print(__doc__.strip().splitlines()[-1])
        return 2
    for stream in load().values():
        print(f"{stream.id}: {stream.name} (library {stream.library_days} days)")
        for sub in stream.subcategories:
            rule = ", ".join(sub.domains) or "-"
            extra = f"; from {', '.join(sub.sources)} on {len(sub.keywords)} keywords" if sub.sources else ""
            print(f"  - {sub.id}: {sub.name} [domains: {rule}{extra}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
