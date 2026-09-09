#!/usr/bin/env python3
"""
ingest_sitemap.py — Discover recent pages from sitemap-only sources.

Some labs (Anthropic's blog is the motivating case) publish no RSS/Atom feed
and render their index pages client-side, so neither feedparser nor a plain
HTML scrape works. Most of those sites still serve a static `sitemap.xml`
with a `<lastmod>` per page — this script treats that as the feed substitute
for any `research_index`-type source registered in data/sources.json.

For each registered source, fetches `{scheme}://{netloc}/sitemap.xml`
(cached per host — several sources can share one sitemap), keeps only the
URLs whose path falls under that source's own URL path prefix, and — for
the ones with `<lastmod>` inside the freshness window — fetches the real
page text via the shared Jina Reader helper. A URL slug alone (e.g.
"disrupting-ai-espionage") is too terse for the keyword classifier to place
reliably; the real title + body is what RSS/GHSA candidates get for free
from their feed/API and what this source type otherwise lacks entirely.
The fetched body is persisted immediately (raw_path), so fetch_article.py's
later pass has nothing left to do for these candidates.

A source with no working sitemap (missing, non-XML, or an SPA serving its
app shell for any path — red.anthropic.com does this) is skipped, not
treated as a hard error: that leaves its research_index registration as an
honest, documented gap rather than a silent false success. A single page
fetch failure is likewise best-effort: it falls back to slug-only
classification rather than dropping the candidate outright.

Usage:
    python scripts/ingest_sitemap.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from urllib.parse import urlparse

import aggregate as agg
import common as c
import sources_registry as sr

try:
    import requests
except ImportError:  # pragma: no cover - environment guard
    sys.exit("Missing dependencies. Run: pip install -r requirements.txt")

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def sitemap_url_for(source_url: str) -> str:
    """The site-root sitemap for any page URL, e.g. .../research -> .../sitemap.xml."""
    p = urlparse(source_url)
    return f"{p.scheme}://{p.netloc}/sitemap.xml"


def fetch_sitemap(url: str) -> list[tuple[str, str]]:
    """Return [(loc, lastmod), ...] from a sitemap.xml. [] on any network
    failure or a response that isn't real sitemap XML (some SPAs serve their
    app shell HTML for any path, including /sitemap.xml)."""
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": c.HTTP_USER_AGENT})
        resp.raise_for_status()
    except Exception:  # noqa: BLE001 - discovery is best-effort
        return []
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError:
        return []
    out: list[tuple[str, str]] = []
    for url_el in root.findall(f"{SITEMAP_NS}url"):
        loc = (url_el.findtext(f"{SITEMAP_NS}loc") or "").strip()
        lastmod = (url_el.findtext(f"{SITEMAP_NS}lastmod") or "").strip()
        if loc:
            out.append((loc, lastmod))
    return out


def title_from_slug(url: str) -> str:
    """A readable placeholder title from the URL's last path segment; used
    when the real fetch fails or doesn't carry a parseable title."""
    slug = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    words = [w for w in re.split(r"[-_]+", slug) if w]
    return " ".join(w.capitalize() for w in words) or url


def title_from_reader_text(body: str, url: str) -> str:
    """r.jina.ai's Reader output starts with 'Title: <real title>'; fall back
    to the URL slug if the body doesn't carry that line."""
    first_line = (body or "").split("\n", 1)[0]
    if first_line.startswith("Title:"):
        title = first_line[len("Title:") :].strip()
        if title:
            return title
    return title_from_slug(url)


def path_prefix_of(source_url: str) -> str:
    path = urlparse(source_url).path.rstrip("/")
    return f"{path}/"


def fetch_body(url: str) -> str | None:
    """Real page text via the shared Jina Reader helper; None on any failure."""
    try:
        return c.fetch_readable(url, timeout=30, max_chars=20000)
    except Exception:  # noqa: BLE001 - a single page miss shouldn't halt ingestion
        return None


def url_to_candidate(loc: str, lastmod: str, source: dict, rules: dict) -> dict | None:
    """Map one sitemap (loc, lastmod) pair to a candidate; None if off-topic
    or unusable. Mirrors aggregate.build_candidate's shape/fields."""
    nurl = c.normalize_url(loc)
    if not nurl:
        return None
    dt = c.entry_datetime({"published": lastmod}) if lastmod else None

    body = fetch_body(loc)
    if body:
        title = title_from_reader_text(body, loc)
        excerpt = c.clean_summary(body, 320)
        blob = f"{title} {body[:3000]}".lower()
    else:
        title = title_from_slug(loc)
        excerpt = ""
        blob = title.lower()

    domain = agg.classify_domain(blob, rules, source.get("domains") or [])
    if domain is None:
        return None

    cand_id = c.make_id(title, nurl)
    raw_path = c.write_raw(cand_id, body) if body else None
    return {
        "id": cand_id,
        "discovered_via": "sitemap",
        "title": title,
        "source_name": source["name"],
        "source_type": source.get("notes", ""),
        "source_url": loc,
        "article_url": loc,
        "tweet_url": None,
        "author": None,
        "published": dt.strftime("%Y-%m-%d") if dt else c.date_from_url(loc),
        "date": dt.strftime("%Y-%m") if dt else None,
        "excerpt": excerpt,
        "raw_path": raw_path,
        "guess_topic": c.topic_for_domain(domain),
        "guess_domain": domain,
        "guess_subtype": agg.classify_subtype(blob, domain, rules),
        "source_id": source.get("id"),
        "source_rank": source.get("rank"),
        "source_topics": source.get("topics", []),
        "retrieved_at": c.utcnow_iso(),
    }


def collect(rules: dict, cutoff: datetime) -> list[dict]:
    """Fetch every registered research_index source's sitemap and build
    fresh candidates for the URLs under that source's own path prefix."""
    sources = sr.sources_of_type("research_index")
    sitemap_cache: dict[str, list[tuple[str, str]]] = {}
    candidates: list[dict] = []
    for source in sources:
        base = source.get("url") or source.get("handle") or ""
        if not base:
            continue
        sm_url = sitemap_url_for(base)
        if sm_url not in sitemap_cache:
            print(f"-> {source['name']}: {sm_url}")
            sitemap_cache[sm_url] = fetch_sitemap(sm_url)
            if not sitemap_cache[sm_url]:
                print("   ! no usable sitemap (missing, non-XML, or SPA shell)")
        prefix = path_prefix_of(base)
        for loc, lastmod in sitemap_cache[sm_url]:
            if not urlparse(loc).path.startswith(prefix):
                continue
            dt = c.entry_datetime({"published": lastmod}) if lastmod else None
            if dt is not None and dt < cutoff:
                continue
            cand = url_to_candidate(loc, lastmod, source, rules)
            if cand:
                candidates.append(cand)
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't write changes")
    args = ap.parse_args()

    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    cutoff = datetime.now(UTC) - timedelta(days=c.load_config().max_age_days)
    candidates = collect(rules, cutoff)

    if args.dry_run:
        print(f"\n(dry run) {len(candidates)} candidate(s) would be staged:")
        for cand in candidates:
            print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title']}")
        return 0

    added = c.add_candidates(candidates)
    print(f"\nStaged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    for cand in added:
        print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
