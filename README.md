# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--08-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-20-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-77-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[Latent Space newsletter covers doubts about an Anthropic initial public offering (IPO)](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=latent-space-newsletter-covers-doubts-about-an-a-73728553a3#week)** · _AI Research · Nov 7, 2026_
2. **[Ai2's ToyBlocks shows agent-written skill descriptions beat expert-written ones](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ai2-s-toyblocks-shows-agent-written-skill-descri-2da0dd29ee#week)** · _AI Research · Nov 6, 2026_
3. **[Free Chinese models DeepSeek and GLM come close to OpenAI's cyber model](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=free-chinese-models-deepseek-and-glm-come-close-87c3174d24#week)** · _AI Security · Nov 6, 2026_

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[Attackers exploit new WordPress remote code execution flaw within hours of patch](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=fresh-wordpress-vulnerability-in-attackers-cross-2e4f913135#week)** · _Product Security · Nov 6, 2026 · 3 sources_
2. **[Trojanized Claude Code extension on Cursor Marketplace plants persistent SSH backdoor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=backdoor-in-claude-code-for-vs-code-extension-on-66a4e71dfe#week)** · _Product Security · Nov 1, 2026 · 3 sources_
3. **[Chainalysis discloses breach by attackers using offensive agentic techniques](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=chainalysis-discloses-breach-by-attackers-using-85c9c02a0a#week)** · _AI Security · Nov 6, 2026 · 2 sources_

## This week's top stories

_The last 7 days, newest first._

1. **[D-Link DGS-3130 switches have unpatched discovery protocol zero-days](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=d-link-dgs-3130-switches-have-unpatched-discover-d36b246e37#week)** · _Product Security · Nov 6, 2026_
2. **[OpenAI partners with Hacktron to test its third-party service connections](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openai-partners-with-hacktron-to-test-its-third-a0d1f0830e#week)** · _Product Security · Nov 6, 2026_
3. **[Malicious Ruby gem strutil-core runs a credential-stealing worm at install](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=malicious-ruby-gem-strutil-core-runs-a-credentia-07242a95d4#week)** · _Product Security · Nov 6, 2026_

## Claim changes

_3 changes in the last 7 days; earlier ones fill in, each with its date._

1. **Added:** [Coding-agent permission files leak secrets into public repositories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-permission-files-leak-secrets#claims) · _current · Nov 8, 2026 · 1 source_  
   Coding agents that persist approved shell commands verbatim (such as Claude Code's .claude/settings.local.json) store any password or token typed in those commands in plaintext project files, and…
2. **Added:** [Agent safety eval scores can misjudge how agents behave in production](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-safety-evals-can-misread-production-behavior#claims) · _current · Nov 5, 2026 · 1 source_  
   An agent safety eval's score can differ sharply from the agent's behavior on matched production decisions, and the gap tracks what the model infers the test is checking: in OpenAI's Respecting…
3. **Added:** [Approve agent shell commands by observed effects, not command text](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=approve-agent-commands-by-observed-effects#claims) · _current · Nov 4, 2026 · 1 source_  
   Automated approvers that judge a coding agent's shell command by its text miss harm hidden in the code it invokes; pre-running the command in a snapshot sandbox and approving from its observed…
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
