#!/usr/bin/env python3
"""
generate_html.py - Render the real browsable site into docs/ for GitHub Pages.

The markdown tree is the readable-on-GitHub view. This is the *site*: one
self-contained page that lets you filter the claim ledger by topic and status,
see what it changed this week, jump along supersession edges, and search every
vetted finding - with no
Jekyll theme, no build step, and no external requests (a strict-CSP-safe page).

Writes:
  docs/index.html   the site (data embedded as JSON, styles/scripts inlined)
  docs/feed.xml     Atom feed of the Briefing's picks (text only)
  docs/.nojekyll    tells Pages to serve the HTML as-is instead of running Jekyll

Point GitHub Pages at branch `main`, folder `/docs`.

Usage:
    python scripts/generate_html.py
"""

from __future__ import annotations

import math
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import date
from html import escape
from json import dumps
from pathlib import Path
from urllib.parse import quote, urlparse, urlsplit

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
SITE_AUTHOR = "Awesome Security & AI Research"
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


EXPLOITED_TAGS = frozenset({"exploited-in-the-wild", "active-exploitation", "kev"})
KEV_HOSTS = frozenset({"cisa.gov", "www.cisa.gov"})
KEV_PATH = "/known-exploited-vulnerabilities"


def is_exploited(tags: object, url: str) -> bool:
    """True when a story is known to be exploited: it carries an exploitation tag,
    or its source is CISA's Known Exploited Vulnerabilities catalog."""
    if isinstance(tags, (list, tuple)) and any(str(t).lower() in EXPLOITED_TAGS for t in tags):
        return True
    parts = urlparse(url or "")
    return (parts.hostname or "").lower() in KEV_HOSTS and parts.path.lower().startswith(KEV_PATH)


_ID_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(CVE-\d{4}-\d{4,}|GHSA(?:-[a-z0-9]{4}){3})(?![A-Za-z0-9])", re.I
)
MAX_IDS = 4


def extract_ids(*texts: object) -> list[str]:
    """CVE and GHSA ids named in the given texts, in first-seen order, upper-case
    CVE and lower-case GHSA, deduplicated, at most MAX_IDS. The site builds each
    id's link from this strict match, never from free text."""
    found: list[str] = []
    for text in texts:
        for m in _ID_PATTERN.finditer(str(text or "")):
            raw = m.group(1)
            ident = raw.upper() if raw[:3].upper() == "CVE" else "GHSA" + raw[4:].lower()
            if ident not in found:
                found.append(ident)
    return found[:MAX_IDS]


def finding_row(entry: dict, conf: c.Config, snapshot_days: int) -> dict:
    """The subset of a pool entry the site actually renders."""
    scores = entry.get("scores") or {}
    cred = scores.get("credibility")
    url = c.clean_source_url(entry.get("source_url") or entry.get("article_url") or "")
    return {
        "id": entry.get("id", ""),
        "topic": entry.get("topic", ""),
        "domain": c.domain_name(entry.get("domain") or ""),
        "domain_id": entry.get("domain", ""),
        "title": entry.get("title", ""),
        "url": url,
        "takeaway": entry.get("takeaway") or entry.get("summary") or "",
        "summary": entry.get("summary", ""),
        "published": c.best_date(entry) or "",
        "composite": c.entry_composite(entry, conf),
        "source_name": entry.get("source_name", ""),
        "tags": entry.get("tags") or [],
        "exploited": is_exploited(entry.get("tags"), url),
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
        "lessons": finding_lessons(entry),
        "ids": extract_ids(
            entry.get("title"),
            entry.get("takeaway"),
            entry.get("summary"),
            entry.get("source_url") or entry.get("article_url"),
        ),
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
    """Mirror generate_site's "Moved" stubs at the entry's former paths (its
    pre-taxonomy dir, its previous title slugs), so old docs/findings/ links
    (the modal's URLs) keep resolving."""
    for old_dir, name in c.former_page_paths(entry):
        src, dst = src_root / old_dir / name, dst_root / old_dir / name
        if src.is_file() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)


def finding_lessons(entry: dict) -> list[dict]:
    """A finding's lessons for its detail panel: each point with the verbatim
    excerpt it rests on. A lesson without an excerpt can't be defended, so it
    is dropped."""
    out = []
    for lesson in entry.get("lessons") or []:
        if isinstance(lesson, dict) and lesson.get("excerpt"):
            out.append(
                {
                    "point": str(lesson.get("point") or ""),
                    "excerpt": str(lesson["excerpt"]),
                    "grounded": lesson.get("grounded") is not False,
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
    payload = {
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
        "trends": {t: trend_view(_trend_rows(trends.get(t, []))) for t in c.TOPICS},
        "archive": archived,
        **front_page(findings + editorial, claims_payload(ledger, tax), now, snapshot_days),
    }
    normalize_source_names(payload, list(c.load_sources_by_id().values()))
    return payload


# --- One name per source ------------------------------------------------------
BARE_HOST = re.compile(r"^(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+$", re.I)


def _host(url: object) -> str:
    try:
        host = urlsplit(str(url or "")).hostname or ""
    except ValueError:
        return ""
    return host.lower().removeprefix("www.")


def source_names_by_host(sources: list[dict]) -> dict[str, str]:
    """Registry host -> the registry's display name (first source wins)."""
    out: dict[str, str] = {}
    for src in sources:
        host = _host(src.get("url") or src.get("handle"))
        if host and src.get("name"):
            out.setdefault(host, str(src["name"]))
    return out


def normalize_source_names(node: object, sources: list[dict]) -> None:
    """Name a source the same way everywhere: where a row's `source_name` is empty
    or a bare host (www.bleepingcomputer.com), use the registry's name for that
    host when one matches. Walks the whole payload, in place."""
    names = source_names_by_host(sources)
    _walk_source_names(node, names)


def _walk_source_names(node: object, names: dict[str, str]) -> None:
    if isinstance(node, dict):
        if "source_name" in node:
            given = str(node.get("source_name") or "").strip()
            if not given or BARE_HOST.match(given):
                host = _host(node.get("url")) if not given else given.lower().removeprefix("www.")
                if host in names:
                    node["source_name"] = names[host]
        for value in node.values():
            _walk_source_names(value, names)
    elif isinstance(node, list):
        for value in node:
            _walk_source_names(value, names)


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


# A sentence ends at . ! or ? followed by space and a capital, digit or quote;
# "vs." / "e.g." / "U.S." followed by one is an abbreviation, not an end.
_SENTENCE_END = re.compile(r"[.!?](?=\s+[\"'“‘(A-Z0-9])")
_ABBREVIATIONS = frozenset(
    {
        "vs",
        "e.g",
        "i.e",
        "etc",
        "u.s",
        "u.k",
        "mr",
        "mrs",
        "ms",
        "dr",
        "al",
        "cf",
        "approx",
        "no",
        "fig",
        "inc",
        "ltd",
        "corp",
        "jr",
        "sr",
        "st",
    }
)


def _is_sentence_end(text: str, at: int) -> bool:
    words = text[:at].split()
    word = words[-1].lower().rstrip(".") if words else ""
    return word not in _ABBREVIATIONS and len(word) > 1


def sentence_cut(text: str, limit: int = ARCHIVE_TAKEAWAY_CHARS) -> str:
    """`text` within `limit` chars, ended at a sentence boundary when one falls in
    the back half of the window (else at a word), with an ellipsis when cut."""
    text = c.clean_summary(str(text or ""), 10**6)
    if len(text) <= limit:
        return text
    ends = [
        m.end()
        for m in _SENTENCE_END.finditer(text[: limit + 2])
        if limit // 2 <= m.end() <= limit and _is_sentence_end(text, m.start())
    ]
    if ends:
        return text[: ends[-1]] + " …"
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def archived_brief(entry: dict) -> bool:
    """A grounded news brief past limits.brief_news_days: off the News tab,
    still on the Archive tab (a held brief was never published)."""
    return c.is_news_brief(entry) and vc.publishable_grounding(entry)


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
            "takeaway": sentence_cut(e.get("takeaway") or e.get("summary") or ""),
            "exploited": is_exploited(
                e.get("tags"), c.clean_source_url(e.get("source_url") or e.get("article_url") or "")
            ),
            "ids": extract_ids(
                e.get("title"),
                e.get("takeaway"),
                e.get("summary"),
                e.get("source_url") or e.get("article_url"),
            ),
        }
        for e in archive
        if isinstance(e, dict) and (c.is_curated(e, conf) or archived_brief(e))
    ]
    return sorted(rows, key=lambda r: (r["published"], r["id"]), reverse=True)


def front_page(rows: list[dict], claims: list[dict], now: str, days: int) -> dict:
    """The README teaser's and the Briefing's shared picks: row ids, and the
    claim changes (each names its claim, and for a reversal the one it replaced)."""
    biggest = briefing.biggest_stories(rows, now, days)
    taken = {row["id"] for row in biggest}
    stories, topped_up = briefing.top_stories(rows, now, days, exclude=taken)
    changes, changes_fresh = briefing.claim_changes(claims, now, days)
    return {
        "biggest_stories": [row["id"] for row in biggest],
        "top_stories": [row["id"] for row in stories],
        "top_stories_topped_up": topped_up,
        "top_stories_fresh": briefing.fresh_count(stories, now, days),
        "stories_this_week": briefing.fresh_count(rows, now, days),
        "claim_changes": changes,
        "claim_changes_fresh": changes_fresh,
        "efficiency_claims": [claim["id"] for claim in briefing.efficiency_claims(claims)],
        "efficiency_findings": [row["id"] for row in briefing.efficiency_findings(rows, now, days)],
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


ATOM_NS = "http://www.w3.org/2005/Atom"
_XML_BAD = re.compile("[^\t\n\r -퟿-�\U00010000-\U0010ffff]")
_DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
# Used only when the payload's own `generated` day is not a real date: a fixed day,
# never the wall clock, so a re-render stays byte-identical.
FEED_EPOCH = "2000-01-01"


def _xml_text(value: object) -> str:
    """Plain text safe for an XML text node: no control characters, one-space gaps."""
    return " ".join(_XML_BAD.sub("", str(value or "")).split())


def _real_day(value: object) -> str | None:
    """The first ten characters of `value` if they are an ASCII YYYY-MM-DD real date."""
    text = str(value or "")[:10]
    if not _DAY.fullmatch(text):
        return None
    try:
        date.fromisoformat(text)
    except ValueError:
        return None
    return text


def _rfc3339(day: object, fallback: str) -> str:
    """`day` as RFC 3339 midnight UTC; an invalid day falls back to `fallback`
    (a real day, or FEED_EPOCH when that is invalid too)."""
    text = _real_day(day) or _real_day(fallback) or FEED_EPOCH
    return f"{text}T00:00:00Z"


def feed_items(payload: dict) -> list[dict]:
    """The Briefing's picks as feed items: biggest stories, top stories, claim changes."""
    found = (payload.get("findings") or []) + (payload.get("editorial") or [])
    rows = {r.get("id"): r for r in found}
    claims = {k.get("id"): k for k in payload.get("claims") or []}
    items: list[dict] = []
    for rid in (payload.get("biggest_stories") or []) + (payload.get("top_stories") or []):
        row = rows.get(rid)
        if row:
            items.append(
                {
                    "link": f"{SITE_URL}?finding={quote(str(rid), safe='')}#week",
                    "title": row.get("title"),
                    "updated": briefing.last_activity(row),
                    "summary": row.get("takeaway") or row.get("summary"),
                }
            )
    for change in payload.get("claim_changes") or []:
        claim = claims.get(change.get("claim"))
        if claim:
            items.append(
                {
                    "link": f"{SITE_URL}?claim={quote(str(claim['id']), safe='')}#claims",
                    "title": claim.get("title") or claim.get("statement"),
                    "updated": change.get("date"),
                    "summary": claim.get("statement"),
                }
            )
    return items


def render_feed(payload: dict, now: str) -> str:
    """The Atom 1.0 feed of the Briefing's picks: text content only, built with
    ElementTree (which escapes), dated from the payload's `generated` day (`now`),
    so a re-render is byte-identical. Every payload value is treated as hostile text."""
    feed = ET.Element("feed", {"xmlns": ATOM_NS})  # no ET namespace registry: no global state
    today = _rfc3339(now, FEED_EPOCH)

    def add(parent: ET.Element, tag: str, text: str = "", **attrs: str) -> ET.Element:
        node = ET.SubElement(parent, tag, attrs)
        if text:
            node.text = text
        return node

    add(feed, "title", _xml_text(SITE_TITLE))
    add(feed, "subtitle", _xml_text(SITE_DESC))
    add(feed, "id", SITE_URL)
    add(add(feed, "author"), "name", _xml_text(SITE_AUTHOR))
    add(feed, "updated", today)
    add(feed, "link", href=f"{SITE_URL}feed.xml", rel="self", type="application/atom+xml")
    add(feed, "link", href=SITE_URL, rel="alternate", type="text/html")
    seen: set[str] = set()
    for item in feed_items(payload):
        if item["link"] in seen:
            continue
        seen.add(item["link"])
        entry = add(feed, "entry")
        add(entry, "id", item["link"])
        add(entry, "title", _xml_text(item["title"]) or item["link"])
        add(entry, "updated", _rfc3339(item["updated"], today[:10]))
        add(entry, "link", href=item["link"], rel="alternate", type="text/html")
        add(entry, "summary", _xml_text(item["summary"]), type="text")
    ET.indent(feed)
    return f'<?xml version="1.0" encoding="utf-8"?>\n{ET.tostring(feed, encoding="unicode")}\n'


def render_feed_for_page(page: str) -> str:
    """The feed for a rendered page, from the payload and stamp it carries: exactly
    what the merge gate recomputes (the embedded payload, not the in-memory one)."""
    payload, stamp, problems = cc.embedded(page)
    if problems or payload is None:
        raise ValueError("; ".join(problems))
    return render_feed(payload, stamp)


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
    page = render(payload, now)
    (docs / "index.html").write_text(page, encoding="utf-8")
    (docs / "feed.xml").write_text(render_feed_for_page(page), encoding="utf-8")
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
