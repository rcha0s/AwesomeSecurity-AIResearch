"""Tests for scripts/eval_integrity.py (ISC-24) — a seeded bad entry must fail it."""

from __future__ import annotations

import json

import common
import eval_integrity as ei
import pytest
from conftest import make_entry


def good_entry(**over) -> dict:
    entry = make_entry(
        id="good",
        source_url="https://example.com/posts/compact",
        article_url="https://example.com/posts/compact",
        grounding_score=1.0,
        lessons=[
            {"point": "p", "excerpt": "cut token use by 40%", "confidence": 0.9, "grounded": True}
        ],
    )
    entry.update(over)
    return entry


def site_row(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "story_id": f"story-{entry['id']}",
        "topic": entry["topic"],
        "domain_id": entry["domain"],
        "url": entry.get("article_url") or entry["source_url"],
    }


def publish(sandbox, entries: list[dict], findings=None, editorial=None, archive=None) -> None:
    for topic in common.TOPICS:
        pool = common.empty_pool(topic)
        pool["entries"] = [e for e in entries if e["topic"] == topic]
        common.save_pool(topic, pool)
    common.save_json(common.ARCHIVE_FILE, archive or [])
    data = {
        "findings": [site_row(e) for e in entries] if findings is None else findings,
        "editorial": editorial or [],
    }
    page = (
        f'<html><script id="site-data" type="application/json">{json.dumps(data)}</script></html>'
    )
    (sandbox / "docs").mkdir(exist_ok=True)
    (sandbox / "docs" / "index.html").write_text(page)


def test_the_real_pools_and_site_pass():
    """The probe: integrity holds on the committed data (no sandbox)."""
    report = ei.run()
    assert report["problems"] == [] and report["published"] > 0


def test_a_clean_published_entry_passes(sandbox):
    publish(sandbox, [good_entry()])
    assert ei.run()["passed"]


SEEDED = {
    "ungrounded lesson": ({"lessons": [{"point": "p", "excerpt": "x", "grounded": False}]}, "marked ungrounded"),
    "partial grounding": ({"grounding_score": 0.5}, "grounding_score 0.5"),
    "homepage citation": ({"article_url": "https://example.com/", "source_url": "https://example.com"}, "homepage"),
    "invalid domain": ({"domain": "Agents & Harnesses"}, "not a ai-research taxonomy ID"),
    "other topic's domain": ({"domain": "ais.agent-security"}, "not a ai-research taxonomy ID"),
    "javascript url": ({"tweet_url": "javascript:alert(1)"}, "not an http(s) URL"),
}  # fmt: skip


@pytest.mark.parametrize("name", SEEDED)
def test_a_seeded_bad_entry_fails(sandbox, name, capsys):
    over, needle = SEEDED[name]
    bad = good_entry(**over)
    publish(sandbox, [bad], findings=[site_row(good_entry())])
    report = ei.run()
    assert not report["passed"]
    assert any(needle in p for p in report["problems"]), report["problems"]
    assert ei.main([]) == 1
    assert capsys.readouterr().out.strip().splitlines()[-1].startswith("EVAL integrity FAIL")


def test_an_excerpt_missing_from_its_raw_source_text_fails(sandbox):
    raw = sandbox / "data" / "_raw"
    raw.mkdir(parents=True)
    (raw / "good.txt").write_text("The article says something else entirely.")
    publish(sandbox, [good_entry(raw_path="data/_raw/good.txt")])
    problems = ei.run()["problems"]
    assert any("not found in its raw source text" in p for p in problems)
    (raw / "good.txt").write_text("Compaction cut token use by 40% on long tasks.")
    assert ei.run()["passed"]


def test_a_story_rendered_twice_fails_in_one_lane_or_across_both(sandbox):
    """The story ledger's own check (content_checks.site_story_problems)."""
    e = good_entry()
    publish(sandbox, [e], findings=[site_row(e), site_row(e)])
    assert any("duplicate story id on the site: story-good" in p for p in ei.run()["problems"])
    publish(sandbox, [e], editorial=[site_row(e)])
    assert any("duplicate story id on the site: story-good" in p for p in ei.run()["problems"])


def test_a_rendered_row_without_a_story_id_fails(sandbox):
    e = good_entry()
    publish(sandbox, [e], findings=[{**site_row(e), "story_id": ""}])
    assert any("row without story_id: good" in p for p in ei.run()["problems"])


def test_a_rendered_story_missing_from_the_pools_fails(sandbox):
    publish(sandbox, [good_entry()], findings=[site_row(good_entry(id="ghost"))])
    assert any("is in no pool" in p for p in ei.run()["problems"])


def test_pool_wide_invariants_and_warnings(sandbox):
    held = good_entry(id="held", needs_review=True, article_url="https://blog.example.org/")
    twin = good_entry(id="twin")
    publish(sandbox, [good_entry(), held, twin], findings=[site_row(good_entry())],
            archive=[dict(twin), good_entry(id="old", domain="nonsense")])  # fmt: skip
    report = ei.run()
    assert report["problems"] == [
        "[archive] old: domain 'nonsense' is not a ai-research taxonomy ID"
    ]
    assert any("held entry cites a homepage" in w for w in report["warnings"])
    assert any("twin: in a pool and in the archive" in w for w in report["warnings"])


def test_a_repeated_id_inside_the_live_pools_fails(sandbox):
    publish(sandbox, [good_entry(), good_entry()], findings=[site_row(good_entry())])
    assert "[pools] id good appears 2 times" in ei.run()["problems"]


@pytest.mark.parametrize(
    "url,home",
    [
        ("https://blog.trailofbits.com/", True),
        ("https://example.com", True),
        ("https://example.com/en/", True),
        ("https://example.com/index.html", True),
        ("https://example.com/?p=123", False),
        ("https://example.com/2026/07/post", False),
        ("https://github.com/org/repo", False),
        ("not a url", False),
    ],
)
def test_is_homepage(url, home):
    assert ei.is_homepage(url) is home


def test_a_page_without_its_data_block_cannot_pass(sandbox, capsys):
    publish(sandbox, [good_entry()])
    (sandbox / "docs" / "index.html").write_text("<html></html>")
    assert ei.main([]) == 1
    assert "could not run" in capsys.readouterr().out
