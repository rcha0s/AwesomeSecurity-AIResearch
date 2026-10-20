"""Tests for scripts/briefing.py — the front-page picks README and site share."""

from __future__ import annotations

import briefing as b
import taxonomy

NOW = "2026-10-20"


def row(rid, published, n_corr=0, composite=50, updated=""):
    corr = [{"url": f"https://o{i}.example/{rid}", "source_name": f"o{i}"} for i in range(n_corr)]
    return {
        "id": rid,
        "published": published,
        "updated": updated,
        "corroborators": corr,
        "composite": composite,
    }


def ids(rows):
    return [r["id"] for r in rows]


def test_most_covered_story_leads_then_most_recent():
    rows = [
        row("one-source-newest", "2026-10-19"),
        row("three-sources", "2026-10-14", n_corr=2),
        row("two-sources", "2026-10-18", n_corr=1),
        row("one-source-older", "2026-10-15"),
        row("one-source-mid", "2026-10-17"),
    ]
    got, topped = b.top_stories(rows, NOW, 7)
    assert not topped
    assert ids(got) == [
        "three-sources",
        "two-sources",
        "one-source-newest",
        "one-source-mid",
        "one-source-older",
    ]


def test_capped_at_eight():
    rows = [row(f"s{i}", f"2026-10-{14 + i % 6:02d}") for i in range(10)]
    got, topped = b.top_stories(rows, NOW, 7)
    assert len(got) == 8 and not topped


def test_a_fresh_update_brings_an_old_story_into_the_week():
    rows = [row("old-but-updated", "2026-08-01", updated="2026-10-19")]
    rows += [row(f"s{i}", "2026-10-18") for i in range(4)]
    got, topped = b.top_stories(rows, NOW, 7)
    assert "old-but-updated" in ids(got) and not topped


def test_a_thin_week_is_topped_up_with_the_most_recent_and_says_so():
    rows = [row("fresh", "2026-10-19"), row("aug", "2026-08-01"), row("sep", "2026-09-30")]
    rows += [row("jul", "2026-07-01"), row("sep2", "2026-09-02", n_corr=3), row("may", "2026-05")]
    got, topped = b.top_stories(rows, NOW, 7)
    assert topped
    assert ids(got) == ["fresh", "sep", "sep2", "aug", "jul"]


def test_empty_rows_yield_nothing():
    assert b.top_stories([], NOW, 7) == ([], True)


def claim(cid, status="current", reviewed="", conf=0.5, guidance="Do it."):
    return {
        "id": cid,
        "status": status,
        "last_reviewed": reviewed,
        "confidence": conf,
        "guidance": guidance,
    }


def test_top_claims_are_current_with_guidance_freshest_then_most_confident():
    claims = [
        claim("old-high", reviewed="2026-08-01", conf=0.95),
        claim("new-low", reviewed="2026-09-09", conf=0.6),
        claim("new-high", reviewed="2026-09-09", conf=0.9),
        claim("retired", status="superseded", reviewed="2026-10-01"),
        claim("contested", status="contested", reviewed="2026-10-01"),
        claim("no-guidance", reviewed="2026-10-01", guidance=""),
        claim("never-reviewed", conf=0.99),
    ]
    assert ids(b.top_claims(claims)) == ["new-high", "new-low", "old-high"]


def test_claim_domain_maps_labels_to_taxonomy_ids_but_not_bare_defaults():
    tax = taxonomy.get()
    assert b.claim_domain({"topic": "ai-security", "domain": "Prompt Injection"}, tax) == (
        "ais.prompt-injection"
    )
    assert b.claim_domain({"topic": "ai-security", "domain": "ais.mcp-tools"}, tax) == (
        "ais.mcp-tools"
    )
    assert b.claim_domain({"topic": "ai-security", "domain": "Zzyzx"}, tax) == ""
    assert b.claim_domain({"topic": "nope", "domain": "Prompt Injection"}, tax) == ""
    assert b.claim_domain({"topic": "ai-security"}, tax) == ""
