#!/usr/bin/env python3
"""
ingest_x_list.py — Stage the last 24 hours of Rohan's X list, local runner only.

Reads the list timeline through the Interceptor CLI, in its test browser profile
and its own managed tab group (`x_list.context`, `x_list.group`), so it never
touches the operator's active tab. It is read-only: the only Interceptor verbs
this module can invoke are in ALLOWED_VERBS, enforced in `build_command()`; it
never posts, likes, follows, replies or opens compose. Scrolling happens only
in its own tab (pinned with --tab), to load more of the list.

A status link's id is a snowflake: it carries the post's exact creation time.
Posts are dated by that, so a repost carries the original's time, and anything
older than `x_list.lookback_hours` (24, hard) or without a status id is dropped.
The list page's text shows no per-post URLs, so the `links` verb supplies them
and the page text supplies the words.

Each kept post is on-thesis (the taxonomy keyword hints, no excluded terms, not
on the news deny-list) and not already held (pools, archive, story ledger). A
post that links an article stages the article as the citation (`source_url`)
with the post as `tweet_url`; a post with no article stages its own text as
`raw_path`, like `add.py --text`, so the analysis session never fetches x.com.

`--collect` only reads the list into a gitignored 48h store (data/_x_list_seen.json,
or $X_LIST_SEEN); the scan-time run merges that store with a fresh read, because a
background tab loads only 5 to 10 posts per read. An optional launchd job runs it.

Skips (exit 0, one "skipped" line) under CI/GITHUB_ACTIONS, when SCAN_RUNNER is
not `local`, and when Interceptor or its test profile is unavailable.

Usage:
    SCAN_RUNNER=local python scripts/ingest_x_list.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import aggregate as agg
import common as c
import eval_recall as er
import ingest_curator_links as icl
import taxonomy as tx

SOURCE_ID = "x:list"
SOURCE_NAME = "X list"
TWITTER_EPOCH_MS = 1288834974657
# The only Interceptor verbs this module may run. Nothing here writes to X:
# no click, type, act, keys, eval, navigate. `tab` is further limited to `close`
# (its own tab) and `scroll` to `down`.
ALLOWED_VERBS = frozenset({"open", "read", "links", "scroll", "tab"})
SKIP_ENV = ("CI", "GITHUB_ACTIONS")
DEFAULTS = {
    "list_url": "https://x.com/i/lists/2115494675994071362",
    "lookback_hours": 24,
    "context": "interceptor-test",
    "group": "x-list",
    "open_timeout_ms": 25000,
    "max_scrolls": 6,
    "scroll_wait_s": 3.0,
    "source_rank": 60.0,
    "max_candidates": 40,
}
AGE_RE = re.compile(r"^(\d+)([smhd])$")
DATE_RE = re.compile(r"^[A-Z][a-z]{2} \d{1,2}(, \d{4})?$")
HANDLE_RE = re.compile(r"^@(\w{1,15})$")
STATUS_RE = re.compile(r"^https://x\.com/(\w+)/status/(\d+)$")
NOISE = {"Show more", "Quote", "Pinned", "Replying to"}
FEED_END = (
    "Subscribe to Premium",
    "Who to follow",
    "Trending now",
    "What’s happening",
    "What's happening",
)
LIST_URL_RE = re.compile(r"^https://x\.com/i/lists/\d+$")
OPEN_FLAGS = {"--text-only", "--full", "--json"}  # plus `--timeout <int>`; never --activate
MIN_VERSION = (0, 16)
SEEN_KEEP_HOURS = 48
SEEN_ENV = "X_LIST_SEEN"
OWN_HOSTS = ("x.com", "twitter.com", "twimg.com", "x.ai")
ECHO_RE = re.compile(r"^\[[0-9a-f]+\] → \S+\n?")


class Skip(Exception):
    """A reason to skip the lane without failing the scan."""


@dataclass
class Post:
    handle: str
    age: str
    text: str
    status_id: str | None = None
    links: list[str] = field(default_factory=list)


def settings() -> dict:
    """config.yaml `x_list`, over DEFAULTS."""
    cfg = (c.load_yaml(c.CONFIG_FILE) or {}).get("x_list") or {}
    return {**DEFAULTS, **cfg}


def check_runner(env: dict | None = None) -> None:
    """Raise Skip unless this is the local runner outside CI."""
    env = os.environ if env is None else env
    for name in SKIP_ENV:
        if env.get(name):
            raise Skip(f"{name} is set; the X lane never runs in CI or the cloud")
    if env.get("SCAN_RUNNER") != "local":
        raise Skip("SCAN_RUNNER is not 'local'; the X lane runs only on the local runner")


# --- Interceptor (read-only wrapper) ---------------------------------------
def check_open_args(args: list[str]) -> None:
    """`open` takes only the list URL and read flags; --activate (foreground) is refused."""
    if not args or not LIST_URL_RE.match(args[0]):
        raise ValueError("open is limited to an https://x.com/i/lists/<id> URL")
    rest = args[1:]
    i = 0
    while i < len(rest):
        if rest[i] == "--activate":
            raise ValueError("open --activate is refused (never foreground the tab)")
        if rest[i] == "--timeout" and i + 1 < len(rest) and rest[i + 1].isdigit():
            i += 2
        elif rest[i] in OPEN_FLAGS:
            i += 1
        else:
            raise ValueError(f"open flag {rest[i]!r} is not allowed")


def check_version() -> None:
    """Skip unless the installed Interceptor is at least MIN_VERSION."""
    binary = shutil.which("interceptor")
    if binary is None:
        raise Skip("interceptor is not installed")
    try:
        res = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=20)
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise Skip(f"interceptor --version failed: {type(exc).__name__}") from exc
    m = re.search(r"(\d+)\.(\d+)", res.stdout)
    if res.returncode != 0 or not m or (int(m.group(1)), int(m.group(2))) < MIN_VERSION:
        floor = ".".join(map(str, MIN_VERSION))
        raise Skip(f"interceptor {floor} or newer is required: {res.stdout.strip()[:40]!r}")


def build_command(verb: str, args: list[str], cfg: dict, tab: str | None) -> list[str]:
    """The argv for one allowed Interceptor call; ValueError for anything else."""
    if verb not in ALLOWED_VERBS:
        raise ValueError(f"interceptor verb {verb!r} is not allowed (read-only lane)")
    if verb == "open":
        check_open_args(args)
    if verb == "scroll" and args != ["down"]:
        raise ValueError("scroll is limited to `scroll down`")
    if verb == "tab" and args != ["close"]:
        raise ValueError("tab is limited to `tab close` (own tab)")
    if verb in ("scroll", "tab", "read", "links") and not tab:
        raise ValueError(f"{verb} must name our own tab (--tab)")
    cmd = ["interceptor", verb, *args, "--context", cfg["context"], "--group", cfg["group"]]
    if tab:
        cmd += ["--tab", tab]
    return cmd


def interceptor(verb: str, args: list[str], cfg: dict, tab: str | None = None) -> str:
    """Run one allowed verb; return stdout minus the request echo line."""
    cmd = build_command(verb, args, cfg, tab)
    binary = shutil.which("interceptor")
    if binary is None:
        raise Skip("interceptor is not installed")
    try:
        res = subprocess.run(
            [binary, *cmd[1:]], capture_output=True, text=True, timeout=90, check=False
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise Skip(f"interceptor {verb} failed: {type(exc).__name__}") from exc
    out = ECHO_RE.sub("", res.stdout.strip())
    out = "\n".join(ln for ln in out.splitlines() if not ln.startswith("warning:"))
    if res.returncode != 0 or out.startswith("error"):
        raise Skip(f"interceptor {verb} unavailable: {(out or res.stderr)[:120]!r}")
    return out


def parse_open(out: str) -> tuple[str, str]:
    """(tab id, page text) from `open --json` (data.tabId, data.text); else the
    first line only (`Tab: <id> | <url>`) with the rest as text. Never searches
    the page text for a tab id."""
    if out.lstrip().startswith("{"):
        try:
            data = json.loads(out).get("data") or {}
        except ValueError:
            data = {}
        tab = data.get("tabId")
        if isinstance(tab, int) and not isinstance(tab, bool):
            return str(tab), str(data.get("text") or "")
    first, _, rest = out.partition("\n")
    m = re.match(r"Tab: (\d+) \|", first)
    if not m:
        raise Skip("interceptor open returned no tab id")
    return m.group(1), rest


def open_list(cfg: dict) -> tuple[str, str]:
    """Open the list in the managed group; return (tab id, page text)."""
    args = [cfg["list_url"], "--text-only", "--full", "--json"]
    args += ["--timeout", str(int(cfg["open_timeout_ms"]))]
    return parse_open(interceptor("open", args, cfg))


def read_links(cfg: dict, tab: str) -> list[dict]:
    out = interceptor("links", ["--json"], cfg, tab)
    try:
        data = json.loads(out[out.index("{") :]).get("data") or []
    except ValueError:
        return []
    return [x for x in data if isinstance(x, dict) and x.get("href")]


# --- Parsing ---------------------------------------------------------------
def is_age(line: str) -> bool:
    return bool(AGE_RE.match(line) or DATE_RE.match(line))


def find_headers(lines: list[str]) -> list[int]:
    """Index of each post header's `@handle` line: handle, `·`, then an age."""
    return [
        i
        for i in range(len(lines) - 2)
        if HANDLE_RE.match(lines[i]) and lines[i + 1] == "·" and is_age(lines[i + 2])
    ]


def feed_lines(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines()]
    for i, ln in enumerate(lines):
        if ln in FEED_END:
            return lines[:i]
    return lines


def body_of(lines: list[str]) -> str:
    body = [ln for ln in lines if ln and ln not in NOISE]
    while body and re.fullmatch(r"[\d.,]+[KM]?", body[-1]):
        body.pop()  # the reply/repost/like/view counters
    return "\n".join(body).strip()


def parse_posts(text: str) -> list[Post]:
    """Posts in page order. A quoted post folds into its parent's text."""
    lines = feed_lines(text)
    heads = find_headers(lines)
    posts: list[Post] = []
    for n, h in enumerate(heads):
        start = h + 3
        # The next post's name line (and a "X reposted" line) sit before its handle.
        end = heads[n + 1] - 1 if n + 1 < len(heads) else len(lines)
        if n + 1 < len(heads) and end > 0 and lines[end - 1].endswith("reposted"):
            end -= 1
        quoted = h >= 2 and lines[h - 2] == "Quote"
        piece = body_of(lines[start : max(start, end)])
        match = HANDLE_RE.match(lines[h])
        handle, age = (match.group(1) if match else ""), lines[h + 2]
        if quoted and posts:
            posts[-1].text += f"\n[quoting @{handle}] {piece}"
        else:
            posts.append(Post(handle, age, piece))
    return posts


def external(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if urlparse(url).scheme not in ("http", "https") or not host:
        return False
    if host == "t.co":
        return True
    return not any(host == h or host.endswith("." + h) for h in OWN_HOSTS)


def attach_links(posts: list[Post], links: list[dict]) -> None:
    """Give each post its status id and external links from the `links` list.
    A post's time link is `/<handle>/status/<id>` with the age as its text; the
    external links that follow, until the next post's time link, are its own."""
    stamps = [
        (i, m.group(1), m.group(2), link.get("text") or "")
        for i, link in enumerate(links)
        if (m := STATUS_RE.match(link["href"])) and is_age(link.get("text") or "")
    ]
    ends = [s[0] for s in stamps[1:]] + [len(links)]
    cursor = 0
    for post in posts:
        for k in range(cursor, len(stamps)):
            idx, handle, sid, age = stamps[k]
            if handle.lower() == post.handle.lower() and age == post.age:
                post.status_id = sid
                post.links = [
                    link["href"] for link in links[idx + 1 : ends[k]] if external(link["href"])
                ]
                cursor = k + 1
                break


def snowflake_time(status_id: str) -> datetime:
    return datetime.fromtimestamp(((int(status_id) >> 22) + TWITTER_EPOCH_MS) / 1000, tz=UTC)


# --- Selection and staging -------------------------------------------------
def resolve_tco(url: str, timeout: float = 10.0) -> str | None:
    """Expand a t.co link by reading its redirect, without following it."""

    class NoFollow(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
            return None

    opener = urllib.request.build_opener(NoFollow)
    try:
        opener.open(urllib.request.Request(url, method="HEAD"), timeout=timeout)
    except urllib.error.HTTPError as err:
        loc = err.headers.get("Location")
        return loc if loc and loc.startswith(("http://", "https://")) else None
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return None


def article_for(post: Post, resolve: Callable[[str], str | None]) -> str | None:
    """The first linked article (non-X host, t.co expanded), else None."""
    for href in post.links:
        url = resolve(href) if (urlparse(href).hostname or "") == "t.co" else href
        if url and external(url) and urlparse(url).hostname != "t.co":
            return c.clean_source_url(url)
    return None


def tweet_url(post: Post) -> str:
    return f"https://x.com/{post.handle}/status/{post.status_id}"


def title_of(post: Post) -> str:
    first = " ".join(post.text.split("\n")[0].split()) or "(media post)"
    return f"@{post.handle}: {first[:110]}"


def reject(post: Post, cutoff: datetime, tax: tx.Taxonomy) -> str | None:
    """Why a post is not staged, else None. Undated posts are dropped."""
    if not post.status_id:
        return "undated"
    if snowflake_time(post.status_id) < cutoff:
        return "too-old"
    if "Replying to" in post.text[:40] or post.text.startswith("@"):
        return "reply"
    item = {"title": title_of(post), "text": post.text}
    if not er.on_thesis(item, tax):
        return "off-thesis"
    if c.news_denylist_hit({"title": item["title"], "summary": post.text}):
        return "denylist"
    return None


def candidate(post: Post, article: str | None, rules: dict, cfg: dict) -> dict:
    when = snowflake_time(post.status_id or "0")
    title = title_of(post)
    page = tweet_url(post)
    url = article or page
    cand_id = c.make_id(title, c.normalize_url(url))
    blob = f"{title} {post.text}"
    return {
        "id": cand_id,
        "discovered_via": "x-list",
        "title": title,
        "source_name": SOURCE_NAME,
        "source_type": "X list post",
        "source_url": url,
        "article_url": article,
        "tweet_url": page,
        "author": f"@{post.handle}",
        "published": when.date().isoformat(),
        "date": when.strftime("%Y-%m"),
        "x_posted_at": when.replace(microsecond=0).isoformat(),
        "excerpt": c.clean_summary(post.text, 320),
        "raw_path": None if article else c.write_raw(cand_id, post.text),
        **agg.guess_fields(blob, icl.label_for(blob, rules, tx.get()), rules),
        "source_id": SOURCE_ID,
        "source_rank": float(cfg["source_rank"]),
        "source_topics": ["ai-security", "product-security", "ai-research"],
        "retrieved_at": c.utcnow_iso(),
    }


def is_held(post: Post, article: str | None, keys: set[str], titles: list[str]) -> bool:
    if icl.url_key(article or tweet_url(post)) in keys:
        return True
    return any(c.title_similar(title_of(post), t) for t in titles if t)


def select(posts: list[Post], cfg: dict, rules: dict, resolve: Callable, dry: bool) -> dict:
    """Filter posts into {"candidates", "counts"}. `dry` writes no raw text."""
    cutoff = c.utcnow() - timedelta(hours=float(cfg["lookback_hours"]))
    tax = tx.get()
    keys, titles = icl.held()
    counts: dict[str, int] = {"read": len(posts)}
    out: list[dict] = []
    for post in posts:
        why = reject(post, cutoff, tax)
        article = None if why else article_for(post, resolve)
        if why is None and is_held(post, article, keys, titles):
            why = "held"
        if why is None and len(out) >= int(cfg["max_candidates"]):
            why = "over-cap"
        counts[why or "kept"] = counts.get(why or "kept", 0) + 1
        if why:
            continue
        keys.add(icl.url_key(article or tweet_url(post)))
        titles.append(title_of(post))
        cand = candidate(post, article, rules, cfg)
        if dry and cand["raw_path"]:
            (c.ROOT / cand["raw_path"]).unlink(missing_ok=True)
        out.append(cand)
    return {"candidates": out, "counts": counts}


# --- Collection ------------------------------------------------------------
def snapshot(cfg: dict, tab: str, text: str) -> list[Post]:
    posts = parse_posts(text)
    attach_links(posts, read_links(cfg, tab))
    return posts


def read_text(cfg: dict, tab: str) -> str:
    return interceptor("read", ["--text-only", "--full"], cfg, tab)


def read_list_posts(
    cfg: dict, since: datetime, sleep: Callable[[float], None] = time.sleep
) -> list[Post]:
    """THE reader boundary: posts of the list, newest window first, as Post
    objects with a status id. Everything after it (date and thesis filters,
    staging, dedup) consumes only this, so an API reader can replace this
    function. This one reads the list: scroll within our own tab until a post older than the
    lookback shows (or max_scrolls), and return every distinct dated post. X
    keeps only the visible posts in the page, so each pass is merged by id."""
    tab, text = open_list(cfg)
    cutoff = since
    seen: dict[str, Post] = {}
    try:
        posts = snapshot(cfg, tab, text)
        if not posts:  # an empty render: let the timeline load, read once more
            sleep(float(cfg["scroll_wait_s"]) + 2)
            posts = snapshot(cfg, tab, read_text(cfg, tab))
        for _ in range(int(cfg["max_scrolls"]) + 1):
            before = len(seen)
            for p in posts:
                if p.status_id:
                    seen.setdefault(p.status_id, p)
            # Done at a post past the lookback, or when a scroll loads nothing new
            # (the list's end, or a background tab that does not load more).
            if any(snowflake_time(i) < cutoff for i in seen) or (before and len(seen) == before):
                break
            interceptor("scroll", ["down"], cfg, tab)
            sleep(float(cfg["scroll_wait_s"]))
            posts = snapshot(cfg, tab, read_text(cfg, tab))
    finally:
        try:
            interceptor("tab", ["close"], cfg, tab)
        except Skip:
            pass
    return list(seen.values())


def seen_path() -> Path:
    return Path(os.environ.get(SEEN_ENV) or c.DATA_DIR / "_x_list_seen.json")


def load_seen() -> list[Post]:
    rows = c.load_json(seen_path(), default=[]) or []
    return [Post(**r) for r in rows if isinstance(r, dict) and r.get("status_id")]


def merge_posts(*groups: list[Post]) -> list[Post]:
    """Union of post lists by status id; the first group to hold an id wins."""
    out: dict[str, Post] = {}
    for group in groups:
        for p in group:
            if p.status_id:
                out.setdefault(p.status_id, p)
    return list(out.values())


def upsert_seen(fresh: list[Post], now: datetime) -> list[Post]:
    """Merge `fresh` into the store, drop rows older than SEEN_KEEP_HOURS, save."""
    keep_from = now - timedelta(hours=SEEN_KEEP_HOURS)
    posts = [
        p
        for p in merge_posts(fresh, load_seen())
        if snowflake_time(p.status_id or "0") >= keep_from
    ]
    path = seen_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(p) for p in posts], indent=1), encoding="utf-8")
    return posts


def report(result: dict) -> None:
    print("X list: " + ", ".join(f"{k}={v}" for k, v in result["counts"].items()))
    for cand in result["candidates"]:
        print(f"   {cand['x_posted_at']} {cand['title'][:90]}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument(
        "--collect", action="store_true", help="only read the list into the 48h seen store"
    )
    args = ap.parse_args(argv)
    now = c.utcnow()
    fresh: list[Post] = []
    try:
        check_runner()
        cfg = settings()
        try:
            check_version()
            fresh = read_list_posts(cfg, now - timedelta(hours=float(cfg["lookback_hours"])))
        except Skip as why:
            if args.collect or not load_seen():
                raise
            print(f"X list: fresh read skipped ({why}); using the seen store")
    except Skip as why:
        print(f"X list: skipped ({why})")
        return 0
    if args.collect:
        print(f"X list: collected {len(fresh)} post(s); {len(upsert_seen(fresh, now))} held")
        return 0
    posts = merge_posts(fresh, load_seen())
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    result = select(posts, cfg, rules, resolve_tco, args.dry_run)
    report(result)
    if args.dry_run:
        return 0
    upsert_seen(fresh, now)
    added = c.add_candidates(result["candidates"], max_age=2)
    print(f"Staged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
