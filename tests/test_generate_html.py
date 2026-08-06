"""Tests for the static site generator — the docs/ tree GitHub Pages serves."""

from __future__ import annotations

import json
import re

import common
import generate_html as gh
from conftest import make_entry
from test_claims import ledger_of, make_claim

import claims

NOW = "2026-07-27"


def payload_of(sandbox, entries=(), ledger=None):
    for entry in entries:
        pool = common.load_pool(entry["topic"])
        pool["entries"].append(entry)
        common.save_pool(entry["topic"], pool)
    return gh.build_payload(ledger or ledger_of(make_claim()), common.load_config(), NOW)


# --- Payload ----------------------------------------------------------------
def test_payload_carries_every_claim(sandbox):
    data = payload_of(sandbox, ledger=ledger_of(make_claim(id="a"), make_claim(id="b")))
    assert [c["id"] for c in data["claims"]] == ["a", "b"]


def test_payload_includes_curated_findings(sandbox):
    data = payload_of(sandbox, entries=[make_entry(title="A curated finding")])
    assert [f["title"] for f in data["findings"]] == ["A curated finding"]


def test_payload_excludes_findings_held_for_review(sandbox):
    data = payload_of(sandbox, entries=[make_entry(title="Held back", needs_review=True)])
    assert data["findings"] == []


def test_findings_are_ranked_by_composite(sandbox):
    # Both must clear the curation floor, or the loser is excluded rather than ranked.
    low = make_entry(
        title="Low", source_url="https://e.com/1", scores={"novelty": 60, "relevance": 60}
    )
    high = make_entry(
        title="High", source_url="https://e.com/2", scores={"novelty": 95, "relevance": 95}
    )
    data = payload_of(sandbox, entries=[low, high])
    assert [f["title"] for f in data["findings"]] == ["High", "Low"]


def test_payload_names_every_topic(sandbox):
    data = payload_of(sandbox)
    assert set(data["topics"]) == set(common.TOPICS)
    assert data["topics"]["ai-research"]["name"] == "AI Research"


# --- Rendering --------------------------------------------------------------
def test_render_leaves_no_placeholder_tokens(sandbox):
    html = gh.render(payload_of(sandbox), NOW)
    for token in (
        "__DATA__",
        "__TITLE__",
        "__DESC__",
        "__REPO_NAME__",
        "__REPO_URL__",
        "__GENERATED__",
    ):
        assert token not in html


def test_render_embeds_parseable_json(sandbox):
    html = gh.render(payload_of(sandbox), NOW)
    block = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', html, re.S)
    data = json.loads(block.group(1).replace("<\\/", "</"))
    assert data["claims"][0]["id"] == "toon-over-json-for-agent-io"


def test_a_closing_script_tag_in_the_data_cannot_break_out(sandbox):
    evil = make_claim(id="evil", statement="Danger </script><script>alert(1)</script>")
    html = gh.render(payload_of(sandbox, ledger=ledger_of(evil)), NOW)
    block = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', html, re.S)
    # The whole payload must survive inside one JSON block, un-terminated early.
    data = json.loads(block.group(1).replace("<\\/", "</"))
    assert data["claims"][0]["statement"].startswith("Danger </script>")


def test_page_makes_no_external_requests(sandbox):
    html = gh.render(payload_of(sandbox), NOW)
    for host in ("cdn.", "fonts.googleapis", "unpkg", "jsdelivr", 'src="http'):
        assert host not in html


# --- main() -----------------------------------------------------------------
def test_main_writes_the_site_and_bypasses_jekyll(sandbox):
    claims.save_ledger(ledger_of(make_claim()))
    assert gh.main() == 0
    assert (sandbox / "docs" / "index.html").exists()
    assert (sandbox / "docs" / ".nojekyll").exists()


def test_main_refuses_to_render_an_invalid_ledger(sandbox):
    claims.save_ledger(ledger_of(make_claim(status="superseded")))
    assert gh.main() != 0
    assert not (sandbox / "docs" / "index.html").exists()


def test_main_succeeds_with_an_empty_ledger(sandbox):
    assert gh.main() == 0
    assert (sandbox / "docs" / "index.html").exists()


# --- Detail modal wiring ----------------------------------------------------
def test_finding_row_carries_detail_path(sandbox):
    """The modal fetches by detail_path; if it's missing, clicks fall back to
    the raw source. Lock the exact path the modal expects."""
    data = payload_of(sandbox, entries=[make_entry(title="AsyncAPI npm compromise")])
    row = data["findings"][0]
    assert row["detail_path"] == (
        "findings/ai-research/agents-harnesses/"
        "2026-07-asyncapi-npm-compromise.md"
    )


def test_main_mirrors_finding_markdown_into_docs_findings(sandbox):
    """generate_site.py writes track/domain/<file>.md; generate_html.py must
    copy that same file into docs/findings/... so the site's modal can fetch
    it same-origin."""
    import generate_site

    claims.save_ledger(ledger_of(make_claim()))
    pool = common.load_pool("ai-research")
    pool["entries"].append(make_entry(title="Compaction saves tokens"))
    common.save_pool("ai-research", pool)

    # generate_site writes the source .md; generate_html copies it into docs/
    generate_site.main()
    assert gh.main() == 0

    detail = (
        sandbox
        / "docs"
        / "findings"
        / "ai-research"
        / "agents-harnesses"
        / "2026-07-compaction-saves-tokens.md"
    )
    assert detail.is_file()
    assert "Compaction saves tokens" in detail.read_text(encoding="utf-8")


def test_main_mirrors_editorial_finding_markdown(sandbox):
    """Editorial-promoted findings advertise a detail_path just like curated
    ones do; the copy step must include them too, or the modal falls back
    to \"Couldn't load the detail page\" for every promoted item."""
    import generate_site

    claims.save_ledger(ledger_of(make_claim()))
    # A held finding (needs_review) that the editorial pass promoted.
    entry = make_entry(
        title="Provider guardrails blocked incident response",
        needs_review=True,
        editorial={
            "promoted": True,
            "reason": "Real-world incident with an actionable IR lesson.",
            "signals": ["timely"],
            "at": "2026-07-26T21:08:26+00:00",
        },
    )
    pool = common.load_pool("ai-research")
    pool["entries"].append(entry)
    common.save_pool("ai-research", pool)

    generate_site.main()
    assert gh.main() == 0

    detail = (
        sandbox
        / "docs"
        / "findings"
        / "ai-research"
        / "agents-harnesses"
        / "2026-07-provider-guardrails-blocked-incident-response.md"
    )
    assert detail.is_file(), (
        f"Editorial detail page not copied to {detail} — modal will 404 "
        f"on this card and fall back to the raw source."
    )
