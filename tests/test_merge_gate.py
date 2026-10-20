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

    monkeypatch.setattr(gate.subprocess, "run", lambda *a, **k: R())
    assert gate.main([]) == 1
