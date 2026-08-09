"""Tests for scripts/ingest_github.py — pure mapping functions (offline).

The `min_stars_for` seam resolves the effective star threshold for a source:
per-source override wins over the global default. Enables MCP-focused queries
to survive at low star counts while general queries stay at the 40-star floor.
"""

from __future__ import annotations

import ingest_github as ig


def test_min_stars_for_uses_per_source_when_set():
    source = {"type": "github_query", "handle": "mcp protocol", "min_stars": 10}
    assert ig.min_stars_for(source, default=40) == 10


def test_min_stars_for_falls_back_to_default_when_missing():
    source = {"type": "github_query", "handle": "prompt injection"}
    assert ig.min_stars_for(source, default=40) == 40


def test_min_stars_for_falls_back_to_default_when_none():
    """`min_stars: null` in the source record is treated as "inherit default"."""
    source = {"type": "github_query", "handle": "q", "min_stars": None}
    assert ig.min_stars_for(source, default=40) == 40


def test_min_stars_for_accepts_zero_override():
    """A per-source `min_stars: 0` MUST be respected — some MCP-focused queries
    genuinely want no star floor (protocol changes may land in a 1-star repo)."""
    source = {"type": "github_query", "handle": "q", "min_stars": 0}
    assert ig.min_stars_for(source, default=40) == 0


def test_min_stars_for_rejects_non_int_override():
    """Malformed config falls back to default rather than crashing the run."""
    source = {"type": "github_query", "handle": "q", "min_stars": "forty"}
    assert ig.min_stars_for(source, default=40) == 40
