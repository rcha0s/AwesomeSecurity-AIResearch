"""refuter_panel.py — perspective-diverse refuter panel for standing claims.

The panel runs three lenses against a claim, each pushed to refute:

- **correctness** — is the claim actually true given the source? Refuting here
  is a *hard veto*: the claim's status moves to `contested` in the ledger.
- **prior-art**  — is this genuinely new, or a restatement of a known result?
  Refuting is *advisory*: attached as a caveat chip, status unchanged.
- **scope**      — does the claim generalize as stated? Refuting is *advisory*:
  attached as a caveat chip, status unchanged.

The LLM boundary is a `verdict_provider` callable — one call per lens, giving
each lens the same claim + source but a different system prompt. This module
is pure composition around that callable; tests stub the provider and assert
the composition logic, not the model reasoning.

Mirrors `verify_citations.py`'s shape: a single small pure module that can be
composed into `drift_review.py` and exercised with fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol


LENSES: tuple[str, ...] = ("correctness", "prior-art", "scope")
VERDICTS: tuple[str, ...] = ("uphold", "refute", "abstain")

# Only prior-art and scope refutes become advisory notes; correctness is a
# hard veto, not a caveat (the caveat surface is for "true but with a hedge").
ADVISORY_LENSES: tuple[str, ...] = ("prior-art", "scope")


@dataclass(frozen=True)
class Verdict:
    """One lens's verdict on a claim. Immutable — retries build new instances."""

    lens: str
    verdict: str
    note: str

    def __post_init__(self) -> None:
        if self.lens not in LENSES:
            raise ValueError(f"lens must be one of {LENSES} (got {self.lens!r})")
        if self.verdict not in VERDICTS:
            raise ValueError(f"verdict must be one of {VERDICTS} (got {self.verdict!r})")


@dataclass(frozen=True)
class Caveat:
    """An advisory note rendered as a chip next to the claim."""

    lens: str
    note: str


@dataclass(frozen=True)
class PanelResult:
    """The panel's decision. `status_change` is None or `'contested'`."""

    verdicts: tuple[Verdict, ...]
    status_change: str | None
    caveats: tuple[Caveat, ...]


class VerdictProvider(Protocol):
    """The LLM boundary. Tests stub this; production hands in a real model call."""

    def __call__(self, claim: dict, lens: str, source_text: str) -> Verdict: ...


def run_panel(
    claim: dict,
    source_text: str,
    provider: Callable[[dict, str, str], Verdict],
) -> PanelResult:
    """Run all three lenses and reconcile their verdicts into a panel result.

    Correctness=refute → status_change='contested' (hard veto).
    prior-art/scope=refute → attached to `caveats` (advisory, status unchanged).
    Uphold and abstain contribute nothing to `caveats` or `status_change`.
    """
    verdicts = tuple(provider(claim, lens, source_text) for lens in LENSES)
    status_change = _reconcile_status(verdicts)
    caveats = _extract_caveats(verdicts)
    return PanelResult(verdicts=verdicts, status_change=status_change, caveats=caveats)


def _reconcile_status(verdicts: tuple[Verdict, ...]) -> str | None:
    for v in verdicts:
        if v.lens == "correctness" and v.verdict == "refute":
            return "contested"
    return None


def _extract_caveats(verdicts: tuple[Verdict, ...]) -> tuple[Caveat, ...]:
    return tuple(
        Caveat(lens=v.lens, note=v.note)
        for v in verdicts
        if v.lens in ADVISORY_LENSES and v.verdict == "refute"
    )
