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


CAVEAT_LENSES = ("correctness", "prior-art", "scope")


def _clean_caveats(raw: object) -> list[dict]:
    """Only well-formed {lens, note} pairs survive; malformed entries dropped
    so a stale field can't crash the render. Correctness caveats are permitted
    on the wire but the refuter panel emits none — the veto handles them."""
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        lens = item.get("lens")
        if lens not in CAVEAT_LENSES:
            continue
        out.append({"lens": lens, "note": str(item.get("note") or "")})
    return out


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
        "caveats": _clean_caveats(entry.get("caveats")),
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
    """Findings for the 'Trending & in the news' lane.

    Two sources of truth feed this band, unioned and deduped:

    - Editorial pass: entries flagged with editorial.promoted = true.
      Humans surface a timely/teachable held finding.
    - News gate: entries that pass is_news_curated, i.e. a news-track
      source dropped a fresh (≤7d) on-topic item that clears the deny
      list.

    News-gated rows are further deduped through the story-key index
    (dedupe_stories.py). Duplicates become corroborators on the winning
    row — a story on OpenAI's blog and mirrored on Hugging Face collapses
    to one entry with 'Also reported by: Hugging Face'."""
    import dedupe_stories as ds

    sources_by_id = c.load_sources_by_id()

    # First pass — identify which entries will be news candidates so we
    # can exclude them from the seed pass (otherwise every candidate
    # fingerprint-matches itself and gets marked as a duplicate).
    news_candidate_ids: set[str] = set()
    for topic in c.TOPICS:
        for entry in c.load_pool(topic)["entries"]:
            if c.is_news_curated(entry, conf, sources_by_id):
                news_candidate_ids.add(entry.get("id") or "")

    # Seed the story-key index from every recent finding EXCEPT the current
    # news candidates. What remains is prior art: research findings and
    # already-shipped news that we don't want to re-surface.
    dedup_idx = ds.load_index()
    dedup_idx = ds.prune_index(dedup_idx)
    ds.seed_index_from_pools(dedup_idx, skip_ids=news_candidate_ids)

    rows: list[dict] = []
    seen_ids: set[str] = set()
    row_by_story: dict[str, int] = {}

    def _emit(entry: dict, *, lane: str, reason: str = "", signals=None,
              at: str = "") -> None:
        row = finding_row(entry, conf, snapshot_days)
        row["signals"] = signals or []
        row["reason"] = reason
        row["at"] = at
        row["lane"] = lane
        rows.append(row)
        seen_ids.add(entry.get("id") or "")

    for topic in c.TOPICS:
        for entry in c.load_pool(topic)["entries"]:
            eid = entry.get("id") or ""
            if eid and eid in seen_ids:
                continue
            if c.is_editorial(entry):
                ed = entry.get("editorial") or {}
                _emit(entry, lane="editorial",
                      reason=ed.get("reason", ""),
                      signals=ed.get("signals") or [],
                      at=ed.get("at", ""))
                continue
            if c.is_news_curated(entry, conf, sources_by_id):
                src = sources_by_id.get(entry.get("source_id") or "", {})
                src_name = src.get("name", "")
                tier = src.get("tier", "medium")
                story_id, is_new = ds.assign_story_id(
                    entry, dedup_idx,
                    source_tier=tier,
                    source_name=src_name,
                )
                if not is_new:
                    # Attach as corroborator to whatever row already holds
                    # this story. If the collision is against a research
                    # finding not in `rows`, skip — we don't repeat it.
                    if story_id in row_by_story:
                        rows[row_by_story[story_id]].setdefault(
                            "corroborators", []
                        ).append({
                            "url": entry.get("source_url", ""),
                            "source_name": src_name,
                            "tier": tier,
                        })
                    continue
                reason = (
                    f"{src_name} announcement" if src_name
                    else "Passed the news gate — fresh + on-topic + trusted source"
                )
                _emit(entry, lane="news",
                      reason=reason,
                      at=entry.get("published", ""))
                row_by_story[story_id] = len(rows) - 1

    ds.save_index(dedup_idx)
    return sorted(rows, key=lambda row: row.get("at", ""), reverse=True)


def _claims_since(ledger: dict) -> str:
    """Earliest first_seen across the ledger, so the site can say how far back the
    durable claims reach (they never age out, unlike findings)."""
    seen = [c_.get("first_seen", "") for c_ in cl.all_claims(ledger) if c_.get("first_seen")]
    return min(seen) if seen else ""


def _copy_detail_pages(docs: Path, conf: c.Config) -> int:
    """Mirror every vetted and editorial-promoted finding's rendered .md
    into docs/findings/ so the site's modal can fetch it same-origin.

    Both curated and editorial-promoted entries carry a detail_path in the
    payload (the modal advertises one for every card). Without copying the
    editorial ones, those cards fall back to \"Couldn't load the detail
    page\". Stale files are pruned so a finding that leaves the pool
    doesn't linger in the served tree.
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
            if not (c.is_curated(entry, conf) or c.is_editorial(entry)):
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


def lessons_index(conf: c.Config, snapshot_days: int) -> list[dict]:
    """A flat list of every lesson across the curated pool.

    Each lesson carries the finding it came from (title + detail_path + url),
    the topic, and any related_claims the analyzer surfaced, so the lessons
    view can render standalone cards that click through to (a) the finding
    detail modal and (b) the source article. Lessons without an excerpt are
    dropped — they can't be defended and shouldn't reach the view."""
    out: list[dict] = []
    for topic in c.TOPICS:
        for entry in c.load_pool(topic)["entries"]:
            if not c.is_curated(entry, conf):
                continue
            row = finding_row(entry, conf, snapshot_days)
            for lesson in entry.get("lessons") or []:
                if not isinstance(lesson, dict):
                    continue
                excerpt = lesson.get("excerpt") or ""
                if not excerpt:
                    continue
                out.append(
                    {
                        "point": lesson.get("point") or "",
                        "excerpt": excerpt,
                        "confidence": lesson.get("confidence"),
                        "grounded": lesson.get("grounded"),
                        "finding_id": row["id"],
                        "finding_title": row["title"],
                        "topic": row["topic"],
                        "domain": row["domain"],
                        "url": row["url"],
                        "detail_path": row["detail_path"],
                        "published": row["published"],
                        "related_claims": list(entry.get("related_claims") or []),
                    }
                )
    return out


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
        "lessons": lessons_index(conf, snapshot_days),
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
