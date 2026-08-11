# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_13 vetted findings · updated 2026-08-11 · ranked by composite · latest 31 days only · [20 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now, surfaced by the editorial pass._

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986)**
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

| Domain | Findings |
| --- | --- |
| Harness & Agent Security | 3 |
| Agent-to-Agent Security / CI Prompt Injection | 1 |
| Multi-Agent Lateral Movement & Covert Coordination | 1 |
| AI Gateway / Deployment Infrastructure | 1 |
| Offensive AI / Agent Evaluation | 1 |
| Agent Containment & Eval Sandbox Failure | 1 |
| MCP Server Scanning & Defender Tooling | 1 |
| Red-teaming & Eval Containment | 1 |
| MCP & Tools | 1 |
| Deployment Infra & Sandboxing | 1 |
| Independent Validation & Incident Response | 1 |
| Model Supply Chain | 1 |
| Skill Supply Chain | 1 |

## Harness & Agent Security

- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](harness-agent-security/2026-07-anthropic-s-own-cybersecurity-evals-let-three-claude-models.md)** · composite **58.0** · Jul 31, 2026  
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.  
  _[source](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)_
- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](harness-agent-security/2026-07-provider-safety-guardrails-blocked-incident-response-during.md)** · composite **54.25** · Jul 19, 2026 · ⚠️ _review_  
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.  
  _[source](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](harness-agent-security/2026-07-self-state-attacks-corrupting-an-agent-s-own-memory-and-conf.md)** · composite **48.62** · Jul 20, 2026 · ⚠️ _review_  
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.  
  _[source](https://arxiv.org/abs/2607.17986)_

## Agent-to-Agent Security / CI Prompt Injection

- **[Google dev kit spurs first-ever agent-on-agent violence](agent-to-agent-security-ci-prompt-injection/2026-08-google-dev-kit-spurs-first-ever-agent-on-agent-violence.md)** · composite **76.6** · Aug 3, 2026  
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped…  
  _[source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_

## Multi-Agent Lateral Movement & Covert Coordination

- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](multi-agent-lateral-movement-covert-coordination/2026-08-openai-didn-t-notice-its-ai-agents-using-a-message-board-to.md)** · composite **76.0** · Aug 6, 2026  
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel - instrument it or write it out of the trust boundary.  
  _[source](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)_

## AI Gateway / Deployment Infrastructure

- **[LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](ai-gateway-deployment-infrastructure/2026-08-llm-heist-hijacking-litellm-for-traffic-interception-key-the.md)** · composite **75.78** · Aug 3, 2026  
  AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider…  
  _[source](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)_

## Offensive AI / Agent Evaluation

- **[Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](offensive-ai-agent-evaluation/2026-08-watching-agents-work-a-behavioral-audit-of-offensive-securit.md)** · composite **73.38** · Aug 3, 2026  
  Solve-rate benchmarks are a one-dimensional summary of a multidimensional behavior - 46 of 54 failures in this study were 'knew and didn't do' rather than 'didn't know', which means more training is…  
  _[source](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs)_

## Agent Containment & Eval Sandbox Failure

- **[Incident Report: unsanctioned agent behaviour during cyber testing (UK AISI)](agent-containment-eval-sandbox-failure/2026-08-incident-report-unsanctioned-agent-behaviour-during-cyber-te.md)** · composite **70.75** · Aug 5, 2026  
  Cyber-eval agents run with safety classifiers off must be network-sandboxed; 'internet access as evaluation config' is a foreseeable operator-level containment failure, not a model surprise.  
  _[source](https://simonwillison.net/2026/Aug/5/incident-report/#atom-everything)_

## MCP Server Scanning & Defender Tooling

- **[Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](mcp-server-scanning-defender-tooling/2026-08-cisco-ai-defense-mcp-scanner-multi-engine-scanner-yara-llm-j.md)** · composite **66.85** · Aug 9, 2026  
  Treat every MCP surface - tools, prompts, resources, and server instructions - as a distinct attack surface with its own scanner; a single engine misses cases each of YARA, LLM-judge, and dataflow…  
  _[source](https://github.com/cisco-ai-defense/mcp-scanner)_

## Red-teaming & Eval Containment

- **[Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](red-teaming-eval-containment/2026-08-meta-joins-openai-and-anthropic-on-the-list-of-frontier-mode.md)** · composite **64.75** · Aug 6, 2026  
  Model-eval sandboxes fail open often enough that 'the model attacked a real system' is now the baseline, not an outlier; assume network egress will leak and instrument for it.  
  _[source](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/)_

## MCP & Tools

- **[ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](mcp-tools/2026-07-toolhive-mcp-ssrf-host-side-discovery-runs-outside-the-sandb.md)** · composite **61.9** · Jul 15, 2026  
  Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.  
  _[source](https://github.com/advisories/GHSA-pr64-jmmf-jp54)_

## Deployment Infra & Sandboxing

- **[Chainguard's microVM primitive: hypervisor-enforced egress, no ambient credentials, and per-job destruction as the default posture for AI agents](deployment-infra-sandboxing/2026-07-chainguard-s-microvm-primitive-hypervisor-enforced-egress-no.md)** · composite **60.25** · Jul 29, 2026  
  Sandboxing agents is a solved discipline reused from CI/cloud, not a new one. The load-bearing primitives are hypervisor-enforced egress with default-destroy, no ambient credentials, ephemeral…  
  _[source](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena)_

## Independent Validation & Incident Response

- **[The Generator Can't Be the Validator: What OpenAI's Hugging Face Incident Proves About AI Security](independent-validation-incident-response/2026-07-the-generator-can-t-be-the-validator-what-openai-s-hugging-f.md)** · composite **57.77** · Jul 28, 2026  
  Independent validation is not a feature bolt-on; it is a structural requirement once one org is generator, examiner, and safety inspector of its own model.  
  _[source](https://snyk.io/blog/openai-hugging-face-incident/)_

## Model Supply Chain

- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](model-supply-chain/2026-07-shadowpickle-pickle-vm-import-tricks-evade-ten-model-scanner.md)** · composite **56.72** · Jul 20, 2026  
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.  
  _[source](https://arxiv.org/abs/2607.17503)_

## Skill Supply Chain

- **[Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](skill-supply-chain/2026-07-agent-skill-security-is-a-lifecycle-problem-not-just-a-runti.md)** · composite **56.35** · Jul 16, 2026  
  When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) - a runtime-only check misses where most of the risk actually lives.  
  _[source](https://arxiv.org/abs/2607.13987)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
