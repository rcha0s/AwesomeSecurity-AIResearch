"""Tests for the editorial review track: importance signal, eligibility, promotion."""

from __future__ import annotations

import common as c
import importance as imp
import promote_editorial as pe
from conftest import make_entry


def _held(**over):
    """A held (needs_review) finding that is grounded + verified — editorial-eligible."""
    e = make_entry(**over)
    e["needs_review"] = True
    e.setdefault("id", c.make_id(e["title"], c.normalize_url(e["source_url"])))
    return e


# --- newsworthiness signal --------------------------------------------------


def test_event_signal_detects_cve_and_advisory():
    assert imp.event_signal({"title": "Foo (CVE-2026-16584) bypass"}) == 100.0
    assert imp.event_signal({"source_url": "https://github.com/advisories/GHSA-x"}) == 100.0
    assert imp.event_signal({"title": "A neat idea about prompts"}) == 0.0


def test_corroboration_saturates_at_three_sources():
    assert imp.corroboration_signal({"corroborating_sources": []}) == 0.0
    two = {"corroborating_sources": [{"url": "a"}, {"url": "b"}]}
    assert 0 < imp.corroboration_signal(two) < 100.0
    five = {"corroborating_sources": [{"url": str(i)} for i in range(5)]}
    assert imp.corroboration_signal(five) == 100.0  # capped


def test_trend_index_maps_member_url_to_cluster_momentum():
    trends = {
        "ai-security": [
            {"momentum": 17.0, "members": [{"url": "https://x/a"}, {"url": "https://x/b"}]},
            {"momentum": 5.0, "members": [{"url": "https://x/a"}]},  # lower — keep the max
        ]
    }
    idx = imp.build_trend_index(trends)
    assert idx[c.normalize_url("https://x/a")] == 17.0


def test_newsworthiness_rewards_trending_event_entry():
    conf = c.load_config()
    idx = {c.normalize_url("https://x/hot"): 20.0}
    hot = _held(
        source_url="https://x/hot",
        title="Breach via CVE-2026-1",
        scores={"novelty": 40, "relevance": 90},
        corroborating_sources=[{"url": "s1"}, {"url": "s2"}, {"url": "s3"}],
    )
    cold = _held(
        source_url="https://x/cold", title="A quiet idea", scores={"novelty": 40, "relevance": 50}
    )
    assert imp.newsworthiness(hot, idx, conf) > imp.newsworthiness(cold, {}, conf)


# --- eligibility (the integrity floor) --------------------------------------


def test_eligibility_blocks_ungrounded_and_refuted(sandbox):
    conf = c.load_config()
    ok = _held(source_url="https://x/ok")
    ungrounded = _held(source_url="https://x/u", grounding_score=0.5)
    refuted = _held(source_url="https://x/r", verified=False)
    curated = make_entry(source_url="https://x/c")  # not held → not eligible
    assert c.editorial_eligible(ok, conf) is True
    assert c.editorial_eligible(ungrounded, conf) is False
    assert c.editorial_eligible(refuted, conf) is False
    assert c.editorial_eligible(curated, conf) is False


# --- promotion consumer -----------------------------------------------------


def test_apply_promotions_stamps_eligible_and_skips_ineligible(sandbox):
    conf = c.load_config()
    pool = c.load_pool("ai-security")
    good = _held(topic="ai-security", source_url="https://x/good", id="good-1")
    bad = _held(topic="ai-security", source_url="https://x/bad", id="bad-1", grounding_score=0.0)
    pool["entries"] = [good, bad]
    c.save_pool("ai-security", pool)

    promoted, skipped, cleared = pe.apply_promotions(
        [
            {"id": "good-1", "reason": "trending", "signals": ["trending"]},
            {"id": "bad-1", "reason": "trending", "signals": ["trending"]},
        ],
        conf,
    )
    assert len(promoted) == 1 and len(skipped) == 1
    entries = {e["id"]: e for e in c.load_pool("ai-security")["entries"]}
    assert c.is_editorial(entries["good-1"]) is True
    assert c.is_editorial(entries["bad-1"]) is False  # integrity floor blocked it


def test_apply_promotions_clears_delisted(sandbox):
    conf = c.load_config()
    pool = c.load_pool("ai-security")
    e = _held(topic="ai-security", source_url="https://x/e", id="e-1")
    e["editorial"] = {"promoted": True, "reason": "old", "signals": [], "at": "2026-01-01"}
    pool["entries"] = [e]
    c.save_pool("ai-security", pool)

    _, _, cleared = pe.apply_promotions([], conf)  # nothing listed → de-promote
    assert cleared == [e["title"]]
    assert c.is_editorial(c.load_pool("ai-security")["entries"][0]) is False
