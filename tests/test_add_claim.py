"""Tests for the add_claim CLI — the only sanctioned way to write the ledger."""

from __future__ import annotations

from pathlib import Path

import add_claim
import pytest

import claims

ROOT = Path(__file__).resolve().parents[1]

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


# --- correct ----------------------------------------------------------------
def test_correct_rewrites_live_fields_and_stays_valid(sandbox):
    add_claim.main(new_args("live"))
    argv = ["correct", "live", "--statement", "Sharper.", "--confidence", "0.4"]
    assert add_claim.main(argv + ["--first-seen", "2006-07-19", "--tags", "x, y"]) == 0
    (claim,) = claims.load_ledger()["claims"]
    assert claim["statement"] == "Sharper."
    assert claim["confidence"] == 0.4
    assert claim["first_seen"] == "2006-07-19"
    assert claim["tags"] == ["x", "y"]


def test_correct_resolves_a_domain_name_to_its_taxonomy_id(sandbox):
    add_claim.main(new_args("dom"))
    assert add_claim.main(["correct", "dom", "--domain", "Evaluation & Benchmarks"]) == 0
    assert claims.load_ledger()["claims"][0]["domain"] == "air.evals"


def test_correct_rejects_a_domain_from_another_topic(sandbox):
    add_claim.main(new_args("dom"))
    assert add_claim.main(["correct", "dom", "--domain", "ps.appsec"]) == 1
    assert claims.load_ledger()["claims"][0]["domain"] == ""


def test_correct_refuses_to_rewrite_a_retired_claims_history(sandbox):
    add_claim.main(new_args("old"))
    add_claim.main(new_args("new"))
    add_claim.main(["supersede", "old", "new", "--reason", "Better."])
    assert add_claim.main(["correct", "old", "--statement", "Rewritten."]) == 1
    assert add_claim.main(["correct", "old", "--domain", "air.evals"]) == 0
    old = claims.claim_index(claims.load_ledger()["claims"])["old"]
    assert old["statement"] == "Statement for old."
    assert old["domain"] == "air.evals"


def test_correct_rejects_bad_input(sandbox):
    add_claim.main(new_args("conf"))
    assert add_claim.main(["correct", "conf", "--confidence", "1.5"]) == 1
    assert add_claim.main(["correct", "nope", "--confidence", "0.5"]) == 1
    assert add_claim.main(["correct", "conf"]) == 1


# --- fix-evidence -----------------------------------------------------------
def test_fix_evidence_corrects_stance_title_and_url(sandbox):
    add_claim.main(new_args("ev"))
    argv = ["fix-evidence", "ev", "--url", "https://example.com/paper", "--stance", "contests"]
    argv += ["--new-url", "https://example.com/real", "--title", "Real", "--note", "n"]
    assert add_claim.main(argv) == 0
    (item,) = claims.load_ledger()["claims"][0]["evidence"]
    assert item == {
        "stance": "contests",
        "url": "https://example.com/real",
        "title": "Real",
        "published": "2026-06-01",
        "note": "n",
    }


def test_fix_evidence_removes_one_duplicate_by_occurrence(sandbox):
    add_claim.main(new_args("dup", "--evidence", EVIDENCE))
    url = "https://example.com/paper"
    assert add_claim.main(["fix-evidence", "dup", "--url", url, "--remove"]) == 1
    argv = ["fix-evidence", "dup", "--url", url, "--remove", "--occurrence"]
    assert add_claim.main(argv + ["3"]) == 1
    assert add_claim.main(argv + ["2"]) == 0
    assert len(claims.load_ledger()["claims"][0]["evidence"]) == 1


def test_fix_evidence_never_leaves_a_claim_without_sources(sandbox):
    add_claim.main(new_args("solo"))
    argv = ["fix-evidence", "solo", "--url", "https://example.com/paper", "--remove"]
    assert add_claim.main(argv) == 1
    assert len(claims.load_ledger()["claims"][0]["evidence"]) == 1


def test_fix_evidence_rejects_unknowns_and_retired_claims(sandbox):
    add_claim.main(new_args("a"))
    add_claim.main(new_args("b"))
    url = "https://example.com/paper"
    assert add_claim.main(["fix-evidence", "zz", "--url", url, "--remove"]) == 1
    assert add_claim.main(["fix-evidence", "a", "--url", "https://x.test", "--remove"]) == 1
    assert add_claim.main(["fix-evidence", "a", "--url", url, "--stance", "vibes"]) == 1
    add_claim.main(["supersede", "a", "b", "--reason", "Better."])
    assert add_claim.main(["fix-evidence", "a", "--url", url, "--stance", "contests"]) == 1


# --- ledger dates + refuted controls ----------------------------------------
def _dates(claim_id: str) -> tuple:
    found = claims.claim_index(claims.load_ledger()["claims"])[claim_id]
    return found.get("added_on"), found.get("changed_on")


def _rewrite(claim_id: str, **fields) -> None:
    ledger = claims.load_ledger()
    claims.claim_index(ledger["claims"])[claim_id].update(fields)
    claims.save_ledger(ledger)


def test_new_stamps_added_on_and_changed_on(sandbox):
    assert add_claim.main(new_args("dated")) == 0
    assert _dates("dated") == ("2026-07-15", "2026-07-15")  # the frozen test clock


def test_status_move_stamps_changed_on_but_a_no_op_does_not(sandbox):
    add_claim.main(new_args("moving"))
    _rewrite("moving", added_on="2026-07-01", changed_on="2026-07-01")
    assert add_claim.main(["status", "moving", "--set", "current"]) == 0
    assert _dates("moving") == ("2026-07-01", "2026-07-01")
    assert add_claim.main(["status", "moving", "--set", "contested"]) == 0
    assert _dates("moving") == ("2026-07-01", "2026-07-15")


@pytest.mark.parametrize(
    "argv",
    [
        ["evidence", "steady", "--evidence", "supports|https://example.com/more"],
        ["correct", "steady", "--guidance", "Reworded."],
        ["fix-evidence", "steady", "--url", "https://example.com/paper", "--note", "n"],
    ],
)
def test_non_status_writes_leave_changed_on_alone(sandbox, argv):
    add_claim.main(new_args("steady"))
    _rewrite("steady", added_on="2026-07-01", changed_on="2026-07-01")
    assert add_claim.main(argv) == 0
    assert _dates("steady") == ("2026-07-01", "2026-07-01")


def test_supersede_records_refuted_controls_and_changed_on(sandbox):
    add_claim.main(new_args("old-way"))
    add_claim.main(new_args("new-way"))
    argv = ["supersede", "old-way", "new-way", "--reason", "r", "--refuted", "--date", "2026-07-01"]
    assert add_claim.main([*argv, "--refuted-control=--ignore-scripts"]) == 0
    old = claims.claim_index(claims.load_ledger()["claims"])["old-way"]
    assert old["refuted_controls"] == ["--ignore-scripts"]
    assert (old["superseded_on"], old["changed_on"]) == ("2026-07-01", "2026-07-15")


def test_correct_sets_refuted_controls_on_retired_only(sandbox):
    add_claim.main(new_args("old-way"))
    add_claim.main(new_args("new-way"))
    add_claim.main(["supersede", "old-way", "new-way", "--reason", "r"])
    assert add_claim.main(["correct", "new-way", "--refuted-control", "x"]) == 1
    assert add_claim.main(["correct", "old-way", "--refuted-control", "prefer json"]) == 0
    old = claims.claim_index(claims.load_ledger()["claims"])["old-way"]
    assert old["refuted_controls"] == ["prefer json"]


def test_correct_refuses_a_refuted_control_that_live_guidance_recommends(sandbox):
    add_claim.main(new_args("old-way"))
    add_claim.main(new_args("new-way", "--guidance", "Prefer --ignore-scripts."))
    add_claim.main(["supersede", "old-way", "new-way", "--reason", "r"])
    assert add_claim.main(["correct", "old-way", "--refuted-control=--ignore-scripts"]) == 1
    old = claims.claim_index(claims.load_ledger()["claims"])["old-way"]
    assert "refuted_controls" not in old


def test_backfill_dates_fills_missing_dates_once(sandbox, monkeypatch):
    add_claim.main(new_args("legacy"))
    ledger = claims.load_ledger()
    for claim in ledger["claims"]:
        del claim["added_on"], claim["changed_on"]
    claims.save_ledger(ledger)
    history = [("2026-07-02", {"claims": [{"id": "legacy", "status": "current"}]})]
    monkeypatch.setattr(add_claim, "ledger_history", lambda: history)
    assert add_claim.main(["backfill-dates"]) == 0
    assert _dates("legacy") == ("2026-07-02", "2026-07-02")
    monkeypatch.setattr(add_claim, "ledger_history", lambda: pytest.fail("history re-read"))
    assert add_claim.main(["backfill-dates"]) == 0


def test_parse_evidence_reads_an_optional_note_that_may_hold_pipes():
    (item,) = add_claim.parse_evidence(["supports|https://example.com/a|T|2026-09-01|x | y"])
    assert item["note"] == "x | y"
    (bare,) = add_claim.parse_evidence(["supports|https://example.com/a|T|2026-09-01|"])
    assert "note" not in bare


def test_scan_session_writes_claims_only_through_the_cli():
    text = (ROOT / "scripts" / "scan_containment.sh").read_text()
    assert '"Edit(data/claims.json)"' in text
    assert '"Bash(python scripts/add_claim.py evidence *)"' in text
    assert "add_claim.py supersede" not in text and "add_claim.py *" not in text
