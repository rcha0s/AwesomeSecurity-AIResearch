"""Tests for scripts/ingest_youtube.py — URL building + candidate mapping."""

from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path

import common as c
import ingest_youtube as iy


def test_channel_videos_url_forms():
    assert iy.channel_videos_url("@LiveOverflow") == "https://www.youtube.com/@LiveOverflow/videos"
    assert iy.channel_videos_url("UCabc123") == "https://www.youtube.com/channel/UCabc123/videos"
    assert iy.channel_videos_url("plainname") == "https://www.youtube.com/@plainname/videos"
    # a full URL keeps its host, gains /videos once (not twice)
    assert iy.channel_videos_url("https://youtube.com/@x") == "https://youtube.com/@x/videos"
    assert iy.channel_videos_url("https://youtube.com/@x/videos") == "https://youtube.com/@x/videos"


def test_video_to_candidate_maps_fields():
    v = {
        "webpage_url": "https://youtu.be/abc",
        "title": "Exploiting a parser bug",
        "upload_date": "20260701",
        "description": "A deep dive into the bug.",
        "channel": "LiveOverflow",
    }
    source = {"id": "youtube:lo", "rank": 70.0, "topics": ["product-security"]}
    cand = iy.video_to_candidate(v, source)
    assert cand["discovered_via"] == "youtube"
    assert cand["published"] == "2026-07-01" and cand["date"] == "2026-07"
    assert cand["source_id"] == "youtube:lo" and cand["source_rank"] == 70.0
    assert cand["article_url"] == "https://youtu.be/abc"


def test_video_to_candidate_requires_url_and_title():
    src = {"id": "s", "rank": 1, "topics": []}
    assert iy.video_to_candidate({"title": "x"}, src) is None  # no url
    assert iy.video_to_candidate({"webpage_url": "https://y", "title": ""}, src) is None


def test_video_to_candidate_handles_missing_date():
    v = {"webpage_url": "https://y", "title": "t"}
    cand = iy.video_to_candidate(v, {"id": "s", "rank": 1, "topics": []})
    assert cand["published"] is None and cand["date"] is None


def test_collect_empty_without_sources(sandbox):
    assert iy.collect(3) == []  # no youtube sources registered


def _video(i: int, days_ago: int) -> dict:
    day = (c.utcnow().date() - timedelta(days=days_ago)).strftime("%Y%m%d")
    return {"webpage_url": f"https://youtu.be/v{i}", "title": f"Video {i}", "upload_date": day}


def _channels(monkeypatch, n: int) -> None:
    rows = [
        {"id": f"youtube:c{i}", "handle": f"@c{i}", "rank": 50.0, "topics": []} for i in range(n)
    ]
    monkeypatch.setattr(iy.sr, "sources_of_type", lambda t: rows)


def test_collect_keeps_only_videos_inside_the_ingest_window(monkeypatch):
    _channels(monkeypatch, 1)
    monkeypatch.setattr(iy, "list_videos", lambda h, n: [_video(1, 1), _video(2, 400)])
    assert [x["title"] for x in iy.collect(2)] == ["Video 1"]


def test_collect_asks_for_per_channel_videos_and_caps_the_run(monkeypatch):
    _channels(monkeypatch, 3)
    asked: list[int] = []

    def fake(handle, n):
        asked.append(n)
        return [_video(len(asked) * 10 + k, 1) for k in range(n)]

    monkeypatch.setattr(iy, "list_videos", fake)
    out = iy.collect(2, max_total=5)
    assert asked == [2, 2, 2] and len(out) == 5


def test_collect_without_yt_dlp_stages_nothing(monkeypatch):
    _channels(monkeypatch, 2)
    monkeypatch.setattr(iy, "list_videos", lambda h, n: [])  # list_videos' failure result
    assert iy.collect(2, max_total=8) == []


def test_the_daily_scan_runs_the_ingestor_with_a_small_cap():
    sh = (Path(__file__).resolve().parent.parent / "scripts" / "run_scan.sh").read_text()
    assert "ingest_youtube" in re.search(r"INGESTORS=\((.*?)\)", sh).group(1).split()
    limits = c.load_config().limits
    assert 1 <= limits["youtube_per_channel"] <= 3 and limits["youtube_max_per_run"] <= 10
