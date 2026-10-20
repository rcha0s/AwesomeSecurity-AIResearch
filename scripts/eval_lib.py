"""
eval_lib.py — What the Phase 3 evals share (ISA ISC-22..26).

Every eval is a CLI a merge gate can run: exit 0 = pass, non-zero = fail, and
the LAST line of stdout is one machine-readable summary:

    EVAL <name> PASS|FAIL key=value key=value ...

Results that outlive a run (weekly recall and golden scores, the per-run
history) live under data/evals/.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

import common as c

DEFAULTS = {
    "gate_runs": 7,
    "max_result_age_days": 8,
    "thresholds": {
        "recall_min": 0.85,
        "golden_min": 0.90,
        "off_topic_max": 0.10,
        "max_run_usd": None,
    },
    "recall": {"lookback_days": 7},
    "golden": {"min_fact_coverage": 0.5, "cases_per_run": 8, "max_usd": 4},
}
_DAYS_PER_MONTH = 30
_WEEK_FILE = re.compile(r"-(\d{4}-W\d{2}|\d{4}-\d{2}-\d{2})\.json$")


def evals_dir() -> Path:
    """data/evals/ (read through c.DATA_DIR so the test sandbox redirects it)."""
    return c.DATA_DIR / "evals"


def settings(config: Path | str | None = None) -> dict:
    """The `evals:` block of config.yaml over DEFAULTS (one level deep)."""
    raw = c.load_yaml(Path(config or c.CONFIG_FILE)).get("evals") or {}
    out = {**DEFAULTS, **{k: v for k, v in raw.items() if not isinstance(v, dict)}}
    for key, default in DEFAULTS.items():
        if isinstance(default, dict):
            out[key] = {**default, **(raw.get(key) or {})}
    return out


def per_run_cap(config: Path | str | None = None) -> float | None:
    """thresholds.max_run_usd, else the monthly cap spread over 30 daily runs."""
    cap = settings(config)["thresholds"].get("max_run_usd")
    if cap is not None:
        return float(cap)
    monthly = (c.load_yaml(Path(config or c.CONFIG_FILE)).get("budget") or {}).get(
        "monthly_cap_usd"
    )
    return round(float(monthly) / _DAYS_PER_MONTH, 4) if monthly is not None else None


def fmt(value: object) -> str:
    """A summary-line value: floats to 3 places, no spaces."""
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value).replace(" ", "_")


def summary_line(name: str, passed: bool, **fields: object) -> str:
    """`EVAL <name> PASS|FAIL k=v ...`: the line a merge gate parses."""
    parts = [f"{k}={fmt(v)}" for k, v in fields.items()]
    return " ".join(["EVAL", name, "PASS" if passed else "FAIL", *parts])


def iso_week(day: datetime) -> str:
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def latest_result(prefix: str, directory: Path | None = None) -> tuple[Path, dict] | None:
    """The newest data/evals/<prefix>-<week or date>.json, by its name's key."""
    found = []
    for path in (directory or evals_dir()).glob(f"{prefix}-*.json"):
        m = _WEEK_FILE.search(path.name)
        if m:
            found.append((m.group(1), path))
    if not found:
        return None
    path = max(found)[1]
    return path, c.load_json(path, default={}) or {}


def is_stale(result: dict, max_age_days: int, now: datetime | None = None) -> bool:
    """True when a result has no `generated` stamp or is older than max_age_days."""
    stamp = str(result.get("generated") or "")
    try:
        made = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return True
    if made.tzinfo is None:
        return True
    return (now or c.utcnow()) - made > timedelta(days=max_age_days)
