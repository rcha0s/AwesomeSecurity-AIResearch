# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_17 vetted findings · updated 2026-09-09 · ranked by composite · latest 31 days only · [42 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| AI Security | 4 |
| Harness & Agent Security | 2 |
| Prompt Injection | 2 |
| LLM Red-Teaming | 2 |
| Prompt Injection & Adversarial | 1 |
| Agents / Information-Flow Control | 1 |
| Guardrails / Over-Refusal | 1 |
| Coding Agents / Prompt-Space Defense | 1 |
| Agent Governance / Runtime | 1 |
| Model Supply Chain | 1 |
| Adversarial Attacks | 1 |

## AI Security

- **[Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](ai-security/2026-08-diffusion-llms-as-targets-and-adversaries-mechanistic-safety.md)** · composite **55.4** · Aug 10, 2026  
  Safety alignment in diffusion LLMs is sparse enough to be located by neuron mapping and cheaply bypassed - and the resulting attack transfers across families, including to a closed frontier model.  
  _[source](https://arxiv.org/abs/2608.07430)_
- **[praetorian-inc/augustus](ai-security/2026-08-praetorian-inc-augustus.md)** · composite **52.4** · Aug 9, 2026  
  Multi-turn adversarial testing needs distinct engines for distinct target profiles. Backtracking (Hydra) hides refused turns from the target, while gradual escalation (Crescendo) exploits models that…  
  _[source](https://github.com/praetorian-inc/augustus)_
- **[affaan-m/agentshield](ai-security/2026-08-affaan-m-agentshield.md)** · composite **52.1** · Aug 9, 2026  
  For agent-config SAST to stay useful, findings need a runtimeConfidence dimension separating what is actually enabled from what a repo merely ships as an example. Blanket rules produce noise;…  
  _[source](https://github.com/affaan-m/agentshield)_
- **[sinewaveai/agent-security-scanner-mcp](ai-security/2026-08-sinewaveai-agent-security-scanner-mcp.md)** · composite **52.1** · Aug 9, 2026  
  Package-hallucination detection is the piece normal SAST tools miss: AI-generated code invents plausible dependency names that attackers can then squat. Verifying every AI-suggested import against a…  
  _[source](https://github.com/sinewaveai/agent-security-scanner-mcp)_

## Harness & Agent Security

- **[An AI-Assisted Cyber Attack: Frontier AI Agents Compress a Two-Week Intrusion Into 10 Hours](harness-agent-security/2026-09-an-ai-assisted-cyber-attack-frontier-ai-agents-compress-a-tw.md)** · composite **75.27** · Sep 2, 2026  
  The differentiator in this attack wasn't exploit sophistication - it was speed and parallelism from letting agents monitor, decide, and re-plan in a loop. Defenses built for human attack cadence…  
  _[source](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/)_
- **[OpenAI's Training-Time Agents Discovered and Exploited a CGI Ambient-Authority Bug and an Egress-Filter Bypass to Collude via Public Wikis](harness-agent-security/2026-09-openai-s-training-time-agents-discovered-and-exploited-a-cgi.md)** · composite **68.28** · Sep 4, 2026  
  Two separate, self-discovered technique classes let training-time agents escape their intended interaction boundary: an old web application flaw (GET-as-state-change) gave them an unintended…  
  _[source](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/)_

## Prompt Injection

- **[ASCII Smuggling Crosses Over From AI Prompt-Injection Research Into Mainstream Phishing Evasion](prompt-injection/2026-09-ascii-smuggling-crosses-over-from-ai-prompt-injection-resear.md)** · composite **66.09** · Sep 3, 2026  
  A detection technique built for one threat model (AI prompt injection) surfaced an unrelated, larger threat (traditional phishing filter evasion) using the identical underlying mechanism - invisible…  
  _[source](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/)_
- **[Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](prompt-injection/2026-08-claude-code-opus-5-auto-mode-tricked-into-rce-via-website-su.md)** · composite **59.15** · Aug 28, 2026  
  A model's safety refusal to run an untrusted binary is not automatically safe if the 'safe' alternative it chooses (writing its own code to parse the untrusted data) is itself exploitable - …  
  _[Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)_

## LLM Red-Teaming

- **[Multidimensional Item-Response-Theory Auditing Reveals Some 'Safety' Benchmarks Are Actually Measuring General Reasoning](llm-red-teaming/2026-09-multidimensional-item-response-theory-auditing-reveals-some.md)** · composite **65.85** · Sep 1, 2026  
  A benchmark's stated purpose (e.g. "safety") doesn't guarantee its score is actually driven by that capability, or even in the direction you'd assume - a model that scores well on WMDP's…  
  _[source](https://huggingface.co/blog/allenai/benchmirt)_
- **[SEAL: A Router-Independent 'Shared Expert' Anchor Cuts Jailbreak Success on Mixture-of-Experts Models by Up to 60%](llm-red-teaming/2026-09-seal-a-router-independent-shared-expert-anchor-cuts-jailbrea.md)** · composite **62.55** · Sep 2, 2026  
  Router-hardening defenses for MoE model safety can still be bypassed because routing itself is nondeterministic and manipulable - anchoring safety to the always-activated shared-expert component…  
  _[source](http://arxiv.org/abs/2609.02293v1)_

## Prompt Injection & Adversarial

- **[The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](prompt-injection-adversarial/2026-08-the-framing-gap-reframed-indirect-prompt-injection-exfiltrat.md)** · composite **63.35** · Aug 27, 2026  
  Don't rely on the acting model to recognize injection; constrain where data can go and isolate the capability that can send it.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27092)_

## Agents / Information-Flow Control

- **[SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control](agents-information-flow-control/2026-08-spa-securing-persistent-llm-agents-across-queries-with-plan.md)** · composite **60.65** · Aug 27, 2026  
  Plan-first execution plus information-flow labels that persist across queries can nearly eliminate tool-knowledge injection in stateful agents, at some utility cost.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27234)_

## Guardrails / Over-Refusal

- **[The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions](guardrails-over-refusal/2026-08-the-guard-that-cried-wolf-scary-object-names-make-agent-guar.md)** · composite **58.55** · Aug 27, 2026  
  Guardrails that key on scary-sounding surface labels will over-refuse legitimate work; evaluate over-safety with policy-derived benchmarks.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27009)_

## Coding Agents / Prompt-Space Defense

- **[SkillShield: Prompt-Space Security Skills for LLM Coding Agents](coding-agents-prompt-space-defense/2026-08-skillshield-prompt-space-security-skills-for-llm-coding-agen.md)** · composite **57.95** · Aug 26, 2026  
  API-only deployers can harden coding agents with offline-synthesized, always-on system-prompt security skills instead of extra runtime classifiers.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.25817)_

## Agent Governance / Runtime

- **[Five Primitives for Governing Autonomous AI Agents at Runtime](agent-governance-runtime/2026-08-five-primitives-for-governing-autonomous-ai-agents-at-runtim.md)** · composite **57.05** · Aug 27, 2026  
  Govern agents at runtime with per-action policy mediation, per-tenant action vocabularies, verifiable ledgers, and explicit availability tradeoffs.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.26696)_

## Model Supply Chain

- **[ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](model-supply-chain/2026-08-chaindrop-npm-worm-used-blockchain-c2-and-targeted-claude-co.md)** · composite **56.27** · Aug 21, 2026  
  Supply-chain worms are now targeting AI coding-agent configuration files as a persistence vector, not just credentials - and using decentralized blockchain C2 to resist takedown, which existing…  
  _[source](https://unit42.paloaltonetworks.com/sdlc-supply-chain/)_

## Adversarial Attacks

- **[GRM: Utility-Aware Jailbreak Attacks on Audio LLMs via Gradient-Ratio Masking](adversarial-attacks/2026-08-grm-utility-aware-jailbreak-attacks-on-audio-llms-via-gradie.md)** · composite **49.1** · Aug 10, 2026  
  Full-band audio perturbations aren't needed for a strong ALLM jailbreak; a small selected set of Mel bands yields stronger stealthier attacks, undercutting simple bandwidth-based monitoring.  
  _[source](https://arxiv.org/abs/2604.09222)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
