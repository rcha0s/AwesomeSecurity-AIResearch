#!/usr/bin/env python3
"""
newsworthy.py — Which staged candidates are the week's big stories? Pure, no I/O.

2026-10-23: PHP2Shell (two unauthenticated PHP RCEs, exploited before the
patch) was staged from six registered feeds (Snyk, Talos, The Register, Wired,
Simon Willison, Semgrep) and none of them reached the 14-slot batch. Their
batch ranks were 50 to 186, because selection knew only newness and source
rank. This module gives select_batch.py three signals it can read before any
analysis:

    severity      markers in the title/excerpt: rce, unauthenticated, critical,
                  exploited (in the wild, zero-day), compromise (supply chain,
                  backdoor, credential stealer)
    ai-incident   an AI subject (agent, assistant, MCP, coding agent, LLM, ...)
                  next to an incident word (hijack, exfiltrate, RCE, abuse, ...)
    corroboration how many OTHER sources staged the same story this run

Same-story matching is stricter than story_ledger's shortlist, which is tuned
to over-match because a judge reads it. Here a false match can put a story in
a lane, so it has to be precise. Two candidates are the same story when they
share a CVE or GHSA id, or, published within MATCH_DAYS of each other, when
they share name tokens: two of them (one in a title), or one in BOTH titles
when published within TITLE_MATCH_DAYS. Two candidates that each carry ids,
none shared, are different bugs and never match; when only one carries an id,
they must be published within TITLE_MATCH_DAYS (a 2026-10-14 KEV entry for
one PAN-OS CVE is not the 10-20 news about another PAN-OS bug).

A name token is a distinctive proper noun (PHP, LiteLLM, ARTEX, eMudhra): rare
in the reference corpus (the pools + archive, so this run's own burst of
coverage can't make a name look common) and written capitalized in at least
NAME_CASED of its body-text occurrences, so "heap" or "accounts" never counts.

Matching is pairwise, never transitive: a chain of loose matches can't grow
one story out of unrelated ones.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from urllib.parse import urlparse

import dedupe_stories as ds

# Publishers that don't count as independent corroboration: anyone can push a
# repo or an advisory to GitHub, and an HN post is a vote on someone else's link.
# 2026-10-23 review: two attacker repos found by two github_query searches faked
# "2 sources + RCE" and took a lane slot.
GITHUB, HN = "github", "hn"
NON_INDEPENDENT = frozenset({GITHUB, HN})
# Second-level labels under which a registrable domain takes three labels.
_SECOND_LEVEL = frozenset({"co", "com", "org", "net", "gov", "ac", "edu"})
MATCH_DAYS = 7
TITLE_MATCH_DAYS = 2
NAME_MAX_DF = 0.01  # a name appears in at most 1% of reference documents
NAME_MIN_DF_CAP = 5  # ...or in at most this many, for a small corpus
NAME_CASED = 0.75  # share of body occurrences written with a capital
BODY_CHARS = 300  # the excerpt prefix matched (same scale as a feed summary)
# Capitalized by convention, not by being a name: months, days, and the
# acronyms of the trade, which every story shares.
NOT_NAMES = frozenset(
    "january february march april may june july august september october november "
    "december monday tuesday wednesday thursday friday saturday sunday "
    "rce rces cve cves cvss poc api apis sdk sql xss csrf ssrf dos ddos llm llms ai mcp "
    "rat kev cisa ghsa url http https dns tls ssl ssh vpn mfa sso ceo cto".split()
)
ID_RE = re.compile(r"\b(cve-\d{4}-\d{4,}|ghsa-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})\b", re.I)
_WORD = re.compile(r"[A-Za-z0-9]+")
_CODENAME = re.compile(r"\b([A-Za-z]{2,})-\d+")  # Storm-0940, WT-2026
_SENTENCE = re.compile(r"(?<=[.!?:;])\s+|\n+")

SEVERITY = {
    "rce": r"\brces?\b|remote code execution|code execution|command execution",
    "unauthenticated": r"\bunauthenticated\b|\bunauth\b|pre-?auth|without authentication",
    "critical": r"\bcritical\b|max(?:imum)?[- ]severity|cvss(?:v[34](?:\.\d)?)?[: ]+(?:9\.\d|10)",
    "exploited": r"actively exploited|exploited in (?:the )?wild|in-the-wild|zero[- ]day"
    r"|\b0[- ]?day\b|exploitation (?:began|attempts|activity)|under (?:active )?attack"
    r"|broadly exploited|being exploited",
    "compromise": r"supply[- ]chain (?:attack|compromise)|\bcompromised\b|backdoor"
    r"|credential[- ]stealer|infostealer|malicious (?:version|package|release|wheels?)",
}
AI_SUBJECT = (
    r"\bgpt-?\d|\bopenai\b|\banthropic\b|\bclaude\b|\bgemini\b|\bdeepseek\b"
    r"|\bai agents?\b|\bagentic\b|\bcoding agents?\b|\bai assistants?\b|\bai bots?\b"
    r"|\bchatbots?\b|\bllms?\b|\bmcp\b|model context protocol|\bcopilot\b|claude code"
    r"|\bchatgpt\b|\bai[- ](?:driven|powered)\b|\bai gateway\b|\bai tools?\b"
)
AI_INCIDENT = (
    r"hijack|exfiltrat|\bleak|\bsteal|\bstole|credential|\brces?\b|code execution"
    r"|prompt injection|\babus|weaponi|\bbreach|\bcompromis|malicious|\bexploit"
    r"|\battack|backdoor|bypass|\bhack|rogue|sabotag|unsanctioned|deceiv"
    r"|safety monitoring"
)
# An incident in the headline, short of a severity marker ("Tor exit relays
# hijacked", "Qilin exploits Palo Alto flaw"): enough to keep a router
# catch-all admit out of prefilter's hold (prefilter.catch_all_without_marker).
INCIDENT = (
    r"\bexploit|hijack|\bhack(?:ed|s)?\b|ransomware|emergency patch|\battack(?:s|ed)?\b"
    r"|\bbreach|malware|backdoor|stealer|\bcompromis"
)
_INCIDENT_RE = re.compile(INCIDENT, re.I)
_SEVERITY_RE = {k: re.compile(v, re.I) for k, v in SEVERITY.items()}
_AI_SUBJECT_RE = re.compile(AI_SUBJECT, re.I)
_AI_INCIDENT_RE = re.compile(AI_INCIDENT, re.I)


def _body(cand: dict) -> str:
    return (cand.get("excerpt") or cand.get("summary") or "")[:BODY_CHARS]


def _text(cand: dict) -> str:
    return f"{cand.get('title') or ''} {_body(cand)}"


def markers(cand: dict) -> frozenset[str]:
    """Severity markers plus `ai-incident`, read from the title + excerpt."""
    text = _text(cand)
    found = {name for name, rx in _SEVERITY_RE.items() if rx.search(text)}
    if _AI_SUBJECT_RE.search(text) and _AI_INCIDENT_RE.search(text):
        found.add("ai-incident")
    return frozenset(found)


def is_incident(cand: dict) -> bool:
    """Any marker (title + excerpt), or an incident word in the TITLE: vendor
    posts mention "exploit" in passing, an incident leads with it."""
    return bool(markers(cand)) or bool(_INCIDENT_RE.search(cand.get("title") or ""))


def _tokens(text: str) -> set[str]:
    return {t for t in ds._tokens(text) if len(t) > 2 and not t.isdigit()}


def _shape_is_name(word: str) -> bool:
    """With no body text to judge by: digits mixed in, an inner capital, or caps."""
    inner = any(ch.isupper() for ch in word[1:])
    mixed = any(ch.isdigit() for ch in word) and any(ch.isalpha() for ch in word)
    return inner or mixed or (word.isupper() and len(word) >= 2)


def mid_sentence_words(text: str) -> list[str]:
    """Words that don't open a sentence: an opening word is capitalized by
    grammar ("Hackers exploited..."), which says nothing about it being a name."""
    return [w for part in _SENTENCE.split(text) for w in _WORD.findall(part)[1:]]


@dataclass(frozen=True)
class NameModel:
    """Which tokens are names: document frequency over the reference corpus,
    capitalization over every body text seen."""

    df: Counter
    n_docs: int
    cased: Counter
    seen: Counter
    shaped: frozenset[str]

    def is_name(self, token: str) -> bool:
        if token in NOT_NAMES:
            return False
        if self.df[token] > max(NAME_MIN_DF_CAP, NAME_MAX_DF * self.n_docs):
            return False
        if self.seen[token]:
            return self.cased[token] / self.seen[token] >= NAME_CASED
        return token in self.shaped


def name_model(reference: list[dict], staged: list[dict]) -> NameModel:
    """`reference` = documents written before this run (pools + archive)."""
    df = Counter(t for doc in reference for t in _tokens(_text(doc)))
    cased, seen, shaped = Counter(), Counter(), set()
    for doc in [*reference, *staged]:
        for word in mid_sentence_words(_body(doc)):
            seen[word.lower()] += 1
            cased[word.lower()] += word[0].isupper()
        title = doc.get("title") or ""
        shaped |= {w.lower() for w in _WORD.findall(title) if _shape_is_name(w)}
        shaped |= {w.lower() for w in _CODENAME.findall(f"{title} {_body(doc)}")}
    return NameModel(df, len(reference), cased, seen, frozenset(shaped))


@dataclass(frozen=True)
class Profile:
    title: frozenset[str]
    names: frozenset[str]
    ids: frozenset[str]
    day: date | None


def profile(cand: dict, model: NameModel) -> Profile:
    text = _text(cand)
    found_ids = {m.lower() for m in ID_RE.findall(f"{text} {cand.get('excerpt') or ''}")}
    return Profile(
        title=frozenset(_tokens(cand.get("title") or "")),
        names=frozenset(t for t in _tokens(text) if model.is_name(t)),
        ids=frozenset(found_ids),
        day=_day(cand),
    )


def _day(cand: dict) -> date | None:
    try:
        return date.fromisoformat(str(cand.get("published") or "")[:10])
    except ValueError:
        return None


def _gap(a: Profile, b: Profile) -> float:
    return abs((a.day - b.day).days) if a.day and b.day else math.inf


def same_story(a: Profile, b: Profile, title_days: int = TITLE_MATCH_DAYS) -> bool:
    """The pairwise rule in the module docstring. `title_days` widens the
    same-days windows (one shared title name; one side naming a CVE) for a
    caller whose matches a judge reads anyway: story_ledger's shortlist passes
    MATCH_DAYS, since a follow-up three days on is still the story."""
    if a.ids & b.ids:
        return True
    if (a.ids and b.ids) or _gap(a, b) > MATCH_DAYS:
        return False
    if bool(a.ids) != bool(b.ids) and _gap(a, b) > title_days:
        return False  # one names its CVE, the other doesn't: only same-days coverage
    shared = a.names & b.names
    if len(shared) >= 2 and shared & (a.title | b.title):
        return True
    return bool(shared & a.title & b.title) and _gap(a, b) <= title_days


def registrable_domain(url: str) -> str:
    """example.co.uk / nvidia.com from a URL: same-publisher hosts are one."""
    host = (urlparse(url or "").hostname or "").lower()
    labels = [p for p in host.split(".") if p]
    if len(labels) >= 3 and labels[-2] in _SECOND_LEVEL and len(labels[-1]) == 2:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def publisher(cand: dict) -> str:
    """Who published a candidate, for corroboration: never the feed id. Every
    GitHub ingestor and github.com URL is one publisher (GITHUB), every HN item
    another (HN); anything else is the registrable domain of its URL, so
    developer.nvidia.com's two feeds count once."""
    sid = str(cand.get("source_id") or "")
    if cand.get("discovered_via") == "hackernews" or sid.startswith("hackernews"):
        return HN
    url = cand.get("source_url") or cand.get("article_url") or ""
    domain = registrable_domain(url)
    github_ingest = sid.split(":", 1)[0] in ("github_query", "github_user")
    if github_ingest or cand.get("source_type") == "GHSA" or domain == "github.com":
        return GITHUB
    return domain or sid or str(cand.get("discovered_via") or "")


@dataclass(frozen=True)
class Signal:
    """One candidate's view: its markers, which other candidates (by position
    in the analyzed list) from OTHER publishers tell the same story, and whether
    the story ledger already holds it."""

    markers: frozenset[str]
    matches: tuple[int, ...]
    sources: int  # distinct publishers covering the story, this one included
    known: bool = False
    ids: frozenset[str] = frozenset()  # CVE / GHSA ids this copy names
    best_rank: float = 0.0  # highest source rank among the independent copies


def analyze(
    cands: list[dict], reference: list[dict], publisher_of=publisher, known: list[dict] = ()
) -> list[Signal]:
    """Signals aligned with `cands`. `publisher_of(cand)` names who published a
    copy: two copies from one publisher corroborate nothing. `known` are covering
    sources already in the story ledger ({title, published}); a candidate that
    matches one is a story we hold, so it is never lane-worthy."""
    model = name_model(reference, cands)
    profs = [profile(x, model) for x in cands]
    held = [profile(x, model) for x in known]
    keys = [publisher_of(x) for x in cands]
    out: list[Signal] = []
    for i, prof in enumerate(profs):
        hits = tuple(
            j
            for j, other in enumerate(profs)
            if j != i and keys[j] != keys[i] and same_story(prof, other)
        )
        copies = (i, *hits)
        out.append(
            Signal(
                markers=markers(cands[i]),
                matches=hits,
                sources=len({keys[j] for j in copies}),
                known=any(same_story(prof, h) for h in held),
                ids=prof.ids,
                best_rank=max(
                    [_rank(cands[j]) for j in copies if keys[j] not in NON_INDEPENDENT],
                    default=0.0,
                ),
            )
        )
    return out


def _rank(cand: dict) -> float:
    return float(cand.get("source_rank") or 0.0)


def is_big(sig: Signal, min_sources: int, any_sources: int, min_rank: float = 0.0) -> bool:
    """Lane-worthy: not already held; reported by `min_sources` publishers with
    a severity or AI-incident marker, or by `any_sources` without one; and at
    least one copy from a publisher outside GitHub/HN whose source ranks
    `min_rank` or more, so GitHub repos, HN votes or two low-rank feeds can't
    qualify on markers alone. One publisher never qualifies: its markers only
    earn the score bonus."""
    if sig.known or sig.sources < 2 or sig.best_rank < max(min_rank, 1e-9):
        return False
    return (sig.sources >= min_sources and bool(sig.markers)) or sig.sources >= any_sources


def bonus(sig: Signal, marker_points: float, source_points: float, max_sources: int) -> float:
    """Score points for the deal: any marker, plus each corroborating source.
    Nothing for a story the ledger already holds: it needs no help."""
    if sig.known:
        return 0.0
    extra = min(max(0, sig.sources - 1), max_sources)
    return (marker_points if sig.markers else 0.0) + source_points * extra
