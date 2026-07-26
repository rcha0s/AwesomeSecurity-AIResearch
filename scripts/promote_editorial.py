#!/usr/bin/env python3
"""
promote_editorial.py — Apply the editorial agent's promotions to the pools.

The editorial agent (the /editorial-review skill) reads the REVIEW.md queue and
writes data/editorial_out.json — a list of the held findings it judges worth
surfacing for being trending / newsworthy / in the news, each with a rationale:

    [{"id": "...", "reason": "...", "signals": ["trending", "widely-reported"]}]

This script is the deterministic half. For each promoted id it:
  * finds the pool entry,
  * re-checks it is editorial_eligible (held, scored, grounded, not refuted) —
    so the agent can never surface an ungrounded or verifier-refuted item, no
    matter what it wrote,
  * stamps entry["editorial"] = {promoted, reason, signals, at}.

It never edits scores, novelty, or needs_review — it does not override the
novelty reviewer. Re-running is idempotent. An id that no longer qualifies is
skipped with a warning (and any stale promotion on it is cleared).

Usage:
    python scripts/promote_editorial.py
    python scripts/promote_editorial.py --dry-run
"""

from __future__ import annotations

import argparse

import common as c

EDITORIAL_OUT = c.DATA_DIR / "editorial_out.json"
MAX_SIGNALS = 6


def _index_by_id(pools: dict) -> dict[str, dict]:
    return {e["id"]: e for pool in pools.values() for e in pool["entries"] if e.get("id")}


def _stamp(entry: dict, decision: dict) -> None:
    signals = [str(s) for s in (decision.get("signals") or [])][:MAX_SIGNALS]
    entry["editorial"] = {
        "promoted": True,
        "reason": c.clean_summary(decision.get("reason", ""), 240),
        "signals": signals,
        "at": c.utcnow_iso(),
    }


def apply_promotions(
    decisions: list[dict], conf: c.Config
) -> tuple[list[str], list[str], list[str]]:
    """Returns (promoted_titles, skipped_msgs, cleared_titles)."""
    pools = {t: c.load_pool(t) for t in c.TOPICS}
    by_id = _index_by_id(pools)
    wanted = {d["id"] for d in decisions if d.get("id")}

    promoted: list[str] = []
    skipped: list[str] = []
    for decision in decisions:
        entry = by_id.get(decision.get("id", ""))
        if entry is None:
            skipped.append(f"{decision.get('id', '?')}: not found in any pool")
            continue
        if not c.editorial_eligible(entry, conf):
            skipped.append(
                f"{entry.get('title', '?')[:50]}: not eligible ({c.review_reason(entry, conf)})"
            )
            entry.pop("editorial", None)  # clear any stale promotion
            continue
        _stamp(entry, decision)
        promoted.append(entry.get("title", "?"))

    # Drop promotions the agent no longer lists (it reconsidered / item aged out).
    cleared: list[str] = []
    for entry in by_id.values():
        if c.is_editorial(entry) and entry["id"] not in wanted:
            entry.pop("editorial", None)
            cleared.append(entry.get("title", "?"))

    for topic, pool in pools.items():
        c.save_pool(topic, pool)
    return promoted, skipped, cleared


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report without writing pools")
    args = ap.parse_args()

    conf = c.load_config()
    decisions = c.load_json(EDITORIAL_OUT, default=[]) or []
    if not isinstance(decisions, list):
        print("editorial_out.json is not a list; nothing to do.")
        return 1
    if args.dry_run:
        ranked = {e["id"]: True for e in decisions if e.get("id")}
        print(f"(dry run) {len(ranked)} promotion(s) requested.")
        return 0

    promoted, skipped, cleared = apply_promotions(decisions, conf)
    print(f"Editorial: {len(promoted)} promoted, {len(skipped)} skipped, {len(cleared)} cleared.")
    for title in promoted:
        print(f"  + {title[:72]}")
    for msg in skipped:
        print(f"  ~ {msg}")
    for title in cleared:
        print(f"  - de-promoted (no longer listed): {title[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
