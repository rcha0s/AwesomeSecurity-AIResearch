#!/usr/bin/env python3
"""
budget.py — The scan's spend guard and ledger (ISA ISC-8).

A cloud routine cannot read its remaining credit balance or its own token use
(routines.md § Usage and limits), so the pipeline keeps its own ledger on the
`budget-ledger` branch. run_scan.sh always appends to a fresh copy fetched from
that branch, never to a working-tree file the model could edit.

Reserve before spending. Once `check` passes, `pre` appends a `reserve` row for
the run's whole ceiling (max_stories_per_run × measured per-story cost, or
`uncalibrated_run_usd` before any calibration). A run that fails halfway is
therefore still charged. Local runs later append an `actual` row with the
`total_cost_usd` that `claude -p --output-format json` reported; an actual row
replaces its run's reservation. Cloud runs keep the reservation: their true
cost is unreadable, so they are charged the ceiling.

`check` refuses when no cap is set, the month's spend has reached it, the run
ceiling no longer fits, a cloud run has no calibration yet, or any run already
happened today (unless --allow-repeat). The settings come from the config file
passed with --config, which run_scan.sh takes from origin/main.

Usage:
    python scripts/budget.py --config CFG check --runner cloud     # exit 0 go, 3 skip
    python scripts/budget.py --config CFG reserve --runner cloud --run-id ID
    python scripts/budget.py --config CFG actual --run-id ID --stories 6 --cost-usd 1.84
    python scripts/budget.py --config CFG status          # this month's spend report (markdown)
    python scripts/budget.py --config CFG done --run-id ID --stories 6
    python scripts/budget.py --config CFG session-limits --runner local  # "<usd> <turns>"
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from collections.abc import Iterable
from pathlib import Path

import common as c

SKIP_EXIT = 3
RUNNERS = ("cloud", "local")
KINDS = ("reserve", "actual", "done")  # done: post finished; costs nothing
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DEFAULT_LEDGER = c.DATA_DIR / "_budget_ledger.json"


class LedgerError(ValueError):
    """A ledger row that doesn't match the schema: fail closed, never guess."""


def ledger_path() -> Path:
    return Path(os.environ.get("BUDGET_LEDGER", DEFAULT_LEDGER))


def validate_row(row: dict) -> dict:
    cost, stories = row.get("cost_usd"), row.get("stories")
    ok = (
        isinstance(row.get("run_id"), str)
        and bool(row["run_id"])
        and DATE_RE.match(str(row.get("date", ""))) is not None
        and row.get("runner") in RUNNERS
        and row.get("kind") in KINDS
        and isinstance(stories, int)
        and not isinstance(stories, bool)
        and stories >= 0
        and isinstance(cost, int | float)
        and not isinstance(cost, bool)
        and math.isfinite(cost)
        and cost >= 0
    )
    if not ok:
        raise LedgerError(f"invalid ledger row: {row}")
    return row


def load_ledger(path: Path) -> list[dict]:
    data = c.load_json(path, default={"runs": []})
    return [validate_row(r) for r in data.get("runs", [])]


def budget_settings(config: Path | str = c.CONFIG_FILE) -> dict:
    raw = c.load_yaml(Path(config))
    settings = dict(raw.get("budget") or {})
    limits = raw.get("limits", {})
    settings["max_stories_per_run"] = int(limits.get("max_stories_per_run", 8))
    settings["max_turns"] = int(limits.get("max_turns", 150))
    return settings


def effective_runs(runs: Iterable[dict]) -> list[dict]:
    """One row per run: its `actual` row if it has one, else its reservation."""
    by_run: dict[str, dict] = {}
    for r in runs:
        if r["kind"] == "done":
            continue
        if r["kind"] == "actual" or r["run_id"] not in by_run:
            by_run[r["run_id"]] = r
    return list(by_run.values())


def month_spend(runs: list[dict], month: str) -> float:
    rows = effective_runs(runs)
    return round(sum(float(r["cost_usd"]) for r in rows if r["date"].startswith(month)), 4)


def usd_per_story(runs: list[dict], override: float | None = None) -> float | None:
    """Worst measured cost per story across `actual` rows, or the config override.

    The worst run, not the mean: padding one run with cheap stories can't lower
    the ceiling every later cloud run is charged.
    """
    if override is not None:
        return float(override)
    measured = [
        r["cost_usd"] / r["stories"] for r in runs if r["kind"] == "actual" and r["stories"] > 0
    ]
    return max(measured) if measured else None


def run_ceiling(runs: list[dict], settings: dict, runner: str) -> tuple[float | None, str]:
    """The most one run may cost, or (None, reason) when it can't be bounded."""
    per_story = usd_per_story(runs, settings.get("usd_per_story"))
    if per_story is not None:
        return round(per_story * settings["max_stories_per_run"], 4), "calibrated"
    if runner == "cloud":
        return None, "no measured per-story cost yet: run one local scan first"
    reserve = settings.get("uncalibrated_run_usd")
    if reserve is None:
        return None, "no calibration and no budget.uncalibrated_run_usd for a first local run"
    return round(float(reserve), 4), "uncalibrated reserve"


def check(
    runs: list[dict], settings: dict, runner: str, today: str, allow_repeat: bool = False
) -> tuple[bool, str]:
    """Decide whether a run may start LLM work. Returns (ok, reason)."""
    cap = settings.get("monthly_cap_usd")
    if cap is None:
        return False, "no budget configured: set budget.monthly_cap_usd in config.yaml"
    if not allow_repeat:
        # A day is done once any run finished it. A run that failed doesn't
        # block the other runner (the Mac falls back for a failed cloud run),
        # but a runner never retries its own failed day unattended.
        today_rows = [r for r in runs if r["date"] == today]
        if any(r["kind"] == "done" for r in today_rows):
            return False, f"a scan already finished on {today}"
        if any(r["kind"] == "reserve" and r["runner"] == runner for r in today_rows):
            return False, f"the {runner} runner already tried on {today}"
    month = today[:7]
    spent = month_spend(runs, month)
    remaining = round(float(cap) - spent, 4)
    if remaining <= 0:
        return False, f"budget exhausted: ${spent:.2f} of ${cap:.2f} spent in {month}"
    ceiling, why = run_ceiling(runs, settings, runner)
    if ceiling is None:
        return False, why
    if ceiling > remaining:
        return False, f"run ceiling ${ceiling:.2f} exceeds the ${remaining:.2f} left in {month}"
    return True, f"${remaining:.2f} left in {month}; this run reserves ${ceiling:.2f} ({why})"


def spend_report(runs: list[dict], settings: dict, month: str) -> str:
    """This month's spend as markdown: the total against the cap, then one row per run."""
    cap = settings.get("monthly_cap_usd")
    cap_txt = f"${float(cap):.2f}" if cap is not None else "no cap set (runs skip)"
    finished = {r["run_id"]: r["stories"] for r in runs if r["kind"] == "done"}
    rows = [r for r in effective_runs(runs) if r["date"].startswith(month)]
    lines = [
        f"# Scan spend, {month}",
        "",
        f"**${month_spend(runs, month):.2f} charged of {cap_txt}.** Local runs are charged "
        "their measured `total_cost_usd`; cloud runs can't read their cost, so they are "
        "charged their reserved ceiling.",
        "",
        "| Date | Runner | Run | Stories | Charged | Basis | Finished |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (r["date"], r["run_id"])):
        basis = "measured" if r["kind"] == "actual" else "reserved ceiling"
        stories = finished.get(r["run_id"], r["stories"])
        done = "yes" if r["run_id"] in finished else "no"
        lines.append(
            f"| {r['date']} | {r['runner']} | `{r['run_id']}` | {stories} "
            f"| ${float(r['cost_usd']):.2f} | {basis} | {done} |"
        )
    if not rows:
        lines.append("| | | no runs yet | | | | |")
    return "\n".join(lines) + "\n"


def append_row(path: Path, runs: list[dict], row: dict) -> None:
    runs.append(validate_row(row))
    c.save_json(path, {"runs": runs})
    print(f"budget: recorded {row}")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--config", type=Path, default=c.CONFIG_FILE)
    sub = ap.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("--runner", choices=RUNNERS, required=True)
    chk.add_argument("--allow-repeat", action="store_true")
    res = sub.add_parser("reserve")
    res.add_argument("--runner", choices=RUNNERS, required=True)
    res.add_argument("--run-id", required=True)
    act = sub.add_parser("actual")
    act.add_argument("--run-id", required=True)
    act.add_argument("--stories", type=int, required=True)
    act.add_argument("--cost-usd", type=float, required=True)
    sub.add_parser("status")
    lim = sub.add_parser("session-limits")
    lim.add_argument("--runner", choices=RUNNERS, required=True)
    done = sub.add_parser("done")
    done.add_argument("--run-id", required=True)
    done.add_argument("--stories", type=int, required=True)
    return ap.parse_args(argv)


def reserve(path: Path, runs: list[dict], settings: dict, args, today: str) -> int:
    ceiling, why = run_ceiling(runs, settings, args.runner)
    if ceiling is None:
        raise SystemExit(f"reserve: {why}")
    row = {"run_id": args.run_id, "date": today, "runner": args.runner, "kind": "reserve"}
    append_row(path, runs, {**row, "stories": 0, "cost_usd": ceiling})
    return 0


def actual(path: Path, runs: list[dict], args) -> int:
    held = [r for r in runs if r["run_id"] == args.run_id and r["kind"] == "reserve"]
    if not held:
        raise SystemExit(f"actual: no reservation for run {args.run_id}")
    row = {**held[0], "kind": "actual", "stories": args.stories, "cost_usd": args.cost_usd}
    append_row(path, runs, row)
    return 0


def mark_done(path: Path, runs: list[dict], args) -> int:
    held = [r for r in runs if r["run_id"] == args.run_id and r["kind"] == "reserve"]
    if not held:
        raise SystemExit(f"done: no reservation for run {args.run_id}")
    row = {**held[0], "kind": "done", "stories": args.stories, "cost_usd": 0}
    append_row(path, runs, row)
    return 0


def session_limits(runs: list[dict], settings: dict, runner: str) -> int:
    """Print `<max_budget_usd> <max_turns>` for the model session."""
    ceiling, why = run_ceiling(runs, settings, runner)
    if ceiling is None:
        raise SystemExit(f"session-limits: {why}")
    fraction = float(settings.get("session_cap_fraction", 0.8))
    print(f"{ceiling * fraction:.2f} {settings['max_turns']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    path, settings = ledger_path(), budget_settings(args.config)
    if args.cmd != "status" and not path.exists():
        # run_scan.sh always writes the fetched ledger first; a missing file
        # means the fetch failed, and an empty ledger would read as "GO".
        raise LedgerError(f"ledger file missing: {path}")
    runs = load_ledger(path)
    today = c.utcnow().strftime("%Y-%m-%d")
    if args.cmd == "check":
        ok, reason = check(runs, settings, args.runner, today, args.allow_repeat)
        print(f"budget: {'GO' if ok else 'SKIP'}: {reason}")
        return 0 if ok else SKIP_EXIT
    if args.cmd == "reserve":
        return reserve(path, runs, settings, args, today)
    if args.cmd == "actual":
        return actual(path, runs, args)
    if args.cmd == "done":
        return mark_done(path, runs, args)
    if args.cmd == "session-limits":
        return session_limits(runs, settings, args.runner)
    print(spend_report(runs, settings, today[:7]), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
