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


def test_newest_story_leads_then_most_covered():
    rows = [
        row("one-source-newest", "2026-10-19"),
        row("three-sources", "2026-10-14", n_corr=2),
        row("two-sources-same-day", "2026-10-19", n_corr=1),
        row("one-source-older", "2026-10-15"),
        row("updated-yesterday", "2026-10-10", updated="2026-10-18"),
    ]
    got, topped = b.top_stories(rows, NOW, 7)
    assert not topped
    assert ids(got) == [
        "two-sources-same-day",
        "one-source-newest",
        "updated-yesterday",
        "one-source-older",
        "three-sources",
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


def test_an_old_reversal_takes_only_a_free_slot_and_is_pinned():
    claims = [claim(f"c{i}", first_seen=f"2026-10-1{i}") for i in range(5, 9)]  # 4 in the window
    claims += [claim("old", first_seen="2026-01-01"), retired("gone", "old", "2026-09-01")]
    got, fresh = b.claim_changes(claims, NOW, 7, n_max=6)
    assert fresh == 4 and len(got) == 5  # 4 from the window + the reversal in a free slot
    reversal = [ch for ch in got if ch["kind"] == "overturned"]
    assert [(ch["replaced"], ch["pinned"]) for ch in reversal] == [("gone", True)]
    assert not any("pinned" in ch for ch in got if ch["kind"] != "overturned")
    # No free slot (the window fills the cap): the reversal stays off the list.
    got, _ = b.claim_changes(claims, NOW, 7, n_max=4)
    assert [ch["kind"] for ch in got] == ["added"] * 4


def test_a_reversal_inside_the_window_is_not_pinned():
    claims = [claim("w", supersedes=["l"]), retired("l", "w", "2026-10-18")]
    got, _ = b.claim_changes(claims, NOW, 7)
    assert [ch["kind"] for ch in got] == ["overturned"] and "pinned" not in got[0]


def test_a_full_week_is_capped_and_counted_in_full_and_an_old_reversal_waits():
    claims = [claim(f"c{i}", first_seen=f"2026-10-1{i}") for i in range(4, 10)]
    claims += [claim("c-extra", first_seen="2026-10-19"), claim("old", first_seen="2026-01-01")]
    claims += [retired("gone", "old", "2026-09-01")]
    got, fresh = b.claim_changes(claims, NOW, 7, n_max=6)
    assert fresh == 7  # every change in the window, not just the ones shown
    assert len(got) == 6  # the cap holds
    assert all(ch["kind"] == "added" and ch["date"] >= "2026-10-14" for ch in got)
    assert [ch["date"] for ch in got] == sorted((ch["date"] for ch in got), reverse=True)


def test_an_old_reversal_never_takes_a_slot_from_a_full_window():
    """8 adds this week + a reversal on 10-15 + a January one: the six newest
    show, and neither reversal pushes a change from the window off the list."""
    claims = [claim(f"a{i}", first_seen=f"2026-10-{16 + i % 4}") for i in range(8)]
    claims += [claim("w1", supersedes=["l1"]), retired("l1", "w1", "2026-10-15")]
    claims += [claim("w0", supersedes=["l0"]), retired("l0", "w0", "2026-01-01")]
    got, fresh = b.claim_changes(claims, "2026-10-22", 7)
    assert fresh == 9 and len(got) == b.CHANGES_MAX
    assert not [ch for ch in got if ch["kind"] == "overturned"]
    assert b.changes_note(fresh, len(got), 7) == "The 6 newest of 9 changes in the last 7 days."


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
    assert b.changes_note(9, 6, 7) == "The 6 newest of 9 changes in the last 7 days."
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


# --- Biggest this week --------------------------------------------------------
def big(rid, published, n_corr=0, exploited=False, composite=50):
    return {**row(rid, published, n_corr=n_corr, composite=composite), "exploited": exploited}


def test_biggest_needs_two_sources_or_exploited_in_the_window():
    rows = [
        big("single", "2026-10-19"),
        big("two", "2026-10-19", n_corr=1),
        big("exploited-single", "2026-10-18", exploited=True),
        big("old-and-covered", "2026-09-01", n_corr=4),
    ]
    assert ids(b.biggest_stories(rows, NOW, 7)) == ["exploited-single", "two"]


def test_biggest_ranks_exploited_then_sources_then_newest_then_composite():
    rows = [
        big("three-src", "2026-10-15", n_corr=2),
        big("two-new", "2026-10-19", n_corr=1),
        big("two-old", "2026-10-16", n_corr=1),
        big("kev", "2026-10-14", exploited=True),
        big("two-new-high", "2026-10-19", n_corr=1, composite=90),
    ]
    got = b.biggest_stories(rows, NOW, 7, n_max=10)
    assert ids(got) == ["kev", "three-src", "two-new-high", "two-new", "two-old"]


def test_biggest_is_capped_at_three():
    rows = [big(f"s{i}", "2026-10-19", n_corr=1) for i in range(6)]
    assert len(b.biggest_stories(rows, NOW, 7)) == 3


def test_biggest_is_empty_when_nothing_qualifies():
    assert b.biggest_stories([big("a", "2026-10-19")], NOW, 7) == []
    assert b.biggest_stories([], NOW, 7) == []


def test_top_stories_leave_out_the_biggest_and_stay_capped_and_topped_up():
    rows = [big(f"s{i}", f"2026-10-{12 + i:02d}", n_corr=1 if i < 3 else 0) for i in range(10)]
    taken = set(ids(b.biggest_stories(rows, NOW, 7)))
    got, topped = b.top_stories(rows, NOW, 7, exclude=taken)
    assert not taken & set(ids(got))
    assert len(got) == 7 and not topped  # 10 rows minus the 3 in the lane
    thin = [big("a", "2026-10-19", n_corr=1)] + [
        big(f"o{i}", f"2026-09-{10 + i}") for i in range(6)
    ]
    lane = set(ids(b.biggest_stories(thin, NOW, 7)))
    got, topped = b.top_stories(thin, NOW, 7, exclude=lane)
    assert topped and "a" not in ids(got) and len(got) == 5
    assert b.fresh_count(got, NOW, 7) == 0


def test_biggest_note_names_the_window():
    assert b.biggest_note(7) == "Most covered or exploited in the last 7 days."
