# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="820"></a></p>

> **A weekly, source-cited briefing on AI security, product security, and applied AI research** - every finding vetted, distilled to one lesson, and filed by field. A [standing-claims ledger](claims/README.md) tracks what the field currently believes and what it stopped believing, with the date and reason each answer fell.

![Updated](https://img.shields.io/badge/updated-2026--08--29-1f6feb) ![Vetted findings](https://img.shields.io/badge/vetted-55-2da44e) ![Window](https://img.shields.io/badge/findings_window-last_31_days-bf8700) ![Cadence](https://img.shields.io/badge/refreshed-weekly-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

<h3 align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/">Read the live briefing &#8594;</a></h3>

The live site is the best read - one page for the week's news, another for standing claims, a searchable index for every finding. This README mirrors the same data for readers who prefer GitHub.

---

## Latest findings

> The top curated findings published in the last 7 days. Each links to its writeup here **and** the original source. For the full digest see the [newsletter](NEWSLETTER.md).

- **[VMs won't contain cyber-capable agents](product-security/cloud-infrastructure/2026-08-vms-won-t-contain-cyber-capable-agents.md)** · _Product Security · Aug 26, 2026_  
  Treat capable AI agents as an advanced persistent threat: isolate them with hardened microVMs, enforce least privilege, monitor actively, and keep host and hypervisor dependencies…
- **[Breaking Claude Code Opus 5 Auto Mode with indirect prompt injection to code execution](ai-security/prompt-injection-agent-harness/2026-08-breaking-claude-code-opus-5-auto-mode-with-indirect-prompt-i.md)** · _AI Security · Aug 26, 2026_  
  A benign-looking summary request drove a 60-80% code-execution rate against Claude Code Opus 5 Auto Mode, showing classifier 'zero-injection' claims and OS sandboxing are not…
- **[The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](ai-security/prompt-injection-adversarial/2026-08-the-framing-gap-reframed-indirect-prompt-injection-exfiltrat.md)** · _AI Security · Aug 27, 2026_  
  Don't rely on the acting model to recognize injection; constrain where data can go and isolate the capability that can send it.
- **[When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](ai-research/agents-harnesses/2026-08-when-context-gets-root-instruction-privilege-escalation-in-l.md)** · _AI Research · Aug 27, 2026_  
  How a harness assembles context is a privilege boundary; if it can promote untrusted data, model-side instruction hierarchy provides little protection.
- **[What's in a tag name? JavaScript, apparently](product-security/web-security/2026-08-what-s-in-a-tag-name-javascript-apparently.md)** · _Product Security · Aug 25, 2026_  
  Do not rely on WAFs or character blocklists to stop XSS; enforce context-aware output encoding, a strict Content-Security-Policy, and trusted HTML sanitization, since exotic…

## The three databases

- **[AI Security](ai-security/README.md)** (37 vetted findings). Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.
- **[Product Security](product-security/README.md)** (7 vetted findings). Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).
- **[AI Research](ai-research/README.md)** (11 vetted findings). Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

Also generated every run: [Newsletter](NEWSLETTER.md) (full digest) · [Trends](TRENDS.md) (emerging themes) · [Review queue](REVIEW.md) (not-yet-vetted).

## Standing claims

> The databases below track **what was published**. The ledger tracks **what we currently believe**: 46 standing answers, each with the evidence behind it, plus 7 retired ones kept underneath with the date and reason they stopped being true. See the [full ledger](claims/README.md).

- **[AI Security](claims/ai-security.md)** - 17 standing · 2 retired
- **[Product Security](claims/product-security.md)** - 11 standing · 2 retired
- **[AI Research](claims/ai-research.md)** - 18 standing · 3 retired

**Most recent reversal** (2026-07-20): ~~A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.~~  
↳ Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.

---

## Contribute

The repo grows two ways:

- **Suggest a source.** The [source-scout agent](.github/workflows/source-scout.yml) runs daily and proposes new publishers via PR. See a source we're missing? Open an issue with the feed URL and we'll consider it - or run `python scripts/add_source.py` if you're set up locally.
- **Flag a bad claim.** The claim ledger is a living record; if you have evidence that refines or refutes a current claim, open an issue with the source. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow and the maintainer command reference.

Automation and dev workflow: [AGENTS.md](AGENTS.md). Local setup for the scan pipeline: [PUBLISH.md](PUBLISH.md).

<details>
<summary><strong>How this is built</strong> (methodology, source pipeline, and the limits of automated review - click to expand)</summary>

### Why this exists

Security + AI is producing more research than any practitioner can read. Aggregator sites solve the *coverage* problem - they list every paper - and leave you the *judgment* problem: which claims are load-bearing, which have been quietly refuted, which are new work vs. a restatement of prior art. A newsletter, an awesome-list, or a Twitter feed can tell you what was published this week. None of them can tell you **what the field currently believes and what it stopped believing**.

This repo tries. Every finding is one article distilled to a transferable lesson; every lesson maps to a durable **claim** in the ledger; claims retire when better evidence arrives, and the old claim stays visible with the date and reason it fell. You get both surfaces: the week's news, and a living record of what to actually believe.

### Methodology

Each choice is a response to a specific failure mode we've seen in the security-research firehose:

- **Two tracks, one gate each.** *Research* (papers, harness design, capability shifts) passes a novelty + grounding gate: the lesson excerpt must be found verbatim in the source, and a separate model pass must not refute the claim. *News* (capability announcements, spec changes, incident disclosures) passes a trust + scope gate: fresh, from a first-party or high-trust source, and on-topic per a shared classifier with a hard deny list for stock/consumer/business puff. Novelty is the wrong rubric for a Kimi K3 release note - trust is.
- **Grounded excerpts, not paraphrased summaries.** Every claim in a research finding cites a literal quote from the source; the pipeline re-verifies the quote against the fetched article at build time. An excerpt that doesn't match kicks the finding into [REVIEW.md](REVIEW.md) instead of publishing it as fact. Follows the same discipline as evidence-based systematic reviews (Cochrane, PRISMA): the quote is the audit trail.
- **Adversarial verification pass.** After the first analysis, a fresh subagent gets only the raw source and the extracted claims - no scores, no prior context - and tries to refute. Novelty is re-scored as *claim-level delta vs. named prior art*, not text similarity. The **lower** of the two novelty scores wins. This mirrors the "adversarial collaboration" pattern from meta-science (Mellers, Tetlock 2019) - a single scorer overrates their own work; two independent scorers, one incentivized to refute, produce calibrated estimates.
- **Story-key dedup across the news lane.** Same story on three sites (vendor blog, HN thread, HuggingFace mirror) collapses to one row with the others as corroborators. Story key is *canonical URL + title trigrams + entity set*, two-of-three collision rule, 30-day lookback across every pool. Prevents the newsletter effect where the same claim shows up three times because three outlets covered it.
- **Claim supersession is a first-class relation, not a delete.** When new evidence retires an old answer, both the old and new claim persist. The retired one carries `superseded_by`, `superseded_on`, and `supersession_reason`; the new one carries `supersedes`. The renderer pushes retired claims to the bottom of the page with their reason visible. This is the shape a [Popper-style falsificationist record](https://plato.stanford.edu/entries/popper/#Fal) has always wanted; git history is not enough because it doesn't render.
- **Ranked, self-adjusting source registry.** Every source has a manual authority tier, a log-scaled reach signal (followers/stars), and a Bayesian-smoothed hit-rate (curated/ingested over the source's lifetime). A source that trended once but never yields curated findings *drops* in ranking; a quiet source with consistently-vetted work rises. Prevents the awesome-list rot problem where every source is equal forever.
- **A source-scout agent proposes new sources; a human approves.** A daily job discovers publishers via HN top-of-window trending, qualifies them by back-catalog classifier hit-rate (≥40% on-topic over the last 25 items), and opens a PR against main. The human merges or closes; closing can add the domain to a durable blocklist that prevents re-proposal. No auto-apply. See [.github/workflows/source-scout.yml](.github/workflows/source-scout.yml).

### What we deliberately don't do

- **We don't score "quality" holistically.** Every axis (newness, novelty, relevance, credibility) is scored separately with a written rubric. An LLM asked "how good is this paper" is systematically biased toward long, elaborate output ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685) - LLM-as-judge prefers longer answers independent of quality); we don't ask.
- **We don't dedupe by URL alone.** URL dedup misses same-story-different-URL, which is where a news feed spams you. Title-trigram + entity-set matching catches those; the trade-off is a slightly more complex collision test.
- **We don't do sentiment or engagement scoring.** A story with 1000 HN upvotes isn't automatically more relevant to defenders than one with 40. Engagement gates ingestion (velocity signal), never curation.
- **We don't paraphrase what wasn't said.** If a source doesn't state a lesson directly, the finding gets `lessons: []` and lives on its takeaway alone. News items normally ship this way - the event is the point.

### How the data flows

```
X / GitHub / YouTube / articles / RSS   (ranked source registry)
  └─ ingest + Jina Reader (clean text)      → data/candidates.json
     └─ analyze  (extract teachable lessons · score newness/novelty/relevance)
        └─ curate (vetted-only gate) → merge into the 3 topic pools → re-rank
           ├─ reconcile against data/claims.json  (new claim? supersedes an old one?)
           └─ render  README · topic pages · claims · newsletter · trends · review
```

- **Latest only.** Findings older than 31 days age out to [`data/archive.json`](data/archive.json); the snapshot at the top is the last 7 days when we have fresh material, otherwise the most recent we have.
- **Vetted only.** Everything that fails the gate waits in [REVIEW.md](REVIEW.md). Nothing is deleted.
- **Emerging trends.** Tagged findings are clustered over time to surface waves early ([TRENDS.md](TRENDS.md)).

### Honest limits

A research tracker lives or dies on trust, so - being upfront:

- **What runs where.** Ingestion and the LLM analysis run locally (the `/research-scan` and `/add-resource` skills, plus an X account for social sources). The GitHub Actions job only re-ranks the committed pools and regenerates the rendered files. In practice the repo is refreshed weekly by the maintainer; it is not reproducible from a clean clone without the local pipeline and credentials.
- **Windows.** All three finding tracks share one rolling window of 31 days (the snapshot is the last 7); older findings move to [`data/archive.json`](data/archive.json). The claim ledger is durable and never ages out. Findings tell you what was published lately; claims tell you what to believe now.
- **What "vetted" and "checked" mean.** A finding is curated only if it clears the novelty and relevance bars, its lesson excerpt is found in the source text (grounding), and a separate model pass does not refute it. That is automated review with a mechanical grounding check, not human verification. Treat it as a strong filter, not a guarantee.
- **Source caveat.** Social ingestion leans on an X account and is inherently fragile; when it stalls, the RSS, GitHub, arXiv, and advisory feeds keep the pipeline running.

### Repo layout

```
data/{ai-security,product-security,ai-research}.json  the 3 rolling pools (source of truth)
data/claims.json                                      the claim ledger (durable, never ages out)
data/archive.json · data/sources.json                 aged-out findings · ranked sources
scripts/                                               ingest · analyze-merge · rank · render
.claude/skills/                                        /research-scan /add-resource /add-source
ai-security/ product-security/ ai-research/            rendered per-topic pages (generated)
claims/                                                rendered claim ledger (generated)
README.md NEWSLETTER.md TRENDS.md REVIEW.md            generated - do not hand-edit
```

</details>

## License

Curated content under [CC BY 4.0](LICENSE); scripts under MIT. Linked research remains the property of its original authors - every finding cites its source.

<sub>Generated by <code>scripts/generate_site.py</code> on 2026-08-29. Edit the pools in <code>data/</code> and regenerate - do not hand-edit rendered files.</sub>
