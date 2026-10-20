"""Audit F4: scan PRs may not edit data/sources.json (it is off the auto-merge
allowlist), so scan-time hit-rate stats live in data/source_stats.json."""

from __future__ import annotations

import common as c
import merge_analysis as m
import sources_registry as sr
from conftest import make_entry


def test_scan_stats_never_touch_the_registry_file(sandbox):
    src = sr.new_source("rss", "https://a/feed", tier="medium")
    sr.add_source(src)
    before = sr.REGISTRY_FILE.read_bytes()
    sr.update_stats({src["id"]: (3, 2)})
    sr.update_stats({src["id"]: (1, 0)})
    assert sr.REGISTRY_FILE.read_bytes() == before
    assert sr.load_stats() == {src["id"]: {"ingested": 4, "curated": 2}}
    loaded = sr.get_by_id(src["id"])
    assert loaded["stats"] == {"ingested": 4, "curated": 2}
    assert loaded["rank"] == sr.compute_rank(loaded)


def test_merge_analysis_writes_stats_not_the_registry(sandbox):
    src = sr.new_source("rss", "https://example.com/feed")
    sr.add_source(src)
    before = sr.REGISTRY_FILE.read_bytes()
    m.merge([make_entry(source_id=src["id"])], c.load_config())
    m.update_source_hit_rate([make_entry(source_id=src["id"], needs_review=False)])
    assert sr.REGISTRY_FILE.read_bytes() == before
    assert sr.load_stats()[src["id"]]["ingested"] == 1


def test_stats_start_from_the_registry_baseline(sandbox):
    src = sr.new_source("rss", "https://b/feed")
    src["stats"] = {"ingested": 10, "curated": 4}
    sr.save_sources([src])
    sr.update_stats({src["id"]: (1, 1)})
    assert sr.load_stats()[src["id"]] == {"ingested": 11, "curated": 5}


def test_malformed_stats_file_is_ignored(sandbox):
    src = sr.new_source("rss", "https://c/feed")
    sr.save_sources([src])
    sr.STATS_FILE.write_text("[1, 2]")
    assert sr.load_stats() == {}
    assert sr.get_by_id(src["id"])["stats"] == {"ingested": 0, "curated": 0}


def test_merge_analysis_rejects_non_http_urls(sandbox):
    """Audit F3: a javascript: (or any non-http) URL never enters a pool."""
    bad = [
        make_entry(title="js link", source_url="javascript:alert(1)"),
        make_entry(title="data link", article_url="data:text/html,x"),
        make_entry(title="quote breakout", source_url='https://e.example/"onmouseover=x'),
    ]
    merged, errors, _, _ = m.merge([*bad, make_entry()], c.load_config())
    assert [e["title"] for e in merged] == [make_entry()["title"]]
    assert len(errors) == 3 and all("http(s)" in e for e in errors)
