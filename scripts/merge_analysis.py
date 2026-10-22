#!/usr/bin/env python3
"""
merge_analysis.py — Fold the LLM's analysis output into the research pools.

Reads data/analysis_out.json (a list of fully-analyzed v2 entries emitted by the
/research-scan or /add-resource skill), validates each against the schema,
de-duplicates against the existing pools (URL + fuzzy title), gates low-confidence
findings to needs_review, holds any entry whose `domain` is not a taxonomy ID
(data/taxonomy.yaml; the free-text label moves to `tags`), routes each into its
topic pool, records verified new-domain proposals, clears the merged candidates,
and re-ranks. Before that it applies the story judge's verdicts
(data/story_verdicts.json, see story_ledger.py): `same`/`update` candidates join
their story without a new entry, and every merged entry is put in its story. Idempotent: re-merging the same URL
updates the entry in place rather than duplicating it.

Each run also adds its counts to data/_merge_outcomes.json (merged, new,
updated, skipped_invalid), a code-owned record like data/_story_outcomes.md:
the scan session can't edit it, and `scan_count.py --work` reads it to decide
whether a scan did any work.

Usage:
    python scripts/merge_analysis.py
"""

from __future__ import annotations

import sys

import common as c
import content_checks as cc
import rerank
import sources_registry as sr
import story_ledger as sl
import taxonomy as tx
import taxonomy_proposals as tp
import verify_citations as vc


def record_merge(merged: int, new: int, invalid: int) -> dict:
    """Add one merge_analysis.py run's counts to the code-owned record."""
    rec = c.merge_record()
    add = {"merged": merged, "new": new, "updated": merged - new, "skipped_invalid": invalid}
    rec = {k: rec[k] + add[k] for k in c.MERGE_COUNTS}
    c.save_json(c.DATA_DIR / c.MERGE_RECORD_NAME, rec)
    return rec


def update_source_hit_rate(new_entries: list[dict]) -> None:
    """Bump each source's ingested/curated stats so productive sources rank up.
    Pass ONLY newly-added entries (not in-place updates) so re-merging the same
    input never double-counts. ingested = analyzed, curated = needs_review False."""
    deltas: dict[str, list[int]] = {}
    for e in new_entries:
        sid = e.get("source_id")
        if not sid:
            continue
        d = deltas.setdefault(sid, [0, 0])
        d[0] += 1
        if not e.get("needs_review"):
            d[1] += 1
    sr.update_stats({sid: (d[0], d[1]) for sid, d in deltas.items()})


def entry_confidence(entry: dict) -> float:
    lessons = entry.get("lessons") or []
    confs = [
        float(x.get("confidence"))
        for x in lessons
        if isinstance(x, dict) and x.get("confidence") is not None
    ]
    if "confidence" in entry:
        confs.append(float(entry["confidence"]))
    return min(confs) if confs else 1.0


def reconcile(existing: dict, new: dict) -> dict:
    """Fold a matched entry into an existing one. Same source ⇒ in-place update.
    Different source telling the same story ⇒ corroboration: keep the existing
    entry canonical and record the other source (raises its credibility)."""
    same_source = c.normalize_url(new.get("source_url", "")) == c.normalize_url(
        existing.get("source_url", "")
    )
    corr = list(existing.get("corroborating_sources") or [])
    if same_source:
        return {
            **existing,
            **new,
            "id": existing.get("id") or new.get("id"),
            "corroborating_sources": corr,
        }
    nu = c.normalize_url(new.get("source_url", ""))
    if nu and all(c.normalize_url(s.get("url", "")) != nu for s in corr):
        corr.append(
            {
                "name": new.get("source_name"),
                "url": new.get("source_url"),
                "published": new.get("published"),
            }
        )
    return {**existing, "corroborating_sources": corr}


def same_url(a: dict, b: dict) -> bool:
    return c.normalize_url(a.get("source_url", "")) == c.normalize_url(b.get("source_url", ""))


def match_index(entries: list[dict], entry: dict) -> int | None:
    urls = {
        c.normalize_url(entry.get(k, ""))
        for k in ("source_url", "article_url", "tweet_url")
        if entry.get(k)
    }
    for i, existing in enumerate(entries):
        for k in ("source_url", "article_url", "tweet_url"):
            if existing.get(k) and c.normalize_url(existing[k]) in urls:
                return i
        if c.title_similar(existing.get("title", ""), entry.get("title", "")):
            return i
    return None


def below_curation_bar(entry: dict, conf: c.Config) -> bool:
    """True if the finding isn't novel/relevant enough for the vetted set."""
    scores = entry.get("scores") or {}
    min_nov = conf.curation.get("min_novelty", 0)
    min_rel = conf.curation.get("min_relevance", 0)
    return (
        float(scores.get("novelty", 0) or 0) < min_nov
        or float(scores.get("relevance", 0) or 0) < min_rel
    )


def normalize_entry(entry: dict, conf: c.Config) -> dict:
    entry = dict(entry)
    for key in ("source_url", "article_url", "tweet_url"):
        if entry.get(key):
            entry[key] = c.clean_source_url(entry[key])
    url = entry.get("source_url") or entry.get("article_url") or entry.get("title", "")
    entry.setdefault("id", c.make_id(entry.get("title", ""), c.normalize_url(url)))
    entry.setdefault("retrieved_at", c.utcnow_iso())
    entry.setdefault("discovered_via", "manual")
    # Held from the vetted set if unverifiable OR not novel/relevant enough.
    entry["needs_review"] = entry_confidence(entry) < conf.confidence_min or below_curation_bar(
        entry, conf
    )
    return entry


def merge(
    analyzed: list[dict], conf: c.Config, placements: list | None = None
) -> tuple[list[dict], list[str], set[str], list[dict]]:
    """Returns (merged, errors, merged_urls, newly_added). `newly_added` are the
    entries that were freshly appended (not in-place updates) — only these should
    credit a source's hit-rate, so re-merging the same input never double-counts.
    `placements`, when given, collects (pool entry id, merged entry) pairs."""
    pools = {t: c.load_pool(t) for t in c.TOPICS}
    merged: list[dict] = []
    errors: list[str] = []
    merged_urls: set[str] = set()
    newly_added: list[dict] = []
    for raw in analyzed:
        # Only http(s) links reach the site: a javascript: URL is rejected here.
        problems = c.validate_entry(raw) + cc.url_problems(raw)
        if problems:
            errors.append(f"{raw.get('title', '?')[:50]}: {'; '.join(problems)}")
            continue
        entry = tx.enforce(normalize_entry(raw, conf), tx.get())
        # Ground each cited excerpt against the source; unverified quotes → review.
        vc.ground_entry(entry)
        if conf.curation.get("require_grounding", True) and not vc.fully_grounded(entry):
            entry["needs_review"] = True
        # A low-authority source whose quotes we couldn't confirm is suspect → review.
        gs = entry.get("grounding_score")
        confirmed = gs is not None and gs >= 1.0
        if c.credibility_of(entry) < conf.curation.get("min_credibility", 0) and not confirmed:
            entry["needs_review"] = True
        # The independent verifier (run by the skill) may have refuted the finding.
        if conf.curation.get("require_verification", True) and entry.get("verified") is False:
            entry["needs_review"] = True
        entries = pools[entry["topic"]]["entries"]
        idx = match_index(entries, entry)
        if idx is None:
            entries.append(entry)
            newly_added.append(entry)
        else:
            entries[idx] = reconcile(entries[idx], entry)
            if "domain_hold" not in entry and same_url(entries[idx], entry):
                for stale in ("domain_hold", "domain_label"):  # re-analysis fixed it
                    entries[idx].pop(stale, None)
        merged.append(entry)
        if placements is not None:
            placements.append((entries[len(entries) - 1 if idx is None else idx]["id"], entry))
        for k in ("source_url", "article_url"):
            if entry.get(k):
                merged_urls.add(c.normalize_url(entry[k]))
    for topic, pool in pools.items():
        c.save_pool(topic, pool)
    return merged, errors, merged_urls, newly_added


def clear_candidates(merged: list[dict], merged_urls: set[str]) -> int:
    merged_ids = {m["id"] for m in merged}
    remaining = [
        cand
        for cand in c.load_candidates()
        if cand.get("id") not in merged_ids
        and c.normalize_url(cand.get("source_url", "")) not in merged_urls
    ]
    before = len(c.load_candidates())
    c.save_candidates(remaining)
    return before - len(remaining)


def _corroborate_leads(outcomes: list[dict], ledger: dict) -> int:
    """A `same`/`update` source raises the story's lead pool entry's
    corroboration (and so its credibility). Archived leads are left alone."""
    pools = {t: c.load_pool(t) for t in c.TOPICS}
    by_id = {e.get("id"): e for p in pools.values() for e in p["entries"]}
    bumped = 0
    for out in outcomes:
        if out["action"] not in ("same", "update"):
            continue
        story = ledger["stories"][out["story_id"]]
        lead = next((by_id[e] for e in story["entry_ids"] if e in by_id), None)
        src = {"url": out["url"], "source_name": out.get("source_name"), "tier": out.get("tier")}
        if lead is not None and sl.corroborate_entry(lead, src):
            bumped += 1
    if bumped:
        for topic, pool in pools.items():
            c.save_pool(topic, pool)
    return bumped


def apply_story_verdicts() -> list[dict]:
    """Apply data/story_verdicts.json (the judge's output) to the ledger, drop
    the candidates it settled (same/update need no analysis), and record what a
    human should see — counts, every same/update, every CLAIM REVIEW, every
    rejection — both on stdout and in the code-owned data/_story_outcomes.md.
    Each verdict is checked against a freshly recomputed shortlist."""
    verdicts = c.load_json(c.DATA_DIR / sl.VERDICTS_FILE.name, default=None)
    if not verdicts:
        return []
    ledger = sl.load_ledger()
    cands = c.load_candidates()
    entries_by_id = {e["id"]: e for e in sl.all_entries() if e.get("id")}
    shortlists = sl.recompute_shortlists(ledger, cands, entries_by_id)
    outcomes = sl.apply_verdicts(
        ledger,
        verdicts,
        cands,
        shortlists,
        sources_by_id=c.load_sources_by_id(),
        entries_by_id=entries_by_id,
    )
    for out in outcomes:
        out["source_name"] = next(
            (x.get("source_name") for x in cands if x.get("id") == out.get("candidate_id")), ""
        )
    sl.save_ledger(ledger)
    _corroborate_leads(outcomes, ledger)
    settled = {o["candidate_id"] for o in outcomes if o["action"] in ("same", "update")}
    c.save_candidates([x for x in cands if x.get("id") not in settled])
    (c.DATA_DIR / sl.VERDICTS_FILE.name).unlink(missing_ok=True)
    sl.append_outcomes(outcomes)
    _print_outcomes(outcomes)
    return outcomes


def _print_outcomes(outcomes: list[dict]) -> None:
    counts = {a: sum(1 for o in outcomes if o["action"] == a) for a in sl.VERDICTS}
    rejected = [o for o in outcomes if o["action"] == "rejected"]
    print(
        f"Story verdicts: {counts['same']} same, {counts['update']} update, "
        f"{counts['new']} new, {len(rejected)} rejected."
    )
    for o in outcomes:
        if o["action"] == "update" and o.get("claims_to_review"):
            print(
                f"  CLAIM REVIEW: story {o['story_id']} updated by {o['url']}; linked claims "
                f"{', '.join(o['claims_to_review'])} may need supersession (not automatic)"
            )
    for o in rejected:
        print(f"  rejected verdict for {o.get('candidate_id')}: {o.get('reason')}", file=sys.stderr)


def ledger_placements(placements: list, outcomes: list[dict]) -> None:
    """Put every merged entry in its story: the judge's story for a judged
    candidate that was analyzed anyway, a forced new story for a `new`
    verdict, else the conservative deterministic match."""
    by_url = {c.normalize_url(o.get("url", "")): o for o in outcomes if o.get("url")}
    ledger = sl.load_ledger()
    sources = c.load_sources_by_id()
    window = sl.settings()["match_window_days"]
    for pool_id, entry in placements:
        out = by_url.get(c.normalize_url(entry.get("source_url", ""))) or {}
        src = sources.get(entry.get("source_id") or "", {})
        sl.assign_entry(
            ledger,
            {**entry, "id": pool_id},
            story_id=out.get("story_id") if out.get("action") in ("same", "update") else None,
            force_new=out.get("action") == "new",
            tier=src.get("tier", ""),
            source_name=src.get("name", ""),
            window_days=window,
        )
    sl.save_ledger(ledger)


CURATOR_FIELDS = ("curated_by", "curator_issue")


def stamp_curator(analyzed: list[dict], candidates: list[dict]) -> int:
    """Copy a curator-link candidate's provenance onto its analyzed entry.

    The recall eval's independent figure must know which entries came from a
    curator's own links (ingest_curator_links.py), so the marker is copied here,
    by candidate id or source URL, instead of trusting the analyzer to carry it."""
    by_key: dict[str, dict] = {}
    for cand in candidates:
        if cand.get("curated_by"):
            for key in (cand.get("id"), c.normalize_url(cand.get("source_url", ""))):
                if key:
                    by_key[str(key)] = cand
    stamped = 0
    for entry in (e for e in analyzed if isinstance(e, dict)):
        keys = (entry.get("id"), c.normalize_url(entry.get("source_url") or ""))
        cand = next((by_key[str(k)] for k in keys if k and str(k) in by_key), None)
        if cand:
            entry.update({k: cand[k] for k in CURATOR_FIELDS if cand.get(k)})
            entry.setdefault("source_id", cand.get("source_id"))
            stamped += 1
    return stamped


def main() -> int:
    conf = c.load_config()
    outcomes = apply_story_verdicts()
    analyzed = c.load_json(c.ANALYSIS_OUT, default=None)
    if not analyzed:
        if outcomes:
            rerank.rerank_all(conf)
            return 0
        print(f"No {c.ANALYSIS_OUT.name} to merge.", file=sys.stderr)
        return 1
    if isinstance(analyzed, dict):
        analyzed = analyzed.get("entries", [])

    stamp_curator(analyzed, c.load_candidates())
    placements: list = []
    merged, errors, merged_urls, newly_added = merge(analyzed, conf, placements)
    ledger_placements(placements, outcomes)
    record_merge(len(merged), len(newly_added), len(errors))
    print(f"Merged {len(merged)} entr(y/ies) into the pools ({len(newly_added)} new).")
    for topic in c.TOPICS:
        flagged = sum(1 for m in merged if m["topic"] == topic and m.get("needs_review"))
        count = sum(1 for m in merged if m["topic"] == topic)
        print(f"  {topic}: {count} merged ({flagged} flagged needs_review)")
    if errors:
        print(f"\nSkipped {len(errors)} invalid entr(y/ies):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)

    cleared = clear_candidates(merged, merged_urls)
    print(f"Cleared {cleared} staged candidate(s).")

    update_source_hit_rate(newly_added)  # credit only NEW findings, never re-counts
    proposals = tp.record(merged)
    if proposals:
        print(f"Recorded {len(proposals)} verified new-domain proposal(s).")
    rerank.rerank_all(conf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
