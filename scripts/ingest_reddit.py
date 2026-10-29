#!/usr/bin/env python3
"""
ingest_reddit.py — Subreddit threads as practitioner signal, keyless and logged out.

Reddit's JSON, RSS and API endpoints all answer 403 without a key. The one keyless
door is the server-rendered partial the site loads for "more posts":

    https://www.reddit.com/svc/shreddit/community-more-posts/{sort}/?name={sub}

It returns HTML; each post is a `<shreddit-post ...>` start tag whose attributes
carry `permalink`, `content-href`, `post-title`, `score`, `comment-count`,
`created-timestamp` and `post-type`. Attributes are read with the stdlib HTML
parser. Never a logged-in session, never a browser.

A Reddit thread alone never becomes a finding:
  * a link post whose `content-href` is not a Reddit host stages that ARTICLE as
    the candidate's `source_url`; the thread rides along as `reddit_url`,
    `reddit_score`, `reddit_comments` and `discovered_via: "reddit"`;
  * a self/text post is not staged. It is recorded in the gitignored
    data/_practitioner_signal.json (title, permalink, score, comments, sub, created)
    for the "what practitioners are arguing" section;
  * merge_analysis.py holds any entry whose only citations are Reddit URLs.

Per sub it makes one request per sort (config.yaml `reddit`), keeps posts from the
last `lookback_hours` that pass the on-thesis filter the curator ingestor uses, and
stages at most `max_per_run` links, best engagement first. It fails soft: a 403,
429 or network error is logged and the exit code stays 0, so a scan never fails
because of Reddit.

Usage:
    python scripts/ingest_reddit.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path

import aggregate as agg
import common as c
import eval_recall as er
import ingest_curator_links as icl
import taxonomy as tx

SOURCE_PREFIX = "reddit"
BASE = "https://www.reddit.com"
ENDPOINT = BASE + "/svc/shreddit/community-more-posts/{sort}/"
# A normal desktop browser agent: the endpoint serves the site's own page loads.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
SIGNAL_NAME = "_practitioner_signal.json"
DEFAULTS = {
    "subreddits": [],
    "sorts": ["new"],
    "lookback_hours": 48,
    "timeout_seconds": 15,
    "delay_seconds": 1.0,
    "max_per_run": 6,
    "min_score": 2,
    "source_rank": 55.0,
    "signal_days": 14,
}


def signal_file() -> Path:
    return c.DATA_DIR / SIGNAL_NAME


def settings() -> dict:
    cfg = (c.load_yaml(c.CONFIG_FILE) or {}).get("reddit") or {}
    return {**DEFAULTS, **cfg}


class PostParser(HTMLParser):
    """Collects the attributes of every `<shreddit-post>` start tag."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.posts: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "shreddit-post":
            self.posts.append({k: v or "" for k, v in attrs})


def parse_posts(html: str) -> list[dict[str, str]]:
    parser = PostParser()
    parser.feed(html)
    parser.close()
    return parser.posts


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def created_at(raw: dict[str, str]) -> datetime | None:
    stamp = raw.get("created-timestamp", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(stamp, fmt)
        except ValueError:
            continue
    return None


def normalize(raw: dict[str, str], sub: str) -> dict | None:
    """A post as {sub, title, permalink, link, kind, score, comments, created}; None
    when it lacks a title, a permalink or a parseable time. `sub` is the configured
    name. `link` is the linked article of a link post, never a Reddit URL."""
    when, title, link = created_at(raw), raw.get("post-title", "").strip(), None
    permalink = raw.get("permalink", "")
    if not (when and title and permalink):
        return None
    href = raw.get("content-href", "")
    if raw.get("post-type") == "link" and href.startswith("http") and not c.is_reddit_url(href):
        link = href
    return {
        "sub": sub,
        "title": title,
        "permalink": BASE + permalink if permalink.startswith("/") else permalink,
        "link": link,
        "kind": "link" if link else ("text" if raw.get("post-type") == "text" else "other"),
        "score": to_int(raw.get("score")),
        "comments": to_int(raw.get("comment-count")),
        "created": when,
    }


def fetch_html(sub: str, sort: str, cfg: dict) -> str:
    import requests

    params = {"name": sub}
    if sort == "top":
        params["t"] = "day"
    resp = requests.get(
        ENDPOINT.format(sort=sort),
        params=params,
        headers={"User-Agent": BROWSER_UA, "Accept": "text/html"},
        timeout=float(cfg["timeout_seconds"]),
    )
    resp.raise_for_status()
    return resp.text


def read_all(fetch, cfg: dict, stats: dict) -> list[dict]:
    """One request per sub per sort, de-duplicated by thread. A failed request is
    logged and skipped."""
    posts: dict[str, dict] = {}
    first = True
    for sub in cfg["subreddits"]:
        row = stats.setdefault(sub, {"read": 0, "kept": 0, "staged": 0})
        for sort in cfg["sorts"]:
            if not first and cfg["delay_seconds"]:
                time.sleep(float(cfg["delay_seconds"]))
            first = False
            try:
                html = fetch(sub, sort, cfg)
            except Exception as exc:  # 403/429/network: never fail the scan
                print(f"reddit: r/{sub} {sort} skipped ({type(exc).__name__}: {exc})",
                      file=sys.stderr)  # fmt: skip
                continue
            for raw in parse_posts(html):
                post = normalize(raw, sub)
                if post is None:
                    continue
                row["read"] += 1
                best = posts.get(post["permalink"])
                if best is None or post["score"] > best["score"]:
                    posts[post["permalink"]] = post
    return list(posts.values())


def keep(post: dict, cfg: dict, now: datetime, tax: tx.Taxonomy) -> str | None:
    """Why a post is dropped, else None."""
    if now - post["created"] > timedelta(hours=float(cfg["lookback_hours"])):
        return "stale"
    if post["score"] < int(cfg["min_score"]):
        return "low-score"
    if post["kind"] == "other":
        return "media"
    if not er.on_thesis({"title": post["title"], "text": ""}, tax):
        return "off-thesis"
    if c.news_denylist_hit({"title": post["title"], "summary": ""}):
        return "denylist"
    return None


def candidate(post: dict, rules: dict, tax: tx.Taxonomy, rank: float) -> dict:
    url = c.clean_source_url(post["link"])
    day = post["created"].date().isoformat()
    blob = post["title"]
    return {
        "id": c.make_id(post["title"], c.normalize_url(url)),
        "discovered_via": "reddit",
        "title": post["title"],
        "source_name": f"Reddit r/{post['sub']} (linked)",
        "source_type": f"Reddit link: r/{post['sub']}",
        "source_url": url,
        "article_url": url,
        "tweet_url": None,
        "author": None,
        "published": day,
        "date": day[:7],
        "excerpt": "",
        "raw_path": None,
        **agg.guess_fields(blob, icl.label_for(blob, rules, tax), rules),
        "source_id": f"{SOURCE_PREFIX}:{post['sub'].lower()}",
        "source_rank": rank,
        "source_topics": ["ai-security", "product-security"],
        "reddit_url": post["permalink"],
        "reddit_score": post["score"],
        "reddit_comments": post["comments"],
        "retrieved_at": c.utcnow_iso(),
    }


def engagement(post: dict) -> int:
    return post["score"] + 2 * post["comments"]


def select(posts: list[dict], cfg: dict, stats: dict, rules: dict) -> tuple[list[dict], list[dict]]:
    """(candidates, self posts) from the posts read: filter, dedup the links against
    what is held, cap them at `max_per_run` by engagement."""
    tax, now = tx.get(), c.utcnow()
    keys, titles = icl.held()
    links: list[dict] = []
    selfposts: list[dict] = []
    for post in sorted(posts, key=engagement, reverse=True):
        if keep(post, cfg, now, tax) is not None:
            continue
        stats[post["sub"]]["kept"] += 1
        if not post["link"]:
            selfposts.append(post)
            continue
        if not icl.is_held({"href": post["link"], "title": post["title"]}, keys, titles):
            keys.add(icl.url_key(post["link"]))
            links.append(post)
    links = links[: int(cfg["max_per_run"])]
    for post in links:
        stats[post["sub"]]["staged"] += 1
    return [candidate(p, rules, tax, float(cfg["source_rank"])) for p in links], selfposts


def signal_row(post: dict) -> dict:
    return {
        "title": post["title"],
        "permalink": post["permalink"],
        "score": post["score"],
        "comments": post["comments"],
        "sub": post["sub"],
        "created": post["created"].isoformat(),
    }


def save_signal(posts: list[dict], cfg: dict, path: Path | None = None) -> int:
    """Upsert self posts into the gitignored signal file by permalink and drop rows
    older than `signal_days`. Returns the rows written this run."""
    path = path or signal_file()
    cutoff = (c.utcnow() - timedelta(days=int(cfg["signal_days"]))).isoformat()
    rows = {r["permalink"]: r for r in c.load_json(path, default=[]) or []}
    rows.update({r["permalink"]: r for r in map(signal_row, posts)})
    live = [r for r in rows.values() if r["created"] >= cutoff]
    c.save_json(path, sorted(live, key=lambda r: r["created"], reverse=True))
    return len(posts)


def report(stats: dict, staged: int, signal: int) -> None:
    for sub, row in stats.items():
        print(f"   r/{sub}: read={row['read']} kept={row['kept']} staged={row['staged']}")
    print(f"Reddit: {staged} link(s) staged, {signal} self post(s) as practitioner signal.")


def main(argv: list[str] | None = None, fetch=fetch_html) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    args = ap.parse_args(argv)
    cfg = settings()
    if c.backfill_window() is not None or not cfg["subreddits"]:
        print("reddit: skipped (backfill run, or no subreddits configured)")
        return 0
    try:
        rules = c.load_yaml(c.SOURCES_FILE)["classification"]
        stats: dict = {}
        cands, selfposts = select(read_all(fetch, cfg, stats), cfg, stats, rules)
        for cand in cands:
            print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title'][:80]}")
        report(stats, len(cands), len(selfposts))
        if not args.dry_run:
            save_signal(selfposts, cfg)
            c.add_candidates(cands)
    except Exception as exc:  # the lane is optional: log and exit 0
        print(f"reddit: failed soft ({type(exc).__name__}: {exc})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
