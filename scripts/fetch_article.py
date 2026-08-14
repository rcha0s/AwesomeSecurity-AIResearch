#!/usr/bin/env python3
"""
fetch_article.py — Populate `raw_path` for prefilter-survivor candidates.

Runs after `scripts/prefilter.py`. Reads `data/candidates.routed.json` and
`data/candidates.filtered.json`, and for each candidate that still has
`raw_path: None`, fetches the article body via r.jina.ai and writes
`data/_raw/<candidate_id>.txt`. Updates the candidate's `raw_path` in
place so the downstream LLM step grounds against the paper body, not the
abstract.

Strategy dispatcher per source:

  arxiv `/abs/<id>` → try `/html/<id>v1` first, fall back to
                      `/pdf/<id>` (both via r.jina). Final fallback: the
                      abstract landing page.
  GitHub repos      → already handled by ingest_github.py (README written
                      at ingest time). No re-fetch here.
  HN / GHSA / RSS   → r.jina fetch of the article_url directly.

No paid dependencies. All routes go through `common.fetch_readable`.

Usage:
    python scripts/fetch_article.py                  # fetch survivors
    python scripts/fetch_article.py --dry-run        # print planned fetches
    python scripts/fetch_article.py --limit 20       # cap network work
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from typing import Callable

import common as c

MIN_BODY_CHARS = 4000  # below this, we assume the HTML variant is a stub
FETCH_DELAY_SECONDS = 1.0  # be polite to r.jina


ARXIV_ABS_RE = re.compile(r"https?://arxiv\.org/abs/([\d.]+)(?:v\d+)?/?", re.I)


def _routed_file() -> Path:
    return c.DATA_DIR / "candidates.routed.json"


def _filtered_file() -> Path:
    return c.DATA_DIR / "candidates.filtered.json"


def arxiv_id(url: str) -> str | None:
    """Extract the bare arxiv ID from any of the /abs/, /html/, or /pdf/
    forms. Returns None if the URL is not an arxiv article link."""
    m = ARXIV_ABS_RE.search(url or "")
    if m:
        return m.group(1)
    m = re.search(r"arxiv\.org/(?:html|pdf)/([\d.]+)(?:v\d+)?/?", url or "", re.I)
    if m:
        return m.group(1)
    return None


def arxiv_html_url(paper_id: str) -> str:
    return f"https://arxiv.org/html/{paper_id}v1"


def arxiv_pdf_url(paper_id: str) -> str:
    return f"https://arxiv.org/pdf/{paper_id}"


FetchFn = Callable[[str], str]


def default_fetch(url: str) -> str:
    """Real network fetch; monkeypatched in tests to stay offline."""
    return c.fetch_readable(url, timeout=30, max_chars=40000)


def fetch_arxiv_body(paper_id: str, fetch: FetchFn = default_fetch) -> str | None:
    """Try HTML variant first, PDF fallback. Return None if both fail."""
    for candidate_url in (arxiv_html_url(paper_id), arxiv_pdf_url(paper_id)):
        try:
            body = fetch(candidate_url)
        except Exception:  # noqa: BLE001 — any HTTP or parse error is a miss
            continue
        if body and len(body) >= MIN_BODY_CHARS:
            return body
    return None


def fetch_generic_body(article_url: str, fetch: FetchFn = default_fetch) -> str | None:
    """Read the article via r.jina; None on any error or empty response."""
    try:
        return fetch(article_url)
    except Exception:  # noqa: BLE001
        return None


def fetch_body(candidate: dict, fetch: FetchFn = default_fetch) -> str | None:
    """Dispatcher. Returns the body text or None if no strategy applies."""
    url = candidate.get("article_url") or candidate.get("source_url") or ""
    paper_id = arxiv_id(url)
    if paper_id:
        return fetch_arxiv_body(paper_id, fetch=fetch)
    if url:
        return fetch_generic_body(url, fetch=fetch)
    return None


def needs_fetch(candidate: dict) -> bool:
    """True if raw_path is missing AND we have a URL to try."""
    if candidate.get("raw_path"):
        return False
    return bool(candidate.get("article_url") or candidate.get("source_url"))


def populate_raw_paths(candidates: list[dict], *, dry_run: bool = False,
                       limit: int | None = None,
                       fetch: FetchFn | None = None,
                       delay: float = FETCH_DELAY_SECONDS) -> tuple[int, int]:
    """For each candidate needing a body, fetch + write + set raw_path in place.

    Returns (fetched_count, skipped_count). Mutates the input list."""
    # Resolve default_fetch lazily so tests can monkeypatch the module attr
    # after import.
    if fetch is None:
        fetch = default_fetch
    fetched = skipped = 0
    for cand in candidates:
        if not needs_fetch(cand):
            skipped += 1
            continue
        if limit is not None and fetched >= limit:
            skipped += 1
            continue
        title = (cand.get("title") or "")[:50]
        if dry_run:
            url = cand.get("article_url") or cand.get("source_url") or "?"
            paper_id = arxiv_id(url)
            plan = arxiv_html_url(paper_id) if paper_id else url
            print(f"  plan: {title} → {plan}")
            fetched += 1
            continue
        body = fetch_body(cand, fetch=fetch)
        if not body:
            print(f"  miss: {title}", file=sys.stderr)
            skipped += 1
            continue
        cand["raw_path"] = c.write_raw(cand["id"], body)
        fetched += 1
        print(f"  ok:   {title} ({len(body)}c)")
        if delay:
            time.sleep(delay)
    return fetched, skipped


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true",
                   help="Print planned fetches; don't hit the network.")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap the number of fetches this run.")
    args = p.parse_args(argv)

    total_fetched = total_skipped = 0
    for path in (_routed_file(), _filtered_file()):
        if not path.exists():
            print(f"fetch_article: {path.name} missing — run prefilter.py first.",
                  file=sys.stderr)
            continue
        cands = c.load_json(path, default=[]) or []
        print(f"fetch_article: {path.name} — {len(cands)} candidates")
        f, s = populate_raw_paths(cands, dry_run=args.dry_run,
                                   limit=args.limit)
        total_fetched += f
        total_skipped += s
        if not args.dry_run:
            c.save_json(path, cands)
    print(f"fetch_article: fetched={total_fetched} skipped={total_skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
