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


def claim(cid, status="current", **over):
    c = {"id": cid, "status": status, "claim": f"claim {cid}", "evidence": [{"url": "https://e/1"}]}
    if status in cc.RETIRED:
        c.update(superseded_by=["new"], superseded_on="2026-10-01", supersession_reason="r")
    c.update(over)
    return c


def ledger(*claims):
    return {"schema_version": 1, "claims": list(claims)}


MAIN = ledger(claim("live"), claim("old", "superseded"), claim("wrong", "refuted"), claim("new"))


def test_unchanged_ledger_passes():
    assert cc.claim_history_problems(MAIN, copy.deepcopy(MAIN)) == []


def test_new_claims_and_live_edits_pass():
    pr = copy.deepcopy(MAIN)
    pr["claims"][0]["claim"] = "reworded live claim"
    pr["claims"][0]["status"] = "superseded"  # a live claim may retire
    pr["claims"].append(claim("brand-new"))
    assert cc.claim_history_problems(MAIN, pr) == []


def test_deleted_claim_fails():
    pr = ledger(*[c for c in copy.deepcopy(MAIN)["claims"] if c["id"] != "old"])
    assert cc.claim_history_problems(MAIN, pr) == ["claim old on main is missing from the PR"]


@pytest.mark.parametrize(
    "field, value",
    [
        ("status", "current"),
        ("claim", "rewritten history"),
        ("supersession_reason", "a different reason"),
        ("superseded_on", "2026-10-19"),
        ("superseded_by", ["other"]),
        ("confidence", 0.1),
    ],
)
def test_retired_claim_history_is_frozen(field, value):
    pr = copy.deepcopy(MAIN)
    pr["claims"][1][field] = value
    assert cc.claim_history_problems(MAIN, pr) != []


def test_retired_claim_field_removal_fails():
    pr = copy.deepcopy(MAIN)
    del pr["claims"][2]["supersession_reason"]
    assert cc.claim_history_problems(MAIN, pr) != []


def test_add_claim_style_updates_to_retired_claims_pass():
    pr = copy.deepcopy(MAIN)
    old = pr["claims"][1]
    old["evidence"].append({"url": "https://e/2"})
    old["last_reviewed"] = "2026-10-20"
    old["supersedes"] = ["older"]
    assert cc.claim_history_problems(MAIN, pr) == []


def test_rewritten_evidence_fails():
    pr = copy.deepcopy(MAIN)
    pr["claims"][1]["evidence"] = [{"url": "https://e/other"}]
    assert any("evidence" in p for p in cc.claim_history_problems(MAIN, pr))


def test_dropped_supersedes_edge_fails():
    main = copy.deepcopy(MAIN)
    main["claims"][1]["supersedes"] = ["older"]
    pr = copy.deepcopy(main)
    pr["claims"][1]["supersedes"] = []
    assert any("supersedes" in p for p in cc.claim_history_problems(main, pr))


def test_garbage_ledgers_report_missing_claims():
    assert cc.claim_history_problems(MAIN, {"claims": "nope"}) != []
    assert cc.claim_history_problems(MAIN, None) != []
