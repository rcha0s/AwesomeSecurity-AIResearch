"""arguments.py: the committed rows behind "What practitioners are arguing" (ISC-61).

The model supplies prose and URLs; code checks every URL against this run's signal,
computes the engagement, ages rows out, and the merge gate re-checks the file's shape.
"""

from __future__ import annotations

import json

import arguments as ar
import common as c
import content_checks as cc
import generate_html as gh
import pytest
from conftest import make_entry
from test_claims import ledger_of, make_claim
from test_site_views import EVIL, assert_inert, run_js

TODAY = "2026-07-15"
R1 = "https://www.reddit.com/r/netsec/comments/abc123/mcp_servers_are_rce/"
R2 = "https://www.reddit.com/r/LLMDevs/comments/def456/should_agents_ask_first/"
R3 = "https://www.reddit.com/r/AI_Agents/comments/ghi789/sandbox_or_not/"
X1 = "https://x.com/alice_sec/status/1900000000000000001"
X2 = "https://x.com/bob_dev/status/1900000000000000002"
X3 = "https://x.com/alice_sec/status/1900000000000000003"  # alice again
CFG = {**ar.DEFAULTS}


def write_signal(sandbox, rows):
    (sandbox / "data" / "_practitioner_signal.json").write_text(json.dumps(rows))


def self_post(permalink, score, comments, title="A self post", created="2026-07-14T10:00:00+00:00"):
    return {
        "title": title,
        "permalink": permalink,
        "score": score,
        "comments": comments,
        "sub": "netsec",
        "created": created,
    }


@pytest.fixture
def signal(sandbox):
    write_signal(sandbox, [self_post(R1, 300, 100), self_post(R2, 50, 10)])
    pool = c.load_pool("ai-security")
    pool["entries"].append(
        make_entry(
            topic="ai-security",
            title="Agent approval bypass",
            source_url="https://example.com/a",
            published="2026-07-13",
            reddit_url=R3,
            reddit_score=20,
            reddit_comments=5,
        )
    )
    pool["entries"].append(
        make_entry(
            topic="ai-security",
            title="Harness note",
            source_url="https://example.com/b",
            published="2026-07-14",
            discovered_via="x-list",
            tweet_url=X1,
        )
    )
    c.save_pool("ai-security", pool)
    c.save_json(
        c.CANDIDATES_FILE,
        [
            {
                "title": "Staged X post",
                "published": "2026-07-15",
                "discovered_via": "x-list",
                "tweet_url": X2,
            },
            {
                "title": "Alice again",
                "published": "2026-07-15",
                "discovered_via": "x-list",
                "tweet_url": X3,
            },
        ],
    )
    return sandbox


def arg(
    *urls,
    position="MCP servers should be treated as untrusted code.",
    counter="Most are read-only.",
):
    return {"position": position, "counterpoint": counter, "sources": list(urls)}


# --- URLs ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "url,kind",
    [
        (R1, "reddit"),
        ("https://old.reddit.com/r/netsec/comments/abc123/", "reddit"),
        ("http://reddit.com/r/netsec/comments/abc123", "reddit"),
        (X1, "x"),
        ("https://twitter.com/alice_sec/status/1900000000000000001", "x"),
    ],
)
def test_permalinks_parse(url, kind):
    assert ar.parse_source(url)["kind"] == kind


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/r/netsec/comments/abc123/",
        "https://reddit.com.evil.com/r/netsec/comments/abc123/",
        "https://evil.com/?u=https://www.reddit.com/r/netsec/comments/abc123/",
        "https://www.reddit.com/r/netsec/",  # a subreddit, not a thread
        "https://www.reddit.com/r/netsec/comments/abc123/x?utm=1",
        "https://x.com/alice_sec",  # a profile
        "https://x.com/alice_sec/status/12",  # not a real id
        "javascript:alert(1)",
        None,
        42,
    ],
)
def test_other_urls_are_not_permalinks(url):
    assert ar.parse_source(url) is None


# --- The signal ---------------------------------------------------------------------
def test_signal_collects_self_posts_candidates_and_pool_entries(signal):
    sig = ar.load_signal(CFG)
    assert set(sig) == {
        "reddit:abc123",
        "reddit:def456",
        "reddit:ghi789",
        "x:1900000000000000001",
        "x:1900000000000000002",
        "x:1900000000000000003",
    }
    assert sig["reddit:ghi789"]["score"] == 20 and sig["reddit:ghi789"]["comments"] == 5


def test_stale_signal_is_not_citable(sandbox):
    write_signal(sandbox, [self_post(R1, 300, 100, created="2026-06-01T00:00:00+00:00")])
    assert ar.load_signal(CFG) == {}


# --- Merge --------------------------------------------------------------------------
def merged(staged, existing=(), today=TODAY, cfg=CFG):
    return ar.merge_rows(list(existing), staged, ar.load_signal(cfg), cfg, today)


def test_a_row_takes_its_numbers_from_the_signal_not_the_model(signal):
    staged = [{**arg(R1, R2, X1, X2, X3), "reddit_score": 99999, "weight": 99999}]
    rows, notes = merged(staged)
    assert notes == []
    row = rows[0]
    assert (row["reddit_score"], row["reddit_comments"]) == (350, 110)
    assert row["x_authors"] == 2  # alice (twice) and bob
    assert row["weight"] == 350 + 2 * 110 + 2 * 25 == 620
    assert [s["label"] for s in row["sources"]][:2] == ["r/netsec", "r/LLMDevs"]
    assert ar.row_problems(row, CFG) == []


def test_x_only_rows_weigh_distinct_authors(signal):
    rows, _ = merged([arg(X1, X3), arg(X1, X2)])
    by_authors = {r["x_authors"]: r["weight"] for r in rows}
    assert by_authors == {1: 25, 2: 50}


@pytest.mark.parametrize(
    "bad,why",
    [
        (arg(R1, "https://example.com/blog"), "not a Reddit or X permalink"),
        (arg(R1, "https://www.reddit.com/r/netsec/comments/zzz999/"), "not in this run's signal"),
        (arg(R1), "needs 2-6 distinct sources"),
        (arg(R1, R1), "needs 2-6 distinct sources"),
        (arg(R1, R2, position=""), "position empty"),
        (arg(R1, R2, position="x" * 281), "position empty or over"),
        (arg(R1, R2, counter="y" * 281), "counterpoint over"),
        ("just text", "not an object"),
    ],
)
def test_bad_arguments_are_dropped_with_a_reason(signal, bad, why):
    rows, notes = merged([bad])
    assert rows == [] and why in notes[0]


def test_at_most_max_new_per_run_rows_are_taken(signal):
    staged = [arg(R1, R2, position=f"p{i}") for i in range(3)]
    rows, notes = merged(staged, cfg={**CFG, "max_new_per_run": 1})
    assert len(rows) == 1 and "over max_new_per_run" in notes[0]


def test_a_new_row_replaces_an_old_one_that_shares_a_thread(signal):
    old, _ = merged([arg(R1, R2, position="old")], today="2026-07-10")
    rows, _ = merged([arg(R1, X1, position="new")], existing=old)
    assert [r["position"] for r in rows] == ["new"]


def test_rows_age_out_after_row_days_and_rank_by_weight(signal):
    first, _ = merged([arg(R1, R2, position="big")], today="2026-07-10")
    second, _ = merged([arg(X1, X2, position="small")], existing=first, today="2026-07-12")
    assert [r["position"] for r in second] == ["big", "small"]
    on_day_14, _ = merged([], existing=second, today="2026-07-24")  # big is 14 days old
    assert [r["position"] for r in on_day_14] == ["big", "small"]
    day_15, _ = merged([], existing=second, today="2026-07-25")  # big is 15 days old
    assert [r["position"] for r in day_15] == ["small"]
    assert ar.shown(second, "2026-07-25", CFG)[0]["position"] == "small"  # the page agrees


def test_the_store_and_the_page_have_their_own_caps(signal):
    rows = [
        {
            **merged([arg(R1, R2, position="p")])[0][0],
            "id": f"arg-{i:010x}",
            "reddit_score": i,
            "reddit_comments": 0,
            "weight": i,
        }
        for i in range(8)
    ]
    assert len(ar.shown(rows, TODAY, CFG)) == CFG["max_rows"]
    assert [r["weight"] for r in ar.shown(rows, TODAY, CFG)] == [7, 6, 5, 4, 3]


def test_cli_signal_and_merge(signal, capsys):
    assert ar.main(["signal"]) == 0
    first = json.loads(capsys.readouterr().out.splitlines()[0])
    assert first["url"] == R1 and first["score"] == 300  # best engagement first
    (signal / "data" / ar.OUT_NAME).write_text(json.dumps([arg(R1, R2)]))
    assert ar.main(["merge"]) == 0
    stored = json.loads((signal / "data" / ar.ROWS_NAME).read_text())
    assert stored[0]["created"] == TODAY and cc.arguments_problems(stored) == []
    assert ar.main(["nonsense"]) == 2


def test_merge_with_no_staging_file_keeps_live_rows(signal):
    rows, _ = merged([arg(R1, R2)])
    c.save_json(c.DATA_DIR / ar.ROWS_NAME, rows)
    assert ar.main(["merge"]) == 0
    assert json.loads((c.DATA_DIR / ar.ROWS_NAME).read_text()) == rows


# --- The gate -----------------------------------------------------------------------
def good_row(signal):
    return merged([arg(R1, R2, X1)])[0][0]


def test_the_gate_accepts_what_merge_writes(signal):
    assert cc.arguments_problems([good_row(signal)], CFG) == []
    assert cc.arguments_problems([], CFG) == []


def test_the_gate_refuses_a_link_that_is_not_a_reddit_or_x_permalink(signal):
    row = good_row(signal)
    row["sources"][0]["url"] = "https://evil.example/r/netsec/comments/abc123/"
    assert any("permalink" in p for p in cc.arguments_problems([row], CFG))
    row = good_row(signal)
    row["sources"][0]["url"] = "https://www.reddit.com/r/netsec/comments/abc123/?x=1"
    assert any("permalink" in p for p in cc.arguments_problems([row], CFG))


@pytest.mark.parametrize(
    "tamper,why",
    [
        (lambda r: r.update(weight=r["weight"] + 1), "weight"),
        (lambda r: r.update(x_authors=5), "x_authors"),
        (lambda r: r.update(extra="<img>"), "keys"),
        (lambda r: r.update(position="z" * 281), "position"),
        (lambda r: r.update(created="yesterday"), "created"),
        (lambda r: r.update(reddit_score=True), "reddit_score"),
        (lambda r: r.update(id="arg-<script>"), "id"),
        (lambda r: r.update(sources=r["sources"][:1]), "sources"),
        (lambda r: r["sources"][0].update(label="r/other"), "label"),
        (lambda r: r["sources"][0].update(kind="x"), "label"),
        (lambda r: r["sources"].append(dict(r["sources"][0])), "repeated"),
    ],
)
def test_the_gate_refuses_tampered_rows(signal, tamper, why):
    row = good_row(signal)
    tamper(row)
    assert cc.arguments_problems([row], CFG), why


def test_the_gate_refuses_too_many_rows_a_duplicate_id_and_a_non_list(signal):
    row = good_row(signal)
    assert any("duplicate" in p for p in cc.arguments_problems([row, row], CFG))
    many = [{**row, "id": f"arg-{i:010x}"} for i in range(CFG["store_max"] + 1)]
    assert any("more than" in p for p in cc.arguments_problems(many, CFG))
    assert cc.arguments_problems({"a": 1}, CFG) == ["arguments.json: not a list"]
    assert cc.arguments_problems(["row"], CFG)


# --- Payload and page ---------------------------------------------------------------
def test_payload_ships_live_rows_ranked_and_nothing_else(signal):
    rows, _ = merged([arg(X1, X2, position="small"), arg(R1, R2, position="big")])
    old = {**rows[0], "id": "arg-0000000000", "created": "2026-06-01"}
    c.save_json(c.DATA_DIR / ar.ROWS_NAME, rows + [old])
    (signal / "data" / "archive.json").write_text("[]")
    data = gh.build_payload(ledger_of(make_claim()), c.load_config(), TODAY)
    assert [r["position"] for r in data["arguments"]] == ["big", "small"]
    assert all(r["id"] != "arg-0000000000" for r in data["arguments"])


def test_payload_arguments_default_to_empty(sandbox):
    (sandbox / "data" / "archive.json").write_text("[]")
    assert gh.build_payload(ledger_of(make_claim()), c.load_config(), TODAY)["arguments"] == []


def page_row(**over):
    return {
        "id": "arg-0123456789",
        "created": TODAY,
        "position": "Sandboxes beat approval prompts.",
        "counterpoint": "Prompts catch intent.",
        "sources": [
            {"url": R1, "label": "r/netsec", "kind": "reddit"},
            {"url": X1, "label": "@alice_sec", "kind": "x"},
        ],
        "reddit_score": 300,
        "reddit_comments": 100,
        "x_authors": 1,
        "weight": 525,
        **over,
    }


def test_the_section_renders_ranked_by_weight_with_every_link():
    rows = [page_row(position="Small", weight=5), page_row(position="Big", weight=900)]
    html = run_js({"arguments": rows}, "argumentsHTML()")
    assert "What practitioners are arguing" in html
    assert html.index("Big") < html.index("Small")
    assert "300 points and 100 comments on Reddit; 1 author on X" in html
    assert f'href="{R1}"' in html and f'href="{X1}"' in html
    assert "Counterpoint: Prompts catch intent." in html


@pytest.mark.parametrize("arguments", [None, [], "x", {}, [None], [page_row(position="")]])
def test_an_empty_section_renders_nothing(arguments):
    assert run_js({"arguments": arguments}, "argumentsHTML()") == ""


def test_a_row_needs_two_reddit_or_x_links_on_the_page_too():
    one = page_row(sources=[{"url": R1, "label": "r/netsec", "kind": "reddit"}])
    off_host = page_row(
        sources=[
            {"url": R1, "label": "a", "kind": "reddit"},
            {"url": "https://evil.example/x", "label": "b", "kind": "x"},
        ]
    )
    assert run_js({"arguments": [one, off_host]}, "argumentsHTML()") == ""


@pytest.mark.parametrize("field", ["position", "counterpoint", "reddit_score", "x_authors"])
def test_hostile_row_values_render_inert(field):
    row = page_row(**{field: EVIL})
    row["sources"] += [
        {"url": "javascript:alert(1)", "label": EVIL, "kind": "x"},
        {"url": R2 + '"onmouseover=alert(1) x="', "label": EVIL, "kind": "reddit"},
    ]
    html = run_js({"arguments": [row]}, "argumentsHTML()")
    assert html and EVIL not in html
    assert_inert(html)
    assert "javascript:" not in html


def test_the_week_view_places_the_section_after_biggest_and_before_top_stories():
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    line = next(ln for ln in src.splitlines() if "var html = focusHTML(shown)" in ln)
    assert line.index("biggestHTML") < line.index("argumentsHTML") < line.index("topStoriesHTML")
