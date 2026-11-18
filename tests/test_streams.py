"""Research streams: data/streams.yaml rules (scripts/streams.py) and the renderer
(scripts/generate_stream.py)."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

import common as c
import generate_stream as gs
import streams as st
import taxonomy as tx

RULES = {
    "streams": {
        "harness": {
            "name": "Harness",
            "blurb": "Build better harnesses.",
            "library_days": 90,
            "feed_max": 5,
            "watch_min_relevance": 60,
            "subcategories": [
                {"id": "cost", "name": "Cost", "domains": ["air.cost-efficiency"],
                 "from": ["air.agents"], "keywords": ["prompt caching"]},
                {"id": "speed", "name": "Speed", "domains": ["air.tooling"],
                 "from": ["air.agents"], "keywords": ["latency"]},
                {"id": "design", "name": "Design", "domains": ["air.agents"]},
            ],
        }
    }
}  # fmt: skip


def stream() -> st.Stream:
    return st.parse(RULES)["harness"]


def test_the_shipped_streams_file_names_only_taxonomy_domains():
    streams = st.load(known_domains=set(tx.get().domains))
    harness = streams["harness-engineering"]
    ids = [s.id for s in harness.subcategories]
    assert ids[0] == "cost-efficiency"  # cost efficiency is one sub-category, listed first
    assert {"air.cost-efficiency", "air.work-efficiency", "air.agents", "air.context"} <= harness.domains()
    # every domain a stream draws on is an ai-research domain
    assert {tx.get().domains[d].topic for d in harness.domains()} == {"ai-research"}


def test_an_unknown_domain_in_a_rule_is_an_error():
    bad = {"streams": {"s": {"subcategories": [{"id": "x", "domains": ["air.nope"]}]}}}
    with pytest.raises(ValueError, match="unknown domains"):
        st.parse(bad, known_domains={"air.agents"})


def test_from_without_keywords_is_an_error():
    bad = {"streams": {"s": {"subcategories": [{"id": "x", "from": ["air.agents"]}]}}}
    with pytest.raises(ValueError, match="no keywords"):
        st.parse(bad)


def test_domain_rule_wins_and_first_match_wins():
    s = stream()
    assert st.classify({"domain": "air.cost-efficiency", "title": "latency"}, s) == "cost"
    assert st.classify({"domain": "air.tooling"}, s) == "speed"
    # air.agents: a keyword moves it into an earlier sub-category, else the catch-all
    assert st.classify({"domain": "air.agents", "title": "Cutting tool latency in half"}, s) == "speed"
    assert st.classify({"domain": "air.agents", "takeaway": "Use prompt caching."}, s) == "cost"
    assert st.classify({"domain": "air.agents", "title": "A new agent loop"}, s) == "design"


def test_keywords_match_whole_words_and_tags():
    s = stream()
    assert st.classify({"domain": "air.agents", "title": "latencyfree"}, s) == "design"
    assert st.classify({"domain": "air.agents", "tags": ["prompt-caching"]}, s) == "cost"


def test_a_domain_outside_the_stream_is_not_in_it():
    assert st.classify({"domain": "ais.prompt-injection", "title": "latency"}, stream()) is None
    assert st.classify({"title": "latency"}, stream()) is None


def test_claims_classify_on_domain_and_statement():
    s = stream()
    claim = {"domain": "air.agents", "statement": "Parallel tool calls cut latency."}
    assert st.classify(claim, s) == "speed"


def test_library_window_counts_from_the_finding_date():
    now = datetime(2026, 11, 18)
    assert st.in_library({"published": "2026-09-01"}, now, 90)
    assert not st.in_library({"published": "2026-08-01"}, now, 90)
    assert st.in_library({"date": "2026-08"}, now, 90)  # a month counts from its last day
    assert not st.in_library({}, now, 90)  # undated findings stay out


def test_a_keyword_rule_may_not_take_a_later_subcategorys_own_domain():
    bad = {"streams": {"s": {"subcategories": [
        {"id": "a", "from": ["air.context"], "keywords": ["x"]},
        {"id": "b", "domains": ["air.context"]},
        {"id": "z", "domains": ["air.agents"]},
    ]}}}  # fmt: skip
    with pytest.raises(ValueError, match="owns them"):
        st.parse(bad)
    # the last sub-category is the catch-all: keywords may draw on its domains
    st.parse({"streams": {"s": {"subcategories": [
        {"id": "a", "from": ["air.agents"], "keywords": ["x"]},
        {"id": "z", "domains": ["air.agents"]},
    ]}}})  # fmt: skip


def entry(eid: str, domain: str, published: str, **extra) -> dict:
    base = {
        "id": eid, "topic": "ai-research", "domain": domain, "title": f"Finding {eid}",
        "takeaway": f"Takeaway {eid}.", "summary": "Summary.", "published": published,
        "date": published[:7], "article_url": f"https://example.com/{eid}",
        "source_name": "Example", "scores": {"novelty": 80, "relevance": 80},
        "needs_review": False, "verified": True, "grounding_score": 1.0,
    }  # fmt: skip
    base.update(extra)
    return base


def test_collect_keeps_vetted_and_watch_tiers_and_drops_refuted():
    conf = c.load_config()
    now = datetime(2026, 11, 18)
    pool = [
        entry("v", "air.agents", "2026-11-10"),
        entry("w", "air.agents", "2026-11-09", needs_review=True, scores={"novelty": 20, "relevance": 75}),
        entry("unchecked", "air.agents", "2026-11-09", needs_review=True, grounding_score=None,
              scores={"novelty": 20, "relevance": 75}),
        entry("low", "air.agents", "2026-11-08", needs_review=True, scores={"novelty": 20, "relevance": 30}),
        entry("refuted", "air.agents", "2026-11-07", needs_review=True, verified=False),
        entry("old", "air.agents", "2026-05-01"),
        entry("off", "ais.prompt-injection", "2026-11-10", topic="ai-security"),
    ]
    archive = [entry("arch", "air.tooling", "2026-10-01")]
    rows = gs.collect(stream(), conf, now, {"ai-research": pool}, archive, {})
    tiers = {r["id"]: r["_tier"] for r in rows}
    assert tiers == {"v": "vetted", "w": "watch", "arch": "vetted"}
    assert [r["id"] for r in rows] == ["v", "w", "arch"]  # newest first


def test_collect_lists_one_entry_per_story():
    conf = c.load_config()
    now = datetime(2026, 11, 18)
    a = entry("a", "air.agents", "2026-11-10")
    b = entry("b", "air.agents", "2026-11-10", scores={"novelty": 90, "relevance": 90})
    rows = gs.collect(stream(), conf, now, {"ai-research": [a, b]}, [], {"a": "s1", "b": "s1"})
    assert [r["id"] for r in rows] == ["b"]


def test_feed_is_json_feed_1_1_with_stream_extension():
    conf = c.load_config()
    now = datetime(2026, 11, 18)
    rows = gs.collect(stream(), conf, now, {"ai-research": [entry("v", "air.agents", "2026-11-10")]}, [], {})
    claims = gs.stream_claims(stream(), {"claims": [
        {"id": "k", "title": "Cache prompts", "statement": "Prompt caching cuts cost.",
         "domain": "air.agents", "status": "current"},
        {"id": "gone", "title": "Old", "statement": "x", "domain": "air.agents", "status": "superseded"},
    ]})  # fmt: skip
    feed = json.loads(gs.render_feed(stream(), rows, claims, {"v"}, "2026-11-18"))
    assert feed["version"] == "https://jsonfeed.org/version/1.1"
    assert feed["feed_url"].endswith("/streams/harness.json")
    item = feed["items"][0]
    assert item["url"] == "https://example.com/v" and item["date_published"] == "2026-11-10T00:00:00Z"
    assert item["_stream"]["subcategory"] == "design" and item["_stream"]["tier"] == "vetted"
    assert [x["id"] for x in feed["_stream"]["claims"]] == ["k"]
    assert feed["_stream"]["claims"][0]["subcategory"] == "cost"


def test_an_old_finding_is_vetted_as_if_fresh():
    conf = c.load_config()
    now = datetime(2026, 11, 18)
    old = entry("old", "air.agents", "2026-09-01")  # past the site window, inside the stream's
    rows = gs.collect(stream(), conf, now, {}, [old], {})
    assert [(r["id"], r["_tier"]) for r in rows] == [("old", "vetted")]


def test_feed_leaves_out_an_empty_url_and_pads_a_month_date():
    row = {**entry("m", "air.agents", "2026-10", article_url=""), "date": "2026-10",
           "_sub": "design", "_tier": "vetted", "_in_pool": False}  # fmt: skip
    item = gs.feed_item(row, stream(), set())
    assert "url" not in item and item["date_published"] == "2026-10-01T00:00:00Z"


def test_markdown_lists_every_subcategory():
    rows = [{**entry("v", "air.agents", "2026-11-10"), "_sub": "design", "_tier": "vetted", "_in_pool": True}]
    md = gs.render_md(stream(), rows, [], set(), "2026-11-18")
    for name in ("## Cost", "## Speed", "## Design", "Finding v"):
        assert name in md
