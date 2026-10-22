#!/usr/bin/env python3
"""
readability.py — A deterministic readability check for each brief's generated text.

Readers are senior security engineers who skim. A brief is the text WE wrote:
title, takeaway, summary, every lesson `point`, and the action
(`actionable.title` + `actionable.detail`). Lesson excerpts are verbatim quotes
from the source and are never scored (or rewritten): readability never trades
away grounding.

Checks (each a number compared with the `readability:` block of config.yaml;
above `warn` is a mild issue, above `hold` a severe one):

  sentence_words     the longest sentence or clause, in words (`;` ends a clause)
  grade              Flesch-Kincaid grade of the brief's prose (pure-Python syllables)
  long_word_ratio    share of words with 3+ syllables (per hyphen part)
  jargon_chain       longest run of content words with no function word or
                     punctuation between them ("agent framework checkpoint state")
  acronyms           distinct acronyms used without an expansion anywhere in the
                     brief ("SSRF (server-side request forgery)" or the reverse),
                     minus `allow_acronyms`
  hedges             most hedge words ("may", "could", "likely"...) in one sentence
  banned             filler/marketing phrases ("game-changer", "it's worth noting")
  title_words        words in the title
  takeaway_sentences sentences in the takeaway (it should be one)
  takeaway_words     words in the takeaway
  summary_sentences  sentences in the summary

A brief `passed` with no issues; `hold` is true when any check is severe, and
merge_analysis.py then holds the entry in REVIEW.md ("readability: ..."). Mild
issues are only reported. `score` is 100 minus a fixed cost per issue.

Usage:
    python scripts/readability.py --analysis   # the skill's check of data/analysis_out.json
    python scripts/readability.py              # distribution over pools + archive
    python scripts/readability.py --flagged 5  # ...plus the 5 worst briefs
    python scripts/readability.py --id <entry-id>
"""

from __future__ import annotations

import argparse
import re
import statistics
from pathlib import Path

import common as c

DEFAULTS: dict = {
    "thresholds": {},
    "allow_acronyms": [],
    "banned_phrases": [],
    "hedges": [],
    "mild_cost": 8,
    "severe_cost": 25,
    "eval_min_pass": 0.0,
}
FUNCTION_WORDS = frozenset("""
    a an the and or but nor so yet of in on at to for from by with without into onto
    over under via as than then that this these those it its is are was were be been
    being has have had do does did can will would should must may might could not no if
    when while where which who what how why each every any all one two their them they
    we you your our his her he she about after before between against through only also
    even just still more most less very such other both either neither same own up out
    off down there here gets get makes make lets let uses use runs run needs need says
    """.split())
SHOUTED = frozenset("never always before after only none must".split())  # emphasis, not acronyms
CODE = re.compile(r"`[^`]*`|https?://\S+")
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'’&]*(?:[-/][A-Za-z0-9'’&]+)*|\d[\d.,%x]*")
ACRONYM = re.compile(r"(?<![\w-])([A-Z][A-Z0-9&]*[A-Z][A-Z0-9&]*)s?(?![\w-]*[a-z])")
ABBREV = re.compile(r"\b(e\.g|i\.e|vs|etc|cf|approx|incl|U\.S|Fig|No)\.", re.I)
SENTENCE_END = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9`])")
CLAUSE_END = re.compile(r";\s+|\s+\([a-z0-9]\)\s+|\n+")
CHAIN_BREAK = re.compile(r"[,.;:!?()\[\]\"—–]|\s-\s")
VOWELS = re.compile(r"[aeiouy]+")


def settings(config: Path | str | None = None) -> dict:
    """The `readability:` block of config.yaml over DEFAULTS."""
    raw = c.load_yaml(Path(config or c.CONFIG_FILE)).get("readability") or {}
    return {**DEFAULTS, **raw}


# --- Text primitives ----------------------------------------------------------
def brief_fields(entry: dict) -> list[tuple[str, str]]:
    """(field, text) for every piece of generated text; excerpts excluded."""
    out = [(k, entry.get(k)) for k in ("title", "takeaway", "summary")]
    for i, le in enumerate(entry.get("lessons") or []):
        if isinstance(le, dict):
            out.append((f"lessons[{i}].point", le.get("point")))
    act = entry.get("actionable") if isinstance(entry.get("actionable"), dict) else {}
    out += [("actionable.title", act.get("title")), ("actionable.detail", act.get("detail"))]
    return [(k, str(v).strip()) for k, v in out if isinstance(v, str) and v.strip()]


def clean(text: str) -> str:
    """Text without code spans and URLs, and with abbreviation dots removed."""
    return ABBREV.sub(lambda m: m.group(1).replace(".", ""), CODE.sub(" x ", text))


def sentences(text: str) -> list[str]:
    parts = SENTENCE_END.split(clean(text).strip())
    return [p.strip() for p in parts if WORD.search(p)]


def clauses(text: str) -> list[str]:
    """Sentences, further split at `;`, numbered list markers and line breaks."""
    return [q.strip() for s in sentences(text) for q in CLAUSE_END.split(s) if WORD.search(q)]


def words(text: str) -> list[str]:
    return WORD.findall(clean(text))


def _part_syllables(part: str) -> int:
    p = part.lower().strip("'’")
    if not p.isalpha():
        return 1  # numbers, versions, mixed tokens read as one beat
    n = len(VOWELS.findall(p))
    if p.endswith("e") and not p.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    if p.endswith(("ed", "es")) and len(p) > 3 and p[-3] not in "aeioudt" and n > 1:
        n -= 1
    return max(1, n)


def syllables(word: str) -> int:
    return sum(_part_syllables(p) for p in re.split(r"[-/]", word) if p)


def is_long(word: str) -> bool:
    """3+ syllables in one hyphen part: 'side-channel' is two easy words."""
    return any(_part_syllables(p) >= 3 for p in re.split(r"[-/]", word) if p)


# --- Measures -----------------------------------------------------------------
def grade(text: str) -> float:
    """Flesch-Kincaid grade level: 0.39 words/sentence + 11.8 syllables/word - 15.59."""
    sents, ws = clauses(text), words(text)
    if not sents or not ws:
        return 0.0
    spw = sum(syllables(w) for w in ws) / len(ws)
    return round(0.39 * len(ws) / len(sents) + 11.8 * spw - 15.59, 1)


def long_word_ratio(text: str) -> float:
    ws = [w for w in words(text) if w.isalpha() or "-" in w]
    return round(sum(is_long(w) for w in ws) / len(ws), 3) if ws else 0.0


def jargon_chain(text: str, function_words: frozenset[str] = FUNCTION_WORDS) -> list[str]:
    """Longest run of lowercase content words with no function word, name or
    punctuation between them ("agent checkpoint state rehydration path")."""
    best: list[str] = []
    for chunk in CHAIN_BREAK.split(clean(text)):
        run: list[str] = []
        for w in WORD.findall(chunk):
            content = w[0].islower() and w.lower() not in function_words
            run = run + [w] if content else []
            best = run if len(run) > len(best) else best
    return best


def unexplained_acronyms(text: str, allow: set[str]) -> list[str]:
    """Distinct acronyms, in first-use order, with no expansion anywhere in `text`."""
    body = CODE.sub(" ", text)
    seen: list[str] = []
    for m in ACRONYM.finditer(body):
        a = m.group(1)
        if a in seen or a in allow or a.lower() in FUNCTION_WORDS | SHOUTED:
            continue
        expanded = re.search(rf"\(\s*{re.escape(a)}s?\s*\)|\b{re.escape(a)}s?\s*\(", body)
        if not expanded:
            seen.append(a)
    return seen


def max_hedges(text: str, hedges: set[str]) -> int:
    return max((sum(w.lower() in hedges for w in words(s)) for s in sentences(text)), default=0)


def banned_hits(text: str, phrases: list[str]) -> list[str]:
    low = text.lower()
    return [p for p in phrases if re.search(rf"(?<!\w){re.escape(p.lower())}(?!\w)", low)]


# --- The check ----------------------------------------------------------------
def measure(entry: dict, cfg: dict) -> tuple[dict, dict]:
    """(metrics, details) for one brief."""
    fields = dict(brief_fields(entry))
    prose = "\n".join(v for k, v in fields.items() if k != "title")
    every = "\n".join(fields.values())
    longest = (
        max((len(words(s)), s) for v in fields.values() for s in clauses(v)) if fields else (0, "")
    )
    chain = jargon_chain(prose)
    acr = unexplained_acronyms(every, set(cfg["allow_acronyms"]))
    banned = banned_hits(every, cfg["banned_phrases"])
    metrics = {
        "sentence_words": longest[0],
        "grade": grade(prose),
        "long_word_ratio": long_word_ratio(prose),
        "jargon_chain": len(chain),
        "acronyms": len(acr),
        "hedges": max_hedges(prose, {h.lower() for h in cfg["hedges"]}),
        "banned": len(banned),
        "title_words": len(words(fields.get("title", ""))),
        "takeaway_sentences": len(sentences(fields.get("takeaway", ""))),
        "takeaway_words": len(words(fields.get("takeaway", ""))),
        "summary_sentences": len(sentences(fields.get("summary", ""))),
    }  # fmt: skip
    details = {"sentence_words": longest[1][:120], "acronyms": ", ".join(acr),
               "jargon_chain": " ".join(chain)[:80],
               "banned": ", ".join(banned)}  # fmt: skip
    return metrics, details


def check(entry: dict, cfg: dict | None = None) -> dict:
    """The brief's readability record: score, passed, hold, issues, metrics."""
    cfg = cfg or settings()
    metrics, details = measure(entry, cfg)
    issues = []
    for name, value in metrics.items():
        limits = cfg["thresholds"].get(name) or {}
        level = (
            "severe" if value > limits.get("hold", float("inf"))
            else "mild" if value > limits.get("warn", float("inf")) else None
        )  # fmt: skip
        if level:
            note = f"{name} {value} > {limits['hold' if level == 'severe' else 'warn']}"
            extra = details.get(name)
            issues.append({"check": name, "level": level,
                           "detail": f"{note} ({extra})" if extra else note})  # fmt: skip
    severe = [i for i in issues if i["level"] == "severe"]
    cost = len(severe) * cfg["severe_cost"] + (len(issues) - len(severe)) * cfg["mild_cost"]
    return {
        "score": max(0, 100 - cost),
        "passed": not issues,
        "hold": bool(severe),
        "issues": issues,
        "metrics": metrics,
    }


def hold_reason(result: dict) -> str:
    """The REVIEW.md reason for a brief that fails badly."""
    severe = [i["detail"] for i in result["issues"] if i["level"] == "severe"]
    return "readability: " + "; ".join(severe)


def apply(entry: dict, cfg: dict | None = None) -> dict:
    """Merge's step: record the brief's readability on the entry; a severe
    failure holds it for review (`readability_hold`), a mild one is only noted."""
    result = check(entry, cfg)
    entry["readability"] = {
        "score": result["score"],
        "passed": result["passed"],
        "issues": [f"{i['level']}: {i['detail']}" for i in result["issues"]],
    }
    entry.pop("readability_hold", None)
    if result["hold"]:
        entry["needs_review"] = True
        entry["readability_hold"] = hold_reason(result)
    return entry


# --- The skill's rewrite check -----------------------------------------------
ENUMERATOR = re.compile(r"\(\d{1,2}\)|(?<![\w.])\d{1,2}[.)](?=\s)")  # "(1)" / "2." list markers
DRAFT = "_analysis_draft.json"  # the analysis before the readability rewrite
FACT = re.compile(r"`[^`]+`|\b(?:CVE|GHSA)-[\w-]+|\d[\d.,]*\s?(?:%|[kKMB]\b|x\b)?")


def facts(entry: dict) -> set[str]:
    """Numbers, CVE/GHSA ids and code spans in the brief: what a rewrite must keep."""
    text = ENUMERATOR.sub(" ", " ".join(v for _, v in brief_fields(entry)))
    return {m.group(0).strip().rstrip(".,") for m in FACT.finditer(text)} - {""}


def rewrite_problems(draft: dict, final: dict) -> list[str]:
    """What the readability rewrite changed that it must not: a dropped fact,
    or any excerpt (excerpts stay verbatim quotes)."""
    out = [f"dropped fact {f!r}" for f in sorted(facts(draft) - facts(final))]
    quotes = [[le.get("excerpt") for le in e.get("lessons") or [] if isinstance(le, dict)]
              for e in (draft, final)]  # fmt: skip
    if quotes[0] != quotes[1]:
        out.append("lesson excerpts changed")
    return out


def check_analysis(cfg: dict) -> list[str]:
    """One line per analyzed entry (OK / MILD / HOLD), plus rewrite problems
    against data/_analysis_draft.json when the skill saved one."""
    entries = c.load_json(c.ANALYSIS_OUT, default=[]) or []
    entries = entries.get("entries", []) if isinstance(entries, dict) else entries
    drafts = c.load_json(c.DATA_DIR / DRAFT, default=[]) or []
    by_url = {d.get("source_url"): d for d in drafts if isinstance(d, dict)}
    lines = []
    for e in entries:
        r = check(e, cfg)
        level = "HOLD" if r["hold"] else "OK" if r["passed"] else "MILD"
        lines.append(f"{level} [{r['score']}] {e.get('title', '')[:90]}")
        lines += [f"    {i['level']}: {i['detail']}" for i in r["issues"]]
        draft = by_url.get(e.get("source_url"))
        lines += [f"    REWRITE: {p}" for p in rewrite_problems(draft, e)] if draft else []
    return lines


# --- Calibration report -------------------------------------------------------
def corpus() -> list[dict]:
    """Every analyzed brief we hold: pools + archive, with a summary or lessons."""
    entries = c.all_pool_entries() + (c.load_json(c.ARCHIVE_FILE, default=[]) or [])
    return [e for e in entries if e.get("summary") or e.get("lessons")]


def _quantiles(values: list[float]) -> str:
    if len(values) < 2:
        return f"n={len(values)}"
    q = statistics.quantiles(values, n=20)
    return f"p50={q[9]:g} p75={q[14]:g} p90={q[17]:g} p95={q[18]:g} max={max(values):g}"


def report(entries: list[dict], cfg: dict, worst: int = 0) -> list[str]:
    results = [(e, check(e, cfg)) for e in entries]
    lines = [f"{len(results)} briefs"]
    for name in results[0][1]["metrics"] if results else []:
        lines.append(f"  {name:<19} {_quantiles([r['metrics'][name] for _, r in results])}")
    passed = sum(r["passed"] for _, r in results)
    held = sum(r["hold"] for _, r in results)
    lines.append(f"passed {passed}, mild only {len(results) - passed - held}, would hold {held}")
    for e, r in sorted(results, key=lambda x: x[1]["score"])[:worst]:
        lines.append(f"- [{r['score']}] {e.get('title', '')[:90]}")
        lines += [f"    {i['level']}: {i['detail']}" for i in r["issues"]]
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--flagged", type=int, default=0, help="also list the N worst briefs")
    ap.add_argument("--id", help="check one entry by id")
    ap.add_argument("--analysis", action="store_true", help=f"check {c.ANALYSIS_OUT.name}")
    args = ap.parse_args(argv)
    if args.analysis:
        print("\n".join(check_analysis(settings())) or f"no {c.ANALYSIS_OUT.name}")
        return 0
    cfg, entries = settings(), corpus()
    if args.id:
        entries = [e for e in entries if e.get("id") == args.id]
    print("\n".join(report(entries, cfg, args.flagged if not args.id else 1)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
