"""Tests for the claim-ledger renderer — the pages a reader actually lands on."""

from __future__ import annotations

import generate_claims as gc
from test_claims import ledger_of, make_claim

import claims

NOW = "2026-07-26"


def superseded_pair() -> dict:
    """A retired claim plus the claim that replaced it, edges already wired."""
    old = make_claim(
        id="grep-is-enough-for-code-search",
        statement="Lexical grep/glob search is sufficient for agent code retrieval.",
        first_seen="2026-03-01",
    )
    new = make_claim(
        id="code-graph-beats-lexical-search",
        statement="Graph-based code retrieval beats lexical search on multi-hop tasks.",
        first_seen="2026-07-20",
    )
    return claims.supersede(
        ledger_of(old, new),
        old_id="grep-is-enough-for-code-search",
        new_id="code-graph-beats-lexical-search",
        reason="Lexical search misses cross-file call relationships.",
        date="2026-07-26",
    )


# --- Topic page -------------------------------------------------------------
def test_current_claims_render_above_retired_ones():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    assert md.index("Graph-based code retrieval") < md.index("Lexical grep/glob search")


def test_retired_claim_shows_why_it_was_pushed_down():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    assert "Lexical search misses cross-file call relationships." in md
    assert "2026-07-26" in md


def test_retired_claim_links_to_what_replaced_it():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    assert f"(#{gc.anchor_id('code-graph-beats-lexical-search')})" in md


def test_winning_claim_says_what_it_replaced():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    winner = md.split("Lexical grep/glob search")[0]
    assert "Replaces" in winner
    assert f"(#{gc.anchor_id('grep-is-enough-for-code-search')})" in winner


def test_current_claim_renders_guidance_and_evidence():
    ledger = ledger_of(
        make_claim(guidance="Use TOON for large uniform arrays.", scope="Not for nested data.")
    )
    md = gc.render_topic("ai-research", ledger, NOW)
    assert "Use TOON for large uniform arrays." in md
    assert "Not for nested data." in md
    assert "https://example.com/toon-benchmarks" in md


def test_contested_claims_get_their_own_section():
    ledger = ledger_of(make_claim(id="disputed", status="contested"))
    md = gc.render_topic("ai-research", ledger, NOW)
    assert "Contested" in md


def test_other_topics_are_excluded():
    ledger = ledger_of(
        make_claim(id="research-one", topic="ai-research"),
        make_claim(id="security-one", topic="ai-security", statement="A security claim."),
    )
    md = gc.render_topic("ai-research", ledger, NOW)
    assert "A security claim." not in md


def test_empty_topic_renders_without_crashing():
    md = gc.render_topic("product-security", claims.empty_ledger(), NOW)
    assert "Product Security" in md
    assert "No claims" in md


def test_topic_page_reports_status_counts():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    assert "1 current" in md
    assert "1 superseded" in md


# --- Index page -------------------------------------------------------------
def test_index_links_every_topic():
    md = gc.render_index(superseded_pair(), NOW)
    for topic in claims.c.TOPICS:
        assert f"{topic}.md" in md


def test_index_shows_recent_supersessions_newest_first():
    ledger = superseded_pair()
    older = make_claim(
        id="older-retired",
        statement="An older retired claim.",
        status="superseded",
        superseded_by=["code-graph-beats-lexical-search"],
        superseded_on="2026-02-01",
        supersession_reason="Old reason.",
    )
    ledger = claims.add_claim(ledger, older)
    index = claims.claim_index(ledger["claims"])
    index["code-graph-beats-lexical-search"]["supersedes"] = [
        "grep-is-enough-for-code-search",
        "older-retired",
    ]
    md = gc.render_index(ledger, NOW)
    assert md.index("Lexical grep/glob search") < md.index("An older retired claim.")


def test_index_handles_an_empty_ledger():
    md = gc.render_index(claims.empty_ledger(), NOW)
    assert "0 claims" in md or "No claims" in md


# --- Anchors ----------------------------------------------------------------
def test_anchor_ids_are_stable_and_slug_like():
    assert (
        gc.anchor_id("code-graph-beats-lexical-search") == "claim-code-graph-beats-lexical-search"
    )


def test_every_rendered_link_target_exists_on_the_page():
    md = gc.render_topic("ai-research", superseded_pair(), NOW)
    for claim_id in ("code-graph-beats-lexical-search", "grep-is-enough-for-code-search"):
        anchor = gc.anchor_id(claim_id)
        assert f'<a id="{anchor}">' in md or f'name="{anchor}"' in md


# --- main() -----------------------------------------------------------------
def test_main_writes_the_index_and_every_topic_page(sandbox):
    claims.save_ledger(superseded_pair())
    assert gc.main() == 0
    base = sandbox / "claims"
    assert (base / "README.md").exists()
    for topic in claims.c.TOPICS:
        assert (base / f"{topic}.md").exists()


def test_main_refuses_to_render_an_invalid_ledger(sandbox):
    broken = ledger_of(make_claim(status="superseded"))  # retired with no successor
    claims.save_ledger(broken)
    assert gc.main() != 0


def test_main_succeeds_on_an_empty_ledger(sandbox):
    assert gc.main() == 0
    assert (sandbox / "claims" / "README.md").exists()
