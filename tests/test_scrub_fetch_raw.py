"""Tests for scripts/scrub.py (PR-body leak guard) and scripts/fetch_raw.py."""

from __future__ import annotations

import common
import fetch_raw
import pytest
import scrub

DEFAULT = "default body"


@pytest.mark.parametrize(
    "secret",
    [
        "ghp_" + "a" * 36,
        "github_pat_" + "B" * 30,
        "sk-ant-" + "c" * 30,
        "AKIA" + "D" * 16,
        "-" * 5 + "BEGIN OPENSSH " + "PRIVATE KEY" + "-" * 5,  # built at runtime: no literal
    ],
)
def test_secret_shaped_summary_is_withheld(tmp_path, secret):
    path = tmp_path / "s.md"
    path.write_text(f"Great scan. {secret}")
    body = scrub.safe_body(path, DEFAULT, {})
    assert secret not in body and body.startswith(DEFAULT) and "withheld" in body


def test_exact_env_secret_is_withheld_but_placeholders_pass(tmp_path):
    path = tmp_path / "s.md"
    path.write_text("token is hunter2hunter2 and proxy-injected")
    assert "hunter2" not in scrub.safe_body(path, DEFAULT, {"MY_API_KEY": "hunter2hunter2"})
    clean = scrub.safe_body(path, DEFAULT, {"GH_TOKEN": "proxy-injected", "HOME": "hunter2hunter2"})
    assert clean.startswith("token is")


def test_missing_or_long_summary(tmp_path):
    assert scrub.safe_body(tmp_path / "nope.md", DEFAULT, {}) == DEFAULT
    path = tmp_path / "s.md"
    path.write_text("x" * (scrub.MAX_CHARS + 50))
    assert scrub.safe_body(path, DEFAULT, {}).endswith("_(summary truncated)_")


def test_fetch_raw_fetches_only_the_candidates_own_url(sandbox, monkeypatch):
    common.save_candidates([{"id": "c1", "article_url": "https://example.com/a"}])
    seen = []
    monkeypatch.setattr(common, "fetch_readable", lambda url: seen.append(url) or "body")
    path = fetch_raw.fetch_one("c1")
    assert seen == ["https://example.com/a"]
    assert (sandbox / path).read_text() == "body"
    assert common.load_candidates()[0]["raw_path"] == path


@pytest.mark.parametrize("bad", ["../../etc/passwd", "a/b", "", "c1;rm -rf /"])
def test_fetch_raw_rejects_bad_ids(sandbox, bad):
    with pytest.raises(SystemExit):
        fetch_raw.fetch_one(bad)


def test_fetch_raw_rejects_unknown_or_non_http(sandbox):
    common.save_candidates([{"id": "c2", "article_url": "file:///etc/passwd"}])
    with pytest.raises(SystemExit):
        fetch_raw.fetch_one("c2")
    with pytest.raises(SystemExit):
        fetch_raw.fetch_one("missing")
