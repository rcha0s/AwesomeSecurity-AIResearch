"""Tests for scripts/source_scout.py — the daily source-discovery agent."""

from __future__ import annotations

import json

import common
import source_scout as ss


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def _ctx_with(sandbox, sources=(), blocklist=()):
    (sandbox / "data" / "sources.json").write_text(
        json.dumps(list(sources)), encoding="utf-8"
    )
    (sandbox / "data" / "source_blocklist.json").write_text(
        json.dumps(list(blocklist)), encoding="utf-8"
    )
    # Point the module's Paths at the sandbox
    ss.SOURCES = sandbox / "data" / "sources.json"
    ss.BLOCKLIST = sandbox / "data" / "source_blocklist.json"
    ss.PROPOSALS = sandbox / "data" / "source_proposals.json"
    return ss._ctx()


def _story(url, title="Trending story", points=200):
    return {"title": title, "url": url, "points": points, "signal": "hackernews"}


# ---------------------------------------------------------------------------
# Filter logic (no network needed)
# ---------------------------------------------------------------------------
def test_host_extracts_and_strips_www():
    assert ss._host("https://www.Example.com/x/y") == "example.com"
    assert ss._host("http://Example.com/") == "example.com"
    assert ss._host("") == ""
    assert ss._host("not-a-url") == ""


def test_permanent_block_hosts_never_proposed(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (10, 10))
    proposal = ss._propose(ctx, _story("https://www.bloomberg.com/x"))
    assert proposal is None


def test_already_registered_domain_skipped(sandbox, monkeypatch):
    sources = [{
        "id": "rss:example",
        "url": "https://example.com/feed",
        "handle": "https://example.com/feed",
    }]
    ctx = _ctx_with(sandbox, sources=sources)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (10, 10))
    proposal = ss._propose(ctx, _story("https://example.com/some-article"))
    assert proposal is None


def test_blocklisted_domain_skipped(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox, blocklist=[{"domain": "spammy.com"}])
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (10, 10))
    proposal = ss._propose(ctx, _story("https://spammy.com/x"))
    assert proposal is None


def test_no_feed_records_skipped_reason(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: None)
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (0, 0))
    p = ss._propose(ctx, _story("https://newpub.example/x"))
    assert p is not None
    assert p["status"] == "skipped"
    assert "feed" in p["reason"].lower()


def test_below_hit_rate_records_skipped(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://newpub.example/feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (2, 20))
    p = ss._propose(ctx, _story("https://newpub.example/x"))
    assert p["status"] == "skipped"
    assert "hit-rate" in p["reason"]
    assert p["hit_rate"] == 0.1


def test_above_hit_rate_records_proposed(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://goodpub.example/feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (10, 20))
    p = ss._propose(ctx, _story("https://goodpub.example/x"))
    assert p["status"] == "proposed"
    assert p["hit_rate"] == 0.5
    assert p["suggested_track"] == "news"
    assert p["suggested_tier"] == "medium"


# ---------------------------------------------------------------------------
# End-to-end scout() with a small stubbed set of trending stories
# ---------------------------------------------------------------------------
def test_scout_dedupes_domain_seen_twice(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: "https://newpub.example/feed")
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (10, 20))
    trending = [
        _story("https://newpub.example/a", "First"),
        _story("https://newpub.example/b", "Second"),
    ]
    doc = ss.scout(ctx, trending)
    assert doc["summary"]["candidate_domains"] == 1
    assert doc["summary"]["proposed"] == 1


def test_scout_writes_doc_shape(sandbox, monkeypatch):
    ctx = _ctx_with(sandbox)
    monkeypatch.setattr(ss, "_discover_feed", lambda h: None)
    monkeypatch.setattr(ss, "_classifier_hit_rate", lambda f, r: (0, 0))
    doc = ss.scout(ctx, [_story("https://newpub.example/x")])
    assert set(doc.keys()) == {"generated", "proposed", "skipped", "summary"}
    assert doc["summary"]["skipped"] == 1
    assert doc["summary"]["proposed"] == 0


# --- remove_source CLI -----------------------------------------------------
def test_remove_source_deletes_and_optionally_blocklists(sandbox, monkeypatch, capsys):
    import remove_source as rs

    (sandbox / "data" / "sources.json").write_text(json.dumps([
        {"id": "rss:x", "name": "X", "url": "https://x.example.com/feed"},
        {"id": "rss:y", "name": "Y", "url": "https://y.example.com/feed"},
    ]), encoding="utf-8")
    (sandbox / "data" / "source_blocklist.json").write_text("[]", encoding="utf-8")
    monkeypatch.setattr(rs, "SOURCES", sandbox / "data" / "sources.json")
    monkeypatch.setattr(rs, "BLOCKLIST", sandbox / "data" / "source_blocklist.json")

    rc = rs.main(["rss:x", "--blocklist", "--reason", "test drop"])
    assert rc == 0

    left = json.loads((sandbox / "data" / "sources.json").read_text())
    assert [s["id"] for s in left] == ["rss:y"]
    block = json.loads((sandbox / "data" / "source_blocklist.json").read_text())
    assert block[0]["domain"] == "x.example.com"
    assert block[0]["reason"] == "test drop"


def test_remove_source_missing_id_errors(sandbox, monkeypatch):
    import remove_source as rs
    (sandbox / "data" / "sources.json").write_text("[]", encoding="utf-8")
    monkeypatch.setattr(rs, "SOURCES", sandbox / "data" / "sources.json")
    monkeypatch.setattr(rs, "BLOCKLIST", sandbox / "data" / "source_blocklist.json")
    assert rs.main(["rss:not-there"]) == 1
