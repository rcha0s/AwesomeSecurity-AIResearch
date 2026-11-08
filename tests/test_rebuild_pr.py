"""rebuild_pr.py: the three-way data merge that resolves a scan PR conflicting with main."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import rebuild_pr as rb

M = rb.MISSING


def test_one_sided_changes_take_that_side():
    assert rb.merge3(1, 1, 2) == 2
    assert rb.merge3(1, 3, 1) == 3
    assert rb.merge3(1, 3, 3) == 3


def test_both_changed_scalar_keeps_main():
    assert rb.merge3("a", "main", "pr") == "main"


def test_additive_counts_add_both_increments():
    b, o, t = {"s": {"ingested": 5}}, {"s": {"ingested": 8}}, {"s": {"ingested": 7}}
    assert rb.merge3(b, o, t, additive=True) == {"s": {"ingested": 10}}
    assert rb.merge3(b, o, t) == {"s": {"ingested": 8}}  # not additive: main wins


def test_keyed_records_add_the_prs_new_ones_after_mains():
    b = [{"id": "a", "v": 1}]
    o = [{"id": "a", "v": 1}, {"id": "m", "v": 1}]
    t = [{"id": "a", "v": 1}, {"id": "p", "v": 1}]
    assert [x["id"] for x in rb.merge3(b, o, t)] == ["a", "m", "p"]


def test_keyed_records_merge_field_by_field():
    b = [{"id": "a", "score": 1, "title": "x"}]
    o = [{"id": "a", "score": 2, "title": "x"}]
    t = [{"id": "a", "score": 3, "title": "y"}]
    assert rb.merge3(b, o, t) == [{"id": "a", "score": 2, "title": "y"}]


def test_a_record_the_pr_deleted_goes_and_mains_change_stays():
    b = [{"id": "a", "v": 1}, {"id": "b", "v": 1}]
    o = [{"id": "a", "v": 1}, {"id": "b", "v": 2}]  # main changed b
    t = [{"id": "b", "v": 1}]  # the PR archived a, which main left alone
    assert rb.merge3(b, o, t) == [{"id": "b", "v": 2}]


def test_a_change_beats_a_deletion_on_either_side():
    """Opus on #169: the PR archiving an entry main promoted must not drop main's
    promoted copy, or the gate reads it as an editorial demotion."""
    assert rb.merge3({"k": 1}, M, {"k": 2}) == {"k": 2}
    assert rb.merge3({"k": 1}, {"k": 2, "promoted": True}, M) == {"k": 2, "promoted": True}


def test_a_repeated_url_is_not_a_key():
    """7 real claims cite one URL several times with different notes; keying by url
    collapsed them and destroyed an item."""
    a1 = {"url": "https://u", "note": "one"}
    a2 = {"url": "https://u", "note": "two"}
    x, y = {"url": "https://x"}, {"url": "https://y"}
    assert rb.merge3([a1, a2], [a1, a2, x], [a1, a2, y]) == [a1, a2, x, y]


def test_a_pr_entry_for_a_story_main_already_added_is_dropped():
    base = {"entries": [{"id": "old", "source_url": "https://s"}]}
    ours = {"entries": base["entries"] + [{"id": "m1", "source_url": "https://n"}]}
    pool = {"entries": ours["entries"] + [{"id": "p1", "source_url": "https://n"},
                                          {"id": "p2", "source_url": "https://s"},
                                          {"id": "p3", "source_url": "https://z"}]}  # fmt: skip
    rb.dedupe_new_urls(pool, base, ours)
    # p2 shares a URL only with an old entry (two findings from one page are allowed).
    assert [e["id"] for e in pool["entries"]] == ["old", "m1", "p2", "p3"]


def test_history_rows_keep_mains_prefix_then_the_prs_row():
    b = {"runs": [{"run_id": "r1"}]}
    o = {"runs": [{"run_id": "r1"}, {"run_id": "r2"}]}
    t = {"runs": [{"run_id": "r1"}, {"run_id": "r3"}]}
    assert [r["run_id"] for r in rb.merge3(b, o, t)["runs"]] == ["r1", "r2", "r3"]


def test_unkeyed_lists_union_and_honour_removals():
    b, o, t = ["x", "y"], ["x", "y", "m"], ["y", "p"]
    assert rb.merge3(b, o, t) == ["y", "m", "p"]


def test_claim_evidence_is_appended_not_duplicated():
    ev = {"stance": "supports", "url": "https://a"}
    new = {"stance": "supports", "url": "https://b"}
    b = {"claims": [{"id": "c", "evidence": [ev]}]}
    o = {"claims": [{"id": "c", "evidence": [ev]}]}
    t = {"claims": [{"id": "c", "evidence": [ev, new]}, {"id": "d", "evidence": [new]}]}
    out = rb.merge3(b, o, t)
    assert out["claims"][0]["evidence"] == [ev, new]
    assert [c["id"] for c in out["claims"]] == ["c", "d"]


def test_both_sides_add_the_same_key_differently():
    assert rb.merge3(M, {"a": 1, "b": 1}, {"a": 2, "c": 3}) == {"a": 1, "b": 1, "c": 3}


def test_dedupe_archive_keeps_the_pool_copy():
    pools = {"p": {"entries": [{"id": "x"}]}}
    assert rb.dedupe_archive(pools, [{"id": "x"}, {"id": "y"}]) == [{"id": "y"}]


# ---------------------------------------------------------------- on a real repo


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return out.stdout.strip()


def _commit(root: Path, files: dict[str, object], msg: str) -> str:
    for path, value in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(json.dumps(value, indent=2) + "\n")
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@i", "commit", "-qm", msg)
    return _git(root, "rev-parse", "HEAD")


def test_rebuild_resolves_a_real_conflict(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q", "-b", "main")
    pool = {"topic": "ai-security", "entries": [{"id": "a", "scores": {"composite": 1}}]}
    base = _commit(tmp_path, {"data/ai-security.json": pool}, "base")
    main_pool = {**pool, "entries": pool["entries"] + [{"id": "m", "scores": {"composite": 5}}]}
    ours = _commit(tmp_path, {"data/ai-security.json": main_pool}, "main")
    _git(tmp_path, "checkout", "-q", "-b", "pr", base)
    pr_pool = {**pool, "entries": pool["entries"] + [{"id": "p", "scores": {"composite": 3}}]}
    theirs = _commit(tmp_path, {"data/ai-security.json": pr_pool}, "pr")
    merge = ["-c", "user.name=t", "-c", "user.email=t@i", "merge", "--no-ff", "--no-commit", ours]
    assert subprocess.run(["git", *merge], cwd=tmp_path, capture_output=True).returncode != 0
    monkeypatch.setattr(rb, "ROOT", tmp_path)
    assert rb.rebuild(base, ours, theirs, "python", do_render=False) == ["data/ai-security.json"]
    out = json.loads((tmp_path / "data/ai-security.json").read_text())
    assert [e["id"] for e in out["entries"]] == ["m", "p", "a"]  # re-sorted by composite
    _git(tmp_path, "add", "-A")
    assert _git(tmp_path, "ls-files", "-u") == ""


def test_rebuild_refuses_a_conflict_it_cannot_resolve(tmp_path, monkeypatch):
    """Opus on #169: the workflow's `! git grep` marker check never failed under
    set -e. A conflicted non-JSON data file must refuse the rebuild."""
    _git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "data").mkdir()
    (tmp_path / "data/backlog.md").write_text("base\n")
    base = _commit(tmp_path, {"data/x.json": {"v": 0}}, "base")
    (tmp_path / "data/backlog.md").write_text("main\n")
    ours = _commit(tmp_path, {"data/x.json": {"v": 1}}, "main")
    _git(tmp_path, "checkout", "-q", "-b", "pr", base)
    (tmp_path / "data/backlog.md").write_text("pr\n")
    theirs = _commit(tmp_path, {"data/x.json": {"v": 2}}, "pr")
    merge = ["-c", "user.name=t", "-c", "user.email=t@i", "merge", "--no-ff", "--no-commit", ours]
    subprocess.run(["git", *merge], cwd=tmp_path, capture_output=True)
    monkeypatch.setattr(rb, "ROOT", tmp_path)
    try:
        rb.rebuild(base, ours, theirs, "python", do_render=False)
    except rb.RebuildError as e:
        assert "data/backlog.md" in str(e)
    else:
        raise AssertionError("an unresolved conflict must refuse the rebuild")


def test_check_clean_finds_a_marker_in_a_staged_file(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q", "-b", "main")
    _commit(tmp_path, {"data/x.json": {}}, "base")
    (tmp_path / "README.md").write_text("ok\n<<<<<<< HEAD\nours\n>>>>>>> pr\n")
    _git(tmp_path, "add", "README.md")
    monkeypatch.setattr(rb, "ROOT", tmp_path)
    try:
        rb.check_clean()
    except rb.RebuildError as e:
        assert "README.md" in str(e)
    else:
        raise AssertionError("a conflict marker must refuse the rebuild")


def test_rebuild_refuses_an_invalid_claim_ledger(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q", "-b", "main")
    base = _commit(tmp_path, {"data/claims.json": {"claims": []}}, "base")
    ours = _commit(tmp_path, {"data/claims.json": {"claims": [{"id": "Bad Id"}]}}, "main")
    _git(tmp_path, "checkout", "-q", "-b", "pr", base)
    theirs = _commit(tmp_path, {"data/claims.json": {"claims": [{"id": "x"}]}}, "pr")
    monkeypatch.setattr(rb, "ROOT", tmp_path)
    try:
        rb.rebuild(base, ours, theirs, "python", do_render=False)
    except rb.RebuildError as e:
        assert "claim ledger" in str(e)
    else:
        raise AssertionError("an invalid merged ledger must be refused")
