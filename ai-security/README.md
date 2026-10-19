# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_6 vetted findings · updated 2026-10-19 · ranked by composite · findings from the latest 31 days._

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
| Harness & Agent Security | 3 |
| Coding-agent security | 1 |
| Agent-to-Agent Security / CI Prompt Injection | 1 |
| Multi-Agent Lateral Movement & Covert Coordination | 1 |
| Prompt Injection | 1 |
| LLM Red-Teaming | 1 |
| MCP & Tools | 1 |

## Harness & Agent Security

- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](harness-agent-security/2026-07-anthropic-s-own-cybersecurity-evals-let-three-claude-models.md)** · composite **55.5** · Jul 31, 2026  
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.  
  _[source](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)_
- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](harness-agent-security/2026-07-provider-safety-guardrails-blocked-incident-response-during.md)** · composite **51.75** · Jul 19, 2026 · ⚠️ _review_  
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.  
  _[source](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](harness-agent-security/2026-07-self-state-attacks-corrupting-an-agent-s-own-memory-and-conf.md)** · composite **46.12** · Jul 20, 2026 · ⚠️ _review_  
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.  
  _[source](https://arxiv.org/abs/2607.17986)_

## Coding-agent security

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](coding-agent-security/2026-10-trojan-horse-automated-repository-poisoning-against-coding-a.md)** · composite **65.84** · Oct 19, 2026  
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.  
  _[arXiv cs.CR (Cryptography and Security)](https://arxiv.org/abs/2610.23109)_

## Agent-to-Agent Security / CI Prompt Injection

- **[Google dev kit spurs first-ever agent-on-agent violence](agent-to-agent-security-ci-prompt-injection/2026-08-google-dev-kit-spurs-first-ever-agent-on-agent-violence.md)** · composite **62.35** · Aug 3, 2026  
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped…  
  _[source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_

## Multi-Agent Lateral Movement & Covert Coordination

- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](multi-agent-lateral-movement-covert-coordination/2026-08-openai-didn-t-notice-its-ai-agents-using-a-message-board-to.md)** · composite **61.75** · Aug 6, 2026  
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel - instrument it or write it out of the trust boundary.  
  _[source](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)_

## Prompt Injection

- **[Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](prompt-injection/2026-08-claude-code-opus-5-auto-mode-tricked-into-rce-via-website-su.md)** · composite **56.65** · Aug 28, 2026  
  A model's safety refusal to run an untrusted binary is not automatically safe if the 'safe' alternative it chooses (writing its own code to parse the untrusted data) is itself exploitable - …  
  _[Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)_

## LLM Red-Teaming

- **[Multidimensional Item-Response-Theory Auditing Reveals Some 'Safety' Benchmarks Are Actually Measuring General Reasoning](llm-red-teaming/2026-09-multidimensional-item-response-theory-auditing-reveals-some.md)** · composite **51.85** · Sep 1, 2026  
  A benchmark's stated purpose (e.g. "safety") doesn't guarantee its score is actually driven by that capability, or even in the direction you'd assume - a model that scores well on WMDP's…  
  _[source](https://huggingface.co/blog/allenai/benchmirt)_

## MCP & Tools

- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](mcp-tools/2026-06-treat-mcp-tool-descriptions-as-system-prompts-silent-re-trus.md)** · composite **51.45** · Jun 30, 2026 · ⚠️ _review_  
  Version and change-review every MCP tool description as if it were a system prompt, and force re-approval whenever tool metadata changes.  
  _[source](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
