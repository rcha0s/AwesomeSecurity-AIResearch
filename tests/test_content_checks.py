"""content_checks.py: URL schemes, render equality, claim history (audit F2, F3, F5)."""

from __future__ import annotations

import copy

import content_checks as cc
import generate_html as gh
import pytest

# ---------------------------------------------------------------- URLs


@pytest.mark.parametrize(
    "url",
    ["https://a.example/x?y=1&z=2", "http://a.example/", "HTTPS://A.EXAMPLE/", None, ""],
)
def test_http_urls_pass(url):
    assert cc.url_problems({"url": url, "source_url": url}) == []


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        " https://a.example/",
        "data:text/html,x",
        "vbscript:x",
        "//evil.example/",
        "findings/a.md",
        'https://a.example/"onmouseover=x',
        "https://a.example/<script>",
        "https://a.example/ x",
        "https://a.example/`x",
        "https://",
        3,
        ["https://a.example/"],
    ],
)
def test_non_http_urls_fail(url):
    assert cc.url_problems({"article_url": url}) != []


def test_url_fields_are_found_at_any_depth():
    doc = {"entries": [{"lessons": [{"evidence": {"tweet_url": "javascript:x"}}]}]}
    assert cc.url_problems(doc) == ["entries[0].lessons[0].evidence.tweet_url: not an http(s) URL"]


def test_non_url_keys_are_not_checked():
    assert cc.url_problems({"title": "javascript:x", "urlish": "javascript:x"}) == []


# ---------------------------------------------------------------- render equality

PAYLOAD = {"claims": [], "findings": [{"title": "A </script> b", "url": "https://a.example/"}]}


def page(stamp="2026-10-20", payload=PAYLOAD):
    return gh.render(payload, stamp)


def test_main_renderer_output_passes():
    assert cc.render_problems(page(), gh.render) == []


def test_a_real_rendered_site_passes():
    assert cc.render_problems((gh.c.ROOT / "docs" / "index.html").read_text(), gh.render) == []


@pytest.mark.parametrize(
    "tamper",
    [
        lambda p: p.replace("</body>", "<script>alert(1)</script></body>"),
        lambda p: p.replace("function esc(s)", "function esc(s) { return s; } function x(s)"),
        lambda p: p + "<!-- -->",
        lambda p: p.replace('<script id="site-data"', '<script id="site-data" onload="x"'),
    ],
)
def test_hand_edited_pages_fail(tamper):
    assert cc.render_problems(tamper(page()), gh.render) != []


def test_two_data_blocks_fail():
    p = page()
    block = p[p.index('<script id="site-data"') : p.index("</script>", p.index("site-data")) + 9]
    assert cc.render_problems(p.replace(block, block + block), gh.render) != []


def test_unparseable_payload_fails():
    p = page().replace(
        '<script id="site-data" type="application/json">{',
        '<script id="site-data" type="application/json">{{',
    )
    assert cc.render_problems(p, gh.render) != []


def test_missing_stamp_fails():
    assert cc.render_problems(page().replace("<span>Generated <b>", "<span><b>"), gh.render) != []


# ---------------------------------------------------------------- claim history
# Policy: a scan PR may add claims and append evidence (bumping last_reviewed);
# any other change to an existing claim, live or retired, needs a human.

RETIRED = ("superseded", "refuted")


def claim(cid, status="current", **over):
    c = {
        "id": cid,
        "status": status,
        "statement": f"claim {cid}",
        "title": f"Title {cid}",
        "guidance": "do the thing",
        "confidence": 0.8,
        "evidence": [{"url": "https://e/1"}],
    }
    if status in RETIRED:
        c.update(superseded_by=["new"], superseded_on="2026-10-01", supersession_reason="r")
    c.update(over)
    return c


def ledger(*claims):
    return {"schema_version": 1, "claims": list(claims)}


MAIN = ledger(
    claim("live"),
    claim("old", "superseded"),
    claim("wrong", "refuted"),
    claim("new", supersedes=["old"]),
)
LIVE, OLD, WRONG, NEW = 0, 1, 2, 3


def test_unchanged_ledger_passes():
    assert cc.claim_history_problems(MAIN, copy.deepcopy(MAIN)) == []


def test_scans_may_add_claims_and_append_evidence():
    pr = copy.deepcopy(MAIN)
    pr["claims"].append(claim("brand-new"))
    for i in (LIVE, OLD, WRONG):
        pr["claims"][i]["evidence"].append({"url": "https://e/2", "stance": "supports"})
        pr["claims"][i]["last_reviewed"] = "2026-10-20"
    assert cc.claim_history_problems(MAIN, pr) == []


def test_refusal_reason_is_the_agreed_wording():
    pr = copy.deepcopy(MAIN)
    pr["claims"][0]["status"] = "contested"
    problems = cc.claim_history_problems(MAIN, pr)
    assert problems == ["claim change needs human review: live `status` changed"]


def test_deleted_claim_fails():
    pr = ledger(*[c for c in copy.deepcopy(MAIN)["claims"] if c["id"] != "old"])
    assert cc.claim_history_problems(MAIN, pr) == ["claim old on main is missing from the PR"]


FROZEN = [
    ("status", "contested"),
    ("statement", "reworded"),
    ("title", "Retitled"),
    ("guidance", "do something else"),
    ("superseded_by", ["other"]),
    ("superseded_on", "2026-10-19"),
    ("supersession_reason", "a different reason"),
    ("supersedes", ["another"]),
    ("confidence", 0.1),
    ("scope", "new scope"),
    # ledger dates and retired controls: only a reviewed correction moves them
    ("added_on", "2026-10-21"),
    ("changed_on", "2026-10-21"),
    ("refuted_controls", ["--ignore-scripts"]),
]


@pytest.mark.parametrize("index", [LIVE, OLD, WRONG, NEW])
@pytest.mark.parametrize("field, value", FROZEN)
def test_any_other_change_needs_human_review(index, field, value):
    pr = copy.deepcopy(MAIN)
    pr["claims"][index][field] = value
    problems = cc.claim_history_problems(MAIN, pr)
    assert problems and all(p.startswith(cc.NEEDS_REVIEW) for p in problems)
    assert f"`{field}`" in problems[0]


def test_retiring_a_live_claim_needs_human_review():
    """Superseding an existing claim edits both ends: never unattended."""
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE].update(status="superseded", superseded_by=["x"], supersession_reason="r")
    pr["claims"].append(claim("x", supersedes=["live"]))
    problems = cc.claim_history_problems(MAIN, pr)
    assert {p.split("`")[1] for p in problems} == {
        "status",
        "superseded_by",
        "supersession_reason",
    }


@pytest.mark.parametrize("field", ["supersession_reason", "guidance", "title"])
def test_removing_a_field_needs_human_review(field):
    pr = copy.deepcopy(MAIN)
    del pr["claims"][WRONG][field]
    assert cc.claim_history_problems(MAIN, pr) != []


def test_adding_a_new_field_to_an_existing_claim_needs_human_review():
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE]["basis"] = "added later"
    assert cc.claim_history_problems(MAIN, pr) != []


@pytest.mark.parametrize(
    "evidence",
    [[{"url": "https://e/other"}], [], "nope", [{"url": "https://e/2"}, {"url": "https://e/1"}]],
)
def test_rewritten_evidence_needs_human_review(evidence):
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE]["evidence"] = evidence
    problems = cc.claim_history_problems(MAIN, pr)
    assert any("evidence" in p and p.startswith(cc.NEEDS_REVIEW) for p in problems)


def test_garbage_ledgers_report_missing_claims():
    assert cc.claim_history_problems(MAIN, {"claims": "nope"}) != []
    assert cc.claim_history_problems(MAIN, None) != []


# ---------------------------------------------------------------- sticky promotions
PROMO = {"promoted": True, "reason": "trending", "signals": [], "at": "2026-10-20"}


def _pool(*entries) -> dict:
    return {"entries": list(entries)}


def _ed(eid: str, **over) -> dict:
    return {"id": eid, "editorial": dict(PROMO), "grounding_score": 1.0, **over}


def test_kept_and_new_promotions_pass():
    main = [_pool(_ed("a")), []]
    pr = [_pool(_ed("a"), _ed("b")), []]
    assert cc.editorial_problems(main, pr) == []
    assert cc.editorial_problems([_pool({"id": "c"})], [_pool(_ed("c"))]) == []  # added


def test_a_promotion_may_move_to_the_archive():
    assert cc.editorial_problems([_pool(_ed("a")), []], [_pool(), [_ed("a")]]) == []


@pytest.mark.parametrize(
    "after,needle",
    [
        ({"id": "a", "grounding_score": 1.0}, "lost its promotion with main's integrity intact"),
        ({"id": "a", "editorial": {"promoted": False}}, "integrity intact"),
        ({"id": "a", "editorial": "yes"}, "integrity intact"),
        ({"id": "a", "verified": True, "grounding_score": None}, "integrity intact"),
        (None, "promoted entry a is gone"),
    ],
)
def test_a_demotion_with_integrity_intact_needs_review(after, needle):
    pr = [_pool(*([after] if after else []))]
    problems = cc.editorial_problems([_pool(_ed("a"))], pr)
    assert len(problems) == 1 and needle in problems[0]
    assert problems[0].startswith(cc.DEMOTION_REVIEW)


@pytest.mark.parametrize("lost", [{"verified": False}, {"grounding_score": 0.5}])
def test_integrity_flipped_inside_the_pr_is_not_evidence(lost):
    """verified / grounding_score are session-writable: flipping them on a
    promoted entry must not launder a demotion past the gate."""
    after = {"id": "a", "grounding_score": 1.0, **lost}
    problems = cc.editorial_problems([_pool(_ed("a"))], [_pool(after)])
    assert len(problems) == 1 and problems[0].startswith(cc.DEMOTION_REVIEW)


@pytest.mark.parametrize("lost", [{"verified": False}, {"grounding_score": 0.5}])
def test_integrity_already_lost_on_main_may_remove_a_promotion(lost):
    after = {"id": "a", "grounding_score": 1.0, **lost}
    assert cc.editorial_problems([_pool(_ed("a", **lost))], [_pool(after)]) == []


@pytest.mark.parametrize("order", ["demoted-last", "demoted-first"])
def test_an_id_is_kept_only_if_every_copy_stays_promoted(order):
    """A promoted copy elsewhere (pool vs archive) can't mask a demoted one."""
    kept, dropped = _ed("a"), {"id": "a", "grounding_score": 1.0}
    pr = [_pool(kept), [dropped]] if order == "demoted-last" else [_pool(dropped), [kept]]
    problems = cc.editorial_problems([_pool(_ed("a"))], pr)
    assert len(problems) == 1 and problems[0].startswith(cc.DEMOTION_REVIEW)
    assert cc.editorial_problems([_pool(_ed("a"))], [_pool(kept), [dict(kept)]]) == []


def test_garbage_docs_do_not_crash():
    assert cc.editorial_problems([None, "x", {"entries": "x"}], [None]) == []
    assert cc.editorial_problems([_pool(_ed("a"))], [None]) != []


def test_a_new_claim_may_arrive_with_its_ledger_dates():
    pr = copy.deepcopy(MAIN)
    pr["claims"].append(claim("dated", added_on="2026-10-21", changed_on="2026-10-21"))
    assert cc.claim_history_problems(MAIN, pr) == []


def test_add_claim_evidence_leaves_ledger_dates_alone(sandbox):
    """The one claim write a scan makes (add_claim.py evidence) must stay a
    content-only change on a ledger that carries added_on/changed_on."""
    import add_claim

    import claims as cl

    base = claim("dated", topic="ai-research", added_on="2026-07-01", changed_on="2026-07-01")
    base["evidence"] = [{"url": "https://e/1", "stance": "supports", "published": "2026-06-01"}]
    main = ledger(base)
    cl.save_ledger(copy.deepcopy(main))
    assert add_claim.main(["evidence", "dated", "--evidence", "supports|https://e/2"]) == 0
    assert cc.claim_history_problems(main, cl.load_ledger()) == []
