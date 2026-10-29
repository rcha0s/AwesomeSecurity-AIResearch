#!/usr/bin/env python3
"""
arguments.py — "What practitioners are arguing": the committed, grounded rows behind
the Briefing section.

The raw signal never reaches the public site: Reddit self posts sit in the gitignored
data/_practitioner_signal.json, and X / Reddit link posts ride on candidates and pool
entries. The daily scan session reads them (`signal`), writes at most a handful of
arguments to data/_arguments_out.json, and `merge` validates them into the committed
data/arguments.json. The model supplies only prose and URLs. Everything else is code:

  * each source URL must be a Reddit thread or an X post permalink AND appear in the
    signal frozen by `pre` before the session started (the Reddit signal file and the
    staged candidates; `signal` and `merge` read only that frozen, session-proof file);
  * position and counterpoint may not contain a URL, `www.` or a bare domain;
  * the stored URL, label (r/sub or @handle) and engagement come from the signal, never
    from the model;
  * a position is one sentence of at most `text_max_chars`; a row needs `min_sources`
    distinct threads or posts; at most `max_new_per_run` rows are taken per run.

Engagement weight (documented in AGENTS.md):
    Reddit thread  = score + 2 x comments
    X              = `x_author_weight` per distinct author (the X list lane captures no
                     like or reply counts, so this is count-based, not engagement-based)
    row weight     = sum of both; the section ranks by it.

Rows age out `row_days` after the day they were written. merge_gate.py runs
`content_checks.arguments_problems` on every scan PR, which re-checks the shape, the
hosts and the weight arithmetic (it cannot see the gitignored signal).

Usage:
    python scripts/arguments.py freeze    # `pre`: freeze the signal into data/_scan_arguments_signal.json
    python scripts/arguments.py signal    # compact view of this run's signal, best first
    python scripts/arguments.py merge     # data/_arguments_out.json -> data/arguments.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, timedelta

import common as c

OUT_NAME = "_arguments_out.json"
ROWS_NAME = "arguments.json"
SIGNAL_NAME = "_practitioner_signal.json"
FROZEN_NAME = "_scan_arguments_signal.json"  # code-owned: Edit(data/_scan*) is denied
DEFAULTS = {
    "max_new_per_run": 5,  # rows taken from one run's staging file
    "max_rows": 5,  # rows the site shows
    "store_max": 10,  # rows kept in data/arguments.json (best weight first)
    "row_days": 14,  # a row leaves the file and the page this many days after it was written
    "min_sources": 2,
    "max_sources": 6,
    "text_max_chars": 280,
    "x_author_weight": 25,
    "signal_rows": 40,  # `signal` prints this many
    "signal_days": 14,  # entries older than this are not signal
}
_SEG = r"[A-Za-z0-9_%.\-]+"
REDDIT_RE = re.compile(
    rf"^https?://(?:www\.|old\.|np\.)?reddit\.com/r/([A-Za-z0-9_]{{2,21}})/comments/([a-z0-9]{{4,10}})(?:/{_SEG})*/?$",
    re.I | re.ASCII,  # ASCII: no dotless i or Kelvin sign standing in for i / k
)
X_RE = re.compile(
    r"^https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/status/(\d{5,25})/?$",
    re.I | re.ASCII,
)
# A link-like string in prose: a scheme, www., or a bare domain. A position is a claim,
# never a lure, so any of these refuses the text.
LINKISH = re.compile(
    r"://|\bwww\.|\b[a-z0-9-]+\.(?:com|io|net|org|dev|ai|xyz|co|app|sh|me|info|biz|us|uk|gg|ly)\b",
    re.I | re.ASCII,
)
ROW_KEYS = {
    "id",
    "created",
    "position",
    "counterpoint",
    "sources",
    "reddit_score",
    "reddit_comments",
    "x_authors",
    "weight",
}
SOURCE_KEYS = {"url", "label", "kind"}
MAX_COUNT = 10_000_000
_CTRL = re.compile(r"[\x00-\x1f\x7f]+")


def settings() -> dict:
    return {**DEFAULTS, **((c.load_yaml(c.CONFIG_FILE) or {}).get("arguments") or {})}


def parse_source(url: object) -> dict | None:
    """{kind, key, label} for a Reddit thread or X post permalink, else None."""
    text = url if isinstance(url, str) else ""
    if m := REDDIT_RE.fullmatch(text):
        return {"kind": "reddit", "key": f"reddit:{m.group(2).lower()}", "label": f"r/{m.group(1)}"}
    if m := X_RE.fullmatch(text):
        return {"kind": "x", "key": f"x:{m.group(2)}", "label": f"@{m.group(1)}"}
    return None


def x_handle(label: str) -> str:
    return label.lstrip("@").lower()


def weight_of(score: int, comments: int, authors: int, cfg: dict) -> int:
    return score + 2 * comments + authors * int(cfg["x_author_weight"])


def clean_text(value: object, cfg: dict) -> str | None:
    """One line of prose, within the length limit; None when empty or too long."""
    text = _CTRL.sub(" ", value).strip() if isinstance(value, str) else ""
    if not text or len(text) > int(cfg["text_max_chars"]) or LINKISH.search(text):
        return None
    return text


# --- The signal: what a source URL may point at -----------------------------------
def _num(value: object) -> int:
    try:
        return max(0, min(int(value or 0), MAX_COUNT))
    except (TypeError, ValueError):
        return 0


def _signal_item(url: str, title: str, score: int, comments: int) -> dict | None:
    src = parse_source(url)
    if src is None:
        return None
    return {**src, "url": url.strip(), "title": title, "score": score, "comments": comments}


def _recent(stamp: object, cfg: dict) -> bool:
    cutoff = (c.utcnow() - timedelta(days=int(cfg["signal_days"]))).date().isoformat()
    return not isinstance(stamp, str) or stamp[:10] >= cutoff


def _from_entry(row: dict, cfg: dict) -> list[dict]:
    """Signal items on a candidate or pool entry: its Reddit thread, its X post."""
    if not isinstance(row, dict) or not _recent(row.get("published") or row.get("date"), cfg):
        return []
    title = str(row.get("title") or "")
    items = [
        _signal_item(
            str(row.get("reddit_url") or ""),
            title,
            _num(row.get("reddit_score")),
            _num(row.get("reddit_comments")),
        )
    ]
    if row.get("discovered_via") == "x-list":
        items.append(_signal_item(str(row.get("tweet_url") or ""), title, 0, 0))
    return [i for i in items if i]


def build_signal(cfg: dict) -> dict[str, dict]:
    """Every thread or post this run may cite, by key, from the Reddit signal file and the
    staged candidates (Reddit links, X list posts). A repeat keeps the larger counts.
    Pool entries are not read: the session can edit them."""
    items: list[dict] = []
    for row in c.load_json(c.DATA_DIR / SIGNAL_NAME, default=[]) or []:
        if isinstance(row, dict) and _recent(row.get("created"), cfg):
            item = _signal_item(
                str(row.get("permalink") or ""),
                str(row.get("title") or ""),
                _num(row.get("score")),
                _num(row.get("comments")),
            )
            items += [item] if item else []
    for row in c.load_json(c.CANDIDATES_FILE, default=[]) or []:
        items += _from_entry(row, cfg)
    out: dict[str, dict] = {}
    for item in items:
        old = out.get(item["key"])
        if old is None or (item["score"], item["comments"]) > (old["score"], old["comments"]):
            out[item["key"]] = item
    return out


def load_signal(cfg: dict) -> dict[str, dict]:
    """The signal frozen by `freeze` in `pre`, before the session started. It is the only
    signal `signal` and `merge` read: the session can edit the files it was built from."""
    frozen = c.load_json(c.DATA_DIR / FROZEN_NAME, default=[]) or []
    out: dict[str, dict] = {}
    for item in frozen if isinstance(frozen, list) else []:
        info = parse_source(item.get("url")) if isinstance(item, dict) else None
        if info is not None:
            out[info["key"]] = {
                **info,
                "url": item["url"],
                "title": str(item.get("title") or ""),
                "score": _num(item.get("score")),
                "comments": _num(item.get("comments")),
            }
    return out


def engagement(item: dict, cfg: dict) -> int:
    if item["kind"] == "x":
        return int(cfg["x_author_weight"])
    return item["score"] + 2 * item["comments"]


# --- Rows ----------------------------------------------------------------------------
def build_row(
    raw: object, signal: dict[str, dict], cfg: dict, today: str
) -> tuple[dict | None, str]:
    """(row, "") from one staged argument, or (None, why it was dropped)."""
    if not isinstance(raw, dict):
        return None, "not an object"
    position = clean_text(raw.get("position"), cfg)
    if position is None:
        return None, "position empty or over the length limit"
    counter = raw.get("counterpoint")
    counterpoint = clean_text(counter, cfg) if counter else ""
    if counterpoint is None:
        return None, "counterpoint over the length limit"
    sources: dict[str, dict] = {}
    for url in raw.get("sources") if isinstance(raw.get("sources"), list) else []:
        src = parse_source(url)
        if src is None:
            return None, "a source is not a Reddit or X permalink"
        if src["key"] not in signal:
            return None, "a source is not in this run's signal"
        sources.setdefault(src["key"], signal[src["key"]])
    if not int(cfg["min_sources"]) <= len(sources) <= int(cfg["max_sources"]):
        return None, f"needs {cfg['min_sources']}-{cfg['max_sources']} distinct sources"
    reddit = [s for s in sources.values() if s["kind"] == "reddit"]
    authors = {x_handle(s["label"]) for s in sources.values() if s["kind"] == "x"}
    score, comments = sum(s["score"] for s in reddit), sum(s["comments"] for s in reddit)
    digest = hashlib.sha1("|".join(sorted(sources)).encode()).hexdigest()[:10]
    return {
        "id": f"arg-{digest}",
        "created": today,
        "position": position,
        "counterpoint": counterpoint,
        "sources": [
            {"url": s["url"], "label": s["label"], "kind": s["kind"]}
            for s in sorted(sources.values(), key=lambda s: -engagement(s, cfg))
        ],
        "reddit_score": score,
        "reddit_comments": comments,
        "x_authors": len(authors),
        "weight": weight_of(score, comments, len(authors), cfg),
    }, ""


def live(rows: object, today: str, cfg: dict) -> list[dict]:
    """The rows still inside `row_days`, best weight first. Hostile shapes are dropped."""
    cutoff = (date.fromisoformat(today) - timedelta(days=int(cfg["row_days"]))).isoformat()
    kept = [
        r
        for r in (rows if isinstance(rows, list) else [])
        if isinstance(r, dict) and isinstance(r.get("created"), str) and r["created"] >= cutoff
    ]
    return sorted(kept, key=lambda r: (-_num(r.get("weight")), str(r.get("id"))))


def merge_rows(existing: list, staged: object, signal: dict, cfg: dict, today: str):
    """(rows to store, notes). A new row replaces an old one that shares a source."""
    notes: list[str] = []
    new: list[dict] = []
    for i, raw in enumerate(staged if isinstance(staged, list) else []):
        if len(new) >= int(cfg["max_new_per_run"]):
            notes.append(f"argument {i}: over max_new_per_run, dropped")
            continue
        row, why = build_row(raw, signal, cfg, today)
        if row is None:
            notes.append(f"argument {i}: {why}")
        else:
            new.append(row)
    taken = {s["url"] for r in new for s in r["sources"]}
    kept = [
        r
        for r in live(existing, today, cfg)
        if not taken & {s.get("url") for s in r.get("sources") or [] if isinstance(s, dict)}
        and r.get("id") not in {n["id"] for n in new}
    ]
    rows = sorted(kept + new, key=lambda r: (-r["weight"], r["id"]))
    return rows[: int(cfg["store_max"])], notes


def shown(rows: object, now: str, cfg: dict) -> list[dict]:
    """The rows the page renders: live, best first, `max_rows`, numbers and links re-checked."""
    out = []
    for row in live(rows, now[:10], cfg):
        if not row_problems(row, cfg):
            out.append(row)
    return out[: int(cfg["max_rows"])]


def row_problems(row: dict, cfg: dict | None = None) -> list[str]:
    """Why a stored row is malformed; [] when sound. Shared by the renderer and the gate."""
    cfg = cfg or settings()
    if not isinstance(row, dict) or set(row) != ROW_KEYS:
        return ["row keys are not exactly the argument schema"]
    out = []
    if not (isinstance(row["id"], str) and re.fullmatch(r"arg-[0-9a-f]{10}", row["id"])):
        out.append("bad id")
    try:
        if date.fromisoformat(row["created"]) > c.utcnow().date() + timedelta(days=1):
            out.append("created is in the future")
    except (TypeError, ValueError):
        out.append("created is not a date")
    for key in ("position", "counterpoint"):
        text = row[key]
        if not isinstance(text, str) or len(text) > int(cfg["text_max_chars"]):
            out.append(f"{key} is not text within the limit")
        elif LINKISH.search(text):
            out.append(f"{key} contains a link or domain")
    if not row["position"] if isinstance(row["position"], str) else True:
        out.append("position is empty")
    counts = _count_problems(row)
    if counts:  # weight arithmetic below needs real integers
        return out + counts
    return out + _source_problems(row, cfg)


def _count_problems(row: dict) -> list[str]:
    bad = [
        k
        for k in ("reddit_score", "reddit_comments", "x_authors", "weight")
        if isinstance(row[k], bool)
        or not isinstance(row[k], int)
        or not 0 <= row[k] <= MAX_COUNT * 10
    ]
    return [f"{k} is not a count" for k in bad]


def _source_problems(row: dict, cfg: dict) -> list[str]:
    srcs = row["sources"]
    if not isinstance(srcs, list) or not int(cfg["min_sources"]) <= len(srcs) <= int(
        cfg["max_sources"]
    ):
        return ["sources count is outside the limits"]
    keys, authors = set(), set()
    for s in srcs:
        info = parse_source(s.get("url")) if isinstance(s, dict) else None
        if info is None or set(s) != SOURCE_KEYS:
            return ["a source is not a Reddit or X permalink"]
        if s["kind"] != info["kind"] or s["label"] != info["label"]:
            return ["a source label or kind disagrees with its URL"]
        keys.add(info["key"])
        authors |= {x_handle(info["label"])} if info["kind"] == "x" else set()
    problems = [] if len(keys) == len(srcs) else ["a source is repeated"]
    if len(authors) != row["x_authors"]:
        problems.append("x_authors disagrees with the X sources")
    expect = weight_of(row["reddit_score"], row["reddit_comments"], row["x_authors"], cfg)
    if row["weight"] != expect:
        problems.append("weight is not score + 2 x comments + x authors x weight")
    return problems


# --- CLI -----------------------------------------------------------------------------
def cmd_signal(cfg: dict) -> int:
    items = sorted(load_signal(cfg).values(), key=lambda i: -engagement(i, cfg))
    for item in items[: int(cfg["signal_rows"])]:
        print(
            json.dumps(
                {
                    "url": item["url"],
                    "label": item["label"],
                    "title": item["title"][:200],
                    "score": item["score"],
                    "comments": item["comments"],
                },
                ensure_ascii=False,
            )
        )
    print(f"arguments: {len(items)} thread(s) or post(s) in this run's signal", file=sys.stderr)
    return 0


def cmd_freeze(cfg: dict) -> int:
    """Write the signal the session may cite to data/_scan_arguments_signal.json. Run by
    `pre` before the session starts; the session cannot Edit data/_scan* files."""
    items = list(build_signal(cfg).values())
    keep = ("url", "title", "score", "comments")
    c.save_json(c.DATA_DIR / FROZEN_NAME, [{k: i[k] for k in keep} for i in items])
    print(f"arguments: froze {len(items)} thread(s) or post(s)")
    return 0


def cmd_merge(cfg: dict) -> int:
    today = c.utcnow().date().isoformat()
    staged = c.load_json(c.DATA_DIR / OUT_NAME, default=[])
    path = c.DATA_DIR / ROWS_NAME
    rows, notes = merge_rows(c.load_json(path, default=[]), staged, load_signal(cfg), cfg, today)
    c.save_json(path, rows)
    for note in notes:
        print(f"arguments: {note}")
    print(f"arguments: {len(rows)} row(s) stored ({len(notes)} staged argument(s) dropped)")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    cfg = settings()
    if args == ["signal"]:
        return cmd_signal(cfg)
    if args == ["merge"]:
        return cmd_merge(cfg)
    if args == ["freeze"]:
        return cmd_freeze(cfg)
    print(__doc__.split("Usage:")[1].strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
