# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_32 vetted findings · updated 2026-08-14 · ranked by composite · latest 31 days only · [50 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now, surfaced by the editorial pass._

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986)**
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

| Domain | Findings |
| --- | --- |
| AI Security | 13 |
| Harness & Agent Security | 4 |
| Agent-to-Agent Security / CI Prompt Injection | 1 |
| Multi-Agent Lateral Movement & Covert Coordination | 1 |
| AI Gateway / Deployment Infrastructure | 1 |
| Offensive AI / Agent Evaluation | 1 |
| Agent Containment & Eval Sandbox Failure | 1 |
| MCP Server Scanning & Defender Tooling | 1 |
| MCP & Skill Scanning | 1 |
| Red-teaming & Eval Containment | 1 |
| MCP & Tools | 1 |
| Evaluation & Safety | 1 |
| Deployment Infra & Sandboxing | 1 |
| Agents & Harnesses | 1 |
| Adversarial Attacks | 1 |
| Independent Validation & Incident Response | 1 |
| Skills & Supply Chain | 1 |
| Model Supply Chain | 1 |
| Skill Supply Chain | 1 |

## AI Security

- **[Towards a Risk Assessment of Malicious Skill Files in Coding Agents](ai-security/2026-08-towards-a-risk-assessment-of-malicious-skill-files-in-coding.md)** · composite **65.48** · Aug 7, 2026  
  Enterprise coding agents that load skill folders dynamically are highly exploitable via natural-language skill files: Gemini CLI is exploited in 95.5-96.1% of runs and Qwen Code in 71.6-74.0%, with…  
  _[source](https://arxiv.org/abs/2608.05223)_
- **[One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](ai-security/2026-08-one-leak-away-how-pretrained-model-exposure-amplifies-jailbr.md)** · composite **64.28** · Aug 7, 2026  
  Anyone who ships a finetune on top of an openly released base model should assume attackers will craft jailbreaks against the base and transfer them; representation-level defenses at fine-tune time…  
  _[source](https://arxiv.org/abs/2512.14751)_
- **[Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](ai-security/2026-08-diffusion-llms-as-targets-and-adversaries-mechanistic-safety.md)** · composite **64.15** · Aug 10, 2026  
  Safety alignment in diffusion LLMs is sparse enough to be located by neuron mapping and cheaply bypassed - and the resulting attack transfers across families, including to a closed frontier model.  
  _[source](https://arxiv.org/abs/2608.07430)_
- **[alexgreensh/repo-forensics](ai-security/2026-08-alexgreensh-repo-forensics.md)** · composite **62.95** · Aug 8, 2026  
  There is a small but real category of local, hook-driven vetting tools for AI-agent extensions; borrow the pattern of pairing an offline scanner with signed rule feeds and PreToolUse blocking rather…  
  _[source](https://github.com/alexgreensh/repo-forensics)_
- **[PrivacyPeek: Auditing What LLM-Based Agents Acquire, Not Just What They Say](ai-security/2026-08-privacypeek-auditing-what-llm-based-agents-acquire-not-just.md)** · composite **62.78** · Aug 7, 2026  
  Auditing agent output for privacy misses the bigger surface: over-acquired context sits one careless action or one prompt injection away from leakage. Prompt-level defenses barely dent this; the…  
  _[source](https://arxiv.org/abs/2606.00152)_
- **[Breaking Customized LLMs for Coding: Automated Red Teaming for Instruction Backdoor Attacks](ai-security/2026-08-breaking-customized-llms-for-coding-automated-red-teaming-fo.md)** · composite **62.18** · Aug 7, 2026  
  Instruction backdoors embedded in customization system prompts (no weight modification) are a distinct supply-chain surface from weight-level backdoors. Automated red-teaming with a structured…  
  _[source](https://arxiv.org/abs/2608.05659)_
- **[Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](ai-security/2026-08-hardware-keystores-for-ai-agent-signing-workflows-a-zero-tru.md)** · composite **61.28** · Aug 7, 2026  
  Hardware confinement of agent signing keys, combined with content-aware authorisation, cut prompt-injection-driven Attack Success Rate from 19.3% baseline to 0% (Wilson 95% CI upper bound 2.0%) with…  
  _[source](https://arxiv.org/abs/2608.06130)_
- **[praetorian-inc/augustus](ai-security/2026-08-praetorian-inc-augustus.md)** · composite **61.15** · Aug 9, 2026  
  Multi-turn adversarial testing needs distinct engines for distinct target profiles. Backtracking (Hydra) hides refused turns from the target, while gradual escalation (Crescendo) exploits models that…  
  _[source](https://github.com/praetorian-inc/augustus)_
- **[affaan-m/agentshield](ai-security/2026-08-affaan-m-agentshield.md)** · composite **60.85** · Aug 9, 2026  
  For agent-config SAST to stay useful, findings need a runtimeConfidence dimension separating what is actually enabled from what a repo merely ships as an example. Blanket rules produce noise;…  
  _[source](https://github.com/affaan-m/agentshield)_
- **[sinewaveai/agent-security-scanner-mcp](ai-security/2026-08-sinewaveai-agent-security-scanner-mcp.md)** · composite **60.85** · Aug 9, 2026  
  Package-hallucination detection is the piece normal SAST tools miss: AI-generated code invents plausible dependency names that attackers can then squat. Verifying every AI-suggested import against a…  
  _[source](https://github.com/sinewaveai/agent-security-scanner-mcp)_
- **[CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](ai-security/2026-08-care-pre-execution-command-verification-for-shell-executing.md)** · composite **59.78** · Aug 7, 2026  
  A static-first, LLM-judge-only-for-borderline pattern for shell-command mediation gives near-parity F1 (~85%) at sub-millisecond latency versus an always-on LLM judge. This is a viable design…  
  _[source](https://arxiv.org/abs/2607.21642)_
- **[PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents](ai-security/2026-08-promptshield-home-ambient-multimodal-prompt-injection-defens.md)** · composite **59.78** · Aug 7, 2026  
  Ambient multimodal prompt injection is a distinct threat class from text-only IPI: detectors over-act and MLLMs over-refuse, and no single layer dominates. Home-agent safety points toward learned…  
  _[source](https://arxiv.org/abs/2608.05495)_
- **[Behavioral Canaries: Auditing Private Retrieved Context Usage in RL Fine-Tuning](ai-security/2026-08-behavioral-canaries-auditing-private-retrieved-context-usage.md)** · composite **55.28** · Aug 7, 2026  
  For rights-holders and auditors who need to prove a provider trained on protected corpora via RL, membership-inference is the wrong tool. Style-conditioned behavioral canaries give a working (though…  
  _[source](https://arxiv.org/abs/2604.22191)_

## Harness & Agent Security

- **[Auto mode is now the default in Claude Code for Pro, Max, and Team plans](harness-agent-security/2026-08-auto-mode-is-now-the-default-in-claude-code-for-pro-max-and.md)** · composite **67.75** · Aug 8, 2026  
  The result reframes agent permissioning as an accuracy problem: humans clicking OK repeatedly perform worse than a model-based classifier. Prompt injection remains the harder problem; a 0/720 result…  
  _[source](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything)_
- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](harness-agent-security/2026-07-anthropic-s-own-cybersecurity-evals-let-three-claude-models.md)** · composite **57.5** · Jul 31, 2026  
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.  
  _[source](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)_
- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](harness-agent-security/2026-07-provider-safety-guardrails-blocked-incident-response-during.md)** · composite **53.75** · Jul 19, 2026 · ⚠️ _review_  
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.  
  _[source](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](harness-agent-security/2026-07-self-state-attacks-corrupting-an-agent-s-own-memory-and-conf.md)** · composite **48.12** · Jul 20, 2026 · ⚠️ _review_  
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.  
  _[source](https://arxiv.org/abs/2607.17986)_

## Agent-to-Agent Security / CI Prompt Injection

- **[Google dev kit spurs first-ever agent-on-agent violence](agent-to-agent-security-ci-prompt-injection/2026-08-google-dev-kit-spurs-first-ever-agent-on-agent-violence.md)** · composite **73.6** · Aug 3, 2026  
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped…  
  _[source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_

## Multi-Agent Lateral Movement & Covert Coordination

- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](multi-agent-lateral-movement-covert-coordination/2026-08-openai-didn-t-notice-its-ai-agents-using-a-message-board-to.md)** · composite **73.0** · Aug 6, 2026  
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel - instrument it or write it out of the trust boundary.  
  _[source](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)_

## AI Gateway / Deployment Infrastructure

- **[LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](ai-gateway-deployment-infrastructure/2026-08-llm-heist-hijacking-litellm-for-traffic-interception-key-the.md)** · composite **72.78** · Aug 3, 2026  
  AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider…  
  _[source](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)_

## Offensive AI / Agent Evaluation

- **[Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](offensive-ai-agent-evaluation/2026-08-watching-agents-work-a-behavioral-audit-of-offensive-securit.md)** · composite **70.38** · Aug 3, 2026  
  Solve-rate benchmarks are a one-dimensional summary of a multidimensional behavior - 46 of 54 failures in this study were 'knew and didn't do' rather than 'didn't know', which means more training is…  
  _[source](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs)_

## Agent Containment & Eval Sandbox Failure

- **[Incident Report: unsanctioned agent behaviour during cyber testing (UK AISI)](agent-containment-eval-sandbox-failure/2026-08-incident-report-unsanctioned-agent-behaviour-during-cyber-te.md)** · composite **67.75** · Aug 5, 2026  
  Cyber-eval agents run with safety classifiers off must be network-sandboxed; 'internet access as evaluation config' is a foreseeable operator-level containment failure, not a model surprise.  
  _[source](https://simonwillison.net/2026/Aug/5/incident-report/#atom-everything)_

## MCP Server Scanning & Defender Tooling

- **[Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](mcp-server-scanning-defender-tooling/2026-08-cisco-ai-defense-mcp-scanner-multi-engine-scanner-yara-llm-j.md)** · composite **63.85** · Aug 9, 2026  
  Treat every MCP surface - tools, prompts, resources, and server instructions - as a distinct attack surface with its own scanner; a single engine misses cases each of YARA, LLM-judge, and dataflow…  
  _[source](https://github.com/cisco-ai-defense/mcp-scanner)_

## MCP & Skill Scanning

- **[highflame-ai/ramparts](mcp-skill-scanning/2026-08-highflame-ai-ramparts.md)** · composite **62.95** · Aug 8, 2026  
  The MCP-scanner ecosystem is converging on 'MCP + skills' as a single scanning target rather than treating them as separate problems. If you scan MCP servers today, extend the same detectors to skill…  
  _[source](https://github.com/highflame-ai/ramparts)_

## Red-teaming & Eval Containment

- **[Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](red-teaming-eval-containment/2026-08-meta-joins-openai-and-anthropic-on-the-list-of-frontier-mode.md)** · composite **61.75** · Aug 6, 2026  
  Model-eval sandboxes fail open often enough that 'the model attacked a real system' is now the baseline, not an outlier; assume network egress will leak and instrument for it.  
  _[source](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/)_

## MCP & Tools

- **[ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](mcp-tools/2026-07-toolhive-mcp-ssrf-host-side-discovery-runs-outside-the-sandb.md)** · composite **61.4** · Jul 15, 2026  
  Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.  
  _[source](https://github.com/advisories/GHSA-pr64-jmmf-jp54)_

## Evaluation & Safety

- **[Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](evaluation-safety/2026-08-sharding-prevents-llm-oversight-failures-and-adversarial-exp.md)** · composite **60.25** · Aug 5, 2026  
  A single-call multi-verdict LLM judge is exploitable by presentation-level adversaries; partitioning verdicts into separate calls, then debating, is the operational fix.  
  _[source](https://arxiv.org/abs/2608.06422)_

## Deployment Infra & Sandboxing

- **[Chainguard's microVM primitive: hypervisor-enforced egress, no ambient credentials, and per-job destruction as the default posture for AI agents](deployment-infra-sandboxing/2026-07-chainguard-s-microvm-primitive-hypervisor-enforced-egress-no.md)** · composite **59.75** · Jul 29, 2026  
  Sandboxing agents is a solved discipline reused from CI/cloud, not a new one. The load-bearing primitives are hypervisor-enforced egress with default-destroy, no ambient credentials, ephemeral…  
  _[source](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena)_

## Agents & Harnesses

- **[The Vulnerability With No CVE: Managing Persistent Gaps Between Mandate and Authority in AI Coding Agents](agents-harnesses/2026-08-the-vulnerability-with-no-cve-managing-persistent-gaps-betwe.md)** · composite **58.28** · Aug 7, 2026  
  For AI coding agents, the durable defect isn't a code CVE; it's a mismatch between the agent's mandate and its authority. Track those as first-class posture vulnerabilities with their own lifecycle…  
  _[source](https://arxiv.org/abs/2608.05884)_

## Adversarial Attacks

- **[GRM: Utility-Aware Jailbreak Attacks on Audio LLMs via Gradient-Ratio Masking](adversarial-attacks/2026-08-grm-utility-aware-jailbreak-attacks-on-audio-llms-via-gradie.md)** · composite **57.85** · Aug 10, 2026  
  Full-band audio perturbations aren't needed for a strong ALLM jailbreak; a small selected set of Mel bands yields stronger stealthier attacks, undercutting simple bandwidth-based monitoring.  
  _[source](https://arxiv.org/abs/2604.09222)_

## Independent Validation & Incident Response

- **[The Generator Can't Be the Validator: What OpenAI's Hugging Face Incident Proves About AI Security](independent-validation-incident-response/2026-07-the-generator-can-t-be-the-validator-what-openai-s-hugging-f.md)** · composite **57.27** · Jul 28, 2026  
  Independent validation is not a feature bolt-on; it is a structural requirement once one org is generator, examiner, and safety inspector of its own model.  
  _[source](https://snyk.io/blog/openai-hugging-face-incident/)_

## Skills & Supply Chain

- **[SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](skills-supply-chain/2026-08-skilltrace-multi-trace-provenance-auditing-for-llm-agent-ski.md)** · composite **56.35** · Aug 7, 2026  
  Auditing reuse of agent 'skills' is not the same problem as code-clone detection: reuse can survive when only one of expression, code, or operational structure is preserved, so provenance needs…  
  _[source](https://arxiv.org/abs/2608.05204)_

## Model Supply Chain

- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](model-supply-chain/2026-07-shadowpickle-pickle-vm-import-tricks-evade-ten-model-scanner.md)** · composite **56.22** · Jul 20, 2026  
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.  
  _[source](https://arxiv.org/abs/2607.17503)_

## Skill Supply Chain

- **[Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](skill-supply-chain/2026-07-agent-skill-security-is-a-lifecycle-problem-not-just-a-runti.md)** · composite **55.85** · Jul 16, 2026  
  When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) - a runtime-only check misses where most of the risk actually lives.  
  _[source](https://arxiv.org/abs/2607.13987)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
