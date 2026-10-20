#!/usr/bin/env python3
"""
generate_site.py - Render README.md and the three topic trees from the pools.

Reads the three topic pools and writes:
  - README.md               short developer guide: this week's top stories and
                            claims (briefing.py picks, same as the site), links
                            into the site's views, how to contribute
  - <topic>/README.md       ranked index per topic (ai-security, product-security,
                            ai-research)
  - <topic>/<domain>/<YYYY-MM>-<slug>.md   one citation-first page per finding

Ranking uses each entry's composite score (rerank.py fills these); entries with
no scores yet are ranked by a live-computed newness so legacy items still sort.
Do not hand-edit generated files - edit the pools and regenerate.

Usage:
    python scripts/generate_site.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlencode

import briefing
import common as c
import generate_html as gh
import story_ledger as sl

import claims as cl

_DASH = re.compile(r"\s*[—–]\s*")


def _dedash(text: str) -> str:
    """Normalize em/en dashes to a SPACED hyphen in rendered markdown.

    A dash acting as a clause break becomes " - " rather than a compound-looking
    "word-word", keeping a consistent house style across every rendered file."""
    return _DASH.sub(" - ", text)


def fmt_month(date: str) -> str:
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(date, fmt).strftime("%b %Y")
        except (ValueError, TypeError):
            continue
    return date or "-"


def fmt_published(entry: dict) -> str:
    """Human-readable source publish date, day-precision when known."""
    pub = entry.get("published") or entry.get("date") or ""
    try:
        return datetime.strptime(pub, "%Y-%m-%d").strftime("%b %-d, %Y")
    except (ValueError, TypeError):
        pass
    try:  # Windows strftime has no %-d
        return datetime.strptime(pub, "%Y-%m-%d").strftime("%b %d, %Y").replace(" 0", " ")
    except (ValueError, TypeError):
        return fmt_month(pub)


def entry_scores(entry: dict, conf: c.Config) -> dict:
    scores = dict(entry.get("scores") or {})
    if "newness" not in scores:
        scores["newness"] = c.newness_score(entry.get("date") or "", conf.half_life_days)
    scores.setdefault("novelty", 0)
    scores.setdefault("relevance", 0)
    scores.setdefault("credibility", c.credibility_of(entry))
    if "composite" not in scores:
        scores["composite"] = c.composite_score(scores, conf.weights)
    return scores


def rank(entries: list[dict], conf: c.Config) -> list[dict]:
    return sorted(
        entries,
        key=lambda e: (
            -entry_scores(e, conf)["composite"],
            e.get("date") or "",
            e.get("title", ""),
        ),
    )


def entry_filename(entry: dict) -> str:
    return f"{(entry.get('date') or 'undated')}-{c.slugify(entry.get('title', ''), 60)}.md"


def entry_relpath(entry: dict) -> str:
    return f"{c.domain_slug(entry.get('domain') or 'General')}/{entry_filename(entry)}"


def score_line(scores: dict) -> str:
    return (
        f"**Scores:** Newness {scores['newness']} · Novelty {scores['novelty']} · "
        f"Relevance {scores['relevance']} · Credibility {round(scores.get('credibility', 50))} · "
        f"**Composite {scores['composite']}**"
    )


def _entry_top_meta(entry: dict) -> str:
    """The one line worth seeing before deciding to read: when this ran."""
    return f"**Published:** {fmt_published(entry)}"


def _entry_meta(entry: dict, scores: dict) -> list[str]:
    src = entry.get("source_url", "")
    topic_name = c.TOPICS.get(entry.get("topic", ""), {}).get("name", entry.get("topic", ""))
    meta = [
        f"**Topic:** {topic_name}  ·  **Domain:** {c.domain_name(entry.get('domain') or '-')}",
        f"**Source:** [{entry.get('source_name', 'source')}]({src})"
        + (f"  ·  **Author:** {entry['author']}" if entry.get("author") else "")
        + (
            f"  ·  **Retrieved:** {entry['retrieved_at'][:10]}" if entry.get("retrieved_at") else ""
        ),
        score_line(scores),
    ]
    if entry.get("tags"):
        meta.append("**Tags:** " + ", ".join(f"`{t}`" for t in entry["tags"]))
    corr = entry.get("corroborating_sources") or []
    if corr:
        links = ", ".join(f"[{s.get('name') or 'source'}]({s.get('url', '')})" for s in corr)
        meta.append(f"**Also reported by:** {links} _(+{len(corr)} corroborating)_")
    verified = entry.get("verified")
    if verified is True:
        line = "**Verification:** ✓ independently verified"
        if entry.get("prior_art"):
            line += f" · closest prior art: {entry['prior_art']}"
        meta.append(line)
    elif verified is False:
        meta.append("> ⚠️ _Failed independent verification._")
    if entry.get("needs_review"):
        meta.append("> ⚠️ _Pending review - auto-analyzed, not yet human-verified._")
    return meta


def _grounding_mark(les: dict) -> str:
    """Only the exceptional case earns a marker - a grounded excerpt is the
    expected state and doesn't need a checkmark decorating every bullet."""
    if les.get("grounded") is False:
        return " ⚠️ _(excerpt not found in source)_"
    return ""


def _entry_lessons_md(entry: dict) -> list[str]:
    lessons = entry.get("lessons") or []
    if not lessons:
        return []
    out = ["## What to learn", ""]
    for les in lessons:
        if isinstance(les, dict):
            line = f"- {les.get('point', '')}"
            if les.get("excerpt"):
                line += f' - _"{les["excerpt"]}"_{_grounding_mark(les)}'
            out.append(line)
        else:
            out.append(f"- {les}")
    return out + [""]


def _entry_tcm_md(entry: dict) -> list[str]:
    if not any(entry.get(k) for k in ("threat", "conditions", "mitigations")):
        return []
    out = ["## Threat · Conditions · Mitigations", ""]
    for label in ("threat", "conditions", "mitigations"):
        if entry.get(label):
            out.append(f"- **{label.title()}:** {entry[label].strip()}")
    return out + [""]


def render_entry_page(entry: dict, conf: c.Config) -> str:
    src = entry.get("source_url", "")
    out = [
        f"# {entry.get('title', 'Untitled')}",
        "",
        _entry_top_meta(entry),
        "",
    ]
    if entry.get("takeaway"):
        out += [f"> **Takeaway:** {entry['takeaway']}", ""]
    if entry.get("summary"):
        out += [
            "## TL;DR",
            "",
            entry["summary"].strip(),
            "",
        ]
    out += _entry_lessons_md(entry)
    out += _entry_tcm_md(entry)
    out += [
        "---",
        "",
        "  \n".join(_entry_meta(entry, entry_scores(entry, conf))),
        "",
        f"_Source: [{src}]({src})_  ·  [← back to index](../README.md)",
        "",
    ]
    return "\n".join(out)


def render_index_block(entry: dict, conf: c.Config) -> str:
    scores = entry_scores(entry, conf)
    takeaway = entry.get("takeaway") or entry.get("summary") or entry.get("threat") or ""
    flag = " · ⚠️ _review_" if entry.get("needs_review") else ""
    n_corr = len(entry.get("corroborating_sources") or [])
    corr = f" · 🔗 +{n_corr} sources" if n_corr else ""
    return (
        f"- **[{entry.get('title', 'Untitled')}]({entry_relpath(entry)})** "
        f"· composite **{scores['composite']}** · {fmt_published(entry)}{corr}{flag}  \n"
        f"  {c.clean_summary(takeaway, 200)}  \n"
        f"  _[{entry.get('source_name', 'source')}]({entry.get('source_url', '')})_"
    )


def _write_entry_pages(base: c.Path, by_domain: dict[str, list[dict]], conf: c.Config) -> None:
    if base.exists():  # clear stale per-domain pages first
        for old in base.glob("*/*.md"):
            old.unlink()
    for domain, items in by_domain.items():
        dpath = base / c.domain_slug(domain)
        dpath.mkdir(parents=True, exist_ok=True)
        for e in items:
            (dpath / entry_filename(e)).write_text(
                _dedash(render_entry_page(e, conf)), encoding="utf-8"
            )


def moved_stub(entry: dict) -> str:
    """A deterministic pointer page left at a finding's pre-taxonomy path."""
    new = f"../{c.domain_slug(entry.get('domain') or 'General')}/{entry_filename(entry)}"
    return (
        "# Moved\n\n"
        f"This finding now lives at [{entry.get('title', 'its new page')}]({new}).\n\n"
        "_Domains became fixed taxonomy IDs (data/taxonomy.yaml) and its page moved "
        "with its domain._\n"
    )


def _write_moved_stubs(base: c.Path, entries: list[dict]) -> int:
    """Leave a "Moved" stub at each page's old path so outside links still resolve."""
    written = 0
    for e in entries:
        old = c.moved_slug(e)
        path = base / old / entry_filename(e) if old else None
        if path is None or path.exists():  # never shadow a real page
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(moved_stub(e), encoding="utf-8")
        written += 1
    return written


def _editorial_section(editorial: list[dict]) -> list[str]:
    """A compact 'Trending & In the News' block for a topic page (links to source)."""
    if not editorial:
        return []
    editorial = sorted(
        editorial, key=lambda e: (e.get("editorial") or {}).get("at", ""), reverse=True
    )
    out = [
        "## 📈 Trending & In the News",
        "",
        "_Not new ideas - what the field is watching now, surfaced by the editorial pass._",
        "",
    ]
    for e in editorial:
        ed = e.get("editorial") or {}
        note = " · ".join(
            part for part in (ed.get("reason"), " · ".join(ed.get("signals") or [])) if part
        )
        out.append(f"- **[{e.get('title','')}]({e.get('source_url','')})**")
        if note:
            out.append(f"  _Why now: {note}_")
    return out + [""]


def _topic_index_md(topic, by_domain, curated, held, conf, now, editorial=()) -> str:
    meta = c.TOPICS[topic]
    held_note = f" · [{held} held for review](../REVIEW.md)" if held else ""
    out = [
        f"# {meta['name']}",
        "",
        f"> {meta['blurb']}",
        "",
        f"_{len(curated)} vetted findings · updated {now} · ranked by composite · "
        f"findings from the latest {conf.max_age_days} days{held_note}._",
        "",
    ]
    out += _editorial_section(list(editorial))
    out += ["| Domain | Findings |", "| --- | --- |"]
    order = sorted(by_domain, key=lambda d: -len(by_domain[d]))
    out += [f"| {c.domain_name(d)} | {len(by_domain[d])} |" for d in order] + [""]
    for domain in order:
        out += (
            [f"## {c.domain_name(domain)}", ""]
            + [render_index_block(e, conf) for e in rank(by_domain[domain], conf)]
            + [""]
        )
    out += [
        "---",
        "",
        f"[← Home](../README.md) · [Standing claims](../claims/{topic}.md) · "
        "[Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · "
        "[Review queue](../REVIEW.md)",
        "",
    ]
    return "\n".join(out)


def write_topic(topic: str, conf: c.Config, now: str) -> list[dict]:
    base = c.ROOT / topic
    all_entries = c.load_pool(topic)["entries"]
    # Only VETTED findings are shown; the rest live in the REVIEW.md queue.
    curated = [e for e in all_entries if c.is_curated(e, conf)]
    editorial = [e for e in all_entries if c.is_editorial(e)]

    # Editorial-promoted findings need their own detail pages too — the site
    # modal advertises a detail_path for them, and without a written .md the
    # modal falls back to the raw source. Merge them into the domain map so
    # they share the exact same page-rendering path as curated entries.
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for e in curated:
        by_domain[e.get("domain") or "General"].append(e)
    for e in editorial:
        by_domain[e.get("domain") or "General"].append(e)

    _write_entry_pages(base, by_domain, conf)
    _write_moved_stubs(base, [e for items in by_domain.values() for e in items])
    base.mkdir(parents=True, exist_ok=True)
    sources = c.load_sources_by_id()
    held = sum(1 for e in all_entries if c.is_held(e, conf, sources))
    md = _topic_index_md(topic, by_domain, curated, held, conf, now, editorial)
    (base / "README.md").write_text(_dedash(md), encoding="utf-8")
    return curated


# --- README: a short developer guide that points into the site ---------------
# The site carries everything in detail; the README teases this week's picks
# (chosen by briefing.py, the same picks the site's Briefing leads with) and
# links into the site's views. Methodology and honest limits live on the site's
# Methodology view.
SITE_URL = gh.SITE_URL
SITE_VIEWS = (
    ("Briefing", "week"),
    ("Claims", "claims"),
    ("Topics", "topics"),
    ("Methodology", "methodology"),
    ("Archive", "archive"),
)
ISSUES_URL = f"{gh.REPO_URL}/issues/new"


def site_link(view: str, **params: str) -> str:
    """A deep link into the site: `?<params>#<view>` (the site handles both)."""
    query = urlencode(params)
    return f"{SITE_URL}{'?' + query if query else ''}#{view}"


def md_text(text: str, limit: int = 0) -> str:
    """Plain text safe inside a markdown link label or list item."""
    text = c.clean_summary(str(text or ""), limit) if limit else " ".join(str(text or "").split())
    return re.sub(r"([\\\[\]<>*_`|])", r"\\\1", text)


def _story_line(n: int, row: dict, topic_names: dict) -> str:
    n_src = briefing.source_count(row)
    meta = [
        topic_names.get(row.get("topic", ""), row.get("topic", "")),
        fmt_published({"published": briefing.last_activity(row)}),
        f"{n_src} source{'s' if n_src > 1 else ''}",
    ]
    return (
        f"{n}. **[{md_text(row.get('title'))}]({site_link('week', finding=row['id'])})** "
        f"· _{md_text(' · '.join(meta))}_"
    )


def _claim_line(n: int, claim: dict) -> str:
    return (
        f"{n}. **[{md_text(claim.get('title') or claim.get('statement'))}]"
        f"({site_link('claims', claim=claim['id'])})**  \n"
        f"   {md_text(claim.get('guidance'), 200)}"
    )


def _teaser(payload: dict) -> list[str]:
    rows = {r["id"]: r for r in payload["findings"] + payload["editorial"]}
    claims = {cl_["id"]: cl_ for cl_ in payload["claims"]}
    names = {t: m["name"] for t, m in payload["topics"].items()}
    stories = [rows[i] for i in payload["top_stories"][:3] if i in rows]
    picks = [claims[i] for i in payload["top_claims"][:3] if i in claims]
    when = briefing.window_note(
        payload["top_stories_fresh"], len(payload["top_stories"]), payload["snapshot_days"]
    )
    out = ["## This week's top stories", "", f"_{when}_", ""]
    out += [_story_line(i, r, names) for i, r in enumerate(stories, 1)] or ["_No stories yet._"]
    out += ["", "## What to do now", "", "_Standing answers from the claim ledger._", ""]
    out += [_claim_line(i, cl_) for i, cl_ in enumerate(picks, 1)] or ["_No claims yet._"]
    return out + [""]


def _readme_head(payload: dict, now: str) -> list[str]:
    live = sum(1 for claim in payload["claims"] if cl.is_live(claim))
    badges = (
        f"![Updated](https://img.shields.io/badge/updated-{now.replace('-', '--')}-1f6feb) "
        f"![Vetted](https://img.shields.io/badge/vetted_findings-{len(payload['findings'])}-2da44e) "
        f"![Claims](https://img.shields.io/badge/standing_claims-{live}-6f42c1) "
        "![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)"
    )
    return [
        "# Awesome Security & AI Research",
        "",
        f'<p align="center"><a href="{SITE_URL}"><img src="docs/og.png" '
        'alt="Awesome Security & AI Research - a weekly, source-cited briefing" '
        'width="720"></a></p>',
        "",
        "> A weekly, source-cited briefing on AI security, product security and applied AI "
        "research. Every finding is vetted and distilled to one lesson; a claim ledger tracks "
        "what to do now and what it replaced.",
        "",
        badges,
        "",
        f"**The site is the product: [{SITE_URL.removeprefix('https://')}]({SITE_URL})**. "
        "Open the Briefing for this week, Claims for what to act on, Topics to browse by "
        "domain. Click any title for the full writeup with its sources; every view and "
        "finding has a link you can share.",
        "",
    ]


def _readme_tail(now: str) -> list[str]:
    big = " · ".join(f"[{label}]({site_link(view)})" for label, view in SITE_VIEWS)
    trees = " · ".join(f"[{meta['name']}]({t}/README.md)" for t, meta in c.TOPICS.items())
    return [
        "## Explore",
        "",
        f"### {big}",
        "",
        f"On GitHub: {trees} · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · "
        "[Trends](TRENDS.md) · [Review queue](REVIEW.md)",
        "",
        "## Contribute",
        "",
        f"- **Suggest a source:** [open an issue]({ISSUES_URL}) with the feed or account URL. "
        "Sources join the ranked registry through a reviewed PR "
        "(`python scripts/add_source.py`).",
        f"- **Challenge a claim:** [open an issue]({ISSUES_URL}) with the evidence that "
        "refines or refutes it.",
        "- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · "
        "[AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).",
        "",
        "Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.",
        "",
        f"<sub>Last updated {now} by <code>scripts/generate_site.py</code> from the pools in "
        "<code>data/</code>. Generated - do not hand-edit.</sub>",
        "",
    ]


def render_readme(payload: dict, now: str) -> str:
    """The short README: pitch, this week's picks, links into the site."""
    return "\n".join(_readme_head(payload, now) + _teaser(payload) + _readme_tail(now))


def one_entry_per_story(entries: list[dict], conf: c.Config) -> list[dict]:
    """The best-composite entry of each story (story_ledger.py), so a story is
    listed once however many outlets covered it."""
    _, index = sl.render_context()
    best: dict[str, dict] = {}
    for entry in sorted(entries, key=lambda e: -c.entry_composite(e, conf)):
        eid = entry.get("id") or ""
        best.setdefault(index.get(eid) or f"e-{eid}", entry)
    return list(best.values())


def main() -> int:
    conf = c.load_config()
    now = c.utcnow().strftime("%Y-%m-%d")
    all_entries: list[dict] = []
    for topic in c.TOPICS:
        all_entries += write_topic(topic, conf, now)
    payload = gh.build_payload(cl.load_ledger(), conf, now)
    readme = render_readme(payload, now)
    (c.ROOT / "README.md").write_text(_dedash(readme), encoding="utf-8")
    print(f"Rendered README.md + {'/ '.join(c.TOPICS)}/ ({len(all_entries)} vetted findings).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
