"""The scan's news tier: every relevant news story past the deep batch gets a
short, grounded news brief (select_batch.py, merge_analysis.py, budget.py).

2026-10-23: the run staged ~400 candidates and analyzed 10, cutting PHP2Shell,
Node2Shell, GitLab, PAN-OS and the AI-agent incidents. Rohan: "they are not
sources but the actual relevant news stories that should have been caught
instead of just getting the 10." These fixtures rebuild that shape offline."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import budget
import common
import fetch_raw
import merge_analysis as m
import prefilter
import pytest
import scan_count
import select_batch
import story_ledger as sl
import verify_citations as vc
from test_prefilter import _cand
from test_select_batch import conf

REPO = Path(__file__).resolve().parent.parent
TIER = {
    "max_news_per_run": 10,
    "batch_news_per_source": 3,
    "batch_story_max": 1,
    "batch_story_min_sources": 2,
    "batch_story_any_sources": 4,
    "batch_story_days": 7,
    "batch_story_min_rank": 55,
    "batch_priority_max": 1,
    "batch_priority_per_source": 3,
}
REFERENCE = [{"title": "Old", "summary": "A heap overflow in the parser was patched."}]


def table() -> prefilter.KeywordTable:
    return prefilter.KeywordTable(keywords={"ais.prompt-injection": ("jailbreak",)}, excluded=())


def news(i, title, src, rank=70.0, published="2026-07-14", **over) -> dict:
    base = {
        "id": f"n{i}",
        "title": title,
        "source_url": f"https://{src}.example/{i}",
        "article_url": f"https://{src}.example/{i}",
        "source_id": f"rss:{src}",
        "source_rank": rank,
        "published": published,
    }
    return _cand(**{**base, **over})


def flood(n: int = 12) -> list[dict]:
    """Higher-scoring routine posts that win every deep slot."""
    return [
        _cand(
            id=f"f{i}",
            title=f"Neutral finding number {i} about topic{i}",
            source_url=f"https://flood{i}.example/p",
            source_id=f"rss:flood{i}",
            source_rank=90.0,
            published="2026-07-15",
        )
        for i in range(n)
    ]


def story(tag: str, name: str, n: int) -> list[dict]:
    """One story told by n publishers (shared rare name, an RCE marker)."""
    return [
        news(f"{tag}{k}", f"{name} critical RCE patched in release {k}", f"{tag}pub{k}")
        for k in range(n)
    ]


def kev(i: int) -> dict:
    return _cand(
        id=f"kev{i}",
        title=f"CISA KEV: Vendor{i} flaw CVE-2026-{1000 + i} exploited in the wild",
        source_url=f"https://nvd.example/CVE-2026-{1000 + i}",
        article_url=f"https://nvd.example/CVE-2026-{1000 + i}",
        source_id="kev_json:cisa",
        source_rank=72.0,
        published="2026-07-14",
    )


def tiers(staged, cap=3, margin=0, known=(), **over):
    c = conf(cap, margin, **{**TIER, **over})
    return select_batch.select_tiers(staged, c, table(), reference=REFERENCE, known=list(known))


def ids(rows):
    return [r["id"] for r in rows]


# --- tier selection --------------------------------------------------------------
def staged_day() -> list[dict]:
    return [
        *flood(),
        *story("php", "PhpCore", 3),  # takes the one lane slot
        *story("gl", "GitLabber", 3),  # a second big story: no lane slot left
        kev(1),
        kev(2),  # one priority slot: the other KEV overflows
        news("m1", "Hackers hijack AI agents to exfiltrate credentials", "wire"),
        news("m2", "Critical unauthenticated RCE in WidgetCorp gateway", "wire"),
        news("low", "Critical RCE in Lowcorp router", "smallfeed", rank=40.0),  # under rank 55
        news("gh", "Critical RCE in some repo", "github", source_id="github_query:x"),
        news("old", "Critical RCE in Oldcorp", "wire2", published="2026-07-01"),  # past 7 days
        news("deny", "Widgetco raised $40m after a critical RCE scare", "wire3"),  # puff
        news("plain", "Our quarterly product roundup", "wire4"),  # no marker
    ]


def test_every_relevant_leftover_gets_a_news_slot(sandbox):
    deep, news_tier, backlog = tiers(staged_day())
    assert deep[0]["batch_priority"] == "story" and len(deep) == 3  # one big story leads deep
    lane = deep[0]["id"][:3]  # "ngl" or "nph"
    reasons = {x["id"]: x["batch_news"]["reason"] for x in news_tier}
    other = next(i for i in reasons if i.startswith(("ngl", "nph")))
    assert other[:3] != lane and reasons.pop(other) == "story"  # the second story: one brief
    assert reasons == {"kev2": "kev", "nm1": "marker", "nm2": "marker"}
    assert [x["batch_news"]["reason"] for x in news_tier][:2] == ["story", "kev"]  # order
    assert all(x["batch_tier"] == "news" for x in news_tier)
    left = set(ids(backlog))
    assert {"nlow", "ngh", "nold", "ndeny", "nplain"} <= left


def test_a_story_gets_one_brief_and_its_copies_are_its_coverage(sandbox):
    _, news_tier, backlog = tiers(staged_day())
    brief = next(x for x in news_tier if x["batch_news"]["reason"] == "story")
    tag = brief["id"][1:3]  # "gl" or "ph"
    cover = brief["batch_news"]["coverage"]
    assert len(cover) == 2 and all(r["url"].startswith(f"https://{tag}") for r in cover)
    assert brief["batch_news"]["sources"] == 3 and "rce" in brief["batch_news"]["markers"]
    parked = [x for x in backlog if x["id"].startswith(f"n{tag}")]
    assert len(parked) == 2 and all(x["batch_same_story_as"] == brief["id"] for x in parked)


def test_a_story_the_ledger_holds_never_takes_a_news_slot(sandbox):
    held = [{"title": "GitLabber critical RCE patched", "published": "2026-07-13"}]
    held += [{"title": "PhpCore critical RCE patched", "published": "2026-07-13"}]
    held += [{"title": "WidgetCorp gateway unauthenticated RCE", "published": "2026-07-13"}]
    _, news_tier, _ = tiers(staged_day(), known=held)
    assert {x["id"] for x in news_tier} - {"kev2"} == {"nm1"}  # no held story, no nm2


def test_the_news_cap_and_per_source_cap_bind(sandbox):
    many = [news(f"w{i}", f"Critical RCE in Product{i} gateway", "wire") for i in range(5)]
    other = [news(f"o{i}", f"Critical RCE in Thing{i} server", f"other{i}") for i in range(5)]
    _, news_tier, _ = tiers([*flood(), *many, *other[:2]], max_news_per_run=6)
    assert sum(1 for x in news_tier if x["source_id"] == "rss:wire") == 3  # per-source cap
    assert len(news_tier) == 5
    _, news_tier, _ = tiers([*flood(), *many, *other], max_news_per_run=6)
    assert len(news_tier) == 6  # the run cap
    _, none, _ = tiers([*flood(), *many], max_news_per_run=0)
    assert none == []  # 0 turns the tier off


def test_off_by_default_selection_is_unchanged(sandbox):
    """Without max_news_per_run (code default 0), select() is the old batch."""
    c = conf(4, 0, **{k: v for k, v in TIER.items() if k != "max_news_per_run"})
    batch, _ = select_batch.select(staged_day(), c, table(), reference=REFERENCE, known=[])
    assert len(batch) == 4 and not any(x.get("batch_tier") for x in batch)


def test_main_records_the_tiers_and_the_url_snapshot_covers_both(sandbox, monkeypatch):
    monkeypatch.setattr(prefilter, "load_keywords", lambda path=None: table())
    monkeypatch.setattr(select_batch, "reference_docs", lambda: REFERENCE)
    real = common.load_config()
    lim = {**real.limits, **TIER, "max_stories_per_run": 4, "batch_margin": 0}
    monkeypatch.setattr(common, "load_config", lambda path=None: common.Config(
        **{**real.__dict__, "limits": lim}))  # fmt: skip
    common.save_candidates(staged_day())
    assert select_batch.main([]) == 0
    rec = json.loads((sandbox / "data" / common.SCAN_TIERS_SNAPSHOT).read_text())
    assert len(rec["deep"]) == 4 and set(rec["news"]) & {"kev2", "nm1", "nm2"} == {
        "kev2", "nm1", "nm2"
    }  # fmt: skip
    assert rec["news"]["nm1"]["url"] == "https://wire.example/m1"
    assert fetch_raw.snapshot_urls() == 0
    urls = json.loads((sandbox / "data" / common.SCAN_URL_SNAPSHOT).read_text())
    assert set(rec["news"]) | set(rec["deep"]) == set(urls)  # fetch_raw may fetch every one


# --- the news-brief schema --------------------------------------------------------
SOURCE = (
    "Widgetcorp shipped 4.2.1 on Monday. The flaw lets an unauthenticated attacker run code "
    "on the gateway through a crafted header, and exploitation began last week."
)


def brief(**over) -> dict:
    out = {
        "brief": "news",
        "topic": "product-security",
        "domain": "ps.appsec",
        "title": "Widgetcorp gateway RCE exploited before the patch",
        "source_url": "https://wire.example/m2",
        "article_url": "https://wire.example/m2",
        "takeaway": "Patch Widgetcorp gateways to 4.2.1 now.",
        "summary": "An unauthenticated header bug gives code execution. Attacks began first.",
        "lessons": [
            {
                "point": "Exploited before the fix",
                "excerpt": "exploitation began last week",
                "confidence": 0.9,
            }
        ],
        "published": "2026-07-14",
        "source_id": "rss:wire",
        "raw_path": "data/_raw/nm2.txt",
    }
    out.update(over)
    return out


@pytest.mark.parametrize(
    "over, problem",
    [
        ({"takeaway": ""}, "missing: takeaway"),
        ({"summary": ""}, "missing: summary"),
        ({"scores": {"novelty": 90}}, "must not carry scores"),
        ({"actionable": {"type": "tool"}}, "must not carry actionable"),
        ({"lessons": []}, "exactly one lesson"),
        ({"lessons": [{"point": "a", "excerpt": "x" * 30}] * 2}, "exactly one lesson"),
        ({"lessons": [{"point": "a", "excerpt": "short"}]}, "excerpt under"),
        ({"lessons": [{"point": "", "excerpt": "x" * 30}]}, "needs a point"),
        ({"summary": "One. Two. Three."}, "over 2 sentences"),
    ],
)
def test_news_brief_schema_errors(over, problem):
    assert common.news_brief_errors(brief()) == []
    assert any(problem in e for e in common.news_brief_errors(brief(**over)))


# --- merge: stamping, grounding hold, tier check ------------------------------------
def stage_run(sandbox, text: str = SOURCE) -> None:
    raw = sandbox / "data" / "_raw"
    raw.mkdir(exist_ok=True)
    (raw / "nm2.txt").write_text(text)
    rec = {
        "deep": ["f0"],
        "news": {
            "nm2": {
                "url": "https://wire.example/m2",
                "reason": "story",
                "markers": ["rce", "unauthenticated"],
                "sources": 3,
                "coverage": [
                    {"url": "https://other.example/a", "name": "Other", "published": "2026-07-14"},
                    {"url": "javascript:alert(1)", "name": "Bad", "published": ""},
                ],
            }
        },
    }
    (sandbox / "data" / common.SCAN_TIERS_SNAPSHOT).write_text(json.dumps(rec))


def merged_one(entry: dict) -> tuple[list, list]:
    out, errors, _, _ = m.merge([entry], common.load_config())
    return out, errors


def test_a_grounded_brief_merges_stamped_and_shows_in_the_news_lane(sandbox):
    stage_run(sandbox)
    out, errors = merged_one(brief(grounding_score=None))
    assert errors == [] and len(out) == 1
    e = out[0]
    assert "brief" not in e and e["news_brief"]["reason"] == "story"
    assert e["news_brief"]["markers"] == ["rce", "unauthenticated"]
    assert e["needs_review"] is True  # never a vetted finding
    assert [s["url"] for s in e["corroborating_sources"]] == ["https://other.example/a"]
    assert e["grounding_score"] == 1.0 and e["lessons"][0]["grounded"] is True
    conf, sources = common.load_config(), {}
    assert not common.is_curated(e, conf)
    assert common.news_shown(e, conf, sources) and common.is_news_story(e, conf, sources)


def test_an_ungrounded_brief_is_held_never_published(sandbox):
    stage_run(sandbox)
    forged = brief()
    forged["lessons"][0].update(excerpt="the vendor denies any exploitation at all", grounded=True)
    out, errors = merged_one({**forged, "grounding_score": 1.0})  # analyzer-written verdicts
    assert errors == []
    e = out[0]
    assert e["grounding_score"] == 0.0 and e["lessons"][0]["grounded"] is False
    conf = common.load_config()
    assert not common.news_shown(e, conf, {})
    assert "ungrounded excerpt" in common.review_reason(e, conf, {})  # held in REVIEW.md
    assert not common.is_news_story(e, conf, {})  # and not kept: it ages out


def test_an_unverifiable_brief_is_held(sandbox):
    """No source text (grounding_score null) passes a finding, never a brief."""
    stage_run(sandbox)
    (sandbox / "data" / "_raw" / "nm2.txt").unlink()
    out, _ = merged_one(brief(raw_path=None))
    e = out[0]
    assert e["grounding_score"] is None
    assert not vc.publishable_grounding(e) and not common.news_shown(e, common.load_config(), {})


def test_an_analyzer_written_verdict_never_publishes_an_unverifiable_brief(sandbox):
    """No source text, but the analyzer wrote grounded: true and a 1.0 score:
    merge drops both before the check, so the brief is held."""
    stage_run(sandbox)
    (sandbox / "data" / "_raw" / "nm2.txt").unlink()
    forged = brief(raw_path=None, grounding_score=1.0)
    forged["lessons"][0]["grounded"] = True
    e = merged_one(forged)[0][0]
    assert e["grounding_score"] is None and "grounded" not in e["lessons"][0]
    assert not common.news_shown(e, common.load_config(), {})


@pytest.mark.parametrize(
    "score, verdicts, shown",
    [
        (1.0, [True], True),
        (None, [True], False),  # unverifiable: held even with a lesson verdict
        (1.0, [None], False),  # a lesson never checked
        (1.0, [False], False),
        (0.5, [True], False),
        (1.0, [], False),
    ],
)
def test_a_brief_publishes_only_on_a_confirmed_quote(score, verdicts, shown):
    e = {"news_brief": {}, "grounding_score": score,
         "lessons": [{"excerpt": "x" * 30, "grounded": v} for v in verdicts]}  # fmt: skip
    assert vc.publishable_grounding(e) is shown


def test_a_brief_keeps_its_verdict_when_the_source_is_gone(sandbox):
    stage_run(sandbox)
    e = merged_one(brief())[0][0]
    gone = {**e, "raw_path": None}
    vc.ground_entry(gone)  # a later re-check with no text: verdict kept, not wiped
    assert gone["grounding_score"] == 1.0 and vc.publishable_grounding(gone)


def test_a_brief_outside_the_news_tier_is_rejected(sandbox):
    stage_run(sandbox)
    out, errors = merged_one(brief(source_url="https://elsewhere.example/x", article_url=None))
    assert out == [] and "not in this run's news tier" in errors[0]
    out, errors = merged_one(brief(brief="teaser"))
    assert out == [] and "unknown brief kind" in errors[0]
    (sandbox / "data" / common.SCAN_TIERS_SNAPSHOT).unlink()  # outside a scan: no tier
    out, errors = merged_one(brief())
    assert out == [] and errors


def test_a_deep_entry_cannot_claim_the_news_brief_stamp(sandbox):
    from conftest import make_entry

    stage_run(sandbox)
    forged = make_entry(news_brief={"reason": "story"}, source_url="https://wire.example/m2")
    out, _ = merged_one(forged)
    assert not common.is_news_brief(out[0])


def test_briefs_never_count_toward_source_hit_rates(sandbox, monkeypatch):
    seen = {}
    monkeypatch.setattr(m.sr, "update_stats", lambda d: seen.update(d))
    m.update_source_hit_rate([{"source_id": "rss:wire", "news_brief": {}}])
    assert seen == {}


# --- one story, both tiers -----------------------------------------------------------
def test_a_news_tier_copy_of_a_held_story_is_shortlisted_and_settled_as_same(sandbox):
    """Ledger dedupe spans the tiers: a deep entry merged earlier is offered to a
    news-tier copy of the same story, and the judge's `same` folds it in."""
    entry = brief(title="Widgetcorp gateway RCE CVE-2026-4242 exploited", id="deep-1")
    entry.pop("brief")
    ledger = sl.empty_ledger()
    sl.assign_entry(ledger, entry, window_days=90)
    sl.save_ledger(ledger)
    copy = news("cp", "Attackers exploit CVE-2026-4242 in gateways", "wire9", batch_tier="news")
    rows = sl.shortlist_many([copy], ledger, {"deep-1": entry}, window_days=90, k=5)["ncp"]
    assert [r["story_id"] for r in rows] == list(ledger["stories"])
    verdict = [{"candidate_id": "ncp", "verdict": "same", "story_id": rows[0]["story_id"]}]
    out = sl.apply_verdicts(ledger, verdict, [copy], {"ncp": rows}, entries_by_id={})
    assert out[0]["action"] == "same"
    srcs = next(iter(ledger["stories"].values()))["sources"]
    assert "https://wire9.example/cp" in {s["url"] for s in srcs}


# --- caps --------------------------------------------------------------------------
def test_scan_count_counts_briefs_apart_from_stories(sandbox, monkeypatch):
    monkeypatch.setattr(common, "main_entry_ids", lambda: set())
    monkeypatch.setattr(scan_count, "main_archive_ids", lambda: set())
    pool = {"topic": "ai-security", "entries": [{"id": "d1"}, {"id": "b1", "news_brief": {}}]}
    common.save_pool("ai-security", pool)
    common.save_json(common.ANALYSIS_OUT, [{"t": 1}, brief(), brief(), brief()])
    assert scan_count.counts() == (1, 3)


def row(run_id, cost, stories, news=0, kind="actual"):
    r = {"run_id": run_id, "date": "2026-07-14", "runner": "local", "kind": kind,
         "stories": stories, "cost_usd": cost}  # fmt: skip
    return {**r, "news": news} if news else r


def settings(**over):
    base = {"monthly_cap_usd": 400, "usd_per_story": None, "calibration_runs": 5,
            "ceiling_headroom": 1.5, "uncalibrated_run_usd": 5, "max_stories_per_run": 25,
            "max_news_per_run": 50, "news_cost_ratio": 0.3, "max_turns": 300}  # fmt: skip
    return {**base, **over}


def test_the_ceiling_prices_both_tiers_in_story_units():
    runs = [row("a", cost=8.0, stories=25, news=50)]  # 25 + 0.3 x 50 = 40 units: $0.20/unit
    assert budget.run_units(runs[0], 0.3) == 40
    ceiling, why = budget.run_ceiling(runs, settings(), "cloud")
    assert why == "calibrated" and ceiling == pytest.approx(0.2 * 1.5 * 40)
    assert budget.run_ceiling(runs, settings(max_news_per_run=0), "cloud")[0] == pytest.approx(
        8.0 / 25 * 1.5 * 25
    )  # no news tier: a deep-only ceiling (news priced at nothing)


def test_calibration_clamps_both_counts_to_their_caps():
    padded = [row("p", cost=8.0, stories=25, news=500)]  # 500 briefs: post refuses over 50
    rate = budget.usd_per_story(padded, max_stories=25, ratio=0.3, max_news=50)
    assert rate == pytest.approx(8.0 / 40)
    one_row = [row("x", 4.0, 10, news=10), row("x", 8.0, 25, news=50)]  # one row per run
    assert budget.usd_per_story(one_row, ratio=0.3, max_news=50) == pytest.approx(0.2)


def test_a_missing_ratio_prices_a_brief_like_a_story():
    assert budget.news_ratio({}) == 1.0 and budget.news_ratio({"news_cost_ratio": 0.3}) == 0.3


def test_ledger_rows_validate_the_news_count():
    budget.validate_row(row("a", 1.0, 2, news=3))
    for bad in (-1, 1.5, True, "3"):
        with pytest.raises(budget.LedgerError):
            budget.validate_row({**row("a", 1.0, 2), "news": bad})


def test_actual_records_news_and_the_report_shows_it(tmp_path):
    path = tmp_path / "ledger.json"
    runs = [row("r1", 0, 0, kind="reserve")]
    args = type("A", (), {"run_id": "r1", "stories": 20, "cost_usd": 6.0, "news": 30,
                          "outcome": None})()  # fmt: skip
    budget.actual(path, runs, args)
    assert runs[-1]["news"] == 30
    assert "20 + 30 news" in budget.spend_report(runs, settings(), "2026-07")


LEDGER_10_23 = [  # the measured runs on the budget ledger when the tiers shipped
    row("10-19", cost=1.33, stories=3),  # the worst recent rate: $0.443/story
    row("10-22", cost=1.67, stories=8),
    row("10-23", cost=2.32, stories=10),  # the latest: $0.232/story
]


def test_real_config_session_cap_clears_a_full_two_tier_run():
    """--max-budget-usd must not kill a full 25 deep + 80 brief run: it clears
    one at the latest measured rate, and at the worst recent rate with briefs
    priced at the pessimistic ratio (0.5, not the 0.3 estimate)."""
    s = budget.budget_settings()
    deep, briefs = s["max_stories_per_run"], s["max_news_per_run"]
    assert (deep, briefs) == (25, 80) and s["monthly_cap_usd"] == 600
    cap, why = budget.session_budget(LEDGER_10_23, s, "local")
    assert why == "calibrated"
    latest, worst = 2.32 / 10, 1.33 / 3
    pessimistic = budget.session_ratio(s)
    assert pessimistic == 0.5 > budget.news_ratio(s)
    assert cap >= latest * (deep + budget.news_ratio(s) * briefs)
    assert cap >= worst * (deep + pessimistic * briefs)
    assert s["max_turns"] >= 4 * deep + 1.5 * briefs + 50  # the turn estimate in config
    # ...and a month of cloud ceilings at the 2026-10-22 rate still fits the cap
    ceiling, _ = budget.run_ceiling([row("m", cost=1.6749, stories=8)], s, "cloud")
    assert 31 * ceiling <= s["monthly_cap_usd"]


def test_the_session_ratio_never_undercuts_the_estimate():
    assert budget.session_ratio({"news_cost_ratio": 0.3}) == 0.3  # unset: the estimate
    assert budget.session_ratio({"news_cost_ratio": 0.6, "session_news_ratio": 0.5}) == 0.6
    s = settings(session_news_ratio=0.5, session_cap_fraction=0.8)
    runs = [row("a", cost=8.0, stories=25, news=50)]  # $0.20/unit
    assert budget.session_budget(runs, s, "local")[0] == round(0.2 * 1.5 * (25 + 0.5 * 50) * 0.8, 2)
    assert budget.run_ceiling(runs, s, "local")[0] == pytest.approx(0.2 * 1.5 * 40)  # reserve


# --- containment ---------------------------------------------------------------------
def allowed_tools() -> list[str]:
    out = subprocess.run(
        ["bash", "-c", 'source scripts/scan_containment.sh; printf "%s\\n" "${ALLOWED_TOOLS[@]}"'],
        cwd=REPO, capture_output=True, text=True, check=True,
    )  # fmt: skip
    return out.stdout.splitlines()


def test_containment_allows_exactly_the_named_scripts():
    """The news tier needs no new tool: briefs are fetched with fetch_raw.py,
    merged, grounded and readability-checked by the scripts already allowed."""
    tools = allowed_tools()
    assert tools == [
        "Read", "Glob", "Grep", "Task", "Edit(data/**)",
        "Bash(python scripts/fetch_raw.py *)",
        "Bash(python scripts/merge_analysis.py)", "Bash(python scripts/verify_citations.py)",
        "Bash(python scripts/importance.py *)", "Bash(python scripts/promote_editorial.py)",
        "Bash(python scripts/readability.py --analysis)",
    ]  # fmt: skip
    for rule in (t for t in tools if t.startswith("Bash(")):
        assert re.fullmatch(r"Bash\(python scripts/[a-z_]+\.py( [^*]+| \*)?\)", rule), rule
    text = (REPO / "scripts/scan_containment.sh").read_text()
    assert '"Edit(data/_scan*)"' in text  # the tier record is session-proof


def test_post_refuses_more_briefs_than_the_news_cap(scan_repo):
    """post caps the news tier apart from the deep tier: 2 briefs over a cap of
    1 fail the run, with 0 deep stories (so the story cap can't be what fired)."""
    from test_run_scan import merged, open_budget, run_scan

    work, _, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", usd_per_story="0.25", max_news_per_run="1")
    assert run_scan(work, env, "pre", SCAN_RUN_ID="C1").returncode == 0
    (work / "data/analysis_out.json").write_text(json.dumps([brief(), brief()]))
    merged(work, 2)
    res = run_scan(work, env, "post")
    assert res.returncode != 0
    log = (work / "data/_scan.log").read_text()
    assert "wrote 2 news briefs, over the per-run cap of 1" in log
    assert "over the per-run cap of 10" not in log


def test_news_reason_refuses_deny_listed_text_even_past_the_prefilter():
    """prefilter.bucket drops deny-list hits before selection; news_reason
    checks again, so a caller that skips bucketing can't brief stock noise."""
    c = conf(3, 0, **TIER)
    sig = select_batch.nw.Signal(markers=frozenset({"rce"}), matches=(), sources=1)
    ok = news("ok", "Critical RCE in WidgetCorp gateway", "wire")
    puff = news("puff", "Widgetco raised $40m after a critical RCE scare", "wire")
    assert select_batch.news_reason(ok, sig, None, c) == "marker"
    assert select_batch.news_reason(puff, sig, None, c) is None


def test_the_news_tier_has_its_own_rank_floor(sandbox):
    """A brief needs batch_news_min_rank (The Register 49, Dark Reading 40
    qualify); the big-story lane keeps batch_story_min_rank; unset falls back."""
    sig = select_batch.nw.Signal(markers=frozenset({"compromise"}), matches=(), sources=1)
    dr = news("dr", "Hackers abuse AI pen-test tool Cairn in a compromise spree", "dr", rank=40.0)
    low = news("low", "Hackers abuse AI pen-test tool Cairn in a compromise spree", "x", rank=39.0)
    c = conf(3, 0, **{**TIER, "batch_news_min_rank": 40})
    assert select_batch.news_reason(dr, sig, None, c) == "marker"
    assert select_batch.news_reason(low, sig, None, c) is None
    assert select_batch.news_reason(dr, sig, None, conf(3, 0, **TIER)) is None  # lane's 55
    real = common.load_config().limits
    assert (real["batch_news_min_rank"], real["batch_story_min_rank"]) == (40, 55)


def test_a_story_carries_a_marker_any_of_its_copies_carries(sandbox):
    """2026-10-23 PAN-OS: only The Register's headline said "under attack"."""
    copies = [  # THN is the best-covered copy (3 publishers) and has no marker itself
        news("thn", "Qilin groups exploit PanCorpX flaw to bypass MFA", "thn"),
        news("reg", "PanCorpX firewall OS under attack from ransomware", "reg", rank=49.0,
             published="2026-07-12"),
        news("blog", "PanCorpX MFA bypass: notes from the field", "blog", published="2026-07-15"),
    ]  # fmt: skip
    _, news_tier, _ = tiers([*flood(), *copies], batch_story_max=0, batch_marker_bonus=0.01)
    assert [x["batch_news"]["reason"] for x in news_tier] == ["story"]
    assert news_tier[0]["batch_news"]["markers"] == ["exploited"]


def test_one_two_word_name_is_not_two_shared_names():
    """The PAN-OS over-merge: a BeyondTrust roundup naming "Palo Alto" in its
    body shared "palo" + "alto" with PAN-OS news, which counted as two names."""
    nw = select_batch.nw
    ref = [{"title": f"Old {i}", "summary": "Nothing to see."} for i in range(3)]
    dr = {"title": "BeyondTrust Remote Support Zero-Day Continues Trend of Exploited Edge Bugs",
          "excerpt": "Attackers hit BeyondTrust, Cisco and Palo Alto edge devices.",
          "published": "2026-10-16"}  # fmt: skip
    reg = {"title": "Palo Alto's firewall OS has been under attack from ransomware groups",
           "excerpt": "Several gangs hit Palo Alto firewalls.", "published": "2026-10-20"}  # fmt: skip
    model = nw.name_model(ref, [dr, reg])
    a, b = (nw.profile(d, model) for d in (dr, reg))
    assert {"palo", "alto"} <= a.names & b.names
    assert not nw.same_story(a, b)


def test_a_corporate_suffix_is_not_a_name():
    """praetorian-inc/augustus joined the INC-ransomware PAN-OS story on "inc"."""
    model = select_batch.nw.name_model([], [{"title": "Qilin and INC ransomware LLC"}])
    assert model.shaped >= {"inc", "llc"}  # all-caps: a name by shape alone
    assert not model.is_name("inc") and not model.is_name("llc")


def test_the_backfill_campaign_fits_the_two_tier_ceiling():
    """Rohan 2026-10-23: backfill.max_usd 200, so all 5 chunks fit at the worst
    recent rate (the 10-19 run, $1.33 for 3 stories) before any is measured."""
    s = budget.budget_settings()
    ceiling, _ = budget.run_ceiling([row("w", cost=1.33, stories=3)], s, "local")
    assert s["backfill"]["max_runs"] == 6
    assert 5 * ceiling <= s["backfill"]["max_usd"] == 200


# --- retention: briefs don't accumulate forever -------------------------------------
def pooled_brief(title: str, published: str, grounded: bool = True) -> dict:
    return {
        "id": title.lower().replace(" ", "-"),
        "topic": "product-security",
        "domain": "ps.appsec",
        "title": title,
        "source_url": f"https://wire.example/{title.lower().replace(' ', '-')}",
        "takeaway": "Patch it.",
        "summary": "A bug was exploited.",
        "published": published,
        "needs_review": True,
        "news_brief": {"reason": "marker"},
        "grounding_score": 1.0 if grounded else 0.0,
        "lessons": [{"point": "p", "excerpt": "x" * 30, "grounded": grounded}],
    }


def test_briefs_age_out_and_grounded_ones_archive_after_brief_news_days(sandbox):
    """Clock: 2026-07-15. max_age_days 31, brief_news_days 60."""
    import generate_html
    import rerank
    from conftest import make_entry

    sources = [{"id": "rss:news", "name": "News", "tier": "high", "track": "news"}]
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
    pool = common.load_pool("product-security")
    pool["entries"] = [
        pooled_brief("Held old", "2026-06-01", grounded=False),  # 44 days, held: ages out
        pooled_brief("Held fresh", "2026-07-10", grounded=False),  # inside max_age_days
        pooled_brief("Grounded 44 days", "2026-06-01"),  # kept as news (< 60)
        pooled_brief("Grounded 75 days", "2026-05-01"),  # past 60: archived
        make_entry(topic="product-security", domain="ps.appsec", title="Old news story",
                   source_url="https://n.example/old", source_id="rss:news",
                   published="2026-01-01"),  # fmt: skip
    ]
    common.save_pool("product-security", pool)
    conf = common.load_config()
    assert conf.limits["brief_news_days"] == 60
    rerank.rerank_pool("product-security", conf)
    live = sorted(e["title"] for e in common.load_pool("product-security")["entries"])
    assert live == ["Grounded 44 days", "Held fresh", "Old news story"]  # news story unchanged
    archive = common.load_json(common.ARCHIVE_FILE, default=[])
    assert sorted(e["title"] for e in archive) == ["Grounded 75 days", "Held old"]
    rerank.rerank_pool("product-security", conf)  # not pulled back as news
    assert len(common.load_pool("product-security")["entries"]) == 3
    shown = [r["title"] for r in generate_html.archive_rows(archive, conf)]
    assert shown == ["Grounded 75 days"]  # on the Archive tab; the held one never published


# --- a brief is bound to its tier record --------------------------------------------
def test_a_brief_citing_another_url_under_a_real_candidate_id_is_rejected(sandbox):
    stage_run(sandbox)
    forged = brief(id="nm2", source_url="https://attacker.example/x", article_url=None)
    out, errors = merged_one(forged)
    assert out == [] and "is not its news-tier candidate's URL" in errors[0]


def test_stamp_takes_urls_and_raw_text_from_the_run_not_the_analyzer(sandbox):
    stage_run(sandbox)
    tampered = brief(article_url="https://elsewhere.example/page", raw_path="data/_raw/other.txt")
    e = merged_one(tampered)[0][0]
    assert (e["source_url"], e["article_url"]) == ("https://wire.example/m2",) * 2
    assert e["raw_path"] == "data/_raw/nm2.txt" and e["grounding_score"] == 1.0


# --- a capped session still ships what it merged -------------------------------------
@pytest.mark.parametrize("subtype", ["error_max_budget_usd", "error_max_turns"])
def test_a_session_stopped_by_its_cap_still_posts_its_partial_run(scan_repo, tmp_path, subtype):
    from test_run_scan import ledger_rows, open_budget
    from test_run_scan_local import run_local

    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, _ = run_local(work, env, tmp_path, rc=1, FAKE_SUBTYPE=subtype, FAKE_ANALYSIS="1",
                       FAKE_TOUCH="1")  # fmt: skip
    assert res.returncode == 0, res.stdout + res.stderr
    rows = [(r["kind"], r.get("outcome")) for r in ledger_rows(origin)]
    assert rows == [("reserve", None), ("actual", "session-capped"), ("done", None)]
    assert "stopped by its cap" in (work / "data/_scan.log").read_text()


def test_a_capped_session_that_merged_nothing_fails_analysis_empty(scan_repo, tmp_path):
    from test_run_scan import ledger_rows, open_budget
    from test_run_scan_local import run_local

    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0", retry_max_usd="0.1")
    res, _ = run_local(work, env, tmp_path, rc=1, FAKE_SUBTYPE="error_max_turns")
    assert res.returncode != 0
    actual = [r for r in ledger_rows(origin) if r["kind"] == "actual"]
    assert [r.get("outcome") for r in actual] == ["analysis-empty"]  # post ran and judged it


def test_any_other_session_failure_still_skips_post(scan_repo, tmp_path):
    from test_run_scan import ledger_rows, open_budget
    from test_run_scan_local import run_local

    work, origin, env = scan_repo
    open_budget(work, monthly_cap_usd="10.0", uncalibrated_run_usd="2.0")
    res, _ = run_local(work, env, tmp_path, rc=1, FAKE_SUBTYPE="error_during_execution",
                       FAKE_ANALYSIS="1")  # fmt: skip
    assert res.returncode != 0
    assert [r["kind"] for r in ledger_rows(origin)] == ["reserve", "actual"]  # no post
