#!/usr/bin/env python3
"""
common.py — Shared foundation for the research analyzer pipeline.

Everything that more than one script needs lives here: path constants, config
loading, the entry schema + validation, small text/url helpers (reused by the
aggregators), deterministic scoring math (reused by rerank + tests), and the
Jina Reader article fetch used by every ingestion path.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Windows consoles default to cp1252, which can't encode much of the research
# text we print (curly quotes, non-breaking hyphens, emoji). Force UTF-8 so the
# pipeline never crashes on a stray glyph.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):  # pragma: no cover - already-detached streams
            pass

try:
    import truststore
    import yaml
    from dateutil import parser as dateparser
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Missing dependencies. Run: pip install -r requirements.txt") from exc

import taxonomy  # noqa: E402  (after the dependency guard: it needs yaml)

# Use the OS-native certificate trust store (Windows/macOS/Linux) instead of
# the bundled `certifi` CA list. A stale or unlucky `certifi` release can
# silently break ingestion of major sources (OpenAI, Anthropic, GitHub
# Security Lab, etc. all failed with "certificate has expired" simultaneously
# in Sept 2026, even though their real certs were valid — `certifi`'s bundle
# had simply drifted from what the OS already trusted). This monkey-patches
# `ssl.SSLContext` process-wide, so it must run before any HTTPS request is
# made by feedparser/urllib/requests in this process.
truststore.inject_into_ssl()

# --- Paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_FILE = ROOT / "config.yaml"
SOURCES_FILE = ROOT / "scripts" / "sources.yaml"

CANDIDATES_FILE = DATA_DIR / "candidates.json"
ANALYSIS_OUT = DATA_DIR / "analysis_out.json"
ARCHIVE_FILE = DATA_DIR / "archive.json"
RAW_DIR = DATA_DIR / "_raw"

SCHEMA_VERSION = "3.0"
JINA_READER = "https://r.jina.ai/"

# Several source sites (OpenAI Blog, Wired, tldr;sec, GitHub Security Lab)
# reject the default library User-Agent (e.g. "Python-urllib/3.x",
# "feedparser/6.x") with HTTP 403 — an explicit, honestly-identifying UA
# clears it. Shared so every outbound request identifies consistently.
HTTP_USER_AGENT = "AwesomeSecurityResearch/1.0"

# --- Topics: the three tracked databases -----------------------------------
# Each topic is its own rolling pool + rendered directory. `domains` are the
# topic's domain IDs from data/taxonomy.yaml (enforced at merge; taxonomy.py).
TOPICS: dict[str, dict] = {
    "ai-security": {
        "name": "AI Security",
        "blurb": "Securing AI systems: harness & agent security, MCP, skill scanning, "
        "prompt injection, memory poisoning, model supply chain, LLM red-teaming.",
    },
    "product-security": {
        "name": "Product Security",
        "blurb": "Securing products: application security, supply chain, cloud & infra, "
        "identity, mobile, plus red teaming and threat modeling (AI-assisted or not).",
    },
    "ai-research": {
        "name": "AI Research",
        "blurb": "Practitioner AI: improving your harness, understanding, and architecture "
        "for using LLMs/agents on real tasks. Not model internals or ML-research.",
    },
}
for _topic, _meta in TOPICS.items():
    _meta["domains"] = [d.id for d in taxonomy.get().for_topic(_topic)]

# Convenience: {topic: [domain ids]} (mirrors the old TRACK_DOMAINS shape).
TOPIC_DOMAINS: dict[str, list[str]] = {k: v["domains"] for k, v in TOPICS.items()}

POOL_FILES: dict[str, Path] = {t: DATA_DIR / f"{t}.json" for t in TOPICS}

# Maps the legacy 2-track domains onto the three topics (used to migrate old
# data and to coarse-guess a topic at ingest from the keyword classifier).
LEGACY_DOMAIN_TO_TOPIC: dict[str, str] = {
    "AI Security": "ai-security",
    "Web Application Security": "product-security",
    "Mobile Security": "product-security",
    "Agents & Harnesses": "ai-research",
    "Prompting & Context": "ai-research",
    "Models & Capabilities": "ai-research",
    "Tooling & Infrastructure": "ai-research",
    "Evaluation & Safety": "ai-research",
}

# The pre-taxonomy TOPICS "suggested domains" display names. Main's
# topic_for_domain resolved these by TOPICS membership; frozen here so an ingest
# path handing one in still guesses the same topic (tests pin the whole table).
_OLD_TOPIC_DOMAINS: dict[str, tuple[str, ...]] = {
    "ai-security": ("Harness & Agent Security", "MCP & Tools", "Prompt Injection",
                    "Memory & Context Poisoning", "Model Supply Chain", "LLM Red-Teaming",
                    "RAG / Data Poisoning", "Information Disclosure"),
    "product-security": ("Application Security", "Supply Chain & Dependencies",
                         "Cloud & Infrastructure", "Identity & Access", "Mobile Security",
                         "Threat Modeling & Red Teaming", "Detection & Response",
                         "AI-Generated Code Risk"),
    "ai-research": ("Agents & Harnesses", "Prompting & Context", "Tooling & Infrastructure",
                    "Evaluation", "Architecture & Optimization", "Models & Capabilities"),
}  # fmt: skip
for _topic, _names in _OLD_TOPIC_DOMAINS.items():
    for _name in _names:
        LEGACY_DOMAIN_TO_TOPIC.setdefault(_name, _topic)

DISCOVERED_VIA = ("twitter", "linkedin", "rss", "github", "youtube", "manual")


def domain_slug(domain: str) -> str:
    """Directory-safe slug for a domain: an ID's slug part ('ais.mcp-tools' ->
    'mcp-tools'), else the slugified label ('AI Security' -> 'ai-security')."""
    dom = taxonomy.get().domains.get(domain)
    return dom.slug if dom else slugify(domain)


def moved_slug(entry: dict) -> str | None:
    """The directory an entry's page lived in before domains became taxonomy
    IDs (the slugified free-text label, from `domain_label` provenance), when it
    differs from today's. Renderers leave a "Moved" stub there so old links work."""
    label = entry.get("domain_label")
    if not label:
        return None
    old = slugify(label)
    return old if old != domain_slug(entry.get("domain") or "General") else None


def title_slug(title: str | None) -> str:
    """The title part of an entry's page filename (generate_site.entry_filename)."""
    return slugify(title or "", 60)


def carry_previous_slugs(old: dict, new: dict) -> dict:
    """`new` (an updated copy of `old`) keeping every page slug `old` ever had.

    When a retitle changes the page slug, the old slug is appended to
    `previous_slugs` so the renderers can leave a "Moved" stub at the old page
    path. Every code path that changes an existing entry's title goes through
    this (merge_analysis.reconcile, retitle)."""
    prev: list[str] = []
    for slug in list(old.get("previous_slugs") or []) + list(new.get("previous_slugs") or []):
        if isinstance(slug, str) and slug and slug not in prev:
            prev.append(slug)
    if old.get("title") and title_slug(old["title"]) not in prev:
        prev.append(title_slug(old["title"]))
    current = title_slug(new.get("title"))
    prev = [s for s in prev if s != current]
    out = {k: v for k, v in new.items() if k != "previous_slugs"}
    return {**out, "previous_slugs": prev} if prev else out


def retitle(entry: dict, title: str) -> dict:
    """A copy of `entry` with a new title, recording the old page slug."""
    return carry_previous_slugs(entry, {**entry, "title": title})


def former_page_paths(entry: dict) -> list[tuple[str, str]]:
    """(domain dir, filename) of every page path this entry used to have: its
    pre-taxonomy dir (moved_slug) and every previous title slug, in any mix.
    Excludes its current path. Renderers leave a "Moved" stub at each."""
    date = entry.get("date") or "undated"
    here = domain_slug(entry.get("domain") or "General")
    dirs = [here] + [d for d in [moved_slug(entry)] if d]
    slugs = [title_slug(entry.get("title"))] + [
        s for s in entry.get("previous_slugs") or [] if isinstance(s, str) and s
    ]
    current = (here, f"{date}-{slugs[0]}.md")
    out: list[tuple[str, str]] = []
    for d in dirs:
        for s in slugs:
            path = (d, f"{date}-{s}.md")
            if path != current and path not in out:
                out.append(path)
    return out


def domain_name(domain: str) -> str:
    """Display name for a domain ID; a non-ID label passes through."""
    return taxonomy.get().name(domain)


def topic_for_domain(domain: str) -> str | None:
    """Topic for a domain ID, else exactly what main's pre-taxonomy code returned
    for a legacy ingest label (None for anything it didn't know)."""
    dom = taxonomy.get().domains.get(domain)
    return dom.topic if dom else LEGACY_DOMAIN_TO_TOPIC.get(domain)


# --- Config ----------------------------------------------------------------
@dataclass(frozen=True)
class Config:
    weights: dict[str, float]
    half_life_days: float
    confidence_min: float
    limits: dict[str, int]
    curation: dict[str, float]
    max_age_days: int
    snapshot_days: int
    news_front_page_days: int = 7
    news_front_page_max: int = 30


def load_config(path: Path = CONFIG_FILE) -> Config:
    raw = load_yaml(path)
    weights = raw["weights"]
    total = sum(weights.get(k, 0) for k in ("newness", "novelty", "relevance", "credibility"))
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"config weights must sum to 1.0 (got {total})")
    return Config(
        weights=weights,
        half_life_days=float(raw["half_life_days"]),
        confidence_min=float(raw["confidence_min"]),
        limits=raw.get("limits", {}),
        curation=raw.get("curation", {}),
        max_age_days=int(raw.get("max_age_days", 31)),
        snapshot_days=int(raw.get("snapshot_days", 7)),
        news_front_page_days=int(raw.get("news_front_page_days", 7)),
        news_front_page_max=int(raw.get("news_front_page_max", 30)),
    )


# --- IO --------------------------------------------------------------------
def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def empty_pool(topic: str) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "topic": topic,
        "name": TOPICS[topic]["name"],
        "domains": TOPICS[topic]["domains"],
        "entries": [],
    }


def load_pool(topic: str) -> dict:
    pool = load_json(POOL_FILES[topic], default=None)
    return pool if pool else empty_pool(topic)


def save_pool(topic: str, pool: dict) -> None:
    save_json(POOL_FILES[topic], pool)


# --- Text / URL helpers (reused by both aggregators) -----------------------
def normalize_url(url: str) -> str:
    url = (url or "").strip().lower()
    url = re.sub(r"#.*$", "", url)
    url = re.sub(r"\?.*$", "", url)
    return url.rstrip("/")


_TRACKING_PARAM = re.compile(r"^(utm_|fbclid|gclid|mc_|ref$|ref_|igshid|si$)", re.I)


def clean_source_url(url: str) -> str:
    """Strip tracking query params (utm_*, fbclid, …) for clean public citations.

    Keeps meaningful query params; only removes known tracking keys. Preserves
    case and path (unlike normalize_url, which is for de-duplication only).
    """
    url = (url or "").strip()
    if "?" not in url:
        return url
    base, _, query = url.partition("?")
    kept = [
        pair
        for pair in query.split("&")
        if pair and not _TRACKING_PARAM.match(pair.split("=", 1)[0])
    ]
    return f"{base}?{'&'.join(kept)}" if kept else base


# Link shorteners whose URLs we resolve to the final destination at ingest, so
# the same article via a tweet (t.co/…) and via RSS (the permalink) de-dup.
SHORTENER_HOSTS = (
    "t.co",
    "bit.ly",
    "buff.ly",
    "lnkd.in",
    "ow.ly",
    "goo.gl",
    "tinyurl.com",
    "trib.al",
    "dlvr.it",
    "ift.tt",
    "hubs.ly",
    "spr.ly",
)


def resolve_redirects(url: str, timeout: int = 12) -> str:
    """If `url` is a known shortener, follow redirects to the final URL (network,
    best-effort). Returns the original URL unchanged on any failure or non-shortener."""
    host = re.sub(r"^https?://(www\.)?", "", (url or "").lower()).split("/", 1)[0]
    if host not in SHORTENER_HOSTS:
        return url
    import requests  # local import keeps offline unit tests import-clean

    try:
        resp = requests.head(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": HTTP_USER_AGENT},
        )
        return resp.url or url
    except Exception:  # noqa: BLE001 - resolution is best-effort
        return url


def slugify(text: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:limit].strip("-") or "item"


def make_id(title: str, url: str) -> str:
    digest = hashlib.sha1((title + url).encode("utf-8")).hexdigest()[:10]
    return f"{slugify(title, 48)}-{digest}"


def clean_summary(raw: str, limit: int = 320) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


# Fold typographic unicode so a verbatim quote isn't rejected over a dash/curly quote.
_PUNCT_FOLD = str.maketrans(
    {
        "–": "-",
        "—": "-",
        "−": "-",  # en/em dash, minus
        "‘": "'",
        "’": "'",
        "‚": "'",
        "′": "'",  # curly singles / prime
        "“": '"',
        "”": '"',
        "„": '"',
        "″": '"',  # curly doubles
        " ": " ",
        "​": "",
        " ": " ",  # nbsp, zero/thin spaces
    }
)


def normalize_text(s: str) -> str:
    """Lowercase, fold typographic punctuation, and collapse whitespace — so a
    verbatim quote grounds even if the source uses en-dashes or curly quotes."""
    s = (s or "").translate(_PUNCT_FOLD).replace("…", "...")
    return re.sub(r"\s+", " ", s.lower()).strip()


def is_grounded(excerpt: str, source_text: str, threshold: float = 0.85) -> bool:
    """True if `excerpt` genuinely appears in `source_text` — verbatim after
    normalization, or a near-verbatim longest-common-substring (tolerates minor
    punctuation/whitespace). A paraphrased or invented 'quote' fails this."""
    ne, ns = normalize_text(excerpt), normalize_text(source_text)
    if not ne or not ns:
        return False
    if ne in ns:
        return True
    match = SequenceMatcher(None, ne, ns).find_longest_match(0, len(ne), 0, len(ns))
    return match.size >= threshold * len(ne)


def title_similar(a: str, b: str, threshold: float = 0.87) -> bool:
    """Fuzzy title match for cross-source de-duplication."""
    na = re.sub(r"\s+", " ", (a or "").lower()).strip()
    nb = re.sub(r"\s+", " ", (b or "").lower()).strip()
    if not na or not nb:
        return False
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def entry_datetime(entry: dict) -> datetime | None:
    for key in ("published", "updated", "created"):
        val = entry.get(key)
        if val:
            try:
                dt = dateparser.parse(val)
                return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt
            except (ValueError, OverflowError, TypeError):
                continue
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            return datetime(*val[:6], tzinfo=UTC)
    return None


def extract_urls(text: str) -> list[str]:
    """Pull http(s) URLs out of free text (tweet bodies), de-duplicated."""
    found = re.findall(r"https?://[^\s<>\"')]+", text or "")
    seen: dict[str, None] = {}
    for url in found:
        seen.setdefault(url.rstrip(".,);"), None)
    return list(seen)


def date_from_url(url: str) -> str | None:
    """Extract a publish date embedded in a URL path, e.g. /2026/05/13/ or
    /2026/05/. Returns YYYY-MM-DD or YYYY-MM, or None. Many blogs (OWASP, Unit42,
    Google, Microsoft, Project Zero) date their permalinks this way."""
    m = re.search(r"/(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])(?:/|-)", url or "")
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"/(20\d{2})/(0[1-9]|1[0-2])/", url or "")
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None


def to_month(date: str | None) -> str | None:
    """Coerce a full or partial date string to YYYY-MM (for newness scoring)."""
    return date[:7] if date and len(date) >= 7 and date[4] == "-" else None


def best_date(entry: dict) -> str | None:
    """The most precise source date available for an entry."""
    return entry.get("published") or entry.get("date")


def parse_date_end(date: str | None) -> datetime | None:
    """Parse YYYY-MM-DD, or YYYY-MM as the LAST day of that month (lenient — a
    month-only date shouldn't age out early). Returns None if unparseable."""
    if not date:
        return None
    try:
        return datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC)
    except (ValueError, TypeError):
        pass
    try:
        start = datetime.strptime(date[:7], "%Y-%m").replace(tzinfo=UTC)
    except (ValueError, TypeError):
        return None
    nxt = start.replace(year=start.year + (start.month == 12), month=start.month % 12 + 1)
    return nxt - timedelta(days=1)


def is_fresh(entry: dict, max_age_days: int, now: datetime | None = None) -> bool:
    """True if the entry's source date is within the freshness window. Undated
    entries are treated as fresh (we don't drop what we can't date)."""
    dt = parse_date_end(best_date(entry))
    if dt is None:
        return True
    now = now or utcnow()
    return (now - dt).days <= max_age_days


# --- Scoring math (deterministic; shared by rerank + tests) ----------------
def parse_month(date: str) -> datetime | None:
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(date, fmt).replace(tzinfo=UTC)
        except (ValueError, TypeError):
            continue
    return None


def newness_score(date: str, half_life_days: float, now: datetime | None = None) -> int:
    """Time-decayed newness in [0, 100]; halves every half_life_days."""
    published = parse_month(date)
    if published is None:
        return 0
    now = now or utcnow()
    age_days = max(0.0, (now - published).total_seconds() / 86400.0)
    return round(100 * math.exp(-age_days / max(1.0, half_life_days)))


COMPOSITE_AXES = ("newness", "novelty", "relevance", "credibility")


def composite_score(scores: dict, weights: dict[str, float]) -> float:
    total = sum(weights.get(axis, 0.0) * float(scores.get(axis, 0) or 0) for axis in COMPOSITE_AXES)
    return round(total, 2)


CORROBORATION_BONUS = 5  # credibility points per independent corroborating source
CORROBORATION_CAP = 4  # …up to this many sources


def _host(url: str) -> str:
    host = urlparse(url or "").netloc.lower()
    return host[4:] if host.startswith("www.") else host


def story_corroboration_count(entry: dict) -> int:
    """Distinct hosts among the judge-verdict sources (`story_corroboration`,
    story_ledger.py) that may count for credibility: high/medium tier, and not
    the lead entry's own host. Never consulted by the news gate."""
    lead = _host(entry.get("source_url", ""))
    hosts = {
        _host(s.get("url", ""))
        for s in entry.get("story_corroboration") or []
        if s.get("tier") in ("high", "medium")
    }
    return len(hosts - {"", lead})


def credibility_of(entry: dict, default: float = 50.0) -> float:
    """A finding's source authority (0-100): its source registry rank, plus a
    bonus for each independent source that corroborates the same story (a finding
    3 sources report is more trustworthy). Neutral default for unknown sources.
    Judge-verdict corroboration counts only per story_corroboration_count."""
    rank = entry.get("source_rank")
    base = float(rank) if rank is not None else default
    n = len(entry.get("corroborating_sources") or []) + story_corroboration_count(entry)
    return min(100.0, base + min(n, CORROBORATION_CAP) * CORROBORATION_BONUS)


def entry_composite(entry: dict, conf: Config) -> float:
    """An entry's composite, recomputing decayed newness + credibility if missing."""
    scores = dict(entry.get("scores") or {})
    if "composite" in scores:
        return float(scores["composite"])
    scores["newness"] = newness_score(best_date(entry) or "", conf.half_life_days)
    scores.setdefault("credibility", credibility_of(entry))
    return composite_score(scores, conf.weights)


def is_scored(entry: dict) -> bool:
    """True if the entry was actually analyzed (has a novelty or relevance score).
    An unscored entry must never reach the curated view on recency (newness) alone."""
    scores = entry.get("scores") or {}
    return bool(float(scores.get("novelty", 0) or 0) or float(scores.get("relevance", 0) or 0))


def is_curated(entry: dict, conf: Config) -> bool:
    """True if the finding belongs in the public curated view (topic pages +
    newsletter). Everything else — flagged needs_review, unscored, ungrounded, OR
    below the composite floor — is held in the REVIEW.md queue (still in the pool)."""
    if entry.get("needs_review") or domain_held(entry) or readability_held(entry):
        return False
    if not is_scored(entry):
        return False
    if conf.curation.get("require_verification", True) and entry.get("verified") is False:
        return False  # the independent verifier refuted it
    if conf.curation.get("require_grounding", True):
        gs = entry.get("grounding_score")
        if gs is not None and gs < 1.0:  # verified a source and found a bad quote
            return False
    return entry_composite(entry, conf) >= conf.curation.get("min_composite", 0)


def domain_held(entry: dict) -> bool:
    """True while merge holds the entry because the analyzer's domain was not a
    taxonomy ID (taxonomy.enforce). An integrity floor: no lane publishes it."""
    return bool(entry.get("domain_hold"))


def readability_held(entry: dict) -> bool:
    """True while merge holds the entry because its brief failed the readability
    check badly (readability.py `hold`). It keeps the entry out of the findings
    lists, the news gate and new editorial promotions until it is rewritten (or
    rerank releases it under a looser config). A sticky editorial promotion
    stays shown: promotions leave only by demotion or lost integrity."""
    return bool(entry.get("readability_hold"))


def is_shown(entry: dict, conf: Config, sources_by_id: dict[str, dict]) -> bool:
    """True if the site shows this entry: a vetted finding or a news-lane story."""
    return is_curated(entry, conf) or news_shown(entry, conf, sources_by_id)


def is_editorial(entry: dict) -> bool:
    """True if the SEPARATE editorial track promoted this held finding for being
    trending/newsworthy. Independent of is_curated: the novelty gate still holds
    it (needs_review stays set), but it surfaces in the 'Trending & In the News'
    section instead of the review queue."""
    return bool((entry.get("editorial") or {}).get("promoted"))


def editorial_eligible(entry: dict, conf: Config) -> bool:
    """Whether the editorial agent is even ALLOWED to promote this held finding.

    The editorial track can bypass the novelty gate but never the integrity
    floors: an ungrounded quote or a verifier-refuted claim is not a matter of
    editorial taste. Only findings the novelty gate held (i.e. not already
    curated), that are scored, grounded, and not refuted, are in play."""
    if is_curated(entry, conf) or not is_scored(entry) or domain_held(entry):
        return False
    return not readability_held(entry) and not integrity_lost(entry)


def integrity_lost(entry: dict) -> bool:
    """The integrity floor the editorial track can never cross: the verifier
    refuted it, or a quote didn't ground. The one fact (besides an explicit,
    reasoned demotion) that takes an earlier promotion away."""
    if entry.get("verified") is False:
        return True
    gs = entry.get("grounding_score")
    return gs is not None and gs < 1.0


# --- Track-B (news lane) gate ----------------------------------------------
# The research gate above (is_curated) tests novelty + grounding — the wrong
# rubric for a "Kimi K3 open weights" release note or an incident disclosure.
# The news gate below tests trust + scope + freshness instead. It intentionally
# never runs the grounding/verification step; news items describe events, not
# claims we're ranking against a body of evidence.
# Freshness for a story to ENTER the news lane. Once in, a story stays: news
# is kept like claims, never aged out (Rohan, 2026-10-19). Dedup lookback
# lives in dedupe_stories.py.
NEWS_MAX_AGE_DAYS = 7
NEWS_HN_STANDALONE_MIN_POINTS = 100

# Deny terms split into two lists: "hard" fires unconditionally, "puff" fires
# only when NO technical term co-occurs (so "Anthropic hires former NSA
# cryptographer to lead red team" survives even though `hires former` is puff).
# All terms are matched as substrings on a lowercased title+summary+takeaway
# haystack; keep them long enough to avoid false positives (`stockpile` won't
# match `stock jumps`).
NEWS_DENY_HARD = (
    # Stock / market
    "stock jumps",
    "stock drops",
    "stock price",
    "stock soars",
    "stock rally",
    "stock plummets",
    "share price",
    "market cap",
    "price target",
    "quarterly earnings",
    "beats earnings",
    "misses earnings",
    " ipo ",
    "ipo filing",
    "valuation of $",
    "$nvda",
    "$meta",
    "$msft",
    "$googl",
    "$amzn",
    "ticker symbol",
    "analyst rating",
    "upgraded to buy",
    "downgraded to sell",
    "wall street",
    "shareholders",
    "hedge fund",
    "trading day",
    # Consumer / social feed noise
    "chatgpt tips",
    "prompts to try",
    "best ai apps",
    "chatgpt for beginners",
    "chatgpt hacks",
    "genius chatgpt",
    "ai girlfriend",
    "ai boyfriend",
    "ai for coffee",
    "ways to use chatgpt",
    "ai productivity hacks",
    # Pure hype
    "agi is here",
    "will ai replace",
    "ai is coming for",
    "ai apocalypse",
    "ai-driven revolution",
)
NEWS_DENY_PUFF = (
    "signs deal",
    "signs partnership",
    "signs cloud partnership",
    "signs strategic",
    "partnership announced",
    "strategic partnership",
    "joins the board",
    "appointed ceo",
    "hires former",
    "raised $",
    "closes series",
    "funding round",
    "seed round",
)
# Terms that RESCUE a puff hit — the co-occurrence carve-out.
NEWS_TECHNICAL_TERMS = (
    "security research",
    "sandbox",
    "sandbox escape",
    "red team",
    "red-team",
    "red-team methodology",
    "evaluation",
    "alignment",
    "guardrail",
    "prompt injection",
    "memory poisoning",
    "supply chain",
    "provenance",
    "attestation",
    "eval",
    "benchmark",
    "vulnerability",
    "exploit",
    "cve",
    "advisory",
    "harness",
    "agent framework",
    "mcp",
    "model context protocol",
    "open weights",
    "capability",
    "spec",
    "release notes",
    "regulation",
    "disclosure",
)


def _has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(n in text for n in needles)


def news_denylist_hit(entry: dict) -> bool:
    """True if the entry looks like stock/consumer/puff/hype content.

    A hard hit fires no matter what. A puff hit fires only when no technical
    term co-occurs — that's the "Anthropic + red team + hires former"
    rescue case."""
    hay = " ".join(
        [
            (entry.get("title") or ""),
            (entry.get("summary") or ""),
            (entry.get("takeaway") or ""),
        ]
    ).lower()
    if _has_any(hay, NEWS_DENY_HARD):
        return True
    if _has_any(hay, NEWS_DENY_PUFF) and not _has_any(hay, NEWS_TECHNICAL_TERMS):
        return True
    return False


def topic_scope_ok(entry: dict) -> bool:
    """True if the entry's topic classifies to one of the three tracks. The
    ingest-side classifier already assigns `topic`; if it landed there, it's
    in scope. Untopiced entries are out."""
    return entry.get("topic") in TOPICS


def _source_track_and_tier(entry: dict, sources_by_id: dict[str, dict]) -> tuple[str, str]:
    """(track, tier) for the entry's originating source, or ('research','low')
    if the source isn't in the registry (defensive default — treats orphaned
    entries as research-track low-tier, which fails the news floor)."""
    sid = entry.get("source_id") or ""
    src = sources_by_id.get(sid) or {}
    return src.get("track", "research"), src.get("tier", "low")


def is_news_curated(
    entry: dict,
    conf: Config,
    sources_by_id: dict[str, dict] | None = None,
    now: datetime | None = None,
    window: int | None = NEWS_MAX_AGE_DAYS,
) -> bool:
    """True if the entry belongs in the news lane (Trending & in the news).

    Distinct from is_curated: novelty and grounding aren't tested here; instead
    we check freshness, source track/tier, topic scope, and the deny list. A
    news source can pass this gate on the same day it publishes, without ever
    clearing the research floor."""
    if not topic_scope_ok(entry) or domain_held(entry) or readability_held(entry):
        return False
    if window is not None and not is_fresh(entry, window, now=now):
        return False
    if news_denylist_hit(entry):
        return False
    sources_by_id = sources_by_id or {}
    track, tier = _source_track_and_tier(entry, sources_by_id)
    if track not in ("news", "both"):
        return False
    if tier not in ("high", "medium"):
        return False
    # HN-standalone rule: an HN-only story needs a higher points floor to
    # stand alone as news (the keyword ingest already applies ≥40 for velocity;
    # 100 is the standalone bar).
    if entry.get("discovered_via") == "hackernews" and not entry.get("corroborating_sources"):
        points = int((entry.get("signals") or {}).get("hn_points") or 0)
        if points < NEWS_HN_STANDALONE_MIN_POINTS:
            return False
    return True


def is_news_story(entry: dict, conf: Config, sources_by_id: dict[str, dict]) -> bool:
    """True for anything the news lane keeps: an editorial promotion, or a
    news-gated story of any age. These are exempt from the freshness prune."""
    return is_editorial(entry) or is_news_curated(entry, conf, sources_by_id, window=None)


def news_shown(entry: dict, conf: Config, sources_by_id: dict[str, dict]) -> bool:
    """True if the site's news lane (and so the News tab) renders this entry: a
    kept news story whose quotes are grounded. Kept is not shown: an ungrounded
    news story stays in the pool but waits in REVIEW.md."""
    from verify_citations import publishable_grounding

    return is_news_story(entry, conf, sources_by_id) and publishable_grounding(entry)


def is_window_finding(entry: dict, conf: Config, sources_by_id: dict[str, dict]) -> bool:
    """A vetted finding of the last max_age_days that the findings lists show.
    Findings age out; news never does, so a vetted news story belongs to the
    news lane instead (one story, one lane) and never counts as a finding."""
    return (
        is_curated(entry, conf)
        and is_fresh(entry, conf.max_age_days)
        and not news_shown(entry, conf, sources_by_id)
    )


def is_held(entry: dict, conf: Config, sources_by_id: dict[str, dict]) -> bool:
    """Waiting in REVIEW.md: shown nowhere, neither as a vetted finding nor in
    the news lane."""
    return not is_curated(entry, conf) and not news_shown(entry, conf, sources_by_id)


def load_sources_by_id() -> dict[str, dict]:
    """Cache-friendly lookup for the news gate. Reloads on every call — the
    registry is small (≤ hundreds of entries) and only the render pipeline
    calls this once per run."""
    from sources_registry import load_sources

    return {s["id"]: s for s in load_sources() if "id" in s}


def review_reason(entry: dict, conf: Config, sources_by_id: dict[str, dict] | None = None) -> str:
    """Why an entry is in the review queue (for REVIEW.md)."""
    if sources_by_id is None:
        sources_by_id = load_sources_by_id()
    if is_news_story(entry, conf, sources_by_id) and not news_shown(entry, conf, sources_by_id):
        gs = entry.get("grounding_score")
        pct = f" (only {int(gs * 100)}% of quotes verified)" if gs is not None and gs < 1.0 else ""
        return f"news story: excerpt not grounded in source{pct}"
    if domain_held(entry):
        return f"domain not in the taxonomy — {entry['domain_hold']}"
    if entry.get("verified") is False:
        note = entry.get("verify_note") or "the independent verifier refuted a claim/score"
        return f"failed independent verification — {note}"
    gs = entry.get("grounding_score")
    if gs is not None and gs < 1.0:
        return f"ungrounded excerpt — only {int(gs * 100)}% of quotes verified against the source"
    if readability_held(entry):
        return entry["readability_hold"]
    if entry.get("needs_review"):
        return "flagged needs_review (low confidence / novelty / relevance)"
    if not is_scored(entry):
        return "not yet scored (no novelty/relevance — needs analysis)"
    floor = conf.curation.get("min_composite", 0)
    return f"composite {entry_composite(entry, conf)} < floor {floor}"


# --- Schema validation -----------------------------------------------------
# `topic` is the hard constraint. `domain` must be a taxonomy ID of that topic,
# but a free-text label is not a schema error: merge_analysis HOLDS the entry
# for review (taxonomy.enforce) rather than dropping the analysis.
REQUIRED_FIELDS = ("topic", "domain", "title", "source_url")

# Drift review reads `related_claims` on every analyzed entry; capping at 3
# bounds the wall-clock cost of the refuter panel per lesson.
MAX_RELATED_CLAIMS = 3


def _related_claims_errors(related: object) -> list[str]:
    if not isinstance(related, list):
        return ["related_claims must be a list of claim IDs"]
    errors: list[str] = []
    if len(related) > MAX_RELATED_CLAIMS:
        errors.append(f"related_claims exceeds cap of {MAX_RELATED_CLAIMS} (got {len(related)})")
    if any(not isinstance(x, str) for x in related):
        errors.append("related_claims entries must all be strings")
    return errors


def _proposed_domain_errors(proposal: object) -> list[str]:
    """A `proposed_domain` (no existing domain fits) needs a name and a scope."""
    if proposal is None:
        return []
    if not isinstance(proposal, dict):
        return ["proposed_domain must be an object"]
    missing = [k for k in ("name", "scope") if not str(proposal.get(k) or "").strip()]
    return [f"proposed_domain missing: {', '.join(missing)}"] if missing else []


def validate_entry(entry: dict) -> list[str]:
    """Return a list of human-readable validation errors (empty == valid)."""
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if not entry.get(field):
            errors.append(f"missing required field: {field}")
    topic = entry.get("topic")
    if topic and topic not in TOPICS:
        errors.append(f"unknown topic: {topic} (want one of {tuple(TOPICS)})")
    lessons = entry.get("lessons")
    if lessons is not None and not isinstance(lessons, list):
        errors.append("lessons must be a list")
    if "related_claims" in entry:
        errors += _related_claims_errors(entry["related_claims"])
    errors += _proposed_domain_errors(entry.get("proposed_domain"))
    return errors


# --- Pool / candidate helpers (shared by ingestors + merge) ----------------
def all_pool_entries() -> list[dict]:
    entries: list[dict] = []
    for topic in TOPICS:
        entries += load_pool(topic)["entries"]
    return entries


def known_urls() -> set[str]:
    """Normalized source/article URLs already present in either pool."""
    urls: set[str] = set()
    for entry in all_pool_entries():
        for key in ("source_url", "article_url", "tweet_url"):
            if entry.get(key):
                urls.add(normalize_url(entry[key]))
    return urls


def archive_entries(entries: list[dict]) -> int:
    """Append aged-out entries to data/archive.json, de-duped by id. Preserves
    history so the growing pool isn't lost even though the live tracker prunes."""
    if not entries:
        return 0
    existing = load_json(ARCHIVE_FILE, default=[]) or []
    seen = {e.get("id") for e in existing}
    added = [e for e in entries if e.get("id") not in seen]
    if added:
        save_json(ARCHIVE_FILE, existing + added)
    return len(added)


def unarchive(keep) -> list[dict]:
    """Take the archived entries `keep` accepts back out of data/archive.json
    and return them (news archived before it was kept like claims)."""
    existing = load_json(ARCHIVE_FILE, default=[]) or []
    back = [e for e in existing if keep(e)]
    if back:
        save_json(ARCHIVE_FILE, [e for e in existing if not keep(e)])
    return back


# merge_analysis.py's code-owned record of what it merged this run (summed over
# invocations); `scan_count.py --work` reads it. Never written by the model.
MERGE_RECORD_NAME = "_merge_outcomes.json"
MERGE_COUNTS = ("merged", "new", "updated", "skipped_invalid")


def merge_record() -> dict:
    """This run's merge counts so far (zeros when nothing merged yet)."""
    raw = load_json(DATA_DIR / MERGE_RECORD_NAME, default=None) or {}
    return {k: int(raw.get(k, 0)) for k in MERGE_COUNTS}


def load_candidates() -> list[dict]:
    return load_json(CANDIDATES_FILE, default=[]) or []


def save_candidates(candidates: list[dict]) -> None:
    save_json(CANDIDATES_FILE, candidates)


def add_candidates(new: list[dict]) -> list[dict]:
    """Merge new candidates into the staging file, de-duped by URL + title.

    De-dupes against both the existing staging queue and the published pools,
    so nothing already analyzed gets re-queued. Returns the actually-added list.
    """
    existing = load_candidates()
    max_age = load_config().max_age_days
    now = freshness_now()  # a backfill judges freshness at its window's end
    seen_urls = known_urls() | {normalize_url(c.get("source_url", "")) for c in existing}
    seen_titles = [c.get("title", "") for c in existing] + [
        e.get("title", "") for e in all_pool_entries()
    ]
    added: list[dict] = []
    for cand in new:
        nurl = normalize_url(cand.get("source_url", ""))
        if not nurl or nurl in seen_urls:
            continue
        # HARD freshness gate: never stage anything older than the window.
        # A backfill stages only what it can date inside its window.
        if not is_fresh(cand, max_age, now=now) or not in_backfill_window(cand):
            continue
        if any(title_similar(cand.get("title", ""), t) for t in seen_titles):
            continue
        existing.append(cand)
        added.append(cand)
        seen_urls.add(nurl)
        seen_titles.append(cand.get("title", ""))
    if added:
        save_candidates(existing)
    return added


def utcnow() -> datetime:
    """The one wall-clock read. Tests pin it (conftest) so fixtures never age out."""
    return datetime.now(UTC)


def utcnow_iso() -> str:
    return utcnow().replace(microsecond=0).isoformat()


# --- Backfill window ---------------------------------------------------------
# A backfill scan (scripts/backfill.sh, issue #52) is a normal scan whose ingest
# pulls items published inside [FROM, TO] instead of "recent". run_scan.sh's
# wrapper sets both variables; the model session inherits them and can't change
# them. Unset = a normal scan, and every helper below behaves as before.
BACKFILL_FROM_ENV = "SCAN_BACKFILL_FROM"
BACKFILL_TO_ENV = "SCAN_BACKFILL_TO"
BACKFILL_MAX_SPAN_DAYS = 31  # one chunk; config.yaml backfill.max_chunk_days is tighter
_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class BackfillWindowError(ValueError):
    """A malformed backfill window: fail closed, never fall back to "recent"."""


def parse_backfill_window(frm: str, to: str, today: date) -> tuple[date, date]:
    """(FROM, TO) as dates, or BackfillWindowError: both full YYYY-MM-DD days,
    FROM <= TO <= today, at most BACKFILL_MAX_SPAN_DAYS days inclusive."""
    if not (_DAY_RE.match(frm or "") and _DAY_RE.match(to or "")):
        raise BackfillWindowError(f"backfill window needs two YYYY-MM-DD days, got {frm!r}..{to!r}")
    try:
        start, end = date.fromisoformat(frm), date.fromisoformat(to)
    except ValueError as exc:
        raise BackfillWindowError(f"backfill window {frm}..{to}: {exc}") from exc
    if start > end:
        raise BackfillWindowError(f"backfill window {frm}..{to} ends before it starts")
    if end > today:
        raise BackfillWindowError(f"backfill window {frm}..{to} ends in the future")
    if (end - start).days + 1 > BACKFILL_MAX_SPAN_DAYS:
        raise BackfillWindowError(
            f"backfill window {frm}..{to} spans over {BACKFILL_MAX_SPAN_DAYS} days"
        )
    return start, end


def backfill_window() -> tuple[date, date] | None:
    """The run's backfill window from the environment, None for a normal scan.
    One variable without the other is an error, not a normal scan."""
    frm, to = os.environ.get(BACKFILL_FROM_ENV, ""), os.environ.get(BACKFILL_TO_ENV, "")
    if not frm and not to:
        return None
    return parse_backfill_window(frm, to, utcnow().date())


def freshness_now() -> datetime:
    """The "now" freshness and newness are judged at: the end of a backfill's
    window (so its items are not stale on arrival), else the wall clock."""
    window = backfill_window()
    if window is None:
        return utcnow()
    return datetime.combine(window[1], time(23, 59, 59), UTC)


def ingest_window(max_age_days: int) -> tuple[datetime, datetime | None]:
    """(since, until) for an ingestor: a backfill's [FROM 00:00, TO 23:59:59],
    else the last max_age_days with no upper bound (as before)."""
    window = backfill_window()
    if window is None:
        return utcnow() - timedelta(days=max_age_days), None
    return datetime.combine(window[0], time(0), UTC), freshness_now()


def in_ingest_window(dt: datetime | None, since: datetime, until: datetime | None) -> bool:
    """True when `dt` lies in [since, until]; an undated item never does."""
    return dt is not None and dt >= since and (until is None or dt <= until)


def window_days(lookback: int) -> list[str]:
    """The days a per-day API (HF Daily Papers) is asked for, newest first:
    every day of a backfill's window, else the last `lookback` days."""
    window = backfill_window()
    if window is None:
        today = utcnow().date()
        return [(today - timedelta(days=b)).isoformat() for b in range(lookback)]
    start, end = window
    return [(end - timedelta(days=b)).isoformat() for b in range((end - start).days + 1)]


def in_backfill_window(entry: dict) -> bool:
    """For a backfill, True only when the entry's own day is inside the window
    (a month-only or missing date can't be placed, so it is out). Always True
    for a normal scan."""
    window = backfill_window()
    if window is None:
        return True
    day = str(best_date(entry) or "")
    return bool(_DAY_RE.match(day)) and window[0].isoformat() <= day <= window[1].isoformat()


def write_raw(cand_id: str, text: str) -> str:
    """Persist fetched article text to data/_raw/<id>.txt; return its path str."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{cand_id}.txt"
    path.write_text(text, encoding="utf-8")
    return str(path.relative_to(ROOT))


# Set (to "1") only in the environment of the Mac scan's model session. Under
# it, the only URLs any script may fetch are the staged candidates' own, as
# `run_scan.sh pre` recorded them: model-written entry fields can't make the
# runner request an attacker's URL.
SCAN_LOCK_ENV = "SCAN_LOCKED"
SCAN_URL_SNAPSHOT = "_scan_urls.json"


def scan_locked() -> bool:
    return os.environ.get(SCAN_LOCK_ENV) == "1"


def check_scan_lock(url: str) -> None:
    if not scan_locked():
        return
    allowed = set((load_json(DATA_DIR / SCAN_URL_SNAPSHOT, default={}) or {}).values())
    if url not in allowed:
        raise PermissionError(f"scan lock: {url} is not a staged candidate URL")


_MAIN_IDS: set[str] | None = None


def main_entry_ids() -> set[str]:
    """Ids of every pool entry on origin/main (cached). Entries absent from main
    are this run's own; the scan lock judges only those."""
    global _MAIN_IDS
    if _MAIN_IDS is None:
        import subprocess

        ids: set[str] = set()
        for path in POOL_FILES.values():
            rel = path.relative_to(ROOT).as_posix()
            out = subprocess.run(
                ["git", "show", f"origin/main:{rel}"], cwd=ROOT, capture_output=True, text=True
            )
            if out.returncode == 0:
                ids |= {e.get("id") for e in json.loads(out.stdout).get("entries", [])}
        _MAIN_IDS = ids
    return _MAIN_IDS


def raw_file(raw_path: str | None) -> Path | None:
    """The cached source file for a raw_path, only if it lives under data/_raw/.

    raw_path is model-writable, and `ROOT / "/abs/path"` would escape ROOT.
    """
    if not raw_path:
        return None
    path = (ROOT / raw_path).resolve()
    return path if path.is_relative_to(RAW_DIR.resolve()) else None


def fetch_readable(url: str, timeout: int = 30, max_chars: int = 20000) -> str:
    """Fetch clean reader text for a URL via Jina Reader. Raises on failure."""
    import requests  # local import keeps offline unit tests import-clean

    check_scan_lock(url)

    resp = requests.get(
        JINA_READER + url,
        timeout=timeout,
        headers={"Accept": "text/plain", "User-Agent": HTTP_USER_AGENT},
    )
    resp.raise_for_status()
    text = resp.text.strip()
    if not text:
        raise RuntimeError(f"empty reader response for {url}")
    return text[:max_chars]
