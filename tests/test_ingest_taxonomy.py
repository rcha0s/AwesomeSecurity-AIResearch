"""The ingest router emits taxonomy IDs without changing what it ingests.

`aggregate.classify_domain` (the sources.yaml keyword router) still makes every
ingest decision and topic guess; only the emitted `guess_domain` became a
taxonomy ID (the router label moved to `guess_label`). These tests replay the
router over the real pool + archive text to pin that."""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

import aggregate
import common as c
import ingest_json_feeds as ijf
import pytest
import taxonomy as tx

REPO = Path(__file__).resolve().parent.parent
RULES = c.load_yaml(c.SOURCES_FILE)["classification"]
# {label: topic} frozen from origin/main's pre-taxonomy topic_for_domain (generated
# once, committed): every router + subtype label, every legacy key, the old TOPICS
# display names and every registered source's domain label. Not computed here.
FROZEN = json.loads((REPO / "tests" / "fixtures" / "legacy_label_topics.json").read_text())
MAIN_TOPIC = FROZEN["labels"]
# Router classes added after the taxonomy (2026-10-23 catch-alls, checked last):
# taxonomy IDs, so their topic is the taxonomy's, not a frozen legacy guess.
CATCH_ALLS = ("ais.agent-security", "ps.appsec")
# Efficiency classes (F9), also taxonomy IDs, checked after every legacy class and
# before the catch-alls.
EFFICIENCY = ("air.cost-efficiency", "air.work-efficiency")
FEEDS = [
    {"name": "strict", "strict": True, "domains": ["AI Security"]},
    {"name": "fallback", "domains": ["Web Application Security"]},
    {"name": "ambiguous", "domains": ["AI Security", "Mobile Security"]},
    {"name": "none", "domains": []},
]


def _corpus() -> list[dict]:
    entries = [
        e
        for t in c.TOPICS
        for e in json.loads((REPO / "data" / f"{t}.json").read_text())["entries"]
    ]
    entries += json.loads((REPO / "data" / "archive.json").read_text())
    return [{"link": e["source_url"], "title": e["title"], "summary": e.get("summary") or ""}
            for e in entries]  # fmt: skip


@pytest.mark.parametrize("feed", FEEDS, ids=lambda f: f["name"])
def test_router_decisions_are_unchanged_and_domains_are_ids(feed):
    corpus = _corpus()
    assert len(corpus) > 400
    kept = 0
    for item in corpus:
        blob = f"{item['title']} {c.clean_summary(item['summary'])}"
        fallback = [] if feed.get("strict") else feed["domains"]
        label = aggregate.classify_domain(blob, RULES, fallback)
        cand = aggregate.build_candidate(item, feed, RULES)
        assert (cand is None) == (label is None)  # same ingest decision
        if cand is None:
            continue
        kept += 1
        assert cand["guess_label"] == label
        if label in CATCH_ALLS + EFFICIENCY:
            assert cand["guess_topic"] == tx.get().domains[label].topic
        else:
            assert cand["guess_topic"] == MAIN_TOPIC[label]  # main's topic guess, frozen
        assert tx.get().is_valid(cand["guess_domain"], cand["guess_topic"])
    assert kept  # the replay exercised the keep path


def test_the_catch_alls_come_last_so_no_earlier_label_changes():
    labels = list(RULES["domains"])
    assert labels[-len(CATCH_ALLS) :] == list(CATCH_ALLS)
    before = labels[: -len(CATCH_ALLS)]
    assert before[-len(EFFICIENCY) :] == list(EFFICIENCY)
    assert all(label in MAIN_TOPIC for label in before[: -len(EFFICIENCY)])


def test_efficiency_posts_stage_with_an_ai_research_guess():
    feed = {"name": "x", "domains": []}
    item = {"link": "https://e.com/a", "title": "How we cut token usage with prompt caching",
            "summary": "A look at cost per task."}  # fmt: skip
    cand = aggregate.build_candidate(item, feed, RULES)
    assert cand["guess_label"] == "air.cost-efficiency"
    assert (cand["guess_topic"], cand["guess_domain"]) == ("ai-research", "air.cost-efficiency")
    item = {"link": "https://e.com/b", "title": "Running parallel agents", "summary": ""}
    assert aggregate.build_candidate(item, feed, RULES)["guess_domain"] == "air.work-efficiency"


def _kev(name: str, desc: str = "") -> dict:
    return {
        "cveID": "CVE-2026-9",
        "vendorProject": "Acme",
        "product": "Widget",
        "vulnerabilityName": name,
        "shortDescription": desc,
        "dateAdded": "2026-07-10",
    }


@pytest.mark.parametrize(
    "name, want",
    [
        ("Acme Widget Improper Input Validation", "ps.appsec"),  # fallback only
        ("Android Framework Use-After-Free", "ps.mobile"),
        ("Acme Widget SQL Injection", "ps.appsec"),
    ],
)
def test_kev_candidates_carry_product_security_ids(name, want):
    src = {"id": "kev_json:x", "name": "CISA KEV", "rank": 75.0, "topics": [], "domains": []}
    data = {"vulnerabilities": [_kev(name)]}
    (cand,) = ijf.kev_candidates(data, src, RULES, c.utcnow() - timedelta(days=31))
    assert cand["guess_topic"] == "product-security" and cand["guess_domain"] == want


def test_hf_paper_candidates_carry_ids():
    paper = {"id": "2607.00001", "title": "Jailbreak and prompt injection of LLM agents"}
    paper.update(summary="an attack on llm agents", publishedAt="2026-07-14T00:00:00.000Z")
    item = {"paper": paper}
    src = {"id": "hf_papers:x", "name": "HF Daily Papers", "rank": 55.0, "topics": []}
    out = ijf.hf_candidates([item], src, RULES, c.utcnow() - timedelta(days=31))
    assert out and out[0]["guess_domain"] == "ais.prompt-injection"


def test_domain_hint_falls_back_to_a_valid_default():
    assert tx.domain_hint("product-security", "nothing here", default="ps.mobile") == "ps.mobile"
    assert tx.domain_hint("product-security", "nothing", default="Web App") == "ps.appsec"


def test_frozen_table_covers_every_label_the_router_can_emit():
    labels = set(RULES["domains"]) | {s for sub in RULES["subtypes"].values() for s in sub}
    sources = json.loads((REPO / "data" / "sources.json").read_text())
    labels |= {d for src in sources for d in src.get("domains") or []}
    labels |= set(c.LEGACY_DOMAIN_TO_TOPIC)
    labels -= set(CATCH_ALLS + EFFICIENCY)  # taxonomy IDs: the taxonomy decides their topic
    assert labels <= set(MAIN_TOPIC), sorted(labels - set(MAIN_TOPIC))
    assert all(tx.get().domains.get(label) for label in CATCH_ALLS + EFFICIENCY)
    assert len(MAIN_TOPIC) >= 50


@pytest.mark.parametrize("label", sorted(MAIN_TOPIC))
def test_topic_for_a_legacy_label_matches_main_exactly(label):
    """Nulls included: a label main didn't know must not start guessing a topic."""
    assert c.topic_for_domain(label) == MAIN_TOPIC[label]
