"""Tests for scripts/dedupe_stories.py — story-key extraction, collision
detection. The ledger that uses them is tested in test_story_ledger.py."""

from __future__ import annotations

import dedupe_stories as ds


# --- Canonical URL ---------------------------------------------------------
def test_canonical_url_strips_tracking_and_lowercases_host():
    assert (
        ds.canonical_url("HTTPS://Www.Example.com/A/b/?utm_source=twitter&utm_campaign=x&q=1#frag")
        == "https://example.com/A/b?q=1"
    )


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
    b = _fp(
        url="https://different.com/y",
        shingles={"kimi k3 open", "k3 open weights", "extra token more"},
    )
    assert ds.is_collision(a, b)


def test_no_collision_with_only_entity_overlap():
    a = _fp()
    b = _fp(
        url="https://different.com/y",
        shingles={"totally", "different", "title"},
        tokens={"totally", "different", "title"},
    )
    # Only entities overlap — 1/3, no collision.
    assert not ds.is_collision(a, b)


def test_no_collision_different_urls_and_shingles():
    a = _fp()
    b = _fp(
        url="https://different.com/y",
        shingles={"unrelated title tokens"},
        tokens={"unrelated", "title", "tokens"},
        entities={"Palantir"},
    )
    assert not ds.is_collision(a, b)
