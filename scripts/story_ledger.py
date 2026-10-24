#!/usr/bin/env python3
"""
story_ledger.py — The permanent story ledger (data/news_stories.json).

A *story* is the unit the site shows: one row per real-world story, however
many outlets covered it. Pool entries are the analyzed coverage; the ledger
says which entries (and which unanalyzed covering sources) are the same story.
Rows never expire: no prune, no TTL, no age filter on load or save.

Row shape (keyed by story id):

    {"title": str, "entities": [str], "first_seen": "YYYY-MM-DD",
     "last_updated": "YYYY-MM-DD", "entry_ids": [str],
     "sources": [{"url", "source_name", "tier", "date", "title", "entry_id"?}],
     "updates": [{"date", "note", "url", "source_name", "claims_to_review"}]}

Matching a new candidate (ISC-20), in three steps:

1. `shortlist()` — deterministic, tuned to over-match: stories touched in the
   last `stories.match_window_days` that share a URL, title tokens, entities,
   or distinctive text with the candidate, or that newsworthy.py's same-story
   rule matches (a shared CVE/GHSA id, or shared rare proper nouns within
   days: what select_batch groups a run's copies by), best
   `stories.shortlist_max` first.
   `python scripts/story_ledger.py shortlist` writes data/story_shortlist.json.
2. A small-model judge (the scan's Haiku subagent, research-scan step 2b)
   writes data/story_verdicts.json: `[{candidate_id, verdict, story_id, note}]`
   with verdict `same` | `update` | `new`.
3. `apply_verdicts()` (called by merge_analysis.py) — `same` adds a covering
   source, `update` adds a covering source plus a dated Updated line and flags
   the story's linked claims for review (never auto-supersedes), `new` leaves
   the candidate for analysis. A verdict naming a story outside that
   candidate's shortlist is rejected, so the judge can't attach anything to
   an arbitrary story.

Pool entries reach the ledger through `assign_entry()`: a judged story id, else
a conservative deterministic match (the two-of-three URL/title/entity
collision rule in dedupe_stories.py; a homepage URL never counts), else a new
story.

Usage:
    python scripts/story_ledger.py shortlist   # stage data/story_shortlist.json
    python scripts/story_ledger.py backfill    # ledger every unledgered pool/archive entry
    python scripts/story_ledger.py check       # ledger integrity (exit 1 on problems)
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import date
from urllib.parse import urlparse

import common as c
import dedupe_stories as ds
import newsworthy as nw

LEDGER_FILE = c.DATA_DIR / "news_stories.json"
SHORTLIST_FILE = c.DATA_DIR / "story_shortlist.json"
VERDICTS_FILE = c.DATA_DIR / "story_verdicts.json"
# Code-owned record of what the verdicts did; run_scan.sh post puts it in the PR
# body. data/_* is never committed and never written by the model.
OUTCOMES_FILE = c.DATA_DIR / "_story_outcomes.md"
LEDGER_VERSION = 2
VERDICTS = ("same", "update", "new")
DEFAULT_WINDOW_DAYS = 90
DEFAULT_SHORTLIST_MAX = 5
# Over-match thresholds: any one admits a story to the shortlist.
SHORTLIST_TITLE = 0.2
SHORTLIST_ENTITY = 0.5
SHORTLIST_TEXT = 0.15
# A newsworthy.same_story match admits a story at this score. #104 (2026-10-23):
# covering articles for Cairn, x402, OpenCode, eMudhra, PAN-OS, BeyondTrust,
# Pillow and more never got their story offered, because a lead's analyzed
# title ("V12 audit of the x402 agent-payments protocol: 25 flaws...") shares
# few tokens with a news headline ("Critical x402 SDK Flaw Could Let ..."),
# while the rare name (x402) or the CVE id is the whole signal.
SHORTLIST_SAME_STORY = 0.6
_TIER_RANK = {"high": 3, "medium": 2, "low": 1}


# --- settings + small helpers ------------------------------------------------
def settings() -> dict:
    """`stories:` block of config.yaml, with defaults."""
    raw = (c.load_yaml(c.CONFIG_FILE) or {}).get("stories") or {}
    return {
        "match_window_days": int(raw.get("match_window_days", DEFAULT_WINDOW_DAYS)),
        "shortlist_max": int(raw.get("shortlist_max", DEFAULT_SHORTLIST_MAX)),
    }


def _ledger_path():
    return c.DATA_DIR / LEDGER_FILE.name


def _day(value: str | None) -> str:
    """A YYYY-MM-DD from a full or month-only date ('' when unknown)."""
    s = (value or "")[:10]
    if len(s) == 7:
        return s + "-01"
    return s if len(s) == 10 else ""


def _days_between(a: str, b: str) -> float | None:
    try:
        da, db = date.fromisoformat(a), date.fromisoformat(b)
    except ValueError:
        return None
    return abs((da - db).days)


def entry_day(entry: dict) -> str:
    return _day(entry.get("published") or entry.get("date"))


def _text(entry: dict) -> str:
    return f"{entry.get('title', '')} {entry.get('summary') or entry.get('excerpt') or ''}"


# --- load / save / migrate ---------------------------------------------------
def empty_ledger() -> dict:
    return {"version": LEDGER_VERSION, "stories": {}}


def migrate_legacy(index: dict) -> dict:
    """Turn the old 30-day story-key index ({sid: {fp, corroborators, ...}})
    into ledger rows. Entries are linked later by URL (sync_entries)."""
    ledger = empty_ledger()
    for sid, rec in index.items():
        fp = rec.get("fp") or {}
        first = _day(rec.get("first_seen")) or ""
        sources = [
            {"url": fp.get("url", ""), "source_name": "", "tier": rec.get("winner_tier", "")}
        ]
        sources += [dict(s) for s in rec.get("corroborators") or []]
        story = new_row(fp.get("title", ""), sorted(fp.get("entities") or []), first)
        for src in sources:
            add_source(story, {**src, "date": src.get("date") or first})
        ledger["stories"][sid] = story
    return ledger


def load_ledger(path=None) -> dict:
    """The ledger; a missing file is empty, a legacy index is migrated."""
    raw = c.load_json(path or _ledger_path(), default=None)
    if not raw:
        return empty_ledger()
    if raw.get("version") == LEDGER_VERSION:
        return raw
    return migrate_legacy(raw)


def save_ledger(ledger: dict, path=None) -> None:
    """One story per line, ordered by first_seen then id: a story change is a
    one-line git diff, and the file stays compact as it grows."""
    stories = ledger["stories"]
    order = sorted(stories, key=lambda sid: (stories[sid].get("first_seen", ""), sid))
    lines = [f"  {json.dumps(sid)}: {_compact(stories[sid])}" for sid in order]
    body = ",\n".join(lines)
    text = f'{{"version": {LEDGER_VERSION}, "stories": {{\n{body}\n}}}}\n'
    target = path or _ledger_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _compact(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, separators=(",", ":"))


# --- rows --------------------------------------------------------------------
def new_row(title: str, entities: list[str], day: str) -> dict:
    return {
        "title": title,
        "entities": entities,
        "first_seen": day,
        "last_updated": day,
        "entry_ids": [],
        "sources": [],
        "updates": [],
    }


def make_story_id(entry: dict, ledger: dict) -> str:
    """Stable id from the first coverage's canonical URL (else its title)."""
    seed = ds.canonical_url(entry.get("source_url") or entry.get("article_url") or "")
    seed = seed or entry.get("id") or entry.get("title", "")
    base = "s-" + hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
    sid, n = base, 2
    while sid in ledger["stories"]:
        sid, n = f"{base}-{n}", n + 1
    return sid


def source_row(entry: dict, *, tier: str = "", source_name: str = "", entry_id: str = "") -> dict:
    row = {
        "url": entry.get("source_url") or entry.get("article_url") or "",
        "source_name": source_name or entry.get("source_name") or "",
        "tier": tier,
        "date": entry_day(entry),
        "title": entry.get("title", ""),
    }
    if entry_id:  # an analyzed pool entry, not a bare covering source
        row["entry_id"] = entry_id
    return row


def add_source(story: dict, src: dict) -> bool:
    """Append a covering source unless its canonical URL is already there."""
    url = ds.canonical_url(src.get("url", ""))
    if any(url and ds.canonical_url(s.get("url", "")) == url for s in story["sources"]):
        return False
    row = {k: v for k, v in src.items() if v not in (None, "")}
    if row.get("title") == story.get("title"):
        row.pop("title")  # the story title already says it
    story["sources"].append(row)
    return True


def entry_index(ledger: dict) -> dict[str, str]:
    """{entry_id: story_id} across the ledger."""
    return {eid: sid for sid, row in ledger["stories"].items() for eid in row.get("entry_ids", [])}


def attach_entry(ledger: dict, sid: str, entry: dict, *, tier: str = "", source_name: str = ""):
    story = ledger["stories"][sid]
    if entry.get("id") and entry["id"] not in story["entry_ids"]:
        story["entry_ids"].append(entry["id"])
    src = source_row(entry, tier=tier, source_name=source_name, entry_id=entry.get("id") or "")
    add_source(story, src)
    story["entities"] = sorted(set(story["entities"]) | ds.entities(*_head(entry)))
    day = entry_day(entry)
    if day and (not story["first_seen"] or day < story["first_seen"]):
        story["first_seen"] = day
    if day and day > story.get("last_updated", ""):
        story["last_updated"] = day


def _head(entry: dict) -> tuple[str, str]:
    return entry.get("title", ""), (entry.get("summary") or entry.get("excerpt") or "")[:200]


def create_story(ledger: dict, entry: dict, *, tier: str = "", source_name: str = "") -> str:
    sid = make_story_id(entry, ledger)
    ledger["stories"][sid] = new_row(entry.get("title", ""), [], entry_day(entry))
    attach_entry(ledger, sid, entry, tier=tier, source_name=source_name)
    return sid


# --- conservative deterministic match (backfill + unjudged entries) ----------
def _in_window(story: dict, day: str, window_days: int) -> bool:
    gap = _days_between(story.get("last_updated") or story.get("first_seen", ""), day)
    return gap is None or gap <= window_days


def _fp(url: str, title: str, entities: set[str]) -> dict:
    fp = ds.story_fingerprint({"title": title, "source_url": url})
    if urlparse(fp["url"]).path in ("", "/"):
        fp["url"] = ""  # a homepage URL says nothing about which story it is
    fp["entities"] = entities
    return fp


def find_clear_duplicate(ledger: dict, entry: dict, window_days: int) -> str | None:
    """Only clear duplicates: the two-of-three collision rule (URL, title,
    entities) against any covering source of a story touched within the
    window. Paraphrased follow-ups are the judge's job, not this one's."""
    url = entry.get("source_url") or entry.get("article_url") or ""
    fp = _fp(url, entry.get("title", ""), ds.entities(*_head(entry)))
    day = entry_day(entry)
    for sid, story in ledger["stories"].items():
        if day and not _in_window(story, day, window_days):
            continue
        ents = set(story.get("entities") or [])
        for src in story["sources"]:
            other = _fp(src.get("url", ""), src.get("title") or story["title"], ents)
            if ds.is_collision(fp, other):
                return sid
    return None


def assign_entry(
    ledger: dict,
    entry: dict,
    *,
    story_id: str | None = None,
    force_new: bool = False,
    tier: str = "",
    source_name: str = "",
    window_days: int = DEFAULT_WINDOW_DAYS,
) -> tuple[str, str]:
    """Put a pool entry in the ledger. Returns (story_id, how) where how is
    known | judged | duplicate | new."""
    known = entry_index(ledger).get(entry.get("id") or "")
    kw = {"tier": tier, "source_name": source_name}
    if known:
        attach_entry(ledger, known, entry, **kw)
        return known, "known"
    if story_id and story_id in ledger["stories"]:
        attach_entry(ledger, story_id, entry, **kw)
        return story_id, "judged"
    if not force_new:
        sid = find_clear_duplicate(ledger, entry, window_days)
        if sid:
            attach_entry(ledger, sid, entry, **kw)
            return sid, "duplicate"
    return create_story(ledger, entry, **kw), "new"


def _tier_of(entry: dict, sources_by_id: dict) -> tuple[str, str]:
    src = sources_by_id.get(entry.get("source_id") or "", {})
    return src.get("tier", ""), src.get("name", "") or entry.get("source_name") or ""


def sync_entries(
    ledger: dict, entries: list[dict], sources_by_id: dict | None = None, window_days=None
) -> list[dict]:
    """Ledger every entry not yet in it, oldest first. Returns one report row
    per entry that joined an EXISTING story (the merges a human should see)."""
    sources_by_id = sources_by_id or {}
    window = window_days or DEFAULT_WINDOW_DAYS
    known = entry_index(ledger)
    merges: list[dict] = []
    for entry in sorted(entries, key=lambda e: (entry_day(e), e.get("id") or "")):
        if not entry.get("id") or entry["id"] in known:
            continue
        tier, name = _tier_of(entry, sources_by_id)
        sid, how = assign_entry(ledger, entry, tier=tier, source_name=name, window_days=window)
        known[entry["id"]] = sid
        if how == "duplicate" and len(ledger["stories"][sid]["entry_ids"]) > 1:
            merges.append(
                {
                    "story_id": sid,
                    "entry_id": entry["id"],
                    "how": how,
                    "title": entry.get("title", ""),
                    "story": ledger["stories"][sid]["title"],
                }
            )
    return merges


def all_entries() -> list[dict]:
    """Every pool entry plus the archive (archived entries stay in their story)."""
    archive = c.load_json(c.ARCHIVE_FILE, default=[]) or []
    return c.all_pool_entries() + list(archive)


def sync_and_save() -> list[dict]:
    """Load, ledger every unledgered entry, save. Never prunes."""
    ledger = load_ledger()
    before = c.load_json(_ledger_path(), default=None)
    merges = sync_entries(
        ledger, all_entries(), c.load_sources_by_id(), settings()["match_window_days"]
    )
    if before != ledger:
        save_ledger(ledger)
    return merges


def render_context() -> tuple[dict, dict[str, str]]:
    """(ledger, {entry_id: story_id}) with every pool + archive entry ledgered
    IN MEMORY. Renderers use this and never write the ledger; rerank.py does."""
    ledger = load_ledger()
    sync_entries(ledger, all_entries(), c.load_sources_by_id(), settings()["match_window_days"])
    return ledger, entry_index(ledger)


# --- shortlist (deterministic, over-matching) --------------------------------
def _content_tokens(text: str) -> set[str]:
    return {t for t in ds._tokens(text) if len(t) > 2 and not t.isdigit()}


def story_text(story: dict, entries_by_id: dict) -> str:
    parts = [story.get("title", "")] + [s.get("title", "") for s in story["sources"]]
    parts += [_text(entries_by_id[e]) for e in story.get("entry_ids", []) if e in entries_by_id]
    parts += [u.get("note", "") for u in story.get("updates", [])]
    return " ".join(parts)


def _idf(docs: list[set[str]]) -> dict[str, float]:
    n = len(docs) or 1
    df: dict[str, int] = {}
    for doc in docs:
        for t in doc:
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (k + 0.5)) for t, k in df.items()}


def _containment(cand: set[str], story: set[str], idf: dict, default: float) -> float:
    den = sum(idf.get(t, default) for t in cand)
    return sum(idf.get(t, default) for t in cand & story) / den if den else 0.0


def match_score(cand: dict, prof: dict, idf: dict, default: float) -> float:
    """0..1; 0 means 'not shortlisted'. Any one signal admits (over-match)."""
    url = cand["url"] and cand["url"] in prof["urls"]
    title = max(ds.title_similarity(cand["title"], t) for t in prof["titles"])
    ent = ds.overlap_coefficient(cand["entities"], prof["entities"])
    text = _containment(cand["tokens"], prof["tokens"], idf, default)
    if not (url or title >= SHORTLIST_TITLE or ent >= SHORTLIST_ENTITY or text >= SHORTLIST_TEXT):
        return 0.0
    return 1.0 if url else max(title, text, 0.5 * ent + 0.5 * text)


def _profile(story: dict, entries_by_id: dict) -> dict:
    return {
        "urls": {ds.canonical_url(s.get("url", "")) for s in story["sources"]} - {""},
        "titles": [story.get("title", "")] + [s.get("title", "") for s in story["sources"]],
        "entities": set(story.get("entities") or []),
        "tokens": _content_tokens(story_text(story, entries_by_id)),
    }


def _cand_profile(cand: dict) -> dict:
    return {
        "url": ds.canonical_url(cand.get("source_url") or cand.get("article_url") or ""),
        "title": cand.get("title", ""),
        "entities": ds.entities(*_head(cand)),
        "tokens": _content_tokens(_text(cand)),
    }


def story_docs(story: dict, entries_by_id: dict) -> list[dict]:
    """The story as newsworthy.py documents: every covering source's headline
    (the story title when the row has none) and every analyzed entry (title +
    summary), each dated and with its URL (for its publisher)."""
    first = story.get("first_seen") or story.get("last_updated") or ""
    docs = [
        {
            "title": s.get("title") or story.get("title", ""),
            "published": s.get("date") or first,
            "source_url": s.get("url", ""),
        }
        for s in story["sources"]
    ]
    for eid in story.get("entry_ids", []):
        e = entries_by_id.get(eid)
        if e:
            body = e.get("summary") or e.get("excerpt") or ""
            docs.append({**e, "excerpt": body, "published": entry_day(e)})
    return docs or [{"title": story.get("title", ""), "published": first}]


SameStoryDoc = tuple[nw.Profile, str]  # (profile, publisher)


def same_story_profiles(
    ledger: dict, entries_by_id: dict, cands: list[dict]
) -> tuple[nw.NameModel, dict[str, list[SameStoryDoc]]]:
    """newsworthy.py's name model (reference = the analyzed entries) and each
    story's documents as (profile, publisher), for the same-story signal."""
    model = nw.name_model(list(entries_by_id.values()), cands)
    profs = {
        sid: [(nw.profile(d, model), nw.publisher(d)) for d in story_docs(story, entries_by_id)]
        for sid, story in ledger["stories"].items()
    }
    return model, profs


def same_story_hit(cand: nw.Profile, publisher: str, story: list[SameStoryDoc]) -> bool:
    """newsworthy's rule with its same-days windows widened to MATCH_DAYS: the
    shortlist over-matches by design (the judge reads it), and the strict
    2-day window is tuned for lane corroboration, where a false match costs a
    slot. A copy naming only CVEs the story doesn't is still never offered.
    Publisher-aware: against a document from the candidate's own publisher
    only a shared CVE/GHSA id counts, since one outlet's posts share its own
    names (Wiz's blog says "Wiz" in every title)."""
    for doc, pub in story:
        if pub and pub == publisher:
            if cand.ids & doc.ids:
                return True
        elif nw.same_story(cand, doc, title_days=nw.MATCH_DAYS):
            return True
    return False


def shortlist_many(
    cands: list[dict], ledger: dict, entries_by_id: dict, *, window_days: int, k: int
) -> dict[str, list[dict]]:
    """{candidate_id: [{story_id, score, title, last_updated}]} — best k per
    candidate among stories touched within window_days of the candidate.
    Admitted by token/title/entity overlap (match_score) or by newsworthy.py's
    same-story rule (SHORTLIST_SAME_STORY)."""
    profiles = {sid: _profile(s, entries_by_id) for sid, s in ledger["stories"].items()}
    idf = _idf([p["tokens"] for p in profiles.values()])
    default = math.log(len(profiles) + 1) + 1 if profiles else 1.0
    model, nw_profiles = same_story_profiles(ledger, entries_by_id, cands)
    out: dict[str, list[dict]] = {}
    for cand in cands:
        cp, day = _cand_profile(cand), entry_day(cand) or c.utcnow().strftime("%Y-%m-%d")
        np_, pub = nw.profile(cand, model), nw.publisher(cand)
        scored = []
        for sid, story in ledger["stories"].items():
            if not _in_window(story, day, window_days):
                continue
            score = match_score(cp, profiles[sid], idf, default)
            if same_story_hit(np_, pub, nw_profiles[sid]):
                score = max(score, SHORTLIST_SAME_STORY)
            if score > 0:
                scored.append((score, sid))
        scored.sort(key=lambda x: (-x[0], x[1]))
        out[cand.get("id") or ""] = [_short_row(ledger, sid, s) for s, sid in scored[:k]]
    return out


def _short_row(ledger: dict, sid: str, score: float) -> dict:
    story = ledger["stories"][sid]
    return {
        "story_id": sid,
        "score": round(score, 3),
        "title": story["title"],
        "last_updated": story.get("last_updated", ""),
        "sources": [s.get("source_name") or s.get("url", "") for s in story["sources"]][:6],
        "latest_update": (story.get("updates") or [{}])[-1].get("note", ""),
    }


def write_shortlist() -> int:
    """Stage data/story_shortlist.json for the judge. Returns candidates with a
    non-empty shortlist (the ones the judge must look at)."""
    ledger = load_ledger()
    sync_entries(ledger, all_entries(), c.load_sources_by_id(), settings()["match_window_days"])
    by_id = {e["id"]: e for e in all_entries() if e.get("id")}
    conf = settings()
    out = shortlist_many(
        c.load_candidates(),
        ledger,
        by_id,
        window_days=conf["match_window_days"],
        k=conf["shortlist_max"],
    )
    c.save_json(c.DATA_DIR / SHORTLIST_FILE.name, out)
    return sum(1 for rows in out.values() if rows)


# --- verdicts ------------------------------------------------------------------
def linked_claims(story: dict, entries_by_id: dict) -> list[str]:
    ids: set[str] = set()
    for eid in story.get("entry_ids", []):
        ids |= set(entries_by_id.get(eid, {}).get("related_claims") or [])
    return sorted(ids)


def apply_verdict(
    ledger: dict,
    cand: dict,
    verdict: dict,
    *,
    allowed: list[str],
    tier: str = "",
    entries_by_id: dict | None = None,
) -> dict:
    """Apply one judge verdict. Returns {action, story_id, reason?}; action is
    same | update | new | rejected. Only same/update write the ledger."""
    v, sid = verdict.get("verdict"), verdict.get("story_id")
    base = {
        "candidate_id": cand.get("id"),
        "story_id": sid,
        "title": cand.get("title", ""),
        "url": cand.get("source_url", ""),
        "tier": tier,
    }
    if v not in VERDICTS:
        return {**base, "action": "rejected", "reason": f"unknown verdict {v!r}"}
    if v == "new":
        return {**base, "action": "new", "story_id": None}
    if sid not in allowed or sid not in ledger["stories"]:
        return {
            **base,
            "action": "rejected",
            "reason": "story_id not in this candidate's shortlist",
        }
    story = ledger["stories"][sid]
    add_source(story, source_row(cand, tier=tier))
    if v == "update":
        day = entry_day(cand) or c.utcnow().strftime("%Y-%m-%d")
        claims = linked_claims(story, entries_by_id or {})
        note = str(verdict.get("note") or cand.get("title", ""))[:280]
        row = {
            "date": day,
            "note": note,
            "url": cand.get("source_url", ""),
            "source_name": cand.get("source_name", ""),
            "claims_to_review": claims,
        }
        if not any(u.get("url") == row["url"] for u in story["updates"]):
            story["updates"].append(row)
        story["last_updated"] = max(story.get("last_updated", ""), day)
        return {**base, "action": "update", "claims_to_review": claims}
    return {**base, "action": "same"}


def apply_verdicts(
    ledger: dict,
    verdicts: list[dict],
    candidates: list[dict],
    shortlists: dict,
    *,
    sources_by_id: dict | None = None,
    entries_by_id: dict | None = None,
) -> list[dict]:
    """Apply every verdict whose candidate is staged. Unstaged → rejected."""
    by_id = {cand.get("id"): cand for cand in candidates}
    out = []
    for verdict in verdicts:
        cand = by_id.get(verdict.get("candidate_id"))
        if cand is None:
            out.append({**verdict, "action": "rejected", "reason": "candidate not staged"})
            continue
        allowed = [row["story_id"] for row in shortlists.get(cand["id"], [])]
        tier, _ = _tier_of(cand, sources_by_id or {})
        out.append(
            apply_verdict(
                ledger, cand, verdict, allowed=allowed, tier=tier, entries_by_id=entries_by_id
            )
        )
    return out


def corroborate_entry(entry: dict, src: dict) -> bool:
    """Record a judged `same`/`update` source on the story's lead pool entry,
    in `story_corroboration` — NOT `corroborating_sources`. A verdict comes
    from a model that read untrusted text, so it only earns what
    common.credibility_of allows (high/medium tier, a different host) and
    never satisfies the HN-standalone rule or keeps a story out of the prune."""
    corr = entry.setdefault("story_corroboration", [])
    nu = c.normalize_url(src.get("url", ""))
    if not nu or nu == c.normalize_url(entry.get("source_url", "")):
        return False
    known = (entry.get("corroborating_sources") or []) + corr
    if any(c.normalize_url(s.get("url", "")) == nu for s in known):
        return False
    corr.append(
        {
            "name": src.get("source_name"),
            "url": src.get("url"),
            "tier": src.get("tier") or "",
            "published": src.get("date"),
        }
    )
    return True


def outcomes_record(outcomes: list[dict]) -> str:
    """The code-owned markdown record of one verdict application."""
    counts = {a: sum(1 for o in outcomes if o["action"] == a) for a in (*VERDICTS, "rejected")}
    lines = [
        "### Story verdicts (applied by merge_analysis.py)",
        "",
        ", ".join(f"{n} {a}" for a, n in counts.items()),
        "",
    ]
    for o in outcomes:
        act, sid, url = o["action"], o.get("story_id") or "-", o.get("url") or "-"
        if act in ("same", "update"):
            lines.append(f"- `{act}`: {url} -> story `{sid}`")
        if act == "update" and o.get("claims_to_review"):
            lines.append(
                f"  - CLAIM REVIEW: linked claims {', '.join(o['claims_to_review'])} "
                "may need supersession (not automatic)"
            )
        if act == "rejected":
            lines.append(f"- rejected `{o.get('candidate_id')}`: {o.get('reason')}")
    return "\n".join(lines) + "\n"


def settled_count(record: str) -> int:
    """`same`/`update` verdicts applied, read back from outcomes_record() text."""
    return sum(1 for ln in record.splitlines() if ln.startswith(("- `same`:", "- `update`:")))


def append_outcomes(outcomes: list[dict]) -> None:
    path = c.DATA_DIR / OUTCOMES_FILE.name
    prior = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(prior + ("\n" if prior else "") + outcomes_record(outcomes), encoding="utf-8")


def recompute_shortlists(ledger: dict, cands: list[dict], entries_by_id: dict) -> dict:
    """The shortlists a verdict is checked against: recomputed from the ledger
    and the staged candidates, never read back from data/story_shortlist.json
    (which the model session could have edited)."""
    conf = settings()
    sync_entries(
        ledger, list(entries_by_id.values()), c.load_sources_by_id(), conf["match_window_days"]
    )
    return shortlist_many(
        cands, ledger, entries_by_id, window_days=conf["match_window_days"], k=conf["shortlist_max"]
    )


# --- integrity ---------------------------------------------------------------
def check_ledger(ledger: dict) -> list[str]:
    """Ledger integrity: every entry belongs to exactly one story, and every
    row carries the fields the schema promises."""
    errors, owner = [], {}
    for sid, row in ledger["stories"].items():
        for key in ("title", "first_seen", "last_updated", "entry_ids", "sources", "updates"):
            if key not in row:
                errors.append(f"{sid}: missing {key}")
        for eid in row.get("entry_ids", []):
            if eid in owner:
                errors.append(f"entry {eid} in two stories: {owner[eid]} and {sid}")
            owner[eid] = sid
    return errors


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "shortlist":
        n = write_shortlist()
        print(f"story shortlist: {n} candidate(s) match a known story -> {SHORTLIST_FILE.name}")
        return 0
    if cmd == "backfill":
        merges = sync_and_save()
        ledger = load_ledger()
        print(f"story ledger: {len(ledger['stories'])} stories; {len(merges)} merge(s)")
        for m in merges:
            print(f"  [{m['how']}] {m['entry_id']} -> {m['story_id']} ({m['story'][:70]})")
        return 0
    if cmd == "check":
        errors = check_ledger(load_ledger())
        for e in errors:
            print(f"  - {e}")
        return 1 if errors else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
