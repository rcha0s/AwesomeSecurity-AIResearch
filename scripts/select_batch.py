#!/usr/bin/env python3
"""
select_batch.py — Hand the scan's model session a batch sized to the run.

`run_scan.sh pre` runs this right after ingest. The session's budget is sized
for `limits.max_stories_per_run` analyzed stories, so the session must not see
the whole ingest (286 candidates on 2026-10-20: it judged the set too big for
its budget and analyzed nothing). This keeps
`max_stories_per_run + batch_margin` candidates in data/candidates.json, the
file the session reads. The margin covers batch members the story judge finds
to be `same`/`update` (they are not analyzed and don't count toward the cap).

Scoring reuses the existing signals, no new scorer: the composite formula over
the two axes known before analysis, newness (decayed from the source date) and
credibility (source registry rank), with config.yaml's weights, plus a small
`batch_routed_bonus` when prefilter.py routed the candidate to a domain.
Routing measures taxonomy confidence, not newsworthiness, so it only nudges.
prefilter.py's deny-list, excluded-term and pool/archive-duplicate hits never
enter the batch.

Fairness: one source class would otherwise take every slot (on 2026-10-20 a
pure score order gave six GHSA advisories and no KEV, HN or Simon Willison).
Slots are dealt round-robin across ingestor classes (KEV, HN, GHSA, GitHub
search, HF papers, conference papers, research sitemaps, RSS feeds), best
class first, each class giving its best remaining candidate, and no single
source takes more than `batch_per_source` slots unless nothing else is left.
Curator links (ingest_curator_links.py, `curator:` source ids) are their own
class, and `batch_class_min` reserves each named class a floor of slots right
after the must-not-miss lane: a curator link carries the issue's date, so its
newness can sink it under fresher feeds, and the per-source cap (all curator
links share one source) holds it to `batch_per_source`. With a floor of 1 and
a cap of 2, each batch gets one or two.

`batch_class_slots` lets a class deal more than one candidate per round: plain
RSS feeds are one class of 60+ feeds and a third of the staged set, and the
research posts the recall eval misses most come from them.

Must-not-miss lane: the recall eval scores every new CISA KEV entry, and on
2026-W43 held 0 of 19 KEV and critical GHSA items. Before the deal, up to
`batch_priority_max` slots go to new KEV entries and to the GHSA advisories
`ghsa_keep_reason` keeps, AI-tooling advisories first, at most
`batch_priority_per_source` from one source. Each carries `batch_priority`
so the session analyzes it before the cap runs out.

GitHub advisories (Rohan, 2026-10-28): they are not stories until they blow up
on the internet, so a GHSA candidate is dropped before it can take a deal slot,
a lane slot or a news slot unless `ghsa_keep_reason` keeps it: it is AI-related
(the prefilter routed it to an `ais.*` domain, or a package is in config
`ghsa.ai_packages`), or it is CRITICAL in a package in `ghsa.well_known_packages`.
The head of a big-story group (2+ independent publishers) still gets in through
the story lane. Dropped advisories go to the backlog with reason `ghsa:not-kept`.

Big-story lane (newsworthy.py): on 2026-10-23 PHP2Shell was staged from six
registered feeds and every copy ranked 50th or worse, because newness and
source rank can't tell the week's biggest story from a routine post. First of
all, up to `batch_story_max` slots go to stories that `batch_story_min_sources`
independent sources staged this run with a severity or AI-incident marker (or
`batch_story_any_sources` without one), published in the last
`batch_story_days`, and not already in the story ledger. Each story gets ONE
slot: its most credible copy, at most `batch_per_source` from a source,
carrying `batch_story` (its sources, markers and the other copies' URLs). The
other copies wait in the backlog marked `batch_same_story_as`, since the judge
would only call them `same`. Outside the lane, markers and corroboration add
`batch_marker_bonus` + `batch_corroboration_bonus` per extra source (up to
three) to the score the deal ranks by; per-source caps and the class
round-robin are unchanged.

News tier (2026-10-23, Rohan: "the actual relevant news stories that should
have been caught instead of just getting the 10"). The batch above is the
DEEP tier: full analysis, at most `max_stories_per_run`. Every candidate left
over that is relevant news joins the session's set as the NEWS tier, tagged
`batch_tier: "news"`, and gets a short grounded news brief instead of deep
analysis (research-scan step 3c). A leftover candidate is news when it was
published in the last `batch_story_days`, is not on the news deny list, and is

    story     the head of a big-story group (newsworthy.py, judged as the lane
              judges it) that the lane had no slot for
    priority  a new CISA KEV entry, or a GHSA advisory that is AI-related or
              critical in a well-known package, which the must-not-miss lane
              had no slot for
    marker    a severity or AI-incident marker from a publisher outside
              GitHub/HN whose source ranks `batch_news_min_rank` or more (40:
              The Register, Dark Reading; the lane keeps its own 55), and not
              a story the ledger already holds

in that order, at most `max_news_per_run` (a runaway guard, not a quota) and
at most `batch_news_per_source` from one source. A story group's other copies
stay in the backlog (`batch_same_story_as`); the brief's `batch_news.coverage`
lists them, and merge_analysis.py attaches them as its covering sources.
main() also writes data/_scan_tiers.json, the code-owned record of which
candidate is in which tier: merge_analysis.py accepts a news brief only for a
news-tier candidate named there, and the session can't edit data/_scan*.

Everything not selected goes to data/_scan_backlog.json, each with its
prefilter reason and rank. On the Mac runner the session can neither edit nor
read it (scan_containment.sh denies both); the cloud routine has no per-tool
scoping, so there it is only a convention. It is a record for diagnosis, not a
queue: the next scan's ingest re-stages any candidate still fresh and still in
its feed, and it competes for that day's batch again.

Usage:
    python scripts/select_batch.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import common as c
import newsworthy as nw
import prefilter as pf
import story_ledger as sl

BACKLOG_NAME = "_scan_backlog.json"
DEFAULTS = {
    "batch_margin": 4,
    "batch_per_source": 2,
    "batch_routed_bonus": 5.0,
    "batch_priority_max": 0,  # off unless config.yaml names a lane size
    "batch_priority_per_source": 2,
    "batch_story_max": 0,  # off unless config.yaml names a lane size
    "batch_story_min_sources": 2,
    "batch_story_any_sources": 4,
    "batch_story_days": 7,
    "batch_story_min_rank": 0.0,
    "batch_marker_bonus": 0.0,
    "batch_corroboration_bonus": 0.0,
    "max_news_per_run": 0,  # news tier off unless config.yaml sizes it
    "batch_news_per_source": 4,
    "batch_news_min_rank": None,  # None = batch_story_min_rank
    "batch_lab_max": 0,  # off unless config.yaml names a lane size (and hosts + terms)
    "batch_lab_per_source": 2,
    "batch_eff_max": 0,  # off unless config.yaml names a lane size (and terms)
    "batch_eff_per_source": 1,
}
NEWS = "news"  # batch_tier of a news-tier candidate
CORROBORATION_MAX = 3  # extra sources that earn the corroboration bonus
# source_id prefixes that name their own ingestor; plain `rss:` feeds share one class.
OWN_CLASS = ("kev_json", "hf_papers", "research_index", "github_query", "sitemap", "curator", "reddit")


def backlog_file() -> Path:
    return c.DATA_DIR / BACKLOG_NAME


def setting(conf: c.Config, key: str) -> float:
    return conf.limits.get(key, DEFAULTS[key])


def batch_size(conf: c.Config) -> int:
    """Stories the run may analyze, plus the margin for same/update verdicts."""
    cap = int(conf.limits.get("max_stories_per_run", 8))
    return max(0, cap) + max(0, int(setting(conf, "batch_margin")))


def source_key(cand: dict) -> str:
    """The source a candidate came from (registry id, else ingestor + type)."""
    return cand.get("source_id") or f"{cand.get('discovered_via')}:{cand.get('source_type')}"


def ingestor_class(cand: dict) -> str:
    sid = cand.get("source_id") or ""
    prefix = sid.split(":", 1)[0]
    if prefix in OWN_CLASS:
        return prefix
    return str(cand.get("discovered_via")) if sid else source_key(cand)


def score(cand: dict, conf: c.Config) -> float:
    """Composite over the axes known before analysis, plus the routing nudge."""
    axes = {
        # A backfill ranks its batch by newness as of its window's end.
        "newness": c.newness_score(
            c.best_date(cand) or "", conf.half_life_days, now=c.freshness_now()
        ),
        "credibility": c.credibility_of(cand),
    }
    routed = (cand.get("prefilter") or {}).get("reason") == "routed"
    return c.composite_score(axes, conf.weights) + (
        float(setting(conf, "batch_routed_bonus")) if routed else 0.0
    )


def deal(
    ranked: list[dict],
    size: int,
    per_source: int,
    slots: dict[str, int] | None = None,
    used: Counter | None = None,
    fill: bool = True,
) -> list[dict]:
    """Round-robin over ingestor classes (best head first), `slots[class]`
    picks per round (default 1), per-source capped; then (`fill`) fill any
    slots left by score alone. `ranked` is best-first; `used` counts slots
    already taken."""
    queues: dict[str, list[dict]] = {}
    for cand in ranked:
        queues.setdefault(ingestor_class(cand), []).append(cand)
    pos = {id(x): i for i, x in enumerate(ranked)}
    taken: list[dict] = []
    used = Counter(used or {})
    while len(taken) < size:
        dealt = False
        for cls in sorted(queues, key=lambda k: pos[id(queues[k][0])] if queues[k] else len(pos)):
            for _ in range(max(1, int((slots or {}).get(cls, 1)))):
                pick = next((x for x in queues[cls] if used[source_key(x)] < per_source), None)
                if pick is None or len(taken) >= size:
                    break
                queues[cls].remove(pick)
                used[source_key(pick)] += 1
                taken.append(pick)
                dealt = True
        if not dealt:
            break
    if not fill:
        return taken
    ids = {id(x) for x in taken}
    return taken + [x for x in ranked if id(x) not in ids][: size - len(taken)]


def priority_class(cand: dict, conf: c.Config) -> str | None:
    """The must-not-miss class a candidate belongs to, else None. A GHSA advisory
    is in it only when ghsa_keep_reason keeps it: `ghsa-ai` (AI-related) or
    `ghsa-critical` (critical in a well-known package)."""
    if (cand.get("source_id") or "").startswith("kev_json:"):
        return "kev"
    if cand.get("source_type") != "GHSA":
        return None
    reason = ghsa_keep_reason(cand, conf)
    return {"ai-domain": "ghsa-ai", "ai-package": "ghsa-ai", "critical": "ghsa-critical"}.get(
        reason or ""
    )


def is_ai_tooling(cand: dict) -> bool:
    """Prefilter routed it to an AI-security domain on the taxonomy's own hints.
    Not the ingest-time topic guess: that is a keyword match on package names."""
    return str((cand.get("prefilter") or {}).get("domain_hint") or "").startswith("ais.")


def package_names(cand: dict) -> set[str]:
    """Lower-cased `name` and `ecosystem/name` of each affected package (the
    GHSA ingestor's `packages` rows)."""
    out: set[str] = set()
    for row in cand.get("packages") or []:
        name = str((row or {}).get("name") or "").strip().lower()
        if name:
            out |= {name, f"{str((row or {}).get('ecosystem') or '').strip().lower()}/{name}"}
    return out


def ghsa_keep_reason(cand: dict, conf: c.Config) -> str | None:
    """Why a GitHub advisory stays in play, else None (drop it). Pure.

    Rohan, 2026-10-28: advisories are not stories until they blow up on the
    internet, but AI bugs from them stay, and so do CRITICAL ones in well-known
    libraries (litellm). Kept when:
      ai-domain   the prefilter routed it to an ais.* domain
      ai-package  an affected package is in config `ghsa.ai_packages`
      critical    severity CRITICAL and an affected package is in
                  `ghsa.well_known_packages`
    The third way in, a big-story group of 2+ independent publishers, is the
    story lane's call (newsworthy.py), not decided here. A candidate that is not
    a GHSA advisory has no reason (the rule is about GHSA only)."""
    if cand.get("source_type") != "GHSA":
        return None
    if is_ai_tooling(cand):
        return "ai-domain"
    names = package_names(cand)
    listed = lambda key: {str(x).strip().lower() for x in (conf.ghsa.get(key) or [])}  # noqa: E731
    if names & listed("ai_packages"):
        return "ai-package"
    if str(cand.get("severity") or "").upper() == "CRITICAL" and names & listed(
        "well_known_packages"
    ):
        return "critical"
    return None


def ghsa_drop_note(cand: dict) -> dict:
    """The backlog copy of an advisory the keep rule refused."""
    return {**cand, "prefilter": {**(cand.get("prefilter") or {}), "reason": "ghsa:not-kept"}}


def ghsa_dropped(cand: dict, conf: c.Config, groups: dict[int, tuple]) -> bool:
    """A GHSA advisory the keep rule refuses and no big story vouches for. The
    head of a lane-worthy story group (2+ independent publishers) is not dropped."""
    if cand.get("source_type") != "GHSA" or ghsa_keep_reason(cand, conf):
        return False
    group = groups.get(id(cand))
    return not (group and group[1])


def lab_source(cand: dict, conf: c.Config) -> bool:
    """Published by a major AI lab: the article URL's host (no www., no trailing
    dot) is one of `batch_lab_hosts` or a subdomain of it, and its path is the
    entry's path or under it. "openai.com" covers alignment.openai.com but not
    notopenai.com; "microsoft.com/en-us/research" covers /en-us/research/blog/x
    but not /en-us/researchx. A URL that won't parse is not a lab post."""
    try:
        url = urlparse(cand.get("article_url") or cand.get("source_url") or "")
        host = (url.hostname or "").lower().rstrip(".").removeprefix("www.")
    except ValueError:
        return False
    path = url.path.lower().strip("/")
    for entry in conf.limits.get("batch_lab_hosts") or []:
        want_host, _, want_path = str(entry).lower().strip("/").partition("/")
        if host != want_host and not host.endswith("." + want_host):
            continue
        if not want_path or path == want_path or path.startswith(want_path + "/"):
            return True
    return False


def lab_terms_hit(text: str, conf: c.Config, key: str = "batch_lab_terms") -> bool:
    """One of the `key` terms (`batch_lab_terms`, or `batch_eff_terms`) as a whole
    word or phrase (a plural s allowed): "security" but not "securities",
    "evals" but not "retrievals"."""
    for term in conf.limits.get(key) or []:
        if re.search(rf"\b{re.escape(str(term).lower())}s?\b", text):
            return True
    return False


def lab_relevant(cand: dict, conf: c.Config) -> bool:
    """A lab post on-thesis for this tracker: a `batch_lab_terms` word in its
    title or excerpt. Labs also post customer stories and launches ("Uber brings
    ChatGPT Work to all employees"), which this skips."""
    if not lab_source(cand, conf):
        return False
    return lab_terms_hit(f"{cand.get('title') or ''} {cand.get('excerpt') or ''}".lower(), conf)


def lab_on(conf: c.Config) -> bool:
    return int(setting(conf, "batch_lab_max")) > 0


def lab_rescue(dropped: list[dict], conf: c.Config) -> list[dict]:
    """Relevant lab posts the prefilter dropped only for a catch-all class with
    no marker (Cloudflare + OpenAI on vulnerability discovery, 2026-10-21).
    Excluded-term and duplicate drops stand. The prefilter checks catch-alls
    before duplicates, so a rescued post is re-checked against the pools here."""
    if not lab_on(conf):
        return []
    picks = [
        x for x in dropped
        if str((x.get("prefilter") or {}).get("reason") or "").startswith("catch-all")
        and lab_relevant(x, conf)
    ]  # fmt: skip
    if not picks:
        return []
    urls = c.known_urls()
    titles = [e.get("title", "") for e in c.all_pool_entries()]
    return [x for x in picks if not pf.duplicate_of_pool(x, urls, titles)]


def lab_lane(
    ranked: list[dict], conf: c.Config, limit: int, used: Counter, known: set[int]
) -> list[dict]:
    """Up to `limit` recent posts from the major AI labs (rank order: newest,
    most credible first), at most `batch_lab_per_source` per source. They carry
    no severity marker, so without a lane they sank below the cut: OpenAI's
    "Securing our frontier model training environment" (2026-10-23) did."""
    days = int(setting(conf, "batch_story_days"))
    eligible = [
        x for x in ranked
        if id(x) not in known and lab_relevant(x, conf) and recent(x, days)
        and not c.news_denylist_hit(x)
    ]  # fmt: skip
    per_source = max(1, int(setting(conf, "batch_lab_per_source")))
    return deal(eligible, limit, per_source, used=used, fill=False)


def eff_lane(
    ranked: list[dict], conf: c.Config, limit: int, used: Counter, known: set[int]
) -> list[dict]:
    """Up to `limit` recent candidates whose title or excerpt names a
    `batch_eff_terms` phrase (token spend, prompt caching, subagents, parallel
    agents, ...), at most `batch_eff_per_source` per source. Practitioner posts
    on cost and work efficiency carry no severity marker, so they sank below the
    cut like lab posts did. Runs after the must-not-miss and lab lanes; the
    caller passes only what those lanes left."""
    days = int(setting(conf, "batch_story_days"))
    eligible = [
        x for x in ranked
        if id(x) not in known and recent(x, days) and not c.news_denylist_hit(x)
        and lab_terms_hit(
            f"{x.get('title') or ''} {x.get('excerpt') or ''}".lower(), conf, "batch_eff_terms"
        )
    ]  # fmt: skip
    per_source = max(1, int(setting(conf, "batch_eff_per_source")))
    return deal(eligible, limit, per_source, used=used, fill=False)


def priority_lane(ranked: list[dict], limit: int, per_source: int, conf: c.Config) -> list[dict]:
    """Up to `limit` must-not-miss candidates, dealt in turn between KEV and
    GHSA, at most `per_source` from either. Within GHSA: critical advisories in
    AI tooling, then the other critical ones, then high ones in AI tooling, so
    a HIGH can never take a critical's slot. Otherwise rank (newest) order."""
    eligible = sorted(
        (x for x in ranked if priority_class(x, conf)), key=lambda x: lane_order(x, conf)
    )  # stable
    return deal(eligible, limit, per_source, fill=False)


def class_floor(
    ranked: list[dict], mins: dict[str, int], room: int, per_source: int, used: Counter
) -> list[dict]:
    """The best `mins[class]` candidates of each named class, before the deal, so a
    class whose heads score low (curator links carry the issue's date, not the
    article's) still reaches the batch. Per-source capped like the deal."""
    out: list[dict] = []
    for cls in sorted(mins):
        pool = [x for x in ranked if ingestor_class(x) == cls]
        limit = min(max(0, int(mins[cls])), room - len(out))
        out += deal(pool, limit, per_source, used=used + Counter(map(source_key, out)), fill=False)
    return out


# --- big stories (newsworthy.py) ---------------------------------------------
def story_signals_on(conf: c.Config) -> bool:
    keys = ("batch_story_max", "batch_marker_bonus", "batch_corroboration_bonus")
    return any(float(setting(conf, k)) > 0 for k in keys)


def reference_docs() -> list[dict]:
    """What was written before this run: the pools + archive."""
    return c.all_pool_entries() + list(c.load_json(c.ARCHIVE_FILE, default=[]) or [])


def ledger_sources(days: int) -> list[dict]:
    """Covering sources the story ledger holds from the last `days`."""
    cutoff = (c.utcnow().date() - timedelta(days=days)).isoformat()
    rows = []
    for story in sl.load_ledger()["stories"].values():
        for src in story.get("sources") or []:
            day = src.get("date") or story.get("last_updated") or ""
            if day >= cutoff:
                rows.append({"title": src.get("title") or story["title"], "published": day})
    return rows


def story_signals(
    pool: list[dict], conf: c.Config, reference: list[dict] | None, known: list[dict] | None
) -> list[nw.Signal | None]:
    """newsworthy.analyze over the bucketed pool, or Nones when every story
    knob is off (then selection is exactly what it was)."""
    if not story_signals_on(conf):
        return [None] * len(pool)
    reference = reference_docs() if reference is None else reference
    known = ledger_sources(nw.MATCH_DAYS) if known is None else known
    return nw.analyze(pool, reference, nw.publisher, known)


def news_bonus(sig: nw.Signal | None, conf: c.Config) -> float:
    if sig is None:
        return 0.0
    marker = float(setting(conf, "batch_marker_bonus"))
    per_source = float(setting(conf, "batch_corroboration_bonus"))
    return nw.bonus(sig, marker, per_source, CORROBORATION_MAX)


def recent(cand: dict, days: int) -> bool:
    day = str(cand.get("published") or "")[:10]
    return bool(day) and day >= (c.utcnow().date() - timedelta(days=days)).isoformat()


def story_groups(pool: list[dict], sigs: list, pos: dict) -> list[list[int]]:
    """Pool positions grouped by story, for every story staged by 2+ publishers.
    Greedy, best-covered first: a group is its leader plus the leader's own
    matches, then any other candidate matching at least half the group (so a
    twelve-outlet story stays one group). Never a plain chain: one loose match
    can't pull an unrelated story in, and a copy naming only CVEs the group
    doesn't is a different bug, never parked as "same" (an untagged article
    matching both CVE-1111 and CVE-2222 coverage can't bridge them)."""
    multi = [i for i, sig in enumerate(sigs) if sig is not None and sig.sources >= 2]
    order = sorted(multi, key=lambda i: (-sigs[i].sources, -len(sigs[i].markers), pos[id(pool[i])]))
    taken: set[int] = set()
    groups: list[list[int]] = []
    for i in order:
        if i in taken:
            continue
        group, ids = [i], set(sigs[i].ids)
        for k in [*sigs[i].matches, *multi]:
            if k in taken or k in group or not ids_compatible(ids, sigs[k].ids):
                continue
            if k in sigs[i].matches or 2 * len(set(group) & set(sigs[k].matches)) >= len(group):
                group.append(k)
                ids |= sigs[k].ids
        taken |= set(group)
        if len(group) > 1:  # a lone leader's coverage went to a bigger group
            groups.append(group)
    return groups


def ids_compatible(group_ids: set[str], ids: frozenset[str]) -> bool:
    """A copy may join unless both name CVE/GHSA ids and none are shared."""
    return not group_ids or not ids or bool(group_ids & ids)


def lane_worthy(cand: dict, sig: nw.Signal, conf: c.Config) -> bool:
    lo = int(setting(conf, "batch_story_min_sources"))
    hi = int(setting(conf, "batch_story_any_sources"))
    rank = float(setting(conf, "batch_story_min_rank"))
    return nw.is_big(sig, lo, hi, rank) and recent(cand, int(setting(conf, "batch_story_days")))


def story_lane(
    pool: list[dict], sigs: list, conf: c.Config, pos: dict, per_source: int, size: int
) -> tuple[list[dict], dict[int, dict], dict[int, tuple]]:
    """(lane, siblings, groups). Every multi-source story keeps ONE copy in
    play, its most credible; the others wait (siblings: id(copy) -> that head),
    since the judge would only call them `same`. Up to `batch_story_max`
    lane-worthy stories take a lane slot, at most `per_source` heads from one
    source. `groups` maps id(head) -> (leader's signal, lane-worthy, the other
    copies) for every story left without a lane slot (the news tier reads it)."""
    limit = min(size, int(setting(conf, "batch_story_max")))
    lane: list[dict] = []
    siblings: dict[int, dict] = {}
    groups: dict[int, tuple] = {}
    used: Counter = Counter()
    for group in story_groups(pool, sigs, pos):
        by_trust = sorted(
            group, key=lambda k: (-(pool[k].get("source_rank") or 0), pos[id(pool[k])])
        )
        open_heads = [k for k in by_trust if used[source_key(pool[k])] < per_source]
        lead = group_signal(sigs, group)
        worthy = lane_worthy(pool[group[0]], lead, conf)
        if len(lane) < limit and open_heads and worthy:
            head = open_heads[0]
            used[source_key(pool[head])] += 1
            lane.append(with_story(pool[head], lead, [pool[k] for k in group if k != head]))
        else:
            head = by_trust[0]
            groups[id(pool[head])] = (lead, worthy, [pool[k] for k in group if k != head])
        siblings |= {id(pool[k]): pool[head] for k in group if k != head}
    return lane, siblings, groups


def group_signal(sigs: list, group: list[int]) -> nw.Signal:
    """The story's signal: its best-covered copy's, with every copy's markers.
    A story carries a marker when any outlet's copy does: 2026-10-23's PAN-OS
    pair had "under attack" only in The Register's headline, not THN's."""
    lead = sigs[group[0]]
    return replace(lead, markers=frozenset().union(*(sigs[k].markers for k in group)))


def with_story(head: dict, sig: nw.Signal, others: list[dict]) -> dict:
    coverage = [x.get("source_url") or x.get("article_url") or "" for x in others]
    story = {"sources": sig.sources, "markers": sorted(sig.markers), "coverage": coverage}
    return {**head, "batch_priority": "story", "batch_story": story, "_head": id(head)}


def lane_order(cand: dict, conf: c.Config) -> int:
    kind = priority_class(cand, conf)
    if kind == "ghsa-ai" and str(cand.get("severity") or "").upper() == "CRITICAL":
        return 0
    return 2 if kind == "ghsa-ai" else 1


def select(
    candidates: list[dict],
    conf: c.Config,
    table: pf.KeywordTable,
    reference: list[dict] | None = None,
    known: list[dict] | None = None,
) -> tuple[list[dict], list[dict]]:
    """Split staged candidates into (session set, backlog): the deep batch,
    then the news tier (each tagged `batch_tier: "news"`). See select_tiers."""
    batch, news, backlog = select_tiers(candidates, conf, table, reference, known)
    return batch + news, backlog


def select_tiers(
    candidates: list[dict],
    conf: c.Config,
    table: pf.KeywordTable,
    reference: list[dict] | None = None,
    known: list[dict] | None = None,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Split staged candidates into (deep batch, news tier, backlog).
    `reference` (pools + archive) and `known` (story-ledger sources) default
    to the data files."""
    buckets = pf.bucket(candidates, table)
    rescued = lab_rescue(buckets.dropped, conf)
    rescued_ids = {id(x) for x in rescued}
    dropped = [x for x in buckets.dropped if id(x) not in rescued_ids]
    pool = buckets.routed + buckets.filtered + rescued
    sigs = story_signals(pool, conf, reference, known)
    bonus = {id(x): news_bonus(sig, conf) for x, sig in zip(pool, sigs, strict=True)}
    ranked = sorted(pool, key=lambda x: (-(score(x, conf) + bonus[id(x)]), str(x.get("id") or "")))
    pos = {id(x): i for i, x in enumerate(ranked)}
    size = batch_size(conf)
    per_source = max(1, int(setting(conf, "batch_per_source")))
    stories, siblings, groups = story_lane(pool, sigs, conf, pos, per_source, size)
    heads = {s.pop("_head") for s in stories}
    out = heads | set(siblings)
    open_ = [x for x in ranked if id(x) not in out]
    lane_max = min(size - len(stories), max(0, int(setting(conf, "batch_priority_max"))))
    gone = [x for x in open_ if ghsa_dropped(x, conf, groups)]
    open_ = [x for x in open_ if id(x) not in {id(g) for g in gone}]
    dropped += [ghsa_drop_note(x) for x in gone]
    lane = priority_lane(
        open_, lane_max, max(1, int(setting(conf, "batch_priority_per_source"))), conf
    )
    room = size - len(stories) - len(lane)
    lab_max = min(room, max(0, int(setting(conf, "batch_lab_max"))))
    lane_ids0 = {id(x) for x in lane}
    held = {id(x) for x, sig in zip(pool, sigs, strict=True) if sig is not None and sig.known}
    labs = lab_lane(
        [x for x in open_ if id(x) not in lane_ids0], conf, lab_max,
        Counter(source_key(x) for x in stories + lane), held,
    )  # fmt: skip
    lane = lane + labs
    eff_max = min(size - len(stories) - len(lane), max(0, int(setting(conf, "batch_eff_max"))))
    taken = {id(x) for x in lane}
    effs = eff_lane(
        [x for x in open_ if id(x) not in taken], conf, eff_max,
        Counter(source_key(x) for x in stories + lane), held,
    )  # fmt: skip
    eff_ids = {id(x) for x in effs}
    lane = lane + effs
    mins = conf.limits.get("batch_class_min") or {}
    lane_ids = {id(x) for x in lane}
    first = Counter(source_key(x) for x in stories + lane)
    floor = class_floor(
        [x for x in open_ if id(x) not in lane_ids], mins, size - len(stories) - len(lane),
        per_source, first,
    )  # fmt: skip
    in_lane = lane_ids | {id(x) for x in floor}
    slots = conf.limits.get("batch_class_slots") or {}
    used = first + Counter(source_key(x) for x in floor)
    dealt = deal(
        [x for x in open_ if id(x) not in in_lane],
        size - len(stories) - len(lane) - len(floor), per_source, slots, used,
    )  # fmt: skip
    ids = in_lane | {id(x) for x in dealt}
    left = [x for x in open_ if id(x) not in ids]
    sig_of = {id(x): sig for x, sig in zip(pool, sigs, strict=True)}
    news = news_tier(left, sig_of, groups, conf)
    news_ids = {n.pop("_cand") for n in news}
    rest = [x for x in left if id(x) not in news_ids] + [x for x in ranked if id(x) in siblings]
    batch = (
        stories
        + [{**x, "batch_priority": lane_tag(x, eff_ids, conf)} for x in lane]
        + floor
        + dealt
    )
    backlog = [
        {**x, "batch_rank": i, **same_story_note(x, siblings)}
        for i, x in enumerate(rest, start=len(batch) + len(news) + 1)
    ]
    return batch, news, backlog + dropped


def lane_tag(cand: dict, eff_ids: set[int], conf: c.Config) -> str:
    """batch_priority of a lane member: its must-not-miss class, else efficiency
    (the efficiency lane's pick), else lab."""
    return priority_class(cand, conf) or ("efficiency" if id(cand) in eff_ids else "lab")


# --- the news tier -------------------------------------------------------------
NEWS_ORDER = ("story", "priority", "marker", "lab")  # reasons, strongest first


def news_reason(
    cand: dict, sig: nw.Signal | None, group: tuple | None, conf: c.Config
) -> str | None:
    """Why a candidate the deep batch left over is relevant news, else None."""
    if not recent(cand, int(setting(conf, "batch_story_days"))) or c.news_denylist_hit(cand):
        return None
    if group is not None and group[1]:
        return "story"
    if priority_class(cand, conf):
        return "priority"
    held = sig is not None and sig.known  # the ledger already has this story
    lab = "lab" if lab_on(conf) and not held and lab_relevant(cand, conf) else None
    if sig is None or not sig.markers or sig.known or nw.publisher(cand) in nw.NON_INDEPENDENT:
        return lab
    return "marker" if float(cand.get("source_rank") or 0.0) >= news_rank_floor(conf) else lab


def news_rank_floor(conf: c.Config) -> float:
    """The source rank a single-source marker needs for a brief: its own
    `batch_news_min_rank` (a brief is one grounded quote, not a lane slot, so
    credible outlets ranked below the lane's floor count), else the lane's."""
    own = setting(conf, "batch_news_min_rank")
    floor = setting(conf, "batch_story_min_rank") if own is None else own
    return max(float(floor), 1e-9)


def news_tier(left: list[dict], sig_of: dict, groups: dict, conf: c.Config) -> list[dict]:
    """Up to `max_news_per_run` news-tier candidates from `left` (best-first):
    stories, then must-not-miss advisories, then single-source markers, at
    most `batch_news_per_source` from one source. Each carries `batch_tier`
    and `batch_news`; `_cand` (id() of the original) is popped by the caller."""
    limit = max(0, int(setting(conf, "max_news_per_run")))
    if not limit:
        return []
    found = [(news_reason(x, sig_of.get(id(x)), groups.get(id(x)), conf), x) for x in left]
    order = {r: i for i, r in enumerate(NEWS_ORDER)}
    picks = sorted(((r, x) for r, x in found if r), key=lambda rx: order[rx[0]])  # stable
    per_source = max(1, int(setting(conf, "batch_news_per_source")))
    used: Counter = Counter()
    out: list[dict] = []
    for reason, cand in picks:
        if len(out) >= limit:
            break
        if used[source_key(cand)] >= per_source:
            continue
        used[source_key(cand)] += 1
        out.append(news_entry(cand, reason, sig_of.get(id(cand)), groups.get(id(cand)), conf))
    return out


def news_entry(
    cand: dict, reason: str, sig: nw.Signal | None, group: tuple | None, conf: c.Config
) -> dict:
    """The news-tier copy of a candidate: why it is news, its markers, how many
    publishers told it, and the story's other copies (its covering sources)."""
    lead = group[0] if group else sig
    note = {
        "reason": priority_class(cand, conf) if reason == "priority" else reason,
        "markers": sorted(lead.markers) if lead else [],
        "sources": lead.sources if lead else 1,
        "coverage": [coverage_row(x) for x in (group[2] if group else [])],
    }
    return {**cand, "batch_tier": NEWS, "batch_news": note, "_cand": id(cand)}


def coverage_row(cand: dict) -> dict:
    return {
        "url": cand.get("source_url") or cand.get("article_url") or "",
        "name": cand.get("source_name") or "",
        "published": cand.get("published") or "",
    }


def tiers_record(session: list[dict]) -> dict:
    """data/_scan_tiers.json: which candidate is in which tier. Code-owned (the
    session can't edit data/_scan*): merge_analysis.py accepts a news brief
    only for a news-tier candidate named here, and takes its coverage from here."""
    news = {
        x["id"]: {
            "url": x.get("article_url") or x.get("source_url") or "",
            "source_url": x.get("source_url") or x.get("article_url") or "",
            **x["batch_news"],
        }
        for x in session
        if x.get("batch_tier") == NEWS and x.get("id")
    }
    return {"deep": [x.get("id") for x in session if x.get("id") not in news], "news": news}


def same_story_note(cand: dict, siblings: dict[int, dict]) -> dict:
    head = siblings.get(id(cand))
    return {"batch_same_story_as": head.get("id")} if head else {}


def composition(batch: list[dict]) -> str:
    counts = Counter(source_key(x) for x in batch)
    return ", ".join(f"{k} x{n}" for k, n in counts.most_common())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(c.CONFIG_FILE))
    args = parser.parse_args(argv)
    conf = c.load_config(Path(args.config))
    candidates = c.load_candidates()
    batch, news, backlog = select_tiers(candidates, conf, pf.load_keywords())
    c.save_candidates(batch + news)
    c.save_json(c.DATA_DIR / c.SCAN_TIERS_SNAPSHOT, tiers_record(batch + news))
    c.save_json(backlog_file(), backlog)
    dropped = sum(1 for b in backlog if "batch_rank" not in b)
    print(
        f"SCAN_BATCH: {len(batch)} of {len(candidates)} candidates selected "
        f"(batch size {batch_size(conf)}); {len(news)} news-tier briefs "
        f"(cap {int(setting(conf, 'max_news_per_run'))}); {len(backlog) - dropped} below the "
        f"cut and {dropped} prefilter-dropped -> data/{BACKLOG_NAME}"
    )
    print(f"SCAN_BATCH sources: {composition(batch)}")
    if news:
        why = Counter(x["batch_news"]["reason"] for x in news)
        print(f"SCAN_BATCH news tier: {', '.join(f'{k} x{n}' for k, n in why.most_common())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
