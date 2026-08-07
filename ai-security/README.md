# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_3 vetted findings · updated 2026-08-07 · ranked by composite · latest 31 days only · [7 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now, surfaced by the editorial pass._

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)**
  _Why now: Microsoft security guidance on a fast-moving theme (agentic MCP tooling): version and re-approve tool descriptions like system prompts. Part of the top agent-security trend cluster. · trending · newsworthy · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986)**
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

| Domain | Findings |
| --- | --- |
| MCP & Tools | 2 |
| Harness & Agent Security | 2 |
| Model Supply Chain | 1 |
| Skill Supply Chain | 1 |

## MCP & Tools

- **[ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](mcp-tools/2026-07-toolhive-mcp-ssrf-host-side-discovery-runs-outside-the-sandb.md)** · composite **63.9** · Jul 15, 2026  
  Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.  
  _[source](https://github.com/advisories/GHSA-pr64-jmmf-jp54)_
- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](mcp-tools/2026-06-treat-mcp-tool-descriptions-as-system-prompts-silent-re-trus.md)** · composite **52.2** · Jun 30, 2026 · ⚠️ _review_  
  Version and change-review every MCP tool description as if it were a system prompt, and force re-approval whenever tool metadata changes.  
  _[source](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)_

## Harness & Agent Security

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](harness-agent-security/2026-07-provider-safety-guardrails-blocked-incident-response-during.md)** · composite **56.25** · Jul 19, 2026 · ⚠️ _review_  
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.  
  _[source](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](harness-agent-security/2026-07-self-state-attacks-corrupting-an-agent-s-own-memory-and-conf.md)** · composite **50.62** · Jul 20, 2026 · ⚠️ _review_  
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.  
  _[source](https://arxiv.org/abs/2607.17986)_

## Model Supply Chain

- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](model-supply-chain/2026-07-shadowpickle-pickle-vm-import-tricks-evade-ten-model-scanner.md)** · composite **58.72** · Jul 20, 2026  
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.  
  _[source](https://arxiv.org/abs/2607.17503)_

## Skill Supply Chain

- **[Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](skill-supply-chain/2026-07-agent-skill-security-is-a-lifecycle-problem-not-just-a-runti.md)** · composite **58.35** · Jul 16, 2026  
  When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) - a runtime-only check misses where most of the risk actually lives.  
  _[source](https://arxiv.org/abs/2607.13987)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
