#!/usr/bin/env python3
"""
migrate_lessons.py — One-shot schema migration for the lessons-not-actions rework.

Two changes in one pass:

1. Drop `actionable` from every pool entry (and archive.json). The skills
   pipeline that depended on it is being removed in this same MR; the field
   no longer earns its place. `lessons` (which already exists as a structured
   list) becomes the sole "what to take away" surface.

2. Add `track: "research" | "news" | "both"` and `scope: "ai" | "security" | "both"`
   to every source in data/sources.json. All existing sources are `research` on
   Track A (the ones currently in the registry are academic / vendor research
   feeds); Track B sources will be added in a later MR. Scope is inferred from
   the topics array.

Idempotent: running twice does nothing. Use --dry-run to preview.

    python scripts/migrate_lessons.py --dry-run
    python scripts/migrate_lessons.py

Do NOT run this against a live scan run — it edits data files in place.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

POOLS = ["ai-security.json", "ai-research.json", "product-security.json"]
ARCHIVE = "archive.json"
SOURCES = "sources.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _scope_for_topics(topics: list[str]) -> str:
    """AI-only sources are 'ai', product-security-only are 'security', anything
    that touches both is 'both'. Every source has at least one topic."""
    has_ai = any(t.startswith("ai-") for t in topics)
    has_sec = "product-security" in topics
    if has_ai and has_sec:
        return "both"
    return "ai" if has_ai else "security"


def migrate_sources(path: Path) -> dict:
    """Add `track` and `scope` to every source. Track defaults to 'research'
    for the existing registry (the news sources come in a later MR)."""
    sources = _load(path)
    added_track = 0
    added_scope = 0
    for s in sources:
        if "track" not in s:
            s["track"] = "research"
            added_track += 1
        if "scope" not in s:
            s["scope"] = _scope_for_topics(s.get("topics", []))
            added_scope += 1
    return {
        "path": path.name,
        "sources": len(sources),
        "track_added": added_track,
        "scope_added": added_scope,
    }


def _pool_paths() -> list[Path]:
    return [DATA / p for p in POOLS + [ARCHIVE]]


def _preview(stats: list[dict]) -> None:
    for s in stats:
        line = ", ".join(f"{k}={v}" for k, v in s.items() if k != "path")
        print(f"  {s['path']:<32} {line}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes, write nothing.")
    args = parser.parse_args(argv)

    pool_stats: list[dict] = []
    for path in _pool_paths():
        if not path.exists():
            continue
        doc = _load(path)
        entries = doc.get("entries") if isinstance(doc, dict) else doc
        stripped = sum(1 for e in entries if "actionable" in e)
        pool_stats.append({"path": path.name, "entries": len(entries), "would_strip": stripped})

    src_path = DATA / SOURCES
    sources = _load(src_path)
    would_track = sum(1 for s in sources if "track" not in s)
    would_scope = sum(1 for s in sources if "scope" not in s)
    src_preview = {
        "path": SOURCES,
        "sources": len(sources),
        "would_add_track": would_track,
        "would_add_scope": would_scope,
    }

    print("Pools:")
    _preview(pool_stats)
    print("Sources:")
    _preview([src_preview])

    if args.dry_run:
        print("\n[dry-run] no files written.")
        return 0

    for path in _pool_paths():
        if not path.exists():
            continue
        doc = _load(path)
        entries = doc.get("entries") if isinstance(doc, dict) else doc
        stripped = 0
        for e in entries:
            if e.pop("actionable", None) is not None:
                stripped += 1
        _save(path, doc)
        print(f"wrote {path.name}: stripped {stripped} actionable field(s)")

    stat = migrate_sources(src_path)
    _save(src_path, sources)
    print(
        f"wrote {SOURCES}: added track on {stat['track_added']}, scope on {stat['scope_added']}"
    )

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
