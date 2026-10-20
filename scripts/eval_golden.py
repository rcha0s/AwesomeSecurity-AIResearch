#!/usr/bin/env python3
"""
eval_golden.py — Score an analyzer run against checked answers (ISA ISC-23).

data/evals/golden.json holds ~30 past stories with checked answers: keep or
drop (curated vs held, with the reason), whether the story is on-thesis at all,
the correct taxonomy domain ID, and 1-3 key facts a correct analysis states.

`score` compares an analyzer output file (the shape of data/analysis_out.json)
with those answers. It is deterministic; only producing the file needs an LLM.

  keep/drop    the analyzer keeps a story when merge would not hold it: lesson
               confidence >= confidence_min, novelty/relevance at the curation
               bar, not refuted by its verifier, and a valid domain ID. A staged
               case missing from the output counts as dropped (shortlist skip).
  domain       the output's domain is the answer (or one in `also_accept`)
  facts        a fact is covered when any of its `any` phrases appears in the
               output's title, summary, takeaway or lessons (case-insensitive)
  off-topic    share of the analyzer's kept cases that the answers mark off-topic

A case passes when keep/drop is right and, for a keep, the domain is right and
at least `evals.golden.min_fact_coverage` of its facts are covered. The run
passes when the pass rate >= `evals.thresholds.golden_min` and the off-topic
rate <= `evals.thresholds.off_topic_max`.

The weekly analyzer run (scripts/run_golden_local.sh) stages a rotating slice
of cases as candidates in a throwaway worktree, hides their own entries from
the pools there so novelty is judged fresh, and runs research-scan steps 2-5
under the scan's containment. When a real run gets a story wrong that the set
doesn't cover, add a case: copy the story's entry into `cases` with the checked
answer and a `reason`, and run `eval_golden.py check`.

Usage:
    python scripts/eval_golden.py score data/analysis_out.json [--manifest M] [--write]
    python scripts/eval_golden.py stage --out data/candidates.json --scratch [--limit N --offset K]
    python scripts/eval_golden.py check          # the answer file itself is well-formed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import common as c
import dedupe_stories as ds
import eval_lib as el
import merge_analysis as ma
import taxonomy as tx

GOLDEN_FILE = "golden.json"
MANIFEST = "_golden_manifest.json"  # beside the staged candidates; gitignored
CANDIDATE_FIELDS = ("source_name", "source_id", "source_rank", "source_topics", "author", "date")


def golden_path() -> Path:
    return el.evals_dir() / GOLDEN_FILE


def load_cases(path: Path | None = None) -> list[dict]:
    return (c.load_json(path or golden_path(), default={}) or {}).get("cases") or []


# --- Matching an output entry to a case ---------------------------------------
def _urls(entry: dict) -> set[str]:
    keys = ("url", "source_url", "article_url")
    return {ds.canonical_url(entry[k]) for k in keys if entry.get(k)}


def find_output(case: dict, outputs: list[dict]) -> dict | None:
    """The analyzer entry for a case: same canonical URL, else a near-identical title."""
    want = _urls(case)
    for out in outputs:
        if want & _urls(out):
            return out
    return next((o for o in outputs if c.title_similar(o.get("title", ""), case["title"])), None)


# --- Per-case scoring ---------------------------------------------------------
def predicted_keep(out: dict | None, conf: c.Config, tax: tx.Taxonomy) -> bool:
    """Would merge_analysis put this output in the curated view (before grounding)?"""
    if out is None:
        return False
    return not (
        ma.entry_confidence(out) < conf.confidence_min
        or ma.below_curation_bar(out, conf)
        or out.get("verified") is False
        or not tax.is_valid(out.get("domain"), out.get("topic"))
    )


def output_text(out: dict) -> str:
    parts = [out.get(k) or "" for k in ("title", "summary", "takeaway")]
    for le in out.get("lessons") or []:
        if isinstance(le, dict):
            parts += [le.get("point") or "", le.get("excerpt") or ""]
    return c.normalize_text(" ".join(str(p) for p in parts))


def fact_coverage(case: dict, out: dict | None) -> tuple[float, list[str]]:
    """(share of facts covered, the facts missed)."""
    facts = case.get("facts") or []
    if not facts:
        return 1.0, []
    text = output_text(out) if out else ""
    missed = [
        f["fact"] for f in facts if not any(c.normalize_text(p) in text for p in f.get("any", []))
    ]
    return round(1 - len(missed) / len(facts), 3), missed


def score_case(
    case: dict, out: dict | None, conf: c.Config, tax: tx.Taxonomy, min_cov: float
) -> dict:
    keep = predicted_keep(out, conf, tax)
    domains = {case["domain"], *case.get("also_accept", [])}
    domain_ok = out is not None and out.get("domain") in domains
    coverage, missed = fact_coverage(case, out)
    passed = keep == case["keep"] and (not case["keep"] or (domain_ok and coverage >= min_cov))
    why = []
    if keep != case["keep"]:
        why.append(
            f"{'kept' if keep else 'dropped'}, answer is {'keep' if case['keep'] else 'drop'}"
        )
    if case["keep"] and not domain_ok:
        why.append(f"domain {out.get('domain') if out else None!r}, answer {case['domain']}")
    if case["keep"] and coverage < min_cov:
        why.append(f"facts missed: {'; '.join(missed)}")
    return {
        "id": case["id"],
        "passed": passed,
        "expected_keep": case["keep"],
        "predicted_keep": keep,
        "emitted": out is not None,
        "domain_ok": domain_ok,
        "fact_coverage": coverage,
        "on_topic": case.get("on_topic", True),
        "why": "; ".join(why),
    }


def _ratio(num: int | float, den: int) -> float:
    return round(num / den, 3) if den else 0.0


def score(cases: list[dict], outputs: list[dict], config: Path | None = None) -> dict:
    conf, tax, cfg = c.load_config(config or c.CONFIG_FILE), tx.get(), el.settings(config)
    min_cov = float(cfg["golden"]["min_fact_coverage"])
    rows = [score_case(k, find_output(k, outputs), conf, tax, min_cov) for k in cases]
    kept = [r for r in rows if r["predicted_keep"]]
    emitted = [r for r in rows if r["emitted"]]
    keeps = [r for r in rows if r["expected_keep"] and r["emitted"]]
    result = {
        "cases": len(rows),
        "score": _ratio(sum(r["passed"] for r in rows), len(rows)),
        "keep_drop_accuracy": _ratio(sum(r["predicted_keep"] == r["expected_keep"] for r in rows), len(rows)),
        "domain_accuracy": _ratio(sum(r["domain_ok"] for r in emitted), len(emitted)),
        "fact_coverage": _ratio(sum(r["fact_coverage"] for r in keeps), len(keeps)),
        "off_topic_rate": _ratio(sum(not r["on_topic"] for r in kept), len(kept)),
        "results": rows,
    }  # fmt: skip
    limits = cfg["thresholds"]
    result["passed"] = bool(rows) and (
        result["score"] >= float(limits["golden_min"])
        and result["off_topic_rate"] <= float(limits["off_topic_max"])
    )
    return result


# --- Staging a weekly analyzer run --------------------------------------------
def select(cases: list[dict], limit: int | None, offset: int) -> list[dict]:
    """`limit` cases starting at `offset`, wrapping around the set."""
    if not cases or limit is None or limit >= len(cases):
        return list(cases)
    start = offset % len(cases)
    return [cases[(start + i) % len(cases)] for i in range(limit)]


def find_entry(case: dict) -> dict | None:
    for e in c.all_pool_entries() + (c.load_json(c.ARCHIVE_FILE, default=[]) or []):
        if e.get("id") == case["id"]:
            return e
    return None


def to_candidate(case: dict, entry: dict | None) -> dict:
    """A candidate carrying only what ingest would know: never the checked answer
    or our earlier analysis (summary, scores, lessons, domain)."""
    entry = entry or {}
    cand = {
        "id": case["id"],
        "discovered_via": "manual",
        "title": case["title"],
        "source_url": entry.get("source_url") or case["url"],
        "article_url": case["url"],
        "tweet_url": None,
        "published": entry.get("published"),
        "excerpt": "",
        "raw_path": None,
        "retrieved_at": c.utcnow_iso(),
    }
    return {**cand, **{k: entry.get(k) for k in CANDIDATE_FIELDS if entry.get(k) is not None}}


def needles_for(cases: list[dict]) -> set[str]:
    """Lowercased strings that name a case: its title and its scheme-less canonical URL."""
    out = {k["title"].lower() for k in cases}
    return out | {ds.canonical_url(k["url"]).split("://", 1)[-1].lower() for k in cases}


def _mentions(value: object, needles: set[str]) -> bool:
    text = json.dumps(value, ensure_ascii=False).lower()
    return any(n in text for n in needles)


def forget(entries: list[dict], ids: set[str], needles: set[str]) -> tuple[list[dict], int]:
    """Drop the cases' entries (and any other entry whose title or URL is one of
    them), and delete fields of the rest that mention a case, e.g. a `prior_art`
    naming it. Returns (kept entries, entries dropped)."""
    kept = []
    for e in entries:
        same = {k: e.get(k) for k in ("title", "source_url", "article_url", "tweet_url")}
        if e.get("id") in ids or _mentions(same, needles):
            continue
        kept.append({k: v for k, v in e.items() if not _mentions(v, needles)})
    return kept, len(entries) - len(kept)


def hide_cases(ids: set[str], needles: set[str] = frozenset()) -> int:
    """Remove the staged cases from this tree's pools and archive, so the analyzer
    judges novelty without seeing its earlier answer. Scratch trees only."""
    removed = 0
    for topic in c.TOPICS:
        pool = c.load_pool(topic)
        keep, gone = forget(pool["entries"], ids, set(needles))
        removed += gone
        c.save_pool(topic, {**pool, "entries": keep})
    archive, gone = forget(c.load_json(c.ARCHIVE_FILE, default=[]) or [], ids, set(needles))
    c.save_json(c.ARCHIVE_FILE, archive)
    return removed + gone


# What a scratch tree must lose before the golden session sees it: every place
# a hidden case's old analysis, title or verdict is rendered or indexed. Pools,
# archive and claims are kept (novelty and related_claims need them) but have
# the hidden cases cut out.
SCRUB_PATHS = (
    "README.md", "NEWSLETTER.md", "TRENDS.md", "REVIEW.md",
    "ai-security", "product-security", "ai-research", "claims", "docs",
    "data/evals", "data/news_stories.json", "data/story_shortlist.json",
    "data/story_verdicts.json", "data/trends.json", "data/backlog.md",
    "data/candidates.backlog.json", "data/taxonomy_migration.json",
    "data/taxonomy_proposals.json",
)  # fmt: skip
SCRUB_GLOBS = ("data/discovery-*.md",)
# Where the staged cases legitimately appear: what the session is asked to analyze.
TRACE_ALLOWED = ("data/candidates.json", "data/_scan_urls.json", "data/_raw/")
TRACE_SKIP_DIRS = (".git", ".venv", "__pycache__", "node_modules")


def _remove(path: Path) -> bool:
    if path.is_dir():
        import shutil

        shutil.rmtree(path)
        return True
    if path.exists():
        path.unlink()
        return True
    return False


def strip_claim_evidence(cases: list[dict]) -> int:
    """Drop claim evidence citing a hidden case (by canonical URL or title)."""
    urls = {ds.canonical_url(k["url"]) for k in cases}
    titles = {k["title"].lower() for k in cases}
    path = c.DATA_DIR / "claims.json"
    ledger = c.load_json(path, default=None)
    if not isinstance(ledger, dict):
        return 0
    cut = 0
    for claim in ledger.get("claims") or []:
        kept = [
            ev for ev in claim.get("evidence") or []
            if ds.canonical_url(ev.get("url") or "") not in urls
            and (ev.get("title") or "").lower() not in titles
        ]  # fmt: skip
        cut += len(claim.get("evidence") or []) - len(kept)
        claim["evidence"] = kept
    c.save_json(path, ledger)
    return cut


def traces(cases: list[dict], root: Path | None = None) -> list[str]:
    """Files under the tree (outside TRACE_ALLOWED) that still name a hidden case
    by title or URL. [] = the session can't read its old answer."""
    root = root or c.ROOT
    needles = needles_for(cases)
    found = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if not path.is_file() or any(part in TRACE_SKIP_DIRS for part in path.parts):
            continue
        if rel.startswith(TRACE_ALLOWED):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        found += [f"{rel}: {n[:60]}" for n in needles if n in text]
    return found


def scrub_tree(cases: list[dict]) -> dict:
    """Make a scratch tree forget the staged cases (see SCRUB_PATHS)."""
    hidden = hide_cases({k["id"] for k in cases}, needles_for(cases))
    removed = [p for p in SCRUB_PATHS if _remove(c.ROOT / p)]
    for pattern in SCRUB_GLOBS:
        removed += [p.relative_to(c.ROOT).as_posix() for p in c.ROOT.glob(pattern) if _remove(p)]
    return {"hidden": hidden, "removed": removed, "evidence_cut": strip_claim_evidence(cases)}


def stage(out: Path, limit: int | None, offset: int, manifest: Path | None = None) -> dict:
    """Stage a slice of cases as candidates and scrub the tree of their answers.
    The manifest (the staged ids) goes to `manifest`, outside the tree."""
    chosen = select(load_cases(), limit, offset)
    cands = [to_candidate(k, find_entry(k)) for k in chosen]
    manifest = manifest or out.parent / MANIFEST
    c.save_json(manifest, {"generated": c.utcnow_iso(), "ids": [k["id"] for k in chosen]})
    report = scrub_tree(chosen)
    c.save_json(out, cands)
    left = traces(chosen)
    return {"staged": len(cands), **report, "manifest": str(manifest), "traces": left}


# --- The answer file itself ---------------------------------------------------
def check_cases(cases: list[dict], tax: tx.Taxonomy, known_ids: set[str]) -> list[str]:
    out, seen = [], set()
    for k in cases:
        cid = k.get("id")
        if cid in seen:
            out.append(f"{cid}: duplicate case")
        seen.add(cid)
        if cid not in known_ids:
            out.append(f"{cid}: not in any pool or the archive")
        for did in [k.get("domain"), *k.get("also_accept", [])]:
            if not tax.is_valid(did):
                out.append(f"{cid}: {did!r} is not a taxonomy ID")
        if not isinstance(k.get("keep"), bool) or not k.get("reason"):
            out.append(f"{cid}: needs a boolean keep and a reason")
        facts = k.get("facts") or []
        if k.get("keep") and not 1 <= len(facts) <= 3:
            out.append(f"{cid}: a keep case needs 1-3 facts")
        if any(not f.get("fact") or not f.get("any") for f in facts):
            out.append(f"{cid}: every fact needs text and `any` phrases")
    return out


# --- CLI ----------------------------------------------------------------------
def _outputs(path: Path) -> list[dict]:
    data = c.load_json(path, default=[]) or []
    return data if isinstance(data, list) else data.get("entries", [])


def cmd_score(args) -> int:
    cases = load_cases(Path(args.golden) if args.golden else None)
    if args.manifest:
        ids = set((c.load_json(Path(args.manifest), default={}) or {}).get("ids") or [])
        cases = [k for k in cases if k["id"] in ids]
    result = score(cases, _outputs(Path(args.analysis)))
    for r in result["results"]:
        print(
            f"{'PASS' if r['passed'] else 'FAIL'} {r['id']}" + (f": {r['why']}" if r["why"] else "")
        )
    if args.write:
        result["generated"] = c.utcnow_iso()
        out = el.evals_dir() / f"golden-{c.utcnow():%Y-%m-%d}.json"
        c.save_json(out, result)
        print(f"wrote {out.relative_to(c.ROOT)}")
    fields = {k: result[k] for k in ("score", "cases", "keep_drop_accuracy", "domain_accuracy",
                                     "fact_coverage", "off_topic_rate")}  # fmt: skip
    print(el.summary_line("golden", result["passed"], **fields))
    return 0 if result["passed"] else 1


def cmd_stage(args) -> int:
    if not args.scratch:
        print(
            "stage rewrites this tree's pools; pass --scratch in a throwaway worktree",
            file=sys.stderr,
        )
        return 2
    manifest = Path(args.manifest) if args.manifest else None
    report = stage(Path(args.out), args.limit, args.offset, manifest)
    print(json.dumps(report))
    if report["traces"]:
        print("stage: the tree still names a staged case; refusing to analyze", file=sys.stderr)
        return 3
    return 0


def cmd_check(_args) -> int:
    known = {e.get("id") for e in c.all_pool_entries()}
    known |= {e.get("id") for e in c.load_json(c.ARCHIVE_FILE, default=[]) or []}
    cases = load_cases()
    problems = check_cases(cases, tx.get(), known)
    for p in problems:
        print(f"PROBLEM {p}")
    print(el.summary_line("golden-set", not problems, cases=len(cases), problems=len(problems)))
    return 0 if problems == [] and cases else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("score", help="score an analyzer output file")
    sc.add_argument("analysis")
    sc.add_argument("--manifest", help="score only the cases a stage run listed")
    sc.add_argument("--golden", help="the answer file (stage deletes data/evals/)")
    sc.add_argument("--write", action="store_true", help="save data/evals/golden-<date>.json")
    st = sub.add_parser("stage", help="stage golden cases as candidates (scratch trees only)")
    st.add_argument("--out", default=str(c.CANDIDATES_FILE))
    st.add_argument("--limit", type=int, default=None)
    st.add_argument("--offset", type=int, default=0)
    st.add_argument("--scratch", action="store_true", help="confirm this tree is disposable")
    st.add_argument("--manifest", help="where to write the staged ids (keep it outside the tree)")
    sub.add_parser("check", help="validate data/evals/golden.json")
    args = ap.parse_args(argv)
    return {"score": cmd_score, "stage": cmd_stage, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
