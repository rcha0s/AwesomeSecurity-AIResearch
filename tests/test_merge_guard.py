"""The auto-merge path guard is the security boundary (ISA Anti ISC-A3): exhaustive."""

from __future__ import annotations

import merge_guard as mg
import pytest

REPO = "rcha0s/AwesomeSecurity-AIResearch"
SHA = "a" * 40


def make_pr(**over) -> dict:
    pr = {
        "state": "open",
        "draft": False,
        "labels": [],
        "base": {"ref": "main", "repo": {"full_name": REPO}},
        "head": {"ref": "claude/scan-2026-10-19-cloud", "sha": SHA, "repo": {"full_name": REPO}},
    }
    pr.update(over)
    return pr


def mod(path: str, status: str = "M", new: str = "100644", old: str = "100644") -> mg.Change:
    return mg.Change(old, new, status, path)


def api(path: str, status: str = "modified", prev: str | None = None) -> dict:
    entry = {"filename": path, "status": status}
    if prev:
        entry["previous_filename"] = prev
    return entry


def judge(paths: list[str], **pr_over) -> mg.Verdict:
    return mg.evaluate(
        make_pr(**pr_over), [api(p) for p in paths], [mod(p) for p in paths], REPO, SHA
    )


# ---------------------------------------------------------------- the allowlist

ALLOWED = [
    "data/ai-security.json",
    "data/source_stats.json",
    "data/claims.json",
    "data/backlog.md",
    "docs/index.html",
    "docs/og.png",
    "docs/.nojekyll",
    "docs/findings/ai-research/agent-evals/2026-08-some-slug.md",
    "ai-security/README.md",
    "product-security/x/y.md",
    "ai-research/topic.md",
    "claims/README.md",
    "README.md",
    "NEWSLETTER.md",
    "TRENDS.md",
    "REVIEW.md",
]

REFUSED = [
    # code, workflows, skills, tests, evals
    "scripts/common.py",
    "scripts/templates/site.html",
    ".github/workflows/automerge.yml",
    ".github/CODEOWNERS",
    ".claude/skills/daily-scan/SKILL.md",
    ".claude/settings.json",
    "tests/conftest.py",
    "evals/golden/classification.json",
    # config and agent docs
    "config.yaml",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "setup.cfg",
    "ISA.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "PUBLISH.md",
    "LICENSE",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    "conftest.py",
    "sitecustomize.py",
    # pipeline tuning and staging under data/
    "data/cluster_keywords.yaml",
    "data/sources.json",
    "data/source_proposals.json",
    "data/interests.yaml",
    "data/source_blocklist.json",
    "data/candidates.json",
    "data/analysis_out.json",
    "data/editorial_out.json",
    "data/_raw/abc.txt",
    "data/_scan_lock",
    "data/_budget_ledger.json",
    # wrong file types inside content dirs
    "data/evil.py",
    "data/x.sh",
    "docs/app.js",
    "docs/evil.html",
    "docs/findings/x/y.html",
    "docs/index.htm",
    "docs/index.html.md.html",
    "data/index.html",
    "ai-security/index.html",
    "index.html",
    "docs/conftest.py",
    "ai-security/run.yaml",
    "data/noext",
    # dot paths inside content dirs
    "data/.github/workflows/x.json",
    "docs/.gitattributes",
    "docs/.well-known/x.json",
    # look-alikes of allowed names
    "README.md.py",
    "readme.md",
    "Data/ai-security.json",
    "datax/a.json",
    "data",
    "docs",
    "docsx/index.html",
    "ai-security",
    "notes/README.md",
    "README",
    # traversal and odd paths
    "data/../scripts/common.py",
    "docs/../.github/workflows/x.json",
    "./data/a.json",
    "data/./a.json",
    "/data/a.json",
    "data//a.json",
    "data/a.json/",
    "data\\..\\scripts\\common.py",
    "data/a b.json",
    "data/a\nb.json",
    "data/a\x00.json",
    "data/ä.json",
    "data/‮swap.json",
    "",
    "data/" + "a" * 400 + ".json",
]


@pytest.mark.parametrize("path", ALLOWED)
def test_allowlisted_content_passes(path):
    assert mg.path_reason(path) is None
    assert judge([path]).ok


@pytest.mark.parametrize("path", REFUSED)
def test_everything_else_is_refused(path):
    assert mg.path_reason(path) is not None
    verdict = judge([path])
    assert not verdict.ok and verdict.reasons


@pytest.mark.parametrize("path", REFUSED)
def test_one_bad_path_poisons_an_otherwise_clean_pr(path):
    assert not judge(["data/ai-security.json", "README.md", path]).ok


def test_display_neutralises_markup_and_control_chars():
    shown = mg.display("data/[x](http://evil)\n@rcha0s`")
    assert shown == "data/?x??http?//evil???rcha0s?"
    assert mg.display("a" * 200).endswith("...")


# ---------------------------------------------------------------- renames and deletions


def test_rename_out_of_scripts_is_refused():
    files = [api("data/common.json", "renamed", prev="scripts/common.py")]
    changes = [mod("scripts/common.py", "D", new="000000"), mod("data/common.json", "A")]
    v = mg.evaluate(make_pr(), files, changes, REPO, SHA)
    assert not v.ok and any("scripts/common.py" in r for r in v.reasons)


def test_rename_into_scripts_is_refused():
    files = [api("scripts/x.json", "renamed", prev="data/x.json")]
    changes = [mod("data/x.json", "D", new="000000"), mod("scripts/x.json", "A")]
    assert not mg.evaluate(make_pr(), files, changes, REPO, SHA).ok


def test_rename_within_content_passes():
    files = [api("docs/b.md", "renamed", prev="docs/a.md")]
    changes = [mod("docs/a.md", "D", new="000000"), mod("docs/b.md", "A")]
    assert mg.evaluate(make_pr(), files, changes, REPO, SHA).ok


def test_api_rename_whose_old_side_git_missed_is_refused():
    # previous_filename is checked even if the git view somehow lacks it.
    files = [api("data/x.json", "renamed", prev=".github/workflows/t.yml")]
    v = mg.evaluate(make_pr(), files, [mod("data/x.json", "A")], REPO, SHA)
    assert not v.ok
    # Refused for the path itself, not only for the git/API disagreement.
    assert any(r.startswith(".github/workflows/t.yml:") for r in v.reasons)


@pytest.mark.parametrize("path", ["scripts/common.py", ".github/workflows/tests.yml", "ISA.md"])
def test_deleting_pipeline_files_is_refused(path):
    files = [api(path, "removed")]
    changes = [mod(path, "D", new="000000")]
    assert not mg.evaluate(make_pr(), files, changes, REPO, SHA).ok


def test_deleting_content_passes():
    files = [api("docs/old.md", "removed")]
    changes = [mod("docs/old.md", "D", new="000000")]
    assert mg.evaluate(make_pr(), files, changes, REPO, SHA).ok


# ---------------------------------------------------------------- modes and statuses


@pytest.mark.parametrize("mode", ["120000", "160000", "100755", "040000", "100664"])
def test_non_regular_files_are_refused(mode):
    files = [api("data/a.json", "added")]
    changes = [mod("data/a.json", "A", new=mode, old="000000")]
    v = mg.evaluate(make_pr(), files, changes, REPO, SHA)
    assert not v.ok and any("mode" in r for r in v.reasons)


@pytest.mark.parametrize("status", ["T", "U", "X", "R100", "C100", ""])
def test_unexpected_git_statuses_are_refused(status):
    assert mg.mode_reason(mod("data/a.json", status)) is not None


def test_delete_must_have_an_empty_new_mode():
    assert mg.mode_reason(mod("data/a.json", "D", new="100644")) is not None
    assert mg.mode_reason(mod("data/a.json", "D", new="000000")) is None


@pytest.mark.parametrize("status", ["changed", "copied", "unchanged", None, "weird"])
def test_unexpected_api_statuses_are_refused(status):
    v = mg.evaluate(make_pr(), [api("data/a.json", status)], [mod("data/a.json")], REPO, SHA)
    assert not v.ok


# ---------------------------------------------------------------- cross-checks


def test_git_and_api_must_agree():
    files = [api("data/a.json")]
    changes = [mod("data/a.json"), mod("data/b.json")]
    v = mg.evaluate(make_pr(), files, changes, REPO, SHA)
    assert not v.ok and any("disagree" in r for r in v.reasons)


def test_truncated_api_list_is_refused():
    paths = [f"docs/p{i}.md" for i in range(mg.API_FILE_CAP)]
    assert not judge(paths).ok
    assert judge(paths[:-1]).ok


def test_empty_pr_is_refused():
    assert not mg.evaluate(make_pr(), [], [], REPO, SHA).ok


def test_api_entry_without_filename_is_refused():
    v = mg.evaluate(make_pr(), [{"status": "modified"}], [mod("data/a.json")], REPO, SHA)
    assert not v.ok


# ---------------------------------------------------------------- PR metadata


@pytest.mark.parametrize(
    "over",
    [
        {"state": "closed"},
        {"draft": True},
        {"draft": None},
        {"labels": [{"name": "automerge:hold"}]},
        {"base": {"ref": "dev", "repo": {"full_name": REPO}}},
        {"base": {"ref": "main", "repo": {"full_name": "evil/fork"}}},
        {"head": {"ref": "claude/scan-x", "sha": SHA, "repo": {"full_name": "evil/fork"}}},
        {"head": {"ref": "claude/scan-x", "sha": SHA, "repo": None}},
        {"head": {"ref": "feat/anything", "sha": SHA, "repo": {"full_name": REPO}}},
        {"head": {"ref": "claude/scan-", "sha": SHA, "repo": {"full_name": REPO}}},
        {"head": {"ref": "claude/scan-a/b", "sha": SHA, "repo": {"full_name": REPO}}},
        {"head": {"ref": "xclaude/scan-a", "sha": SHA, "repo": {"full_name": REPO}}},
        {"head": {"ref": "claude/scan-a", "sha": "b" * 40, "repo": {"full_name": REPO}}},
    ],
)
def test_pr_metadata_refusals(over):
    assert not judge(["data/a.json"], **over).ok


def test_expected_sha_must_be_a_full_sha():
    pr = make_pr(head={"ref": "claude/scan-a", "sha": "", "repo": {"full_name": REPO}})
    assert mg.pr_reasons(pr, REPO, "") != []
    assert mg.pr_reasons(make_pr(), REPO, SHA[:12]) != []


def test_other_labels_do_not_block():
    assert judge(["data/a.json"], labels=[{"name": "scan"}]).ok


def test_clean_scan_pr_passes_with_no_reasons():
    v = judge(["data/ai-security.json", "docs/index.html", "README.md"])
    assert v.ok and v.reasons == [] and "README.md" in v.paths


# ---------------------------------------------------------------- raw diff parsing


def test_parse_raw_diff_round_trip():
    raw = (
        ":100644 100644 aaa bbb M\0data/a.json\0"
        ":000000 100644 000 ccc A\0docs/new file?.md\0"
        ":100644 000000 ddd 000 D\0scripts/x.py\0"
    )
    changes = mg.parse_raw_diff(raw)
    assert [(c.status, c.path) for c in changes] == [
        ("M", "data/a.json"),
        ("A", "docs/new file?.md"),
        ("D", "scripts/x.py"),
    ]
    assert changes[2].new_mode == "000000"


def test_parse_raw_diff_rename_record_keeps_both_paths_in_sync():
    raw = ":100644 100644 a b R100\0scripts/x.py\0data/x.json\0:100644 100644 a b M\0README.md\0"
    changes = mg.parse_raw_diff(raw)
    assert [c.path for c in changes] == ["scripts/x.py", "README.md"]
    assert mg.mode_reason(changes[0]) is not None


@pytest.mark.parametrize("raw", ["garbage\0", ":100644 100644 a b\0x\0", ":100644 100644 a b M\0"])
def test_parse_raw_diff_rejects_malformed(raw):
    with pytest.raises(ValueError):
        mg.parse_raw_diff(raw)


def test_parse_raw_diff_empty():
    assert mg.parse_raw_diff("") == []


def test_cli(tmp_path, capsys):
    import json

    (tmp_path / "pr.json").write_text(json.dumps(make_pr()))
    (tmp_path / "f.json").write_text(json.dumps([api("scripts/x.py")]))
    (tmp_path / "raw").write_text(":100644 100644 a b M\0scripts/x.py\0")
    args = ["x", *(str(tmp_path / n) for n in ("pr.json", "f.json", "raw")), REPO, SHA]
    assert mg.main(args) == 1
    assert json.loads(capsys.readouterr().out)["ok"] is False
    assert mg.main(["x"]) == 2
