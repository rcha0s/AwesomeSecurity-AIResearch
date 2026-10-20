#!/usr/bin/env python3
"""
ingest_json_feeds.py — Discover from keyless JSON feeds (no RSS/Atom exists).

Two registered source types:
  kev_json    CISA Known Exploited Vulnerabilities catalog. Every entry is a
              vulnerability CISA confirms is exploited in the wild, the strongest
              "this matters now" signal in the pipeline. Entries added inside the
              freshness window are staged (de-duped by CVE URL).
  hf_papers   Hugging Face Daily Papers. A listing there is one of the paper
              quality signals (paper_gate), so these papers are admitted by
              construction; each must still keyword-classify on-topic.

Usage:
    python scripts/ingest_json_feeds.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta

import aggregate as agg
import common as c
import paper_gate as pg
import sources_registry as sr

try:
    import requests
except ImportError:  # pragma: no cover - environment guard
    sys.exit("Missing dependencies. Run: pip install -r requirements.txt")

NVD_URL = "https://nvd.nist.gov/vuln/detail/"
# KEV entries are product vulnerabilities; titles rarely hit the AI/web keyword
# rules, so without a fallback nearly all would be dropped. The fallback is a
# taxonomy ID: it routes to product-security like the old "Web Application
# Security" label did, and guess_domain refines it by keyword (ps.mobile, ...).
KEV_DEFAULT_DOMAINS = ["ps.appsec"]


def fetch_json(url: str, **params) -> dict | list | None:
    try:
        resp = requests.get(
            url, params=params or None, timeout=45, headers={"User-Agent": c.HTTP_USER_AGENT}
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # noqa: BLE001 - discovery is best-effort
        print(f"   ! fetch failed for {url}: {exc}", file=sys.stderr)
        return None


def _base(source: dict, title: str, url: str, published: str | None, excerpt: str) -> dict:
    return {
        "id": c.make_id(title, c.normalize_url(url)),
        "discovered_via": "rss",
        "title": title,
        "source_name": source["name"],
        "source_type": source.get("notes", ""),
        "source_url": url,
        "article_url": url,
        "tweet_url": None,
        "author": None,
        "published": published,
        "date": published[:7] if published else None,
        "excerpt": excerpt,
        "raw_path": None,
        "source_id": source.get("id"),
        "source_rank": source.get("rank"),
        "source_topics": source.get("topics", []),
        "retrieved_at": c.utcnow_iso(),
    }


def _classify(cand: dict, blob: str, fallback: list[str], rules: dict) -> dict | None:
    domain = agg.classify_domain(blob, rules, fallback)
    if domain is None:
        return None
    cand.update(agg.guess_fields(blob, domain, rules))
    return cand


def kev_candidates(data: dict, source: dict, rules: dict, cutoff: datetime) -> list[dict]:
    out = []
    vulns = data.get("vulnerabilities") if isinstance(data, dict) else None
    for vuln in vulns if isinstance(vulns, list) else []:
        if not isinstance(vuln, dict):
            continue
        added = vuln.get("dateAdded") or ""
        if not added or added < cutoff.date().isoformat():
            continue
        cve = vuln.get("cveID", "")
        name = vuln.get("vulnerabilityName") or f"{vuln.get('vendorProject')} {vuln.get('product')}"
        title = f"CISA KEV: {name} ({cve}) exploited in the wild"
        excerpt = c.clean_summary(vuln.get("shortDescription", ""), 320)
        cand = _base(source, title, NVD_URL + cve, added, excerpt)
        fallback = source.get("domains") or KEV_DEFAULT_DOMAINS
        cand = _classify(cand, f"{title} {excerpt}", fallback, rules)
        if cand:
            cand["kev"] = {
                k: vuln.get(k) for k in ("cveID", "vendorProject", "product", "dateAdded")
            }
            out.append(cand)
    return out


def hf_candidates(
    items: list[dict],
    source: dict,
    rules: dict,
    cutoff: datetime,
    security_terms: tuple[str, ...] = (),
) -> list[dict]:
    """HF Daily Papers is mostly general ML, so like the broad conference venues an
    item must also name a security concern (`security_terms`) on top of classifying."""
    items = [i for i in items if isinstance(i, dict) and isinstance(i.get("paper"), dict)]
    signals = pg.Signals(
        hf_ids={str(i["paper"]["id"]).lower() for i in items if i["paper"].get("id")}
    )
    out = []
    for item in items:
        paper = item["paper"]
        published = (paper.get("publishedAt") or item.get("publishedAt") or "")[:10]
        if not paper.get("id") or not published or published < cutoff.date().isoformat():
            continue
        title = " ".join((paper.get("title") or "").split())
        url = f"https://arxiv.org/abs/{paper['id']}"
        excerpt = c.clean_summary(paper.get("summary", ""), 320)
        if security_terms and not any(t in f"{title} {excerpt}".lower() for t in security_terms):
            continue
        cand = _base(source, title, url, published, excerpt)
        cand["hf_upvotes"] = paper.get("upvotes")
        cand = _classify(cand, f"{title} {excerpt}", [], rules)  # strict: keywords only
        if cand and pg.admit(cand, signals)[0]:
            out.append(cand)
    return out


def collect(rules: dict, cutoff: datetime, security_terms: tuple[str, ...] = ()) -> list[dict]:
    """Stage KEV and HF independently: a failure in one never sinks the other."""
    out: list[dict] = []
    for source in sr.sources_of_type("kev_json"):
        print(f"-> {source['name']}: {source['handle']}")
        try:
            out += kev_candidates(fetch_json(source["handle"]), source, rules, cutoff)
        except Exception as exc:  # noqa: BLE001
            print(f"   ! KEV ingest failed: {exc}", file=sys.stderr)
    for source in sr.sources_of_type("hf_papers"):
        print(f"-> {source['name']}: {source['handle']}")
        try:
            items: list = []
            today = c.utcnow().date()
            for back in range(pg.HF_LOOKBACK_DAYS):
                day = (today - timedelta(days=back)).isoformat()
                day_items = fetch_json(source["handle"], date=day, limit=100)
                if isinstance(day_items, list):
                    items += day_items
            out += hf_candidates(items, source, rules, cutoff, security_terms)
        except Exception as exc:  # noqa: BLE001
            print(f"   ! HF Daily Papers ingest failed: {exc}", file=sys.stderr)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't write changes")
    args = ap.parse_args()

    cfg = c.load_yaml(c.SOURCES_FILE)
    terms = tuple(t.lower() for t in cfg.get("conferences", {}).get("security_terms", []))
    cutoff = c.utcnow() - timedelta(days=c.load_config().max_age_days)
    candidates = collect(cfg["classification"], cutoff, terms)
    print(f"\nFound {len(candidates)} JSON-feed candidate(s).")
    if args.dry_run:
        for cand in candidates:
            print(f"   [{cand['guess_topic']}/{cand['guess_domain']}] {cand['title'][:90]}")
        return 0
    added = c.add_candidates(candidates)
    print(f"Staged {len(added)} new candidate(s) in {c.CANDIDATES_FILE.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
