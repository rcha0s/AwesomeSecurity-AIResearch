"""The big-story lane and newsworthiness bonus in scripts/select_batch.py.

2026-10-23: PHP2Shell was staged from six registered feeds, and every copy
ranked 50th or worse of 393, below a flood of fresher, higher-ranked routine
posts. These fixtures rebuild that shape offline: a story told by several
low-ranked sources against many higher-scoring single-source items."""

from __future__ import annotations

import common
import select_batch
from test_prefilter import _cand
from test_select_batch import cands, conf, table  # noqa: F401  (fixture)

STORY = {
    "batch_story_max": 2,
    "batch_story_min_sources": 2,
    "batch_story_any_sources": 4,
    "batch_story_days": 7,
}
BONUS = {"batch_marker_bonus": 4, "batch_corroboration_bonus": 3}
REFERENCE = [{"title": "Old", "summary": "A heap overflow in the parser was patched."}]


def copy(i: int, title: str, src: str, rank: float = 35.0, **over) -> dict:
    return _cand(
        id=f"php{i}",
        title=title,
        source_url=f"https://{src}.example/php",
        article_url=f"https://{src}.example/php",
        source_id=f"rss:{src}",
        source_rank=rank,
        published="2026-07-14",
        **over,
    )


def php2shell() -> list[dict]:
    """Six sources, two posts from one of them, the most credible one ranked 60."""
    return [
        copy(0, "PHP patches two critical unauthenticated RCEs", "snyk"),
        copy(1, "Two critical RCEs in PHP core", "talos", rank=60.0),
        copy(2, "Hackers exploited the PHP vulnerabilities before the patch", "wired"),
        copy(3, "Today's PHP security release", "simon"),
        copy(4, "If you run Apache with mod_php, patch now", "semgrep", rank=30.0),
        copy(5, "PHP blames Chainguard for the disclosure", "register"),
        copy(6, "Our PHP RCE detection rules", "semgrep", rank=30.0),
    ]


def flood(n: int = 30) -> list[dict]:
    """Higher-scoring routine posts, one source each, on unrelated subjects."""
    return [
        _cand(
            id=f"f{i}",
            title=f"Neutral finding number {i} about topic{i}",
            source_url=f"https://flood{i}.example/p",
            source_id=f"rss:flood{i}",
            source_rank=80.0,
            published="2026-07-15",
        )
        for i in range(n)
    ]


def run(staged, cap=4, margin=1, known=(), **extra):
    c = conf(cap, margin, **extra)
    return select_batch.select(staged, c, table_(), reference=REFERENCE, known=list(known))


def table_():
    import prefilter

    return prefilter.KeywordTable(keywords={"ais.prompt-injection": ("jailbreak",)}, excluded=())


def ids(rows):
    return [r["id"] for r in rows]


def test_without_the_lane_the_story_loses_to_the_flood(sandbox):
    batch, _ = run(php2shell() + flood())
    assert not any(i.startswith("php") for i in ids(batch))


def test_a_big_story_takes_one_lane_slot_first(sandbox):
    staged = php2shell() + flood()
    batch, backlog = run(staged, **STORY, batch_story_min_rank=55)
    assert ids(batch)[0] == "php1"  # the most credible copy (Talos, rank 60) leads
    assert batch[0]["batch_priority"] == "story"
    story = batch[0]["batch_story"]
    assert story["sources"] == 6 and {"critical", "rce"} <= set(story["markers"])
    assert len(story["coverage"]) >= 4  # the other copies' URLs ride along
    assert sum(1 for i in ids(batch) if i.startswith("php")) == 1  # one slot per story
    same = {r["id"]: r.get("batch_same_story_as") for r in backlog if r["id"].startswith("php")}
    assert same and set(same.values()) == {"php1"}  # every copy waits behind the head
    assert sorted(ids(batch + backlog)) == sorted(ids(staged))  # nothing lost


def test_a_story_the_ledger_holds_takes_no_lane_slot(sandbox):
    known = [{"title": "Two critical RCEs in PHP core", "published": "2026-07-13"}]
    batch, _ = run(php2shell() + flood(), known=known, **STORY)
    assert not any(r.get("batch_priority") == "story" for r in batch)


def test_an_old_story_takes_no_lane_slot(sandbox):
    old = [{**c, "published": "2026-07-01"} for c in php2shell()]
    batch, _ = run(old + flood(), **STORY)
    assert not any(r.get("batch_priority") == "story" for r in batch)
    batch, _ = run(old + flood(), **{**STORY, "batch_story_days": 30})
    assert batch[0]["batch_priority"] == "story"


def test_two_sources_without_a_marker_are_not_a_big_story(sandbox):
    calm = [
        copy(0, "PHP release notes for 8.6", "snyk"),
        copy(1, "What is new in PHP 8.6", "talos"),
    ]
    batch, _ = run(calm + flood(), **STORY)
    assert not any(r.get("batch_priority") == "story" for r in batch)


def test_the_lane_respects_its_size_and_the_per_source_cap(sandbox):
    second = [
        _cand(id=f"gl{i}", title=t, source_url=f"https://{s}.example/gl", source_id=f"rss:{s}",
              source_rank=35.0, published="2026-07-14")
        for i, (t, s) in enumerate([
            ("GitLab max-severity RCE in the importer", "talos"),
            ("Critical GitLab flaw allows unauthenticated RCE", "wired"),
        ])
    ]  # fmt: skip
    staged = php2shell() + second + flood()
    batch, _ = run(staged, **{**STORY, "batch_story_max": 1})
    assert [r.get("batch_priority") for r in batch].count("story") == 1
    batch, _ = run(staged, per_source=1, **STORY)
    heads = [r for r in batch if r.get("batch_priority") == "story"]
    assert len(heads) == 2 and len({select_batch.source_key(r) for r in heads}) == 2
    batch, _ = run(staged, cap=0, margin=1, **{**STORY, "batch_story_max": 5})
    assert len(batch) == 1  # the lane never overfills the batch


def test_copies_of_any_shared_story_wait_behind_one_head(sandbox):
    calm = [
        copy(0, "PHP release notes for 8.6", "snyk", rank=90.0),
        copy(1, "What is new in PHP 8.6", "talos", rank=90.0),
    ]
    batch, backlog = run(calm + flood(3), cap=9, **STORY)
    assert sum(1 for i in ids(batch) if i.startswith("php")) == 1
    assert any(r.get("batch_same_story_as") for r in backlog)


def test_groups_absorb_what_matches_half_the_group_never_a_chain():
    import newsworthy as nw

    pool = [{"id": str(i), "source_rank": 50.0} for i in range(5)]
    matches = {0: (1, 2, 3), 1: (0, 2, 3), 2: (0, 1), 3: (0, 1, 4), 4: (3,)}
    sigs = [nw.Signal(frozenset({"rce"}), matches[i], 1 + len(matches[i])) for i in range(5)]
    pos = {id(x): i for i, x in enumerate(pool)}
    groups = select_batch.story_groups(pool, sigs, pos)
    assert sorted(groups[0]) == [0, 1, 2, 3]  # 4 matches only one of the four
    assert [4] not in groups  # and is alone, so it is no story


def test_an_untagged_article_cannot_bridge_two_different_cves():
    """Review F2: A names CVE-1111, B names CVE-2222, C names neither and matches
    both. B must not be parked as "same" as A's story."""
    import newsworthy as nw

    pool = [{"id": x, "source_rank": 50.0} for x in "ABC"]
    ids = {0: {"cve-2026-1111"}, 1: {"cve-2026-2222"}, 2: set()}
    matches = {0: (2,), 1: (2,), 2: (0, 1)}
    sigs = [nw.Signal(frozenset({"rce"}), matches[i], 3 if i == 2 else 2, ids=frozenset(ids[i]))
            for i in range(3)]  # fmt: skip
    pos = {id(x): i for i, x in enumerate(pool)}
    groups = select_batch.story_groups(pool, sigs, pos)
    assert not any({0, 1} <= set(g) for g in groups)


def test_one_story_with_two_cves_still_groups():
    import newsworthy as nw

    pool = [{"id": x, "source_rank": 50.0} for x in "ABC"]
    ids = {0: {"cve-1", "cve-2"}, 1: {"cve-2"}, 2: set()}
    matches = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    sigs = [nw.Signal(frozenset({"rce"}), matches[i], 3, ids=frozenset(ids[i])) for i in range(3)]
    pos = {id(x): i for i, x in enumerate(pool)}
    assert [sorted(g) for g in select_batch.story_groups(pool, sigs, pos)] == [[0, 1, 2]]


def test_end_to_end_two_cves_and_a_bridge_stay_two_stories(sandbox):
    a = copy(0, "Citrix NetScaler pre-auth RCE (CVE-2026-1111)", "watchtowr", rank=70.0)
    b = copy(1, "Citrix NetScaler memory overflow RCE (CVE-2026-2222)", "talos", rank=70.0)
    bridge = copy(2, "Citrix NetScaler under attack: patch now", "register", rank=60.0)
    batch, backlog = run([a, b, bridge] + flood(), cap=6, **STORY)
    parked = {r["id"]: r.get("batch_same_story_as") for r in backlog}
    assert not (parked.get("php1") == "php0" or parked.get("php0") == "php1")


def test_attacker_repos_take_no_lane_slot(sandbox):
    repos = [
        _cand(id=f"r{i}", title=f"zorbex/frobnicate{i}: unauthenticated FrobServer RCE exploit",
              source_url=f"https://github.com/zorbex/frobnicate{i}", source_id=f"github_query:q{i}",
              discovered_via="github", source_rank=75.0, published="2026-07-14")
        for i in range(2)
    ]  # fmt: skip
    batch, _ = run(repos + flood(), **STORY, batch_story_min_rank=55)
    assert not any(r.get("batch_priority") == "story" for r in batch)


def test_two_low_rank_feeds_take_no_lane_slot_under_the_rank_floor(sandbox):
    low = [
        copy(0, "PHP patches two critical unauthenticated RCEs", "low1", rank=40.0),
        copy(1, "Two critical RCEs in PHP core", "low2", rank=49.0),
    ]
    batch, _ = run(low + flood(), **STORY, batch_story_min_rank=55)
    assert not any(r.get("batch_priority") == "story" for r in batch)
    batch, _ = run(low + flood(), **STORY, batch_story_min_rank=45)
    assert batch[0]["batch_priority"] == "story"


def test_markers_and_corroboration_lift_a_candidate_in_the_deal(sandbox):
    one = {"source_id": "rss:one"}  # one source: pure score order
    plain = _cand(id="plain", title="A neutral finding", source_url="https://p.ex/1",
                  source_rank=60.0, published="2026-07-15", **one)  # fmt: skip
    severe = _cand(id="severe", title="Unauthenticated RCE in the router",
                   source_url="https://s.ex/1", source_rank=40.0, published="2026-07-15", **one)  # fmt: skip
    batch, _ = run([plain, severe], cap=1, margin=0, per_source=9)
    assert ids(batch) == ["plain"]  # 60 vs 40 rank: 3 composite points apart
    batch, _ = run([plain, severe], cap=1, margin=0, per_source=9, **BONUS)
    assert ids(batch) == ["severe"]  # +4 for its markers


def test_real_config_turns_the_lane_on():
    real = common.load_config().limits
    assert real["batch_story_max"] == 4 and real["batch_priority_max"] == 4
    assert real["batch_story_min_sources"] == 2 and real["batch_story_any_sources"] == 4
    assert real["batch_story_min_rank"] == 55
    assert real["batch_marker_bonus"] == 4 and real["batch_corroboration_bonus"] == 3
    assert select_batch.story_signals_on(common.load_config())
