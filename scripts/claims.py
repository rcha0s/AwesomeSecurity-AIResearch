#!/usr/bin/env python3
"""claims.py — the claim ledger: what we currently believe, and what we used to.

The three topic pools answer "what was published lately". They are a *feed*, and
they age out after `max_age_days`. This module answers a different question:
**what is the standing guidance right now, and what did it replace?**

A claim is durable and never ages out. It carries a `status`:

    current     the standing answer for its topic
    contested   credible evidence on both sides; no winner yet
    superseded  a better answer replaced it (the old one stays, demoted)
    refuted     shown to be wrong, not merely improved on

Supersession is an edge between claims, recorded on both ends: the retired claim
gets `superseded_by` + `superseded_on` + `supersession_reason`, and the winning
claim gets `supersedes`. That reciprocity is what lets the renderer push old
conclusions to the bottom of a page *with the reason they were pushed down*.

Every mutation here returns a new ledger — nothing is edited in place.
"""

from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

import common as c

CLAIMS_FILE = c.DATA_DIR / "claims.json"
CLAIMS_SCHEMA_VERSION = "1.0"

# `current`/`contested` are live (shown on top); `superseded`/`refuted` are
# retired (pushed to the bottom, with their reason).
LIVE_STATUSES = ("current", "contested")
RETIRED_STATUSES = ("superseded", "refuted")
STATUSES = LIVE_STATUSES + RETIRED_STATUSES

# How a cited source relates to the claim it is attached to.
STANCES = ("supports", "contests", "refutes")

# Research-phase axis, layered on top of the topic axis so the Fields view
# can render a taxonomy: what part of the research lifecycle does this claim
# speak to? Optional — a claim without a phase is fine, just harder to
# discover under the taxonomy view.
PHASES = (
    "threat-model",    # what the adversary can do; assumptions about power
    "attack",          # concrete attack techniques and demonstrations
    "defense",         # mitigations, detections, controls
    "evaluation",      # how to measure any of the above
    "deployment",      # what to do at operate/build time (harnesses, gates)
    "incident",        # observed real-world compromises + response
)

REQUIRED_FIELDS = ("id", "topic", "statement", "status")
EDGE_FIELDS = ("supersedes", "superseded_by")

DEFAULT_CONFIDENCE = 0.5

_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# --- Small accessors --------------------------------------------------------
def is_retired(claim: dict) -> bool:
    """True if this claim has been replaced or disproved (renders at the bottom)."""
    return claim.get("status") in RETIRED_STATUSES


def is_live(claim: dict) -> bool:
    """True if this claim still stands. An unrecognized status counts as live so a
    malformed entry is surfaced for a human rather than silently hidden."""
    return not is_retired(claim)


def confidence_of(claim: dict) -> float:
    try:
        return float(claim.get("confidence", DEFAULT_CONFIDENCE))
    except (TypeError, ValueError):
        return DEFAULT_CONFIDENCE


def edges(claim: dict, field: str) -> list[str]:
    """The claim ids on one side of the supersession edge (always a list)."""
    return list(claim.get(field) or [])


def claim_index(claim_list: list[dict]) -> dict[str, dict]:
    return {claim["id"]: claim for claim in claim_list if claim.get("id")}


def evidence_by_stance(claim: dict, stance: str) -> list[dict]:
    return [e for e in (claim.get("evidence") or []) if e.get("stance") == stance]


# --- Validation -------------------------------------------------------------

# A live claim whose statement invokes a fast-moving, recent domain (agents,
# MCP, LLM-specific attack surface) needs at least one evidence item dated in
# that era. Without one, the citation risks being a generic pre-agent
# reference that doesn't actually corroborate the specific mechanism being
# claimed — exactly the failure mode found in
# ssrf-guards-must-cover-agent-outbound-calls, an agent/MCP-specific claim
# whose only evidence was the undated, pre-2020 generic OWASP SSRF page.
# Retired claims are exempt: their evidence is frozen on purpose, as a record
# of what was believed at the time.
MODERN_AI_TERMS = re.compile(
    r"\bmcp\b|\bagents?\b|\bagentic\b|tool[- ](calls?|responses?|selection|descriptions?)"
    r"|retrieval[- ]augmented|\brag\b|coding[- ](agents?|assistants?)|prompt injection"
    r"|\bllms?\b|chatbot|jailbreak|ai[- ]generated|llm-generated",
    re.IGNORECASE,
)
MODERN_EVIDENCE_CUTOFF_YEAR = 2023


def _evidence_years(claim: dict) -> list[int]:
    years = []
    for item in claim.get("evidence") or []:
        if not isinstance(item, dict):
            continue
        match = re.match(r"(\d{4})", str(item.get("published") or ""))
        if match:
            years.append(int(match.group(1)))
    return years


def _validate_evidence_currency(claim: dict) -> list[str]:
    """A live claim describing agent/LLM-era concepts needs at least one
    evidence item dated in that era — see MODERN_AI_TERMS docstring above."""
    if claim.get("status") not in LIVE_STATUSES:
        return []
    text = f"{claim.get('statement') or ''} {' '.join(claim.get('tags') or [])}"
    if not MODERN_AI_TERMS.search(text):
        return []
    if any(year >= MODERN_EVIDENCE_CUTOFF_YEAR for year in _evidence_years(claim)):
        return []
    return [
        f"statement references agent/LLM-era concepts but no evidence item is dated "
        f"{MODERN_EVIDENCE_CUTOFF_YEAR} or later — the citation may predate the specific "
        "mechanism claimed; add a dated, on-topic source"
    ]


def _validate_evidence(claim: dict) -> list[str]:
    evidence = claim.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return ["evidence must be a non-empty list (a claim needs at least one source)"]
    errors: list[str] = []
    for i, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{i}] must be an object")
            continue
        if not item.get("url"):
            errors.append(f"evidence[{i}] missing url")
        if item.get("stance") not in STANCES:
            errors.append(f"evidence[{i}] stance must be one of {STANCES}")
    return errors


def _validate_status(claim: dict) -> list[str]:
    """Status must agree with the supersession edges: a retired claim has to say
    what replaced it and why; a live claim cannot already be replaced."""
    status = claim.get("status")
    if status is not None and status not in STATUSES:
        return [f"unknown status: {status} (want one of {STATUSES})"]
    errors: list[str] = []
    if status in RETIRED_STATUSES:
        if not edges(claim, "superseded_by"):
            errors.append(f"status '{status}' requires superseded_by (what replaced it)")
        if not claim.get("supersession_reason"):
            errors.append(f"status '{status}' requires supersession_reason (why it was retired)")
        if not claim.get("superseded_on"):
            errors.append(f"status '{status}' requires superseded_on (when it was retired)")
    elif status in LIVE_STATUSES and edges(claim, "superseded_by"):
        errors.append(
            f"a '{status}' claim cannot have superseded_by — set status to "
            f"one of {RETIRED_STATUSES} to retire it"
        )
    return errors


def _validate_edges(claim: dict, known_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for field in EDGE_FIELDS:
        for target in edges(claim, field):
            if target == claim.get("id"):
                errors.append(f"{field} references itself — a claim cannot supersede itself")
            elif target not in known_ids:
                errors.append(f"{field} references unknown claim: {target}")
    return errors


def validate_claim(claim: dict, known_ids: set[str]) -> list[str]:
    """Human-readable validation errors for one claim (empty == valid).

    `known_ids` is every id in the ledger, so edges can be resolved.
    """
    errors = [f"missing required field: {f}" for f in REQUIRED_FIELDS if not claim.get(f)]
    claim_id = claim.get("id")
    if claim_id and not _KEBAB.match(str(claim_id)):
        errors.append(f"id must be kebab-case: {claim_id}")
    topic = claim.get("topic")
    if topic and topic not in c.TOPICS:
        errors.append(f"unknown topic: {topic} (want one of {tuple(c.TOPICS)})")
    confidence = claim.get("confidence")
    if confidence is not None:
        try:
            if not 0.0 <= float(confidence) <= 1.0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"confidence must be a number in [0, 1] (got {confidence!r})")
    phase = claim.get("phase")
    if phase is not None and phase not in PHASES:
        errors.append(f"unknown phase: {phase} (want one of {PHASES})")
    return (
        errors
        + _validate_evidence(claim)
        + _validate_evidence_currency(claim)
        + _validate_status(claim)
        + _validate_edges(claim, known_ids)
    )


def _reciprocity_errors(index: dict[str, dict]) -> list[str]:
    """Both ends of a supersession must agree, or the ledger renders a claim as
    retired with nothing pointing back at it (or vice versa)."""
    errors: list[str] = []
    mirror = {"superseded_by": "supersedes", "supersedes": "superseded_by"}
    for claim_id, claim in index.items():
        for field, back in mirror.items():
            for target in edges(claim, field):
                other = index.get(target)
                if other is not None and claim_id not in edges(other, back):
                    errors.append(
                        f"non-reciprocal edge: {claim_id}.{field} lists {target}, "
                        f"but {target}.{back} does not list {claim_id}"
                    )
    return errors


def _cycle_errors(index: dict[str, dict]) -> list[str]:
    """Supersession must be a DAG — A replacing B replacing A is unrenderable."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(index, WHITE)
    errors: list[str] = []

    def visit(node: str, trail: list[str]) -> None:
        colour[node] = GREY
        for nxt in edges(index[node], "superseded_by"):
            if nxt not in index:
                continue
            if colour[nxt] == GREY:
                errors.append(f"supersession cycle: {' -> '.join(trail + [nxt])}")
            elif colour[nxt] == WHITE:
                visit(nxt, trail + [nxt])
        colour[node] = BLACK

    for node in index:
        if colour[node] == WHITE:
            visit(node, [node])
    return errors


def validate_ledger(ledger: dict) -> list[str]:
    """Validate every claim plus the cross-claim invariants (unique ids,
    reciprocal edges, no cycles)."""
    claim_list = ledger.get("claims") or []
    seen: set[str] = set()
    errors: list[str] = []
    for claim in claim_list:
        claim_id = claim.get("id")
        if claim_id and claim_id in seen:
            errors.append(f"duplicate claim id: {claim_id}")
        if claim_id:
            seen.add(claim_id)
    for claim in claim_list:
        errors += [f"{claim.get('id', '?')}: {e}" for e in validate_claim(claim, seen)]
    index = claim_index(claim_list)
    return errors + _reciprocity_errors(index) + _cycle_errors(index)


# --- Ordering: live on top, retired pushed to the bottom --------------------
def _live_key(claim: dict) -> tuple:
    """Settled answers before contested ones, then most-confident first."""
    return (0 if claim.get("status") == "current" else 1, -confidence_of(claim))


def order_claims(claim_list: list[dict]) -> list[dict]:
    """The canonical render order: live claims (current before contested, by
    confidence then recency), then retired ones, most recently retired first."""
    live = [claim for claim in claim_list if is_live(claim)]
    retired = [claim for claim in claim_list if is_retired(claim)]
    # Sort by date first; the stable sort below preserves it as the tie-breaker.
    live = sorted(live, key=lambda claim: claim.get("first_seen") or "", reverse=True)
    return sorted(live, key=_live_key) + sorted(
        retired, key=lambda claim: claim.get("superseded_on") or "", reverse=True
    )


def lineage(claim: dict, index: dict[str, dict]) -> list[dict]:
    """The chain of claims this one replaced, newest-replaced first. Dangling ids
    and cycles are skipped rather than raising — rendering must never crash."""
    chain: list[dict] = []
    seen: set[str] = {claim.get("id", "")}
    queue = edges(claim, "supersedes")
    while queue:
        claim_id = queue.pop(0)
        ancestor = index.get(claim_id)
        if ancestor is None or claim_id in seen:
            continue
        seen.add(claim_id)
        chain.append(ancestor)
        queue += edges(ancestor, "supersedes")
    return chain


# --- Mutations (each returns a new ledger) ---------------------------------
def add_claim(ledger: dict, claim: dict) -> dict:
    """Append a claim. Raises ValueError if the id is already taken."""
    updated = deepcopy(ledger)
    if claim.get("id") in claim_index(updated["claims"]):
        raise ValueError(f"claim id already exists: {claim.get('id')}")
    updated["claims"] = updated["claims"] + [deepcopy(claim)]
    return updated


def supersede(
    ledger: dict,
    old_id: str,
    new_id: str,
    reason: str,
    date: str,
    status: str = "superseded",
) -> dict:
    """Retire `old_id` in favour of `new_id`, writing both ends of the edge.

    `status` is "superseded" (a better answer replaced it) or "refuted" (it was
    shown to be wrong). Raises KeyError if either claim is unknown.
    """
    if status not in RETIRED_STATUSES:
        raise ValueError(f"status must be one of {RETIRED_STATUSES} (got {status!r})")
    updated = deepcopy(ledger)
    index = claim_index(updated["claims"])
    for claim_id in (old_id, new_id):
        if claim_id not in index:
            raise KeyError(f"unknown claim id: {claim_id}")

    old, new = index[old_id], index[new_id]
    old["status"] = status
    old["superseded_by"] = sorted(set(edges(old, "superseded_by") + [new_id]))
    old["superseded_on"] = date
    old["supersession_reason"] = reason
    new["supersedes"] = sorted(set(edges(new, "supersedes") + [old_id]))
    return updated


# --- Persistence ------------------------------------------------------------
def empty_ledger() -> dict:
    return {"schema_version": CLAIMS_SCHEMA_VERSION, "claims": []}


def load_ledger(path: Path | None = None) -> dict:
    ledger = c.load_json(path or CLAIMS_FILE, default=None)
    return ledger if ledger else empty_ledger()


def save_ledger(ledger: dict, path: Path | None = None) -> None:
    c.save_json(path or CLAIMS_FILE, ledger)


def claims_for_topic(ledger: dict, topic: str) -> list[dict]:
    """Every claim in one topic, in canonical render order."""
    return order_claims([cl for cl in ledger.get("claims") or [] if cl.get("topic") == topic])


def all_claims(ledger: dict) -> list[dict]:
    return list(ledger.get("claims") or [])


def stats(ledger: dict) -> dict[str, int]:
    """Counts per status, for badges and run summaries."""
    counts: dict[str, int] = dict.fromkeys(STATUSES, 0)
    for claim in all_claims(ledger):
        status = claim.get("status")
        if status in counts:
            counts[status] += 1
    return counts
