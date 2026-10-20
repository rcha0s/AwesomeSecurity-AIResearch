#!/usr/bin/env python3
"""
eval_history.py — Per-run eval history, the cost eval, and the Phase 3 gate (ISA ISC-25, ISC-26).

`run_scan.sh post` calls `append` once per scan that opens a PR: one row in
data/evals/history.json with that run's numbers (candidates staged, stories
analyzed, stories kept), the integrity eval run then and there, the newest
weekly recall and golden results, and the run's charge on the budget ledger
against the per-run cap. `body` renders those numbers and the 7-run trend for
the scan PR. `gate` says whether the last `evals.gate_runs` rows all pass:

  recall     >= thresholds.recall_min, from a result at most max_result_age_days old
  golden     >= thresholds.golden_min and off-topic <= thresholds.off_topic_max (same age rule)
  integrity  passed: all or nothing
  cost       charged <= the per-run cap (thresholds.max_run_usd, else monthly cap / 30)

A run counts only once its scan PR merges: rows ride on the PR, and post resets
data/evals/ to main's copy before it appends, so nothing a session wrote there ships.

Usage:
    python scripts/eval_history.py append --run-id ID --runner cloud --stories 6 \\
        --candidates 40 [--ledger L] [--config CFG]
    python scripts/eval_history.py body --run-id ID     # markdown for the PR body
    python scripts/eval_history.py gate [--json]         # exit 0 = the last N runs pass
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import budget
import common as c
import eval_integrity
import eval_lib as el

HISTORY_FILE = "history.json"
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
def weekly(prefix: str, keys: tuple[str, ...], max_age: int) -> dict | None:
    """The newest recall/golden result's headline numbers, with a staleness flag."""
    found = el.latest_result(prefix)
    if not found:
        return None
    path, result = found
    row = {k: result.get(k) for k in keys}
    return {**row, "file": path.name, "stale": el.is_stale(result, max_age)}


def kept_new() -> tuple[int, int]:
    """(new entries this run, of them kept: curated or a news story)."""
    conf, sources, on_main = c.load_config(), c.load_sources_by_id(), c.main_entry_ids()
    new = [e for e in c.all_pool_entries() if e.get("id") not in on_main]
    kept = [e for e in new if c.is_curated(e, conf) or c.is_news_story(e, conf, sources)]
    return len(new), len(kept)


def run_charge(ledger: Path | None, run_id: str) -> float | None:
    """This run's charge: its measured cost, else its reservation."""
    if ledger is None or not ledger.exists():
        return None
    rows = budget.effective_runs(budget.load_ledger(ledger))
    return next((float(r["cost_usd"]) for r in rows if r["run_id"] == run_id), None)


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
        "recall": weekly("recall", ("recall", "week", "generated"), age),
        "golden": weekly("golden", ("score", "off_topic_rate", "cases", "generated"), age),
        "integrity": {"passed": integrity["passed"], "problems": len(integrity["problems"])},
        "cost_usd": run_charge(args.ledger, args.run_id),
        "cap_usd": el.per_run_cap(args.config),
    }


# --- The gate -----------------------------------------------------------------
def verdict(row: dict, thresholds: dict) -> list[str]:
    """Why this run fails the gate ([] = it passes)."""
    out = []
    rec, gold = row.get("recall") or {}, row.get("golden") or {}
    if rec.get("stale", True) or rec.get("recall") is None:
        out.append("no fresh recall result")
    elif rec["recall"] < float(thresholds["recall_min"]):
        out.append(f"recall {rec['recall']:.2f} < {thresholds['recall_min']}")
    if gold.get("stale", True) or gold.get("score") is None:
        out.append("no fresh golden result")
    else:
        if gold["score"] < float(thresholds["golden_min"]):
            out.append(f"golden {gold['score']:.2f} < {thresholds['golden_min']}")
        if (gold.get("off_topic_rate") or 0) > float(thresholds["off_topic_max"]):
            out.append(f"off-topic {gold['off_topic_rate']:.2f} > {thresholds['off_topic_max']}")
    integ = row.get("integrity") or {}
    if not integ.get("passed"):
        out.append(f"integrity failed ({integ.get('problems', '?')} problems)")
    cost, cap = row.get("cost_usd"), row.get("cap_usd")
    if cost is None or cap is None:
        out.append("cost or per-run cap unknown")
    elif cost > cap:
        out.append(f"cost ${cost:.2f} > cap ${cap:.2f}")
    return out


def gate(rows: list[dict], cfg: dict) -> dict:
    """Whether the last `gate_runs` consecutive runs all pass."""
    need = int(cfg["gate_runs"])
    window = rows[-need:]
    checked = [{"run_id": r.get("run_id"), "date": r.get("date"),
                "fails": verdict(r, cfg["thresholds"])} for r in window]  # fmt: skip
    streak = 0
    for r in reversed([verdict(r, cfg["thresholds"]) for r in rows]):
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
        f"LLM calls: {LLM_CALLS_NOTE} · charged {_money(row['cost_usd'])} of a "
        f"{_money(row['cap_usd'])} per-run cap.",
        "",
        f"**Last {cfg['gate_runs']} runs** (Phase 3 gate):",
        "",
        "| Date | Runner | Candidates | Stories | Kept | Charged | Gate |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows[-int(cfg["gate_runs"]) :]:
        fails = verdict(r, cfg["thresholds"])
        mark = "pass" if not fails else "fail: " + "; ".join(fails)
        lines.append(
            f"| {r.get('date')} | {r.get('runner')} | {r.get('candidates')} | {r.get('stories')} "
            f"| {r.get('kept')} ({_pct(r.get('kept_ratio'))}) | {_money(r.get('cost_usd'))} | {mark} |"
        )
    return "\n".join(lines)


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
        fails = verdict(row, cfg["thresholds"])
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
