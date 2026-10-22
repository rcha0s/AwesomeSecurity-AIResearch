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


def test_apply_decisions_stamps_eligible_and_skips_ineligible(sandbox):
    conf = c.load_config()
    pool = c.load_pool("ai-security")
    good = _held(topic="ai-security", source_url="https://x/good", id="good-1")
    bad = _held(topic="ai-security", source_url="https://x/bad", id="bad-1", grounding_score=0.0)
    pool["entries"] = [good, bad]
    c.save_pool("ai-security", pool)

    out = pe.apply_decisions(
        [
            {"id": "good-1", "reason": "trending", "signals": ["trending"]},
            {"id": "bad-1", "reason": "trending", "signals": ["trending"]},
        ],
        conf,
    )
    assert len(out.promoted) == 1 and len(out.skipped) == 1
    entries = {e["id"]: e for e in c.load_pool("ai-security")["entries"]}
    assert c.is_editorial(entries["good-1"]) is True
    assert c.is_editorial(entries["bad-1"]) is False  # integrity floor blocked it


def _seed(*entries) -> None:
    pool = c.load_pool("ai-security")
    pool["entries"] = list(entries)
    c.save_pool("ai-security", pool)


def _pool() -> dict[str, dict]:
    return {e["id"]: e for e in c.load_pool("ai-security")["entries"]}


def _promoted(id_: str, **over) -> dict:
    e = _held(topic="ai-security", source_url=f"https://x/{id_}", id=id_, **over)
    e["editorial"] = {"promoted": True, "reason": "old", "signals": [], "at": "2026-01-01"}
    return e


def test_promotions_are_sticky_when_not_listed_again(sandbox):
    """The 2026-10-22 bug: a run that promoted one item de-promoted four earlier ones."""
    conf = c.load_config()
    _seed(*(_promoted(f"e-{i}") for i in range(4)), _held(topic="ai-security", id="new-1"))
    out = pe.apply_decisions([{"id": "new-1", "reason": "fresh", "signals": []}], conf)
    assert out.promoted and out.demoted == [] and out.lost == []
    assert all(c.is_editorial(e) for e in _pool().values())  # four kept + one added
    assert pe.apply_decisions([], conf).demoted == []  # an empty run keeps them too
    assert all(c.is_editorial(e) for e in _pool().values())


def test_relisting_keeps_the_original_stamp(sandbox):
    conf = c.load_config()
    _seed(_promoted("e-1"))
    pe.apply_decisions([{"id": "e-1", "reason": "again", "signals": []}], conf)
    assert _pool()["e-1"]["editorial"]["at"] == "2026-01-01"  # no bump up the lane


def test_an_explicit_reasoned_demotion_removes_and_reports(sandbox):
    conf = c.load_config()
    _seed(_promoted("e-1"), _promoted("e-2"))
    out = pe.apply_decisions([{"id": "e-1", "demote": True, "reason": "story retracted"}], conf)
    assert out.demoted == [f"{_pool()['e-1']['title'][:72]}: story retracted"]
    assert not c.is_editorial(_pool()["e-1"]) and c.is_editorial(_pool()["e-2"])
    record = pe.outcomes_record(out)
    assert "- DEMOTED: " in record and "story retracted" in record


def test_a_demotion_without_a_reason_or_target_is_ignored(sandbox):
    conf = c.load_config()
    _seed(_promoted("e-1"), _held(topic="ai-security", id="plain"))
    out = pe.apply_decisions(
        [
            {"id": "e-1", "demote": True, "reason": "  "},
            {"id": "e-1", "demote": "yes", "reason": "not the literal true"},
            {"id": "plain", "demote": True, "reason": "never promoted"},
            {"id": "ghost", "demote": True, "reason": "no such entry"},
            "not-an-object",
        ],
        conf,
    )
    assert out.demoted == [] and c.is_editorial(_pool()["e-1"])
    assert len(out.skipped) == 5  # "yes" reads as a promotion: already promoted
    assert not c.is_editorial(_pool()["plain"])


def test_integrity_failure_removes_a_promotion_and_reports_it(sandbox):
    conf = c.load_config()
    _seed(_promoted("refuted", verified=False), _promoted("ungrounded", grounding_score=0.5),
          _promoted("fine"))  # fmt: skip
    out = pe.apply_decisions([], conf)
    assert len(out.lost) == 2 and out.demoted == []
    pool = _pool()
    assert not c.is_editorial(pool["refuted"]) and not c.is_editorial(pool["ungrounded"])
    assert c.is_editorial(pool["fine"])
    assert pe.outcomes_record(out).count("- REMOVED (integrity): ") == 2


def test_a_promotion_that_is_merely_ineligible_now_is_kept(sandbox):
    """Ineligible for a NEW promotion (here: unscored) is not an integrity failure."""
    conf = c.load_config()
    e = _promoted("e-1")
    e["scores"] = {}
    _seed(e)
    assert not c.editorial_eligible(e, conf) and not c.integrity_lost(e)
    assert pe.apply_decisions([], conf).lost == []
    assert c.is_editorial(_pool()["e-1"])


def test_the_record_is_appended_for_the_pr_body(sandbox):
    conf = c.load_config()
    _seed(_promoted("e-1"))
    pe.append_record(pe.apply_decisions([{"id": "e-1", "demote": True, "reason": "dup"}], conf))
    pe.append_record(pe.apply_decisions([], conf))
    text = (c.DATA_DIR / pe.OUTCOMES_NAME).read_text()
    assert text.count("### Editorial decisions") == 2 and "- DEMOTED: " in text
