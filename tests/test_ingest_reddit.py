"""Tests for scripts/ingest_reddit.py — the subreddit lane over Reddit's official API
(app-only OAuth). A recorded-shape listing (tests/fixtures/reddit), no network."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

import common
import ingest_reddit as ir
import merge_analysis as m
import pytest
import select_batch as sb
from conftest import make_entry

FIXTURE = Path(__file__).parent / "fixtures" / "reddit" / "netsec_new.json"
NOW = datetime(2026, 10, 29, 6, 0, tzinfo=UTC)
CFG = {**ir.DEFAULTS, "subreddits": ["netsec"], "sorts": ["new"], "delay_seconds": 0}
SECRET = "s3cr3t-value"
TRIAGE = "How do you triage prompt injection reports from agents in production?"


@pytest.fixture(autouse=True)
def clock(monkeypatch):
    monkeypatch.setattr(common, "utcnow", lambda: NOW)
    import requests

    def boom(*a, **k):
        raise AssertionError("ingest_reddit touched the network in a test")

    monkeypatch.setattr(requests, "get", boom)
    monkeypatch.setattr(requests, "post", boom)


def listing() -> dict:
    return json.loads(FIXTURE.read_text())


def items() -> list[dict]:
    return [ch["data"] for ch in listing()["data"]["children"] if ch["kind"] == "t3"]


def serve(data=None):
    data = items() if data is None else data
    return lambda sub, sort, cfg: data


def run(cfg=None, data=None):
    cfg = {**CFG, **(cfg or {})}
    stats: dict = {}
    posts = ir.read_all(serve(data), cfg, stats)
    rules = common.load_yaml(common.SOURCES_FILE)["classification"]
    cands, selfposts = ir.select(posts, cfg, stats, rules)
    return stats, cands, selfposts


# --- field mapping --------------------------------------------------------------------
def by_title() -> dict:
    return {p["title"]: ir.normalize(p, "netsec") for p in items()}


def test_normalize_maps_the_listing_fields():
    post = by_title()["Prompt injection in MCP servers: a field report"]
    assert post["kind"] == "link" and post["link"].startswith("https://mcp.example.com/")
    assert (post["score"], post["comments"]) == (20, 5)
    assert post["permalink"].startswith("https://www.reddit.com/r/netsec/comments/1s001/")
    assert post["created"] == datetime.fromtimestamp(post["created"].timestamp(), UTC)
    assert post["created"].isoformat() == "2026-10-28T21:24:39+00:00"


def test_normalize_classifies_self_reddit_hosted_and_broken_posts():
    posts = by_title()
    triage = posts[TRIAGE]
    assert triage["kind"] == "text" and triage["link"] is None and "dedupe" in triage["text"]
    assert posts["Thread about an RCE exploit chain"]["kind"] == "other"  # Reddit-hosted url
    assert posts["No timestamp prompt injection post"] is None


def test_the_listing_reader_keeps_only_posts(monkeypatch):
    import requests

    seen = {}

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return listing()

    def fake(url, params=None, headers=None, timeout=None):
        seen.update(url=url, params=params, headers=headers, timeout=timeout)
        return Resp()

    monkeypatch.setattr(requests, "get", fake)
    got = ir.fetch_listing("netsec", "top", CFG, "tok-123")
    assert len(got) == 11  # the t1 child is dropped
    assert seen["url"] == "https://oauth.reddit.com/r/netsec/top"
    assert seen["params"]["t"] == "day" and seen["timeout"] == CFG["timeout_seconds"]
    assert seen["headers"]["Authorization"] == "Bearer tok-123"
    assert seen["headers"]["User-Agent"] == ir.USER_AGENT
    assert "tok-123" not in seen["url"] and "tok-123" not in str(seen["params"])
    ir.fetch_listing("netsec", "new", CFG, "tok-123")
    assert "t" not in seen["params"]


# --- window, filters, staging ---------------------------------------------------------
def test_stats_count_every_valid_post_and_the_window_drops_old_ones():
    stats, cands, _ = run()
    assert stats["netsec"]["read"] == 10  # 11 posts, one without a timestamp
    titles = [x["title"] for x in cands]
    assert not any("Old prompt injection" in t for t in titles)  # 9 days old, lookback 48h
    assert not any("Low score" in t for t in titles)
    assert not any("sourdough" in t for t in titles)  # off-thesis
    assert any("MCP servers" in t for t in titles) and any("MPass" in t for t in titles)


def test_lookback_hours_is_configurable():
    _, cands, _ = run({"lookback_hours": 24 * 30, "min_score": 0})
    assert any("Old prompt injection" in x["title"] for x in cands)


def test_a_link_post_stages_its_article_with_the_thread_as_signal():
    _, cands, _ = run()
    top = cands[0]  # best engagement first
    assert "MCP servers" in top["title"]
    assert top["source_url"] == "https://mcp.example.com/field-report"  # tracking param cleaned
    assert top["article_url"] == top["source_url"]
    assert top["discovered_via"] == "reddit" and top["source_id"] == "reddit:netsec"
    assert top["reddit_url"].startswith("https://www.reddit.com/r/netsec/comments/1s001/")
    assert (top["reddit_score"], top["reddit_comments"]) == (20, 5)
    assert top["published"] == "2026-10-28"


def test_a_self_post_is_signal_and_never_a_candidate():
    _, cands, selfposts = run()
    assert [p["title"] for p in selfposts] == [TRIAGE, "Weekly discussion thread"]
    assert not any(p["title"] in {x["title"] for x in cands} for p in selfposts)
    assert not any(common.is_reddit_url(x["source_url"]) for x in cands)


def test_a_self_posts_body_counts_for_the_on_thesis_check():
    _, _, selfposts = run()
    assert "Weekly discussion thread" in [p["title"] for p in selfposts]  # title alone has no hint
    assert "Self post about sourdough" not in [p["title"] for p in selfposts]


def test_a_link_to_reddit_itself_is_never_staged():
    _, cands, selfposts = run()
    everything = [x["title"] for x in cands] + [p["title"] for p in selfposts]
    assert "Thread about an RCE exploit chain" not in everything


def test_the_per_run_cap_keeps_the_best_engagement():
    _, all_cands, _ = run({"max_per_run": 99})
    _, capped, _ = run({"max_per_run": 1})
    assert len(all_cands) > 1 and [x["title"] for x in capped] == [all_cands[0]["title"]]


def test_top_and_new_are_deduplicated_by_thread():
    cfg = {**CFG, "sorts": ["new", "top"]}
    stats: dict = {}
    posts = ir.read_all(serve(), cfg, stats)
    assert stats["netsec"]["read"] == 20 and len(posts) == 10


def test_a_held_article_is_not_staged_again(sandbox):
    url = "https://mcp.example.com/field-report"
    entry = make_entry(source_url=url, article_url=url, title="Something else entirely")
    common.save_pool("ai-security", {**common.load_pool("ai-security"), "entries": [entry]})
    _, cands, _ = run()
    assert not any("mcp.example.com" in x["source_url"] for x in cands)


# --- main: credentials, writes, idempotence, soft failure --------------------------------
def test_main_stages_candidates_and_writes_the_gitignored_signal_file(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main([], fetch=serve()) == 0
    staged = common.load_candidates()
    assert staged and all(x["discovered_via"] == "reddit" for x in staged)
    rows = common.load_json(ir.signal_file())
    assert [r["title"] for r in rows] == [TRIAGE, "Weekly discussion thread"]
    assert rows[0] == {
        "title": TRIAGE,
        "permalink": rows[0]["permalink"], "score": 31, "comments": 22, "sub": "netsec",
        "created": "2026-10-28T21:24:39+00:00",
    }  # fmt: skip
    assert ir.main([], fetch=serve()) == 0  # a rerun adds nothing
    assert len(common.load_candidates()) == len(staged)
    assert len(common.load_json(ir.signal_file())) == 2


def test_no_credentials_skips_the_lane_and_exits_zero(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    assert ir.main([]) == 0  # the autouse guard would fail on any request
    assert "skipped: no Reddit API credentials" in capsys.readouterr().out
    assert not common.load_candidates() and not ir.signal_file().exists()


def test_one_credential_alone_is_not_enough(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "id")
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    assert ir.credentials() is None


def test_the_token_request_uses_basic_auth_and_the_secret_stays_out_of_the_url(monkeypatch):
    import requests

    seen = {}

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"access_token": "tok-abc", "token_type": "bearer"}

    def fake(url, auth=None, data=None, headers=None, timeout=None):
        seen.update(url=url, auth=auth, data=data, headers=headers)
        return Resp()

    monkeypatch.setattr(requests, "post", fake)
    assert ir.get_token("cid", SECRET, CFG) == "tok-abc"
    assert seen["url"] == "https://www.reddit.com/api/v1/access_token"
    assert seen["auth"] == ("cid", SECRET) and seen["data"] == {"grant_type": "client_credentials"}
    assert seen["headers"]["User-Agent"] == "awesomesec-research/1.0"
    assert SECRET not in seen["url"]


def test_a_failed_token_request_is_soft_and_never_logs_the_secret(monkeypatch, capsys):
    import requests

    def fake(*a, **k):
        raise RuntimeError(f"401 for {SECRET}")  # even if a library echoed it

    monkeypatch.setattr(requests, "post", fake)
    monkeypatch.setenv("REDDIT_CLIENT_ID", "cid")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", SECRET)
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main([]) == 0
    out = capsys.readouterr()
    assert "token request failed" in out.err
    assert SECRET not in out.err and SECRET not in out.out


def test_make_fetch_binds_the_token_for_the_listing_calls(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "cid")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", SECRET)
    monkeypatch.setattr(ir, "get_token", lambda cid, secret, cfg: "tok-1")
    calls = []
    monkeypatch.setattr(
        ir, "fetch_listing", lambda sub, sort, cfg, tok: calls.append((sub, sort, tok)) or []
    )
    fetch = ir.make_fetch(CFG)
    fetch("netsec", "new", CFG)
    assert calls == [("netsec", "new", "tok-1")]


def test_dry_run_writes_nothing(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main(["--dry-run"], fetch=serve()) == 0
    assert not common.load_candidates() and not ir.signal_file().exists()


def test_signal_rows_older_than_signal_days_are_dropped(sandbox):
    old = {"title": "t", "permalink": "p", "score": 1, "comments": 0, "sub": "x",
           "created": "2026-09-01T00:00:00+00:00"}  # fmt: skip
    common.save_json(ir.signal_file(), [old])
    ir.save_signal([], CFG)
    assert common.load_json(ir.signal_file()) == []


@pytest.mark.parametrize("status", ["401 Unauthorized", "403 Blocked", "429 Too Many", "timeout"])
def test_a_failed_request_is_soft(sandbox, monkeypatch, capsys, status):
    monkeypatch.setattr(ir, "settings", lambda: CFG)

    def fail(sub, sort, cfg):
        raise RuntimeError(status)

    assert ir.main([], fetch=fail) == 0
    err = capsys.readouterr().err
    assert "skipped (RuntimeError)" in err and status not in err  # type only, not the message
    assert not common.load_candidates()


def test_an_unexpected_error_is_logged_and_exit_is_zero(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    monkeypatch.setattr(ir, "select", lambda *a: 1 / 0)
    assert ir.main([], fetch=serve()) == 0
    assert "failed soft" in capsys.readouterr().err


def test_an_empty_listing_yields_nothing(sandbox, monkeypatch):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    assert ir.main([], fetch=serve([])) == 0
    assert not common.load_candidates()


def test_a_backfill_run_skips_the_lane(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(common, "backfill_window", lambda: (date(2026, 9, 1), date(2026, 9, 9)))
    assert ir.main([], fetch=serve()) == 0
    assert "skipped" in capsys.readouterr().out and not common.load_candidates()


def test_config_lists_the_five_subreddits_and_a_lookback():
    cfg = ir.settings()
    assert cfg["subreddits"] == ["netsec", "cybersecurity", "AI_Agents", "LLMDevs", "devsecops"]
    assert cfg["lookback_hours"] == 48 and cfg["sorts"][0] == "new"


# --- merge: a Reddit thread alone is never a finding ----------------------------------------
REDDIT_URL = "https://www.reddit.com/r/netsec/comments/1xsynth1/how_do_you_triage/"


def merged(sandbox, **over):
    out, errors, _, _ = m.merge([make_entry(**over)], common.load_config())
    assert not errors, errors
    return out[0]


def test_an_entry_whose_only_citation_is_reddit_is_held(sandbox):
    entry = merged(sandbox, source_url=REDDIT_URL, article_url=REDDIT_URL)
    assert entry["needs_review"] is True
    assert entry["citation_hold"] == m.REDDIT_ONLY_HOLD


def test_reddit_short_and_media_hosts_count_as_reddit():
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
    assert sb.ingestor_class({"source_id": "reddit:netsec", "discovered_via": "reddit"}) == "reddit"
    assert sb.ingestor_class({"source_id": "reddit:devsecops"}) == "reddit"


def test_the_scan_allowlist_names_the_reddit_api_hosts():
    import allowlist

    assert {"www.reddit.com", "oauth.reddit.com"} <= set(allowlist.FIXED_HOSTS)


# --- the floor: no lane may show a Reddit-only entry ------------------------------------------
def _held_entry(**over):
    return make_entry(needs_review=True, **over)


def test_the_editorial_track_can_never_promote_a_reddit_only_entry():
    conf = common.load_config()
    assert common.editorial_eligible(_held_entry(), conf)  # control: eligible otherwise
    entry = _held_entry(source_url=REDDIT_URL, article_url=REDDIT_URL)
    assert not common.editorial_eligible(entry, conf)


def test_a_reddit_only_entry_is_never_a_finding_or_news():
    conf = common.load_config()
    ok = make_entry()
    assert common.is_curated(ok, conf)
    reddit = make_entry(source_url=REDDIT_URL, article_url=REDDIT_URL)
    assert not common.is_curated(reddit, conf)
    promoted = {"editorial": {"promoted": True}, "grounding_score": 1.0}
    assert common.is_news_story({**ok, **promoted}, conf, {})  # control
    assert not common.is_news_story({**reddit, **promoted}, conf, {})  # even if promoted
    assert not common.news_shown({**reddit, **promoted}, conf, {})
    assert not common.is_shown({**reddit, **promoted}, conf, {})


def test_a_reddit_only_news_brief_is_not_kept_or_shown():
    conf = common.load_config()
    brief = make_entry(news_brief={"tier": "news"}, source_url=REDDIT_URL, article_url=REDDIT_URL)
    assert common.is_news_brief(brief)
    assert not common.is_news_curated(brief, conf, {}, window=None)
    assert not common.is_news_story(brief, conf, {})
    assert not common.brief_kept(brief, conf, {})


def test_the_hold_is_judged_after_stamp_brief_rewrites_the_url(sandbox, monkeypatch):
    def rewrite(entry, note):
        entry["source_url"] = entry["article_url"] = REDDIT_URL

    monkeypatch.setattr(m, "stamp_brief", rewrite)
    monkeypatch.setattr(m, "news_tier_note", lambda raw, tiers: {})
    monkeypatch.setattr(m, "brief_problems", lambda raw, note: [])
    entry = merged(sandbox, brief=common.NEWS_BRIEF)
    assert entry["citation_hold"] == m.REDDIT_ONLY_HOLD and entry["needs_review"] is True


@pytest.mark.parametrize(
    "url",
    [
        "https://www.reddit.com./r/x",
        "https://REDDIT.COM./r/x",
        "https://i.reddituploads.com/x",
        "https://reddit.app.link/abc",
    ],
)
def test_more_reddit_spellings_count_as_reddit(url):
    assert common.is_reddit_url(url) and common.reddit_only({"source_url": url})


def test_lookalike_hosts_are_not_reddit():
    for url in (
        "https://notreddit.com/x",
        "https://reddit.com.evil.example/x",
        "https://example.com/reddit.com",
    ):
        assert not common.is_reddit_url(url)


def test_a_non_http_link_scheme_is_never_staged():
    for href in ("ftp://example.com/x", "javascript:alert(1)", "httpx://example.com"):
        post = {**items()[0], "url": href}
        assert ir.normalize(post, "netsec")["link"] is None


def test_log_lines_carry_the_type_and_status_not_the_message():
    class Err(Exception):
        response = type("R", (), {"status_code": 429})()

    assert ir.describe(Err("Bearer tok-123 in message")) == "Err HTTP 429"
    assert ir.describe(ValueError("x")) == "ValueError"


def test_a_failing_candidate_write_does_not_lose_the_signal_file(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(ir, "settings", lambda: CFG)
    monkeypatch.setattr(common, "add_candidates", lambda cands: 1 / 0)
    assert ir.main([], fetch=serve()) == 0
    assert "candidates not written (ZeroDivisionError)" in capsys.readouterr().err
    assert len(common.load_json(ir.signal_file())) == 2


# --- the merge gate refuses a shown Reddit-only row ---------------------------------------------
def test_the_gate_refuses_a_rendered_row_that_cites_only_reddit():
    import content_checks as cc

    row = {"id": "r1", "url": REDDIT_URL, "corroborators": [{"url": "https://redd.it/abc"}]}
    payload = {"findings": [row], "editorial": [{**row, "id": "r2"}]}
    assert cc.reddit_shown_problems(payload) == [
        f"{cc.REDDIT_SHOWN}: r1",
        f"{cc.REDDIT_SHOWN}: r2",
    ]
    assert cc.REDDIT_SHOWN == "reddit-only citation on a shown entry"
    ok = {**row, "corroborators": [{"url": "https://example.com/a"}]}
    other = {"id": "x", "url": "https://a.example/"}
    assert cc.reddit_shown_problems({"findings": [ok, other]}) == []
    assert cc.reddit_shown_problems({}) == []


def test_content_problems_refuse_a_page_showing_a_reddit_only_entry(tmp_path, monkeypatch):
    import generate_html as gh
    import test_merge_gate as tg

    row = {"id": "r1", "url": REDDIT_URL, "corroborators": []}
    page = gh.render({"findings": [row]}, "2026-10-20")
    root = tg._tree(tmp_path, page=page)
    monkeypatch.setattr(tg.gate, "main_ledger", lambda base: {"claims": [{"id": "a"}]})
    tg.no_main_history(monkeypatch)
    monkeypatch.setattr(tg.gate, "main_stories", lambda base: {})
    monkeypatch.setattr(tg.gate, "main_has_feed", lambda base: False)
    assert "reddit-only citation on a shown entry: r1" in tg.gate.content_problems("main", root)
