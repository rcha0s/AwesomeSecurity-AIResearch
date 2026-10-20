"""Tests for scripts/eval_golden.py (ISC-23) — deterministic scoring of an analyzer run."""

from __future__ import annotations

import json

import common
import eval_golden as eg
import pytest
from conftest import make_entry

TOPICS = ("harness permission bypass", "sandbox egress leak", "tool schema regression",
          "memory poisoning", "eval contamination", "context compaction", "token cost",
          "judge reliability", "retrieval drift", "skill marketplace", "planner split")  # fmt: skip


def title(cid: str) -> str:
    """Distinct titles: near-identical ones would title-match each other's cases."""
    n = int(cid) if cid.isdigit() else ord(cid[0])
    return f"{TOPICS[n % len(TOPICS)].title()} findings, part {cid}"


def case(cid: str, keep: bool = True, on_topic: bool = True, **over) -> dict:
    out = {
        "id": cid,
        "title": title(cid),
        "url": f"https://example.com/posts/{cid}",
        "keep": keep,
        "on_topic": on_topic,
        "domain": "air.agents",
        "reason": "checked",
        "facts": [{"fact": "the number", "any": ["42%", "forty-two percent"]}] if keep else [],
    }
    out.update(over)
    return out


def output(cid: str, **over) -> dict:
    """An analyzer entry merge would keep, stating the case's fact."""
    entry = make_entry(
        title=title(cid),
        source_url=f"https://example.com/posts/{cid}/?utm_source=x",
        summary="Bypass rate was 42% across harnesses.",
        verified=True,
    )
    entry.update(over)
    return entry


def scored(cases, outputs):
    return eg.score(cases, outputs)


def test_the_real_golden_set_is_well_formed_and_about_thirty_cases():
    cases = eg.load_cases()
    assert 28 <= len(cases) <= 36
    keeps = [k for k in cases if k["keep"]]
    assert 0.35 <= len(keeps) / len(cases) <= 0.65  # both answers well represented
    assert sum(not k["on_topic"] for k in cases) >= 4  # the off-topic rate means something
    assert {k["domain"].split(".")[0] for k in cases} == {"ais", "ps", "air"}
    assert eg.main(["check"]) == 0


def test_the_pipelines_own_past_answers_score_perfectly(tmp_path):
    """The real entries, replayed as analyzer output, agree with every checked answer:
    the answers were built from the data, and the matcher/fact phrases find them."""
    cases = eg.load_cases()
    outs = [eg.find_entry(k) for k in cases]
    assert all(outs)
    result = scored(cases, outs)
    assert result["score"] == 1.0 and result["fact_coverage"] == 1.0, [
        r for r in result["results"] if not r["passed"]
    ]


def test_a_perfect_run_passes_and_a_skipped_drop_is_a_correct_drop():
    cases = [case("a"), case("b", keep=False)]
    result = scored(cases, [output("a")])
    assert result["passed"] and result["score"] == 1.0
    assert result["keep_drop_accuracy"] == 1.0 and result["off_topic_rate"] == 0.0


@pytest.mark.parametrize(
    "over,why",
    [
        ({"domain": "air.evals"}, "domain 'air.evals', answer air.agents"),
        ({"scores": {"novelty": 30, "relevance": 85}}, "dropped, answer is keep"),
        ({"verified": False}, "dropped, answer is keep"),
        ({"domain": "Agents"}, "dropped, answer is keep"),  # not an ID: merge would hold it
        ({"summary": "No numbers here.", "lessons": []}, "facts missed: the number"),
    ],
)
def test_a_wrong_keep_case_fails_with_its_reason(over, why):
    row = scored([case("a")], [output("a", **over)])["results"][0]
    assert not row["passed"] and why in row["why"]


def test_low_lesson_confidence_drops_a_story():
    lessons = [{"point": "p", "excerpt": "42%", "confidence": 0.3}]
    assert not scored([case("a")], [output("a", lessons=lessons)])["results"][0]["predicted_keep"]


def test_also_accept_and_title_matching():
    k = case("a", also_accept=["air.evals"])
    moved = output("a", domain="air.evals", source_url="https://mirror.example.net/x")
    assert scored([k], [moved])["results"][0]["passed"]


def test_kept_off_topic_stories_raise_the_off_topic_rate_and_fail_the_run():
    cases = [case(str(i)) for i in range(9)] + [case("off", keep=False, on_topic=False)]
    outs = [output(str(i)) for i in range(9)] + [output("off")]
    result = scored(cases, outs)
    assert result["off_topic_rate"] == 0.1 and result["score"] == 0.9
    assert result["passed"]  # exactly at both bars
    result = scored(cases[1:], outs[1:])
    assert result["off_topic_rate"] == 0.111 and not result["passed"]


def test_fact_coverage_threshold_counts_half_the_facts():
    facts = [{"fact": "f1", "any": ["42%"]}, {"fact": "f2", "any": ["seven harnesses"]}]
    row = scored([case("a", facts=facts)], [output("a")])["results"][0]
    assert row["fact_coverage"] == 0.5 and row["passed"]  # min_fact_coverage 0.5


def test_select_rotates_and_wraps():
    cases = [case(str(i)) for i in range(5)]
    assert [k["id"] for k in eg.select(cases, 3, 4)] == ["4", "0", "1"]
    assert eg.select(cases, None, 0) == cases and eg.select(cases, 9, 2) == cases


def test_a_staged_candidate_never_carries_the_answer_or_the_old_analysis():
    entry = output("a", id="a", source_id="rss:x", source_rank=60, scores={"novelty": 90})
    cand = eg.to_candidate(case("a"), entry)
    for leaked in ("summary", "scores", "lessons", "domain", "takeaway", "keep", "facts", "topic"):
        assert leaked not in cand
    assert cand["source_id"] == "rss:x" and cand["article_url"] == "https://example.com/posts/a"


def test_stage_needs_scratch_and_hides_the_cases_entries(sandbox, capsys):
    (sandbox / "data" / "evals").mkdir()
    golden = {"cases": [case("a"), case("b", keep=False)]}
    (sandbox / "data" / "evals" / "golden.json").write_text(json.dumps(golden))
    pool = common.empty_pool("ai-research")
    pool["entries"] = [make_entry(id="a"), make_entry(id="other")]
    common.save_pool("ai-research", pool)
    common.save_json(common.ARCHIVE_FILE, [make_entry(id="b")])
    assert eg.main(["stage", "--out", str(sandbox / "data" / "candidates.json")]) == 2
    assert eg.main(["stage", "--scratch", "--out", str(sandbox / "data" / "candidates.json")]) == 0
    assert [e["id"] for e in common.load_pool("ai-research")["entries"]] == ["other"]
    assert common.load_json(common.ARCHIVE_FILE) == []
    assert [cand["id"] for cand in common.load_candidates()] == ["a", "b"]
    manifest = json.loads((sandbox / "data" / "_golden_manifest.json").read_text())
    assert manifest["ids"] == ["a", "b"]


def test_cli_score_prints_per_case_lines_and_writes_the_result(sandbox, capsys):
    (sandbox / "data" / "evals").mkdir()
    golden = {"cases": [case("a"), case("b"), case("c", keep=False)]}
    (sandbox / "data" / "evals" / "golden.json").write_text(json.dumps(golden))
    analysis = sandbox / "data" / "analysis_out.json"
    analysis.write_text(json.dumps([output("a"), output("c")]))
    manifest = sandbox / "m.json"
    manifest.write_text(json.dumps({"ids": ["a", "b", "c"]}))
    assert eg.main(["score", str(analysis), "--manifest", str(manifest), "--write"]) == 1
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines[:3] == [
        "PASS a",
        "FAIL b: dropped, answer is keep; domain None, answer air.agents; facts missed: the number",
        "FAIL c: kept, answer is drop",
    ]
    assert lines[-1].startswith("EVAL golden FAIL score=0.333 cases=3")
    saved = json.loads((sandbox / "data" / "evals" / "golden-2026-07-15.json").read_text())
    assert saved["score"] == 0.333 and saved["generated"].startswith("2026-07-15")


def test_check_flags_a_malformed_case():
    import taxonomy as tx

    bad = [case("a", domain="nope", facts=[]), case("a", keep="yes")]
    problems = eg.check_cases(bad, tx.get(), {"a"})
    assert "a: 'nope' is not a taxonomy ID" in problems
    assert "a: a keep case needs 1-3 facts" in problems
    assert "a: duplicate case" in problems and "a: needs a boolean keep and a reason" in problems
