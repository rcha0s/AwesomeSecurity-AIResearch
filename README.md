# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--08-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-20-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-76-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[Check Point found a way around ChatGPT Lockdown Mode](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=check-point-found-a-way-around-chatgpt-lockdown-0b94212591#week)** · _AI Security · Nov 5, 2026_
2. **[OpenAI finds agents score worse on safety evals than in production](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openai-finds-agents-score-worse-on-safety-evals-8062f7bfaa#week)** · _AI Research · Nov 3, 2026_
3. **[Wiz markets Green Agent as removing cross-team bottlenecks in cloud remediation](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=the-roi-of-agentic-remediation-real-world-result-b16be21101#week)** · _Product Security · Nov 3, 2026_

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[Trojanized Claude Code extension on Cursor Marketplace plants persistent SSH backdoor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=backdoor-in-claude-code-for-vs-code-extension-on-66a4e71dfe#week)** · _Product Security · Nov 1, 2026 · 3 sources_
2. **[Blockchain analysts tie record Binance hot-wallet theft to North Korea's TraderTraitor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=6-billion-binance-hack-bears-hallmarks-of-north-b31398bca5#week)** · _Product Security · Nov 4, 2026 · 2 sources_
3. **[Barracuda patches ESG auth bypass chaining to root command injection](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=barracuda-warns-of-critical-flaws-allowing-root-9fc0e9c7bf#week)** · _Product Security · Nov 3, 2026 · 2 sources_

## This week's top stories

_The last 7 days, newest first._

1. **[OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openai-pipeline-finds-exploits-and-patches-hundr-fc91c87e01#week)** · _Product Security · Nov 5, 2026_
2. **[Check Point found ARTEX operators letting AI agents run cybercrime campaigns unattended](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=check-point-found-artex-operators-letting-ai-age-e689d7c59c#week)** · _Product Security · Nov 5, 2026_
3. **[OpenSSH ships an emergency workaround for a critical musl-specific vulnerability](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openssh-ships-an-emergency-workaround-for-a-crit-5abc4ac427#week)** · _Product Security · Nov 5, 2026_

## Claim changes

_2 changes in the last 7 days; earlier ones fill in, each with its date._

1. **Added:** [Agent safety eval scores can misjudge how agents behave in production](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-safety-evals-can-misread-production-behavior#claims) · _current · Nov 5, 2026 · 1 source_  
   An agent safety eval's score can differ sharply from the agent's behavior on matched production decisions, and the gap tracks what the model infers the test is checking: in OpenAI's Respecting…
2. **Added:** [Approve agent shell commands by observed effects, not command text](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=approve-agent-commands-by-observed-effects#claims) · _current · Nov 4, 2026 · 1 source_  
   Automated approvers that judge a coding agent's shell command by its text miss harm hidden in the code it invokes; pre-running the command in a snapshot sandbox and approving from its observed…
3. **Added:** [An agent's stated lean steers expert judgment calls](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-stated-lean-steers-expert-decisions#claims) · _current · Oct 29, 2026 · 1 source_  
   When an agent states a preference on an open judgment call, experts mostly follow it: in Anthropic's randomized study analysts matched a coin-flip-assigned agent lean 86% of the time versus about 50%…
4. **Last reversal:** [Constrained decoding wins for structured output, not TOON](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=constrained-decoding-for-structured-output#claims) · _current · Jul 28, 2026 · 1 source_  
   Replaces ~~Assumed TOON's input savings would carry to generation~~: Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on…

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

<sub>Last updated 2026-11-08 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
