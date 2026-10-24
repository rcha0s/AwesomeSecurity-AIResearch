#!/usr/bin/env python3
"""
eval_readability.py — Share of published briefs that read clearly on first pass.

Deterministic, no network. Every story the site shows (docs/index.html's data
block, joined back to its pool entry, as eval_integrity.py does) is scored by
scripts/readability.py. It reports the share that pass with no issue, the
share with mild issues only, and the share that would be held.

Listed under `automerge.evals` as optional: it fails only when the pass share
is below `readability.eval_min_pass` (0 = report only, today's setting).

Usage:
    python scripts/eval_readability.py            # summary line
    python scripts/eval_readability.py --verbose  # every brief with an issue
Exit 0 = pass, 1 = below the floor or could not run.
"""

from __future__ import annotations

import argparse

import common as c
import eval_integrity as ei
import eval_lib as el
import readability as rd


def published_entries(page: str | None = None) -> list[dict]:
    """The pool entry behind every story the site renders (unknown ids skipped:
    eval_integrity.py reports those)."""
    page = page if page is not None else (c.ROOT / ei.SITE).read_text(encoding="utf-8")
    pools, _ = ei.load_entries()
    by_id = {e.get("id"): e for _, e in pools}
    rows = ei.site_rows(ei.site_payload(page))
    ids = list(dict.fromkeys(row.get("id") for _, row in rows))
    return [by_id[i] for i in ids if i in by_id]


def run(page: str | None = None, cfg: dict | None = None) -> dict:
    cfg = cfg or rd.settings()
    results = [(e, rd.check(e, cfg)) for e in published_entries(page)]
    n = len(results)
    passed = sum(r["passed"] for _, r in results)
    held = sum(r["hold"] for _, r in results)
    share = round(passed / n, 3) if n else 1.0
    return {
        "published": n,
        "pass_share": share,
        "mild": n - passed - held,
        "would_hold": held,
        "mean_score": round(sum(r["score"] for _, r in results) / n, 1) if n else 100.0,
        "passed": share >= float(cfg.get("eval_min_pass") or 0),
        "flagged": [(e.get("id"), r) for e, r in results if not r["passed"]],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--verbose", action="store_true", help="list every brief with an issue")
    args = ap.parse_args(argv)
    try:
        report = run()
    except (OSError, ValueError) as exc:
        print(f"PROBLEM could not run: {type(exc).__name__}: {exc}")
        print(el.summary_line("readability", False, published=0))
        return 1
    for eid, r in report["flagged"] if args.verbose else []:
        print(f"{'HOLD' if r['hold'] else 'MILD'} [{r['score']}] {eid}")
        for i in r["issues"]:
            print(f"    {i['level']}: {i['detail']}")
    print(
        el.summary_line(
            "readability",
            report["passed"],
            published=report["published"],
            pass_share=report["pass_share"],
            mild=report["mild"],
            would_hold=report["would_hold"],
            mean_score=report["mean_score"],
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
