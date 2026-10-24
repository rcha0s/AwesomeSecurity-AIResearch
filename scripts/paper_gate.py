#!/usr/bin/env python3
"""
paper_gate.py — Admission gate for research papers (ISC-29).

A raw preprint feed is a firehose; a paper only enters the candidate queue when
it carries a quality signal other than "it exists on arXiv":

  * venue          accepted at a registered venue (the ingest_conferences path;
                   the candidate carries a `venue` that path already vetted),
  * hf-daily       listed on Hugging Face Daily Papers (keyless public API),
  * curator-link   linked from a trusted curator's feed (TRUSTED_CURATORS), or
                   from a recent tl;dr sec issue page (ingest_curator_links.py
                   records those ids in data/_curator_arxiv.json).

Deterministic by design — no LLM judgment. Non-paper candidates (blogs, advisories,
repos) are not this gate's business and pass through. If a signal source cannot be
fetched the signal set is empty, so papers are dropped (fail closed), never admitted.
"""

from __future__ import annotations

import re
import sys
from datetime import timedelta
from urllib.parse import urlparse

import common as c

HF_DAILY_API = "https://huggingface.co/api/daily_papers"
HF_LOOKBACK_DAYS = 7  # the API serves one day per call; weekends come back empty

# Registry source ids whose links count as a curator endorsement.
TRUSTED_CURATORS = frozenset(
    {
        "rss:https-tldrsec-com-feed",  # tl;dr sec (feed 404s since ~2026-10; see below)
        "rss:https-simonwillison-net-atom-everything",  # Simon Willison
        "rss:https-googleprojectzero-blogspot-com-feeds-posts",  # Project Zero
    }
)
# tl;dr sec's issue pages, read by ingest_curator_links.py, which records the arXiv
# ids they link to here ({arxiv id: issue date}). It runs before aggregate.py.
CURATOR_LINKS_NAME = "_curator_arxiv.json"
CURATOR_LINKS_DEFAULT_DAYS = 14  # sources.yaml curator_links.lookback_days decides

PREPRINT_HOSTS = ("arxiv.org", "openreview.net", "eprint.iacr.org")
ARXIV_ID_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf|html)/((?:\d{4}\.\d{4,5})|(?:[a-z-]+(?:\.[A-Za-z]{2})?/\d{7}))",
    re.I,
)


def arxiv_ids(text: str) -> set[str]:
    """Every arXiv id mentioned in `text` (version suffix stripped, lowercased)."""
    return {m.lower() for m in ARXIV_ID_RE.findall(text or "")}


def arxiv_id(url: str) -> str | None:
    ids = arxiv_ids(url)
    return next(iter(ids)) if ids else None


def is_preprint(url: str) -> bool:
    host = (urlparse(url or "").hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in PREPRINT_HOSTS)


def curator_ids_from_entries(entries: list[dict]) -> set[str]:
    """arXiv ids a curator feed links to (entry link, summary and full content)."""
    ids: set[str] = set()
    for entry in entries:
        parts = [entry.get("link", ""), entry.get("summary", "")]
        parts += [part.get("value", "") for part in entry.get("content") or []]
        ids |= arxiv_ids(" ".join(parts))
    return ids


def curator_links_file():
    return c.DATA_DIR / CURATOR_LINKS_NAME


def save_curator_link_ids(ids: dict[str, str]) -> None:
    """Record {arXiv id: issue date} found in curator issues (ingest_curator_links)."""
    c.save_json(curator_links_file(), dict(sorted(ids.items())))


def curator_window_days() -> int:
    cfg = (c.load_yaml(c.SOURCES_FILE) or {}).get("curator_links") or {}
    return int(cfg.get("lookback_days", CURATOR_LINKS_DEFAULT_DAYS))


def curator_link_ids(max_age_days: int | None = None) -> set[str]:
    """arXiv ids linked from curator issues published inside the curator window
    (the same `curator_links.lookback_days` the ingestor reads). Missing file = none."""
    max_age_days = curator_window_days() if max_age_days is None else max_age_days
    data = c.load_json(curator_links_file(), default={}) or {}
    # A backfill counts the issues of the curator window before its own end.
    since = (c.freshness_now() - timedelta(days=max_age_days)).date().isoformat()
    if not isinstance(data, dict):
        return set()
    return {str(k).lower() for k, day in data.items() if str(day or "") >= since}


def fetch_hf_daily() -> tuple[set[str], int]:
    """(arXiv ids on HF Daily Papers over the lookback window, days that answered).

    A day "answers" when the API returns a JSON list (empty is fine: weekends).
    Prints HF-SIGNAL-UNAVAILABLE when no day answered, so a total outage or a schema
    change is visible in the scan log instead of silently closing the gate.
    """
    import requests  # local import keeps offline unit tests import-clean

    ids: set[str] = set()
    ok_days = 0
    days = c.window_days(HF_LOOKBACK_DAYS)  # a backfill asks for its own window's days
    for day in days:
        try:
            resp = requests.get(
                HF_DAILY_API,
                params={"date": day, "limit": 100},
                timeout=30,
                headers={"User-Agent": c.HTTP_USER_AGENT},
            )
            resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, list):
                raise ValueError(f"unexpected {type(data).__name__} payload")
            ids |= {
                str(i["paper"]["id"]).lower()
                for i in data
                if isinstance(i, dict) and isinstance(i.get("paper"), dict) and i["paper"].get("id")
            }
            ok_days += 1
        except Exception as exc:  # noqa: BLE001 - fail closed, never block the scan
            print(f"   ! HF Daily Papers {day} unavailable: {exc}", file=sys.stderr)
    if ok_days == 0:
        print(
            "HF-SIGNAL-UNAVAILABLE: Hugging Face Daily Papers answered 0 of "
            f"{len(days)} days; ungated preprints will be dropped this run"
        )
    return ids, ok_days


def fetch_hf_daily_ids() -> set[str]:
    return fetch_hf_daily()[0]


class Signals:
    """The quality-signal sets a scan has gathered. HF ids load lazily, once."""

    def __init__(self, hf_ids: set[str] | None = None, curator_ids: set[str] | None = None):
        self._hf_ids = hf_ids
        self.hf_days_ok: int | None = None  # None until fetched (or when preset)
        self.curator_ids: set[str] = set(curator_ids or ())
        self.gated = 0

    @property
    def hf_ids(self) -> set[str]:
        if self._hf_ids is None:
            self._hf_ids, self.hf_days_ok = fetch_hf_daily()
        return self._hf_ids

    def status_line(self) -> str:
        if self.hf_days_ok is None:
            hf = "not needed"
        elif self.hf_days_ok == 0:
            hf = "unavailable"
        else:
            hf = f"ok ({self.hf_days_ok}/{len(c.window_days(HF_LOOKBACK_DAYS))} days)"
        return f"papers gated: {self.gated}, HF signal: {hf}"


def admit(cand: dict, signals: Signals) -> tuple[bool, str]:
    """(admitted, reason). Papers need a quality signal; everything else passes."""
    url = cand.get("article_url") or cand.get("source_url") or ""
    if not is_preprint(url):
        return True, "not-a-preprint"
    if cand.get("venue"):
        return True, "venue"
    pid = arxiv_id(url)
    if pid and pid in signals.curator_ids:
        return True, "curator-link"
    if pid and pid in signals.hf_ids:
        return True, "hf-daily"
    signals.gated += 1
    return False, "no-quality-signal"
