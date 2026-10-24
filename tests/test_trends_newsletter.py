"""Tests for scripts/trends.py and scripts/generate_newsletter.py."""

from __future__ import annotations

from datetime import UTC, datetime

import common as c
import generate_newsletter as nl
import trends
from conftest import make_entry


def _seed_cluster(topic="ai-security"):
    pool = c.load_pool(topic)
    pool["entries"] = [
        make_entry(
            topic=topic,
            domain="ais.mcp-tools",
            title="Tool A",
            source_url="https://a/1",
            source_id="src-1",
            tags=["agent-security", "mcp"],
            published="2026-07-01",
        ),
        make_entry(
            topic=topic,
            domain="ais.mcp-tools",
            title="Tool B",
            source_url="https://a/2",
            source_id="src-2",
            tags=["agent-security"],
            published="2026-07-02",
        ),
    ]
    c.save_pool(topic, pool)


def test_build_trends_clusters_by_tag(sandbox):
    _seed_cluster()
    conf = c.load_config()
    result = trends.build_trends("ai-security", conf, datetime(2026, 7, 13, tzinfo=UTC))
    tags = {t["tag"] for t in result}
    assert "agent-security" in tags  # 2 findings, 2 sources -> qualifies
    assert "mcp" not in tags  # only 1 finding -> below threshold


def test_trends_main_writes_files(sandbox):
    _seed_cluster()
    assert trends.main() == 0
    assert (sandbox / "TRENDS.md").exists()
    assert (c.DATA_DIR / "trends.json").exists()
    body = (sandbox / "TRENDS.md").read_text(encoding="utf-8")
    assert "agent-security" in body


def test_newsletter_has_all_topics(sandbox):
    _seed_cluster()
    trends.main()
    assert nl.main() == 0
    text = (sandbox / "NEWSLETTER.md").read_text(encoding="utf-8")
    for meta in c.TOPICS.values():
        assert meta["name"] in text
    assert "Emerging trends" in text
    assert "Tool A" in text  # latest research surfaced


# --- rising / steady / quiet, and source names are not themes ---------------
NOW = datetime(2026, 7, 15, tzinfo=UTC)
SETTINGS = {"baseline_days": 180, "rising_ratio": 1.0, "rising_min_recent": 2, "exclude_tags": []}


def _seed(rows, topic="ai-research"):
    """rows: (tag, published, source_id)."""
    pool = c.load_pool(topic)
    pool["entries"] = [
        make_entry(
            topic=topic,
            domain="air.agents",
            title=f"{tag} {i}",
            source_url=f"https://a/{i}",
            source_id=src,
            tags=[tag],
            published=day,
        )
        for i, (tag, day, src) in enumerate(rows)
    ]
    c.save_pool(topic, pool)


def _states(excluded=frozenset()):
    rows = trends.build_trends("ai-research", c.load_config(), NOW, SETTINGS, set(excluded))
    return {t["tag"]: t for t in rows}


def test_old_theme_with_no_recent_findings_is_quiet_not_rising(sandbox):
    """The bug: 'arxiv ▲ rising 76 total / 0 recent'."""
    _seed([("mcp", "2026-03-01", "s1"), ("mcp", "2026-04-01", "s2"), ("mcp", "2026-05-01", "s3")])
    mcp = _states()["mcp"]
    assert (mcp["state"], mcp["recent"], mcp["momentum"]) == ("quiet", 0, 0.0)


def test_theme_above_its_baseline_rate_is_rising(sandbox):
    _seed(
        [("evals", "2026-02-01", "s1")]  # one finding in the baseline period
        + [("evals", f"2026-07-0{d}", f"s{d}") for d in (2, 3, 4)]  # three this window
    )
    evals = _states()["evals"]
    assert evals["state"] == "rising"
    assert evals["recent"] == 3 and evals["baseline"] < 1
    assert evals["momentum"] == evals["excess"] > 0


def test_theme_at_its_usual_rate_is_steady(sandbox):
    """Two a month for six months, two this month: busy, not rising."""
    rows = [("rag", f"2026-0{m}-{d:02d}", f"s{m}{d}") for m in range(1, 7) for d in (5, 10)]
    _seed(rows + [("rag", "2026-07-05", "x1"), ("rag", "2026-07-10", "x2")])
    rag = _states()["rag"]
    assert (rag["state"], rag["recent"], rag["momentum"]) == ("steady", 2, 0.0)
    assert rag["baseline"] >= 2


def test_one_recent_finding_is_not_enough_to_rise(sandbox):
    _seed([("new-thing", "2026-07-10", "s1"), ("new-thing", "2026-01-10", "s2")])
    assert _states()["new-thing"]["state"] == "steady"  # below rising_min_recent


def test_rising_sorts_before_steady_before_quiet(sandbox):
    _seed(
        [("old", "2026-03-01", "s1"), ("old", "2026-03-02", "s2"), ("old", "2026-03-03", "s3")]
        + [("hot", "2026-07-10", "s1"), ("hot", "2026-07-11", "s2")]
        + [("warm", "2026-07-10", "s1"), ("warm", "2026-01-10", "s2")]
    )
    rows = trends.build_trends("ai-research", c.load_config(), NOW, SETTINGS, set())
    assert [t["tag"] for t in rows] == ["hot", "warm", "old"]


def test_source_and_feed_names_are_not_themes(sandbox):
    _seed([("arxiv", "2026-07-10", "s1"), ("arxiv", "2026-07-11", "s2")])
    assert "arxiv" in _states()
    assert "arxiv" not in _states({"arxiv"})


def test_source_tags_come_from_the_registry_and_config():
    sources = [
        {"name": "Palo Alto Networks Unit 42", "url": "https://unit42.paloaltonetworks.com/feed/"},
        {"name": "arXiv cs.CR", "url": "https://export.arxiv.org/rss/cs.CR"},
        {"name": "Simon", "type": "x", "handle": "@simonw"},
        {"name": "Google AI", "url": "https://blog.google/technology/ai/rss/"},
        {"name": "AISI", "url": "https://www.aisi.gov.uk/blog"},
        {"name": "Anthropic Alignment Science", "url": "https://alignment.anthropic.com/"},
    ]
    tags = trends.source_tags(sources, ["GHSA"])
    for expected in ("paloaltonetworks", "arxiv", "simonw", "google", "aisi", "anthropic", "ghsa"):
        assert expected in tags
    assert "alignment" not in tags  # a subdomain is not a source name: alignment is a theme
    assert "blog" not in tags and "www" not in tags


def test_config_settings_reach_the_classifier():
    assert trends.classify(0, 0.0, SETTINGS) == "quiet"
    assert trends.classify(2, 1.9, SETTINGS) == "rising"
    assert trends.classify(2, 2.0, SETTINGS) == "steady"  # equal is not above
    assert trends.classify(3, 2.0, {**SETTINGS, "rising_ratio": 1.5}) == "steady"
    assert trends.classify(3, 0.0, {**SETTINGS, "rising_min_recent": 4}) == "steady"
    assert trends.trend_settings()["baseline_days"] > 0  # the shipped config.yaml block


def test_trends_md_and_newsletter_label_the_state(sandbox):
    _seed([("mcp", "2026-03-01", "s1"), ("mcp", "2026-04-01", "s2")])
    trends.main()
    nl.main()
    assert "quiet mcp" in (sandbox / "TRENDS.md").read_text(encoding="utf-8")
    text = (sandbox / "NEWSLETTER.md").read_text(encoding="utf-8")
    assert "**mcp** (quiet)" in text and "rising" not in text.split("Emerging trends")[-1]
