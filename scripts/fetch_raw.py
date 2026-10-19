#!/usr/bin/env python3
"""
fetch_raw.py — Fetch one staged candidate's article text into data/_raw/.

The scan's analysis step needs source text to ground excerpts. Giving the
model a free-form `curl` would also give a prompt-injected model a way to send
data to any URL, so it gets this instead: it names a candidate id, and this
fetches that candidate's URL as `run_scan.sh pre` recorded it in
data/_scan_urls.json (via Jina Reader), writes data/_raw/<id>.txt and sets the
candidate's `raw_path`. The snapshot, not candidates.json, is the source of
URLs: the model may edit candidates.json, but not data/_scan* files.

Usage:
    python scripts/fetch_raw.py <candidate_id>
"""

from __future__ import annotations

import re
import sys

import common as c

URL_SNAPSHOT = "_scan_urls.json"
ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,200}$")


def fetch_one(cand_id: str) -> str:
    if not ID_RE.match(cand_id) or ".." in cand_id:
        raise SystemExit(f"fetch_raw: invalid candidate id: {cand_id!r}")
    urls = c.load_json(c.DATA_DIR / URL_SNAPSHOT, default=None)
    if urls is None:
        raise SystemExit("fetch_raw: no URL snapshot; run `run_scan.sh pre` first")
    url = urls.get(cand_id)
    if not url or not url.startswith(("https://", "http://")):
        raise SystemExit(f"fetch_raw: no http(s) URL recorded for {cand_id}")
    raw_path = c.write_raw(cand_id, c.fetch_readable(url))
    candidates = c.load_candidates()
    for cand in candidates:
        if cand.get("id") == cand_id:
            cand["raw_path"] = raw_path
    c.save_candidates(candidates)
    return raw_path


def snapshot_urls() -> int:
    """Record every staged candidate's URL; run_scan.sh pre calls this."""
    urls = {
        x["id"]: x.get("article_url") or x.get("source_url")
        for x in c.load_candidates()
        if x.get("id") and (x.get("article_url") or x.get("source_url"))
    }
    c.save_json(c.DATA_DIR / URL_SNAPSHOT, urls)
    print(f"fetch_raw: recorded {len(urls)} candidate URLs")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--snapshot"]:
        return snapshot_urls()
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    print(fetch_one(argv[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
