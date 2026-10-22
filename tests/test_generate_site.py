"""Tests for scripts/generate_site.py — trees, per-entry pages, tolerant ranking."""

from __future__ import annotations

import common as c
import generate_site as g
from conftest import make_entry


def _seed(sandbox):
    ai = c.load_pool("ai-research")
    ai["entries"] = [make_entry(source_url="https://a/ai1")]
    c.save_pool("ai-research", ai)
    sec = c.load_pool("ai-security")
    sec["entries"] = [
        # security entry: scored (so it's curated), no summary, has threat block
        {
            "topic": "ai-security",
            "domain": "ais.prompt-injection",
            "title": "Legacy XSS finding",
            "source_url": "https://a/sec1",
            "date": "2026-01",
            "scores": {"novelty": 70, "relevance": 70},
            "threat": "Reflected XSS in search.",
            "conditions": "Unescaped param.",
            "mitigations": "Encode output.",
        }
    ]
    c.save_pool("ai-security", sec)


def test_generate_site_builds_trees_and_pages(sandbox):
    _seed(sandbox)
    g.main()
    assert (sandbox / "README.md").exists()
    assert (sandbox / "ai-security" / "README.md").exists()
    assert (sandbox / "ai-research" / "README.md").exists()
    ai_pages = list((sandbox / "ai-research" / c.domain_slug("air.agents")).glob("*.md"))
    sec_pages = list((sandbox / "ai-security" / c.domain_slug("ais.prompt-injection")).glob("*.md"))
    assert ai_pages and sec_pages
    readme = (sandbox / "README.md").read_text(encoding="utf-8")
    # The short guide: teaser of this week's picks, big links into the site.
    assert "## This week's top stories" in readme
    assert "## Claim changes" in readme and "What to do now" not in readme
    assert "## Contribute" in readme


def test_legacy_entry_renders_without_scores(sandbox):
    _seed(sandbox)
    conf = c.load_config()
    legacy = c.load_pool("ai-security")["entries"][0]
    page = g.render_entry_page(legacy, conf)
    assert "Legacy XSS finding" in page
    assert "Threat" in page  # threat/conditions/mitigations block still appears


def test_ai_entry_with_summary_no_threat(sandbox):
    conf = c.load_config()
    page = g.render_entry_page(make_entry(), conf)
    assert "## TL;DR" in page  # entries are condensed TL;DR gists
    assert "Threat · Conditions" not in page  # no threat on AI-research entry


def test_entry_scores_tolerant_of_missing():
    conf = c.load_config()
    s = g.entry_scores({"date": "2026-07"}, conf)
    assert {"newness", "novelty", "relevance", "composite"} <= s.keys()


def test_score_line_has_no_decorative_emoji():
    """Score labels are plain text, not emoji markers - the labels and
    numbers already carry the meaning."""
    line = g.score_line({"newness": 20, "novelty": 88, "relevance": 85, "composite": 67.85})
    assert "Newness 20" in line and "Novelty 88" in line
    assert not any(ch in line for ch in "🆕✨🎯🏛️")


def test_grounding_mark_only_flags_the_exceptional_case():
    """A normal, grounded excerpt gets no marker; only a failed grounding
    check (the case a reader should actually notice) does."""
    assert g._grounding_mark({"grounded": True}) == ""
    assert g._grounding_mark({}) == ""
    assert "⚠️" in g._grounding_mark({"grounded": False})


def test_counts_labelled_as_the_window_exclude_vetted_news(sandbox):
    """A vetted news story is news, not a finding: the topic page and the
    newsletter count only the window's findings and list the story as news."""
    import json

    import generate_newsletter as gn

    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    pool = c.load_pool("ai-research")
    pool["entries"] = [
        make_entry(source_url="https://a/finding", title="finding"),
        make_entry(
            source_url="https://a/news",
            title="old vetted news",
            source_id="rss:news",
            published="2020-01-01",
            date="2020-01-01",
        ),
    ]
    c.save_pool("ai-research", pool)
    conf = c.load_config()
    window = g.write_topic("ai-research", conf, "now")
    assert [e["title"] for e in window] == ["finding"]
    page = (sandbox / "ai-research" / "README.md").read_text(encoding="utf-8")
    assert "_1 vetted findings" in page
    assert "old vetted news" in page.split("| Domain |")[0]  # in the news section
    assert "1 vetted findings in window" in gn.build(conf, "now")
