"""Tests for scripts/select_batch.py (the run-sized batch the scan session
reads) and scripts/scan_count.py (what a run analyzed, and whether it worked).

2026-10-20: the session was handed all 286 staged candidates, judged them too
many for its budget, analyzed nothing, and post still opened a "0 stories" PR
whose ledger row counted 19 news stories rerank had restored from the archive.
"""

from __future__ import annotations

import json

import common
import prefilter
import pytest
import scan_count
import select_batch
import story_ledger
from test_prefilter import _cand


@pytest.fixture
def table() -> prefilter.KeywordTable:
    return prefilter.KeywordTable(
        keywords={"ais.prompt-injection": ("prompt injection", "jailbreak", "memory poisoning")},
        excluded=("autonomous driving",),
    )


def conf(cap: int = 2, margin: int = 1) -> common.Config:
    base = common.load_config()
    return common.Config(
        **{**base.__dict__, "limits": {"max_stories_per_run": cap, "batch_margin": margin}}
    )


def cands(n: int, **over) -> list[dict]:
    return [
        _cand(
            id=f"c{i}",
            title=f"Neutral finding number {i} about topic{i}",
            source_url=f"https://ex{i}.example/p",
            article_url=f"https://ex{i}.example/p",
            **over,
        )
        for i in range(n)
    ]


def test_batch_size_is_the_story_cap_plus_the_named_margin():
    assert select_batch.batch_size(conf(8, 4)) == 12
    real = common.load_config()
    assert real.limits["batch_margin"] == 4  # named in config.yaml, not a code default
    assert select_batch.batch_size(real) == real.limits["max_stories_per_run"] + 4


def test_the_batch_is_cut_to_size_and_nothing_is_lost(sandbox, table):
    staged = cands(10)
    batch, backlog = select_batch.select(staged, conf(2, 1), table)
    assert len(batch) == 3
    assert sorted(c["id"] for c in batch + backlog) == sorted(c["id"] for c in staged)
    assert [b["batch_rank"] for b in backlog] == list(range(4, 11))


def test_rank_prefers_routed_then_credible_then_new(sandbox, table):
    routed = _cand(
        id="routed",
        title="Prompt injection and jailbreak via memory poisoning",
        source_url="https://r.example/1",
        source_rank=10.0,
        published="2026-06-20",
    )
    credible = _cand(id="credible", source_url="https://c.example/1", source_rank=90.0)
    fresh = _cand(id="fresh", source_url="https://f.example/1", published="2026-07-14")
    stale = _cand(id="stale", source_url="https://s.example/1", published="2026-06-20")
    batch, backlog = select_batch.select([stale, fresh, credible, routed], conf(2, 1), table)
    assert [c["id"] for c in batch] == ["routed", "credible", "fresh"]
    assert [c["id"] for c in backlog] == ["stale"]


def test_prefilter_drops_never_enter_the_batch(sandbox, table):
    noise = [
        _cand(id="deny", title="Vendor stock jumps after earnings", source_url="https://d.ex/1"),
        _cand(id="off", title="Autonomous driving dataset", source_url="https://o.ex/1"),
    ]
    batch, backlog = select_batch.select([*noise, *cands(1)], conf(5, 5), table)
    assert [c["id"] for c in batch] == ["c0"]
    reasons = {c["id"]: c["prefilter"]["reason"] for c in backlog}
    assert reasons == {"deny": "denylist", "off": "excluded:autonomous driving"}


def test_main_writes_the_batch_and_a_code_owned_backlog(sandbox, capsys, table, monkeypatch):
    monkeypatch.setattr(prefilter, "load_keywords", lambda path=None: table)
    common.save_candidates(cands(20))
    assert select_batch.main([]) == 0
    size = select_batch.batch_size(common.load_config())
    assert len(common.load_candidates()) == size
    backlog = json.loads((sandbox / "data" / "_scan_backlog.json").read_text())
    assert len(backlog) == 20 - size
    assert f"SCAN_BATCH: {size} of 20 candidates selected" in capsys.readouterr().out


# --- scan_count ----------------------------------------------------------------
@pytest.fixture
def on_main(monkeypatch):
    def set_main(pools=(), archive=()):
        monkeypatch.setattr(common, "main_entry_ids", lambda: set(pools))
        monkeypatch.setattr(scan_count, "main_archive_ids", lambda: set(archive))

    return set_main


def pool_with(*ids: str) -> None:
    common.save_pool("ai-security", {"topic": "ai-security", "entries": [{"id": i} for i in ids]})


def test_entries_rerank_restored_from_the_archive_are_not_this_runs(sandbox, on_main, capsys):
    on_main(pools={"kept"}, archive={"news-1", "news-2"})
    pool_with("kept", "news-1", "news-2")  # rerank pulled archived news back
    assert scan_count.main([]) == 0 and capsys.readouterr().out.strip() == "0"
    assert scan_count.main(["--work"]) == scan_count.NO_WORK
    capsys.readouterr()
    pool_with("kept", "news-1", "news-2", "fresh")
    assert scan_count.main([]) == 0 and capsys.readouterr().out.strip() == "1"


def test_work_is_analysis_or_an_applied_same_or_update_verdict(sandbox, on_main):
    on_main()
    assert scan_count.main(["--work"]) == scan_count.NO_WORK
    common.save_json(common.ANALYSIS_OUT, [])
    assert scan_count.main(["--work"]) == scan_count.NO_WORK
    outcomes = sandbox / "data" / "_story_outcomes.md"
    new_only = [{"action": "new", "candidate_id": "x"}]
    outcomes.write_text(story_ledger.outcomes_record(new_only))
    assert scan_count.main(["--work"]) == scan_count.NO_WORK  # `new` alone changed nothing
    same = [{"action": "same", "story_id": "s1", "url": "https://x.example/a"}]
    outcomes.write_text(story_ledger.outcomes_record(same))
    assert scan_count.main(["--work"]) == 0
    outcomes.unlink()
    common.save_json(common.ANALYSIS_OUT, [{"id": "a"}])
    assert scan_count.main(["--work"]) == 0


def test_settled_count_reads_the_code_owned_record():
    outs = [
        {"action": "same", "story_id": "s1", "url": "u1"},
        {"action": "update", "story_id": "s2", "url": "u2"},
        {"action": "new", "candidate_id": "c"},
        {"action": "rejected", "candidate_id": "d", "reason": "r"},
    ]
    assert story_ledger.settled_count(story_ledger.outcomes_record(outs)) == 2
