#!/usr/bin/env python3
"""
hot_watch.py - between scans, look for a hot incident the site has not called out yet.

The daily scan runs once a day on the Mac, so an incident disclosed just after it waits
up to a day (NGINX2Root, 2026-11-18: disclosed after the 2026-11-18 scan, and no scan
ran before Rohan looked). This watch is the fast path that needs no model and no Mac:
an hourly GitHub Actions job (.github/workflows/hot-watch.yml) reads CISA KEV and the
registered security news feeds named in config.yaml `hot_incidents.watch_sources`,
groups same-story copies the way the scan's story lane does (newsworthy.py), applies
the hot bar (hot_incidents.bar_reasons), and drops anything data/hot_incidents.json
already covers (a shared CVE, or the incident's name in a headline).

What is left is new and hot. With --alert, each one opens a GitHub issue labelled
`hot-incident` in this repo (one per incident: the issue body carries a key, and an
issue already holding that key, open or closed, is never opened again), so Rohan gets
a GitHub notification within the hour. The next scan's hot fast path writes the summary
(research-scan skill, hot-incident step). Nothing is written to the pools or the site.

The issue is public, so it carries only what the feeds already published: each copy's
headline (plain text, no markup, no @mentions), its link (https only) and the CVE ids.
Never log text, never model output.

Usage:
    python scripts/hot_watch.py                # print what is new and hot
    python scripts/hot_watch.py --alert        # ...and open an issue for each
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import timedelta

import aggregate as agg
import common as c
import hot_incidents as hot
import ingest_json_feeds as jf
import newsworthy as nw
import select_batch as sb
import sources_registry as sr

LABEL = "hot-incident"
WATCH_DAYS = 3  # how far back a copy may be published to count
KEY_RE = re.compile(r"<!-- hot-key: ([a-f0-9]{16}) -->")
TITLE_MAX = 160


def watch_sources(conf: c.Config) -> list[dict]:
    """The registry rows named in `hot_incidents.watch_sources` that are active."""
    wanted = [str(x) for x in (conf.hot.get("watch_sources") or []) if isinstance(x, str)]
    by_id = {s["id"]: s for s in sr.load_sources() if s.get("active", True) is not False}
    return [by_id[i] for i in wanted if i in by_id]


def fetch(sources: list[dict], days: int = WATCH_DAYS) -> list[dict]:
    """Recent copies from the watched sources, as staged-candidate-shaped dicts."""
    cutoff = c.utcnow() - timedelta(days=days)
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    out: list[dict] = []
    for source in sources:
        if source.get("type") == "kev_json":
            data = jf.fetch_json(source["handle"])
            if isinstance(data, dict):
                out += jf.kev_candidates(data, source, rules, cutoff)
            continue
        feed = agg.feed_from_source(source)
        parsed = agg.parse_feed(feed["url"])
        for entry in parsed.entries or []:
            if not c.in_ingest_window(c.entry_datetime(entry), cutoff, None):
                continue
            title = c.clean_summary(entry.get("title", ""), 300)
            link = entry.get("link") or ""
            if not title or not link:
                continue
            published = c.entry_datetime(entry)
            out.append(
                {
                    "id": c.make_id(title, c.normalize_url(link)),
                    "title": title,
                    "excerpt": c.clean_summary(entry.get("summary", ""), 320),
                    "source_url": link,
                    "published": published.strftime("%Y-%m-%d") if published else "",
                    "source_id": source["id"],
                    "source_rank": source.get("rank"),
                    "source_name": source.get("name", ""),
                }
            )
    return out


def covered(group: list[dict], ids: set[str], incidents: list[dict]) -> bool:
    """data/hot_incidents.json already has this story: a shared CVE, or an incident's
    name in one of the copies' headlines."""
    for inc in incidents:
        if ids & {str(x).lower() for x in inc.get("cves") or []}:
            return True
        name = str(inc.get("name") or "")
        if name and any(re.search(re.escape(name), x.get("title") or "", re.I) for x in group):
            return True
    return False


def detect(cands: list[dict], conf: c.Config, incidents: list[dict], reference=None) -> list[dict]:
    """New hot stories among `cands`: [{key, title, reasons, cves, copies}]."""
    if not cands:
        return []
    reference = sb.reference_docs() if reference is None else reference
    sigs = nw.analyze(cands, reference, nw.publisher, [])
    pos = {id(x): i for i, x in enumerate(cands)}
    out = []
    for group in sb.story_groups(cands, sigs, pos):
        reasons = sb.hot_reasons(cands, sigs, group, conf)
        if not reasons:
            continue
        copies = [cands[k] for k in group]
        ids = set().union(*(sigs[k].ids for k in group))
        if covered(copies, ids, incidents):
            continue
        copies.sort(key=lambda x: -(float(x.get("source_rank") or 0)))
        cves = sorted(i.upper() for i in ids if i.startswith("cve-"))
        anchor = ",".join(cves) or plain(copies[0].get("title")).lower()
        out.append(
            {
                "key": hashlib.sha256(anchor.encode()).hexdigest()[:16],
                "title": plain(copies[0].get("title")),
                "reasons": reasons,
                "cves": cves,
                "copies": [
                    {"title": plain(x.get("title")), "url": x.get("source_url") or ""}
                    for x in copies
                    if hot._https(x.get("source_url"))
                ],
            }
        )
    return out


def plain(text: object) -> str:
    """A feed headline as inert plain text for a public issue."""
    out = " ".join(str(text or "").split())
    out = re.sub(r"[\x00-\x1f<>\[\]()`*_|\\#!]", "", out)
    out = out.replace("@", "@​")  # never a GitHub mention
    return out[:TITLE_MAX]


def issue_body(item: dict) -> str:
    lines = [
        f"A new incident clears the hot bar: {hot.reasons_text(item['reasons'])}.",
        "",
        f"CVEs: {', '.join(item['cves']) or 'none named yet'}",
        "",
        "Covered by:",
        *[f"- {x['title']}: {x['url']}" for x in item["copies"]],
        "",
        f"Bar: {hot.BAR_NOTE}",
        "",
        "The next daily scan writes the summary (root cause, conditions, exploitation, fix) "
        "into data/hot_incidents.json. To get it sooner, run the scan now.",
        "",
        f"<!-- hot-key: {item['key']} -->",
    ]
    return "\n".join(lines)


def _gh(*args: str, body: dict | None = None) -> str:
    cmd = ["gh", "api", *args]
    res = subprocess.run(
        cmd,
        input=json.dumps(body) if body is not None else None,
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        raise RuntimeError(f"gh api {args[0]} failed: {res.stderr.strip()[:200]}")
    return res.stdout


def known_keys(repo: str) -> set[str]:
    raw = _gh(f"repos/{repo}/issues?state=all&labels={LABEL}&per_page=100")
    return {m for issue in json.loads(raw or "[]") for m in KEY_RE.findall(issue.get("body") or "")}


def alert(items: list[dict], repo: str) -> int:
    """Open one `hot-incident` issue per new item; returns how many were opened."""
    if not items:
        return 0
    try:
        _gh(f"repos/{repo}/labels", "--method", "POST", "--input", "-",
            body={"name": LABEL, "color": "b60205", "description": "A hot incident to call out"})  # fmt: skip
    except RuntimeError as exc:
        if "already_exists" not in str(exc):
            raise
    seen = known_keys(repo)
    opened = 0
    for item in items:
        if item["key"] in seen:
            continue
        title = f"Hot incident: {item['title']}"[:200]
        _gh(f"repos/{repo}/issues", "--method", "POST", "--input", "-",
            body={"title": title, "body": issue_body(item), "labels": [LABEL]})  # fmt: skip
        opened += 1
    return opened


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--alert", action="store_true", help="open a GitHub issue for each")
    ap.add_argument("--repo", default="", help="owner/name (default: GITHUB_REPOSITORY)")
    args = ap.parse_args(argv)
    conf = c.load_config()
    sources = watch_sources(conf)
    if not sources:
        print("hot watch: no watch_sources in config.yaml; nothing to do")
        return 0
    items = detect(fetch(sources), conf, hot.load())
    for item in items:
        print(f"HOT ({', '.join(item['reasons'])}): {item['title']} [{len(item['copies'])} copies]")
    print(f"hot watch: {len(items)} new hot incident(s) from {len(sources)} sources")
    if args.alert and items:
        repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
        if not re.match(r"^[\w.-]+/[\w.-]+$", repo):
            print("hot watch: --alert needs --repo owner/name or GITHUB_REPOSITORY")
            return 2
        print(f"hot watch: opened {alert(items, repo)} issue(s)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
