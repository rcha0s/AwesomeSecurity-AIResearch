"""Tests for the claim ledger — the durable layer that records what we currently
believe, what we used to believe, and why the old answer was retired."""

from __future__ import annotations

import pytest

import claims


def make_claim(**over) -> dict:
    """A valid `current` claim; override any field via kwargs."""
    claim = {
        "id": "toon-over-json-for-agent-io",
        "topic": "ai-research",
        "domain": "Architecture & Optimization",
        "statement": "TOON encoding cuts agent I/O tokens 30-60% versus JSON at equal fidelity.",
        "status": "current",
        "confidence": 0.8,
        "guidance": "Use TOON for large uniform arrays in tool output.",
        "evidence": [
            {
                "stance": "supports",
                "url": "https://example.com/toon-benchmarks",
                "title": "TOON benchmarks",
                "published": "2026-06-01",
            }
        ],
        "tags": ["tokens", "serialization"],
        "first_seen": "2026-06-01",
    }
    claim.update(over)
    return claim


def ledger_of(*claim_list) -> dict:
    return {"schema_version": claims.CLAIMS_SCHEMA_VERSION, "claims": list(claim_list)}


# --- Single-claim validation ------------------------------------------------
def test_valid_claim_has_no_errors():
    assert claims.validate_claim(make_claim(), {"toon-over-json-for-agent-io"}) == []


@pytest.mark.parametrize("field", ["id", "topic", "statement", "status"])
def test_missing_required_field_is_an_error(field):
    claim = make_claim()
    del claim[field]
    errors = claims.validate_claim(claim, set())
    assert any(field in e for e in errors)


def test_id_must_be_kebab_case():
    errors = claims.validate_claim(make_claim(id="TOON Over JSON"), set())
    assert any("kebab" in e.lower() for e in errors)


def test_unknown_topic_is_rejected():
    errors = claims.validate_claim(make_claim(topic="quantum-basketry"), set())
    assert any("topic" in e for e in errors)


def test_unknown_status_is_rejected():
    errors = claims.validate_claim(make_claim(status="vibes"), set())
    assert any("status" in e for e in errors)


@pytest.mark.parametrize("bad", [-0.1, 1.5, "high"])
def test_confidence_must_be_a_unit_float(bad):
    errors = claims.validate_claim(make_claim(confidence=bad), set())
    assert any("confidence" in e for e in errors)


def test_claim_needs_at_least_one_piece_of_evidence():
    errors = claims.validate_claim(make_claim(evidence=[]), set())
    assert any("evidence" in e for e in errors)


def test_evidence_needs_a_url_and_a_known_stance():
    claim = make_claim(evidence=[{"stance": "vibes", "title": "no url"}])
    errors = claims.validate_claim(claim, set())
    assert any("url" in e for e in errors)
    assert any("stance" in e for e in errors)


# --- Evidence currency: catch stale citations on fast-moving claims ---------
def test_agent_era_claim_with_only_undated_generic_evidence_is_flagged():
    """Regression guard for ssrf-guards-must-cover-agent-outbound-calls: an
    agent/MCP-specific claim backed only by a generic, undated pre-agent
    reference should fail validation, not silently ship."""
    claim = make_claim(
        statement=(
            "SSRF guards on user-input URLs are not sufficient for agent "
            "applications: the agent can be steered into making outbound "
            "calls from tool responses, retrieval results, or MCP metadata."
        ),
        evidence=[{"stance": "supports", "url": "https://owasp.org/x", "title": "SSRF (OWASP)"}],
    )
    errors = claims.validate_claim(claim, {claim["id"]})
    assert any("agent/LLM-era" in e for e in errors)


def test_agent_era_claim_with_a_modern_dated_source_is_not_flagged():
    claim = make_claim(
        statement="MCP tool metadata can inject instructions into an agent.",
        evidence=[
            {"stance": "supports", "url": "https://example.com/a", "published": "2025-03-01"}
        ],
    )
    assert claims.validate_claim(claim, {claim["id"]}) == []


def test_retired_agent_era_claim_is_exempt_from_the_currency_check():
    """A superseded/refuted claim's evidence is frozen on purpose — it's a
    record of what was believed at the time, not something to keep fresh."""
    claim = make_claim(
        statement="Agents using MCP tools are inherently safe from injection.",
        status="refuted",
        evidence=[{"stance": "refutes", "url": "https://example.com/old"}],
        superseded_by=["something-newer"],
        superseded_on="2026-01-01",
        supersession_reason="Shown false.",
    )
    errors = claims.validate_claim(claim, {claim["id"], "something-newer"})
    assert not any("agent/LLM-era" in e for e in errors)


def test_claim_without_agent_era_terms_is_exempt_from_the_currency_check():
    claim = make_claim(
        statement="Canonicalize a user-derived file path before checking it stays in-sandbox.",
        evidence=[{"stance": "supports", "url": "https://cwe.mitre.org/data/definitions/22.html"}],
    )
    assert claims.validate_claim(claim, {claim["id"]}) == []


def test_the_live_claim_ledger_has_no_stale_agent_era_evidence():
    """The actual gate: every claim committed to data/claims.json must pass
    the currency check, independent of any sandboxing. Run as part of the
    normal test suite so a claim added or edited without a modern, on-topic
    source fails CI before it reaches prod."""
    import json
    from pathlib import Path

    real_path = Path(__file__).resolve().parent.parent / "data" / "claims.json"
    ledger = json.loads(real_path.read_text(encoding="utf-8"))
    assert claims.validate_ledger(ledger) == []


# --- Status / edge consistency ---------------------------------------------
def test_superseded_claim_must_name_its_successor_and_reason():
    claim = make_claim(status="superseded")
    errors = claims.validate_claim(claim, set())
    assert any("superseded_by" in e for e in errors)
    assert any("reason" in e for e in errors)
    assert any("superseded_on" in e for e in errors)


def test_superseded_claim_with_full_supersession_metadata_is_valid():
    claim = make_claim(
        id="json-is-default-agent-io",
        status="superseded",
        superseded_by=["toon-over-json-for-agent-io"],
        superseded_on="2026-07-26",
        supersession_reason="TOON showed equal fidelity at 30-60% fewer tokens.",
    )
    known = {"json-is-default-agent-io", "toon-over-json-for-agent-io"}
    assert claims.validate_claim(claim, known) == []


def test_current_claim_cannot_have_been_superseded():
    claim = make_claim(status="current", superseded_by=["something-newer"])
    errors = claims.validate_claim(claim, {"toon-over-json-for-agent-io", "something-newer"})
    assert any("current" in e for e in errors)


def test_edges_must_point_at_known_claims():
    claim = make_claim(supersedes=["a-claim-that-does-not-exist"])
    errors = claims.validate_claim(claim, {"toon-over-json-for-agent-io"})
    assert any("unknown claim" in e for e in errors)


def test_a_claim_cannot_supersede_itself():
    claim = make_claim(supersedes=["toon-over-json-for-agent-io"])
    errors = claims.validate_claim(claim, {"toon-over-json-for-agent-io"})
    assert any("itself" in e for e in errors)


# --- Ledger-level validation ------------------------------------------------
def test_duplicate_ids_are_rejected():
    errors = claims.validate_ledger(ledger_of(make_claim(), make_claim()))
    assert any("duplicate" in e.lower() for e in errors)


def test_supersession_edges_must_be_reciprocal():
    old = make_claim(
        id="json-is-default-agent-io",
        status="superseded",
        superseded_by=["toon-over-json-for-agent-io"],
        superseded_on="2026-07-26",
        supersession_reason="Fewer tokens at equal fidelity.",
    )
    new = make_claim()  # missing the matching `supersedes` back-edge
    errors = claims.validate_ledger(ledger_of(old, new))
    assert any("reciprocal" in e.lower() for e in errors)


def test_reciprocal_edges_validate_cleanly():
    old = make_claim(
        id="json-is-default-agent-io",
        status="superseded",
        superseded_by=["toon-over-json-for-agent-io"],
        superseded_on="2026-07-26",
        supersession_reason="Fewer tokens at equal fidelity.",
    )
    new = make_claim(supersedes=["json-is-default-agent-io"])
    assert claims.validate_ledger(ledger_of(old, new)) == []


def test_supersession_cycles_are_rejected():
    a = make_claim(
        id="claim-a",
        status="superseded",
        supersedes=["claim-b"],
        superseded_by=["claim-b"],
        superseded_on="2026-07-01",
        supersession_reason="b won",
    )
    b = make_claim(
        id="claim-b",
        status="superseded",
        supersedes=["claim-a"],
        superseded_by=["claim-a"],
        superseded_on="2026-07-02",
        supersession_reason="a won",
    )
    errors = claims.validate_ledger(ledger_of(a, b))
    assert any("cycle" in e.lower() for e in errors)


# --- Ordering: live on top, retired pushed to the bottom --------------------
def test_live_claims_sort_above_retired_ones():
    live = make_claim(id="live-claim", confidence=0.4)
    retired = make_claim(
        id="retired-claim",
        status="superseded",
        confidence=0.99,
        superseded_by=["live-claim"],
        superseded_on="2026-07-26",
        supersession_reason="replaced",
    )
    ordered = claims.order_claims([retired, live])
    assert [c["id"] for c in ordered] == ["live-claim", "retired-claim"]


def test_live_claims_sort_by_confidence_then_recency():
    low = make_claim(id="low", confidence=0.5, first_seen="2026-07-01")
    high = make_claim(id="high", confidence=0.9, first_seen="2026-06-01")
    ordered = claims.order_claims([low, high])
    assert [c["id"] for c in ordered] == ["high", "low"]


def test_contested_claims_rank_below_current_ones():
    current = make_claim(id="settled", confidence=0.5)
    contested = make_claim(id="disputed", status="contested", confidence=0.95)
    ordered = claims.order_claims([contested, current])
    assert [c["id"] for c in ordered] == ["settled", "disputed"]


def test_retired_claims_sort_most_recently_retired_first():
    older = make_claim(
        id="older",
        status="superseded",
        superseded_by=["x"],
        superseded_on="2026-01-01",
        supersession_reason="r",
    )
    newer = make_claim(
        id="newer",
        status="refuted",
        superseded_by=["x"],
        superseded_on="2026-07-01",
        supersession_reason="r",
    )
    ordered = claims.order_claims([older, newer])
    assert [c["id"] for c in ordered] == ["newer", "older"]


def test_is_live_and_is_retired_partition_the_statuses():
    for status in claims.STATUSES:
        claim = make_claim(status=status)
        assert claims.is_live(claim) != claims.is_retired(claim)


# --- Lineage ----------------------------------------------------------------
def test_lineage_walks_the_full_chain_of_replaced_claims():
    oldest = make_claim(
        id="v1",
        status="superseded",
        superseded_by=["v2"],
        superseded_on="2026-05-01",
        supersession_reason="v2 better",
    )
    middle = make_claim(
        id="v2",
        status="superseded",
        supersedes=["v1"],
        superseded_by=["v3"],
        superseded_on="2026-06-01",
        supersession_reason="v3 better",
    )
    newest = make_claim(id="v3", supersedes=["v2"])
    index = claims.claim_index([oldest, middle, newest])
    assert [c["id"] for c in claims.lineage(newest, index)] == ["v2", "v1"]


def test_lineage_is_empty_for_an_original_claim():
    claim = make_claim()
    assert claims.lineage(claim, claims.claim_index([claim])) == []


def test_lineage_survives_a_dangling_edge():
    claim = make_claim(supersedes=["never-written"])
    assert claims.lineage(claim, claims.claim_index([claim])) == []


# --- Mutations are immutable ------------------------------------------------
def test_supersede_sets_both_edges_and_retires_the_old_claim():
    old = make_claim(id="grep-is-enough")
    new = make_claim(id="code-graph-beats-grep")
    ledger = ledger_of(old, new)

    updated = claims.supersede(
        ledger,
        old_id="grep-is-enough",
        new_id="code-graph-beats-grep",
        reason="Graph retrieval beat lexical search on multi-hop tasks.",
        date="2026-07-26",
    )

    index = claims.claim_index(updated["claims"])
    assert index["grep-is-enough"]["status"] == "superseded"
    assert index["grep-is-enough"]["superseded_by"] == ["code-graph-beats-grep"]
    assert index["grep-is-enough"]["superseded_on"] == "2026-07-26"
    assert "multi-hop" in index["grep-is-enough"]["supersession_reason"]
    assert index["code-graph-beats-grep"]["supersedes"] == ["grep-is-enough"]
    assert claims.validate_ledger(updated) == []


def test_supersede_does_not_mutate_the_original_ledger():
    ledger = ledger_of(make_claim(id="old"), make_claim(id="new"))
    claims.supersede(ledger, "old", "new", reason="r", date="2026-07-26")
    assert ledger["claims"][0]["status"] == "current"
    assert "superseded_by" not in ledger["claims"][0]


def test_supersede_can_mark_a_claim_refuted_instead_of_superseded():
    ledger = ledger_of(make_claim(id="old"), make_claim(id="new"))
    updated = claims.supersede(
        ledger, "old", "new", reason="disproved", date="2026-07-26", status="refuted"
    )
    assert claims.claim_index(updated["claims"])["old"]["status"] == "refuted"


def test_supersede_rejects_an_unknown_claim_id():
    ledger = ledger_of(make_claim(id="old"))
    with pytest.raises(KeyError):
        claims.supersede(ledger, "old", "nope", reason="r", date="2026-07-26")


def test_add_claim_appends_without_mutating():
    ledger = ledger_of(make_claim(id="first"))
    updated = claims.add_claim(ledger, make_claim(id="second"))
    assert [c["id"] for c in updated["claims"]] == ["first", "second"]
    assert len(ledger["claims"]) == 1


def test_add_claim_rejects_a_duplicate_id():
    ledger = ledger_of(make_claim(id="first"))
    with pytest.raises(ValueError, match="already exists"):
        claims.add_claim(ledger, make_claim(id="first"))


# --- Persistence ------------------------------------------------------------
def test_load_ledger_returns_an_empty_ledger_when_absent(sandbox):
    ledger = claims.load_ledger()
    assert ledger["claims"] == []
    assert ledger["schema_version"] == claims.CLAIMS_SCHEMA_VERSION


def test_save_then_load_round_trips(sandbox):
    claims.save_ledger(ledger_of(make_claim()))
    assert claims.load_ledger()["claims"][0]["id"] == "toon-over-json-for-agent-io"


def test_claims_for_topic_filters_and_orders(sandbox):
    research = make_claim(id="research-claim", topic="ai-research")
    security = make_claim(id="security-claim", topic="ai-security")
    claims.save_ledger(ledger_of(security, research))
    got = claims.claims_for_topic(claims.load_ledger(), "ai-research")
    assert [c["id"] for c in got] == ["research-claim"]
