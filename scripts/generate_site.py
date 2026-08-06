#!/usr/bin/env python3
"""
generate_site.py - Render the two knowledge directories from the pools.

Reads data/security.json + data/ai.json and writes:
  - README.md               landing page (what this is + global Top-10 learnings)
  - security/README.md      ranked Security-track index
  - ai/README.md            ranked AI-track index
  - <track>/<domain>/<YYYY-MM>-<slug>.md   one citation-first page per finding

Ranking uses each entry's composite score (rerank.py fills these); entries with
no scores yet are ranked by a live-computed newness so legacy items still sort.
Do not hand-edit generated files - edit the pools and regenerate.

Usage:
    python scripts/generate_site.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import UTC, datetime

import common as c

import claims as cl

TOP_N_LANDING = 10


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
        f"**Scores:** 🆕 Newness {scores['newness']} · ✨ Novelty {scores['novelty']} · "
        f"🎯 Relevance {scores['relevance']} · 🏛️ Credibility {round(scores.get('credibility', 50))} · "
        f"**Composite {scores['composite']}**"
    )


def _entry_meta(entry: dict, scores: dict) -> list[str]:
    src = entry.get("source_url", "")
    topic_name = c.TOPICS.get(entry.get("topic", ""), {}).get("name", entry.get("topic", ""))
    meta = [
        f"**Topic:** {topic_name}  ·  **Domain:** {entry.get('domain', '-')}",
        f"**Source:** [{entry.get('source_name', 'source')}]({src})"
        + (f"  ·  **Author:** {entry['author']}" if entry.get("author") else "")
        + f"  ·  **Published:** {fmt_published(entry)}"
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
    grounded = les.get("grounded")
    if grounded is True:
        return " ✅"
    if grounded is False:
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
        "  \n".join(_entry_meta(entry, entry_scores(entry, conf))),
        "",
    ]
    if entry.get("takeaway"):
        out += [f"> **Takeaway:** {entry['takeaway']}", ""]
    if entry.get("summary"):
        out += [
            "## TL;DR",
            "",
            "_The gist, not every detail - read the [full source](#) for the complete write-up._".replace(
                "(#)", f"({entry.get('source_url', '')})"
            ),
            "",
            entry["summary"].strip(),
            "",
        ]
    out += _entry_lessons_md(entry)
    out += _entry_tcm_md(entry)
    out += ["---", "", f"_Source: [{src}]({src})_  ·  [← back to index](../README.md)", ""]
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
        f"latest {conf.max_age_days} days only{held_note}._",
        "",
    ]
    out += _editorial_section(list(editorial))
    out += ["| Domain | Findings |", "| --- | --- |"]
    order = sorted(by_domain, key=lambda d: -len(by_domain[d]))
    out += [f"| {d} | {len(by_domain[d])} |" for d in order] + [""]
    for domain in order:
        out += (
            [f"## {domain}", ""]
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
    base.mkdir(parents=True, exist_ok=True)
    held = len(all_entries) - len(curated) - len(editorial)
    md = _topic_index_md(topic, by_domain, curated, held, conf, now, editorial)
    (base / "README.md").write_text(_dedash(md), encoding="utf-8")
    return curated


TOPIC_EMOJI = {"ai-security": "🤖🛡️", "product-security": "🛡️", "ai-research": "🧠"}


def _week_snapshot(curated_entries: list[dict], conf: c.Config) -> list[str]:
    """This week's snapshot: curated findings published in the last snapshot_days,
    each linking to both its writeup page and the original source article."""
    fresh = [e for e in curated_entries if c.is_fresh(e, conf.snapshot_days)]
    ranked = rank(fresh, conf)[:TOP_N_LANDING]
    out = [
        "## This week's snapshot",
        "",
        f"> The top curated findings published in the last {conf.snapshot_days} days. Each entry is "
        "the gist (what's new, why it matters, what to do), and links to both its writeup here "
        "**and** the original source. For the full digest see the [newsletter](NEWSLETTER.md).",
        "",
    ]
    if not ranked:
        return out + [
            "_No new curated findings this week. Browse the databases below or the "
            "[latest newsletter](NEWSLETTER.md)._",
            "",
        ]
    for e in ranked:
        s = entry_scores(e, conf)
        take = e.get("takeaway") or e.get("summary") or e.get("threat") or ""
        tname = c.TOPICS.get(e.get("topic", ""), {}).get("name", e.get("topic", ""))
        out.append(
            f"- **[{e.get('title', '')}]({e['topic']}/{entry_relpath(e)})** · {tname} · "
            f"{fmt_published(e)} · composite **{s['composite']}** · "
            f"[source ↗]({e.get('source_url', '')})  \n  {c.clean_summary(take, 180)}"
        )
    return out + [""]


def _claims_index() -> list[str]:
    """Surface the claim ledger on the landing page: how many answers stand per
    topic, how many were retired, and the most recent thing the field changed."""
    ledger = cl.load_ledger()
    every = cl.all_claims(ledger)
    if not every:
        return []
    retired = [claim for claim in every if cl.is_retired(claim)]
    lines = [
        "## Standing claims",
        "",
        "> The databases below track **what was published**. The ledger tracks **what we "
        f"currently believe**: {len(every) - len(retired)} standing answers, each with the "
        f"evidence behind it, plus {len(retired)} retired ones kept underneath with the date "
        "and reason they stopped being true. See the [full ledger](claims/README.md).",
        "",
    ]
    for topic, meta in c.TOPICS.items():
        topic_claims = cl.claims_for_topic(ledger, topic)
        live = sum(1 for claim in topic_claims if cl.is_live(claim))
        lines.append(
            f"- **[{meta['name']}](claims/{topic}.md)** - "
            f"{live} standing · {len(topic_claims) - live} retired"
        )
    latest = sorted(retired, key=lambda claim: claim.get("superseded_on") or "", reverse=True)
    if latest:
        top = latest[0]
        lines += [
            "",
            f"**Most recent reversal** ({top.get('superseded_on')}): ~~{top['statement']}~~  ",
            f"↳ {top.get('supersession_reason', '')}",
        ]
    return lines + [""]


def _databases_index(counts: dict[str, int]) -> list[str]:
    lines = ["## The three databases", ""]
    for t, meta in c.TOPICS.items():
        lines.append(
            f"- **[{meta['name']}]({t}/README.md)** "
            f"({counts[t]} vetted findings). {meta['blurb']}"
        )
    lines += [
        "",
        "Also generated every run: [Newsletter](NEWSLETTER.md) (full digest) · "
        "[Trends](TRENDS.md) (emerging themes) · [Review queue](REVIEW.md) "
        "(not-yet-vetted).",
        "",
    ]
    return lines


def _how_it_works(conf: c.Config) -> list[str]:
    return [
        "## How it works",
        "",
        "```",
        "X / GitHub / YouTube / LinkedIn / articles / RSS   (ranked source registry)",
        "  └─ ingest + Jina Reader (clean text)      → data/candidates.json",
        "     └─ analyze  (extract teachable lessons · score newness/novelty/relevance)",
        "        └─ curate (vetted-only gate) → merge into the 3 topic pools → re-rank",
        "           ├─ reconcile against data/claims.json  (new claim? supersedes an old one?)",
        "           └─ render  README · topic pages · claims · newsletter · trends · review · skills",
        "```",
        "",
        "- **Latest only.** Findings older than about "
        f"{conf.max_age_days} days age out to [`data/archive.json`](data/archive.json); the "
        f"snapshot at the top is the last {conf.snapshot_days} days.",
        "- **Vetted only.** A finding is shown only if it clears the novelty and relevance floor "
        "and passes verification; the rest wait in [REVIEW.md](REVIEW.md). Nothing is deleted.",
        "- **Ranked sources.** Approved sources live in a registry and self-rank by how often they "
        "yield curated findings (tier, reach, and hit-rate).",
        "- **Emerging trends.** Tagged findings are clustered over time to surface waves early "
        "([TRENDS.md](TRENDS.md)).",
        "",
    ]


def _honesty(conf: c.Config) -> list[str]:
    return [
        "## How the data is produced, and its limits",
        "",
        "Being upfront, because a research tracker lives or dies on trust:",
        "",
        "- **What runs where.** Ingestion and the LLM analysis run locally (the `/research-scan` "
        "and `/add-resource` skills, plus an X account for social sources). The GitHub Actions job "
        "only re-ranks the committed pools and regenerates the rendered files. In practice the "
        "repo is refreshed weekly by the maintainer; it is not reproducible from a clean clone "
        "without the local pipeline and credentials.",
        f"- **Windows.** All three finding tracks share one rolling window of about "
        f"{conf.max_age_days} days (the this-week snapshot is the last {conf.snapshot_days}); older "
        "findings move to [`data/archive.json`](data/archive.json). The claim ledger is durable and "
        "never ages out, so it reaches back years. Findings tell you what was published lately; "
        "claims tell you what to believe now.",
        "- **What \"vetted\" and \"checked\" mean.** A finding is curated only if it clears the "
        "novelty and relevance bars, its lesson excerpt is found in the source text (grounding), "
        "and a separate model pass does not refute it. That is automated review with a mechanical "
        "grounding check, not human verification. Treat it as a strong filter, not a guarantee.",
        "- **Source caveat.** Social ingestion leans on an X account and is inherently fragile; "
        "when it stalls, the RSS, GitHub, arXiv, and advisory feeds keep the pipeline running.",
        "",
    ]


def _how_to_use() -> list[str]:
    return [
        "## How to use this repo",
        "",
        "| I want to… | Do this |",
        "| --- | --- |",
        "| Read the latest, curated | Skim the snapshot above → open a topic database or "
        "[the newsletter](NEWSLETTER.md) |",
        "| Know what to actually DO right now | Open the [claim ledger](claims/README.md) - "
        "current answers on top, retired ones underneath with why they fell |",
        "| Record a new standing answer | `python scripts/add_claim.py new <id> --topic … "
        '--statement … --evidence "supports|<url>|<title>|<date>"` |',
        "| Retire an answer the field moved past | `python scripts/add_claim.py supersede "
        '<old-id> <new-id> --reason "…"` (add `--refuted` if it was simply wrong) |',
        "| Track a new source | `python scripts/add_source.py <type> <handle> --topics …` "
        "(or the `/add-source` skill) - X user, blog, newsletter, GitHub user/query, YouTube |",
        "| Capture one article now | `python scripts/add.py <url>` then the `/add-resource` skill "
        "- returns summary + takeaway + action and files it |",
        "| Run a full scan | the `/research-scan` skill (self-pace with `/loop 12h /research-scan`) |",
        "| Run it daily on autopilot | `powershell -File scripts/install_daily_scan.ps1` - a Scheduled "
        "Task ingests, runs Claude headless to analyze+verify, and opens a PR each day (never "
        "auto-merges). Remove with `-Uninstall`. |",
        "| Regenerate the site | `rerank.py` → `generate_site.py` → `generate_claims.py` → "
        "`trends.py` → `generate_newsletter.py` → `generate_review.py` |",
        "",
        "**Setup** (Agent Reach + burner X account in WSL2, one-time): see "
        "[PUBLISH.md](PUBLISH.md). **Contributing / how findings are structured:** "
        "[CONTRIBUTING.md](CONTRIBUTING.md). **Automation & dev workflow:** [AGENTS.md](AGENTS.md).",
        "",
        "## Repo layout",
        "",
        "```",
        "data/{ai-security,product-security,ai-research}.json  the 3 rolling pools (source of truth)",
        "data/claims.json                                      the claim ledger (durable, never ages out)",
        "data/archive.json · data/sources.json                 aged-out findings · ranked sources",
        "scripts/                                               ingest · analyze-merge · rank · render",
        ".claude/skills/                                        /research-scan /add-resource /add-source",
        "ai-security/ product-security/ ai-research/            rendered per-topic pages (generated)",
        "claims/                                                rendered claim ledger (generated)",
        "README.md NEWSLETTER.md TRENDS.md REVIEW.md              generated - do not hand-edit",
        "```",
        "",
    ]


def render_readme(curated_entries: list[dict], conf: c.Config, now: str) -> str:
    counts = {
        t: sum(1 for e in c.load_pool(t)["entries"] if c.is_curated(e, conf)) for t in c.TOPICS
    }
    total = sum(counts.values())
    out = [
        "# Awesome Security & AI Research",
        "",
        '<p align="center">'
        '<a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/">'
        '<img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited '
        'briefing" width="820"></a></p>',
        "",
        "> **A weekly, source-cited briefing on AI security, product security, and applied AI "
        "research.** Every week it scans a ranked set of sources (X, GitHub, YouTube, blogs, "
        "newsletters, RSS), keeps only the findings that teach something you can act on, and files "
        "each one under **AI Security**, **Product Security**, or **AI Research** with a one-line "
        "lesson and a concrete next step.",
        "",
        f"![Updated](https://img.shields.io/badge/updated-{now.replace('-', '--')}-1f6feb) "
        f"![Vetted findings](https://img.shields.io/badge/vetted-{total}-2da44e) "
        f"![Window](https://img.shields.io/badge/findings_window-last_{conf.max_age_days}_days-bf8700) "
        "![Cadence](https://img.shields.io/badge/refreshed-weekly-6f42c1) "
        "![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)",
        "",
        "<h3 align=\"center\">"
        "<a href=\"https://rcha0s.github.io/AwesomeSecurity-AIResearch/\">Read this week's briefing "
        "&#8594;</a></h3>",
        "",
        "The live site opens on this week's briefing (the lead finding, what's trending, what's "
        "most novel, and the strongest research in each field), then lets you browse every "
        "subfield, filter the claim ledger, and search the full feed. The markdown below is the "
        "same data, readable on GitHub.",
        "",
        "### What makes it different",
        "",
        "- **Findings age out; claims don't.** A finding is one article, good for about a month. A "
        "**claim** is a durable answer to a recurring question (\"which serialization should agents "
        "use?\"). The [claim ledger](claims/README.md) keeps the current answer on top and every "
        "answer it replaced underneath, with the date and reason it was retired, so you can see "
        "what the field stopped believing and why.",
        "- **One lesson, one action.** Nothing here is a link dump. Each finding is distilled to "
        "the transferable lesson and the concrete thing to do about it.",
        "- **Vetted, not scraped.** A finding is shown only after it clears a novelty and relevance "
        "bar, its lesson excerpt is grounded against the source text, and a separate model pass "
        "cross-checks the claim. This is automated review, not human review; everything that fails "
        "waits in the [review queue](REVIEW.md), and nothing is deleted.",
        "- **Every claim cites its sources.** No anonymous assertions; follow the evidence yourself.",
        "",
    ]
    out += _week_snapshot(curated_entries, conf)
    out += _claims_index()
    out += _databases_index(counts)
    out += _how_it_works(conf)
    out += _honesty(conf)
    out += _how_to_use()
    out += [
        "## License",
        "",
        "Curated content under [CC BY 4.0](LICENSE); scripts under MIT. Linked research remains "
        "the property of its original authors - every finding cites its original source.",
        "",
        f"<sub>Generated by <code>scripts/generate_site.py</code> on {now}. "
        "Edit the pools in <code>data/</code> and regenerate - do not hand-edit rendered files.</sub>",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    conf = c.load_config()
    now = datetime.now(UTC).strftime("%Y-%m-%d")
    all_entries: list[dict] = []
    for topic in c.TOPICS:
        all_entries += write_topic(topic, conf, now)
    (c.ROOT / "README.md").write_text(
        _dedash(render_readme(all_entries, conf, now)), encoding="utf-8"
    )
    print(f"Rendered README.md + {'/ '.join(c.TOPICS)}/ ({len(all_entries)} vetted findings).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
