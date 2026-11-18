"""Tests for docs/efficiency.md, the harness-fetchable efficiency feed."""

from __future__ import annotations

import briefing
import efficiency_feed as ef

COST = briefing.EFFICIENCY_DOMAINS["cost"]
SITE = "https://example.test/site/"


def _claim(cid, changed, evidence_days=(), status="current", domain=COST):
    return {
        "id": cid,
        "title": f"Title {cid}",
        "statement": f"Statement {cid}",
        "status": status,
        "confidence": 0.7,
        "domain_id": domain,
        "guidance": "Do the *thing* [now](javascript:alert(1))",
        "scope": "Long sessions",
        "changed_on": changed,
        "history": [{"on": changed, "status": status}],
        "evidence": [
            {
                "url": f"https://ex.test/{d}",
                "title": f"Paper {d}",
                "published": d,
                "stance": "supports",
            }
            for d in evidence_days
        ],
    }


def test_claims_order_by_newest_evidence_and_skip_retired_and_other_domains():
    payload = {
        "claims": [
            _claim("old", "2026-10-01"),
            _claim("fresh", "2026-10-01", evidence_days=("2026-11-15",)),
            _claim("gone", "2026-11-17", status="superseded"),
            _claim("security", "2026-11-17", domain="air.agent-security"),
        ]
    }
    md = ef.render(payload, "2026-11-18", SITE)
    assert md.index("Title fresh") < md.index("Title old")
    assert "Title gone" not in md and "Title security" not in md
    assert "updated 2026-11-15" in md


def test_text_is_escaped_and_only_http_links_render():
    claim = _claim("x", "2026-11-01", evidence_days=("2026-11-02",))
    claim["evidence"].append(
        {"url": "javascript:alert(1)", "title": "Bad", "published": "2026-11-03"}
    )
    md = ef.render({"claims": [claim]}, "2026-11-18", SITE)
    assert "- supports: Bad (2026-11-03)" in md  # a non-http URL renders as plain text
    assert r"\*thing\*" in md and r"\[now\]" in md
    assert "[Paper 2026-11-02](https://ex.test/2026-11-02)" in md
    # newest evidence first
    assert md.index("Bad") < md.index("Paper 2026-11-02")


def test_empty_feed_says_so():
    md = ef.render({}, "2026-11-18", SITE)
    assert "_No live claims._" in md
    assert "_No vetted efficiency findings in this window._" in md
