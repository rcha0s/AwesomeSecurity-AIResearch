"""Tests for scripts/rerank.py — decay, composite, and sort."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import common as c
import pytest
import rerank
from conftest import make_entry


def test_score_entry_fills_scores():
    conf = c.load_config()
    now = datetime(2026, 7, 1, tzinfo=UTC)
    scored = rerank.score_entry(make_entry(scores={"novelty": 50, "relevance": 60}), conf, now=now)
    s = scored["scores"]
    assert "newness" in s and "composite" in s and "scored_at" in s
    assert s["composite"] == c.composite_score(s, conf.weights)


def test_score_entry_keeps_scored_at_when_scores_unchanged():
    conf = c.load_config()
    now = datetime(2026, 7, 1, tzinfo=UTC)
    first = rerank.score_entry(make_entry(scores={"novelty": 50, "relevance": 60}), conf, now=now)
    first["scores"]["scored_at"] = "2026-01-01T00:00:00Z"
    again = rerank.score_entry(first, conf, now=now)
    assert again == first  # byte-identical: no drift for the render job
    later = rerank.score_entry(first, conf, now=datetime(2026, 9, 1, tzinfo=UTC))
    assert later["scores"]["newness"] != first["scores"]["newness"]
    assert later["scores"]["scored_at"] != "2026-01-01T00:00:00Z"


def test_score_entry_defaults_missing_axes():
    conf = c.load_config()
    scored = rerank.score_entry(make_entry(scores=None, date="2026-07"), conf)
    assert scored["scores"]["novelty"] == 0
    assert scored["scores"]["relevance"] == 0


def test_rerank_pool_sorts_by_composite(sandbox):
    pool = c.load_pool("ai-research")
    pool["entries"] = [
        make_entry(title="low", source_url="https://a/1", scores={"novelty": 5, "relevance": 5}),
        make_entry(title="high", source_url="https://a/2", scores={"novelty": 95, "relevance": 95}),
    ]
    c.save_pool("ai-research", pool)
    out = rerank.rerank_pool("ai-research")
    assert out["entries"][0]["title"] == "high"
    # persisted
    assert c.load_pool("ai-research")["entries"][0]["title"] == "high"


def test_rerank_all_scores_pools(sandbox):
    for topic, domain in (
        ("ai-research", "air.agents"),
        ("ai-security", "ais.prompt-injection"),
    ):
        pool = c.load_pool(topic)
        pool["entries"] = [make_entry(topic=topic, domain=domain, source_url=f"https://a/{topic}")]
        c.save_pool(topic, pool)
    rerank.rerank_all()
    for topic in ("ai-research", "ai-security"):
        assert "composite" in c.load_pool(topic)["entries"][0]["scores"]


def test_rerank_prunes_stale_to_archive(sandbox):
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(
            topic="ai-security",
            domain="ais.prompt-injection",
            title="fresh",
            source_url="https://a/fresh",
            published="2099-01-01",
        ),
        make_entry(
            topic="ai-security",
            domain="ais.prompt-injection",
            title="stale",
            source_url="https://a/stale",
            published="2000-01-01",
        ),
    ]
    c.save_pool("ai-security", pool)
    rerank.rerank_pool("ai-security")
    live = [e["title"] for e in c.load_pool("ai-security")["entries"]]
    assert live == ["fresh"]
    archived = [e["title"] for e in c.load_json(c.ARCHIVE_FILE, default=[])]
    assert "stale" in archived


def test_rerank_main_cli(sandbox, monkeypatch):
    pool = c.load_pool("ai-research")
    pool["entries"] = [make_entry(source_url="https://a/cli")]
    c.save_pool("ai-research", pool)
    monkeypatch.setattr("sys.argv", ["rerank", "--topic", "ai-research"])
    assert rerank.main() == 0
    assert "composite" in c.load_pool("ai-research")["entries"][0]["scores"]


def test_rerank_keeps_old_news_and_editorial_out_of_the_archive(sandbox):
    """Findings age out; news is kept like claims (Rohan, 2026-10-19)."""
    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    old = {"topic": "ai-security", "domain": "ais.prompt-injection", "published": "2000-01-01"}
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(**old, title="old finding", source_url="https://a/f"),
        make_entry(**old, title="old news", source_url="https://a/n", source_id="rss:news"),
        make_entry(
            **old,
            title="old editorial",
            source_url="https://a/e",
            editorial={"promoted": True, "at": "2000-01-02"},
        ),
    ]
    c.save_pool("ai-security", pool)
    rerank.rerank_pool("ai-security")
    live = sorted(e["title"] for e in c.load_pool("ai-security")["entries"])
    assert live == ["old editorial", "old news"]
    archived = [e["title"] for e in c.load_json(c.ARCHIVE_FILE, default=[])]
    assert archived == ["old finding"]


def test_rerank_restores_news_that_was_archived_before(sandbox):
    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    old = {"topic": "ai-security", "domain": "ais.prompt-injection", "published": "2000-01-01"}
    news = make_entry(**old, title="news", source_url="https://a/n", source_id="rss:news")
    finding = make_entry(**old, title="finding", source_url="https://a/f")
    other_topic = make_entry(
        **{**old, "topic": "ai-research"},
        title="other",
        source_url="https://a/o",
        source_id="rss:news",
    )
    c.save_json(c.ARCHIVE_FILE, [news, finding, other_topic])
    rerank.rerank_pool("ai-security")
    assert [e["title"] for e in c.load_pool("ai-security")["entries"]] == ["news"]
    assert [e["title"] for e in c.load_json(c.ARCHIVE_FILE)] == ["finding", "other"]


# ------------------------------------------------------------ bar re-judging
# merge_analysis holds an entry for review once, at merge time. Rerank re-judges the
# hold under the current config, so lowering curation.min_novelty frees what the old
# bar held, and frees nothing held for another reason.


def held(**over):
    entry = make_entry(
        scores={"novelty": 55, "relevance": 80},
        needs_review=True,
        verified=True,
        grounding_score=1.0,
        source_rank=70,
    )
    entry.update(over)
    return entry


def test_a_finding_held_only_by_a_bar_the_config_no_longer_sets_is_released():
    conf = c.load_config()
    e = held()
    assert rerank.release_bar_holds([e], conf) == 1
    assert e["needs_review"] is False


def test_it_is_still_held_below_the_current_bar():
    conf = c.load_config()
    low_nov = held(scores={"novelty": conf.curation["min_novelty"] - 1, "relevance": 80})
    low_rel = held(scores={"novelty": 90, "relevance": conf.curation["min_relevance"] - 1})
    assert rerank.release_bar_holds([low_nov, low_rel], conf) == 0
    assert low_nov["needs_review"] and low_rel["needs_review"]


@pytest.mark.parametrize(
    "over",
    [
        {"verified": False},  # the verifier refuted it
        {"grounding_score": 0.5},  # an excerpt is not in the source
        {"lessons": [{"point": "x", "grounded": False}]},
        {"confidence": 0.2},  # low analyzer confidence
        {"scores": None},  # never scored
        {"news_brief": {"reason": "r", "markers": []}},  # a brief is news-lane only
        {"domain_hold": "not a taxonomy id"},
        {"readability_hold": "readability: too long"},
        {"citation_hold": "reddit-only citation"},
        {"source_rank": 10, "grounding_score": None},  # low authority, quotes unconfirmed
    ],
)
def test_a_hold_for_any_other_reason_is_never_released(over):
    conf = c.load_config()
    e = held(**over)
    assert rerank.release_bar_holds([e], conf) == 0
    assert e["needs_review"] is True


def test_an_entry_that_is_not_held_is_left_alone_and_rerank_never_adds_a_hold():
    conf = c.load_config()
    fine = held(needs_review=False)
    bad = held(needs_review=False, scores={"novelty": 1, "relevance": 1})
    assert rerank.release_bar_holds([fine, bad], conf) == 0
    assert fine["needs_review"] is False and bad["needs_review"] is False


def test_rerank_pool_releases_through_the_pool_path(tmp_path, monkeypatch):
    conf = c.load_config()
    e = held(date="2026-11-10")
    pool = {"entries": [e], "domains": []}
    monkeypatch.setattr(c, "load_pool", lambda t: pool)
    monkeypatch.setattr(c, "save_pool", lambda t, p: None)
    monkeypatch.setattr(c, "load_sources_by_id", lambda: {})
    monkeypatch.setattr(c, "unarchive", lambda pred: [])
    monkeypatch.setattr(c, "archive_entries", lambda stale: 0)
    out = rerank.rerank_pool(next(iter(c.TOPICS)), conf, now=datetime(2026, 11, 14, tzinfo=UTC))
    assert out["entries"][0]["needs_review"] is False
