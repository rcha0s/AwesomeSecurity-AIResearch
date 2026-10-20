#!/usr/bin/env python3
"""
prefilter.py — Deterministic funnel between ingest and LLM analysis.

Runs on `data/candidates.json` (title + short summary each ingestor already
stores) and splits candidates into three buckets so the LLM stops burning
tokens on obvious noise:

    candidates.dropped.json    Definitely not tier-1. Deny-list hit, off-topic,
                               or a near-duplicate of a pool/archive entry.
                               Never gets a full-text fetch. Never sees an LLM.

    candidates.routed.json     High-confidence domain hint (a taxonomy ID)
                               from the keyword table. The analyzer starts
                               from that domain instead of classifying cold.

    candidates.filtered.json   Ambiguous. Domain hint was weak/tied, or the
                               item lives in the tier-2 news lane. The LLM
                               does the full classification pass here.

Input, output, and behavior are pure JSON I/O. No network. No LLM. Operates
only on data the ingestors already stored.

Keywords and deny terms come from `data/taxonomy.yaml` (via taxonomy.py), the
same vocabulary the analyzer picks domain IDs from; the LLM still owns the
call for anything that lands in `candidates.filtered.json`.

Usage:
    python scripts/prefilter.py             # write the three buckets
    python scripts/prefilter.py --dry-run   # print counts and top titles only
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import common as c
import taxonomy as tx


def _dropped_file() -> Path:
    return c.DATA_DIR / "candidates.dropped.json"


def _routed_file() -> Path:
    return c.DATA_DIR / "candidates.routed.json"


def _filtered_file() -> Path:
    return c.DATA_DIR / "candidates.filtered.json"


# A domain hint is authoritative only if its keyword-hit count is >= this
# AND beats the runner-up by at least this margin. Ties or weak wins fall
# through to `candidates.filtered.json` for the LLM to adjudicate.
DOMAIN_MIN_HITS = 2
DOMAIN_MIN_MARGIN = 1


@dataclass(frozen=True)
class KeywordTable:
    keywords: dict[str, tuple[str, ...]]  # domain id -> keyword hints
    excluded: tuple[str, ...]


def load_keywords(path: Path | None = None) -> KeywordTable:
    """The prefilter's view of the taxonomy: every domain's hints + deny terms."""
    tax = tx.load(path) if path else tx.get()
    keywords = {did: dom.keywords for did, dom in tax.domains.items()}
    return KeywordTable(keywords=keywords, excluded=tax.excluded_terms)


def haystack(candidate: dict) -> str:
    """The lowercased text field the keyword matcher scans."""
    parts = [
        candidate.get("title") or "",
        candidate.get("excerpt") or "",
        candidate.get("guess_domain") or "",
        candidate.get("guess_subtype") or "",
    ]
    return " ".join(parts).lower()


def score_domains(text: str, table: KeywordTable) -> dict[str, int]:
    """Keyword-hit count per domain on the given haystack."""
    return {did: sum(1 for kw in terms if kw in text) for did, terms in table.keywords.items()}


def best_domain(scores: dict[str, int]) -> tuple[str | None, int, int]:
    """Return (winning_domain, winner_hits, margin_over_runner_up).

    winning_domain is None if no domain scored above zero. Ties return the
    first alphabetically but with margin=0, so the caller can reject."""
    if not scores or max(scores.values()) == 0:
        return None, 0, 0
    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    top_id, top_hits = ordered[0]
    runner_hits = ordered[1][1] if len(ordered) > 1 else 0
    return top_id, top_hits, top_hits - runner_hits


def excluded_hit(text: str, table: KeywordTable) -> str | None:
    """Return the first excluded term found in `text`, else None."""
    for term in table.excluded:
        if term in text:
            return term
    return None


def duplicate_of_pool(candidate: dict, pool_urls: set[str], pool_titles: list[str]) -> bool:
    """URL exact-match or title trigram-similarity against the pool + archive."""
    for key in ("source_url", "article_url", "tweet_url"):
        url = candidate.get(key)
        if url and c.normalize_url(url) in pool_urls:
            return True
    title = candidate.get("title") or ""
    if not title:
        return False
    return any(c.title_similar(title, t) for t in pool_titles)


@dataclass(frozen=True)
class Bucketed:
    dropped: list[dict]
    routed: list[dict]
    filtered: list[dict]


def bucket(candidates: list[dict], table: KeywordTable) -> Bucketed:
    """Sort candidates into (dropped, routed, filtered)."""
    pool_entries = c.all_pool_entries()
    pool_urls = c.known_urls()
    pool_titles = [e.get("title", "") for e in pool_entries]

    dropped: list[dict] = []
    routed: list[dict] = []
    filtered: list[dict] = []

    for cand in candidates:
        text = haystack(cand)
        # 1. Existing news deny-list (stock/puff/hype).
        if c.news_denylist_hit(cand):
            dropped.append(_annotate(cand, "denylist"))
            continue
        # 2. Taxonomy excluded-terms deny list (out-of-scope subjects).
        term = excluded_hit(text, table)
        if term is not None:
            dropped.append(_annotate(cand, f"excluded:{term}"))
            continue
        # 3. Near-duplicate of a pool/archive entry.
        if duplicate_of_pool(cand, pool_urls, pool_titles):
            dropped.append(_annotate(cand, "duplicate"))
            continue
        # 4. Domain hint from keywords.
        scores = score_domains(text, table)
        domain, hits, margin = best_domain(scores)
        if domain and hits >= DOMAIN_MIN_HITS and margin >= DOMAIN_MIN_MARGIN:
            routed.append(
                _annotate(
                    cand, "routed", domain_hint=domain, domain_hits=hits, domain_margin=margin
                )
            )
        else:
            # No hint or ambiguous — hand to the LLM.
            filtered.append(_annotate(cand, "filtered", domain_hits=hits, domain_margin=margin))

    return Bucketed(dropped=dropped, routed=routed, filtered=filtered)


def _annotate(cand: dict, reason: str, **fields) -> dict:
    """Return a shallow copy with prefilter metadata attached under `prefilter`."""
    out = dict(cand)
    out["prefilter"] = {"reason": reason, **fields}
    return out


def _write(path: Path, entries: list[dict]) -> None:
    c.save_json(path, entries)


def summarize(b: Bucketed) -> str:
    lines = [
        f"prefilter: dropped={len(b.dropped)} routed={len(b.routed)} " f"filtered={len(b.filtered)}"
    ]
    for label, group in (("dropped", b.dropped), ("routed", b.routed), ("filtered", b.filtered)):
        if not group:
            continue
        top = ", ".join((e.get("title") or "")[:40] for e in group[:3])
        lines.append(f"  {label}: {top}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Print counts only; do not write output files."
    )
    args = parser.parse_args(argv)

    candidates = c.load_candidates()
    if not candidates:
        print("prefilter: no candidates to sort — did the ingest run?", file=sys.stderr)
        return 1
    table = load_keywords()
    result = bucket(candidates, table)
    print(summarize(result))
    if args.dry_run:
        return 0
    _write(_dropped_file(), result.dropped)
    _write(_routed_file(), result.routed)
    _write(_filtered_file(), result.filtered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
