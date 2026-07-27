#!/usr/bin/env python3
"""
add_claim.py — Write to the claim ledger (data/claims.json) safely.

Every mutation re-validates the whole ledger before saving, so a bad edge or a
half-finished supersession can never land on disk.

Evidence is given as pipe-delimited fields, repeatable:

    --evidence "stance|url|title|published"      # title/published optional

Usage:
    # a new standing answer
    python scripts/add_claim.py new toon-over-json-for-agent-io \\
        --topic ai-research --domain "Architecture & Optimization" \\
        --statement "TOON encoding cuts agent I/O tokens 30-60% vs JSON at equal fidelity." \\
        --guidance "Use TOON for large uniform arrays in tool output; keep JSON when nested." \\
        --confidence 0.8 --tags tokens,serialization \\
        --evidence "supports|https://arxiv.org/abs/...|TOON paper|2026-06-01"

    # retire an old answer in favour of a new one (writes both ends of the edge)
    python scripts/add_claim.py supersede grep-is-enough code-graph-beats-grep \\
        --reason "Lexical search misses cross-file call relationships."

    # …or mark it outright wrong rather than merely replaced
    python scripts/add_claim.py supersede old-claim new-claim --reason "…" --refuted

    python scripts/add_claim.py evidence some-claim --evidence "contests|https://…|Rebuttal"
    python scripts/add_claim.py status some-claim --set contested
    python scripts/add_claim.py list [--topic ai-research]
    python scripts/add_claim.py validate
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime

import common as c

import claims as cl


def parse_evidence(specs: list[str] | None) -> list[dict]:
    """'stance|url|title|published' -> evidence dicts. Title/published optional."""
    evidence: list[dict] = []
    for spec in specs or []:
        parts = [p.strip() for p in spec.split("|")]
        if len(parts) < 2:
            raise SystemExit(f"--evidence needs at least 'stance|url' (got {spec!r})")
        stance, url = parts[0], parts[1]
        if stance not in cl.STANCES:
            raise SystemExit(f"stance must be one of {cl.STANCES} (got {stance!r})")
        item = {"stance": stance, "url": url}
        if len(parts) > 2 and parts[2]:
            item["title"] = parts[2]
        if len(parts) > 3 and parts[3]:
            item["published"] = parts[3]
        evidence.append(item)
    return evidence


def today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def save_validated(ledger: dict) -> int:
    """Persist only if the whole ledger still holds together."""
    errors = cl.validate_ledger(ledger)
    if errors:
        print(f"refusing to save — {len(errors)} validation problem(s):")
        for error in errors[:20]:
            print(f"  - {error}")
        return 1
    cl.save_ledger(ledger)
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    claim = {
        "id": args.id,
        "topic": args.topic,
        "domain": args.domain or "",
        "statement": args.statement,
        "status": args.status,
        "confidence": args.confidence,
        "evidence": parse_evidence(args.evidence),
        "first_seen": args.first_seen or today(),
        "last_reviewed": today(),
    }
    for key in ("guidance", "scope"):
        if getattr(args, key):
            claim[key] = getattr(args, key)
    if args.tags:
        claim["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]

    try:
        ledger = cl.add_claim(cl.load_ledger(), claim)
    except ValueError as exc:
        print(exc)
        return 1
    rc = save_validated(ledger)
    if rc == 0:
        print(f"added claim {args.id} ({args.status}) to {args.topic}")
    return rc


def cmd_supersede(args: argparse.Namespace) -> int:
    try:
        ledger = cl.supersede(
            cl.load_ledger(),
            old_id=args.old_id,
            new_id=args.new_id,
            reason=args.reason,
            date=args.date or today(),
            status="refuted" if args.refuted else "superseded",
        )
    except KeyError as exc:
        print(f"unknown claim: {exc}")
        return 1
    rc = save_validated(ledger)
    if rc == 0:
        verb = "refuted" if args.refuted else "superseded"
        print(f"{args.old_id} is now {verb}, replaced by {args.new_id}")
    return rc


def cmd_evidence(args: argparse.Namespace) -> int:
    ledger = cl.load_ledger()
    index = cl.claim_index(ledger["claims"])
    if args.id not in index:
        print(f"unknown claim: {args.id}")
        return 1
    new_items = parse_evidence(args.evidence)
    updated = {
        **ledger,
        "claims": [
            {
                **claim,
                "evidence": (claim.get("evidence") or []) + new_items,
                "last_reviewed": today(),
            }
            if claim["id"] == args.id
            else claim
            for claim in ledger["claims"]
        ],
    }
    rc = save_validated(updated)
    if rc == 0:
        print(f"added {len(new_items)} source(s) to {args.id}")
    return rc


def cmd_status(args: argparse.Namespace) -> int:
    if args.set in cl.RETIRED_STATUSES:
        print(f"use `supersede` to set {args.set} — it needs a successor, reason, and date")
        return 1
    ledger = cl.load_ledger()
    if args.id not in cl.claim_index(ledger["claims"]):
        print(f"unknown claim: {args.id}")
        return 1
    updated = {
        **ledger,
        "claims": [
            {**claim, "status": args.set, "last_reviewed": today()}
            if claim["id"] == args.id
            else claim
            for claim in ledger["claims"]
        ],
    }
    rc = save_validated(updated)
    if rc == 0:
        print(f"{args.id} is now {args.set}")
    return rc


def cmd_list(args: argparse.Namespace) -> int:
    ledger = cl.load_ledger()
    topics = [args.topic] if args.topic else list(c.TOPICS)
    for topic in topics:
        topic_claims = cl.claims_for_topic(ledger, topic)
        print(f"\n{c.TOPICS[topic]['name']} ({len(topic_claims)})")
        for claim in topic_claims:
            mark = "  " if cl.is_live(claim) else "x "
            print(f"  {mark}[{claim.get('status'):10}] {claim['id']}  {claim['statement'][:70]}")
    return 0


def cmd_validate(_args: argparse.Namespace) -> int:
    errors = cl.validate_ledger(cl.load_ledger())
    if not errors:
        print(f"claim ledger OK — {len(cl.all_claims(cl.load_ledger()))} claims")
        return 0
    print(f"{len(errors)} problem(s):")
    for error in errors:
        print(f"  - {error}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    new = sub.add_parser("new", help="add a new claim")
    new.add_argument("id", help="kebab-case stable id")
    new.add_argument("--topic", required=True, choices=list(c.TOPICS))
    new.add_argument("--statement", required=True, help="the claim, as one sentence")
    new.add_argument("--domain", default="")
    new.add_argument("--guidance", help="what a practitioner should DO about it")
    new.add_argument("--scope", help="boundary conditions / where it does not apply")
    new.add_argument("--status", default="current", choices=list(cl.LIVE_STATUSES))
    new.add_argument("--confidence", type=float, default=cl.DEFAULT_CONFIDENCE)
    new.add_argument("--tags", help="comma-separated")
    new.add_argument("--first-seen", dest="first_seen", help="YYYY-MM-DD (default: today)")
    new.add_argument("--evidence", action="append", help="'stance|url|title|published'")
    new.set_defaults(func=cmd_new)

    sup = sub.add_parser("supersede", help="retire a claim in favour of another")
    sup.add_argument("old_id")
    sup.add_argument("new_id")
    sup.add_argument("--reason", required=True, help="why the old answer no longer holds")
    sup.add_argument("--date", help="YYYY-MM-DD (default: today)")
    sup.add_argument("--refuted", action="store_true", help="wrong, not merely replaced")
    sup.set_defaults(func=cmd_supersede)

    ev = sub.add_parser("evidence", help="attach sources to an existing claim")
    ev.add_argument("id")
    ev.add_argument("--evidence", action="append", required=True)
    ev.set_defaults(func=cmd_evidence)

    st = sub.add_parser("status", help="move a claim between live statuses")
    st.add_argument("id")
    st.add_argument("--set", required=True, choices=list(cl.LIVE_STATUSES))
    st.set_defaults(func=cmd_status)

    ls = sub.add_parser("list", help="list claims")
    ls.add_argument("--topic", choices=list(c.TOPICS))
    ls.set_defaults(func=cmd_list)

    sub.add_parser("validate", help="check the ledger's integrity").set_defaults(func=cmd_validate)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
