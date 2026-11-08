#!/usr/bin/env python3
"""
rebuild_pr.py — resolve a scan PR that conflicts with main, by code (2026-11-07).

Two scan PRs opened on different days both rewrite the pools, the ledgers and the
rendered site, so once one merges the other conflicts on every generated file and
sits open until someone merges main into it by hand (#165, 11-04). This does that
merge deterministically:

  - every data/*.json the PR changed is merged three ways (merge base, main, PR
    head) record by record: the PR's new records are added, a field only one side
    changed takes that side, a field both sides changed keeps main's value (counts
    in data/source_stats.json add both sides' increments instead), and a record one
    side deleted while the other changed it is kept as changed;
  - a pool entry the PR added for a source_url main also added is dropped (main's
    copy stays), as merge_analysis would have deduped it;
  - the claim ledger is re-validated with claims.py; a merge it rejects is refused;
  - rendered files git could not merge start from main's copy, and main's renderers
    then redraw the site from the merged data; anything still unmerged, or carrying
    a conflict marker, refuses the rebuild.

It runs in the automerge workflow's `rebuild` job, in a checkout of the PR head
where `git merge --no-commit <main>` has just stopped on conflicts. The job turns
the resolved tree into a new commit on main and opens it as a replacement PR,
which the next gate run judges like any other (path guard + merge_gate.py). So this
decides nothing about what may merge: a bad rebuild is refused by the gate.

It never runs rerank.py (that prunes on the wall clock); pools are re-sorted with
rerank's sort key only. It reads git objects and JSON; it executes nothing from the PR.

Usage: rebuild_pr.py --base <merge-base sha> --ours <main sha> --theirs <PR head sha>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MISSING = object()
KEYS = ("id", "run_id", "url", "source_url")
ADDITIVE = {"data/source_stats.json"}
POOLS = ("data/ai-security.json", "data/product-security.json", "data/ai-research.json")
RENDERERS = ("generate_site", "generate_claims", "generate_html", "trends",
             "generate_newsletter", "generate_review")  # fmt: skip
RENDERED = ("README.md", "NEWSLETTER.md", "TRENDS.md", "REVIEW.md", "ai-security",
            "product-security", "ai-research", "claims", "docs")  # fmt: skip
MARKER = re.compile(r"^(<<<<<<<|>>>>>>>)( |$)", re.M)


class RebuildError(RuntimeError):
    pass


# ---------------------------------------------------------------- three-way merge (pure)


def _scalar(b: object, o: object, t: object, additive: bool) -> object:
    """Both sides changed one value: main wins, except additive integer counts."""
    if additive and all(isinstance(v, int) and not isinstance(v, bool) for v in (b, o, t)):
        return o + (t - b)  # type: ignore[operator]
    return o


def _unique(lst: list, key: str) -> bool:
    values = [x[key] for x in lst]
    return all(isinstance(v, (str, int)) for v in values) and len(set(values)) == len(values)


def _list_key(*lists: list) -> str | None:
    """A field that names every record exactly once in each of the three lists.
    A repeated value (claim evidence citing one URL twice) means no key: by value."""
    items = [x for lst in lists for x in lst]
    if not items or not all(isinstance(x, dict) for x in items):
        return None
    return next(
        (k for k in KEYS if all(k in x for x in items) and all(_unique(lst, k) for lst in lists)),
        None,
    )


def _merge_keyed(b: list, o: list, t: list, key: str, additive: bool) -> list:
    """Main's order, then the PR's new records in the PR's order."""
    bi, oi, ti = ({x[key]: x for x in lst} for lst in (b, o, t))
    order = [x[key] for x in o] + [x[key] for x in t if x[key] not in oi]
    out = []
    for k in order:
        v = merge3(bi.get(k, MISSING), oi.get(k, MISSING), ti.get(k, MISSING), additive)
        if v is not MISSING:
            out.append(v)
    return out


def _merge_list(b: list, o: list, t: list, additive: bool) -> list:
    key = _list_key(b, o, t)
    if key:
        return _merge_keyed(b, o, t, key, additive)
    # Unkeyed (evidence items, tags, covering sources): main's items minus what the
    # PR removed, plus what the PR added. Equality is by value.
    dropped = [x for x in b if x not in t]
    kept = [x for x in o if x not in dropped]
    return kept + [x for x in t if x not in b and x not in kept]


def _merge_dict(b: dict, o: dict, t: dict, additive: bool) -> dict:
    out = {}
    for k in list(o) + [k for k in t if k not in o]:
        v = merge3(b.get(k, MISSING), o.get(k, MISSING), t.get(k, MISSING), additive)
        if v is not MISSING:
            out[k] = v
    return out


def merge3(b: object, o: object, t: object, additive: bool = False) -> object:
    """Three-way merge of JSON values. MISSING marks an absent key or record."""
    if t == b or o == t:
        return o
    if o == b:
        return t
    # One side deleted what the other changed: keep the change. Deleting a pool
    # entry is archiving it, and dropping main's promoted copy would read as an
    # editorial demotion to the gate.
    if o is MISSING:
        return t
    if t is MISSING:
        return o
    if b is MISSING:
        b = type(o)() if isinstance(o, (dict, list)) and type(o) is type(t) else None
    if isinstance(o, dict) and isinstance(t, dict) and isinstance(b, dict):
        return _merge_dict(b, o, t, additive)
    if isinstance(o, list) and isinstance(t, list) and isinstance(b, list):
        return _merge_list(b, o, t, additive)
    return _scalar(b, o, t, additive)


def dedupe_archive(pools: dict[str, dict], archive: list) -> list:
    """An entry the merge left both in a pool and in the archive stays in the pool."""
    shown = {e.get("id") for p in pools.values() for e in p.get("entries", [])}
    return [e for e in archive if not (isinstance(e, dict) and e.get("id") in shown)]


def _entries(pool: object) -> list:
    return pool.get("entries", []) if isinstance(pool, dict) else []


def dedupe_new_urls(pool: dict, base: object, ours: object) -> None:
    """Drop a PR-added entry whose source_url an entry main added already has: both
    runs analyzed the same story, and main's copy is the one already published."""
    old = {e.get("id") for e in _entries(base)}
    mains = {e.get("source_url") for e in _entries(ours) if e.get("id") not in old} - {None, ""}
    mine = {e.get("id") for e in _entries(ours)}
    pool["entries"] = [
        e
        for e in pool["entries"]
        if e.get("id") in mine or e.get("id") in old or e.get("source_url") not in mains
    ]


# ---------------------------------------------------------------- git + files


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return out.stdout.decode("utf-8")


def blob(sha: str, path: str) -> object:
    """The JSON at `path` in commit `sha`, or MISSING when the file isn't there."""
    try:
        return json.loads(git("show", f"{sha}:{path}"))
    except subprocess.CalledProcessError:
        return MISSING


def changed_data(base: str, theirs: str) -> list[str]:
    names = git("diff", "--name-only", "--no-renames", base, theirs, "--", "data").splitlines()
    return sorted(n for n in names if n.endswith(".json"))


def write_json(path: str, value: object) -> None:
    target = ROOT / path
    if value is MISSING:
        target.unlink(missing_ok=True)
        return
    if path == "data/news_stories.json" and isinstance(value, dict):
        import story_ledger  # its one-story-per-line format keeps story diffs to a line

        story_ledger.save_ledger(value, target)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_data(base: str, ours: str, theirs: str) -> dict[str, object]:
    merged = {}
    for path in changed_data(base, theirs):
        b, o, t = (blob(s, path) for s in (base, ours, theirs))
        merged[path] = merge3(b, o, t, additive=path in ADDITIVE)
    return merged


def finish_pools(merged: dict[str, object], base: str, ours: str) -> None:
    """Dedupe new same-story entries, re-sort each pool, and dedupe the archive."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import rerank  # imported for its sort key only; rerank.main never runs

    for path in POOLS:
        pool = merged.get(path)
        if isinstance(pool, dict) and isinstance(pool.get("entries"), list):
            dedupe_new_urls(pool, blob(base, path), blob(ours, path))
            pool["entries"] = sorted(pool["entries"], key=rerank.sort_key)
    archive = merged.get("data/archive.json")
    if isinstance(archive, list):
        pools = {p: merged.get(p, blob(ours, p)) for p in POOLS}
        pools = {p: v for p, v in pools.items() if isinstance(v, dict)}
        merged["data/archive.json"] = dedupe_archive(pools, archive)


def check_claims(merged: dict[str, object]) -> None:
    ledger = merged.get("data/claims.json")
    if ledger is None or ledger is MISSING:
        return
    import claims

    errors = claims.validate_ledger(ledger)  # type: ignore[arg-type]
    if errors:
        raise RebuildError(f"merged claim ledger is invalid: {errors[0]}")


def unmerged(*paths: str) -> list[str]:
    return sorted(set(git("diff", "--name-only", "--diff-filter=U", "--", *paths).split()))


def reset_conflicted_rendered(ours: str) -> None:
    """A rendered file git could not merge starts from main's copy; the renderers
    then redraw it. Files only one side changed (a digest-day docs/digest.md) keep
    git's clean merge."""
    paths = unmerged(*RENDERED)
    if paths:
        git("checkout", ours, "--", *paths)


def render(python: str) -> None:
    for name in RENDERERS:
        subprocess.run([python, f"scripts/{name}.py"], cwd=ROOT, check=True)


def check_clean() -> None:
    """Nothing may stay unmerged, and no tracked text file may carry a marker."""
    left = unmerged(".")
    if left:
        raise RebuildError(f"unresolved paths remain: {', '.join(left[:10])}")
    for path in git("diff", "--cached", "--name-only", "--diff-filter=AM").splitlines():
        file = ROOT / path
        if file.is_file() and MARKER.search(file.read_text(encoding="utf-8", errors="ignore")):
            raise RebuildError(f"conflict marker left in {path}")


def rebuild(base: str, ours: str, theirs: str, python: str, do_render: bool = True) -> list[str]:
    merged = resolve_data(base, ours, theirs)
    finish_pools(merged, base, ours)
    check_claims(merged)
    for path, value in merged.items():
        write_json(path, value)
    if merged:
        git("add", "-A", "--", *merged)
    if do_render:
        reset_conflicted_rendered(ours)
        render(python)
        # trends.py rewrites data/trends.json after the data was staged above.
        drawn = [*RENDERED, "data/trends.json"]
        git("add", "-A", "--", *(p for p in drawn if (ROOT / p).exists()))
    check_clean()
    return sorted(merged)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    for flag in ("--base", "--ours", "--theirs"):
        ap.add_argument(flag, required=True)
    ap.add_argument("--no-render", action="store_true", help="data only (tests)")
    a = ap.parse_args(argv)
    try:
        paths = rebuild(a.base, a.ours, a.theirs, sys.executable, not a.no_render)
    except (RebuildError, subprocess.CalledProcessError, ValueError, TypeError) as e:
        print(f"rebuild refused: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    print(f"rebuilt {len(paths)} data file(s): {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
