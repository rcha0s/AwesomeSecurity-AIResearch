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
`hot-incident` in this repo, so Rohan gets a GitHub notification within the hour. One
issue per incident: the body carries a key for each CVE and each copy's URL, and an
incident sharing ANY key with an issue already opened (open or closed) is the same
incident, so a CVE assigned later or a new outlet never opens a second issue. The next scan's hot fast path writes the summary
(research-scan skill, hot-incident step). Nothing is written to the pools or the site.

The issue is public, so it carries only what the feeds already published: each copy's
headline (plain text, no markup, no @mentions), its link (https only) and the CVE ids.
The job log prints those public headlines and nothing else; no model runs here.

If no watched source returns anything (all feeds down, or every id in watch_sources
wrong), the job exits non-zero so the failure shows in Actions instead of a quiet 0.

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
KEY_RE = re.compile(r"<!-- hot-key: ([a-z0-9-]{1,40}) -->")
TITLE_MAX = 160


def watch_sources(conf: c.Config) -> list[dict]:
    """The registry rows named in `hot_incidents.watch_sources` that are active."""
    wanted = [str(x) for x in (conf.hot.get("watch_sources") or []) if isinstance(x, str)]
    by_id = {s["id"]: s for s in sr.load_sources() if s.get("active", True) is not False}
    for missing in (i for i in wanted if i not in by_id):
        print(f"hot watch: watch_sources id {missing} is not an active registry source")
    return [by_id[i] for i in wanted if i in by_id]


def fetch(sources: list[dict], days: int = WATCH_DAYS) -> tuple[list[dict], int]:
    """(recent copies from the watched sources as staged-candidate-shaped dicts, how
    many sources answered at all). A dead feed is skipped, never fatal."""
    cutoff = c.utcnow() - timedelta(days=days)
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    out: list[dict] = []
    answered = 0
    for source in sources:
        if source.get("type") == "kev_json":
            data = jf.fetch_json(source["handle"])
            if isinstance(data, dict):
                answered += 1
                out += jf.kev_candidates(data, source, rules, cutoff)
            continue
        feed = agg.feed_from_source(source)
        parsed = agg.parse_feed(feed["url"])
        if parsed.entries:
            answered += 1
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
    return out, answered


def keys_for(cves: list[str], urls: list[str]) -> list[str]:
    """Stable identity markers: one per CVE and one per copy URL. Two runs that share
    any marker are the same incident, however the story grouped or got renamed."""
    out = [cve.lower() for cve in cves]
    out += ["url-" + hashlib.sha256(c.normalize_url(u).encode()).hexdigest()[:16] for u in urls]
    return out


def detect(cands: list[dict], conf: c.Config, incidents: list[dict], reference=None) -> list[dict]:
    """New hot stories among `cands`: [{keys, title, reasons, cves, copies}]."""
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
        if hot.covered([str(x.get("title") or "") for x in copies], ids, incidents):
            continue
        copies.sort(key=lambda x: -(float(x.get("source_rank") or 0)))
        cves = sorted(i.upper() for i in ids if i.startswith("cve-"))
        out.append(
            {
                "keys": keys_for(
                    cves, [x.get("source_url") or "" for x in copies if x.get("source_url")]
                ),
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
        *[f"<!-- hot-key: {k} -->" for k in item["keys"]],
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
        # gh puts the API's error body (e.g. "already_exists") on stdout, not stderr.
        detail = f"{res.stderr.strip()} {res.stdout.strip()}"[:400]
        raise RuntimeError(f"gh api {args[0]} failed: {detail}")
    return res.stdout


def known_keys(repo: str) -> set[str]:
    """Every key in every `hot-incident` issue, open or closed, all pages."""
    raw = _gh(
        f"repos/{repo}/issues?state=all&labels={LABEL}&per_page=100",
        "--paginate",
        "--jq",
        ".[].body | @json",
    )
    bodies = [json.loads(line) for line in raw.splitlines() if line.strip()]
    return {m for body in bodies for m in KEY_RE.findall(body or "")}


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
        if seen & set(item["keys"]):
            continue
        title = f"Hot incident: {item['title']}"[:200]
        _gh(f"repos/{repo}/issues", "--method", "POST", "--input", "-",
            body={"title": title, "body": issue_body(item), "labels": [LABEL]})  # fmt: skip
        seen |= set(item["keys"])  # a second group of the same incident in this run
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
    cands, answered = fetch(sources)
    if not answered:
        print(f"hot watch: none of the {len(sources)} watched sources answered; failing")
        return 1
    items = detect(cands, conf, hot.load())
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
