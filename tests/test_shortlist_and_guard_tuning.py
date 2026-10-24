"""Two tunings from the 2026-10-23 catch-up (#104):

1. The story shortlist also offers a story newsworthy.py's same-story rule
   matches (a shared CVE/GHSA id; a shared rare name within days), so a news
   headline links to a story whose lead title shares few tokens with it. The
   replay of #104's stories: 26 new offers (Cairn on Dark Reading, the OpenCode
   MCP flaw on The Hacker News, BeyondTrust on Dark Reading, the PHP2Shell
   copies, the PAN-OS ransomware story), one lost to the top-5 cut.
2. rewrite_guard accepts an acronym replaced by its expansion (the rewriter is
   told to expand acronyms). On a Haiku rewrite of #104's 30 briefs this
   released 4 of 32 reverts (IOCs, CT, VCO x2) and nothing else; the polarity
   words on/up/all/any released one revert, which was a real fact loss, so
   they stay."""

from __future__ import annotations

import newsworthy as nw
import pytest
import rewrite_guard as rg
import story_ledger as sl
from test_rewrite_guard import FLIPS


# --- the shortlist's same-story signal ----------------------------------------------
def entry(eid, title, url, summary="", day="2026-07-13"):
    return {"id": eid, "title": title, "source_url": url, "published": day, "summary": summary}


def ledger_with(*entries):
    led = sl.empty_ledger()
    for e in entries:
        sl.assign_entry(led, e, window_days=90)
    return led, {e["id"]: e for e in entries}


def cand(cid, title, url, day="2026-07-15", excerpt=""):
    return {"id": cid, "title": title, "source_url": url, "published": day, "excerpt": excerpt}


def offered(led, by_id, c, reference=()):
    return [r["story_id"] for r in sl.shortlist_many([c], led, by_id, window_days=90, k=5)[c["id"]]]


LEAD = entry(
    "x402",
    "V12 audit of the x402 agent-payments protocol: 25 flaws, three critical",
    "https://v12.example/blog/x402",
    "V12 reviewed the X402 codebase, which lets AI agents pay for resources.",
)


def test_a_shared_rare_name_offers_the_story_token_overlap_misses(sandbox, monkeypatch):
    led, by_id = ledger_with(LEAD)
    copy = cand("thn", "Critical X402 SDK Flaw Could Let Malicious APIs Drain Token Balances",
                "https://thn.example/x402")  # fmt: skip
    monkeypatch.setattr(sl, "same_story_hit", lambda *a: False)
    assert offered(led, by_id, copy) == []  # the old shortlist: nothing to judge
    monkeypatch.undo()
    assert offered(led, by_id, copy) == list(led["stories"])


def test_a_shared_cve_offers_the_story(sandbox):
    lead = entry("u42", "Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass MFA",
                 "https://unit42.example/p")  # fmt: skip
    led, by_id = ledger_with(lead)
    copy = cand("q", "Qilin hits firewalls through CVE-2026-0257", "https://wire.example/q")
    assert offered(led, by_id, copy) == list(led["stories"])


def test_different_cves_are_never_offered_by_the_same_story_rule(sandbox):
    lead = entry("a", "Gizmo CVE-2026-1111 heap overflow", "https://a.example/a")
    led, by_id = ledger_with(lead)
    copy = cand("b", "Gizmo CVE-2026-2222 auth bypass", "https://b.example/b")
    profile_model, profs = sl.same_story_profiles(led, by_id, [copy])
    hit = sl.same_story_hit(nw.profile(copy, profile_model), nw.publisher(copy),
                            next(iter(profs.values())))  # fmt: skip
    assert hit is False


def test_one_publishers_own_brand_name_is_no_story_match(sandbox):
    """Wiz's blog says "Wiz" in every title: same-publisher docs need a shared id."""
    lead = entry("w1", "Wiz CIRT: AI-driven cloud intrusions at machine tempo",
                 "https://www.wiz.io/blog/ai-cloud", "Responders at Wiz traced it.")  # fmt: skip
    led, by_id = ledger_with(lead)
    copy = cand("w2", "Wiz Agents Arrive in Wiz for Gov", "https://www.wiz.io/blog/gov",
                excerpt="Agencies get Wiz agents.")  # fmt: skip
    model, profs = sl.same_story_profiles(led, by_id, [copy])
    docs = next(iter(profs.values()))
    assert sl.same_story_hit(nw.profile(copy, model), nw.publisher(copy), docs) is False
    other = cand("o", "Wiz Agents Arrive in Wiz for Gov", "https://news.example/wiz",
                 excerpt="Agencies get Wiz agents.")  # fmt: skip
    assert sl.same_story_hit(nw.profile(other, model), nw.publisher(other), docs) is True


def test_the_shortlist_window_is_wider_than_the_lanes():
    """A single shared title name, 3 days apart: the lane's strict rule says
    no (corroboration costs a slot), the shortlist's says yes (a judge reads it)."""
    docs = [
        {"title": "OpenCode flaw lets MCP servers run code", "published": "2026-10-22"},
        {"title": "Pillar: OpenCode RCE during sign-in", "published": "2026-10-19"},
    ]
    model = nw.name_model([], docs)
    a, b = (nw.profile(d, model) for d in docs)
    assert not nw.same_story(a, b)
    assert nw.same_story(a, b, title_days=nw.MATCH_DAYS)


# --- rewrite_guard: an acronym spelled out is not a name change --------------------
@pytest.mark.parametrize(
    "draft, final",
    [
        ("Add detections for the published IOCs.",
         "Add detections for the published indicators of compromise."),
        ("Keep CT monitoring on your domains.",
         "Keep Certificate Transparency monitoring on your domains."),
        ("Patch VCO on-prem and restrict its web interface.",
         "Patch VeloCloud Orchestrator on-prem and restrict its web interface."),
    ],
)  # fmt: skip
def test_an_acronym_replaced_by_its_expansion_passes(draft, final):
    assert rg.changes(draft, final) == []


@pytest.mark.parametrize(
    "draft, final",
    [
        # half an expansion loses a fact: IAM is identity AND ACCESS management
        ("It is a billing and IAM problem.", "It is a billing and identity-management problem."),
        ("It bypassed in-guest EDR.", "It bypassed in-guest endpoint detection."),
        # the draft's own words never "expand" an acronym
        ("Inventory certificates that chain to the root; keep CT logs.",
         "Inventory certificates that chain to the root; keep logs."),
        # a vendor swap is still a swap
        ("The bug ships in AWS.", "The bug ships in Google Cloud."),
    ],
)  # fmt: skip
def test_anything_short_of_a_full_expansion_is_still_reverted(draft, final):
    assert any("names changed" in w for w in rg.changes(draft, final))


def test_every_fact_flip_is_still_caught():
    for kind, draft, final in FLIPS:
        assert rg.changes(draft, final), kind


@pytest.mark.parametrize("word", ["on", "up", "all", "any"])
def test_the_polarity_words_stay_guarded(word):
    """#104 evidence: dropping them released one revert, 'all users told to roll
    secrets' -> nothing, a real fact loss."""
    assert word in rg.GUARD_WORDS
    draft = "Railway told all users to roll secrets."
    assert rg.changes(draft, "Railway told users to roll secrets.")
