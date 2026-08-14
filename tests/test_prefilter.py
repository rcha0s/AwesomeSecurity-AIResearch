"""Tests for scripts/prefilter.py — the deterministic funnel that sorts
candidates into dropped / routed / filtered before any LLM sees them."""

from __future__ import annotations

import json
from pathlib import Path

import common
import prefilter
import pytest


# ------------------------------------------------------------------ fixtures

def _cand(**over) -> dict:
    """Build a minimal candidate — the shape the ingestors write."""
    base = {
        "id": over.get("id", "cand-1"),
        "discovered_via": "rss",
        "title": "A generic title",
        "source_name": "arXiv cs.AI",
        "source_url": "https://example.com/a",
        "article_url": "https://example.com/a",
        "tweet_url": None,
        "author": None,
        "published": "2026-08-10",
        "date": "2026-08",
        "excerpt": "A short summary.",
        "raw_path": None,
        "guess_topic": None,
        "guess_domain": None,
        "guess_subtype": None,
        "source_id": "rss:example",
        "source_rank": 55.0,
        "source_topics": ["ai-research"],
        "retrieved_at": "2026-08-10T00:00:00+00:00",
    }
    base.update(over)
    return base


@pytest.fixture
def tiny_table() -> prefilter.ClusterTable:
    """Tiny keyword table so unit tests don't depend on the real YAML."""
    return prefilter.ClusterTable(
        keywords={
            "B": ("agent harness", "multi-agent", "tool schema"),
            "E": ("prompt injection", "jailbreak", "memory poisoning"),
            "F": ("mcp", "model context protocol"),
        },
        excluded=("clinical automl", "autonomous driving"),
    )


# ------------------------------------------------------------------ unit tests

def test_haystack_lowercases_and_joins():
    cand = _cand(title="RAG For Everyone", excerpt="A summary.",
                 guess_domain="AI Security", guess_subtype="Prompt Injection")
    hay = prefilter.haystack(cand)
    assert "rag for everyone" in hay
    assert "a summary." in hay
    assert "ai security" in hay
    assert "prompt injection" in hay
    # No uppercase leaks.
    assert hay == hay.lower()


def test_score_clusters_counts_hits(tiny_table):
    text = "an mcp server that supports multi-agent orchestration"
    scores = prefilter.score_clusters(text, tiny_table)
    assert scores["B"] == 1
    assert scores["F"] == 1
    assert scores["E"] == 0


def test_best_cluster_prefers_wider_margin(tiny_table):
    text = ("prompt injection is a jailbreak vector against memory poisoning "
            "of an mcp server")
    scores = prefilter.score_clusters(text, tiny_table)
    winner, hits, margin = prefilter.best_cluster(scores)
    assert winner == "E"
    assert hits == 3
    assert margin == 2  # E=3, F=1


def test_best_cluster_returns_none_for_empty_scores(tiny_table):
    scores = prefilter.score_clusters("nothing to see here", tiny_table)
    winner, hits, margin = prefilter.best_cluster(scores)
    assert winner is None
    assert hits == 0
    assert margin == 0


def test_best_cluster_tie_returns_zero_margin(tiny_table):
    text = "mcp meets multi-agent"
    scores = prefilter.score_clusters(text, tiny_table)
    winner, hits, margin = prefilter.best_cluster(scores)
    assert hits == 1
    assert margin == 0  # tie F=1 vs B=1


def test_excluded_hit_returns_matching_term(tiny_table):
    text = "clinical automl over icu vitals"
    assert prefilter.excluded_hit(text, tiny_table) == "clinical automl"


def test_excluded_hit_returns_none_for_clean(tiny_table):
    assert prefilter.excluded_hit("agent harness paper", tiny_table) is None


# ---------------------------------------------------------------- bucket flow

def test_denylist_hit_goes_to_dropped(sandbox, tiny_table):
    stock = _cand(title="Nvidia stock jumps 15% on AI hype")
    result = prefilter.bucket([stock], tiny_table)
    assert len(result.dropped) == 1
    assert len(result.routed) == 0
    assert len(result.filtered) == 0
    assert result.dropped[0]["prefilter"]["reason"] == "denylist"


def test_excluded_term_goes_to_dropped(sandbox, tiny_table):
    med = _cand(title="A clinical automl pipeline for MRI scans")
    result = prefilter.bucket([med], tiny_table)
    assert len(result.dropped) == 1
    assert result.dropped[0]["prefilter"]["reason"].startswith("excluded:")


def test_pool_duplicate_goes_to_dropped(sandbox, tiny_table):
    # Seed the pool with an entry so the candidate collides on URL.
    pool = common.load_pool("ai-security")
    pool["entries"].append({
        "topic": "ai-security", "domain": "MCP & Tools",
        "title": "Existing MCP finding",
        "source_url": "https://example.com/dup",
    })
    common.save_pool("ai-security", pool)
    dup = _cand(title="Different title but same URL",
                source_url="https://example.com/dup",
                article_url="https://example.com/dup")
    result = prefilter.bucket([dup], tiny_table)
    assert len(result.dropped) == 1
    assert result.dropped[0]["prefilter"]["reason"] == "duplicate"


def test_strong_cluster_hint_routes(sandbox, tiny_table):
    # 3 matches on E (prompt injection, jailbreak, memory poisoning) → margin 3.
    cand = _cand(title="Prompt injection, jailbreak, memory poisoning survey")
    result = prefilter.bucket([cand], tiny_table)
    assert len(result.routed) == 1
    r = result.routed[0]
    assert r["prefilter"]["reason"] == "routed"
    assert r["prefilter"]["cluster_hint"] == "E"
    assert r["prefilter"]["cluster_hits"] == 3


def test_weak_hint_goes_to_filtered(sandbox, tiny_table):
    # A single hit — below CLUSTER_MIN_HITS (2). Goes to filtered.
    cand = _cand(title="A study of MCP interoperability")
    result = prefilter.bucket([cand], tiny_table)
    assert len(result.filtered) == 1
    assert result.filtered[0]["prefilter"]["reason"] == "filtered"


def test_tie_goes_to_filtered(sandbox, tiny_table):
    # Both B (agent harness) and E (prompt injection) hit twice → margin 0.
    cand = _cand(title="Agent harness + tool schema meets prompt injection + jailbreak")
    result = prefilter.bucket([cand], tiny_table)
    assert len(result.filtered) == 1
    assert result.filtered[0]["prefilter"]["cluster_margin"] == 0


def test_no_hint_goes_to_filtered(sandbox, tiny_table):
    cand = _cand(title="A completely off-topic robotics paper")
    result = prefilter.bucket([cand], tiny_table)
    assert len(result.filtered) == 1


# ------------------------------------------------ zero false-drops on keepers

def test_zero_false_drops_on_hand_labeled_keepers(sandbox, tiny_table):
    """Nothing that looks like tier-1 security material should be dropped."""
    keepers = [
        _cand(id="k1", title="MCP server SSRF: host-side discovery outside sandbox"),
        _cand(id="k2", title="Agent harness memory poisoning via self-state attack"),
        _cand(id="k3", title="Prompt injection turns a jailbreak into RCE"),
        _cand(id="k4", title="Multi-agent orchestration failure modes"),
    ]
    result = prefilter.bucket(keepers, tiny_table)
    dropped_titles = [d["title"] for d in result.dropped]
    assert dropped_titles == []
    # All either routed or filtered — never silently killed.
    assert len(result.routed) + len(result.filtered) == len(keepers)


# --------------------------------------------------- integration & CLI

def test_load_cluster_keywords_reads_real_yaml():
    """Sanity: the shipped YAML parses and produces non-empty tables."""
    # Point at the tracked file directly; the sandbox fixture (not used here)
    # would otherwise redirect DATA_DIR to a tmp path with no keyword file.
    yaml_path = Path(__file__).resolve().parent.parent / "data" / "cluster_keywords.yaml"
    table = prefilter.load_cluster_keywords(yaml_path)
    # All 13 clusters present.
    assert set(table.keywords) == set("ABCDEFGHIJKLM")
    # None empty.
    for letter, terms in table.keywords.items():
        assert terms, f"cluster {letter} has no keywords"
    assert table.excluded  # some exclusion terms configured


def _seed_keywords(sandbox_path: Path) -> None:
    """Copy the real cluster_keywords.yaml into the sandbox data dir."""
    real = Path(__file__).resolve().parent.parent / "data" / "cluster_keywords.yaml"
    (sandbox_path / "data" / "cluster_keywords.yaml").write_text(real.read_text())


def test_main_writes_three_buckets(sandbox):
    _seed_keywords(sandbox)
    cands = [
        _cand(id="a", title="Nvidia stock jumps"),                        # deny
        _cand(id="b", title="Agent harness memory poisoning "
                            "and prompt injection audit"),                # route
        _cand(id="c", title="A survey of MCP interoperability"),           # filter (weak)
    ]
    common.save_candidates(cands)
    rc = prefilter.main([])
    assert rc == 0
    dropped = json.loads(prefilter._dropped_file().read_text())
    routed = json.loads(prefilter._routed_file().read_text())
    filtered = json.loads(prefilter._filtered_file().read_text())
    assert len(dropped) == 1
    assert len(routed) == 1
    assert len(filtered) == 1


def test_main_exits_nonzero_on_empty_input(sandbox):
    _seed_keywords(sandbox)
    rc = prefilter.main([])
    assert rc == 1


def test_dry_run_does_not_write(sandbox):
    _seed_keywords(sandbox)
    common.save_candidates([_cand()])
    rc = prefilter.main(["--dry-run"])
    assert rc == 0
    assert not prefilter._dropped_file().exists()
    assert not prefilter._routed_file().exists()
    assert not prefilter._filtered_file().exists()
