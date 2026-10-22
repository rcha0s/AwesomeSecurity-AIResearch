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
    python scripts/add_claim.py correct some-claim --first-seen 2006-07-19 --domain ps.appsec
    python scripts/add_claim.py fix-evidence some-claim --url https://… --stance contests --note "…"
    python scripts/add_claim.py fix-evidence some-claim --url https://… --occurrence 2 --remove
    python scripts/add_claim.py list [--topic ai-research]
    python scripts/add_claim.py validate
"""

from __future__ import annotations

import argparse

import common as c
import taxonomy

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
    return c.utcnow().strftime("%Y-%m-%d")


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
    for key in ("title", "basis", "guidance", "scope"):
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
            (
                {
                    **claim,
                    "evidence": (claim.get("evidence") or []) + new_items,
                    "last_reviewed": today(),
                }
                if claim["id"] == args.id
                else claim
            )
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
            (
                {**claim, "status": args.set, "last_reviewed": today()}
                if claim["id"] == args.id
                else claim
            )
            for claim in ledger["claims"]
        ],
    }
    rc = save_validated(updated)
    if rc == 0:
        print(f"{args.id} is now {args.set}")
    return rc


# Fields `correct` may rewrite on a LIVE claim. A retired claim is the record of
# what we used to believe, so only its classification (domain) may change.
CORRECTABLE = (
    "statement",
    "title",
    "basis",
    "guidance",
    "scope",
    "confidence",
    "first_seen",
    "tags",
)


def _resolve_domain(claim: dict, label: str) -> str:
    """The taxonomy ID `label` names within the claim's topic (ID, alias or name)."""
    tax = taxonomy.get()
    did, how = taxonomy.resolve(tax, claim.get("topic") or "", label)
    if how not in ("id", "alias", "name"):
        raise ValueError(
            f"domain {label!r} is not a {claim.get('topic')} taxonomy ID, alias or name"
        )
    return did


def _corrections(args: argparse.Namespace) -> dict:
    changes = {f: getattr(args, f) for f in CORRECTABLE if getattr(args, f) is not None}
    if "tags" in changes:
        changes["tags"] = [t.strip() for t in changes["tags"].split(",") if t.strip()]
    return changes


def cmd_correct(args: argparse.Namespace) -> int:
    """Fix an inaccurate field on a claim, re-validating the whole ledger."""
    ledger = cl.load_ledger()
    claim = cl.claim_index(ledger["claims"]).get(args.id)
    if claim is None:
        print(f"unknown claim: {args.id}")
        return 1
    changes = _corrections(args)
    if changes and cl.is_retired(claim):
        print("a retired claim's history is frozen — only --domain may change on it")
        return 1
    if args.domain:
        try:
            changes["domain"] = _resolve_domain(claim, args.domain)
        except ValueError as exc:
            print(exc)
            return 1
    if not changes:
        print("nothing to correct")
        return 1
    if cl.is_live(claim):
        changes["last_reviewed"] = today()
    updated = {
        **ledger,
        "claims": [{**x, **changes} if x["id"] == args.id else x for x in ledger["claims"]],
    }
    rc = save_validated(updated)
    if rc == 0:
        print(f"corrected {args.id}: {', '.join(sorted(changes))}")
    return rc


def _evidence_edit(items: list[dict], args: argparse.Namespace) -> list[dict]:
    """Apply one fix-evidence edit; raises ValueError when the target is ambiguous."""
    hits = [i for i, e in enumerate(items) if e.get("url") == args.url]
    if not hits:
        raise ValueError(f"no evidence item with url {args.url}")
    if args.occurrence:
        if args.occurrence > len(hits):
            raise ValueError(f"only {len(hits)} item(s) carry that url")
        hits = [hits[args.occurrence - 1]]
    elif len(hits) > 1:
        raise ValueError(f"{len(hits)} items carry that url — pass --occurrence N")
    target = hits[0]
    if args.remove:
        return items[:target] + items[target + 1 :]
    item = dict(items[target])
    if args.stance:
        if args.stance not in cl.STANCES:
            raise ValueError(f"stance must be one of {cl.STANCES}")
        item["stance"] = args.stance
    for field, value in (
        ("url", args.new_url),
        ("title", args.title),
        ("published", args.published),
        ("note", args.note),
    ):
        if value is not None:
            item[field] = value
    return items[:target] + [item] + items[target + 1 :]


def cmd_fix_evidence(args: argparse.Namespace) -> int:
    """Correct (or drop) a mis-cited evidence item on a live claim."""
    ledger = cl.load_ledger()
    claim = cl.claim_index(ledger["claims"]).get(args.id)
    if claim is None:
        print(f"unknown claim: {args.id}")
        return 1
    if cl.is_retired(claim):
        print("a retired claim's evidence is frozen as the record of what was believed")
        return 1
    try:
        evidence = _evidence_edit(list(claim.get("evidence") or []), args)
    except ValueError as exc:
        print(exc)
        return 1
    updated = {
        **ledger,
        "claims": [
            {**x, "evidence": evidence, "last_reviewed": today()} if x["id"] == args.id else x
            for x in ledger["claims"]
        ],
    }
    rc = save_validated(updated)
    if rc == 0:
        print(f"{'removed' if args.remove else 'fixed'} evidence {args.url} on {args.id}")
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
    new.add_argument("--title", help="concise headline (~5-10 words) shown on the claim card")
    new.add_argument(
        "--basis",
        help="the method/evidence type that established this (e.g. 'benchmarked head-to-head')",
    )
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

    co = sub.add_parser(
        "correct", help="fix an inaccurate field (live claims; domain only on retired)"
    )
    co.add_argument("id")
    for field in ("statement", "title", "basis", "guidance", "scope", "tags"):
        co.add_argument(f"--{field}")
    co.add_argument("--confidence", type=float)
    co.add_argument("--first-seen", dest="first_seen", help="YYYY-MM[-DD]")
    co.add_argument("--domain", help="taxonomy ID (or an alias/name it resolves from)")
    co.set_defaults(func=cmd_correct)

    fe = sub.add_parser("fix-evidence", help="correct or remove a mis-cited source on a live claim")
    fe.add_argument("id")
    fe.add_argument("--url", required=True, help="the evidence item's current url")
    fe.add_argument("--occurrence", type=int, help="1-based, when several items share the url")
    fe.add_argument("--remove", action="store_true")
    fe.add_argument("--stance")
    fe.add_argument("--new-url", dest="new_url")
    fe.add_argument("--title")
    fe.add_argument("--published")
    fe.add_argument("--note")
    fe.set_defaults(func=cmd_fix_evidence)

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
