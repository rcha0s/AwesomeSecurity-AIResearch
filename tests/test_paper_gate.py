"""Tests for the paper admission gate (ISC-29) and its wiring into aggregate."""

from __future__ import annotations

from datetime import timedelta

import aggregate
import common as c
import ingest_conferences as ic
import ingest_json_feeds as ijf
import paper_gate as pg
import pytest

NO_HF = pg.Signals(hf_ids=set())
PAPER = "https://arxiv.org/abs/2607.00001"


def paper(url=PAPER, **extra):
    return {"title": "Prompt injection attack", "article_url": url, **extra}


# --- the gate itself --------------------------------------------------------


def test_bare_preprint_is_refused():
    assert pg.admit(paper(), NO_HF) == (False, "no-quality-signal")


def test_venue_accepted_paper_is_admitted():
    assert pg.admit(paper(venue="USENIX Security"), NO_HF) == (True, "venue")


def test_hf_daily_listed_paper_is_admitted():
    sig = pg.Signals(hf_ids={"2607.00001"})
    assert pg.admit(paper(), sig) == (True, "hf-daily")


def test_curator_linked_paper_is_admitted():
    sig = pg.Signals(hf_ids=set(), curator_ids={"2607.00001"})
    assert pg.admit(paper(), sig) == (True, "curator-link")


def test_version_suffix_and_url_forms_match_the_signal():
    sig = pg.Signals(hf_ids={"2607.00001"})
    for url in (
        "http://arxiv.org/abs/2607.00001v2",
        "https://arxiv.org/pdf/2607.00001v1",
        "https://arxiv.org/html/2607.00001",
    ):
        assert pg.admit(paper(url), sig)[0] is True, url


def test_other_papers_signal_does_not_admit():
    sig = pg.Signals(hf_ids={"2607.99999"}, curator_ids={"2607.88888"})
    assert pg.admit(paper(), sig)[0] is False


def test_non_papers_pass_through_ungated():
    assert pg.admit({"article_url": "https://blog.example.com/post"}, NO_HF) == (
        True,
        "not-a-preprint",
    )


def test_look_alike_host_is_not_a_preprint():
    assert pg.is_preprint("https://notarxiv.org/abs/2607.00001") is False
    assert pg.is_preprint("https://arxiv.org.evil.com/abs/2607.00001") is False


def test_hf_failure_fails_closed(monkeypatch):
    import requests

    def boom(*a, **k):
        raise requests.ConnectionError("down")

    monkeypatch.setattr(requests, "get", boom)
    assert pg.fetch_hf_daily_ids() == set()
    assert pg.admit(paper(), pg.Signals())[0] is False


def test_curator_ids_read_links_summary_and_content():
    entries = [
        {"link": "https://arxiv.org/abs/2601.00001", "summary": ""},
        {"link": "https://x.com/p", "summary": 'see <a href="https://arxiv.org/pdf/2601.00002v3">'},
        {"link": "", "content": [{"value": "read https://arxiv.org/abs/2601.00003"}]},
    ]
    assert pg.curator_ids_from_entries(entries) == {"2601.00001", "2601.00002", "2601.00003"}


def test_trusted_curators_are_registered_sources():
    import sources_registry as sr

    ids = {s["id"] for s in sr.load_sources()}
    assert pg.TRUSTED_CURATORS <= ids


# --- wiring: aggregate.collect_rss -----------------------------------------


def _feed_env(monkeypatch, feeds):
    """feeds: {url: (source_dict, [entries])}"""

    def fake_parse(url, request_headers=None, **kwargs):
        class _P:
            bozo = False
            entries = feeds[url][1]

        return _P()

    monkeypatch.setattr(aggregate.feedparser, "parse", fake_parse)
    monkeypatch.setattr(
        aggregate.sr,
        "sources_of_type",
        lambda kind: [s for s, _ in feeds.values()] if kind == "rss" else [],
    )


def _src(sid, url):
    return {"id": sid, "name": sid, "handle": url, "rank": 50.0, "topics": [], "domains": []}


def _entry(link, title="Prompt injection jailbreak of LLM agents"):
    return {
        "link": link,
        "title": title,
        "summary": "a jailbreak and prompt injection attack on an llm",
        "published": "2026-07-14T00:00:00Z",
    }


def test_collect_rss_drops_bare_preprints_keeps_signalled(monkeypatch):
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    _feed_env(
        monkeypatch,
        {
            "u1": (
                _src("rss:arxiv", "u1"),
                [
                    _entry("http://arxiv.org/abs/2607.11111", "Bare preprint jailbreak"),
                    _entry("http://arxiv.org/abs/2607.22222", "HF listed jailbreak"),
                    _entry("http://arxiv.org/abs/2607.33333", "Curator linked jailbreak"),
                ],
            ),
            "u2": (
                _src(next(iter(pg.TRUSTED_CURATORS)), "u2"),
                [_entry("https://blog.example.com/p", "Curator post jailbreak llm")]
                + [
                    {
                        **_entry("https://curator.example/x"),
                        "summary": "see arxiv.org/abs/2607.33333",
                    }
                ],
            ),
        },
    )
    cutoff = c.utcnow() - timedelta(days=31)
    out = aggregate.collect_rss(rules, cutoff, pg.Signals(hf_ids={"2607.22222"}))
    titles = {x["title"] for x in out}
    assert "Bare preprint jailbreak" not in titles
    assert {"HF listed jailbreak", "Curator linked jailbreak"} <= titles
    assert "Curator post jailbreak llm" in titles  # non-paper content is not gated


# --- wiring: conferences + json feeds --------------------------------------


def test_conference_candidates_carry_the_venue_signal():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    item = {
        "title": "Backdoor attacks on LLM agents",
        "summary": "prompt injection and backdoor poisoning",
        "published": "2026-07-14T00:00:00Z",
        "link": "https://arxiv.org/abs/2607.00001",
        "comment": "Accepted at IEEE S&P 2027",
    }
    cand = ic.entry_to_candidate(item, "IEEE S&P", rules)
    assert cand and pg.admit(cand, NO_HF) == (True, "venue")


def test_registered_venues_include_sp_and_ccs():
    venues = c.load_yaml(c.SOURCES_FILE)["conferences"]["venues"]
    assert "CCS" in venues and "IEEE S&P" in venues


def _hf_item(pid, title, summary, published="2026-07-14T00:00:00.000Z"):
    return {"paper": {"id": pid, "title": title, "summary": summary, "publishedAt": published}}


def test_hf_papers_stage_only_on_topic_items():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    src = {"id": "hf_papers:x", "name": "HF Daily Papers", "rank": 55.0, "topics": []}
    items = [
        _hf_item("2607.00001", "Jailbreak and prompt injection of LLM agents", "attack on llm"),
        _hf_item("2607.00002", "A diffusion model for protein folding", "biology"),
    ]
    out = ijf.hf_candidates(items, src, rules, c.utcnow() - timedelta(days=31))
    assert [x["article_url"] for x in out] == ["https://arxiv.org/abs/2607.00001"]


def test_hf_papers_need_a_security_term_when_gated():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    src = {"id": "hf_papers:x", "name": "HF Daily Papers", "rank": 55.0, "topics": []}
    items = [_hf_item("2607.00003", "A faster LLM inference engine", "llm serving throughput")]
    cutoff = c.utcnow() - timedelta(days=31)
    assert ijf.hf_candidates(items, src, rules, cutoff)  # ungated: on-topic by keywords
    assert not ijf.hf_candidates(items, src, rules, cutoff, ("jailbreak", "attack"))


def test_kev_candidates_window_and_shape():
    import datetime as dt

    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    src = {"id": "kev_json:x", "name": "CISA KEV", "rank": 75.0, "topics": [], "domains": []}
    data = {
        "vulnerabilities": [
            {
                "cveID": "CVE-2026-1",
                "vendorProject": "Acme",
                "product": "Widget",
                "vulnerabilityName": "Acme Widget Authentication Bypass",
                "dateAdded": "2026-07-10",
                "shortDescription": "auth bypass",
            },
            {"cveID": "CVE-2020-1", "vulnerabilityName": "Old", "dateAdded": "2020-01-01"},
        ]
    }
    out = ijf.kev_candidates(data, src, rules, c.utcnow() - dt.timedelta(days=31))
    assert len(out) == 1
    assert out[0]["article_url"] == "https://nvd.nist.gov/vuln/detail/CVE-2026-1"
    assert out[0]["guess_topic"] == "product-security"


@pytest.mark.parametrize("kind", ["kev_json", "hf_papers"])
def test_new_source_types_are_registered_and_allowlisted(kind):
    import allowlist
    import sources_registry as sr

    assert kind in sr.SOURCE_TYPES
    host = allowlist.source_hosts([{"type": kind, "handle": "https://api.example.org/x"}])
    assert host == {"api.example.org"}


# --- review fixes: robustness, HF outage visibility, HN gating --------------

SRC = {"id": "s", "name": "S", "rank": 1.0, "topics": [], "handle": "x://"}


def test_hf_candidates_survive_malformed_items():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    items = [
        {"no_paper": 1},
        {"paper": None},
        {"paper": {"title": "no id jailbreak"}},
        "junk",
        _hf_item("2607.00001", "Jailbreak and prompt injection of LLM agents", "attack on llm"),
    ]
    out = ijf.hf_candidates(items, SRC, rules, c.utcnow() - timedelta(days=31))
    assert [x["article_url"] for x in out] == ["https://arxiv.org/abs/2607.00001"]


def test_kev_candidates_tolerate_non_dict_payloads():
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    cutoff = c.utcnow() - timedelta(days=31)
    for bad in (None, [], "x", {"vulnerabilities": "nope"}, {"vulnerabilities": [None, 3]}):
        assert ijf.kev_candidates(bad, SRC, rules, cutoff) == []


def test_collect_stages_kev_even_when_hf_returns_dict_or_raises(monkeypatch):
    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    kev = {
        "vulnerabilities": [
            {
                "cveID": "CVE-2026-9",
                "vulnerabilityName": "Acme Authentication Bypass",
                "dateAdded": "2026-07-10",
                "shortDescription": "auth bypass",
            }
        ]
    }
    sources = {
        "kev_json": [{**SRC, "handle": "kev://"}],
        "hf_papers": [{**SRC, "handle": "hf://"}],
    }
    monkeypatch.setattr(ijf.sr, "sources_of_type", lambda k: sources.get(k, []))
    for hf_resp in ({"error": "rate limited"}, RuntimeError("boom")):

        def fake_fetch(url, hf_resp=hf_resp, **params):
            if url == "kev://":
                return kev
            if isinstance(hf_resp, Exception):
                raise hf_resp
            return hf_resp

        monkeypatch.setattr(ijf, "fetch_json", fake_fetch)
        out = ijf.collect(rules, c.utcnow() - timedelta(days=31))
        assert [x["kev"]["cveID"] for x in out] == ["CVE-2026-9"]


class _Resp:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def test_hf_total_outage_is_loud_and_counted(monkeypatch, capsys):
    import requests

    def boom(*a, **k):
        raise requests.ConnectionError("down")

    monkeypatch.setattr(requests, "get", boom)
    sig = pg.Signals()
    assert pg.admit(paper(), sig) == (False, "no-quality-signal")
    assert "HF-SIGNAL-UNAVAILABLE" in capsys.readouterr().out
    assert sig.status_line() == "papers gated: 1, HF signal: unavailable"


def test_hf_schema_change_counts_as_unavailable(monkeypatch, capsys):
    import requests

    monkeypatch.setattr(requests, "get", lambda *a, **k: _Resp({"error": "schema changed"}))
    ids, ok = pg.fetch_hf_daily()
    assert ids == set() and ok == 0
    assert "HF-SIGNAL-UNAVAILABLE" in capsys.readouterr().out


def test_hf_partial_success_is_not_unavailable(monkeypatch, capsys):
    import requests

    monkeypatch.setattr(requests, "get", lambda *a, **k: _Resp([{"paper": {"id": "2607.00001"}}]))
    sig = pg.Signals()
    assert pg.admit(paper(), sig) == (True, "hf-daily")
    assert "HF-SIGNAL-UNAVAILABLE" not in capsys.readouterr().out
    assert sig.status_line().endswith("ok (7/7 days)")


def test_allowlist_fixed_hosts_include_hf():
    import allowlist

    assert "huggingface.co" in allowlist.FIXED_HOSTS


def test_hn_arxiv_link_needs_a_quality_signal(monkeypatch):
    import ingest_hn as hn

    rules = c.load_yaml(c.SOURCES_FILE)["classification"]
    hit = {
        "title": "Jailbreak and prompt injection attack on LLM agents",
        "url": "https://arxiv.org/abs/2607.00001",
        "objectID": "1",
        "points": 300,
        "created_at": "2026-07-14T00:00:00Z",
    }
    blog = {**hit, "url": "https://blog.example.com/jailbreak", "objectID": "2"}
    cfg = {"hackernews": {"queries": ["x"], "top_stories": False, "min_points": 1}}
    monkeypatch.setattr(hn, "search_stories", lambda *a, **k: [hit, blog])

    monkeypatch.setattr(pg, "fetch_hf_daily", lambda: (set(), 7))
    urls = {x["article_url"] for x in hn.collect(cfg, rules, None)}
    assert urls == {"https://blog.example.com/jailbreak"}  # arXiv link dropped

    monkeypatch.setattr(pg, "fetch_hf_daily", lambda: ({"2607.00001"}, 7))
    urls = {x["article_url"] for x in hn.collect(cfg, rules, None)}
    assert "https://arxiv.org/abs/2607.00001" in urls
