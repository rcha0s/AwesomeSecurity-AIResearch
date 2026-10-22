# Awesome Security & AI Research

<p align="center"><a href="https://rcha0s.github.io/AwesomeSecurity-AIResearch/"><img src="docs/og.png" alt="Awesome Security & AI Research - a weekly, source-cited briefing" width="720"></a></p>

> A weekly, source-cited briefing on AI security, product security and applied AI research. Every finding is vetted and distilled to one lesson; a claim ledger tracks what to do now and what it replaced.

![Updated](https://img.shields.io/badge/updated-2026--10--22-1f6feb) ![Vetted](https://img.shields.io/badge/vetted_findings-11-2da44e) ![Claims](https://img.shields.io/badge/standing_claims-53-6f42c1) ![License](https://img.shields.io/badge/content-CC--BY--4.0-8b949e)

**The site is the product: [rcha0s.github.io/AwesomeSecurity-AIResearch/](https://rcha0s.github.io/AwesomeSecurity-AIResearch/)**. Open the Briefing for this week, Claims for what to act on, Topics to browse by domain. Click any title for the full writeup with its sources; every view and finding has a link you can share.

## This week's top stories

_The last 7 days: the stories with the most covering sources first._

1. **[Pillow MIC images hang n\_frames forever: an inherited method that depends on an overridden tell() (GHSA-22hg-r758-rrw9)](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=ghsa-22hg-r758-rrw9-7a9523be43#week)** · _Product Security · Oct 21, 2026 · 1 source_
2. **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=review-of-the-misalignment-in-high-stakes-settin-5863cde447#week)** · _AI Research · Oct 20, 2026 · 1 source_
3. **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?finding=trojan-horse-automated-repository-poisoning-agai-c6a8fe9d8c#week)** · _AI Security · Oct 19, 2026 · 1 source_

## What to do now

_Standing answers from the claim ledger._

1. **[Indirect injection via retrieved content is a real vector](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=indirect-injection-via-retrieved-content-is-viable#claims)**  
   Treat every retrieval-augmented context as untrusted input. Never let retrieved content unilaterally cause a tool call with side effects.
2. **[WebView JS bridges turn web XSS into device RCE](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=mobile-webviews-are-a-persistent-cross-context-attack-surface#claims)**  
   Never expose native bridges to WebViews that render third-party content.
3. **[Auto-evolved harness gains are mostly overfitting](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-evolution-gains-need-held-out-attribution#claims)**  
   Accept an auto-evolved harness change only on its delta over a held-out task set the optimizer never saw, measured at matched inference budget; don't trust search-set or validation-set improvement.

## Explore

### [Briefing](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#week) · [Claims](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#claims) · [Topics](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#topics) · [Methodology](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#methodology) · [Archive](https://rcha0s.github.io/AwesomeSecurity-AIResearch/#archive)

On GitHub: [AI Security](ai-security/README.md) · [Product Security](product-security/README.md) · [AI Research](ai-research/README.md) · [Claims](claims/README.md) · [Newsletter](NEWSLETTER.md) · [Trends](TRENDS.md) · [Review queue](REVIEW.md)

## Contribute

- **Suggest a source:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the feed or account URL. Sources join the ranked registry through a reviewed PR (`python scripts/add_source.py`).
- **Challenge a claim:** [open an issue](https://github.com/rcha0s/AwesomeSecurity-AIResearch/issues/new) with the evidence that refines or refutes it.
- **Work on the pipeline:** [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) (layout, tests, automation) · [PUBLISH.md](PUBLISH.md).

Content is [CC BY 4.0](LICENSE), scripts MIT; linked research belongs to its authors.

<sub>Last updated 2026-10-22 by <code>scripts/generate_site.py</code> from the pools in <code>data/</code>. Generated - do not hand-edit.</sub>
