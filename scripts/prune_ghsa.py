#!/usr/bin/env python3
"""
prune_ghsa.py — Apply the GitHub-advisory keep rule to what is already on the site.

Rohan, 2026-10-28: advisories are not stories until they blow up on the
internet. select_batch.ghsa_keep_reason decides which new candidates stay; this
applies the same rule to pool entries that came from the GitHub Advisory
Database. An entry stays when any of these holds, checked in order:

  ai-security   it is in the ai-security pool, or its domain is an `ais.*` ID
  promoted      it is an editorial promotion (sticky, never demoted here)
  claim         its advisory URL is evidence for a claim in data/claims.json
  critical      it reads as CRITICAL and names a package in `ghsa.well_known_packages`
  corroborated  2+ independent publishers cover it (corroborating sources and
                story corroboration, not GitHub, HN or its own host)

Pool entries store neither severity nor package, so "critical" is read from the
news brief's own `ghsa-critical` reason or markers, else the word "critical" in
the title, summary or takeaway, and the package is a `well_known_packages` name
in the title, tags or id. Everything else moves to data/archive.json through
common.archive_entries (the helper rerank uses), stamped
`archived_reason: ghsa-not-kept` so rerank's news restore leaves it there.
Nothing is deleted; the entries stay on the site's Archive tab.

Usage:
    python scripts/prune_ghsa.py --dry-run
    python scripts/prune_ghsa.py
"""

from __future__ import annotations

import argparse
import json
import re

import common as c
import newsworthy as nw

ARCHIVED_REASON = "ghsa-not-kept"
ADVISORY_HOST = "github.com/advisories/"
NOT_INDEPENDENT = frozenset({"github.com", "ycombinator.com"})  # GitHub and HN


def is_ghsa_entry(entry: dict) -> bool:
    """Came from the GitHub Advisory Database (by source name or advisory URL)."""
    urls = f"{entry.get('source_url') or ''} {entry.get('article_url') or ''}".lower()
    return entry.get("source_name") == "GitHub Advisory Database" or ADVISORY_HOST in urls


def reads_critical(entry: dict) -> bool:
    brief = entry.get("news_brief") or {}
    if brief.get("reason") == "ghsa-critical" or "critical" in (brief.get("markers") or []):
        return True
    text = " ".join(str(entry.get(k) or "") for k in ("title", "summary", "takeaway")).lower()
    return bool(re.search(r"\bcritical\b", text))


def names_package(entry: dict, packages: list[str]) -> str | None:
    """The `packages` name the entry's title, tags or id mention first."""
    text = " ".join([str(entry.get("title") or ""), *map(str, entry.get("tags") or [])]).lower()
    text += " " + str(entry.get("id") or "").lower()
    hits = [
        (m.start(), name)
        for name in packages
        if (m := re.search(rf"(?<![a-z0-9]){re.escape(name)}(?![a-z0-9])", text))
    ]
    return min(hits)[1] if hits else None


def independent_publishers(entry: dict) -> set[str]:
    """Distinct publishers of the entry's other coverage, minus GitHub, HN and
    the entry's own host."""
    own = nw.registrable_domain(entry.get("source_url") or "")
    urls = [
        (s.get("url") if isinstance(s, dict) else s)
        for key in ("corroborating_sources", "story_corroboration")
        for s in entry.get(key) or []
    ]
    pubs = {nw.registrable_domain(u or "") for u in urls}
    return {p for p in pubs if p and p != own and p not in NOT_INDEPENDENT}


def claim_urls(claims: dict) -> set[str]:
    out: set[str] = set()
    for claim in claims.get("claims") or []:
        for ev in claim.get("evidence") or []:
            if isinstance(ev, dict) and ev.get("url"):
                out.add(c.normalize_url(ev["url"]))
    return out


def keep_reason(entry: dict, conf: c.Config, cited: set[str]) -> str | None:
    """Why a GHSA-sourced pool entry stays, else None (it moves to the archive)."""
    if entry.get("topic") == "ai-security" or str(entry.get("domain") or "").startswith("ais."):
        return "ai-security"
    if c.is_editorial(entry):
        return "editorially promoted"
    if c.normalize_url(entry.get("source_url") or "") in cited:
        return "evidence for a claim"
    well_known = [str(p).lower() for p in conf.ghsa.get("well_known_packages") or []]
    package = names_package(entry, well_known)
    if reads_critical(entry) and package:
        return f"critical in well-known package {package}"
    if len(independent_publishers(entry)) >= 2:
        return "covered by 2+ independent publishers"
    return None


def move_reason(entry: dict, conf: c.Config) -> str:
    """Why an entry moved, for the PR body."""
    package = names_package(entry, [str(p).lower() for p in conf.ghsa.get("well_known_packages")])
    critical = "critical" if reads_critical(entry) else "not critical"
    pubs = len(independent_publishers(entry))
    return (
        f"not AI-related; {critical}, "
        f"{'package ' + package if package else 'package not in the well-known list'}; "
        f"{pubs} independent covering publisher(s)"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    conf = c.load_config()
    cited = claim_urls(c.load_json(c.DATA_DIR / "claims.json", default={}) or {})
    kept: list[tuple[dict, str]] = []
    moved: list[tuple[dict, str]] = []
    pools: dict[str, dict] = {}
    for track in c.TOPICS:
        pools[track] = c.load_pool(track)
        for entry in pools[track]["entries"]:
            if not is_ghsa_entry(entry):
                continue
            why = keep_reason(entry, conf, cited)
            (kept if why else moved).append((entry, why or move_reason(entry, conf)))
    print(f"GHSA pool entries: {len(kept) + len(moved)} (keep {len(kept)}, move {len(moved)})")
    for label, rows in (("KEEP", kept), ("MOVE", moved)):
        for entry, why in rows:
            print(f"{label}\t{entry['id']}\t{entry.get('topic')}\t{entry['title']}\t{why}")
    if args.dry_run or not moved:
        return 0
    gone = {e["id"] for e, _ in moved}
    c.archive_entries([{**e, "archived_reason": ARCHIVED_REASON} for e, _ in moved])
    for track, pool in pools.items():
        if any(e["id"] in gone for e in pool["entries"]):
            pool["entries"] = [e for e in pool["entries"] if e["id"] not in gone]
            c.save_pool(track, pool)
    print(json.dumps({"archived": len(moved)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
