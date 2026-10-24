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
therefore still charged. Local runs append an `actual` row with the
`total_cost_usd` that `claude -p --output-format json` reported, after the
session and before `post`, so the scan PR shows it; an actual row replaces its
run's reservation (the latest actual row wins). Cloud runs keep the reservation: their true
cost is unreadable, so they are charged the ceiling.

`check` refuses when no cap is set, the month's spend has reached it, the run
ceiling no longer fits, a cloud run has no calibration yet, or any run already
happened today (unless --allow-repeat). One exception: a local run whose
`actual` row says `outcome: analysis-empty` and cost less than
`budget.retry_max_usd` may be followed by exactly one more local run that day.
The retry's own reservation is the record: a second tried run id blocks the day. The settings come from the config file
passed with --config, which run_scan.sh takes from origin/main.

Backfill (issue #52, scripts/backfill.sh): `check --backfill FROM..TO` and
`reserve --backfill FROM..TO` label a local run as one backfill chunk. Its rows
carry `backfill: "FROM..TO"` (actual and done rows copy it from the
reservation), so they never count as the day's scan, and `check_backfill`
enforces the campaign config.yaml `backfill:` approves on main: chunks inside
its window, none overlapping a finished chunk, at most `max_runs` started and
`max_usd` charged (this run's ceiling included), and the monthly cap.

Usage:
    python scripts/budget.py --config CFG check --runner cloud     # exit 0 go, 3 skip
    python scripts/budget.py --config CFG reserve --runner cloud --run-id ID
    python scripts/budget.py --config CFG actual --run-id ID --stories 6 --cost-usd 1.84
    python scripts/budget.py --config CFG actual --run-id ID --stories 0 --cost-usd 0.4 \
        --outcome analysis-empty
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
from datetime import date, timedelta
from pathlib import Path

import common as c

SKIP_EXIT = 3
RUNNERS = ("cloud", "local")
KINDS = ("reserve", "actual", "done")  # done: post finished; costs nothing
OUTCOMES = ("analysis-empty",)  # optional on an actual row: why the run failed
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WINDOW_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")  # a backfill row's window
RUN_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")  # also keeps SPEND.md's table intact
DEFAULT_LEDGER = c.DATA_DIR / "_budget_ledger.json"


class LedgerError(ValueError):
    """A ledger row that doesn't match the schema: fail closed, never guess."""


def ledger_path() -> Path:
    return Path(os.environ.get("BUDGET_LEDGER", DEFAULT_LEDGER))


def validate_row(row: dict) -> dict:
    cost, stories = row.get("cost_usd"), row.get("stories")
    ok = (
        isinstance(row.get("run_id"), str)
        and RUN_ID_RE.match(row["run_id"]) is not None
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
        and row.get("outcome", OUTCOMES[0]) in OUTCOMES
        and ("backfill" not in row or WINDOW_RE.fullmatch(str(row["backfill"])) is not None)
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
    settings["backfill"] = dict(raw.get("backfill") or {})
    return settings


def is_backfill(row: dict) -> bool:
    return "backfill" in row


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


def usd_per_story(
    runs: list[dict],
    override: float | None = None,
    window: int | None = None,
    max_stories: int | None = None,
) -> float | None:
    """Worst measured cost per story across runs, or the config override.

    The worst run, not the mean: padding one run with cheap stories can't lower
    the ceiling every later cloud run is charged. With `window`, the worst of
    the last `window` measured runs only, so one early outlier doesn't price
    every later run forever (the first run, 3 stories at $0.44 each, set the
    ceiling while the 8-story run cost $0.21 each). Lowering it then takes
    `window` padded runs in a row, each still charged its measured cost.

    One row per run (its latest `actual`, as in effective_runs), so a run with
    two actual rows can't fill two window slots. With `max_stories`, a row's
    story count is capped at it: post refuses more, so a bigger count is padding.
    """
    if override is not None:
        return float(override)
    latest: dict[str, dict] = {}
    for r in runs:
        if r["kind"] == "actual":
            latest.pop(r["run_id"], None)  # re-insert: order by each run's latest row
            latest[r["run_id"]] = r
    measured = [
        r["cost_usd"] / min(r["stories"], max_stories or r["stories"])
        for r in latest.values()
        if r["stories"] > 0
    ]
    if window is not None and int(window) > 0:  # 0 or less: every measured run
        measured = measured[-int(window) :]
    return max(measured) if measured else None


def run_ceiling(runs: list[dict], settings: dict, runner: str) -> tuple[float | None, str]:
    """The most one run may cost, or (None, reason) when it can't be bounded.

    A measured rate is multiplied by `ceiling_headroom` (default 1): the local
    session's hard cap is `session_cap_fraction` of this ceiling, so a run as
    expensive as the worst one measured must still fit under it.
    """
    override = settings.get("usd_per_story")
    per_story = usd_per_story(
        runs, override, settings.get("calibration_runs"), settings["max_stories_per_run"]
    )
    if per_story is not None:
        headroom = (
            1.0 if override is not None else max(1.0, float(settings.get("ceiling_headroom") or 1))
        )
        return round(per_story * headroom * settings["max_stories_per_run"], 4), "calibrated"
    if runner == "cloud":
        return None, "no measured per-story cost yet: run one local scan first"
    reserve = settings.get("uncalibrated_run_usd")
    if reserve is None:
        return None, "no calibration and no budget.uncalibrated_run_usd for a first local run"
    return round(float(reserve), 4), "uncalibrated reserve"


def retry_allowed(today_rows: list[dict], tried: set[str], settings: dict, runner: str) -> bool:
    """One local retry a day: the only earlier attempt failed analysis-empty and
    its measured cost stayed under budget.retry_max_usd."""
    limit = settings.get("retry_max_usd")
    if runner != "local" or len(tried) != 1 or limit is None:
        return False
    (run_id,) = tried
    return any(
        r["run_id"] == run_id
        and r["kind"] == "actual"
        and r.get("outcome") == "analysis-empty"
        and r["cost_usd"] < float(limit)
        for r in today_rows
    )


def check(
    runs: list[dict], settings: dict, runner: str, today: str, allow_repeat: bool = False
) -> tuple[bool, str]:
    """Decide whether a daily run may start LLM work. Returns (ok, reason)."""
    cap = settings.get("monthly_cap_usd")
    if cap is None:
        return False, "no budget configured: set budget.monthly_cap_usd in config.yaml"
    if not allow_repeat:
        # A day is done once any run finished it. A run that failed doesn't
        # block the other runner (the Mac falls back for a failed cloud run),
        # but a runner never retries its own failed day unattended. Backfill
        # runs are never the day's scan: they neither finish nor try a day.
        today_rows = [r for r in runs if r["date"] == today and not is_backfill(r)]
        if any(r["kind"] == "done" for r in today_rows):
            return False, f"a scan already finished on {today}"
        tried = {
            r["run_id"] for r in today_rows if r["kind"] == "reserve" and r["runner"] == runner
        }
        if tried and not retry_allowed(today_rows, tried, settings, runner):
            return False, f"the {runner} runner already tried on {today}"
    return fits_month(runs, settings, runner, today)


def fits_month(runs: list[dict], settings: dict, runner: str, today: str) -> tuple[bool, str]:
    """The monthly cap: this run's ceiling must fit in what the month has left."""
    cap = settings.get("monthly_cap_usd")
    if cap is None:
        return False, "no budget configured: set budget.monthly_cap_usd in config.yaml"
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


def parse_window(text: str) -> tuple[str, str]:
    """`FROM..TO` as two ISO days, or ValueError."""
    m = WINDOW_RE.fullmatch(text or "")
    if not m:
        raise ValueError(f"backfill window must be YYYY-MM-DD..YYYY-MM-DD, got {text!r}")
    return m.group(1), m.group(2)


def overlaps(a: tuple[str, str], b: tuple[str, str]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def campaign_rows(runs: list[dict], approved: tuple[str, str]) -> list[dict]:
    """The backfill rows whose window lies inside the approved campaign window."""
    out = []
    for r in runs:
        if is_backfill(r):
            frm, to = parse_window(r["backfill"])
            if approved[0] <= frm and to <= approved[1]:
                out.append(r)
    return out


def campaign(settings: dict) -> tuple[str, str] | None:
    """The approved campaign window (config.yaml backfill.from/to), else None."""
    cfg = settings.get("backfill") or {}
    if cfg.get("from") is None or cfg.get("to") is None:
        return None
    return str(cfg["from"]), str(cfg["to"])


BACKFILL_KEYS = ("from", "to", "max_runs", "max_usd", "max_chunk_days")


def backfill_window_problem(cfg: dict, window: str, today: str) -> str | None:
    """Why this chunk's window can't run under the approved campaign, else None."""
    try:
        frm, to = parse_window(window)
        c.parse_backfill_window(frm, to, date.fromisoformat(today))
    except ValueError as exc:
        return str(exc)
    if any(cfg.get(k) is None for k in BACKFILL_KEYS):
        return "no backfill approved: set backfill." + "/".join(BACKFILL_KEYS) + " in config.yaml"
    if not (str(cfg["from"]) <= frm and to <= str(cfg["to"])):
        return f"{window} is outside the approved {cfg['from']}..{cfg['to']}"
    span = (date.fromisoformat(to) - date.fromisoformat(frm)).days + 1
    if span > int(cfg["max_chunk_days"]):
        return f"{window} spans {span} days, over backfill.max_chunk_days {cfg['max_chunk_days']}"
    return None


def chunk_windows(frm: str, to: str, days: int) -> list[tuple[str, str]]:
    """[FROM, TO] split into consecutive windows of `days` days (the last one
    shorter), oldest first. ValueError on a bad window or chunk size."""
    if not 1 <= days <= c.BACKFILL_MAX_SPAN_DAYS:
        raise ValueError(f"chunk days must be 1..{c.BACKFILL_MAX_SPAN_DAYS}, got {days}")
    start, end = (date.fromisoformat(d) for d in parse_window(f"{frm}..{to}"))
    if start > end:
        raise ValueError(f"{frm}..{to} ends before it starts")
    out = []
    while start <= end:
        stop = min(end, start + timedelta(days=days - 1))
        out.append((start.isoformat(), stop.isoformat()))
        start = stop + timedelta(days=1)
    return out


def check_backfill(
    runs: list[dict], settings: dict, runner: str, window: str, today: str
) -> tuple[bool, str]:
    """Decide whether one backfill chunk may start LLM work. Returns (ok, reason).

    A backfill is approved on main as config.yaml `backfill:`: a campaign
    window, a chunk size, and caps for the whole campaign. A chunk must lie
    inside the campaign, must not overlap a chunk that already finished, and
    must fit the campaign's caps (runs started; dollars charged plus this run's
    ceiling) and the month's. `check`'s day rules don't apply: a backfill is
    never the day's scan, so it neither blocks nor is blocked by one."""
    cfg = settings.get("backfill") or {}
    if runner != "local":
        return False, "backfill runs only on the local runner (its cost is measured)"
    problem = backfill_window_problem(cfg, window, today)
    if problem:
        return False, f"backfill: {problem}"
    chunk = parse_window(window)
    for r in runs:
        if is_backfill(r) and r["kind"] == "done" and overlaps(parse_window(r["backfill"]), chunk):
            return False, f"backfill {window} overlaps {r['backfill']}, which already finished"
    rows = campaign_rows(runs, (str(cfg["from"]), str(cfg["to"])))
    started = {r["run_id"] for r in rows if r["kind"] == "reserve"}
    if len(started) >= int(cfg["max_runs"]):
        return False, f"backfill cap reached: {len(started)} of {cfg['max_runs']} runs started"
    spent = round(sum(float(r["cost_usd"]) for r in effective_runs(rows)), 4)
    ceiling, why = run_ceiling(runs, settings, runner)
    if ceiling is None:
        return False, why
    if spent + ceiling > float(cfg["max_usd"]):
        return False, (
            f"backfill cap: ${spent:.2f} charged + this run's ${ceiling:.2f} ceiling "
            f"exceeds backfill.max_usd ${float(cfg['max_usd']):.2f}"
        )
    ok, reason = fits_month(runs, settings, runner, today)
    if not ok:
        return False, reason
    run_n = f"run {len(started) + 1} of {cfg['max_runs']}"
    return True, f"backfill {window}, {run_n}, ${spent:.2f} charged so far; {reason}"


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
        runner = f"{r['runner']} backfill {r['backfill']}" if is_backfill(r) else r["runner"]
        lines.append(
            f"| {r['date']} | {runner} | `{r['run_id']}` | {stories} "
            f"| ${float(r['cost_usd']):.2f} | {basis} | {done} |"
        )
    if not rows:
        lines.append("| | | no runs yet | | | | |")
    return "\n".join(lines + backfill_lines(runs, settings)) + "\n"


def backfill_lines(runs: list[dict], settings: dict) -> list[str]:
    """The approved backfill campaign against its caps (nothing when none is set)."""
    approved, cfg = campaign(settings), settings.get("backfill") or {}
    if approved is None:
        return []
    rows = campaign_rows(runs, approved)
    started = {r["run_id"] for r in rows if r["kind"] == "reserve"}
    done = sorted({r["backfill"] for r in rows if r["kind"] == "done"})
    spent = sum(float(r["cost_usd"]) for r in effective_runs(rows))
    return [
        "",
        f"**Backfill {approved[0]}..{approved[1]}:** ${spent:.2f} charged of "
        f"${float(cfg.get('max_usd') or 0):.2f}, {len(started)} of {cfg.get('max_runs')} "
        f"runs started. Finished windows: {', '.join(done) or 'none'}.",
    ]


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
    chk.add_argument("--backfill", metavar="FROM..TO", help="check one backfill chunk")
    res = sub.add_parser("reserve")
    res.add_argument("--runner", choices=RUNNERS, required=True)
    res.add_argument("--run-id", required=True)
    res.add_argument("--backfill", metavar="FROM..TO", help="label the run a backfill")
    act = sub.add_parser("actual")
    act.add_argument("--run-id", required=True)
    act.add_argument("--stories", type=int, required=True)
    act.add_argument("--cost-usd", type=float, required=True)
    act.add_argument("--outcome", choices=OUTCOMES)
    sub.add_parser("status")
    lim = sub.add_parser("session-limits")
    lim.add_argument("--runner", choices=RUNNERS, required=True)
    chunks = sub.add_parser("chunks", help="split FROM..TO into backfill chunks")
    chunks.add_argument("start", metavar="FROM")
    chunks.add_argument("end", metavar="TO")
    chunks.add_argument("days", type=int)
    done = sub.add_parser("done")
    done.add_argument("--run-id", required=True)
    done.add_argument("--stories", type=int, required=True)
    return ap.parse_args(argv)


def reserve(path: Path, runs: list[dict], settings: dict, args, today: str) -> int:
    ceiling, why = run_ceiling(runs, settings, args.runner)
    if ceiling is None:
        raise SystemExit(f"reserve: {why}")
    row = {"run_id": args.run_id, "date": today, "runner": args.runner, "kind": "reserve"}
    if args.backfill:
        # Re-checked against the very ledger the row is appended to.
        ok, why = check_backfill(runs, settings, args.runner, args.backfill, today)
        if not ok:
            raise SystemExit(f"reserve: {why}")
        row["backfill"] = args.backfill
    append_row(path, runs, {**row, "stories": 0, "cost_usd": ceiling})
    return 0


def actual(path: Path, runs: list[dict], args) -> int:
    held = [r for r in runs if r["run_id"] == args.run_id and r["kind"] == "reserve"]
    if not held:
        raise SystemExit(f"actual: no reservation for run {args.run_id}")
    if held[0]["runner"] != "local":
        # A cloud run can't read its own cost: it stays charged its reservation.
        # An actual row would replace that charge and feed the calibration.
        raise SystemExit(f"actual: run {args.run_id} is a {held[0]['runner']} run")
    row = {**held[0], "kind": "actual", "stories": args.stories, "cost_usd": args.cost_usd}
    if args.outcome:
        row["outcome"] = args.outcome
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
    if args.cmd == "chunks":  # pure: no ledger, no config
        for frm, to in chunk_windows(args.start, args.end, args.days):
            print(frm, to)
        return 0
    path, settings = ledger_path(), budget_settings(args.config)
    if args.cmd != "status" and not path.exists():
        # run_scan.sh always writes the fetched ledger first; a missing file
        # means the fetch failed, and an empty ledger would read as "GO".
        raise LedgerError(f"ledger file missing: {path}")
    runs = load_ledger(path)
    today = c.utcnow().strftime("%Y-%m-%d")
    if args.cmd == "check":
        if args.backfill:
            ok, reason = check_backfill(runs, settings, args.runner, args.backfill, today)
        else:
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
