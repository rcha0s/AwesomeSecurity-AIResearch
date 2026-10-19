#!/usr/bin/env python3
"""
fetch_raw.py — Fetch one staged candidate's article text into data/_raw/.

The scan's analysis step needs source text to ground excerpts. Giving the
model a free-form `curl` would also give a prompt-injected model a way to send
data to any URL, so it gets this instead: it names a candidate id, and this
fetches only the URL already on that candidate (via Jina Reader), writes
data/_raw/<id>.txt and sets the candidate's `raw_path`.

Usage:
    python scripts/fetch_raw.py <candidate_id>
"""

from __future__ import annotations

import re
import sys

import common as c

ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,200}$")


def fetch_one(cand_id: str) -> str:
    if not ID_RE.match(cand_id) or ".." in cand_id:
        raise SystemExit(f"fetch_raw: invalid candidate id: {cand_id!r}")
    candidates = c.load_candidates()
    match = next((x for x in candidates if x.get("id") == cand_id), None)
    if match is None:
        raise SystemExit(f"fetch_raw: no staged candidate {cand_id}")
    url = match.get("article_url") or match.get("source_url")
    if not url or not url.startswith(("https://", "http://")):
        raise SystemExit(f"fetch_raw: candidate {cand_id} has no http(s) URL")
    match["raw_path"] = c.write_raw(cand_id, c.fetch_readable(url))
    c.save_candidates(candidates)
    return match["raw_path"]


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    print(fetch_one(argv[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
