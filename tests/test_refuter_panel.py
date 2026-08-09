"""Unit tests for scripts/refuter_panel.py — perspective-diverse refuter panel.

The panel runs three lenses (correctness, prior-art, scope) against a claim.
`correctness=refute` is a hard veto that flips the claim to `contested`.
`prior-art=refute` and `scope=refute` are advisory caveats — status unchanged.

All LLM work is behind a `verdict_provider` callable; tests stub the provider so
the composition logic is what's under test, not the model.
"""

from __future__ import annotations

import pytest
import refuter_panel as rp
from test_claims import make_claim


def stubbed_provider(mapping):
    """Return a provider that maps lens -> (verdict, note)."""

    def provider(claim, lens, source_text):
        verdict, note = mapping.get(lens, ("abstain", ""))
        return rp.Verdict(lens=lens, verdict=verdict, note=note)

    return provider


# --- Panel composition ------------------------------------------------------
def test_panel_runs_all_three_lenses():
    calls = []

    def provider(claim, lens, source_text):
        calls.append(lens)
        return rp.Verdict(lens=lens, verdict="uphold", note="")

    rp.run_panel(make_claim(), "source", provider)
    assert calls == list(rp.LENSES)  # correctness, prior-art, scope in order
    assert len(calls) == 3


def test_all_uphold_no_status_change_no_caveats():
    provider = stubbed_provider(
        {lens: ("uphold", "") for lens in rp.LENSES}
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change is None
    assert result.caveats == ()
    assert len(result.verdicts) == 3


def test_correctness_refute_is_hard_veto():
    """Correctness lens refuting the claim flips status to contested."""
    provider = stubbed_provider(
        {
            "correctness": ("refute", "source contradicts the statement"),
            "prior-art": ("uphold", ""),
            "scope": ("uphold", ""),
        }
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change == "contested"


def test_prior_art_refute_is_advisory_note_only():
    """Prior-art refuting produces a caveat but does NOT change status."""
    provider = stubbed_provider(
        {
            "correctness": ("uphold", ""),
            "prior-art": ("refute", "similar result in Smith 2024"),
            "scope": ("uphold", ""),
        }
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change is None
    assert len(result.caveats) == 1
    caveat = result.caveats[0]
    assert caveat.lens == "prior-art"
    assert "Smith 2024" in caveat.note


def test_scope_refute_is_advisory_note_only():
    provider = stubbed_provider(
        {
            "correctness": ("uphold", ""),
            "prior-art": ("uphold", ""),
            "scope": ("refute", "applies only to open-weights models"),
        }
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change is None
    assert len(result.caveats) == 1
    assert result.caveats[0].lens == "scope"


def test_correctness_veto_still_records_prior_art_and_scope_caveats():
    """A correctness refute vetoes, but the other advisory notes remain visible."""
    provider = stubbed_provider(
        {
            "correctness": ("refute", "contradicts source"),
            "prior-art": ("refute", "restates known result"),
            "scope": ("refute", "narrow domain"),
        }
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change == "contested"
    lenses = {c.lens for c in result.caveats}
    assert lenses == {"prior-art", "scope"}  # correctness is a veto, not a caveat


def test_abstain_verdict_is_neutral():
    """Abstain neither vetoes nor produces a caveat."""
    provider = stubbed_provider(
        {"correctness": ("abstain", ""), "prior-art": ("abstain", ""), "scope": ("abstain", "")}
    )
    result = rp.run_panel(make_claim(), "source", provider)
    assert result.status_change is None
    assert result.caveats == ()


# --- Verdict shape ----------------------------------------------------------
def test_verdict_rejects_unknown_lens():
    with pytest.raises(ValueError):
        rp.Verdict(lens="bogus", verdict="uphold", note="")


def test_verdict_rejects_unknown_verdict():
    with pytest.raises(ValueError):
        rp.Verdict(lens="correctness", verdict="mostly-uphold", note="")


def test_verdicts_are_immutable():
    v = rp.Verdict(lens="correctness", verdict="uphold", note="")
    with pytest.raises((AttributeError, Exception)):
        v.verdict = "refute"  # frozen dataclass


# --- Provider contract ------------------------------------------------------
def test_provider_receives_claim_lens_and_source_text():
    seen = []

    def provider(claim, lens, source_text):
        seen.append((claim["id"], lens, source_text[:10]))
        return rp.Verdict(lens=lens, verdict="uphold", note="")

    rp.run_panel(make_claim(id="my-claim"), "source-excerpt-goes-here", provider)
    assert all(x[0] == "my-claim" for x in seen)
    assert {x[1] for x in seen} == set(rp.LENSES)
    assert all(x[2] == "source-exc" for x in seen)


def test_panel_result_carries_all_verdicts_for_render():
    """The renderer will need every verdict (including uphold + abstain) so
    users see the whole panel's decision, not just the refutations."""
    provider = stubbed_provider(
        {
            "correctness": ("uphold", ""),
            "prior-art": ("abstain", "insufficient prior art in context"),
            "scope": ("refute", "narrow"),
        }
    )
    result = rp.run_panel(make_claim(), "source", provider)
    lens_to_verdict = {v.lens: v.verdict for v in result.verdicts}
    assert lens_to_verdict == {"correctness": "uphold", "prior-art": "abstain", "scope": "refute"}
