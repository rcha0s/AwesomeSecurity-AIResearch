"""A daily scan ingests the last `ingest_days` (a week); a backfill keeps its
own window. A page's own publish date beats a feed or sitemap date wherever
the text is fetched (2026-10-25: a rebuild staged 2022 and Dec 2025 posts as
Sep 28 news)."""

from __future__ import annotations

import dataclasses
from datetime import timedelta
from pathlib import Path

import common as c
import fetch_raw
import merge_analysis as m
import pytest
from conftest import make_entry


def days_ago(n: int) -> str:
    return (c.utcnow().date() - timedelta(days=n)).isoformat()


def page(published: str) -> str:
    return f"Title: A post\n\nPublished Time: {published}T00:00:00.000Z\n\nMarkdown Content:\nbody"


@pytest.fixture
def week(monkeypatch):
    conf = dataclasses.replace(c.load_config(), ingest_days=7, max_age_days=31)
    monkeypatch.setattr(c, "load_config", lambda *a, **k: conf)
    return conf


def test_the_shipped_config_ingests_a_week_and_shows_a_month():
    conf = c.load_config()
    assert (conf.ingest_days, conf.max_age_days) == (7, 31)


def test_a_daily_scan_ingests_a_week_and_a_backfill_its_window(week, monkeypatch):
    assert c.ingest_age_days() == 7
    monkeypatch.setenv(c.BACKFILL_FROM_ENV, days_ago(40))
    monkeypatch.setenv(c.BACKFILL_TO_ENV, days_ago(33))
    assert c.ingest_age_days() == 31


def test_staging_drops_what_is_older_than_the_ingest_week(sandbox, week):
    new = [
        {"id": "a", "title": "Fresh agent hijack", "source_url": "https://x.tld/a",
         "published": days_ago(3)},
        {"id": "b", "title": "Ten day old sandbox escape", "source_url": "https://x.tld/b",
         "published": days_ago(10)},
    ]  # fmt: skip
    assert [x["id"] for x in c.add_candidates(new)] == ["a"]


def test_a_deliberate_add_still_takes_the_sites_month(sandbox, week):
    old = {"id": "b", "title": "Ten day old sandbox escape", "source_url": "https://x.tld/b",
           "published": days_ago(10)}  # fmt: skip
    assert [x["id"] for x in c.add_candidates([old], max_age=week.max_age_days)] == ["b"]


@pytest.mark.parametrize("age, stale", [(10, True), (2, False)])
def test_stale_page_reads_the_pages_own_date(week, age, stale):
    assert (c.stale_page(page(days_ago(age)), 7) is not None) is stale
    assert c.stale_page("Title: no date header\n\nbody", 7) is None  # undated is not stale


def test_fetch_raw_refuses_a_republished_page_before_analysis(sandbox, week, monkeypatch):
    c.save_candidates([{"id": "c1", "article_url": "https://www.anthropic.com/news/bun"}])
    fetch_raw.snapshot_urls()
    monkeypatch.setattr(c, "fetch_readable", lambda url: page("2025-12-03"))
    with pytest.raises(SystemExit, match="STALE c1.*2025-12-03"):
        fetch_raw.fetch_one("c1")
    assert not (c.RAW_DIR / "c1.txt").exists()
    assert "raw_path" not in c.load_candidates()[0]


def test_fetch_raw_keeps_a_page_from_this_week(sandbox, week, monkeypatch):
    c.save_candidates([{"id": "c1", "article_url": "https://openai.com/index/x"}])
    fetch_raw.snapshot_urls()
    monkeypatch.setattr(c, "fetch_readable", lambda url: page(days_ago(1)))
    assert fetch_raw.fetch_one("c1") == c.load_candidates()[0]["raw_path"]


def test_merge_refuses_a_new_entry_whose_page_is_past_the_sites_window(sandbox, week):
    c.RAW_DIR.mkdir(parents=True, exist_ok=True)
    (c.RAW_DIR / "old.txt").write_text(page("2022-12-19"))
    (c.RAW_DIR / "new.txt").write_text(page(days_ago(1)))
    old = make_entry(title="Model-written evals", source_url="https://a/old",
                     raw_path="data/_raw/old.txt")  # fmt: skip
    new = make_entry(
        title="Fresh finding", source_url="https://a/new", raw_path="data/_raw/new.txt"
    )
    merged, errors, _, _ = m.merge([old, new], week)
    assert [x["title"] for x in merged] == ["Fresh finding"]
    assert len(errors) == 1 and "stale: the page says it was published 2022-12-19" in errors[0]


def test_the_golden_wrapper_fetches_past_stories(sandbox, week, monkeypatch):
    c.save_candidates([{"id": "c1", "article_url": "https://www.anthropic.com/research/x"}])
    fetch_raw.snapshot_urls()
    monkeypatch.setattr(c, "fetch_readable", lambda url: page("2022-12-19"))
    monkeypatch.setenv(fetch_raw.ANY_DATE_ENV, "1")
    assert fetch_raw.fetch_one("c1") == c.load_candidates()[0]["raw_path"]
    golden = Path(__file__).resolve().parents[1] / "scripts/run_golden_local.sh"
    assert 'FETCH_RAW_ANY_DATE=1 "$PYTHON" scripts/fetch_raw.py' in golden.read_text()
