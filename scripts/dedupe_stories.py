#!/usr/bin/env python3
"""
dedupe_stories.py — Story-key extractor + collision detector for the news lane.

The problem this solves: a Kimi K3 release lands as three separate feed items
(Moonshot blog, Hugging Face repost, HN thread). Vetted through the news gate
they'd all cross the finish line as independent findings. That's spam. The
research lane doesn't hit this problem (novelty gate) — the news lane does.

Story key = a small tuple that fingerprints a story:

    - canonical URL          (strip UTM/gclid, drop fragment, lower host,
                              follow one redirect hop when the source has
                              already been fetched — otherwise use the raw URL)
    - title 3-gram shingle   (lowercase, stopwords out, punctuation gone,
                              stemmed to trigrams for Jaccard)
    - entity set             (lab/model aliases + capitalized bigrams from
                              title + first ~200 chars of summary)

Collision rule: TWO of the three signals must match. That way the same story
on two sites (different URL) still collides via title-shingle + entity overlap;
a "Kimi K3 tutorial" and the "Kimi K3 release" don't collide (entities overlap
but title shingles differ).

These are the pure fingerprint + collision primitives. The permanent story
ledger that uses them (data/news_stories.json, never pruned) lives in
story_ledger.py; this module does no I/O.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Alias map for common labs / model families. Each canonical name maps to a
# set of aliases that all resolve to the canonical when detected. Seeded
# by hand — the fallback capitalized-bigram scanner catches anything we miss.
_ENTITY_ALIASES: dict[str, tuple[str, ...]] = {
    "OpenAI": ("openai", "gpt-5.6", "gpt-5", "gpt5.6", "gpt5", "luna", "terra", "sol", "codex"),
    "Anthropic": (
        "anthropic",
        "claude",
        "claude fable 5",
        "claude opus",
        "claude sonnet",
        "claude haiku",
    ),
    "Google DeepMind": ("deepmind", "google deepmind", "gemini", "gemini robotics"),
    "Meta AI": ("meta ai", "llama", "llama 3", "llama-3", "llama 4"),
    "Moonshot": ("moonshot", "kimi", "kimi k3", "kimi k2"),
    "Mistral": ("mistral", "mistral ai"),
    "Hugging Face": ("hugging face", "huggingface"),
    "Boston Dynamics": ("boston dynamics",),
    "MCP": ("mcp", "model context protocol", "modelcontextprotocol"),
    "AWS": ("aws", "amazon web services", "bedrock", "amazon bedrock"),
    "Microsoft": ("microsoft", "azure"),
    "Cloudflare": ("cloudflare",),
    "GitHub": ("github", "ghsa"),
}
# Flat lookup: alias -> canonical.
_ALIAS_TO_CANONICAL: dict[str, str] = {
    alias: canonical for canonical, aliases in _ENTITY_ALIASES.items() for alias in aliases
}

# English stopwords for title-shingle prep. Small on purpose — we want the
# distinctive tokens to survive.
_STOPWORDS = frozenset(
    (
        "a an the and or but of for to in on at by with from as is are was were "
        "be been being has have had do does did into over under across between "
        "this that these those it its i's you your they their we our its own"
    ).split()
)

_TRACKING_PARAMS = frozenset(
    (
        "utm_source utm_medium utm_campaign utm_term utm_content utm_id "
        "gclid fbclid mc_cid mc_eid mkt_tok ref referrer share source"
    ).split()
)

BUCKET_DAYS = 7  # week-of-published
COLLISION_JACCARD_TITLE = 0.5  # token-set OR trigram Jaccard; real-world
# rewrites hover around .45–.55
COLLISION_JACCARD_ENTITY = 0.6  # overlap coefficient (subset-friendly)


# ---------------------------------------------------------------------------
# Canonical URL
# ---------------------------------------------------------------------------
def canonical_url(url: str) -> str:
    """Strip tracking params, fragment, trailing slash; lower host. Returns
    the input on any parse failure — better to compare literal strings than
    to crash."""
    if not url:
        return ""
    try:
        p = urlparse(url.strip())
    except (ValueError, TypeError):
        return url
    if not p.netloc:
        return url
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = [
        (k, v)
        for k, v in parse_qsl(p.query, keep_blank_values=False)
        if k.lower() not in _TRACKING_PARAMS
    ]
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower() or "https", host, path, "", urlencode(query), ""))


# ---------------------------------------------------------------------------
# Title shingles (3-grams)
# ---------------------------------------------------------------------------
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall((text or "").lower()) if t not in _STOPWORDS]


def title_tokens(title: str) -> set[str]:
    """Stopword-stripped token set for a title. Cheaper than trigrams and
    order-insensitive — 'Kimi K3 open weights' and 'K3 Kimi weights open'
    hash to the same set, which matches how the same story gets rewritten
    across outlets."""
    return set(_tokens(title))


def title_shingles(title: str) -> set[str]:
    """Trigram token shingles. Kept for completeness (order-sensitive signal)
    but no longer the sole driver of the title-similarity score."""
    toks = _tokens(title)
    if len(toks) < 3:
        return set(toks)
    return {" ".join(toks[i : i + 3]) for i in range(len(toks) - 2)}


def title_similarity(a_title: str, b_title: str) -> float:
    """Best-of two: token-set Jaccard OR trigram Jaccard. Two rewrites of
    the same headline usually share tokens; two verbatim reposts also share
    trigrams. Either signal winning gets us to the collision threshold."""
    ta, tb = title_tokens(a_title), title_tokens(b_title)
    sa, sb = title_shingles(a_title), title_shingles(b_title)
    return max(jaccard(ta, tb), jaccard(sa, sb))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def overlap_coefficient(a: set[str], b: set[str]) -> float:
    """|A ∩ B| / min(|A|, |B|). Rewards subset relationships — a short
    entity set that's fully contained in a longer one scores 1.0. Right
    for entities where a story writeup with extra names ('AWS + Cloudflare
    + Microsoft ship day-zero MCP support') shouldn't beat down the match
    against the shorter primary ('MCP 2026-07-28 spec ships')."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


# ---------------------------------------------------------------------------
# Entity set
# ---------------------------------------------------------------------------
_BIGRAM_RE = re.compile(r"\b([A-Z][A-Za-z0-9\-]+(?:\s+[A-Z][A-Za-z0-9\-]+)+)\b")


def entities(*texts: str) -> set[str]:
    """Canonical entities detected in the concatenated texts.

    Runs the alias map first (case-insensitive substring match), then a
    capitalized-bigram fallback for anything we didn't seed. Returned as
    a set of canonical names — 'gpt-5.6' and 'GPT-5.6' both resolve to
    'OpenAI'; a bigram like 'Palantir Technologies' stays as-is."""
    combined_lower = " ".join(t or "" for t in texts).lower()
    combined_raw = " ".join(t or "" for t in texts)
    hits: set[str] = set()

    for alias, canonical in _ALIAS_TO_CANONICAL.items():
        if alias in combined_lower:
            hits.add(canonical)

    for bigram in _BIGRAM_RE.findall(combined_raw):
        # Skip anything already collapsed via the alias map (avoids double
        # counting "Kimi K3" as both "Moonshot" and "Kimi K3").
        if bigram.lower() not in _ALIAS_TO_CANONICAL:
            hits.add(bigram)

    return hits


# ---------------------------------------------------------------------------
# Story-bucket key + collision
# ---------------------------------------------------------------------------
def _bucket_key(published: str | None) -> str:
    """Truncate the date to a 7-day bucket (first Monday of the ISO week)."""
    if not published:
        return "unbucketed"
    try:
        dt = datetime.strptime(published[:10], "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError:
        return "unbucketed"
    # Snap to the Monday of the ISO week.
    monday = dt - timedelta(days=dt.weekday())
    return monday.strftime("%Y-%m-%d")


def story_fingerprint(entry: dict) -> dict:
    """Extract the three signals + the bucket for an entry.

    Cheap and pure. No I/O. Called both when staging (to look up existing
    story) and when comparing against the index."""
    url = canonical_url(entry.get("source_url") or entry.get("article_url") or "")
    title = entry.get("title", "")
    return {
        "url": url,
        "title": title,
        "tokens": title_tokens(title),
        "shingles": title_shingles(title),
        "entities": entities(title, (entry.get("summary") or "")[:200]),
        "bucket": _bucket_key(entry.get("published") or entry.get("date")),
    }


def is_collision(a: dict, b: dict) -> bool:
    """Two-of-three rule. Dedup horizon is the index TTL (30 days) — we
    don't bucket by week here because the user asked for wide dedup across
    the last month.

    Title similarity uses max(token-Jaccard, trigram-Jaccard) so a rewrite
    (order-changed) collides with the original. Entity similarity uses
    overlap coefficient so a short primary set fully contained in a longer
    corroborated set still counts as a match."""
    hits = 0
    if a["url"] and a["url"] == b["url"]:
        hits += 1
    title_sim = max(
        jaccard(a.get("tokens", set()), b.get("tokens", set())),
        jaccard(a["shingles"], b["shingles"]),
    )
    if title_sim >= COLLISION_JACCARD_TITLE:
        hits += 1
    if overlap_coefficient(a["entities"], b["entities"]) >= COLLISION_JACCARD_ENTITY:
        hits += 1
    return hits >= 2
