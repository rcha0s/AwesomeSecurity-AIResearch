"""automerge.py orchestration: mode handling, TOCTOU re-check, merge-with-sha, reporting."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import automerge as am
import merge_guard as mg
import pytest

REPO = "rcha0s/AwesomeSecurity-AIResearch"
SHA = "a" * 40
MAIN = "c" * 40


def scan_pr(number=7, sha=SHA, ref="claude/scan-2026-10-19-cloud") -> dict:
    return {
        "number": number,
        "state": "open",
        "draft": False,
        "labels": [],
        "base": {"ref": "main", "repo": {"full_name": REPO}},
        "head": {"ref": ref, "sha": sha, "repo": {"full_name": REPO}},
    }


def write_config(root: Path, text: str) -> None:
    (root / "config.yaml").write_text(text)


@pytest.mark.parametrize(
    "text, mode",
    [
        ("automerge:\n  mode: merge\n", "merge"),
        ("automerge:\n  mode: shadow\n", "shadow"),
        ("automerge:\n  mode: MERGE\n", "shadow"),
        ("automerge:\n  mode: true\n", "shadow"),
        ("other: 1\n", "shadow"),
        ("automerge: [1, 2]\n", "shadow"),
        (": : not yaml [\n", "shadow"),
        ("", "shadow"),
    ],
)
def test_mode_fails_closed_to_shadow(tmp_path, text, mode):
    write_config(tmp_path, text)
    assert am.settings(tmp_path / "config.yaml")["mode"] == mode


def test_missing_config_is_shadow(tmp_path):
    assert am.settings(tmp_path / "nope.yaml") == {
        "mode": "shadow",
        "merge_method": "squash",
        "rebuild": False,
    }


def test_shipped_config_is_merge():
    """Rohan ended the shadow period 2026-10-31 (ISA.md). Changing the mode again
    should change this test too, so the switch is always a deliberate edit."""
    assert am.settings(am.ROOT / "config.yaml")["mode"] == "merge"


# ---------------------------------------------------------------- a fake GitHub


class FakeGitHub:
    def __init__(self, prs, files, changes, behind=0, check="success"):
        self.prs = {p["number"]: p for p in prs}
        self.files, self.changes = files, changes
        self.behind, self.check = behind, check
        self.calls: list[tuple] = []
        self.comments: dict[int, list[dict]] = {}

    def gh(self, path, *args):
        self.calls.append((path, *args))
        if "/check-runs" in path:
            conclusion = self.check
            return {"check_runs": [{"conclusion": conclusion, "app": {"id": am.PYTEST_APP_ID}}]}
        if "/compare/" in path:
            return {"behind_by": self.behind}
        if path.endswith("/comments") and "-X" in args:
            body = args[args.index("-f") + 1].removeprefix("body=")
            self.comments.setdefault(int(path.split("/")[-2]), []).append({"body": body})
            return {}
        if "/pulls/" in path and not args:
            return self.prs[int(path.rsplit("/", 1)[-1])]
        return {}

    def pages(self, path):
        if path.endswith("/files"):
            return self.files
        if path.endswith("/comments"):
            return self.comments.get(int(path.split("/")[-2]), [])
        return list(self.prs.values())

    def install(self, monkeypatch, tmp_path, mode):
        monkeypatch.setattr(am, "gh", self.gh)
        monkeypatch.setattr(am, "gh_pages", self.pages)
        monkeypatch.setattr(am, "raw_changes", lambda n, h, m: self.changes)
        monkeypatch.setattr(am, "ROOT", tmp_path)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        write_config(tmp_path, f"automerge:\n  mode: {mode}\n")
        return self

    def did(self, fragment: str) -> list[tuple]:
        return [c for c in self.calls if fragment in c[0] and "-X" in c]


def content_only():
    return [{"filename": "data/a.json", "status": "modified"}], [
        mg.Change("100644", "100644", "M", "data/a.json")
    ]


def touches_scripts():
    files = [{"filename": "scripts/common.py", "status": "modified"}]
    return files, [mg.Change("100644", "100644", "M", "scripts/common.py")]


def run_decide(fake, number="7", sha=SHA, tests="success"):
    return am.cmd_decide(REPO, MAIN, number, sha, tests)


# ---------------------------------------------------------------- decide


def test_shadow_mode_never_merges(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "shadow")
    assert run_decide(fake) == 0
    assert not fake.did("/merge") and not fake.did("update-branch") and not fake.did("dispatches")
    assert "would merge" in fake.comments[7][0]["body"]


def test_merge_mode_merges_with_the_tested_sha(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "merge")
    run_decide(fake)
    (merge_call,) = fake.did("/pulls/7/merge")
    assert f"sha={SHA}" in merge_call and "merge_method=squash" in merge_call
    assert fake.did("update.yml/dispatches") and fake.did("pages/builds")
    assert fake.comments[7][0]["body"].count("merged") >= 1


def test_merge_mode_refuses_pipeline_changes(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *touches_scripts()).install(monkeypatch, tmp_path, "merge")
    run_decide(fake)
    assert not fake.did("/merge")
    body = fake.comments[7][0]["body"]
    assert "refused" in body and "scripts/common.py" in body


def test_head_moved_after_testing_is_not_merged(monkeypatch, tmp_path):
    moved = "b" * 40
    fake = FakeGitHub([scan_pr(sha=moved)], *content_only()).install(monkeypatch, tmp_path, "merge")
    run_decide(fake, sha=SHA)  # tested SHA != current head
    assert not fake.did("/merge")


def test_head_moved_between_listing_and_rejudge_is_refused(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "merge")
    fresh = scan_pr(sha="b" * 40)  # the re-fetch sees a new head
    orig = fake.gh
    monkeypatch.setattr(am, "gh", lambda p, *a: fresh if p.endswith("/pulls/7") else orig(p, *a))
    run_decide(fake)
    assert not fake.did("/merge")
    assert "head moved" in fake.comments[7][0]["body"]


@pytest.mark.parametrize("tests", ["failure", "cancelled", "skipped", ""])
def test_merge_needs_green_in_workflow_tests(monkeypatch, tmp_path, tests):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "merge")
    run_decide(fake, tests=tests)
    assert not fake.did("/merge")


def test_failed_tests_are_reported_as_refused(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "shadow")
    run_decide(fake, tests="failure")
    assert "refused" in fake.comments[7][0]["body"]


def test_behind_main_updates_branch_but_does_not_dispatch(monkeypatch, tmp_path):
    # update-branch makes a new, unjudged head; the next run judges it first.
    fake = FakeGitHub([scan_pr()], *content_only(), behind=2).install(
        monkeypatch, tmp_path, "merge"
    )
    run_decide(fake)
    assert not fake.did("/merge")
    (update,) = fake.did("update-branch")
    assert f"expected_head_sha={SHA}" in update
    assert not fake.did("tests.yml/dispatches")


def test_no_dispatch_if_head_moved_just_before(monkeypatch, tmp_path):
    """Audit F7: tests.yml runs the branch's own workflow file, so a dispatch
    goes out only after re-confirming the head is still the judged SHA."""
    fake = FakeGitHub([scan_pr()], *content_only(), check=None).install(
        monkeypatch, tmp_path, "merge"
    )
    orig, fetches = fake.gh, []

    def gh(path, *args):
        if path.endswith("/pulls/7") and not args:
            fetches.append(path)
            # first fetch (judge) sees the judged head; the re-check sees a new one
            return scan_pr() if len(fetches) == 1 else scan_pr(sha="b" * 40)
        return orig(path, *args)

    monkeypatch.setattr(am, "gh", gh)
    run_decide(fake)
    assert len(fetches) == 2
    assert not fake.did("tests.yml/dispatches")


def test_missing_required_check_dispatches_tests(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only(), check=None).install(
        monkeypatch, tmp_path, "merge"
    )
    run_decide(fake)
    assert not fake.did("/merge") and not fake.did("update-branch")
    (dispatch,) = fake.did("tests.yml/dispatches")
    assert "ref=claude/scan-2026-10-19-cloud" in dispatch


def test_shadow_mode_does_not_unblock(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only(), behind=1, check=None)
    fake.install(monkeypatch, tmp_path, "shadow")
    run_decide(fake)
    assert not fake.did("update-branch") and not fake.did("dispatches")


def test_failed_merge_is_reported_not_raised(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "merge")
    orig = fake.gh

    def gh(path, *args):
        if path.endswith("/merge"):
            raise subprocess.CalledProcessError(1, "gh")
        return orig(path, *args)

    monkeypatch.setattr(am, "gh", gh)
    run_decide(fake)
    assert "merge FAILED" in fake.comments[7][0]["body"]


def test_comments_are_posted_once_per_head_and_verdict(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *touches_scripts()).install(monkeypatch, tmp_path, "shadow")
    run_decide(fake)
    run_decide(fake)
    assert len(fake.comments[7]) == 1


def test_untested_scan_prs_are_only_reported(monkeypatch, tmp_path):
    prs = [scan_pr(7), scan_pr(8, sha="d" * 40)]
    fake = FakeGitHub(prs, *content_only()).install(monkeypatch, tmp_path, "merge")
    run_decide(fake, number="7")
    merges = fake.did("/merge")
    assert len(merges) == 1 and "/pulls/7/" in merges[0][0]
    assert 8 not in fake.comments  # guard-clean but untested: summary only, no verdict


@pytest.mark.parametrize("number, sha", [("7; rm", SHA), ("7", "xyz"), ("-1", SHA)])
def test_decide_rejects_malformed_inputs(monkeypatch, tmp_path, number, sha):
    fake = FakeGitHub([scan_pr()], *content_only()).install(monkeypatch, tmp_path, "merge")
    assert run_decide(fake, number=number, sha=sha) == 1
    assert not fake.did("/merge")


def test_main_rejects_bad_main_sha():
    assert am.main(["select", "--repo", REPO, "--main-sha", "main"]) == 1


def test_judge_errors_refuse(monkeypatch):
    def boom(*a):
        raise subprocess.CalledProcessError(1, "gh")

    monkeypatch.setattr(am, "gh", boom)
    v = am.judge(REPO, 7, SHA, MAIN)
    assert not v.ok and "could not evaluate" in v.reasons[0]


# ---------------------------------------------------------------- select


def test_select_picks_the_oldest_passing_pr(monkeypatch, tmp_path):
    prs = [scan_pr(5, sha="e" * 40), scan_pr(7)]
    FakeGitHub(prs, *content_only()).install(monkeypatch, tmp_path, "shadow")
    out = tmp_path / "out"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    am.cmd_select(REPO, MAIN)
    assert out.read_text().startswith(f"number=5\nsha={'e' * 40}\n")


def test_select_skips_a_pr_that_conflicts_with_main(monkeypatch, tmp_path):
    """11-06: #165 conflicted with main, failed the test merge every run, and blocked #166."""
    dirty = {**scan_pr(5, sha="e" * 40), "mergeable": False}
    pending = {**scan_pr(7), "mergeable": None}  # GitHub still computing: tested as before
    FakeGitHub([dirty, pending], *content_only()).install(monkeypatch, tmp_path, "merge")
    out, summ = tmp_path / "out", tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summ))
    am.cmd_select(REPO, MAIN)
    assert out.read_text().startswith(f"number=7\nsha={SHA}\nrebuild_number=\n")
    assert "#5" in summ.read_text() and "conflicts with main" in summ.read_text()


def _select(monkeypatch, tmp_path, fake, config=None):
    if config is not None:
        write_config(tmp_path, config)
    out, summ = tmp_path / "out", tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summ))
    am.cmd_select(REPO, MAIN)
    values = dict(line.split("=", 1) for line in out.read_text().splitlines())
    return values, summ.read_text()


REBUILD_ON = "automerge:\n  mode: merge\n  rebuild_conflicts: true\n"


def test_select_hands_a_conflicting_pr_to_the_rebuild_job(monkeypatch, tmp_path):
    dirty = {**scan_pr(5, sha="e" * 40, ref="claude/scan-2026-11-04-local"), "mergeable": False}
    fake = FakeGitHub([dirty, scan_pr(7)], *content_only()).install(monkeypatch, tmp_path, "merge")
    out, summ = _select(monkeypatch, tmp_path, fake, REBUILD_ON)
    assert (out["rebuild_number"], out["rebuild_sha"]) == ("5", "e" * 40)
    assert out["rebuild_ref"] == "claude/scan-2026-11-04-local-rebuilt-cccccccc"
    assert (out["number"], out["sha"]) == ("7", SHA)  # the next PR is still tested
    assert "to be rebuilt on main" in summ


def test_rebuilt_ref_replaces_an_earlier_rebuild_suffix():
    assert (
        am.rebuilt_ref("claude/scan-x-rebuilt-0123abcd", "f" * 40)
        == "claude/scan-x-rebuilt-ffffffff"
    )


@pytest.mark.parametrize(
    "config",
    [
        "automerge:\n  mode: shadow\n  rebuild_conflicts: true\n",
        "automerge:\n  mode: merge\n  rebuild_conflicts: yes-please\n",
    ],
)
def test_no_rebuild_in_shadow_mode_or_without_an_explicit_true(monkeypatch, tmp_path, config):
    dirty = {**scan_pr(5), "mergeable": False}
    fake = FakeGitHub([dirty], *content_only()).install(monkeypatch, tmp_path, "merge")
    out, summ = _select(monkeypatch, tmp_path, fake, config)
    assert out["rebuild_number"] == "" and out["number"] == ""
    assert "rebuild is off" in summ


def _gate_comment(sha, outcome="refused", login="github-actions[bot]", reason=None):
    body = am.comment_body(sha, outcome, "merge", [reason or am.TESTS_FAILED])
    return {"user": {"login": login}, "body": body}


def test_select_skips_a_head_whose_tests_already_failed(monkeypatch, tmp_path):
    """A held claim change fails merge_gate the same way every run; re-testing it
    first would starve every newer scan PR, as the conflicting #165 did."""
    held = scan_pr(5, sha="e" * 40)
    fake = FakeGitHub([held, scan_pr(7)], *content_only()).install(monkeypatch, tmp_path, "merge")
    fake.comments[5] = [_gate_comment("e" * 40)]
    out, summ = _select(monkeypatch, tmp_path, fake)
    assert (out["number"], out["sha"]) == ("7", SHA)
    assert "tests already failed on this head" in summ


@pytest.mark.parametrize(
    "comment",
    [
        _gate_comment("f" * 40),  # an older head failed; this one is new
        _gate_comment("e" * 40, outcome="would wait (shadow mode)"),
        _gate_comment("e" * 40, login="rcha0s"),  # only the workflow's own comments count
        # A guard refusal (hold label, draft, API blip) is re-judged every run anyway:
        # lifting the hold must be enough, so it never skips the head.
        _gate_comment("e" * 40, reason="labelled automerge:hold"),
    ],
)
def test_select_still_tests_a_head_whose_tests_did_not_fail(monkeypatch, tmp_path, comment):
    fake = FakeGitHub([scan_pr(5, sha="e" * 40)], *content_only())
    fake.install(monkeypatch, tmp_path, "merge")
    fake.comments[5] = [comment]
    out, _ = _select(monkeypatch, tmp_path, fake)
    assert out["number"] == "5"


def test_a_failed_rebuild_moves_on_to_the_next_conflicting_pr(monkeypatch, tmp_path):
    """Opus on #169: a rebuild that fails every run must not jam the rebuild slot."""
    stuck = {**scan_pr(5, sha="e" * 40), "mergeable": False}
    nxt = {**scan_pr(6, sha="d" * 40), "mergeable": False}
    fake = FakeGitHub([stuck, nxt], *content_only()).install(monkeypatch, tmp_path, "merge")
    fake.comments[5] = [_gate_comment("e" * 40, reason=am.rebuild_failed(MAIN))]
    out, summ = _select(monkeypatch, tmp_path, fake, REBUILD_ON)
    assert out["rebuild_number"] == "6"
    assert "rebuild already failed" in summ


def test_a_rebuild_that_failed_on_an_older_main_is_retried(monkeypatch, tmp_path):
    stuck = {**scan_pr(5, sha="e" * 40), "mergeable": False}
    fake = FakeGitHub([stuck], *content_only()).install(monkeypatch, tmp_path, "merge")
    fake.comments[5] = [_gate_comment("e" * 40, reason=am.rebuild_failed("b" * 40))]
    out, _ = _select(monkeypatch, tmp_path, fake, REBUILD_ON)
    assert out["rebuild_number"] == "5"


def test_rebuild_failed_records_the_main_it_failed_on(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr(5, sha="e" * 40)], *content_only())
    fake.install(monkeypatch, tmp_path, "merge")
    assert am.cmd_rebuild_failed(REPO, MAIN, "5", "e" * 40) == 0
    assert am.rebuild_failed(MAIN) in fake.comments[5][0]["body"]


class ReplaceGitHub:
    def __init__(self, old_head):
        self.old = {**scan_pr(5, sha=old_head), "title": "chore: daily scan (local, 2026-11-04)"}
        self.calls: list[tuple] = []

    def gh(self, path, *args):
        self.calls.append((path, *args))
        if path.endswith("/pulls") and "POST" in args:
            return {"number": 170}
        if path.endswith("/pulls/5") and not args:
            return self.old
        return {}


@pytest.mark.parametrize("old_head, closed", [("e" * 40, True), ("f" * 40, False)])
def test_replace_opens_the_new_pr_and_closes_the_old_only_if_unmoved(
    monkeypatch, tmp_path, old_head, closed
):
    fake = ReplaceGitHub(old_head)
    monkeypatch.setattr(am, "gh", fake.gh)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    ref = "claude/scan-2026-11-04-local-rebuilt-cccccccc"
    assert am.cmd_replace(REPO, MAIN, "5", "e" * 40, ref) == 0
    opened = [c for c in fake.calls if c[0].endswith("/pulls") and "POST" in c]
    assert opened and f"head={ref}" in opened[0] and "base=main" in opened[0]
    assert any("(rebuilt on main)" in a for a in opened[0])
    closes = [c for c in fake.calls if c[0].endswith("/pulls/5") and "state=closed" in c]
    assert bool(closes) == closed


@pytest.mark.parametrize(
    "args",
    [
        ["replace", "--number", "5", "--sha", SHA, "--new-ref", "main"],
        ["replace", "--number", "5", "--sha", SHA, "--new-ref", "claude/scan-x"],
        ["replace", "--number", "x", "--sha", SHA, "--new-ref", "claude/scan-x-rebuilt-cccccccc"],
        ["rebuild-failed", "--number", "5", "--sha", "nope"],
    ],
)
def test_rebuild_commands_reject_malformed_inputs(args):
    assert am.main([*args, "--repo", REPO, "--main-sha", MAIN]) == 1


def _repo(tmp_path: Path) -> tuple[Path, str]:
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True)

    run("init", "-q", "-b", "main")
    (tmp_path / "data").mkdir()
    (tmp_path / "data/a.json").write_text("{}\n")
    run("add", "-A")
    run("-c", "user.name=t", "-c", "user.email=t@i", "commit", "-qm", "main")
    return tmp_path, run("rev-parse", "HEAD").stdout.strip()


def _commit_on(root: Path, parents: list[str], files: dict[str, str]) -> str:
    def run(*a, **kw):
        return subprocess.run(
            ["git", *a], cwd=root, check=True, capture_output=True, text=True, **kw
        )

    run("checkout", "-q", "--detach", parents[0])
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text)
    run("add", "-A")
    tree = run("write-tree").stdout.strip()
    flags = [x for p in parents for x in ("-p", p)]
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@i",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@i"}  # fmt: skip
    return run("commit-tree", tree, *flags, "-m", "x", env=env).stdout.strip()


def test_check_tree_passes_content_on_main(monkeypatch, tmp_path):
    root, main = _repo(tmp_path)
    monkeypatch.setattr(am, "ROOT", root)
    commit = _commit_on(root, [main], {"data/a.json": '{"x": 1}\n', "docs/index.html": "<p>"})
    assert am.tree_reasons(main, commit) == []


@pytest.mark.parametrize(
    "files", [{"scripts/x.py": "print(1)\n"}, {".github/workflows/x.yml": "on: push\n"}]
)
def test_check_tree_refuses_a_pipeline_path(monkeypatch, tmp_path, files):
    root, main = _repo(tmp_path)
    monkeypatch.setattr(am, "ROOT", root)
    assert am.tree_reasons(main, _commit_on(root, [main], files))


def test_check_tree_refuses_a_commit_not_directly_on_main(monkeypatch, tmp_path):
    root, main = _repo(tmp_path)
    monkeypatch.setattr(am, "ROOT", root)
    side = _commit_on(root, [main], {"data/b.json": "{}\n"})
    merge = _commit_on(root, [side, main], {"data/c.json": "{}\n"})
    assert "rebuilt commit's only parent is not main" in am.tree_reasons(main, merge)


def test_select_outputs_nothing_when_all_refused(monkeypatch, tmp_path):
    fake = FakeGitHub([scan_pr()], *touches_scripts()).install(monkeypatch, tmp_path, "shadow")
    out, summ = tmp_path / "out", tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summ))
    am.cmd_select(REPO, MAIN)
    assert out.read_text().startswith("number=\nsha=\nrebuild_number=\n")
    assert "refused" in summ.read_text()
    assert fake.comments == {}  # the read-only job never comments


def test_scan_prs_filters_non_scan_branches(monkeypatch):
    prs = [scan_pr(1), scan_pr(2, ref="feat/x"), scan_pr(3, ref="chore/render-refresh")]
    monkeypatch.setattr(am, "gh_pages", lambda path: prs)
    assert [p["number"] for p in am.scan_prs(REPO)] == [1]


def test_gh_pages_follows_pages(monkeypatch):
    pages = {1: [{"i": n} for n in range(100)], 2: [{"i": 100}]}
    monkeypatch.setattr(am, "gh", lambda path: pages[int(path.rsplit("page=", 1)[1])])
    assert len(am.gh_pages("repos/x/pulls/1/files")) == 101


def test_comment_body_fences_and_strips_backticks():
    body = am.comment_body(SHA, "refused", "shadow", ["a`b"] * 30)
    assert body.startswith(am.MARKER) and "a'b" in body and "a`b" not in body
    assert "and 5 more" in body


# ---------------------------------------------------------------- real git


def git(cwd: Path, *args: str) -> str:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
    }
    env["GIT_COMMITTER_EMAIL"] = "t@t"
    out = subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True)
    return out.stdout.decode().strip()


def test_raw_changes_on_a_real_repo_sees_both_sides_of_a_rename_and_symlinks(tmp_path, monkeypatch):
    origin, clone = tmp_path / "origin", tmp_path / "clone"
    origin.mkdir()
    git(origin, "init", "-q", "-b", "main")
    (origin / "scripts").mkdir()
    (origin / "scripts" / "common.py").write_text("x = 1\n")
    (origin / "README.md").write_text("hi\n")
    git(origin, "add", "-A")
    git(origin, "commit", "-qm", "base")
    main_sha = git(origin, "rev-parse", "HEAD")
    git(origin, "checkout", "-q", "-b", "claude/scan-x")
    (origin / "data").mkdir()
    git(origin, "mv", "scripts/common.py", "data/common.json")
    os.symlink("../README.md", origin / "data" / "link.json")
    git(origin, "add", "-A")
    git(origin, "commit", "-qm", "scan")
    head = git(origin, "rev-parse", "HEAD")
    git(origin, "update-ref", "refs/pull/9/head", head)
    git(tmp_path, "clone", "-q", str(origin), str(clone))
    monkeypatch.setattr(am, "ROOT", clone)
    changes = am.raw_changes(9, head, main_sha)
    by_path = {c.path: c for c in changes}
    assert by_path["scripts/common.py"].status == "D"
    assert by_path["data/common.json"].status == "A"
    assert by_path["data/link.json"].new_mode == "120000"
    with pytest.raises(RuntimeError):
        am.raw_changes(9, "f" * 40, main_sha)
