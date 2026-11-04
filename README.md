# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--04-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-23-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-75-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[OpenAI describes its layered monitor for misbehaving frontier agents](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openai-describes-its-layered-monitor-for-misbeha-3d848d3ef4#week)** · _AI Security · Oct 29, 2026_
2. **[Wiz lists the fingerprints that mark an intrusion as agent-driven](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=wiz-lists-the-fingerprints-that-mark-an-intrusio-b890aba68a#week)** · _Product Security · Oct 29, 2026_
3. **[Hugging Face cryptomining malware campaign returned days after takedown](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=hugging-face-malware-campaign-returns-to-hijack-7725614bd1#week)** · _AI Security · Oct 29, 2026_

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[Ivanti Connect Secure chain to root is exploited, CISA adds two CVEs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ivanti-connect-secure-chain-to-root-is-exploited-7f77ca0434#week)** · _Product Security · Oct 30, 2026 · 2 sources_
2. **[Attackers exploit a missing-authorization flaw in Drupal Commerce Core](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=hackers-actively-exploit-highly-critical-drupal-bb564fb962#week)** · _Product Security · Oct 30, 2026_
3. **[KeyDrift malware steals Cisco SD-WAN encryption keys from hacked controllers](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=hackers-exploited-cisco-sd-wan-flaw-to-plant-mal-907b712081#week)** · _Product Security · Oct 29, 2026_

## This week's top stories

_The last 7 days, newest first._

1. **[Trojanized Claude Code extension on Cursor Marketplace plants persistent SSH backdoor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=backdoor-in-claude-code-for-vs-code-extension-on-66a4e71dfe#week)** · _Product Security · Nov 1, 2026 · 3 sources_
2. **[Canonical LXD and MicroCloud accepted forged client certificate chains](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=canonical-lxd-and-microcloud-accepted-forged-cli-522855cdae#week)** · _Product Security · Nov 1, 2026_
3. **[Callix finds 819 vulnerable paths in Android vendors' pre-installed apps](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=beyond-sensitive-apis-detecting-access-control-f-2b34c23353#week)** · _Product Security · Oct 31, 2026_

## Claim changes

_The 6 newest of 15 changes in the last 7 days._

1. **Added:** [Approve agent shell commands by observed effects, not command text](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=approve-agent-commands-by-observed-effects#claims) · _current · Nov 4, 2026 · 1 source_  
   Automated approvers that judge a coding agent's shell command by its text miss harm hidden in the code it invokes; pre-running the command in a snapshot sandbox and approving from its observed…
2. **Added:** [An agent's stated lean steers expert judgment calls](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-stated-lean-steers-expert-decisions#claims) · _current · Oct 29, 2026 · 1 source_  
   When an agent states a preference on an open judgment call, experts mostly follow it: in Anthropic's randomized study analysts matched a coin-flip-assigned agent lean 86% of the time versus about 50%…
3. **Added:** [Send simple subagent jobs to a cheaper model](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=cheaper-models-for-simple-subagent-jobs#claims) · _current · Oct 28, 2026 · 3 sources_  
   Anthropic's docs recommend routing simple subagent jobs to a cheaper model such as Haiku, and Aider's architect/editor split shows a reasoning model can pair with a weaker editor without losing…
4. **Added:** [Compact near the context limit; reset only if the model needs it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=compact-first-reset-only-if-the-model-needs-it#claims) · _current · Oct 28, 2026 · 3 sources_  
   A harness should compact long sessions automatically, and add hard context resets only for models that wrap up early near the limit.
5. **Added:** [Return short tool responses and distilled subagent summaries](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims) · _current · Oct 28, 2026 · 2 sources_  
   A harness that makes tools return concise fields, and subagents return condensed summaries (often 1,000-2,000 tokens), keeps the main context smaller; Anthropic's example used about a third of the…
6. **Added:** [Keep intermediate tool results out of the model context](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims) · _current · Oct 28, 2026 · 3 sources_  
   In Anthropic's own measurement, processing tool output in code and passing only results to the model cut average tokens by 37% on complex research tasks.

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
