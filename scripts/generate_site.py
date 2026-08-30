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


def _entry_top_meta(entry: dict) -> str:
    """The one line worth seeing before deciding to read: when this ran."""
    return f"**Published:** {fmt_published(entry)}"


def _entry_meta(entry: dict, scores: dict) -> list[str]:
    src = entry.get("source_url", "")
    topic_name = c.TOPICS.get(entry.get("topic", ""), {}).get("name", entry.get("topic", ""))
    meta = [
        f"**Topic:** {topic_name}  ·  **Domain:** {entry.get('domain', '-')}",
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
    """Landing-view snapshot: prefers the last snapshot_days, but if no
    finding is that fresh (e.g. the ingest pipeline hasn't run recently),
    falls back to the newest N regardless of window. An empty landing page
    kills trust; showing 'the most recent things I have' is more honest
    than 'nothing here.'"""
    fresh = [e for e in curated_entries if c.is_fresh(e, conf.snapshot_days)]
    ranked = rank(fresh, conf)[:TOP_N_LANDING]
    fallback = False
    if not ranked:
        ranked = rank(list(curated_entries), conf)[:TOP_N_LANDING]
        fallback = True

    if fallback:
        header = (
            f"> The most recent curated findings we have (nothing new this "
            f"{conf.snapshot_days}-day window). Each links to its writeup here **and** "
            "the original source. For the full digest see the [newsletter](NEWSLETTER.md)."
        )
    else:
        header = (
            f"> The top curated findings published in the last {conf.snapshot_days} days. "
            "Each links to its writeup here **and** the original source. For the full "
            "digest see the [newsletter](NEWSLETTER.md)."
        )

    out = [
        "## Latest findings",
        "",
        header,
        "",
    ]
    if not ranked:
        return out + [
            "_The pool is currently empty. Browse the [latest newsletter](NEWSLETTER.md) "
            "or the [review queue](REVIEW.md)._",
            "",
        ]
    for e in ranked[:5]:  # 5 keeps the landing view scannable — full list on the live site
        take = e.get("takeaway") or e.get("summary") or e.get("threat") or ""
        tname = c.TOPICS.get(e.get("topic", ""), {}).get("name", e.get("topic", ""))
        out.append(
            f"- **[{e.get('title', '')}]({e['topic']}/{entry_relpath(e)})** · "
            f"_{tname} · {fmt_published(e)}_  \n"
            f"  {c.clean_summary(take, 180)}"
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


def render_readme(curated_entries: list[dict], conf: c.Config, now: str) -> str:
    """Reader-first README.

    Old layout led with three sections of methodology prose before any
    reader saw a single finding — good for credibility, terrible for
    first-impression usability. This shape reverses it: a reader lands
    on the pitch, immediately sees what's in the repo (findings, claims,
    databases), and can drill into methodology if they care.

    The methodology / honesty content is preserved verbatim, just moved
    inside a collapsible <details> block so it doesn't push the actual
    content below the fold."""
    counts = {
        t: sum(1 for e in c.load_pool(t)["entries"] if c.is_curated(e, conf)) for t in c.TOPICS
    }
    total = sum(counts.values())

    # --- Header + pitch --------------------------------------------------
    out = [
        "# Awesome Security & AI Research",
        "",
        '<p align="center">'
        '<a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/">'
        '<img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited '
        'briefing" width="820"></a></p>',
        "",
        "> **A weekly, source-cited briefing on AI security, product security, and applied "
        "AI research** — every finding vetted, distilled to one lesson, and filed by field. "
        "A [standing-claims ledger](claims/README.md) tracks what the field currently believes "
        "and what it stopped believing, with the date and reason each answer fell.",
        "",
        f"![Updated](https://img.shields.io/badge/updated-{now.replace('-', '--')}-1f6feb) "
        f"![Vetted findings](https://img.shields.io/badge/vetted-{total}-2da44e) "
        f"![Window](https://img.shields.io/badge/findings_window-last_{conf.max_age_days}_days-bf8700) "
        "![Cadence](https://img.shields.io/badge/refreshed-weekly-6f42c1) "
        "![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)",
        "",
        "<h3 align=\"center\">"
        "<a href=\"https://rcha0s.github.io/AwesomeSecurity-AIResearch/\">"
        "Read the live briefing &#8594;</a></h3>",
        "",
        "The live site is the best read — one page for the week's news, another for "
        "standing claims, a searchable index for every finding. This README mirrors the "
        "same data for readers who prefer GitHub.",
        "",
        "---",
        "",
    ]

    # --- What's in the repo, right now ----------------------------------
    # The reader sees content before they see methodology. If the pool is
    # empty, _week_snapshot falls back to the newest N and says so
    # honestly — a landing view with actual findings, not a hollow
    # "nothing this week" placeholder that erodes trust in the pitch.
    out += _week_snapshot(curated_entries, conf)
    out += _databases_index(counts)
    out += _claims_index()

    # --- Contributing signpost ------------------------------------------
    out += [
        "---",
        "",
        "## Contribute",
        "",
        "The repo grows two ways:",
        "",
        "- **Suggest a source.** The [source-scout agent](.github/workflows/source-scout.yml) "
        "runs daily and proposes new publishers via PR. See a source we're missing? Open an "
        "issue with the feed URL and we'll consider it — or run `python scripts/add_source.py` "
        "if you're set up locally.",
        "- **Flag a bad claim.** The claim ledger is a living record; if you have evidence that "
        "refines or refutes a current claim, open an issue with the source. See "
        "[CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow and the maintainer command "
        "reference.",
        "",
        "Automation and dev workflow: [AGENTS.md](AGENTS.md). Local setup for the scan "
        "pipeline: [PUBLISH.md](PUBLISH.md).",
        "",
    ]

    # --- Methodology (collapsed by default) -----------------------------
    # Everything that follows is credibility content — argued once for
    # readers who care, folded behind a <details> so it doesn't push the
    # actual findings below the fold.
    out += _methodology_details(conf)

    # --- License --------------------------------------------------------
    out += [
        "## License",
        "",
        "Curated content under [CC BY 4.0](LICENSE); scripts under MIT. Linked research "
        "remains the property of its original authors — every finding cites its source.",
        "",
        f"<sub>Generated by <code>scripts/generate_site.py</code> on {now}. "
        "Edit the pools in <code>data/</code> and regenerate — do not hand-edit rendered "
        "files.</sub>",
        "",
    ]
    return "\n".join(out)


def _methodology_details(conf: c.Config) -> list[str]:
    """The full pitch, methodology, and honesty content wrapped in a
    <details> block so GitHub renders it as a click-to-expand section.
    Not hidden — one click reveals the whole argument for anyone who
    wants to know how the data is produced."""
    return [
        "<details>",
        "<summary><strong>How this is built</strong> "
        "(methodology, source pipeline, and the limits of automated review — click to expand)"
        "</summary>",
        "",
        "### Why this exists",
        "",
        "Security + AI is producing more research than any practitioner can read. "
        "Aggregator sites solve the *coverage* problem — they list every paper — and leave "
        "you the *judgment* problem: which claims are load-bearing, which have been quietly "
        "refuted, which are new work vs. a restatement of prior art. A newsletter, an "
        "awesome-list, or a Twitter feed can tell you what was published this week. None of "
        "them can tell you **what the field currently believes and what it stopped believing**.",
        "",
        "This repo tries. Every finding is one article distilled to a transferable lesson; "
        "every lesson maps to a durable **claim** in the ledger; claims retire when better "
        "evidence arrives, and the old claim stays visible with the date and reason it fell. "
        "You get both surfaces: the week's news, and a living record of what to actually "
        "believe.",
        "",
        "### Methodology",
        "",
        "Each choice is a response to a specific failure mode we've seen in the "
        "security-research firehose:",
        "",
        "- **Two tracks, one gate each.** *Research* (papers, harness design, capability "
        "shifts) passes a novelty + grounding gate: the lesson excerpt must be found "
        "verbatim in the source, and a separate model pass must not refute the claim. *News* "
        "(capability announcements, spec changes, incident disclosures) passes a trust + "
        "scope gate: fresh, from a first-party or high-trust source, and on-topic per a "
        "shared classifier with a hard deny list for stock/consumer/business puff. Novelty "
        "is the wrong rubric for a Kimi K3 release note — trust is.",
        "- **Grounded excerpts, not paraphrased summaries.** Every claim in a research "
        "finding cites a literal quote from the source; the pipeline re-verifies the quote "
        "against the fetched article at build time. An excerpt that doesn't match kicks the "
        "finding into [REVIEW.md](REVIEW.md) instead of publishing it as fact. Follows the "
        "same discipline as evidence-based systematic reviews (Cochrane, PRISMA): the quote "
        "is the audit trail.",
        "- **Adversarial verification pass.** After the first analysis, a fresh subagent "
        "gets only the raw source and the extracted claims — no scores, no prior context — "
        "and tries to refute. Novelty is re-scored as *claim-level delta vs. named prior "
        "art*, not text similarity. The **lower** of the two novelty scores wins. This "
        "mirrors the \"adversarial collaboration\" pattern from meta-science (Mellers, "
        "Tetlock 2019) — a single scorer overrates their own work; two independent scorers, "
        "one incentivized to refute, produce calibrated estimates.",
        "- **Story-key dedup across the news lane.** Same story on three sites (vendor blog, "
        "HN thread, HuggingFace mirror) collapses to one row with the others as "
        "corroborators. Story key is *canonical URL + title trigrams + entity set*, "
        "two-of-three collision rule, 30-day lookback across every pool. Prevents the "
        "newsletter effect where the same claim shows up three times because three outlets "
        "covered it.",
        "- **Claim supersession is a first-class relation, not a delete.** When new evidence "
        "retires an old answer, both the old and new claim persist. The retired one carries "
        "`superseded_by`, `superseded_on`, and `supersession_reason`; the new one carries "
        "`supersedes`. The renderer pushes retired claims to the bottom of the page with "
        "their reason visible. This is the shape a "
        "[Popper-style falsificationist record](https://plato.stanford.edu/entries/popper/#Fal) "
        "has always wanted; git history is not enough because it doesn't render.",
        "- **Ranked, self-adjusting source registry.** Every source has a manual authority "
        "tier, a log-scaled reach signal (followers/stars), and a Bayesian-smoothed "
        "hit-rate (curated/ingested over the source's lifetime). A source that trended once "
        "but never yields curated findings *drops* in ranking; a quiet source with "
        "consistently-vetted work rises. Prevents the awesome-list rot problem where every "
        "source is equal forever.",
        "- **A source-scout agent proposes new sources; a human approves.** A daily job "
        "discovers publishers via HN top-of-window trending, qualifies them by back-catalog "
        "classifier hit-rate (≥40% on-topic over the last 25 items), and opens a PR against "
        "main. The human merges or closes; closing can add the domain to a durable "
        "blocklist that prevents re-proposal. No auto-apply. See "
        "[.github/workflows/source-scout.yml](.github/workflows/source-scout.yml).",
        "",
        "### What we deliberately don't do",
        "",
        "- **We don't score \"quality\" holistically.** Every axis (newness, novelty, "
        "relevance, credibility) is scored separately with a written rubric. An LLM asked "
        "\"how good is this paper\" is systematically biased toward long, elaborate output "
        "([Zheng et al., 2023](https://arxiv.org/abs/2306.05685) — LLM-as-judge prefers "
        "longer answers independent of quality); we don't ask.",
        "- **We don't dedupe by URL alone.** URL dedup misses same-story-different-URL, "
        "which is where a news feed spams you. Title-trigram + entity-set matching catches "
        "those; the trade-off is a slightly more complex collision test.",
        "- **We don't do sentiment or engagement scoring.** A story with 1000 HN upvotes "
        "isn't automatically more relevant to defenders than one with 40. Engagement gates "
        "ingestion (velocity signal), never curation.",
        "- **We don't paraphrase what wasn't said.** If a source doesn't state a lesson "
        "directly, the finding gets `lessons: []` and lives on its takeaway alone. News "
        "items normally ship this way — the event is the point.",
        "",
        "### How the data flows",
        "",
        "```",
        "X / GitHub / YouTube / articles / RSS   (ranked source registry)",
        "  └─ ingest + Jina Reader (clean text)      → data/candidates.json",
        "     └─ analyze  (extract teachable lessons · score newness/novelty/relevance)",
        "        └─ curate (vetted-only gate) → merge into the 3 topic pools → re-rank",
        "           ├─ reconcile against data/claims.json  (new claim? supersedes an old one?)",
        "           └─ render  README · topic pages · claims · newsletter · trends · review",
        "```",
        "",
        f"- **Latest only.** Findings older than {conf.max_age_days} days age out to "
        "[`data/archive.json`](data/archive.json); the snapshot at the top is the last "
        f"{conf.snapshot_days} days when we have fresh material, otherwise the most recent "
        "we have.",
        "- **Vetted only.** Everything that fails the gate waits in [REVIEW.md](REVIEW.md). "
        "Nothing is deleted.",
        "- **Emerging trends.** Tagged findings are clustered over time to surface waves "
        "early ([TRENDS.md](TRENDS.md)).",
        "",
        "### Honest limits",
        "",
        "A research tracker lives or dies on trust, so — being upfront:",
        "",
        "- **What runs where.** Ingestion and the LLM analysis run locally (the "
        "`/research-scan` and `/add-resource` skills, plus an X account for social "
        "sources). The GitHub Actions job only re-ranks the committed pools and regenerates "
        "the rendered files. In practice the repo is refreshed weekly by the maintainer; it "
        "is not reproducible from a clean clone without the local pipeline and credentials.",
        f"- **Windows.** All three finding tracks share one rolling window of "
        f"{conf.max_age_days} days (the snapshot is the last {conf.snapshot_days}); older "
        "findings move to [`data/archive.json`](data/archive.json). The claim ledger is "
        "durable and never ages out. Findings tell you what was published lately; claims "
        "tell you what to believe now.",
        "- **What \"vetted\" and \"checked\" mean.** A finding is curated only if it clears "
        "the novelty and relevance bars, its lesson excerpt is found in the source text "
        "(grounding), and a separate model pass does not refute it. That is automated "
        "review with a mechanical grounding check, not human verification. Treat it as a "
        "strong filter, not a guarantee.",
        "- **Source caveat.** Social ingestion leans on an X account and is inherently "
        "fragile; when it stalls, the RSS, GitHub, arXiv, and advisory feeds keep the "
        "pipeline running.",
        "",
        "### Repo layout",
        "",
        "```",
        "data/{ai-security,product-security,ai-research}.json  the 3 rolling pools (source of truth)",
        "data/claims.json                                      the claim ledger (durable, never ages out)",
        "data/archive.json · data/sources.json                 aged-out findings · ranked sources",
        "scripts/                                               ingest · analyze-merge · rank · render",
        ".claude/skills/                                        /research-scan /add-resource /add-source",
        "ai-security/ product-security/ ai-research/            rendered per-topic pages (generated)",
        "claims/                                                rendered claim ledger (generated)",
        "README.md NEWSLETTER.md TRENDS.md REVIEW.md            generated — do not hand-edit",
        "```",
        "",
        "</details>",
        "",
    ]


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
