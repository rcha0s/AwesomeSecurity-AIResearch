#!/usr/bin/env python3
"""
generate_html.py - Render the real browsable site into docs/ for GitHub Pages.

The markdown tree is the readable-on-GitHub view. This is the *site*: one
self-contained page that lets you filter the claim ledger by topic and status,
search it, jump along supersession edges, and read the findings feed - with no
Jekyll theme, no build step, and no external requests (a strict-CSP-safe page).

Writes:
  docs/index.html   the site (data embedded as JSON, styles/scripts inlined)
  docs/.nojekyll    tells Pages to serve the HTML as-is instead of running Jekyll

Point GitHub Pages at branch `main`, folder `/docs`.

Usage:
    python scripts/generate_html.py
"""

from __future__ import annotations

import re
import shutil
from datetime import UTC, datetime
from html import escape
from json import dumps
from pathlib import Path

import common as c

import claims as cl


def _entry_filename(entry: dict) -> str:
    """Filename generate_site.py writes for this entry.

    Kept in lockstep with scripts/generate_site.py:entry_filename — if you
    change one, change both. Duplicated here (rather than imported) because
    generate_site.py has side-effects at import time we don't want here.
    """
    return f"{(entry.get('date') or 'undated')}-{c.slugify(entry.get('title', ''), 60)}.md"


def _detail_relpath(entry: dict) -> str:
    """Where the finding's rendered .md lives, relative to the docs/ site
    root. This is what the modal fetches — see docs/index.html."""
    topic = entry.get("topic") or ""
    domain = c.domain_slug(entry.get("domain") or "General")
    return f"findings/{topic}/{domain}/{_entry_filename(entry)}"

# Normalize em/en dashes to a SPACED hyphen so they never read as a compound
# ("word-word"); an em dash acting as a clause break becomes " - ".
_DASH = re.compile(r"\s*[—–]\s*")


def _sub_dash(text: str) -> str:
    return _DASH.sub(" - ", text)

# A code asset that ships beside this script - not data under ROOT.
TEMPLATE = Path(__file__).resolve().parent / "templates" / "site.html"
REPO_NAME = "AwesomeSecurity-AIResearch"
REPO_URL = f"https://github.com/rcha0s/{REPO_NAME}"
SITE_TITLE = "Awesome Security & AI Research: a weekly vetted briefing"
SITE_DESC = (
    "A weekly, source-cited briefing on AI security, product security, and applied "
    "AI research. Every finding is vetted, distilled to one lesson and one action, and "
    "filed by field. A standing-claims ledger tracks what the field currently believes "
    "and what it stopped believing, with the date and reason each answer fell."
)


def _round(value) -> int:
    try:
        return round(float(value))
    except (TypeError, ValueError):
        return 0


def finding_row(entry: dict, conf: c.Config, snapshot_days: int) -> dict:
    """The subset of a pool entry the site actually renders."""
    scores = entry.get("scores") or {}
    cred = scores.get("credibility")
    return {
        "id": entry.get("id", ""),
        "topic": entry.get("topic", ""),
        "domain": entry.get("domain", ""),
        "title": entry.get("title", ""),
        "url": c.clean_source_url(entry.get("source_url") or entry.get("article_url") or ""),
        "takeaway": entry.get("takeaway") or entry.get("summary") or "",
        "summary": entry.get("summary", ""),
        "published": c.best_date(entry) or "",
        "composite": c.entry_composite(entry, conf),
        "source_name": entry.get("source_name", ""),
        "tags": entry.get("tags") or [],
        "scores": {
            "novelty": _round(scores.get("novelty")),
            "newness": _round(scores.get("newness")),
            "relevance": _round(scores.get("relevance")),
            "credibility": _round(cred if cred is not None else c.credibility_of(entry)),
        },
        "verified": entry.get("verified") is True,
        "fresh": c.is_fresh(entry, snapshot_days),
        "detail_path": _detail_relpath(entry),
    }


def curated_findings(conf: c.Config, snapshot_days: int) -> list[dict]:
    """Every vetted finding across the three pools, ranked by composite."""
    rows = [
        finding_row(entry, conf, snapshot_days)
        for topic in c.TOPICS
        for entry in c.load_pool(topic)["entries"]
        if c.is_curated(entry, conf)
    ]
    return sorted(rows, key=lambda row: -row["composite"])


def editorial_rows(conf: c.Config, snapshot_days: int) -> list[dict]:
    """Findings the editorial track promoted for being timely / in the news.

    These are held by the novelty gate (so they are NOT in curated_findings), but
    the editorial pass surfaced them as trending. They power the briefing's
    'Trending & in the news' lane."""
    rows = []
    for topic in c.TOPICS:
        for entry in c.load_pool(topic)["entries"]:
            if not c.is_editorial(entry):
                continue
            ed = entry.get("editorial") or {}
            row = finding_row(entry, conf, snapshot_days)
            row["signals"] = ed.get("signals") or []
            row["reason"] = ed.get("reason", "")
            row["at"] = ed.get("at", "")
            rows.append(row)
    return sorted(rows, key=lambda row: row.get("at", ""), reverse=True)


def _claims_since(ledger: dict) -> str:
    """Earliest first_seen across the ledger, so the site can say how far back the
    durable claims reach (they never age out, unlike findings)."""
    seen = [c_.get("first_seen", "") for c_ in cl.all_claims(ledger) if c_.get("first_seen")]
    return min(seen) if seen else ""


def _copy_detail_pages(docs: Path, conf: c.Config) -> int:
    """Mirror every vetted finding's rendered .md into docs/findings/ so the
    site's modal can fetch it same-origin. Stale files are pruned so a
    finding that leaves the pool doesn't linger in the served tree.
    """
    target_root = docs / "findings"
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True, exist_ok=True)

    written = 0
    for topic in c.TOPICS:
        pool = c.load_pool(topic)
        src_root = c.ROOT / topic
        for entry in pool["entries"]:
            if not c.is_curated(entry, conf):
                continue
            src = src_root / c.domain_slug(entry.get("domain") or "General") / _entry_filename(entry)
            if not src.is_file():
                # generate_site.py hasn't run in this workflow step yet, or
                # slug drifted — skip silently rather than fail the render.
                continue
            dst = target_root / topic / c.domain_slug(entry.get("domain") or "General") / _entry_filename(entry)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            written += 1
    return written


def build_payload(ledger: dict, conf: c.Config, now: str) -> dict:
    snapshot_days = conf.snapshot_days
    trends = c.load_json(c.DATA_DIR / "trends.json", {}) or {}
    archive = c.load_json(c.DATA_DIR / "archive.json", []) or []
    return {
        "generated": now,
        "snapshot_days": snapshot_days,
        "max_age_days": conf.max_age_days,
        "archive_count": len(archive),
        "claims_since": _claims_since(ledger),
        "topic_order": list(c.TOPICS.keys()),
        "topics": {
            slug: {
                "name": meta["name"],
                "blurb": meta["blurb"],
                "domains": meta.get("domains", []),
            }
            for slug, meta in c.TOPICS.items()
        },
        "claims": cl.all_claims(ledger),
        "findings": curated_findings(conf, snapshot_days),
        "editorial": editorial_rows(conf, snapshot_days),
        "trends": {t: trends.get(t, []) for t in c.TOPICS},
    }


def render(payload: dict, now: str) -> str:
    """Inject the data + chrome into the template.

    The payload goes into a <script type="application/json"> block, so the only
    sequence that could break out is `</script>`; escaping the opening angle
    bracket of any closing tag keeps it inert without corrupting the JSON.
    """
    data = _sub_dash(dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    html = TEMPLATE.read_text(encoding="utf-8")
    for token, value in (
        ("__DATA__", data),
        ("__TITLE__", escape(SITE_TITLE)),
        ("__DESC__", escape(SITE_DESC)),
        ("__REPO_NAME__", escape(REPO_NAME)),
        ("__REPO_URL__", escape(REPO_URL)),
        ("__GENERATED__", escape(now)),
    ):
        html = html.replace(token, value)
    return html


def main() -> int:
    ledger = cl.load_ledger()
    errors = cl.validate_ledger(ledger)
    if errors:
        print(f"claim ledger is invalid - refusing to render the site ({len(errors)} problems):")
        for error in errors[:20]:
            print(f"  - {error}")
        return 1

    conf = c.load_config()
    now = datetime.now(UTC).strftime("%Y-%m-%d")
    payload = build_payload(ledger, conf, now)

    docs = c.ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "index.html").write_text(render(payload, now), encoding="utf-8")
    # Without this, Pages runs the output through Jekyll and mangles it.
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    detail_pages = _copy_detail_pages(docs, conf)

    print(
        f"site: docs/index.html - {len(payload['claims'])} claims, "
        f"{len(payload['findings'])} findings, {detail_pages} detail pages"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
