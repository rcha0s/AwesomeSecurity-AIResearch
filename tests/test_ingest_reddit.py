"""Tests for scripts/ingest_reddit.py — the keyless subreddit lane. A recorded,
trimmed community-more-posts partial (tests/fixtures/reddit), no network."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import common
import ingest_reddit as ir
import merge_analysis as m
import pytest
import select_batch as sb
from conftest import make_entry

FIXTURE = Path(__file__).parent / "fixtures" / "reddit" / "netsec_new.html"
NOW = datetime(2026, 10, 29, 6, 0, tzinfo=UTC)
CFG = {**ir.DEFAULTS, "subreddits": ["netsec"], "sorts": ["new"], "delay_seconds": 0}


@pytest.fixture(autouse=True)
def clock(monkeypatch):
    monkeypatch.setattr(common, "utcnow", lambda: NOW)
    import requests

    def boom(*a, **k):
        raise AssertionError("ingest_reddit touched the network in a test")

    monkeypatch.setattr(requests, "get", boom)


def html() -> str:
    return FIXTURE.read_text()


def serve(text: str):
    return lambda sub, sort, cfg: text


def run(cfg=None, text=None):
    cfg = {**CFG, **(cfg or {})}
    stats: dict = {}
    posts = ir.read_all(serve(text or html()), cfg, stats)
    rules = common.load_yaml(common.SOURCES_FILE)["classification"]
    cands, selfposts = ir.select(posts, cfg, stats, rules)
    return stats, cands, selfposts


# --- attribute parsing --------------------------------------------------------------
def test_parser_reads_only_post_tags_and_unescapes_attributes():
    posts = ir.parse_posts(html())
    assert len(posts) == 11  # the overflow-menu element is not a post
    first = posts[0]
    assert first["score"] == "49" and first["comment-count"] == "2"
    assert first["post-type"] == "link" and first["subreddit-name"] == "netsec"
    assert first["content-href"].startswith("https://www.atredis.com/")
    assert first["created-timestamp"] == "2026-10-28T21:24:39.496000+0000"
    assert "&#39;" not in posts[1]["post-title"] and "Moldova's" in posts[1]["post-title"]


def test_normalize_classifies_link_text_and_reddit_hosted_links():
    by = {p["permalink"].split("/")[-2]: ir.normalize(p, "netsec") for p in ir.parse_posts(html())}
    text = by["how_do_you_triage_prompt_injection_reports"]
    assert text["kind"] == "text" and text["link"] is None
    assert text["permalink"].startswith("https://www.reddit.com/r/netsec/comments/")
    reddit_link = by["crosspost_of_a_thread_about_rce"]
    assert reddit_link["link"] is None  # a Reddit-hosted href is never an article
    atredis = by["turning_the_valve_exploiting_rce_and_lpe_in_the"]
    assert atredis["kind"] == "link" and atredis["score"] == 49 and atredis["comments"] == 2
    assert atredis["created"].utcoffset().total_seconds() == 0
    crosspost = next(p for k, p in by.items() if k.startswith("cache_me_if_you_can"))
    assert crosspost["kind"] == "other"  # a crosspost has no article of its own
    assert by["broken"] is None  # no timestamp: skipped


# --- window, filters, staging ---------------------------------------------------------
def test_stats_count_every_parsed_post_and_the_window_drops_old_ones():
    stats, cands, selfposts = run()
    assert stats["netsec"]["read"] == 10  # 11 parsed, one without a timestamp
    titles = [x["title"] for x in cands]
    assert not any("Old prompt injection" in t for t in titles)  # 9 days old, lookback is 48h
    assert not any("Low score prompt injection" in t for t in titles)
    assert not any("sourdough" in t for t in titles)  # off-thesis
    assert any("MCP servers" in t for t in titles) and any("MPass" in t for t in titles)
    assert not any("Valve" in t for t in titles)  # no taxonomy hint in its title


def test_lookback_hours_is_configurable():
    _, cands, _ = run({"lookback_hours": 24 * 30, "min_score": 0})
    assert any("Old prompt injection" in x["title"] for x in cands)


def test_a_link_post_stages_its_article_with_the_thread_as_signal():
    _, cands, _ = run()
    top = cands[0]  # best engagement first
    assert "MCP servers" in top["title"]
    assert top["source_url"] == "https://mcp.example.com/field-report"  # tracking param cleaned
    assert top["article_url"] == top["source_url"]
    assert not common.is_reddit_url(top["source_url"])
    assert top["discovered_via"] == "reddit"
    assert top["reddit_url"].startswith("https://www.reddit.com/r/netsec/comments/")
    assert (top["reddit_score"], top["reddit_comments"]) == (20, 5)
    assert top["source_id"] == "reddit:netsec"
    assert top["published"] == "2026-10-28"  # the post's own date


def test_a_self_post_is_signal_and_never_a_candidate():
    _, cands, selfposts = run()
    assert [p["title"] for p in selfposts] == [
        "How do you triage prompt injection reports from agents in production?"
    ]
    assert not any("triage prompt injection" in x["title"] for x in cands)
    assert not any(common.is_reddit_url(x["source_url"]) for x in cands)


def test_a_link_to_reddit_itself_is_never_staged():
    _, cands, selfposts = run()
    assert not any("Thread about an RCE" in x["title"] for x in cands)
    assert not any("Thread about an RCE" in p["title"] for p in selfposts)  # kind: other


def test_the_per_run_cap_keeps_the_best_engagement():
    _, all_cands, _ = run({"max_per_run": 99})
    _, capped, _ = run({"max_per_run": 1})
    assert len(all_cands) > 1 and [x["title"] for x in capped] == [all_cands[0]["title"]]


def test_top_and_new_are_deduplicated_by_thread():
    cfg = {**CFG, "sorts": ["new", "top"]}
    stats: dict = {}
    posts = ir.read_all(serve(html()), cfg, stats)
    assert stats["netsec"]["read"] == 20 and len(posts) == 10


def test_a_held_article_is_not_staged_again(sandbox):
    url = "https://mcp.example.com/field-report"
    entry = make_entry(source_url=url, article_url=url, title="Something else entirely")
    common.save_pool("ai-security", {**common.load_pool("ai-security"), "entries": [entry]})
    _, cands, _ = run()
    assert not any("mcp.example.com" in x["source_url"] for x in cands)


# --- main: writes, idempotence, soft failure --------------------------------------------
def test_main_stages_candidates_and_writes_the_gitignored_signal_file(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main([], fetch=serve(html())) == 0
    staged = common.load_candidates()
    assert staged and all(x["discovered_via"] == "reddit" for x in staged)
    rows = common.load_json(ir.signal_file())
    assert rows == [
        {
            "title": "How do you triage prompt injection reports from agents in production?",
            "permalink": "https://www.reddit.com/r/netsec/comments/1xsynth1/how_do_you_triage_prompt_injection_reports/",
            "score": 31, "comments": 22, "sub": "netsec",
            "created": "2026-10-28T21:24:39.496000+00:00",
        }
    ]  # fmt: skip
    assert ir.main([], fetch=serve(html())) == 0  # a rerun adds nothing
    assert len(common.load_candidates()) == len(staged)
    assert len(common.load_json(ir.signal_file())) == 1


def test_dry_run_writes_nothing(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main(["--dry-run"], fetch=serve(html())) == 0
    assert not common.load_candidates() and not ir.signal_file().exists()


def test_signal_rows_older_than_signal_days_are_dropped(sandbox):
    old = {"title": "t", "permalink": "p", "score": 1, "comments": 0, "sub": "x",
           "created": "2026-09-01T00:00:00+00:00"}  # fmt: skip
    common.save_json(ir.signal_file(), [old])
    ir.save_signal([], CFG)
    assert common.load_json(ir.signal_file()) == []


@pytest.mark.parametrize("status", ["403 Blocked", "429 Too Many Requests", "timeout"])
def test_a_failed_request_is_soft(sandbox, monkeypatch, capsys, status):
    monkeypatch.setattr(ir, "settings", lambda: CFG)

    def fail(sub, sort, cfg):
        raise RuntimeError(status)

    assert ir.main([], fetch=fail) == 0
    out = capsys.readouterr()
    assert "skipped" in out.err and status in out.err
    assert not common.load_candidates()


def test_an_unexpected_error_is_logged_and_exit_is_zero(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    monkeypatch.setattr(ir, "select", lambda *a: 1 / 0)
    assert ir.main([], fetch=serve(html())) == 0
    assert "failed soft" in capsys.readouterr().err


def test_garbage_html_yields_nothing(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main([], fetch=serve("<html><body>Blocked</body></html>")) == 0
    assert not common.load_candidates()


def test_a_backfill_run_skips_the_lane(sandbox, monkeypatch, capsys):
    from datetime import date

    monkeypatch.setattr(common, "backfill_window", lambda: (date(2026, 9, 1), date(2026, 9, 9)))
    assert ir.main([], fetch=serve(html())) == 0
    assert "skipped" in capsys.readouterr().out and not common.load_candidates()


def test_live_fetch_asks_once_per_sub_per_sort_with_a_browser_agent(monkeypatch):
    import requests

    seen = []

    class Resp:
        text = "<html></html>"

        def raise_for_status(self):
            pass

    def fake(url, params=None, headers=None, timeout=None):
        seen.append((url, params, headers["User-Agent"], timeout))
        return Resp()

    monkeypatch.setattr(requests, "get", fake)
    ir.fetch_html("netsec", "new", CFG)
    ir.fetch_html("netsec", "top", CFG)
    assert seen[0][0].endswith("/svc/shreddit/community-more-posts/new/")
    assert seen[0][1] == {"name": "netsec"} and seen[1][1] == {"name": "netsec", "t": "day"}
    assert seen[0][2].startswith("Mozilla/5.0") and seen[0][3] == CFG["timeout_seconds"]


def test_config_lists_the_five_subreddits_and_a_lookback():
    cfg = ir.settings()
    assert cfg["subreddits"] == ["netsec", "cybersecurity", "AI_Agents", "LLMDevs", "devsecops"]
    assert cfg["lookback_hours"] == 48 and cfg["sorts"][0] == "new"


# --- merge: a Reddit thread alone is never a finding ----------------------------------------
REDDIT_URL = "https://www.reddit.com/r/netsec/comments/1xsynth1/how_do_you_triage/"


def merged(sandbox, **over):
    conf = common.load_config()
    out, errors, _, _ = m.merge([make_entry(**over)], conf)
    assert not errors, errors
    return out[0]


def test_an_entry_whose_only_citation_is_reddit_is_held(sandbox):
    entry = merged(sandbox, source_url=REDDIT_URL, article_url=REDDIT_URL)
    assert entry["needs_review"] is True
    assert entry["citation_hold"] == m.REDDIT_ONLY_HOLD


def test_reddit_short_and_media_hosts_count_as_reddit(sandbox):
    for url in ("https://redd.it/1xsynth1", "https://old.reddit.com/r/x/comments/1/t/",
                "https://i.redd.it/a.png"):  # fmt: skip
        assert common.reddit_only({"source_url": url})


def test_an_entry_citing_an_article_as_well_is_not_held_for_reddit(sandbox):
    entry = merged(sandbox, source_url="https://example.com/post", article_url=REDDIT_URL)
    assert "citation_hold" not in entry
    corr = [{"url": "https://example.com/real"}]
    assert not common.reddit_only({"source_url": REDDIT_URL, "corroborating_sources": corr})
    assert not common.reddit_only({})


def test_merge_stamps_the_thread_fields_from_the_candidate():
    cands = [{"id": "c1", "source_url": "https://blog.example/rce", "source_id": "reddit:netsec",
              "reddit_url": REDDIT_URL, "reddit_score": 49, "reddit_comments": 2}]  # fmt: skip
    analyzed = [{"id": "x", "source_url": "https://blog.example/rce"}]
    assert m.stamp_curator(analyzed, cands) == 1
    assert analyzed[0]["reddit_url"] == REDDIT_URL and analyzed[0]["reddit_score"] == 49
    assert analyzed[0]["source_id"] == "reddit:netsec"


# --- batch + allowlist ------------------------------------------------------------------------
def test_reddit_is_its_own_batch_class():
    cand = {"source_id": "reddit:netsec", "discovered_via": "reddit"}
    assert sb.ingestor_class(cand) == "reddit"
    assert sb.ingestor_class({"source_id": "reddit:devsecops"}) == "reddit"


def test_the_scan_allowlist_names_reddit():
    import allowlist

    assert "www.reddit.com" in allowlist.FIXED_HOSTS
