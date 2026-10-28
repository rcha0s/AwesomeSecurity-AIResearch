"""Tests for scripts/taxonomy.py + migrate_taxonomy.py — one vocabulary of fixed
domain IDs (ISA ISC-14..17)."""

from __future__ import annotations

import json
from pathlib import Path

import common as c
import migrate_taxonomy
import pytest
import rerank
import taxonomy as tx
import yaml
from conftest import make_entry

REPO = Path(__file__).resolve().parent.parent
REAL_POOLS = [REPO / "data" / f"{t}.json" for t in c.TOPICS]
REAL_ARCHIVE = REPO / "data" / "archive.json"
REAL_MIGRATION = REPO / "data" / "taxonomy_migration.json"


@pytest.fixture
def tax() -> tx.Taxonomy:
    return tx.get()


# --- the vocabulary itself ---------------------------------------------------
def test_three_topics_each_with_six_to_ten_domains(tax):
    assert set(tax.defaults) == set(c.TOPICS)
    for topic in c.TOPICS:
        assert 6 <= len(tax.for_topic(topic)) <= 10, topic


def test_efficiency_domains_are_claim_eligible_and_own_their_cost_hints(tax):
    for did in ("air.cost-efficiency", "air.work-efficiency"):
        assert tax.domains[did].topic == "ai-research" and tax.domains[did].claim_eligible
    moved = {"token cost", "prompt cache", "prompt caching", "model routing"}
    assert moved <= set(tax.domains["air.cost-efficiency"].keywords)
    assert not moved & set(tax.domains["air.model-io"].keywords)


def test_ids_carry_their_topic_prefix(tax):
    prefix = {"ai-security": "ais.", "product-security": "ps.", "ai-research": "air."}
    for did, dom in tax.domains.items():
        assert did.startswith(prefix[dom.topic]), did
        assert dom.name and dom.scope and dom.keywords


def test_every_old_interests_cluster_folds_into_a_domain(tax):
    """The 13 interests.yaml clusters (A-M) all live on as some domain's
    legacy_clusters, so no tier-1 area was dropped in the fold."""
    folded = {letter for d in tax.domains.values() for letter in d.legacy_clusters}
    assert folded == set("ABCDEFGHIJKLM")


def test_claim_eligibility_is_expressible_per_domain(tax):
    """The old `cluster: null` (adjacent, news only) survives as claim_eligible: false."""
    assert tx.claim_eligible(make_entry(topic="ai-security", domain="ais.prompt-injection"))
    assert not tx.claim_eligible(make_entry(topic="ai-research", domain="air.models"))
    assert not tx.claim_eligible(make_entry(topic="ai-research", domain="Agents & Harnesses"))
    # An ID of another topic is not eligible either.
    assert not tx.claim_eligible(make_entry(topic="ai-research", domain="ais.prompt-injection"))


def test_common_topics_list_the_taxonomy_ids(tax):
    for topic, meta in c.TOPICS.items():
        assert meta["domains"] == [d.id for d in tax.for_topic(topic)]
    assert c.domain_slug("ais.mcp-tools") == "mcp-tools"
    assert c.domain_name("ais.mcp-tools") == "MCP, Tools & Skills"
    assert c.topic_for_domain("ps.appsec") == "product-security"
    assert c.topic_for_domain("Web Application Security") == "product-security"


def _write_taxonomy(tmp_path: Path, mutate) -> Path:
    raw = yaml.safe_load(tx.TAXONOMY_FILE.read_text())
    mutate(raw)
    path = tmp_path / "taxonomy.yaml"
    path.write_text(yaml.safe_dump(raw))
    return path


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda r: r["domains"].update({"ais.Bad_Slug": r["domains"]["ais.ai-infra"]}), "bad"),
        (lambda r: r["domains"].update({"zz.thing": r["domains"]["ais.ai-infra"]}), "prefix"),
        (lambda r: r["domains"]["ais.ai-infra"].pop("scope"), "needs name"),
        (lambda r: r["topics"]["ai-security"].update(default_domain="ps.appsec"), "default"),
        (lambda r: r["aliases"]["ai-security"].update({"Oops": "ps.appsec"}), "alias"),
    ],
)
def test_load_rejects_a_malformed_taxonomy(tmp_path, mutate, message):
    path = _write_taxonomy(tmp_path, mutate)
    with pytest.raises(ValueError, match=message):
        tx.load(path)


# --- resolution --------------------------------------------------------------
def test_resolve_prefers_id_then_alias_then_name_then_keywords_then_default(tax):
    assert tx.resolve(tax, "ai-security", "ais.mcp-tools") == ("ais.mcp-tools", "id")
    assert tx.resolve(tax, "ai-security", "MCP & Tools") == ("ais.mcp-tools", "alias")
    assert tx.resolve(tax, "ai-security", "mcp and tools") == ("ais.mcp-tools", "alias")
    assert tx.resolve(tax, "ai-security", "MCP, Tools & Skills") == ("ais.mcp-tools", "name")
    got = tx.resolve(tax, "ai-security", "Novel thing", "a jailbreak via prompt injection")
    assert got == ("ais.prompt-injection", "keywords")
    assert tx.resolve(tax, "ai-security", "zzz", "nothing") == ("ais.agent-security", "default")


def test_resolve_never_crosses_topics(tax):
    """An ID of another topic is a label like any other, resolved within the topic."""
    did, how = tx.resolve(tax, "ai-research", "ais.prompt-injection")
    assert tax.domains[did].topic == "ai-research" and how != "id"


def test_norm_label_and_label_tag():
    assert tx.norm_label("Agents & Harnesses") == tx.norm_label("agents and harnesses")
    assert tx.label_tag("MCP Protocol / Output-Neutralization Injection") == (
        "mcp-protocol-output-neutralization-injection"
    )


# --- merge gate (enforce) ----------------------------------------------------
def test_enforce_holds_a_known_alias_without_adding_a_synonym_tag(tax):
    entry = tx.enforce(make_entry(topic="ai-security", domain="MCP & Tools", tags=["x"]), tax)
    assert entry["domain"] == "ais.mcp-tools" and entry["domain_label"] == "MCP & Tools"
    assert entry["needs_review"] is True and "MCP & Tools" in entry["domain_hold"]
    assert entry["tags"] == ["x"]  # the alias map already knows it: not new information


def test_enforce_tags_a_label_the_alias_map_does_not_know(tax):
    raw = make_entry(topic="ai-security", domain="Agent Wallets", title="A jailbreak", tags=[])
    entry = tx.enforce(raw, tax)
    assert entry["domain"] == "ais.prompt-injection" and entry["tags"] == ["agent-wallets"]


def test_enforce_holds_an_unknown_id(tax):
    entry = tx.enforce(make_entry(topic="ai-security", domain="ais.not-a-domain"), tax)
    assert entry["domain_hold"] and tax.is_valid(entry["domain"], "ai-security")


def test_enforce_passes_a_valid_id_untouched(tax):
    raw = make_entry(topic="ai-research", domain="air.agents")
    assert tx.enforce(dict(raw), tax) == raw


def test_held_entry_is_published_nowhere(sandbox, tax):
    conf = c.load_config()
    entry = tx.enforce(make_entry(topic="ai-security", domain="Free Text", verified=True), tax)
    entry["needs_review"] = False  # even if something cleared the flag
    assert c.domain_held(entry)
    assert not c.is_curated(entry, conf)
    assert not c.editorial_eligible(entry, conf)
    assert not c.is_news_curated(entry, conf, {}, window=None)
    assert c.review_reason(entry, conf).startswith("domain not in the taxonomy")


# --- migration (ISC-16/17) ---------------------------------------------------
def test_every_real_pool_and_archive_entry_has_a_valid_domain_id(tax):
    """ISC-16: 100% of the committed data carries a domain ID of its own topic."""
    entries = [e for p in REAL_POOLS for e in json.loads(p.read_text())["entries"]]
    entries += json.loads(REAL_ARCHIVE.read_text())
    assert len(entries) > 400
    bad = [
        (e.get("topic"), e.get("domain"))
        for e in entries
        if not tax.is_valid(e.get("domain"), e.get("topic"))
    ]
    assert bad == []


def test_migration_table_agrees_with_the_alias_map(tax):
    """ISC-17: every pre-migration label has an ID, and the taxonomy's alias map
    resolves that label to the same ID (so pipeline normalization matches it)."""
    table = json.loads(REAL_MIGRATION.read_text())
    labels = [(t, lab, row) for t, rows in table["labels"].items() for lab, row in rows.items()]
    assert len(labels) >= 200
    for topic, label, row in labels:
        assert tax.is_valid(row["id"], topic), (topic, label)
        assert tx.resolve(tax, topic, label) == (row["id"], "alias"), (topic, label)
        assert row["entries"] >= 1
    for key, row in table["entry_overrides"].items():
        assert row["label"] in table["labels"][row["topic"]], key
        assert tax.is_valid(row["id"], row["topic"]) and row["why"], key


def _seed_legacy(sandbox: Path) -> None:
    pool = c.load_pool("ai-security")
    pool["entries"] = [
        make_entry(topic="ai-security", domain="Prompt Injection", source_url="https://a/1"),
        make_entry(
            topic="ai-security",
            domain="Brand New Label",
            source_url="https://a/2",
            title="An MCP server with tool poisoning",
        ),
        make_entry(topic="ai-security", domain="ais.red-teaming", source_url="https://a/3"),
    ]
    c.save_pool("ai-security", pool)
    old = make_entry(topic="ai-research", domain="Evaluation", source_url="https://a/4")
    c.save_json(c.ARCHIVE_FILE, [old])


def test_migrate_is_idempotent_and_check_reports_pending(sandbox, capsys):
    _seed_legacy(sandbox)
    assert migrate_taxonomy.main(["--check"]) == 1
    assert c.load_pool("ai-security")["entries"][0]["domain"] == "Prompt Injection"  # untouched
    assert migrate_taxonomy.main([]) == 0
    entries = c.load_pool("ai-security")["entries"]
    assert [e["domain"] for e in entries] == [
        "ais.prompt-injection",
        "ais.mcp-tools",
        "ais.red-teaming",
    ]
    assert "brand-new-label" in entries[1]["tags"]
    assert c.load_json(c.ARCHIVE_FILE)[0]["domain"] == "air.evals"
    before = c.load_pool("ai-security")
    assert migrate_taxonomy.main(["--check"]) == 0
    assert migrate_taxonomy.main([]) == 0
    assert c.load_pool("ai-security") == before


def test_entry_override_beats_the_label(sandbox, tax):
    entry = make_entry(id="special", topic="ai-research", domain="Evaluation")
    did, how = tx.normalize_entry(entry, tax, {"special": "air.alignment"})
    assert (did, how) == ("air.alignment", "override")
    # An override pointing at another topic's id is ignored, never applied.
    entry = make_entry(id="special", topic="ai-research", domain="Evaluation")
    assert tx.normalize_entry(entry, tax, {"special": "ps.appsec"})[0] == "air.evals"


def test_entry_key_falls_back_to_the_source_url():
    assert tx.entry_key({"id": "x"}) == "x"
    assert tx.entry_key({"source_url": "https://A.com/p/?q=1#f"}) == "url:https://a.com/p"


def test_rerank_converges_a_branch_with_pre_taxonomy_data(sandbox):
    """Another branch's pool (free-text labels) normalizes on its next rerank."""
    _seed_legacy(sandbox)
    rerank.rerank_all()
    pool = c.load_pool("ai-security")
    assert all(tx.get().is_valid(e["domain"], "ai-security") for e in pool["entries"])
    assert pool["domains"] == c.TOPICS["ai-security"]["domains"]
    assert c.load_json(c.ARCHIVE_FILE)[0]["domain"] == "air.evals"


def test_prompt_context_and_cli_list_every_id(tax, capsys):
    text = tx.prompt_context(tax)
    assert all(f"`{did}`" in text for did in tax.domains)
    assert tx.main(["list"]) == 0 and "ais.prompt-injection" in capsys.readouterr().out
    assert tx.main([]) == 2


def test_load_overrides_missing_file_is_empty(tmp_path):
    assert tx.load_overrides(tmp_path / "nope.json") == {}
