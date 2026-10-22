#!/usr/bin/env python3
"""
select_batch.py — Hand the scan's model session a batch sized to the run.

`run_scan.sh pre` runs this right after ingest. The session's budget is sized
for `limits.max_stories_per_run` analyzed stories, so the session must not see
the whole ingest (286 candidates on 2026-10-20: it judged the set too big for
its budget and analyzed nothing). This keeps the top
`max_stories_per_run + batch_margin` candidates in data/candidates.json, the
file the session reads. The margin covers batch members the story judge finds
to be `same`/`update` (they are not analyzed and don't count toward the cap).

Ranking reuses the existing signals, no new scorer:
1. prefilter.py's funnel: deny-list, excluded-term and pool/archive-duplicate
   hits never enter the batch; a `routed` candidate (confident taxonomy
   domain hint) ranks before a `filtered` (ambiguous) one;
2. then the composite formula over the two axes known before analysis,
   newness (decayed from the source date) and credibility (source registry
   rank), with config.yaml's weights;
3. then the candidate id, so the order is deterministic.

Everything not selected goes to data/_scan_backlog.json, each with its
prefilter reason and rank. The session can neither edit it (the containment
denies Edit(data/_scan*)) nor read it. It is a record for diagnosis, not a
queue: the next scan's ingest re-stages any candidate still fresh and still in
its feed, and it competes for that day's batch again.

Usage:
    python scripts/select_batch.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import common as c
import prefilter as pf

BACKLOG_NAME = "_scan_backlog.json"
DEFAULT_MARGIN = 4
_BUCKET_ORDER = {"routed": 0, "filtered": 1}


def backlog_file() -> Path:
    return c.DATA_DIR / BACKLOG_NAME


def batch_size(conf: c.Config) -> int:
    """Stories the run may analyze, plus the margin for same/update verdicts."""
    cap = int(conf.limits.get("max_stories_per_run", 8))
    margin = int(conf.limits.get("batch_margin", DEFAULT_MARGIN))
    return max(0, cap) + max(0, margin)


def pre_analysis_score(cand: dict, conf: c.Config) -> float:
    """The composite over the axes known before analysis: newness + credibility."""
    scores = {
        "newness": c.newness_score(c.best_date(cand) or "", conf.half_life_days),
        "credibility": c.credibility_of(cand),
    }
    return c.composite_score(scores, conf.weights)


def rank(cands: list[dict], conf: c.Config) -> list[dict]:
    def key(cand: dict) -> tuple:
        bucket = _BUCKET_ORDER.get((cand.get("prefilter") or {}).get("reason"), 2)
        return (bucket, -pre_analysis_score(cand, conf), str(cand.get("id") or ""))

    return sorted(cands, key=key)


def select(
    candidates: list[dict], conf: c.Config, table: pf.KeywordTable
) -> tuple[list[dict], list[dict]]:
    """Split staged candidates into (batch, backlog)."""
    sorted_ = pf.bucket(candidates, table)
    ranked = rank(sorted_.routed + sorted_.filtered, conf)
    size = batch_size(conf)
    backlog = [{**cand, "batch_rank": i} for i, cand in enumerate(ranked[size:], start=size + 1)]
    return ranked[:size], backlog + sorted_.dropped


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
    return 0


if __name__ == "__main__":
    sys.exit(main())
