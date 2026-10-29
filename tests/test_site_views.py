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
        "ids",
        "exploited",
    }
    assert data["archive"][0]["domain"] == "Agents & Harnesses"
    assert len(data["archive"][2]["takeaway"]) <= gh.ARCHIVE_TAKEAWAY_CHARS + 2


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
    ledger = ledger_of(
        make_claim(id="a", first_seen="2026-07-12"),
        make_claim(id="b"),
        make_claim(id="c", status="contested"),
    )
    data = build(
        sandbox,
        entries=[make_entry(title="Fresh", source_url="https://e.com/f", published="2026-07-14")],
        ledger=ledger,
    )
    rendered = {r["id"] for r in data["findings"] + data["editorial"]}
    assert data["top_stories"] and set(data["top_stories"]) <= rendered
    assert data["top_stories_topped_up"] is True  # one story < five
    assert "top_claims" not in data  # "What to do now" is gone
    assert data["claim_changes_fresh"] == 1
    assert [(ch["kind"], ch["claim"]) for ch in data["claim_changes"]] == [
        ("added", "a"),
        ("added", "b"),
        ("contested", "c"),
    ]


def test_claim_changes_name_the_winner_and_the_claim_it_replaced(sandbox):
    ledger = ledger_of(
        make_claim(
            id="old",
            status="refuted",
            superseded_by=["new"],
            superseded_on="2026-07-13",
            supersession_reason="It broke.",
        ),
        make_claim(id="new", supersedes=["old"], first_seen="2026-07-13"),
    )
    data = build(sandbox, ledger=ledger)
    assert data["claim_changes"] == [
        {"kind": "overturned", "date": "2026-07-13", "claim": "new", "replaced": "old"}
    ]


# --- Template JS in Node -------------------------------------------------------
FNS = [
    "esc",
    "safeUrl",
    "hrefOf",
    "num",
    "safeRel",
    "clean",
    "txt",
    "rich",
    "isBoilerplate",
    "sortedUpdates",
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
    "windowNote",
    "biggestNote",
    "biggestHTML",
    "topStoriesHTML",
    "rowsById",
    "emergingBlock",
    "secHead",
    "lessonsHTML",
    "changesNote",
    "topEvidence",
    "evidenceLine",
    "claimChangeHTML",
    "claimChangesHTML",
    "quotePreview",
    "checkedChip",
    "caveatChips",
    "idChip",
    "triageChips",
    "alsoReported",
    "storyUpdates",
    "articleHTML",
    "newsCardHTML",
    "ageText",
    "validChange",
    "ledgerCounts",
    "countsLine",
    "lastChange",
    "claimMatches",
    "sortClaims",
    "claimEvidenceHTML",
    "claimHTML",
    "doLine",
    "claimChain",
    "storyMatches",
    "allStories",
    "storyCard",
    "clearFiltersFor",
    "effKey",
    "effMatches",
    "efficiencyClaimHTML",
    "efficiencyHTML",
    "efficiencyNote",
    "stateObjs",
    "fieldOptions",
    "cleanField",
    "stateFromQuery",
    "statePairs",
    "stateQuery",
    "shareHref",
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
    labels = re.search(r"var CHANGE_LABEL = \{.*?\};", src).group(0)
    labels += "\n" + re.search(r"var CHECKED_TIP = .*?;\n", src, re.S).group(0)
    labels += "\n" + re.search(r"var CONF_TIP = .*?;\n", src, re.S).group(0)
    labels += "\n" + re.search(r"var BOILERPLATE = .*?;\n", src, re.S).group(0)
    labels += "\n" + re.search(r"var claimState = \{.*?\};", src).group(0)
    labels += "\n" + re.search(r"var EFF_DOMAINS = \{.*?\};", src).group(0)
    labels += "\n" + re.search(r"var EFF_LABEL = \{.*?\};", src).group(0)
    for name in ("newsState", "archiveState", "siteState"):
        labels += "\n" + re.search(rf"var {name} = \{{.*?\}};", src).group(0)
    labels += "\n" + re.search(r"var STATE_MAX_Q = .*?;", src).group(0)
    labels += "\n" + re.search(r"var STATE_FIELDS = \[.*?\n  \];", src, re.S).group(0)
    prelude = (
        "var TMETA = {}; var TOPIC_ORDER = ['ai-security'];\n"
        f"{labels}\nvar DATA = {json.dumps(data)};\n"
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
        "claim_changes": [
            {"kind": "added", "date": EVIL, "claim": EVIL},
            {"kind": "overturned", "date": EVIL, "claim": EVIL, "replaced": "old"},
            {"kind": "contested", "date": EVIL, "claim": "old"},
        ],
        "claim_changes_fresh": EVIL,
        "snapshot_days": EVIL,
    }


def evil_claim_data():
    """evil_data with every claim field a change card renders made hostile."""
    data = evil_data()
    evidence = [
        {
            "stance": "supports",
            "url": EVIL_URL,
            "source_name": EVIL,
            "published": EVIL,
            "title": EVIL,
        },
        {"stance": EVIL, "url": EVIL_URL, "source_name": EVIL, "published": "9999", "title": EVIL},
    ]
    for claim in data["claims"]:
        claim.update(
            title=EVIL,
            statement=EVIL + "!",
            status=EVIL,
            topic=EVIL,
            supersession_reason=EVIL,
            evidence=evidence,
        )
    return data


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
        "lessonsHTML(DATA.findings[0])",
    ],
)
def test_new_sinks_render_hostile_rows_inert(expr):
    data = evil_data()
    data["findings"][0]["lessons"] = [{"point": EVIL, "excerpt": EVIL, "grounded": EVIL}]
    assert_inert(run_js(data, expr))


@pytest.mark.parametrize(
    "expr",
    [
        "DATA.claim_changes.map(claimChangeHTML).join('')",
        "claimChangesHTML()",
        "evidenceLine(DATA.claims[0])",
        "claimChangeHTML({kind: 'overturned', claim: 'old', replaced: 'old', date: DATA.claims[0].title})",
    ],
)
def test_claim_change_sinks_render_hostile_claims_inert(expr):
    html = run_js(evil_claim_data(), expr)
    assert html and EVIL not in html
    assert_inert(html)


def test_claim_changes_skip_unknown_kinds_and_missing_claims():
    data = {
        "claims": [{"id": "a", "status": "current", "title": "A"}],
        "claim_changes": [
            {"kind": "__proto__", "claim": "a", "date": "2026-07-01"},
            {"kind": "toString", "claim": "a", "date": "2026-07-01"},
            {"kind": "added", "claim": "missing", "date": "2026-07-01"},
            "not an object",
            None,
        ],
    }
    assert run_js(data, "DATA.claim_changes.map(claimChangeHTML).join('')") == ""


def test_claim_change_card_shows_the_reversal_and_shows_the_do_line():
    data = {
        "topics": {},
        "claims": [
            {
                "id": "new",
                "status": "current",
                "title": "New belief",
                "statement": "The full new statement.",
                "guidance": "DO-THIS-ON-THE-CLAIMS-TAB",
                "topic": "ai-security",
                "evidence": [
                    {
                        "stance": "supports",
                        "url": "https://a.example/1",
                        "source_name": "Older",
                        "published": "2026-06-01",
                    },
                    {
                        "stance": "supports",
                        "url": "https://b.example/2",
                        "source_name": "Newer",
                        "published": "2026-07-01",
                    },
                    {
                        "stance": "contests",
                        "url": "https://c.example/3",
                        "source_name": "Contra",
                        "published": "2026-08-01",
                    },
                ],
            },
            {
                "id": "old",
                "status": "refuted",
                "title": "Old belief",
                "supersession_reason": "Ten scanners missed it.",
            },
        ],
        "claim_changes": [
            {"kind": "overturned", "date": "2026-07-20", "claim": "new", "replaced": "old"}
        ],
    }
    html = run_js(data, "claimChangeHTML(DATA.claim_changes[0])")
    assert "Overturned" in html and "Jul 20, 2026" in html
    assert "New belief" in html and "The full new statement." in html
    assert "<s>" in html and "Old belief" in html and 'href="?claim=old#claims"' in html
    assert "Ten scanners missed it." in html and "refuted" in html
    assert "3 sources" in html and "https://b.example/2" in html and "Newer" in html
    assert "<b>Do.</b> DO-THIS-ON-THE-CLAIMS-TAB" in html


def test_site_and_readme_print_the_same_changes_sentence():
    import briefing

    cases = [(0, 0), (0, 3), (1, 3), (2, 4), (3, 3), (9, 6)]
    js = ",".join(f"changesNote({f}, {t}, 7, 'Jul 20, 2026')" for f, t in cases)
    got = run_js({}, "[" + js + "]")
    assert got == [briefing.changes_note(f, t, 7, "Jul 20, 2026") for f, t in cases]
    assert "the last change was Jul 20, 2026." in got[1]


def test_old_tab_links_redirect_to_the_nearest_view():
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    aliases = re.search(r"var VIEW_ALIASES = (\{.*?\});", src).group(1)
    got = json.loads(re.sub(r"(\w+):", r'"\1":', aliases))
    assert got == {"fields": "topics", "feed": "news", "lessons": "news"}
    views = re.search(r"var VIEWS = \{(.*?)\};", src, re.S).group(1)
    assert set(got.values()) <= set(re.findall(r"(\w+):", views))


def test_hostile_shapes_do_not_throw():
    data = evil_data()
    data["findings"][0].update(corroborators="x", updates={"a": 1})
    got = run_js(data, "[storyCardHTML(DATA.findings[0], 0), storyPanelHTML(DATA.findings[0])]")
    assert all(isinstance(h, str) and h for h in got)


def test_a_top_story_card_is_compact_like_a_news_card():
    """Rohan, 2026-10-26: top stories were already expanded. A card shows one
    "Also reported by" line and the two newest updates; the panel has the rest."""
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
            {"date": "2026-09-09", "note": "third", "url": ""},
        ],
    }
    html = run_js({"topics": {}, "findings": [row]}, "storyCardHTML(DATA.findings[0], 2)")
    assert "srclist" not in html and "Also reported by: O0, O1, O2, O3 +2" in html
    assert "7 sources" in html and ">3</span>" in html
    assert "first" not in html and html.index("third") < html.index("second")
    panel = run_js({"topics": {}, "findings": [row]},
                   "allUpdates(DATA.findings[0]) + storySources(DATA.findings[0])")  # fmt: skip
    assert all(f"https://o{i}.example/" in panel for i in range(6)) and "first" in panel


SHUFFLED = [
    {"date": "2026-09-05", "note": "mid-a", "url": "https://u.example/a"},
    {"date": "2026-09-09", "note": "newest", "url": ""},
    {"date": "2026-09-01", "note": "oldest", "url": ""},
    {"date": "2026-09-05", "note": "mid-b", "url": ""},
]


def test_updates_are_newest_first_whatever_order_the_payload_has():
    """ISC-43: the card shows the two newest, the panel every one; ties keep payload order."""
    row = {"id": "s", "topic": "ai-security", "title": "T", "url": "https://l.example/"}
    data = {"topics": {}, "findings": [{**row, "updates": SHUFFLED}]}
    card = run_js(data, "storyUpdates(DATA.findings[0])")
    assert "newest" in card and "mid-a" in card
    assert "mid-b" not in card and "oldest" not in card
    assert card.index("newest") < card.index("mid-a")
    panel = run_js(data, "allUpdates(DATA.findings[0])")
    order = [panel.index(n) for n in ("newest", "mid-a", "mid-b", "oldest")]
    assert order == sorted(order)
    assert run_js(data, "DATA.findings[0].updates.map(function (u) { return u.note; })") == [
        u["note"] for u in SHUFFLED
    ]  # the payload itself is not reordered


def test_metric_boilerplate_is_not_shown_as_a_quote():
    """ISC-50: a CVSS table cell is skipped for the next lesson, else no quote."""

    def lesson(text):
        return {"point": "p", "excerpt": text, "grounded": True}

    boiler = [
        "Attack Vector: Network, Attack Complexity: Low",
        "This metric reflects the context by which exploitation is possible.",
        "Score CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    ]
    base = {"id": "s", "topic": "ai-security", "title": "T", "url": "https://l.example/"}
    fallback = {**base, "lessons": [lesson(b) for b in boiler] + [lesson("A real sentence.")]}
    none = {**base, "lessons": [lesson(b) for b in boiler]}
    data = {"topics": {}, "findings": [fallback, none]}
    got = run_js(data, "[quotePreview(DATA.findings[0]), quotePreview(DATA.findings[1])]")
    assert "A real sentence." in got[0] and "Attack Vector" not in got[0]
    assert got[1] == ""


def test_backtick_spans_render_as_escaped_code():
    """ISC-50: escape first, then wrap, so a payload `<b>` never becomes markup."""
    row = {
        "id": "s",
        "topic": "ai-security",
        "title": "T",
        "url": "https://l.example/",
        "takeaway": "Use `<b>bold</b>` and `rm -rf` carefully",
        "lessons": [
            {"point": "p", "excerpt": "call `<img src=x onerror=1>` now", "grounded": True}
        ],
        "updates": [{"date": "2026-09-09", "note": "patched `v1.2`", "url": ""}],
    }
    data = {"topics": {}, "findings": [row]}
    html = run_js(
        data,
        "quotePreview(DATA.findings[0]) + newsCardHTML(DATA.findings[0], {}) + "
        "storyUpdates(DATA.findings[0])",
    )
    assert "<code>&lt;b&gt;bold&lt;/b&gt;</code>" in html
    assert "<code>&lt;img src=x onerror=1&gt;</code>" in html
    assert "<code>rm -rf</code>" in html and "<code>v1.2</code>" in html
    assert "<b>" not in html and "<img" not in html and "`" not in html


def test_a_pinned_reversal_is_labeled_last_reversal():
    data = {
        "topics": {},
        "claims": [
            {"id": "new", "status": "current", "title": "New belief", "topic": "ai-security"}
        ],
        "claim_changes": [
            {"kind": "overturned", "date": "2026-01-20", "claim": "new", "replaced": "new"},
            {"kind": "overturned", "date": "2026-10-20", "claim": "new", "replaced": "new"},
        ],
    }
    data["claim_changes"][0]["pinned"] = True
    old, fresh = run_js(
        data, "[claimChangeHTML(DATA.claim_changes[0]), claimChangeHTML(DATA.claim_changes[1])]"
    )
    assert "Last reversal" in old and "Overturned" not in old
    assert "Overturned" in fresh and "Last reversal" not in fresh


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


SITE_TABS = ("week", "news", "claims", "topics", "archive", "methodology")


def test_rendered_site_has_every_view_section(sandbox):
    html = gh.render(build(sandbox), NOW)
    for view in SITE_TABS:
        assert f'id="view-{view}"' in html and f'data-view="{view}"' in html
    assert re.findall(r'data-view="(\w+)"', html) == list(SITE_TABS)  # tab order


def test_header_is_title_sentence_and_chips_methods_prose_on_methodology(sandbox):
    html = gh.render(build(sandbox), NOW)
    head = html[html.index('<header class="masthead">') : html.index("</header>")]
    assert "<h1>" in head and head.count('<p class="sub">') == 1 and 'id="dateline"' in head
    assert 'id="methods"' not in html and "rolling last" not in html
    method = _extract(gh.TEMPLATE.read_text(encoding="utf-8"), "renderMethodology")
    for word in (
        "<b>Finding</b>",
        "<b>Takeaway</b>",
        "<b>Lessons</b>",
        "<b>Claim</b>",
        "<b>Source-checked (automated)</b>",
    ):
        assert word in method
    assert "not human review" in method


# --- UX review: cards, ledger, search ------------------------------------------
def _evil_lessons(data):
    data["findings"][0]["lessons"] = [{"point": EVIL, "excerpt": EVIL, "grounded": True}]
    data["findings"][0]["verified"] = True
    data["findings"][0]["caveats"] = [{"lens": EVIL, "note": EVIL}]
    data["findings"][0]["signals"] = [EVIL]
    return data


@pytest.mark.parametrize(
    "expr",
    [
        "articleHTML(DATA.findings[0], {kind: true, q: 'img'})",
        "newsCardHTML(DATA.findings[0], {kind: true, q: 'img'})",
        "quotePreview(DATA.findings[0], 'onerror')",
        "storyCard({f: DATA.findings[0], kind: 'research'}, 'x')",
        "DATA.claims.map(claimHTML).join('')",
        "DATA.claims.map(claimChain).join('')",
        "claimEvidenceHTML(DATA.claims[0].evidence)",
        "detailAnchor(DATA.findings[0], 'x')",
    ],
)
def test_review_sinks_render_hostile_rows_inert(expr):
    data = _evil_lessons(evil_claim_data())
    assert_inert(run_js(data, expr))


def test_story_titles_link_to_the_shareable_finding_url_not_raw_markdown():
    got = run_js({}, "detailAnchor({id: 'a b&c', detail_path: 'findings/x/y.md'}, 'T')")
    assert 'href="?finding=a%20b%26c#week"' in got and ".md" not in got


def test_cards_show_a_grounded_quote_and_no_single_source_count():
    row = {
        "id": "s",
        "topic": "ai-security",
        "title": "T",
        "url": "https://e.example/",
        "lessons": [
            {"point": "p0", "excerpt": "ungrounded quote", "grounded": False},
            {"point": "p1", "excerpt": "first grounded quote", "grounded": True},
            {"point": "needle", "excerpt": "second quote", "grounded": True},
        ],
    }
    data = {"topics": {}, "findings": [row]}
    card, hit = run_js(
        data, "[storyCardHTML(DATA.findings[0], 0), quotePreview(DATA.findings[0], 'needle')]"
    )
    assert "first grounded quote" in card and "ungrounded quote" not in card
    assert "1 source" not in card
    assert "second quote" in hit  # a search shows the quote that matched


def test_ledger_cards_are_collapsed_with_guidance_inside_and_retired_lead_with_why():
    data = {
        "topics": {},
        "claims": [
            {
                "id": "a",
                "status": "superseded",
                "title": "A",
                "statement": "A said.",
                "superseded_by": ["b"],
                "supersession_reason": "A fell.",
                "confidence": 0.9,
                "basis": "A basis",
            },
            {
                "id": "b",
                "status": "refuted",
                "title": "B",
                "supersedes": ["a"],
                "superseded_by": ["c"],
                "supersession_reason": "B fell.",
            },
            {
                "id": "c",
                "status": "current",
                "title": "C",
                "statement": "C holds.",
                "supersedes": ["b"],
                "guidance": "Do C.",
                "basis": "C basis",
                "confidence": 0.8,
                "first_seen": "2016-06",
                "added_on": "2026-10-01",
            },
        ],
    }
    old, mid, live = run_js(data, "DATA.claims.map(claimHTML)")
    summary = live[: live.index("</summary>")]
    assert live.startswith("<details") and "Do C." in summary and "Do C." in live
    assert "80% confidence" in summary and "C basis" in live
    assert "belief dates from 2016-06" in live and "added to the ledger 2026-10-01" in live
    assert "confidence" not in old and "A basis" not in old
    assert old.index("A fell.") < old.index("Chain")
    chain = mid[mid.index("Chain") :]
    assert chain.index(">A<") < chain.index(">B<") < chain.index(">C<")  # A -> B -> C


def test_claim_chain_survives_a_cycle():
    data = {
        "claims": [
            {"id": "a", "status": "superseded", "supersedes": ["b"], "superseded_by": ["b"]},
            {"id": "b", "status": "superseded", "supersedes": ["a"], "superseded_by": ["a"]},
        ]
    }
    assert isinstance(run_js(data, "claimChain(DATA.claims[0])"), str)


def test_ledger_counts_and_sorting_use_status_not_review_dates():
    data = {
        "claims": [
            {"id": "x", "status": "current", "confidence": 0.5, "first_seen": "2020-01"},
            {"id": "y", "status": "contested", "confidence": 0.9, "changed_on": "2026-10-01"},
            {"id": "z", "status": "refuted", "superseded_on": "2026-09-01"},
        ]
    }
    data["claims"][0]["last_reviewed"] = "2026-10-22"  # bumped on every review: ignored
    got = run_js(
        data,
        "[countsLine(ledgerCounts(DATA.claims)),"
        " sortClaims(DATA.claims, 'change').map(function (c) { return c.id; }),"
        " sortClaims(DATA.claims, 'confidence').map(function (c) { return c.id; })]",
    )
    assert got == ["1 current · 1 contested · 1 retired", ["y", "z", "x"], ["y", "x", "z"]]


def test_stories_list_news_and_research_together():
    data = {
        "editorial": [{"id": "n", "title": "News"}],
        "findings": [{"id": "r", "title": "Research", "lessons": [{"excerpt": "a quote"}]}],
    }
    got = run_js(
        data,
        "[allStories().map(function (i) { return i.kind + ':' + i.f.id; }),"
        " storyMatches(DATA.findings[0], 'a quote'), storyMatches(DATA.findings[0], 'zzz')]",
    )
    assert got == [["news:n", "research:r"], True, False]


def test_age_is_counted_from_the_generated_date_not_the_clock():
    got = run_js(
        {"generated": "2026-10-22"},
        "[ageText('2026-10-22'), ageText('2026-10-19'), ageText('2026-07-20'),"
        " ageText('2016-06'), ageText('bogus'), ageText('2027-01-01')]",
    )
    assert got == ["today", "3 days ago", "3 months ago", "10 years ago", "", ""]


def test_empty_domains_are_greyed_and_claims_lead_the_count():
    data = {"findings": [], "claims": [{"id": "c", "domain_id": "ais.y"}]}
    empty, full = run_js(
        data,
        "[domainCard({id: 'ais.x', name: 'X', scope: 's'}),"
        " domainCard({id: 'ais.y', name: 'Y', scope: 's'})]",
    )
    assert 'class="domcard empty"' in empty and 'class="domcard"' in full
    assert full.index("1 claim") < full.index("0 findings")


def test_archive_takeaways_end_at_a_sentence():
    text = "First sentence is here. " * 4 + "Then a long tail " * 20
    got = gh.sentence_cut(text, 120)
    assert got.endswith(". …") and len(got) <= 122
    assert gh.sentence_cut("short", 120) == "short"
    assert gh.sentence_cut("word " * 100, 50).endswith("…")


def test_a_claim_link_clears_a_search_that_would_hide_the_claim():
    data = {"claims": [{"id": "a", "status": "current", "title": "Pickle loads run code"}]}
    got = run_js(
        data,
        "(function () { var out = [];"
        " claimState.q = 'pickle'; out.push(clearFiltersFor(DATA.claims[0]), claimState.q);"
        " claimState.q = 'zzz'; out.push(clearFiltersFor(DATA.claims[0]), claimState.q);"
        " claimState.topic = 'ai-research'; out.push(clearFiltersFor(DATA.claims[0]), claimState.topic);"
        " return out; })()",
    )
    assert got == [False, "pickle", True, "", True, "all"]


def test_an_ungrounded_excerpt_is_not_shown_as_a_verbatim_quote():
    row = {
        "lessons": [
            {"point": "kept", "excerpt": "real quote", "grounded": True},
            {"point": "flagged", "excerpt": "INVENTED QUOTE", "grounded": False},
        ]
    }
    html = run_js({"findings": [row]}, "lessonsHTML(DATA.findings[0])")
    assert "real quote" in html and "flagged" in html
    assert "INVENTED QUOTE" not in html and "excerpt not found in source" in html


def test_sentence_cut_does_not_end_at_abbreviations():
    text = (
        "Agents compared vs. humans in the U.S. trial, e.g. Claude, did well across tasks. "
        "The rest of this takeaway runs on for a long while past the limit."
    )
    got = gh.sentence_cut(text, 100)
    assert (
        got == "Agents compared vs. humans in the U.S. trial, e.g. Claude, did well across tasks. …"
    )
    assert (
        gh.sentence_cut("We tested v. 2. It held up. More " + "x " * 60, 40)
        == "We tested v. 2. It held up. …"
    )


def _card_data():
    return {
        "topics": {},
        "claims": [
            {
                "id": "g",
                "status": "current",
                "title": "T",
                "statement": "S",
                "confidence": 0.8,
                "guidance": "Pin <b>x</b> & verify.",
                "added_on": "2026-10-01",
            },
            {"id": "n", "status": "current", "title": "T2", "statement": "S2", "confidence": 0.6},
            {
                "id": "old",
                "status": "superseded",
                "guidance": "stale advice",
                "superseded_by": ["g"],
            },
        ],
        "claim_changes": [
            {"kind": "added", "claim": "g", "date": "2026-10-02"},
            {"kind": "added", "claim": "n", "date": "2026-10-02"},
        ],
    }


def test_collapsed_claim_card_shows_do_line_and_escapes_it():
    html = run_js(_card_data(), "claimHTML(DATA.claims[0])")
    summary = html[: html.index("</summary>")]
    assert '<p class="guide do"><b>Do.</b> Pin &lt;b&gt;x&lt;/b&gt; &amp; verify.</p>' in summary
    assert "<b>x</b>" not in html


def test_claim_card_without_guidance_has_no_do_line_in_summary():
    html = run_js(_card_data(), "claimHTML(DATA.claims[1])")
    assert "Do." not in html[: html.index("</summary>")]
    retired = run_js(_card_data(), "claimHTML(DATA.claims[2])")
    assert "stale advice" not in retired


def test_confidence_explainer_present_with_how_link():
    html = run_js(_card_data(), "claimHTML(DATA.claims[0])")
    summary = html[: html.index("</summary>")]
    assert "80% confidence" in summary and ">how?</a>" in summary
    assert 'data-goto="methodology"' in summary and 'data-anchor="method-confidence"' in summary
    assert "not a formula" in summary  # tooltip
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    assert 'id="method-confidence"' in src and "<b>Confidence</b>" in src


def test_claims_default_order_is_most_recently_changed_first():
    data = {
        "claims": [
            {"id": "evergreen", "status": "current", "confidence": 0.95, "first_seen": "2016-01"},
            {"id": "fresh", "status": "current", "confidence": 0.5, "added_on": "2026-10-20"},
            {"id": "changed", "status": "contested", "confidence": 0.6, "changed_on": "2026-10-25"},
        ]
    }
    got = run_js(
        data,
        "[claimState.sort, sortClaims(DATA.claims, claimState.sort).map(function (c) { return c.id; }),"
        " sortClaims(DATA.claims, 'confidence').map(function (c) { return c.id; })]",
    )
    assert got == ["change", ["changed", "fresh", "evergreen"], ["evergreen", "changed", "fresh"]]


def test_briefing_change_card_shows_do_line_only_when_guidance_exists():
    with_g, without = run_js(_card_data(), "DATA.claim_changes.map(claimChangeHTML)")
    assert "<b>Do.</b> Pin &lt;b&gt;x&lt;/b&gt; &amp; verify." in with_g
    assert "Do." not in without


# --- Biggest this week (JS) ----------------------------------------------------
def _story(rid, **over):
    return {
        "id": rid,
        "topic": "ai-security",
        "title": f"Story {rid}",
        "url": "https://example.com/" + rid,
        "published": "2026-07-14",
        "corroborators": [],
        "updates": [],
        "lessons": [],
        **over,
    }


def test_biggest_lane_renders_cards_with_the_exploited_chip():
    data = {
        "topics": {},
        "snapshot_days": 7,
        "biggest_stories": ["hot", "wide", "gone"],
        "findings": [_story("hot", exploited=True), _story("wide", exploited=False)],
        "editorial": [],
    }
    shown = {}
    html = run_js(data, "biggestHTML(DATA.__shown = {})")
    assert "Biggest this week" in html
    assert "Most covered or exploited in the last 7 days." in html
    assert html.count('class="art story"') == 2  # the unknown id is skipped
    assert html.count('class="chip exploited">Exploited<') == 1
    assert html.index("Story hot") < html.index("Story wide")
    assert shown == {}


def test_biggest_lane_marks_its_rows_shown_and_hides_when_empty():
    data = {
        "topics": {},
        "snapshot_days": 7,
        "biggest_stories": ["hot"],
        "findings": [_story("hot")],
        "editorial": [],
    }
    assert run_js(data, "(function(){var s={};biggestHTML(s);return s;})()") == {"hot": 1}
    empty = {
        "snapshot_days": 7,
        "biggest_stories": [],
        "findings": [_story("hot")],
        "editorial": [],
    }
    assert run_js(empty, "biggestHTML({})") == ""
    assert run_js({"snapshot_days": 7, "findings": [], "editorial": []}, "biggestHTML({})") == ""


def test_biggest_and_top_cards_carry_no_focus_chips():
    """Array.map passes the index and the array: the array must not read as `tags`."""
    data = {
        "topics": {},
        "snapshot_days": 7,
        "biggest_stories": ["hot"],
        "top_stories": ["hot", "wide"],
        "top_stories_fresh": 2,
        "findings": [_story("hot", exploited=True), _story("wide")],
        "editorial": [],
    }
    for expr in ("biggestHTML({})", "topStoriesHTML({})"):
        html = run_js(data, expr)
        assert 'class="art story"' in html
        assert "chip sig" not in html and "[object" not in html
    # a non-string `tags` value is ignored; strings still render as chips
    got = run_js(
        data,
        "[storyCardHTML(DATA.findings[0], 0, [{}, 3]), storyCardHTML(DATA.findings[0], 0, ['MCP'])]",
    )
    assert "chip sig" not in got[0] and 'chip sig">MCP<' in got[1]


def test_exploited_chip_is_only_for_a_true_boolean():
    data = {"topics": {}, "findings": [_story("a", exploited="yes"), _story("b", exploited=True)]}
    got = run_js(data, "[storyCardHTML(DATA.findings[0], 0), storyCardHTML(DATA.findings[1], 0)]")
    assert "Exploited" not in got[0] and "Exploited" in got[1]


# ---- shareable state: filters and search live in the URL ----

STATE_QUERY = "nq=prompt+injection&nkind=research&ntopic=ai-security"


def test_filtered_route_round_trips_state_url_state():
    expr = (
        "(function(){"
        "var applied = stateFromQuery('?cq=agent&cstatus=refuted&csort=confidence&nq=x&nkind=news');"
        "var first = [claimState.q, claimState.status, claimState.sort, newsState.q, newsState.kind];"
        "var cq = stateQuery('claims'), nq = stateQuery('news');"
        # Reset, then restore from the URLs built from the state.
        "claimState.q = ''; claimState.status = 'all'; claimState.sort = 'change';"
        "newsState.q = ''; newsState.kind = 'all';"
        "stateFromQuery('?' + cq + '&' + nq);"
        "return {applied: applied, first: first, cq: cq, nq: nq,"
        "  again: [claimState.q, claimState.status, claimState.sort, newsState.q, newsState.kind]};"
        "})()"
    )
    got = run_js({}, expr)
    assert got["first"] == ["agent", "refuted", "confidence", "x", "news"]
    assert got["again"] == got["first"]
    assert got["cq"] == "cq=agent&cstatus=refuted&csort=confidence"
    assert got["nq"] == "nq=x&nkind=news"
    assert set(got["applied"]) == {"cq", "cstatus", "csort", "nq", "nkind"}


def test_state_query_covers_every_search_and_filter_and_skips_defaults():
    expr = (
        "(function(){var out = {};"
        "stateFromQuery('?"
        + STATE_QUERY
        + "&ctopic=ai-security&aq=kev&atopic=ai-security&sq=hello');"
        "['news','claims','archive','search'].forEach(function(v){ out[v] = stateQuery(v); });"
        "out.defaults = (function(){ claimState.sort='change'; return stateQuery('week'); })();"
        "return out;})()"
    )
    got = run_js({}, expr)
    assert got["news"] == STATE_QUERY
    assert got["claims"] == "ctopic=ai-security"
    assert got["archive"] == "aq=kev&atopic=ai-security"
    assert got["search"] == "sq=hello"
    assert got["defaults"] == ""
    # Only defaults: nothing in the URL.
    expr = "(function(){stateFromQuery('?nkind=all&csort=change&cstatus=all');return stateQuery('news')+stateQuery('claims');})()"
    assert run_js({}, expr) == ""


@pytest.mark.parametrize(
    "query",
    [
        "?nkind=bogus&ceff=bogus&ntopic=nope&cstatus=__proto__&csort=toString&ctopic=%3Cb%3E&atopic=constructor",
        "?nkind=news%20&ntopic=AI-SECURITY&cstatus=",
    ],
)
def test_unknown_filter_values_are_ignored(query):
    expr = (
        "(function(){var applied = stateFromQuery(" + json.dumps(query) + ");"
        "return {applied: applied, news: newsState, claim: claimState, archive: archiveState};})()"
    )
    got = run_js({}, expr)
    assert got["applied"] == {}
    assert got["news"] == {"topic": "all", "kind": "all", "q": ""}
    assert got["claim"] == {
        "topic": "all",
        "eff": "all",
        "status": "all",
        "sort": "change",
        "q": "",
    }
    assert got["archive"] == {"topic": "all", "q": ""}


def test_hostile_search_value_in_url_renders_escaped():
    expr = (
        "(function(){stateFromQuery('?nq=' + encodeURIComponent(" + json.dumps(EVIL) + "));"
        "return {q: newsState.q, cards: DATA.findings.map(function(f){"
        "return storyCard({f: f, kind: 'research'}, newsState.q.toLowerCase()); }).join(''),"
        "input: '<input value=\"' + esc(newsState.q) + '\">'};})()"
    )
    got = run_js(evil_data(), expr)
    assert got["q"] == EVIL  # kept as text...
    assert_inert(got["input"])  # ...and escaped wherever it becomes markup
    assert_inert(got["cards"])


def test_search_text_is_length_capped():
    got = run_js(
        {}, "(function(){stateFromQuery('?nq=' + 'a'.repeat(5000)); return newsState.q.length;})()"
    )
    assert got == 200


def test_copy_link_button_is_keyboard_reachable_and_wired_to_the_panel_url():
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    btn = re.search(r'<button[^>]*id="modal-copy"[^>]*>', src).group(0)
    assert 'type="button"' in btn and 'aria-label="' in btn and "tabindex" not in btn
    assert 'id="modal-copy-url"' in src and "readonly" in src
    assert "navigator.clipboard.writeText" in src and "setTimeout(resetCopyBtn, 2000)" in src
    # openModal points the button at the panel's own URL.
    assert 'copyBtn.setAttribute("data-url", shareHref("finding", finding.id, pageBase()))' in src
    got = run_js(
        {},
        "[shareHref('finding', 'abc 1', 'https://x.test/site/'), shareHref('claim', 'c-1', 'https://x.test/site/')]",
    )
    assert got == [
        "https://x.test/site/?finding=abc%201#week",
        "https://x.test/site/?claim=c-1#claims",
    ]


# --- Triage chips (ISC-46) ------------------------------------------------------
def triage_row(**kw):
    row = {
        "id": "t1",
        "topic": "ai-security",
        "title": "A story",
        "url": "https://e.com/a",
        "takeaway": "Takeaway.",
        "published": "2026-10-20",
        "signals": ["week-of-2026-10-13", "timely", "high-relevance", "cve"],
        "tags": ["timely", "week-of-2026-10-13"],
        "ids": ["CVE-2026-12345", "GHSA-abcd-1234-wxyz"],
        "exploited": True,
        "corroborators": [],
        "updates": [],
    }
    row.update(kw)
    return row


def cards(data):
    return run_js({"topics": {}, **data}, ALL_CARDS)


ALL_CARDS = (
    "[storyCardHTML(DATA.r, 0), articleHTML(DATA.r), articleHTML(DATA.r, {kind: 1}),"
    " newsCardHTML(DATA.r), newsCardHTML(DATA.r, {kind: 1}), archiveRowHTML(DATA.r)]"
)


def test_extract_ids_finds_cve_and_ghsa_in_order():
    got = gh.extract_ids(
        "Patch cve-2026-0001 now", "see GHSA-ABCD-1234-wxyz and CVE-2025-99999", "https://x.io/p"
    )
    assert got == ["CVE-2026-0001", "GHSA-abcd-1234-wxyz", "CVE-2025-99999"]


def test_extract_ids_none_dedupes_and_caps():
    assert gh.extract_ids("", None, "no ids here, CVE-12-1 or GHSA-abc") == []
    assert gh.extract_ids("CVE-2026-1111 CVE-2026-1111", "cve-2026-1111") == ["CVE-2026-1111"]
    many = " ".join(f"CVE-2026-{n}" for n in range(1000, 1010))
    assert gh.extract_ids(many) == [f"CVE-2026-{n}" for n in range(1000, 1004)]
    assert gh.extract_ids("xCVE-2026-1111") == []


def test_payload_rows_carry_ids(sandbox):
    entry = make_entry(
        title="Exploit for CVE-2026-4242",
        takeaway="Also GHSA-aaaa-bbbb-cccc",
        source_url="https://e.com/q",
    )
    data = build(sandbox, entries=[entry])
    assert data["findings"][0]["ids"] == ["CVE-2026-4242", "GHSA-aaaa-bbbb-cccc"]


def test_id_chips_link_to_nvd_and_advisories_on_every_card():
    for html in cards({"r": triage_row()}):
        assert 'href="https://nvd.nist.gov/vuln/detail/CVE-2026-12345"' in html
        assert 'href="https://github.com/advisories/GHSA-abcd-1234-wxyz"' in html
        assert_inert(html)


def test_hostile_ids_render_inert():
    bad = [EVIL_URL, '"><img src=x onerror=alert(1)>', "CVE-2026-1<b>", EVIL, 7, None, {}]
    for html in cards({"r": triage_row(ids=bad)}):
        assert_inert(html)
        assert "chip vid" not in html


def test_no_pipeline_tags_on_cards():
    for html in cards({"r": triage_row()}):
        assert "week-of-" not in html and "timely" not in html
        assert "high-relevance" not in html and 'class="chip sig"' not in html


def test_exploited_chip_only_when_true():
    on = cards({"r": triage_row()})
    assert all('<span class="chip exploited">Exploited</span>' in h for h in on)
    for flag in (False, "true", 1, None):
        off = cards({"r": triage_row(exploited=flag)})
        assert not any("Exploited" in h for h in off)


# --- Efficiency track (cost / work) -------------------------------------------
def eff_data(claims, **over):
    base = {"claims": claims, "findings": [], "editorial": [], "generated": NOW, "topics": {}}
    return base | over


def eff_claim(cid, domain_id, **over):
    return {
        "id": cid,
        "topic": "ai-research",
        "domain_id": domain_id,
        "title": cid,
        "statement": cid + " statement",
        "status": "current",
        "evidence": [],
        "first_seen": "2026-07-10",
        **over,
    }


def test_efficiency_filter_narrows_claims_and_unknown_value_is_ignored():
    claims = [
        eff_claim("c1", "air.cost-efficiency"),
        eff_claim("w1", "air.work-efficiency"),
        eff_claim("o1", "air.evals"),
    ]
    got = run_js(
        eff_data(claims),
        "['cost','work','all','bogus','__proto__','constructor'].map(function (e) {"
        " return DATA.claims.filter(function (c) { return effMatches(c, e); })"
        ".map(function (c) { return c.id; }); })",
    )
    everyone = ["c1", "w1", "o1"]
    assert got == [["c1"], ["w1"], everyone, everyone, everyone, everyone]


def test_clearing_filters_for_a_claim_resets_the_efficiency_filter():
    data = eff_data([eff_claim("o1", "air.evals")])
    expr = "(claimState.eff = 'cost', clearFiltersFor(DATA.claims[0]), claimState.eff)"
    assert run_js(data, expr) == "all"


def test_efficiency_section_is_hidden_when_empty():
    assert run_js(eff_data([]), "efficiencyHTML({})") == ""
    data = eff_data(
        [eff_claim("o1", "air.evals")],
        efficiency_claims=["o1", "missing"],
        efficiency_findings=["nope"],
    )
    assert run_js(data, "efficiencyHTML({})") == ""
    assert run_js(eff_data([], efficiency_claims="junk"), "efficiencyHTML(null)") == ""


def test_efficiency_section_lists_claims_in_payload_order_and_findings_once():
    claims = [eff_claim("c1", "air.cost-efficiency"), eff_claim("w1", "air.work-efficiency")]
    data = eff_data(
        claims,
        findings=[evil_row(id="f1", title="Fresh find")],
        efficiency_claims=["w1", "c1"],
        efficiency_findings=["f1"],
    )
    html = run_js(data, "efficiencyHTML({})")
    assert html.index("w1 statement") < html.index("c1 statement")
    assert "Fresh find" in html
    assert "Fresh find" not in run_js(data, "efficiencyHTML({f1: 1})")


def test_efficiency_section_renders_hostile_values_inert():
    claim = eff_claim("c1", "air.cost-efficiency", title=EVIL, statement=EVIL + "!", status=EVIL)
    claim["evidence"] = [{"stance": "supports", "url": EVIL_URL, "source_name": EVIL}]
    data = eff_data([claim], efficiency_claims=["c1"], efficiency_findings=[])
    html = run_js(data, "efficiencyHTML({})")
    assert html and EVIL not in html
    assert_inert(html)


def test_site_and_readme_print_the_same_efficiency_sentence():
    import briefing

    assert run_js({}, "efficiencyNote()") == briefing.efficiency_note()


def test_front_page_ships_efficiency_picks_as_ids(sandbox):
    ledger = ledger_of(
        make_claim(id="cost-1", topic="ai-research", domain="Cost Efficiency"),
        make_claim(id="other-1", topic="ai-research", domain="Evals"),
    )
    data = build(sandbox, ledger=ledger)
    assert data["efficiency_claims"] == ["cost-1"]
    assert data["efficiency_findings"] == []


def test_efficiency_filter_round_trips_through_the_url_and_ignores_unknown_values():
    expr = (
        "(function(){"
        "var applied = stateFromQuery('?ceff=cost&cstatus=current');"
        "var q = stateQuery('claims');"
        "claimState.eff = 'all'; claimState.status = 'all';"
        "stateFromQuery('?' + q);"
        "var back = claimState.eff;"
        "claimState.eff = 'all'; claimState.status = 'all';"
        "claimState.eff = 'work'; stateFromQuery('?ceff=bogus');"
        "var bad = claimState.eff;"
        "stateFromQuery('?ceff=__proto__');"
        "var proto = claimState.eff;"
        "claimState.eff = 'all'; claimState.status = 'all';"
        "return {applied: applied, q: q, back: back, bad: bad, proto: proto,"
        " dflt: stateQuery('claims')};"
        "})()"
    )
    got = run_js({}, expr)
    assert got["applied"] == {"ceff": "cost", "cstatus": "current"}
    assert got["q"] == "ceff=cost&cstatus=current"
    assert got["back"] == "cost"
    assert got["bad"] == "work" and got["proto"] == "work"  # unknown values leave state alone
    assert got["dflt"] == ""  # the default never reaches the URL
