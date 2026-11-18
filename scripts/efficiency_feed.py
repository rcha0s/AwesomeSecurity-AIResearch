#!/usr/bin/env python3
"""
efficiency_feed.py — docs/efficiency.md: the cost and work efficiency track as one
plain Markdown page an agent harness can fetch and act on.

Rohan, 2026-11-18: "when I am updating my harness, I can keep pointing it to this
resource where it can always fetch the latest research in cost efficiency." The
site is a JavaScript app, which an agent's fetch tool reads badly; this page is the
same data (live efficiency claims with what to do, plus the vetted efficiency
findings of the last month) in a stable shape at a stable URL:

    https://rcha0s.github.io/AwesomeSecurity-AIResearch/efficiency.md

generate_html.py writes it on every render, from the same payload as the site, so
it can never drift from what the site shows. Generated - do not hand-edit.
"""

from __future__ import annotations

import re

import briefing

FEED_NAME = "efficiency.md"
FINDINGS_DAYS = 31  # the pool's max_age_days: every efficiency finding still live
TRACKS = (("cost", "Cost efficiency"), ("work", "Work efficiency"))


def _md(text: object, limit: int = 0) -> str:
    """One line of plain text, safe inside Markdown (no stray links or emphasis)."""
    out = " ".join(str(text or "").split())
    if limit and len(out) > limit:
        out = out[: limit - 1].rstrip() + "…"
    return re.sub(r"([\\\[\]<>*_`|])", r"\\\1", out)


def _url(value: object) -> str:
    """An http(s) URL safe to put in a Markdown link, or ""."""
    url = str(value or "").strip()
    if not re.match(r"^https?://", url, re.I) or re.search(r"[\s()<>]", url):
        return ""
    return url


def _link(label: object, url: object) -> str:
    u = _url(url)
    return f"[{_md(label)}]({u})" if u else _md(label)


def _claim_block(claim: dict, site_url: str) -> list[str]:
    title = claim.get("title") or claim.get("statement") or claim.get("id")
    meta = [str(claim.get("status") or ""), f"confidence {float(claim.get('confidence') or 0):.2f}"]
    updated = briefing.claim_updated(claim)
    if updated:
        meta.append(f"updated {updated}")
    out = [
        f"### {_md(title)}",
        "",
        f"`{_md(claim.get('id'))}` · {' · '.join(meta)} · "
        f"[on the site]({site_url}?claim={claim.get('id')}#claims)",
        "",
    ]
    if claim.get("statement") and claim.get("statement") != title:
        out += [_md(claim["statement"]), ""]
    if claim.get("guidance"):
        out += [f"**Do this:** {_md(claim['guidance'])}", ""]
    if claim.get("scope"):
        out += [f"**Conditions:** {_md(claim['scope'])}", ""]
    evidence = [e for e in claim.get("evidence") or [] if isinstance(e, dict)]
    evidence.sort(key=lambda e: str(e.get("published") or ""), reverse=True)
    if evidence:
        out.append("Evidence, newest first:")
        for e in evidence:
            when = f" ({_md(e.get('published'))})" if e.get("published") else ""
            note = f" {_md(e.get('note'), 240)}" if e.get("note") else ""
            stance = _md(e.get("stance") or "supports")
            out.append(
                f"- {stance}: {_link(e.get('title') or e.get('url'), e.get('url'))}{when}{note}"
            )
        out.append("")
    return out


def _finding_line(row: dict) -> list[str]:
    head = f"- **{_link(row.get('title'), row.get('url'))}** · {_md(row.get('published'))}"
    if row.get("source_name"):
        head += f" · {_md(row.get('source_name'))}"
    out = [head]
    if row.get("takeaway"):
        out.append(f"  {_md(row['takeaway'], 400)}")
    act = row.get("actionable") or {}
    if act.get("title"):
        detail = f" {_md(act.get('detail'), 500)}" if act.get("detail") else ""
        out.append(f"  Try: {_md(act['title'])}.{detail}")
    return out


def render(payload: dict, now: str, site_url: str) -> str:
    """The whole page. Claims: every live claim in the two efficiency domains, most
    recently updated first. Findings: every vetted efficiency finding of the last
    FINDINGS_DAYS days, newest first, whatever other Briefing lane also shows it."""
    claims = [
        c
        for c in payload.get("claims") or []
        if c.get("domain_id") in briefing.EFFICIENCY_DOMAINS.values()
        and c.get("status") in ("current", "contested")
    ]
    claims.sort(key=lambda c: str(c.get("id")))
    claims.sort(key=briefing.claim_updated, reverse=True)
    rows = list(payload.get("findings") or []) + list(payload.get("editorial") or [])
    seen, finds = set(), []
    for row in briefing.efficiency_findings(rows, now, FINDINGS_DAYS, n_max=10_000):
        if row.get("id") not in seen:
            seen.add(row.get("id"))
            finds.append(row)
    out = [
        "# Agent efficiency: what to change in your harness",
        "",
        f"_Generated {now} from the claim ledger and the vetted findings of "
        f"[Awesome Security & AI Research]({site_url}). Generated - do not hand-edit._",
        "",
        "This page is meant to be fetched by an agent harness. Each claim is a standing answer: "
        "**Do this** is the change to make, **Conditions** is where it does not hold, and the "
        "evidence is newest first. Contested claims have evidence on both sides; weigh them "
        "before acting. New research lists the last month of vetted findings that have not "
        "necessarily changed a claim yet.",
        "",
    ]
    for key, name in TRACKS:
        domain = briefing.EFFICIENCY_DOMAINS[key]
        mine = [c for c in claims if c.get("domain_id") == domain]
        out += [f"## {name} ({len(mine)} claims)", ""]
        for claim in mine:
            out += _claim_block(claim, site_url)
        if not mine:
            out += ["_No live claims._", ""]
    out += [f"## New research, last {FINDINGS_DAYS} days ({len(finds)})", ""]
    for row in finds:
        out += _finding_line(row)
    if not finds:
        out.append("_No vetted efficiency findings in this window._")
    return "\n".join(out).rstrip() + "\n"
