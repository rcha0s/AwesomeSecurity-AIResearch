"""drift_review.py — evidence-driven + time-based drift monitoring for the ledger.

Reads `related_claims` off analyzed entries and cross-references them against
the standing claim ledger. Runs the refuter panel on every (lesson, claim)
pairing so the lesson either:

- attaches to the claim as supporting evidence (correctness upheld);
- attaches with an advisory caveat (prior-art or scope refute);
- contests the claim (correctness refuted → status flips to contested).

Also runs a time-based sweep: any live claim whose `last_reviewed` is older
than the configured stale window (default 90 days) gets a `sweep_stale`
action, so quiet corners of the ledger don't rot silently.

`review()` returns a list of DriftAction objects — pure data. The renderer
turns those into PR body sections (`chore: contest <id>` / `chore: supersede
<old> → <new>` / evidence-attach edits). Git operations live in the render
skill, not here.

Mirrors the seam-shape of `verify_citations.py` and `refuter_panel.py`: pure
composition around a `verdict_provider` callable that tests stub.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Iterable

import claims
import refuter_panel as rp

# Default stale-review window. Revisit after the pipeline runs a few cycles —
# 90 was picked in the spec as a starting calibration, not a proven number.
DEFAULT_STALE_DAYS = 90

ACTION_KINDS = ("evidence_attach", "contest", "supersede", "refute", "sweep_stale")


@dataclass(frozen=True)
class DriftAction:
    """One proposed change against the ledger. The renderer turns these into
    PR body sections; nothing here writes to disk or opens a PR."""

    kind: str
    claim_id: str
    reason: str = ""
    caveats: tuple[rp.Caveat, ...] = ()
    source: dict | None = None


def review(
    entries: Iterable[dict],
    ledger: dict,
    provider: Callable[[dict, str, str], rp.Verdict],
    *,
    today: datetime,
    stale_days: int = DEFAULT_STALE_DAYS,
) -> list[DriftAction]:
    """Cross-reference entries' related_claims with the ledger; return the
    proposed drift actions plus the stale-review sweep."""
    index = claims.claim_index(claims.all_claims(ledger))
    actions: list[DriftAction] = []
    for entry in entries:
        actions.extend(_actions_for_entry(entry, index, provider))
    actions.extend(_stale_sweep(index, today=today, stale_days=stale_days))
    return actions


def _actions_for_entry(
    entry: dict,
    index: dict[str, dict],
    provider: Callable[[dict, str, str], rp.Verdict],
) -> list[DriftAction]:
    related = entry.get("related_claims") or []
    actions: list[DriftAction] = []
    for claim_id in related:
        claim = index.get(claim_id)
        if claim is None:
            # A stale claim_id from the analyzer isn't a bug worth crashing on,
            # but the maintainer should see it — the ledger and analyzer drift
            # apart quietly otherwise.
            _log_missing_claim(entry, claim_id)
            continue
        result = rp.run_panel(claim, _source_text_of(entry), provider)
        actions.append(_action_from_panel(entry, claim, result))
    return actions


def _action_from_panel(entry: dict, claim: dict, result: rp.PanelResult) -> DriftAction:
    if result.status_change == "contested":
        reason = _correctness_note(result) or "correctness refuter flagged the claim"
        return DriftAction(
            kind="contest",
            claim_id=claim["id"],
            reason=reason,
            caveats=result.caveats,
            source=entry,
        )
    # Correctness upheld → attach as evidence, with any advisory caveats.
    return DriftAction(
        kind="evidence_attach",
        claim_id=claim["id"],
        reason="",
        caveats=result.caveats,
        source=entry,
    )


def _correctness_note(result: rp.PanelResult) -> str:
    for v in result.verdicts:
        if v.lens == "correctness" and v.verdict == "refute":
            return v.note
    return ""


def _source_text_of(entry: dict) -> str:
    """Best available text to hand the refuter. Prefer summary + takeaway; fall
    back to the title. The provider is free to ignore this if it fetches its own."""
    for key in ("summary", "takeaway", "title"):
        if entry.get(key):
            return str(entry[key])
    return ""


# --- Time-based sweep -------------------------------------------------------
def _stale_sweep(
    index: dict[str, dict],
    *,
    today: datetime,
    stale_days: int,
) -> list[DriftAction]:
    cutoff = today - timedelta(days=stale_days)
    actions: list[DriftAction] = []
    for claim in index.values():
        if not claims.is_live(claim):
            continue
        last_reviewed = _parse_date(claim.get("last_reviewed"), tz=today.tzinfo)
        if last_reviewed is None or last_reviewed < cutoff:
            actions.append(
                DriftAction(
                    kind="sweep_stale",
                    claim_id=claim["id"],
                    reason=f"last_reviewed older than {stale_days} days",
                )
            )
    return actions


def _parse_date(value: str | None, *, tz) -> datetime | None:
    """Parse an ISO date/datetime and align its tz with `today` so comparisons
    are meaningful. Returns None for missing or malformed input."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None and tz is not None:
        return parsed.replace(tzinfo=tz)
    return parsed


def _log_missing_claim(entry: dict, claim_id: str) -> None:
    """Warn (not error) when an analyzer-emitted claim ID isn't in the ledger."""
    title = (entry.get("title") or "<untitled>")[:60]
    print(
        f"  ⚠ drift_review: unknown claim id {claim_id!r} referenced by "
        f"{title!r} — skipping",
        file=sys.stderr,
    )


# --- Summary shape for the render PR body -----------------------------------
def summarize(actions: Iterable[DriftAction]) -> dict[str, int]:
    """Counts per kind, in canonical order — the render step turns this into
    an H2 outline in the PR body ('N evidence-attached', 'N contested', ...)."""
    counts: dict[str, int] = dict.fromkeys(ACTION_KINDS, 0)
    for action in actions:
        if action.kind in counts:
            counts[action.kind] += 1
    return counts
