"""Unit tests for scripts/drift_review.py — reads related_claims + ledger, stages
proposed changes (evidence attach, contest, supersede, refute, stale sweep).

The refuter-panel LLM boundary is a `verdict_provider` callable — tests stub it.
Drift review is pure composition on top; we assert the actions it produces,
not the model reasoning.
"""

from __future__ import annotations

from datetime import UTC, datetime

import drift_review as dr
import refuter_panel as rp
from conftest import make_entry
from test_claims import ledger_of
from test_claims import make_claim as _make_claim_base


def make_claim(**over):
    """Fresh claim for drift-review tests — sets last_reviewed=recent by default so
    the stale sweep doesn't fire on every fixture claim. Tests that exercise the
    sweep override last_reviewed explicitly."""
    over.setdefault("last_reviewed", "2026-08-01")
    return _make_claim_base(**over)


def entry(**over):
    """A curated finding that flags one or more related claims."""
    over.setdefault("title", "Compact tool outputs cuts context tokens 40%")
    over.setdefault("source_url", "https://example.com/compact-40")
    over.setdefault("article_url", "https://example.com/compact-40")
    over.setdefault("published", "2026-08-01")
    over.setdefault("related_claims", ["toon-over-json-for-agent-io"])
    over.setdefault("cluster", "B")
    return make_entry(**over)


def always(verdict, note=""):
    """A provider that returns the same verdict for every lens."""

    def provider(claim, lens, source_text):
        return rp.Verdict(lens=lens, verdict=verdict, note=note)

    return provider


def lens_map(mapping):
    """Provider dispatching (lens -> (verdict, note))."""

    def provider(claim, lens, source_text):
        verdict, note = mapping.get(lens, ("abstain", ""))
        return rp.Verdict(lens=lens, verdict=verdict, note=note)

    return provider


TODAY = datetime(2026, 8, 8, tzinfo=UTC)


# --- Evidence attach --------------------------------------------------------
def test_supporting_evidence_auto_attaches():
    """When correctness=uphold and the entry supports the claim, the action is
    to attach the entry's URL as evidence — no retirement, no caveats."""
    ledger = ledger_of(make_claim(id="toon-over-json-for-agent-io"))
    actions = dr.review(
        entries=[entry()],
        ledger=ledger,
        provider=always("uphold"),
        today=TODAY,
    )
    assert len(actions) == 1
    action = actions[0]
    assert action.kind == "evidence_attach"
    assert action.claim_id == "toon-over-json-for-agent-io"
    assert action.source["source_url"] == "https://example.com/compact-40"


def test_multiple_supporting_lessons_produce_one_action_each():
    ledger = ledger_of(
        make_claim(id="toon-over-json-for-agent-io"),
        make_claim(
            id="hybrid-retrieval-beats-lexical",
            topic="ai-security",
            statement="Hybrid retrieval beats lexical at recall@10.",
            evidence=[
                {"stance": "supports", "url": "https://x", "title": "T", "published": "2026-01-01"}
            ],
        ),
    )
    entries = [
        entry(related_claims=["toon-over-json-for-agent-io"]),
        entry(
            source_url="https://y/other",
            article_url="https://y/other",
            related_claims=["hybrid-retrieval-beats-lexical"],
        ),
    ]
    actions = dr.review(entries=entries, ledger=ledger, provider=always("uphold"), today=TODAY)
    assert len(actions) == 2
    ids = {a.claim_id for a in actions}
    assert ids == {"toon-over-json-for-agent-io", "hybrid-retrieval-beats-lexical"}


# --- Contest (correctness veto) ---------------------------------------------
def test_correctness_refute_produces_contest_action():
    ledger = ledger_of(make_claim(id="toon-over-json-for-agent-io"))
    actions = dr.review(
        entries=[entry()],
        ledger=ledger,
        provider=lens_map(
            {
                "correctness": ("refute", "benchmark methodology flawed"),
                "prior-art": ("uphold", ""),
                "scope": ("uphold", ""),
            }
        ),
        today=TODAY,
    )
    assert len(actions) == 1
    action = actions[0]
    assert action.kind == "contest"
    assert action.claim_id == "toon-over-json-for-agent-io"
    assert "benchmark methodology flawed" in action.reason


def test_contest_action_carries_prior_art_and_scope_caveats():
    ledger = ledger_of(make_claim(id="toon-over-json-for-agent-io"))
    actions = dr.review(
        entries=[entry()],
        ledger=ledger,
        provider=lens_map(
            {
                "correctness": ("refute", "wrong"),
                "prior-art": ("refute", "cf. Zhao 2024"),
                "scope": ("uphold", ""),
            }
        ),
        today=TODAY,
    )
    action = actions[0]
    assert action.kind == "contest"
    assert len(action.caveats) == 1
    assert action.caveats[0].lens == "prior-art"


# --- Advisory-only caveats (no retirement) ----------------------------------
def test_prior_art_only_refute_is_evidence_with_caveat_not_retirement():
    """When only prior-art/scope refute (correctness upheld), the claim is
    still supported — attach as evidence but flag the caveat so the render
    surface shows a warning chip."""
    ledger = ledger_of(make_claim(id="toon-over-json-for-agent-io"))
    actions = dr.review(
        entries=[entry()],
        ledger=ledger,
        provider=lens_map(
            {
                "correctness": ("uphold", ""),
                "prior-art": ("refute", "restates Zhao 2024"),
                "scope": ("uphold", ""),
            }
        ),
        today=TODAY,
    )
    assert len(actions) == 1
    action = actions[0]
    assert action.kind == "evidence_attach"
    assert action.claim_id == "toon-over-json-for-agent-io"
    assert len(action.caveats) == 1
    assert action.caveats[0].lens == "prior-art"


# --- Unknown / missing claims -----------------------------------------------
def test_related_claim_not_in_ledger_is_skipped():
    """If an entry names a claim ID that doesn't exist, drop the pairing.
    The ledger is the source of truth; a stale ID isn't reason to break."""
    ledger = ledger_of(make_claim(id="known-claim"))
    stray = entry(related_claims=["not-a-real-claim", "known-claim"])
    actions = dr.review(entries=[stray], ledger=ledger, provider=always("uphold"), today=TODAY)
    assert len(actions) == 1
    assert actions[0].claim_id == "known-claim"


def test_unknown_claim_id_emits_stderr_warning(capsys):
    """The skip is deliberate but should be visible — otherwise the ledger and
    analyzer drift apart silently."""
    ledger = ledger_of(make_claim(id="known-claim"))
    stray = entry(
        title="A stray finding",
        related_claims=["not-a-real-claim"],
    )
    dr.review(entries=[stray], ledger=ledger, provider=always("uphold"), today=TODAY)
    captured = capsys.readouterr()
    assert "not-a-real-claim" in captured.err
    assert "unknown claim" in captured.err.lower()


def test_entry_without_related_claims_produces_no_action():
    ledger = ledger_of(make_claim(id="toon-over-json-for-agent-io"))
    e = make_entry()
    e.pop("related_claims", None)
    actions = dr.review(entries=[e], ledger=ledger, provider=always("uphold"), today=TODAY)
    assert actions == []


# --- Time-based drift sweep -------------------------------------------------
def test_stale_claim_beyond_90_days_produces_sweep_action():
    stale = make_claim(id="old-belief", last_reviewed="2026-04-01")  # >90d before TODAY
    fresh = make_claim(
        id="recent-belief",
        last_reviewed="2026-08-01",
        statement="Recent belief.",
        evidence=[
            {"stance": "supports", "url": "https://x", "title": "T", "published": "2026-08-01"}
        ],
    )
    ledger = ledger_of(stale, fresh)
    actions = dr.review(entries=[], ledger=ledger, provider=always("uphold"), today=TODAY)
    kinds = [(a.kind, a.claim_id) for a in actions]
    assert ("sweep_stale", "old-belief") in kinds
    assert ("sweep_stale", "recent-belief") not in kinds


def test_stale_sweep_ignores_retired_claims():
    """Retired claims (superseded/refuted) don't need a stale-review PR — they
    already have a final answer."""
    retired = make_claim(
        id="retired-belief",
        status="superseded",
        superseded_by=["successor"],
        superseded_on="2025-05-01",
        supersession_reason="better method found",
        last_reviewed="2025-05-01",
    )
    ledger = ledger_of(retired)
    actions = dr.review(entries=[], ledger=ledger, provider=always("uphold"), today=TODAY)
    assert actions == []


def test_stale_threshold_is_configurable():
    """The 90-day default is calibration-driven; the caller can override."""
    claim = make_claim(id="borderline", last_reviewed="2026-07-05")  # 34 days before TODAY
    ledger = ledger_of(claim)
    # Default 90 → not stale
    default = dr.review(entries=[], ledger=ledger, provider=always("uphold"), today=TODAY)
    assert default == []
    # Tighter 30 → stale
    tighter = dr.review(
        entries=[], ledger=ledger, provider=always("uphold"), today=TODAY, stale_days=30
    )
    assert any(a.kind == "sweep_stale" and a.claim_id == "borderline" for a in tighter)


def test_missing_last_reviewed_treated_as_stale():
    """A claim with no last_reviewed date is stale by default — it's never
    been checked, so trigger the sweep."""
    claim = make_claim(id="unreviewed")
    claim.pop("last_reviewed", None)
    ledger = ledger_of(claim)
    actions = dr.review(entries=[], ledger=ledger, provider=always("uphold"), today=TODAY)
    assert any(a.kind == "sweep_stale" and a.claim_id == "unreviewed" for a in actions)


# --- PR body shape ----------------------------------------------------------
def test_summarize_actions_groups_by_kind_verb_first():
    """The render PR body leads with claim changes. summarize() returns a
    verb-first grouping ('contest N', 'evidence_attach N', 'sweep_stale N')
    so the renderer can turn it into an H2-section outline."""
    ledger = ledger_of(
        make_claim(id="claim-a"),
        make_claim(
            id="claim-b",
            statement="B",
            evidence=[
                {"stance": "supports", "url": "https://x", "title": "T", "published": "2026-08-01"}
            ],
        ),
    )
    actions = [
        dr.DriftAction(kind="contest", claim_id="claim-a", reason="r", source=None),
        dr.DriftAction(kind="evidence_attach", claim_id="claim-b", reason="", source=None),
        dr.DriftAction(kind="evidence_attach", claim_id="claim-a", reason="", source=None),
    ]
    summary = dr.summarize(actions)
    assert summary["contest"] == 1
    assert summary["evidence_attach"] == 2
    assert summary["sweep_stale"] == 0
