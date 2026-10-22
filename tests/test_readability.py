"""Tests for scripts/readability.py, its merge recording and hold, and eval_readability.py."""

from __future__ import annotations

import copy

import common as c
import eval_golden as eg
import eval_readability as er
import merge_analysis as m
import pytest
import readability as rd
import taxonomy as tx
from conftest import make_entry
from test_eval_integrity import good_entry, publish

GOOD = {
    "title": "Agent frameworks, not models, hold the exploitable bugs",
    "takeaway": "Treat every agent framework's state store as untrusted input.",
    "summary": (
        "Check Point audited six agent frameworks and found 11 bugs. Most were old bug "
        "classes such as path traversal and SSRF. One let a payload planted in one session "
        "run code in another."
    ),
    "lessons": [
        {"point": "Assume prompt injection will happen; guard what the framework does next.",
         "excerpt": "notwithstanding the aforementioned considerations, heretofore " * 9,
         "confidence": 0.9},  # fmt: skip
        {"point": "Saved checkpoints can carry a payload from one user to another.",
         "excerpt": "x", "confidence": 0.9},  # fmt: skip
    ],
    "actionable": {
        "type": "harness",
        "title": "Turn off pickle-style state loading",
        "detail": "Load saved agent state only from signed data. Require login on dev endpoints.",
    },
}
LONG = (
    "Furthermore the comprehensive organizational infrastructure methodology fundamentally "
    "necessitates continuous multidimensional interoperability verification across "
    "heterogeneous distributed authentication authorization virtualization environments "
    "whenever administrators deliberately reconfigure exceptionally complicated "
    "enterprise-grade orchestration capabilities simultaneously everywhere."
)


def brief(**over) -> dict:
    entry = make_entry(**copy.deepcopy(GOOD))
    entry.update(over)
    return entry


def cfg(**thresholds) -> dict:
    """The real config with some thresholds replaced."""
    out = rd.settings()
    return {**out, "thresholds": {**out["thresholds"], **thresholds}}


def levels(result: dict) -> dict:
    return {i["check"]: i["level"] for i in result["issues"]}


# --- The scorer ---------------------------------------------------------------
def test_a_clear_brief_passes_and_its_excerpts_are_never_scored():
    r = rd.check(brief())
    assert r == {**r, "passed": True, "hold": False, "issues": [], "score": 100}
    assert rd.check(make_entry())["passed"]  # the shared fixture is a clean brief


def test_a_hard_brief_is_flagged_on_each_check():
    bad = brief(
        title=" ".join(["word"] * 30),
        takeaway="This is a game-changer. It may possibly unlock seamless value. Act now.",
        summary=LONG + " The QZX and the WVB and PLM and RTY could perhaps likely matter.",
    )
    r = rd.check(bad)
    found = levels(r)
    assert found["title_words"] == "severe"
    assert found["banned"] == "severe"  # game-changer, unlock, seamless = 3 > hold 2
    assert found["hedges"] == "mild" and found["acronyms"] == "mild"
    assert found["takeaway_sentences"] == "mild" and found["jargon_chain"] == "severe"
    assert found["long_word_ratio"] == "mild"
    assert r["hold"] and not r["passed"] and r["score"] < 50
    reason = rd.hold_reason(r)
    assert reason.startswith("readability: ") and "; title_words 30 > 24" in reason


@pytest.mark.parametrize(
    ("name", "entry", "value"),
    [
        ("title_words", brief(title="one two three four five"), 5),
        ("takeaway_words", brief(takeaway="Patch the five exposed hosts today."), 6),
        ("takeaway_sentences", brief(takeaway="Patch it. Then rotate keys. Then log."), 3),
        ("summary_sentences", brief(summary="One. Two here. Three now. Four too. Five."), 5),
        (
            "sentence_words",
            brief(
                summary="Patch the five exposed hosts in the lab today "
                "and rotate every key you hold."
            ),
            15,
        ),
        ("hedges", brief(summary="It may possibly fail."), 2),
        ("banned", brief(summary="A groundbreaking, seamless fix."), 2),
        ("acronyms", brief(summary="The QZX, WVB and PLM bugs."), 3),
        ("jargon_chain", brief(summary="It found heap buffer overflow bugs."), 5),
    ],
)
def test_each_check_flags_exactly_above_its_limits(name, entry, value):
    """At warn: clean. One above warn: mild. One above hold: severe."""
    assert rd.check(entry)["metrics"][name] == value
    assert name not in levels(rd.check(entry, cfg(**{name: {"warn": value, "hold": value + 5}})))
    mild = rd.check(entry, cfg(**{name: {"warn": value - 1, "hold": value}}))
    assert levels(mild)[name] == "mild" and not mild["hold"]
    severe = rd.check(entry, cfg(**{name: {"warn": value - 2, "hold": value - 1}}))
    assert levels(severe)[name] == "severe" and severe["hold"]


def test_grade_and_long_words_rise_with_hard_prose():
    easy, hard = "We fix the bug. It was in the code.", LONG
    assert rd.grade(easy) < 5 < 20 < rd.grade(hard)
    assert rd.long_word_ratio(easy) == 0 and rd.long_word_ratio(hard) > 0.5
    assert rd.grade("") == 0.0 and rd.long_word_ratio("") == 0.0


@pytest.mark.parametrize(
    ("word", "n"),
    [("the", 1), ("make", 1), ("attack", 2), ("security", 4), ("table", 2),
     ("used", 1), ("side-channel", 3), ("injected", 3), ("v2.1", 1), ("deserialization", 6)],
)  # fmt: skip
def test_syllables(word, n):
    assert rd.syllables(word) == n


def test_is_long_judges_each_hyphen_part():
    assert not rd.is_long("side-channel") and rd.is_long("authentication")


def test_sentences_survive_abbreviations_code_and_urls():
    text = "Use tools, e.g. `x.y()` here. See https://a.b/c.d now! Done."
    assert rd.sentences(text) == ["Use tools, eg  x  here.", "See  x  now!", "Done."]
    assert len(rd.clauses("First part; second part (1) third")) == 3


def test_acronyms_count_only_when_unexplained_and_not_allowed():
    allow = {"CVE"}
    text = "SSRF (server-side request forgery) and CVE-1. Then QZX, and NEVER do it."
    assert rd.unexplained_acronyms(text, allow) == ["QZX"]
    assert rd.unexplained_acronyms("Use a TEE. A trusted execution environment (TEE)", allow) == []
    assert rd.unexplained_acronyms("PoC and `ABC` code and IDs", allow) == ["ID"]


def test_jargon_chain_skips_names_and_function_words():
    assert rd.jargon_chain("Microsoft Agent Framework Checkpoint Store") == []
    assert rd.jargon_chain("the agent state store path, then a fix") == [
        "agent",
        "state",
        "store",
        "path",
    ]


def test_banned_phrases_match_whole_words_only():
    assert rd.banned_hits(
        "We unlocked it and it's worth noting", ["unlock", "it's worth noting"]
    ) == ["it's worth noting"]


# --- The skill's rewrite check -------------------------------------------------
def test_rewrite_problems_catch_dropped_facts_and_changed_excerpts():
    draft = brief(summary="Six frameworks, 11 bugs, CVE-2026-1234 and `pickle` (1) first.")
    ok = brief(summary="It found 11 bugs in six frameworks: CVE-2026-1234 and `pickle`.")
    assert rd.rewrite_problems(draft, ok) == []  # the "(1)" list marker is not a fact
    lost = brief(summary="It found bugs in six frameworks.")
    assert rd.rewrite_problems(draft, lost) == [
        "dropped fact '11'", "dropped fact 'CVE-2026-1234'", "dropped fact '`pickle`'"
    ]  # fmt: skip
    quoted = copy.deepcopy(ok)
    quoted["lessons"][1]["excerpt"] = "reworded"
    assert rd.rewrite_problems(draft, quoted) == ["lesson excerpts changed"]


def test_check_analysis_reports_each_entry_and_rewrite_problems(sandbox, capsys):
    draft = brief(summary="It found 11 bugs.")
    final = brief(summary="It found bugs.", title=" ".join(["word"] * 30))
    c.save_json(c.ANALYSIS_OUT, [final, brief(source_url="https://example.com/b")])
    c.save_json(c.DATA_DIR / rd.DRAFT, [draft])
    assert rd.main(["--analysis"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0].startswith("HOLD [") and "    REWRITE: dropped fact '11'" in out
    assert out[-1].startswith("OK [100]")


def test_report_summarizes_the_corpus():
    lines = rd.report([brief(), brief(title=" ".join(["w"] * 30))], rd.settings(), worst=1)
    assert lines[0] == "2 briefs" and "passed 1, mild only 0, would hold 1" in lines
    assert any(line.startswith("- [") for line in lines)


# --- Merge recording and the hold ---------------------------------------------
def at(url: str, **over) -> dict:
    return brief(source_url=url, article_url=url, **over)


def _pool_entry(url: str) -> dict:
    return next(e for e in c.load_pool("ai-research")["entries"] if e["source_url"] == url)


def test_merge_records_readability_and_holds_only_a_severe_failure(sandbox):
    conf = c.load_config()
    mild = at(
        "https://example.com/mild",
        title="Rotate keys after a leak",
        takeaway="Patch it. Then rotate keys.",
    )
    bad = at("https://example.com/bad", title=" ".join(["word"] * 30))
    m.merge([brief(), mild, bad], conf)
    clean, mild_e, bad_e = (_pool_entry(u) for u in (
        "https://example.com/compact", "https://example.com/mild", "https://example.com/bad"))  # fmt: skip
    assert clean["readability"] == {"score": 100, "passed": True, "issues": []}
    assert "readability_hold" not in clean and not clean["needs_review"]
    assert mild_e["readability"]["issues"] == ["mild: takeaway_sentences 2 > 1"]
    assert "readability_hold" not in mild_e and not mild_e["needs_review"]
    assert bad_e["needs_review"] and bad_e["readability_hold"].startswith("readability: ")
    assert c.review_reason(bad_e, conf, {}) == bad_e["readability_hold"]
    assert not c.is_curated(bad_e, conf) and c.is_curated(clean, conf)


def test_a_rewritten_brief_clears_its_hold_on_re_merge(sandbox):
    conf = c.load_config()
    m.merge([brief(title=" ".join(["word"] * 30))], conf)
    assert _pool_entry("https://example.com/compact")["readability_hold"]
    m.merge([brief()], conf)
    fixed = _pool_entry("https://example.com/compact")
    assert "readability_hold" not in fixed and fixed["readability"]["passed"]


def test_a_held_brief_is_shown_in_no_lane():
    conf = c.load_config()
    held = brief(readability_hold="readability: x", source_id="news", published="2026-07-14")
    sources = {"news": {"track": "news", "tier": "high"}}
    assert c.is_news_curated({**held, "readability_hold": None}, conf, sources)
    assert not c.is_news_curated(held, conf, sources)
    assert not c.editorial_eligible(held, conf) and not c.is_curated(held, conf)
    assert c.is_held(held, conf, sources)


# --- The eval ----------------------------------------------------------------
def test_eval_reports_the_share_of_published_briefs_passing(sandbox, capsys):
    bad = good_entry(id="bad", source_url="https://example.com/posts/b",
                     article_url="https://example.com/posts/b", title=" ".join(["w"] * 30))  # fmt: skip
    mild = good_entry(id="mild", source_url="https://example.com/posts/m",
                      article_url="https://example.com/posts/m", takeaway="One. Two.")  # fmt: skip
    publish(sandbox, [good_entry(), bad, mild])
    report = er.run()
    assert report["published"] == 3 and report["pass_share"] == 0.333
    assert (report["mild"], report["would_hold"], report["passed"]) == (1, 1, True)
    assert er.main([]) == 0
    assert capsys.readouterr().out.strip().startswith("EVAL readability PASS published=3")
    assert er.run(cfg={**rd.settings(), "eval_min_pass": 0.333})["passed"]  # at the floor
    assert not er.run(cfg={**rd.settings(), "eval_min_pass": 0.5})["passed"]


def test_eval_fails_closed_when_the_site_is_missing(sandbox, capsys):
    assert er.main([]) == 1
    assert "EVAL readability FAIL" in capsys.readouterr().out


def test_the_real_site_runs():
    report = er.run()
    assert report["published"] > 0 and 0 <= report["pass_share"] <= 1


# --- Golden -------------------------------------------------------------------
def test_golden_counts_a_readability_hold_as_a_drop():
    conf, tax = c.load_config(), tx.get()
    case = {"id": "k", "title": "Agent frameworks", "url": "https://example.com/compact",
            "keep": True, "domain": "air.agents", "facts": []}  # fmt: skip
    ok = eg.score_case(case, brief(), conf, tax, 0.5)
    assert ok["passed"] and ok["readable"]
    held = eg.score_case(case, brief(title=" ".join(["w"] * 30)), conf, tax, 0.5)
    assert not held["passed"] and not held["readable"] and "readability:" in held["why"]
    assert eg.score([case], [brief()])["readability_pass"] == 1.0
