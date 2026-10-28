"""ISC-33 link check: every README link resolves.

- a relative link names a file that exists (fragment ignored);
- a site link (https://rcha0s.github.io/AwesomeSecurity-AIResearch/...) targets
  a view the site renders (#hash), only route params the site reads, and ids
  that exist: ?finding= a payload row, ?claim= a claim, ?domain= a taxonomy ID,
  ?topic= a topic.

The views and params are read from the template itself, so a renamed view or
dropped route fails here rather than as a dead link on GitHub.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import common
import generate_html as gh
import generate_site as gs
import pytest
from conftest import make_entry
from test_claims import ledger_of, make_claim

import claims

REPO = Path(__file__).resolve().parents[1]
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
HREF = re.compile(r'href="([^"]+)"')
TEMPLATE = gh.TEMPLATE.read_text(encoding="utf-8")


def links(md: str) -> list[str]:
    return MD_LINK.findall(md) + HREF.findall(md)


def site_views() -> set[str]:
    def keys(var: str) -> set[str]:
        body = re.search(r"var " + var + r" = \{(.*?)\};", TEMPLATE, re.S).group(1)
        return set(re.findall(r"(\w+):", body))

    return keys("VIEWS") | keys("VIEW_ALIASES")


def site_params() -> set[str]:
    body = re.search(r"var ROUTE_PARAMS = \[(.*?)\];", TEMPLATE).group(1)
    params = set(re.findall(r'"(\w+)"', body))
    if "p.get('finding')" in TEMPLATE:
        params.add("finding")
    return params


def payload_of_page(page: str) -> dict:
    block = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', page, re.S)
    return json.loads(block.group(1).replace("<\\/", "</"))


def site_problems(url: str, payload: dict) -> list[str]:
    parts = urlsplit(url)
    out = []
    if parts.fragment and parts.fragment not in site_views():  # no hash = Briefing
        out.append(f"{url}: #{parts.fragment} is not a site view")
    known = {
        "finding": {r["id"] for r in payload["findings"] + payload["editorial"]},
        "claim": {c["id"] for c in payload["claims"]},
        "topic": set(payload["topics"]),
        "domain": {d["id"] for t in payload["topics"].values() for d in t["domain_ids"]},
    }
    for key, values in parse_qs(parts.query).items():
        if key not in site_params():
            out.append(f"{url}: the site does not read ?{key}=")
        elif any(v not in known.get(key, set()) for v in values):
            out.append(f"{url}: ?{key}={values} names nothing on the site")
    return out


def link_problems(md: str, roots: list[Path], payload: dict) -> list[str]:
    """Problems with every link in a root-level markdown file; a relative link
    may resolve under any of `roots` (generated files vs committed static ones)."""
    out = []
    for target in links(md):
        if target.startswith(gh.SITE_URL):
            out += site_problems(target, payload)
        elif target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        elif not any((root / target.split("#")[0]).exists() for root in roots):
            out.append(f"{target}: no such file")
    return out


# --- The committed README and topic trees ------------------------------------
def test_committed_readme_links_all_resolve():
    payload = payload_of_page((REPO / "docs" / "index.html").read_text(encoding="utf-8"))
    md = (REPO / "README.md").read_text(encoding="utf-8")
    assert links(md), "README has no links"
    assert link_problems(md, [REPO], payload) == []


def test_committed_readme_is_short_and_has_every_big_link():
    md = (REPO / "README.md").read_text(encoding="utf-8")
    assert len(md.splitlines()) < 80
    for label, view in gs.SITE_VIEWS:
        assert f"[{label}]({gh.SITE_URL}#{view})" in md
    assert "Last updated " in md and "## Contribute" in md


@pytest.mark.parametrize(
    "page",
    ["ai-security/README.md", "product-security/README.md", "ai-research/README.md"],
)
def test_topic_tree_pages_keep_working(page):
    path = REPO / page
    problems = []
    for target in links(path.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (path.parent / target.split("#")[0]).resolve().exists():
            problems.append(target)
    assert problems == []


# --- A generated README in the sandbox ---------------------------------------
def test_generated_readme_deep_links_resolve(sandbox):
    claims.save_ledger(
        ledger_of(
            make_claim(id="a-claim", last_reviewed="2026-07-10"),
            make_claim(id="b-claim", statement="Other.", guidance="Do b."),
        )
    )
    pool = common.load_pool("ai-research")
    pool["entries"] += [
        make_entry(title="Story one", source_url="https://e.com/1", published="2026-07-14"),
        make_entry(title="Story two [x]", source_url="https://e.com/2", published="2026-07-12"),
    ]
    common.save_pool("ai-research", pool)
    gs.main()
    payload = gh.build_payload(claims.load_ledger(), common.load_config(), "2026-07-15")
    md = (sandbox / "README.md").read_text(encoding="utf-8")
    assert "?finding=" in md and "?claim=a-claim#claims" in md
    assert "Story two \\[x\\]" in md  # markdown-escaped label
    assert link_problems(md, [sandbox, REPO], payload) == []
    assert len(md.splitlines()) < 80


def test_link_check_catches_dead_targets(sandbox):
    payload = gh.build_payload(ledger_of(make_claim()), common.load_config(), "2026-07-15")
    md = (
        f"[a]({gh.SITE_URL}#nowhere) [b]({gh.SITE_URL}?claim=missing#claims) "
        f"[c]({gh.SITE_URL}?bogus=1#week) [d](no-such-file.md) "
        f"[e]({gh.SITE_URL}?domain=ais.prompt-injection#topics)"
    )
    problems = link_problems(md, [sandbox], payload)
    assert len(problems) == 4 and not any("ais.prompt-injection" in p for p in problems)


# --- The window sentence above the top stories (review of #77) ----------------
def _readme_with(sandbox, published: list[str]) -> str:
    claims.save_ledger(ledger_of(make_claim()))
    pool = common.load_pool("ai-research")
    pool["entries"] += [
        make_entry(title=f"Story {i}", source_url=f"https://e.com/{i}", published=day)
        for i, day in enumerate(published)
    ]
    common.save_pool("ai-research", pool)
    gs.main()
    return (sandbox / "README.md").read_text(encoding="utf-8")


def test_one_fresh_story_says_fewer_than_five_not_nothing_new(sandbox):
    md = _readme_with(sandbox, ["2026-07-14", "2026-06-20", "2026-06-10"])  # clock: 07-15
    assert "Fewer than five stories in the last 7 days" in md
    assert "Nothing new" not in md


def test_no_fresh_story_says_nothing_new_with_the_real_window(sandbox):
    md = _readme_with(sandbox, ["2026-06-20", "2026-06-10"])
    assert "Nothing new in the last 7 days, so these are the latest top stories." in md
    assert "last week" not in md


def test_site_and_readme_print_the_same_window_sentence():
    import briefing
    from test_site_views import run_js

    cases = [(0, 0), (0, 5), (1, 5), (4, 5), (5, 5), (8, 8)]
    js = ",".join(f"windowNote({f}, {t}, 7)" for f, t in cases)
    got = run_js({}, "[" + js + "]")
    assert got == [briefing.window_note(f, t, 7) for f, t in cases]
