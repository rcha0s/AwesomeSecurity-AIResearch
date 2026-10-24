#!/usr/bin/env python3
"""
eval_history.py — Per-run eval history, the cost eval, and the Phase 3 gate (ISA ISC-25, ISC-26).

`run_scan.sh post` calls `append` once per scan that opens a PR: one row in
data/evals/history.json with that run's numbers (candidates staged, stories
analyzed, stories kept), the integrity eval run then and there, the newest
weekly recall and golden results, and the run's charge on the budget ledger
against the per-run cap. `body` renders those numbers and the 7-run trend for
the scan PR. `gate` says whether the last `evals.gate_runs` rows all pass:

  recall     >= thresholds.recall_min from a clean result (it passed, no curator
             errored) at most max_result_age_days old and not future-dated
  golden     >= thresholds.golden_min and off-topic <= thresholds.off_topic_max (same age rule)
  integrity  passed: all or nothing
  cost       a measured charge <= the per-run cap (thresholds.max_run_usd, else monthly
             cap / 30); a reserved charge (every cloud run, and a local run whose
             cost was unreadable) <= the ceiling it reserved, since its true cost
             is unknowable. The Mac wrapper records the measured cost before post,
             so a local row carries it

Backfill runs (issue #52) are marked `backfill: "FROM..TO"` and never count:
the gate judges the daily pipeline, and a backfill chunk's recall is this
week's, not its window's. `gate` and the PR body's trend skip them; the body
lists them on a line of their own. merge_gate checks the mark against the
run's reservation on the budget ledger, so a daily row can't hide behind it.

A run counts only once its scan PR merges: rows ride on the PR. post resets
data/evals/ to main's copy before it appends, merge_guard lets a scan PR touch
only data/evals/history.json there, and merge_gate (content_checks.history_problems)
proves main's rows are untouched and the one new row agrees with the budget
ledger, the merged tree's integrity and the newest golden result.

Usage:
    python scripts/eval_history.py append --run-id ID --runner cloud --stories 6 \\
        --candidates 40 [--ledger L] [--recall R] [--config CFG]
    python scripts/eval_history.py body --run-id ID     # markdown for the PR body
    python scripts/eval_history.py gate [--json]         # exit 0 = the last N runs pass
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import budget
import common as c
import eval_integrity
import eval_lib as el

HISTORY_FILE = "history.json"
AGE = el.DEFAULTS["max_result_age_days"]
LLM_CALLS_NOTE = "not measurable in-run (cloud runs expose no usage; local cost lands in SPEND.md)"


def history_path() -> Path:
    return el.evals_dir() / HISTORY_FILE


def load_rows(path: Path | None = None) -> list[dict]:
    return (c.load_json(path or history_path(), default={}) or {}).get("runs") or []


def save_row(row: dict, path: Path | None = None) -> list[dict]:
    """Append `row`, replacing an earlier row for the same run (re-run of post)."""
    rows = [r for r in load_rows(path) if r.get("run_id") != row["run_id"]] + [row]
    c.save_json(path or history_path(), {"runs": rows})
    return rows


# --- Inputs for one row -------------------------------------------------------
# independent_recall + curator_recall are reported, not gated (eval_recall.py).
RECALL_KEYS = ("recall", "independent_recall", "curator_recall", "week", "generated", "passed")
GOLDEN_KEYS = ("score", "off_topic_rate", "cases", "generated")


def summarize(result: dict, keys: tuple[str, ...], name: str, max_age: int) -> dict:
    row = {k: result.get(k) for k in keys}
    errors = result.get("errors") or []
    return {**row, "errors": len(errors), "file": name, "stale": el.is_stale(result, max_age)}


def weekly(prefix: str, keys: tuple[str, ...], max_age: int) -> dict | None:
    """The newest recall/golden result's headline numbers, with a staleness flag."""
    found = el.latest_result(prefix)
    return summarize(found[1], keys, found[0].name, max_age) if found else None


def recall_from(path: Path | None, max_age: int) -> dict | None:
    """This run's own recall result (post fetches it fresh, outside the tree)."""
    if path is None:
        return weekly("recall", RECALL_KEYS, max_age)
    result = c.load_json(path, default=None) if path.exists() else None
    return summarize(result, RECALL_KEYS, path.name, max_age) if isinstance(result, dict) else None


def kept_new() -> tuple[int, int]:
    """(new entries this run, of them kept: curated or a news story)."""
    conf, sources, on_main = c.load_config(), c.load_sources_by_id(), c.main_entry_ids()
    new = [e for e in c.all_pool_entries() if e.get("id") not in on_main]
    kept = [e for e in new if c.is_curated(e, conf) or c.is_news_story(e, conf, sources)]
    return len(new), len(kept)


def run_charge(ledger: Path | None, run_id: str) -> dict:
    """This run's charge on the ledger: cost, basis (measured | reserved), and the
    ceiling it reserved. All None when the ledger or the run is missing."""
    out = {"cost_usd": None, "cost_basis": None, "ceiling_usd": None}
    if ledger is None or not ledger.exists():
        return out
    runs = budget.load_ledger(ledger)
    held = [r for r in runs if r["run_id"] == run_id and r["kind"] == "reserve"]
    charge = next((r for r in budget.effective_runs(runs) if r["run_id"] == run_id), None)
    if charge is None or not held:
        return out
    basis = "measured" if charge["kind"] == "actual" else "reserved"
    return {"cost_usd": float(charge["cost_usd"]), "cost_basis": basis,
            "ceiling_usd": float(held[0]["cost_usd"])}  # fmt: skip


def build_row(args) -> dict:
    cfg = el.settings(args.config)
    age = int(cfg["max_result_age_days"])
    try:
        integrity = eval_integrity.run()
    except (OSError, ValueError) as exc:  # no rendered site to check is a failed check
        integrity = {"passed": False, "problems": [f"{type(exc).__name__}: {exc}"]}
    new, kept = kept_new()
    return {
        "run_id": args.run_id,
        "date": c.utcnow().strftime("%Y-%m-%d"),
        "runner": args.runner,
        "candidates": args.candidates,
        "stories": args.stories,
        "kept": kept,
        "kept_ratio": round(kept / new, 3) if new else None,
        "recall": recall_from(args.recall, age),
        "golden": weekly("golden", GOLDEN_KEYS, age),
        "integrity": {"passed": integrity["passed"], "problems": len(integrity["problems"])},
        **run_charge(args.ledger, args.run_id),
        "cap_usd": el.per_run_cap(args.config),
        **({"backfill": args.backfill} if args.backfill else {}),
    }


def gate_rows(rows: list[dict]) -> list[dict]:
    """The rows the gate judges: daily runs only, never a backfill chunk."""
    return [r for r in rows if not r.get("backfill")]


# --- The gate -----------------------------------------------------------------
def stale_at_run(result: dict, row: dict, max_age_days: int) -> bool:
    """Staleness as of the run's own date, from the result's `generated` stamp, so a
    row can't simply claim `stale: false`."""
    try:
        asof = datetime.fromisoformat(f"{row.get('date')}T23:59:59+00:00")
    except ValueError:
        return True
    return bool(result.get("stale", True)) or el.is_stale(result, max_age_days, now=asof)


def verdict(row: dict, thresholds: dict, max_age_days: int = AGE) -> list[str]:
    """Why this run fails the gate ([] = it passes)."""
    out = []
    rec, gold = row.get("recall") or {}, row.get("golden") or {}
    if stale_at_run(rec, row, max_age_days) or rec.get("recall") is None:
        out.append("no fresh recall result")
    elif rec.get("errors", 1) or rec.get("passed") is not True:
        out.append("recall result is not clean (curator errors or not passed)")
    elif rec["recall"] < float(thresholds["recall_min"]):
        out.append(f"recall {rec['recall']:.2f} < {thresholds['recall_min']}")
    if stale_at_run(gold, row, max_age_days) or gold.get("score") is None:
        out.append("no fresh golden result")
    else:
        if gold["score"] < float(thresholds["golden_min"]):
            out.append(f"golden {gold['score']:.2f} < {thresholds['golden_min']}")
        if (gold.get("off_topic_rate") or 0) > float(thresholds["off_topic_max"]):
            out.append(f"off-topic {gold['off_topic_rate']:.2f} > {thresholds['off_topic_max']}")
    integ = row.get("integrity") or {}
    if not integ.get("passed"):
        out.append(f"integrity failed ({integ.get('problems', '?')} problems)")
    return out + cost_fails(row)


def cost_fails(row: dict) -> list[str]:
    """A measured charge must fit the per-run cap; a reservation, its own ceiling."""
    cost, basis = row.get("cost_usd"), row.get("cost_basis")
    cap = row.get("cap_usd") if basis == "measured" else row.get("ceiling_usd")
    if cost is None or cap is None or basis not in ("measured", "reserved"):
        return ["cost, basis or cap unknown"]
    if cost > cap:
        limit = "per-run cap" if basis == "measured" else "reserved ceiling"
        return [f"cost ${cost:.2f} > {limit} ${cap:.2f}"]
    return []


def gate(rows: list[dict], cfg: dict) -> dict:
    """Whether the last `gate_runs` consecutive runs all pass."""
    need = int(cfg["gate_runs"])
    rows = gate_rows(rows)
    window = rows[-need:]
    checked = [{"run_id": r.get("run_id"), "date": r.get("date"),
                "fails": verdict(r, cfg["thresholds"], int(cfg["max_result_age_days"]))} for r in window]  # fmt: skip
    streak = 0
    for r in reversed(
        [verdict(r, cfg["thresholds"], int(cfg["max_result_age_days"])) for r in rows]
    ):
        if r:
            break
        streak += 1
    passed = len(window) >= need and all(not x["fails"] for x in checked)
    return {"passed": passed, "need": need, "runs": len(rows), "streak": streak, "window": checked}


# --- The cost eval in the PR body ---------------------------------------------
def _money(value: float | None) -> str:
    return "?" if value is None else f"${value:.2f}"


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.0%}"


def body(rows: list[dict], run_id: str, cfg: dict) -> str:
    row = next((r for r in rows if r.get("run_id") == run_id), None)
    if row is None:
        return "\n\n**Run numbers:** unavailable (no eval history row for this run)."
    lines = [
        "",
        "",
        f"**Run numbers:** {row['candidates']} candidates staged · {row['stories']} stories "
        f"analyzed · {row['kept']} kept ({_pct(row['kept_ratio'])} of new entries) · "
        f"LLM calls: {LLM_CALLS_NOTE} · charged {_money(row.get('cost_usd'))} "
        f"({row.get('cost_basis') or 'unknown'}; reserved ceiling "
        f"{_money(row.get('ceiling_usd'))}, per-run cap {_money(row.get('cap_usd'))}).",
        "",
        f"**Last {cfg['gate_runs']} runs** (Phase 3 gate):",
        "",
        "| Date | Runner | Candidates | Stories | Kept | Recall (independent) | Charged | Gate |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in gate_rows(rows)[-int(cfg["gate_runs"]) :]:
        fails = verdict(r, cfg["thresholds"], int(cfg["max_result_age_days"]))
        mark = "pass" if not fails else "fail: " + "; ".join(fails)
        lines.append(
            f"| {r.get('date')} | {r.get('runner')} | {r.get('candidates')} | {r.get('stories')} "
            f"| {r.get('kept')} ({_pct(r.get('kept_ratio'))}) | {_recall_cell(r)} "
            f"| {_money(r.get('cost_usd'))} | {mark} |"
        )
    if row.get("backfill"):
        lines[2] += f" Backfill {row['backfill']}: not counted in the gate."
    per = _curator_line(row)
    out = lines + ([f"\n**Recall by curator** (this run): {per}"] if per else [])
    return "\n".join(out + _backfill_line(rows))


def _backfill_line(rows: list[dict], last: int = 5) -> list[str]:
    """The latest backfill runs, kept out of the gate's trend table."""
    done = [r for r in rows if r.get("backfill")][-last:]
    if not done:
        return []
    cells = [f"{r.get('backfill')} ({r.get('stories')} stories, {r.get('kept')} kept, "
             f"{_money(_num(r.get('cost_usd')))})" for r in done]  # fmt: skip
    return [f"\n**Backfill runs** (not in the gate): {' · '.join(cells)}"]


def _num(value: object) -> float | None:
    ok = isinstance(value, int | float) and not isinstance(value, bool)
    return float(value) if ok else None


def _recall_cell(row: dict) -> str:
    rec = row.get("recall") if isinstance(row.get("recall"), dict) else {}
    return f"{_pct(_num(rec.get('recall')))} ({_pct(_num(rec.get('independent_recall')))})"


def _curator_line(row: dict) -> str:
    rec = row.get("recall") if isinstance(row.get("recall"), dict) else {}
    per = rec.get("curator_recall")
    if not isinstance(per, dict):
        return ""
    cells = []
    for name, t in sorted(per.items()):
        t = t if isinstance(t, dict) else {}
        cells.append(f"{name} {_pct(_num(t.get('recall')))} "
                     f"({_pct(_num(t.get('independent_recall')))} independent)")  # fmt: skip
    return " · ".join(cells)


# --- CLI ----------------------------------------------------------------------
def parse_args(argv: list[str] | None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--config", type=Path, default=c.CONFIG_FILE)
    sub = ap.add_subparsers(dest="cmd", required=True)
    app = sub.add_parser("append")
    app.add_argument("--run-id", required=True)
    app.add_argument("--runner", choices=budget.RUNNERS, required=True)
    app.add_argument("--stories", type=int, required=True)
    app.add_argument("--candidates", type=int, default=0)
    app.add_argument("--ledger", type=Path)
    app.add_argument("--recall", type=Path, help="this run's recall result (eval_recall --out)")
    app.add_argument("--backfill", metavar="FROM..TO", help="mark the row a backfill run")
    bod = sub.add_parser("body")
    bod.add_argument("--run-id", required=True)
    gat = sub.add_parser("gate")
    gat.add_argument("--json", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = el.settings(args.config)
    if args.cmd == "append":
        row = build_row(args)
        save_row(row)
        fails = verdict(row, cfg["thresholds"], int(cfg["max_result_age_days"]))
        print(el.summary_line("run", not fails, run_id=row["run_id"], fails=len(fails)))
        return 0
    if args.cmd == "body":
        print(body(load_rows(), args.run_id, cfg))
        return 0
    result = gate(load_rows(), cfg)
    if args.json:
        print(json.dumps(result, indent=2))
    for r in result["window"]:
        print(f"{'PASS' if not r['fails'] else 'FAIL'} {r['date']} {r['run_id']}"
              + (": " + "; ".join(r["fails"]) if r["fails"] else ""))  # fmt: skip
    print(el.summary_line("gate", result["passed"], streak=result["streak"],
                          need=result["need"], runs=result["runs"]))  # fmt: skip
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
