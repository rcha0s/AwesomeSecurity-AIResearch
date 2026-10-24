#!/usr/bin/env python3
"""
trends.py — Detect emerging themes per topic and render TRENDS.md.

Clusters entries (live pool + recent archive) by their `tags` within each topic
and keeps tags that have enough members from enough distinct sources. Each theme
then gets a `state`, judged against its own history:

    rising   recent count >= rising_min_recent AND > rising_ratio x its baseline
    steady   it has recent findings, but no more than its baseline predicts
    quiet    no findings inside the recent window

"Recent" is a dated finding inside `max_age_days`. The baseline is the tag's
count over the `trends.baseline_days` before the window (or the topic's whole
history before it, if that is shorter), scaled to the window's length: the
number of recent findings the tag would have at its usual rate. Tags that name
a source, host or feed ("arxiv", "ghsa", a registered source's name or site)
are not themes and are dropped. Writes data/trends.json (machine) + TRENDS.md.

`momentum` is the recent count's excess over the baseline for a rising theme and
0 otherwise (`excess` keeps the signed value), so anything that reads
`momentum > 0` as "rising" agrees with `state`.

Usage:
    python scripts/trends.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime, timedelta
from urllib.parse import urlparse

import common as c
import sources_registry as sr

MIN_MEMBERS = 2  # a theme needs at least this many findings
MIN_SOURCES = 2  # …from at least this many distinct sources
STATES = ("rising", "steady", "quiet")  # also the render order
TREND_DEFAULTS = {
    "baseline_days": 180,
    "rising_ratio": 1.0,
    "rising_min_recent": 2,
    "exclude_tags": [],
}
# Host labels too generic to name a source ("blog.google" -> "blog").
GENERIC_HOST_LABELS = frozenset({"www", "blog", "blogs", "feeds", "feed", "rss", "news"})
STATE_MARK = {"rising": "🔺 rising", "steady": "▪️ steady", "quiet": "▫️ quiet"}


def trend_settings(raw: dict | None = None) -> dict:
    """config.yaml's `trends:` block over the defaults."""
    if raw is None:
        raw = (c.load_yaml(c.CONFIG_FILE) or {}).get("trends") or {}
    return {**TREND_DEFAULTS, **raw}


def entries_for_topic(topic: str) -> list[dict]:
    live = c.load_pool(topic)["entries"]
    archive = [
        e for e in (c.load_json(c.ARCHIVE_FILE, default=[]) or []) if e.get("topic") == topic
    ]
    seen, out = set(), []
    for e in live + archive:
        key = e.get("id") or e.get("source_url")
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def source_key(e: dict) -> str:
    return e.get("source_id") or e.get("source_name") or e.get("source_url", "")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def _site_label(url: str) -> str:
    """The registrable label of a URL's host: unit42.paloaltonetworks.com ->
    paloaltonetworks, export.arxiv.org -> arxiv, blog.google -> google."""
    labels = [x for x in (urlparse(url).hostname or "").split(".") if x]
    if len(labels) >= 3 and labels[-2] in ("co", "gov", "ac", "org", "com"):
        labels = labels[:-1]  # gov.uk, co.uk
    picks = [x for x in labels[:-1] if x not in GENERIC_HOST_LABELS] or labels[-1:]
    return picks[-1] if picks else ""


def source_tags(sources: list[dict], extra: list[str]) -> set[str]:
    """Every tag that names a source rather than a theme: the registry's names,
    handles and sites, plus the configured `exclude_tags`."""
    out = {_slug(x) for x in extra}
    for s in sources:
        out.add(_slug(s.get("name", "")))
        for value in (s.get("url"), s.get("handle")):
            if not value:
                continue
            out.add(_site_label(value) if "://" in value else _slug(value.lstrip("@")))
    return {x for x in out if x}


def _day(entry: dict) -> datetime | None:
    return c.parse_date_end(c.best_date(entry))


def classify(recent: int, expected: float, settings: dict) -> str:
    """rising / steady / quiet — see the module docstring."""
    if recent == 0:
        return "quiet"
    rising = recent >= int(settings["rising_min_recent"]) and recent > float(
        settings["rising_ratio"]
    ) * float(expected)
    return "rising" if rising else "steady"


def baseline_expected(
    days: list[datetime],
    window_start: datetime,
    history_start: datetime | None,
    window: int,
    settings: dict,
) -> float:
    """How many findings this tag would have in a `window`-day span at its
    baseline rate (its count over the baseline period before the window)."""
    if history_start is None:
        return 0.0
    span = min(int(settings["baseline_days"]), (window_start - history_start).days)
    if span <= 0:
        return 0.0
    since = window_start - timedelta(days=span)
    before = sum(1 for d in days if since <= d < window_start)
    return before * window / span


def _member_view(m: dict, conf: c.Config, now: datetime) -> dict:
    return {
        "title": m.get("title"),
        "url": m.get("source_url"),
        "date": c.best_date(m),
        "fresh": c.is_fresh(m, conf.max_age_days, now=now),
    }


def _trend_row(topic, tag, members, conf, now, history_start, settings) -> dict:
    window_start = now - timedelta(days=conf.max_age_days)
    days = [d for d in (_day(m) for m in members) if d is not None]
    recent = sum(1 for d in days if d >= window_start)
    expected = baseline_expected(days, window_start, history_start, conf.max_age_days, settings)
    state = classify(recent, expected, settings)
    excess = round(recent - expected, 1)
    dates = [c.best_date(m) for m in members if c.best_date(m)]
    return {
        "topic": topic,
        "tag": tag,
        "count": len(members),
        "recent": recent,
        "baseline": round(expected, 1),
        "state": state,
        "excess": excess,
        "momentum": excess if state == "rising" else 0.0,
        "sources": len({source_key(m) for m in members}),
        "first_seen": min(dates) if dates else None,
        "last_seen": max(dates) if dates else None,
        "members": [
            _member_view(m, conf, now)
            for m in sorted(members, key=lambda x: (c.best_date(x) or ""), reverse=True)
        ],
    }


def _rank(t: dict) -> tuple:
    """Rising first (biggest excess first), then steady, then quiet; within a
    state, more recent findings, then more findings overall."""
    return (STATES.index(t["state"]), -t["momentum"], -t["recent"], -t["count"], t["tag"])


def build_trends(
    topic: str,
    conf: c.Config,
    now: datetime,
    settings: dict | None = None,
    excluded: set[str] | None = None,
) -> list[dict]:
    settings = trend_settings(settings)
    if excluded is None:
        excluded = source_tags(sr.load_sources(), settings["exclude_tags"])
    entries = entries_for_topic(topic)
    by_tag: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        for tag in {t.lower() for t in e.get("tags") or []}:
            if _slug(tag) not in excluded:
                by_tag[tag].append(e)
    all_days = [d for d in (_day(e) for e in entries) if d is not None]
    history_start = min(all_days) if all_days else None
    trends = [
        _trend_row(topic, tag, members, conf, now, history_start, settings)
        for tag, members in by_tag.items()
        if len(members) >= MIN_MEMBERS and len({source_key(m) for m in members}) >= MIN_SOURCES
    ]
    trends.sort(key=_rank)
    return trends


def _header(settings: dict, now: str, window: int) -> list[str]:
    return [
        "# 📈 Emerging Trends",
        "",
        f"> Themes per topic, clustered from tagged findings (live + recent archive). "
        f"Updated {now}. A theme needs ≥{MIN_MEMBERS} findings from ≥{MIN_SOURCES} "
        f"sources. **Rising** means at least {settings['rising_min_recent']} findings in "
        f"the last {window} days and more than {settings['rising_ratio']}x what the theme's "
        f"own rate over the prior {settings['baseline_days']} days predicts; **steady** has "
        "recent findings at or under that rate; **quiet** has none. Source and feed names "
        "(arxiv, ghsa, ...) are not themes.",
        "",
    ]


def render_md(
    all_trends: dict[str, list[dict]], now: str, settings: dict | None = None, window: int = 31
) -> str:
    settings = trend_settings(settings)
    out = _header(settings, now, window)
    for topic, meta in c.TOPICS.items():
        trends = all_trends.get(topic, [])
        out += [f"## {meta['name']}", ""]
        if not trends:
            out += ["_No theme has crossed the threshold yet — needs more volume._", ""]
            continue
        for t in trends:
            out.append(
                f"### {STATE_MARK.get(t.get('state'), '▪️')} {t['tag']}  ·  {t['count']} findings "
                f"({t['recent']} recent vs {t.get('baseline', 0)} expected) · "
                f"{t['sources']} sources"
            )
            if t["first_seen"]:
                out.append(f"_First seen {t['first_seen']} · latest {t['last_seen']}._")
            out.append("")
            for m in t["members"][:6]:
                tag = " · _latest_" if m["fresh"] else ""
                out.append(f"- [{m['title']}]({m['url']}) ({m['date']}){tag}")
            out.append("")
    out += ["---", "", f"<sub>Generated by scripts/trends.py on {now}.</sub>", ""]
    return "\n".join(out)


def main() -> int:
    conf = c.load_config()
    settings = trend_settings()
    excluded = source_tags(sr.load_sources(), settings["exclude_tags"])
    now_dt = c.utcnow()
    now = now_dt.strftime("%Y-%m-%d")
    all_trends = {t: build_trends(t, conf, now_dt, settings, excluded) for t in c.TOPICS}
    c.save_json(c.DATA_DIR / "trends.json", all_trends)
    (c.ROOT / "TRENDS.md").write_text(
        render_md(all_trends, now, settings, conf.max_age_days), encoding="utf-8"
    )
    total = sum(len(v) for v in all_trends.values())
    rising = sum(t["state"] == "rising" for v in all_trends.values() for t in v)
    print(f"Detected {total} theme(s), {rising} rising, across {len(c.TOPICS)} topics -> TRENDS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
