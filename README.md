# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--04-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-23-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-73-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[Wiz markets Green Agent as removing cross-team bottlenecks in cloud remediation](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=the-roi-of-agentic-remediation-real-world-result-b16be21101#week)** · _Product Security · Nov 3, 2026_
2. **[OpenAI details how it trains streaming activation probes that block policy-violating completions](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=training-activation-classifiers-for-safety-and-a-669daa6f81#week)** · _AI Security · Nov 2, 2026_
3. **[Trail of Bits uses Codex to backport security fixes to stable Linux](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=backporting-security-fixes-at-scale-with-codex-61b7394775#week)** · _Product Security · Nov 2, 2026_

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[Ivanti Connect Secure chain to root is exploited, CISA adds two CVEs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ivanti-connect-secure-chain-to-root-is-exploited-7f77ca0434#week)** · _Product Security · Oct 30, 2026 · 2 sources_
2. **[Attackers exploit a missing-authorization flaw in Drupal Commerce Core](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=hackers-actively-exploit-highly-critical-drupal-bb564fb962#week)** · _Product Security · Oct 30, 2026_
3. **[KeyDrift malware steals Cisco SD-WAN encryption keys from hacked controllers](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=hackers-exploited-cisco-sd-wan-flaw-to-plant-mal-907b712081#week)** · _Product Security · Oct 29, 2026_

## This week's top stories

_The last 7 days, newest first._

1. **[Barracuda patches ESG auth bypass chaining to root command injection](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=barracuda-warns-of-critical-flaws-allowing-root-9fc0e9c7bf#week)** · _Product Security · Nov 3, 2026_
2. **[Google warns LLMjacking attacks cost some enterprises up to $1 million](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=google-warns-llmjacking-attacks-are-costing-some-b14fb698e3#week)** · _AI Security · Nov 3, 2026_
3. **[UK NCSC warns AI-powered ransomware will hit critical infrastructure by 2028](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=britain-on-notice-ai-powered-ransomware-attacks-666af1d3dd#week)** · _AI Security · Nov 3, 2026_

## Claim changes

_The 6 newest of 14 changes in the last 7 days._

1. **Added:** [An agent's stated lean steers expert judgment calls](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-stated-lean-steers-expert-decisions#claims) · _current · Oct 29, 2026 · 1 source_  
   When an agent states a preference on an open judgment call, experts mostly follow it: in Anthropic's randomized study analysts matched a coin-flip-assigned agent lean 86% of the time versus about 50%…
2. **Added:** [Send simple subagent jobs to a cheaper model](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=cheaper-models-for-simple-subagent-jobs#claims) · _current · Oct 28, 2026 · 3 sources_  
   Anthropic's docs recommend routing simple subagent jobs to a cheaper model such as Haiku, and Aider's architect/editor split shows a reasoning model can pair with a weaker editor without losing…
3. **Added:** [Compact near the context limit; reset only if the model needs it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=compact-first-reset-only-if-the-model-needs-it#claims) · _current · Oct 28, 2026 · 3 sources_  
   A harness should compact long sessions automatically, and add hard context resets only for models that wrap up early near the limit.
4. **Added:** [Return short tool responses and distilled subagent summaries](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims) · _current · Oct 28, 2026 · 2 sources_  
   A harness that makes tools return concise fields, and subagents return condensed summaries (often 1,000-2,000 tokens), keeps the main context smaller; Anthropic's example used about a third of the…
5. **Added:** [Keep intermediate tool results out of the model context](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims) · _current · Oct 28, 2026 · 3 sources_  
   In Anthropic's own measurement, processing tool output in code and passing only results to the model cut average tokens by 37% on complex research tasks.
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

<sub>Last updated 2026-11-04 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
