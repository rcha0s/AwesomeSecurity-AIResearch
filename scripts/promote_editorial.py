#!/usr/bin/env python3
"""
promote_editorial.py — Apply the editorial agent's decisions to the pools.

The editorial agent (the /editorial-review skill) reads the REVIEW.md queue and
writes data/editorial_out.json: the held findings it promotes, and (rarely) an
earlier promotion it takes back, each with a reason:

    [{"id": "...", "reason": "...", "signals": ["trending", "widely-reported"]},
     {"id": "...", "demote": true, "reason": "the story was retracted"}]

Promotions are sticky. News is kept like claims (Rohan, 2026-10-19), so a run
only adds promotions: an earlier one the agent doesn't list again stays. It
leaves only two ways, and each is reported:

  * an explicit demotion with a non-empty reason, on an entry that is promoted;
  * its integrity fails (c.integrity_lost: verifier-refuted or ungrounded).

For each promotion the entry is re-checked with editorial_eligible (held,
scored, grounded, not refuted), so the agent can never surface an ungrounded or
refuted item, whatever it wrote. Scores, novelty and needs_review are never
touched. Re-running is idempotent.

Every run appends what it did to data/_editorial_outcomes.md: code-owned (the
local session is Edit-denied it), and run_scan.sh post puts it in the PR body.

Usage:
    python scripts/promote_editorial.py
    python scripts/promote_editorial.py --dry-run
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field

import common as c

EDITORIAL_OUT = c.DATA_DIR / "editorial_out.json"
OUTCOMES_NAME = "_editorial_outcomes.md"
MAX_SIGNALS = 6


@dataclass
class Outcome:
    promoted: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    demoted: list[str] = field(default_factory=list)  # "title: reason"
    lost: list[str] = field(default_factory=list)  # "title: integrity reason"


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


def _title(entry: dict) -> str:
    return entry.get("title", "?")[:72]


def _demote(entry: dict | None, decision: dict, out: Outcome) -> None:
    reason = c.clean_summary(str(decision.get("reason") or ""), 240)
    if entry is None or not c.is_editorial(entry):
        out.skipped.append(f"{decision.get('id', '?')}: demotion of an entry that isn't promoted")
    elif not reason:
        out.skipped.append(f"{_title(entry)}: demotion without a reason; promotion kept")
    else:
        entry.pop("editorial", None)
        out.demoted.append(f"{_title(entry)}: {reason}")


def _promote(entry: dict | None, decision: dict, conf: c.Config, out: Outcome) -> None:
    if entry is None:
        out.skipped.append(f"{decision.get('id', '?')}: not found in any pool")
    elif c.is_editorial(entry):
        out.skipped.append(f"{_title(entry)}: already promoted; kept as it was")
    elif not c.editorial_eligible(entry, conf):
        out.skipped.append(f"{_title(entry)}: not eligible ({c.review_reason(entry, conf)})")
    else:
        _stamp(entry, decision)
        out.promoted.append(entry.get("title", "?"))


def _sweep_integrity(by_id: dict[str, dict], conf: c.Config, out: Outcome) -> None:
    """The one automatic removal: a promotion whose integrity facts failed."""
    for entry in by_id.values():
        if c.is_editorial(entry) and c.integrity_lost(entry):
            entry.pop("editorial", None)
            out.lost.append(f"{_title(entry)}: {c.review_reason(entry, conf)}")


def apply_decisions(decisions: list[dict], conf: c.Config) -> Outcome:
    pools = {t: c.load_pool(t) for t in c.TOPICS}
    by_id = _index_by_id(pools)
    out = Outcome()
    for decision in decisions:
        if not isinstance(decision, dict):
            out.skipped.append(f"{decision!r}: not an object")
            continue
        entry = by_id.get(decision.get("id", ""))
        if decision.get("demote") is True:
            _demote(entry, decision, out)
        else:
            _promote(entry, decision, conf, out)
    _sweep_integrity(by_id, conf, out)
    for topic, pool in pools.items():
        c.save_pool(topic, pool)
    return out


def outcomes_record(out: Outcome) -> str:
    """Markdown for the PR body. Removals are listed one by one: they are the
    only way a news story leaves the lane."""
    lines = [
        "### Editorial decisions (applied by promote_editorial.py)",
        "",
        f"{len(out.promoted)} promoted · {len(out.demoted)} demoted · "
        f"{len(out.lost)} removed for integrity · {len(out.skipped)} skipped. "
        "Earlier promotions not listed this run are kept.",
    ]
    lines += [f"- promoted: {t[:72]}" for t in out.promoted]
    lines += [f"- DEMOTED: {t}" for t in out.demoted]
    lines += [f"- REMOVED (integrity): {t}" for t in out.lost]
    return "\n".join(lines) + "\n"


def append_record(out: Outcome) -> None:
    path = c.DATA_DIR / OUTCOMES_NAME
    prior = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(prior + ("\n" if prior else "") + outcomes_record(out), encoding="utf-8")


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
        print(f"(dry run) {len(decisions)} decision(s) requested.")
        return 0

    out = apply_decisions(decisions, conf)
    append_record(out)
    print(
        f"Editorial: {len(out.promoted)} promoted, {len(out.demoted)} demoted, "
        f"{len(out.lost)} removed for integrity, {len(out.skipped)} skipped."
    )
    for title in out.promoted:
        print(f"  + {title[:72]}")
    for msg in out.skipped:
        print(f"  ~ {msg}")
    for msg in out.demoted:
        print(f"  - demoted: {msg}")
    for msg in out.lost:
        print(f"  - removed (integrity): {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
