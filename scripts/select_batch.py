#!/usr/bin/env python3
"""
select_batch.py — Hand the scan's model session a batch sized to the run.

`run_scan.sh pre` runs this right after ingest. The session's budget is sized
for `limits.max_stories_per_run` analyzed stories, so the session must not see
the whole ingest (286 candidates on 2026-10-20: it judged the set too big for
its budget and analyzed nothing). This keeps
`max_stories_per_run + batch_margin` candidates in data/candidates.json, the
file the session reads. The margin covers batch members the story judge finds
to be `same`/`update` (they are not analyzed and don't count toward the cap).

Scoring reuses the existing signals, no new scorer: the composite formula over
the two axes known before analysis, newness (decayed from the source date) and
credibility (source registry rank), with config.yaml's weights, plus a small
`batch_routed_bonus` when prefilter.py routed the candidate to a domain.
Routing measures taxonomy confidence, not newsworthiness, so it only nudges.
prefilter.py's deny-list, excluded-term and pool/archive-duplicate hits never
enter the batch.

Fairness: one source class would otherwise take every slot (on 2026-10-20 a
pure score order gave six GHSA advisories and no KEV, HN or Simon Willison).
Slots are dealt round-robin across ingestor classes (KEV, HN, GHSA, GitHub
search, HF papers, conference papers, research sitemaps, RSS feeds), best
class first, each class giving its best remaining candidate, and no single
source takes more than `batch_per_source` slots unless nothing else is left.
Curator links (ingest_curator_links.py, `curator:` source ids) are their own
class, and `batch_class_min` reserves each named class a floor of slots right
after the must-not-miss lane: a curator link carries the issue's date, so its
newness can sink it under fresher feeds, and the per-source cap (all curator
links share one source) holds it to `batch_per_source`. With a floor of 1 and
a cap of 2, each batch gets one or two.

`batch_class_slots` lets a class deal more than one candidate per round: plain
RSS feeds are one class of 60+ feeds and a third of the staged set, and the
research posts the recall eval misses most come from them.

Must-not-miss lane: the recall eval scores every new CISA KEV entry and every
critical GHSA advisory, and on 2026-W43 held 0 of 19. Before the deal, up to
`batch_priority_max` slots go to those classes (and to high-severity GHSA
advisories in AI tooling), AI-tooling advisories first, at most
`batch_priority_per_source` from one source. Each carries `batch_priority`
so the session analyzes it before the cap runs out.

Everything not selected goes to data/_scan_backlog.json, each with its
prefilter reason and rank. On the Mac runner the session can neither edit nor
read it (scan_containment.sh denies both); the cloud routine has no per-tool
scoping, so there it is only a convention. It is a record for diagnosis, not a
queue: the next scan's ingest re-stages any candidate still fresh and still in
its feed, and it competes for that day's batch again.

Usage:
    python scripts/select_batch.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import common as c
import prefilter as pf

BACKLOG_NAME = "_scan_backlog.json"
DEFAULTS = {
    "batch_margin": 4,
    "batch_per_source": 2,
    "batch_routed_bonus": 5.0,
    "batch_priority_max": 0,  # off unless config.yaml names a lane size
    "batch_priority_per_source": 2,
}
# source_id prefixes that name their own ingestor; plain `rss:` feeds share one class.
OWN_CLASS = ("kev_json", "hf_papers", "research_index", "github_query", "sitemap", "curator")


def backlog_file() -> Path:
    return c.DATA_DIR / BACKLOG_NAME


def setting(conf: c.Config, key: str) -> float:
    return conf.limits.get(key, DEFAULTS[key])


def batch_size(conf: c.Config) -> int:
    """Stories the run may analyze, plus the margin for same/update verdicts."""
    cap = int(conf.limits.get("max_stories_per_run", 8))
    return max(0, cap) + max(0, int(setting(conf, "batch_margin")))


def source_key(cand: dict) -> str:
    """The source a candidate came from (registry id, else ingestor + type)."""
    return cand.get("source_id") or f"{cand.get('discovered_via')}:{cand.get('source_type')}"


def ingestor_class(cand: dict) -> str:
    sid = cand.get("source_id") or ""
    prefix = sid.split(":", 1)[0]
    if prefix in OWN_CLASS:
        return prefix
    return str(cand.get("discovered_via")) if sid else source_key(cand)


def score(cand: dict, conf: c.Config) -> float:
    """Composite over the axes known before analysis, plus the routing nudge."""
    axes = {
        "newness": c.newness_score(c.best_date(cand) or "", conf.half_life_days),
        "credibility": c.credibility_of(cand),
    }
    routed = (cand.get("prefilter") or {}).get("reason") == "routed"
    return c.composite_score(axes, conf.weights) + (
        float(setting(conf, "batch_routed_bonus")) if routed else 0.0
    )


def deal(
    ranked: list[dict],
    size: int,
    per_source: int,
    slots: dict[str, int] | None = None,
    used: Counter | None = None,
    fill: bool = True,
) -> list[dict]:
    """Round-robin over ingestor classes (best head first), `slots[class]`
    picks per round (default 1), per-source capped; then (`fill`) fill any
    slots left by score alone. `ranked` is best-first; `used` counts slots
    already taken."""
    queues: dict[str, list[dict]] = {}
    for cand in ranked:
        queues.setdefault(ingestor_class(cand), []).append(cand)
    pos = {id(x): i for i, x in enumerate(ranked)}
    taken: list[dict] = []
    used = Counter(used or {})
    while len(taken) < size:
        dealt = False
        for cls in sorted(queues, key=lambda k: pos[id(queues[k][0])] if queues[k] else len(pos)):
            for _ in range(max(1, int((slots or {}).get(cls, 1)))):
                pick = next((x for x in queues[cls] if used[source_key(x)] < per_source), None)
                if pick is None or len(taken) >= size:
                    break
                queues[cls].remove(pick)
                used[source_key(pick)] += 1
                taken.append(pick)
                dealt = True
        if not dealt:
            break
    if not fill:
        return taken
    ids = {id(x) for x in taken}
    return taken + [x for x in ranked if id(x) not in ids][: size - len(taken)]


def priority_class(cand: dict) -> str | None:
    """The must-not-miss class a candidate belongs to, else None."""
    if (cand.get("source_id") or "").startswith("kev_json:"):
        return "kev"
    if cand.get("source_type") != "GHSA":
        return None
    severity = str(cand.get("severity") or "").upper()
    if severity == "CRITICAL":
        return "ghsa-critical"
    if severity == "HIGH" and is_ai_tooling(cand):
        return "ghsa-ai"
    return None


def is_ai_tooling(cand: dict) -> bool:
    """Prefilter routed it to an AI-security domain on the taxonomy's own hints.
    Not the ingest-time topic guess: that is a keyword match on package names."""
    return str((cand.get("prefilter") or {}).get("domain_hint") or "").startswith("ais.")


def priority_lane(ranked: list[dict], limit: int, per_source: int) -> list[dict]:
    """Up to `limit` must-not-miss candidates, dealt in turn between KEV and
    GHSA, at most `per_source` from either. Within GHSA: critical advisories in
    AI tooling, then the other critical ones, then high ones in AI tooling, so
    a HIGH can never take a critical's slot. Otherwise rank (newest) order."""
    eligible = sorted((x for x in ranked if priority_class(x)), key=lane_order)  # stable
    return deal(eligible, limit, per_source, fill=False)


def class_floor(
    ranked: list[dict], mins: dict[str, int], room: int, per_source: int, used: Counter
) -> list[dict]:
    """The best `mins[class]` candidates of each named class, before the deal, so a
    class whose heads score low (curator links carry the issue's date, not the
    article's) still reaches the batch. Per-source capped like the deal."""
    out: list[dict] = []
    for cls in sorted(mins):
        pool = [x for x in ranked if ingestor_class(x) == cls]
        limit = min(max(0, int(mins[cls])), room - len(out))
        out += deal(pool, limit, per_source, used=used + Counter(map(source_key, out)), fill=False)
    return out


def lane_order(cand: dict) -> int:
    kind = priority_class(cand)
    if kind == "ghsa-critical" and is_ai_tooling(cand):
        return 0
    return 2 if kind == "ghsa-ai" else 1


def select(
    candidates: list[dict], conf: c.Config, table: pf.KeywordTable
) -> tuple[list[dict], list[dict]]:
    """Split staged candidates into (batch, backlog)."""
    buckets = pf.bucket(candidates, table)
    ranked = sorted(
        buckets.routed + buckets.filtered,
        key=lambda x: (-score(x, conf), str(x.get("id") or "")),
    )
    size = batch_size(conf)
    lane_max = min(size, max(0, int(setting(conf, "batch_priority_max"))))
    lane = priority_lane(ranked, lane_max, max(1, int(setting(conf, "batch_priority_per_source"))))
    per_source = max(1, int(setting(conf, "batch_per_source")))
    mins = conf.limits.get("batch_class_min") or {}
    lane_ids = {id(x) for x in lane}
    floor = class_floor(
        [x for x in ranked if id(x) not in lane_ids], mins, size - len(lane),
        per_source, Counter(source_key(x) for x in lane),
    )  # fmt: skip
    in_lane = {id(x) for x in lane + floor}
    slots = conf.limits.get("batch_class_slots") or {}
    used = Counter(source_key(x) for x in lane + floor)
    dealt = deal(
        [x for x in ranked if id(x) not in in_lane],
        size - len(lane) - len(floor), per_source, slots, used,
    )  # fmt: skip
    ids = in_lane | {id(x) for x in dealt}
    rest = [x for x in ranked if id(x) not in ids]
    batch = [{**x, "batch_priority": priority_class(x)} for x in lane] + floor + dealt
    backlog = [{**x, "batch_rank": i} for i, x in enumerate(rest, start=len(batch) + 1)]
    return batch, backlog + buckets.dropped


def composition(batch: list[dict]) -> str:
    counts = Counter(source_key(x) for x in batch)
    return ", ".join(f"{k} x{n}" for k, n in counts.most_common())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(c.CONFIG_FILE))
    args = parser.parse_args(argv)
    conf = c.load_config(Path(args.config))
    candidates = c.load_candidates()
    batch, backlog = select(candidates, conf, pf.load_keywords())
    c.save_candidates(batch)
    c.save_json(backlog_file(), backlog)
    dropped = sum(1 for b in backlog if "batch_rank" not in b)
    print(
        f"SCAN_BATCH: {len(batch)} of {len(candidates)} candidates selected "
        f"(batch size {batch_size(conf)}); {len(backlog) - dropped} below the cut and "
        f"{dropped} prefilter-dropped -> data/{BACKLOG_NAME}"
    )
    print(f"SCAN_BATCH sources: {composition(batch)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
