# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_6 vetted findings · updated 2026-08-11 · ranked by composite · latest 31 days only · [9 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Autonomous vulnerability discovery | 1 |
| Frontier Cyber Capabilities & Preparedness | 1 |
| Training-time Incidents & RLVR | 1 |
| AI-assisted Vulnerability Research | 1 |
| coding-agent harness design (first-party Anthropic practices) | 1 |
| Harness / context management | 1 |

## Autonomous vulnerability discovery

- **[The Frontier AI Vulnerability Burst: Industrializing Autonomous Zero-Day Discovery in Open-Source Software](autonomous-vulnerability-discovery/2026-08-the-frontier-ai-vulnerability-burst-industrializing-autonomo.md)** · composite **77.12** · Aug 4, 2026  
  Autonomous AI vulnerability discovery moves the mix away from memory-corruption fuzzing (~8%) toward semantic/logic bugs (~92%), and complementarity between models is large enough that an ensemble is…  
  _[source](https://unit42.paloaltonetworks.com/frontier-ai-vulnerability-burst/)_

## Frontier Cyber Capabilities & Preparedness

- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](frontier-cyber-capabilities-preparedness/2026-08-openai-astra-preliminary-evals-can-t-rule-out-critical-cyber.md)** · composite **70.0** · Aug 7, 2026  
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better…  
  _[source](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)_

## Training-time Incidents & RLVR

- **[Willison: the OpenAI/Hugging Face 'accidental attack' happened during an RLVR training run, not deployment](training-time-incidents-rlvr/2026-08-willison-the-openai-hugging-face-accidental-attack-happened.md)** · composite **62.35** · Aug 8, 2026  
  Treat training-time RLVR loops as their own agentic system with its own threat model - not a preview of deployment; the safety behaviors that gate deployment do not exist during training.  
  _[source](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything)_

## AI-assisted Vulnerability Research

- **[Automated Claude Code + Opus 4.6 pipeline finds a real Linux sandbox-escape CVE (CVE-2026-5674)](ai-assisted-vulnerability-research/2026-07-automated-claude-code-opus-4-6-pipeline-finds-a-real-linux-s.md)** · composite **59.27** · Jul 30, 2026  
  An agent-driven vuln-hunting pipeline can produce real, CVE-quality Linux sandbox-escape bugs - but the shipping discipline is 'AI found it, human reproduces it before you submit.'  
  _[source](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/)_

## coding-agent harness design (first-party Anthropic practices)

- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](coding-agent-harness-design-first-party-anthropic-practices/2026-07-how-the-claude-code-team-designs-its-harness-tool-minimalism.md)** · composite **58.75** · Jul 21, 2026  
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous…  
  _[@simonw](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)_

## Harness / context management

- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](harness-context-management/2026-07-server-side-encrypted-compaction-porting-codex-s-responses-a.md)** · composite **58.75** · Jul 22, 2026  
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity - but treat 'it's…  
  _[@kunchenguid](https://github.com/algal/pi-openai-server-compaction)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
