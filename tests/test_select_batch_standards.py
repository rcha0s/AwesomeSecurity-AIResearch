"""The standards lane (F10, ISC-57): releases from OWASP GenAI, NIST, CoSAI, the MCP
spec and NAIC get batch slots right after the must-not-miss lane. OWASP's Agent
Control Standard (2026-09-01) was captured and then sank below the cut."""

from __future__ import annotations

import common
import prefilter
import pytest
import select_batch
from test_select_batch import cands, conf
from test_select_batch_labs import lab, today

HOSTS = ["genai.owasp.org", "nist.gov", "coalitionforsecureai.org", "naic.org"]
TERMS = ["standard", "framework", "guidance", "ai"]
MCP = "rss:mcp-spec-releases"
STD = {
    "batch_std_max": 2,
    "batch_std_per_source": 1,
    "batch_std_hosts": HOSTS,
    "batch_std_terms": TERMS,
    "batch_std_sources": [MCP],
}


@pytest.fixture
def table() -> prefilter.KeywordTable:
    return prefilter.KeywordTable(keywords={}, excluded=(), catch_alls=("AI Security",))


def std_conf(cap: int = 3, margin: int = 0, **extra) -> common.Config:
    return conf(cap, margin, **{**STD, **extra})


def std(i: int, title: str, url: str, days_ago: int = 0, **over) -> dict:
    return lab(i, title, url, days_ago, **over)


def ids(batch: list[dict], tag: str = "standard") -> list[str]:
    return [x["id"] for x in batch if x.get("batch_priority") == tag]


ACS = ("Introducing the Agent Control Standard v0.1.0", "https://genai.owasp.org/2026/09/acs/")


def test_an_owasp_standard_gets_a_slot_even_with_a_full_kev_ghsa_lane(sandbox, table):
    kev = [
        std(
            10 + i,
            f"CISA KEV entry {i}",
            f"https://kev{i}.example/x",
            source_id="kev_json:cisa",
            source_rank=90.0,
        )
        for i in range(6)
    ]
    acs = std(1, *ACS)
    c = std_conf(5, 0, batch_priority_max=4, batch_priority_per_source=4)
    batch, _ = select_batch.select([*cands(6), *kev, acs], c, table)
    assert len(ids(batch, "kev")) == 4  # the must-not-miss lane is full
    assert ids(batch) == ["lab1"]


def test_standards_come_before_labs_and_are_tagged(sandbox, table):
    labs = [lab(2, "Securing our frontier model", "https://openai.com/a")]
    c = std_conf(3, 0, batch_lab_max=2, batch_lab_per_source=1, batch_lab_hosts=["openai.com"],
                 batch_lab_terms=["securing"])  # fmt: skip
    batch, _ = select_batch.select([*cands(6), std(1, *ACS), *labs], c, table)
    lane = [x["id"] for x in batch if x.get("batch_priority")]
    assert lane == ["lab1", "lab2"]
    assert ids(batch, "lab") == ["lab2"]


@pytest.mark.parametrize(
    "url, title, hit",
    [
        ("https://genai.owasp.org/x", "Agent Control Standard released", True),
        ("https://genai.owasp.org/x", "Meet us at the summit", False),  # no term
        ("https://www.nist.gov/news/x", "NIST AI risk framework update", True),
        ("https://csrc.nist.gov/pubs/x", "Guidance on controls", True),  # subdomain
        ("https://notnist.gov/x", "NIST AI standard", False),  # whole labels only
        ("https://content.naic.org/x", "Model bulletin guidance", True),
        ("https://example.com/x", "A new AI standard", False),
    ],
)
def test_hosts_match_by_label_and_need_a_term(url, title, hit):
    assert select_batch.std_relevant(std(1, title, url), std_conf()) is hit


def test_the_mcp_spec_feed_needs_no_term():
    release = std(1, "2026-11-25", "https://spec.example/r", source_id=MCP)
    assert select_batch.std_relevant(release, std_conf())
    assert not select_batch.std_relevant(release, conf(3, 0))  # lane unconfigured


def test_lane_is_recent_per_source_capped_and_sized(sandbox, table):
    posts = [
        std(1, *ACS),
        std(2, "NIST AI guidance draft", "https://www.nist.gov/a", 1),
        std(3, "CoSAI framework for agents", "https://www.coalitionforsecureai.org/a", 2),
        std(4, "NIST framework again", "https://www.nist.gov/b", 3),  # per-source cap 1
        std(5, "Old OWASP standard", "https://genai.owasp.org/old/", 30),  # not recent
    ]
    batch, backlog = select_batch.select([*cands(6), *posts], std_conf(), table)
    assert ids(batch) == ["lab1", "lab2"]  # batch_std_max 2, newest first
    assert sorted(x["id"] for x in batch + backlog) == sorted(x["id"] for x in [*cands(6), *posts])


def test_leftover_standards_get_a_news_brief(sandbox, table):
    posts = [
        std(1, *ACS),
        std(2, "NIST AI guidance draft", "https://www.nist.gov/a", 1),
        std(3, "CoSAI framework for agents", "https://www.coalitionforsecureai.org/a", 2),
    ]
    c = std_conf(3, 0, batch_std_max=1, max_news_per_run=5, batch_news_per_source=5)
    batch, news, _ = select_batch.select_tiers([*cands(6), *posts], c, table)
    assert ids(batch) == ["lab1"]
    assert [(x["id"], x["batch_news"]["reason"]) for x in news] == [
        ("lab2", "standard"),
        ("lab3", "standard"),
    ]


def test_with_the_lane_off_nothing_is_tagged(sandbox, table):
    off = conf(3, 0, batch_std_hosts=HOSTS, batch_std_terms=TERMS, max_news_per_run=5)
    batch, news, _ = select_batch.select_tiers([*cands(6), std(1, *ACS)], off, table)
    assert ids(batch) == [] and news == []


def test_the_real_config_names_the_lane():
    real = common.load_config().limits
    assert real["batch_std_max"] > 0 and real["batch_std_per_source"] >= 1
    assert "genai.owasp.org" in real["batch_std_hosts"]
    assert all(real.get(k) for k in ("batch_std_terms", "batch_std_sources"))
    assert today() >= "2026-01-01"


STRICT = {
    "batch_std_strict_hosts": ["nist.gov"],
    "batch_std_topic_terms": ["ai", "artificial intelligence", "cybersecurity", "agent"],
    "batch_std_pub_terms": ["standard", "framework", "guidance", "draft"],
}


@pytest.mark.parametrize(
    "title, hit",
    [
        ("NIST releases draft AI risk management profile", True),
        ("NIST publishes cybersecurity framework guidance", True),
        ("NIST unveils new time standard for atomic clocks", False),  # no AI / cyber term
        ("NIST AI researchers win an award", False),  # no publication term
        ("Security of the lab building", False),
    ],
)
def test_nist_needs_a_topic_term_and_a_publication_term(title, hit):
    post = std(1, title, "https://www.nist.gov/news-events/news/x")
    assert select_batch.std_relevant(post, std_conf(**STRICT)) is hit


def test_a_nist_time_standard_release_takes_no_slot(sandbox, table):
    clock = std(2, "NIST releases new time standard", "https://www.nist.gov/news-events/news/t")
    ai = std(3, "NIST draft guidance on AI agent hijacking", "https://www.nist.gov/news/a", 1)
    c = std_conf(3, 0, **STRICT)
    batch, _ = select_batch.select([*cands(6), clock, ai], c, table)
    assert ids(batch) == ["lab3"]


def test_a_catch_all_drop_of_a_standards_post_is_rescued(sandbox):
    real = prefilter.load_keywords()
    label = next(iter(real.catch_alls))
    acs = std(1, *ACS, guess_label=label)
    other = std(2, "Vendor stock rallies", "https://other.example/x", guess_label=label)
    batch, backlog = select_batch.select([*cands(2), acs, other], std_conf(), real)
    assert ids(batch) == ["lab1"]
    dropped = {x["id"]: x["prefilter"]["reason"] for x in backlog if x.get("prefilter")}
    assert dropped.get("lab2", "").startswith("catch-all")  # only standards posts are rescued


def test_a_rescued_standards_post_already_in_the_pools_stays_dropped(sandbox, monkeypatch):
    real = prefilter.load_keywords()
    acs = std(1, *ACS, guess_label=next(iter(real.catch_alls)))
    monkeypatch.setattr(common, "known_urls", lambda: {common.normalize_url(ACS[1])})
    batch, backlog = select_batch.select([*cands(2), acs], std_conf(), real)
    assert "lab1" not in [x["id"] for x in batch]
    assert [x["id"] for x in backlog if x.get("prefilter")] == ["lab1"]
