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

import math
import re
import shutil
from html import escape
from json import dumps
from pathlib import Path

import briefing
import common as c
import content_checks as cc
import dedupe_stories as ds
import story_ledger as sl
import taxonomy
import verify_citations as vc

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
SITE_URL = f"https://rcha0s.github.io/{REPO_NAME}/"
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
        "domain": c.domain_name(entry.get("domain") or ""),
        "domain_id": entry.get("domain", ""),
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


def story_fields(entry: dict, ctx: tuple[dict, dict[str, str]]) -> dict:
    """The row's story id, the story's other covering sources ('Also reported
    by'), and its dated Updated lines."""
    ledger, index = ctx
    eid = entry.get("id") or c.slugify(entry.get("title", ""), 60)
    sid = index.get(eid) or f"e-{eid}"
    story = ledger["stories"].get(sid) or {}
    own = ds.canonical_url(entry.get("source_url") or entry.get("article_url") or "")
    corr = [
        {
            "url": s.get("url", ""),
            "source_name": s.get("source_name", ""),
            "tier": s.get("tier", ""),
        }
        for s in story.get("sources", [])
        if ds.canonical_url(s.get("url", "")) != own
    ]
    keys = ("date", "note", "url", "source_name")
    updates = [{k: u.get(k, "") for k in keys} for u in story.get("updates", [])]
    return {
        "story_id": sid,
        "corroborators": corr,
        "updates": updates,
        "updated": max((u["date"] for u in updates), default=""),
    }


def one_per_story(rows: list[dict], rank) -> list[dict]:
    """Keep the best-ranked row of each story (lowest `rank(row)`), in the
    order the kept rows first appear after ranking."""
    kept: dict[str, dict] = {}
    for row in sorted(rows, key=rank):
        kept.setdefault(row["story_id"], row)
    return list(kept.values())


def curated_findings(conf: c.Config, snapshot_days: int, ctx=None) -> list[dict]:
    """Every vetted finding of the last max_age_days across the three pools, one
    row per story, ranked by composite. A story's other entries show as 'Also
    reported by'. A vetted news story renders in the news lane instead (one story,
    one lane), so the News tab holds every kept news story."""
    ctx = ctx or sl.render_context()
    sources_by_id = c.load_sources_by_id()
    rows = [
        {**finding_row(entry, conf, snapshot_days), **story_fields(entry, ctx)}
        for topic in c.TOPICS
        for entry in c.load_pool(topic)["entries"]
        if c.is_window_finding(entry, conf, sources_by_id)
    ]
    return one_per_story(rows, lambda row: -row["composite"])


_TIER_RANK = {"high": 0, "medium": 1, "low": 2}


def _lane_row(entry: dict, conf: c.Config, snapshot_days: int, sources_by_id: dict):
    """(row, tier) for an entry the news lane shows, else None. News skips the
    novelty gate, never the grounding floor: an ungrounded quote is not shown."""
    if not vc.publishable_grounding(entry):
        return None
    if c.is_editorial(entry):
        ed = entry.get("editorial") or {}
        meta = {
            "lane": "editorial",
            "reason": ed.get("reason", ""),
            "signals": ed.get("signals") or [],
            "at": ed.get("at", ""),
        }
        tier = "high"
    elif c.is_news_curated(entry, conf, sources_by_id, window=None):
        src = sources_by_id.get(entry.get("source_id") or "", {})
        name, tier = src.get("name", ""), src.get("tier", "medium")
        reason = (
            f"{name} announcement"
            if name
            else "Passed the news gate — fresh + on-topic + trusted source"
        )
        meta = {"lane": "news", "reason": reason, "signals": [], "at": entry.get("published", "")}
        if c.is_curated(entry, conf):
            meta["has_page"] = True  # a vetted finding: generate_site rendered its page
    else:
        return None
    return {**finding_row(entry, conf, snapshot_days), **meta}, tier


def editorial_rows(conf: c.Config, snapshot_days: int, ctx=None, exclude=()) -> list[dict]:
    """Findings for the 'Trending & in the news' lane, one row per story.

    Two sources of truth feed this band:

    - Editorial pass: entries flagged with editorial.promoted = true.
    - News gate: entries that pass is_news_curated with no age limit. News is
      kept like claims: a story stays in this lane, newest first.

    A story's rows collapse through the story ledger (story_ledger.py): the
    editorial pick, else the highest-tier source, else the earliest report
    leads, and the story's other sources become 'Also reported by'. Stories in
    `exclude` (already shown as findings) are left out, so a story renders once.
    A story with a fresh Updated line sorts by that date (it moves back up)."""
    ctx = ctx or sl.render_context()
    sources_by_id = c.load_sources_by_id()
    ranked = []
    for topic in c.TOPICS:
        for entry in c.load_pool(topic)["entries"]:
            got = _lane_row(entry, conf, snapshot_days, sources_by_id)
            if got:
                row, tier = got
                ranked.append(({**row, **story_fields(entry, ctx)}, tier))
    tier_of = {id(row): tier for row, tier in ranked}

    def rank(row: dict) -> tuple:
        return (
            row["lane"] != "editorial",
            _TIER_RANK.get(tier_of[id(row)], 3),
            row.get("published") or "",
            row["id"],
        )

    rows = [r for r in one_per_story([r for r, _ in ranked], rank) if r["story_id"] not in exclude]
    return sorted(
        rows, key=lambda row: max(row.get("at", ""), row.get("updated", "")), reverse=True
    )


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
            src = (
                src_root / c.domain_slug(entry.get("domain") or "General") / _entry_filename(entry)
            )
            if not src.is_file():
                # generate_site.py hasn't run in this workflow step yet, or
                # slug drifted — skip silently rather than fail the render.
                continue
            dst = (
                target_root
                / topic
                / c.domain_slug(entry.get("domain") or "General")
                / _entry_filename(entry)
            )
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            written += 1
            _copy_moved_stub(src_root, target_root / topic, entry)
    return written


def _copy_moved_stub(src_root: Path, dst_root: Path, entry: dict) -> None:
    """Mirror generate_site's "Moved" stub at the entry's pre-taxonomy path, so
    old docs/findings/ links (the modal's URLs) keep resolving."""
    old = c.moved_slug(entry)
    src = src_root / old / _entry_filename(entry) if old else None
    if src is None or not src.is_file():
        return
    dst = dst_root / old / _entry_filename(entry)
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


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


_TREND_NUMBERS = (("count", int), ("recent", int), ("momentum", float))


def _trend_rows(rows: object) -> list[dict]:
    """data/trends.json rows with their numbers coerced; a row that fails is dropped.

    trends.json can arrive in a scan PR, so a "count" could be a string of HTML.
    The page renders these numbers; only real numbers reach it."""
    out = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        try:
            fixed = {key: cast(row.get(key, 0) or 0) for key, cast in _TREND_NUMBERS}
        except (TypeError, ValueError, OverflowError):
            continue
        if any(isinstance(row.get(k), bool) for k, _ in _TREND_NUMBERS):
            continue
        if not math.isfinite(fixed["momentum"]):  # NaN/inf would break the page's JSON
            continue
        out.append({**row, **fixed})
    return out


def build_payload(ledger: dict, conf: c.Config, now: str) -> dict:
    snapshot_days = conf.snapshot_days
    trends = c.load_json(c.DATA_DIR / "trends.json", {}) or {}
    archive = c.load_json(c.DATA_DIR / "archive.json", []) or []
    ctx = sl.render_context()
    findings = curated_findings(conf, snapshot_days, ctx)
    shown = {row["story_id"] for row in findings}
    editorial = without_missing_pages(editorial_rows(conf, snapshot_days, ctx, exclude=shown))
    archived = archive_rows(archive, conf)
    tax = taxonomy.get()
    return {
        "generated": now,
        "snapshot_days": snapshot_days,
        "max_age_days": conf.max_age_days,
        "news_front_page_days": conf.news_front_page_days,
        "news_front_page_max": conf.news_front_page_max,
        "archive_count": len(archive),
        "archive_vetted": len(archived),
        "claims_since": _claims_since(ledger),
        "topic_order": list(c.TOPICS.keys()),
        "topics": topics_payload(tax),
        "claims": claims_payload(ledger, tax),
        "findings": findings,
        "editorial": editorial,
        "lessons": lessons_index(conf, snapshot_days),
        "trends": {t: trend_view(_trend_rows(trends.get(t, []))) for t in c.TOPICS},
        "archive": archived,
        **front_page(findings + editorial, cl.all_claims(ledger), now, snapshot_days),
    }


# --- Phase 6 views: topics/domains, archive, front-page picks ------------------
# Kept apart from the rows above so concurrent work on the lanes rebases cleanly.
TREND_ROWS = 10  # per topic; the site shows at most this many (topic pages)
ARCHIVE_TAKEAWAY_CHARS = 180


def topics_payload(tax: taxonomy.Taxonomy) -> dict:
    """Each topic with its taxonomy domains (stable IDs + display names + scope)."""
    return {
        slug: {
            "name": meta["name"],
            "blurb": meta["blurb"],
            "domains": [c.domain_name(d) for d in meta.get("domains", [])],
            "domain_ids": [
                {"id": d.id, "name": d.name, "scope": d.scope} for d in tax.for_topic(slug)
            ],
        }
        for slug, meta in c.TOPICS.items()
    }


def claims_payload(ledger: dict, tax: taxonomy.Taxonomy) -> list[dict]:
    """The ledger's claims, each tagged with the taxonomy ID its domain label names."""
    return [
        {
            **claim,
            "domain": c.domain_name(claim.get("domain") or ""),
            "domain_id": briefing.claim_domain(claim, tax),
        }
        for claim in cl.all_claims(ledger)
    ]


def without_missing_pages(rows: list[dict]) -> list[dict]:
    """News-gate rows get no rendered .md (only curated and editorial ones do), so
    their detail_path is cleared and the modal builds the story from the row. A
    vetted finding that aged into the news lane keeps its page."""
    out = []
    for row in rows:
        keep = row.get("lane") == "editorial" or row.get("has_page")
        row = {k: v for k, v in row.items() if k != "has_page"}
        out.append(row if keep else {**row, "detail_path": ""})
    return out


def trend_view(rows: list[dict]) -> list[dict]:
    """The rows the site renders, without their member lists (never shown)."""
    return [{k: v for k, v in row.items() if k != "members"} for row in rows[:TREND_ROWS]]


def archive_rows(archive: list, conf: c.Config) -> list[dict]:
    """Aged-out findings that were vetted, as compact searchable rows, newest first.

    Only what passed the curation gate is shown (the rest was never published).
    Rows link to the source; archived findings have no detail page."""
    rows = [
        {
            "id": e.get("id", ""),
            "topic": e.get("topic", ""),
            "domain": c.domain_name(e.get("domain") or ""),
            "domain_id": e.get("domain", ""),
            "title": e.get("title", ""),
            "url": c.clean_source_url(e.get("source_url") or e.get("article_url") or ""),
            "source_name": e.get("source_name", ""),
            "published": c.best_date(e) or "",
            "takeaway": c.clean_summary(
                e.get("takeaway") or e.get("summary") or "", ARCHIVE_TAKEAWAY_CHARS
            ),
        }
        for e in archive
        if isinstance(e, dict) and c.is_curated(e, conf)
    ]
    return sorted(rows, key=lambda r: (r["published"], r["id"]), reverse=True)


def front_page(rows: list[dict], claims: list[dict], now: str, days: int) -> dict:
    """The README teaser's and the Briefing's shared picks, as row/claim ids."""
    stories, topped_up = briefing.top_stories(rows, now, days)
    return {
        "top_stories": [row["id"] for row in stories],
        "top_stories_topped_up": topped_up,
        "top_stories_fresh": briefing.fresh_count(stories, now, days),
        "top_claims": [claim["id"] for claim in briefing.top_claims(claims)],
    }


def render(payload: dict, now: str) -> str:
    """Inject the data + chrome into the template.

    The payload goes into a <script type="application/json"> block, so the only
    sequence that could break out is `</script>`; escaping the opening angle
    bracket of any closing tag keeps it inert without corrupting the JSON.
    """
    data = _sub_dash(
        dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    )
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
    now = c.utcnow().strftime("%Y-%m-%d")
    payload = build_payload(ledger, conf, now)
    problems = cc.site_story_problems(payload)
    if problems:
        print(f"story integrity failed - refusing to render the site ({len(problems)} problems):")
        for problem in problems[:20]:
            print(f"  - {problem}")
        return 1

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
