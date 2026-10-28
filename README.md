# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research, plus a claim ledger that calls out what the field now believes, what changed and what got overturned.

![Updated](https://img.shields.io/badge/updated-2026--10--28-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-18-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-57-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

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

_The 6 newest of 7 changes in the last 7 days._

1. **Added:** [Rendered agent transcripts can show reviewers a false record](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-output-is-untrusted-input-to-review-tooling#claims) · _current · Oct 25, 2026 · 1 source_  
   Agent transcripts, logs and tool output are attacker-controlled content: a viewer or monitor that renders them can be made to show reviewers a false record even while the stored log stays intact.
2. **Added:** [Any webpage can reach a coding agent's localhost server](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=localhost-agent-servers-are-reachable-from-any-webpage#claims) · _current · Oct 25, 2026 · 2 sources_  
   A coding agent's local HTTP server is reachable from any webpage the user visits: top-level form POSTs are not blocked by CORS, so binding to loopback is not a security boundary.
3. **Added:** [Harmful goals split across skills slip past per-skill scanners](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=per-skill-scanning-misses-cross-skill-cascades#claims) · _current · Oct 25, 2026 · 1 source_  
   A harmful goal split across several agent skills that each look benign can get past scanners and reviews that judge one skill at a time.
4. **Added:** [A guardrail weaker than its target can be bypassed](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=input-guardrail-weaker-than-target-is-bypassable#claims) · _current · Oct 24, 2026 · 1 source_  
   An input-screening guardrail model that is less capable than the model it protects (less reasoning effort, no tools) can be bypassed by payloads hidden in plain prose that only the stronger,…
5. **Added:** [Auto-evolved harness gains are mostly overfitting](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-evolution-gains-need-held-out-attribution#claims) · _current · Oct 21, 2026 · 2 sources_  
   Gains from automatically evolving an agent harness (prompts, skills, tools, orchestration around a fixed model) are mostly search-set overfitting and extra inference compute: across 21 settings with…
6. **Contested:** [Diff review catches more LLM-introduced defects than full-file review](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=diff-review-catches-more-than-full-file-review#claims) · _contested · Oct 21, 2026 · 2 sources_  
   Reviewing an LLM's proposed change as a diff catches more defects than reviewing the resulting full file.

## Explore

### [Briefing](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#week) · [Stories](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#news) · [Claims](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#claims) · [Topics](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#topics) · [Archive](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#archive) · [Methodology](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#methodology)

On GitHub: [AI Security](ai-security/README.md) · [Product Security](product-security/README.md) · [AI Research](ai-research/README.md) · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · [Trends](TRENDS.md) · [Review queue](REVIEW.md)

## Contribute

- **Suggest a source:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the feed or account URL. Sources join the ranked registry through a reviewed PR (`python scripts/add_source.py`).
- **Challenge a claim:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the evidence that refines or refutes it.
- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).

Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.

<sub>Last updated 2026-10-28 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
