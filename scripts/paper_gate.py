#!/usr/bin/env python3
"""
paper_gate.py — Admission gate for research papers (ISC-29).

A raw preprint feed is a firehose; a paper only enters the candidate queue when
it carries a quality signal other than "it exists on arXiv":

  * venue          accepted at a registered venue (the ingest_conferences path;
                   the candidate carries a `venue` that path already vetted),
  * hf-daily       listed on Hugging Face Daily Papers (keyless public API),
  * curator-link   linked from a trusted curator's feed (TRUSTED_CURATORS).

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
        "rss:https-tldrsec-com-feed",  # tl;dr sec
        "rss:https-simonwillison-net-atom-everything",  # Simon Willison
        "rss:https-googleprojectzero-blogspot-com-feeds-posts",  # Project Zero
    }
)

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


def fetch_hf_daily_ids() -> set[str]:
    """arXiv ids on HF Daily Papers over the lookback window; empty set on failure."""
    import requests  # local import keeps offline unit tests import-clean

    ids: set[str] = set()
    today = c.utcnow().date()
    for back in range(HF_LOOKBACK_DAYS):
        day = (today - timedelta(days=back)).isoformat()
        try:
            resp = requests.get(
                HF_DAILY_API,
                params={"date": day, "limit": 100},
                timeout=30,
                headers={"User-Agent": c.HTTP_USER_AGENT},
            )
            resp.raise_for_status()
            ids |= {str(i["paper"]["id"]).lower() for i in resp.json()}
        except Exception as exc:  # noqa: BLE001 - fail closed, never block the scan
            print(f"   ! HF Daily Papers {day} unavailable: {exc}", file=sys.stderr)
    return ids


class Signals:
    """The quality-signal sets a scan has gathered. HF ids load lazily, once."""

    def __init__(self, hf_ids: set[str] | None = None, curator_ids: set[str] | None = None):
        self._hf_ids = hf_ids
        self.curator_ids: set[str] = set(curator_ids or ())

    @property
    def hf_ids(self) -> set[str]:
        if self._hf_ids is None:
            self._hf_ids = fetch_hf_daily_ids()
        return self._hf_ids


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
    return False, "no-quality-signal"
