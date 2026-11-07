#!/usr/bin/env python3
"""
watchdog.py — what the daily scan should have done by now and didn't (2026-11-07).

Runs in GitHub Actions (.github/workflows/watchdog.yml), so it still reports when the
Mac is asleep or a scan was killed before it could raise its own alert. It reads
the spend ledger (the budget-ledger branch) and the open scan PRs, and prints one
alert phase per problem for scan_alert.sh. It changes nothing and fixes nothing.

  no-finished-scan     no daily (non-backfill) `done` row for today's UTC date
  stuck-pr-<n>         a claude/scan-* PR open longer than watchdog.stuck_pr_hours

Usage: watchdog.py --ledger budget.json --prs prs.json [--now ISO]
(prs.json is `gh api repos/R/pulls?state=open` output; each phase on its own line).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

STUCK_PR_HOURS = 8.0


def no_finished_scan(runs: list[dict], today: str, cap_set: bool) -> bool:
    """True when no daily run finished today. A null cap means scans are paused on purpose."""
    if not cap_set:
        return False
    return not any(
        r.get("kind") == "done" and r.get("date") == today and "backfill" not in r for r in runs
    )


def stuck_prs(prs: list[dict], now: datetime, hours: float) -> list[int]:
    """Open scan PRs older than `hours`: auto-merge runs every 30 minutes, so a
    healthy one merges within an hour or two of opening."""
    out = []
    for p in prs:
        ref = ((p.get("head") or {}).get("ref")) or ""
        created = p.get("created_at") or ""
        if not ref.startswith("claude/scan-") or not created:
            continue
        opened = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if (now - opened).total_seconds() > hours * 3600 and isinstance(p.get("number"), int):
            out.append(p["number"])
    return sorted(out)


def problems(runs: list[dict], prs: list[dict], now: datetime, cap_set: bool, hours: float):
    found = []
    if no_finished_scan(runs, now.strftime("%Y-%m-%d"), cap_set):
        found.append("no-finished-scan")
    found += [f"stuck-pr-{n}" for n in stuck_prs(prs, now, hours)]
    return found


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--prs", type=Path, required=True)
    ap.add_argument("--now", help="ISO time (tests); default: now, UTC")
    ap.add_argument("--cap-set", choices=("yes", "no"), default="yes")
    ap.add_argument("--stuck-pr-hours", type=float, default=STUCK_PR_HOURS)
    a = ap.parse_args(argv)
    now = datetime.fromisoformat(a.now) if a.now else datetime.now(UTC)
    runs = json.loads(a.ledger.read_text()).get("runs", [])
    prs = json.loads(a.prs.read_text())
    for phase in problems(runs, prs, now, a.cap_set == "yes", a.stuck_pr_hours):
        print(phase)
    return 0


if __name__ == "__main__":
    sys.exit(main())
