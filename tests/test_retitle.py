"""retitle.py: existing titles are cut to 12 words with no list, never with an
invented fact, and old page paths keep a "Moved" stub (Rohan, 2026-10-26)."""

from __future__ import annotations

import json

import add_claim
import common as c
import generate_site as gs
import retitle as rt
from conftest import make_entry
from test_claims import ledger_of, make_claim

import claims

LONG = (
    "OpenAI frontier-agent red team of its own training containment: microVM escapes, "
    "egress via metrics service, cache-timing channels"
)
PROSE = "OpenAI had its frontier agents attack the training sandbox; they escaped 2 microVMs."


def pooled(sandbox, **over):
    e = make_entry(id="e1", date="2026-10-20", title=LONG, summary=PROSE, **over)
    pool = c.load_pool(e["topic"])
    pool["entries"].append(e)
    c.save_pool(e["topic"], pool)
    c.save_json(c.ARCHIVE_FILE, [dict(e)])  # an archived copy too
    return e


def test_list_names_every_long_or_list_title(sandbox):
    e = pooled(sandbox)
    assert rt.main(["list"]) == 0
    assert e["id"] in rt.entries_by_id(rt.load_all()) and rt.too_long(e["title"])


def test_check_refuses_an_invented_fact_or_a_long_title(sandbox, tmp_path):
    e = pooled(sandbox)
    bad = {e["id"]: "OpenAI agents escaped 9 microVMs and CVE-2026-1 in training"}
    long = {e["id"]: " ".join(["word"] * 13)}
    for proposal, why in ((bad, "added"), (long, "13 words")):
        assert any(why in p for p in rt.check(proposal, rt.entries_by_id(rt.load_all()))[e["id"]])
    f = tmp_path / "bad.json"
    f.write_text(json.dumps(bad))
    assert rt.main(["apply", str(f)]) == 1  # refuses the whole file
    assert c.load_pool(e["topic"])["entries"][0]["title"] == LONG


def test_apply_retitles_every_copy_and_the_old_page_gets_a_stub(sandbox, tmp_path):
    e = pooled(sandbox)
    new = "OpenAI's own agents escaped 2 microVMs in its training sandbox"
    f = tmp_path / "ok.json"
    f.write_text(json.dumps({e["id"]: new}))
    assert rt.main(["apply", str(f)]) == 0
    live = c.load_pool(e["topic"])["entries"][0]
    assert live["title"] == new and live["previous_slugs"] == [c.title_slug(LONG)]
    assert c.load_json(c.ARCHIVE_FILE)[0]["title"] == new
    base = sandbox / "tree"
    assert gs._write_moved_stubs(base, [live]) == 1
    old = base / c.domain_slug(live["domain"]) / f"{live['date']}-{c.title_slug(LONG)}.md"
    assert old.read_text().startswith("# Moved")


def test_claims_need_a_short_distinct_title():
    assert claims.validate_ledger(ledger_of(make_claim(title=None))) != []
    assert claims.validate_ledger(ledger_of(make_claim(title=" ".join(["w"] * 13)))) != []
    same = make_claim(title="Same", statement="Same")
    assert any("repeats" in e for e in claims.validate_ledger(ledger_of(same)))


def test_titles_command_sets_many_headlines_in_one_save(sandbox, tmp_path):
    ledger = ledger_of(make_claim(id="a-claim"), make_claim(id="b-claim"))
    for x in ledger["claims"]:
        x.pop("title")
    claims.CLAIMS_FILE.write_text(json.dumps(ledger))  # invalid until both are titled
    f = tmp_path / "t.json"
    f.write_text(json.dumps({"a-claim": "A short headline", "b-claim": "Another headline"}))
    assert add_claim.main(["titles", str(f)]) == 0
    saved = {x["id"]: x["title"] for x in claims.load_ledger()["claims"]}
    assert saved == {"a-claim": "A short headline", "b-claim": "Another headline"}
