"""Unit tests for scripts/common.py helpers, scoring, and validation."""

from __future__ import annotations

from datetime import UTC, datetime

import common as c
from conftest import make_entry


def test_normalize_url_strips_query_fragment_trailing():
    assert c.normalize_url("HTTPS://A.com/x/?q=1#frag") == "https://a.com/x"
    assert c.normalize_url("  https://a.com/x/  ") == "https://a.com/x"


def test_make_id_is_deterministic_and_slugged():
    a = c.make_id("MCP Tool Poisoning!", "http://x/a")
    b = c.make_id("MCP Tool Poisoning!", "http://x/a")
    assert a == b and a.startswith("mcp-tool-poisoning")


def test_slugify_and_clean_summary():
    assert c.slugify("Hello, World!!") == "hello-world"
    assert c.clean_summary("<p>a   b</p>") == "a b"
    assert c.clean_summary("x" * 400).endswith("…")


def test_title_similar():
    assert c.title_similar("MCP tool poisoning", "MCP Tool Poisoning")
    assert not c.title_similar("prompt injection", "supply chain attack")
    assert not c.title_similar("", "anything")


def test_extract_urls_dedup_and_trim():
    urls = c.extract_urls("see https://a.com/x, and https://a.com/x also http://b.io/y).")
    assert urls == ["https://a.com/x", "http://b.io/y"]


def test_clean_source_url_strips_tracking():
    assert c.clean_source_url("https://a.com/x?utm_source=rss&utm_medium=rss") == "https://a.com/x"
    assert c.clean_source_url("https://a.com/x?id=5&utm_source=x") == "https://a.com/x?id=5"
    assert c.clean_source_url("https://a.com/x") == "https://a.com/x"
    assert c.clean_source_url("https://a.com/x?fbclid=abc") == "https://a.com/x"


def test_date_from_url():
    assert c.date_from_url("https://x.com/2026/05/13/post") == "2026-05-13"
    assert c.date_from_url("https://x.com/2026/05/post") == "2026-05"
    assert c.date_from_url("https://x.com/no-date-here") is None


def test_is_fresh_window():
    now = datetime(2026, 7, 13, tzinfo=UTC)
    assert c.is_fresh({"published": "2026-07-01"}, 31, now=now) is True
    assert c.is_fresh({"published": "2026-06-30"}, 31, now=now) is True
    assert c.is_fresh({"published": "2026-05-01"}, 31, now=now) is False
    # month-only is treated as end-of-month (lenient)
    assert c.is_fresh({"date": "2026-06"}, 31, now=now) is True
    assert c.is_fresh({"date": "2026-05"}, 31, now=now) is False
    # undated entries are kept (never dropped for lack of a date)
    assert c.is_fresh({}, 31, now=now) is True


def test_add_candidates_rejects_stale(sandbox):
    stale = {
        "id": "old",
        "title": "Old thing",
        "source_url": "https://a/old",
        "published": "2020-01-01",
    }
    assert c.add_candidates([stale]) == []


def test_newness_score_decays():
    now = datetime(2026, 7, 1, tzinfo=UTC)
    fresh = c.newness_score("2026-07", 45, now=now)
    old = c.newness_score("2026-01", 45, now=now)
    assert fresh > old
    assert c.newness_score("", 45, now=now) == 0
    assert 90 <= fresh <= 100


def test_composite_score_weights():
    scores = {"newness": 100, "novelty": 0, "relevance": 0}
    assert c.composite_score(scores, {"newness": 0.3, "novelty": 0.35, "relevance": 0.35}) == 30.0


def test_composite_includes_credibility():
    w = {"newness": 0.25, "novelty": 0.3, "relevance": 0.3, "credibility": 0.15}
    assert c.composite_score({"credibility": 100}, w) == 15.0
    assert c.composite_score({"credibility": 0}, w) == 0.0


def test_credibility_of_from_source_rank():
    assert c.credibility_of({"source_rank": 80}) == 80.0
    assert c.credibility_of({}) == 50.0  # unknown source -> neutral default


def test_credibility_corroboration_bonus():
    two = [{"url": "https://a"}, {"url": "https://b"}]
    assert c.credibility_of({"source_rank": 60, "corroborating_sources": two}) == 70.0  # +2*5
    # capped at 100
    many = [{"url": f"https://{i}"} for i in range(10)]
    assert c.credibility_of({"source_rank": 95, "corroborating_sources": many}) == 100.0


def test_resolve_redirects_skips_non_shortener():
    # a non-shortener URL is returned unchanged with no network call
    assert c.resolve_redirects("https://blog.example.com/post") == "https://blog.example.com/post"


def test_validate_entry_ok_and_errors():
    assert c.validate_entry(make_entry()) == []
    assert any("missing" in e for e in c.validate_entry({"topic": "ai-research"}))
    # domain is free-text now — any string is valid
    assert c.validate_entry(make_entry(domain="Any Free Domain")) == []
    assert any("unknown topic" in e for e in c.validate_entry(make_entry(topic="nope")))
    # lessons, if provided, must be a list
    bad = make_entry(lessons="not-a-list")
    assert any("lessons must be a list" in e for e in c.validate_entry(bad))


def test_validate_entry_rejects_security_fields_on_research_topics():
    """Threat/Conditions/Mitigations/prior_art are security-disclosure fields.
    An ai-research entry that populates them mis-shapes the site render —
    reject at merge time so the analyzer prompt is corrected, not silently
    tolerated."""
    for field in ("threat", "conditions", "mitigations", "prior_art"):
        bad = make_entry(topic="ai-research", **{field: "some value"})
        errs = c.validate_entry(bad)
        assert any(f"'{field}'" in e for e in errs), \
            f"validate_entry did not flag {field} on ai-research: {errs}"


def test_validate_entry_allows_security_fields_on_security_topics():
    for topic in ("ai-security", "product-security"):
        good = make_entry(
            topic=topic,
            domain="Prompt Injection" if topic == "ai-security" else "Application Security",
            threat="Attacker can steer tool selection via injected content.",
            conditions="Agent has tools with side effects; retrieval includes untrusted docs.",
            mitigations="Human approval on irreversible actions; least-privilege tool scopes.",
        )
        assert c.validate_entry(good) == [], (
            f"security fields should be valid on {topic}: got {c.validate_entry(good)}"
        )


def test_parse_month():
    assert c.parse_month("2026-07").year == 2026
    assert c.parse_month("2026-07-15").day == 15
    assert c.parse_month("garbage") is None


def test_add_candidates_dedup(sandbox):
    cand = {"id": "x1", "title": "A finding", "source_url": "https://a.com/x"}
    dup = {"id": "x2", "title": "A finding!", "source_url": "https://a.com/x/"}
    added = c.add_candidates([cand, dup])
    assert len(added) == 1
    # re-adding the same url is a no-op
    assert c.add_candidates([cand]) == []
    assert len(c.load_candidates()) == 1


def test_add_candidates_skips_pooled(sandbox):
    pool = c.load_pool("ai-security")
    pool["entries"].append(
        make_entry(topic="ai-security", domain="Prompt Injection", source_url="https://a.com/known")
    )
    c.save_pool("ai-security", pool)
    assert (
        c.add_candidates([{"id": "n", "title": "New", "source_url": "https://a.com/known"}]) == []
    )


# --- News-lane gate --------------------------------------------------------
def _news_entry(**over):
    """Fresh news-shaped entry for gate testing. Track A (research) items
    have novelty/relevance scores; news items don't, so we deliberately keep
    them off unless a test wants to prove the gate ignores them."""
    from datetime import UTC, datetime, timedelta

    base = {
        "topic": "ai-security",
        "domain": "MCP & Tools",
        "title": "MCP 2026-07-28 spec drops stateful core for stateless HTTP",
        "summary": "The new spec targets serverless deployments.",
        "takeaway": "MCP is now HTTP-first — check your existing servers.",
        "source_url": "https://modelcontextprotocol.io/spec",
        "source_id": "rss:mcp-spec",
        "published": (datetime.now(UTC) - timedelta(days=3)).strftime("%Y-%m-%d"),
    }
    base.update(over)
    return base


def test_news_denylist_hard_hits():
    """Stock, consumer noise, and hype fire the deny list unconditionally."""
    for title in [
        "Nvidia stock jumps 4% on AI hype",
        "OpenAI $10B valuation of $X — Wall Street analysts weigh in",
        "ChatGPT tips: 5 prompts to try for productivity",
        "AGI is here — why LLMs are coming for your job",
    ]:
        # Neutralize the fixture summary/takeaway so the assertion is on the
        # title alone; hard hits fire regardless, but keep the intent obvious.
        entry = _news_entry(title=title, summary="", takeaway="")
        assert c.news_denylist_hit(entry), title


def test_news_denylist_puff_with_technical_rescue():
    """Business-media puff terms only fire when no technical term co-occurs."""
    # Puff, no technical term anywhere → drop.
    puff_only = _news_entry(
        title="Microsoft signs cloud partnership with Palantir",
        summary="A commercial cloud agreement across sectors.",
        takeaway="",
    )
    assert c.news_denylist_hit(puff_only)
    # Puff + technical rescue → pass.
    rescued = _news_entry(
        title="Anthropic signs deal with former NSA cryptographer to lead red team",
        summary="", takeaway="",
    )
    assert not c.news_denylist_hit(rescued)


def test_news_denylist_lets_real_news_through():
    """None of the sample newsletter stories fire the deny list."""
    for title in [
        "Kimi K3 ships full weights",
        "MCP 2026-07-28 spec drops stateful core for stateless HTTP",
        "Gemini Robotics launches with whole-body humanoid control models",
        "Anthropic caught its own models breaching containment",
    ]:
        assert not c.news_denylist_hit(_news_entry(title=title)), title


def test_is_news_curated_requires_news_track_source():
    """A perfectly on-topic, fresh entry from a research-only source doesn't
    reach the news lane. It has to be sourced from a news-tagged feed."""
    conf = c.load_config()
    entry = _news_entry(source_id="rss:research-only")
    research_source = {"rss:research-only": {"track": "research", "tier": "high"}}
    both_source = {"rss:research-only": {"track": "both", "tier": "high"}}
    news_source = {"rss:research-only": {"track": "news", "tier": "high"}}
    assert not c.is_news_curated(entry, conf, research_source)
    assert c.is_news_curated(entry, conf, both_source)
    assert c.is_news_curated(entry, conf, news_source)


def test_is_news_curated_rejects_low_tier():
    conf = c.load_config()
    entry = _news_entry(source_id="rss:noname")
    sources = {"rss:noname": {"track": "news", "tier": "low"}}
    assert not c.is_news_curated(entry, conf, sources)


def test_is_news_curated_rejects_stale():
    conf = c.load_config()
    entry = _news_entry(published="2020-01-01", source_id="rss:news")
    sources = {"rss:news": {"track": "news", "tier": "high"}}
    assert not c.is_news_curated(entry, conf, sources)


def test_is_news_curated_enforces_7_day_display_window():
    """The news lane shows only the last 7 days — anything older is not news."""
    from datetime import UTC, datetime, timedelta

    conf = c.load_config()
    sources = {"rss:news": {"track": "news", "tier": "high"}}
    day_6 = (datetime.now(UTC) - timedelta(days=6)).strftime("%Y-%m-%d")
    day_8 = (datetime.now(UTC) - timedelta(days=8)).strftime("%Y-%m-%d")
    assert c.is_news_curated(_news_entry(published=day_6, source_id="rss:news"),
                             conf, sources)
    assert not c.is_news_curated(_news_entry(published=day_8, source_id="rss:news"),
                                 conf, sources)


def test_is_news_curated_hn_standalone_needs_100_points():
    """A story discovered only via HN needs a higher points bar to stand
    alone as news. Corroboration from another source removes the bar."""
    conf = c.load_config()
    sources = {"rss:hn": {"track": "news", "tier": "high"}}

    weak = _news_entry(source_id="rss:hn", discovered_via="hackernews",
                       signals={"hn_points": 50})
    assert not c.is_news_curated(weak, conf, sources)

    strong = _news_entry(source_id="rss:hn", discovered_via="hackernews",
                         signals={"hn_points": 150})
    assert c.is_news_curated(strong, conf, sources)

    # Below floor but corroborated by another source → passes.
    corroborated = _news_entry(source_id="rss:hn", discovered_via="hackernews",
                               signals={"hn_points": 50},
                               corroborating_sources=[{"source_name": "OpenAI Blog"}])
    assert c.is_news_curated(corroborated, conf, sources)


def test_is_news_curated_rejects_denylist_stock_story():
    """Even from a valid news source, a stock story never reaches the lane."""
    conf = c.load_config()
    entry = _news_entry(
        title="Nvidia stock jumps 4% after AI benchmark leak",
        source_id="rss:news",
    )
    sources = {"rss:news": {"track": "news", "tier": "high"}}
    assert not c.is_news_curated(entry, conf, sources)


def test_is_news_curated_rejects_untopiced():
    """The classifier assigns `topic` at ingest; without it, the item is out."""
    conf = c.load_config()
    entry = _news_entry(topic=None, source_id="rss:news")
    sources = {"rss:news": {"track": "news", "tier": "high"}}
    assert not c.is_news_curated(entry, conf, sources)
