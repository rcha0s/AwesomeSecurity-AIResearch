# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--11--18-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-34-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-83-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## Your focus

_Your focus areas, last 7 days: most areas matched first, then newest._

1. **[Microsoft shows poisoned fine-tuning data and checkpoints hijack coding agents' tools](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=microsoft-shows-poisoned-fine-tuning-data-and-ch-8d4cff91d3#week)** · _AI Security · Nov 12, 2026_
2. **[Pretxt raises $5M seed for runtime AI agent supervision that steers agents](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=pretxt-emerges-stealth-with-5m-seed-and-an-ai-su-b33ea39de5#week)** · _AI Security · Nov 17, 2026_
3. **[Simon Willison and Prime Radiant release external sandboxes for coding agents](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=simon-willison-and-prime-radiant-release-externa-40b0e5c0ba#week)** · _AI Security · Nov 17, 2026_

## What to learn

_From the last 14 days: each has proof (the work itself or a measured comparison) and serves one of your goals; more independent sources rank first._

1. **[Microsoft finds 8% of coding sessions account for 44% of costs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=microsoft-research-focus-edition-98-87946c1829#week)** · _AI Research · Nov 12, 2026_
2. **[UC Berkeley finds harness overhead can double agent cost at similar accuracy](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=uc-berkeley-finds-harness-overhead-can-double-ag-49f29b0015#week)** · _AI Research · Nov 9, 2026_
3. **[York University's FlowPlan cuts Claude Code tokens by planning edits first](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=york-university-s-flowplan-cuts-claude-code-toke-ab96ed416c#week)** · _AI Research · Nov 9, 2026_

## Biggest this week

_Most covered in the last 7 days; single-outlet patch notices are left out._

1. **[Trojanized Claude Code extension on Cursor Marketplace plants persistent SSH backdoor](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=backdoor-in-claude-code-for-vs-code-extension-on-66a4e71dfe#week)** · _Product Security · Nov 14, 2026 · 4 sources_
2. **[N-able takes hosted N-central offline after researcher publishes 33 zero-day exploits](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=n-able-takes-hosted-n-central-offline-after-rese-5b959f2d42#week)** · _Product Security · Nov 12, 2026 · 4 sources_
3. **[N-able investigates new N-central exploits that work against hotfixed on-premise servers](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=n-able-investigates-new-n-central-exploits-that-2c3354cb8c#week)** · _Product Security · Nov 13, 2026 · 3 sources_

## This week's top stories

_The last 7 days, most covered first._

1. **[SafeDep tracks wfx stealer pushed into 8,093+ repos, likely via stolen tokens](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=safedep-tracks-wfx-stealer-pushed-into-8-093-rep-cf9a2f8a82#week)** · _Product Security · Nov 12, 2026 · 2 sources_
2. **[Researcher releases SignDrop Windows zero-day exploit granting SYSTEM privileges](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=researcher-releases-signdrop-windows-zero-day-ex-4dea8a1318#week)** · _Product Security · Nov 12, 2026 · 2 sources_
3. **[Check Point ships hotfixes for a zero-day exploited for root access](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=check-point-ships-hotfixes-for-a-zero-day-exploi-472c742795#week)** · _Product Security · Nov 13, 2026 · 2 sources_

## Claim changes

_3 changes in the last 7 days; earlier ones fill in, each with its date._

1. **Added:** [Harness overhead, not the model, can double an agent's cost](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-overhead-sets-agent-cost#claims) · _current · Nov 18, 2026 · 2 sources_  
   On the same model and task, a full-featured harness's system prompt and tool schemas can cost about twice a bare agent loop with little accuracy difference, and coding agents' first call alone ranges…
2. **Added:** [Learn per-repo cost controls from past coding agent runs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=learn-per-repo-cost-controls#claims) · _current · Nov 18, 2026 · 1 source_  
   A controller that learns from earlier runs in the same repository which tools to prune, which short notes to inject and when to stop unproductive failure loops cut coding-agent cost by 18-31% on…
3. **Added:** [Use one-hour cache markers when sessions pause over five minutes](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=one-hour-cache-for-paused-sessions#claims) · _current · Nov 18, 2026 · 2 sources_  
   Harnesses that write 5-minute prompt-cache markers re-buy their whole context after an idle gap longer than five minutes, while harnesses with 1-hour markers kept about 86% cache hits after a…
4. **Last reversal:** [Constrained decoding wins for structured output, not TOON](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=constrained-decoding-for-structured-output#claims) · _current · Jul 28, 2026 · 1 source_  
   Replaces ~~Assumed TOON's input savings would carry to generation~~: Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on…

## Efficiency

_Where agent harnesses still waste tokens or time, and what to change. [Harness feed](https://rcha0s.github.io/AwesomeSecurity-AIResearch/efficiency.md)._

- [Harness overhead, not the model, can double an agent's cost](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-overhead-sets-agent-cost#claims) · _updated Nov 18, 2026_
- [Learn per-repo cost controls from past coding agent runs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=learn-per-repo-cost-controls#claims) · _updated Nov 18, 2026_
- [Use one-hour cache markers when sessions pause over five minutes](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=one-hour-cache-for-paused-sessions#claims) · _updated Nov 18, 2026_
- [Keep intermediate tool results out of the model context](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims) · _updated Nov 9, 2026_

## Explore

### [Briefing](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#week) · [Stories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#news) · [Claims](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#claims) · [Topics](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#topics) · [Archive](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#archive) · [Methodology](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#methodology)

On GitHub: [AI Security](ai-security/README.md) · [Product Security](product-security/README.md) · [AI Research](ai-research/README.md) · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · [Trends](TRENDS.md) · [Review queue](REVIEW.md)

## Contribute

- **Suggest a source:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the feed or account URL. Sources join the ranked registry through a reviewed PR (`python scripts/add_source.py`).
- **Challenge a claim:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the evidence that refines or refutes it.
- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).

Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.

<sub>Last updated 2026-11-18 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
