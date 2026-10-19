#!/usr/bin/env python3
"""
budget.py — The scan's spend guard and ledger (ISA ISC-8).

A cloud routine cannot read its remaining credit balance or its own token use
(routines.md § Usage and limits), so the pipeline keeps its own ledger: one row
per run with the stories it analyzed and what it cost. Local runs record the
cost `claude -p --output-format json` reports (`total_cost_usd`); cloud runs
record stories × the per-story cost measured on local runs.

`check` runs BEFORE any LLM work and refuses when:
  - no monthly cap is configured (`budget.monthly_cap_usd` in config.yaml),
  - the month's spend has reached the cap,
  - a run's known ceiling (max_stories_per_run × usd_per_story) no longer fits,
  - a cloud run has no measured per-story cost to estimate from yet.

The ledger file is synced from the `budget-ledger` branch by run_scan.sh, so
a run's spend counts even before its scan PR merges.

Usage:
    python scripts/budget.py check --runner cloud      # exit 0 = go, 3 = skip
    python scripts/budget.py record --runner local --stories 6 --cost-usd 1.84
    python scripts/budget.py status
    python scripts/budget.py ran-today --runner cloud  # exit 0 = a row exists today
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import common as c

SKIP_EXIT = 3
RUNNERS = ("cloud", "local")
DEFAULT_LEDGER = c.DATA_DIR / "_budget_ledger.json"


def ledger_path() -> Path:
    return Path(os.environ.get("BUDGET_LEDGER", DEFAULT_LEDGER))


def load_ledger(path: Path) -> list[dict]:
    return c.load_json(path, default={"runs": []}).get("runs", [])


def budget_settings() -> dict:
    raw = c.load_yaml(c.CONFIG_FILE)
    settings = dict(raw.get("budget") or {})
    settings["max_stories_per_run"] = int(raw.get("limits", {}).get("max_stories_per_run", 8))
    return settings


def month_spend(runs: list[dict], month: str) -> float:
    return round(sum(float(r["cost_usd"]) for r in runs if r["date"].startswith(month)), 4)


def usd_per_story(runs: list[dict], override: float | None = None) -> float | None:
    """Mean measured cost per story across local runs, or the config override."""
    if override is not None:
        return float(override)
    measured = [r for r in runs if r.get("measured") and r.get("stories", 0) > 0]
    if not measured:
        return None
    return sum(r["cost_usd"] for r in measured) / sum(r["stories"] for r in measured)


def check(runs: list[dict], settings: dict, runner: str, month: str) -> tuple[bool, str]:
    """Decide whether a run may start LLM work. Returns (ok, reason)."""
    cap = settings.get("monthly_cap_usd")
    if cap is None:
        return False, "no budget configured: set budget.monthly_cap_usd in config.yaml"
    spent = month_spend(runs, month)
    remaining = round(float(cap) - spent, 4)
    if remaining <= 0:
        return False, f"budget exhausted: ${spent:.2f} of ${cap:.2f} spent in {month}"
    per_story = usd_per_story(runs, settings.get("usd_per_story"))
    if per_story is None:
        if runner == "cloud":
            return False, "no measured per-story cost yet: run one local scan first"
        return True, f"${remaining:.2f} left in {month}; uncalibrated local run"
    ceiling = round(per_story * settings["max_stories_per_run"], 4)
    if ceiling > remaining:
        return False, f"run ceiling ${ceiling:.2f} exceeds the ${remaining:.2f} left in {month}"
    return True, f"${remaining:.2f} left in {month}; this run costs at most ${ceiling:.2f}"


def make_row(runs: list[dict], settings: dict, args: argparse.Namespace) -> dict:
    measured = args.cost_usd is not None
    if measured:
        cost = args.cost_usd
    else:
        per_story = usd_per_story(runs, settings.get("usd_per_story"))
        if per_story is None:
            raise SystemExit("record: no --cost-usd and no measured per-story cost")
        cost = per_story * args.stories
    return {
        "date": c.utcnow().strftime("%Y-%m-%d"),
        "runner": args.runner,
        "stories": args.stories,
        "cost_usd": round(float(cost), 4),
        "measured": measured,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("--runner", choices=RUNNERS, required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--runner", choices=RUNNERS, required=True)
    rec.add_argument("--stories", type=int, required=True)
    rec.add_argument("--cost-usd", type=float)
    sub.add_parser("status")
    today = sub.add_parser("ran-today")
    today.add_argument("--runner", choices=RUNNERS, required=True)
    args = ap.parse_args(argv)

    path, settings = ledger_path(), budget_settings()
    runs = load_ledger(path)
    month = c.utcnow().strftime("%Y-%m")
    if args.cmd == "record":
        runs.append(make_row(runs, settings, args))
        c.save_json(path, {"runs": runs})
        print(f"budget: recorded {runs[-1]}")
        return 0
    if args.cmd == "ran-today":
        date = c.utcnow().strftime("%Y-%m-%d")
        hit = any(r["date"] == date and r["runner"] == args.runner for r in runs)
        print(f"budget: {args.runner} {'ran' if hit else 'has not run'} on {date}")
        return 0 if hit else 1
    if args.cmd == "status":
        print(
            f"budget: ${month_spend(runs, month):.2f} spent in {month}; cap {settings.get('monthly_cap_usd')}"
        )
        return 0
    ok, reason = check(runs, settings, args.runner, month)
    print(f"budget: {'GO' if ok else 'SKIP'}: {reason}")
    return 0 if ok else SKIP_EXIT


if __name__ == "__main__":
    sys.exit(main())
