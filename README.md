# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--10--28-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-18-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-71-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[Arista VeloCloud Orchestrator SQL injection (CVE-2026-114625) is exploited in the wild](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=arista-velocloud-orchestrator-cve-2026-114625-sq-de4dcb4c11#week)** · _Product Security · Oct 22, 2026 · 3 sources_
2. **[Google: eight eMudhra CA keys had weak entropy and Chrome blocked them](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=google-eight-emudhra-intermediate-ca-keys-had-we-ad0993dcd1#week)** · _Product Security · Oct 22, 2026 · 10 sources_
3. **[Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=php2shell-wiz-used-frontier-ai-to-turn-memory-sa-59f53ebd81#week)** · _Product Security · Oct 21, 2026 · 5 sources_

## This week's top stories

_The last 7 days, newest first._

1. **[PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=portswigger-s-gareth-heyes-bypassed-six-of-eight-dbec8f0605#week)** · _Product Security · Oct 27, 2026_
2. **[Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ai2-llm-novelty-judges-flip-verdicts-when-prompt-5187f43a49#week)** · _AI Research · Oct 27, 2026_
3. **[Authlib accepts a JSON web signature with no signatures as verified](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=authlib-accepts-a-json-web-signature-with-no-sig-de447b05f2#week)** · _Product Security · Oct 27, 2026_

## Claim changes

_The 6 newest of 21 changes in the last 7 days._

1. **Added:** [Send simple subagent jobs to a cheaper model](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=cheaper-models-for-simple-subagent-jobs#claims) · _current · Oct 28, 2026 · 3 sources_  
   Anthropic's docs recommend routing simple subagent jobs to a cheaper model such as Haiku, and Aider's architect/editor split shows a reasoning model can pair with a weaker editor without losing…
2. **Added:** [Compact near the context limit; reset only if the model needs it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=compact-first-reset-only-if-the-model-needs-it#claims) · _current · Oct 28, 2026 · 3 sources_  
   A harness should compact long sessions automatically, and add hard context resets only for models that wrap up early near the limit.
3. **Added:** [Return short tool responses and distilled subagent summaries](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims) · _current · Oct 28, 2026 · 2 sources_  
   A harness that makes tools return concise fields, and subagents return condensed summaries (often 1,000-2,000 tokens), keeps the main context smaller; Anthropic's example used about a third of the…
4. **Added:** [Keep intermediate tool results out of the model context](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims) · _current · Oct 28, 2026 · 3 sources_  
   In Anthropic's own measurement, processing tool output in code and passing only results to the model cut average tokens by 37% on complex research tasks.
5. **Added:** [Load tool definitions on demand, not all at start](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=load-tool-definitions-on-demand#claims) · _current · Oct 28, 2026 · 3 sources_  
   Vendors report that loading tool definitions only when needed cut tokens by 47% (Cursor A/B test, runs that called an MCP tool) to 85% (Anthropic Tool Search); Anthropic's 98.7% is a single worked…
6. **Added:** [Measure speedups with repeated trials, not impressions](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=measure-speedups-with-repeated-trials#claims) · _current · Oct 28, 2026 · 3 sources_  
   A harness team should judge work efficiency with repeated-trial evals or timed studies, since in METR's early-2025 study developers believed AI sped them up while it slowed them down.

## Efficiency

_Where agent harnesses still waste tokens or time, and what to change._

- [Send simple subagent jobs to a cheaper model](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=cheaper-models-for-simple-subagent-jobs#claims)
- [Compact near the context limit; reset only if the model needs it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=compact-first-reset-only-if-the-model-needs-it#claims)
- [Return short tool responses and distilled subagent summaries](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims)
- [Keep intermediate tool results out of the model context](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims)

## Explore

### [Briefing](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#week) · [Stories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#news) · [Claims](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#claims) · [Topics](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#topics) · [Archive](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#archive) · [Methodology](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#methodology)

On GitHub: [AI Security](ai-security/README.md) · [Product Security](product-security/README.md) · [AI Research](ai-research/README.md) · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · [Trends](TRENDS.md) · [Review queue](REVIEW.md)

## Contribute

- **Suggest a source:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the feed or account URL. Sources join the ranked registry through a reviewed PR (`python scripts/add_source.py`).
- **Challenge a claim:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the evidence that refines or refutes it.
- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).

Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.

<sub>Last updated 2026-10-28 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
