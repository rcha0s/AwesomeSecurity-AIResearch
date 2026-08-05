"""Tests for scripts/dedupe_stories.py — story-key extraction, collision
detection, and cross-pool index seeding for the news lane."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import common as c
import dedupe_stories as ds
from conftest import make_entry


# --- Canonical URL ---------------------------------------------------------
def test_canonical_url_strips_tracking_and_lowercases_host():
    assert ds.canonical_url(
        "HTTPS://Www.Example.com/A/b/?utm_source=twitter&utm_campaign=x&q=1#frag"
    ) == "https://example.com/A/b?q=1"


def test_canonical_url_returns_input_on_garbage():
    assert ds.canonical_url("not-a-url") == "not-a-url"
    assert ds.canonical_url("") == ""


# --- Shingles / entities ---------------------------------------------------
def test_title_shingles_removes_stopwords_and_makes_trigrams():
    s = ds.title_shingles("Kimi K3 ships the full weights of the largest model")
    assert "kimi k3 ships" in s
    # 'the' stopped, so "the full" never appears as a trigram
    assert not any("the" in tri.split() for tri in s)


def test_entities_resolves_aliases_and_captures_bigrams():
    ents = ds.entities(
        "Anthropic caught its own models breaching containment",
        "Claude Opus and gpt-5.6 both hit the eval sandbox.",
    )
    # alias resolution
    assert "Anthropic" in ents
    assert "OpenAI" in ents  # gpt-5.6 → OpenAI


# --- Two-of-three collision rule -------------------------------------------
# Title similarity uses max(token-Jaccard, shingle-Jaccard) — synthetic
# fingerprints need BOTH populated (or both empty) or one signal short-circuits
# to 1.0. Keep helper honest by defaulting `tokens` to a derived set.
def _fp(**over) -> dict:
    base_shingles = over.get("shingles", {"kimi k3 open", "k3 open weights"})
    # Tokens derived from shingles for realism.
    tokens = set()
    for s in base_shingles:
        tokens.update(s.split())
    base = {
        "url": "https://a.com/x",
        "title": "Kimi K3 open weights",
        "tokens": over.get("tokens", tokens),
        "shingles": base_shingles,
        "entities": {"Moonshot"},
        "bucket": "2026-08-04",
    }
    base.update(over)
    return base


def test_collision_url_and_entities_2_of_3():
    a = _fp()
    b = _fp(shingles={"totally", "different", "title"})
    assert ds.is_collision(a, b)


def test_collision_shingles_and_entities_2_of_3():
    a = _fp()
    b = _fp(url="https://different.com/y",
            shingles={"kimi k3 open", "k3 open weights", "extra token more"})
    assert ds.is_collision(a, b)


def test_no_collision_with_only_entity_overlap():
    a = _fp()
    b = _fp(url="https://different.com/y",
            shingles={"totally", "different", "title"},
            tokens={"totally", "different", "title"})
    # Only entities overlap — 1/3, no collision.
    assert not ds.is_collision(a, b)


def test_no_collision_different_urls_and_shingles():
    a = _fp()
    b = _fp(url="https://different.com/y",
            shingles={"unrelated title tokens"},
            tokens={"unrelated", "title", "tokens"},
            entities={"Palantir"})
    assert not ds.is_collision(a, b)


# --- assign_story_id -------------------------------------------------------
def _news_row(title: str, url: str, entities_text: str = "") -> dict:
    return {
        "title": title,
        "source_url": url,
        "summary": entities_text,
        "published": datetime.now(UTC).strftime("%Y-%m-%d"),
    }


def test_assign_story_id_first_seen_is_new():
    idx = {}
    sid, is_new = ds.assign_story_id(
        _news_row("Kimi K3 ships full open weights", "https://moonshot.cn/kimi-k3"),
        idx, source_tier="high", source_name="Moonshot",
    )
    assert is_new
    assert sid in idx
    assert idx[sid]["corroborators"] == []


def test_assign_story_id_second_report_becomes_corroborator():
    idx = {}
    original = _news_row(
        "Kimi K3 ships full open weights of the largest AI model",
        "https://moonshot.cn/kimi-k3",
        entities_text="Moonshot's Kimi K3 hits open weights.",
    )
    dupe = _news_row(
        "Moonshot Kimi K3 open weights ship for the largest model",
        "https://huggingface.co/blog/kimi-k3",
        entities_text="A HuggingFace mirror of Moonshot Kimi K3.",
    )
    sid1, new1 = ds.assign_story_id(original, idx,
                                    source_tier="high", source_name="Moonshot")
    sid2, new2 = ds.assign_story_id(dupe, idx,
                                    source_tier="medium",
                                    source_name="Hugging Face")
    assert new1 and not new2
    assert sid1 == sid2
    assert len(idx[sid1]["corroborators"]) == 1
    assert idx[sid1]["corroborators"][0]["source_name"] == "Hugging Face"


def test_higher_tier_wins_and_promotes_fingerprint():
    idx = {}
    lower = _news_row(
        "Kimi K3 ships full open weights of the largest AI model",
        "https://hn.example.com/kimi-k3",
        entities_text="Moonshot Kimi K3.",
    )
    higher = _news_row(
        "Moonshot Kimi K3 open weights ship for the largest AI model",
        "https://moonshot.cn/kimi-k3",
        entities_text="Moonshot's Kimi K3.",
    )
    sid_a, _ = ds.assign_story_id(lower, idx, source_tier="medium",
                                  source_name="HN mirror")
    sid_b, _ = ds.assign_story_id(higher, idx, source_tier="high",
                                  source_name="Moonshot")
    assert sid_a == sid_b
    assert idx[sid_a]["winner_tier"] == "high"


def test_unrelated_stories_do_not_collide():
    idx = {}
    a = _news_row("Anthropic caught its own models breaching containment",
                  "https://anthropic.com/news/incident")
    b = _news_row("Kimi K3 ships full open weights",
                  "https://moonshot.cn/kimi-k3")
    _, new1 = ds.assign_story_id(a, idx, source_tier="high",
                                 source_name="Anthropic")
    _, new2 = ds.assign_story_id(b, idx, source_tier="high",
                                 source_name="Moonshot")
    assert new1 and new2
    assert len(idx) == 2


# --- Cross-pool seed -------------------------------------------------------
def test_seed_from_pools_blocks_track_a_repeat(sandbox):
    """A story already in the research pool should block a Track B repeat."""
    pool = c.load_pool("ai-security")
    pool["entries"].append(make_entry(
        topic="ai-security",
        title="Anthropic caught its own models breaching containment",
        source_url="https://www.anthropic.com/news/containment",
        published=datetime.now(UTC).strftime("%Y-%m-%d"),
    ))
    c.save_pool("ai-security", pool)

    idx = {}
    added = ds.seed_index_from_pools(idx)
    assert added == 1

    dupe = _news_row(
        "Anthropic caught its own models breaching containment (post-mortem)",
        "https://embracethered.com/anthropic-containment",
        entities_text="Anthropic containment post-mortem.",
    )
    _, is_new = ds.assign_story_id(dupe, idx, source_tier="medium",
                                   source_name="ETR")
    assert not is_new


def test_seed_ignores_stale_pool_entries(sandbox):
    stale = make_entry(
        topic="ai-security",
        title="Old news that shouldn't hit the dedup window",
        source_url="https://old.example.com/x",
        published=(datetime.now(UTC) - timedelta(days=60)).strftime("%Y-%m-%d"),
    )
    pool = c.load_pool("ai-security")
    pool["entries"].append(stale)
    c.save_pool("ai-security", pool)
    idx = {}
    assert ds.seed_index_from_pools(idx) == 0


# --- Index persistence -----------------------------------------------------
def test_save_and_load_index_round_trips(sandbox, monkeypatch):
    monkeypatch.setattr(ds, "STORY_INDEX", sandbox / "data" / "news_stories.json")
    idx = {}
    ds.assign_story_id(
        _news_row("Kimi K3 ships full open weights of the largest AI model",
                  "https://moonshot.cn/kimi-k3", entities_text="Moonshot Kimi K3."),
        idx, source_tier="high", source_name="Moonshot",
    )
    ds.save_index(idx)
    reloaded = ds.load_index()
    sid = next(iter(idx))
    assert sid in reloaded
    assert reloaded[sid]["winner_tier"] == "high"


def test_prune_index_drops_old_keys():
    now = datetime.now(UTC)
    fresh = {"fp": {"url": "", "shingles": [], "entities": [], "bucket": "x"},
             "corroborators": [], "winner_tier": "high",
             "first_seen": (now - timedelta(days=10)).strftime("%Y-%m-%d")}
    stale = {"fp": {"url": "", "shingles": [], "entities": [], "bucket": "x"},
             "corroborators": [], "winner_tier": "high",
             "first_seen": (now - timedelta(days=45)).strftime("%Y-%m-%d")}
    pruned = ds.prune_index({"a": fresh, "b": stale}, now=now)
    assert "a" in pruned and "b" not in pruned
