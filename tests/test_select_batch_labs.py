"""The lab lane: recent, on-thesis posts from the major AI labs get batch slots
(Rohan, 2026-10-24), and leftover ones get a news brief, not the backlog."""

from __future__ import annotations

from datetime import timedelta

import common
import prefilter
import pytest
import select_batch
from test_prefilter import _cand
from test_select_batch import cands, conf

HOSTS = ["openai.com", "anthropic.com", "microsoft.com/en-us/research", "huggingface.co/blog"]
TERMS = ["securing", "security", "red team", "vulnerability", "safety", "evals"]
LAB = {"batch_lab_max": 2, "batch_lab_per_source": 1, "batch_lab_hosts": HOSTS}


def today(days_ago: int = 0) -> str:
    return (common.utcnow().date() - timedelta(days=days_ago)).isoformat()


def lab(i: int, title: str, url: str, days_ago: int = 0, **over) -> dict:
    return _cand(
        id=f"lab{i}",
        title=title,
        source_url=url,
        article_url=url,
        published=today(days_ago),
        source_id=over.pop("source_id", f"rss:{url.split('/')[2]}"),  # one feed per host
        source_rank=over.pop("source_rank", 30.0),  # below the neutral pile: no lane, no slot
        **over,
    )


@pytest.fixture
def table() -> prefilter.KeywordTable:
    return prefilter.KeywordTable(keywords={}, excluded=(), catch_alls=("AI Security",))


def lab_conf(cap: int = 3, margin: int = 0, **extra) -> common.Config:
    return conf(cap, margin, **{**LAB, "batch_lab_terms": TERMS, **extra})


@pytest.mark.parametrize(
    "url, hit",
    [
        ("https://openai.com/index/securing-x", True),
        ("https://alignment.openai.com/post", True),  # subdomain
        ("https://www.anthropic.com/research/x", True),  # www. stripped
        ("https://notopenai.com/securing", False),  # whole labels only
        ("https://www.microsoft.com/en-us/research/blog/x", True),  # path prefix
        ("https://www.microsoft.com/en-us/store/x", False),
        ("https://huggingface.co/papers/2610.1", False),  # papers are not the blog
        ("https://www.microsoft.com/en-us/researchx/a", False),  # whole path segments
        ("https://huggingface.co/blogs/x", False),
        ("https://openai.com./index/x", True),  # trailing-dot host
        ("https://OpenAI.com:443/index/x", True),
        ("http://[bad/x", False),  # unparseable: not a lab post, never a crash
    ],
)
def test_lab_source_matches_hosts_by_label_and_path(url, hit):
    assert select_batch.lab_source({"article_url": url}, lab_conf()) is hit


def test_lab_relevance_needs_a_security_or_safety_term():
    c = lab_conf()
    on = lab(1, "Securing our frontier model training environment", "https://openai.com/a")
    off = lab(2, "Uber brings ChatGPT Work to all employees", "https://openai.com/b")
    assert select_batch.lab_relevant(on, c) and not select_batch.lab_relevant(off, c)
    assert not select_batch.lab_relevant(on, conf(3, 0, **LAB))  # no terms: lane off


@pytest.mark.parametrize(
    "title, hit",
    [
        ("New security research", True),
        ("Our evals for agents", True),
        ("Trading securities with GPT", False),  # not "security"
        ("Faster retrievals at scale", False),  # not "evals"
    ],
)
def test_lab_terms_match_whole_words(title, hit):
    post = lab(1, title, "https://openai.com/a")
    assert select_batch.lab_relevant(post, lab_conf()) is hit


def test_relevant_lab_posts_get_lane_slots_ahead_of_the_deal(sandbox, table):
    labs = [
        lab(1, "Securing our frontier model training environment", "https://openai.com/a"),
        lab(2, "Red team findings on model safety", "https://openai.com/b"),  # same source
        lab(3, "Vulnerability research at scale", "https://www.anthropic.com/c", 1),
        lab(4, "Uber brings ChatGPT Work to all employees", "https://openai.com/d"),
        lab(5, "Old security post", "https://www.anthropic.com/e", 30),  # not recent
    ]
    batch, backlog = select_batch.select([*cands(6), *labs], lab_conf(), table)
    lane = [x["id"] for x in batch if x.get("batch_priority") == "lab"]
    assert lane == ["lab1", "lab3"]  # per-source cap 1, newest first, in batch_lab_max 2
    deep = [x for x in batch if x.get("batch_tier") != "news"]
    assert [x["id"] for x in deep][:2] == lane and len(deep) == 3
    ids = [x["id"] for x in batch + backlog]
    assert sorted(ids) == sorted(x["id"] for x in [*cands(6), *labs])


def test_leftover_lab_posts_get_a_news_brief(sandbox, table):
    labs = [
        lab(1, "Securing our frontier model training environment", "https://openai.com/a"),
        lab(2, "Red team findings on model safety", "https://openai.com/b"),
        lab(3, "Uber brings ChatGPT Work to all employees", "https://openai.com/d"),
    ]
    c = lab_conf(max_news_per_run=5, batch_news_per_source=5)
    batch, news, _ = select_batch.select_tiers([*cands(6), *labs], c, table)
    assert [x["id"] for x in batch if x.get("batch_priority") == "lab"] == ["lab1"]
    assert [(x["id"], x["batch_news"]["reason"]) for x in news] == [("lab2", "lab")]


def test_a_catch_all_drop_of_a_relevant_lab_post_is_rescued(sandbox, table):
    url = "https://openai.com/index/cloudflare-vulnerability-discovery"
    post = lab(1, "Cloudflare links vulnerability discovery to defense", url)
    post["guess_label"] = "AI Security"  # a catch-all with no marker: prefilter drops it
    other = lab(2, "Vendor stock rallies", "https://other.example/x", guess_label="AI Security")
    batch, backlog = select_batch.select([*cands(2), post, other], lab_conf(), table)
    assert "lab1" in [x["id"] for x in batch]
    dropped = {x["id"]: x["prefilter"]["reason"] for x in backlog if x.get("prefilter")}
    assert dropped.get("lab2", "").startswith("catch-all")  # only lab posts are rescued


def test_without_a_lab_lane_size_the_batch_is_unchanged(sandbox, table):
    labs = [lab(1, "Securing our frontier model training environment", "https://openai.com/a")]
    off = conf(3, 0, batch_lab_hosts=HOSTS, batch_lab_terms=TERMS)
    batch, _ = select_batch.select([*cands(6), *labs], off, table)
    assert not any(x.get("batch_priority") == "lab" for x in batch)


def test_with_the_lane_off_lab_posts_get_no_briefs_either(sandbox, table):
    labs = [lab(1, "Securing our frontier model training environment", "https://openai.com/a")]
    off = conf(3, 0, batch_lab_hosts=HOSTS, batch_lab_terms=TERMS, max_news_per_run=5)
    _, news, _ = select_batch.select_tiers([*cands(6), *labs], off, table)
    assert news == []


def test_a_rescued_lab_post_already_in_the_pools_stays_dropped(sandbox, table, monkeypatch):
    url = "https://openai.com/index/cloudflare-vulnerability-discovery"
    post = lab(1, "Cloudflare links vulnerability discovery to defense", url)
    post["guess_label"] = "AI Security"
    monkeypatch.setattr(common, "known_urls", lambda: {common.normalize_url(url)})
    batch, backlog = select_batch.select([*cands(2), post], lab_conf(), table)
    assert "lab1" not in [x["id"] for x in batch]
    assert [x["id"] for x in backlog if x.get("prefilter")] == ["lab1"]


def test_a_story_the_ledger_holds_gets_no_lab_slot_or_brief(sandbox, table, monkeypatch):
    post = lab(1, "Securing our frontier model training environment", "https://openai.com/a")
    held = select_batch.nw.Signal(markers=frozenset(), matches=(), sources=1, known=True)
    monkeypatch.setattr(select_batch, "story_signals", lambda pool, *a: [
        held if x["id"] == "lab1" else None for x in pool
    ])  # fmt: skip
    c = lab_conf(max_news_per_run=5)
    fresh = [  # outrank the post in the deal, one source each: only the lane could take it
        {**x, "source_id": f"rss:filler{i}"} for i, x in enumerate(cands(6, published=today()))
    ]
    batch, news, _ = select_batch.select_tiers([*fresh, post], c, table)
    assert "lab1" not in [x["id"] for x in batch + news]


# --- the efficiency lane (F9) --------------------------------------------------
EFF_TERMS = ["prompt caching", "token usage", "subagent", "harness"]
EFF = {"batch_eff_max": 3, "batch_eff_per_source": 1, "batch_eff_terms": EFF_TERMS}


def eff(i: int, title: str, host: str = "", days_ago: int = 0, **over) -> dict:
    host = host or f"eff{i}.example"
    return lab(i, title, f"https://{host}/p{i}", days_ago, source_id=f"rss:{host}", **over)


def eff_ids(batch: list[dict]) -> list[str]:
    return [x["id"] for x in batch if x.get("batch_priority") == "efficiency"]


def test_the_efficiency_lane_fills_with_recent_term_matches(sandbox, table):
    posts = [
        eff(1, "Cutting token usage with prompt caching"),
        eff(2, "Subagent patterns that save time", days_ago=1),
        eff(3, "Building a harness that verifies itself", days_ago=2),
        eff(4, "More prompt caching notes", days_ago=3),  # a fourth: over batch_eff_max
        eff(5, "Weekend reading list"),  # no term
        eff(6, "Old harness post", days_ago=30),  # not recent
    ]
    batch, backlog = select_batch.select([*cands(4), *posts], conf(6, 0, **EFF), table)
    assert eff_ids(batch) == ["lab1", "lab2", "lab3"]
    assert {x["id"] for x in backlog} >= {"lab4", "lab6"}  # over the lane size, and stale


def test_the_efficiency_lane_caps_each_source(sandbox, table):
    posts = [
        eff(1, "Prompt caching in practice", host="blog.example"),
        eff(2, "Token usage of a subagent", host="blog.example", days_ago=1),
        eff(3, "A harness for evals", host="other.example", days_ago=2),
    ]
    batch, _ = select_batch.select([*cands(3), *posts], conf(6, 0, **EFF), table)
    assert eff_ids(batch) == ["lab1", "lab3"]


def test_the_efficiency_lane_is_empty_without_matches_or_a_lane_size(sandbox, table):
    posts = [eff(1, "Weekend reading list"), eff(2, "Notes on a new model")]
    batch, _ = select_batch.select([*cands(3), *posts], conf(6, 0, **EFF), table)
    assert eff_ids(batch) == []
    match = [eff(3, "Prompt caching in practice")]
    off_conf = conf(6, 0, **{**EFF, "batch_eff_max": 0})
    off, _ = select_batch.select([*cands(3), *match], off_conf, table)
    assert eff_ids(off) == []


def test_the_efficiency_lane_never_takes_what_an_earlier_lane_took(sandbox, table):
    both = lab(1, "Securing our harness against prompt injection", "https://openai.com/a")
    other = eff(2, "Prompt caching in practice")
    extra = {**LAB, "batch_lab_terms": TERMS, **EFF}
    batch, _ = select_batch.select([*cands(3), both, other], conf(6, 0, **extra), table)
    tags = {x["id"]: x.get("batch_priority") for x in batch}
    assert tags["lab1"] == "lab" and tags["lab2"] == "efficiency"
    assert [x["id"] for x in batch].count("lab1") == 1
