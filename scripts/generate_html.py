#!/usr/bin/env python3
"""
generate_html.py — Render the real browsable site into docs/ for GitHub Pages.

The markdown tree is the readable-on-GitHub view. This is the *site*: one
self-contained page that lets you filter the claim ledger by topic and status,
search it, jump along supersession edges, and read the findings feed — with no
Jekyll theme, no build step, and no external requests (a strict-CSP-safe page).

Writes:
  docs/index.html   the site (data embedded as JSON, styles/scripts inlined)
  docs/.nojekyll    tells Pages to serve the HTML as-is instead of running Jekyll

Point GitHub Pages at branch `main`, folder `/docs`.

Usage:
    python scripts/generate_html.py
"""

from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from json import dumps
from pathlib import Path

import common as c

import claims as cl

# A code asset that ships beside this script — not data under ROOT.
TEMPLATE = Path(__file__).resolve().parent / "templates" / "site.html"
REPO_NAME = "AwesomeSecurity-AIResearch"
REPO_URL = f"https://github.com/rcha0s/{REPO_NAME}"
SITE_TITLE = "Standing Claims — AI Agent & Security Research"
SITE_DESC = (
    "What currently holds for building agentic systems and securing AI — "
    "each claim with its evidence, and every superseded answer kept with the reason it fell."
)


def finding_row(entry: dict, conf: c.Config) -> dict:
    """The subset of a pool entry the site actually renders."""
    return {
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
    }


def curated_findings(conf: c.Config) -> list[dict]:
    """Every vetted finding across the three pools, ranked by composite."""
    rows = [
        finding_row(entry, conf)
        for topic in c.TOPICS
        for entry in c.load_pool(topic)["entries"]
        if c.is_curated(entry, conf)
    ]
    return sorted(rows, key=lambda row: -row["composite"])


def build_payload(ledger: dict, conf: c.Config, now: str) -> dict:
    return {
        "generated": now,
        "max_age_days": conf.max_age_days,
        "topics": {
            slug: {"name": meta["name"], "blurb": meta["blurb"]} for slug, meta in c.TOPICS.items()
        },
        "claims": cl.all_claims(ledger),
        "findings": curated_findings(conf),
    }


def render(payload: dict, now: str) -> str:
    """Inject the data + chrome into the template.

    The payload goes into a <script type="application/json"> block, so the only
    sequence that could break out is `</script>`; escaping the opening angle
    bracket of any closing tag keeps it inert without corrupting the JSON.
    """
    data = dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
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
        print(f"claim ledger is invalid — refusing to render the site ({len(errors)} problems):")
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

    print(
        f"site: docs/index.html — {len(payload['claims'])} claims, "
        f"{len(payload['findings'])} findings"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
