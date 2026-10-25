# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--10--25-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-11-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-56-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for the ledger, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## This week's top stories

_The last 7 days: the stories with the most covering sources first._

1. **[Google: eight eMudhra intermediate CA keys had weak entropy, so Chrome blocked them within two hours and is removing the root](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=google-eight-emudhra-intermediate-ca-keys-had-we-ad0993dcd1#week)** · _Product Security · Oct 22, 2026 · 10 sources_
2. **[333 Tor exit relays hijacked with the Ebury backdoor to intercept SSH passwords and unencrypted mail](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=333-tor-exit-relays-hijacked-with-the-ebury-back-02fda395c8#week)** · _Product Security · Oct 20, 2026 · 4 sources_
3. **[Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=pillow-ghsa-w889-685w-c8fh-attacker-controlled-f-6e66febba5#week)** · _Product Security · Oct 23, 2026 · 3 sources_

## Claim changes

_Every claim added, contested or overturned in the last 7 days._

1. **Added:** [A coding agent's local HTTP server is reachable from any webpage the user visits: top-level form POSTs are not blocked by CORS, so binding to loopback is not a…](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=localhost-agent-servers-are-reachable-from-any-webpage#claims) · _current · Oct 25, 2026 · 2 sources_
2. **Added:** [A harmful goal split across several agent skills that each look benign can get past scanners and reviews that judge one skill at a time.](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=per-skill-scanning-misses-cross-skill-cascades#claims) · _current · Oct 25, 2026 · 1 source_
3. **Added:** [A guardrail weaker than its target can be bypassed](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=input-guardrail-weaker-than-target-is-bypassable#claims) · _current · Oct 24, 2026 · 1 source_  
   An input-screening guardrail model that is less capable than the model it protects (less reasoning effort, no tools) can be bypassed by payloads hidden in plain prose that only the stronger,…
4. **Added:** [Auto-evolved harness gains are mostly overfitting](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-evolution-gains-need-held-out-attribution#claims) · _current · Oct 21, 2026 · 1 source_  
   Gains from automatically evolving an agent harness (prompts, skills, tools, orchestration around a fixed model) are mostly search-set overfitting and extra inference compute: across 21 settings with…
5. **Contested:** [Diff review catches more LLM-introduced defects than full-file review](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=diff-review-catches-more-than-full-file-review#claims) · _contested · Oct 21, 2026 · 2 sources_  
   Reviewing an LLM's proposed change as a diff catches more defects than reviewing the resulting full file.
6. **Overturned:** [Constrained decoding wins for structured output, not TOON](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=constrained-decoding-for-structured-output#claims) · _current · Jul 28, 2026 · 1 source_  
   Replaces ~~Assumed TOON's input savings would carry to generation~~: Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on…

## Explore

### [Briefing](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#week) · [Stories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#news) · [Claims](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#claims) · [Topics](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#topics) · [Archive](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#archive) · [Methodology](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#methodology)

On GitHub: [AI Security](ai-security/README.md) · [Product Security](product-security/README.md) · [AI Research](ai-research/README.md) · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · [Trends](TRENDS.md) · [Review queue](REVIEW.md)

## Contribute

- **Suggest a source:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the feed or account URL. Sources join the ranked registry through a reviewed PR (`python scripts/add_source.py`).
- **Challenge a claim:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the evidence that refines or refutes it.
- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).

Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.

<sub>Last updated 2026-10-25 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
