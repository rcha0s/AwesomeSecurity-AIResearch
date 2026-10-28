"""merge_gate.py: the Phase 3 eval hook fails closed only once an eval is required."""

from __future__ import annotations

import merge_gate as gate
import pytest


def cfg(*evals) -> dict:
    return {"automerge": {"evals": list(evals)}}


def names(steps) -> list[str]:
    return [name for name, _ in steps]


def test_builtins_always_run(tmp_path):
    steps, problems = gate.plan({}, tmp_path)
    assert names(steps) == ["pytest", "claim ledger", "analysis eval"]
    assert problems == []


def test_missing_optional_eval_is_skipped(tmp_path):
    steps, problems = gate.plan(cfg({"script": "scripts/eval_integrity.py"}), tmp_path)
    assert "scripts/eval_integrity.py" not in names(steps) and problems == []


def test_missing_required_eval_fails_closed(tmp_path):
    entry = {"script": "scripts/eval_integrity.py", "required": True}
    _, problems = gate.plan(cfg(entry), tmp_path)
    assert problems == ["required eval scripts/eval_integrity.py is missing"]


@pytest.mark.parametrize("required", [True, False])
def test_present_eval_runs(tmp_path, required):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "eval_integrity.py").write_text("")
    entry = {"script": "scripts/eval_integrity.py", "required": required}
    steps, problems = gate.plan(cfg(entry), tmp_path)
    assert names(steps)[-1] == "scripts/eval_integrity.py" and problems == []


def test_required_must_be_literally_true(tmp_path):
    _, problems = gate.plan(cfg({"script": "scripts/e.py", "required": "yes"}), tmp_path)
    assert problems == []  # "yes" is not true: optional, so skipped (documented)


@pytest.mark.parametrize(
    "entry",
    ["scripts/e.py", {"script": "/etc/passwd"}, {"script": "scripts/../x.py"}, {"script": 3}, {}],
)
def test_malformed_entries_raise(tmp_path, entry):
    with pytest.raises(ValueError):
        gate.plan(cfg(entry), tmp_path)


def test_evals_must_be_a_list(tmp_path):
    with pytest.raises(ValueError):
        gate.plan({"automerge": {"evals": "scripts/e.py"}}, tmp_path)


def test_shipped_config_plans_cleanly():
    import yaml

    config = yaml.safe_load((gate.ROOT / "config.yaml").read_text())
    steps, problems = gate.plan(config)
    assert problems == [] and names(steps)[:3] == ["pytest", "claim ledger", "analysis eval"]


def test_dry_run_runs_nothing(capsys):
    assert gate.main(["--dry-run"]) == 0
    assert "merge_gate: pytest" in capsys.readouterr().out


def test_failing_step_fails_the_gate(monkeypatch):
    monkeypatch.setattr(gate, "BUILTIN", (("boom", ["false"]),))

    class R:
        returncode = 1

    monkeypatch.setattr(gate, "content_problems", lambda base: [])
    monkeypatch.setattr(gate.subprocess, "run", lambda *a, **k: R())
    assert gate.main([]) == 1


def test_content_problems_fail_the_gate(monkeypatch):
    monkeypatch.setattr(gate, "BUILTIN", ())
    monkeypatch.setattr(gate, "content_problems", lambda base: ["x.json: bad"])
    assert gate.main([]) == 1
    monkeypatch.setattr(gate, "content_problems", lambda base: [])
    assert gate.main([]) == 0


def test_content_checks_that_cannot_run_fail_closed(monkeypatch):
    def boom(base):
        raise OSError("no such ref")

    monkeypatch.setattr(gate, "BUILTIN", ())
    monkeypatch.setattr(gate, "content_problems", boom)
    assert gate.main([]) == 1


def _tree(tmp_path, url="https://ok.example/", page=None):
    import json

    import generate_html as gh

    (tmp_path / "data").mkdir()
    (tmp_path / "docs").mkdir()
    pool = {"entries": [{"source_url": url}]}
    (tmp_path / "data" / "ai-security.json").write_text(json.dumps(pool))
    (tmp_path / "data" / "claims.json").write_text(json.dumps({"claims": [{"id": "a"}]}))
    (tmp_path / "docs" / "index.html").write_text(page or gh.render({"x": 1}, "2026-10-20"))
    return tmp_path


@pytest.fixture(autouse=True)
def _no_main_stories(monkeypatch):
    """main's story ledger and eval history come from git; these trees carry
    neither (the real main does once a scan has merged)."""
    monkeypatch.setattr(gate, "main_stories", lambda base: {})
    monkeypatch.setattr(gate, "main_has_feed", lambda base: False)
    no_main_history(monkeypatch)


# main's files these fixture trees don't model: the eval history, and the pools
# + archive the sticky-promotion check reads (the real main has promotions).
ABSENT_ON_MAIN = tuple(
    f":data/{n}"
    for n in ("evals/history.json", "ai-security.json", "product-security.json",
              "ai-research.json", "archive.json")
)  # fmt: skip


def no_main_history(monkeypatch) -> None:
    """main's history, pools and archive read as absent; every other git read is real."""
    real = gate.git_json

    def fake(ref_path: str, default: object) -> object:
        if ref_path.endswith(ABSENT_ON_MAIN):
            return default
        return real(ref_path, default)

    monkeypatch.setattr(gate, "git_json", fake)


def test_editorial_check_holds_a_demotion_for_a_human(tmp_path, monkeypatch):
    import json

    root = _tree(tmp_path)
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": [{"id": "a"}]})
    promo = {"id": "p1", "editorial": {"promoted": True}, "grounding_score": 1.0}
    main = {"BASE:data/ai-security.json": {"entries": [promo]}}
    monkeypatch.setattr(gate, "git_json", lambda ref, default: main.get(ref, default))
    pool = root / "data" / "ai-security.json"
    pool.write_text(json.dumps({"entries": [{"id": "p1", "grounding_score": 1.0}]}))
    problems = gate.content_problems("BASE", root)
    assert problems == ["editorial demotion needs human review: p1 lost its promotion "
                        "with main's integrity intact"]  # fmt: skip
    pool.write_text(json.dumps({"entries": [{"id": "p1", "verified": False}]}))
    assert gate.editorial_check("BASE", root) != []  # refuted in this PR: a human decides
    main["BASE:data/ai-security.json"] = {"entries": [{**promo, "verified": False}]}
    assert gate.editorial_check("BASE", root) == []  # already refuted on main
    main["BASE:data/ai-security.json"] = {"entries": [promo]}
    pool.unlink()
    (root / "data" / "archive.json").write_text(json.dumps([promo]))
    assert gate.editorial_check("BASE", root) == []  # aged into the archive, still promoted


def test_content_problems_refuse_a_hold_on_a_published_entry(tmp_path, monkeypatch):
    import json

    from conftest import make_entry

    root = _tree(tmp_path)
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": [{"id": "a"}]})
    shown = make_entry(id="s", topic="ai-security", domain="ais.agent-security")
    main = {"BASE:data/ai-security.json": {"entries": [shown]}}
    monkeypatch.setattr(gate, "git_json", lambda ref, default: main.get(ref, default))
    held = {**shown, "readability_hold": "readability: title_words 30 > 24"}
    (root / "data" / "ai-security.json").write_text(json.dumps({"entries": [held]}))
    assert gate.content_problems("BASE", root) == [
        "readability hold of a published entry needs human review: s"
    ]


def test_content_problems_on_a_clean_tree(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": [{"id": "a"}]})
    assert gate.content_problems("main", _tree(tmp_path)) == []


def test_content_problems_catch_each_invariant(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": [{"id": "a"}, {"id": "b"}]})
    root = _tree(tmp_path, url="javascript:alert(1)", page="<html>hand written</html>")
    problems = gate.content_problems("main", root)
    assert any("ai-security.json" in p and "http(s)" in p for p in problems)
    assert any("docs/index.html" in p for p in problems)
    assert any("claim b" in p for p in problems)


def test_missing_page_is_a_problem(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": []})
    root = _tree(tmp_path)
    (root / "docs" / "index.html").unlink()
    assert "docs/index.html is missing" in gate.content_problems("main", root)


def test_main_ledger_reads_git_not_the_tree():
    ledger = gate.main_ledger("HEAD")
    assert isinstance(ledger, dict) and "claims" in ledger


def test_feed_check_accepts_exact_render_and_refuses_edits(tmp_path, monkeypatch):
    import generate_html as gh

    root = _tree(tmp_path)
    page = (root / "docs" / "index.html").read_text()
    feed = root / "docs" / "feed.xml"
    monkeypatch.setattr(gate, "main_has_feed", lambda base: True)
    assert gate.feed_check("main", root) == ["docs/feed.xml is missing"]
    feed.write_text(gh.render_feed_for_page(page))
    assert gate.feed_check("main", root) == []
    feed.write_text(feed.read_text().replace("<title>", "<title>x", 1))
    assert gate.feed_check("main", root) != []
    feed.unlink()
    monkeypatch.setattr(gate, "main_has_feed", lambda base: False)
    assert gate.feed_check("main", root) == []


REAL_MAIN_HAS_FEED = gate.main_has_feed


@pytest.mark.parametrize("eol", ["\r\n", "\r"])
def test_feed_and_page_are_compared_as_raw_bytes(tmp_path, monkeypatch, eol):
    import generate_html as gh

    root = _tree(tmp_path)
    monkeypatch.setattr(gate, "main_has_feed", lambda base: True)
    index, feed = root / "docs" / "index.html", root / "docs" / "feed.xml"
    good = gh.render_feed_for_page(index.read_text())
    feed.write_bytes(good.encode())
    assert gate.feed_check("main", root) == []
    feed.write_bytes(good.replace("\n", eol).encode())
    assert gate.feed_check("main", root) != []
    feed.write_bytes(good.encode())
    index.write_bytes(index.read_text().replace("\n", eol).encode())
    assert any("docs/index.html" in p for p in gate.content_problems("main", root))


def test_main_has_feed_fails_closed():
    main_has_feed = REAL_MAIN_HAS_FEED  # the autouse fixture stubs gate.main_has_feed
    with pytest.raises(RuntimeError):
        main_has_feed("no-such-ref-xyz")
    head = gate.subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=gate.ROOT, capture_output=True, text=True
    ).stdout.strip()
    assert main_has_feed(head) in (True, False)  # a valid commit answers
    with pytest.raises(RuntimeError):
        main_has_feed("4b825dc642cb6eb9a060e54bf8d69288fbee4904")  # a tree, not a commit
