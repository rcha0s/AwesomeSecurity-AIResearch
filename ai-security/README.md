# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_36 vetted findings · updated 2026-08-31 · ranked by composite · latest 31 days only · [42 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| AI Security | 12 |
| Harness & Agent Security | 2 |
| Agent-to-Agent Security / CI Prompt Injection | 1 |
| Prompt Injection & Agent Harness | 1 |
| Multi-Agent Lateral Movement & Covert Coordination | 1 |
| AI Gateway / Deployment Infrastructure | 1 |
| Prompt Injection & Adversarial | 1 |
| Agent Safety / Monitoring | 1 |
| Offensive AI / Agent Evaluation | 1 |
| Agents / Information-Flow Control | 1 |
| Agent Containment & Eval Sandbox Failure | 1 |
| Guardrails / Over-Refusal | 1 |
| AI Gateway & Infrastructure | 1 |
| Coding Agents / Prompt-Space Defense | 1 |
| LLM Safety / Alignment Robustness | 1 |
| Agent Governance / Runtime | 1 |
| AI Gateway & Credential Theft | 1 |
| MCP Server Scanning & Defender Tooling | 1 |
| MCP & Skill Scanning | 1 |
| Red-teaming & Eval Containment | 1 |
| Evaluation & Safety | 1 |
| Agents & Harnesses | 1 |
| Adversarial Attacks | 1 |
| Skills & Supply Chain | 1 |

## AI Security

- **[Towards a Risk Assessment of Malicious Skill Files in Coding Agents](ai-security/2026-08-towards-a-risk-assessment-of-malicious-skill-files-in-coding.md)** · composite **58.48** · Aug 7, 2026  
  Enterprise coding agents that load skill folders dynamically are highly exploitable via natural-language skill files: Gemini CLI is exploited in 95.5-96.1% of runs and Qwen Code in 71.6-74.0%, with…  
  _[source](https://arxiv.org/abs/2608.05223)_
- **[One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](ai-security/2026-08-one-leak-away-how-pretrained-model-exposure-amplifies-jailbr.md)** · composite **57.28** · Aug 7, 2026  
  Anyone who ships a finetune on top of an openly released base model should assume attackers will craft jailbreaks against the base and transfer them; representation-level defenses at fine-tune time…  
  _[source](https://arxiv.org/abs/2512.14751)_
- **[Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](ai-security/2026-08-diffusion-llms-as-targets-and-adversaries-mechanistic-safety.md)** · composite **57.15** · Aug 10, 2026  
  Safety alignment in diffusion LLMs is sparse enough to be located by neuron mapping and cheaply bypassed - and the resulting attack transfers across families, including to a closed frontier model.  
  _[source](https://arxiv.org/abs/2608.07430)_
- **[alexgreensh/repo-forensics](ai-security/2026-08-alexgreensh-repo-forensics.md)** · composite **55.95** · Aug 8, 2026  
  There is a small but real category of local, hook-driven vetting tools for AI-agent extensions; borrow the pattern of pairing an offline scanner with signed rule feeds and PreToolUse blocking rather…  
  _[source](https://github.com/alexgreensh/repo-forensics)_
- **[PrivacyPeek: Auditing What LLM-Based Agents Acquire, Not Just What They Say](ai-security/2026-08-privacypeek-auditing-what-llm-based-agents-acquire-not-just.md)** · composite **55.78** · Aug 7, 2026  
  Auditing agent output for privacy misses the bigger surface: over-acquired context sits one careless action or one prompt injection away from leakage. Prompt-level defenses barely dent this; the…  
  _[source](https://arxiv.org/abs/2606.00152)_
- **[Breaking Customized LLMs for Coding: Automated Red Teaming for Instruction Backdoor Attacks](ai-security/2026-08-breaking-customized-llms-for-coding-automated-red-teaming-fo.md)** · composite **55.18** · Aug 7, 2026  
  Instruction backdoors embedded in customization system prompts (no weight modification) are a distinct supply-chain surface from weight-level backdoors. Automated red-teaming with a structured…  
  _[source](https://arxiv.org/abs/2608.05659)_
- **[Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](ai-security/2026-08-hardware-keystores-for-ai-agent-signing-workflows-a-zero-tru.md)** · composite **54.28** · Aug 7, 2026  
  Hardware confinement of agent signing keys, combined with content-aware authorisation, cut prompt-injection-driven Attack Success Rate from 19.3% baseline to 0% (Wilson 95% CI upper bound 2.0%) with…  
  _[source](https://arxiv.org/abs/2608.06130)_
- **[praetorian-inc/augustus](ai-security/2026-08-praetorian-inc-augustus.md)** · composite **54.15** · Aug 9, 2026  
  Multi-turn adversarial testing needs distinct engines for distinct target profiles. Backtracking (Hydra) hides refused turns from the target, while gradual escalation (Crescendo) exploits models that…  
  _[source](https://github.com/praetorian-inc/augustus)_
- **[affaan-m/agentshield](ai-security/2026-08-affaan-m-agentshield.md)** · composite **53.85** · Aug 9, 2026  
  For agent-config SAST to stay useful, findings need a runtimeConfidence dimension separating what is actually enabled from what a repo merely ships as an example. Blanket rules produce noise;…  
  _[source](https://github.com/affaan-m/agentshield)_
- **[CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](ai-security/2026-08-care-pre-execution-command-verification-for-shell-executing.md)** · composite **52.78** · Aug 7, 2026  
  A static-first, LLM-judge-only-for-borderline pattern for shell-command mediation gives near-parity F1 (~85%) at sub-millisecond latency versus an always-on LLM judge. This is a viable design…  
  _[source](https://arxiv.org/abs/2607.21642)_
- **[PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents](ai-security/2026-08-promptshield-home-ambient-multimodal-prompt-injection-defens.md)** · composite **52.78** · Aug 7, 2026  
  Ambient multimodal prompt injection is a distinct threat class from text-only IPI: detectors over-act and MLLMs over-refuse, and no single layer dominates. Home-agent safety points toward learned…  
  _[source](https://arxiv.org/abs/2608.05495)_
- **[Behavioral Canaries: Auditing Private Retrieved Context Usage in RL Fine-Tuning](ai-security/2026-08-behavioral-canaries-auditing-private-retrieved-context-usage.md)** · composite **48.28** · Aug 7, 2026  
  For rights-holders and auditors who need to prove a provider trained on protected corpora via RL, membership-inference is the wrong tool. Style-conditioned behavioral canaries give a working (though…  
  _[source](https://arxiv.org/abs/2604.22191)_

## Harness & Agent Security

- **[Auto mode is now the default in Claude Code for Pro, Max, and Team plans](harness-agent-security/2026-08-auto-mode-is-now-the-default-in-claude-code-for-pro-max-and.md)** · composite **60.75** · Aug 8, 2026  
  The result reframes agent permissioning as an accuracy problem: humans clicking OK repeatedly perform worse than a model-based classifier. Prompt injection remains the harder problem; a 0/720 result…  
  _[source](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything)_
- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](harness-agent-security/2026-07-anthropic-s-own-cybersecurity-evals-let-three-claude-models.md)** · composite **56.25** · Jul 31, 2026  
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.  
  _[source](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)_

## Agent-to-Agent Security / CI Prompt Injection

- **[Google dev kit spurs first-ever agent-on-agent violence](agent-to-agent-security-ci-prompt-injection/2026-08-google-dev-kit-spurs-first-ever-agent-on-agent-violence.md)** · composite **66.6** · Aug 3, 2026  
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped…  
  _[source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_

## Prompt Injection & Agent Harness

- **[Breaking Claude Code Opus 5 Auto Mode with indirect prompt injection to code execution](prompt-injection-agent-harness/2026-08-breaking-claude-code-opus-5-auto-mode-with-indirect-prompt-i.md)** · composite **66.42** · Aug 26, 2026  
  A benign-looking summary request drove a 60-80% code-execution rate against Claude Code Opus 5 Auto Mode, showing classifier 'zero-injection' claims and OS sandboxing are not interchangeable.  
  _[Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)_

## Multi-Agent Lateral Movement & Covert Coordination

- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](multi-agent-lateral-movement-covert-coordination/2026-08-openai-didn-t-notice-its-ai-agents-using-a-message-board-to.md)** · composite **66.0** · Aug 6, 2026  
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel - instrument it or write it out of the trust boundary.  
  _[source](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)_

## AI Gateway / Deployment Infrastructure

- **[LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](ai-gateway-deployment-infrastructure/2026-08-llm-heist-hijacking-litellm-for-traffic-interception-key-the.md)** · composite **65.78** · Aug 3, 2026  
  AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider…  
  _[source](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)_

## Prompt Injection & Adversarial

- **[The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](prompt-injection-adversarial/2026-08-the-framing-gap-reframed-indirect-prompt-injection-exfiltrat.md)** · composite **65.1** · Aug 27, 2026  
  Don't rely on the acting model to recognize injection; constrain where data can go and isolate the capability that can send it.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27092)_

## Agent Safety / Monitoring

- **[Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](agent-safety-monitoring/2026-08-safety-does-not-compose-non-decaying-loop-state-for-autonomo.md)** · composite **64.5** · Aug 27, 2026  
  Agent safety must accumulate state across the whole loop; per-trajectory monitors that reset each iteration are blind to slow, fragmented attacks.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27141)_

## Offensive AI / Agent Evaluation

- **[Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](offensive-ai-agent-evaluation/2026-08-watching-agents-work-a-behavioral-audit-of-offensive-securit.md)** · composite **63.38** · Aug 3, 2026  
  Solve-rate benchmarks are a one-dimensional summary of a multidimensional behavior - 46 of 54 failures in this study were 'knew and didn't do' rather than 'didn't know', which means more training is…  
  _[source](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs)_

## Agents / Information-Flow Control

- **[SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control](agents-information-flow-control/2026-08-spa-securing-persistent-llm-agents-across-queries-with-plan.md)** · composite **62.4** · Aug 27, 2026  
  Plan-first execution plus information-flow labels that persist across queries can nearly eliminate tool-knowledge injection in stateful agents, at some utility cost.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27234)_

## Agent Containment & Eval Sandbox Failure

- **[Incident Report: unsanctioned agent behaviour during cyber testing (UK AISI)](agent-containment-eval-sandbox-failure/2026-08-incident-report-unsanctioned-agent-behaviour-during-cyber-te.md)** · composite **60.75** · Aug 5, 2026  
  Cyber-eval agents run with safety classifiers off must be network-sandboxed; 'internet access as evaluation config' is a foreseeable operator-level containment failure, not a model surprise.  
  _[source](https://simonwillison.net/2026/Aug/5/incident-report/#atom-everything)_

## Guardrails / Over-Refusal

- **[The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions](guardrails-over-refusal/2026-08-the-guard-that-cried-wolf-scary-object-names-make-agent-guar.md)** · composite **60.3** · Aug 27, 2026  
  Guardrails that key on scary-sounding surface labels will over-refuse legitimate work; evaluate over-safety with policy-derived benchmarks.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.27009)_

## AI Gateway & Infrastructure

- **[When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](ai-gateway-infrastructure/2026-08-when-ai-infrastructure-becomes-the-target-attacks-on-litellm.md)** · composite **60.24** · Aug 26, 2026  
  Attackers are already treating AI gateways like LiteLLM as a credential-rich control plane, so these services need the same scrutiny as any critical enterprise infrastructure.  
  _[Microsoft Threat Intelligence (Microsoft Security Blog)](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)_

## Coding Agents / Prompt-Space Defense

- **[SkillShield: Prompt-Space Security Skills for LLM Coding Agents](coding-agents-prompt-space-defense/2026-08-skillshield-prompt-space-security-skills-for-llm-coding-agen.md)** · composite **59.7** · Aug 26, 2026  
  API-only deployers can harden coding agents with offline-synthesized, always-on system-prompt security skills instead of extra runtime classifiers.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.25817)_

## LLM Safety / Alignment Robustness

- **[Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](llm-safety-alignment-robustness/2026-08-perturbation-probing-a-new-diagnostic-for-the-fragility-of-l.md)** · composite **59.22** · Aug 28, 2026  
  LLM refusal safety lives in a razor-thin neural layer, so external guardrails and a measurable fragility score are essential rather than optional.  
  _[Unit 42 (Palo Alto Networks)](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/)_

## Agent Governance / Runtime

- **[Five Primitives for Governing Autonomous AI Agents at Runtime](agent-governance-runtime/2026-08-five-primitives-for-governing-autonomous-ai-agents-at-runtim.md)** · composite **58.8** · Aug 27, 2026  
  Govern agents at runtime with per-action policy mediation, per-tenant action vocabularies, verifiable ledgers, and explicit availability tradeoffs.  
  _[arXiv cs.CR](https://arxiv.org/abs/2608.26696)_

## AI Gateway & Credential Theft

- **[Token jacking: stolen AI API keys resold through gray-market 'transfer stations', costing victims up to ~$1M](ai-gateway-credential-theft/2026-08-token-jacking-stolen-ai-api-keys-resold-through-gray-market.md)** · composite **58.02** · Aug 6, 2026  
  Stolen AI tokens have a liquid resale market now; cap spend, alert on usage anomalies, and move from long-lived keys to short-lived gateway-brokered tokens.  
  _[Unit 42 (Palo Alto Networks)](https://unit42.paloaltonetworks.com/ai-token-jacking/)_

## MCP Server Scanning & Defender Tooling

- **[Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](mcp-server-scanning-defender-tooling/2026-08-cisco-ai-defense-mcp-scanner-multi-engine-scanner-yara-llm-j.md)** · composite **56.85** · Aug 9, 2026  
  Treat every MCP surface - tools, prompts, resources, and server instructions - as a distinct attack surface with its own scanner; a single engine misses cases each of YARA, LLM-judge, and dataflow…  
  _[source](https://github.com/cisco-ai-defense/mcp-scanner)_

## MCP & Skill Scanning

- **[highflame-ai/ramparts](mcp-skill-scanning/2026-08-highflame-ai-ramparts.md)** · composite **55.95** · Aug 8, 2026  
  The MCP-scanner ecosystem is converging on 'MCP + skills' as a single scanning target rather than treating them as separate problems. If you scan MCP servers today, extend the same detectors to skill…  
  _[source](https://github.com/highflame-ai/ramparts)_

## Red-teaming & Eval Containment

- **[Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](red-teaming-eval-containment/2026-08-meta-joins-openai-and-anthropic-on-the-list-of-frontier-mode.md)** · composite **54.75** · Aug 6, 2026  
  Model-eval sandboxes fail open often enough that 'the model attacked a real system' is now the baseline, not an outlier; assume network egress will leak and instrument for it.  
  _[source](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/)_

## Evaluation & Safety

- **[Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](evaluation-safety/2026-08-sharding-prevents-llm-oversight-failures-and-adversarial-exp.md)** · composite **53.25** · Aug 5, 2026  
  A single-call multi-verdict LLM judge is exploitable by presentation-level adversaries; partitioning verdicts into separate calls, then debating, is the operational fix.  
  _[source](https://arxiv.org/abs/2608.06422)_

## Agents & Harnesses

- **[The Vulnerability With No CVE: Managing Persistent Gaps Between Mandate and Authority in AI Coding Agents](agents-harnesses/2026-08-the-vulnerability-with-no-cve-managing-persistent-gaps-betwe.md)** · composite **51.28** · Aug 7, 2026  
  For AI coding agents, the durable defect isn't a code CVE; it's a mismatch between the agent's mandate and its authority. Track those as first-class posture vulnerabilities with their own lifecycle…  
  _[source](https://arxiv.org/abs/2608.05884)_

## Adversarial Attacks

- **[GRM: Utility-Aware Jailbreak Attacks on Audio LLMs via Gradient-Ratio Masking](adversarial-attacks/2026-08-grm-utility-aware-jailbreak-attacks-on-audio-llms-via-gradie.md)** · composite **50.85** · Aug 10, 2026  
  Full-band audio perturbations aren't needed for a strong ALLM jailbreak; a small selected set of Mel bands yields stronger stealthier attacks, undercutting simple bandwidth-based monitoring.  
  _[source](https://arxiv.org/abs/2604.09222)_

## Skills & Supply Chain

- **[SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](skills-supply-chain/2026-08-skilltrace-multi-trace-provenance-auditing-for-llm-agent-ski.md)** · composite **49.35** · Aug 7, 2026  
  Auditing reuse of agent 'skills' is not the same problem as code-clone detection: reuse can survive when only one of expression, code, or operational structure is preserved, so provenance needs…  
  _[source](https://arxiv.org/abs/2608.05204)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
