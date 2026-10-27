#!/usr/bin/env python3
"""
rewrite_guard.py — The readability rewrite may change words, never facts.

The analysis skill saves its entries to data/_analysis_draft.json before the
small-model readability rewrite. merge_analysis.py matches each analyzed entry
to its draft by source_url and, field by field (title, takeaway, summary, each
lesson point, actionable title + detail), restores the draft's text when the
rewrite changed what it says:

  number pairs   each number with the word after it, as a multiset
                 ("11 bugs in 6 frameworks" vs "6 bugs in 11 frameworks",
                 "5 MB" vs "5 GB", "92%" vs "3%", "Six" vs "Seven")
  guard words    negations, version-range, severity and polarity words, as
                 a multiset (not, no, never, n't, without, before, after,
                 critical, low, only, any, signed, default, enabled, patched,
                 authenticated, required, remote, ... see GUARD_WORDS), plus
                 any un-/non- form of one ("unfixed", "non-default")
  anchor pairs   each guard word or number with the next name or number in
                 its sentence, as a multiset, so a swap of what it applies to
                 shows ("Linux but not Windows", "critical in OpenSSL, low in
                 LibreSSL", "9.8 for CVE-A and 5.3 for CVE-B")
  names          capitalized words used mid-sentence (and sentence-initial or
                 title words that look like names, or are used as one elsewhere
                 in the entry) that vanish or appear: a vendor or product swap.
                 Moving a name within the field is fine
  facts          CVE/GHSA ids, numbers and code spans added or removed

The title is checked one way (`title_changes`): a shorter title may drop what
the takeaway or summary still says, but whatever it says must come from the
draft title or that prose, and it keeps every negation.

Lesson excerpts are verbatim quotes: any change to one is restored. A revert is
recorded on the entry (`readability_rewrite: "reverted <fields>"`) and never
holds it.

Scope: this catches a small model's rewrite errors. It is not a defence
against a hostile session, which writes the draft itself.

Usage:
    python scripts/rewrite_guard.py --check-draft   # exit 1 + warning when an
                                                    # analysis has no draft
"""

from __future__ import annotations

import argparse
import copy
import re
from collections import Counter

import common as c
import readability as rd

DRAFT = "_analysis_draft.json"  # the analysis before the readability rewrite
GUARD_WORDS = frozenset(
    "not no never without cannot unaffected before after prior since through until "
    "above below critical high medium low "
    # polarity: scope, defaults, state, auth, reach
    "only any all every none signed unsigned default enabled disabled on off patched "
    "fixed introduced vulnerable affected authenticated unauthenticated required "
    "mandatory optional local remote remotely up".split()
)
NUMBER_WORDS = (
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty "
    "hundred thousand million billion dozen half double triple"
)
TOKEN = re.compile(
    rf"\d[\d.,]*(?:%|[A-Za-z]+)?|\b(?:{NUMBER_WORDS.replace(' ', '|')})\b|[A-Za-z][\w'’&-]*",
    re.I,
)
NUMBER = re.compile(rf"\d|(?:{NUMBER_WORDS.replace(' ', '|')})$", re.I)
FACT = re.compile(r"`[^`]+`|\b(?:CVE|GHSA)-[\w-]+|\d[\d.,]*\s?(?:%|[kKMGTB]B?\b|x\b)?")
ENUMERATOR = re.compile(r"\(\d{1,2}\)|(?<![\w.])\d{1,2}[.)](?=\s)")  # "(1)" / "2." markers
POSSESSIVE = re.compile(r"['’]s$")
NOTE = "WARN: no data/_analysis_draft.json; the readability rewrite was not fact-checked"


# --- What a field says ------------------------------------------------------
def _tokens(text: str) -> list[str]:
    return [POSSESSIVE.sub("", t.rstrip(".,")) for t in TOKEN.findall(ENUMERATOR.sub(" ", text))]


def number_pairs(text: str) -> Counter:
    toks = _tokens(text)
    return Counter(
        (t.lower(), toks[i + 1].lower() if i + 1 < len(toks) else "")
        for i, t in enumerate(toks)
        if NUMBER.match(t)
    )


def guard(token: str) -> str | None:
    """The guard word a token is ('n't' for any contraction), or None."""
    t = token.lower()
    if t.endswith(("n't", "n’t")):
        return "n't"
    stem = re.sub(r"^(?:un|non-?)", "", t)
    return t if stem in GUARD_WORDS else None  # stem == t when there is no prefix


def guard_words(text: str) -> Counter:
    return Counter(g for g in map(guard, _tokens(text)) if g)


ANCHOR_WINDOW = 4  # tokens after a guard word or number that its anchor may sit in


def _is_name(token: str) -> bool:
    return token[:1].isupper() and token.lower() not in rd.FUNCTION_WORDS


def anchor_pairs(text: str) -> Counter:
    """Each guard word with the next name or number, and each number with the
    next name, within ANCHOR_WINDOW tokens of its sentence."""
    out: Counter = Counter()
    for s in rd.sentences(text):
        toks = _tokens(s)
        for i, t in enumerate(toks):
            g, num = guard(t), bool(NUMBER.match(t))
            if not (g or num):
                continue
            ahead = toks[i + 1 : i + 1 + ANCHOR_WINDOW]
            fits = (lambda x: _is_name(x) or bool(NUMBER.match(x))) if g else _is_name
            out[(g or t.lower(), next((x.lower() for x in ahead if fits(x)), ""))] += 1
    return out


def _namelike(token: str) -> bool:
    """Looks like a name wherever it stands: OpenAI, X25519, AWS."""
    return any(ch.isupper() or ch.isdigit() for ch in token[1:])


def names(text: str, known: frozenset[str] = frozenset(), title: bool = False) -> Counter:
    """Name uses in `text` (lowercased, counted): capitalized words used
    mid-sentence, plus a sentence's first word (or any Title Case title word)
    when it looks like a name or is used as one mid-sentence elsewhere in the
    entry (`known`, lowercased)."""
    out: Counter = Counter()
    for s in rd.sentences(text):
        toks = _tokens(s)
        for i, t in enumerate(toks):
            if not t[:1].isupper() or t.lower() in rd.FUNCTION_WORDS:
                continue
            if not (title or i == 0) or _namelike(t) or t.lower() in known:
                out[t.lower()] += 1
    return out


ACRONYM = re.compile(r"[A-Z][A-Z0-9&]{1,7}s?")  # IAM, IOCs, VCO, CT
CONNECTORS = frozenset({"of", "and", "the", "for", "to", "in", "on", "&"})
_PARTS = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")  # VeloCloud -> Velo, Cloud


def expansion(acronym: str, text: str, old: frozenset[str] = frozenset()) -> list[str] | None:
    """The words of `text` that spell out `acronym` by their initials (each
    word, or each camel-case/hyphen part of one, gives one letter; small
    connector words may be skipped), else None. Every spelled-out word must be
    new (not in `old`, the draft's words, lowercased): "Inventory certificates
    that" is the draft's own text, never an expansion of CT. "IOCs" -> "indicators of
    compromise", "VCO" -> "VeloCloud Orchestrator", "CT" -> "Certificate
    Transparency"; "IAM" -> "identity-management" is no expansion (it lost
    "access"), and neither is "EDR" -> "endpoint detection"."""
    letters = (acronym[:-1] if acronym.endswith("s") else acronym).lower()
    toks = [t for t in _tokens(text) if t[:1].isalpha()]
    for start, first in enumerate(toks):
        if first.lower() in CONNECTORS:
            continue
        used, k = [], 0
        for word in toks[start:]:
            initials = "".join(p[0].lower() for p in _PARTS.findall(word))
            if word.lower() in old and word.lower() not in CONNECTORS:
                break
            if initials and letters.startswith(initials, k):
                k += len(initials)
            elif word[:1].lower() == letters[k : k + 1]:
                k += 1
            elif word.lower() not in CONNECTORS:
                break
            used.append(word)
            if k == len(letters):
                return used
    return None


def explained_names(draft: str, final: str, lost: Counter, gained: Counter) -> None:
    """Forgive a name change that is only an acronym spelled out (the
    readability rewrite is told to expand acronyms): drop the acronym from
    `lost` and its expansion's words from `gained`, in place."""
    originals = {t.lower(): t for t in _tokens(draft) if ACRONYM.fullmatch(t)}
    old = frozenset(t.lower() for t in _tokens(draft))
    for acr in [a for a in lost if a in originals]:
        words = expansion(originals[acr], final, old)
        if words:
            del lost[acr]
            gained.subtract(Counter(w.lower() for w in words))
    for k in [k for k, v in gained.items() if v <= 0]:
        del gained[k]


def known_names(*entries: dict) -> frozenset[str]:
    """Mid-sentence names across the entries' prose fields (not the title), lowercased."""
    return frozenset(
        n.lower()
        for e in entries
        for path, text in fields(e).items()
        if path != "title"
        for n in names(text)
    )


def facts(text: str) -> set[str]:
    """CVE/GHSA ids, numbers and code spans."""
    found = {m.group(0).strip().rstrip(".,") for m in FACT.finditer(ENUMERATOR.sub(" ", text))}
    return found - {""}


def changes(
    draft: str, final: str, known: frozenset[str] = frozenset(), title: bool = False
) -> list[str]:
    """Why `final` no longer says what `draft` said ([] = same facts)."""
    out = []
    if number_pairs(draft) != number_pairs(final):
        out.append("numbers or what they count changed")
    if guard_words(draft) != guard_words(final):
        out.append("negation, range, severity or polarity words changed")
    elif anchor_pairs(draft) != anchor_pairs(final):
        out.append("what a guard word or number applies to changed")
    known = known | set(names(draft)) | set(names(final))  # names either text uses mid-sentence
    before, after = names(draft, known, title), names(final, known, title)
    lost, gained = before - after, after - before
    explained_names(draft, final, lost, gained)
    if lost or gained:
        out.append(f"names changed ({', '.join(sorted(lost + gained))})")
    lost, added = facts(draft) - facts(final), facts(final) - facts(draft)
    out += [f"dropped {f!r}" for f in sorted(lost)] + [f"added {f!r}" for f in sorted(added)]
    return out


NEGATIONS = frozenset({"not", "no", "never", "without", "cannot", "n't"})
PREPOSITIONS = frozenset({"on", "up"})  # guard words a rephrased title uses as plain prepositions


def title_changes(draft: str, final: str, prose: str = "") -> list[str]:
    """Why a shortened title no longer says what its draft said ([] = fine).

    A title may drop what the entry's takeaway or summary (`prose`) still
    says, so it is checked one way only: everything the new title says must
    be in the draft title or that prose, and it keeps every negation."""
    source = f"{draft}\n{prose}"
    out = []
    if number_pairs(final) - number_pairs(source):
        out.append("numbers or what they count changed")
    if set(guard_words(final)) - set(guard_words(source)) - PREPOSITIONS:
        out.append("negation, range, severity or polarity words changed")
    neg = Counter({g: n for g, n in guard_words(draft).items() if g in NEGATIONS})
    if neg - guard_words(final):
        out.append("dropped a negation")
    words = {t.lower() for t in _tokens(source)}
    gained = {
        t.lower() for t in _tokens(final)
        if t[:1].isupper() and t.lower() not in rd.FUNCTION_WORDS and t.lower() not in words
    }  # fmt: skip
    if gained:
        out.append(f"names changed ({', '.join(sorted(gained))})")
    out += [f"added {f!r}" for f in sorted(facts(final) - facts(source))]
    return out


# --- Fields -----------------------------------------------------------------
def fields(entry: dict) -> dict[str, str]:
    """Every rewritable field (plus excerpts) by path."""
    out = {k: entry.get(k) for k in ("title", "takeaway", "summary")}
    for i, le in enumerate(entry.get("lessons") or []):
        if isinstance(le, dict):
            out[f"lessons[{i}].point"] = le.get("point")
            out[f"lessons[{i}].excerpt"] = le.get("excerpt")
    act = entry.get("actionable") if isinstance(entry.get("actionable"), dict) else {}
    out["actionable.title"], out["actionable.detail"] = act.get("title"), act.get("detail")
    return {k: v for k, v in out.items() if isinstance(v, str)}


def _set(entry: dict, path: str, value: str) -> None:
    m = re.fullmatch(r"lessons\[(\d+)\]\.(\w+)", path)
    if m:
        entry["lessons"][int(m.group(1))][m.group(2)] = value
    elif path.startswith("actionable."):
        entry["actionable"][path.split(".", 1)[1]] = value
    else:
        entry[path] = value


def problems(draft: dict, final: dict) -> dict[str, list[str]]:
    """{field: reasons} for each field the rewrite must give back."""
    before, after = fields(draft), fields(final)
    out: dict[str, list[str]] = {}
    if len(draft.get("lessons") or []) != len(final.get("lessons") or []):
        out["lessons"] = ["lesson count changed"]  # all of them come back; check the rest
        before = {k: v for k, v in before.items() if not k.startswith("lessons[")}
    known = known_names(draft, final)
    for path, text in before.items():
        new = after.get(path)
        if new == text:
            continue
        excerpt = path.endswith(".excerpt")
        if new is None:
            why = ["field removed"]
        elif path == "title":
            why = title_changes(
                text, new, f"{before.get('takeaway', '')}\n{before.get('summary', '')}"
            )
        else:
            why = ["excerpt changed"] if excerpt else changes(text, new, known)
        if why:
            out[path] = why
    return out


def restore(entry: dict, draft: dict | None) -> dict[str, list[str]]:
    """Give back every field whose rewrite changed a fact; record what was reverted."""
    entry.pop("readability_rewrite", None)
    if draft is None:
        return {}
    found = problems(draft, entry)
    if "lessons" in found:
        entry["lessons"] = copy.deepcopy(draft.get("lessons"))
    for path in found:
        if path != "lessons":
            if path.startswith("actionable.") and not isinstance(entry.get("actionable"), dict):
                entry["actionable"] = {}
            _set(entry, path, fields(draft)[path])
    if found:
        entry["readability_rewrite"] = "reverted " + ", ".join(found)
    return found


# --- Drafts -----------------------------------------------------------------
def _unwrap(doc: object) -> list[dict]:
    rows = doc.get("entries", []) if isinstance(doc, dict) else doc
    return [e for e in rows or [] if isinstance(e, dict)] if isinstance(rows, list) else []


def load_drafts() -> dict[str, dict] | None:
    """Drafts by normalized source_url, or None when no draft file exists."""
    path = c.DATA_DIR / DRAFT
    if not path.exists():
        return None
    return {
        c.normalize_url(c.clean_source_url(d["source_url"])): d
        for d in _unwrap(c.load_json(path, default=[]))
        if d.get("source_url")
    }


def draft_for(drafts: dict[str, dict] | None, entry: dict) -> dict | None:
    url = entry.get("source_url") or ""
    return (drafts or {}).get(c.normalize_url(c.clean_source_url(url))) if url else None


def analyzed() -> list[dict]:
    return _unwrap(c.load_json(c.ANALYSIS_OUT, default=[]))


def missing_draft() -> bool:
    """True when there is an analysis but no pre-rewrite draft to check it against."""
    return bool(analyzed()) and not (c.DATA_DIR / DRAFT).exists()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--check-draft", action="store_true", help="warn if the draft is missing")
    args = ap.parse_args(argv)
    if args.check_draft and missing_draft():
        print(NOTE)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
