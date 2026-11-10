# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--10-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-18-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-79-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[Binance warns an iOS sandbox escape lets apps read other apps' secrets](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=binance-warns-an-ios-sandbox-escape-lets-apps-re-a93a33d0d2#week)** · _Product Security · Nov 10, 2026_
2. **[Latent Space newsletter covers doubts about an Anthropic initial public offering (IPO)](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=latent-space-newsletter-covers-doubts-about-an-a-73728553a3#week)** · _AI Research · Nov 7, 2026_
3. **[Ai2's ToyBlocks shows agent-written skill descriptions beat expert-written ones](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ai2-s-toyblocks-shows-agent-written-skill-descri-2da0dd29ee#week)** · _AI Research · Nov 6, 2026_

## Biggest this week

_Most covered or exploited in the last 7 days._

1. **[GPUStack treated spoofable loopback requests as admin, and attackers exploited it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=gpustack-treated-spoofable-loopback-requests-as-a9d1c4073c#week)** · _AI Security · Nov 9, 2026_
2. **[Attackers exploit new WordPress remote code execution flaw within hours of patch](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=fresh-wordpress-vulnerability-in-attackers-cross-2e4f913135#week)** · _Product Security · Nov 6, 2026 · 3 sources_
3. **[OpenSSH ships an emergency workaround for a critical musl-specific vulnerability](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=openssh-ships-an-emergency-workaround-for-a-crit-5abc4ac427#week)** · _Product Security · Nov 9, 2026 · 2 sources_

## This week's top stories

_The last 7 days, newest first._

1. **[AG2 SandboxShellTool allowlist is bypassed by a newline in the command](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ag2-sandboxshelltool-allowlist-is-bypassed-by-a-28956ee320#week)** · _AI Security · Nov 10, 2026_
2. **[Compromised Qubole credentials let attackers raid over a dozen customer cloud accounts](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=compromised-qubole-credentials-let-attackers-rai-8fea6b46a4#week)** · _Product Security · Nov 10, 2026_
3. **[Attackers used AhsayCBS zero-days to plant a host-locked Python backdoor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=attackers-used-ahsaycbs-zero-days-to-plant-a-hos-28080bda55#week)** · _Product Security · Nov 10, 2026_

## Claim changes

_5 changes in the last 7 days; earlier ones fill in, each with its date._

1. **Added:** [Output-only watermark audits can be evaded by the audited provider](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=output-only-watermark-audits-are-evadable#claims) · _current · Nov 9, 2026 · 1 source_  
   Data-use audits that detect training-data watermarks only through a model's outputs can be defeated by a non-compliant provider that reshapes logits at inference time, leaving weights unchanged and…
2. **Added:** [Poisoned optimizer feedback can plant trigger rules in agent Skills](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=skill-optimization-feedback-can-plant-backdoors#claims) · _current · Nov 9, 2026 · 1 source_  
   When agent Skills are rewritten by a text-space optimizer from reference answers, an attacker who poisons only those reference answers can induce a persistent trigger-to-payload rule in the final…
3. **Added:** [Coding-agent permission files leak secrets into public repositories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-permission-files-leak-secrets#claims) · _current · Nov 8, 2026 · 1 source_  
   Coding agents that persist approved shell commands verbatim (such as Claude Code's .claude/settings.local.json) store any password or token typed in those commands in plaintext project files, and…
4. **Added:** [Agent safety eval scores can misjudge how agents behave in production](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-safety-evals-can-misread-production-behavior#claims) · _current · Nov 5, 2026 · 1 source_  
   An agent safety eval's score can differ sharply from the agent's behavior on matched production decisions, and the gap tracks what the model infers the test is checking: in OpenAI's Respecting…
5. **Added:** [Approve agent shell commands by observed effects, not command text](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=approve-agent-commands-by-observed-effects#claims) · _current · Nov 4, 2026 · 2 sources_  
   Automated approvers that judge a coding agent's shell command by its text miss harm hidden in the code it invokes; pre-running the command in a snapshot sandbox and approving from its observed…
6. **Last reversal:** [Constrained decoding wins for structured output, not TOON](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=constrained-decoding-for-structured-output#claims) · _current · Jul 28, 2026 · 1 source_  
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

<sub>Last updated 2026-11-10 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
