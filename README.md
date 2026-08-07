# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="820"></a></p>

> **A weekly, source-cited briefing on AI security, product security, and applied AI research.** Every week it scans a ranked set of sources (X, GitHub, YouTube, blogs, newsletters, RSS), keeps only the findings that teach something you can act on, and files each one under **AI Security**, **Product Security**, or **AI Research** with a one-line lesson and a concrete next step.

![Updated](https://img.shields.io/badge/updated-2026--08--07-1f6feb) ![Vetted findings](https://img.shields.io/badge/vetted-15-2da44e) ![Window](https://img.shields.io/badge/findings_window-last_31_days-bf8700) ![Cadence](https://img.shields.io/badge/refreshed-weekly-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

<h3 align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/">Read this week's briefing &#8594;</a></h3>

The live site opens on this week's briefing (the lead finding, what's trending, what's most novel, and the strongest research in each field), then lets you browse every subfield, filter the claim ledger, and search the full feed. The markdown below is the same data, readable on GitHub.

## Why this exists

Security + AI is producing more research than any practitioner can read. Aggregator sites solve the *coverage* problem - they list every paper - and leave you the *judgment* problem: which claims are load-bearing, which have been quietly refuted, which are new work vs. a restatement of prior art. A newsletter, an awesome-list, or a Twitter feed can tell you what was published this week. None of them can tell you **what the field currently believes and what it stopped believing**.

This repo tries. Every finding is one article distilled to a transferable lesson; every lesson maps to a durable **claim** in the [ledger](claims/README.md); claims retire when better evidence arrives, and the old claim stays visible with the date and reason it fell. You get both surfaces: the week's news, and a living record of what to actually believe.

## Methodology

The design here is opinionated. Each choice is a response to a specific failure mode we've seen in the security-research firehose:

- **Two tracks, one gate each.** *Research* (paper of the week, harness design, capability shifts) passes a novelty + grounding gate: the lesson excerpt must be found verbatim in the source, and a separate model pass must not refute the claim. *News* (capability announcements, spec changes, incident disclosures) passes a trust + scope gate: fresh, from a first-party or high-trust source, and on-topic per a shared classifier with a hard deny list for stock/consumer/business puff. Novelty is the wrong rubric for a Kimi K3 release note - trust is.
- **Grounded excerpts, not paraphrased summaries.** Every claim in a research finding cites a literal quote from the source; the pipeline re-verifies the quote against the fetched article at build time. An excerpt that doesn't match kicks the finding into [REVIEW.md](REVIEW.md) instead of publishing it as fact. Follows the same discipline as evidence-based systematic reviews (Cochrane, PRISMA): the quote is the audit trail.
- **Adversarial verification pass.** After the first analysis, a fresh subagent gets only the raw source and the extracted claims - no scores, no prior context - and tries to refute. Novelty is re-scored as *claim-level delta vs. named prior art*, not text similarity. The **lower** of the two novelty scores wins. This mirrors the "adversarial collaboration" pattern from meta-science (Mellers, Tetlock 2019) - a single scorer overrates their own work; two independent scorers, one incentivized to refute, produce calibrated estimates.
- **Story-key dedup across the news lane.** Same story on three sites (vendor blog, HN thread, HuggingFace mirror) collapses to one row with the others as corroborators. Story key is *canonical URL + title trigrams + entity set*, two-of-three collision rule, 30-day lookback across every pool. Prevents the newsletter effect where the same claim shows up three times because three outlets covered it.
- **Claim supersession is a first-class relation, not a delete.** When new evidence retires an old answer, both the old and new claim persist. The retired one carries `superseded_by`, `superseded_on`, and `supersession_reason`; the new one carries `supersedes`. The renderer pushes retired claims to the bottom of the page with their reason visible. This is the shape a [Karl Popper-style falsificationist record](https://plato.stanford.edu/entries/popper/#Fal) has always wanted; git history is not enough because it doesn't render.
- **Ranked, self-adjusting source registry.** Every source has a manual authority tier ("we trust arXiv cs.CR more than Reddit"), a log-scaled reach signal (followers/stars), and a Bayesian-smoothed hit-rate (curated/ingested over the source's lifetime). A source that trended once but never yields curated findings *drops* in ranking; a quiet source with consistently-vetted work rises. Prevents the awesome-list rot problem where every source is equal forever.
- **A source-scout agent proposes new sources; a human approves.** A daily job discovers publishers via HN top-of-window trending, qualifies them by back-catalog classifier hit-rate (≥40% on-topic over the last 25 items), and opens a PR against main. The human merges or closes; closing can add the domain to a durable blocklist that prevents re-proposal. No auto-apply. See [.github/workflows/source-scout.yml](.github/workflows/source-scout.yml).

### What we deliberately don't do

- **We don't score "quality" holistically.** Every axis (newness, novelty, relevance, credibility) is scored separately with a written rubric. An LLM asked "how good is this paper" is systematically biased toward long, elaborate output ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685) - LLM-as-judge prefers longer answers independent of quality); we don't ask.
- **We don't dedupe by URL alone.** URL dedup misses same-story-different-URL, which is where a news feed spams you. Title-trigram + entity-set matching catches those; the trade-off is a slightly more complex collision test.
- **We don't do sentiment or engagement scoring.** A story with 1000 HN upvotes isn't automatically more relevant to defenders than one with 40. Engagement gates ingestion (velocity signal), never curation.
- **We don't paraphrase what wasn't said.** If a source doesn't state a lesson directly, the finding gets `lessons: []` and lives on its takeaway alone. News items normally ship this way - the event is the point.

### What makes it different, in one screen

- **Findings age out; claims don't.** A finding is one article, good for ~31 days. A **claim** is a durable answer to a recurring question ("which serialization should agents use?"). The [ledger](claims/README.md) keeps the current answer on top and every retired answer underneath, with the date and reason it fell.
- **One lesson, one takeaway.** Nothing here is a link dump. Each finding is distilled to the transferable lesson.
- **Vetted, not scraped.** Automated review with a mechanical grounding check - treat it as a strong filter, not a guarantee.
- **Every claim cites its sources.** No anonymous assertions.

## This week's snapshot

> The top curated findings published in the last 7 days. Each entry is the gist (what's new, why it matters, what to do), and links to both its writeup here **and** the original source. For the full digest see the [newsletter](NEWSLETTER.md).

_No new curated findings this week. Browse the databases below or the [latest newsletter](NEWSLETTER.md)._

## Standing claims

> The databases below track **what was published**. The ledger tracks **what we currently believe**: 45 standing answers, each with the evidence behind it, plus 7 retired ones kept underneath with the date and reason they stopped being true. See the [full ledger](claims/README.md).

- **[AI Security](claims/ai-security.md)** - 16 standing · 2 retired
- **[Product Security](claims/product-security.md)** - 11 standing · 2 retired
- **[AI Research](claims/ai-research.md)** - 18 standing · 3 retired

**Most recent reversal** (2026-07-20): ~~A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.~~  
↳ Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.

## The three databases

- **[AI Security](ai-security/README.md)** (3 vetted findings). Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.
- **[Product Security](product-security/README.md)** (7 vetted findings). Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).
- **[AI Research](ai-research/README.md)** (5 vetted findings). Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

Also generated every run: [Newsletter](NEWSLETTER.md) (full digest) · [Trends](TRENDS.md) (emerging themes) · [Review queue](REVIEW.md) (not-yet-vetted).

## How it works

```
X / GitHub / YouTube / LinkedIn / articles / RSS   (ranked source registry)
  └─ ingest + Jina Reader (clean text)      → data/candidates.json
     └─ analyze  (extract teachable lessons · score newness/novelty/relevance)
        └─ curate (vetted-only gate) → merge into the 3 topic pools → re-rank
           ├─ reconcile against data/claims.json  (new claim? supersedes an old one?)
           └─ render  README · topic pages · claims · newsletter · trends · review · skills
```

- **Latest only.** Findings older than about 31 days age out to [`data/archive.json`](data/archive.json); the snapshot at the top is the last 7 days.
- **Vetted only.** A finding is shown only if it clears the novelty and relevance floor and passes verification; the rest wait in [REVIEW.md](REVIEW.md). Nothing is deleted.
- **Ranked sources.** Approved sources live in a registry and self-rank by how often they yield curated findings (tier, reach, and hit-rate).
- **Emerging trends.** Tagged findings are clustered over time to surface waves early ([TRENDS.md](TRENDS.md)).

## How the data is produced, and its limits

Being upfront, because a research tracker lives or dies on trust:

- **What runs where.** Ingestion and the LLM analysis run locally (the `/research-scan` and `/add-resource` skills, plus an X account for social sources). The GitHub Actions job only re-ranks the committed pools and regenerates the rendered files. In practice the repo is refreshed weekly by the maintainer; it is not reproducible from a clean clone without the local pipeline and credentials.
- **Windows.** All three finding tracks share one rolling window of about 31 days (the this-week snapshot is the last 7); older findings move to [`data/archive.json`](data/archive.json). The claim ledger is durable and never ages out, so it reaches back years. Findings tell you what was published lately; claims tell you what to believe now.
- **What "vetted" and "checked" mean.** A finding is curated only if it clears the novelty and relevance bars, its lesson excerpt is found in the source text (grounding), and a separate model pass does not refute it. That is automated review with a mechanical grounding check, not human verification. Treat it as a strong filter, not a guarantee.
- **Source caveat.** Social ingestion leans on an X account and is inherently fragile; when it stalls, the RSS, GitHub, arXiv, and advisory feeds keep the pipeline running.

## How to use this repo

| I want to… | Do this |
| --- | --- |
| Read the latest, curated | Skim the snapshot above → open a topic database or [the newsletter](NEWSLETTER.md) |
| Know what to actually DO right now | Open the [claim ledger](claims/README.md) - current answers on top, retired ones underneath with why they fell |
| Record a new standing answer | `python scripts/add_claim.py new <id> --topic … --statement … --evidence "supports|<url>|<title>|<date>"` |
| Retire an answer the field moved past | `python scripts/add_claim.py supersede <old-id> <new-id> --reason "…"` (add `--refuted` if it was simply wrong) |
| Track a new source | `python scripts/add_source.py <type> <handle> --topics …` (or the `/add-source` skill) - X user, blog, newsletter, GitHub user/query, YouTube |
| Capture one article now | `python scripts/add.py <url>` then the `/add-resource` skill - returns summary + takeaway + action and files it |
| Run a full scan | the `/research-scan` skill (self-pace with `/loop 12h /research-scan`) |
| Run it daily on autopilot | `powershell -File scripts/install_daily_scan.ps1` - a Scheduled Task ingests, runs Claude headless to analyze+verify, and opens a PR each day (never auto-merges). Remove with `-Uninstall`. |
| Regenerate the site | `rerank.py` → `generate_site.py` → `generate_claims.py` → `trends.py` → `generate_newsletter.py` → `generate_review.py` |

**Setup** (Agent Reach + burner X account in WSL2, one-time): see [PUBLISH.md](PUBLISH.md). **Contributing / how findings are structured:** [CONTRIBUTING.md](CONTRIBUTING.md). **Automation & dev workflow:** [AGENTS.md](AGENTS.md).

## Repo layout

```
data/{ai-security,product-security,ai-research}.json  the 3 rolling pools (source of truth)
data/claims.json                                      the claim ledger (durable, never ages out)
data/archive.json · data/sources.json                 aged-out findings · ranked sources
scripts/                                               ingest · analyze-merge · rank · render
.claude/skills/                                        /research-scan /add-resource /add-source
ai-security/ product-security/ ai-research/            rendered per-topic pages (generated)
claims/                                                rendered claim ledger (generated)
README.md NEWSLETTER.md TRENDS.md REVIEW.md              generated - do not hand-edit
```

## License

Curated content under [CC BY 4.0](LICENSE); scripts under MIT. Linked research remains the property of its original authors - every finding cites its original source.

<sub>Generated by <code>scripts/generate_site.py</code> on 2026-08-07. Edit the pools in <code>data/</code> and regenerate - do not hand-edit rendered files.</sub>
