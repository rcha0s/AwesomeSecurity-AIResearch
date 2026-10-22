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


def claim(cid, status="current", first_seen="2026-01-01", **over):
    return {"id": cid, "status": status, "first_seen": first_seen, **over}


def retired(cid, by, on, status="superseded"):
    return claim(cid, status, superseded_by=[by], superseded_on=on, supersession_reason="why")


def kinds(changes):
    return [(ch["kind"], ch["claim"], ch.get("replaced", "")) for ch in changes]


def test_each_claim_stands_for_one_change():
    claims = [
        claim("added", first_seen="2026-10-18"),
        claim("winner", first_seen="2026-10-17", supersedes=["loser"]),
        retired("loser", "winner", "2026-10-17", status="refuted"),
        claim(
            "fight",
            "contested",
            first_seen="2026-02-01",
            evidence=[
                {"stance": "supports", "published": "2026-10-19"},
                {"stance": "contests", "published": "2026-10-16"},
                {"stance": "refutes", "published": "2026-03-01"},
            ],
        ),
        claim("undated", first_seen=""),
    ]
    assert kinds(b.all_changes(claims)) == [
        ("added", "added", ""),
        ("overturned", "winner", "loser"),  # the reversal, told once, by its winner
        ("contested", "fight", ""),  # dated by its newest contesting evidence
    ]
    assert [ch["date"] for ch in b.all_changes(claims)] == [
        "2026-10-18",
        "2026-10-17",
        "2026-10-16",
    ]


def test_contested_without_contesting_evidence_dates_from_first_seen():
    got = b.all_changes([claim("c", "contested", first_seen="2026-05", evidence=[{}])])
    assert got == [{"kind": "contested", "date": "2026-05", "claim": "c"}]


def test_a_full_week_shows_only_the_week_capped():
    claims = [claim(f"c{i}", first_seen=f"2026-10-1{i}") for i in range(4, 10)]
    claims += [claim("c-extra", first_seen="2026-10-19"), claim("old", first_seen="2026-01-01")]
    claims += [retired("gone", "old", "2026-09-01")]
    got, fresh = b.claim_changes(claims, NOW, 7, n_max=6)
    assert fresh == 6 and len(got) == 7  # the week's six, plus the latest reversal
    assert got[-1]["kind"] == "overturned" and got[-1]["replaced"] == "gone"


def test_a_quiet_week_tops_up_with_dated_earlier_changes():
    claims = [claim("new", first_seen="2026-10-19"), claim("sep", first_seen="2026-09-09")]
    claims += [claim("aug", first_seen="2026-08-01"), claim("jul", first_seen="2026-07-01")]
    claims += [claim("winner", supersedes=["loser"]), retired("loser", "winner", "2026-06-01")]
    got, fresh = b.claim_changes(claims, NOW, 7)
    assert fresh == 1
    assert kinds(got) == [
        ("added", "new", ""),
        ("added", "sep", ""),
        ("added", "aug", ""),
        ("overturned", "winner", "loser"),
    ]


def test_nothing_this_week_still_shows_the_latest_changes():
    got, fresh = b.claim_changes([claim("a", first_seen="2026-01-02")], NOW, 7)
    assert fresh == 0 and kinds(got) == [("added", "a", "")]
    assert b.claim_changes([], NOW, 7) == ([], 0)


def test_changes_note_says_what_the_window_held():
    assert b.changes_note(0, 0, 7) == "No claim has changed yet."
    assert b.changes_note(0, 3, 7).startswith("No claim changed in the last 7 days")
    assert b.changes_note(1, 3, 7).startswith("1 change in the last 7 days")
    assert b.changes_note(2, 3, 7).startswith("2 changes in the last 7 days")
    assert (
        b.changes_note(3, 3, 7) == "Every claim added, contested or overturned in the last 7 days."
    )


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
