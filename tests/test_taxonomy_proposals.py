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
            return json.dumps(self.issues)
        if args[2].endswith("/labels"):
            raise subprocess.CalledProcessError(1, "gh", stderr='{"code":"already_exists"}')
        return "{}"

    def posts(self, suffix: str) -> list[tuple[str, ...]]:
        return [a for a in self.calls if a[0] == "-X" and a[2].endswith(suffix)]


@pytest.fixture
def due(sandbox, monkeypatch):
    monkeypatch.setattr(tp, "repo_slug", lambda: "o/r")
    c.save_json(tp.proposals_file(), _rows([1, 2, 3]))


def _field(call: tuple[str, ...], name: str) -> str:
    return next(a.split("=", 1)[1] for a in call if a.startswith(f"{name}="))


def test_notify_opens_a_labelled_issue(due, monkeypatch):
    gh = FakeGh()
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {"ai-security/agent-payments": "opened"}
    (post,) = gh.posts("/issues")
    assert _field(post, "labels[]") == "taxonomy"
    body = _field(post, "body")
    assert "taxonomy-proposal:ai-security/agent-payments" in body
    assert body.count("`entry:") == 3
    assert all(not a[0].startswith("graphql") for a in gh.calls)  # REST only


def test_notify_comments_only_the_entries_the_issue_lacks(due, monkeypatch):
    marker = tp.MARKER.format(key="ai-security/agent-payments")
    issue = {"number": 7, "body": f"{marker}\n- `entry:e0` old"}
    gh = FakeGh(issues=[issue], comments=[{"body": "- `entry:e1` seen"}])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {"ai-security/agent-payments": "commented"}
    (post,) = gh.posts("/issues/7/comments")
    body = _field(post, "body")
    assert "entry:e2" in body and "entry:e0" not in body and "entry:e1" not in body


def test_notify_is_quiet_when_the_issue_already_lists_everything(due, monkeypatch):
    marker = tp.MARKER.format(key="ai-security/agent-payments")
    body = marker + "".join(f"\n- `entry:e{n}` x" for n in range(3))
    gh = FakeGh(issues=[{"number": 7, "body": body}])
    monkeypatch.setattr(tp, "gh_api", gh)
    assert tp.notify() == {"ai-security/agent-payments": "unchanged"}
    assert gh.posts("/comments") == [] and gh.posts("/issues") == []


def test_notify_dry_run_and_nothing_due_touch_no_github(sandbox, monkeypatch):
    def boom(*a):
        raise AssertionError("no GitHub call expected")

    monkeypatch.setattr(tp, "gh_api", boom)
    assert tp.notify() == {}
    c.save_json(tp.proposals_file(), _rows([1, 2, 3]))
    assert tp.notify(dry_run=True) == {"ai-security/agent-payments": "due"}


def test_a_secret_shaped_body_falls_back_to_a_plain_one(due, monkeypatch):
    rows = _rows([1, 2, 3])
    rows[0]["verifier_reason"] = "token ghp_" + "a" * 30
    c.save_json(tp.proposals_file(), rows)
    gh = FakeGh()
    monkeypatch.setattr(tp, "gh_api", gh)
    tp.notify()
    body = _field(gh.posts("/issues")[0], "body")
    assert "ghp_" not in body and "details withheld" in body


def test_main_prints_actions(sandbox, capsys):
    assert tp.main(["notify", "--dry-run"]) == 0
    assert "none recurring" in capsys.readouterr().out
