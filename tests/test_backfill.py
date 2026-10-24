"""Backfill mode (issue #52): windowed ingest per source, window-relative
freshness, and what a backfill chunk does to the pools. No network: every
source's fetch is a recorded fixture or a fake. The ledger side (labelling,
caps, never the day's scan) is in test_budget_backfill.py; the shell side in
test_backfill_sh.py."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime

import aggregate
import common as c
import eval_recall as er
import ingest_conferences
import ingest_curator_links as icl
import ingest_ghsa
import ingest_github
import ingest_hn
import ingest_json_feeds as ijf
import ingest_sitemap
import paper_gate as pg
import pytest
import rerank
from conftest import make_entry
from test_ingest_curator_links import FIXTURES

# conftest pins the clock at 2026-07-15. This window ended 26 days before it
# and starts 44 days before it: past max_age_days (31), so a normal scan would
# call its items stale.
FROM, TO = "2026-06-01", "2026-06-19"


@pytest.fixture
def window(monkeypatch):
    monkeypatch.setenv(c.BACKFILL_FROM_ENV, FROM)
    monkeypatch.setenv(c.BACKFILL_TO_ENV, TO)
    return date.fromisoformat(FROM), date.fromisoformat(TO)


@pytest.fixture(autouse=True)
def normal_scan(monkeypatch):
    """No test inherits a window from the shell that runs the suite."""
    monkeypatch.delenv(c.BACKFILL_FROM_ENV, raising=False)
    monkeypatch.delenv(c.BACKFILL_TO_ENV, raising=False)


def rules() -> dict:
    return c.load_yaml(c.SOURCES_FILE)["classification"]


# --- The window itself ----------------------------------------------------------
@pytest.mark.parametrize(
    "frm,to,why",
    [
        ("2026-06-01", "", "two YYYY-MM-DD"),
        ("2026/06/01", "2026-06-08", "two YYYY-MM-DD"),
        ("2026-06-31", "2026-07-01", "day is out of range"),
        ("2026-06-08", "2026-06-01", "ends before it starts"),
        ("2026-07-10", "2026-07-16", "ends in the future"),
        ("2026-05-01", "2026-06-08", "spans over 31"),
    ],
)
def test_a_bad_window_fails_closed(frm, to, why):
    with pytest.raises(c.BackfillWindowError, match=why):
        c.parse_backfill_window(frm, to, date(2026, 7, 15))


def test_one_variable_alone_is_an_error_not_a_normal_scan(monkeypatch):
    monkeypatch.setenv(c.BACKFILL_FROM_ENV, FROM)
    with pytest.raises(c.BackfillWindowError):
        c.backfill_window()


def test_no_window_is_a_normal_scan():
    now = c.utcnow()
    assert c.backfill_window() is None
    assert c.freshness_now() == now
    since, until = c.ingest_window(31)
    assert until is None and (now - since).days == 31
    assert c.window_days(3) == ["2026-07-15", "2026-07-14", "2026-07-13"]
    assert c.in_backfill_window({"published": "2020-01-01"})  # no window: no filter


def test_a_window_bounds_ingest_and_moves_now_to_its_end(window):
    since, until = c.ingest_window(31)
    assert since == datetime(2026, 6, 1, tzinfo=UTC)
    assert until == datetime(2026, 6, 19, 23, 59, 59, tzinfo=UTC) == c.freshness_now()
    days = c.window_days(7)  # every day of the window, not the last week
    assert days[0] == TO and days[-1] == FROM and len(days) == 19
    assert c.in_ingest_window(datetime(2026, 6, 19, 23, 0, tzinfo=UTC), since, until)
    assert not c.in_ingest_window(datetime(2026, 6, 20, tzinfo=UTC), since, until)
    assert not c.in_ingest_window(datetime(2026, 5, 31, tzinfo=UTC), since, until)
    assert not c.in_ingest_window(None, since, until)


@pytest.mark.parametrize(
    "published,inside",
    [("2026-06-01", True), ("2026-06-19", True), ("2026-06-20", False), ("2026-06", False)],
)
def test_only_an_entry_dated_inside_the_window_is_in_it(window, published, inside):
    assert c.in_backfill_window({"published": published}) is inside
    assert not c.in_backfill_window({})  # undated can't be placed


# --- Staging and the pools -------------------------------------------------------
def cand(day: str, n: int) -> dict:
    return {
        "id": f"c{n}",
        "title": [
            "Kernel heap exploit chain",
            "Prompt injection in IDE agents",
            "Supply chain worm in npm",
        ][n - 1],
        "source_url": f"https://example.com/post-{n}",
        "published": day,
    }


def test_staging_judges_freshness_at_the_windows_end(sandbox, window):
    added = c.add_candidates([cand("2026-06-02", 1), cand("2026-06-25", 2), cand("2026-05-20", 3)])
    assert [x["id"] for x in added] == ["c1"]  # 43 days old, but inside the window


def test_a_normal_scan_still_drops_that_item_as_stale(sandbox):
    assert c.add_candidates([cand("2026-06-02", 1)]) == []


def pool_with(*entries: dict) -> None:
    pool = c.load_pool("ai-research")
    pool["entries"] = list(entries)
    c.save_pool("ai-research", pool)


def backfilled() -> dict:
    return make_entry(id="bf", date="2026-06-02", published="2026-06-02", source_url="https://a/bf")


def live_entry() -> dict:
    """An entry already on main, published after the window (2026-07-10)."""
    return make_entry(id="live", date="2026-07-10", published="2026-07-10",
                      source_url="https://a/live", title="A live story already ranked")  # fmt: skip


def stale_on_main() -> dict:
    """An entry on main that aged past max_age_days: a normal prune archives it."""
    return make_entry(id="old", date="2026-05-01", published="2026-05-01",
                      source_url="https://a/old", title="An old story due to age out")  # fmt: skip


@pytest.fixture
def on_main(monkeypatch):
    """Ids origin/main already holds; everything else is this run's merge."""
    monkeypatch.setattr(c, "main_entry_ids", lambda: {"live", "old"})


def test_a_backfill_rerank_keeps_what_it_merged_and_leaves_the_ranking_alone(
    sandbox, window, on_main
):
    pool_with(backfilled(), live_entry(), stale_on_main())
    out = rerank.rerank_pool("ai-research")
    by_id = {e["id"]: e for e in out["entries"]}
    assert set(by_id) == {"bf", "live"}  # this run's merge kept; main's prune as usual
    archived = [e["id"] for e in c.load_json(c.ARCHIVE_FILE, default=[])]
    assert archived == ["old"]
    # Scores are wall-clock: the post-window entry keeps its own newness (5 days
    # old), not the 100 a window-end clock would give it.
    wall = c.newness_score("2026-07-10", c.load_config().half_life_days, now=c.utcnow())
    assert by_id["live"]["scores"]["newness"] == wall < 100
    assert by_id["bf"]["scores"]["newness"] == c.newness_score(
        "2026-06-02", c.load_config().half_life_days, now=c.utcnow()
    )
    assert c.is_curated(by_id["bf"], c.load_config())


def test_a_normal_rerank_protects_nothing_extra(sandbox, on_main):
    pool_with(backfilled(), live_entry())
    out = rerank.rerank_pool("ai-research")
    assert [e["id"] for e in out["entries"]] == ["live"]  # bf is stale at the wall clock


def test_the_next_normal_rerank_archives_the_finding_vetted_and_keeps_news(
    sandbox, window, monkeypatch, on_main
):
    """Expected, not a bug: once the backfill PR merges, the next normal rerank
    ages a backfilled finding past max_age_days into the archive, still vetted
    and with its scores; news stays."""
    news = {**backfilled(), "id": "news", "source_url": "https://a/news"}
    news["editorial"] = {"promoted": True}
    pool_with(backfilled(), news)
    rerank.rerank_pool("ai-research")
    scored = {e["id"]: e["scores"] for e in c.load_pool("ai-research")["entries"]}
    monkeypatch.delenv(c.BACKFILL_FROM_ENV)  # the next run is a normal scan
    monkeypatch.delenv(c.BACKFILL_TO_ENV)
    rerank.rerank_pool("ai-research")
    archived = {e["id"]: e for e in c.load_json(c.ARCHIVE_FILE, default=[])}
    assert list(archived) == ["bf"]
    assert archived["bf"]["scores"] == scored["bf"]  # archived as scored, still vetted
    assert c.is_curated(archived["bf"], c.load_config())
    assert [e["id"] for e in c.load_pool("ai-research")["entries"]] == ["news"]


# --- Windowed ingest, per source --------------------------------------------------
def test_kev_takes_exactly_the_entries_added_in_the_window(window):
    since, until = c.ingest_window(31)
    data = {
        "vulnerabilities": [
            {"cveID": f"CVE-2026-{n}", "dateAdded": d, "vulnerabilityName": "X SQL injection"}
            for n, d in ((1, "2026-05-31"), (2, "2026-06-01"), (3, "2026-06-19"), (4, "2026-06-20"))
        ]
    }
    src = {"id": "kev_json:cisa", "name": "CISA KEV", "handle": "x"}
    got = ijf.kev_candidates(data, src, rules(), since, until)
    assert [x["kev"]["cveID"] for x in got] == ["CVE-2026-2", "CVE-2026-3"]


def test_hf_papers_are_asked_for_every_window_day_and_bounded(monkeypatch, window):
    asked = []

    def fetch(url, **params):
        asked.append(params["date"])
        return [
            {
                "paper": {
                    "id": f"2606.{params['date'][-2:]}001",
                    "title": "Prompt injection attacks on LLM agents",
                    "summary": "A jailbreak and prompt injection security study of agents.",
                    "publishedAt": params["date"],
                }
            }
        ]

    monkeypatch.setattr(ijf, "fetch_json", fetch)
    src = {"id": "hf_papers:daily", "name": "HF", "handle": "h"}
    monkeypatch.setattr(ijf.sr, "sources_of_type", lambda t: [src] if t == "hf_papers" else [])
    since, until = c.ingest_window(31)
    got = ijf.collect(rules(), since, ("prompt injection",), until)
    assert asked == c.window_days(pg.HF_LOOKBACK_DAYS) and len(asked) == 19
    assert got and all(FROM <= x["published"] <= TO for x in got)


def test_hf_drops_a_paper_published_after_the_window(window):
    since, until = c.ingest_window(31)
    item = {"paper": {"id": "2606.99", "title": "Prompt injection", "publishedAt": "2026-06-25"}}
    assert ijf.hf_candidates([item], {"id": "h", "name": "HF"}, rules(), since, (), until) == []


def test_ghsa_asks_the_api_for_each_window_day_and_the_windows_critical_ones(monkeypatch, window):
    queries = []

    def gh(args, timeout=60):
        queries.append(args[1])
        day = args[1].split("published=")[1][:10]
        return json.dumps(
            [
                {
                    "ghsa_id": f"GHSA-{day}-{len(queries)}",
                    "html_url": f"https://github.com/advisories/GHSA-{day}-{len(queries)}",
                    "summary": "Path traversal in a package",
                    "severity": "high",
                    "published_at": f"{day}T10:00:00Z",
                }
            ]
        )

    monkeypatch.setattr(ingest_ghsa, "run_gh", gh)
    cfg = {"ghsa": {"per_run": 5, "per_run_critical": 7}}
    got = ingest_ghsa.collect(cfg, rules(), None)
    per_day = [q for q in queries if "severity" not in q]
    assert len(per_day) == 19 and all("per_page=5&published=2026-06-" in q for q in per_day)
    assert queries[-1].endswith("per_page=7&severity=critical&published=2026-06-01..2026-06-19")
    assert len(got) == 20  # 43 days old, still fresh at the window's end


def test_ghsa_daily_query_is_unchanged(monkeypatch):
    calls = []
    monkeypatch.setattr(
        ingest_ghsa, "run_gh", lambda args, timeout=60: calls.append(args[1]) or "[]"
    )
    ingest_ghsa.fetch_advisories(20)
    assert calls == ["/advisories?type=reviewed&sort=published&direction=desc&per_page=20"]


def test_hn_bounds_created_at_on_both_sides(monkeypatch, window):
    assert ingest_hn.numeric_filters(10, 40, 20) == "created_at_i>=10,created_at_i<=20,points>=40"
    assert ingest_hn.numeric_filters(10) == "created_at_i>=10"  # daily: no upper bound
    seen = []
    monkeypatch.setattr(
        ingest_hn,
        "search_stories",
        lambda q, n, since, pts=0, until=None: seen.append((since, until)) or [],
    )
    ingest_hn.collect(
        {"hackernews": {"queries": ["llm security"], "top_stories": True}}, rules(), 3
    )
    since, until = c.ingest_window(31)
    assert seen == [(int(since.timestamp()), int(until.timestamp()))] * 2


def test_conferences_search_the_windows_submitted_dates(monkeypatch, window):
    q = ingest_conferences.search_query("USENIX Security", c.backfill_window())
    assert q == 'co:"USENIX Security" AND submittedDate:[202606010000 TO 202606192359]'
    assert ingest_conferences.search_query("NDSS") == 'co:"NDSS"'
    item = {
        "title": "Prompt injection attacks against LLM agents",
        "summary": "A security study of prompt injection.",
        "link": "http://arxiv.org/abs/2606.00001v1",
        "comment": "Accepted at USENIX Security 2026",
    }
    days = ("2026-05-31", "2026-06-05", "2026-06-25")
    monkeypatch.setattr(
        ingest_conferences,
        "search_venue",
        lambda v, n, w=None: [{**item, "published": d, "link": f"{item['link']}{d}"} for d in days],
    )
    got = ingest_conferences.collect({"conferences": {"venues": ["USENIX Security"]}}, rules(), 5)
    assert [x["published"] for x in got] == ["2026-06-05"]


ISSUE_DAYS = {"350": "2026-06-30", "349": "2026-06-10", "348": "2026-05-28", "126": "2022-01-01"}


def test_curator_takes_the_issues_published_in_the_window_and_stops_after(window):
    asked = []

    def fetch(url: str) -> str:
        asked.append(url)
        if url == er.TLDRSEC_SITEMAP:
            return (FIXTURES / "tldrsec_sitemap.xml").read_text()
        n = url.rsplit("-", 1)[1]
        return f'<script>{{"datePublished":"{ISSUE_DAYS[n]}T14:30:00.000Z"}}</script>'

    got = icl.window_issues(fetch, FROM, TO)
    assert [(u.rsplit("-", 1)[1], d) for u, d, _ in got] == [("349", "2026-06-10")]
    assert asked[-1].endswith("-348")  # first issue before the window: stop, #126 unread


def test_curator_collect_uses_the_window(monkeypatch, sandbox, window):
    seen = {}
    monkeypatch.setattr(icl, "window_issues", lambda f, s, u: seen.update(s=s, u=u) or [])
    icl.collect(lambda u: "", icl.settings(), rules())
    assert seen == {"s": FROM, "u": TO}


def rss_source() -> dict:
    return {
        "id": "rss:ex",
        "name": "Ex",
        "handle": "https://ex.com/feed",
        "domains": ["AI Security"],
    }


def test_rss_keeps_only_items_the_feed_still_carries_inside_the_window(monkeypatch, window):
    entries = [
        {"link": f"https://ex.com/{d}", "title": f"Prompt injection in agents {d}", "published": d}
        for d in ("2026-05-30", "2026-06-03", "2026-06-21")
    ]

    class Parsed:
        bozo = False

    Parsed.entries = entries
    monkeypatch.setattr(aggregate.feedparser, "parse", lambda *a, **k: Parsed())
    monkeypatch.setattr(
        aggregate.sr, "sources_of_type", lambda t: [rss_source()] if t == "rss" else []
    )
    monkeypatch.setattr(aggregate.pg, "curator_link_ids", lambda: set())
    since, until = c.ingest_window(31)
    got = aggregate.collect_rss(rules(), since, until=until)
    assert [x["published"] for x in got] == ["2026-06-03"]


def test_sitemap_fetches_from_the_windows_start_and_keeps_the_pages_own_date(monkeypatch, window):
    pages = {  # loc -> (lastmod, the page's own Published Time)
        "https://lab.ai/research/old": ("2026-05-01", "2026-05-01"),
        "https://lab.ai/research/rebuilt": ("2026-07-10", "2026-06-05"),
        "https://lab.ai/research/new": ("2026-07-10", "2026-07-02"),
    }
    monkeypatch.setattr(
        ingest_sitemap, "fetch_sitemap", lambda u: [(k, v[0]) for k, v in pages.items()]
    )
    fetched = []

    def body(url):
        fetched.append(url)
        return (
            f"Title: LLM agent prompt injection\nPublished Time: {pages[url][1]}T00:00:00Z\n\nbody"
        )

    monkeypatch.setattr(ingest_sitemap, "fetch_body", body)
    monkeypatch.setattr(ingest_sitemap.c, "write_raw", lambda i, t: None)
    src = {
        "id": "research_index:lab",
        "name": "Lab",
        "url": "https://lab.ai/research",
        "domains": ["AI Security"],
    }
    monkeypatch.setattr(ingest_sitemap.sr, "sources_of_type", lambda t: [src])
    since, until = c.ingest_window(31)
    got = ingest_sitemap.collect(rules(), since, until)
    assert "https://lab.ai/research/old" not in fetched  # lastmod before the window
    assert [x["source_url"] for x in got] == ["https://lab.ai/research/rebuilt"]


def test_github_searches_repos_created_in_the_window(monkeypatch, window):
    assert ingest_github.date_qualifier("2026-06-14") == "pushed:>2026-06-14"
    assert (
        ingest_github.date_qualifier("x", c.backfill_window()) == "created:2026-06-01..2026-06-19"
    )
    repo = {"fullName": "a/b", "url": "https://github.com/a/b", "createdAt": "2026-06-04T00:00:00Z",
            "updatedAt": "2026-07-14T00:00:00Z", "stargazersCount": 99}  # fmt: skip
    cand_ = ingest_github.repo_to_candidate(repo, {"domains": []}, False, 100, by_created=True)
    assert cand_["published"] == "2026-06-04"  # its creation, inside the window
    daily = ingest_github.repo_to_candidate(repo, {"domains": []}, False, 100)
    assert daily["published"] == "2026-07-14"


def test_paper_gate_reads_curator_ids_and_hf_days_relative_to_the_window(
    monkeypatch, sandbox, window
):
    c.save_json(pg.curator_links_file(), {"2606.1": "2026-06-10", "2607.1": "2026-07-14"})
    monkeypatch.setattr(pg, "curator_window_days", lambda: 14)
    assert pg.curator_link_ids() == {"2606.1", "2607.1"}  # since 06-05; no upper bound
    asked = []

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return []

    import requests

    monkeypatch.setattr(
        requests, "get", lambda url, params, **k: asked.append(params["date"]) or Resp()
    )
    pg.fetch_hf_daily()
    assert asked == c.window_days(pg.HF_LOOKBACK_DAYS)
