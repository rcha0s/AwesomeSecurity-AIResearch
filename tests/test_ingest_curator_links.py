"""Tests for scripts/ingest_curator_links.py — tl;dr sec curator links, staged with
the article as the citation. Recorded issue pages (trimmed to their headings and
paragraphs), no network."""

from __future__ import annotations

import json
from pathlib import Path

import common
import eval_recall as er
import ingest_curator_links as icl
import merge_analysis
import paper_gate as pg
import pytest
import story_ledger
from conftest import make_entry

FIXTURES = Path(__file__).parent / "fixtures" / "curator"
ISSUE_349 = "https://tldrsec.com/p/tldr-sec-349"
ISSUE_350 = "https://tldrsec.com/p/tldr-sec-350"
STAGED = [  # the lead, on-thesis, free story links of both recorded issues, newest first
    "Zero to Calc in Six Days: Inside XBOW’s Chrome Full Chain",
    "Grounded or Gamed? We Audited Our Own Cyber Benchmark",
    "What Is EntraGoat? A Deliberately Vulnerable Entra ID Simulation Environment",
    "AgentCorruption: How A Single Prompt Collapsed The Entire Cloud Security Model",
    "runZeroInc/sshamble",
    "Introducing CAIRN: Frontier tracking for AI-integrated malware",
    "Context Collapse, Part 3 - AI Worming through Word",
    "REA - Reverse Engineer Anything",
    "AI for Offensive Security: What Works, What Does Not, and How to Adopt It",
    "How DigitalOcean Manages Credentials for Autonomous Agents",
    "Test-driving Jev on a security task: identity resolution",
    "How XBOW Finds IDORs with High Accuracy and Low Noise",
    "HTTP/3 in Burp Suite - it’s time to find a bigger wordlist",
    "Graphalgo campaign spreads to Terraform providers and Go Modules",
    "Package Manager Sandboxing",
    "Where do detection ideas come from",
    "Vulnerability Discovery and Exploitation Trends in the AI Era",
    "$1 Million Sandbox Challenge Uncovers Linux Kernel Flaws",
    "Escaping SPACE: Part I",
]
SPONSORED = ("nudgesecurity.com", "wiz.io", "opal.dev")


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    import requests

    def boom(*a, **k):
        raise AssertionError("ingest_curator_links touched the network in a test")

    monkeypatch.setattr(requests, "get", boom)


class Recorded:
    """A fetch() over the recorded pages that logs every URL asked for."""

    def __init__(self):
        self.asked: list[str] = []

    def __call__(self, url: str) -> str:
        self.asked.append(url)
        if url == er.TLDRSEC_SITEMAP:
            return (FIXTURES / "tldrsec_sitemap.xml").read_text()
        return (FIXTURES / f"{url.rsplit('/', 1)[1]}.html").read_text()


def cfg(**over) -> dict:
    return {**icl.settings(), **over}


def rules() -> dict:
    return common.load_yaml(common.SOURCES_FILE)["classification"]


def run(**over) -> dict:
    return icl.collect(Recorded(), cfg(**over), rules())


def titles(result: dict) -> list[str]:
    return [cand["title"] for cand in result["candidates"]]


def issue(n: int) -> str:
    return (FIXTURES / f"tldr-sec-{n}.html").read_text()


# --- Fetching -----------------------------------------------------------------
def test_reads_the_sitemap_then_only_issues_inside_the_window(sandbox):
    """By issue number, never lastmod: #126 (2022) carries a fresh lastmod and the
    newest issues a 2025 bulk-touch one, as on the live sitemap."""
    fetch = Recorded()
    result = icl.collect(fetch, cfg(), rules())
    assert fetch.asked == [er.TLDRSEC_SITEMAP, ISSUE_350, ISSUE_349]  # newest 2; not #126
    assert result["counts"]["issues"] == 2  # staged despite their old bulk lastmod
    one = Recorded()
    icl.collect(one, cfg(max_issues=1), rules())
    assert one.asked == [er.TLDRSEC_SITEMAP, ISSUE_350]


def test_the_window_is_judged_by_the_issues_own_publish_date(sandbox):
    result = run(lookback_days=3)  # since 2026-07-12: #349 (published 07-08) is out
    assert list(result["per_issue"]) == [ISSUE_350]
    assert {x["curator_issue"] for x in result["candidates"]} == {ISSUE_350}


def test_live_fetch_is_held_to_the_curator_hosts():
    with pytest.raises(ValueError, match="not a curator host"):
        er.http_get("https://labs.zenity.io/post/agentcorruption")


def test_settings_come_from_sources_yaml():
    s = icl.settings()
    assert s["lookback_days"] == 14 and s["max_issues"] == 2 and s["source_rank"] == 70.0
    assert "link.springer.com" in s["paywall_hosts"] and "archive.is" in s["paywall_hosts"]


def test_the_staged_rank_is_the_configured_one(sandbox):
    assert {x["source_rank"] for x in run(source_rank=55.0)["candidates"]} == {55.0}


def test_an_issue_page_without_a_publish_date_is_skipped(capsys):
    pages = {er.TLDRSEC_SITEMAP: (FIXTURES / "tldrsec_sitemap.xml").read_text(),
             ISSUE_350: issue(350).replace('"datePublished"', '"dateModified"'),
             ISSUE_349: issue(349)}  # fmt: skip
    got = er.tldrsec_issues(pages.__getitem__, "2026-07-01")
    assert [(u, d) for u, d, _ in got] == [(ISSUE_349, "2026-07-08")]
    assert "tldr-sec-350 has no publish date" in capsys.readouterr().err


@pytest.mark.parametrize(
    "page,day",
    [
        ('<script>{"datePublished":"2026-10-15T14:30:00.000Z"}</script>', "2026-10-15"),
        ('<meta property="article:published_time" content="2026-10-08T14:30:00Z">', "2026-10-08"),
        ('<meta content="2026-10-01T00:00:00Z" property="article:published_time"/>', "2026-10-01"),
        ('<meta property="og:updated_time" content="2026-10-20">', None),
        ("", None),
    ],
)
def test_issue_published_reads_the_pages_own_date(page, day):
    assert er.issue_published(page) == day


def test_the_newest_issues_are_picked_by_number_not_lastmod():
    xml = (FIXTURES / "tldrsec_sitemap.xml").read_text()
    assert er.parse_tldrsec_sitemap(xml, 3) == [ISSUE_350, ISSUE_349,
                                                "https://tldrsec.com/p/tldr-sec-348"]  # fmt: skip
    assert er.parse_tldrsec_sitemap(xml, 0) == []


# --- The shared parser ----------------------------------------------------------
def test_sponsor_blocks_and_paid_links_are_not_headlines():
    for n in (349, 350):
        urls = [it["url"] for it in er.parse_tldrsec_issue(issue(n), "2026-07-15")]
        assert urls and not [u for u in urls if any(s in u for s in SPONSORED)]


@pytest.mark.parametrize(
    "url,paid",
    [
        ("https://a.example/x?utm_source=tldrsec.com&utm_medium=referral", False),
        ("https://a.example/x", False),
        ("https://a.example/x?utm_source=tldrsec.com", False),
        ("https://a.example/x?utm_source=tldrsec&utm_medium=cpc", True),
        ("https://a.example/x?utm_medium=sponsored&utm_source=tldr", True),
        ("https://a.example/x?utm_source=tldrsec&utm_medium=paid-email", True),
        ("https://a.example/x?utm_source=tldrsec&utm_medium=newsletter", True),
    ],
)
def test_is_sponsored_reads_the_utm_medium(url, paid):
    assert er.is_sponsored(url) is paid


def mini_issue(*paras: str, heading: str = "AI + Security") -> str:
    return f"<h2>{heading}</h2>" + "".join(f"<p>{p}</p>" for p in paras) + "<h2>Misc</h2>"


def story(url: str, title: str, blurb: str = "about prompt injection in AI agents") -> str:
    return f'<a href="{url}?utm_source=tldrsec.com&amp;utm_medium=referral">{title}</a> {blurb}'


def test_a_sponsor_heading_skips_its_section_even_with_referral_links():
    page = mini_issue(
        story("https://vendor.example/demo", "Agent security demo portal"),
        heading="\N{WHITE RIGHT POINTING BACKHAND INDEX} Explore the demo portal "
        "\N{WHITE LEFT POINTING BACKHAND INDEX}",
    )
    assert er.parse_tldrsec_issue(page, "2026-07-15") == []
    assert len(er.parse_tldrsec_issue(page.replace("\N{WHITE LEFT POINTING BACKHAND INDEX}", ""),
                                      "2026-07-15")) == 1  # fmt: skip


def test_lead_marks_headlines_and_not_follow_on_paragraphs():
    items = {it["title"]: it for it in er.parse_tldrsec_issue(issue(350), "2026-07-15")}
    assert items["Context Collapse, Part 3 - AI Worming through Word"]["lead"] is True
    quorum = items["The Closed Quorum: Inside the first reported autonomous AI C2 implant"]
    assert quorum["lead"] is False  # "CAIRN's initial findings reveal ..." links to it
    assert items["REA - Reverse Engineer Anything"]["section"] == "red team"


# --- Staging --------------------------------------------------------------------
def test_stages_the_lead_on_thesis_links_of_both_issues(sandbox):
    result = run()
    assert titles(result) == STAGED
    counts = result["counts"]
    assert counts["issues"] == 2 and counts["staged"] == len(STAGED)
    assert counts["follow-on"] >= 3 and counts["off-thesis"] >= 1
    assert result["per_issue"][ISSUE_350]["staged"] == 11
    assert sum(n["links"] for n in result["per_issue"].values()) == counts["links"]


def test_a_candidate_cites_the_article_not_the_newsletter(sandbox):
    cand = next(x for x in run()["candidates"] if x["title"].startswith("AgentCorruption"))
    assert cand["article_url"] == cand["source_url"]
    assert cand["source_url"].startswith("https://labs.zenity.io/post/agentcorruption")
    assert "tldrsec" not in cand["source_url"] and "utm_" not in cand["source_url"]
    assert cand["source_id"] == "curator:tldrsec" and cand["curated_by"] == "tldrsec"
    assert cand["curator_issue"] == ISSUE_350 and cand["discovered_via"] == "curator"
    assert cand["published"] == "2026-07-15"  # the issue's sitemap date
    assert "AWS Bedrock" in cand["excerpt"]  # the curator's blurb
    assert cand["guess_topic"] in common.TOPICS and cand["guess_domain"]
    assert cand["source_rank"] == 70.0  # sources.yaml curator_links.source_rank, not a registry row


def test_off_thesis_links_are_not_staged(sandbox):
    result = run()
    off = "Navier-Stokes lost in translation"
    assert any(it["title"].startswith(off) for it in er.parse_tldrsec_issue(issue(349), "x"))
    assert not [t for t in titles(result) if t.startswith(off)]


def test_an_excluded_term_or_a_denylist_hit_drops_a_link(sandbox, monkeypatch):
    import taxonomy as tx

    real = tx.get()
    excluded = real.__class__(**{**real.__dict__, "excluded_terms": ("entra id",)})
    monkeypatch.setattr(tx, "get", lambda: excluded)
    assert "What Is EntraGoat?" not in " ".join(titles(run()))
    monkeypatch.setattr(tx, "get", lambda: real)
    monkeypatch.setattr(common, "news_denylist_hit", lambda e: "REA" in e["title"])
    assert "REA - Reverse Engineer Anything" not in titles(run())


def test_on_thesis_needs_a_taxonomy_hint(sandbox):
    tax = __import__("taxonomy").get()
    lead = {"lead": True, "href": "https://a.example/x", "text": ""}
    keep = {**lead, "title": "Prompt injection in a coding agent"}
    off = {**lead, "title": "My favourite sourdough recipe"}
    assert icl.keep(keep, tax, ()) is None
    assert icl.keep(off, tax, ()) == "off-thesis"
    assert icl.keep({**keep, "lead": False}, tax, ()) == "follow-on"


def test_paywalled_hosts_are_never_staged(sandbox):
    result = run(paywall_hosts=("semperis.com", "zenity.io"))
    assert "paywall" in result["counts"]
    assert not [t for t in titles(result) if "EntraGoat" in t or "AgentCorruption" in t]
    assert icl.host_in("https://www.link.springer.com/a", ("link.springer.com",))
    assert not icl.host_in("https://notspringer.com/a", ("springer.com",))


# --- Dedupe ---------------------------------------------------------------------
def held_by_pool(url: str, title: str = "Unrelated pool finding about kittens") -> None:
    pool = common.load_pool("ai-security")
    pool["entries"].append(
        make_entry(topic="ai-security", domain="ais.agent-security", title=title,
                   source_url=url, article_url=url)
    )  # fmt: skip
    common.save_pool("ai-security", pool)


def test_a_story_already_in_a_pool_is_not_staged(sandbox):
    held_by_pool("https://www.labs.zenity.io/post/agentcorruption-how-a-single-prompt-"
                 "collapsed-the-entire-cloud-security-model/?utm_source=x")  # fmt: skip
    result = run()
    assert result["counts"]["held"] == 1
    assert not [t for t in titles(result) if t.startswith("AgentCorruption")]


def test_a_story_in_the_archive_is_not_staged(sandbox):
    common.save_json(
        common.ARCHIVE_FILE,
        [make_entry(title="Old", source_url="https://rea.tools/", article_url="https://rea.tools")],
    )
    assert "REA - Reverse Engineer Anything" not in titles(run())


def test_a_story_in_the_story_ledger_is_not_staged(sandbox):
    ledger = story_ledger.empty_ledger()
    ledger["stories"]["s-1"] = {
        "title": "x", "entities": [], "first_seen": "2026-07-01", "last_updated": "2026-07-01",
        "entry_ids": [], "updates": [],
        "sources": [{"url": "https://specterops.io/blog/2026/09/24/ai-for-offensive-security"}],
    }  # fmt: skip
    story_ledger.save_ledger(ledger)
    assert not [t for t in titles(run()) if t.startswith("AI for Offensive Security")]


def test_a_near_identical_title_is_held(sandbox):
    held_by_pool("https://elsewhere.example/p", "Package Manager Sandboxing")
    assert "Package Manager Sandboxing" not in titles(run())


def test_the_same_link_in_two_issues_is_staged_once(sandbox, monkeypatch):
    same = issue(350)
    fetch = Recorded()
    monkeypatch.setattr(
        er, "tldrsec_issues", lambda f, since, newest: [(ISSUE_349, "2026-07-08", same),
                                                (ISSUE_350, "2026-07-15", same)]
    )  # fmt: skip
    result = icl.collect(fetch, cfg(), rules())
    assert len(titles(result)) == len(set(titles(result))) == 11


def two_issues(monkeypatch, first: str, second: str) -> list[str]:
    pages = [(ISSUE_349, "2026-07-08", first), (ISSUE_350, "2026-07-15", second)]
    monkeypatch.setattr(er, "tldrsec_issues", lambda f, since, newest: pages)
    return titles(icl.collect(Recorded(), cfg(), rules()))


def test_one_url_under_two_headlines_is_staged_once(sandbox, monkeypatch):
    url = "https://blog.example/agent-hijack"
    staged = two_issues(
        monkeypatch,
        mini_issue(story(url, "Agent hijack via poisoned tool output")),
        mini_issue(story(url, "Zero-click exfiltration from a coding agent")),
    )
    assert staged == ["Agent hijack via poisoned tool output"]


def test_one_headline_at_two_urls_is_staged_once(sandbox, monkeypatch):
    title = "Agent hijack via poisoned tool output"
    staged = two_issues(
        monkeypatch,
        mini_issue(story("https://blog.example/a", title)),
        mini_issue(story("https://mirror.example/b", title)),
    )
    assert staged == [title]


def test_a_story_held_as_a_corroborating_source_is_not_staged(sandbox):
    held_by_pool("https://other.example/x")
    pool = common.load_pool("ai-security")
    pool["entries"][0]["corroborating_sources"] = [{"url": "https://rea.tools/"}]
    common.save_pool("ai-security", pool)
    assert "REA - Reverse Engineer Anything" not in titles(run())


def test_main_stages_once_and_a_rerun_adds_nothing(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(er, "http_get", Recorded())
    assert icl.main([]) == 0
    staged = common.load_candidates()
    assert [x["title"] for x in staged] == STAGED
    assert icl.main([]) == 0
    assert len(common.load_candidates()) == len(STAGED)
    assert "Staged 0 new candidate(s)" in capsys.readouterr().out


def test_dry_run_writes_nothing_and_reports_recall_misses_it_would_stage(
    sandbox, monkeypatch, capsys
):
    monkeypatch.setattr(er, "http_get", Recorded())
    recall = sandbox / "recall.json"
    misses = [
        {"curator": "tldrsec", "title": "REA", "url": "https://rea.tools"},
        {"curator": "tldrsec", "title": "Quorum", "url": "https://blog.talosintelligence.com/"
         "the-closed-quorum-inside-the-first-reported-autonomous-ai-c2-implant"},
    ]  # fmt: skip
    recall.write_text(json.dumps({"misses": misses}))
    assert icl.main(["--dry-run", "--misses", str(recall)]) == 0
    out = capsys.readouterr().out
    assert "Recall misses this would stage: 1" in out and "[tldrsec] REA" in out
    assert f"{ISSUE_350}: 12 story links, 11 staged" in out
    assert common.load_candidates() == [] and not pg.curator_links_file().exists()


# --- Paper gate -----------------------------------------------------------------
def test_arxiv_links_in_an_issue_become_the_curator_signal(sandbox, monkeypatch):
    monkeypatch.setattr(er, "http_get", Recorded())
    icl.main([])
    assert json.loads(pg.curator_links_file().read_text()) == {"2610.08144": "2026-07-08"}
    ids = pg.curator_link_ids()
    paper = {"article_url": "https://arxiv.org/abs/2610.08144v2"}
    assert pg.admit(paper, pg.Signals(hf_ids=set(), curator_ids=ids)) == (True, "curator-link")
    other = {"article_url": "https://arxiv.org/abs/2610.99999"}
    assert pg.admit(other, pg.Signals(hf_ids=set(), curator_ids=ids))[0] is False


def test_an_old_or_missing_curator_signal_vouches_for_nothing(sandbox):
    assert pg.curator_link_ids() == set()
    pg.save_curator_link_ids({"2601.00001": "2026-05-01", "2607.00002": "2026-07-10"})
    assert pg.curator_link_ids() == {"2607.00002"}


def test_aggregate_seeds_the_gate_with_curator_links(sandbox, monkeypatch):
    import aggregate

    pg.save_curator_link_ids({"2607.00002": "2026-07-10"})
    monkeypatch.setattr(aggregate.sr, "sources_of_type", lambda t: [])
    signals = pg.Signals(hf_ids=set())
    aggregate.collect_rss({}, common.utcnow(), signals)
    assert "2607.00002" in signals.curator_ids


# --- Provenance reaches the pool --------------------------------------------------
def test_merge_stamps_curator_provenance_from_the_candidate():
    cands = [
        {"id": "c1", "source_url": "https://rea.tools/", "curated_by": "tldrsec",
         "curator_issue": ISSUE_350, "source_id": "curator:tldrsec"},
        {"id": "c2", "source_url": "https://b.example/", "source_id": "rss:b"},
    ]  # fmt: skip
    analyzed = [
        {"id": "other-id", "source_url": "https://rea.tools"},  # matched by URL
        {"id": "c2", "source_url": "https://b.example/"},
        "not-a-dict",
    ]
    assert merge_analysis.stamp_curator(analyzed, cands) == 1
    assert analyzed[0]["curated_by"] == "tldrsec" and analyzed[0]["curator_issue"] == ISSUE_350
    assert analyzed[0]["source_id"] == "curator:tldrsec"
    assert "curated_by" not in analyzed[1]


def test_merge_stamps_by_article_url_or_raw_path_and_logs_the_rest(capsys):
    base = {"curated_by": "tldrsec", "curator_issue": ISSUE_350, "source_id": "curator:tldrsec"}
    cands = [
        {**base, "id": "a", "title": "By article", "source_url": "https://x.example/1",
         "article_url": "https://art.example/1"},
        {**base, "id": "b", "title": "By raw", "source_url": "https://x.example/2",
         "raw_path": "data/_raw/b.txt"},
        {**base, "id": "c", "title": "Never analyzed", "source_url": "https://x.example/3"},
    ]  # fmt: skip
    analyzed = [
        {"id": "e1", "source_url": "https://other.example/1", "article_url": "https://art.example/1/"},
        {"id": "e2", "source_url": "https://other.example/2", "raw_path": "data/_raw/b.txt"},
    ]  # fmt: skip
    assert merge_analysis.stamp_curator(analyzed, cands) == 2
    assert all(e["curated_by"] == "tldrsec" for e in analyzed)
    err = capsys.readouterr().err
    assert "left unstamped (not analyzed): Never analyzed" in err and "By raw" not in err
