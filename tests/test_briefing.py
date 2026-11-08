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


# --- Efficiency track ---------------------------------------------------------
COST, WORK = "air.cost-efficiency", "air.work-efficiency"


def eff(cid, domain_id, first_seen="2026-10-01", status="current", **over):
    return claim(cid, status=status, first_seen=first_seen, domain_id=domain_id, **over)


def test_efficiency_claims_pick_only_the_two_domains_live_newest_first():
    claims = [
        eff("old-cost", COST, "2026-09-01"),
        eff("new-work", WORK, "2026-10-10"),
        eff("other", "air.evals", "2026-10-15"),
        eff("gone", COST, "2026-10-12", status="superseded"),
        eff("mid-cost", COST, "2026-10-05", changed_on="2026-10-11", status="contested"),
    ]
    assert ids(b.efficiency_claims(claims)) == ["mid-cost", "new-work", "old-cost"]


def test_efficiency_claims_cap_at_four_and_tie_on_id():
    claims = [eff(f"c{i}", COST if i % 2 else WORK, "2026-10-10") for i in range(6)]
    assert ids(b.efficiency_claims(claims)) == ["c0", "c1", "c2", "c3"]


def test_efficiency_claims_empty():
    assert b.efficiency_claims([]) == []
    assert b.efficiency_claims([eff("x", "air.evals")]) == []


def test_efficiency_findings_are_recent_in_domain_capped_at_three():
    rows = [
        {**row("a", "2026-10-19"), "domain_id": COST},
        {**row("b", "2026-10-18"), "domain_id": WORK},
        {**row("c", "2026-10-17"), "domain_id": "air.evals"},
        {**row("d", "2026-10-01"), "domain_id": COST},
        {**row("e", "2026-10-16"), "domain_id": COST},
        {**row("f", "2026-10-15"), "domain_id": WORK},
    ]
    assert ids(b.efficiency_findings(rows, NOW, 7)) == ["a", "b", "e"]
    assert b.efficiency_findings([], NOW, 7) == []


# --- What to learn (ISA F11) ---
LEARN = {
    "days": 14,
    "max": 3,
    "min_pointers": 2,
    "proof_hosts": ["github.com", "arxiv.org", "huggingface.co"],
    "goals": [
        {"id": "evals", "name": "Evals", "domains": ["air.evals"], "keywords": ["benchmark"]},
        {"id": "lean", "name": "Low-token harness", "domains": [], "keywords": ["prompt caching"]},
    ],
}


def learn_row(rid, **over):
    base = {
        "id": rid,
        "published": "2026-10-18",
        "domain_id": "air.evals",
        "title": "A new eval method",
        "takeaway": "Cuts judge cost by 40% on the same set.",
        "summary": "",
        "url": f"https://blog-a.example/{rid}",
        "corroborators": [{"url": f"https://news-b.example/{rid}", "source_name": "B"}],
        "verified": True,
        "actionable": {"type": "eval", "title": "Try it", "detail": "Run it on your set."},
        "composite": 50,
    }
    return {**base, **over}


def picked(*rows, learning=LEARN, exclude=frozenset()):
    return ids(b.learning_picks(list(rows), learning, NOW, exclude=exclude)[0])


def test_a_row_passing_all_three_filters_is_picked_with_its_reasons():
    got, why = b.learning_picks([learn_row("ok")], LEARN, NOW)
    assert ids(got) == ["ok"]
    assert why["ok"] == {"proof": "measured", "pointers": 2, "goals": ["Evals"]}


def test_measured_means_a_comparison_never_a_bare_number():
    yes = [
        "Cuts judge cost by 40% on the same set.",
        "Runs 4x faster than the baseline.",
        "Review time fell from 30 days to 2 days.",
        "Scores 12 percentage points higher on SWE-bench.",
        "F1 0.92 vs 0.81 for the prior judge.",
        "Uses 60% fewer tokens per task.",
    ]
    no = [
        "Affects OpenSSL 3.0.x and 2.x before the patch.",
        "The startup raises $25M for agent security.",
        "Patch within 24 hours of disclosure.",
        "Ships a 128,000 tokens context window.",
        "802.1X authentication is bypassed.",
        "Present on 100% of installs.",
    ]
    for text in yes:
        assert b._MEASURED.search(text), text
    for text in no:
        assert not b._MEASURED.search(text), text


def test_no_proof_fails_even_with_pointers_and_a_goal():
    assert picked(learn_row("bare", takeaway="A thoughtful essay on evals.")) == []
    paper = learn_row("paper", takeaway="An essay.", url="https://arxiv.org/abs/2610.1")
    assert b.learning_picks([paper], LEARN, NOW)[1]["paper"]["proof"] == "arxiv.org"


def test_a_proof_host_page_that_is_not_the_work_is_not_proof():
    for url in (
        "https://github.com/acme/sdk/issues/4",
        "https://gist.github.com/a/1",
        "https://huggingface.co/pricing",
        "https://huggingface.co/blog/post",
        "https://arxiv.org/list/cs.CR/new",
    ):
        assert picked(learn_row("p", takeaway="An essay.", url=url)) == [], url
    repo = learn_row("repo", takeaway="An essay.", url="https://github.com/acme/sdk")
    assert picked(repo) == ["repo"]


def test_one_pointer_fails_even_with_proof_and_a_goal():
    assert picked(learn_row("lone", corroborators=[])) == []
    same = learn_row("same", corroborators=[{"url": "https://www.blog-a.example/x"}])
    assert picked(same) == []


def test_the_channel_that_brought_a_row_in_is_not_a_second_voice():
    curated = learn_row("cur", corroborators=[], curated_by="tldrsec")
    listed = learn_row("xl", corroborators=[], discovered_via="x-list", author="someone")
    assert picked(curated) == [] and picked(listed) == []


def test_a_vendor_and_its_own_repo_count_once():
    row = learn_row(
        "vendor",
        url="https://acme.com/blog/launch",
        corroborators=[{"url": "https://github.com/acme/sdk"}],
    )
    assert picked(row) == []
    row["corroborators"].append({"url": "https://news-b.example/acme"})
    assert picked(row) == ["vendor"]


def test_x_posts_count_by_author_and_shared_blog_hosts_by_subdomain():
    two_authors = learn_row(
        "x2",
        url="https://arxiv.org/abs/2610.2",
        corroborators=[{"url": "https://x.com/alice/status/1"}],
    )
    assert b.learning_picks([two_authors], LEARN, NOW)[1]["x2"]["pointers"] == 2
    same_author = learn_row(
        "x1",
        url="https://x.com/alice/status/1",
        corroborators=[{"url": "https://twitter.com/Alice/status/2"}],
    )
    assert picked(same_author) == []
    blogs = learn_row(
        "io",
        url="https://karpathy.github.io/post",
        corroborators=[{"url": "https://someone.github.io/reply"}],
    )
    assert b.learning_picks([blogs], LEARN, NOW)[1]["io"]["pointers"] == 2


def test_no_goal_match_fails_even_with_proof_and_pointers():
    assert picked(learn_row("off", domain_id="ps.appsec", title="A WAF bypass")) == []
    kw = learn_row("kw", domain_id="ps.appsec", title="Prompt caching cut our bill")
    assert b.learning_picks([kw], LEARN, NOW)[1]["kw"]["goals"] == ["Low-token harness"]


def test_news_held_unverified_stepless_old_and_excluded_rows_never_show():
    rows = [
        learn_row("news", lane="news"),
        learn_row("unverified", verified=False),
        learn_row("unchecked", verified=None),
        learn_row("no-step", actionable={}),
        learn_row("old", published="2026-09-01"),
        learn_row("taken"),
    ]
    assert b.learning_picks(rows, LEARN, NOW, exclude={"taken"}) == ([], {})
    assert picked(learn_row("vetted-news", lane="news", has_page=True)) == ["vetted-news"]


def test_capped_ranked_by_parties_and_never_topped_up():
    rows = [learn_row(f"r{i}") for i in range(5)]
    rows[3]["corroborators"].append({"url": "https://third.example/a"})
    got, _ = b.learning_picks(rows, LEARN, NOW)
    assert len(got) == 3 and got[0]["id"] == "r3"
    assert b.learning_picks([], LEARN, NOW) == ([], {})
    assert b.learning_picks(rows, {}, NOW) == ([], {})


def test_zero_settings_are_honoured_not_replaced_by_defaults():
    assert picked(learn_row("a"), learning={**LEARN, "max": 0}) == []
    lone = learn_row("lone", corroborators=[])
    assert picked(lone, learning={**LEARN, "min_pointers": 1}) == ["lone"]


def test_hacker_news_and_reddit_are_discussion_not_another_publisher():
    row = learn_row(
        "hn",
        corroborators=[
            {"url": "https://news.ycombinator.com/item?id=1"},
            {"url": "https://www.reddit.com/r/netsec/comments/a"},
        ],
    )
    assert picked(row) == []


def test_a_plain_appsec_cve_does_not_match_the_shipped_goals():
    import common as c

    goals = {**LEARN, "goals": c.load_config().learning["goals"]}
    cve = learn_row(
        "cve",
        domain_id="ps.appsec",
        title="Memory corruption exploit in libfoo leaks tokens",
        takeaway="Patched within 72 hours; cuts exposure by 90% once applied.",
    )
    assert picked(cve, learning=goals) == []
