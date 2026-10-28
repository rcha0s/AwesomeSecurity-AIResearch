"""Tests for the static site generator — the docs/ tree GitHub Pages serves."""

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


# --- Rendered chips + lessons view (MR-D) -----------------------------------
def test_rendered_html_wires_caveat_chip_template(sandbox):
    """The rendered site is a JS-driven SPA — the chip class + data-lens
    attribute only exist client-side. Lock (a) the JS template that emits the
    chip is present and (b) the caveat data reaches the embedded JSON payload,
    so pytest alone can regress-test the wiring end-to-end."""
    entry = make_entry(
        title="Restated result",
        caveats=[{"lens": "prior-art", "note": "cf. Zhao 2024"}],
    )
    payload_of(sandbox, entries=[entry])
    html = gh.render(gh.build_payload(ledger_of(make_claim()), common.load_config(), NOW), NOW)
    # (a) The JS uses this exact class name; CSS keys on it.
    assert "chip caveat" in html
    # (b) The caveat lens + note reach the client. Extract the JSON payload and
    # look for the caveat there, so a broken payload can't slip past.
    block = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', html, re.S)
    data = json.loads(block.group(1).replace("<\\/", "</"))
    row = data["findings"][0]
    assert row["caveats"] == [{"lens": "prior-art", "note": "cf. Zhao 2024"}]


def test_lessons_are_not_a_tab_old_links_redirect_to_the_archive(sandbox):
    """Lessons live in each finding's detail panel now, not in their own view."""
    html = gh.render(gh.build_payload(ledger_of(make_claim()), common.load_config(), NOW), NOW)
    assert 'data-view="lessons"' not in html and 'id="view-lessons"' not in html
    assert 'data-view="feed"' not in html and 'id="view-feed"' not in html
    assert 'lessons: "news"' in html and 'feed: "news"' in html


def test_finding_rows_carry_their_lessons_with_quotes(sandbox):
    """The detail panel reads each row's lessons: point + verbatim excerpt."""
    entry = make_entry(
        title="Compaction saves tokens",
        lessons=[
            {"point": "Summarize before re-injecting", "excerpt": "40% less", "confidence": 0.9}
        ],
    )
    data = payload_of(sandbox, entries=[entry])
    assert "lessons" not in data  # no flat list: no Lessons view to feed
    assert data["findings"][0]["lessons"] == [
        {"point": "Summarize before re-injecting", "excerpt": "40% less", "grounded": True}
    ]


def test_lesson_without_excerpt_is_dropped(sandbox):
    """A lesson without an excerpt isn't groundable and can't be defended."""
    entry = make_entry(
        lessons=[
            {"point": "solid", "excerpt": "quote", "confidence": 0.9},
            {"point": "empty", "excerpt": "", "confidence": 0.9},
            {"point": "missing"},  # no excerpt key at all
            "a bare string",
        ],
    )
    data = payload_of(sandbox, entries=[entry])
    assert [le["point"] for le in data["findings"][0]["lessons"]] == ["solid"]


# --- Refuter-panel caveats --------------------------------------------------
def test_finding_row_omits_caveats_when_entry_has_none(sandbox):
    """Default entries have no caveats — the field must be absent or empty so
    the render layer doesn't render an empty chip block."""
    data = payload_of(sandbox, entries=[make_entry(title="Uncaveated")])
    row = data["findings"][0]
    assert row.get("caveats", []) == []


def test_finding_row_carries_prior_art_caveat(sandbox):
    """When drift review has attached prior-art/scope caveats to the entry,
    the finding row surfaces them so the render layer can chip them."""
    entry = make_entry(
        title="Restated result",
        caveats=[{"lens": "prior-art", "note": "cf. Zhao 2024"}],
    )
    data = payload_of(sandbox, entries=[entry])
    row = data["findings"][0]
    assert len(row["caveats"]) == 1
    assert row["caveats"][0]["lens"] == "prior-art"
    assert row["caveats"][0]["note"] == "cf. Zhao 2024"


def test_finding_row_drops_malformed_caveats(sandbox):
    """A malformed caveat entry (not a dict, or missing lens) is dropped so a
    stale field can't crash the render."""
    entry = make_entry(
        title="Bad caveat",
        caveats=[
            {"lens": "scope", "note": "narrow"},
            "not a dict",
            {"note": "missing lens"},
        ],
    )
    data = payload_of(sandbox, entries=[entry])
    row = data["findings"][0]
    assert len(row["caveats"]) == 1
    assert row["caveats"][0]["lens"] == "scope"


# --- Detail modal wiring ----------------------------------------------------
def test_finding_row_carries_detail_path(sandbox):
    """The modal fetches by detail_path; if it's missing, clicks fall back to
    the raw source. Lock the exact path the modal expects."""
    data = payload_of(sandbox, entries=[make_entry(title="AsyncAPI npm compromise")])
    row = data["findings"][0]
    assert row["detail_path"] == (
        "findings/ai-research/agents/" "2026-07-asyncapi-npm-compromise.md"
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
        / "agents"
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
        / "agents"
        / "2026-07-provider-guardrails-blocked-incident-response.md"
    )
    assert detail.is_file(), (
        f"Editorial detail page not copied to {detail} — modal will 404 "
        f"on this card and fall back to the raw source."
    )


# --- News-lane wiring in editorial_rows -------------------------------------
def _news_source(
    sid: str, name: str, tier: str = "high", track: str = "news", scope: str = "ai"
) -> dict:
    return {"id": sid, "name": name, "tier": tier, "track": track, "scope": scope}


def _write_sources(sandbox, sources):
    (sandbox / "data" / "sources.json").write_text(json.dumps(sources), encoding="utf-8")


def _pool_news_entry(**over):
    from datetime import timedelta

    base = make_entry(
        id="news-openai-fast-mode",
        topic="ai-research",
        title="OpenAI ships Fast mode: Sol 2.5x quicker at same price",
        source_url="https://openai.com/blog/fast-mode",
        source_id="rss:openai-blog",
        published=(common.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d"),
        needs_review=True,
    )
    base.update(over)
    return base


def test_editorial_rows_includes_news_curated_entries(sandbox):
    _write_sources(sandbox, [_news_source("rss:openai-blog", "OpenAI Blog")])
    pool = common.load_pool("ai-research")
    pool["entries"].append(_pool_news_entry())
    common.save_pool("ai-research", pool)
    claims.save_ledger(ledger_of(make_claim()))
    rows = gh.editorial_rows(common.load_config(), 7)
    assert len(rows) == 1
    assert rows[0]["lane"] == "news"
    assert "OpenAI Blog" in rows[0]["reason"]


@pytest.mark.parametrize(
    "over",
    [
        {"grounding_score": 0.5},
        {"lessons": [{"point": "p", "excerpt": "e", "confidence": 0.9, "grounded": False}]},
        {"editorial": {"promoted": True}, "grounding_score": 0.0},
    ],
)
def test_news_lane_never_shows_an_ungrounded_story(sandbox, over):
    """The renderer holds the same grounding floor eval_integrity.py checks."""
    _write_sources(sandbox, [_news_source("rss:openai-blog", "OpenAI Blog")])
    pool = common.load_pool("ai-research")
    pool["entries"].append(_pool_news_entry(**over))
    common.save_pool("ai-research", pool)
    claims.save_ledger(ledger_of(make_claim()))
    assert gh.editorial_rows(common.load_config(), 7) == []


def test_editorial_rows_dedupes_same_story_across_sources(sandbox):
    _write_sources(
        sandbox,
        [
            _news_source("rss:openai-blog", "OpenAI Blog", tier="high"),
            _news_source("rss:hn", "Hacker News", tier="medium"),
        ],
    )
    from datetime import timedelta

    same_day = (common.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")

    a = _pool_news_entry(
        id="a-1",
        source_id="rss:openai-blog",
        title="OpenAI ships Fast mode: Sol 2.5x quicker at same price",
        source_url="https://openai.com/blog/fast-mode",
        published=same_day,
    )
    b = _pool_news_entry(
        id="b-2",
        source_id="rss:hn",
        title="Sol Fast mode: OpenAI ships 2.5x quicker at the same price",
        source_url="https://news.ycombinator.com/item?id=999",
        discovered_via="hackernews",
        signals={"hn_points": 250},
        published=same_day,
    )
    pool = common.load_pool("ai-research")
    pool["entries"].extend([a, b])
    common.save_pool("ai-research", pool)
    claims.save_ledger(ledger_of(make_claim()))
    rows = gh.editorial_rows(common.load_config(), 7)
    assert len(rows) == 1
    row = rows[0]
    assert row["title"].startswith("OpenAI ships")
    assert row.get("corroborators")
    assert row["corroborators"][0]["source_name"] == "Hacker News"


def test_editorial_rows_keeps_old_news(sandbox):
    """News is kept like claims: an old story stays in the lane."""
    _write_sources(sandbox, [_news_source("rss:openai-blog", "OpenAI Blog")])
    old = _pool_news_entry(published="2020-01-01")
    pool = common.load_pool("ai-research")
    pool["entries"].append(old)
    common.save_pool("ai-research", pool)
    claims.save_ledger(ledger_of(make_claim()))
    rows = gh.editorial_rows(common.load_config(), 7)
    assert [r["lane"] for r in rows] == ["news"]


def test_a_vetted_news_story_past_max_age_moves_from_findings_to_the_news_lane(sandbox):
    """Findings age out after max_age_days; a vetted story kept only as news is
    shown in the news lane (and so on the News tab), not as a finding."""
    _write_sources(sandbox, [_news_source("rss:openai-blog", "OpenAI Blog")])
    old = _pool_news_entry(published="2020-01-01", needs_review=False)
    fresh = _pool_news_entry(id="fresh-1", source_url="https://example.com/new", source_id="")
    fresh.update(needs_review=False, title="A different fresh story about tokens")
    data = payload_of(sandbox, entries=[old, fresh])
    assert [f["id"] for f in data["findings"]] == ["fresh-1"]
    news = {r["id"]: r for r in data["editorial"]}
    assert set(news) == {"news-openai-fast-mode"}
    assert news["news-openai-fast-mode"]["detail_path"]  # a vetted finding keeps its page
    assert "has_page" not in news["news-openai-fast-mode"]


def test_a_fresh_vetted_news_story_is_on_the_news_tab_once_not_also_a_finding(sandbox):
    """Every kept news story is on the News tab, vetted or not, fresh or not; a
    story is rendered in one lane, so the front page cannot list it twice."""
    import content_checks as cc

    _write_sources(sandbox, [_news_source("rss:openai-blog", "OpenAI Blog")])
    vetted = _pool_news_entry(needs_review=False)  # vetted, 2 days old, news source
    plain = _pool_news_entry(id="plain-1", source_url="https://example.com/p", source_id="")
    plain.update(needs_review=False, title="A different fresh story about tokens")
    data = payload_of(sandbox, entries=[vetted, plain])
    assert [f["id"] for f in data["findings"]] == ["plain-1"]
    assert [r["id"] for r in data["editorial"]] == ["news-openai-fast-mode"]
    assert data["editorial"][0]["detail_path"]  # it is a vetted finding: its page exists
    on_front = data["top_stories"]
    assert len(on_front) == len(set(on_front))
    assert cc.site_story_problems(data) == []


# --- Client-side markdown renderer ------------------------------------------
def _extract_js_function(src: str, name: str) -> str:
    """Pull one top-level `function <name>(...) { ... }` out of a JS blob by
    brace-counting, so a test can execute it standalone in Node."""
    start = src.index(f"function {name}(")
    brace = src.index("{", start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return src[start : i + 1]
    raise ValueError(f"unbalanced braces extracting {name}")


def test_modal_markdown_renderer_honors_hard_line_breaks():
    """generate_site.py joins each metadata field with a Markdown hard break
    ('  \\n' - two trailing spaces before the newline). The modal's
    hand-rolled renderMarkdown must render that as <br>, not silently
    collapse every field into one dense, unreadable run-on paragraph."""
    if not shutil.which("node"):
        pytest.skip("node not available")
    fn = _extract_js_function(gh.TEMPLATE.read_text(encoding="utf-8"), "renderMarkdown")
    script = fn + '\nprocess.stdout.write(renderMarkdown("**Topic:** X  \\n**Source:** Y"));'
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("<p>") == 1  # both fields stay in one paragraph
    assert "<br>" in result.stdout  # but on separate visual lines
    assert "Topic" in result.stdout and "Source" in result.stdout


# --- Front-page news cap and the News tab ------------------------------------
def _run_js(names: list[str], body: str) -> str:
    if not shutil.which("node"):
        pytest.skip("node not available")
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    script = "\n".join(_extract_js_function(src, n) for n in names) + "\n" + body
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_front_page_news_is_last_n_days_newest_first_capped():
    """The front page shows only recent news, newest first, at most `max`;
    older stories are left for the News tab."""
    body = """
    function day(n) { return new Date(Date.now() - n * 864e5).toISOString().slice(0, 10); }
    var rows = [];
    for (var i = 0; i < 40; i++) rows.push({ id: "n" + i, published: day(i % 6) });
    rows.push({ id: "old", published: day(8) }, { id: "undated", published: "" });
    var out = frontNews(rows, 7, 30);
    process.stdout.write(JSON.stringify({
      n: out.length, ids: out.map(function (r) { return r.id; }),
      sorted: out.every(function (r, i) { return !i || out[i - 1].published >= r.published; })
    }));
    """
    got = json.loads(_run_js(["_daysAgo", "frontNews"], body))
    assert got["n"] == 30 and got["sorted"]
    assert "old" not in got["ids"] and "undated" not in got["ids"]


def test_news_tab_groups_every_story_by_month_newest_first():
    body = """
    var g = newsByMonth([{ published: "2026-09-03" }, { published: "2026-10-12" },
      { published: "2026-10-01" }, { published: "" }]);
    process.stdout.write(JSON.stringify(g.map(function (x) { return [x.month, x.rows.length]; })));
    """
    assert json.loads(_run_js(["newsByMonth"], body)) == [
        ["2026-10", 2],
        ["2026-09", 1],
        ["undated", 1],
    ]


def test_payload_carries_the_front_page_news_settings(sandbox):
    claims.save_ledger(ledger_of(make_claim()))
    conf = common.load_config()
    payload = gh.build_payload(claims.load_ledger(), conf, "2026-07-15")
    assert payload["news_front_page_days"] == conf.news_front_page_days
    assert payload["news_front_page_max"] == conf.news_front_page_max


def test_real_config_caps_front_page_news_at_30_over_7_days():
    conf = common.load_config()
    assert (conf.news_front_page_days, conf.news_front_page_max) == (7, 30)


def _render_moved(sandbox) -> tuple[str, str]:
    import generate_site

    claims.save_ledger(ledger_of(make_claim()))
    pool = common.load_pool("ai-research")
    pool["entries"] += [
        make_entry(
            title="Relocated finding", domain="air.agents", domain_label="Agents & Harnesses"
        ),
        make_entry(
            title="Same dir",
            source_url="https://a/same",
            domain="air.agents",
            domain_label="Agents",
        ),
    ]
    common.save_pool("ai-research", pool)
    generate_site.main()
    assert gh.main() == 0
    tree = (
        sandbox / "ai-research" / "agents-harnesses" / "2026-07-relocated-finding.md"
    ).read_text()
    docs = sandbox / "docs" / "findings" / "ai-research" / "agents-harnesses"
    return tree, (docs / "2026-07-relocated-finding.md").read_text()


def test_old_page_paths_get_a_moved_stub_in_the_tree_and_the_docs_mirror(sandbox):
    """Pages moved when domains became IDs (old dir = slugified free-text label).
    A stub at the old path points at the new page, so outside links still work."""
    tree, docs = _render_moved(sandbox)
    assert tree == docs
    assert tree.startswith("# Moved\n")
    assert "](../agents/2026-07-relocated-finding.md)" in tree
    new_page = sandbox / "ai-research" / "agents" / "2026-07-relocated-finding.md"
    assert new_page.is_file() and not new_page.read_text().startswith("# Moved")
    # A label whose slug already equals the ID slug needs no stub (and never
    # overwrites the real page).
    assert (
        not (sandbox / "ai-research" / "agents" / "2026-07-same-dir.md")
        .read_text()
        .startswith("# Moved")
    )


def test_moved_stubs_are_deterministic(sandbox):
    first = _render_moved(sandbox)
    assert _render_moved(sandbox) == first


# --- Link hardening (auto-merge audit F3) ------------------------------------
# Scan PRs carry attacker-influenced URLs and markdown; the page must never turn
# them into script. Each case runs the template's own JS in Node.
LINK_FNS = ["esc", "safeUrl", "hrefOf", "safeRel", "renderMarkdown"]


def _links(body: str) -> list:
    return json.loads(_run_js(LINK_FNS, "process.stdout.write(JSON.stringify(" + body + "));"))


def test_non_http_hrefs_are_neutralised():
    got = _links(
        "['javascript:alert(1)', ' javascript:alert(1)', 'JaVaScRiPt:alert(1)',"
        " 'data:text/html,<b>x</b>', 'vbscript:x', 'https://ok.example/a?b=1&c=2',"
        " 'http://ok.example/', 'https://x.example/\"onmouseover=alert(1)', '', null]"
        ".map(hrefOf)"
    )
    assert got[:5] == ["#"] * 5
    assert got[5] == "https://ok.example/a?b=1&amp;c=2"
    assert got[6] == "http://ok.example/"
    assert got[7:] == ["#", "#", "#"]


def test_markdown_links_cannot_run_script_or_break_out_of_href():
    got = _links(
        "[renderMarkdown('[x](javascript:alert(1))'),"
        " renderMarkdown('[x](a\"onmouseover=alert(1))'),"
        " renderMarkdown('[x](https://e.example/\"onmouseover=alert(1))'),"
        " renderMarkdown('[ok](https://ok.example/p)'),"
        ' renderMarkdown(\'say "hi" [t"x](https://ok.example/)\')]'
    )
    # Quotes are escaped before link substitution, so none survive raw in text.
    assert "&quot;hi&quot;" in got[4] and "t&quot;x" in got[4]
    assert got[4].count('"') == 4  # exactly the two attribute value delimiters pairs
    assert 'href="#"' in got[0] and "javascript" not in got[0].split("</a>")[0].split(">")[0]
    assert 'href="#"' in got[1]
    for html in got[:3]:
        assert not re.search(r"<a [^>]*\son\w+=", html), html  # no event-handler attribute
    assert '<a href="https://ok.example/p"' in got[3]


def test_detail_paths_must_be_relative_findings_markdown():
    got = _links(
        "['findings/ai-security/x/a.md', 'javascript:alert(1)', 'https://evil.example/a.md',"
        " 'findings/../../x.md', '/findings/a.md', 'findings/a.html'].map(safeRel)"
    )
    assert got == ["findings/ai-security/x/a.md", "", "", "", "", ""]


def test_every_data_href_goes_through_the_scheme_check():
    src = gh.TEMPLATE.read_text(encoding="utf-8")
    assert not re.search(r"href=\"' \+ esc\([a-z]+\.url", src)
    assert "window.open(finding.url" not in src


def test_a_bare_host_or_empty_source_name_becomes_the_registry_name():
    """ISC-50: one source, one name, resolved in the payload (not in JS)."""
    sources = [
        {"id": "r1", "name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/"},
        {"id": "r2", "name": "Other", "handle": "https://blog.example.org/rss"},
    ]
    payload = {
        "findings": [
            {"source_name": "www.bleepingcomputer.com", "url": "https://x.example/a"},
            {"source_name": "", "url": "https://www.bleepingcomputer.com/news/a"},
            {"source_name": "blog.example.org", "url": ""},
            {"source_name": "Already Named", "url": "https://www.bleepingcomputer.com/b"},
            {"source_name": "unknown.example.net", "url": "https://unknown.example.net/"},
            {"source_name": "", "url": "https://unknown.example.net/"},
        ],
        "nested": {"updates": [{"source_name": "", "url": "https://blog.example.org/p"}]},
    }
    gh.normalize_source_names(payload, sources)
    assert [r["source_name"] for r in payload["findings"]] == [
        "BleepingComputer",
        "BleepingComputer",
        "Other",
        "Already Named",
        "unknown.example.net",
        "",
    ]
    assert payload["nested"]["updates"][0]["source_name"] == "Other"


@pytest.mark.parametrize(
    "tags,url,want",
    [
        (["exploited-in-the-wild"], "https://x.example/a", True),
        (["Active-Exploitation"], "https://x.example/a", True),
        (["kev", "cve"], "https://x.example/a", True),
        ([], "https://www.cisa.gov/known-exploited-vulnerabilities-catalog", True),
        ([], "https://cisa.gov/known-exploited-vulnerabilities", True),
        ([], "https://www.cisa.gov/news-events/alerts/2026/10/01/x", False),
        ([], "https://evilcisa.gov/known-exploited-vulnerabilities", False),
        ([], "https://x.example/cisa.gov/known-exploited-vulnerabilities", False),
        (["exploit"], "https://x.example/a", False),
        (None, "", False),
        ("kev", "", False),
    ],
)
def test_is_exploited_rule(tags, url, want):
    assert gh.is_exploited(tags, url) is want


def test_payload_rows_carry_exploited_and_no_story_is_in_both_lists(sandbox):
    hot = make_entry(title="Hot one", source_url="https://e.com/hot", tags=["kev"])
    data = payload_of(sandbox, entries=[hot])
    row = next(f for f in data["findings"] if f["title"] == "Hot one")
    assert row["exploited"] is True
    assert not set(data["biggest_stories"]) & set(data["top_stories"])
