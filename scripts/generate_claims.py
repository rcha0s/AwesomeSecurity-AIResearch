#!/usr/bin/env python3
"""
generate_claims.py — Render the claim ledger into browsable markdown.

Reads data/claims.json and writes:
  - claims/README.md          the index: counts per topic + "what changed recently"
  - claims/<topic>.md         one page per topic: standing answers on top,
                              retired ones at the bottom with why they fell

The layout is the whole point: a reader lands on the current answer, and the
answer it replaced is still there — demoted, struck through, and carrying the
reason and date it was retired. Nothing is deleted.

Do not hand-edit generated files — edit data/claims.json and regenerate.

Usage:
    python scripts/generate_claims.py
"""

from __future__ import annotations

from datetime import UTC, datetime

import common as c

import claims as cl

RECENT_CHANGES = 12  # supersessions listed in the index changelog

STATUS_LABEL = {
    "current": "✅ Current",
    "contested": "⚖️ Contested",
    "superseded": "🪦 Superseded & refuted",
    "refuted": "🪦 Superseded & refuted",
}


def anchor_id(claim_id: str) -> str:
    """Stable in-page anchor for a claim (namespaced so it can't collide with
    a markdown heading slug)."""
    return f"claim-{claim_id}"


def fmt_date(date: str | None) -> str:
    """'2026-07-26' -> 'Jul 26, 2026'; '2026-07' -> 'Jul 2026'; None -> 'undated'."""
    for fmt, out in (("%Y-%m-%d", "%b %-d, %Y"), ("%Y-%m", "%b %Y")):
        try:
            parsed = datetime.strptime(date or "", fmt)
        except (ValueError, TypeError):
            continue
        return parsed.strftime(out.replace("%-d", "%d")).replace(" 0", " ")
    return "undated"


def claim_title(claim: dict) -> str:
    """Concise headline for a claim, falling back to the full statement for
    claims (or test fixtures) written before the title field existed."""
    return claim.get("title") or claim["statement"]


def claim_link(claim_id: str, index: dict[str, dict]) -> str:
    """A link to another claim on the same page: id, then its title."""
    target = index.get(claim_id)
    label = f"[`{claim_id}`](#{anchor_id(claim_id)})"
    return f"{label} — {claim_title(target)}" if target else label


def evidence_block(claim: dict) -> list[str]:
    """Sources behind a claim, as a collapsed table so the page stays skimmable."""
    evidence = claim.get("evidence") or []
    if not evidence:
        return []
    rows = ["| Stance | Source | Published |", "| --- | --- | --- |"]
    for item in evidence:
        title = item.get("title") or item.get("source_name") or item.get("url", "source")
        published = fmt_date(item.get("published"))
        rows.append(f"| {item.get('stance', '?')} | [{title}]({item['url']}) | {published} |")
    return [
        f"<details><summary>Evidence ({len(evidence)})</summary>",
        "",
        *rows,
        "",
        "</details>",
        "",
    ]


def _meta_line(claim: dict) -> str:
    bits = [f"`{claim['id']}`"]
    if cl.is_retired(claim):
        bits.append(f"**{claim.get('status')}** on {fmt_date(claim.get('superseded_on'))}")
        if claim.get("first_seen"):
            bits.append(f"had stood since {fmt_date(claim.get('first_seen'))}")
    else:
        bits.append(f"confidence **{cl.confidence_of(claim):.2f}**")
        if claim.get("domain"):
            bits.append(str(claim["domain"]))
        if claim.get("first_seen"):
            bits.append(f"standing since {fmt_date(claim.get('first_seen'))}")
    return " · ".join(bits)


def render_live_claim(claim: dict, index: dict[str, dict]) -> list[str]:
    """A standing answer: title, the full statement, basis, limits, what to do."""
    title = claim_title(claim)
    out = [
        f'<a id="{anchor_id(claim["id"])}"></a>',
        "",
        f"### {title}",
        "",
        _meta_line(claim),
        "",
    ]
    if title != claim["statement"]:
        out += [claim["statement"], ""]
    if claim.get("basis"):
        out += [f"**Basis —** {claim['basis']}", ""]
    if claim.get("guidance"):
        out += [f"**Do this —** {claim['guidance']}", ""]
    if claim.get("scope"):
        out += [f"**Conditions —** {claim['scope']}", ""]
    for replaced in cl.edges(claim, "supersedes"):
        out += [f"**Replaces** {claim_link(replaced, index)}", ""]
    if claim.get("tags"):
        out += ["_Tags: " + ", ".join(f"`{t}`" for t in claim["tags"]) + "_", ""]
    return out + evidence_block(claim)


def render_retired_claim(claim: dict, index: dict[str, dict]) -> list[str]:
    """A retired answer: struck through, with the reason and the replacement."""
    title = claim_title(claim)
    out = [
        f'<a id="{anchor_id(claim["id"])}"></a>',
        "",
        f"### ~~{title}~~",
        "",
        _meta_line(claim),
        "",
    ]
    if title != claim["statement"]:
        out += [claim["statement"], ""]
    out += [
        f"**Why it was retired —** {claim.get('supersession_reason', 'no reason recorded')}",
        "",
    ]
    for winner in cl.edges(claim, "superseded_by"):
        out += [f"**Replaced by** {claim_link(winner, index)}", ""]
    return out + evidence_block(claim)


def _counts_line(topic_claims: list[dict], now: str) -> str:
    counts = {s: 0 for s in cl.STATUSES}
    for claim in topic_claims:
        if claim.get("status") in counts:
            counts[claim["status"]] += 1
    parts = [f"{counts[s]} {s}" for s in cl.STATUSES]
    return f"_{' · '.join(parts)} · updated {now}_"


def _section(title: str, section_claims: list[dict], index: dict[str, dict], intro="") -> list[str]:
    if not section_claims:
        return []
    out = [f"## {title}", ""]
    if intro:
        out += [f"> {intro}", ""]
    for claim in section_claims:
        renderer = render_retired_claim if cl.is_retired(claim) else render_live_claim
        out += renderer(claim, index)
    return out


def render_topic(topic: str, ledger: dict, now: str) -> str:
    """One topic's standing answers, with the retired ones kept underneath."""
    meta = c.TOPICS[topic]
    topic_claims = cl.claims_for_topic(ledger, topic)
    index = cl.claim_index(cl.all_claims(ledger))
    out = [
        f"# {meta['name']} — standing claims",
        "",
        f"> {meta['blurb']}",
        "",
        "> **What this page is.** The current answer for each question in this topic, "
        "ranked by confidence — and underneath, every answer it replaced, kept on "
        "purpose with the date and reason it was retired.",
        "",
        _counts_line(topic_claims, now),
        "",
        f"[← Claim index](README.md) · [{meta['name']} findings feed](../{topic}/README.md) "
        "· [Home](../README.md)",
        "",
    ]
    if not topic_claims:
        return "\n".join(out + ["_No claims tracked in this topic yet._", ""])

    by_status = {s: [cx for cx in topic_claims if cx.get("status") == s] for s in cl.STATUSES}
    out += _section("✅ Current", by_status["current"], index)
    out += _section(
        "⚖️ Contested",
        by_status["contested"],
        index,
        "Credible evidence on both sides. Treat these as open questions, not guidance.",
    )
    out += _section(
        "🪦 Superseded & refuted",
        by_status["superseded"] + by_status["refuted"],
        index,
        "Kept deliberately. Knowing what we used to believe — and why it stopped being "
        "true — is how you avoid re-adopting an answer the field has already moved past.",
    )
    return "\n".join(out + ["---", "", "[← Claim index](README.md)", ""])


def recent_changes(ledger: dict) -> list[dict]:
    """Retired claims, most recently retired first — the ledger's changelog."""
    retired = [claim for claim in cl.all_claims(ledger) if cl.is_retired(claim)]
    return sorted(retired, key=lambda claim: claim.get("superseded_on") or "", reverse=True)


def _changelog(ledger: dict) -> list[str]:
    changes = recent_changes(ledger)[:RECENT_CHANGES]
    out = [
        "## 🔁 What changed recently",
        "",
        "> Every time the field moved and we retired an answer. Newest first.",
        "",
    ]
    if not changes:
        return out + ["_Nothing has been superseded yet._", ""]
    index = cl.claim_index(cl.all_claims(ledger))
    for claim in changes:
        winners = ", ".join(
            f"[{claim_title(index[w])}]({claim['topic']}.md#{anchor_id(w)})"
            for w in cl.edges(claim, "superseded_by")
            if w in index
        )
        out += [
            f"- **{fmt_date(claim.get('superseded_on'))}** · {claim.get('status')} · "
            f"[~~{claim_title(claim)}~~]({claim['topic']}.md#{anchor_id(claim['id'])})  ",
            f"  ↳ {claim.get('supersession_reason', '')}"
            + (f"  \n  ↳ **Now:** {winners}" if winners else ""),
        ]
    return out + [""]


def _topic_table(ledger: dict) -> list[str]:
    out = ["| Topic | Current | Contested | Retired |", "| --- | --- | --- | --- |"]
    for topic, meta in c.TOPICS.items():
        topic_claims = cl.claims_for_topic(ledger, topic)
        live = [cx for cx in topic_claims if cl.is_live(cx)]
        current = sum(1 for cx in live if cx.get("status") == "current")
        out.append(
            f"| [{meta['name']}]({topic}.md) | {current} | {len(live) - current} "
            f"| {sum(1 for cx in topic_claims if cl.is_retired(cx))} |"
        )
    return out + [""]


def render_index(ledger: dict, now: str) -> str:
    """The ledger landing page: how it works, counts per topic, what changed."""
    total = len(cl.all_claims(ledger))
    out = [
        "# 📒 Standing claims",
        "",
        "> The findings feed tracks **what was published**. This ledger tracks **what we "
        "currently believe** — one durable claim per question, each with the evidence "
        "behind it, and each superseded answer kept underneath with the reason it fell.",
        "",
        f"_{total} claims tracked · updated {now}_",
        "",
        "**Status meanings**",
        "",
        "| Status | Meaning |",
        "| --- | --- |",
        "| ✅ `current` | The standing answer. Follow this. |",
        "| ⚖️ `contested` | Credible evidence both ways — an open question, not guidance. |",
        "| 🪦 `superseded` | A better answer replaced it. Kept, with the reason. |",
        "| 🪦 `refuted` | Shown to be wrong, not merely improved on. |",
        "",
        *_topic_table(ledger),
        *_changelog(ledger),
        "---",
        "",
        "[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md)",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ledger = cl.load_ledger()
    errors = cl.validate_ledger(ledger)
    if errors:
        print(f"claim ledger is invalid — refusing to render ({len(errors)} problems):")
        for error in errors[:20]:
            print(f"  - {error}")
        return 1

    now = datetime.now(UTC).strftime("%Y-%m-%d")
    base = c.ROOT / "claims"
    base.mkdir(parents=True, exist_ok=True)
    (base / "README.md").write_text(render_index(ledger, now), encoding="utf-8")
    for topic in c.TOPICS:
        (base / f"{topic}.md").write_text(render_topic(topic, ledger, now), encoding="utf-8")
    print(f"claims: rendered {len(cl.all_claims(ledger))} claims -> {base}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
