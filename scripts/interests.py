"""interests.py — the 13-cluster taxonomy seam.

Every downstream tier-decision reads one of two functions here:

- `cluster_for(entry, tax)` — the cluster letter the analyzer assigned,
  or None if the entry is adjacent (out of taxonomy).
- `is_tier1(entry, tax)` — shorthand for `cluster_for(entry, tax) is not None`.

The taxonomy itself lives in `data/interests.yaml`. The analyzer receives
that file as prompt context and emits `cluster: <letter>` per finding;
no keyword matching happens here — the model does the reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from common import DATA_DIR

DEFAULT_INTERESTS_FILE = DATA_DIR / "interests.yaml"

VALID_CLUSTERS = frozenset("ABCDEFGHIJKLM")


@dataclass(frozen=True)
class Cluster:
    letter: str
    name: str
    description: str
    scope: tuple[str, ...]


@dataclass(frozen=True)
class Taxonomy:
    version: int
    clusters: dict[str, Cluster]
    adjacent: tuple[str, ...]
    excluded: tuple[str, ...]


def load_interests(path: Path | None = None) -> Taxonomy:
    """Load and validate `data/interests.yaml`.

    Raises FileNotFoundError if the file is missing (a bug, not a soft
    default — the taxonomy is load-bearing config). Raises ValueError if
    the shape is wrong (missing `clusters` key, empty scope, unknown
    cluster letter, etc.).
    """
    file = path if path is not None else DEFAULT_INTERESTS_FILE
    if not file.exists():
        raise FileNotFoundError(f"interests taxonomy not found: {file}")
    with file.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict) or "clusters" not in raw:
        raise ValueError(f"interests taxonomy missing 'clusters' key: {file}")
    clusters_raw = raw["clusters"]
    if not isinstance(clusters_raw, dict) or not clusters_raw:
        raise ValueError(f"interests taxonomy has empty or invalid clusters: {file}")

    clusters: dict[str, Cluster] = {}
    for letter, body in clusters_raw.items():
        if letter not in VALID_CLUSTERS:
            raise ValueError(f"interests taxonomy contains unknown cluster letter: {letter!r}")
        if not isinstance(body, dict):
            raise ValueError(f"cluster {letter} is not a mapping")
        name = (body.get("name") or "").strip()
        description = (body.get("description") or "").strip()
        scope = tuple(body.get("scope") or ())
        if not name or not description or not scope:
            raise ValueError(f"cluster {letter} is missing name/description/scope")
        clusters[letter] = Cluster(letter=letter, name=name, description=description, scope=scope)

    adjacent = tuple(raw.get("adjacent") or ())
    excluded = tuple(raw.get("excluded") or ())
    return Taxonomy(
        version=int(raw.get("version", 1)),
        clusters=clusters,
        adjacent=adjacent,
        excluded=excluded,
    )


def cluster_for(entry: dict, tax: Taxonomy) -> str | None:
    """Return the cluster letter for an analyzed entry, or None if adjacent.

    Reads the `cluster` field the analyzer emits. An unknown or missing
    letter is treated as adjacent — never raises — so a stale entry can't
    break the pipeline.
    """
    value = entry.get("cluster")
    if not isinstance(value, str):
        return None
    if value not in tax.clusters:
        return None
    return value


def is_tier1(entry: dict, tax: Taxonomy) -> bool:
    """True if the entry falls inside the taxonomy (gets full claim work)."""
    return cluster_for(entry, tax) is not None
