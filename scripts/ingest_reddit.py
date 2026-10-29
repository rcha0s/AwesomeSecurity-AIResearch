#!/usr/bin/env python3
"""
ingest_reddit.py — Subreddits as practitioner signal, through Reddit's official API.

App-only OAuth (client-credentials grant): POST https://www.reddit.com/api/v1/access_token
with HTTP basic auth, then GET https://oauth.reddit.com/r/{sub}/new and /top?t=day as
JSON, with a descriptive User-Agent. Credentials come from the environment only
(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, from a "script" app at reddit.com/prefs/apps).
Unset, the lane logs "skipped: no Reddit API credentials" and exits 0. The token lives
in memory and goes only in the Authorization header: never logged, never in a URL.
No user login, no scraping, no browser.

A Reddit thread alone never becomes a finding:
  * a link post whose `url` is not a Reddit host stages that ARTICLE as the candidate's
    `source_url`; the thread rides along as `reddit_url`, `reddit_score`,
    `reddit_comments` and `discovered_via: "reddit"`;
  * a self post (`is_self`) is not staged. It is recorded in the gitignored
    data/_practitioner_signal.json (title, permalink, score, comments, sub, created)
    for the "what practitioners are arguing" section;
  * merge_analysis.py holds any entry whose only citations are Reddit URLs.

Per sub it makes one request per sort (config.yaml `reddit`), keeps posts from the
last `lookback_hours` that pass the on-thesis filter the curator ingestor uses (title
plus a self post's `selftext`), and stages at most `max_per_run` links, best
engagement first. It fails soft: a 401, 403, 429 or network error is logged and the
exit code stays 0, so a scan never fails because of Reddit.

Usage:
    REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... python scripts/ingest_reddit.py [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import aggregate as agg
import common as c
import eval_recall as er
import ingest_curator_links as icl
import taxonomy as tx

SOURCE_PREFIX = "reddit"
BASE = "https://www.reddit.com"
TOKEN_URL = BASE + "/api/v1/access_token"
API = "https://oauth.reddit.com"
USER_AGENT = "awesomesec-research/1.0"
SELFTEXT_CHARS = 2000  # of a self post's body, for the on-thesis check
LISTING_LIMIT = 100
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


def to_int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def selftext_of(raw: dict) -> str:
    return (raw.get("selftext") or "")[:SELFTEXT_CHARS]


def normalize(raw: dict, sub: str) -> dict | None:
    """A listing item (`data` of a t3) as {sub, title, permalink, link, kind, score,
    comments, created, text}; None when it lacks a title, a permalink or a time. `sub`
    is the configured name. `link` is the linked article of a link post, never a
    Reddit URL."""
    title, permalink = (raw.get("title") or "").strip(), raw.get("permalink") or ""
    try:
        when = datetime.fromtimestamp(float(raw["created_utc"]), UTC)
    except (KeyError, TypeError, ValueError, OverflowError, OSError):
        return None
    if not (title and permalink):
        return None
    href = raw.get("url") or ""
    link = None
    if not raw.get("is_self") and href.startswith("http") and not c.is_reddit_url(href):
        link = href
    return {
        "sub": sub,
        "title": title,
        "permalink": BASE + permalink if permalink.startswith("/") else permalink,
        "link": link,
        "kind": "link" if link else ("text" if raw.get("is_self") else "other"),
        "score": to_int(raw.get("score")),
        "comments": to_int(raw.get("num_comments")),
        "created": when,
        "text": selftext_of(raw),
    }


def get_token(client_id: str, client_secret: str, cfg: dict) -> str:
    """App-only access token (client-credentials grant), kept in memory."""
    import requests

    resp = requests.post(
        TOKEN_URL,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        headers={"User-Agent": USER_AGENT},
        timeout=float(cfg["timeout_seconds"]),
    )
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("token response carried no access_token")
    return token


def fetch_listing(sub: str, sort: str, cfg: dict, token: str) -> list[dict]:
    """The `data` of each post in /r/{sub}/{sort}. The token travels only in the header."""
    import requests

    params = {"limit": LISTING_LIMIT, "raw_json": 1}
    if sort == "top":
        params["t"] = "day"
    resp = requests.get(
        f"{API}/r/{sub}/{sort}",
        params=params,
        headers={"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT},
        timeout=float(cfg["timeout_seconds"]),
    )
    resp.raise_for_status()
    children = (resp.json().get("data") or {}).get("children") or []
    return [ch["data"] for ch in children if isinstance(ch, dict) and ch.get("kind") == "t3"]


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
                items = fetch(sub, sort, cfg)
            except Exception as exc:  # 403/429/network: never fail the scan
                print(f"reddit: r/{sub} {sort} skipped ({type(exc).__name__}: {exc})",
                      file=sys.stderr)  # fmt: skip
                continue
            for raw in items:
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
    if not er.on_thesis({"title": post["title"], "text": post["text"]}, tax):
        return "off-thesis"
    if c.news_denylist_hit({"title": post["title"], "summary": post["text"]}):
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


def credentials() -> tuple[str, str] | None:
    cid, secret = os.environ.get("REDDIT_CLIENT_ID"), os.environ.get("REDDIT_CLIENT_SECRET")
    return (cid, secret) if cid and secret else None


def make_fetch(cfg: dict):
    """A fetch(sub, sort, cfg) bound to a fresh app-only token, or None (logged) when
    there are no credentials or the token request fails."""
    creds = credentials()
    if creds is None:
        print("reddit: skipped: no Reddit API credentials")
        return None
    try:
        token = get_token(*creds, cfg)
    except Exception as exc:  # status or type only: never echo a request
        status = getattr(getattr(exc, "response", None), "status_code", "")
        print(f"reddit: skipped: token request failed ({type(exc).__name__} {status})",
              file=sys.stderr)  # fmt: skip
        return None
    return lambda sub, sort, cfg: fetch_listing(sub, sort, cfg, token)


def main(argv: list[str] | None = None, fetch=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    args = ap.parse_args(argv)
    cfg = settings()
    if c.backfill_window() is not None or not cfg["subreddits"]:
        print("reddit: skipped (backfill run, or no subreddits configured)")
        return 0
    fetch = fetch or make_fetch(cfg)
    if fetch is None:
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
