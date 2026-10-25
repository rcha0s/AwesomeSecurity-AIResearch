"""Audit F4: scan PRs may not edit data/sources.json (it is off the auto-merge
allowlist), so scan-time hit-rate stats live in data/source_stats.json."""

from __future__ import annotations

import json

import common as c
import merge_analysis as m
import pytest
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


@pytest.mark.parametrize(
    "counts",
    [
        {"ingested": "abc", "curated": 1},
        {"ingested": 10**12, "curated": 1},
        {"ingested": 5, "curated": -1},
        {"ingested": [1], "curated": 1},
        {"ingested": 1.5, "curated": 1},
        {"ingested": True, "curated": 1},
        {"ingested": None, "curated": 1},
        "not a dict",
        [1, 2],
        7,
    ],
)
def test_insane_stats_are_ignored_not_fatal(sandbox, counts):
    """Re-audit item 2: a scan-written stats file can't crash every ingestor
    (or allowlist.py); the bad id falls back to its registry baseline."""
    bad, good = sr.new_source("rss", "https://bad/feed"), sr.new_source("rss", "https://good/feed")
    bad["stats"] = {"ingested": 4, "curated": 2}
    sr.save_sources([bad, good])
    ok = {"ingested": 9, "curated": 3}
    sr.STATS_FILE.write_text(json.dumps({bad["id"]: counts, good["id"]: ok}))
    assert sr.load_stats() == {good["id"]: ok}
    by_id = {s["id"]: s for s in sr.load_sources()}
    assert by_id[bad["id"]]["stats"] == {"ingested": 4, "curated": 2}
    assert by_id[good["id"]]["stats"] == ok
    sr.update_stats({bad["id"]: (1, 0)})  # still works, from the baseline
    assert sr.load_stats()[bad["id"]] == {"ingested": 5, "curated": 2}


def test_stats_bounds_are_inclusive(sandbox):
    src = sr.new_source("rss", "https://edge/feed")
    sr.save_sources([src])
    edge = {"ingested": sr.MAX_STAT, "curated": 0}
    sr.STATS_FILE.write_text(json.dumps({src["id"]: edge}))
    assert sr.load_stats() == {src["id"]: edge}
    sr.STATS_FILE.write_text(json.dumps({src["id"]: {"ingested": sr.MAX_STAT + 1}}))
    assert sr.load_stats() == {}


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


def test_adding_a_source_never_copies_scan_stats_into_the_registry(sandbox):
    first = sr.new_source("rss", "https://a/feed", tier="medium")
    sr.add_source(first)
    baseline = json.loads(sr.REGISTRY_FILE.read_text())
    sr.update_stats({first["id"]: (9, 7)})  # scan counts move its overlaid rank
    sr.add_source(sr.new_source("rss", "https://b/feed", tier="medium"))
    raw = json.loads(sr.REGISTRY_FILE.read_text())
    assert raw[0] == baseline[0]  # first row untouched: no stats, no rank change
    assert [s["id"] for s in raw] == [first["id"], "rss:https-b-feed"]
