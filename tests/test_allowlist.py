"""Tests for scripts/allowlist.py — every fetched host is in the cloud allowlist."""

from __future__ import annotations

import allowlist


def test_source_hosts_takes_feed_handle_and_site_url():
    sources = [
        {"type": "rss", "handle": "https://feeds.example.com/rss", "url": "https://Example.com"},
        {"type": "research_index", "url": "https://www.anthropic.com/research"},
        {"type": "rss", "handle": "https://off.example.org/feed", "active": False},
        {"type": "x_account", "handle": "@someone"},
    ]
    assert allowlist.source_hosts(sources) == {
        "feeds.example.com",
        "example.com",
        "www.anthropic.com",
    }


def test_fixed_hosts_cover_the_ingestor_apis():
    import common
    import ingest_conferences
    import ingest_hn

    for url in (common.JINA_READER, ingest_conferences.ARXIV_API, ingest_hn.HN_SEARCH):
        assert any(h in url for h in allowlist.FIXED_HOSTS), url


def test_fixed_hosts_cover_the_curator_link_ingestor():
    """It fetches the sitemap and issue pages itself; the linked articles go
    through r.jina.ai (fetch_raw.py) like every other candidate."""
    from urllib.parse import urlparse

    import common
    import eval_recall

    for url in (eval_recall.TLDRSEC_SITEMAP, "https://tldrsec.com/p/tldr-sec-350",
                common.JINA_READER):  # fmt: skip
        assert urlparse(url).hostname in allowlist.FIXED_HOSTS, url


def test_fixed_hosts_cover_the_recall_eval_curators():
    import eval_recall

    for url in (eval_recall.TLDRSEC_SITEMAP, *eval_recall.SIMON_FEEDS, eval_recall.KEV_URL):
        assert any(h in url for h in allowlist.FIXED_HOSTS), url
