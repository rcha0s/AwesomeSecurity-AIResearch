"""Tests for the focus lane, the focus matcher and the weekly digest (ISA ISC-56)."""

from __future__ import annotations

from datetime import UTC, datetime

import briefing as b
import common as c
import focus
import generate_html as gh
import taxonomy
import weekly_digest as wd

NOW = "2026-10-20"
FOCUS = {
    "lane_min": 2,
    "lane_max": 4,
    "claim_changes_max": 3,
    "digest_days": 7,
    "areas": [
        {"id": "mcp", "name": "MCP security", "domains": ["ais.mcp-tools"], "keywords": ["mcp"]},
        {
            "id": "guard",
            "name": "Guardrails",
            "domains": ["ais.guardrails"],
            "keywords": ["agent control standard"],
        },
        {"id": "ins", "name": "Insurers", "domains": [], "keywords": ["naic", "insurer"]},
    ],
}


def row(rid, published, title="x", domain_id="ps.appsec", n_corr=0, composite=50, **over):
    corr = [{"url": f"https://o{i}.example/{rid}"} for i in range(n_corr)]
    return {
        "id": rid,
        "published": published,
        "updated": "",
        "corroborators": corr,
        "composite": composite,
        "title": title,
        "takeaway": "",
        "domain_id": domain_id,
        "url": f"https://example.com/{rid}",
        **over,
    }


def ids(rows):
    return [r["id"] for r in rows]


# --- the matcher ---------------------------------------------------------------


def test_a_domain_id_or_a_whole_word_keyword_matches():
    assert focus.areas(row("a", NOW, domain_id="ais.mcp-tools"), FOCUS) == ["mcp"]
    assert focus.areas(row("b", NOW, title="NAIC adopts a model bulletin"), FOCUS) == ["ins"]
    assert focus.areas(row("c", NOW, takeaway="The Agent Control Standard shipped"), FOCUS) == [
        "guard"
    ]


def test_keywords_match_whole_words_only_and_no_focus_matches_nothing():
    assert focus.areas(row("d", NOW, title="Snapcmp and mcpx are unrelated"), FOCUS) == []
    assert (
        focus.areas(row("e", NOW, title="Insurers win"), FOCUS) == []
    )  # whole words: "insurer" is not "insurers"
    assert focus.areas(row("f", NOW, domain_id="ais.mcp-tools"), {}) == []
    assert focus.names(["guard", "mcp", "gone"], FOCUS) == ["Guardrails", "MCP security"]


def test_every_configured_domain_id_is_in_the_taxonomy_and_the_seven_areas_exist():
    conf = c.load_config()
    tax = taxonomy.get()
    areas = conf.focus["areas"]
    assert len(areas) == 7
    for area in areas:
        for domain in area["domains"]:
            assert domain in tax.domains, f"{area['id']}: {domain} is not a taxonomy ID"
        assert area["domains"] or area["keywords"]
    assert 0 <= conf.focus["digest_weekday"] <= 6


# --- the lane ------------------------------------------------------------------


def lane_rows():
    return [
        row("cve-big", "2026-10-19", title="Router CVE-2026-1", n_corr=3, exploited=True),
        row("eff", "2026-10-19", title="Token cost cut", domain_id="air.cost-efficiency"),
        row("mcp-new", "2026-10-17", title="Server flaw", domain_id="ais.mcp-tools"),
        row("two-areas", "2026-10-15", title="MCP guardrail gap", domain_id="ais.guardrails"),
        row("acs", "2026-10-16", title="OWASP Agent Control Standard v0.1.0"),
        row("mcp-old", "2026-08-01", title="Old mcp thing"),
    ]


def test_focus_lane_ranks_matches_by_areas_then_newest_and_skips_the_rest():
    got, topped = b.focus_stories(lane_rows(), FOCUS, NOW, 7)
    assert ids(got) == ["two-areas", "mcp-new", "acs"] and not topped


def test_a_thin_week_is_topped_up_with_the_latest_earlier_matches():
    rows = [r for r in lane_rows() if r["id"] in ("mcp-new", "mcp-old", "cve-big")]
    got, topped = b.focus_stories(rows, FOCUS, NOW, 7)
    assert ids(got) == ["mcp-new", "mcp-old"] and topped
    assert b.focus_stories([r for r in rows if r["id"] == "cve-big"], FOCUS, NOW, 7) == ([], False)


def test_the_lane_leads_and_nothing_appears_twice_while_generic_items_still_show():
    rows = lane_rows()
    fp = gh.front_page(rows, [], NOW, 7, FOCUS)
    assert fp["focus_stories"] == ["two-areas", "mcp-new", "acs"]
    assert fp["biggest_stories"] == ["cve-big"]  # the generic CVE still shows, below
    assert "eff" in fp["top_stories"] and "eff" not in fp["biggest_stories"]
    lanes = [fp["focus_stories"], fp["biggest_stories"], fp["top_stories"]]
    flat = [i for lane in lanes for i in lane]
    assert len(flat) == len(set(flat))
    assert fp["focus_tags"]["two-areas"] == ["MCP security", "Guardrails"]


def test_a_focus_story_that_is_also_big_shows_in_the_focus_lane_only():
    rows = lane_rows() + [row("mcp-big", "2026-10-19", title="MCP RCE", n_corr=2, exploited=True)]
    fp = gh.front_page(rows, [], NOW, 7, FOCUS)
    assert "mcp-big" in fp["focus_stories"]
    assert "mcp-big" not in fp["biggest_stories"] + fp["top_stories"]


def test_without_a_focus_block_the_existing_lanes_are_unchanged():
    fp = gh.front_page(lane_rows(), [], NOW, 7)
    assert fp["focus_stories"] == [] and fp["focus_claim_changes"] == []
    assert fp["biggest_stories"] == ["cve-big"]


def claim(cid, title, added, **over):
    return {"id": cid, "status": "current", "title": title, "added_on": added, **over}


def test_focus_claim_changes_lead_and_leave_the_general_list():
    claims = [
        claim("mcp-claim", "MCP servers need Origin checks", "2026-10-18"),
        claim("generic", "Use a cache key", "2026-10-19"),
        claim("old-mcp", "Old MCP claim", "2026-08-01"),
    ]
    fp = gh.front_page([], claims, NOW, 7, FOCUS)
    assert [ch["claim"] for ch in fp["focus_claim_changes"]] == ["mcp-claim"]
    assert "mcp-claim" not in [ch["claim"] for ch in fp["claim_changes"]]
    assert "generic" in [ch["claim"] for ch in fp["claim_changes"]]


# --- OWASP ACS on the real data ------------------------------------------------


def test_the_real_acs_entry_reaches_the_focus_lane_the_week_it_shipped():
    """ACS (2026-09-01) sat in the archive, held. It is kept like news now, and the
    focus rules put it in the lane on the 2026-09-09 scan's front page."""
    conf = c.load_config()
    sources = c.load_sources_by_id()
    entries = [e for t in c.TOPICS for e in c.load_pool(t)["entries"]]
    acs = [e for e in entries if "2026 Top 10 for LLM Applications" in e.get("title", "")]
    assert acs, "ACS must be back in its pool (rerank keeps focus news)"
    assert c.is_news_story(acs[0], conf, sources)
    assert focus.matches(acs[0], conf.focus)
    rows = [
        r
        for r in (
            gh.build_payload(__import__("claims").load_ledger(), conf, "2026-10-29")["editorial"]
        )
        if b.last_activity(r) <= "2026-09-09"
    ]
    lane, _ = b.focus_stories(rows, conf.focus, "2026-09-09", 7)
    assert any("2026 Top 10 for LLM Applications" in r["title"] for r in lane)


# --- the weekly digest ---------------------------------------------------------


def test_digest_lists_only_the_window_with_title_takeaway_and_link():
    rows = [
        row(
            "a",
            "2026-10-18",
            title="MCP flaw [critical]",
            takeaway="Check Origin. More text.",
            domain_id="ais.mcp-tools",
        ),
        row("old", "2026-09-01", title="Old MCP", domain_id="ais.mcp-tools"),
        row("generic", "2026-10-19", title="Router CVE"),
    ]
    claims = [claim("mcp-claim", "MCP servers need Origin checks", "2026-10-19", statement="S.")]
    stories, changes = wd.pick(rows, claims, FOCUS, NOW)
    text = wd.render(stories, changes, claims, FOCUS, NOW)
    assert ids(stories) == ["a"]  # no top-up: the old one stays out
    assert "- [MCP flaw (critical)](https://example.com/a) - Check Origin." in text
    assert "(MCP security)" in text and "Old MCP" not in text and "Router CVE" not in text
    assert "Added: [MCP servers need Origin checks]" in text and "?claim=mcp-claim#claims" in text
    assert text == wd.render(stories, changes, claims, FOCUS, NOW)  # deterministic


def test_a_quiet_week_says_so():
    text = wd.render([], [], [], FOCUS, NOW)
    assert "Nothing new in your focus areas this week." in text
    assert "## Claim changes" not in text


def test_message_is_one_line_with_counts():
    assert wd.message(1, 0).startswith("Weekly focus digest: 1 story, 0 claim changes.")
    assert "\n" not in wd.message(5, 1)


def test_due_on_the_configured_weekday_with_an_env_override():
    sunday = datetime(2026, 10, 25, tzinfo=UTC)
    assert wd.is_due({"digest_weekday": 6}, sunday, override="")
    assert not wd.is_due({"digest_weekday": 0}, sunday, override="")
    assert wd.is_due({"digest_weekday": 0}, sunday, override="6")
    assert wd.is_due({"digest_weekday": 0}, sunday, override="any")
