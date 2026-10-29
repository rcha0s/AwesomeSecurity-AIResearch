"""Tests for scripts/ingest_x_list.py — the local-only X list lane.

The fixture is a recorded `interceptor read --text-only` of the list page and its
`interceptor links --json` (trimmed to public posts). No network, no Interceptor.
Fixture time: the newest post is 20 minutes old at NOW."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import common
import ingest_x_list as xl
import pytest
from conftest import make_entry

FIXTURES = Path(__file__).parent / "fixtures" / "x_list"
NOW = datetime(2026, 10, 29, 7, 25, 50, tzinfo=UTC)
HARNESS_ID = "2115700736084648177"  # theo, 20m: on-thesis (harness / MCP / skills)
NOTEBOOK_ID = "2115454036690510133"  # alphaXiv, 16h: on-thesis, a repost shown in the list
OLD_ID = "2115394340357116169"  # divagr1925, 20h in the list but off-thesis
TCO = "https://t.co/abc123"
ARTICLE = "https://example.org/harness-config-post?utm_source=x"


@pytest.fixture(autouse=True)
def pinned(monkeypatch):
    monkeypatch.setattr(common, "utcnow", lambda: NOW)


def page() -> str:
    return (FIXTURES / "page.txt").read_text()


def links(extra: bool = False) -> list[dict]:
    raw = (FIXTURES / "links.json").read_text()
    data = json.loads(raw[raw.index("{") :])["data"]
    if extra:  # the harness post links an article through t.co
        at = next(i for i, x in enumerate(data) if x["href"].endswith(f"/status/{HARNESS_ID}"))
        data.insert(at + 1, {"href": TCO, "text": "example.org/harness-config-post"})
    return data


def rules() -> dict:
    return common.load_yaml(common.SOURCES_FILE)["classification"]


def posts(extra: bool = False) -> list[xl.Post]:
    out = xl.parse_posts(page())
    xl.attach_links(out, links(extra))
    return out


def run(cfg_over: dict | None = None, extra: bool = False, resolve=None) -> dict:
    cfg = {**xl.DEFAULTS, **(cfg_over or {})}
    return xl.select(posts(extra), cfg, rules(), resolve or (lambda u: ARTICLE), dry=False)


# --- Parsing and dating --------------------------------------------------------
def test_parses_posts_with_their_status_ids():
    out = posts()
    assert [p.handle for p in out][:3] == ["askalphaxiv", "theo", "theo"]
    assert out[0].status_id == NOTEBOOK_ID and out[1].status_id == HARNESS_ID
    assert all(p.status_id for p in out)
    assert "Subscribe to Premium" not in " ".join(p.text for p in out)  # sidebar cut


def test_quoted_posts_fold_into_their_parent():
    parent = next(p for p in posts() if p.text.startswith("It's been amazing"))
    assert "[quoting @notsky]" in parent.text


def test_snowflake_gives_the_exact_post_time():
    assert xl.snowflake_time(HARNESS_ID).isoformat().startswith("2026-10-29T07:02:17")


def test_only_posts_from_the_last_24_hours_stage(sandbox):
    result = run()
    kept = {c["tweet_url"].rsplit("/", 1)[1] for c in result["candidates"]}
    assert HARNESS_ID in kept and NOTEBOOK_ID in kept
    assert all(
        (NOW - datetime.fromisoformat(c["x_posted_at"])).total_seconds() <= 24 * 3600
        for c in result["candidates"]
    )


def test_the_lookback_is_hard(sandbox):
    result = run({"lookback_hours": 10})  # the 16h-old post is now out
    kept = {c["tweet_url"].rsplit("/", 1)[1] for c in result["candidates"]}
    assert NOTEBOOK_ID not in kept and HARNESS_ID in kept
    assert result["counts"]["too-old"] >= 1


def test_a_repost_is_dated_by_the_original_post(sandbox, monkeypatch):
    """The time link of a reposted item is the original's status id."""
    monkeypatch.setattr(common, "utcnow", lambda: datetime(2026, 10, 30, 6, 0, tzinfo=UTC))
    result = run()  # 15h later: the 16h-old original is 31h old, though the repost is fresh
    kept = {c["tweet_url"].rsplit("/", 1)[1] for c in result["candidates"]}
    assert NOTEBOOK_ID not in kept


def test_undated_posts_are_dropped(sandbox):
    out = posts()
    out[1].status_id = None
    result = xl.select(out, xl.DEFAULTS, rules(), lambda u: None, dry=False)
    assert result["counts"]["undated"] == 1


def test_off_thesis_and_replies_do_not_stage(sandbox):
    counts = run()["counts"]
    assert counts["off-thesis"] >= 1 and counts["reply"] == 1
    assert counts["read"] == sum(v for k, v in counts.items() if k != "read")


# --- Article vs text -----------------------------------------------------------
def test_a_linked_article_is_the_citation(sandbox):
    result = run(extra=True)
    cand = next(c for c in result["candidates"] if c["tweet_url"].endswith(HARNESS_ID))
    assert cand["source_url"] == cand["article_url"] == "https://example.org/harness-config-post"
    assert cand["tweet_url"] == f"https://x.com/theo/status/{HARNESS_ID}"
    assert cand["raw_path"] is None
    assert cand["discovered_via"] == "x-list" and cand["source_id"] == "x:list"
    assert cand["author"] == "@theo"


def test_a_post_with_no_article_stages_its_own_text(sandbox):
    result = run()
    cand = next(c for c in result["candidates"] if c["tweet_url"].endswith(HARNESS_ID))
    assert cand["article_url"] is None and cand["source_url"] == cand["tweet_url"]
    raw = (common.ROOT / cand["raw_path"]).read_text()
    assert "harness configuration" in raw  # the same mechanism as add.py --text


def test_x_links_never_count_as_articles():
    post = xl.Post("a", "1m", "x", "1", ["https://x.com/i/article/1", "https://pic.twitter.com/z"])
    assert xl.article_for(post, lambda u: None) is None


def test_an_unresolvable_tco_falls_back_to_the_post_text(sandbox):
    cand = next(
        c
        for c in run(extra=True, resolve=lambda u: None)["candidates"]
        if c["tweet_url"].endswith(HARNESS_ID)
    )
    assert cand["article_url"] is None and cand["raw_path"]


def test_dedupes_against_pools(sandbox):
    common.save_json(
        common.POOL_FILES["ai-research"],
        {"entries": [make_entry(source_url=f"https://x.com/theo/status/{HARNESS_ID}")]},
    )
    result = run()
    assert result["counts"]["held"] == 1
    assert not any(c["tweet_url"].endswith(HARNESS_ID) for c in result["candidates"])


def test_the_candidate_cap(sandbox):
    result = run({"max_candidates": 1})
    assert len(result["candidates"]) == 1 and result["counts"]["over-cap"] >= 1


def test_dry_run_leaves_no_raw_files(sandbox):
    xl.select(posts(), xl.DEFAULTS, rules(), lambda u: None, dry=True)
    assert not list((common.RAW_DIR).glob("*.txt")) if common.RAW_DIR.exists() else True


# --- Refusals and soft failures ------------------------------------------------
@pytest.mark.parametrize("name", ["CI", "GITHUB_ACTIONS"])
def test_refuses_under_ci(name):
    with pytest.raises(xl.Skip, match="never runs in CI"):
        xl.check_runner({name: "true", "SCAN_RUNNER": "local"})


@pytest.mark.parametrize("runner", [None, "cloud", ""])
def test_refuses_off_the_local_runner(runner):
    env = {} if runner is None else {"SCAN_RUNNER": runner}
    with pytest.raises(xl.Skip, match="local"):
        xl.check_runner(env)


def test_main_skips_without_touching_interceptor(monkeypatch, capsys):
    monkeypatch.setenv("CI", "true")
    monkeypatch.setenv("SCAN_RUNNER", "local")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("ran a subprocess"))
    assert xl.main([]) == 0
    assert "skipped" in capsys.readouterr().out


def test_main_soft_fails_when_interceptor_is_missing(monkeypatch, capsys, sandbox):
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("SCAN_RUNNER", "local")
    monkeypatch.setattr(xl.shutil, "which", lambda name: None)
    assert xl.main([]) == 0
    assert "skipped (interceptor is not installed)" in capsys.readouterr().out
    assert common.load_candidates() == []


def test_main_soft_fails_when_the_profile_is_unavailable(monkeypatch, capsys, sandbox):
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("SCAN_RUNNER", "local")
    monkeypatch.setattr(xl.shutil, "which", lambda name: "/bin/interceptor")
    done = subprocess.CompletedProcess([], 1, stdout="", stderr="no context interceptor-test")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: done)
    assert xl.main([]) == 0
    assert "skipped (interceptor open unavailable" in capsys.readouterr().out


# --- Read-only enforcement -----------------------------------------------------
def test_the_verb_allowlist_is_read_only():
    assert xl.ALLOWED_VERBS == {"open", "read", "links", "scroll", "tab"}
    forbidden = ["click", "type", "act", "keys", "eval", "navigate", "select", "check", "drag"]
    for verb in forbidden:
        with pytest.raises(ValueError, match="not allowed"):
            xl.build_command(verb, [], xl.DEFAULTS, "1")


def test_scroll_and_tab_are_narrowed_and_pinned_to_our_tab():
    with pytest.raises(ValueError):
        xl.build_command("scroll", ["up"], xl.DEFAULTS, "1")
    with pytest.raises(ValueError):
        xl.build_command("tab", ["switch"], xl.DEFAULTS, "1")
    with pytest.raises(ValueError, match="own tab"):
        xl.build_command("scroll", ["down"], xl.DEFAULTS, None)  # never the active tab
    cmd = xl.build_command("scroll", ["down"], xl.DEFAULTS, "42")
    assert cmd[-2:] == ["--tab", "42"]
    assert cmd[cmd.index("--context") + 1] == "interceptor-test"
    assert cmd[cmd.index("--group") + 1] == "x-list"


def test_every_call_in_a_full_run_is_allowed_and_in_the_group(monkeypatch):
    """Drive collect() over a fake `interceptor` binary and check each argv."""
    calls: list[list[str]] = []
    reads = iter([page(), page(), page()])

    def fake_run(argv, **kw):
        calls.append(argv)
        verb = argv[1]
        if verb == "open":
            out = "Tab: 77 | https://x.com/i/lists/1\n"
        elif verb == "links":
            out = "[ab12cd34] → links\n" + json.dumps({"success": True, "data": links()})
        elif verb == "read":
            out = next(reads)
        else:
            out = "ok\nwarning: DOM has changed since last state read"
        return subprocess.CompletedProcess(argv, 0, stdout=out, stderr="")

    monkeypatch.setattr(xl.shutil, "which", lambda name: "/bin/interceptor")
    monkeypatch.setattr(subprocess, "run", fake_run)
    found = xl.read_list_posts(xl.DEFAULTS, NOW - timedelta(hours=24), sleep=lambda s: None)
    assert len(found) == 9
    verbs = [c[1] for c in calls]
    assert verbs[0] == "open" and verbs[-1] == "tab"
    assert set(verbs) <= xl.ALLOWED_VERBS
    for argv in calls:
        assert argv[argv.index("--context") + 1] == "interceptor-test"
        assert argv[argv.index("--group") + 1] == "x-list"
        assert argv[1] == "open" or argv[argv.index("--tab") + 1] == "77"
    opened = calls[0]
    assert opened[opened.index("--timeout") + 1] == "25000" and "--text-only" in opened


def test_an_empty_render_is_retried_once(monkeypatch):
    seen: list[str] = []
    state = {"reads": 0}

    def fake(verb, args, cfg, tab=None):
        seen.append(verb)
        if verb == "open":
            return "Tab: 5 | https://x.com/i/lists/1\nHome\nExplore"  # no posts yet
        if verb == "links":
            return json.dumps({"success": True, "data": links()})
        if verb == "read":
            state["reads"] += 1
            return page()
        return "ok"

    monkeypatch.setattr(xl, "interceptor", fake)
    found = xl.read_list_posts(xl.DEFAULTS, NOW - timedelta(hours=24), sleep=lambda s: None)
    # one retry read of the empty render, then one after the scroll that loads nothing new
    assert seen.count("read") == 2 and seen.count("scroll") == 1 and len(found) == 9
