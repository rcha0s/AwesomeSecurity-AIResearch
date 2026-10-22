"""Tests for scripts/add_source.py — type resolution, feed discovery, signals."""

from __future__ import annotations

import argparse

import add_source as a
import sources_registry as sr


def ns(**kw):
    return argparse.Namespace(**kw)


def test_deactivate_sets_one_source_inactive_and_keeps_its_row(sandbox, capsys):
    import common

    raw = [
        {"id": "rss:dead", "type": "rss", "handle": "https://d.example/feed", "active": True,
         "rank": 80.0, "stats": {"ingested": 3, "curated": 1}},
        {"id": "rss:live", "type": "rss", "handle": "https://l.example/feed", "active": True},
    ]  # fmt: skip
    common.save_json(sr.REGISTRY_FILE, raw)
    common.save_json(sr.STATS_FILE, {"rss:dead": {"ingested": 9, "curated": 9}})
    assert a.main(["deactivate", "rss:dead", "--reason", "feed 404s"]) == 0
    saved = common.load_json(sr.REGISTRY_FILE)
    assert saved[0] == {**raw[0], "active": False, "deactivated": "2026-07-15",
                        "deactivated_reason": "feed 404s"}  # fmt: skip
    assert saved[1] == raw[1]  # untouched, and stats were not baked into the registry
    assert [s["id"] for s in sr.sources_of_type("rss")] == ["rss:live"]
    assert "Deactivated rss:dead" in capsys.readouterr().out


def test_deactivate_refuses_an_unknown_id_or_an_empty_reason(sandbox, capsys):
    import common

    common.save_json(sr.REGISTRY_FILE, [{"id": "rss:x", "type": "rss", "active": True}])
    assert a.main(["deactivate", "rss:nope", "--reason", "gone"]) == 1
    assert a.main(["deactivate", "rss:x", "--reason", "  "]) == 1
    assert common.load_json(sr.REGISTRY_FILE)[0]["active"] is True
    assert "no registered source" in capsys.readouterr().err


def test_the_dead_tldrsec_feed_is_deactivated_in_the_real_registry():
    from pathlib import Path

    import common

    real = common.load_json(Path(__file__).resolve().parent.parent / "data" / "sources.json")
    row = next(s for s in real if s["id"] == "rss:https-tldrsec-com-feed")
    assert row["active"] is False and "404" in row["deactivated_reason"]


def test_looks_feed_url():
    assert a.looks_feed_url("https://x.com/feed")
    assert a.looks_feed_url("https://x.com/atom.xml")
    assert not a.looks_feed_url("https://x.com/blog/post")


def test_resolve_x_account():
    stored, handle, url = a.resolve(ns(type="x_account", handle="@simonw"))
    assert (stored, handle, url) == ("x_account", "simonw", "https://x.com/simonw")


def test_resolve_github_user_and_query():
    assert a.resolve(ns(type="github_user", handle="trailofbits")) == (
        "github_user",
        "trailofbits",
        "https://github.com/trailofbits",
    )
    assert a.resolve(ns(type="github_query", handle="threat modeling")) == (
        "github_query",
        "threat modeling",
        None,
    )


def test_resolve_youtube():
    stored, handle, url = a.resolve(ns(type="youtube", handle="https://youtube.com/@LiveOverflow"))
    assert stored == "youtube" and url == "https://youtube.com/@LiveOverflow"
    assert a.resolve(ns(type="youtube", handle="@x"))[2] is None  # bare handle -> no url


def test_resolve_rss_feed_url_skips_discovery():
    # an explicit feed URL is used as-is (no network discovery)
    assert a.resolve(ns(type="rss", handle="https://blog.example.com/feed")) == (
        "rss",
        "https://blog.example.com/feed",
        "https://blog.example.com/feed",
    )


def test_resolve_blog_discovers_feed(monkeypatch):
    monkeypatch.setattr(a, "discover_feed", lambda url: "https://blog.example.com/rss.xml")
    stored, handle, url = a.resolve(ns(type="blog", handle="https://blog.example.com"))
    assert stored == "rss"
    assert handle == "https://blog.example.com/rss.xml"
    assert url == "https://blog.example.com"


def test_collect_signals_manual_and_github(monkeypatch):
    manual = a.collect_signals(
        ns(followers=1000, stars=None, subscribers=None), "x_account", "simonw"
    )
    assert manual == {"followers": 1000}
    monkeypatch.setattr(a, "github_user_followers", lambda u: 3012)
    auto = a.collect_signals(
        ns(followers=None, stars=None, subscribers=None), "github_user", "trailofbits"
    )
    assert auto == {"followers": 3012}


def test_main_registers_source(sandbox, monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["add_source", "github_query", "mcp security", "--topics", "ai-security", "--tier", "high"],
    )
    assert a.main() == 0
    sources = sr.load_sources()
    assert len(sources) == 1
    assert sources[0]["type"] == "github_query" and sources[0]["tier"] == "high"


def test_main_rejects_bad_topic(sandbox, monkeypatch):
    import pytest

    monkeypatch.setattr("sys.argv", ["add_source", "x_account", "@x", "--topics", "bogus"])
    with pytest.raises(SystemExit):
        a.main()
