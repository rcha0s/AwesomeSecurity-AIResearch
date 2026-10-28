"""GitHub advisories are kept only when AI-related, critical in a well-known
library, or a story (Rohan, 2026-10-28), and the "Pending review" label is gone.

`select_batch.ghsa_keep_reason` is the one pure decision; select_batch uses it
for the must-not-miss lane, the deal and the news tier. `prune_ghsa.py` applies
the same rule to advisories already in the pools."""

from __future__ import annotations

from pathlib import Path

import common
import generate_site
import prune_ghsa
import pytest
import select_batch
from conftest import make_entry
from test_prefilter import _cand
from test_select_batch import conf, table  # noqa: F401  (fixture)
from test_select_batch_stories import STORY, copy, flood, run

CONF = common.load_config()
GHSA = {"source_id": None, "discovered_via": "github", "source_type": "GHSA"}
AI_HINT = {"prefilter": {"domain_hint": "ais.mcp-tools"}}


def pkg(name: str, eco: str = "pip") -> list[dict]:
    return [{"ecosystem": eco, "name": name}]


def adv(i: int, severity: str = "HIGH", packages=None, **over) -> dict:
    url = f"https://github.com/advisories/GHSA-{i}"
    base = {
        "id": f"adv{i}",
        "title": f"Advisory {i} in somepkg",
        "source_url": url,
        "article_url": url,
        "source_rank": 70.0,
        "published": "2026-07-14",
        "severity": severity,
        "packages": packages or [],
        **GHSA,
    }
    return _cand(**{**base, **over})


@pytest.mark.parametrize(
    ("cand", "reason"),
    [
        (adv(1, "MODERATE", **AI_HINT), "ai-domain"),  # AI domain, any severity
        (adv(2, "LOW", pkg("LiteLLM")), "ai-package"),  # AI package, any severity
        (adv(3, "HIGH", pkg("vllm")), "ai-package"),
        (adv(4, "CRITICAL", pkg("Django")), "critical"),  # critical + well-known
        (adv(5, "critical", pkg("pillow", "PIP")), "critical"),  # case-insensitive
        (adv(6, "CRITICAL", pkg("golang.org/x/crypto", "go")), "critical"),
        (adv(7, "CRITICAL", pkg("obscure-widget")), None),  # critical, unknown package
        (adv(8, "HIGH", pkg("django")), None),  # high + well-known: dropped
        (adv(9, "CRITICAL"), None),  # no package named
        (adv(10, "HIGH", guess_topic="ai-security", guess_domain="ais.mcp-tools"), None),  # a guess
    ],
)
def test_the_keep_rule(cand, reason):
    assert select_batch.ghsa_keep_reason(cand, CONF) == reason


def test_the_rule_is_about_ghsa_only():
    rss = _cand(id="x", severity="CRITICAL", packages=pkg("django"), source_id="rss:x")
    assert select_batch.ghsa_keep_reason(rss, CONF) is None
    assert select_batch.priority_class(rss, CONF) is None


def test_package_lists_are_data_in_config():
    assert {"litellm", "django", "pillow"} <= {x.lower() for x in CONF.ghsa["well_known_packages"]}
    custom = common.Config(**{**CONF.__dict__, "ghsa": {"well_known_packages": ["Foo"]}})
    assert select_batch.ghsa_keep_reason(adv(1, "CRITICAL", pkg("foo")), custom) == "critical"
    assert select_batch.ghsa_keep_reason(adv(2, "CRITICAL", pkg("django")), custom) is None


def test_the_ingestor_records_the_affected_packages():
    import ingest_ghsa

    raw = {
        "ghsa_id": "GHSA-aaaa-bbbb-cccc",
        "summary": "Something",
        "severity": "critical",
        "html_url": "https://github.com/advisories/GHSA-aaaa-bbbb-cccc",
        "vulnerabilities": [
            {"package": {"ecosystem": "pip", "name": "litellm"}},
            {"package": {"ecosystem": "pip", "name": "litellm"}},
            {"package": {"ecosystem": "npm", "name": "left-pad"}},
        ],
    }
    rules = common.load_yaml(common.SOURCES_FILE)["classification"]
    cand = ingest_ghsa.advisory_to_candidate(raw, rules)
    assert cand["packages"] == [
        {"ecosystem": "pip", "name": "litellm"},
        {"ecosystem": "npm", "name": "left-pad"},
    ]


LANE = {"batch_priority_max": 4, "batch_priority_per_source": 3, "max_news_per_run": 20}


def staged_mix() -> list[dict]:
    return [
        adv(1, "CRITICAL", pkg("django")),
        adv(2, "CRITICAL", pkg("obscure-widget")),
        adv(3, "HIGH", pkg("django")),
        adv(4, "MODERATE", pkg("litellm")),
        *flood(6),
    ]


def test_unkept_advisories_take_no_batch_lane_or_news_slot(sandbox, table):  # noqa: F811
    staged = staged_mix()
    session, backlog = select_batch.select(staged, conf(8, 4, **LANE), table)
    got = {c["id"] for c in session}
    assert {"adv1", "adv4"} <= got  # critical + well-known, and an AI package
    assert not got & {"adv2", "adv3"}  # not even in the news tier
    held = {c["id"]: c["prefilter"]["reason"] for c in backlog if c["id"].startswith("adv")}
    assert held == {"adv2": "ghsa:not-kept", "adv3": "ghsa:not-kept"}
    assert sorted(c["id"] for c in session + backlog) == sorted(c["id"] for c in staged)
    lane = {c["id"]: c["batch_priority"] for c in session if c.get("batch_priority")}
    assert lane["adv1"] == "ghsa-critical" and lane["adv4"] == "ghsa-ai"


def test_the_news_tier_takes_only_kept_advisories(sandbox, table):  # noqa: F811
    staged = [adv(i, "CRITICAL", pkg("django")) for i in range(1, 4)]
    staged += [adv(i, "CRITICAL", pkg("obscure-widget")) for i in range(4, 8)]
    batch, news, _ = select_batch.select_tiers(
        staged, conf(1, 0, batch_news_per_source=9, **LANE), table, reference=[], known=[]
    )
    assert all(x["batch_news"]["reason"] == "ghsa-critical" for x in news)
    assert {x["id"] for x in batch + news} == {"adv1", "adv2", "adv3"}


def test_an_unkept_advisory_that_became_a_story_still_gets_in(sandbox):
    """Path (c): a big-story group (2+ independent publishers) is the story lane's
    call, so a GHSA copy that heads it is admitted whatever the keep rule says."""
    head = adv(
        1, "HIGH", title="Two critical RCEs in PHP core", source_rank=90.0, published="2026-07-14"
    )
    assert select_batch.ghsa_keep_reason(head, CONF) is None
    copies = [
        copy(1, "Two critical RCEs in PHP core", "talos", rank=60.0),
        copy(2, "Hackers exploited the PHP vulnerabilities before the patch", "wired"),
    ]
    batch, _ = run([head, *copies, *flood()], batch_story_min_rank=55, **STORY)
    story = next(r for r in batch if r.get("batch_priority") == "story")
    assert story["id"] == "adv1"
    alone, _ = run([adv(2, "HIGH"), *flood()], **STORY)
    assert "adv2" not in {r["id"] for r in alone}


# --- advisories already in the pools --------------------------------------------
def ghsa_entry(topic="product-security", domain="ps.appsec", **over) -> dict:
    n = len(over.get("id", "")) + len(over.get("title", ""))
    base = {
        "topic": topic,
        "domain": domain,
        "title": f"Advisory {n}",
        "source_name": "GitHub Advisory Database",
        "source_url": f"https://github.com/advisories/GHSA-test-{n}",
    }
    return make_entry(**{**base, **over})


def keep(entry: dict, cited=frozenset()) -> str | None:
    return prune_ghsa.keep_reason(entry, CONF, set(cited))


def test_existing_entries_follow_the_same_rule():
    assert prune_ghsa.is_ghsa_entry(ghsa_entry(source_name=None))  # by advisory URL
    assert not prune_ghsa.is_ghsa_entry(make_entry(source_url="https://blog.example/x"))
    assert keep(ghsa_entry(topic="ai-security", domain="ais.mcp-tools")) == "ai-security"
    critical = ghsa_entry(title="Critical Pillow flaw lets one file run code")
    assert keep(critical).startswith("critical in well-known package pillow")
    assert keep(ghsa_entry(title="Pillow heap overflow")) is None  # not critical
    assert keep(ghsa_entry(title="Critical Laravel auth bypass")) is None  # unknown package
    promoted = ghsa_entry(title="Plain", editorial={"promoted": True})
    assert keep(promoted) == "editorially promoted"
    own = ghsa_entry(title="Plain", id="own")
    assert keep(own, {common.normalize_url(own["source_url"])}) == "evidence for a claim"


def test_two_independent_publishers_keep_an_entry():
    base = ghsa_entry(title="Plain advisory")
    one = {**base, "corroborating_sources": [{"url": "https://a.example/x"}]}
    assert keep(one) is None
    gh_hn = {
        **one,
        "story_corroboration": [
            {"url": "https://github.com/o/r"},
            {"url": "https://news.ycombinator.com/item?id=1"},
        ],
    }
    assert keep(gh_hn) is None  # GitHub and HN are not independent
    two = {**one, "story_corroboration": [{"url": "https://www.b.example/y"}]}
    assert keep(two) == "covered by 2+ independent publishers"
    same_host = {**one, "story_corroboration": [{"url": "https://a.example/z"}]}
    assert keep(same_host) is None  # one publisher twice


def test_prune_moves_the_rest_to_the_archive_and_deletes_nothing(sandbox, monkeypatch, capsys):
    keepers = ghsa_entry(title="Critical Django bypass", id="keep-django")
    mover = ghsa_entry(title="Contao XSS", id="move-contao")
    other = make_entry(id="not-ghsa", source_url="https://blog.example/x")
    pool = common.load_pool("product-security")
    pool["entries"] = [keepers, mover, other]
    common.save_pool("product-security", pool)
    monkeypatch.setattr(prune_ghsa.c, "load_config", lambda: CONF)
    assert prune_ghsa.main([]) == 0
    left = [e["id"] for e in common.load_pool("product-security")["entries"]]
    assert left == ["keep-django", "not-ghsa"]
    archived = common.load_json(common.ARCHIVE_FILE)
    assert [e["id"] for e in archived] == ["move-contao"]
    assert archived[0]["archived_reason"] == "ghsa-not-kept"
    assert "MOVE\tmove-contao" in capsys.readouterr().out
    assert prune_ghsa.main([]) == 0  # a second run is a no-op
    assert len(common.load_json(common.ARCHIVE_FILE)) == 1


# --- the "Pending review" label is gone -------------------------------------------
BANNED = ("pending review", "not yet human-verified", "auto-analyzed")


def test_no_pending_review_text_in_any_rendered_output(sandbox):
    held = make_entry(
        topic="ai-security",
        domain="ais.mcp-tools",
        title="A held finding",
        source_url="https://a.example/held",
        needs_review=True,
    )
    pool = common.load_pool("ai-security")
    pool["entries"] = [held]
    common.save_pool("ai-security", pool)
    conf_ = common.load_config()
    page = generate_site.render_entry_page(held, conf_)
    block = generate_site.render_index_block(held, conf_)
    assert "A held finding" in page and "A held finding" in block
    generate_site.main()
    for path in sandbox.rglob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        assert not any(b in text for b in BANNED), path
    for text in (page, block):
        assert not any(b in text.lower() for b in BANNED)
    assert "_review_" not in block
    scripts = Path(__file__).parent.parent / "scripts"
    for src in [*scripts.glob("generate_*.py"), scripts / "templates" / "site.html"]:
        assert not any(b in src.read_text(encoding="utf-8").lower() for b in BANNED), src


def test_rerank_does_not_restore_an_advisory_prune_ghsa_archived(sandbox):
    """Rerank pulls archived news back into the pool; a stamped advisory stays."""
    import rerank

    promoted = {"promoted": True, "reason": "x", "signals": [], "at": "2026-10-20T00:00:00+00:00"}
    stamped = ghsa_entry(id="stamped", editorial=promoted, archived_reason="ghsa-not-kept")
    plain = ghsa_entry(id="plain", title="Other", editorial=promoted)
    common.save_json(common.ARCHIVE_FILE, [stamped, plain])
    pool = rerank.rerank_pool("product-security", CONF)
    assert [e["id"] for e in pool["entries"]] == ["plain"]
    assert [e["id"] for e in common.load_json(common.ARCHIVE_FILE)] == ["stamped"]
