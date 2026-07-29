"""Tests for the add_claim CLI — the only sanctioned way to write the ledger."""

from __future__ import annotations

import add_claim
import pytest

import claims

EVIDENCE = "supports|https://example.com/paper|A paper|2026-06-01"


def new_args(claim_id: str, *extra: str) -> list[str]:
    return [
        "new",
        claim_id,
        "--topic",
        "ai-research",
        "--statement",
        f"Statement for {claim_id}.",
        "--evidence",
        EVIDENCE,
        *extra,
    ]


# --- Evidence parsing -------------------------------------------------------
def test_parse_evidence_reads_all_four_fields():
    (item,) = add_claim.parse_evidence([EVIDENCE])
    assert item == {
        "stance": "supports",
        "url": "https://example.com/paper",
        "title": "A paper",
        "published": "2026-06-01",
    }


def test_parse_evidence_allows_stance_and_url_only():
    (item,) = add_claim.parse_evidence(["refutes|https://example.com/x"])
    assert item == {"stance": "refutes", "url": "https://example.com/x"}


def test_parse_evidence_rejects_an_unknown_stance():
    with pytest.raises(SystemExit, match="stance"):
        add_claim.parse_evidence(["vibes|https://example.com/x"])


def test_parse_evidence_rejects_a_missing_url():
    with pytest.raises(SystemExit, match="stance\\|url"):
        add_claim.parse_evidence(["supports"])


def test_parse_evidence_handles_no_input():
    assert add_claim.parse_evidence(None) == []


# --- new --------------------------------------------------------------------
def test_new_writes_a_valid_claim(sandbox):
    assert add_claim.main(new_args("first-claim", "--confidence", "0.9", "--tags", "a,b")) == 0
    (claim,) = claims.load_ledger()["claims"]
    assert claim["id"] == "first-claim"
    assert claim["confidence"] == 0.9
    assert claim["tags"] == ["a", "b"]
    assert claim["first_seen"]


def test_new_rejects_a_duplicate_id(sandbox):
    add_claim.main(new_args("dupe"))
    assert add_claim.main(new_args("dupe")) == 1
    assert len(claims.load_ledger()["claims"]) == 1


def test_new_refuses_to_save_a_claim_with_no_evidence(sandbox):
    argv = ["new", "bare", "--topic", "ai-research", "--statement", "No sources."]
    assert add_claim.main(argv) == 1
    assert claims.load_ledger()["claims"] == []


def test_new_can_record_guidance_and_scope(sandbox):
    add_claim.main(new_args("guided", "--guidance", "Do it.", "--scope", "Not always."))
    (claim,) = claims.load_ledger()["claims"]
    assert claim["guidance"] == "Do it."
    assert claim["scope"] == "Not always."


# --- supersede --------------------------------------------------------------
def test_supersede_wires_both_ends_and_persists(sandbox):
    add_claim.main(new_args("old-answer"))
    add_claim.main(new_args("new-answer"))

    rc = add_claim.main(
        [
            "supersede",
            "old-answer",
            "new-answer",
            "--reason",
            "Better data.",
            "--date",
            "2026-07-26",
        ]
    )

    assert rc == 0
    index = claims.claim_index(claims.load_ledger()["claims"])
    assert index["old-answer"]["status"] == "superseded"
    assert index["old-answer"]["superseded_by"] == ["new-answer"]
    assert index["old-answer"]["supersession_reason"] == "Better data."
    assert index["new-answer"]["supersedes"] == ["old-answer"]


def test_supersede_can_mark_a_claim_refuted(sandbox):
    add_claim.main(new_args("wrong"))
    add_claim.main(new_args("right"))
    add_claim.main(["supersede", "wrong", "right", "--reason", "Disproved.", "--refuted"])
    index = claims.claim_index(claims.load_ledger()["claims"])
    assert index["wrong"]["status"] == "refuted"


def test_supersede_reports_an_unknown_claim(sandbox):
    add_claim.main(new_args("only-one"))
    assert add_claim.main(["supersede", "only-one", "ghost", "--reason", "r"]) == 1


def test_supersede_defaults_the_date_to_today(sandbox):
    add_claim.main(new_args("a"))
    add_claim.main(new_args("b"))
    add_claim.main(["supersede", "a", "b", "--reason", "r"])
    index = claims.claim_index(claims.load_ledger()["claims"])
    assert index["a"]["superseded_on"] == add_claim.today()


# --- evidence / status ------------------------------------------------------
def test_evidence_appends_to_an_existing_claim(sandbox):
    add_claim.main(new_args("growing"))
    rc = add_claim.main(["evidence", "growing", "--evidence", "contests|https://example.com/no"])
    assert rc == 0
    (claim,) = claims.load_ledger()["claims"]
    assert [e["stance"] for e in claim["evidence"]] == ["supports", "contests"]


def test_evidence_reports_an_unknown_claim(sandbox):
    assert add_claim.main(["evidence", "ghost", "--evidence", EVIDENCE]) == 1


def test_status_moves_a_claim_between_live_statuses(sandbox):
    add_claim.main(new_args("settled"))
    assert add_claim.main(["status", "settled", "--set", "contested"]) == 0
    assert claims.load_ledger()["claims"][0]["status"] == "contested"


def test_status_refuses_to_retire_a_claim_without_a_successor(sandbox):
    add_claim.main(new_args("settled"))
    with pytest.raises(SystemExit):  # argparse rejects the retired status outright
        add_claim.main(["status", "settled", "--set", "superseded"])


# --- validate / list --------------------------------------------------------
def test_validate_passes_on_a_healthy_ledger(sandbox):
    add_claim.main(new_args("healthy"))
    assert add_claim.main(["validate"]) == 0


def test_validate_fails_on_a_broken_ledger(sandbox):
    claims.save_ledger(
        {
            "schema_version": claims.CLAIMS_SCHEMA_VERSION,
            "claims": [
                {"id": "broken", "topic": "ai-research", "statement": "x", "status": "current"}
            ],
        }
    )
    assert add_claim.main(["validate"]) == 1


def test_list_runs_over_every_topic(sandbox, capsys):
    add_claim.main(new_args("listed"))
    assert add_claim.main(["list"]) == 0
    assert "listed" in capsys.readouterr().out
