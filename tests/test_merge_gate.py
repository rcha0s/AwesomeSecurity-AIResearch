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
    monkeypatch.setattr(gate, "git_json", lambda ref_path, default: default)


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
