"""Shared pytest fixtures — isolate every test from the real data pools."""

from __future__ import annotations

from datetime import UTC, datetime

import common
import dedupe_stories
import pytest
import sources_registry

import claims

# Fixture dates are written around mid-2026. Pin the clock so no test depends
# on the real date: before this, fixtures aged past max_age_days and the
# freshness prune emptied the pools mid-test (CI red from 2026-09-21).
FIXED_NOW = datetime(2026, 7, 15, tzinfo=UTC)


@pytest.fixture(autouse=True)
def frozen_clock(monkeypatch):
    monkeypatch.setattr(common, "utcnow", lambda: FIXED_NOW)
    return FIXED_NOW


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Redirect all pool/candidate/output paths into a temp dir with empty pools."""
    data = tmp_path / "data"
    data.mkdir()
    pools = {t: data / f"{t}.json" for t in common.TOPICS}
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(common, "DATA_DIR", data)
    monkeypatch.setattr(common, "POOL_FILES", pools)
    monkeypatch.setattr(common, "CANDIDATES_FILE", data / "candidates.json")
    monkeypatch.setattr(common, "ANALYSIS_OUT", data / "analysis_out.json")
    monkeypatch.setattr(common, "ARCHIVE_FILE", data / "archive.json")
    monkeypatch.setattr(common, "RAW_DIR", data / "_raw")
    monkeypatch.setattr(sources_registry, "REGISTRY_FILE", data / "sources.json")
    monkeypatch.setattr(claims, "CLAIMS_FILE", data / "claims.json")
    monkeypatch.setattr(dedupe_stories, "STORY_INDEX", data / "news_stories.json")
    # Keep grounding offline: kill the network re-fetch (raw_path reading still works).
    # Tests that need a fetched source override source_text_for themselves.
    monkeypatch.setattr(common, "fetch_readable", lambda *a, **k: None)
    for topic in common.TOPICS:
        common.save_pool(topic, common.empty_pool(topic))
    return tmp_path


def make_entry(**over) -> dict:
    """A valid analyzed entry; override any field via kwargs."""
    entry = {
        "topic": "ai-research",
        "domain": "Agents & Harnesses",
        "subtype": "Orchestration",
        "title": "Compacting tool outputs cuts agent tokens",
        "source_url": "https://example.com/compact",
        "article_url": "https://example.com/compact",
        "date": "2026-07",
        "summary": "Summarize tool outputs before re-injecting.",
        "takeaway": "Compact tool outputs to shrink context cost.",
        "lessons": [
            {"point": "Summarize before re-injecting", "excerpt": "40% less", "confidence": 0.9}
        ],
        "scores": {"novelty": 80, "relevance": 85},
        "tags": ["agents", "context"],
    }
    entry.update(over)
    return entry


# The throwaway-repo fixture for the run_scan.sh end-to-end tests, shared with
# test_run_scan_local.py.
from test_run_scan import scan_repo  # noqa: E402,F401
