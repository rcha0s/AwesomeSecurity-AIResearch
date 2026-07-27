#!/usr/bin/env python3
"""
importance.py — Newsworthiness signal for the editorial review track.

The primary reviewer curates on *novelty* (is the idea new?). This module powers
a SEPARATE, additive track that asks a different question: of the findings the
novelty gate held back in REVIEW.md, which are worth surfacing anyway because
they are trending, widely reported, tied to a real-world event, and teachable?

It never touches the novelty gate or re-scores anything. It only ranks the
already-held `needs_review` items so the editorial agent (the LLM stage) reads
the most promising ones first, and so promotion has a defensible deterministic
floor. The score blends five signals, each answering one editorial question:

    trend momentum   0.30  "is it trending?"        (cluster it belongs to)
    corroboration    0.20  "is it widely reported?" (independent sources)
    real-world event 0.15  "is it in the news?"     (CVE / advisory / incident)
    relevance        0.20  "useful to the field?"   (analyst relevance score)
    recency          0.15  "right now?"             (newness decay)

Usage:
    python scripts/importance.py                 # print the ranked review queue
    python scripts/importance.py --topic ai-security --top 10
"""

from __future__ import annotations

import argparse
import re

import common as c

# Blend weights (sum to 1.0). Trending is weighted highest because "what the
# field is paying attention to right now" is the whole point of this track.
NEWS_WEIGHTS = {
    "trend": 0.30,
    "corroboration": 0.20,
    "event": 0.15,
    "relevance": 0.20,
    "recency": 0.15,
}
# Corroboration saturates quickly: 3 independent sources already means "widely
# reported", so we cap the scaled contribution there.
CORROBORATION_FULL = 3
# A momentum at/above this maps to a full trend signal (trends.json momentum is
# roughly count + recency-weighted, so double digits is already a live cluster).
MOMENTUM_FULL = 20.0
# Markers that a finding is a concrete, in-the-news event rather than a concept.
EVENT_RE = re.compile(r"\b(cve-\d{4}-\d+|ghsa-|advisory|zero-day|0-day|compromise|breach)\b", re.I)


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def trend_momentum_for(entry: dict, trend_index: dict[str, float]) -> float:
    """The momentum of the hottest trend cluster this entry belongs to (0-100).

    `trend_index` maps a normalized source URL -> the momentum of the cluster it
    appears in, precomputed once from trends.json (see build_trend_index)."""
    url = c.normalize_url(entry.get("source_url", "") or entry.get("article_url", ""))
    momentum = trend_index.get(url, 0.0)
    return _clamp(100.0 * momentum / MOMENTUM_FULL)


def corroboration_signal(entry: dict) -> float:
    n = len(entry.get("corroborating_sources") or [])
    return _clamp(100.0 * min(n, CORROBORATION_FULL) / CORROBORATION_FULL)


def event_signal(entry: dict) -> float:
    blob = f"{entry.get('title', '')} {entry.get('summary', '')} {entry.get('source_url', '')}"
    return 100.0 if EVENT_RE.search(blob) else 0.0


def newsworthiness(entry: dict, trend_index: dict[str, float], conf: c.Config) -> float:
    """Composite 0-100 newsworthiness for one held finding."""
    scores = entry.get("scores") or {}
    parts = {
        "trend": trend_momentum_for(entry, trend_index),
        "corroboration": corroboration_signal(entry),
        "event": event_signal(entry),
        "relevance": float(scores.get("relevance", 0) or 0),
        "recency": c.newness_score(c.best_date(entry) or "", conf.half_life_days),
    }
    total = sum(NEWS_WEIGHTS[k] * v for k, v in parts.items())
    return round(total, 2)


def newsworthiness_breakdown(entry: dict, trend_index: dict[str, float], conf: c.Config) -> dict:
    """The per-signal values behind the score — for the editorial agent + logs."""
    scores = entry.get("scores") or {}
    return {
        "trend": round(trend_momentum_for(entry, trend_index), 1),
        "corroboration": round(corroboration_signal(entry), 1),
        "event": event_signal(entry),
        "relevance": float(scores.get("relevance", 0) or 0),
        "recency": round(c.newness_score(c.best_date(entry) or "", conf.half_life_days), 1),
        "newsworthiness": newsworthiness(entry, trend_index, conf),
    }


def build_trend_index(trends: dict) -> dict[str, float]:
    """Map each trend member's normalized URL -> the max cluster momentum it's in."""
    index: dict[str, float] = {}
    for clusters in trends.values():
        for cluster in clusters:
            momentum = float(cluster.get("momentum", 0) or 0)
            for member in cluster.get("members", []):
                url = c.normalize_url(member.get("url", ""))
                if url:
                    index[url] = max(index.get(url, 0.0), momentum)
    return index


def held_items(topic: str, conf: c.Config) -> list[dict]:
    """The REVIEW.md queue for a topic: pool entries not in the curated view."""
    return [e for e in c.load_pool(topic)["entries"] if not c.is_curated(e, conf)]


def rank_review_queue(conf: c.Config, topic: str | None = None) -> list[tuple[dict, float]]:
    """Held findings across topics, sorted by newsworthiness (desc)."""
    trend_index = build_trend_index(c.load_json(c.DATA_DIR / "trends.json", default={}) or {})
    topics = [topic] if topic else list(c.TOPICS)
    ranked = [
        (entry, newsworthiness(entry, trend_index, conf))
        for t in topics
        for entry in held_items(t, conf)
    ]
    ranked.sort(key=lambda pair: -pair[1])
    return ranked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", choices=list(c.TOPICS))
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()
    conf = c.load_config()
    ranked = rank_review_queue(conf, args.topic)[: args.top]
    print(f"Review queue by newsworthiness (top {len(ranked)}):\n")
    for entry, score in ranked:
        print(f"  {score:5.1f}  [{entry.get('topic')}] {entry.get('title', '')[:72]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
