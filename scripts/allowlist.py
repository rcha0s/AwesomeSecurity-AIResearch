#!/usr/bin/env python3
"""
allowlist.py — Print the hosts a cloud scan must reach, for the routine's
Custom network allowlist (cloud-environments.md § Access levels).

Hosts come from every active registered source plus the fixed APIs the
ingestors and fetchers call. GitHub needs no entry: the cloud GitHub proxy
handles it. Paste the output into the environment's Custom allowlist, with
"include the default package list" on so `pip install` still works.

Usage:
    python scripts/allowlist.py
"""

from __future__ import annotations

from urllib.parse import urlparse

import eval_recall
import sources_registry as sr

FIXED_HOSTS = (
    "r.jina.ai",  # common.fetch_readable — every article fetch
    "export.arxiv.org",  # ingest_conferences ARXIV_API
    "huggingface.co",  # paper_gate HF_DAILY_API: the gate needs it even if hf_papers is off
    "www.reddit.com",  # ingest_reddit: OAuth token endpoint
    "oauth.reddit.com",  # ingest_reddit: listings
    "hn.algolia.com",  # ingest_hn / source_scout HN_SEARCH
    *eval_recall.CURATOR_HOSTS,  # recall eval curators; tldrsec.com is also ingest_curator_links
)
URL_TYPES = ("rss", "newsletter", "research_index", "kev_json", "hf_papers")


def source_hosts(sources: list[dict]) -> set[str]:
    hosts = set()
    for s in sources:
        if not s.get("active", True) or s.get("type") not in URL_TYPES:
            continue
        # Feeds are fetched from `handle` (aggregate.py), sitemaps from `url`.
        for field in ("handle", "url"):
            host = urlparse(s.get(field) or "").hostname
            if host:
                hosts.add(host.lower())
    return hosts


def main() -> int:
    for host in sorted(source_hosts(sr.load_sources()) | set(FIXED_HOSTS)):
        print(host)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
