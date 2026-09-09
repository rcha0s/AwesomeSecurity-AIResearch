"""Tests for the sitemap-based ingestor (research_index sources with no feed)."""

from __future__ import annotations

from datetime import UTC, datetime

import common as c
import ingest_sitemap as ism

RULES = c.load_yaml(c.SOURCES_FILE)["classification"]

ANTHROPIC_SOURCE = {
    "id": "research_index:https-www-anthropic-com-news",
    "name": "Anthropic News",
    "url": "https://www.anthropic.com/news",
    "handle": "https://www.anthropic.com/news",
    "domains": [],
    "rank": 75.0,
    "topics": ["ai-research", "ai-security"],
}

SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://www.anthropic.com/news/disrupting-ai-espionage</loc><lastmod>2026-09-07T09:00:00.000Z</lastmod></url>
<url><loc>https://www.anthropic.com/careers</loc><lastmod>2026-09-07T09:00:00.000Z</lastmod></url>
<url><loc>https://www.anthropic.com/news/old-post</loc><lastmod>2020-01-01T00:00:00.000Z</lastmod></url>
</urlset>
"""

READER_BODY = (
    "Title: Disrupting the first reported AI-orchestrated cyber espionage campaign\n\n"
    "URL Source: https://www.anthropic.com/news/disrupting-ai-espionage\n\n"
    "Markdown Content:\nA state-sponsored actor used an agentic AI harness to "
    "orchestrate a prompt-injection-driven espionage campaign against corporate "
    "targets, automating most of the intrusion chain end to end."
)


def test_sitemap_url_for_derives_site_root():
    assert ism.sitemap_url_for("https://www.anthropic.com/research") == (
        "https://www.anthropic.com/sitemap.xml"
    )


def test_path_prefix_of_adds_trailing_slash():
    assert ism.path_prefix_of("https://www.anthropic.com/news") == "/news/"


def test_title_from_slug_humanizes_hyphens():
    assert (
        ism.title_from_slug("https://www.anthropic.com/news/disrupting-ai-espionage")
        == "Disrupting Ai Espionage"
    )


def test_title_from_reader_text_parses_title_line():
    assert (
        ism.title_from_reader_text(READER_BODY, "https://www.anthropic.com/news/x")
        == "Disrupting the first reported AI-orchestrated cyber espionage campaign"
    )


def test_title_from_reader_text_falls_back_to_slug_without_title_line():
    body = "Markdown Content:\nno title line here"
    assert ism.title_from_reader_text(
        body, "https://www.anthropic.com/news/disrupting-ai-espionage"
    ) == "Disrupting Ai Espionage"


def test_url_to_candidate_classifies_from_real_fetched_body(monkeypatch):
    # The bare URL slug ("disrupting-ai-espionage") doesn't hit any keyword —
    # this is exactly why classification needs the real fetched body, not
    # just the slug: real Anthropic titles miss the keyword classifier most
    # of the time when judged on the slug alone.
    monkeypatch.setattr(ism, "fetch_body", lambda url: READER_BODY)

    cand = ism.url_to_candidate(
        "https://www.anthropic.com/news/disrupting-ai-espionage",
        "2026-09-07T09:00:00.000Z",
        ANTHROPIC_SOURCE,
        RULES,
    )
    assert cand is not None
    assert cand["guess_domain"] == "AI Security"
    assert cand["title"] == "Disrupting the first reported AI-orchestrated cyber espionage campaign"
    assert cand["published"] == "2026-09-07"
    assert cand["date"] == "2026-09"
    assert cand["discovered_via"] == "sitemap"
    assert cand["source_id"] == ANTHROPIC_SOURCE["id"]
    assert cand["article_url"] == "https://www.anthropic.com/news/disrupting-ai-espionage"
    assert cand["raw_path"] is not None


def test_url_to_candidate_falls_back_to_slug_when_fetch_fails(monkeypatch):
    monkeypatch.setattr(ism, "fetch_body", lambda url: None)

    cand = ism.url_to_candidate(
        "https://www.anthropic.com/news/disrupting-ai-espionage",
        "2026-09-07T09:00:00.000Z",
        # slug alone doesn't classify without a domain fallback, so give one
        # to isolate what this test checks: graceful degradation, not the
        # classifier itself.
        dict(ANTHROPIC_SOURCE, domains=["AI Security"]),
        RULES,
    )
    assert cand is not None
    assert cand["title"] == "Disrupting Ai Espionage"
    assert cand["raw_path"] is None
    assert cand["excerpt"] == ""


def test_url_to_candidate_drops_off_topic_with_no_domain_fallback(monkeypatch):
    monkeypatch.setattr(ism, "fetch_body", lambda url: None)
    cand = ism.url_to_candidate(
        "https://www.anthropic.com/news/completely-unrelated-nonsense-words",
        "2026-09-07T09:00:00.000Z",
        ANTHROPIC_SOURCE,
        RULES,
    )
    assert cand is None


def test_fetch_sitemap_parses_loc_and_lastmod(monkeypatch):
    class _Resp:
        content = SITEMAP_XML.encode("utf-8")

        def raise_for_status(self):
            return None

    def fake_get(url, timeout=None, headers=None):
        assert headers == {"User-Agent": c.HTTP_USER_AGENT}
        return _Resp()

    monkeypatch.setattr(ism.requests, "get", fake_get)
    entries = ism.fetch_sitemap("https://www.anthropic.com/sitemap.xml")
    assert len(entries) == 3
    assert entries[0] == (
        "https://www.anthropic.com/news/disrupting-ai-espionage",
        "2026-09-07T09:00:00.000Z",
    )


def test_fetch_sitemap_returns_empty_on_non_xml_response(monkeypatch):
    class _Resp:
        content = b"<!doctype html><html>not a sitemap</html>"

        def raise_for_status(self):
            return None

    monkeypatch.setattr(ism.requests, "get", lambda *a, **k: _Resp())
    assert ism.fetch_sitemap("https://red.anthropic.com/sitemap.xml") == []


def test_fetch_sitemap_returns_empty_on_request_failure(monkeypatch):
    def fake_get(*a, **k):
        raise ConnectionError("boom")

    monkeypatch.setattr(ism.requests, "get", fake_get)
    assert ism.fetch_sitemap("https://alignment.anthropic.com/sitemap.xml") == []


def test_collect_filters_by_prefix_and_freshness(monkeypatch):
    monkeypatch.setattr(ism.sr, "sources_of_type", lambda stype: [ANTHROPIC_SOURCE])
    monkeypatch.setattr(ism, "fetch_body", lambda url: READER_BODY)

    class _Resp:
        content = SITEMAP_XML.encode("utf-8")

        def raise_for_status(self):
            return None

    monkeypatch.setattr(ism.requests, "get", lambda *a, **k: _Resp())

    cutoff = datetime(2026, 8, 1, tzinfo=UTC)
    candidates = ism.collect(RULES, cutoff)

    # /careers is outside the /news/ prefix; the 2020 post is outside the cutoff.
    # Neither should even trigger a fetch_body call for the excluded URLs.
    urls = [cand["article_url"] for cand in candidates]
    assert urls == ["https://www.anthropic.com/news/disrupting-ai-espionage"]


def test_collect_skips_sources_with_no_usable_sitemap(monkeypatch, capsys):
    monkeypatch.setattr(ism.sr, "sources_of_type", lambda stype: [ANTHROPIC_SOURCE])

    def fake_get(*a, **k):
        raise ConnectionError("boom")

    monkeypatch.setattr(ism.requests, "get", fake_get)

    candidates = ism.collect(RULES, datetime(2020, 1, 1, tzinfo=UTC))
    assert candidates == []
    assert "no usable sitemap" in capsys.readouterr().out
