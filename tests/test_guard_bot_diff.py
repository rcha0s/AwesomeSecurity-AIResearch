"""scripts/guard_bot_diff.sh: bot PR branches may only touch their own paths.

Real git repos in tmp_path (no network). `origin/main` is a local ref so the
guard's default base resolves exactly as it does in Actions. Also covers the
PR #98 shape: a branch built on an old main reverts files main gained since.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
GUARD = REPO / "scripts" / "guard_bot_diff.sh"
ENSURE_PR = REPO / "scripts" / "ensure_pr.sh"


def git(cwd: Path, *args: str) -> str:
    env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    ).stdout


def write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    for rel in (
        "data/source_proposals.json",
        "data/ai-security.json",
        "data/evals/history.json",
        "README.md",
        "product-security/a.md",
        "scripts/x.py",
        ".github/workflows/w.yml",
    ):
        write(r, rel, "base\n")
    git(r, "add", "-A")
    git(r, "commit", "-qm", "base")
    git(r, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(r, "checkout", "-q", "-b", "bot")
    return r


def run_guard(r: Path, profile: str) -> subprocess.CompletedProcess:
    return subprocess.run(["bash", str(GUARD), profile], cwd=r, capture_output=True, text=True)


def commit(r: Path, **files: str) -> None:
    for rel, text in files.items():
        write(r, rel.replace("__", "/"), text)
    git(r, "add", "-A")
    git(r, "commit", "-qm", "bot")


def test_source_scout_proposals_only_passes(repo: Path) -> None:
    commit(repo, **{"data__source_proposals.json": "new\n"})
    assert run_guard(repo, "source-scout").returncode == 0


def test_source_scout_extra_path_fails(repo: Path) -> None:
    commit(repo, **{"data__source_proposals.json": "new\n", "scripts__x.py": "evil\n"})
    res = run_guard(repo, "source-scout")
    assert res.returncode == 1
    assert "scripts/x.py" in res.stderr


def test_source_scout_rejects_render_outputs(repo: Path) -> None:
    commit(repo, **{"data__ai-security.json": "new\n"})
    assert run_guard(repo, "source-scout").returncode == 1


def test_render_refresh_allows_rendered_outputs(repo: Path) -> None:
    commit(
        repo,
        **{
            "data__ai-security.json": "new\n",
            "README.md": "new\n",
            "product-security__a.md": "new\n",
            "docs__index.html": "new\n",
            "claims__c.md": "new\n",
        },
    )
    assert run_guard(repo, "render-refresh").returncode == 0


@pytest.mark.parametrize(
    "stray",
    [
        "scripts__x.py",
        ".github__workflows__w.yml",
        "data__evals__history.json",
        "AGENTS.md",
    ],
)
def test_render_refresh_rejects_stray(repo: Path, stray: str) -> None:
    commit(repo, **{"README.md": "new\n", stray: "x\n"})
    res = run_guard(repo, "render-refresh")
    assert res.returncode == 1
    assert stray.replace("__", "/") in res.stderr


def test_stale_base_branch_is_refused(repo: Path) -> None:
    """PR #98: bot branch cut from an old main; main has since moved on."""
    git(repo, "checkout", "-q", "main")
    write(repo, "data/ai-security.json", "newer pool\n")
    write(repo, "product-security/b.md", "new page\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "main moved")
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(repo, "checkout", "-q", "bot")  # still on the old base
    commit(repo, **{"data__source_proposals.json": "new\n"})
    res = run_guard(repo, "source-scout")
    assert res.returncode == 1
    assert "data/ai-security.json" in res.stderr
    assert "product-security/b.md" in res.stderr


def test_deletion_outside_set_fails(repo: Path) -> None:
    git(repo, "rm", "-q", "scripts/x.py")
    git(repo, "commit", "-qm", "rm")
    assert run_guard(repo, "render-refresh").returncode == 1


def test_unknown_profile_is_usage_error(repo: Path) -> None:
    assert run_guard(repo, "nope").returncode == 2


def test_ensure_pr_runs_guard_before_any_api_call(repo: Path, tmp_path: Path) -> None:
    """With BOT_PROFILE set and a stray path, ensure_pr must fail before gh."""
    commit(repo, **{"data__source_proposals.json": "new\n", "scripts__x.py": "evil\n"})
    scripts = repo / "scripts"
    scripts.mkdir(exist_ok=True)
    for f in ("ensure_pr.sh", "lib.sh", "guard_bot_diff.sh"):
        (scripts / f).write_text((REPO / "scripts" / f).read_text())
    git(repo, "remote", "add", "origin", "https://github.com/o/r.git")
    fake = tmp_path / "bin"
    fake.mkdir()
    log = tmp_path / "gh.log"
    (fake / "gh").write_text(f'#!/bin/sh\necho "$*" >> {log}\necho 0\n')
    (fake / "gh").chmod(0o755)
    env = {**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "BOT_PROFILE": "source-scout"}
    res = subprocess.run(
        ["bash", str(scripts / "ensure_pr.sh"), "bot", "t", "b"],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
    )
    assert res.returncode == 1
    assert not log.exists()
