# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_5 vetted findings · updated 2026-07-26 · ranked by composite · latest 31 days only · [5 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Tooling & Infrastructure | 1 |
| coding-agent harness design (first-party Anthropic practices) | 1 |
| Harness / context management | 1 |
| Agents & Harnesses | 1 |
| Meta-Harness | 1 |

## Tooling & Infrastructure

- **[Better Models, Worse Tools: SOTA models regress on non-native tool schemas](tooling-infrastructure/2026-07-better-models-worse-tools-sota-models-regress-on-non-native.md)** · composite **65.25** · Jul 4, 2026  
  Newer ≠ better for YOUR tools: match your harness's tool schemas to what the target model was trained on.  
  _[Simon Willison's Weblog](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything)_

## coding-agent harness design (first-party Anthropic practices)

- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](coding-agent-harness-design-first-party-anthropic-practices/2026-07-how-the-claude-code-team-designs-its-harness-tool-minimalism.md)** · composite **62.25** · Jul 21, 2026  
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous…  
  _[@simonw](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)_

## Harness / context management

- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](harness-context-management/2026-07-server-side-encrypted-compaction-porting-codex-s-responses-a.md)** · composite **62.25** · Jul 22, 2026  
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity — but treat 'it's…  
  _[@kunchenguid](https://github.com/algal/pi-openai-server-compaction)_

## Agents & Harnesses

- **[Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](agents-harnesses/2026-07-goal-persistent-agents-a-frontier-model-built-a-bespoke-zlib.md)** · composite **61.65** · Jul 2, 2026  
  When you hand an agent a durable goal plus strict 'what counts as a real finding' rules, it will plan multi-step tooling and self-filter noise — the rules, not the model alone, are what make the…  
  _[source](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)_

## Meta-Harness

- **[Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](meta-harness/2026-06-omnigent-an-open-source-meta-harness-over-claude-code-codex.md)** · composite **57.1** · Jun 2026  
  The 'meta-harness' is emerging as an abstraction layer above individual coding agents — orchestrate many, swap freely, enforce policy centrally.  
  _[omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent)_

---

[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md) · [Learnings](../LEARNINGS.md)
