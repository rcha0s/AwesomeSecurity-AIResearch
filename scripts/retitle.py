#!/usr/bin/env python3
"""
retitle.py — Shorten finding titles in the pools and archive, safely.

A title is one plain sentence of at most `readability.thresholds.title_words.warn`
words with no "headline: a, b, c" list (Rohan, 2026-10-26). This rewrites
existing titles from a reviewed `{entry id: new title}` JSON file:

  check FILE   report every proposed title that breaks the rule or says
               something its entry does not (rewrite_guard.title_changes:
               new numbers, names, CVE ids or severity words, or a dropped
               negation). Exit 1 if any does.
  apply FILE   write the titles that pass check through common.retitle, so
               each old page path keeps a "Moved" stub. Refuses the whole file
               if any title fails.
  list         print {id: title} for every title over the limit (the input to
               a rewrite pass).

Usage:
    python scripts/retitle.py list > /tmp/long.json
    python scripts/retitle.py check /tmp/new_titles.json
    python scripts/retitle.py apply /tmp/new_titles.json
"""

from __future__ import annotations

import argparse
import json
import sys

import common as c
import readability as rd
import rewrite_guard as rg

ARCHIVE = "archive"


def max_words() -> int:
    return int((rd.settings()["thresholds"].get("title_words") or {}).get("warn", 12))


def too_long(title: str) -> bool:
    return len(rd.words(title)) > max_words() or rd.title_list(title)


def load_all() -> dict[str, dict]:
    """{topic or 'archive': its document}."""
    docs = {t: c.load_pool(t) for t in c.TOPICS}
    docs[ARCHIVE] = {"entries": c.load_json(c.ARCHIVE_FILE, default=[]) or []}  # a bare list
    return docs


def entries_by_id(docs: dict[str, dict]) -> dict[str, dict]:
    return {e["id"]: e for d in docs.values() for e in d.get("entries", []) if isinstance(e, dict)}


def problems(entry: dict, title: str) -> list[str]:
    """Why `title` can't replace the entry's title ([] = it can)."""
    out = []
    if not isinstance(title, str) or not title.strip():
        return ["empty title"]
    if len(rd.words(title)) > max_words():
        out.append(f"{len(rd.words(title))} words (max {max_words()})")
    if rd.title_list(title):
        out.append("headline plus a list")
    prose = f"{entry.get('takeaway', '')}\n{entry.get('summary', '')}"
    return out + rg.title_changes(entry.get("title", ""), title, prose)


def check(proposed: dict[str, str], by_id: dict[str, dict]) -> dict[str, list[str]]:
    out = {}
    for eid, title in proposed.items():
        entry = by_id.get(eid)
        why = ["unknown entry id"] if entry is None else problems(entry, title)
        if why:
            out[eid] = why
    return out


def apply(proposed: dict[str, str], docs: dict[str, dict]) -> int:
    """Retitle every entry named in `proposed` (all copies). Returns the count."""
    n = 0
    for doc in docs.values():
        rows = doc.get("entries", [])
        for i, e in enumerate(rows):
            new = proposed.get(e.get("id")) if isinstance(e, dict) else None
            if new and new != e.get("title"):
                rows[i] = c.retitle(e, new.strip())
                n += 1
    for topic in c.TOPICS:
        c.save_pool(topic, docs[topic])
    c.save_json(c.ARCHIVE_FILE, docs[ARCHIVE]["entries"])
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("cmd", choices=("list", "check", "apply"))
    ap.add_argument("file", nargs="?")
    args = ap.parse_args(argv)
    docs = load_all()
    by_id = entries_by_id(docs)
    if args.cmd == "list":
        print(json.dumps({k: e["title"] for k, e in by_id.items() if too_long(e.get("title", ""))},
                         indent=1, ensure_ascii=False))  # fmt: skip
        return 0
    if not args.file:
        ap.error(f"{args.cmd} needs a FILE")
    proposed = c.load_json(c.Path(args.file), default={})
    bad = check(proposed, by_id)
    for eid, why in bad.items():
        print(f"FAIL {eid}: {'; '.join(why)} | {proposed.get(eid)!r}")
    print(f"retitle {args.cmd}: {len(proposed) - len(bad)} ok, {len(bad)} failed")
    if bad:
        return 1
    if args.cmd == "apply":
        print(f"retitled {apply(proposed, docs)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
