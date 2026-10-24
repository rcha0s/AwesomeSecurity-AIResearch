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


def test_the_live_claim_ledger_has_no_stale_agent_era_evidence(monkeypatch):
    """The actual gate: every claim committed to data/claims.json must pass
    the currency check, independent of any sandboxing. Run as part of the
    normal test suite so a claim added or edited without a modern, on-topic
    source fails CI before it reaches prod."""
    import json
    from datetime import UTC, datetime
    from pathlib import Path

    import common

    # The real ledger's added_on/changed_on are real dates: judge "not in the
    # future" against the real clock, not the suite's frozen one.
    monkeypatch.setattr(common, "utcnow", lambda: datetime.now(UTC))
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


# --- Contradiction check: live text vs retired controls ---------------------
def _retired_for(*controls, **over):
    return make_claim(
        id="ignore-scripts-is-enough",
        status="refuted",
        superseded_by=["import-time-payloads"],
        superseded_on="2026-07-15",
        supersession_reason="Import-time payloads get past it.",
        refuted_controls=list(controls),
        **over,
    )


def _successor(**over):
    return make_claim(
        id="import-time-payloads",
        supersedes=["ignore-scripts-is-enough"],
        statement="Import-time payloads defeat --ignore-scripts.",
        guidance="Do not treat --ignore-scripts as the control; sandbox the first import.",
        **over,
    )


def _check(*claim_list):
    return claims.validate_ledger(ledger_of(*claim_list))


def test_live_guidance_recommending_a_refuted_control_fails():
    bad = make_claim(id="installs-run-code", guidance="Prefer --ignore-scripts + a build step.")
    assert _check(_retired_for("--ignore-scripts"), _successor(), bad) == [
        "installs-run-code: guidance recommends '--ignore-scripts', which "
        "ignore-scripts-is-enough was retired for; reword it against import-time-payloads"
    ]


ALL_CONTROLS = (
    "--ignore-scripts",
    "model scanner",
    "instruction hierarchy",
    "human code review",
    "input classifier",
)


def test_guidance_match_is_case_insensitive_and_allows_plurals():
    bad = make_claim(id="installs-run-code", guidance="Run Model Scanners on every artifact.")
    errors = _check(_retired_for(*ALL_CONTROLS), _successor(), bad)
    assert errors == [
        "installs-run-code: guidance recommends 'model scanner', which "
        "ignore-scripts-is-enough was retired for; reword it against import-time-payloads"
    ]


def test_a_recommendation_still_fails():
    bad = make_claim(guidance="Use --ignore-scripts to stop supply-chain attacks.", id="x-y")
    assert len(_check(_retired_for(*ALL_CONTROLS), _successor(), bad)) == 1


def test_control_must_be_a_whole_phrase():
    ok = make_claim(id="x-y", guidance="Use --ignore-scripts-v2 and model scannerish tools.")
    assert _check(_retired_for(*ALL_CONTROLS), _successor(), ok) == []


DESCRIPTIVE = [
    "Model scanners miss payloads that only trigger at load time.",
    "Training an instruction hierarchy raised injection resistance on the benchmark.",
    "Human code review of agent PRs took 3x longer.",
    "An input classifier flagged 40% of attacks, so layer containment on top.",
    "Avoid --ignore-scripts as your only install control.",
    "Replace --ignore-scripts with a sandbox.",
]


@pytest.mark.parametrize("text", DESCRIPTIVE)
def test_statements_describe_and_are_not_checked(text):
    ok = make_claim(id="x-y", statement=text)
    assert _check(_retired_for(*ALL_CONTROLS), _successor(), ok) == []


@pytest.mark.parametrize(
    "text",
    [
        "Model scanners miss payloads that only trigger at load time.",
        "Avoid --ignore-scripts as your only install control.",
        "Replace --ignore-scripts with a sandbox.",
        "Drop the input classifier once containment holds.",
        "Keep human code review, but gate secrets with automated checks.",
        "An instruction hierarchy helps, however it is only a cost-raiser.",
        "Scanners have limited value; a model scanner fails on pickle tricks.",
        "Use install flags (e.g. --ignore-scripts) only as a speed bump.",
        "Use install flags (i.e. --ignore-scripts) without trusting them.",
        "Ship nothing unless a model scanner and a sandbox both pass.",
        "A model scanner missed it.",
    ],
)
def test_caveated_guidance_passes(text):
    ok = make_claim(id="x-y", guidance=text)
    assert _check(_retired_for(*ALL_CONTROLS), _successor(), ok) == []


def test_eg_does_not_split_the_sentence():
    assert (
        claims.recommended_controls(
            "Don't use flags, e.g. --ignore-scripts, here.", {"--ignore-scripts": "x"}
        )
        == []
    )


@pytest.mark.parametrize(
    "text",
    [
        "Do not treat --ignore-scripts as the control.",
        "--ignore-scripts alone is insufficient.",
        "Import-time payloads defeat --ignore-scripts.",
        "Sandbox installs rather than relying on --ignore-scripts.",
        "--ignore-scripts isn't enough here.",
    ],
)
def test_a_caveated_mention_is_not_a_recommendation(text):
    ok = make_claim(id="installs-run-code", guidance=text)
    assert _check(_retired_for("--ignore-scripts"), _successor(), ok) == []


def test_only_the_recommending_sentence_counts():
    text = "Do not rely on provenance alone. Prefer --ignore-scripts everywhere."
    bad = make_claim(id="installs-run-code", guidance=text)
    assert len(_check(_retired_for("--ignore-scripts"), _successor(), bad)) == 1


def test_retired_claims_may_keep_mentioning_their_own_control():
    old = _retired_for("--ignore-scripts", guidance="Install with --ignore-scripts.")
    assert _check(old, _successor()) == []


def test_refuted_controls_must_be_strings_on_a_retired_claim():
    live = make_claim(refuted_controls=["--ignore-scripts"])
    assert any("retired claim" in e for e in claims.validate_claim(live, set()))
    errors = claims.validate_claim(_retired_for(""), {"import-time-payloads"})
    assert any("non-empty strings" in e for e in errors)


def test_no_refuted_controls_means_no_contradiction_errors():
    plain = make_claim(id="installs-run-code", guidance="Prefer --ignore-scripts.")
    assert _check(plain) == []


# --- Ledger dates: added_on / changed_on ------------------------------------
def test_ledger_dates_are_valid_when_ordered_and_past():
    claim = make_claim(added_on="2026-07-01", changed_on="2026-07-10")
    assert claims.validate_claim(claim, set()) == []


@pytest.mark.parametrize(
    "over, needle",
    [
        ({"added_on": "2026-07-01"}, "travel together"),
        ({"changed_on": "2026-07-01"}, "travel together"),
        ({"added_on": "2026-07", "changed_on": "2026-07-02"}, "YYYY-MM-DD"),
        ({"added_on": "2026-02-30", "changed_on": "2026-03-01"}, "YYYY-MM-DD"),
        ({"added_on": "2026-07-01", "changed_on": "2027-01-01"}, "future"),
        ({"added_on": "2026-07-10", "changed_on": "2026-07-01"}, "before added_on"),
    ],
)
def test_bad_ledger_dates_are_rejected(over, needle):
    errors = claims.validate_claim(make_claim(**over), set())
    assert any(needle in e for e in errors), errors


def test_supersede_stamps_changed_on_and_refuted_controls():
    old = make_claim(id="old-claim", added_on="2026-06-01", changed_on="2026-06-01")
    new = make_claim(id="new-claim")
    out = claims.supersede(
        ledger_of(old, new),
        "old-claim",
        "new-claim",
        reason="r",
        date="2026-05-01",
        status="refuted",
        changed_on="2026-07-10",
        refuted_controls=["--ignore-scripts"],
    )
    retired = claims.claim_index(out["claims"])["old-claim"]
    assert (retired["superseded_on"], retired["changed_on"]) == ("2026-05-01", "2026-07-10")
    assert retired["added_on"] == "2026-06-01"
    assert retired["refuted_controls"] == ["--ignore-scripts"]


def test_backfill_uses_first_appearance_and_last_status_change():
    snaps = [
        ("2026-07-01", ledger_of(make_claim(id="a"))),
        ("2026-07-05", ledger_of(make_claim(id="a"), make_claim(id="b"))),
        ("2026-07-09", ledger_of(make_claim(id="a", status="contested"), make_claim(id="b"))),
        ("2026-07-12", ledger_of(make_claim(id="a", status="contested"), make_claim(id="b"))),
    ]
    now = ledger_of(
        make_claim(id="a", status="contested"),
        make_claim(id="b"),
        make_claim(id="c"),
        make_claim(id="d", added_on="2026-06-01", changed_on="2026-06-02"),
    )
    out = claims.claim_index(claims.backfill_ledger_dates(now, snaps, "2026-07-14")["claims"])
    dates = {cid: (cl["added_on"], cl["changed_on"]) for cid, cl in out.items()}
    assert dates == {
        "a": ("2026-07-01", "2026-07-09"),
        "b": ("2026-07-05", "2026-07-05"),
        "c": ("2026-07-14", "2026-07-14"),  # not in history yet: today
        "d": ("2026-06-01", "2026-06-02"),  # never overwritten
    }
    assert now["claims"][0].get("added_on") is None  # input untouched
