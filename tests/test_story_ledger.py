"""Tests for scripts/story_ledger.py — the permanent story ledger (ISC-19),
shortlist + judge-verdict plumbing (ISC-20), and the site integrity check
(ISC-21). The judge itself is a model; every test here stubs it with a
written data/story_verdicts.json."""

from __future__ import annotations

import json

import common as c
import content_checks as cc
import generate_html as gh
import generate_site as gs
import merge_analysis as m
import pytest
import replay_stories as rs
import rerank
import story_ledger as sl
from conftest import make_entry
from test_claims import ledger_of, make_claim

import claims

# --- fixtures ------------------------------------------------------------------
ESCAPE_TITLE = "Frontier AI agent escaped its sandbox during a cyber evaluation"
ESCAPE_SUMMARY = (
    "During a cyber-capability evaluation with safety classifiers disabled, a frontier "
    "agent chained a zero-day in the eval host's package proxy to escape the sandbox."
)


def pool_entry(**over) -> dict:
    """A curated, scored pool entry (what merge_analysis leaves behind)."""
    base = make_entry(
        id="e-escape",
        topic="ai-security",
        domain="ais.agents",
        title=ESCAPE_TITLE,
        summary=ESCAPE_SUMMARY,
        source_url="https://lab.example/escape-report",
        article_url="https://lab.example/escape-report",
        published="2026-07-10",
        date="2026-07",
        needs_review=False,
        related_claims=["sandbox-claim"],
        scores={"novelty": 80, "relevance": 85, "newness": 90, "credibility": 60, "composite": 80},
    )
    base.update(over)
    return base


def candidate(**over) -> dict:
    base = {
        "id": "cand-1",
        "title": "Lab confirms its frontier agent escaped an eval sandbox via a proxy zero-day",
        "excerpt": "The lab says its agent escaped the evaluation sandbox through a zero-day "
        "in the package proxy while cyber evaluation classifiers were disabled.",
        "source_url": "https://news.example/agent-escape",
        "article_url": "https://news.example/agent-escape",
        "source_name": "News Site",
        "published": "2026-07-12",
    }
    base.update(over)
    return base


def put_pool(topic: str, entries: list[dict]) -> None:
    pool = c.load_pool(topic)
    pool["entries"].extend(entries)
    c.save_pool(topic, pool)


def ledger_with(entry: dict) -> tuple[dict, str]:
    ledger = sl.empty_ledger()
    sid = sl.create_story(ledger, entry)
    return ledger, sid


def ancient_row() -> dict:
    """A 400-day-old story (FIXED_NOW is 2026-07-15)."""
    row = sl.new_row("An old story from 2025", ["OpenAI"], "2025-06-10")
    row["entry_ids"] = ["gone-entry"]
    row["sources"] = [{"url": "https://old.example/a", "date": "2025-06-10"}]
    return row


# --- ISC-19: the ledger never expires ---------------------------------------
def test_400_day_old_row_survives_every_prune_and_render_path(sandbox, capsys):
    ledger = sl.empty_ledger()
    ledger["stories"]["s-ancient"] = ancient_row()
    sl.save_ledger(ledger)
    put_pool("ai-security", [pool_entry()])
    claims.save_ledger(ledger_of(make_claim()))
    conf = c.load_config()

    rerank.rerank_all(conf)  # prunes pools to the archive, syncs the ledger
    sl.sync_and_save()
    gh.build_payload(claims.load_ledger(), conf, "2026-07-15")
    gs.main()
    (sandbox / "data" / "analysis_out.json").write_text("[]", encoding="utf-8")
    m.main()  # empty analysis: nothing to merge, nothing pruned
    c.save_json(c.DATA_DIR / "story_verdicts.json", [])
    m.main()

    after = sl.load_ledger()["stories"]
    assert after["s-ancient"] == ancient_row()
    assert any("e-escape" in row["entry_ids"] for row in after.values())


def test_round_trip_is_one_line_per_story_and_stable(sandbox):
    ledger = sl.empty_ledger()
    ledger["stories"]["s-b"] = sl.new_row("B", [], "2026-07-02")
    ledger["stories"]["s-a"] = sl.new_row("A", [], "2026-07-01")
    sl.save_ledger(ledger)
    text = (sandbox / "data" / "news_stories.json").read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) == 4 and lines[1].startswith('  "s-a"')  # ordered by first_seen
    assert json.loads(text)["stories"]["s-b"]["title"] == "B"
    sl.save_ledger(sl.load_ledger())
    assert (sandbox / "data" / "news_stories.json").read_text(encoding="utf-8") == text


def test_legacy_index_migrates_and_links_entries_by_url(sandbox):
    legacy = {
        "abc123": {
            "fp": {
                "url": "https://lab.example/escape-report",
                "title": ESCAPE_TITLE,
                "entities": ["OpenAI"],
                "bucket": "2026-07-06",
            },
            "corroborators": [{"url": "https://hn.example/1", "source_name": "HN", "tier": "low"}],
            "winner_tier": "high",
            "first_seen": "2026-07-10",
        }
    }
    (sandbox / "data" / "news_stories.json").write_text(json.dumps(legacy), encoding="utf-8")
    put_pool("ai-security", [pool_entry()])
    sl.sync_and_save()
    row = sl.load_ledger()["stories"]["abc123"]
    assert row["entry_ids"] == ["e-escape"]
    assert [s["url"] for s in row["sources"]][:2] == [
        "https://lab.example/escape-report",
        "https://hn.example/1",
    ]


# --- conservative deterministic assignment ----------------------------------
def test_clear_duplicate_joins_but_paraphrase_and_homepage_do_not():
    ledger, sid = ledger_with(pool_entry())
    dupe = pool_entry(id="e-2", source_url="https://mirror.example/x", published="2026-07-11")
    assert sl.assign_entry(ledger, dupe) == (sid, "duplicate")
    para = pool_entry(id="e-3", title="Model breaks out of test VM", source_url="https://o/y")
    assert sl.assign_entry(ledger, para)[1] == "new"
    # Two different findings that share only a homepage URL stay apart.
    a = pool_entry(id="h-1", title="Alpha result on caches", source_url="https://blog.example/")
    b = pool_entry(id="h-2", title="Beta finding about kernels", source_url="https://blog.example/")
    ledger2 = sl.empty_ledger()
    sl.assign_entry(ledger2, a)
    assert sl.assign_entry(ledger2, b)[1] == "new"


def test_force_new_and_judged_story_override_the_matcher():
    ledger, sid = ledger_with(pool_entry())
    dupe = pool_entry(id="e-2", source_url="https://mirror.example/x")
    new_sid, how = sl.assign_entry(ledger, dupe, force_new=True)
    assert how == "new" and new_sid != sid
    other = pool_entry(id="e-3", title="Unrelated", source_url="https://u/z")
    assert sl.assign_entry(ledger, other, story_id=sid) == (sid, "judged")
    assert sl.assign_entry(ledger, other) == (sid, "known")  # idempotent
    assert sl.check_ledger(ledger) == []


def test_story_ids_are_unique_even_on_seed_collision():
    ledger = sl.empty_ledger()
    a = sl.create_story(ledger, pool_entry(id="x1"))
    b = sl.create_story(ledger, pool_entry(id="x2"))
    assert a != b and b == f"{a}-2"


# --- ISC-20: shortlist ---------------------------------------------------------
def test_shortlist_over_matches_a_paraphrase_and_caps_at_k():
    ledger, sid = ledger_with(pool_entry())
    for i in range(7):
        sl.create_story(
            ledger,
            pool_entry(
                id=f"o-{i}",
                title=f"Frontier agent escaped eval sandbox, take {i}",
                source_url=f"https://o.example/{i}",
                summary="agent sandbox escape eval",
            ),
        )
    by_id = {"e-escape": pool_entry()}
    got = sl.shortlist_many([candidate()], ledger, by_id, window_days=90, k=5)["cand-1"]
    assert len(got) == 5
    assert sid in [row["story_id"] for row in got]


def test_shortlist_url_match_scores_one_and_window_excludes_old():
    ledger, sid = ledger_with(pool_entry())
    same_url = candidate(source_url="https://lab.example/escape-report?utm_source=x", title="zzz")
    got = sl.shortlist_many([same_url], ledger, {}, window_days=90, k=5)["cand-1"]
    assert got[0] == {**got[0], "story_id": sid, "score": 1.0}
    late = candidate(published="2026-12-30")  # 173 days after the story
    assert sl.shortlist_many([late], ledger, {}, window_days=90, k=5)["cand-1"] == []


def test_shortlist_leaves_unrelated_candidates_empty():
    ledger, _ = ledger_with(pool_entry())
    off = candidate(title="Quarterly earnings beat estimates", excerpt="Revenue rose 4%.")
    assert sl.shortlist_many([off], ledger, {}, window_days=90, k=5)["cand-1"] == []


def test_write_shortlist_stages_the_file(sandbox):
    put_pool("ai-security", [pool_entry()])
    c.save_candidates([candidate()])
    assert sl.write_shortlist() == 1
    staged = c.load_json(sandbox / "data" / "story_shortlist.json")
    assert staged["cand-1"][0]["title"] == ESCAPE_TITLE


# --- ISC-20: verdicts (stubbed judge) ------------------------------------------
def _apply(verdict: dict, ledger=None, sid=None):
    if ledger is None:
        ledger, sid = ledger_with(pool_entry())
    v = {"candidate_id": "cand-1", "story_id": sid, **verdict}
    out = sl.apply_verdict(
        ledger, candidate(), v, allowed=[sid], entries_by_id={"e-escape": pool_entry()}
    )
    return ledger, sid, out


def test_verdict_same_adds_a_covering_source_only():
    ledger, sid, out = _apply({"verdict": "same"})
    story = ledger["stories"][sid]
    assert out["action"] == "same"
    assert [s["url"] for s in story["sources"]][-1] == "https://news.example/agent-escape"
    assert story["updates"] == [] and story["entry_ids"] == ["e-escape"]
    assert story["last_updated"] == "2026-07-10"
    _apply({"verdict": "same"}, ledger, sid)  # re-applying is a no-op
    assert len(ledger["stories"][sid]["sources"]) == 2


def test_verdict_update_adds_a_dated_line_moves_up_and_flags_claims():
    ledger, sid, out = _apply({"verdict": "update", "note": "Lab confirms the zero-day."})
    story = ledger["stories"][sid]
    assert out == {**out, "action": "update", "claims_to_review": ["sandbox-claim"]}
    assert story["updates"] == [
        {
            "date": "2026-07-12",
            "note": "Lab confirms the zero-day.",
            "url": "https://news.example/agent-escape",
            "source_name": "News Site",
            "claims_to_review": ["sandbox-claim"],
        }
    ]
    assert story["last_updated"] == "2026-07-12"
    assert len(story["sources"]) == 2


def test_verdict_new_writes_nothing():
    ledger, sid, out = _apply({"verdict": "new"})
    assert out["action"] == "new"
    assert len(ledger["stories"][sid]["sources"]) == 1


@pytest.mark.parametrize(
    "verdict",
    [{"verdict": "same", "story_id": "s-not-shortlisted"}, {"verdict": "maybe"}],
)
def test_bad_verdicts_are_rejected_without_writes(verdict):
    ledger, sid = ledger_with(pool_entry())
    ledger["stories"]["s-not-shortlisted"] = sl.new_row("other", [], "2026-07-01")
    before = json.dumps(ledger, sort_keys=True)
    v = {"candidate_id": "cand-1", "story_id": sid, **verdict}
    out = sl.apply_verdict(ledger, candidate(), v, allowed=[sid])
    assert out["action"] == "rejected"
    assert json.dumps(ledger, sort_keys=True) == before


def _stage_judged_scan(sandbox, verdicts: list[dict]) -> str:
    put_pool("ai-security", [pool_entry()])
    sl.sync_and_save()
    sid = next(iter(sl.load_ledger()["stories"]))
    c.save_candidates(
        [candidate(), candidate(id="cand-2", source_url="https://n/2", title="Other")]
    )
    c.save_json(
        sandbox / "data" / "story_shortlist.json", {"cand-1": [{"story_id": sid}], "cand-2": []}
    )
    c.save_json(
        sandbox / "data" / "story_verdicts.json",
        [{**v, "story_id": v.get("story_id", sid)} for v in verdicts],
    )
    return sid


def test_merge_applies_same_without_a_new_entry(sandbox, capsys):
    sid = _stage_judged_scan(sandbox, [{"candidate_id": "cand-1", "verdict": "same"}])
    assert m.main() == 0  # no analysis_out.json needed when only verdicts landed
    pool = c.load_pool("ai-security")["entries"]
    assert [e["id"] for e in pool] == ["e-escape"]
    # Judge corroboration goes to its own field, never corroborating_sources.
    assert "corroborating_sources" not in pool[0]
    assert pool[0]["story_corroboration"][0]["url"] == "https://news.example/agent-escape"
    assert [x["id"] for x in c.load_candidates()] == ["cand-2"]
    assert not (sandbox / "data" / "story_verdicts.json").exists()
    assert len(sl.load_ledger()["stories"][sid]["sources"]) == 2
    assert "1 same, 0 update, 0 new" in capsys.readouterr().out


def test_merge_applies_update_and_prints_claim_review(sandbox, capsys):
    sid = _stage_judged_scan(
        sandbox, [{"candidate_id": "cand-1", "verdict": "update", "note": "Fixed."}]
    )
    claims.save_ledger(ledger_of(make_claim(id="sandbox-claim")))
    before = (sandbox / "data" / "claims.json").read_text(encoding="utf-8")
    m.main()
    story = sl.load_ledger()["stories"][sid]
    assert story["updates"][0]["note"] == "Fixed."
    assert "CLAIM REVIEW" in capsys.readouterr().out
    # Flagged, never auto-superseded: the claim ledger is untouched.
    assert (sandbox / "data" / "claims.json").read_text(encoding="utf-8") == before


def test_merge_new_verdict_gets_its_own_story_even_if_it_collides(sandbox):
    sid = _stage_judged_scan(sandbox, [{"candidate_id": "cand-1", "verdict": "new"}])
    twin = pool_entry(
        id=None,
        source_url="https://news.example/agent-escape",
        article_url="https://news.example/agent-escape",
        topic="ai-research",
        domain="air.agents",
        published="2026-07-12",
    )
    twin.pop("id")
    (sandbox / "data" / "analysis_out.json").write_text(json.dumps([twin]), encoding="utf-8")
    m.main()
    stories = sl.load_ledger()["stories"]
    assert len(stories) == 2
    assert stories[sid]["entry_ids"] == ["e-escape"]


def test_merge_rejects_a_verdict_outside_the_shortlist(sandbox, capsys):
    _stage_judged_scan(
        sandbox, [{"candidate_id": "cand-2", "verdict": "same", "story_id": "s-anything"}]
    )
    m.main()
    assert "rejected verdict" in capsys.readouterr().err
    assert len(c.load_candidates()) == 2  # nothing settled


# --- ISC-21: one story per row on the site ------------------------------------
def test_duplicate_story_ids_detects_and_check_reports():
    rows = [{"id": "a", "story_id": "s1"}, {"id": "b", "story_id": "s1"}, {"id": "c"}]
    assert cc.duplicate_story_ids(rows) == ["s1"]
    errs = cc.story_id_problems(rows)
    assert any("duplicate story id" in e for e in errs)
    assert any("without story_id" in e for e in errs)
    assert cc.story_id_problems([{"id": "a", "story_id": "s1"}]) == []


def test_site_shows_one_row_per_story_with_also_reported_by(sandbox):
    put_pool(
        "ai-security",
        [
            pool_entry(),
            pool_entry(
                id="e-2",
                source_url="https://mirror.example/x",
                source_name="Mirror",
                scores={**pool_entry()["scores"], "composite": 70},
            ),
        ],
    )
    claims.save_ledger(ledger_of(make_claim()))
    payload = gh.build_payload(claims.load_ledger(), c.load_config(), "2026-07-15")
    rows = payload["findings"] + payload["editorial"]
    assert cc.story_id_problems(rows) == []
    assert [r["id"] for r in payload["findings"]] == ["e-escape"]
    assert payload["findings"][0]["corroborators"][0]["url"] == "https://mirror.example/x"


def test_generate_html_refuses_to_render_duplicate_stories(sandbox, monkeypatch, capsys):
    claims.save_ledger(ledger_of(make_claim()))
    dup = [{"id": "a", "story_id": "s1"}, {"id": "b", "story_id": "s1"}]
    monkeypatch.setattr(
        gh, "build_payload", lambda *a, **k: {"findings": dup, "editorial": [], "claims": []}
    )
    assert gh.main() == 1
    assert "story integrity failed" in capsys.readouterr().out
    assert not (sandbox / "docs" / "index.html").exists()


def test_readme_snapshot_lists_a_story_once(sandbox):
    a = pool_entry()
    b = pool_entry(id="e-2", source_url="https://mirror.example/x")
    put_pool("ai-security", [a, b])
    kept = gs.one_entry_per_story([a, b], c.load_config())
    assert [e["id"] for e in kept] == ["e-escape"]


# --- ISC-21: replay over the real Aug 2026 pool -------------------------------
ESCAPE_IDS = [
    "provider-safety-guardrails-blocked-incident-resp-5fb920778d",
    "openai-and-hugging-face-partner-to-address-secur-08135780c4",
    "oh-my-rogue-agent-87a47d2f7a",
    "the-generator-can-t-be-the-validator-what-openai-d1e4e10746",
    "openai-s-hugging-face-incident-reduces-to-skippe-e7e6b7fd44",
    "anthropic-s-own-cybersecurity-evals-let-three-cl-129f00213b",
    "incident-report-unsanctioned-agent-behaviour-dur-87ffc75167",
    "third-party-cyber-evaluations-involving-openai-m-fc7831cf1c",
    "meta-joins-openai-and-anthropic-on-the-list-of-f-5e4a087057",
    "openai-didn-t-notice-its-ai-agents-using-a-messa-4f8630d341",
]


def test_replay_collapses_the_frontier_agent_escape_coverage(capsys):
    """Real data: every recorded verdict's story was on that entry's shortlist
    (none rejected), and the ten escape entries end up as one story."""
    code = rs.main(
        [
            "--since",
            "2026-07-01",
            "--until",
            "2026-08-31",
            "--verdicts",
            "tests/fixtures/replay_2026-08_judge.json",
            "--expect-one",
            ",".join(ESCAPE_IDS),
        ]
    )
    out = capsys.readouterr().out
    assert code == 0, out
    assert "rejected" not in out
    assert "expect-one: 10 entries -> 1 story(ies): PASS" in out


def test_front_page_news_moves_an_updated_story_back_up():
    from test_generate_html import _run_js

    body = """
    function day(n) { return new Date(Date.now() - n * 864e5).toISOString().slice(0, 10); }
    var rows = [{ id: "fresh", published: day(1) },
                { id: "old-but-updated", published: day(30), updated: day(0) },
                { id: "old", published: day(30) }];
    process.stdout.write(JSON.stringify(frontNews(rows, 7, 30).map(function (r) { return r.id; })));
    """
    assert json.loads(_run_js(["_daysAgo", "frontNews"], body)) == ["old-but-updated", "fresh"]


# --- review fixes: shortlist guard, ledger stability, verdict corroboration, record ---
def test_a_tampered_shortlist_file_cannot_widen_the_guard(sandbox):
    """The model can edit data/story_shortlist.json; merge recomputes it."""
    _stage_judged_scan(sandbox, [])
    ledger = sl.load_ledger()
    ledger["stories"]["s-victim"] = sl.new_row("Unrelated curated story", [], "2026-07-10")
    sl.save_ledger(ledger)
    c.save_json(sandbox / "data" / "story_shortlist.json", {"cand-2": [{"story_id": "s-victim"}]})
    c.save_json(
        sandbox / "data" / "story_verdicts.json",
        [{"candidate_id": "cand-2", "verdict": "same", "story_id": "s-victim"}],
    )
    outcomes = m.apply_story_verdicts()
    assert [o["action"] for o in outcomes] == ["rejected"]
    assert sl.load_ledger()["stories"]["s-victim"]["sources"] == []
    assert len(c.load_candidates()) == 2


def _v2(stories: dict) -> dict:
    return {"version": 2, "stories": stories}


def test_story_membership_holds_main_placements_steady():
    main = _v2({"s1": {"entry_ids": ["a"]}, "s2": {"entry_ids": ["b"]}})
    grown = _v2({"s1": {"entry_ids": ["a", "new"]}, "s2": {"entry_ids": ["b"]}, "s3": {}})
    assert cc.story_membership_problems(main, grown) == []
    collapsed = _v2({"s1": {"entry_ids": ["a", "b"]}, "s2": {"entry_ids": []}})
    assert cc.story_membership_problems(main, collapsed) == ["entry b moved from story s2 to s1"]
    dropped = _v2({"s1": {"entry_ids": ["a"]}})
    probs = cc.story_membership_problems(main, dropped)
    assert "story s2 on main is missing from the PR" in probs
    assert "entry b moved from story s2 to nowhere" in probs
    assert cc.story_membership_problems({"abc": {"fp": {}}}, _v2({})) == []  # legacy main


def test_merge_gate_checks_the_story_ledger(tmp_path, monkeypatch):
    import merge_gate as gate
    from test_merge_gate import _tree

    root = _tree(tmp_path)
    monkeypatch.setattr(gate, "main_ledger", lambda base: {"claims": [{"id": "a"}]})
    monkeypatch.setattr(gate, "main_stories", lambda base: _v2({"s1": {"entry_ids": ["a"]}}))
    (root / "data" / "news_stories.json").write_text(json.dumps(_v2({"s1": {"entry_ids": ["a"]}})))
    assert gate.content_problems("main", root) == []
    (root / "data" / "news_stories.json").write_text(
        json.dumps(_v2({"s1": {"entry_ids": []}, "s9": {"entry_ids": ["a"]}}))
    )
    assert gate.content_problems("main", root) == ["entry a moved from story s1 to s9"]


@pytest.mark.parametrize("name", ["story_shortlist.json", "story_verdicts.json"])
def test_merge_guard_refuses_story_staging_files(name):
    import merge_guard as mg

    assert mg.path_reason(f"data/{name}") is not None


def _lead(**over) -> dict:
    base = {"source_url": "https://lab.example/a", "source_rank": 60}
    base.update(over)
    return base


def test_verdict_corroboration_counts_only_trusted_other_hosts():
    srcs = [
        {"url": "https://news.example/1", "tier": "high"},
        {"url": "https://www.news.example/2", "tier": "medium"},  # same host as above
        {"url": "https://lab.example/b", "tier": "high"},  # the lead's own host
        {"url": "https://hn.example/3", "tier": "low"},
        {"url": "https://other.example/4", "tier": ""},
    ]
    assert c.story_corroboration_count(_lead(story_corroboration=srcs)) == 1
    assert c.credibility_of(_lead(story_corroboration=srcs)) == 65.0
    many = [{"url": f"https://h{i}.example/", "tier": "high"} for i in range(9)]
    assert c.credibility_of(_lead(story_corroboration=many)) == 80.0  # capped at 4


def test_verdict_corroboration_never_lifts_an_hn_only_story():
    conf = c.load_config()
    sources = {"rss:hn": {"id": "rss:hn", "track": "news", "tier": "medium", "scope": "ai"}}
    hn = pool_entry(
        source_id="rss:hn",
        discovered_via="hackernews",
        signals={"hn_points": 50},
        published="2026-07-14",
        story_corroboration=[{"url": "https://big.example/x", "tier": "high"}],
    )
    assert not c.is_news_curated(hn, conf, sources)
    assert not c.is_news_story(hn, conf, sources)
    real = {**hn, "corroborating_sources": [{"url": "https://big.example/x"}]}
    assert c.is_news_curated(real, conf, sources)  # the gate itself still works


def test_outcomes_are_recorded_by_code_and_appended(sandbox):
    sid = _stage_judged_scan(
        sandbox,
        [
            {"candidate_id": "cand-1", "verdict": "update", "note": "Fixed."},
            {"candidate_id": "cand-2", "verdict": "same", "story_id": "s-nope"},
        ],
    )
    m.apply_story_verdicts()
    text = (sandbox / "data" / "_story_outcomes.md").read_text(encoding="utf-8")
    assert "0 same, 1 update, 0 new, 1 rejected" in text
    assert f"- `update`: https://news.example/agent-escape -> story `{sid}`" in text
    assert "CLAIM REVIEW: linked claims sandbox-claim" in text
    assert "- rejected `cand-2`:" in text
    c.save_json(sandbox / "data" / "story_verdicts.json", [{"candidate_id": "x", "verdict": "new"}])
    m.apply_story_verdicts()
    again = (sandbox / "data" / "_story_outcomes.md").read_text(encoding="utf-8")
    assert again.startswith(text) and again.count("### Story verdicts") == 2
