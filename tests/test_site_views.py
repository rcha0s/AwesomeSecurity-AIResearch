"""Phase 6 site views: top stories, claim lineage + deep links, topic/domain
pages on taxonomy IDs, the archive, methodology.

Payload side: what build_payload adds. Template side: the new JS runs in Node
against hostile rows, because a scan PR shapes the payload and every value that
reaches innerHTML must be escaped (text) or scheme-checked (links).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import common
import generate_html as gh
import pytest
from conftest import make_entry
from test_claims import ledger_of, make_claim

NOW = "2026-07-15"
EVIL = '<img src=x onerror=alert(1)>"onmouseover=alert(2) x="'
EVIL_URL = "javascript:alert(3)"


def build(sandbox, entries=(), archive=(), ledger=None):
    for entry in entries:
        pool = common.load_pool(entry["topic"])
        pool["entries"].append(entry)
        common.save_pool(entry["topic"], pool)
    (sandbox / "data" / "archive.json").write_text(json.dumps(list(archive)))
    return gh.build_payload(ledger or ledger_of(make_claim()), common.load_config(), NOW)


# --- Payload -------------------------------------------------------------------
def test_archive_ships_only_vetted_findings_newest_first_and_compact(sandbox):
    old = make_entry(title="Old vetted", source_url="https://e.com/o", published="2026-03-01")
    newer = make_entry(title="Newer vetted", source_url="https://e.com/n", published="2026-05-02")
    held = make_entry(title="Held", source_url="https://e.com/h", needs_review=True)
    long_take = make_entry(
        title="Long", source_url="https://e.com/l", published="2026-01-01", takeaway="word " * 200
    )
    data = build(sandbox, archive=[old, newer, held, long_take])
    assert [r["title"] for r in data["archive"]] == ["Newer vetted", "Old vetted", "Long"]
    assert data["archive_count"] == 4 and data["archive_vetted"] == 3
    assert set(data["archive"][0]) == {
        "id",
        "topic",
        "domain",
        "domain_id",
        "title",
        "url",
        "source_name",
        "published",
        "takeaway",
    }
    assert data["archive"][0]["domain"] == "Agents & Harnesses"
    assert len(data["archive"][2]["takeaway"]) <= gh.ARCHIVE_TAKEAWAY_CHARS + 1


def test_topics_carry_taxonomy_domain_ids(sandbox):
    data = build(sandbox)
    ids = [d["id"] for d in data["topics"]["ai-security"]["domain_ids"]]
    assert "ais.prompt-injection" in ids and all(i.startswith("ais.") for i in ids)
    assert all(d["name"] and d["scope"] for d in data["topics"]["ai-security"]["domain_ids"])


def test_claims_get_a_domain_id_without_changing_the_ledger(sandbox):
    ledger = ledger_of(make_claim(topic="ai-security", domain="Prompt Injection"))
    before = json.dumps(ledger, sort_keys=True)
    data = build(sandbox, ledger=ledger)
    assert data["claims"][0]["domain_id"] == "ais.prompt-injection"
    assert json.dumps(ledger, sort_keys=True) == before


def test_trends_ship_without_members_and_capped(sandbox):
    rows = [
        {"tag": f"t{i}", "count": 3, "recent": 1, "momentum": 1.0, "members": [{"title": "x"}]}
        for i in range(gh.TREND_ROWS + 5)
    ]
    (sandbox / "data" / "trends.json").write_text(json.dumps({"ai-security": rows}))
    got = build(sandbox)["trends"]["ai-security"]
    assert len(got) == gh.TREND_ROWS and not any("members" in r for r in got)


def test_news_gate_rows_have_no_detail_page_editorial_rows_keep_theirs():
    rows = [
        {"lane": "news", "detail_path": "findings/a/b/c.md"},
        {"lane": "editorial", "detail_path": "findings/a/b/d.md"},
    ]
    assert [r["detail_path"] for r in gh.without_missing_pages(rows)] == ["", "findings/a/b/d.md"]


def test_front_page_picks_are_ids_of_rendered_rows_and_claims(sandbox):
    ledger = ledger_of(make_claim(id="a", last_reviewed="2026-07-01"), make_claim(id="b"))
    data = build(
        sandbox,
        entries=[make_entry(title="Fresh", source_url="https://e.com/f", published="2026-07-14")],
        ledger=ledger,
    )
    rendered = {r["id"] for r in data["findings"] + data["editorial"]}
    assert data["top_stories"] and set(data["top_stories"]) <= rendered
    assert data["top_stories_topped_up"] is True  # one story < five
    assert data["top_claims"] == ["a", "b"]


# --- Template JS in Node -------------------------------------------------------
FNS = [
    "esc",
    "safeUrl",
    "hrefOf",
    "num",
    "safeRel",
    "clean",
    "txt",
    "tname",
    "tcls",
    "topicPill",
    "host",
    "fmtDate",
    "src",
    "detailAnchor",
    "arr",
    "has",
    "isRetired",
    "routeQuery",
    "routeLink",
    "claimById",
    "claimIds",
    "claimRef",
    "claimLineage",
    "storySources",
    "allUpdates",
    "storyCardHTML",
    "storyPanelHTML",
    "topicDomains",
    "domainInfo",
    "byDomainId",
    "domainCard",
    "archiveRowHTML",
    "archiveMatches",
    "tvar",
    "emergingBlock",
]


def _extract(src: str, name: str) -> str:
    start = src.index(f"function {name}(")
    depth = 0
    for i in range(src.index("{", start), len(src)):
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        if depth == 0:
            return src[start : i + 1]
    raise ValueError(name)


def run_js(data: dict, expr: str):
    if not shutil.which("node"):
        pytest.skip("node not available")
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    prelude = (
        "var TMETA = {}; var TOPIC_ORDER = ['ai-security'];\n" f"var DATA = {json.dumps(data)};\n"
    )
    script = (
        prelude
        + "\n".join(_extract(src, n) for n in FNS)
        + f"\nprocess.stdout.write(JSON.stringify({expr}));"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=10)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def assert_inert(html: str):
    assert "<img" not in html and "<script" not in html.lower()
    assert "javascript:" not in html
    # Raw quotes only ever delimit attribute values (data quotes are &quot;), so
    # with the values blanked any surviving on*= is a real event-handler attribute.
    tags = re.sub(r'"[^"]*"', '""', html)
    assert not re.search(r"<[a-z][^>]*\son\w+=", tags), html


def evil_row(**over):
    row = {
        "id": EVIL,
        "topic": EVIL,
        "domain": EVIL,
        "title": EVIL,
        "takeaway": EVIL,
        "summary": EVIL + "!",
        "url": EVIL_URL,
        "source_name": EVIL,
        "published": EVIL,
        "detail_path": EVIL,
        "corroborators": [
            {"url": EVIL_URL, "source_name": EVIL, "tier": EVIL},
            {"url": "https://ok.example/a", "source_name": "Ok", "tier": "high"},
        ],
        "updates": [{"date": EVIL, "note": EVIL, "url": EVIL_URL, "source_name": EVIL}],
    }
    return {**row, **over}


def evil_data():
    return {
        "topics": {
            "ai-security": {
                "name": EVIL,
                "domain_ids": [{"id": "ais.x", "name": EVIL, "scope": EVIL}],
            }
        },
        "findings": [evil_row(domain_id="ais.x")],
        "claims": [
            {"id": "old", "status": "superseded", "title": EVIL, "superseded_by": [EVIL]},
            {"id": EVIL, "status": "current", "statement": EVIL, "supersedes": "old"},
            {"id": "c", "status": "current", "title": "C", "domain_id": "ais.x"},
        ],
        "archive": [evil_row(domain_id="ais.x")],
        "trends": {"ai-security": [{"tag": EVIL, "count": EVIL, "recent": 1, "momentum": 1}]},
    }


@pytest.mark.parametrize(
    "expr",
    [
        "storyCardHTML(DATA.findings[0], 0)",
        "storyPanelHTML(DATA.findings[0])",
        "storySources(DATA.findings[0])",
        "allUpdates(DATA.findings[0])",
        "archiveRowHTML(DATA.archive[0])",
        "claimLineage(DATA.claims[0]) + claimLineage(DATA.claims[1])",
        "domainCard(DATA.topics['ai-security'].domain_ids[0])",
        "routeLink('claims', {claim: DATA.claims[1].id}, txt(DATA.claims[1].statement))",
        "emergingBlock('ai-security', false, 10)",
    ],
)
def test_new_sinks_render_hostile_rows_inert(expr):
    assert_inert(run_js(evil_data(), expr))


def test_hostile_shapes_do_not_throw():
    data = evil_data()
    data["findings"][0].update(corroborators="x", updates={"a": 1})
    got = run_js(data, "[storyCardHTML(DATA.findings[0], 0), storyPanelHTML(DATA.findings[0])]")
    assert all(isinstance(h, str) and h for h in got)


def test_story_card_lists_every_source_and_update():
    row = {
        "id": "s",
        "topic": "ai-security",
        "title": "T",
        "url": "https://lead.example/",
        "source_name": "Lead",
        "corroborators": [
            {"url": f"https://o{i}.example/", "source_name": f"O{i}"} for i in range(6)
        ],
        "updates": [
            {"date": "2026-09-01", "note": "first", "url": "https://u.example/1"},
            {"date": "2026-09-05", "note": "second", "url": ""},
        ],
    }
    html = run_js({"topics": {}, "findings": [row]}, "storyCardHTML(DATA.findings[0], 2)")
    assert all(f"https://o{i}.example/" in html for i in range(6))  # no "+N" truncation
    assert "6 source" not in html and ">7<" not in html
    assert "7 sources" in html and ">3</span>" in html
    assert html.index("second") < html.index("first")  # newest update first


def test_claim_lineage_links_both_directions_through_deep_links():
    data = {
        "claims": [
            {"id": "old", "status": "refuted", "title": "Old", "superseded_by": ["new"]},
            {"id": "new", "status": "current", "title": "New", "supersedes": ["old"]},
        ]
    }
    old, new = run_js(data, "[claimLineage(DATA.claims[0]), claimLineage(DATA.claims[1])]")
    assert "Replaced by" in old and 'href="?claim=new#claims"' in old
    assert "Replaces" in new and "<s>" in new and 'href="?claim=old#claims"' in new


def test_route_links_encode_their_params():
    got = run_js({}, "routeLink('topics', {domain: 'a b&c'}, 'x')")
    assert 'href="?domain=a%20b%26c#topics"' in got and 'data-route="domain=a%20b%26c"' in got


def test_domain_lookup_ignores_prototype_keys():
    got = run_js(
        {"topics": {"ai-security": {"domain_ids": [{"id": "ais.x"}]}}},
        "[domainInfo('ais.x') && domainInfo('ais.x').topic, domainInfo('__proto__'),"
        " topicDomains('__proto__').length, topicDomains('constructor').length]",
    )
    assert got == ["ai-security", None, 0, 0]


def test_archive_search_matches_title_source_and_domain_and_filters_by_track():
    row = {"topic": "ai-security", "title": "Memory Trap", "takeaway": "", "source_name": "OWASP"}
    row |= {"domain": "Data Poisoning", "domain_id": "ais.data-poisoning"}
    expr = (
        "[archiveMatches(DATA.archive[0], 'all', 'memory'), archiveMatches(DATA.archive[0], 'all', 'owasp'),"
        " archiveMatches(DATA.archive[0], 'all', 'ais.data'), archiveMatches(DATA.archive[0], 'ai-research', ''),"
        " archiveMatches(DATA.archive[0], 'all', 'zzz')]"
    )
    assert run_js({"archive": [row]}, expr) == [True, True, True, False, False]


def test_methodology_numbers_come_from_the_payload_through_num():
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    body = _extract(src, "renderMethodology")
    for key in ("max_age_days", "news_front_page_days", "news_front_page_max", "snapshot_days"):
        assert f"num(D.{key})" in body
    assert not re.search(r"\+ D\.\w+ \+", body)  # no raw payload value concatenated


def test_rendered_site_has_every_view_section(sandbox):
    html = gh.render(build(sandbox), NOW)
    for view in ("week", "topics", "news", "claims", "lessons", "feed", "archive", "methodology"):
        assert f'id="view-{view}"' in html and f'data-view="{view}"' in html
