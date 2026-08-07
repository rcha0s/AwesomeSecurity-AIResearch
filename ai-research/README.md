# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_2 vetted findings · updated 2026-08-07 · ranked by composite · latest 31 days only · [5 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| coding-agent harness design (first-party Anthropic practices) | 1 |
| Harness / context management | 1 |

## coding-agent harness design (first-party Anthropic practices)

- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](coding-agent-harness-design-first-party-anthropic-practices/2026-07-how-the-claude-code-team-designs-its-harness-tool-minimalism.md)** · composite **59.25** · Jul 21, 2026  
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous…  
  _[@simonw](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)_

## Harness / context management

- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](harness-context-management/2026-07-server-side-encrypted-compaction-porting-codex-s-responses-a.md)** · composite **59.25** · Jul 22, 2026  
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity - but treat 'it's…  
  _[@kunchenguid](https://github.com/algal/pi-openai-server-compaction)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
