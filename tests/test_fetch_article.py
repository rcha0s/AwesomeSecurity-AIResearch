"""Tests for scripts/fetch_article.py — arxiv HTML/PDF fallback, generic
r.jina fetch, and in-place raw_path population."""

from __future__ import annotations

import json
from pathlib import Path

import common
import fetch_article
import pytest


# ---------------------------------------------------------------- URL parsing

@pytest.mark.parametrize("url,expected", [
    ("https://arxiv.org/abs/2608.05490", "2608.05490"),
    ("https://arxiv.org/abs/2608.05490v2", "2608.05490"),
    ("http://arxiv.org/abs/2506.09443", "2506.09443"),
    ("https://arxiv.org/html/2608.05490v1", "2608.05490"),
    ("https://arxiv.org/pdf/2608.05490", "2608.05490"),
    ("https://github.com/foo/bar", None),
    ("", None),
])
def test_arxiv_id_extraction(url, expected):
    assert fetch_article.arxiv_id(url) == expected


def test_arxiv_url_helpers():
    assert fetch_article.arxiv_html_url("1234.5678") == "https://arxiv.org/html/1234.5678v1"
    assert fetch_article.arxiv_pdf_url("1234.5678") == "https://arxiv.org/pdf/1234.5678"


# ---------------------------------------------------------------- fetch_body

def test_fetch_arxiv_prefers_html_when_long_enough():
    calls = []

    def fake_fetch(url):
        calls.append(url)
        # HTML variant returns plenty of text.
        return "x" * 6000

    body = fetch_article.fetch_arxiv_body("2608.05490", fetch=fake_fetch)
    assert body is not None and len(body) == 6000
    assert calls == ["https://arxiv.org/html/2608.05490v1"]  # PDF not tried


def test_fetch_arxiv_falls_back_to_pdf_when_html_stubs():
    calls = []

    def fake_fetch(url):
        calls.append(url)
        if "/html/" in url:
            return "abstract only, no paper body"  # under MIN_BODY_CHARS
        return "y" * 8000  # PDF has the real content

    body = fetch_article.fetch_arxiv_body("2608.05490", fetch=fake_fetch)
    assert body is not None and len(body) == 8000
    assert calls == [
        "https://arxiv.org/html/2608.05490v1",
        "https://arxiv.org/pdf/2608.05490",
    ]


def test_fetch_arxiv_falls_back_to_pdf_when_html_raises():
    calls = []

    def fake_fetch(url):
        calls.append(url)
        if "/html/" in url:
            raise RuntimeError("404")
        return "z" * 5000

    body = fetch_article.fetch_arxiv_body("2608.05490", fetch=fake_fetch)
    assert body is not None
    assert "/html/" in calls[0] and "/pdf/" in calls[1]


def test_fetch_arxiv_returns_none_when_both_fail():
    def fake_fetch(url):
        raise RuntimeError("dead")

    assert fetch_article.fetch_arxiv_body("2608.05490", fetch=fake_fetch) is None


def test_fetch_generic_returns_body_on_success():
    body = fetch_article.fetch_generic_body(
        "https://example.com/post",
        fetch=lambda url: "generic body text",
    )
    assert body == "generic body text"


def test_fetch_generic_returns_none_on_error():
    def boom(url):
        raise RuntimeError("timeout")

    assert fetch_article.fetch_generic_body("https://example.com/x", fetch=boom) is None


def test_fetch_body_dispatches_arxiv_vs_generic():
    def fake_fetch(url):
        return "body-of-" + url + ("x" * 6000)

    arxiv = {"article_url": "https://arxiv.org/abs/2608.05490"}
    other = {"article_url": "https://example.com/post"}
    a = fetch_article.fetch_body(arxiv, fetch=fake_fetch)
    b = fetch_article.fetch_body(other, fetch=fake_fetch)
    assert "arxiv.org/html/2608.05490" in a
    assert "example.com/post" in b


def test_fetch_body_returns_none_for_no_url():
    assert fetch_article.fetch_body({"article_url": None, "source_url": None}) is None


# --------------------------------------------------- needs_fetch / populate

def test_needs_fetch_true_when_no_raw_path():
    assert fetch_article.needs_fetch({"article_url": "https://x.y", "raw_path": None})


def test_needs_fetch_false_when_raw_path_set():
    assert not fetch_article.needs_fetch({"article_url": "https://x.y",
                                          "raw_path": "data/_raw/x.txt"})


def test_needs_fetch_false_when_no_url():
    assert not fetch_article.needs_fetch({"raw_path": None})


def test_populate_writes_raw_paths(sandbox):
    cands = [
        {"id": "a", "title": "Paper A",
         "article_url": "https://arxiv.org/abs/2608.05490", "raw_path": None},
        {"id": "b", "title": "Repo B",
         "article_url": "https://example.com/b", "raw_path": None},
        {"id": "c", "title": "Already fetched",
         "article_url": "https://example.com/c",
         "raw_path": "data/_raw/c.txt"},
    ]

    def fake_fetch(url):
        return "body text " + url + ("x" * 6000)

    fetched, skipped = fetch_article.populate_raw_paths(
        cands, fetch=fake_fetch, delay=0
    )
    assert fetched == 2
    assert skipped == 1
    # Both fetched candidates got a raw_path pointing at data/_raw/<id>.txt.
    assert cands[0]["raw_path"].endswith("a.txt")
    assert cands[1]["raw_path"].endswith("b.txt")
    # The one that already had raw_path is unchanged.
    assert cands[2]["raw_path"] == "data/_raw/c.txt"


def test_populate_respects_limit(sandbox):
    cands = [
        {"id": f"c{i}", "title": f"T{i}",
         "article_url": f"https://example.com/{i}", "raw_path": None}
        for i in range(5)
    ]
    fetched, skipped = fetch_article.populate_raw_paths(
        cands, limit=2, fetch=lambda u: "x" * 6000, delay=0
    )
    assert fetched == 2
    assert skipped == 3
    # First two got a raw_path; last three did not.
    assert cands[0]["raw_path"] is not None
    assert cands[1]["raw_path"] is not None
    assert cands[2]["raw_path"] is None


def test_populate_dry_run_writes_nothing(sandbox):
    cands = [{"id": "a", "title": "T",
              "article_url": "https://arxiv.org/abs/2608.05490",
              "raw_path": None}]
    fetched, _ = fetch_article.populate_raw_paths(
        cands, dry_run=True, fetch=lambda u: "x" * 6000, delay=0
    )
    assert fetched == 1
    # dry_run leaves raw_path untouched
    assert cands[0]["raw_path"] is None


def test_populate_records_misses(sandbox):
    cands = [{"id": "a", "title": "T",
              "article_url": "https://example.com/dead", "raw_path": None}]

    def dead(url):
        raise RuntimeError("timeout")

    fetched, skipped = fetch_article.populate_raw_paths(
        cands, fetch=dead, delay=0
    )
    assert fetched == 0
    assert skipped == 1
    assert cands[0]["raw_path"] is None  # no raw_path when the fetch failed


# --------------------------------------------------------------------- main

def test_main_missing_files_are_reported(sandbox, capsys):
    rc = fetch_article.main([])
    assert rc == 0  # missing bucket files are non-fatal
    err = capsys.readouterr().err
    assert "candidates.routed.json missing" in err
    assert "candidates.filtered.json missing" in err


def test_main_reads_and_writes_survivor_files(sandbox, monkeypatch):
    routed = [{"id": "r1", "title": "Routed one",
               "article_url": "https://arxiv.org/abs/2608.05490",
               "raw_path": None}]
    filtered = [{"id": "f1", "title": "Filtered one",
                 "article_url": "https://example.com/post",
                 "raw_path": None}]
    common.save_json(fetch_article._routed_file(), routed)
    common.save_json(fetch_article._filtered_file(), filtered)
    # Patch the default fetch so main() doesn't hit the network.
    monkeypatch.setattr(fetch_article, "default_fetch", lambda url: "y" * 6000)
    rc = fetch_article.main(["--limit", "10"])
    assert rc == 0
    routed_after = json.loads(fetch_article._routed_file().read_text())
    filtered_after = json.loads(fetch_article._filtered_file().read_text())
    assert routed_after[0]["raw_path"].endswith("r1.txt")
    assert filtered_after[0]["raw_path"].endswith("f1.txt")
