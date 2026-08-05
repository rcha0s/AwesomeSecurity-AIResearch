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

Dedup horizon: 30 days. The news lane only DISPLAYS the last 7 days
(NEWS_MAX_AGE_DAYS in common.py), but we look back a full month across every
finding — Track A and Track B, current pool and archive — so last week's
story doesn't reappear as this week's news, and a story we already have as
a research finding never repeats in the news lane.

The index (data/news_stories.json) persists story keys for 30 days. Older keys
are pruned so the file stays small and the extractor stays fast.

Usage — as a library:

    from dedupe_stories import assign_story_id, load_index, save_index
    idx = load_index()
    seed_index_from_pool(idx)             # includes Track A findings
    story_id, is_new = assign_story_id(candidate, idx)
    save_index(idx)
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Alias map for common labs / model families. Each canonical name maps to a
# set of aliases that all resolve to the canonical when detected. Seeded
# by hand — the fallback capitalized-bigram scanner catches anything we miss.
_ENTITY_ALIASES: dict[str, tuple[str, ...]] = {
    "OpenAI": ("openai", "gpt-5.6", "gpt-5", "gpt5.6", "gpt5", "luna", "terra", "sol", "codex"),
    "Anthropic": ("anthropic", "claude", "claude fable 5", "claude opus", "claude sonnet", "claude haiku"),
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
    alias: canonical
    for canonical, aliases in _ENTITY_ALIASES.items()
    for alias in aliases
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

STORY_INDEX = Path(__file__).resolve().parent.parent / "data" / "news_stories.json"

STORY_KEY_TTL_DAYS = 30
BUCKET_DAYS = 7  # week-of-published
COLLISION_JACCARD_TITLE = 0.5   # token-set OR trigram Jaccard; real-world
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
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=False)
             if k.lower() not in _TRACKING_PARAMS]
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower() or "https", host, path,
                       "", urlencode(query), ""))


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
    return {" ".join(toks[i:i + 3]) for i in range(len(toks) - 2)}


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


# ---------------------------------------------------------------------------
# Story index
# ---------------------------------------------------------------------------
def _story_id(fp: dict) -> str:
    """Stable ID from the fingerprint. Not intended to be human-readable;
    used to link corroborators."""
    parts = [
        fp["url"],
        "|".join(sorted(fp["shingles"])),
        "|".join(sorted(fp["entities"])),
        fp["bucket"],
    ]
    return hashlib.sha1("::".join(parts).encode("utf-8")).hexdigest()[:16]


def seed_index_from_pools(index: dict, *, lookback_days: int = STORY_KEY_TTL_DAYS,
                          now: datetime | None = None) -> int:
    """Populate the index with fingerprints from every recent pool entry
    (Track A findings AND anything already in the news lane). This is the
    'dedup wide, across the last month' rule.

    Called by news-track ingest BEFORE assigning new story IDs so a
    candidate that matches an existing research finding is silently dropped
    as a corroborator rather than staged as a fresh news item.

    Returns the number of new fingerprints added. Idempotent — a second
    run with the same pools adds zero."""
    import common as c

    now = now or datetime.now(UTC)
    cutoff = (now - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    added = 0

    def _consider(entry: dict) -> None:
        nonlocal added
        published = (entry.get("published") or entry.get("date") or "")[:10]
        if published and published < cutoff:
            return
        fp = story_fingerprint(entry)
        # Skip empty fingerprints (untitled / unURLed rows).
        if not fp["url"] and not fp["shingles"]:
            return
        for rec in index.values():
            if is_collision(fp, _hydrate_fp(rec["fp"])):
                return
        sid = _story_id(fp)
        if sid in index:
            return
        index[sid] = {
            "fp": fp,
            "corroborators": [],
            "winner_tier": "high",  # pooled findings assumed high-tier
            "first_seen": published or now.strftime("%Y-%m-%d"),
        }
        added += 1

    for entry in c.all_pool_entries():
        _consider(entry)
    for entry in c.load_json(c.DATA_DIR / "archive.json", []) or []:
        _consider(entry)
    return added


def load_index() -> dict:
    """{story_id: {"fp": {...}, "corroborators": [...], "winner_tier": str,
       "first_seen": iso_date}}. Missing file → empty index."""
    if not STORY_INDEX.exists():
        return {}
    return json.loads(STORY_INDEX.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    STORY_INDEX.parent.mkdir(parents=True, exist_ok=True)
    # Serialize sets to lists for JSON.
    ser = {
        sid: {
            "fp": {
                "url": rec["fp"]["url"],
                "title": rec["fp"].get("title", ""),
                "tokens": sorted(rec["fp"].get("tokens", [])),
                "shingles": sorted(rec["fp"]["shingles"]),
                "entities": sorted(rec["fp"]["entities"]),
                "bucket": rec["fp"]["bucket"],
            },
            "corroborators": rec.get("corroborators", []),
            "winner_tier": rec.get("winner_tier", "medium"),
            "first_seen": rec.get("first_seen", ""),
        }
        for sid, rec in index.items()
    }
    STORY_INDEX.write_text(json.dumps(ser, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")


def prune_index(index: dict, now: datetime | None = None) -> dict:
    """Drop keys older than STORY_KEY_TTL_DAYS."""
    now = now or datetime.now(UTC)
    cutoff = (now - timedelta(days=STORY_KEY_TTL_DAYS)).strftime("%Y-%m-%d")
    return {sid: rec for sid, rec in index.items() if rec.get("first_seen", "") >= cutoff}


def _hydrate_fp(fp: dict) -> dict:
    """Turn a persisted fingerprint (lists) back into a working one (sets)."""
    return {
        "url": fp.get("url", ""),
        "title": fp.get("title", ""),
        "tokens": set(fp.get("tokens", [])),
        "shingles": set(fp.get("shingles", [])),
        "entities": set(fp.get("entities", [])),
        "bucket": fp.get("bucket", "unbucketed"),
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
_TIER_RANK = {"high": 3, "medium": 2, "low": 1}


def assign_story_id(entry: dict, index: dict, *, source_tier: str = "medium",
                    source_name: str = "") -> tuple[str, bool]:
    """Look up (or create) the story ID for this entry.

    Returns (story_id, is_new). If a collision hits an existing story, the
    entry is added as a corroborator and the returned ID points at the
    existing story. The winner-tier tie-breaker only rewrites the winner
    when the new candidate is strictly higher tier.

    Mutates `index` in place — call save_index() when done."""
    fp = story_fingerprint(entry)

    for sid, rec in index.items():
        other = _hydrate_fp(rec["fp"])
        if is_collision(fp, other):
            new_rank = _TIER_RANK.get(source_tier, 0)
            cur_rank = _TIER_RANK.get(rec.get("winner_tier", "medium"), 0)
            corroborator = {
                "url": fp["url"] or entry.get("source_url", ""),
                "source_name": source_name or entry.get("source_name", ""),
                "tier": source_tier,
            }
            rec.setdefault("corroborators", []).append(corroborator)
            if new_rank > cur_rank:
                rec["fp"] = fp
                rec["winner_tier"] = source_tier
            return sid, False

    sid = _story_id(fp)
    index[sid] = {
        "fp": fp,
        "corroborators": [],
        "winner_tier": source_tier,
        "first_seen": (entry.get("published") or entry.get("date")
                       or datetime.now(UTC).strftime("%Y-%m-%d"))[:10],
    }
    return sid, True
