"""Tests for scripts/eval_recall.py (ISC-22) — recorded curator responses, no network."""

from __future__ import annotations

import json
from pathlib import Path

import common
import eval_recall as er
import pytest
import taxonomy as tx
from conftest import make_entry

FIXTURES = Path(__file__).parent / "fixtures" / "recall"
SINCE = "2026-07-08"  # frozen clock 2026-07-15 minus the 7-day lookback


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    import requests

    def boom(*a, **k):
        raise AssertionError("eval_recall touched the network in a test")

    monkeypatch.setattr(requests, "get", boom)
    monkeypatch.setattr(er.subprocess, "run", boom)


def read_fixture(url: str) -> str:
    name = "tldrsec_sitemap.xml" if url == er.TLDRSEC_SITEMAP else url.rsplit("/", 1)[1] + ".html"
    path = FIXTURES / name
    return path.read_text() if path.exists() else ""


def collected() -> list[dict]:
    items, errors = er.collect(er.fixture_source(FIXTURES, SINCE), SINCE)
    assert errors == []
    return items


def test_tldrsec_takes_each_paragraphs_first_story_link_from_security_sections():
    urls = er.parse_tldrsec_sitemap((FIXTURES / "tldrsec_sitemap.xml").read_text(), 2)
    assert urls == ["https://tldrsec.com/p/tldr-sec-339", "https://tldrsec.com/p/tldr-sec-337"]
    issues = er.tldrsec_issues(read_fixture, SINCE)
    assert [(u, d) for u, d, _ in issues] == [("https://tldrsec.com/p/tldr-sec-339", "2026-07-10")]
    page = issues[0][2]  # 337 has no recorded page, so no publish date: skipped
    items = er.parse_tldrsec_issue(page, issues[0][1])
    assert [i["title"] for i in items] == [
        "Pre-auth heap overflow in a SAML parser",
        "ChainDrop npm worm steals CI OIDC tokens",
        "Frontier agents escape their sandbox during evals",
        "My favourite sourdough recipe",
    ]  # not Advice, the sponsor block, people links, Misc or Wrapping Up
    assert items[0]["url"] == "https://labs.example.com/heap-overflow-saml"  # utm stripped
    assert items[0]["published"] == "2026-07-10"


def test_atom_keeps_the_window_and_the_linked_story():
    items = er.parse_atom((FIXTURES / "simon-security.atom").read_text(), SINCE)
    assert [i["title"] for i in items] == [
        "Indirect prompt injection in a coding agent's web fetch",
        "Datasette 9.9 release notes",
    ]
    assert "https://embracethered.example.com/blog/agent-rce" in items[0]["urls"]


def test_ghsa_and_kev_carry_their_vulnerability_ids():
    ghsa = er.parse_ghsa(json.loads((FIXTURES / "ghsa.json").read_text()))
    assert ghsa[0]["ids"] == ["CVE-2026-1111", "GHSA-PR64-JMMF-JP54"]
    kev = er.parse_kev(json.loads((FIXTURES / "kev.json").read_text()), SINCE)
    assert [k["ids"] for k in kev] == [["CVE-2026-8452"], ["CVE-2026-2222"]]  # 2025 one dropped


def test_on_thesis_uses_taxonomy_hints_and_excluded_terms():
    tax = tx.get()
    keep = er.item("x", "Prompt injection in a coding agent", "https://a.example/1", SINCE)
    off = er.item("x", "My favourite sourdough recipe", "https://a.example/2", SINCE)
    excluded = er.item(
        "x", "Prompt injection for medical imaging models", "https://a.example/3", SINCE
    )
    assert er.on_thesis(keep, tax)
    assert not er.on_thesis(off, tax) and not er.on_thesis(excluded, tax)


def pool_entries() -> list[dict]:
    return [
        make_entry(id="toolhive", topic="ai-security", domain="ais.mcp-tools",
                   title="ToolHive MCP SSRF: host-side discovery runs outside the sandbox",
                   source_url="https://github.com/advisories/GHSA-pr64-jmmf-jp54",
                   article_url="https://github.com/advisories/GHSA-pr64-jmmf-jp54"),
        make_entry(id="citrix", topic="product-security", domain="ps.appsec",
                   title="Citrix NetScaler Pre-Auth Heap Overflow (CVE-2026-8452)",
                   source_url="https://labs.watchtowr.example/citrix",
                   article_url="https://labs.watchtowr.example/citrix"),
        make_entry(id="chaindrop", topic="ai-security", domain="ais.model-supply-chain",
                   title="ChainDrop npm worm steals CI OIDC tokens from runner memory",
                   summary="ChainDrop npm worm, OIDC tokens, GitHub Actions.",
                   source_url="https://unit42.example/sdlc", article_url="https://unit42.example/sdlc"),
        make_entry(id="agent-rce", topic="ai-security", domain="ais.prompt-injection",
                   title="Coding agent tricked into RCE",
                   source_url="https://embracethered.example.com/blog/agent-rce/",
                   article_url="https://embracethered.example.com/blog/agent-rce/"),
    ]  # fmt: skip


def test_score_matches_by_url_vuln_id_and_title_entities_and_lists_miss_hosts():
    result = er.score(collected(), pool_entries(), tx.get())
    how = {r["title"].split()[0]: r["how"] for r in result["matched_rows"]}
    assert how["ToolHive:"] == "url"
    assert how["Citrix"] == "id"
    assert how["ChainDrop"] == "title+entities"
    assert how["Indirect"] == "url"  # via the story the post links to
    missed = {m["title"] for m in result["misses"]}
    assert "Acme Widget Path Traversal Vulnerability" in missed
    assert "My favourite sourdough recipe" not in missed  # off-thesis, not scored
    assert result["recall"] == round(result["matched"] / result["on_thesis"], 3)
    assert sum(result["miss_hosts"].values()) == len(result["misses"])
    assert "nvd.nist.gov" in result["miss_hosts"]


def test_the_same_link_from_two_curators_counts_once():
    a = er.item("tldrsec", "Story", "https://x.example/a?utm_source=tldrsec.com", SINCE)
    b = er.item("simon", "Story again", "https://x.example/a", SINCE)
    assert len(er.dedupe([a, b])) == 1


def test_http_get_refuses_hosts_outside_the_curators():
    with pytest.raises(ValueError, match="not a curator host"):
        er.http_get("https://evil.example.com/x")


def test_cli_fixtures_mode_writes_the_weekly_file_and_prints_the_summary(sandbox, capsys):
    for topic in common.TOPICS:
        pool = common.empty_pool(topic)
        pool["entries"] = [e for e in pool_entries() if e["topic"] == topic]
        common.save_pool(topic, pool)
    rc = er.main(["--fixtures", str(FIXTURES), "--write"])
    out = capsys.readouterr().out.strip().splitlines()
    assert out[-1].startswith("EVAL recall FAIL recall=") and "week=2026-W29" in out[-1]
    assert rc == 1  # below the 85% bar
    assert any(line.startswith("MISS [kev] Acme Widget") for line in out)
    saved = json.loads((sandbox / "data" / "evals" / "recall-2026-W29.json").read_text())
    assert saved["passed"] is False and saved["generated"].startswith("2026-07-15")
    out_file = sandbox / "elsewhere" / "recall.json"
    assert er.main(["--fixtures", str(FIXTURES), "--out", str(out_file)]) == 1
    assert json.loads(out_file.read_text())["recall"] == saved["recall"]


REAL_FIXTURE_SOURCE = er.fixture_source


def failing_source(*down):
    def factory(directory, since, newest=er.TLDRSEC_MAX_ISSUES):
        real = REAL_FIXTURE_SOURCE(directory, since, newest)

        def get(name):
            if name in down:
                raise ConnectionError(f"{name} down")
            return real(name)

        return get

    return factory


def test_a_curator_outage_is_an_error_and_fails_the_eval(sandbox, capsys):
    items, errors = er.collect(failing_source("kev")(FIXTURES, SINCE), SINCE)
    assert errors == ["kev: ConnectionError: kev down"] and items  # others still counted


@pytest.mark.parametrize("down,rc", [(("kev",), 1), (("tldrsec", "simon", "ghsa", "kev"), 2)])
def test_a_partial_or_total_outage_writes_no_result(sandbox, monkeypatch, capsys, down, rc):
    """A score from three curators of four isn't this week's recall: nothing is
    written, so neither post's row nor a --write file can carry it."""
    monkeypatch.setattr(er, "fixture_source", failing_source(*down))
    out_file = sandbox / "recall.json"
    assert er.main(["--fixtures", str(FIXTURES), "--write"]) == rc
    assert er.main(["--fixtures", str(FIXTURES), "--out", str(out_file)]) == rc
    assert not out_file.exists() and not (sandbox / "data" / "evals").exists()
    out = capsys.readouterr()
    assert "not writing" in out.err and "EVAL recall FAIL" in out.out


def test_recall_is_reported_per_curator_and_independent_of_curator_link_ingest():
    entries = pool_entries()
    # ChainDrop is held only because the curator-link ingestor staged it.
    entries[2] = {**entries[2], "curated_by": "tldrsec"}
    entries[0] = {**entries[0], "source_id": "curator:tldrsec"}  # ToolHive, via source_id
    result = er.score(collected(), entries, tx.get())
    per = result["recall_by_curator"]
    assert set(per) == set(result["by_curator"])
    assert sum(t["on_thesis"] for t in per.values()) == result["on_thesis"]
    assert sum(t["matched"] for t in per.values()) == result["matched"]
    assert per["tldrsec"]["matched"] == 1 and per["tldrsec"]["independent_matched"] == 0
    assert per["ghsa"]["matched"] == 1 and per["ghsa"]["independent_matched"] == 0
    assert per["kev"]["independent_matched"] == per["kev"]["matched"] == 1
    ind = result["independent"]
    assert ind["independent_matched"] == result["matched"] - 2
    assert ind["independent_recall"] == round(ind["independent_matched"] / result["on_thesis"], 3)
    assert result["recall"] > ind["independent_recall"]


def chaindrop_recall(**over) -> dict:
    """Recall when ChainDrop's only holder is a curator-staged entry with `over`."""
    entries = pool_entries()
    entries[2] = {**entries[2], "curated_by": "tldrsec", **over}
    return er.score(collected(), entries, tx.get())


@pytest.mark.parametrize(
    "over",
    [
        {"needs_review": True},
        {"grounding_score": 0.5},
        {"lessons": [{"point": "x", "excerpt": "y", "grounded": False}]},
        {"verified": False},
    ],
)
def test_an_unvetted_curator_staged_entry_does_not_count_as_held(over):
    vetted, unvetted = chaindrop_recall(), chaindrop_recall(**over)
    assert unvetted["matched"] == vetted["matched"] - 1
    miss = next(m for m in unvetted["misses"] if m["title"].startswith("ChainDrop"))
    assert miss["unvetted"] == "chaindrop"
    assert unvetted["recall_by_curator"]["tldrsec"]["matched"] == 0


def test_a_vetted_curator_staged_entry_counts_and_other_entries_need_no_vetting():
    vetted = chaindrop_recall(needs_review=False, verified=True, grounding_score=1.0)
    assert vetted["recall_by_curator"]["tldrsec"]["matched"] == 1
    entries = pool_entries()
    entries[1] = {**entries[1], "needs_review": True}  # Citrix: not curator-staged
    assert er.score(collected(), entries, tx.get())["recall_by_curator"]["kev"]["matched"] == 1


def test_the_result_carries_flat_independent_and_per_curator_recall():
    result = chaindrop_recall()
    assert result["independent_recall"] == result["independent"]["independent_recall"]
    assert result["curator_recall"]["tldrsec"] == {"recall": 0.333, "independent_recall": 0.0}


def test_without_curator_staged_entries_independent_equals_overall():
    result = er.score(collected(), pool_entries(), tx.get())
    assert result["independent"]["independent_recall"] == result["recall"]
    assert all(not r["via_curator"] for r in result["matched_rows"])


def test_cli_prints_per_curator_lines_and_the_independent_figure(sandbox, capsys):
    er.main(["--fixtures", str(FIXTURES)])
    out = capsys.readouterr().out.splitlines()
    assert any(line.startswith("CURATOR tldrsec: ") for line in out)
    assert " independent=" in out[-1]


def test_tldrsec_headlines_carry_only_their_story_url():
    page = (FIXTURES / "tldr-sec-339.html").read_text()
    for it in er.parse_tldrsec_issue(page, "2026-07-10"):
        assert it["urls"] == [it["url"]] and "tldrsec.com" not in it["url"]
