#!/usr/bin/env python3
"""
taxonomy.py — the one loader for `data/taxonomy.yaml` (topics → domain IDs).

Every reader of "what is this finding about" goes through here: the prefilter's
keyword routing, merge's domain gate, rerank's normalization, the renderers'
display names, and the claim engine's eligibility flag. Nothing else parses the
YAML.

A domain value is valid only if it is an ID that belongs to the entry's own
topic (`ais.prompt-injection` on an `ai-security` entry). Anything else is a
free-text label: it is resolved to an ID (migration override → alias → domain
name → keyword hints → the topic's default), the label is kept as
`domain_label`, and a label the alias map didn't know also becomes a tag.

Deliberately imports nothing from `common` so `common` can import it.

Usage:
    python scripts/taxonomy.py list      # the domain list the analyzer picks from
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TAXONOMY_FILE = DATA_DIR / "taxonomy.yaml"
MIGRATION_FILE = DATA_DIR / "taxonomy_migration.json"

_ID = re.compile(r"^[a-z]+\.[a-z0-9]+(?:-[a-z0-9]+)*$")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_STOP_WORDS = frozenset({"and"})


@dataclass(frozen=True)
class Domain:
    id: str
    topic: str
    name: str
    scope: str
    keywords: tuple[str, ...]
    claim_eligible: bool
    legacy_clusters: tuple[str, ...]

    @property
    def slug(self) -> str:
        """Directory-safe part after the prefix: 'ais.mcp-tools' -> 'mcp-tools'."""
        return self.id.split(".", 1)[1]


@dataclass(frozen=True)
class Taxonomy:
    version: int
    domains: dict[str, Domain]
    defaults: dict[str, str]  # topic -> default domain id
    aliases: dict[tuple[str, str], str]  # (topic, norm_label) -> domain id
    excluded_terms: tuple[str, ...]
    adjacent: tuple[str, ...]
    excluded: tuple[str, ...]

    def for_topic(self, topic: str) -> list[Domain]:
        return [d for d in self.domains.values() if d.topic == topic]

    def is_valid(self, value: object, topic: str | None = None) -> bool:
        """True if `value` is a domain ID (of `topic`, when given)."""
        dom = self.domains.get(value) if isinstance(value, str) else None
        return dom is not None and (topic is None or dom.topic == topic)

    def name(self, value: str) -> str:
        """Display name for an ID; a non-ID passes through unchanged."""
        dom = self.domains.get(value)
        return dom.name if dom else value


def norm_label(label: str) -> str:
    """Matching key for a free-text label: case, punctuation and 'and' ignored."""
    words = _NON_ALNUM.sub(" ", (label or "").lower()).split()
    return " ".join(w for w in words if w not in _STOP_WORDS)


def label_tag(label: str) -> str:
    """The kebab tag a free-text label becomes ('MCP & Tools' -> 'mcp-tools')."""
    return norm_label(label).replace(" ", "-")


# --- Loading -----------------------------------------------------------------
def _parse_domain(did: str, body: dict, prefixes: dict[str, str]) -> Domain:
    if not _ID.match(did):
        raise ValueError(f"taxonomy: bad domain id {did!r} (want <prefix>.<kebab-slug>)")
    topic = next((t for t, p in prefixes.items() if did.startswith(p + ".")), None)
    if topic is None:
        raise ValueError(f"taxonomy: {did!r} has no known topic prefix")
    name = str(body.get("name") or "").strip()
    scope = str(body.get("scope") or "").strip()
    keywords = tuple(str(k).lower() for k in body.get("keywords") or ())
    eligible = body.get("claim_eligible")
    if not name or not scope or not keywords or not isinstance(eligible, bool):
        raise ValueError(f"taxonomy: {did} needs name, scope, keywords and claim_eligible")
    clusters = tuple(body.get("legacy_clusters") or ())
    return Domain(did, topic, name, scope, keywords, eligible, clusters)


def _parse_aliases(raw: dict, domains: dict[str, Domain]) -> dict[tuple[str, str], str]:
    aliases: dict[tuple[str, str], str] = {}
    for topic, rows in (raw or {}).items():
        for label, did in (rows or {}).items():
            dom = domains.get(did)
            if dom is None or dom.topic != topic:
                raise ValueError(f"taxonomy: alias {label!r} -> {did!r} is not a {topic} id")
            aliases[(topic, norm_label(str(label)))] = did
    return aliases


def load(path: Path | None = None) -> Taxonomy:
    """Load and validate the taxonomy. Raises on a missing file or bad shape:
    the vocabulary is load-bearing config, never a soft default."""
    raw = yaml.safe_load((path or TAXONOMY_FILE).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not raw.get("topics") or not raw.get("domains"):
        raise ValueError("taxonomy: needs 'topics' and 'domains'")
    prefixes = {t: str(body["prefix"]) for t, body in raw["topics"].items()}
    domains = {did: _parse_domain(did, body, prefixes) for did, body in raw["domains"].items()}
    defaults = {t: str(body.get("default_domain")) for t, body in raw["topics"].items()}
    for topic, did in defaults.items():
        if not (did in domains and domains[did].topic == topic):
            raise ValueError(f"taxonomy: default_domain for {topic} is not one of its ids")
    return Taxonomy(
        version=int(raw.get("version", 1)),
        domains=domains,
        defaults=defaults,
        aliases=_parse_aliases(raw.get("aliases"), domains),
        excluded_terms=tuple(str(t).lower() for t in raw.get("excluded_terms") or ()),
        adjacent=tuple(raw.get("adjacent") or ()),
        excluded=tuple(raw.get("excluded") or ()),
    )


@lru_cache(maxsize=1)
def get() -> Taxonomy:
    """The repo taxonomy, loaded once per process."""
    return load()


def load_overrides(path: Path | None = None) -> dict[str, str]:
    """Entry key -> domain ID from the migration table's per-entry decisions."""
    file = path or MIGRATION_FILE
    if not file.exists():
        return {}
    raw = json.loads(file.read_text(encoding="utf-8"))
    return {key: row["id"] for key, row in (raw.get("entry_overrides") or {}).items()}


# --- Resolution --------------------------------------------------------------
def keyword_scores(text: str, domains: list[Domain]) -> dict[str, int]:
    """Keyword-hit count per domain on a lowercased haystack."""
    text = (text or "").lower()
    return {d.id: sum(1 for kw in d.keywords if kw in text) for d in domains}


def entry_key(entry: dict) -> str:
    """The key `entry_overrides` uses: the entry id, else its source URL."""
    if entry.get("id"):
        return str(entry["id"])
    url = (entry.get("source_url") or "").strip().lower()
    return "url:" + re.sub(r"[#?].*$", "", url).rstrip("/")


def resolve(tax: Taxonomy, topic: str, label: str, text: str = "") -> tuple[str, str]:
    """Map a (possibly free-text) domain to an ID of `topic`.

    Returns (id, how), how ∈ id | alias | name | keywords | default."""
    if tax.is_valid(label, topic):
        return label, "id"
    key = norm_label(label)
    if (topic, key) in tax.aliases:
        return tax.aliases[(topic, key)], "alias"
    for dom in tax.for_topic(topic):
        if key and norm_label(dom.name) == key:
            return dom.id, "name"
    scores = keyword_scores(f"{label} {text}", tax.for_topic(topic))
    best = max(scores.values(), default=0)
    if best > 0:
        return next(d for d, s in scores.items() if s == best), "keywords"
    return tax.defaults[topic], "default"


def entry_text(entry: dict) -> str:
    """What keyword resolution reads when the label alone doesn't decide."""
    return " ".join(str(entry.get(k) or "") for k in ("title", "summary", "takeaway"))


# A label the alias map (or a domain name) already knows is just a synonym of
# its domain; only a genuinely new label carries information worth a tag.
_NEW_LABEL = frozenset({"keywords", "default"})


def _file_label(entry: dict, label: str, did: str, how: str) -> None:
    """Set the ID, keep the original label as `domain_label` (provenance), and
    tag it when it was new to the alias map (normalized: 'MCP Drift' -> 'mcp-drift')."""
    tags = list(entry.get("tags") or [])
    tag = label_tag(label)
    if how in _NEW_LABEL and tag and tag not in tags:
        entry["tags"] = tags + [tag]
    if label:
        entry["domain_label"] = label
    entry["domain"] = did


def normalize_entry(entry: dict, tax: Taxonomy, overrides: dict[str, str]) -> tuple[str, str]:
    """Give a pipeline entry a valid domain ID in place. Returns (id, how).

    Already-published data is remapped, never held: this is the migration's
    path and the convergence path for other branches' pools."""
    topic, label = entry.get("topic") or "", str(entry.get("domain") or "")
    if topic not in tax.defaults or tax.is_valid(label, topic):
        return label, "id"
    override = overrides.get(entry_key(entry))
    if tax.is_valid(override, topic):
        did, how = override, "override"
    else:
        did, how = resolve(tax, topic, label, entry_text(entry))
    _file_label(entry, label, did, how)
    return did, how


def normalize_entries(entries: list[dict], tax: Taxonomy, overrides: dict[str, str]) -> int:
    """Normalize every entry in place; return how many changed."""
    return sum(1 for e in entries if normalize_entry(e, tax, overrides)[1] != "id")


def enforce(entry: dict, tax: Taxonomy) -> dict:
    """Merge's gate: an analyzer domain that is not an ID of the entry's topic
    holds the entry for review (`domain_hold`). It still gets the nearest ID so
    the pool stays 100% valid; a label the alias map doesn't know lands in `tags`."""
    topic, label = entry.get("topic") or "", str(entry.get("domain") or "")
    if tax.is_valid(label, topic):
        return entry
    did, how = resolve(tax, topic, label, entry_text(entry))
    _file_label(entry, label, did, how)
    entry["needs_review"] = True
    entry["domain_hold"] = (
        f"analyzer domain {label!r} is not a {topic} taxonomy id; "
        f"filed under {did} via {how} until a reviewer confirms"
    )
    return entry


def claim_eligible(entry: dict, tax: Taxonomy | None = None) -> bool:
    """True if the entry's domain gets full claim work (ledger, refuter, drift).
    Replaces the old `interests.is_tier1` cluster check."""
    tax = tax or get()
    dom = tax.domains.get(entry.get("domain") or "")
    return bool(dom and dom.topic == entry.get("topic") and dom.claim_eligible)


# --- Analyzer prompt context -------------------------------------------------
def prompt_context(tax: Taxonomy) -> str:
    """The domain list the analyzer picks from, as compact Markdown."""
    lines = ["# Domain IDs (pick exactly one for the entry's topic)", ""]
    for topic in tax.defaults:
        lines.append(f"## {topic}")
        for d in tax.for_topic(topic):
            flag = "claims" if d.claim_eligible else "news only"
            lines.append(f"- `{d.id}` {d.name} ({flag}): {d.scope}")
        lines.append("")
    lines.append("Adjacent (news lane): " + "; ".join(tax.adjacent))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args[:1] != ["list"]:
        print("usage: taxonomy.py list", file=sys.stderr)
        return 2
    print(prompt_context(get()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
