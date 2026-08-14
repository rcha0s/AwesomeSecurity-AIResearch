# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_9 vetted findings · updated 2026-08-14 · ranked by composite · latest 31 days only · [227 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Autonomous vulnerability discovery | 1 |
| Agents & Harnesses | 1 |
| Frontier Cyber Capabilities & Preparedness | 1 |
| Agent Evals | 1 |
| Training-time Incidents & RLVR | 1 |
| AI-assisted Vulnerability Research | 1 |
| Harness / context management | 1 |
| Agents and Harnesses | 1 |
| Prompt & Context Engineering | 1 |

## Autonomous vulnerability discovery

- **[The Frontier AI Vulnerability Burst: Industrializing Autonomous Zero-Day Discovery in Open-Source Software](autonomous-vulnerability-discovery/2026-08-the-frontier-ai-vulnerability-burst-industrializing-autonomo.md)** · composite **74.12** · Aug 4, 2026  
  Autonomous AI vulnerability discovery moves the mix away from memory-corruption fuzzing (~8%) toward semantic/logic bugs (~92%), and complementarity between models is large enough that an ensemble is…  
  _[source](https://unit42.paloaltonetworks.com/frontier-ai-vulnerability-burst/)_

## Agents & Harnesses

- **[When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](agents-harnesses/2026-08-when-history-lies-evaluating-and-improving-tool-use-under-mi.md)** · composite **67.75** · Aug 7, 2026  
  History reliability is a distinct tool-use bottleneck: harnesses that just accumulate turns are silently letting old, wrong state overwrite the current task.  
  _[source](https://arxiv.org/abs/2608.06057)_

## Frontier Cyber Capabilities & Preparedness

- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](frontier-cyber-capabilities-preparedness/2026-08-openai-astra-preliminary-evals-can-t-rule-out-critical-cyber.md)** · composite **67.0** · Aug 7, 2026  
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better…  
  _[source](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)_

## Agent Evals

- **[Evaluating Investment Logic in Large Language Models: A Real-World Benchmark Towards Personalized Financial Agents](agent-evals/2026-08-evaluating-investment-logic-in-large-language-models-a-real.md)** · composite **64.75** · Aug 7, 2026  
  Terminal-P&L and static QA are the wrong ruler for consequential agents: score the P→E→R→D→O trace and you can see how weakly grounded 'logical' answers actually are.  
  _[source](https://arxiv.org/abs/2608.06108)_

## Training-time Incidents & RLVR

- **[Willison: the OpenAI/Hugging Face 'accidental attack' happened during an RLVR training run, not deployment](training-time-incidents-rlvr/2026-08-willison-the-openai-hugging-face-accidental-attack-happened.md)** · composite **59.35** · Aug 8, 2026  
  Treat training-time RLVR loops as their own agentic system with its own threat model - not a preview of deployment; the safety behaviors that gate deployment do not exist during training.  
  _[source](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything)_

## AI-assisted Vulnerability Research

- **[Automated Claude Code + Opus 4.6 pipeline finds a real Linux sandbox-escape CVE (CVE-2026-5674)](ai-assisted-vulnerability-research/2026-07-automated-claude-code-opus-4-6-pipeline-finds-a-real-linux-s.md)** · composite **58.77** · Jul 30, 2026  
  An agent-driven vuln-hunting pipeline can produce real, CVE-quality Linux sandbox-escape bugs - but the shipping discipline is 'AI found it, human reproduces it before you submit.'  
  _[source](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/)_

## Harness / context management

- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](harness-context-management/2026-07-server-side-encrypted-compaction-porting-codex-s-responses-a.md)** · composite **58.25** · Jul 22, 2026  
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity - but treat 'it's…  
  _[@kunchenguid](https://github.com/algal/pi-openai-server-compaction)_

## Agents and Harnesses

- **[OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality](agents-and-harnesses/2026-08-orchestrabench-evaluating-multi-agent-orchestration-failure.md)** · composite **57.25** · Aug 7, 2026  
  Multi-agent orchestration failures are not uniform: tool faults recover, ambiguous delegation partially recovers, latent/semantic faults essentially never self-heal. Blind retry hides latent faults…  
  _[source](https://arxiv.org/abs/2608.05263)_

## Prompt & Context Engineering

- **[Signal or Spurious Cue? A Randomized Audit of Survey-Country Metadata in LLM Social Inference](prompt-context-engineering/2026-08-signal-or-spurious-cue-a-randomized-audit-of-survey-country.md)** · composite **55.75** · Aug 7, 2026  
  Telling the model 'this cue is random, ignore it' does not actually get it to ignore the cue; treat metadata channels as load-bearing even when your prompt says they aren't.  
  _[source](https://arxiv.org/abs/2608.06085)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
