"""A retitled entry keeps a "Moved" stub at its old page path (tree + docs mirror)."""

from __future__ import annotations

import common
import generate_html as gh
import merge_analysis as m
from conftest import make_entry
from test_claims import ledger_of, make_claim

import claims


# --- recording the old slug -------------------------------------------------
def test_retitle_records_the_old_slug_once():
    entry = make_entry(title="Old headline")
    once = common.retitle(entry, "New headline")
    assert once["previous_slugs"] == ["old-headline"]
    twice = common.retitle(once, "Newer headline")
    assert twice["previous_slugs"] == ["old-headline", "new-headline"]
    assert "previous_slugs" not in entry  # input untouched


def test_a_retitle_that_keeps_the_slug_records_nothing():
    entry = make_entry(title="Same Headline")
    assert "previous_slugs" not in common.retitle(entry, "same headline!")


def test_retitling_back_drops_the_slug_that_is_current_again():
    back = common.retitle(common.retitle(make_entry(title="A b"), "C d"), "A b")
    assert back["previous_slugs"] == ["c-d"]


def test_reanalysis_retitle_records_the_old_slug():
    """merge_analysis.reconcile is the automatic rename path."""
    existing = make_entry(title="Original title", source_url="https://a/x")
    out = m.reconcile(existing, {**existing, "title": "Sharper title"})
    assert out["title"] == "Sharper title"
    assert out["previous_slugs"] == ["original-title"]
    same = m.reconcile(existing, dict(existing))
    assert "previous_slugs" not in same


def test_former_page_paths_cover_old_dirs_and_old_titles():
    entry = common.retitle(
        make_entry(title="Old t", domain="air.agents", domain_label="Agents & Harnesses"),
        "New t",
    )
    assert common.former_page_paths(entry) == [
        ("agents", "2026-07-old-t.md"),
        ("agents-harnesses", "2026-07-new-t.md"),
        ("agents-harnesses", "2026-07-old-t.md"),
    ]


# --- rendering --------------------------------------------------------------
def _render(sandbox, entries):
    import generate_site

    claims.save_ledger(ledger_of(make_claim()))
    pool = common.load_pool("ai-research")
    pool["entries"] += entries
    common.save_pool("ai-research", pool)
    generate_site.main()
    assert gh.main() == 0
    return sandbox / "ai-research" / "agents", sandbox / "docs/findings/ai-research/agents"


def test_old_title_path_gets_a_stub_in_the_tree_and_the_docs_mirror(sandbox):
    entry = common.retitle(make_entry(title="Old headline", domain="air.agents"), "New headline")
    tree, docs = _render(sandbox, [entry])
    for base in (tree, docs):
        stub = (base / "2026-07-old-headline.md").read_text()
        assert stub.startswith("# Moved\n")
        assert "](../agents/2026-07-new-headline.md)" in stub
        assert "retitled" in stub
        real = (base / "2026-07-new-headline.md").read_text()
        assert not real.startswith("# Moved")


def test_a_stub_never_overwrites_a_real_page(sandbox):
    """Entry A used to be titled like entry B is now: B's real page wins."""
    a = common.retitle(
        make_entry(title="Taken title", domain="air.agents", source_url="https://a/1"), "A now"
    )
    b = make_entry(title="Taken title", domain="air.agents", source_url="https://a/2")
    tree, docs = _render(sandbox, [a, b])
    for base in (tree, docs):
        assert not (base / "2026-07-taken-title.md").read_text().startswith("# Moved")


def test_retitle_stubs_are_deterministic(sandbox):
    entry = common.retitle(make_entry(title="Old headline", domain="air.agents"), "New headline")
    tree, _ = _render(sandbox, [entry])
    first = (tree / "2026-07-old-headline.md").read_text()
    _render(sandbox, [])
    assert (tree / "2026-07-old-headline.md").read_text() == first
