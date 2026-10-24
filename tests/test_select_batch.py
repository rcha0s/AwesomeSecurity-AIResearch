"""Tests for scripts/select_batch.py (the run-sized batch the scan session
reads) and scripts/scan_count.py (what a run analyzed, and whether it worked).

2026-10-20: the session was handed all 286 staged candidates, judged them too
many for its budget, analyzed nothing, and post still opened a "0 stories" PR
whose ledger row counted 19 news stories rerank had restored from the archive.
"""

from __future__ import annotations

import json

import common
import ingest_ghsa
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


def conf(
    cap: int = 2, margin: int = 1, per_source: int = 2, bonus: float = 5, **extra
) -> common.Config:
    base = common.load_config()
    limits = {
        "max_stories_per_run": cap,
        "batch_margin": margin,
        "batch_per_source": per_source,
        "batch_routed_bonus": bonus,
        **extra,
    }
    return common.Config(**{**base.__dict__, "limits": limits})


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
    assert real.limits["batch_per_source"] == 2 and real.limits["batch_routed_bonus"] == 5
    assert real.limits["batch_priority_max"] == 4  # 5 until the big-story lane (2026-10-23)
    assert real.limits["batch_priority_per_source"] == 3
    assert real.limits["batch_class_slots"] == {"rss": 2}
    assert select_batch.batch_size(real) == real.limits["max_stories_per_run"] + 4


def test_the_batch_is_cut_to_size_and_nothing_is_lost(sandbox, table):
    staged = cands(10)
    batch, backlog = select_batch.select(staged, conf(2, 1), table)
    assert len(batch) == 3
    assert sorted(c["id"] for c in batch + backlog) == sorted(c["id"] for c in staged)
    assert [b["batch_rank"] for b in backlog] == list(range(4, 11))


def test_score_prefers_credible_then_new_and_routing_only_nudges(sandbox, table):
    one = {"source_id": "rss:one"}  # one source, one class: pure score order
    credible = _cand(id="credible", source_url="https://c.example/1", source_rank=90.0, **one)
    fresh = _cand(id="fresh", source_url="https://f.example/1", published="2026-07-14", **one)
    stale = _cand(id="stale", source_url="https://s.example/1", published="2026-06-20", **one)
    weak_routed = _cand(
        id="routed",
        title="Prompt injection and jailbreak via memory poisoning",
        source_url="https://r.example/1",
        source_rank=30.0,
        published="2026-06-20",
        **one,
    )
    staged = [stale, weak_routed, fresh, credible]
    batch, backlog = select_batch.select(staged, conf(2, 1, per_source=9), table)
    assert [c["id"] for c in batch] == ["credible", "fresh", "routed"]  # +5 beats stale only
    assert [c["id"] for c in backlog] == ["stale"]
    batch, _ = select_batch.select(staged, conf(2, 1, per_source=9, bonus=0), table)
    assert [c["id"] for c in batch] == ["credible", "fresh", "stale"]


def realistic_mix() -> list[dict]:
    """2026-10-20's shape: many routed, credible GHSA/vendor items that would win
    on score alone, and filtered KEV, HN and Simon Willison items."""

    def make(prefix, n, rank, title, **over):
        return [
            _cand(
                id=f"{prefix}{i}",
                title=f"{title} {prefix} {i} item{prefix}{i}",
                source_url=f"https://{prefix}.example/{i}",
                article_url=f"https://{prefix}.example/{i}",
                source_rank=rank,
                published="2026-07-14",
                **over,
            )
            for i in range(n)
        ]

    routed = "Prompt injection jailbreak"
    return [
        *make(
            "ghsa", 60, 80.0, routed, source_id=None, discovered_via="github", source_type="GHSA"
        ),
        *make("vendor", 10, 75.0, routed, source_id="rss:vendor"),
        *make("kev", 10, 50.0, "CISA KEV entry", source_id="kev_json:cisa"),
        *make(
            "hn",
            5,
            40.0,
            "Show HN",
            source_id=None,
            discovered_via="hackernews",
            source_type="Hacker News",
        ),
        *make("simon", 10, 60.0, "Notes on", source_id="rss:simonwillison"),
        *[x for j in range(3) for x in make(f"blog{j}", 3, 55.0, "Post", source_id=f"rss:b{j}")],
    ]


def test_no_source_class_starves_the_others(sandbox, table):
    batch, _ = select_batch.select(realistic_mix(), conf(8, 4), table)
    sources = [select_batch.source_key(c) for c in batch]
    assert len(batch) == 12
    assert "kev_json:cisa" in sources and "hackernews:Hacker News" in sources
    assert max(sources.count(s) for s in set(sources)) <= 2  # batch_per_source
    assert sources.count("github:GHSA") == 2  # the score leader still gets its share


def must_not_miss_mix() -> list[dict]:
    """realistic_mix plus the 2026-W43 shape: critical GHSA (one in AI tooling)
    and a high one in AI tooling, all scoring below the routed GHSA flood. "AI
    tooling" means prefilter routed it to an ais.* domain (two keyword hits)."""
    ghsa = {"source_id": None, "discovered_via": "github", "source_type": "GHSA"}

    def adv(i, severity, ai=False, rank=40.0):
        title = f"Prompt injection jailbreak in agentpkg{i}" if ai else f"Advisory {i} in pkg{i}"
        return _cand(
            id=f"adv{i}",
            title=title,
            source_url=f"https://github.com/advisories/GHSA-{i}",
            article_url=f"https://github.com/advisories/GHSA-{i}",
            source_rank=rank,
            published="2026-07-14",
            severity=severity,
            guess_topic="ai-security" if ai else "product-security",
            **ghsa,
        )

    return [
        *realistic_mix(),
        adv(1, "CRITICAL"),
        adv(2, "CRITICAL", rank=30.0),
        adv(3, "CRITICAL", ai=True, rank=20.0),  # Claude Agent SDK, LMCache
        adv(4, "HIGH", ai=True, rank=10.0),
        adv(5, "HIGH"),  # not AI tooling: no lane
        adv(6, "MODERATE", ai=True),  # not severe enough: no lane
    ]


LANE = {"batch_priority_max": 5, "batch_priority_per_source": 3}


def test_must_not_miss_lane_comes_first_and_ai_tooling_leads_it(sandbox, table):
    staged = must_not_miss_mix()
    batch, backlog = select_batch.select(staged, conf(8, 4, **LANE), table)
    assert len(batch) == 12
    lane = [c for c in batch if c.get("batch_priority")]
    assert batch[: len(lane)] == lane and len(lane) == 5
    # dealt in turn, best head first: the critical in AI tooling leads (adv3); then
    # KEV (rank 50) and the other criticals (adv1 rank 40) in rank order. The HIGH
    # AI-tooling advisory (adv4) never takes a critical's place.
    assert [c["id"] for c in lane] == ["adv3", "kev0", "kev1", "adv1", "kev2"]
    kinds = [c["batch_priority"] for c in lane]
    assert kinds == ["ghsa-critical", "kev", "kev", "ghsa-critical", "kev"]
    sources = [select_batch.source_key(c) for c in batch]
    assert sources.count("github:GHSA") == 2  # the lane used GHSA's batch_per_source
    assert sources.count("kev_json:cisa") == 3  # lane cap 3, above batch_per_source
    assert "hackernews:Hacker News" in sources  # the deal still reaches every class
    ids = [c["id"] for c in batch + backlog]
    assert sorted(ids) == sorted(c["id"] for c in staged)  # nothing lost or duplicated
    assert not any(c.get("batch_priority") for c in backlog)


def test_criticals_come_before_high_ai_tooling_within_ghsa(sandbox, table):
    wide = {"batch_priority_max": 9, "batch_priority_per_source": 4}
    batch, _ = select_batch.select(must_not_miss_mix(), conf(8, 4, **wide), table)
    ghsa = [c["id"] for c in batch if c.get("batch_priority", "").startswith("ghsa")]
    assert ghsa == ["adv3", "adv1", "adv2", "adv4"]


def test_lane_order_beats_rank_within_ghsa(sandbox, table):
    """Rank alone can't decide: a critical in AI tooling beats a better-ranked
    critical, and any critical beats a better-ranked HIGH in AI tooling."""
    ghsa = {"source_id": None, "discovered_via": "github", "source_type": "GHSA"}

    def adv(i, severity, ai, rank):
        title = f"Prompt injection jailbreak in agentpkg{i}" if ai else f"Advisory {i} in pkg{i}"
        url = f"https://github.com/advisories/GHSA-{i}"
        return _cand(
            id=f"adv{i}",
            title=title,
            source_url=url,
            article_url=url,
            source_rank=rank,
            severity=severity,
            published="2026-07-14",
            **ghsa,
        )

    one = {"batch_priority_max": 1, "batch_priority_per_source": 1}
    staged = [adv(1, "CRITICAL", False, 95.0), adv(2, "CRITICAL", True, 5.0)]
    batch, _ = select_batch.select(staged, conf(1, 0, **one), table)
    assert [c["id"] for c in batch] == ["adv2"]
    staged = [adv(3, "HIGH", True, 95.0), adv(4, "CRITICAL", False, 5.0)]
    batch, _ = select_batch.select(staged, conf(1, 0, **one), table)
    assert [c["id"] for c in batch] == ["adv4"]


def test_false_ai_highs_cannot_starve_the_criticals(sandbox, table):
    """Review of #89: substring keywords ("ml " in "xml ", bare "agent") marked
    HIGH advisories as AI, the lane put them first, and they used up GHSA's
    per-source slots. Built through the real ingestor mapping."""
    rules = common.load_yaml(common.SOURCES_FILE)["classification"]

    def adv(gid, summary, severity):
        raw = {
            "ghsa_id": gid,
            "summary": summary,
            "severity": severity,
            "html_url": f"https://github.com/advisories/{gid}",
            "published_at": "2026-07-14T00:00:00Z",
            "vulnerabilities": [{"package": {"ecosystem": "pip", "name": gid.lower()}}],
        }
        return ingest_ghsa.advisory_to_candidate(raw, rules)

    false_ai = [
        adv("GHSA-x1", "XXE in the xml parser of docgen", "high"),
        adv("GHSA-x2", "Unsafe yaml load in confkit", "high"),
        adv("GHSA-x3", "Spoofed User-Agent header bypasses the rate limit", "high"),
        adv("GHSA-x4", "Data model validation bypass in ormlib", "high"),
    ]
    assert all(c["guess_topic"] == "product-security" for c in false_ai)
    criticals = [
        adv("GHSA-c1", "Remote code execution in webkit", "critical"),
        adv("GHSA-c2", "SSRF in fetchy", "critical"),
    ]
    kev = [
        _cand(
            id=f"kev{i}",
            title=f"CISA KEV entry {i}",
            source_id="kev_json:cisa",
            source_url=f"https://nvd.example/{i}",
            published="2026-07-14",
        )
        for i in range(2)
    ]
    for c in false_ai:  # even if an ingest guess still said AI, the lane ignores it
        c["guess_topic"] = "ai-security"
    staged = [*false_ai, *criticals, *kev, *cands(20, source_id="rss:feed")]
    batch, _ = select_batch.select(staged, conf(8, 4, **LANE), table)
    ids = {c["id"] for c in batch}
    assert {c["id"] for c in criticals} <= ids and {"kev0", "kev1"} <= ids
    assert [c["batch_priority"] for c in batch[:4]].count("ghsa-critical") == 2


def test_without_a_lane_size_the_batch_is_unchanged(sandbox, table):
    plain, _ = select_batch.select(must_not_miss_mix(), conf(8, 4), table)
    assert not any("batch_priority" in c for c in plain)
    assert "adv3" not in [c["id"] for c in plain]  # what W43 looked like: criticals lose


def test_lane_respects_its_size_and_per_source_cap(sandbox, table):
    staged = must_not_miss_mix()
    batch, _ = select_batch.select(staged, conf(1, 1, **LANE), table)
    assert len(batch) == 2 and all(c.get("batch_priority") for c in batch)  # lane <= batch
    one_each = {"batch_priority_max": 9, "batch_priority_per_source": 1}
    batch, _ = select_batch.select(staged, conf(8, 4, **one_each), table)
    lane = [c["batch_priority"] for c in batch if c.get("batch_priority")]
    assert lane == ["ghsa-critical", "kev"]


def test_priority_class_names_only_the_must_not_miss_kinds():
    ghsa = {"source_type": "GHSA"}
    pc = select_batch.priority_class
    assert pc({"source_id": "kev_json:cisa"}) == "kev"
    assert pc({**ghsa, "severity": "critical"}) == "ghsa-critical"
    assert pc({**ghsa, "severity": "HIGH", "prefilter": {"domain_hint": "ais.mcp-tools"}}) == (
        "ghsa-ai"
    )
    assert pc({**ghsa, "severity": "HIGH", "guess_topic": "ai-security"}) is None  # a guess
    assert pc({**ghsa, "severity": "HIGH", "guess_domain": "ais.mcp-tools"}) is None
    assert pc({**ghsa, "severity": "HIGH", "guess_domain": "ps.appsec"}) is None
    moderate_ai = {"severity": "MODERATE", "prefilter": {"domain_hint": "ais.mcp-tools"}}
    assert pc({**ghsa, **moderate_ai}) is None
    assert pc({"severity": "CRITICAL", "source_id": "rss:x"}) is None


def test_class_slots_let_a_class_deal_more_than_one_per_round(sandbox, table):
    staged = realistic_mix()
    batch, _ = select_batch.select(staged, conf(4, 0), table)
    plain = [select_batch.ingestor_class(c) for c in batch]
    batch, _ = select_batch.select(staged, conf(4, 0, batch_class_slots={"rss": 3}), table)
    slotted = [select_batch.ingestor_class(c) for c in batch]
    assert plain.count("rss") == 1 and slotted.count("rss") == 3
    sources = [select_batch.source_key(c) for c in batch]
    assert max(sources.count(s) for s in set(sources)) <= 2  # per-source cap still holds


def curator_links(n: int) -> list[dict]:
    """Curator links: older (the issue's date) and lower-ranked than the mix."""
    return [
        _cand(
            id=f"cur{i}",
            title=f"Curator link number {i} about topiccur{i}",
            source_url=f"https://cur{i}.example/p",
            article_url=f"https://cur{i}.example/p",
            source_id="curator:tldrsec",
            discovered_via="curator",
            curated_by="tldrsec",
            source_rank=30.0,
            published="2026-07-01",
        )
        for i in range(n)
    ]


def test_curator_links_are_their_own_class():
    assert select_batch.ingestor_class({"source_id": "curator:tldrsec"}) == "curator"


def test_the_class_floor_puts_one_or_two_curator_links_in_every_batch(sandbox, table):
    staged = realistic_mix() + curator_links(5)
    lane = {"batch_priority_max": 1, "batch_priority_per_source": 2}  # 3 slots after it

    def curated(**extra) -> int:
        batch, _ = select_batch.select(staged, conf(3, 1, **lane, **extra), table)
        assert len(batch) == 4 and batch[0].get("batch_priority")  # the lane still goes first
        return sum(1 for c in batch if select_batch.ingestor_class(c) == "curator")

    assert curated() == 0  # without the floor they sink under fresher, ranked feeds
    assert curated(batch_class_min={"curator": 1}) == 1
    assert curated(batch_class_min={"curator": 2}) == 2
    assert curated(batch_class_min={"curator": 4}) == 2  # the per-source cap still holds
    real = common.load_config()
    assert real.limits["batch_class_min"] == {"curator": 1}


def test_the_class_floor_never_overfills_the_batch(sandbox, table):
    staged = cands(3) + curator_links(3)
    batch, backlog = select_batch.select(
        staged, conf(1, 0, batch_class_min={"curator": 5}, batch_per_source=5), table
    )
    assert len(batch) == 1 and batch[0]["source_id"] == "curator:tldrsec"
    assert len(batch) + len(backlog) == len(staged)


def test_the_per_source_cap_yields_when_nothing_else_is_left(sandbox, table):
    batch, _ = select_batch.select(cands(10), conf(2, 2), table)  # all one source
    assert len(batch) == 4


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
    size = select_batch.batch_size(common.load_config())
    staged = size + 6
    common.save_candidates(cands(staged))
    assert select_batch.main([]) == 0
    assert len(common.load_candidates()) == size  # neutral posts: no news tier
    backlog = json.loads((sandbox / "data" / "_scan_backlog.json").read_text())
    assert len(backlog) == staged - size
    assert f"SCAN_BATCH: {size} of {staged} candidates selected" in capsys.readouterr().out
    tiers = json.loads((sandbox / "data" / "_scan_tiers.json").read_text())
    assert len(tiers["deep"]) == size and tiers["news"] == {}


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


def test_work_is_a_merge_or_an_applied_same_or_update_verdict(sandbox, on_main):
    on_main()
    assert scan_count.main(["--work"]) == scan_count.NO_WORK
    common.save_json(common.ANALYSIS_OUT, [{"id": "a"}, {"id": "b"}])
    assert scan_count.main(["--work"]) == scan_count.NO_WORK  # written, never merged
    outcomes = sandbox / "data" / "_story_outcomes.md"
    new_only = [{"action": "new", "candidate_id": "x"}]
    outcomes.write_text(story_ledger.outcomes_record(new_only))
    assert scan_count.main(["--work"]) == scan_count.NO_WORK  # `new` alone changed nothing
    same = [{"action": "same", "story_id": "s1", "url": "https://x.example/a"}]
    outcomes.write_text(story_ledger.outcomes_record(same))
    assert scan_count.main(["--work"]) == 0
    outcomes.unlink()
    common.save_json(common.DATA_DIR / common.MERGE_RECORD_NAME, {"merged": 0, "new": 0})
    assert scan_count.main(["--work"]) == scan_count.NO_WORK
    common.save_json(common.DATA_DIR / common.MERGE_RECORD_NAME, {"merged": 1, "new": 0})
    assert scan_count.main(["--work"]) == 0  # an in-place re-merge is analysis too


def test_settled_count_reads_the_code_owned_record():
    outs = [
        {"action": "same", "story_id": "s1", "url": "u1"},
        {"action": "update", "story_id": "s2", "url": "u2"},
        {"action": "new", "candidate_id": "c"},
        {"action": "rejected", "candidate_id": "d", "reason": "r"},
    ]
    assert story_ledger.settled_count(story_ledger.outcomes_record(outs)) == 2
