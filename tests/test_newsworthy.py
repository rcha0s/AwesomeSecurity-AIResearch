"""Tests for scripts/newsworthy.py: severity / AI-incident markers, the name
model, the pairwise same-story rule, and the lane thresholds. Pure, no I/O.

The fixtures are shaped on the 2026-10-23 staged set: PHP2Shell from six
feeds, LiteLLM's compromise next to an older LiteLLM vulnerability write-up,
and the false matches an earlier draft made ("heap", "Hackers", "October")."""

from __future__ import annotations

import newsworthy as nw
import pytest


def cand(title: str, excerpt: str = "", published: str = "2026-07-14", src: str = "a") -> dict:
    return {"title": title, "excerpt": excerpt, "published": published, "source_id": src}


# Prose the reference corpus is built from: "heap" and "accounts" written
# lowercase mid-sentence, PHP and LiteLLM capitalized, "Hackers" only ever
# opening a sentence, and one word ("openai") that is everywhere.
REFERENCE = [
    {"title": "Old post", "summary": "A heap overflow in the parser. Hackers love it."},
    {"title": "Old post 2", "summary": "Stolen accounts and a heap spray. Hackers again."},
    {"title": "Old post 3", "summary": "The PHP runtime and LiteLLM gateway were audited."},
    {"title": "Old post 4", "summary": "It was patched in October by the vendor."},
] + [{"title": f"OpenAI note {i}", "summary": f"OpenAI shipped thing {i}."} for i in range(30)]


def model(*staged: dict) -> nw.NameModel:
    return nw.name_model(REFERENCE, list(staged))


def profile(c: dict, *others: dict) -> nw.Profile:
    return nw.profile(c, model(c, *others))


# --- markers -------------------------------------------------------------------
@pytest.mark.parametrize(
    "text,expected",
    [
        ("Two critical RCEs in PHP core", {"critical", "rce"}),
        ("Unauthenticated remote code execution in GitLab", {"unauthenticated", "rce"}),
        ("Arista patches zero-day exploited in attacks", {"exploited"}),
        ("The flaw is actively exploited, CISA says", {"exploited"}),
        ("Bug exploited in the wild for months", {"exploited"}),
        ("A supply-chain attack on the npm registry", {"compromise"}),
        ("Backdoored wheels on PyPI", {"compromise"}),
        ("CVSS 10.0 flaw in the importer", {"critical"}),
        ("LiteLLM 1.107.0 compromised: wheels carry a credential stealer", {"compromise"}),
        ("Max-severity bug in the router", {"critical"}),
        ("Open-source release notes for the source forcer", set()),  # "rce" inside words
        ("A new benchmark for summarization", set()),
    ],
)
def test_severity_markers(text, expected):
    assert nw.markers(cand(text)) - {"ai-incident"} == expected


def test_ai_incident_needs_an_ai_subject_and_an_incident():
    assert "ai-incident" in nw.markers(
        cand("Attackers hijack AI agents via a malicious MCP server")
    )
    assert "ai-incident" in nw.markers(cand("OpenAI agent removed its safety monitoring"))
    assert "ai-incident" not in nw.markers(cand("Our new AI agents ship in the console"))
    assert "ai-incident" not in nw.markers(cand("Attackers hijack routers in a botnet"))


def test_markers_read_the_excerpt_too():
    assert "exploited" in nw.markers(cand("PHP bugs", "now being broadly exploited across the web"))


# --- names ---------------------------------------------------------------------
def test_capitalized_rare_words_are_names_and_prose_words_are_not():
    m = model()
    assert m.is_name("php") and m.is_name("litellm")
    assert not m.is_name("heap")  # written lowercase in prose
    assert not m.is_name("hackers")  # capitalized only when it opens a sentence
    assert not m.is_name("openai")  # in too many reference documents
    assert not m.is_name("october")  # capitalized by convention


def test_an_unseen_word_is_a_name_only_by_its_shape():
    m = model(cand("ARTEX and Storm-0940 and eMudhra and Node2Shell hit vendors"))
    assert m.is_name("artex") and m.is_name("emudhra") and m.is_name("node2shell")
    assert not m.is_name("vendors")


# --- same story ----------------------------------------------------------------
PHP_SNYK = cand("PHP patches two critical unauthenticated RCEs (CVE-2026-109618)", src="snyk")
PHP_TALOS = cand("Two critical RCEs in PHP core", src="talos")
PHP_WIRED = cand("Hackers exploited the PHP vulnerabilities days before the patch", src="wired")


def same(a: dict, b: dict) -> bool:
    m = model(a, b)
    return nw.same_story(nw.profile(a, m), nw.profile(b, m))


def test_a_shared_name_in_both_titles_matches_within_two_days():
    assert same(PHP_SNYK, PHP_TALOS) and same(PHP_TALOS, PHP_WIRED)
    late = {**PHP_WIRED, "published": "2026-07-19"}
    assert not same(PHP_TALOS, late)  # five days apart: one shared name is not enough
    assert same(PHP_TALOS, {**late, "published": "2026-07-16"})


def test_two_shared_names_match_within_a_week_when_one_is_in_a_title():
    a = cand("ARTEX in the wild: Storm-0940 expands targeting", src="wiz")
    b = cand("AI-driven nation-state campaign", "Storm-0940 used ARTEX agents.", "2026-07-09", "ms")
    assert same(a, b)
    assert not same(a, {**b, "published": "2026-07-01"})  # 13 days apart


def test_one_name_only_in_an_excerpt_is_not_a_match():
    a = cand("The fastify header bypass", src="ghsa")
    b = cand("Patch your Node runtime", "Express, Koa and Fastify setups reach it.", src="semgrep")
    assert not same(a, b)


def test_a_shared_cve_matches_and_disjoint_cves_never_do():
    a = cand("Citrix NetScaler pre-auth bug (CVE-2026-1111)", src="watchtowr")
    b = cand("CISA KEV: Citrix NetScaler flaw CVE-2026-1111 exploited", "2026-07-01", src="kev")
    c = cand("Citrix NetScaler memory overflow (CVE-2026-2222)", src="watchtowr2")
    assert same(a, {**b, "published": "2026-06-01"})  # an id outranks the date window
    assert not same(a, c)  # same product, different bugs


def test_an_id_on_one_side_only_needs_same_days_coverage():
    kev = cand("CISA KEV: PAN-OS GlobalProtect flaw (CVE-2026-0322)", published="2026-07-08")
    news = cand("PAN-OS GlobalProtect under attack from ransomware groups", src="register")
    assert not same(kev, news)  # six days apart, and only one names its CVE
    assert same({**kev, "published": "2026-07-13"}, news)


def test_a_common_word_in_both_titles_is_not_a_story():
    a = cand("Heap overflow in Pillow's TIFF writer", src="ghsa")
    b = cand("F5 BIG-IP heap overflow to RCE", src="watchtowr")
    assert not same(a, b)


def test_an_old_litellm_bug_is_not_this_weeks_compromise():
    compromise = cand("LiteLLM compromised, steals credentials", src="wiz")
    old_bug = cand(
        "When LLM gateways go wrong: findings from LiteLLM", published="2026-07-06", src="cp"
    )
    assert not same(compromise, old_bug)


# --- analyze / is_big / bonus --------------------------------------------------
def source_of(c: dict) -> str:
    return c["source_id"]


def test_sources_count_distinct_sources_and_one_source_corroborates_nothing():
    twin = {**PHP_SNYK, "title": "PHP patch notes for the two critical RCEs"}
    sigs = nw.analyze([PHP_SNYK, PHP_TALOS, twin], REFERENCE, source_of)
    assert sigs[1].sources == 2  # snyk's two posts count once
    assert sigs[0].matches == (1,)  # never its own source's other post
    assert not sigs[0].known


def test_a_story_the_ledger_holds_is_known():
    known = [{"title": "Two critical RCEs in PHP core", "published": "2026-07-13"}]
    sigs = nw.analyze([PHP_SNYK, PHP_TALOS], REFERENCE, source_of, known)
    assert all(s.known for s in sigs)


@pytest.mark.parametrize(
    "sources,markers,known,big",
    [
        (2, {"rce"}, False, True),
        (2, set(), False, False),  # two sources, no marker
        (4, set(), False, True),  # widely covered without a marker
        (3, set(), False, False),
        (1, {"rce", "ai-incident", "critical"}, False, False),  # one source never
        (6, {"rce"}, True, False),  # already held
    ],
)
def test_is_big(sources, markers, known, big):
    sig = nw.Signal(frozenset(markers), (), sources, known)
    assert nw.is_big(sig, min_sources=2, any_sources=4) is big


def test_one_source_is_never_big_even_with_a_threshold_of_one():
    sig = nw.Signal(frozenset({"rce", "critical"}), (), 1)
    assert not nw.is_big(sig, min_sources=1, any_sources=1)


def test_bonus_counts_markers_and_extra_sources_up_to_a_cap():
    assert nw.bonus(nw.Signal(frozenset(), (), 1), 4, 3, 3) == 0
    assert nw.bonus(nw.Signal(frozenset({"rce"}), (), 1), 4, 3, 3) == 4
    assert nw.bonus(nw.Signal(frozenset({"rce"}), (), 3), 4, 3, 3) == 10
    assert nw.bonus(nw.Signal(frozenset({"rce"}), (), 9), 4, 3, 3) == 13
    assert nw.bonus(nw.Signal(frozenset({"rce"}), (), 9, True), 4, 3, 3) == 0
