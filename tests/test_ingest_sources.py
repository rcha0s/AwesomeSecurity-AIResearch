"""Tests for the HN + GHSA ingestor pure mapping functions (offline, no network)."""

from __future__ import annotations

import common as c
import ingest_ghsa as gh
import ingest_hn as hn
import pytest

RULES = c.load_yaml(c.SOURCES_FILE)["classification"]


def test_hn_hit_classifies_on_topic():
    hit = {
        "objectID": "42",
        "title": "New prompt injection technique bypasses LLM guardrails",
        "url": "https://blog.example.com/pi",
        "author": "researcher",
        "points": 120,
        "num_comments": 30,
        "created_at": "2026-07-14T10:00:00.000Z",
    }
    cand = hn.hit_to_candidate(hit, RULES)
    assert cand["guess_topic"] == "ai-security"
    assert cand["article_url"] == "https://blog.example.com/pi"
    assert cand["source_rank"] == hn.HN_SOURCE_RANK
    assert cand["published"] == "2026-07-14" and cand["date"] == "2026-07"


def test_hn_off_topic_dropped():
    hit = {
        "objectID": "7",
        "title": "My weekend woodworking project",
        "url": "https://blog.example.com/wood",
        "points": 200,
    }
    assert hn.hit_to_candidate(hit, RULES) is None


def test_hn_self_post_falls_back_to_discussion_url():
    hit = {
        "objectID": "99",
        "title": "Ask HN: securing an MCP server against tool poisoning",
        "url": None,  # self/Ask-HN post: no external link
        "points": 80,
        "story_text": "how do you sandbox mcp tools",
    }
    cand = hn.hit_to_candidate(hit, RULES)
    assert cand is not None
    assert cand["article_url"] == "https://news.ycombinator.com/item?id=99"


def test_ghsa_supply_chain_default_routing():
    adv = {
        "ghsa_id": "GHSA-xxxx-yyyy-zzzz",
        "summary": "Arbitrary code execution in leftpad",
        "description": "A malicious version was published.",
        "severity": "high",
        "html_url": "https://github.com/advisories/GHSA-xxxx-yyyy-zzzz",
        "published_at": "2026-07-13T00:00:00Z",
        "vulnerabilities": [{"package": {"ecosystem": "npm", "name": "leftpad"}}],
    }
    cand = gh.advisory_to_candidate(adv, RULES)
    assert cand["guess_topic"] == "product-security"
    assert "GHSA-xxxx-yyyy-zzzz" in cand["title"]
    assert cand["severity"] == "HIGH"
    assert "npm/leftpad" in cand["excerpt"]


def test_ghsa_ai_package_routes_to_ai_security():
    adv = {
        "ghsa_id": "GHSA-aaaa-bbbb-cccc",
        "summary": "Prompt injection in an LLM agent framework",
        "description": "Untrusted tool output reaches the model.",
        "severity": "critical",
        "html_url": "https://github.com/advisories/GHSA-aaaa-bbbb-cccc",
        "published_at": "2026-07-12T00:00:00Z",
        "vulnerabilities": [{"package": {"ecosystem": "pip", "name": "some-agent-lib"}}],
    }
    cand = gh.advisory_to_candidate(adv, RULES)
    assert cand["guess_label"] == "AI Security"
    assert cand["guess_domain"].startswith("ais.")
    assert cand["guess_topic"] == "ai-security"


def test_ghsa_affected_packages_dedup():
    adv = {
        "vulnerabilities": [
            {"package": {"ecosystem": "npm", "name": "a"}},
            {"package": {"ecosystem": "npm", "name": "a"}},  # dup
            {"package": {"ecosystem": "pip", "name": "b"}},
        ]
    }
    assert gh._affected_packages(adv) == "npm/a, pip/b"


def test_ghsa_missing_id_or_url_returns_none():
    assert gh.advisory_to_candidate({"ghsa_id": "", "html_url": "https://x/y"}, RULES) is None
    assert gh.advisory_to_candidate({"ghsa_id": "GHSA-1", "html_url": ""}, RULES) is None


def _adv(ghsa_id: str, summary: str, severity: str = "high") -> dict:
    return {
        "ghsa_id": ghsa_id,
        "summary": summary,
        "severity": severity,
        "html_url": f"https://github.com/advisories/{ghsa_id}",
        "published_at": "2026-07-14T00:00:00Z",
        "vulnerabilities": [{"package": {"ecosystem": "pip", "name": "pkg"}}],
    }


def test_ghsa_always_pulls_the_newest_critical_advisories(monkeypatch):
    """2026-10-21: the newest 20 reviewed advisories were all Pillow, so the
    week's critical ones (Claude Agent SDK, LMCache) were never staged."""
    calls = []
    flood = [_adv(f"GHSA-p{i}", f"Pillow bug {i}") for i in range(3)]
    critical = [_adv("GHSA-crit", "Agent SDK argument injection", "critical"), flood[0]]

    def fake_fetch(limit, severity=None):
        calls.append((limit, severity))
        return critical if severity == "critical" else flood

    monkeypatch.setattr(gh, "fetch_advisories", fake_fetch)
    out = gh.collect({"ghsa": {"per_run": 3, "per_run_critical": 30}}, RULES, None)
    assert calls == [(3, None), (30, "critical")]
    assert any("GHSA-crit" in x["title"] for x in out)
    assert len(out) == 4  # the advisory both passes return is staged once
    calls.clear()
    assert len(gh.collect({"ghsa": {"per_run": 3}}, RULES, None)) == 3  # off unless configured
    assert calls == [(3, None)]


def test_ghsa_fetch_asks_for_the_severity(monkeypatch):
    seen = []
    monkeypatch.setattr(gh, "run_gh", lambda args, timeout: seen.append(args[1]) or "[]")
    gh.fetch_advisories(30, severity="critical")
    gh.fetch_advisories(20)
    assert seen[0].endswith("per_page=30&severity=critical")
    assert "severity" not in seen[1]


@pytest.mark.parametrize(
    "text, ai",
    [
        ("xxe in the xml parser", False),
        ("unsafe yaml load", False),
        ("spoofed user-agent header", False),
        ("data model validation bypass", False),
        ("html sanitizer bypass", False),
        ("llmnr poisoning in netkit", False),
        ("claudette template injection", False),
        ("claude agent sdk argument injection", True),
        ("rce in the llm gateway", True),
        ("mcp server path traversal", True),
        ("unsafe pickle in ml pipeline", True),
        ("prompt injection via tool output", True),
    ],
)
def test_ghsa_ai_keywords_match_whole_words_only(text, ai):
    assert bool(gh.AI_PATTERN.search(text)) is ai


def test_ghsa_critical_pass_is_configured():
    assert int(c.load_yaml(c.SOURCES_FILE)["ghsa"]["per_run_critical"]) >= 20


# --- 2026-10-23 router catch-alls ---------------------------------------------
# Real titles every registered feed dropped before staging: no keyword fired.
@pytest.mark.parametrize(
    "title,label",
    [
        (
            "PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet",
            "ps.appsec",
        ),
        (
            "Max-severity GitLab bug allows remote code execution over 12 years of releases",
            "ps.appsec",
        ),
        ("Node2Shell: From Brotli Data to Remote Code Execution", "ps.appsec"),
        ("Linux KVM guest-host escape rated critical", "ps.appsec"),
        ("Arista patches new VeloCloud Orchestrator zero-day exploited in attacks", "ps.appsec"),
        ("OpenAI models hacked a crypto wallet and breached more websites", "ps.appsec"),
        (
            "Loud, Fast, and Everywhere: Anatomy of a Real AI-Driven Cloud Attack",
            "ais.agent-security",
        ),
        ("Fake Claude, ChatGPT Attacks Surge, Putting Developers at Risk", "ais.agent-security"),
    ],
)
def test_the_catch_alls_stage_the_weeks_missed_stories(title, label):
    import aggregate

    assert aggregate.classify_domain(title, RULES, []) == label


@pytest.mark.parametrize(
    "title,label",
    [
        (
            "New prompt injection technique bypasses LLM guardrails",
            "AI Security",
        ),  # earlier class wins
        ("npm worm hits 400 packages: a supply chain compromise", "Web Application Security"),
        ("Mirai botnet operators join the attacks", None),  # "mirai bot" is not " ai bot"
        ("Our quarterly earnings and the new sales force", None),  # "rce" inside a word
        ("My weekend woodworking project", None),
    ],
)
def test_the_catch_alls_leave_earlier_classes_and_noise_alone(title, label):
    import aggregate

    assert aggregate.classify_domain(title, RULES, []) == label


@pytest.mark.parametrize(
    "title",
    [
        "Uber brings ChatGPT Work to its whole company",
        "ChatGPT Ads expands to more countries",
        "Copilot gets a new sidebar",
        "Claude now writes your spreadsheets",
    ],
)
def test_a_bare_ai_brand_needs_incident_context(title):
    import aggregate

    assert aggregate.classify_domain(title, RULES, []) is None


def test_the_catch_all_context_terms_are_configured():
    assert RULES["catch_alls"]["ais.agent-security"]["context"]
    assert RULES["catch_alls"]["ps.appsec"]["context"] == []
