#!/usr/bin/env python3
"""
aggregate.py — Discover recent research from credible RSS/Atom feeds.

Pulls items from the feeds in sources.yaml, keeps those published in the last
`max_age_days` days (a backfill: inside its window, common.ingest_window), makes a best-guess track/domain classification, and stages
them as candidates in data/candidates.json (de-duped against both the staging
queue and the published pools). The LLM analyze step (the /research-scan skill)
turns candidates into scored, actionable pool entries — this script never writes
to the pools directly.

Usage:
    python scripts/aggregate.py            # stage new candidates
    python scripts/aggregate.py --dry-run  # print what would be staged, no write
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import common as c
import paper_gate as pg
import sources_registry as sr
import taxonomy as tx

try:
    import feedparser
except ImportError:  # pragma: no cover - environment guard
    sys.exit("Missing dependencies. Run: pip install -r requirements.txt")


def classify_domain(text: str, rules: dict, feed_domains: list[str]) -> str | None:
    text = text.lower()
    catch_alls = rules.get("catch_alls") or {}
    for domain, keywords in rules["domains"].items():
        if any(kw in text for kw in keywords) and has_context(text, catch_alls.get(domain)):
            return domain
    if len(feed_domains) == 1:
        return feed_domains[0]
    return None


def has_context(text: str, catch_all: dict | None) -> bool:
    """A catch-all class (sources.yaml `catch_alls`) also needs one context term."""
    terms = (catch_all or {}).get("context") or []
    return not terms or any(t in text for t in terms)


def classify_subtype(text: str, domain: str, rules: dict) -> str:
    text = text.lower()
    for subtype, keywords in rules["subtypes"].get(domain, {}).items():
        if any(kw in text for kw in keywords):
            return subtype
    return "Uncategorized"


def guess_fields(blob: str, label: str, rules: dict, topic: str | None = None) -> dict:
    """The router's verdict as candidate fields.

    `label` is the sources.yaml router class (or a source's fallback label). It
    alone decides whether an item is ingested and which topic it guesses, exactly
    as before the taxonomy. `guess_domain` is a taxonomy ID of that topic, picked
    from the taxonomy's keyword hints (the label itself if it is an ID, else the
    topic default, when none fire); the router label is kept as `guess_label`."""
    topic = c.topic_for_domain(label) or topic
    hint = tx.domain_hint(topic, blob, default=label) if topic else None
    return {
        "guess_topic": topic,
        "guess_domain": hint,
        "guess_label": label,
        "guess_subtype": classify_subtype(blob, label, rules),
    }


def build_candidate(entry: dict, feed: dict, rules: dict) -> dict | None:
    url = entry.get("link", "")
    if not c.normalize_url(url):
        return None
    dt = c.entry_datetime(entry)
    title = (entry.get("title") or "").strip()
    excerpt = c.clean_summary(entry.get("summary", ""))
    blob = f"{title} {excerpt}"
    # A `strict` feed (any high-volume feed) only stages items that actually
    # keyword-match a topic — no single-domain fallback.
    feed_domains = [] if feed.get("strict") else feed.get("domains", [])
    domain = classify_domain(blob, rules, feed_domains)
    if domain is None:
        return None
    return {
        "id": c.make_id(title, c.normalize_url(url)),
        "discovered_via": "rss",
        "title": title,
        "source_name": feed["name"],
        "source_type": feed.get("type", ""),
        "source_url": url,
        "article_url": url,
        "tweet_url": None,
        "author": None,
        "published": dt.strftime("%Y-%m-%d") if dt else c.date_from_url(url),
        "date": dt.strftime("%Y-%m") if dt else None,
        "excerpt": excerpt,
        "raw_path": None,
        **guess_fields(blob, domain, rules),
        "source_id": feed.get("source_id"),
        "source_rank": feed.get("source_rank"),
        "source_topics": feed.get("topics", []),
        "retrieved_at": c.utcnow_iso(),
    }


def feed_from_source(source: dict) -> dict:
    return {
        "name": source["name"],
        "url": source["handle"],
        "type": source.get("notes", ""),
        "domains": source.get("domains", []),
        "strict": source.get("strict", False),
        "source_id": source["id"],
        "source_rank": source.get("rank"),
        "topics": source.get("topics", []),
    }


def collect_rss(
    rules: dict,
    cutoff: datetime,
    signals: pg.Signals | None = None,
    until: datetime | None = None,
) -> list[dict]:
    """Fetch every registered rss/newsletter feed and build fresh candidates
    (published in [cutoff, until]; a backfill sets `until`, and only items its
    feeds still carry can be recovered).

    Two passes: first parse every feed (trusted-curator feeds supply the paper
    gate's curator-link signal), then build candidates and drop any preprint
    that carries no quality signal (paper_gate.admit, ISC-29).
    """
    signals = signals or pg.Signals()
    signals.curator_ids |= pg.curator_link_ids()  # arXiv links in tl;dr sec issues
    feeds = sr.sources_of_type("rss") + sr.sources_of_type("newsletter")
    parsed_feeds: list[tuple[dict, list]] = []
    for source in feeds:
        feed = feed_from_source(source)
        print(f"-> {feed['name']}: {feed['url']}")
        parsed = feedparser.parse(feed["url"], request_headers={"User-Agent": c.HTTP_USER_AGENT})
        if parsed.bozo and not parsed.entries:
            print(f"   ! could not parse feed ({getattr(parsed, 'bozo_exception', '')})")
            continue
        if source["id"] in pg.TRUSTED_CURATORS:
            signals.curator_ids |= pg.curator_ids_from_entries(parsed.entries)
        parsed_feeds.append((feed, parsed.entries))

    candidates: list[dict] = []
    for feed, entries in parsed_feeds:
        for entry in entries:
            if not c.in_ingest_window(c.entry_datetime(entry), cutoff, until):
                continue
            cand = build_candidate(entry, feed, rules)
            if not cand:
                continue
            ok, reason = pg.admit(cand, signals)
            if ok:
                candidates.append(cand)
            else:
                print(f"   - gated ({reason}): {cand['title'][:70]}")
    print(f"   [{signals.status_line()}]")
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't write changes")
    args = ap.parse_args()

    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    cutoff, until = c.ingest_window(c.ingest_age_days())
    candidates = collect_rss(rules, cutoff, until=until)

    if args.dry_run:
        print(f"\n(dry run) {len(candidates)} candidate(s) would be staged:")
        for cand in candidates:
            print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title']}")
        return 0

    added = c.add_candidates(candidates)
    print(f"\nStaged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    for cand in added:
        print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
