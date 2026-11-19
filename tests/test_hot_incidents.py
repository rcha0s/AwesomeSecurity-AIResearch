"""The hot-incident bar and curated file (scripts/hot_incidents.py), the scan's hot
fast path (select_batch.py), the between-scan watch (hot_watch.py) and the outlet
count fix in generate_html.story_fields.

2026-11-18: Rohan could not find NGINX2Root or Java4Shell on the site. Java4Shell was
in the pool but ranked as a one-outlet story; NGINX2Root came out after the day's
scan. Routine advisories must never reach the section ("We don't really care for
every advisory item")."""

from __future__ import annotations

import copy
import json

import common
import generate_html
import hot_incidents as hot
import hot_watch
import pytest
import select_batch
from test_prefilter import _cand
from test_select_batch import conf

CRIT = frozenset({"critical", "rce"})
UBIQ = ["nginx", "Java", "OpenJDK", "Linux kernel"]


def hot_conf(**limits) -> common.Config:
    c = conf(4, 1, **{"batch_story_max": 1, "batch_story_min_sources": 2, **limits})
    hot_cfg = {"wide_outlets": 4, "min_outlets": 3, "min_reach": 2, "ubiquitous": UBIQ}
    return common.Config(**{**c.__dict__, "hot": hot_cfg})


# --- the bar ----------------------------------------------------------------------
def test_bar_needs_critical_and_two_reach_signals():
    s = hot.settings(hot_conf())
    assert hot.bar_reasons(CRIT, 4, False, True, s) == ["wide-coverage", "ubiquitous"]
    assert hot.bar_reasons(CRIT, 3, True, True, s) == ["exploited", "ubiquitous"]


def test_one_reach_signal_is_not_hot():
    s = hot.settings(hot_conf())
    assert hot.bar_reasons(CRIT, 3, True, False, s) == []
    assert hot.bar_reasons(CRIT, 5, False, False, s) == []
    assert hot.bar_reasons(CRIT, 3, False, True, s) == []
    # An exploited bug three outlets wrote up is ordinary news (2026-10-23 PAN-OS shape).
    assert hot.bar_reasons(frozenset({"exploited"}), 3, True, False, s) == []
    # "Exploited" is never critical by itself, so it can't count twice.
    assert hot.bar_reasons(frozenset({"exploited"}), 9, True, True, s) == []


def test_a_routine_advisory_is_never_hot():
    s = hot.settings(hot_conf())
    # Not critical: a medium bug in very common software, everywhere, still is not hot.
    assert hot.bar_reasons(frozenset({"rce"}), 9, False, True, s) == []
    assert hot.bar_reasons(frozenset(), 9, True, True, s) == []
    # Critical but one or two outlets: an advisory few others wrote about.
    assert hot.bar_reasons(CRIT, 1, True, True, s) == []
    assert hot.bar_reasons(CRIT, 2, True, True, s) == []


def test_preauth_rce_counts_as_critical_and_exploited_alone_does_not():
    assert hot.is_critical({"rce", "unauthenticated"})
    assert not hot.is_critical({"exploited"})
    assert not hot.is_critical({"rce"})


def test_ubiquitous_matches_whole_words_only():
    assert hot.ubiquitous_hit("Bug in nginx HTTP/2", UBIQ) == "nginx"
    assert hot.ubiquitous_hit("JavaScript framework flaw", UBIQ) == ""
    assert hot.ubiquitous_hit("A Linux kernel SCTP bug", UBIQ) == "Linux kernel"


def test_settings_fall_back_to_defaults_on_bad_config():
    c = common.Config(**{**common.load_config().__dict__, "hot": {"wide_outlets": "x"}})
    assert hot.settings(c)["wide_outlets"] == hot.DEFAULTS["wide_outlets"]
    assert hot.settings(None)["min_reach"] == 2


# --- the curated file -------------------------------------------------------------
COMMITTED = hot.load()  # read at import, before the sandbox fixture redirects DATA_DIR


def entry() -> dict:
    return copy.deepcopy(COMMITTED[0])


def test_the_committed_file_is_valid_and_leads_with_both_incidents():
    rows = copy.deepcopy(COMMITTED)
    assert hot.validate(rows) == []
    assert [r["id"] for r in rows][:2] == ["nginx2root", "java4shell"]


def test_an_entry_off_the_bar_is_rejected():
    e = entry()
    e["bar"] = ["ubiquitous"]
    assert any("bar" in p for p in hot.problems(e))
    e["bar"] = ["popular"]
    assert hot.problems(e)


def test_exploit_code_is_rejected():
    for text in ("```python\nx```", "run /bin/sh -c", "payload \\x41\\x41", "curl -X POST"):
        e = entry()
        e["exploitation"] = text
        assert hot.problems(e), text


def test_sources_must_be_https_and_independent():
    e = entry()
    e["sources"] = [
        {"name": "One", "url": "https://a.example/x"},
        {"name": "Two", "url": "https://a.example/y"},
    ]
    assert hot.problems(e)  # one host
    e["sources"][1]["url"] = "http://b.example/y"
    assert hot.problems(e)  # not https
    e["sources"][1]["url"] = "https://b.example/y"
    e["bar"] = ["exploited", "ubiquitous"]
    assert hot.problems(e)  # two outlets: below min_outlets
    e["sources"].append({"name": "Repo", "url": "https://github.com/x/poc"})
    assert hot.problems(e)  # GitHub is not an outlet
    e["sources"].append({"name": "Sub", "url": "https://news.b.example/z"})
    assert hot.problems(e)  # one registrable domain is one outlet
    e["sources"].append({"name": "Three", "url": "https://c.example.co.uk/z"})
    assert hot.problems(e) == []
    e["bar"] = ["wide-coverage", "ubiquitous"]
    assert hot.problems(e)  # wide coverage needs 4 hosts


def test_duplicate_ids_and_overlong_fields_are_rejected():
    e = entry()
    assert any("duplicate" in p for p in hot.validate([e, copy.deepcopy(e)]))
    e["impact"] = "x" * (hot.FIELD_MAX + 1)
    assert hot.problems(e)


def test_old_incidents_leave_the_section():
    rows = copy.deepcopy(COMMITTED)
    assert len(hot.active(rows, "2026-11-20", 30)) == 2
    assert hot.active(rows, "2027-01-30", 30) == []


def test_readme_section_states_the_bar_and_links_each_incident():
    lines = hot.readme_lines(COMMITTED, "https://site.example/")
    text = "\n".join(lines)
    assert lines[0] == "## Hot incidents"
    assert "Routine advisories and patch roundups never qualify" in text
    assert "?hot=nginx2root#week" in text and "?hot=java4shell#week" in text
    assert hot.readme_lines([], "https://site.example/") == []


def test_feeds_carry_every_summary_field():
    rows = copy.deepcopy(COMMITTED)
    md = hot.render_feed(rows, "2026-11-19", "https://site.example/")
    for field in ("Root cause", "Conditions", "Fix"):
        assert field in md
    data = json.loads(hot.render_json(rows, "2026-11-19"))
    assert {r["id"] for r in data["incidents"]} == {"nginx2root", "java4shell"}


# --- the scan's hot fast path -----------------------------------------------------
REFERENCE = [{"title": "Old", "summary": "A heap overflow in the parser was patched."}]


def news(i: int, title: str, src: str, rank: float = 40.0, **over) -> dict:
    return _cand(
        id=f"h{i}" if i < 10 else f"a{i}",
        title=title,
        source_url=f"https://{src}.example/story{i}",
        article_url=f"https://{src}.example/story{i}",
        **{"source_id": f"rss:{src}", "source_rank": rank, "published": "2026-07-14", **over},
    )


def nginx_story() -> list[dict]:
    return [
        news(0, "Critical unauthenticated RCE in nginx HTTP/2 CVE-2026-123007", "thn"),
        news(1, "nginx patches critical CVE-2026-123007 remote code execution", "bleeping"),
        news(2, "Critical nginx RCE CVE-2026-123007 chains to root", "register"),
        news(3, "nginx CVE-2026-123007: critical RCE, patch now", "securityweek"),
    ]


def big_story() -> list[dict]:
    """A non-hot multi-source story that would otherwise take the one lane slot."""
    return [
        news(10, "Critical RCE in AcmeCMS plugin CVE-2026-55555", "a1", rank=90.0),
        news(11, "AcmeCMS critical CVE-2026-55555 remote code execution", "a2", rank=90.0),
    ]


def flood(n: int = 20) -> list[dict]:
    return [
        _cand(
            id=f"f{i}",
            title=f"Neutral finding number {i} about topic{i}",
            source_url=f"https://flood{i}.example/p",
            source_id=f"rss:flood{i}",
            source_rank=80.0,
            published="2026-07-15",
        )
        for i in range(n)
    ]


def run(staged, c=None, known=()):
    import prefilter

    table = prefilter.KeywordTable(keywords={"ais.prompt-injection": ("jailbreak",)}, excluded=())
    return select_batch.select(
        staged, c or hot_conf(), table, reference=REFERENCE, known=list(known)
    )


def test_a_hot_story_is_dealt_first_beyond_the_story_cap(sandbox):
    batch, _ = run(big_story() + nginx_story() + flood())
    hot_rows = [r for r in batch if r.get("batch_hot")]
    assert len(hot_rows) == 1 and hot_rows[0]["id"].startswith("h")
    assert set(hot_rows[0]["batch_hot"]) == {"wide-coverage", "ubiquitous"}
    assert sum(1 for r in batch if r["id"].startswith("h")) == 1  # one slot per story
    stories = [r for r in batch if r.get("batch_priority") == "story"]
    assert len(stories) == 2  # the hot one plus the one batch_story_max allows
    flags = select_batch.hot_flags(batch)
    assert flags[0]["reasons"] == hot_rows[0]["batch_hot"] and len(flags[0]["coverage"]) == 3


def test_hot_slots_are_capped(sandbox):
    batch, _ = run(nginx_story() + flood(), hot_conf(batch_hot_max=0))
    assert not any(r.get("batch_hot") for r in batch)


def test_two_outlets_in_niche_software_are_not_hot(sandbox):
    batch, _ = run(big_story() + flood())
    assert not any(r.get("batch_hot") for r in batch)


def test_a_kev_listing_counts_as_exploited_not_as_an_outlet(sandbox):
    kev = news(5, "CISA adds AcmeCMS CVE-2026-55555 to KEV, critical RCE exploited", "cisa",
               source_id="kev_json:cisa")  # fmt: skip
    one = news(6, "Critical AcmeCMS RCE CVE-2026-55555", "thn")
    batch, _ = run([kev, one] + flood())
    assert not any(r.get("batch_hot") for r in batch)  # one outlet + KEV: below min_outlets


def test_a_known_story_can_turn_hot_unless_already_called_out(sandbox):
    """NGINX2Root's pattern: covered quietly first, then everywhere."""
    known = [{"title": nginx_story()[0]["title"], "published": "2026-07-13"}]
    batch, _ = run(nginx_story() + flood(), known=known)
    assert [r["batch_hot"] for r in batch if r.get("batch_hot")] == [
        ["wide-coverage", "ubiquitous"]
    ]
    hot.save([{**entry(), "cves": ["CVE-2026-123007"]}])
    batch, _ = run(nginx_story() + flood(), known=known)
    assert not any(r.get("batch_hot") for r in batch)


def test_an_exploited_appliance_bug_three_outlets_carry_is_not_hot(sandbox):
    copies = [
        news(20, "Critical FortiOS SSL-VPN flaw CVE-2026-77777 actively exploited", "thn"),
        news(21, "Fortinet FortiOS critical CVE-2026-77777 exploited in attacks", "bleeping"),
        news(22, "FortiOS zero-day CVE-2026-77777 critical, patch now", "register"),
    ]
    batch, _ = run(copies + flood())
    assert not any(r.get("batch_hot") for r in batch)  # FortiOS is not on the common list


def test_common_software_counts_only_in_a_headline(sandbox):
    copies = [
        news(30, "Critical RCE in AcmeCMS CVE-2026-88888 under attack", "thn",
             excerpt="Windows and Chrome users are not affected."),
        news(31, "AcmeCMS critical CVE-2026-88888 exploited", "bleeping",
             excerpt="Runs on Windows servers."),
        news(32, "AcmeCMS CVE-2026-88888: critical, exploited", "register"),
    ]  # fmt: skip
    c = hot_conf()
    c = common.Config(**{**c.__dict__, "hot": {**c.hot, "ubiquitous": ["Windows", "Chrome"]}})
    batch, _ = run(copies + flood(), c)
    assert not any(r.get("batch_hot") for r in batch)


def test_roundup_copies_are_not_outlets(sandbox):
    copies = [
        news(0, "Critical unauthenticated RCE in nginx HTTP/2 CVE-2026-123007", "thn"),
        news(40, "Weekly recap: nginx CVE-2026-123007 critical RCE and more", "a1"),
        news(41, "Patch Tuesday roundup: nginx CVE-2026-123007 critical", "a2"),
        news(42, "This week in security: critical nginx CVE-2026-123007", "a3"),
    ]
    batch, _ = run(copies + flood())
    assert not any(r.get("batch_hot") for r in batch)


# --- the between-scan watch -------------------------------------------------------
def test_watch_finds_a_new_hot_story_and_skips_covered_ones():
    c = hot_conf()
    items = hot_watch.detect(nginx_story(), c, [], reference=REFERENCE)
    assert len(items) == 1
    item = items[0]
    assert item["cves"] == ["CVE-2026-123007"] and len(item["copies"]) == 4
    assert "cve-2026-123007" in item["keys"] and len(item["keys"]) == 5  # 1 CVE + 4 URLs
    covered = [{"name": "Other", "cves": ["CVE-2026-123007"]}]
    assert hot_watch.detect(nginx_story(), c, covered, reference=REFERENCE) == []
    by_name = [{"name": "nginx", "cves": []}]
    assert hot_watch.detect(nginx_story(), c, by_name, reference=REFERENCE) == []


def test_watch_ignores_routine_stories():
    assert hot_watch.detect(big_story(), hot_conf(), [], reference=REFERENCE) == []
    assert hot_watch.detect([], hot_conf(), []) == []


def test_issue_text_is_inert():
    assert "<" not in hot_watch.plain("<img src=x> [link](https://e.example)")
    assert "@​" in hot_watch.plain("ping @rcha0s")
    assert len(hot_watch.plain("x" * 500)) == hot_watch.TITLE_MAX
    item = {"keys": ["cve-2026-1", "url-0123456789abcdef"], "reasons": ["exploited", "ubiquitous"], "cves": [],
            "copies": [{"title": "T", "url": "https://e.example/a"}]}  # fmt: skip
    body = hot_watch.issue_body(item)
    assert hot_watch.KEY_RE.findall(body) == ["cve-2026-1", "url-0123456789abcdef"]
    assert "none named yet" in body


def test_alert_opens_one_issue_per_incident(monkeypatch):
    calls = []

    def fake_gh(*args, body=None):
        calls.append((args, body))
        if args[0] == "repos/o/r/labels":
            raise RuntimeError("gh api labels failed: Validation Failed {already_exists}")
        if args[0].startswith("repos/o/r/issues?"):
            assert "--paginate" in args
            return json.dumps("old\n<!-- hot-key: cve-2026-1 -->") + "\n"
        return "{}"

    monkeypatch.setattr(hot_watch, "_gh", fake_gh)
    blank = {"reasons": [], "cves": [], "copies": []}
    items = [
        # a CVE assigned later or a new outlet: shares a key with the old issue
        {**blank, "keys": ["cve-2026-1", "url-aaaaaaaaaaaaaaaa"], "title": "Old, renamed"},
        {**blank, "keys": ["url-bbbbbbbbbbbbbbbb"], "title": "New"},
        {**blank, "keys": ["url-bbbbbbbbbbbbbbbb", "url-cccc"], "title": "New, other group"},
    ]
    assert hot_watch.alert(items, "o/r") == 1
    posted = [b for a, b in calls if a[0] == "repos/o/r/issues"]
    assert len(posted) == 1 and posted[0]["title"] == "Hot incident: New"


def test_gh_errors_carry_the_api_body(monkeypatch):
    """gh writes the API's error body (already_exists) to stdout, not stderr."""

    class Res:
        returncode, stdout, stderr = 1, '{"errors":[{"code":"already_exists"}]}', "HTTP 422"

    monkeypatch.setattr(hot_watch.subprocess, "run", lambda *a, **k: Res())
    with pytest.raises(RuntimeError, match="already_exists"):
        hot_watch._gh("repos/o/r/labels")


def test_the_watch_fails_loudly_when_no_feed_answers(monkeypatch):
    monkeypatch.setattr(hot_watch, "watch_sources", lambda conf: [{"id": "x"}, {"id": "y"}])
    monkeypatch.setattr(hot_watch, "fetch", lambda sources: ([], 0))
    assert hot_watch.main([]) == 1
    monkeypatch.setattr(hot_watch, "fetch", lambda sources: ([], 1))
    assert hot_watch.main([]) == 0


# --- the outlet count fix ---------------------------------------------------------
def test_entry_corroborators_count_as_outlets():
    entry = {
        "id": "java4shell",
        "source_url": "https://securitylabs.example/java4shell",
        "corroborating_sources": [
            {"name": "thn", "url": "https://thn.example/j"},
            {"name": "orca", "url": "https://orca.example/j"},
            {"name": "self", "url": "https://securitylabs.example/java4shell"},
            {"name": "dup", "url": "https://thn.example/j"},
            {"name": "same outlet", "url": "https://www.thn.example/another-article"},
            "not-a-dict",
        ],
    }
    ledger = {
        "stories": {"s1": {"sources": [{"url": "https://ledger.example/j", "source_name": "L"}]}}
    }
    out = generate_html.story_fields(entry, (ledger, {"java4shell": "s1"}))
    urls = [x["url"] for x in out["corroborators"]]
    assert urls == ["https://ledger.example/j", "https://thn.example/j", "https://orca.example/j"]


@pytest.mark.parametrize("bad", ["UPPER", "-lead", "a"])
def test_ids_must_be_url_safe(bad):
    e = entry()
    e["id"] = bad
    assert hot.problems(e)


def test_kev_plus_three_outlets_in_common_software_is_hot_without_wide_coverage(sandbox):
    kev = news(7, "CISA adds nginx CVE-2026-123007 to KEV, critical RCE exploited", "cisa",
               source_id="kev_json:cisa")  # fmt: skip
    batch, _ = run([kev] + nginx_story()[:3] + flood())
    rows = [r for r in batch if r.get("batch_hot")]
    assert len(rows) == 1
    assert rows[0]["batch_hot"] == ["exploited", "ubiquitous"]  # KEV is not a third outlet


def test_add_takes_only_a_flagged_new_entry(sandbox, tmp_path):
    e = {**entry(), "id": "new-incident", "disclosed": "2026-07-14", "updated": "2026-07-15"}
    path = tmp_path / "e.json"

    def add(row) -> int:
        path.write_text(json.dumps(row))
        return hot.main(["add", str(path)])

    assert add(e) == 1  # no flag
    flag = {"id": "h0", "reasons": ["wide-coverage", "ubiquitous"], "url": e["sources"][0]["url"]}
    common.save_json(
        common.DATA_DIR / "_scan_hot.json",
        [flag, {**flag, "id": "h9", "url": "https://x.example/"}],
    )
    assert add({**e, "flag": "h0", "bar": ["exploited", "ubiquitous"]}) == 1  # extra reason
    assert add({**e, "flag": "h9"}) == 1  # cites none of the flagged story's URLs
    assert add({**e, "flag": "h0", "updated": "2026-08-01"}) == 1  # dated in the future
    assert add({**e, "flag": "h0"}) == 0
    assert hot.load()[0]["flag"] == "h0"
    assert add({**e, "id": "second", "flag": "h0"}) == 1  # a flag backs one entry


def test_add_updates_keep_what_was_published(sandbox, tmp_path):
    e = {**entry(), "id": "new-incident", "disclosed": "2026-07-14", "updated": "2026-07-14"}
    e["flag"] = "h0"
    hot.save([e])
    common.save_json(
        common.DATA_DIR / "_scan_hot.json",
        [{"id": "other", "reasons": ["exploited", "ubiquitous"], "url": "https://x.example/"}],
    )
    path = tmp_path / "e.json"

    def add(row) -> int:
        path.write_text(json.dumps(row))
        return hot.main(["add", str(path)])

    assert add({**e, "status": "Now on CISA KEV.", "updated": "2026-07-15"}) == 0
    assert hot.load()[0]["status"] == "Now on CISA KEV."
    e = hot.load()[0]
    assert add({**e, "updated": "2026-07-15"}) == 1  # only re-dated
    assert add({**e, "status": "x", "bar": [*e["bar"], "exploited"]}) == 1
    # an unrelated flag never unlocks a change (review of 2026-11-19)
    assert add({**e, "status": "x", "flag": "other", "cves": ["CVE-2026-9999"]}) == 1
    assert add({**e, "status": "x", "flag": None}) == 1  # cannot free its flag
    assert add({**e, "status": "x", "disclosed": "2026-07-01"}) == 1
    assert add({**e, "status": "x", "updated": "2026-12-31"}) == 1


def test_critical_infrastructure_is_not_a_critical_bug(sandbox):
    copies = [
        news(
            50, "Hackers exploit nginx flaw CVE-2026-66666 against critical infrastructure", "thn"
        ),
        news(51, "nginx CVE-2026-66666 exploited at critical infrastructure sites", "bleeping"),
        news(52, "nginx CVE-2026-66666 hits critical infrastructure", "register"),
        news(53, "Critical infrastructure targeted via nginx CVE-2026-66666", "securityweek"),
    ]
    batch, _ = run(copies + flood())
    assert not any(r.get("batch_hot") for r in batch)
