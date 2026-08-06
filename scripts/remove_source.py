#!/usr/bin/env python3
"""
remove_source.py — Retire a source from the registry.

    python scripts/remove_source.py <source-id> [--blocklist] [--reason TEXT]

`--blocklist` appends the source's domain to data/source_blocklist.json so
source_scout never re-proposes it. The blocklist entry gets an optional
reason and a retired_at timestamp.

Does not delete on-disk artifacts (findings already ingested from the
source stay in the pool). Only prevents future ingestion.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "sources.json"
BLOCKLIST = ROOT / "data" / "source_blocklist.json"


def _load(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _save(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _domain(url: str) -> str:
    if not url:
        return ""
    try:
        host = urlparse(url).netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except (ValueError, TypeError):
        return ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_id", help="The source's `id` field in data/sources.json")
    ap.add_argument("--blocklist", action="store_true",
                    help="Also append the source's domain to source_blocklist.json.")
    ap.add_argument("--reason", default="",
                    help="Why this source was retired (recorded in blocklist).")
    args = ap.parse_args(argv)

    sources = _load(SOURCES) or []
    match = next((s for s in sources if s.get("id") == args.source_id), None)
    if not match:
        print(f"source not found: {args.source_id}", file=sys.stderr)
        return 1

    sources = [s for s in sources if s.get("id") != args.source_id]
    _save(SOURCES, sources)
    print(f"removed source: {match.get('name', args.source_id)}")

    if args.blocklist:
        block = _load(BLOCKLIST) or []
        domain = _domain(match.get("url") or match.get("handle") or "")
        if not domain:
            print("(no domain to blocklist)")
        elif any(b.get("domain") == domain for b in block):
            print(f"(domain {domain} already in blocklist)")
        else:
            block.append({
                "domain": domain,
                "source_id": args.source_id,
                "reason": args.reason,
                "retired_at": datetime.now(UTC).strftime("%Y-%m-%d"),
            })
            _save(BLOCKLIST, block)
            print(f"blocklisted: {domain}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
