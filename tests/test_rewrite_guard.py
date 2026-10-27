"""Tests for scripts/rewrite_guard.py and its enforcement in merge_analysis.py."""

from __future__ import annotations

import copy

import common as c
import merge_analysis as m
import pytest
import rewrite_guard as rg
from test_readability import _pool_entry, at, brief

# The reviewer's table: a readability rewrite that flips meaning.
FLIPS = [
    ("negation", "Versions 2.x are not affected.", "Versions 2.x are affected."),
    ("n't", "The fix doesn't cover SMB.", "The fix covers SMB."),
    ("version range", "It affects releases before 2.4.1.", "It affects releases after 2.4.1."),
    ("vendor swap", "The bug ships in Microsoft Teams.", "The bug ships in Google Meet."),
    ("severity", "Treat it as a critical bug.", "Treat it as a medium bug."),
    ("number swap", "It found 11 bugs in 6 frameworks.", "It found 6 bugs in 11 frameworks."),
    ("unit", "The payload is 5 MB.", "The payload is 5 GB."),
    ("percent swap", "92% of runs failed and 3% passed.", "3% of runs failed and 92% passed."),
    ("CVE swap", "Patch CVE-2026-1111 first.", "Patch CVE-2026-2222 first."),
    ("number word", "Six frameworks were audited.", "Seven frameworks were audited."),
    ("invented facts", "Patch the parser now.", "Patch the parser now (CVSS 9.8, CVE-2026-9999)."),
    ("dropped fact", "It found 11 bugs.", "It found bugs."),
    ("code span", "Disable `pickle` loading.", "Disable `yaml` loading."),
]  # fmt: skip
SAME = [
    (
        "Check Point researchers spent a year auditing six agent frameworks and disclosed "
        "11 vulnerabilities, mostly classic bug classes.",
        "Check Point audited six agent frameworks for a year. It found 11 vulnerabilities, "
        "mostly classic bug classes.",
    ),
    ("Researchers at Google found the flaw.", "Google researchers found the flaw."),
    ("The flaw is in Google's parser.", "The flaw is in the Google parser."),
    ("Steps: (1) patch, (2) rotate keys.", "Patch, then rotate keys."),
    ("Attackers can't read the token without access.", "Without access, attackers can't read the token."),
]  # fmt: skip


@pytest.mark.parametrize(("kind", "draft", "final"), FLIPS, ids=[f[0] for f in FLIPS])
def test_every_meaning_flip_is_caught(kind, draft, final):
    assert rg.changes(draft, final)
    assert rg.changes(final, draft)  # both directions


@pytest.mark.parametrize(("draft", "final"), SAME)
def test_a_plain_rewrite_keeps_its_facts(draft, final):
    assert rg.changes(draft, final) == []


def test_a_sentence_initial_vendor_swap_is_caught_when_the_entry_names_it():
    draft = brief(summary="Microsoft patched it. The flaw was in Microsoft Teams.")
    final = brief(summary="Google patched it. The flaw was in Microsoft Teams.")
    assert "summary" in rg.problems(draft, final)
    title_draft = brief(title="OpenAI agents found a CGI bug")
    assert "title" in rg.problems(title_draft, brief(title="Anthropic agents found a CGI bug"))
    assert rg.problems(title_draft, brief(title="A CGI bug found by OpenAI agents")) == {}


@pytest.mark.parametrize(("kind", "draft", "final"), FLIPS, ids=[f[0] for f in FLIPS])
def test_restore_gives_back_each_flipped_field(kind, draft, final):
    entry = brief(summary=final, takeaway="Patch it now.")
    reverted = rg.restore(entry, brief(summary=draft, takeaway="Patch the parser now, today."))
    assert list(reverted) == ["summary"] and entry["summary"] == draft
    assert entry["takeaway"] == "Patch it now."  # a fact-safe rewrite is kept
    assert entry["readability_rewrite"] == "reverted summary"


def test_restore_covers_lessons_actions_excerpts_and_lesson_count():
    draft = brief()
    final = copy.deepcopy(draft)
    final["lessons"][0]["point"] = "Assume prompt injection will never happen."
    final["lessons"][1]["excerpt"] = "a reworded quote"
    final["actionable"]["detail"] = "Never require login on dev endpoints. Load signed state."
    found = rg.restore(final, draft)
    assert set(found) == {"lessons[0].point", "lessons[1].excerpt", "actionable.detail"}
    assert rg.fields(final) == rg.fields(draft)
    short = copy.deepcopy(draft)
    short["lessons"] = short["lessons"][:1]
    assert rg.restore(short, draft) == {"lessons": ["lesson count changed"]}
    assert short["lessons"] == draft["lessons"]
    assert rg.restore(copy.deepcopy(draft), None) == {}
    gone = copy.deepcopy(draft)
    del gone["takeaway"]
    assert rg.restore(gone, draft) == {"takeaway": ["field removed"]}
    assert gone["takeaway"] == draft["takeaway"]


def test_drafts_unwrap_and_match_by_source_url(sandbox):
    c.save_json(c.DATA_DIR / rg.DRAFT, {"entries": [brief(source_url="https://example.com/a/")]})
    drafts = rg.load_drafts()
    assert rg.draft_for(drafts, brief(source_url="https://example.com/a?utm_source=x"))
    assert rg.draft_for(drafts, brief(source_url="https://example.com/b")) is None
    (c.DATA_DIR / rg.DRAFT).unlink()
    assert rg.load_drafts() is None


def test_check_draft_warns_only_when_an_analysis_has_no_draft(sandbox, capsys):
    assert rg.main(["--check-draft"]) == 0  # no analysis
    c.save_json(c.ANALYSIS_OUT, [brief()])
    assert rg.main(["--check-draft"]) == 1 and rg.NOTE in capsys.readouterr().out
    c.save_json(c.DATA_DIR / rg.DRAFT, [brief()])
    assert rg.main(["--check-draft"]) == 0


# --- Enforcement in merge ----------------------------------------------------
def notes() -> str:
    path = c.DATA_DIR / m.READABILITY_RECORD
    return path.read_text() if path.exists() else ""


def test_merge_restores_a_flipped_field_and_never_holds_for_it(sandbox):
    draft = at("https://example.com/x", summary="It found 11 bugs in 6 frameworks.")
    final = at("https://example.com/x", summary="It found 6 bugs in 11 frameworks.")
    c.save_json(c.DATA_DIR / rg.DRAFT, [draft])
    m.merge([final], c.load_config())
    e = _pool_entry("https://example.com/x")
    assert e["summary"] == "It found 11 bugs in 6 frameworks."
    assert e["readability_rewrite"] == "reverted summary" and "readability_hold" not in e
    assert "- reverted summary of" in notes()


def test_merge_keeps_a_fact_safe_rewrite_and_clears_a_stale_revert(sandbox):
    c.save_json(c.DATA_DIR / rg.DRAFT, [at("https://example.com/x", summary="It found 11 bugs.")])
    m.merge([at("https://example.com/x", summary="It found 6 bugs.")], c.load_config())
    assert _pool_entry("https://example.com/x")["readability_rewrite"]
    c.save_json(c.DATA_DIR / rg.DRAFT, [at("https://example.com/x", summary="It found 11 bugs.")])
    m.merge([at("https://example.com/x", summary="There were 11 bugs.")], c.load_config())
    e = _pool_entry("https://example.com/x")
    assert e["summary"] == "There were 11 bugs." and "readability_rewrite" not in e


def test_merge_ignores_a_session_written_revert_record(sandbox):
    c.save_json(c.DATA_DIR / rg.DRAFT, [brief()])
    m.merge([brief(readability_rewrite="reverted nothing")], c.load_config())
    assert "readability_rewrite" not in _pool_entry("https://example.com/compact")


def test_merge_warns_when_an_analysis_has_no_draft(sandbox, capsys):
    m.merge([brief(readability_rewrite="reverted nothing")], c.load_config())
    assert rg.NOTE in capsys.readouterr().err and rg.NOTE in notes()
    assert "readability_rewrite" not in _pool_entry("https://example.com/compact")


def test_facts_are_checked_in_both_directions():
    plain, coded = "Disable pickle loading.", "Disable `pickle` loading."
    assert rg.changes(plain, coded) == ["added '`pickle`'"]
    assert rg.changes(coded, plain) == ["dropped '`pickle`'"]


# --- Re-review probes ---------------------------------------------------------
PROBES = [
    ("polarity", "Load state only from signed data.", "Load state from any data."),
    ("default", "It is disabled by default.", "It is enabled by default."),
    ("auth", "The endpoint requires authentication.", "The endpoint requires no authentication."),
    ("reach", "It is exploitable remotely.", "It is exploitable locally."),
    ("un- stem", "Upgrade the unfixed build.", "Upgrade the build."),
    ("non- stem", "Ship a non-default config.", "Ship a config."),
    ("guard target", "It hits Linux but not Windows.", "It hits Windows but not Linux."),
    ("severity target", "Critical in OpenSSL, low in LibreSSL.",
     "Low in OpenSSL, critical in LibreSSL."),
    ("score target", "Rated 9.8 for CVE-2026-1 and 5.3 for CVE-2026-2.",
     "Rated 5.3 for CVE-2026-1 and 9.8 for CVE-2026-2."),
]  # fmt: skip


@pytest.mark.parametrize(("kind", "draft", "final"), PROBES, ids=[p[0] for p in PROBES])
def test_the_re_review_probes_are_caught(kind, draft, final):
    assert rg.changes(draft, final) and rg.changes(final, draft)


def test_changes_name_what_moved():
    assert rg.changes("It is not affected.", "It is affected.") == [
        "negation, range, severity or polarity words changed"
    ]
    assert rg.changes("Linux but not Windows.", "Windows but not Linux.") == [
        "what a guard word or number applies to changed"
    ]


def test_anchor_pairs_look_a_few_tokens_ahead_in_the_sentence():
    assert rg.anchor_pairs("Rate 9 of the old core modules in Apache.") == {("9", ""): 1}
    assert rg.anchor_pairs("Fixed in 3.1 for Nginx.") == {("fixed", "3.1"): 1, ("3.1", "nginx"): 1}
    assert rg.anchor_pairs("Not here. Windows is.") == {("not", ""): 1}


def test_guard_maps_contractions_and_un_non_stems():
    assert [rg.guard(t) for t in ("doesn't", "unfixed", "non-default", "nondefault")] == [
        "n't", "unfixed", "non-default", "nondefault"
    ]  # fmt: skip
    assert rg.guard("under") is None and rg.guard("nonce") is None


def test_a_dropped_lesson_still_checks_every_other_field():
    """The reviewer's repro: drop a lesson AND flip two other fields."""
    draft = brief(
        summary="The admin API requires authentication.",
        takeaway="Rotate the signing keys every 30 days.",
    )
    final = brief(
        summary="The admin API requires no authentication.",
        takeaway="Rotate the signing keys every 90 days.",
    )
    final["lessons"] = final["lessons"][:1]
    found = rg.restore(final, draft)
    assert set(found) == {"lessons", "summary", "takeaway"}
    assert rg.fields(final) == rg.fields(draft)


def test_merge_notes_an_entry_with_no_matching_draft(sandbox):
    c.save_json(c.DATA_DIR / rg.DRAFT, [at("https://example.com/other")])
    m.merge([brief()], c.load_config())
    assert "- no draft for 'Agent frameworks, not models" in notes()
    assert "rewrite not fact-checked" in notes()


# A shorter title may drop what the takeaway or summary still says (Rohan,
# 2026-10-26: titles of 12 words or fewer), never add, swap or un-negate.
LONG_TITLE = (
    "OpenAI frontier-agent red team of its own training containment: microVM escapes, "
    "egress via metrics service, cache-timing channels"
)
PROSE = "OpenAI had its frontier agents attack the training sandbox; they escaped 2 microVMs."


@pytest.mark.parametrize(
    "final",
    [
        "OpenAI set its own agents loose in its training sandbox, and they broke out",
        "OpenAI's frontier agents escaped 2 microVMs in its training sandbox",
    ],
)
def test_a_title_may_drop_details_the_prose_keeps(final):
    assert rg.title_changes(LONG_TITLE, final, PROSE) == []


@pytest.mark.parametrize(
    "final, why",
    [
        ("Anthropic set its own agents on its training sandbox", "names changed"),
        ("OpenAI agents escaped 5 microVMs in its training sandbox", "numbers"),
        ("OpenAI agents escaped CVE-2026-1 in its sandbox", "added 'CVE-2026-1'"),
        ("OpenAI agents found a critical sandbox escape", "severity"),
    ],
)
def test_a_title_may_not_add_or_swap_a_fact(final, why):
    assert any(why in p for p in rg.title_changes(LONG_TITLE, final, PROSE))


def test_a_title_keeps_its_negations():
    draft = "Versions 2.x are not affected by the parser bug in libfoo"
    assert rg.title_changes(draft, "Versions 2.x are affected by a libfoo bug") == [
        "dropped a negation"
    ]


def test_merge_keeps_a_shortened_title_and_restores_an_invented_one():
    draft = brief(title=LONG_TITLE, summary=PROSE)
    short = brief(title="OpenAI set its own agents loose in its training sandbox", summary=PROSE)
    assert "title" not in rg.problems(draft, short)
    bad = brief(title="OpenAI agents escaped 9 microVMs", summary=PROSE)
    assert "title" in rg.problems(draft, bad)


# Review of #124 (Sonnet + Gemini): a guard word borrowed from the prose, a
# moved negation, a dropped un-/non- word and a flipped default all fail.
@pytest.mark.parametrize(
    "draft, final, prose",
    [
        ("Nginx is vulnerable to remote RCE", "Nginx is not vulnerable to RCE",
         "A patch is not available yet."),
        ("Foo still unpatched after disclosure", "Foo patched after disclosure",
         "Version 2 of Bar is patched."),
        ("RCE for authenticated users in Foo", "RCE for unauthenticated users in Foo",
         "Unauthenticated access is blocked."),
        ("Debug endpoint off by default in Foo", "Debug endpoint on by default in Foo", ""),
        ("Foo unaffected by the Bar flaw", "Foo hit by the Bar flaw", ""),
        ("None of the Linux releases are vulnerable", "Linux releases are vulnerable", ""),
        ("Patch fixes Alpha but not Beta in Foo", "Patch fixes Beta but not Alpha in Foo", ""),
    ],
)  # fmt: skip
def test_a_title_cannot_borrow_move_or_drop_a_guard_word(draft, final, prose):
    assert rg.title_changes(draft, final, prose) != []


def test_what_code_cannot_see_is_left_to_the_meaning_check():
    """A non-negating guard word moved to another name passes the code check
    (anchors only bind negations: shortening moves the rest legitimately).
    The migration's Gemini pass judged meaning for every pair."""
    assert rg.title_changes("Critical flaw in Foo; Bar also affected", "Critical flaw in Bar") == []
