"""Tests for the ingestion pure functions (aggregate, add) + fetch."""

from __future__ import annotations

import argparse

import add
import aggregate
import common as c
import ingest_conferences as ic
import pytest


def test_aggregate_classifies_tracks():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    ai = aggregate.build_candidate(
        {
            "link": "https://x/a",
            "title": "multi-agent orchestration harness",
            "summary": "tool use",
        },
        {"name": "F", "type": "blog", "domains": ["Agents & Harnesses"]},
        rules,
    )
    assert ai["guess_topic"] == "ai-research" and ai["guess_label"] == "Agents & Harnesses"
    assert ai["guess_domain"] == "air.agents"  # a taxonomy ID of the routed topic
    sec = aggregate.build_candidate(
        {"link": "https://x/b", "title": "request smuggling desync", "summary": "waf bypass"},
        {"name": "G", "type": "v", "domains": ["Web Application Security"]},
        rules,
    )
    assert sec["guess_topic"] == "product-security" and sec["guess_domain"] == "ps.appsec"


def test_classify_domain_does_not_false_positive_on_bare_hyperlinks():
    # Regression: a bare "http" keyword matched any text containing a link
    # (e.g. markdown "[text](https://...)"), so classify_domain silently
    # routed unrelated pages (math papers, product news) to Web Application
    # Security whenever the body happened to cite a URL. See the
    # "Formalizing Fermat's Last Theorem" false positive that surfaced this.
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    blob = (
        "we proved a theorem in the lean programming language. see the "
        "resulting proof at https://github.com/anthropics/example for details."
    )
    assert aggregate.classify_domain(blob, rules, []) is None


def test_collect_rss_passes_shared_user_agent(monkeypatch):
    # feedparser's default UA (e.g. "feedparser/6.x") gets 403'd by several
    # sources (OpenAI Blog, Wired, tldr;sec); every feed fetch must identify
    # with the shared, honest UA instead.
    calls = []

    def fake_parse(url, request_headers=None, **kwargs):
        calls.append((url, request_headers))

        class _Parsed:
            bozo = False
            entries: list = []

        return _Parsed()

    def fake_sources_of_type(kind):
        if kind == "rss":
            return [
                {
                    "id": "rss:example",
                    "name": "Example Feed",
                    "handle": "https://example.com/feed.xml",
                    "rank": 50.0,
                    "topics": [],
                }
            ]
        return []

    monkeypatch.setattr(aggregate.feedparser, "parse", fake_parse)
    monkeypatch.setattr(aggregate.sr, "sources_of_type", fake_sources_of_type)

    aggregate.collect_rss({}, c.utcnow())

    assert calls == [("https://example.com/feed.xml", {"User-Agent": c.HTTP_USER_AGENT})]


def test_add_source_via():
    assert add.source_via("https://www.linkedin.com/posts/x") == "linkedin"
    assert add.source_via("https://x.com/a/status/1") == "twitter"
    assert add.source_via("https://blog.example.com") == "manual"


def test_add_build_candidate(sandbox):
    args = argparse.Namespace(
        url="https://linkedin.com/posts/x",
        text=None,
        file=None,
        title="My title",
        author="Jane",
        date="2026-07",
        topic="ai-research",
    )
    cand = add.build_candidate(args, "Body text about agents.")
    assert cand["discovered_via"] == "linkedin"
    assert cand["guess_topic"] == "ai-research"
    assert cand["title"] == "My title"
    assert cand["raw_path"] is not None


def test_aggregate_strict_feed_requires_keyword():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    item = {"link": "https://x/a", "title": "unrelated philosophical musings", "summary": ""}
    # non-strict single-domain feed: fallback stages the unclassifiable item
    assert aggregate.build_candidate(item, {"name": "F", "domains": ["AI Security"]}, rules)
    # strict feed (arXiv firehose): no keyword match -> not staged
    strict = aggregate.build_candidate(
        {**item, "link": "https://x/b"},
        {"name": "F", "domains": ["AI Security"], "strict": True},
        rules,
    )
    assert strict is None


def test_github_candidate_uses_pushed_date():
    import ingest_github as ig

    src = {
        "id": "github_query:x",
        "rank": 55,
        "topics": ["ai-security"],
        "domains": ["AI Security"],
    }
    repo = {
        "fullName": "a/b",
        "url": "https://github.com/a/b",
        "stargazersCount": 100,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2026-07-10T00:00:00Z",
        "description": "x",
    }
    cand = ig.repo_to_candidate(repo, src, fetch=False, max_chars=100)
    assert cand["published"] == "2026-07-10"  # last-push date, not creation


def test_aggregate_build_candidate_none_cases():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    assert aggregate.build_candidate({"link": "", "title": "x"}, {"domains": []}, rules) is None
    # unclassifiable + multi-domain feed → no confident domain
    none = aggregate.build_candidate(
        {"link": "https://x/z", "title": "zzz qqq", "summary": ""},
        {"name": "F", "domains": ["AI Security", "Mobile Security"]},
        rules,
    )
    assert none is None


def test_add_resolve_text_variants(tmp_path):
    args = argparse.Namespace(text="pasted", file=None, url=None)
    assert add.resolve_text(args) == ("pasted", False)
    f = tmp_path / "body.txt"
    f.write_text("from file", encoding="utf-8")
    args = argparse.Namespace(text=None, file=str(f), url=None)
    assert add.resolve_text(args) == ("from file", False)
    with pytest.raises(SystemExit):
        add.resolve_text(argparse.Namespace(text=None, file=None, url=None))


def test_add_main_stages(sandbox, monkeypatch):
    monkeypatch.setattr(
        "sys.argv", ["add", "--text", "agents body", "--title", "T", "--topic", "ai-research"]
    )
    assert add.main() == 0
    assert len(c.load_candidates()) == 1


def test_fetch_readable_mocked(monkeypatch):
    class Resp:
        text = "clean article text"

        def raise_for_status(self):
            return None

    import requests

    monkeypatch.setattr(requests, "get", lambda *a, **k: Resp())
    assert c.fetch_readable("https://x/y") == "clean article text"


# --- ingest_conferences: acceptance filter + security gate ------------------


def test_is_accepted_distinguishes_acceptance_from_submission():
    accept = [
        "To appear in the 35th USENIX Security Symposium (USENIX Security 2026)",
        "Published at ISOC NDSS 2026",
        "Accepted to AISec'25 co-located with the 32nd ACM CCS",
        "camera-ready, ICML 2026",
        "In Proceedings of CCS 2026",
    ]
    reject = [
        "Submitted to NeurIPS 2026",
        "Under review at ICML",
        "9 pages, 6 figures",
        "",
    ]
    for comment in accept:
        assert ic.is_accepted(comment) is True, comment
    for comment in reject:
        assert ic.is_accepted(comment) is False, comment


def test_entry_to_candidate_requires_acceptance():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    item = {
        "title": "Backdoor attacks on LLM agents",
        "summary": "prompt injection and backdoor poisoning of agent tool use",
        "published": "2026-07-20T00:00:00Z",
        "link": "https://arxiv.org/abs/2607.00001",
        "comment": "Submitted to NeurIPS 2026",
    }
    assert ic.entry_to_candidate(item, "NeurIPS", rules) is None  # unreviewed
    item["comment"] = "Accepted at NeurIPS 2026"
    cand = ic.entry_to_candidate(item, "NeurIPS", rules)
    assert cand and cand["venue"] == "NeurIPS"
    assert cand["source_rank"] == ic.CONFERENCE_SOURCE_RANK


def test_entry_to_candidate_security_gate_filters_broad_venues():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    terms = ("backdoor", "adversarial", "prompt injection")
    off_thesis = {
        "title": "Symbiosis-Inspired Knowledge Distillation for Object Detection",
        "summary": "incremental object detection distillation",
        "published": "2026-07-20T00:00:00Z",
        "link": "https://arxiv.org/abs/2607.00002",
        "comment": "Accepted to ICML 2026",
    }
    # Gated (broad venue) -> dropped; ungated (security venue) -> judged on topic only.
    assert ic.entry_to_candidate(off_thesis, "ICML", rules, terms) is None
    on_thesis = {**off_thesis, "title": "Backdoor attacks via adversarial prompt injection"}
    assert ic.entry_to_candidate(on_thesis, "ICML", rules, terms) is not None
