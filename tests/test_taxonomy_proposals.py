"""Tests for scripts/taxonomy_proposals.py — verified new-domain proposals are
recorded, counted, and escalated to a `taxonomy` issue (ISA ISC-18). The verifier
is stubbed; GitHub is a fake `gh api`."""

from __future__ import annotations

import json
import subprocess
from datetime import timedelta

import common as c
import pytest
import taxonomy_proposals as tp
from conftest import FIXED_NOW, make_entry

PASS = tp.Verdict(passed=True, nearest="ais.agent-security", reason="agents that spend money")


def _entry(n: int, name: str = "Agent Payments", **over) -> dict:
    proposal = {"name": name, "scope": "Agents that hold and spend money"}
    base = dict(
        id=f"e{n}",
        topic="ai-security",
        domain="ais.agent-security",
        title=f"Story {n}",
        source_url=f"https://a/{n}",
        proposed_domain=proposal,
    )
    return make_entry(**{**base, **over})


def test_record_keeps_only_proposals_the_verifier_passes(sandbox):
    fail = tp.Verdict(passed=False, nearest="ais.agent-security", reason="covered already")
    assert tp.record([_entry(1)], verify=lambda p: fail) == []
    added = tp.record([_entry(1)], verify=lambda p: PASS)
    assert [r["key"] for r in added] == ["ai-security/agent-payments"]
    assert added[0]["verifier_nearest"] == "ais.agent-security"


@pytest.mark.parametrize(
    "verdict",
    [
        tp.Verdict(passed=True, nearest="ais.not-real", reason="x"),  # no such domain
        tp.Verdict(passed=True, nearest="air.agents", reason="x"),  # another topic's id
        tp.Verdict(passed=True, nearest="ais.agent-security", reason=""),  # no reason
    ],
)
def test_a_pass_must_name_a_real_nearest_domain_and_a_reason(sandbox, verdict):
    assert tp.record([_entry(1)], verify=lambda p: verdict) == []


def test_record_ignores_entries_without_a_proposal(sandbox):
    assert tp.record([make_entry()], verify=lambda p: PASS) == []


def test_record_is_idempotent_per_entry(sandbox):
    tp.record([_entry(1)], verify=lambda p: PASS)
    assert tp.record([_entry(1)], verify=lambda p: PASS) == []
    assert len(c.load_json(tp.proposals_file())) == 1


def test_skill_verdict_reads_the_verifier_block():
    v = tp.skill_verdict({"verifier": {"verdict": "PASS", "nearest": "x", "reason": " r "}})
    assert v == tp.Verdict(passed=True, nearest="x", reason="r")
    assert not tp.skill_verdict({}).passed


def _rows(days_ago: list[int], name: str = "Agent Payments") -> list[dict]:
    rows = []
    for n, ago in enumerate(days_ago):
        row = tp._row(_entry(n, name), PASS, FIXED_NOW - timedelta(days=ago))
        rows.append(row)
    return rows


def test_recurring_needs_three_distinct_entries_inside_thirty_days():
    assert tp.recurring(_rows([1, 2]), FIXED_NOW, 30, 3) == {}
    assert tp.recurring(_rows([1, 2, 45]), FIXED_NOW, 30, 3) == {}  # one is stale
    due = tp.recurring(_rows([1, 2, 29]), FIXED_NOW, 30, 3)
    assert list(due) == ["ai-security/agent-payments"]
    same_entry = _rows([1, 2, 3])
    for r in same_entry:
        r["entry"] = "e0"
    assert tp.recurring(same_entry, FIXED_NOW, 30, 3) == {}


# --- GitHub escalation ---------------------------------------------------------
KEY = "ai-security/agent-payments"


class FakeGh:
    """Records `gh api` calls and answers the two GETs notify makes."""

    def __init__(self, issues: list[dict] | None = None, comments: list[dict] | None = None):
        self.calls: list[tuple[str, ...]] = []
        self.issues, self.comments = issues or [], comments or []

    def __call__(self, *args: str) -> str:
        self.calls.append(args)
        if args[0] != "-X" and "/comments" in args[0]:
            return json.dumps(self.comments)
        if args[0] != "-X":
            assert "state=all" in args[0]  # closed issues are decisions, not misses
            return json.dumps(self.issues)
        if args[2].endswith("/labels"):
            raise subprocess.CalledProcessError(1, "gh", stderr='{"code":"already_exists"}')
        return "{}"

    def posts(self, suffix: str) -> list[tuple[str, ...]]:
        return [a for a in self.calls if a[0] == "-X" and a[2].endswith(suffix)]

    def writes(self) -> list[tuple[str, ...]]:
        return [a for a in self.calls if a[0] == "-X" and not a[2].endswith("/labels")]


@pytest.fixture
def due(sandbox, monkeypatch):
    monkeypatch.setattr(tp, "repo_slug", lambda: "o/r")
    c.save_json(tp.proposals_file(), _rows([1, 2, 3]))


def _field(call: tuple[str, ...], name: str) -> str:
    return next(a.split("=", 1)[1] for a in call if a.startswith(f"{name}="))


def _ref(n: int) -> str:
    return tp.entry_ref({"entry": f"e{n}"})


def _issue(state: str, body_refs=(), closed_at: str | None = None) -> dict:
    body = tp.marker(KEY) + "".join(f"\n- {_ref(n)} x" for n in body_refs)
    return {"number": 7, "state": state, "body": body, "closed_at": closed_at}


def test_notify_opens_a_labelled_issue(due, monkeypatch):
    gh = FakeGh()
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {KEY: "opened"}
    (post,) = gh.posts("/issues")
    assert _field(post, "labels[]") == "taxonomy"
    assert "Agent Payments" in _field(post, "title")
    body = _field(post, "body")
    assert tp.marker(KEY) in body and body.count("`entry:") == 3
    assert all(not a[0].startswith("graphql") for a in gh.calls)  # REST only


def test_notify_comments_only_the_entries_the_issue_lacks(due, monkeypatch):
    gh = FakeGh(issues=[_issue("open", [0])], comments=[{"body": f"- {_ref(1)} seen"}])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {KEY: "commented"}
    (post,) = gh.posts("/issues/7/comments")
    body = _field(post, "body")
    assert _ref(2) in body and _ref(0) not in body and _ref(1) not in body


def test_notify_is_quiet_when_the_issue_already_lists_everything(due, monkeypatch):
    gh = FakeGh(issues=[_issue("open", [0, 1, 2])])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {KEY: "unchanged"}
    assert gh.writes() == []


def test_a_closed_issue_is_a_decision_never_a_duplicate(due, monkeypatch):
    """Closing the issue (as its body instructs) must not make the next scan
    open a new one, or reopen it, while the same rows are still in the window."""
    closed = (FIXED_NOW - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    gh = FakeGh(issues=[_issue("closed", [0], closed_at=closed)])
    monkeypatch.setattr(tp, "gh_api", gh)
    for _ in range(3):  # every following day's scan
        assert tp.notify() == {KEY: "closed"}
    assert gh.writes() == []


def test_a_closed_issue_hears_back_only_after_a_fresh_recurrence(due, monkeypatch):
    closed = (FIXED_NOW - timedelta(days=10)).isoformat().replace("+00:00", "Z")
    rows = _rows([20, 15, 12])  # recorded before the close
    fresh = [tp._row(_entry(n), PASS, FIXED_NOW - timedelta(days=d)) for n, d in ((5, 3), (6, 2))]
    c.save_json(tp.proposals_file(), rows + fresh)
    gh = FakeGh(issues=[_issue("closed", closed_at=closed)])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {KEY: "closed"}  # 2 new entries since the close: not enough
    third = tp._row(_entry(7), PASS, FIXED_NOW - timedelta(days=1))
    c.save_json(tp.proposals_file(), rows + fresh + [third])
    assert tp.notify() == {KEY: "commented"}
    (post,) = gh.writes()
    assert post[2].endswith("/issues/7/comments")  # a comment, never a reopen or new issue
    body = _field(post, "body")
    assert body.startswith("Recurred since this was closed")
    assert all(_ref(n) in body for n in (5, 6, 7)) and _ref(0) not in body


def test_an_open_issue_wins_over_an_older_closed_one(due, monkeypatch):
    closed = {**_issue("closed", closed_at="2026-01-01T00:00:00Z"), "number": 3}
    gh = FakeGh(issues=[closed, _issue("open", [0, 1, 2])])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {KEY: "unchanged"}


def test_notify_dry_run_and_nothing_due_touch_no_github(sandbox, monkeypatch):
    def boom(*a):
        raise AssertionError("no GitHub call expected")

    monkeypatch.setattr(tp, "gh_api", boom)
    assert tp.notify() == {}
    c.save_json(tp.proposals_file(), _rows([1, 2, 3]))
    assert tp.notify(dry_run=True) == {KEY: "due"}


SECRET = "ghp_" + "a" * 30


def test_a_secret_shaped_body_falls_back_to_a_plain_one(due, monkeypatch):
    rows = _rows([1, 2, 3])
    rows[0]["verifier_reason"] = f"token {SECRET}"
    c.save_json(tp.proposals_file(), rows)
    gh = FakeGh()
    monkeypatch.setattr(tp, "gh_api", gh)
    tp.notify()
    (post,) = gh.posts("/issues")
    assert SECRET not in "".join(post)
    assert "details withheld" in _field(post, "body") and tp.marker(KEY) in _field(post, "body")


def test_a_secret_in_the_proposal_name_never_reaches_the_title(due, monkeypatch):
    """The title carries the model-written proposal name: it is scrubbed with
    the body, and falls back to a plain title on a hit."""
    rows = _rows([1, 2, 3])
    for r in rows:
        r["name"] = f"Wallets {SECRET}"
    c.save_json(tp.proposals_file(), rows)
    gh = FakeGh()
    monkeypatch.setattr(tp, "gh_api", gh)
    tp.notify()
    (post,) = gh.posts("/issues")
    assert SECRET not in _field(post, "title") and SECRET not in _field(post, "body")
    assert _field(post, "title") == "Taxonomy: proposed ai-security domain (details withheld)"


def test_main_prints_actions(sandbox, capsys):
    assert tp.main(["notify", "--dry-run"]) == 0
    assert "none recurring" in capsys.readouterr().out
