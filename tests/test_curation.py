"""Tests for the vetted-only curation gate + REVIEW.md queue."""

from __future__ import annotations

import json

import common as c
import generate_review as gr
import generate_site as g
from conftest import make_entry


def test_is_curated_gate():
    conf = c.load_config()
    # high scores, not flagged -> curated
    assert c.is_curated(make_entry(scores={"novelty": 80, "relevance": 80}), conf)
    # flagged -> not curated regardless of score
    assert not c.is_curated(make_entry(needs_review=True), conf)
    # below composite floor -> not curated
    low = make_entry(date="2020-01", scores={"novelty": 0, "relevance": 0})
    assert not c.is_curated(low, conf)


def test_is_curated_respects_verification():
    conf = c.load_config()
    base = dict(scores={"novelty": 80, "relevance": 80}, grounding_score=1.0)
    assert c.is_curated(make_entry(verified=True, **base), conf)
    assert not c.is_curated(make_entry(verified=False, **base), conf)  # refuted
    assert c.is_curated(make_entry(**base), conf)  # not-yet-verified is not penalized
    assert "failed independent verification" in c.review_reason(make_entry(verified=False), conf)


def test_merge_flags_refuted(sandbox):
    import merge_analysis as m

    conf = c.load_config()
    refuted = make_entry(
        topic="ai-security",
        domain="ais.mcp-tools",
        source_url="https://a/r",
        source_rank=90,
        scores={"novelty": 90, "relevance": 90},
        verified=False,
    )
    merged, _, _, _ = m.merge([refuted], conf)
    assert merged[0]["needs_review"] is True


def test_is_curated_rejects_ungrounded():
    conf = c.load_config()
    good = make_entry(scores={"novelty": 80, "relevance": 80}, grounding_score=1.0)
    bad = make_entry(scores={"novelty": 80, "relevance": 80}, grounding_score=0.5)
    unverifiable = make_entry(scores={"novelty": 80, "relevance": 80}, grounding_score=None)
    assert c.is_curated(good, conf)
    assert not c.is_curated(bad, conf)  # a bad quote drops it to review
    assert c.is_curated(unverifiable, conf)  # unverifiable != ungrounded


def test_is_curated_rejects_unscored_even_if_fresh():
    """An unscored but recent entry must NOT be curated on newness alone."""
    conf = c.load_config()
    unscored = make_entry(published="2099-01-01", scores={})  # future -> high newness
    unscored.pop("scores", None)
    assert not c.is_scored(unscored)
    assert not c.is_curated(unscored, conf)
    assert "not yet scored" in c.review_reason(unscored, conf)


def test_review_reason():
    conf = c.load_config()
    assert "needs_review" in c.review_reason(make_entry(needs_review=True), conf)
    # scored but below the composite floor -> "floor" reason
    assert "floor" in c.review_reason(
        make_entry(date="2020-01", scores={"novelty": 5, "relevance": 5}), conf
    )


def test_weights_must_sum_to_one(tmp_path, monkeypatch):
    import pytest

    bad = tmp_path / "config.yaml"
    bad.write_text(
        "weights: {newness: 0.5, novelty: 0.5, relevance: 0.5}\n"
        "max_age_days: 31\nhalf_life_days: 18\nskill_composite_threshold: 70\n"
        "confidence_min: 0.55\ncuration: {}\nlimits: {}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        c.load_config(bad)


def test_generate_site_excludes_review_items(sandbox):
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(
            title="vetted", source_url="https://a/1", scores={"novelty": 80, "relevance": 80}
        ),
        make_entry(title="flagged", source_url="https://a/2", needs_review=True),
    ]
    c.save_pool("ai-security", pool)
    g.main()
    page = (sandbox / "ai-security" / "README.md").read_text(encoding="utf-8")
    assert "vetted" in page
    assert "flagged" not in page  # review item is not on the topic page
    assert "held for review" in page


def test_generate_review_lists_held_items(sandbox):
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(
            title="vetted", source_url="https://a/1", scores={"novelty": 80, "relevance": 80}
        ),
        make_entry(title="flagged", source_url="https://a/2", needs_review=True),
    ]
    c.save_pool("ai-security", pool)
    assert gr.main() == 0
    review = (sandbox / "REVIEW.md").read_text(encoding="utf-8")
    assert "https://a/2" in review  # the flagged item is listed
    assert "https://a/1" not in review  # the vetted item is not


def test_kept_news_is_not_held_for_review(sandbox):
    """News never ages out, so it must not pile up in REVIEW.md."""
    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(title="news", source_url="https://a/n", source_id="rss:news", needs_review=True),
        make_entry(title="flagged", source_url="https://a/2", needs_review=True),
    ]
    c.save_pool("ai-security", pool)
    assert gr.main() == 0
    review = (sandbox / "REVIEW.md").read_text(encoding="utf-8")
    assert "https://a/2" in review and "https://a/n" not in review
    g.write_topic("ai-security", c.load_config(), "now")
    assert "1 held for review" in (sandbox / "ai-security" / "README.md").read_text()


def _news_pool(sandbox, entries):
    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    pool = c.load_pool("ai-security")
    pool["entries"] = entries
    c.save_pool("ai-security", pool)


def test_an_ungrounded_news_story_waits_in_review_with_its_reason(sandbox):
    """Kept in the pool but rendered nowhere is the one state REVIEW.md must not miss."""
    _news_pool(
        sandbox,
        [
            make_entry(
                title="bad quote",
                source_url="https://a/bad",
                source_id="rss:news",
                grounding_score=0.5,
            ),
            make_entry(title="good news", source_url="https://a/good", source_id="rss:news"),
        ],
    )
    conf = c.load_config()
    sources = c.load_sources_by_id()
    bad, good = c.load_pool("ai-security")["entries"]
    assert c.is_news_story(bad, conf, sources) and c.is_held(bad, conf, sources)
    assert not c.is_held(good, conf, sources)
    assert gr.main() == 0
    review = (sandbox / "REVIEW.md").read_text(encoding="utf-8")
    assert "https://a/bad" in review and "https://a/good" not in review
    assert "news story: excerpt not grounded in source" in review
