"""Tests for the sitemap-based ingestor (research_index sources with no feed)."""

from __future__ import annotations

from datetime import UTC, datetime

import common as c
import ingest_sitemap as ism
import pytest

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
    assert (
        ism.title_from_reader_text(body, "https://www.anthropic.com/news/disrupting-ai-espionage")
        == "Disrupting Ai Espionage"
    )


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
    assert cand["guess_label"] == "AI Security"
    assert cand["guess_domain"].startswith("ais.")
    assert cand["title"] == "Disrupting the first reported AI-orchestrated cyber espionage campaign"
    assert cand["published"] == "2026-09-07"
    assert cand["date"] == "2026-09"
    assert cand["discovered_via"] == "sitemap"
    assert cand["source_id"] == ANTHROPIC_SOURCE["id"]
    assert cand["article_url"] == "https://www.anthropic.com/news/disrupting-ai-espionage"
    assert cand["raw_path"] is not None


def test_a_page_that_cannot_be_fetched_is_dropped_not_dated_by_lastmod(monkeypatch):
    # 2026-10-25: three failed fetches staged 2022 and Dec 2025 posts on a
    # rebuild's lastmod. Without the page there is no date of its own.
    calls = []
    monkeypatch.setattr(c, "fetch_readable", lambda url, **kw: calls.append(url) or 1 / 0)
    cand = ism.url_to_candidate(
        "https://www.anthropic.com/news/disrupting-ai-espionage",
        "2026-09-07T09:00:00.000Z",
        dict(ANTHROPIC_SOURCE, domains=["AI Security"]),
        RULES,
    )
    assert cand is None
    assert len(calls) == 2  # retried once before giving up


def test_one_failed_fetch_is_retried(monkeypatch):
    bodies = iter([None, READER_BODY])

    def flaky(url, **kw):
        body = next(bodies)
        if body is None:
            raise TimeoutError
        return body

    monkeypatch.setattr(c, "fetch_readable", flaky)
    assert ism.fetch_body("https://www.anthropic.com/news/x") == READER_BODY


def test_url_to_candidate_drops_off_topic_with_no_domain_fallback(monkeypatch):
    monkeypatch.setattr(
        ism, "fetch_body", lambda url: "Title: Completely unrelated nonsense words\n"
    )
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


def _old_post_body(published: str) -> str:
    return READER_BODY.replace(
        "\n\nMarkdown Content:", f"\n\nPublished Time: {published}\n\nMarkdown Content:"
    )


def test_reader_published_reads_the_page_date_not_the_body():
    assert ism.reader_published(_old_post_body("2023-07-11T00:00:00.000Z")) == datetime(
        2023, 7, 11, tzinfo=UTC
    )
    assert ism.reader_published(READER_BODY) is None
    assert ism.reader_published(None) is None
    body = READER_BODY + "\n" + "x" * 1200 + "\nPublished Time: 2020-01-01"
    assert ism.reader_published(body) is None  # header only, never quoted body text


def test_page_publish_time_overrides_a_rebuilt_lastmod(monkeypatch):
    """2026-10-22: a site rebuild re-dated 2021-2025 Anthropic posts, so 111 of
    154 sitemap candidates were stale pages with a fresh <lastmod>."""
    monkeypatch.setattr(ism.sr, "sources_of_type", lambda stype: [ANTHROPIC_SOURCE])
    monkeypatch.setattr(ism, "fetch_body", lambda url: _old_post_body("2023-07-11"))

    class _Resp:
        content = SITEMAP_XML.encode("utf-8")

        def raise_for_status(self):
            return None

    monkeypatch.setattr(ism.requests, "get", lambda *a, **k: _Resp())
    assert ism.collect(RULES, datetime(2026, 8, 1, tzinfo=UTC)) == []
    monkeypatch.setattr(ism, "fetch_body", lambda url: _old_post_body("2026-07-10"))
    (cand,) = ism.collect(RULES, datetime(2026, 6, 20, tzinfo=UTC))
    assert cand["published"] == "2026-07-10"  # the page's date, not lastmod's 09-07


@pytest.mark.parametrize(
    "stated, expected",
    [
        ("Tue, 11 Jul 2023 00:00:00 GMT", datetime(2023, 7, 11, tzinfo=UTC)),  # RFC 1123
        ("Tue, 11 Jul 2023 09:30:00 +0200", datetime(2023, 7, 11, 7, 30, tzinfo=UTC)),
        ("July 11, 2023", datetime(2023, 7, 11, tzinfo=UTC)),  # long form
        ("2023-07-11T00:00:00.000Z", datetime(2023, 7, 11, tzinfo=UTC)),
        ("2023-07-11", datetime(2023, 7, 11, tzinfo=UTC)),
        ("July 2023", None),  # no day: dateutil would invent one
        ("Jul 11", None),  # no year: dateutil would use this year's
        ("2026-07-17", None),  # more than a day ahead of the (pinned) clock
        ("soon", None),
    ],
)
def test_reader_published_takes_only_complete_past_dates(stated, expected):
    """Review of #89: `\\S+` cut RFC dates at the first space and dateutil filled
    the rest from today, re-dating a 2023 post to 2026 at full newness."""
    assert ism.reader_published(_old_post_body(stated)) == expected


def test_a_future_page_date_falls_back_to_lastmod(monkeypatch):
    monkeypatch.setattr(ism, "fetch_body", lambda url: _old_post_body("2031-01-01"))
    cand = ism.url_to_candidate(
        "https://www.anthropic.com/news/disrupting-ai-espionage",
        "2026-07-01T09:00:00.000Z",
        ANTHROPIC_SOURCE,
        RULES,
    )
    assert cand["published"] == "2026-07-01"


def test_collect_skips_sources_with_no_usable_sitemap(monkeypatch, capsys):
    monkeypatch.setattr(ism.sr, "sources_of_type", lambda stype: [ANTHROPIC_SOURCE])

    def fake_get(*a, **k):
        raise ConnectionError("boom")

    monkeypatch.setattr(ism.requests, "get", fake_get)

    candidates = ism.collect(RULES, datetime(2020, 1, 1, tzinfo=UTC))
    assert candidates == []
    assert "no usable sitemap" in capsys.readouterr().out
