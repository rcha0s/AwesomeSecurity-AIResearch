# 📈 Emerging Trends

> Themes per topic, clustered from tagged findings (live + recent archive). Updated 2026-10-25. A theme needs ≥2 findings from ≥2 sources. **Rising** means at least 2 findings in the last 31 days and more than 1.0x what the theme's own rate over the prior 180 days predicts; **steady** has recent findings at or under that rate; **quiet** has none. Source and feed names (arxiv, ghsa, ...) are not themes.

## AI Security

### 🔺 rising coding-agents  ·  10 findings (4 recent vs 1.0 expected) · 6 sources
_First seen 2026-08-06 · latest 2026-10-22._

- [ProjectDiscovery backdoored Qwen2.5-7B with a cheap LoRA fine-tune; a trigger phrase made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [OpenAI: two GPT-6 coding agents weakened their own monitoring during routine tasks, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) (2026-10-20) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [SkillShield: Prompt-Space Security Skills for LLM Coding Agents](https://arxiv.org/abs/2608.25817) (2026-08-26)
- [fu351/Doberman-Core](https://github.com/fu351/Doberman-Core) (2026-08-10)

### 🔺 rising windows  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-13 · latest 2026-10-19._

- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Visual Studio Copilot and SSMS RCE (CVE-2026-103572): a trailing dot in a filename lets the agent rewrite its own config](https://embracethered.com/blog/posts/2026/visual-studio-copilot-remote-code-execution/) (2026-10-13) · _latest_

### 🔺 rising red-teaming  ·  5 findings (2 recent vs 0.5 expected) · 5 sources
_First seen 2026-08-06 · latest 2026-10-21._

- [Edge grounding VLMs fall to wearable adversarial patches like detectors, often with confident wrong boxes](http://arxiv.org/abs/2610.29196v1) (2026-10-21) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1) (2026-09-24) · _latest_
- [The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/) (2026-08-06)

### ▪️ steady prompt-injection  ·  32 findings (4 recent vs 4.7 expected) · 17 sources
_First seen 2026-02 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers, including Hydra, which erases refused turns](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Signals Corps: scanning 217 million responses finds 30 sites putting prompt injections in HTTP headers, mostly pranks](https://www.signalscorps.com/blog/prompt-injection-in-http-headers/) (2026-10-15) · _latest_
- [Visual Studio Copilot and SSMS RCE (CVE-2026-103572): a trailing dot in a filename lets the agent rewrite its own config](https://embracethered.com/blog/posts/2026/visual-studio-copilot-remote-code-execution/) (2026-10-13) · _latest_
- [APort Vault: across 14 models, human-written CTF attacks got 140 forbidden payments through the model alone and 0 behind a deterministic pre-action policy check](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [16-day test of eight multi-agent worlds: none resisted all three injected stresses, and agents acted on remembered threats up to 46 hours later](https://arxiv.org/abs/2609.17320) (2026-09-15)

### ▪️ steady mcp  ·  23 findings (3 recent vs 3.3 expected) · 13 sources
_First seen 2026-02 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers; missing credentials now fail closed](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default on streamable-http](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [mysql-mcp-server SSE transport skips the MCP SDK's Origin/Host checks, allowing unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)
- [MCP ZAP Server Hardens Its Own Attack Surface by Shipping a Distroless Runtime With No Shell or curl](https://github.com/dtkmn/mcp-zap-server) (2026-09-02)
- [BurpMCP-Ultra: 150-tool MCP server for Burp with scope-gate, host allowlist, and per-session token](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)

### ▪️ steady agent-security  ·  16 findings (2 recent vs 2.1 expected) · 14 sources
_First seen 2026-02 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Agent Mosaic: LLM agents combine individually allowed documents into forbidden conclusions, even with classification headers](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](https://arxiv.org/abs/2608.06130v1) (2026-08-07)
- [The Vulnerability With No CVE: Managing Persistent Gaps Between Mandate and Authority in AI Coding Agents](https://arxiv.org/abs/2608.05884) (2026-08-07)
- [Humans in the loop miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236) (2026-08-06)
- [AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24)

### ▪️ steady supply-chain  ·  14 findings (1 recent vs 2.2 expected) · 11 sources
_First seen 2026-06-23 · latest 2026-10-21._

- [LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) (2026-08-10)
- [Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) (2026-08-09)
- [alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics) (2026-08-08)

### ▪️ steady guardrails  ·  11 findings (1 recent vs 1.7 expected) · 7 sources
_First seen 2026-07-19 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [CC Safety Net Blocks Destructive Agent Commands by Parsing Command Intent, Not Pattern-Matching Strings](https://github.com/kenryu42/cc-safety-net) (2026-09-08)
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)
- [SkillShield: Prompt-Space Security Skills for LLM Coding Agents](https://arxiv.org/abs/2608.25817) (2026-08-26)
- [Pydantic AI Ships Official First-Party Guardrails, Upstreaming a Community Library](https://github.com/pydantic/pydantic-ai-harness) (2026-08-17)

### ▪️ steady sandboxing  ·  10 findings (1 recent vs 1.6 expected) · 8 sources
_First seen 2026-07-29 · latest 2026-10-23._

- [Anthropic: UK AISI cybertest incident review, where Mythos 5 posed as other users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [Omnigent: A Widely-Adopted (9,800+ Star) Meta-Harness Adds Policy Enforcement and Sandboxing Across Multiple Coding-Agent Backends](https://github.com/omnigent-ai/omnigent) (2026-09-09)
- [OpenClaw 2.0's Usability Overhaul Ships With Security Still Opt-In: Unencrypted Secrets, Sandbox Off by Default](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [OneCLI: Per-Employee Sandboxed Agents Behind a Credential-Injecting MITM Gateway, With Outbound-Only Runners](https://github.com/onecli/onecli) (2026-08-19)
- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [Humans in the loop miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236) (2026-08-06)

### ▪️ steady jailbreak  ·  9 findings (1 recent vs 1.2 expected) · 5 sources
_First seen 2025-12-14 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers, including Hydra, which erases refused turns](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)
- [Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](https://arxiv.org/abs/2608.07430) (2026-08-10)
- [CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310) (2026-08-10)
- [Minimal, Local, Causal Explanations for Jailbreak Success in Large Language Models](https://arxiv.org/abs/2605.00123) (2026-08-10)

### ▪️ steady benchmark  ·  8 findings (1 recent vs 1.2 expected) · 4 sources
_First seen 2026-05-29 · latest 2026-10-19._

- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1) (2026-09-24) · _latest_
- [APort Vault: across 14 models, human-written CTF attacks got 140 forbidden payments through the model alone and 0 behind a deterministic pre-action policy check](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [AgentLSD plants fake flags and decoy endpoints in capture-the-flag (CTF) challenges; traps add about 20 turns even when the agent still wins](http://arxiv.org/abs/2609.19140v1) (2026-09-16)
- [The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)
- [PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents](https://arxiv.org/abs/2608.05495) (2026-08-07)

### ▪️ steady alignment  ·  6 findings (1 recent vs 0.9 expected) · 6 sources
_First seen 2026-08-07 · latest 2026-10-23._

- [Anthropic: UK AISI cybertest incident review, where Mythos 5 posed as other users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [16-day test of eight multi-agent worlds: none resisted all three injected stresses, and agents acted on remembered threats up to 46 hours later](https://arxiv.org/abs/2609.17320) (2026-09-15)
- [SEAL: A Router-Independent 'Shared Expert' Anchor Cuts Jailbreak Success on Mixture-of-Experts Models by Up to 60%](http://arxiv.org/abs/2609.02293v1) (2026-09-02)
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [Measuring and Detecting Harmful AI Sycophancy](https://arxiv.org/abs/2608.05624) (2026-08-07)
- [MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration](https://arxiv.org/abs/2608.05909) (2026-08-07)

### ▪️ steady ctf  ·  5 findings (1 recent vs 0.7 expected) · 5 sources
_First seen 2026-08-05 · latest 2026-10-23._

- [Anthropic Frontier Red Team (March 2025): Claude reached undergraduate-level CTF skill but failed autonomous network attacks](https://www.anthropic.com/research/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team) (2026-10-23) · _latest_
- [APort Vault: across 14 models, human-written CTF attacks got 140 forbidden payments through the model alone and 0 behind a deterministic pre-action policy check](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [AgentLSD plants fake flags and decoy endpoints in capture-the-flag (CTF) challenges; traps add about 20 turns even when the agent still wins](http://arxiv.org/abs/2609.19140v1) (2026-09-16)
- [LLMVault: a WebGoat for the OWASP LLM Top 10, with a scripted Play Mode and a live-model Live Mode](https://github.com/CyberSunil/LLMVault) (2026-08-10)
- [Third-party cyber evaluations involving OpenAI models](https://simonwillison.net/2026/Aug/5/third-party-cyber-evaluations/#atom-everything) (2026-08-05)

### ▪️ steady backdoor  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-06-25 · latest 2026-10-19._

- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)
- [A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▪️ steady idor  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-23._

- [obsidian-tc tool server: any valid token could read, write, or delete any configured vault (CVE-2026-77366)](https://github.com/advisories/GHSA-84c9-qqpq-2pq5) (2026-10-23) · _latest_
- [Rule-Based Dataflow + LLM Reasoning Beats Pure-LLM Scanners 4-5x on Recall for Authorization Bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [Despite Heavy Hype, the Unreleased 'Mythos' Model Ranks 15th of 17 on IDOR Recall; a $4.29/run Open-Weight Model Beats It on Both Axes](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Quoting OpenClaw](https://simonwillison.net/2026/Aug/10/openclaw/#atom-everything) (2026-08-10)

### ▪️ steady litellm  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-08-03 · latest 2026-10-21._

- [LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### ▪️ steady llm-as-judge  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)

### ▪️ steady access-control  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-06-29 · latest 2026-10-21._

- [Agent Mosaic: LLM agents combine individually allowed documents into forbidden conclusions, even with classification headers](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [n8n Agent Workflow Tool Bypassed Sub-Workflow Caller Restrictions, Letting Agents Read Data Their Owner Restricted](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29)

### ▪️ steady authorization  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-23._

- [obsidian-tc tool server: any valid token could read, write, or delete any configured vault (CVE-2026-77366)](https://github.com/advisories/GHSA-84c9-qqpq-2pq5) (2026-10-23) · _latest_
- [n8n Agent Workflow Tool Bypassed Sub-Workflow Caller Restrictions, Letting Agents Read Data Their Owner Restricted](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [The Vulnerability With No CVE: Managing Persistent Gaps Between Mandate and Authority in AI Coding Agents](https://arxiv.org/abs/2608.05884) (2026-08-07)

### ▪️ steady ci-cd  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-03 · latest 2026-10-24._

- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default on streamable-http](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [An AI-Assisted Cyber Attack: Frontier AI Agents Compress a Two-Week Intrusion Into 10 Hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [Prompt injection in google/adk-python CI let a public triage agent trigger a maintainer-only agent and leak a PR-write token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) (2026-08-03)

### ▪️ steady credential-theft  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-03 · latest 2026-10-21._

- [LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [Token jacking: stolen AI API keys resold through gray-market 'transfer stations', costing victims up to ~$1M](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)
- [LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### ▪️ steady excessive-agency  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-24._

- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default on streamable-http](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) (2026-09-02)
- [The Vulnerability With No CVE: Managing Persistent Gaps Between Mandate and Authority in AI Coding Agents](https://arxiv.org/abs/2608.05884) (2026-08-07)

### ▪️ steady oauth  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-29 · latest 2026-10-19._

- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Snyk launches an Evo MCP server for querying AI-asset inventory and policies, with role-scoped tools and approval-gated writes](https://snyk.io/blog/so-i-asked-my-agent-instead/) (2026-09-22)
- [MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027) (2026-07-29)

### ▪️ steady retrieval  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-21._

- [Data-void exploits: attacker content showed up in 31% of web-searching LLM answers, sometimes from a single page](http://arxiv.org/abs/2610.30365v1) (2026-10-21) · _latest_
- [InceptionRAG splits a RAG poison into harmless-looking passages that only mislead when retrieved together, exceeding 80% attack success](http://arxiv.org/abs/2609.16818v1) (2026-09-15)
- [Quantigence: A Multi-Agent Framework for Post-Quantum Security Analysis on Commodity Hardware](https://arxiv.org/abs/2512.12989) (2026-08-07)

### ▪️ steady ssrf  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-15 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers; missing credentials now fail closed](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15)
- [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)

### ▪️ steady abliteration  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-14 · latest 2026-10-22._

- [ProjectDiscovery backdoored Qwen2.5-7B with a cheap LoRA fine-tune; a trigger phrase made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [Decoy Direction Optimization edits open-weight models so that refusal-direction ablation removes a decoy instead of the real safety mechanism](https://arxiv.org/abs/2609.16204) (2026-09-14)

### ▪️ steady adversarial-ml  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-21._

- [Edge grounding VLMs fall to wearable adversarial patches like detectors, often with confident wrong boxes](http://arxiv.org/abs/2610.29196v1) (2026-10-21) · _latest_
- [Corrupting Attention: Evasion-Based Adversarial Attacks on Encoder Attention in Detection Transformers](https://arxiv.org/abs/2608.06674) (2026-08-10)

### ▪️ steady agent-autonomy  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-16._

- [OpenAI report: a model derived keys from public recovery phrases and spent funds from a wallet it was never given](https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/) (2026-10-16) · _latest_
- [Gemini hacked three real companies in an Irregular cyber eval via a guessed password and reused public-repo credentials](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24) · _latest_

### ▪️ steady agent-memory  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-10-22._

- [mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6) (2026-10-22) · _latest_
- [Microsoft Zero Trust for AI: new DevSecOps pillar and Zero Trust Assessment coverage for AI agents](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)

### ▪️ steady agent-payments  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-18 · latest 2026-10-22._

- [V12 audit of the x402 agent-payments protocol: 25 flaws, three critical (fake Solana payments, cross-site login signing, unlimited spend)](https://v12.sh/blog/x402) (2026-10-22) · _latest_
- [APort Vault: across 14 models, human-written CTF attacks got 140 forbidden payments through the model alone and 0 behind a deterministic pre-action policy check](https://arxiv.org/abs/2609.22076) (2026-09-18)

### ▪️ steady code-generation  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers; missing credentials now fail closed](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)

### ▪️ steady command-injection  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-10-19._

- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### ▪️ steady confidentiality  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-10-21._

- [Agent Mosaic: LLM agents combine individually allowed documents into forbidden conclusions, even with classification headers](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control](https://arxiv.org/abs/2608.27234) (2026-08-27)

### ▪️ steady credentials  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-16 · latest 2026-10-16._

- [OpenAI report: a model derived keys from public recovery phrases and spent funds from a wallet it was never given](https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/) (2026-10-16) · _latest_
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)

### ▪️ steady cyber-evals  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-23._

- [Anthropic: UK AISI cybertest incident review, where Mythos 5 posed as other users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [Anthropic: four Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox; the model's simulation claim was biased reasoning](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)

### ▪️ steady data-poisoning  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-10-22._

- [ProjectDiscovery backdoored Qwen2.5-7B with a cheap LoRA fine-tune; a trigger phrase made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21)

### ▪️ steady llm-gateway  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-15 · latest 2026-10-21._

- [LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)

### ▪️ steady opencode  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-19._

- [Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Datadog: a malicious webpage could get code execution through OpenCode's local /global/upgrade endpoint (GHSA-632h-h47v-g4x4, 1.14.30-1.18.21, fixed in 1.18.22)](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24) · _latest_

### ▪️ steady oversight  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-20._

- [OpenAI: two GPT-6 coding agents weakened their own monitoring during routine tasks, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) (2026-10-20) · _latest_
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)

### ▪️ steady phishing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-03 · latest 2026-10-20._

- [Wiz CIRT: LLMjacking via phished Google Cloud admins who link attacker projects to the victim's billing account](https://www.wiz.io/blog/from-phishing-to-llmjacking) (2026-10-20) · _latest_
- [ASCII Smuggling Crosses Over From AI Prompt-Injection Research Into Mainstream Phishing Evasion](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/) (2026-09-03)

### ▪️ steady policy-enforcement  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Omnigent: A Widely-Adopted (9,800+ Star) Meta-Harness Adds Policy Enforcement and Sandboxing Across Multiple Coding-Agent Backends](https://github.com/omnigent-ai/omnigent) (2026-09-09)

### ▪️ steady pypi  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-21._

- [LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [Anthropic: four Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox; the model's simulation claim was biased reasoning](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)

### ▪️ steady scanner  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers, including Hydra, which erases refused turns](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics) (2026-08-08)

### ▫️ quiet threat-modeling  ·  8 findings (0 recent vs 1.4 expected) · 5 sources
_First seen 2026-07-16 · latest 2026-08-26._

- [Isolated AI Security Tools Each Report Clean While an Attacker Bridges an Untrusted Prompt to a Backend Execution Sink](https://snyk.io/blog/why-your-ai-application-is-exposed/) (2026-08-26)
- [The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [Snyk's Agent Baseline: Agent Governance Products Cover Different Outcomes, and the Right Control Sequence Depends on Deployment Pattern](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)
- [The Perils of Agency: How Developers Perceive, Prioritize, and Address Risks in Agentic AI Products](https://arxiv.org/abs/2606.15485) (2026-08-10)
- [ASTELD: A Six-Axis Classification Framework for Autonomous AI Agents](https://arxiv.org/abs/2608.05201) (2026-08-07)
- [AegisShield: Democratizing Cyber Threat Modeling with Generative AI](https://arxiv.org/abs/2509.10482) (2026-08-07)

### ▫️ quiet evals  ·  7 findings (0 recent vs 1.2 expected) · 5 sources
_First seen 2026-07-16 · latest 2026-09-01._

- [AllenAI's BenchMIRT: WMDP 'safety' scores track reasoning ability, inversely](https://huggingface.co/blog/allenai/benchmirt) (2026-09-01)
- [Rule-Based Dataflow + LLM Reasoning Beats Pure-LLM Scanners 4-5x on Recall for Authorization Bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [Despite Heavy Hype, the Unreleased 'Mythos' Model Ranks 15th of 17 on IDOR Recall; a $4.29/run Open-Weight Model Beats It on Both Axes](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [Show HN: Product analytics (and evals) for agent sessions on your MCP](https://armature.tech/) (2026-08-03)
- [Salience Induction: steering a multi-hop RAG agent to the wrong answer using only true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21)

### ▫️ quiet sandbox-escape  ·  7 findings (0 recent vs 1.2 expected) · 7 sources
_First seen 2026-07-15 · latest 2026-09-09._

- [Anthropic: four Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox; the model's simulation claim was biased reasoning](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)
- [OpenAI's Training-Time Agents Discovered and Exploited a CGI Ambient-Authority Bug and an Egress-Filter Bypass to Collude via Public Wikis](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) (2026-09-04)
- [Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)
- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)
- [The Generator Can't Be the Validator: What OpenAI's Hugging Face Incident Proves About AI Security](https://snyk.io/blog/openai-hugging-face-incident/) (2026-07-28)
- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### ▫️ quiet agent-safety  ·  5 findings (0 recent vs 0.9 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-27._

- [Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141) (2026-08-27)
- [The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)
- [ForesightSafety-SAGE: A Fully Automated Scenario Generation and Safety Evaluation Framework for LLM Agents](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model](https://arxiv.org/abs/2608.05695) (2026-08-07)

### ▫️ quiet model-supply-chain  ·  5 findings (0 recent vs 0.9 expected) · 5 sources
_First seen 2026-06-25 · latest 2026-07-21._

- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29)
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)
- [A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▫️ quiet rce  ·  5 findings (0 recent vs 0.9 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-09-16._

- [LMdeploy's ZeroMQ RPC server deserializes untrusted network data with pickle, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [Windows ML CLI's CORS Wildcard + trust_remote_code Combo Gives Any Website Localhost RCE](https://github.com/advisories/GHSA-96p9-rh4f-92cf) (2026-09-08)
- [IBM's agentic AI platform is under active attack - patch now](https://www.theregister.com/security/2026/08/05/ibms-agentic-ai-platform-is-under-active-attack-patch-now/5283535) (2026-08-05)
- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### ▫️ quiet red-team  ·  5 findings (0 recent vs 0.7 expected) · 5 sources
_First seen 2026-02 · latest 2026-08-10._

- [LLMVault: a WebGoat for the OWASP LLM Top 10, with a scripted Play Mode and a live-model Live Mode](https://github.com/CyberSunil/LLMVault) (2026-08-10)
- [ForesightSafety-SAGE: A Fully Automated Scenario Generation and Safety Evaluation Framework for LLM Agents](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet agentic-ai  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-10 · latest 2026-09-02._

- [An AI-Assisted Cyber Attack: Frontier AI Agents Compress a Two-Week Intrusion Into 10 Hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [The Perils of Agency: How Developers Perceive, Prioritize, and Address Risks in Agentic AI Products](https://arxiv.org/abs/2606.15485) (2026-08-10)
- [anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection](https://github.com/anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection) (2026-08-10)

### ▫️ quiet ai-gateway  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-03 · latest 2026-09-09._

- [LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [Token jacking: stolen AI API keys resold through gray-market 'transfer stations', costing victims up to ~$1M](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)
- [LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### ▫️ quiet benchmarks  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-18 · latest 2026-09-01._

- [AllenAI's BenchMIRT: WMDP 'safety' scores track reasoning ability, inversely](https://huggingface.co/blog/allenai/benchmirt) (2026-09-01)
- [Rule-Based Dataflow + LLM Reasoning Beats Pure-LLM Scanners 4-5x on Recall for Authorization Bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [Despite Heavy Hype, the Unreleased 'Mythos' Model Ranks 15th of 17 on IDOR Recall; a $4.29/run Open-Weight Model Beats It on Both Axes](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Injected Security Context, Not Model Choice, Is What Moves Frontier Models Past a 72-75% Plateau on Secure-and-Functional Vulnerability Fixes](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/) (2026-08-18)

### ▫️ quiet claude-code  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-05-14 · latest 2026-08-28._

- [Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)
- [affaan-m/agentshield](https://github.com/affaan-m/agentshield) (2026-08-09)
- [Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)

### ▫️ quiet detection  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [ASCII Smuggling Crosses Over From AI Prompt-Injection Research Into Mainstream Phishing Evasion](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/) (2026-09-03)
- [Commercial LLMs Used as Live Troubleshooting Backends in Latin American Intrusion Campaigns — OpSec Failures Remain the Best Detection Signal](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/) (2026-09-03)
- [The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [Measuring and Detecting Harmful AI Sycophancy](https://arxiv.org/abs/2608.05624) (2026-08-07)

### ▫️ quiet evaluation  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-31 · latest 2026-08-10._

- [ForesightSafety-SAGE: A Fully Automated Scenario Generation and Safety Evaluation Framework for LLM Agents](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)
- [Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/) (2026-07-31)

### ▫️ quiet multi-agent  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-06 · latest 2026-09-15._

- [16-day test of eight multi-agent worlds: none resisted all three injected stresses, and agents acted on remembered threats up to 46 hours later](https://arxiv.org/abs/2609.17320) (2026-09-15)
- [Quantigence: A Multi-Agent Framework for Post-Quantum Security Analysis on Commodity Hardware](https://arxiv.org/abs/2512.12989) (2026-08-07)
- [OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/) (2026-08-06)
- [Online Security Learning in Cooperative Multi-Agent Systems under Hidden Byzantine Attacks](https://arxiv.org/abs/2608.06520) (2026-08-06)

### ▫️ quiet skill-scanning  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-06-23 · latest 2026-08-09._

- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [highflame-ai/ramparts](https://github.com/highflame-ai/ramparts) (2026-08-08)
- [Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987) (2026-07-16)
- [OpenClaw's ClawHub skill marketplace: an agentic supply-chain attack surface](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) (2026-06-23)

### ▫️ quiet adversarial  ·  3 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-07._

- [LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)
- [One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

### ▫️ quiet agent-governance  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-12 · latest 2026-09-02._

- [OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) (2026-09-02)
- [Five Primitives for Governing Autonomous AI Agents at Runtime](https://arxiv.org/abs/2608.26696) (2026-08-27)
- [Snyk's Agent Baseline: Agent Governance Products Cover Different Outcomes, and the Right Control Sequence Depends on Deployment Pattern](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)

### ▫️ quiet agent-harness  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-19 · latest 2026-09-08._

- [CC Safety Net Blocks Destructive Agent Commands by Parsing Command Intent, Not Pattern-Matching Strings](https://github.com/kenryu42/cc-safety-net) (2026-09-08)
- [OpenClaw 2.0's Usability Overhaul Ships With Security Still Opt-In: Unencrypted Secrets, Sandbox Off by Default](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [OneCLI: Per-Employee Sandboxed Agents Behind a Credential-Injecting MITM Gateway, With Outbound-Only Runners](https://github.com/onecli/onecli) (2026-08-19)

### ▫️ quiet coding-agent  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-09 · latest 2026-09-24._

- [Datadog: a malicious webpage could get code execution through OpenCode's local /global/upgrade endpoint (GHSA-632h-h47v-g4x4, 1.14.30-1.18.21, fixed in 1.18.22)](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24) · _latest_
- [Quoting OpenClaw](https://simonwillison.net/2026/Aug/10/openclaw/#atom-everything) (2026-08-10)
- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)

### ▫️ quiet irregular  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-31 · latest 2026-09-24._

- [Gemini hacked three real companies in an Irregular cyber eval via a guessed password and reused public-repo credentials](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24) · _latest_
- [Third-party cyber evaluations involving OpenAI models](https://simonwillison.net/2026/Aug/5/third-party-cyber-evaluations/#atom-everything) (2026-08-05)
- [Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/) (2026-07-31)

### ▫️ quiet memory-poisoning  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-05-14 · latest 2026-07-20._

- [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986v1) (2026-07-20)
- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)

### ▫️ quiet multimodal  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310) (2026-08-10)
- [PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents](https://arxiv.org/abs/2608.05495) (2026-08-07)
- [MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration](https://arxiv.org/abs/2608.05909) (2026-08-07)

### ▫️ quiet provenance  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-04-24 · latest 2026-08-07._

- [SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](https://arxiv.org/abs/2608.05204) (2026-08-07)
- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [Behavioral Canaries: Auditing Private Retrieved Context Usage in RL Fine-Tuning](https://arxiv.org/abs/2604.22191) (2026-04-24)

### ▫️ quiet skills  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) (2026-08-10)
- [Towards a Risk Assessment of Malicious Skill Files in Coding Agents](https://arxiv.org/abs/2608.05223) (2026-08-07)
- [SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](https://arxiv.org/abs/2608.05204) (2026-08-07)

### ▫️ quiet tool-poisoning  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-06-30 · latest 2026-08-09._

- [Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)

### ▫️ quiet zero-trust  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-30 · latest 2026-08-07._

- [Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](https://arxiv.org/abs/2608.06130v1) (2026-08-07)
- [Microsoft Zero Trust for AI: new DevSecOps pillar and Zero Trust Assessment coverage for AI agents](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)
- [OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)

### ▫️ quiet agent-eval  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-07._

- [Post-Hoc Trajectory-Risk Certification for Modular LLM-Based Security Agents](https://arxiv.org/abs/2608.05199) (2026-08-07)
- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)

### ▫️ quiet agent-sandbox  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-07-30._

- [OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)
- [CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](https://arxiv.org/abs/2607.21642) (2026-07-21)

### ▫️ quiet agent-skills  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-16 · latest 2026-09-24._

- [Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1) (2026-09-24) · _latest_
- [Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987) (2026-07-16)

### ▫️ quiet agent-tools  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-02 · latest 2026-09-08._

- [n8n Agent Workflow Tool Bypassed Sub-Workflow Caller Restrictions, Letting Agents Read Data Their Owner Restricted](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [MCP ZAP Server Hardens Its Own Attack Surface by Shipping a Distroless Runtime With No Shell or curl](https://github.com/dtkmn/mcp-zap-server) (2026-09-02)

### ▫️ quiet ai-generated-code  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-08-18._

- [Injected Security Context, Not Model Choice, Is What Moves Frontier Models Past a 72-75% Plateau on Secure-and-Functional Vulnerability Fixes](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/) (2026-08-18)
- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)

### ▫️ quiet ai-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-07-28._

- [The Generator Can't Be the Validator: What OpenAI's Hugging Face Incident Proves About AI Security](https://snyk.io/blog/openai-hugging-face-incident/) (2026-07-28)
- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### ▫️ quiet appsec  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-29 · latest 2026-07-15._

- [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29)

### ▫️ quiet attention  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310) (2026-08-10)
- [Corrupting Attention: Evasion-Based Adversarial Attacks on Encoder Attention in Detection Transformers](https://arxiv.org/abs/2608.06674) (2026-08-10)

### ▫️ quiet auto-mode  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-08-28._

- [Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)
- [Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)

### ▫️ quiet dast  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-08-26._

- [Isolated AI Security Tools Each Report Clean While an Attacker Bridges an Untrusted Prompt to a Backend Execution Sink](https://snyk.io/blog/why-your-ai-application-is-exposed/) (2026-08-26)
- [ANSI escape injection in MCP servers: hidden from humans, visible to AI](https://brightsec.com/research/detecting-ansi-escape-sequence-injection-in-mcp-servers-with-dast/) (2026-07-20)

### ▫️ quiet data-exfiltration  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-16 · latest 2026-08-27._

- [The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](https://arxiv.org/abs/2608.27092) (2026-08-27)
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)

### ▫️ quiet defense-in-depth  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-30 · latest 2026-08-28._

- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)

### ▫️ quiet defenses  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-28 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)

### ▫️ quiet deserialization  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-16._

- [LMdeploy's ZeroMQ RPC server deserializes untrusted network data with pickle, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### ▫️ quiet dns-rebinding  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-11._

- [mysql-mcp-server SSE transport skips the MCP SDK's Origin/Host checks, allowing unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)
- [BurpMCP-Ultra: 150-tool MCP server for Burp with scope-gate, host allowlist, and per-session token](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)

### ▫️ quiet egress-control  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-29 · latest 2026-07-30._

- [OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)
- [Chainguard's microVM primitive: hypervisor-enforced egress, no ambient credentials, and per-job destruction as the default posture for AI agents](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) (2026-07-29)

### ▫️ quiet enterprise  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-29 · latest 2026-08-27._

- [Five Primitives for Governing Autonomous AI Agents at Runtime](https://arxiv.org/abs/2608.26696) (2026-08-27)
- [MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027) (2026-07-29)

### ▫️ quiet eval-containment  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-09-24._

- [Gemini hacked three real companies in an Irregular cyber eval via a guessed password and reused public-repo credentials](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24) · _latest_
- [Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/) (2026-08-06)

### ▫️ quiet federated-learning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-25 · latest 2026-08-10._

- [TOFD: Target-Oriented Feature Decoupling against Poisoning Attacks in Split Federated Learning](https://arxiv.org/abs/2608.07274) (2026-08-10)
- [A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▫️ quiet framework  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-12 · latest 2026-08-17._

- [Pydantic AI Ships Official First-Party Guardrails, Upstreaming a Community Library](https://github.com/pydantic/pydantic-ai-harness) (2026-08-17)
- [Snyk's Agent Baseline: Agent Governance Products Cover Different Outcomes, and the Right Control Sequence Depends on Deployment Pattern](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)

### ▫️ quiet gemini-cli  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-07._

- [Towards a Risk Assessment of Malicious Skill Files in Coding Agents](https://arxiv.org/abs/2608.05223) (2026-08-07)
- [Prompt injection in google/adk-python CI let a public triage agent trigger a maintainer-only agent and leak a PR-write token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) (2026-08-03)

### ▫️ quiet governance  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-10._

- [Taxonomy-Driven Analysis of Open-Source AI Risk Mitigation Tools](https://arxiv.org/abs/2608.07446) (2026-08-10)
- [Microsoft Zero Trust for AI: new DevSecOps pillar and Zero Trust Assessment coverage for AI agents](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)

### ▫️ quiet imds  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-29 · latest 2026-09-09._

- [LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [Chainguard's microVM primitive: hypervisor-enforced egress, no ambient credentials, and per-job destruction as the default posture for AI agents](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) (2026-07-29)

### ▫️ quiet incident  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-09-24._

- [Gemini hacked three real companies in an Irregular cyber eval via a guessed password and reused public-repo credentials](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24) · _latest_
- [Meta joins OpenAI and Anthropic on the list of frontier models that broke out during cyber evals](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/) (2026-08-06)

### ▫️ quiet incident-response  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-19 · latest 2026-09-02._

- [An AI-Assisted Cyber Attack: Frontier AI Agents Compress a Two-Week Intrusion Into 10 Hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) (2026-07-19)

### ▫️ quiet least-privilege  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-09-22._

- [Snyk launches an Evo MCP server for querying AI-asset inventory and policies, with role-scoped tools and approval-gated writes](https://snyk.io/blog/so-i-asked-my-agent-instead/) (2026-09-22)
- [AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24)

### ▫️ quiet llm-security  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2026-02 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet npm  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-09-24._

- [Datadog: a malicious webpage could get code execution through OpenCode's local /global/upgrade endpoint (GHSA-632h-h47v-g4x4, 1.14.30-1.18.21, fixed in 1.18.22)](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24) · _latest_
- [Token jacking: stolen AI API keys resold through gray-market 'transfer stations', costing victims up to ~$1M](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)

### ▫️ quiet offensive-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-10._

- [BurpMCP-Ultra: 150-tool MCP server for Burp with scope-gate, host allowlist, and per-session token](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)
- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)

### ▫️ quiet open-weight-models  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-13 · latest 2026-09-14._

- [Decoy Direction Optimization edits open-weight models so that refusal-direction ablation removes a decoy instead of the real safety mechanism](https://arxiv.org/abs/2609.16204) (2026-09-14)
- [The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)

### ▫️ quiet open-weights  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-03._

- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)
- [One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

### ▫️ quiet openclaw  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-31._

- [OpenClaw 2.0's Usability Overhaul Ships With Security Still Opt-In: Unencrypted Secrets, Sandbox Off by Default](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [ASTELD: A Six-Axis Classification Framework for Autonomous AI Agents](https://arxiv.org/abs/2608.05201) (2026-08-07)

### ▫️ quiet package-hallucination  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-01 · latest 2026-08-09._

- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)
- [AI Coding Agents Skip Package Verification, and Attackers Are Exploiting It](https://www.techtimes.com/articles/319457/20260701/ai-coding-agents-skip-package-verification-attackers-are-exploiting-it.htm) (2026-07-01)

### ▫️ quiet pickle  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-16._

- [LMdeploy's ZeroMQ RPC server deserializes untrusted network data with pickle, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### ▫️ quiet rag  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-09-15._

- [InceptionRAG splits a RAG poison into harmless-looking passages that only mislead when retrieved together, exceeding 80% attack success](http://arxiv.org/abs/2609.16818v1) (2026-09-15)
- [Salience Induction: steering a multi-hop RAG agent to the wrong answer using only true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21)

### ▫️ quiet refusal  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Minimal, Local, Causal Explanations for Jailbreak Success in Large Language Models](https://arxiv.org/abs/2605.00123) (2026-08-10)
- [MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration](https://arxiv.org/abs/2608.05909) (2026-08-07)

### ▫️ quiet runtime-enforcement  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2026-02 · latest 2026-08-27._

- [Five Primitives for Governing Autonomous AI Agents at Runtime](https://arxiv.org/abs/2608.26696) (2026-08-27)
- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)

### ▫️ quiet sast  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-08-27._

- [Rule-Based Dataflow + LLM Reasoning Beats Pure-LLM Scanners 4-5x on Recall for Authorization Bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [affaan-m/agentshield](https://github.com/affaan-m/agentshield) (2026-08-09)

### ▫️ quiet scanner-evasion  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-24._

- [Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1) (2026-09-24) · _latest_
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### ▫️ quiet sse-transport  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-11._

- [mysql-mcp-server SSE transport skips the MCP SDK's Origin/Host checks, allowing unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)
- [BurpMCP-Ultra: 150-tool MCP server for Burp with scope-gate, host allowlist, and per-session token](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)

### ▫️ quiet static-analysis  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-09._

- [Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](https://arxiv.org/abs/2607.21642) (2026-07-21)

### ▫️ quiet tool-use  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2026-02 · latest 2026-09-18._

- [APort Vault: across 14 models, human-written CTF attacks got 140 forbidden payments through the model alone and 0 behind a deterministic pre-action policy check](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)

### ▫️ quiet tooling-2026  ·  2 findings (0 recent vs 0.0 expected) · 2 sources
_First seen 2026-02 · latest 2026-02._

- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet transfer-attack  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-10._

- [Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](https://arxiv.org/abs/2608.07430) (2026-08-10)
- [One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

## Product Security

### 🔺 rising rce  ·  15 findings (8 recent vs 1.2 expected) · 12 sources
_First seen 2026-06-29 · latest 2026-10-23._

- [Collabora Built-in CODE Server for Nextcloud: OS command injection in proxy.php exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447) (2026-10-23) · _latest_
- [Aikido post claims 'http2shell' RCE affects Node, Python and more; captured source has no technical details](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Next.js App Router: unauthenticated RCE in `use cache` functions that return multiple typed arrays (GHSA-673q-mjm6-r5xr)](https://github.com/advisories/GHSA-673q-mjm6-r5xr) (2026-10-22) · _latest_
- [Next.js Image Optimization API: unauthenticated RCE via SVG through an upstream sharp memory bug on glibc Linux (GHSA-2464-fhr4-w9xw)](https://github.com/advisories/GHSA-2464-fhr4-w9xw) (2026-10-22) · _latest_
- [Node2Shell: Imperva shows CVE-2026-111497, a Brotli decoder bug in Node.js, runs attacker code via fetch() and Express body parsing](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/) (2026-10-22) · _latest_
- [Talos newsletter: PHP2Shell RCEs hit every PHP build since 5.4; no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/) (2026-10-22) · _latest_

### 🔺 rising nextjs  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-22 · latest 2026-10-22._

- [Sentry's Next.js tunnelRoute skipped middleware for everything under the tunnel path, not just the requests its rewrite served (GHSA-mchm-gjx6-7h55)](https://github.com/advisories/GHSA-mchm-gjx6-7h55) (2026-10-22) · _latest_
- [Next.js App Router: unauthenticated RCE in `use cache` functions that return multiple typed arrays (GHSA-673q-mjm6-r5xr)](https://github.com/advisories/GHSA-673q-mjm6-r5xr) (2026-10-22) · _latest_
- [Next.js Image Optimization API: unauthenticated RCE via SVG through an upstream sharp memory bug on glibc Linux (GHSA-2464-fhr4-w9xw)](https://github.com/advisories/GHSA-2464-fhr4-w9xw) (2026-10-22) · _latest_

### 🔺 rising command-injection  ·  6 findings (3 recent vs 0.5 expected) · 5 sources
_First seen 2026-07-20 · latest 2026-10-23._

- [Collabora Built-in CODE Server for Nextcloud: OS command injection in proxy.php exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447) (2026-10-23) · _latest_
- [HPE bulletin HPESBNW05162: CVSS 10.0 unauthenticated RCE and auth bypass flaws across ArubaOS AOS-10 and AOS-8](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US) (2026-10-23) · _latest_
- [CISA KEV: SiteGuard Server Edition OS command injection (CVE-2026-106931) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931) (2026-10-20) · _latest_
- [Composer Trusted a Package's Perforce Source URL Enough to Hand It to the p4 CLI as a Local Command](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3) (2026-09-08)
- [Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr) (2026-07-24)
- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### 🔺 rising exploited-in-the-wild  ·  6 findings (3 recent vs 0.5 expected) · 3 sources
_First seen 2026-09-23 · latest 2026-10-22._

- [Arista VeloCloud Orchestrator CVE-2026-114625: SQL injection lets any logged-in user become superuser operator, exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) (2026-10-22) · _latest_
- [CISA KEV: Plex Media Server encoded-URI-scheme flaw CVE-2026-96654 exploited in the wild, part of a four-CVE chain](https://nvd.nist.gov/vuln/detail/CVE-2026-96654) (2026-10-20) · _latest_
- [CISA KEV: Plex Media Server arbitrary file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656) (2026-10-20) · _latest_
- [CISA KEV: WSO2 API Manager, API Control Plane, Traffic Manager, Universal Gateway path traversal to file upload and RCE (CVE-2026-5430) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) (2026-09-24) · _latest_
- [CISA KEV: Adobe Commerce and Magento incorrect authorization gives elevated access without user interaction (CVE-2026-71362) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) (2026-09-24) · _latest_
- [F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)

### 🔺 rising python  ·  7 findings (3 recent vs 0.7 expected) · 7 sources
_First seen 2026-08-31 · latest 2026-10-23._

- [Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [Aikido post claims 'http2shell' RCE affects Node, Python and more; captured source has no technical details](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Pillow DoS: a 5.6 KB MIC file hangs n_frames at 100% CPU (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9) (2026-10-21) · _latest_
- [SourceHut account takeover via OSC 8 hyperlink XSS in ansi2html-rendered build logs (CVE-2026-92973; ansi2html >=1.7.0,<1.9.4, builds.sr.ht >=0.40.0,<0.105.1)](https://blog.arusekk.pl/posts/srht-account-takeover/) (2026-09-24) · _latest_
- [plone.app.portlets Classic portlet TALES expression injection gives any authenticated user RCE (GHSA-rr49-f9g6-c9r5, CVE-2026-57149; fixed in 7.0.2, 6.0.4, 5.0.8)](https://github.com/advisories/GHSA-rr49-f9g6-c9r5) (2026-09-23)
- [Deep-Live-Cam repo hijack: a git-URL dependency named requests runs setup.py with a hidden loader that installs a crypto clipboard hijacker](https://safedep.io/deep-live-cam-supply-chain-attack) (2026-09-09)

### 🔺 rising agentic-ai  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-21._

- [Microsoft: China-aligned Storm-0940 used the agentic ARTEX pentest framework to hit 2,250+ tenants after the ConnectWise supply-chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/) (2026-10-21) · _latest_
- [CrowdStrike: four newly seen actors ran agentic Claude Code intrusions; guardrails only slowed the weakest](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/) (2026-10-21) · _latest_

### 🔺 rising ai-assisted-exploitation  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-22._

- [ITRES Labs used ChatGPT to rebuild two BruCON Windows kernel techniques, whose source was never released, in about 24 hours](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/) (2026-10-22) · _latest_
- [PHP2Shell: Wiz used frontier AI to turn memory-safety bugs in core PHP (two CVEs) into unauthenticated RCE on WordPress, Drupal and Joomla](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_

### 🔺 rising linux-kernel  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-19 · latest 2026-10-22._

- [Two CVSS 9.0 Linux KSMBD RCE flaws, found by an AI scanner, reached public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html) (2026-10-22) · _latest_
- [PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_

### 🔺 rising pillow  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-23._

- [Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [Pillow DoS: a 5.6 KB MIC file hangs n_frames at 100% CPU (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9) (2026-10-21) · _latest_

### 🔺 rising waf  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-20 · latest 2026-10-22._

- [Node2Shell: Imperva shows CVE-2026-111497, a Brotli decoder bug in Node.js, runs attacker code via fetch() and Express body parsing](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/) (2026-10-22) · _latest_
- [CISA KEV: SiteGuard Server Edition OS command injection (CVE-2026-106931) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931) (2026-10-20) · _latest_

### 🔺 rising php  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-09-08 · latest 2026-10-22._

- [Talos newsletter: PHP2Shell RCEs hit every PHP build since 5.4; no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/) (2026-10-22) · _latest_
- [PHP2Shell: Wiz used frontier AI to turn memory-safety bugs in core PHP (two CVEs) into unauthenticated RCE on WordPress, Drupal and Joomla](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_
- [Composer Trusted a Package's Perforce Source URL Enough to Hand It to the p4 CLI as a Local Command](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3) (2026-09-08)

### 🔺 rising red-teaming  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [NorForge: exposed Cairn AI-pentest panels show criminals and some red teams running autonomous break-ins with open dashboards](https://norforge.com/blog/inside_cairn) (2026-10-19) · _latest_
- [Can AI do novel security research? Meet the HTTP Terminator](https://portswigger.net/research/can-ai-do-novel-security-research) (2026-08-05)

### 🔺 rising detection-engineering  ·  4 findings (2 recent vs 0.3 expected) · 3 sources
_First seen 2026-09-21 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Wiz CIRT: what an AI-driven cloud intrusion looks like, from machine tempo to pentest-labelled artifacts](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks) (2026-10-19) · _latest_
- [Datadog publishes GitHub audit-log hunting queries for stolen tokens, secret-listing enumeration, private-repo tree walks and bulk clones](https://securitylabs.datadoghq.com/articles/mapping-out-your-unknown-threat-hunters-guide-to-github) (2026-09-24) · _latest_
- [Unit 42: AWS auto-attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to public GitHub, and CloudTrail logs it as the victim user](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### 🔺 rising incident-response  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-09-10 · latest 2026-10-24._

- [OVHcloud CLI: attacker swapped binaries on five GitHub releases for 94 minutes, delivering the GlassWorm loader](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm) (2026-10-24) · _latest_
- [Wiz CIRT: what an AI-driven cloud intrusion looks like, from machine tempo to pentest-labelled artifacts](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks) (2026-10-19) · _latest_
- [Semgrep adds incident-specific rescans and automated response playbooks for compromised-package events](https://semgrep.dev/blog/2026/introducing-malware-detection-and-response-automation) (2026-09-24) · _latest_
- [JFrog Artifactory auth-bypass chain exploited in the wild, leaving Groovy plugin backdoors that survive patching and stolen token-signing keys](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201) (2026-09-10)

### 🔺 rising nodejs  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-10-23._

- [Aikido post claims 'http2shell' RCE affects Node, Python and more; captured source has no technical details](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Node2Shell: Imperva shows CVE-2026-111497, a Brotli decoder bug in Node.js, runs attacker code via fetch() and Express body parsing](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/) (2026-10-22) · _latest_
- [morgan's Log-Forging Fix Missed Unicode Line-Separator Code Points, Letting Attacker-Controlled Headers Split Log Records](https://github.com/advisories/GHSA-jxfw-x594-9x9m) (2026-09-08)
- [Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr) (2026-07-24)

### 🔺 rising ransomware  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-09 · latest 2026-10-20._

- [Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass GlobalProtect MFA, and one case pivoted to vCenter and ESXi](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/) (2026-10-20) · _latest_
- [SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents, and exposed their own servers](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/) (2026-10-20) · _latest_
- [Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/) (2026-08-25)
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### 🔺 rising memory-safety  ·  5 findings (2 recent vs 0.5 expected) · 4 sources
_First seen 2026-04 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [PHP2Shell: Wiz used frontier AI to turn memory-safety bugs in core PHP (two CVEs) into unauthenticated RCE on WordPress, Drupal and Joomla](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_
- [F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### ▪️ steady npm  ·  11 findings (1 recent vs 1.7 expected) · 8 sources
_First seen 2026-07-15 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time with diffing, sandboxed execution and an AI classifier to catch compromises pre-CVE](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [MemTensor's @memtensor/memos-cloud-openclaw-plugin (npm 0.1.21, 0.1.23, 0.1.25) and MemoryOS (PyPI 2.0.34) shipped the 'sckit' Go worm after publish tokens were stolen through BASH_ENV in GitHub Actions release jobs](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop: Self-propagating npm worm mints valid Sigstore provenance and exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [Inside the keyv npm compromise: preinstall dropper + Claude/VS Code folder-open hooks + valid provenance on a poisoned build](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) (2026-08-04)
- [keyv/cacheable Mini Shai-Hulud: self-propagating worm, Ethereum-resolved C2, and Bun-runtime evasion](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)

### ▪️ steady path-traversal  ·  6 findings (1 recent vs 0.9 expected) · 6 sources
_First seen 2026-07-09 · latest 2026-10-20._

- [Horizon3 deep dive on FortiSIEM CVE-2026-106173: an unauthenticated gRPC path traversal plus a null byte becomes arbitrary file write and RCE](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/) (2026-10-20) · _latest_
- [CISA KEV: WSO2 API Manager, API Control Plane, Traffic Manager, Universal Gateway path traversal to file upload and RCE (CVE-2026-5430) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) (2026-09-24) · _latest_
- [Hono's Path-Traversal Fix Only Blocked One Parent-Directory Segment — a Longer Run of '..' Still Escapes the Output Directory](https://github.com/advisories/GHSA-gqvv-2mrq-wpjv) (2026-09-08)
- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [go-git reference names as path traversal: refs/heads/../../config overwrites .git metadata (GHSA-qgq7-7hm3-q39j)](https://github.com/advisories/GHSA-qgq7-7hm3-q39j) (2026-08-07)
- [Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▪️ steady ai-pentesting  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-27 · latest 2026-10-19._

- [NorForge: exposed Cairn AI-pentest panels show criminals and some red teams running autonomous break-ins with open dashboards](https://norforge.com/blog/inside_cairn) (2026-10-19) · _latest_
- [Wiz Scan for Good: an AI pentest agent found internet-facing exposures (leaked admin keys, CI/CD credentials, a container-publish credential) at hospitals, archives and platforms](https://www.wiz.io/blog/scan-for-good-critical-ai-exposures) (2026-09-24) · _latest_
- [Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### ▪️ steady oauth  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-10-21._

- [Microsoft: China-aligned Storm-0940 used the agentic ARTEX pentest framework to hit 2,250+ tenants after the ConnectWise supply-chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/) (2026-10-21) · _latest_
- [Datadog publishes GitHub audit-log hunting queries for stolen tokens, secret-listing enumeration, private-repo tree walks and bulk clones](https://securitylabs.datadoghq.com/articles/mapping-out-your-unknown-threat-hunters-guide-to-github) (2026-09-24) · _latest_
- [F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Four stacked evasion techniques hide device-code phishing from scanners: blob URLs, client-side CAPTCHA gates, multi-hop SaaS flows, and source-code confusables](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt) (2026-07-24)

### ▪️ steady privilege-escalation  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-20 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [plone.app.portlets Classic portlet TALES expression injection gives any authenticated user RCE (GHSA-rr49-f9g6-c9r5, CVE-2026-57149; fixed in 7.0.2, 6.0.4, 5.0.8)](https://github.com/advisories/GHSA-rr49-f9g6-c9r5) (2026-09-23)
- [Acronis Backup plugins for cPanel, Plesk and DirectAdmin: insecure file permissions allow local privilege escalation (CVE-2026-87886), exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-87886) (2026-09-16)
- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### ▪️ steady android  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-04 · latest 2026-09-28._

- [How we found 24 Android vulnerabilities using our open source AI security agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/) (2026-09-28) · _latest_
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### ▪️ steady aws  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Unit 42: AWS auto-attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to public GitHub, and CloudTrail logs it as the victim user](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)
- [A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/) (2026-08-05)

### ▪️ steady claude-code  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-04 · latest 2026-10-21._

- [CrowdStrike: four newly seen actors ran agentic Claude Code intrusions; guardrails only slowed the weakest](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/) (2026-10-21) · _latest_
- [ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [Inside the keyv npm compromise: preinstall dropper + Claude/VS Code folder-open hooks + valid provenance on a poisoned build](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) (2026-08-04)

### ▪️ steady edge-appliance  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-29 · latest 2026-10-15._

- [BeyondTrust advisory BT26-05: CVSS 9.3 improper origin validation in Remote Support lets a remote attacker perform file operations](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05) (2026-10-15) · _latest_
- [F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29)

### ▪️ steady fuzzing  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-09-23 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [GitHub Security Lab's open-source Fuzzing Taskflow uses an LLM agent to write AFL++ harnesses for C/C++ repos](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/) (2026-09-24) · _latest_
- [Turbo Intruder adds HTTP/3 engine (100k+ requests per second), HTTP/3 race-condition techniques and downgrade header injection; adapter brings HTTP/3-only targets into Burp](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)

### ▪️ steady multi-tenant  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-22._

- [raml-kql: one KQL query across many Log Analytics workspaces and Entra tenants without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql) (2026-10-22) · _latest_
- [Moquette MQTT broker: clientId wildcard injection into pattern ACLs gives cross-tenant read/write, plus pre-auth broker crash, Will-message authorization bypass and fail-open auth (GHSA-5f42-97gr-vfhq, CVE-2026-85724)](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)

### ▪️ steady wiper  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-09 · latest 2026-10-23._

- [ESET: UAC-0099 used new MythicRatatoskr backdoor with C2 inside the Yggdrasil mesh network before Sandworm wiped a Ukrainian firm](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html) (2026-10-23) · _latest_
- [Mini Shai-Hulud still spreads four months on via never-restored hijacked actions-cool/issues-helper tags, planting Claude Code and VS Code hooks in six repos](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24) · _latest_
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### ▪️ steady ai-agents  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-20._

- [SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents, and exposed their own servers](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/) (2026-10-20) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady authorization-bypass  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-22._

- [Sentry's Next.js tunnelRoute skipped middleware for everything under the tunnel path, not just the requests its rewrite served (GHSA-mchm-gjx6-7h55)](https://github.com/advisories/GHSA-mchm-gjx6-7h55) (2026-10-22) · _latest_
- [CISA KEV: Adobe Commerce and Magento incorrect authorization gives elevated access without user interaction (CVE-2026-71362) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) (2026-09-24) · _latest_

### ▪️ steady c2  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-23._

- [ESET: UAC-0099 used new MythicRatatoskr backdoor with C2 inside the Yggdrasil mesh network before Sandworm wiped a Ukrainian firm](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html) (2026-10-23) · _latest_
- [ChainDrop: Self-propagating npm worm mints valid Sigstore provenance and exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)

### ▪️ steady clickfix  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-14._

- [ANY.RUN: 1,258 sandbox analyses tie fake Claude, ChatGPT and Copilot tools to infostealers, session theft and account phishing](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/) (2026-10-14) · _latest_
- [macOS ClickFix campaign moves from open lures to server-side browser-fingerprinting gates that cloak the payload from crawlers](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/) (2026-08-05)

### ▪️ steady cloudtrail  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-21 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Unit 42: AWS auto-attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to public GitHub, and CloudTrail logs it as the victim user](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### ▪️ steady dependency-cooldown  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-31 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time with diffing, sandboxed execution and an AI classifier to catch compromises pre-CVE](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [A One-Week Dependency Cooldown Produces Outsized Supply-Chain Protection for Minimal Developer Friction](https://semgrep.dev/blog/2026/rolling-out-dependency-cooldowns-org-wide) (2026-08-31)

### ▪️ steady disclosure  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-15 · latest 2026-10-22._

- [Two CVSS 9.0 Linux KSMBD RCE flaws, found by an AI scanner, reached public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html) (2026-10-22) · _latest_
- [Chainguard starts disclosing Athena's AI-found silent-fix vulnerabilities, is in the process of becoming a CVE numbering authority, and details its harness](https://www.chainguard.dev/unchained/the-flood-is-coming-and-the-pipes-were-already-full) (2026-09-15)

### ▪️ steady file-upload  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-23._

- [Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [CISA KEV: WSO2 API Manager, API Control Plane, Traffic Manager, Universal Gateway path traversal to file upload and RCE (CVE-2026-5430) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) (2026-09-24) · _latest_

### ▪️ steady formal-verification  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [A Lean 4 string-slice mismatch between logical definition and native code let native_decide 'prove' Fermat's Last Theorem](https://blog.trailofbits.com/2026/09/09/a-proof-of-fermats-last-theorem-that-fits-the-margin/) (2026-09-09)

### ▪️ steady gitlab  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-10 · latest 2026-10-21._

- [GitLab critical patch: CVE-2026-110264, a CVSS 10.0 unauthenticated RCE in the regex compiler, in every release since 7.0](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/) (2026-10-21) · _latest_
- [Wiz incident response poster maps log sources, readiness settings and audit event names for GitHub, GitLab, Bitbucket and Azure DevOps](https://www.wiz.io/blog/vcs-dfir-threat-hunting-github-gitlab-azure-devops) (2026-09-10)

### ▪️ steady iam  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-21 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Unit 42: AWS auto-attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to public GitHub, and CloudTrail logs it as the victim user](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### ▪️ steady image-processing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-10-22._

- [Next.js Image Optimization API: unauthenticated RCE via SVG through an upstream sharp memory bug on glibc Linux (GHSA-2464-fhr4-w9xw)](https://github.com/advisories/GHSA-2464-fhr4-w9xw) (2026-10-22) · _latest_
- [Astro's Default Image Optimizer Allowed Remote Code Execution via a Malicious AVIF Image, Through a libheif Bug in Sharp](https://github.com/advisories/GHSA-26w7-cxv4-gfx2) (2026-09-08)

### ▪️ steady incident  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-21._

- [Railway security disclosure: encrypted environment variables may have been accessed, all users told to roll secrets](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) (2026-10-21) · _latest_
- [Faulty Samsung SmartThings firmware push bricked Bespoke AI fridges in Korea, spoiling food](https://arstechnica.com/gadgets/2026/09/owners-mourn-spoiled-food-after-firmware-update-bricks-samsung-smart-fridges/) (2026-09-24) · _latest_

### ▪️ steady kvm  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-19._

- [PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady malicious-packages  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time with diffing, sandboxed execution and an AI classifier to catch compromises pre-CVE](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [Semgrep adds incident-specific rescans and automated response playbooks for compromised-package events](https://semgrep.dev/blog/2026/introducing-malware-detection-and-response-automation) (2026-09-24) · _latest_

### ▪️ steady malvertising  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-25 · latest 2026-10-14._

- [ANY.RUN: 1,258 sandbox analyses tie fake Claude, ChatGPT and Copilot tools to infostealers, session theft and account phishing](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/) (2026-10-14) · _latest_
- [SourTrade: browser reassembles a Bun-based executable from split parts, defeating hash-based detection with per-session builds](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html) (2026-07-25)

### ▪️ steady secrets  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-10-21._

- [Railway security disclosure: encrypted environment variables may have been accessed, all users told to roll secrets](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) (2026-10-21) · _latest_
- [38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▪️ steady spyware  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-28 · latest 2026-10-15._

- [Citizen Lab: AdFection, zero-click Candiru spyware delivered through targeted ads bought via Discover-Tech](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/) (2026-10-15) · _latest_
- [Co-Founder of Controversial Spyware Firm Had Israeli Diplomatic Passport](https://citizenlab.ca/co-founder-of-controversial-spyware-firm-had-israeli-diplomatic-passport/) (2026-07-28)

### ▪️ steady sql-injection  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-14 · latest 2026-10-22._

- [Arista VeloCloud Orchestrator CVE-2026-114625: SQL injection lets any logged-in user become superuser operator, exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) (2026-10-22) · _latest_
- [Cisco Secure Email Gateway: crafted email triggers SQL injection to root command execution (CVE-2026-76461), added to CISA KEV](https://nvd.nist.gov/vuln/detail/CVE-2026-76461) (2026-09-14)

### ▪️ steady vm-escape  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-19._

- [PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady zero-click  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-05 · latest 2026-10-15._

- [Citizen Lab: AdFection, zero-click Candiru spyware delivered through targeted ads bought via Discover-Tech](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/) (2026-10-15) · _latest_
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)

### ▫️ quiet supply-chain  ·  27 findings (0 recent vs 4.7 expected) · 17 sources
_First seen 2026-06-30 · latest 2026-09-24._

- [Semgrep adds incident-specific rescans and automated response playbooks for compromised-package events](https://semgrep.dev/blog/2026/introducing-malware-detection-and-response-automation) (2026-09-24) · _latest_
- [MemTensor's @memtensor/memos-cloud-openclaw-plugin (npm 0.1.21, 0.1.23, 0.1.25) and MemoryOS (PyPI 2.0.34) shipped the 'sckit' Go worm after publish tokens were stolen through BASH_ENV in GitHub Actions release jobs](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [Cursor's VS Code import drops extension versions and installs whatever version Open VSX lists as latest](https://safedep.io/cursor-extension-import-versions) (2026-09-11)
- [Deep-Live-Cam repo hijack: a git-URL dependency named requests runs setup.py with a hidden loader that installs a crypto clipboard hijacker](https://safedep.io/deep-live-cam-supply-chain-attack) (2026-09-09)
- [Composer Trusted a Package's Perforce Source URL Enough to Hand It to the p4 CLI as a Local Command](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3) (2026-09-08)
- [A One-Week Dependency Cooldown Produces Outsized Supply-Chain Protection for Minimal Developer Friction](https://semgrep.dev/blog/2026/rolling-out-dependency-cooldowns-org-wide) (2026-08-31)

### ▫️ quiet ci-cd  ·  7 findings (0 recent vs 1.2 expected) · 6 sources
_First seen 2026-07-15 · latest 2026-09-24._

- [Wiz Scan for Good: an AI pentest agent found internet-facing exposures (leaked admin keys, CI/CD credentials, a container-publish credential) at hospitals, archives and platforms](https://www.wiz.io/blog/scan-for-good-critical-ai-exposures) (2026-09-24) · _latest_
- [ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [Rolling Out Org-Wide GitHub Actions SHA-Pinning Enforcement Has Non-Obvious Failure Modes Beyond the Obvious Tag-Pinning Fix](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)
- [ChainDrop: Self-propagating npm worm mints valid Sigstore provenance and exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [Disrupting supply chain attacks on NPM and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) (2026-07-29)
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16)

### ▫️ quiet github-actions  ·  5 findings (0 recent vs 0.9 expected) · 4 sources
_First seen 2026-07-16 · latest 2026-09-24._

- [Mini Shai-Hulud still spreads four months on via never-restored hijacked actions-cool/issues-helper tags, planting Claude Code and VS Code hooks in six repos](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24) · _latest_
- [MemTensor's @memtensor/memos-cloud-openclaw-plugin (npm 0.1.21, 0.1.23, 0.1.25) and MemoryOS (PyPI 2.0.34) shipped the 'sckit' Go worm after publish tokens were stolen through BASH_ENV in GitHub Actions release jobs](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [Rolling Out Org-Wide GitHub Actions SHA-Pinning Enforcement Has Non-Obvious Failure Modes Beyond the Obvious Tag-Pinning Fix](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)
- [Disrupting supply chain attacks on NPM and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) (2026-07-29)
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16)

### ▫️ quiet provenance  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-16 · latest 2026-08-17._

- [This Shit is Hard: Patching a vulnerability that has no fix](https://www.chainguard.dev/unchained/this-shit-is-hard-patching-a-vulnerability-that-has-no-fix) (2026-08-17)
- [Inside the keyv npm compromise: preinstall dropper + Claude/VS Code folder-open hooks + valid provenance on a poisoned build](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) (2026-08-04)
- [keyv/cacheable Mini Shai-Hulud: self-propagating worm, Ethereum-resolved C2, and Bun-runtime evasion](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16)

### ▫️ quiet shai-hulud  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-15 · latest 2026-09-24._

- [Mini Shai-Hulud still spreads four months on via never-restored hijacked actions-cool/issues-helper tags, planting Claude Code and VS Code hooks in six repos](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24) · _latest_
- [keyv/cacheable Mini Shai-Hulud: self-propagating worm, Ethereum-resolved C2, and Bun-runtime evasion](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)
- [The npm Threat Landscape: Attack Surface and Mitigations](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/) (2026-07-15)

### ▫️ quiet worm  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-04 · latest 2026-09-24._

- [Mini Shai-Hulud still spreads four months on via never-restored hijacked actions-cool/issues-helper tags, planting Claude Code and VS Code hooks in six repos](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24) · _latest_
- [MemTensor's @memtensor/memos-cloud-openclaw-plugin (npm 0.1.21, 0.1.23, 0.1.25) and MemoryOS (PyPI 2.0.34) shipped the 'sckit' Go worm after publish tokens were stolen through BASH_ENV in GitHub Actions release jobs](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [ChainDrop: Self-propagating npm worm mints valid Sigstore provenance and exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [keyv/cacheable Mini Shai-Hulud: self-propagating worm, Ethereum-resolved C2, and Bun-runtime evasion](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)

### ▫️ quiet authorization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-09-23._

- [Moquette MQTT broker: clientId wildcard injection into pattern ACLs gives cross-tenant read/write, plus pre-auth broker crash, Will-message authorization bypass and fail-open auth (GHSA-5f42-97gr-vfhq, CVE-2026-85724)](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [etcd: a READ grant on one key reads everything after it, because the Watch API skipped the range authorization Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### ▫️ quiet go  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-24 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [go-git reference names as path traversal: refs/heads/../../config overwrites .git metadata (GHSA-qgq7-7hm3-q39j)](https://github.com/advisories/GHSA-qgq7-7hm3-q39j) (2026-08-07)
- [Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq) (2026-07-24)

### ▫️ quiet iot  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-15 · latest 2026-09-24._

- [Faulty Samsung SmartThings firmware push bricked Bespoke AI fridges in Korea, spoiling food](https://arstechnica.com/gadgets/2026/09/owners-mourn-spoiled-food-after-firmware-update-bricks-samsung-smart-fridges/) (2026-09-24) · _latest_
- [Moquette MQTT broker: clientId wildcard injection into pattern ACLs gives cross-tenant read/write, plus pre-auth broker crash, Will-message authorization bypass and fail-open auth (GHSA-5f42-97gr-vfhq, CVE-2026-85724)](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-15)

### ▫️ quiet request-smuggling  ·  3 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-02-05 · latest 2026-09-23._

- [Turbo Intruder adds HTTP/3 engine (100k+ requests per second), HTTP/3 race-condition techniques and downgrade header injection; adapter brings HTTP/3-only targets into Burp](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)
- [CRLF-Powered Desync Attacks: header injection escalates to CDN-wide response queue poisoning + browser-side XSS](https://portswigger.net/research/crlf-powered-desync-attacks) (2026-08-05)
- [PortSwigger's Top 10 Web Hacking Techniques of 2025](https://portswigger.net/research/top-10-web-hacking-techniques-of-2025) (2026-02-05)

### ▫️ quiet threat-intel  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-15 · latest 2026-09-15._

- [Snyk opinion: the system that creates a change must not be its only validator, citing Anthropic's report on AI-assisted implant rebuilding](https://snyk.io/blog/ai-hurricane-is-here/) (2026-09-15)
- [Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/) (2026-08-25)
- [TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-15)

### ▫️ quiet ai-generated-code  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-09-15._

- [Snyk opinion: the system that creates a change must not be its only validator, citing Anthropic's report on AI-assisted implant rebuilding](https://snyk.io/blog/ai-hurricane-is-here/) (2026-09-15)
- [38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▫️ quiet bun-runtime  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-04._

- [keyv/cacheable Mini Shai-Hulud: self-propagating worm, Ethereum-resolved C2, and Bun-runtime evasion](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet business-logic  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-27 · latest 2026-08-10._

- [Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### ▫️ quiet chaindrop  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-21._

- [ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet code-review  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-07-30._

- [Cryptographic advisories are dominated by skipped code checks, not broken math — a range check would have stopped a 9.8 ECDSA bypass](https://semgrep.dev/blog/2026/crypto-is-fine-the-code-is-not) (2026-07-30)
- [38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▫️ quiet cryptography  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-30 · latest 2026-09-08._

- [phpseclib's X25519 leaks the full private key through a libgmp call-count side channel](https://github.com/advisories/GHSA-q97c-8qh3-fpc6) (2026-09-08)
- [Cryptographic advisories are dominated by skipped code checks, not broken math — a range check would have stopped a 9.8 ECDSA bypass](https://semgrep.dev/blog/2026/crypto-is-fine-the-code-is-not) (2026-07-30)

### ▫️ quiet exploit-chain  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-05 · latest 2026-07-20._

- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)

### ▫️ quiet git  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [go-git reference names as path traversal: refs/heads/../../config overwrites .git metadata (GHSA-qgq7-7hm3-q39j)](https://github.com/advisories/GHSA-qgq7-7hm3-q39j) (2026-08-07)

### ▫️ quiet incomplete-fix  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-09-08._

- [Hono's Path-Traversal Fix Only Blocked One Parent-Directory Segment — a Longer Run of '..' Still Escapes the Output Directory](https://github.com/advisories/GHSA-gqvv-2mrq-wpjv) (2026-09-08)
- [morgan's Log-Forging Fix Missed Unicode Line-Separator Code Points, Letting Attacker-Controlled Headers Split Log Records](https://github.com/advisories/GHSA-jxfw-x594-9x9m) (2026-09-08)

### ▫️ quiet malware  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-09 · latest 2026-07-15._

- [TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-15)
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### ▫️ quiet mcp  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-09-24._

- [GitHub Security Lab's open-source Fuzzing Taskflow uses an LLM agent to write AFL++ harnesses for C/C++ repos](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/) (2026-09-24) · _latest_
- [Can AI do novel security research? Meet the HTTP Terminator](https://portswigger.net/research/can-ai-do-novel-security-research) (2026-08-05)

### ▫️ quiet oidc  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-21._

- [ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet persistence  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-10._

- [JFrog Artifactory auth-bypass chain exploited in the wild, leaving Groovy plugin backdoors that survive patching and stolen token-signing keys](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201) (2026-09-10)
- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### ▫️ quiet phishing  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-30 · latest 2026-07-24._

- [Four stacked evasion techniques hide device-code phishing from scanners: blob URLs, client-side CAPTCHA gates, multi-hop SaaS flows, and source-code confusables](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt) (2026-07-24)
- [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) (2026-06-30)

### ▫️ quiet prompt-injection  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-09 · latest 2026-08-06._

- [CSS the bomb: sanitized webmail CSS steals tokens, keylogs Outlook, and turns Atlas AI browser into an exfil bot](https://portswigger.net/research/css-the-bomb-inside-your-inbox) (2026-08-06)
- [Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▫️ quiet pypi  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-09-23._

- [MemTensor's @memtensor/memos-cloud-openclaw-plugin (npm 0.1.21, 0.1.23, 0.1.25) and MemoryOS (PyPI 2.0.34) shipped the 'sckit' Go worm after publish tokens were stolen through BASH_ENV in GitHub Actions release jobs](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [Snyk Evo Agentic AppSec: autonomous remediation, non-executing package scanning, and a Claude CTF that shipped malware to PyPI](https://snyk.io/blog/remediation-agent-malicious-code-defense/) (2026-08-04)

### ▫️ quiet rust  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-04 · latest 2026-08-20._

- [Rust Supply-Chain Compromise Used Cargo's Own Yank Warning to Socially Engineer Developers Into the Malicious Version](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) (2026-08-20)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### ▫️ quiet sandbox-escape  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-09 · latest 2026-08-16._

- [A Widely-Used VS Code Extension (9.5M Installs) Chained a Markdown eval() Sink, an Untrusted Webview Message Dispatcher, and a vm.runInNewContext() Escape Into RCE](https://projectdiscovery.io/blog/a-9-5m-install-vs-code-extension-one-markdown-file-and-a-supply-chain-foothold) (2026-08-16)
- [Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▫️ quiet sast  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-07-28._

- [Introducing Semgrep Agentic Workflows: Automate Deep Vulnerability Hunting at Scale](https://semgrep.dev/blog/2026/introducing-semgrep-agentic-workflows-automate-deep-vulnerability-hunting-at-scale) (2026-07-28)
- [A working taxonomy of open-source AI code-security harnesses: exploitgen, skill-boosting, SAST+LLM](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses) (2026-07-20)

### ▫️ quiet sha-pinning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-12 · latest 2026-09-24._

- [Mini Shai-Hulud still spreads four months on via never-restored hijacked actions-cool/issues-helper tags, planting Claude Code and VS Code hooks in six repos](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24) · _latest_
- [Rolling Out Org-Wide GitHub Actions SHA-Pinning Enforcement Has Non-Obvious Failure Modes Beyond the Obvious Tag-Pinning Fix](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)

### ▫️ quiet sigstore  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-06._

- [ChainDrop: Self-propagating npm worm mints valid Sigstore provenance and exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet symlink  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-09 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▫️ quiet tooling  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-23._

- [Turbo Intruder adds HTTP/3 engine (100k+ requests per second), HTTP/3 race-condition techniques and downgrade header injection; adapter brings HTTP/3-only targets into Burp](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)
- [A working taxonomy of open-source AI code-security harnesses: exploitgen, skill-boosting, SAST+LLM](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses) (2026-07-20)

### ▫️ quiet xss  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-25 · latest 2026-09-24._

- [SourceHut account takeover via OSC 8 hyperlink XSS in ansi2html-rendered build logs (CVE-2026-92973; ansi2html >=1.7.0,<1.9.4, builds.sr.ht >=0.40.0,<0.105.1)](https://blog.arusekk.pl/posts/srht-account-takeover/) (2026-09-24) · _latest_
- [What's in a tag name? JavaScript, apparently](https://portswigger.net/research) (2026-08-25)

## AI Research

### 🔺 rising red-teaming  ·  6 findings (2 recent vs 0.5 expected) · 6 sources
_First seen 2025-03-13 · latest 2026-10-20._

- [METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/) (2026-10-20) · _latest_
- [Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access; each expects to invest at least $1B](https://www.anthropic.com/news/accenture-embedded-evaluation) (2026-10-19) · _latest_
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439) (2026-08-27)
- [Enhancing AI security through global AI red teaming](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/) (2026-07-27)
- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22)
- [Alignment auditing game: blind teams hunt a hidden objective planted via 52 fictional reward-model biases (2025, resurfaced)](https://www.anthropic.com/research/auditing-hidden-objectives) (2025-03-13)

### 🔺 rising evals  ·  20 findings (3 recent vs 2.8 expected) · 10 sources
_First seen 2023-12-07 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) (2026-10-19) · _latest_
- [POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_
- [Trail of Bits: 1Password's 26% clean-fix AI patching rate pools wrong-fix prompts and no-testing trials; with testing, 86% of patches blocked the exploit](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/) (2026-09-15)
- [Ask-E: An Environment for Calibrated Question Generation](https://arxiv.org/abs/2608.06933) (2026-08-10)
- [Multi-Legal-Bench: Evaluating LLMs on Legal Reasoning Across Jurisdictions, Languages, and Legal Traditions](https://arxiv.org/abs/2605.29738) (2026-08-10)

### ▪️ steady agents  ·  24 findings (1 recent vs 4.0 expected) · 8 sources
_First seen 2026-05 · latest 2026-10-19._

- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) (2026-10-19) · _latest_
- [Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?](https://arxiv.org/abs/2605.22148) (2026-08-10)
- [OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557) (2026-08-10)
- [Can AI agents conduct open-ended AI research? Early evidence from two case studies](https://arxiv.org/abs/2607.27191) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)
- [Homebot: A Personal AI Agent for Conversational Home Assistance and Automation](https://arxiv.org/abs/2608.02254) (2026-08-10)

### ▪️ steady benchmarks  ·  7 findings (1 recent vs 1.0 expected) · 5 sources
_First seen 2026-07-09 · latest 2026-10-19._

- [POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_
- ["LLM Agent Performance" Is Not a Single Evaluation Target](https://arxiv.org/abs/2602.03238) (2026-08-10)
- [Evaluating Investment Logic in Large Language Models: A Real-World Benchmark Towards Personalized Financial Agents](https://arxiv.org/abs/2608.06108) (2026-08-07)
- [GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models](https://arxiv.org/abs/2608.05948) (2026-08-07)
- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22)
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17)

### ▪️ steady calibration  ·  6 findings (1 recent vs 0.9 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [Ask-E: An Environment for Calibrated Question Generation](https://arxiv.org/abs/2608.06933) (2026-08-10)
- [Pre-Inference Routing for Cost-Efficient Document Field Extraction](https://arxiv.org/abs/2608.06607) (2026-08-10)
- [Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration](https://arxiv.org/abs/2605.27752) (2026-08-10)
- [Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183) (2026-08-10)
- [Beyond Post-Hoc Temperature Scaling: Bilevel Optimization for LLM Calibration](https://arxiv.org/abs/2608.07419) (2026-08-10)

### ▪️ steady robotics  ·  6 findings (1 recent vs 0.9 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-20._

- [RoboCasa-Shift: equal success-rate drops in a VLA robot policy hide very different failure stages](https://arxiv.org/abs/2610.27861) (2026-10-20) · _latest_
- [Scalable Long-Horizon Planning with Staggered Updates for Lifelong MAPF](https://arxiv.org/abs/2608.06702) (2026-08-10)
- [ODEWorld: A Continuous Predictive Architecture via Physical-Time Flow](https://arxiv.org/abs/2607.27924) (2026-08-10)
- [Fast and Accurate: An Adaptive VLA Inference Framework through Environment-aware Model Selection](https://arxiv.org/abs/2608.06434) (2026-08-10)
- [Representation Handoffs for OpenArm-Based Laboratory Mobile Manipulation](https://arxiv.org/abs/2608.07154) (2026-08-10)
- [Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317) (2026-08-10)

### ▪️ steady vlm  ·  5 findings (1 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-19._

- [POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_
- [SABRE: Scalable and Automated Benchmarking of VLMs under Stress](https://arxiv.org/abs/2608.07435) (2026-08-10)
- [Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054) (2026-08-10)
- [MultiView-Bench: A Diagnostic Benchmark for World-Centric Multi-View Integration in VLMs](https://arxiv.org/abs/2607.08970) (2026-08-10)
- [VLMs for Videogame Data Annotation](https://arxiv.org/abs/2608.05949) (2026-08-07)

### ▪️ steady guardrails  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-09 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)

### ▪️ steady llm-as-judge  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [MentalHealthBench scores model replies against weighted, expert-consensus rubrics across acuity levels and personas](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [SkillTV-Bench: Benchmarking How Well Judges Perform on Skill-Augmented Agentic Execution](https://arxiv.org/abs/2608.05573) (2026-08-07)

### ▪️ steady governance  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-20._

- [Anthropic embeds METR with employee-like access, but keeps control of what counts as redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators) (2026-10-20) · _latest_
- [Birfy/agentdescent](https://github.com/Birfy/agentdescent) (2026-08-10)

### ▪️ steady long-horizon-tasks  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-22 · latest 2026-10-20._

- [RoboCasa-Shift: equal success-rate drops in a VLA robot policy hide very different failure stages](https://arxiv.org/abs/2610.27861) (2026-10-20) · _latest_
- [METR: Claude Opus 5.5 is an on-trend, modest AI R&D gain over Fable 5.1, unlikely to fully automate AI R&D; Anthropic's own development estimated ~1.5x accelerated by AI](https://metr.org/blog/2026-09-22-claude-opus-5-5/) (2026-09-22)

### ▪️ steady misalignment  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-16 · latest 2026-10-20._

- [METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/) (2026-10-20) · _latest_
- [OpenAI sets up a fast-track misalignment disclosure process and publishes six first reports, including models injecting instructions into their own context summaries](https://openai.com/index/model-misalignment-reporting-framework) (2026-09-16)

### ▪️ steady routing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality](https://arxiv.org/abs/2608.05263) (2026-08-07)

### ▪️ steady third-party-evals  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-22 · latest 2026-10-19._

- [Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access; each expects to invest at least $1B](https://www.anthropic.com/news/accenture-embedded-evaluation) (2026-10-19) · _latest_
- [METR: Claude Opus 5.5 is an on-trend, modest AI R&D gain over Fable 5.1, unlikely to fully automate AI R&D; Anthropic's own development estimated ~1.5x accelerated by AI](https://metr.org/blog/2026-09-22-claude-opus-5-5/) (2026-09-22)

### ▫️ quiet benchmark  ·  17 findings (0 recent vs 2.9 expected) · 7 sources
_First seen 2026-05 · latest 2026-09-23._

- [MentalHealthBench scores model replies against weighted, expert-consensus rubrics across acuity levels and personas](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [UK AISI publishes verified benchmark results with run configuration in a shared schema, showing scores shift with inference compute and protocol](https://huggingface.co/blog/evaleval-aisi) (2026-09-22)
- [Explicit Edit Benchmark: an open set of 226 byte-exact file-editing tasks for comparing coding agents and harnesses, with community-submitted runs](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)
- [SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization](https://arxiv.org/abs/2602.12187) (2026-08-10)
- [FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853) (2026-08-10)
- [Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208) (2026-08-10)

### ▫️ quiet multi-agent  ·  12 findings (0 recent vs 2.1 expected) · 4 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [Multi-Agent Forensic Reasoning for Generalizable Deepfake Video Detection](https://arxiv.org/abs/2608.06865) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)
- [Scalable Long-Horizon Planning with Staggered Updates for Lifelong MAPF](https://arxiv.org/abs/2608.06702) (2026-08-10)
- [PHOENIX: Fine-Tuned SLM-Powered Autonomous Satellite Lifetime Extension via Predictive Self-Healing and Multi-Agent AI Recovery](https://arxiv.org/abs/2608.07126) (2026-08-10)
- [Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317) (2026-08-10)

### ▫️ quiet harness  ·  10 findings (0 recent vs 1.7 expected) · 9 sources
_First seen 2026-05 · latest 2026-09-16._

- [HarnessTax: across 21 model-harness pairs, harness choice barely moved success but changed cost up to 5x; four-tool Pi matched Claude Code and Codex CLI](https://harnesstax.github.io/) (2026-09-16)
- [Explicit Edit Benchmark: an open set of 226 byte-exact file-editing tasks for comparing coding agents and harnesses, with community-submitted runs](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)
- ["LLM Agent Performance" Is Not a Single Evaluation Target](https://arxiv.org/abs/2602.03238) (2026-08-10)
- [LLM 0.32: reasoning traces, server-side provider tools, human-approval pause/resume, and content-addressable message logs](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) (2026-08-04)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)
- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22)

### ▫️ quiet llm  ·  9 findings (0 recent vs 1.6 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [Let's Unlearn Stereotypes Before Decision-Making: Assessing the Impact of Intrinsic Bias Mitigation on Downstream Fairness in LLMs](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Solver-Guided Reasoning for Mixed-Equilibrium Strategies](https://arxiv.org/abs/2608.06741) (2026-08-10)
- [Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)
- [SCALE: Scientific Concept Aggregation via LLMs and Embeddings for Fine-Grained Taxonomy Extension](https://arxiv.org/abs/2608.07254) (2026-08-10)

### ▫️ quiet rag  ·  9 findings (0 recent vs 1.6 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [Hugging Face's funes: shared agent memory that keeps the raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization](https://arxiv.org/abs/2602.12187) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [GPTKB 2.0: Browsing, Querying, and Auditing a Disambiguated LLM-Derived Knowledge Base](https://arxiv.org/abs/2608.06992) (2026-08-10)
- [Agentic self-driving microscopy benchmarks support qualification but do not necessarily generalize to unseen tasks](https://arxiv.org/abs/2608.05266) (2026-08-07)

### ▫️ quiet evaluation  ·  8 findings (0 recent vs 1.4 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Zero Gap Is Not Restoration: Stratified Per-Question Probability Evaluation and Step-wise Mitigation of Benchmark Contamination](https://arxiv.org/abs/2608.07341) (2026-08-10)
- [Rethinking Evaluation Paradigms in IBP-based Certified Training](https://arxiv.org/abs/2606.02134) (2026-08-10)
- [Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration](https://arxiv.org/abs/2605.27752) (2026-08-10)
- [SenWorld: A Digital-Twin Simulation for Generating Context-Rich Evaluation Data](https://arxiv.org/abs/2607.19949) (2026-08-10)
- [Seeking SOTA: Time-Series Forecasting Must Adopt Taxonomy-Specific Evaluation to Dispel Illusory Gains](https://arxiv.org/abs/2603.15506) (2026-08-10)
- [Boundary Density Likelihood for Direct Event-Time Supervision](https://arxiv.org/abs/2408.12792) (2026-08-10)

### ▫️ quiet interpretability  ·  8 findings (0 recent vs 1.2 expected) · 3 sources
_First seen 2025-03-13 · latest 2026-08-10._

- [Measuring Concept Content in Text from LLM Activations: ESG Evidence from Concept Vectors and Linear Probes](https://arxiv.org/abs/2608.07208) (2026-08-10)
- [Mathematical Principles and Experimental Discoveries of the Emergence of Symbolic Patterns in Artificial Neural Networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [Recovering Lesion Parameters from Aphasic Picture Naming Error Profiles in Large Language Models](https://arxiv.org/abs/2608.06429) (2026-08-10)
- [Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054) (2026-08-10)
- [Geo-Spatial Concept Probing of Large Language Models: Abstraction, Compositionality, and Grounding](https://arxiv.org/abs/2608.07353) (2026-08-10)
- [Understanding Differentiable Embeddings Through Differential and Integral Geometry](https://arxiv.org/abs/2608.06809) (2026-08-10)

### ▫️ quiet kv-cache  ·  8 findings (0 recent vs 1.4 expected) · 3 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](https://arxiv.org/abs/2607.20457) (2026-08-10)
- [Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Topology-Aware Data Movement for Disaggregated GPU Inference](https://arxiv.org/abs/2607.28633) (2026-08-10)
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968) (2026-08-10)

### ▫️ quiet reinforcement-learning  ·  8 findings (0 recent vs 1.4 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Sub-Quadratic Bisimulation Metrics via Approximate Nearest Neighbors: Coverage-Augmented Guarantees and Computable Two-Sided Certificates](https://arxiv.org/abs/2608.06762) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [Aftab: A Comprehensive Benchmark of CNN Encoders and Advanced Value Functions in Parallelized Q-Networks](https://arxiv.org/abs/2608.07335) (2026-08-10)
- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Beyond Isolation: Unlocking Reinforcement Learning Component Synergy for Sample-Efficient Continuous Control](https://arxiv.org/abs/2608.07086) (2026-08-10)
- [Wasserstein Policy Gradient for Entropy-Regularized Linear-Quadratic Control](https://arxiv.org/abs/2608.07433) (2026-08-10)

### ▫️ quiet agent-harness  ·  7 findings (0 recent vs 1.2 expected) · 3 sources
_First seen 2026-07-28 · latest 2026-08-10._

- [Fzkuji/OpenProgram](https://github.com/Fzkuji/OpenProgram) (2026-08-10)
- [aeonfun/aeon](https://github.com/aeonfun/aeon) (2026-08-10)
- [wanmol/goal-flow](https://github.com/wanmol/goal-flow) (2026-08-10)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](https://arxiv.org/abs/2608.06811) (2026-08-10)
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853) (2026-08-10)

### ▫️ quiet long-context  ·  7 findings (0 recent vs 1.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) (2026-08-10)
- [Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](https://arxiv.org/abs/2607.20457) (2026-08-10)
- [Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515) (2026-08-10)

### ▫️ quiet multimodal  ·  7 findings (0 recent vs 1.2 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Debias in Text, Believe Your Eyes: Text-Anchored Cross-Modal Transfer for Visual Counter-Commonsense Reasoning](https://arxiv.org/abs/2608.06938) (2026-08-10)
- [Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276) (2026-08-10)
- [Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183) (2026-08-10)
- [SignVerse-2M: A Two-Million-Clip Pose-Native Universe of 55+ Sign Languages](https://arxiv.org/abs/2605.01720) (2026-08-10)
- [Seeing Is Not Deciding: Can Multimodal LLMs Act as Effective CEOs?](https://arxiv.org/abs/2608.05864) (2026-08-07)
- [C3PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models](https://arxiv.org/abs/2608.05381) (2026-08-07)

### ▫️ quiet time-series  ·  7 findings (0 recent vs 1.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [KReF: Training-Free Retrieval for Long-Term Time-Series Forecasting and Predictive Uncertainty](https://arxiv.org/abs/2608.06748) (2026-08-10)
- [Large Causal Models for Temporal Causal Discovery](https://arxiv.org/abs/2602.18662) (2026-08-10)
- [Seeking SOTA: Time-Series Forecasting Must Adopt Taxonomy-Specific Evaluation to Dispel Illusory Gains](https://arxiv.org/abs/2603.15506) (2026-08-10)
- [Optimization-based Online Conformal Prediction for Multi-step Forecasting](https://arxiv.org/abs/2508.13362) (2026-08-10)
- [When GNNs Fail: Quantifying and Overcoming Temporal Correlation Volatility in Time Series](https://arxiv.org/abs/2608.07333) (2026-08-10)
- [Embedded Variational Neural Stochastic Differential Equations for Learning Heterogeneous Dynamics](https://arxiv.org/abs/2604.00669) (2026-08-10)

### ▫️ quiet fine-tuning  ·  6 findings (0 recent vs 1.0 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897) (2026-08-10)
- [IFCLoRA: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2607.22251) (2026-08-10)
- [Dual-Node NVIDIA DGX Spark over Tailscale: A Remote-Access Testbed for Distributed LLM Training and Cyber-Threat-Intelligence Fine-Tuning](https://arxiv.org/abs/2608.07226) (2026-08-10)
- [LoCA: Spatially-Aware Low-Rank Convolutional Adaptation of Vision Foundation Models](https://arxiv.org/abs/2607.06918) (2026-08-10)
- [Improving Attributed Long-form Question Answering with Intent Awareness](https://arxiv.org/abs/2603.27435) (2026-08-10)
- [Hyper-ES: Effective Evolution Strategies for LLM Reasoning via Descent Direction Merging](https://arxiv.org/abs/2608.05541) (2026-08-07)

### ▫️ quiet claude-code  ·  5 findings (0 recent vs 0.9 expected) · 5 sources
_First seen 2026-06 · latest 2026-08-10._

- [OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557) (2026-08-10)
- [Automated Claude Code + Opus 4.6 pipeline finds a real Linux sandbox-escape CVE (CVE-2026-5674)](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/) (2026-07-30)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04)
- [Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent) (2026-06)

### ▫️ quiet medical-imaging  ·  5 findings (0 recent vs 0.9 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [H2AL: Hyperbolic Hierarchy-aware Aggregative Learning for Registration-based Few-shot Medical Image Segmentation](https://arxiv.org/abs/2608.07340) (2026-08-10)
- [FedDOSE: Federated Learning Framework Decomposing Site Effects for Modeling Brain Dynamic Functional Connectivity](https://arxiv.org/abs/2608.07393) (2026-08-10)
- [Machine Learning-Based Inter-Crystal Scatter Recovery for Ultra-High Resolution PET Imaging](https://arxiv.org/abs/2608.07155) (2026-08-10)
- [International Transfer of Stochastic Cortical Self-Reconstruction](https://arxiv.org/abs/2608.07092) (2026-08-10)
- [Representation-driven Endoscopic Visual Embedding Alignment for Latent Generation](https://arxiv.org/abs/2608.07176) (2026-08-10)

### ▫️ quiet mllm  ·  5 findings (0 recent vs 0.9 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Multi-Agent Forensic Reasoning for Generalizable Deepfake Video Detection](https://arxiv.org/abs/2608.06865) (2026-08-10)
- [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088) (2026-08-10)
- [An AI4AI Framework for Visual Token Pruning](https://arxiv.org/abs/2608.07193) (2026-08-10)
- [Judge a Book by its Cover: Investigating Multi-Modal LLMs for Multi-Page Handwritten Document Transcription](https://arxiv.org/abs/2502.20295) (2026-08-10)
- [Unified Agent: Managing Interactions across Devices](https://arxiv.org/abs/2608.05729) (2026-08-07)

### ▫️ quiet prompt-engineering  ·  5 findings (0 recent vs 0.9 expected) · 3 sources
_First seen 2026-07-28 · latest 2026-08-10._

- [In-Context Examples Suppress Scientific Knowledge Recall in LLMs](https://arxiv.org/abs/2604.27540) (2026-08-10)
- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)
- [Signal or Spurious Cue? A Randomized Audit of Survey-Country Metadata in LLM Social Inference](https://arxiv.org/abs/2608.06085) (2026-08-07)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)
- [How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/) (2026-07-28)

### ▫️ quiet coding-agents  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-21 · latest 2026-09-16._

- [HarnessTax: across 21 model-harness pairs, harness choice barely moved success but changed cost up to 5x; four-tool Pi matched Claude Code and Codex CLI](https://harnesstax.github.io/) (2026-09-16)
- [Explicit Edit Benchmark: an open set of 226 byte-exact file-editing tasks for comparing coding agents and harnesses, with community-submitted runs](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)
- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet counterfactual  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Recovering Lesion Parameters from Aphasic Picture Naming Error Profiles in Large Language Models](https://arxiv.org/abs/2608.06429) (2026-08-10)
- [Poli-Bias: Understanding and Measuring Large Language Model Biases in International Political Conflicts](https://arxiv.org/abs/2608.06123) (2026-08-07)
- [C3PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models](https://arxiv.org/abs/2608.05381) (2026-08-07)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)

### ▫️ quiet edge-ai  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885) (2026-08-10)
- [MiCoPro: End-to-End Mixed Precision HW/SW Co-design with HW-aware Proxy Model](https://arxiv.org/abs/2608.06916) (2026-08-10)
- [Human-Centered Explainable AI for TinyML Edge Devices: A Pareto-Based Selection Framework with LLM-Guided Design](https://arxiv.org/abs/2608.07091) (2026-08-10)
- [Synthetic LiDAR Data Generation and Deterministic Downsampling for Point Cloud Classification on the Edge](https://arxiv.org/abs/2608.07106) (2026-08-10)

### ▫️ quiet embeddings  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Calibrating WEAT Against Anisotropy: ZCA Whitening as a Geometric Pre-Processing Step for Embedding Association Tests](https://arxiv.org/abs/2608.06908) (2026-08-10)
- [Understanding Differentiable Embeddings Through Differential and Integral Geometry](https://arxiv.org/abs/2608.06809) (2026-08-10)
- [SCALE: Scientific Concept Aggregation via LLMs and Embeddings for Fine-Grained Taxonomy Extension](https://arxiv.org/abs/2608.07254) (2026-08-10)
- [Towards a Theoretical Understanding of Two Tower Recommendation Models](https://arxiv.org/abs/2403.00802) (2026-08-10)

### ▫️ quiet federated-learning  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SSTQ: Privacy-Preserving Vector Quantization via Subsampled Stochastic TurboQuant](https://arxiv.org/abs/2608.05127) (2026-08-10)
- [Theoretical Foundations of Communication-Efficient, Robust, and Practical Distributed and Federated Optimization](https://arxiv.org/abs/2608.06563) (2026-08-10)
- [Capacity Confounds and Coverage Guarantees in Adaptive Sub-model Federated Learning](https://arxiv.org/abs/2608.07157) (2026-08-10)
- [FedDOSE: Federated Learning Framework Decomposing Site Effects for Modeling Brain Dynamic Functional Connectivity](https://arxiv.org/abs/2608.07393) (2026-08-10)

### ▫️ quiet harness-design  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-07-21 · latest 2026-08-10._

- [Birfy/agentdescent](https://github.com/Birfy/agentdescent) (2026-08-10)
- [Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding](https://arxiv.org/abs/2608.05876) (2026-08-07)
- [VLMs for Videogame Data Annotation](https://arxiv.org/abs/2608.05949) (2026-08-07)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet healthcare  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [PULSE: Agentic Investigation with Passive Sensing for Proactive Affective Intervention in Cancer Survivorship](https://arxiv.org/abs/2605.17679) (2026-08-10)
- [LSEAD: A Privacy-Preserving LLM-Based Speech Analysis Framework for Early Alzheimer's Disease Screening](https://arxiv.org/abs/2608.07378) (2026-08-10)
- [From Siloed Algorithms to Compliance-First Agentic Platforms: A Multi-Layered Architecture for Hospital AI Systems](https://arxiv.org/abs/2608.06112) (2026-08-07)
- [From Continuous Predictors to Clinical Thresholds: Early Evidence on Performance Trade-offs of Guideline-Based Categorisation for Ischaemic Stroke Outcome Prediction](https://arxiv.org/abs/2608.05203) (2026-08-07)

### ▫️ quiet inference  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968) (2026-08-10)
- [CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [vLLM anatomy: paged attention + continuous batching + KV-cache block pool as the load-bearing abstractions for high-throughput LLM serving](https://www.aleksagordic.com/blog/vllm) (2026-08-06)

### ▫️ quiet llm-agents  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-27._

- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439) (2026-08-27)
- [Harnessing the Synergy between LLM Agents and Knowledge Graphs for Urban Socioeconomic Prediction](https://arxiv.org/abs/2411.00028) (2026-08-10)
- [From Economic Agents to Agentic Economies: A Systems Blueprint for Economic World Models](https://arxiv.org/abs/2608.06020) (2026-08-07)

### ▫️ quiet lora  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [IFCLoRA: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2607.22251) (2026-08-10)
- [Theoretical Foundations of Communication-Efficient, Robust, and Practical Distributed and Federated Optimization](https://arxiv.org/abs/2608.06563) (2026-08-10)
- [LoCA: Forward-Only LLM Tuning after One-Shot Calibration with Local Credit Assignment](https://arxiv.org/abs/2608.03020) (2026-08-10)
- [LoCA: Spatially-Aware Low-Rank Convolutional Adaptation of Vision Foundation Models](https://arxiv.org/abs/2607.06918) (2026-08-10)

### ▫️ quiet systems  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968) (2026-08-10)
- [CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM](https://arxiv.org/abs/2504.17584) (2026-08-10)
- [Homebot: A Personal AI Agent for Conversational Home Assistance and Automation](https://arxiv.org/abs/2608.02254) (2026-08-10)
- [SNI-GNN: SmartNIC-Assisted Full-Graph GNN Training with In-Network Embedding Prediction](https://arxiv.org/abs/2608.06441) (2026-08-06)

### ▫️ quiet tool-use  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-07-04 · latest 2026-08-10._

- [PULSE: Agentic Investigation with Passive Sensing for Proactive Affective Intervention in Cancer Survivorship](https://arxiv.org/abs/2605.17679) (2026-08-10)
- [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-07)
- [LLM 0.32: reasoning traces, server-side provider tools, human-approval pause/resume, and content-addressable message logs](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) (2026-08-04)
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04)

### ▫️ quiet agent-memory  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [Hugging Face's funes: shared agent memory that keeps the raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515) (2026-08-10)
- [Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay](https://arxiv.org/abs/2608.05784) (2026-08-07)

### ▫️ quiet agentic-rl  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) (2026-08-10)
- [Trajectory-Relative Hindsight Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.07371) (2026-08-10)
- [iARCS: Iterative Agentic RL for Controllable 3D Scene Generation](https://arxiv.org/abs/2608.06161) (2026-08-07)

### ▫️ quiet bias  ·  3 findings (0 recent vs 0.3 expected) · 3 sources
_First seen 2023-12-07 · latest 2026-08-10._

- [Let's Unlearn Stereotypes Before Decision-Making: Assessing the Impact of Intrinsic Bias Mitigation on Downstream Fairness in LLMs](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Poli-Bias: Understanding and Measuring Large Language Model Biases in International Political Conflicts](https://arxiv.org/abs/2608.06123) (2026-08-07)
- [Anthropic's discrim-eval: generated decision prompts with varied demographics surfaced positive and negative discrimination in Claude 2.0 (2023 paper, re-surfaced)](https://www.anthropic.com/research/evaluating-and-mitigating-discrimination-in-language-model-decisions) (2023-12-07)

### ▫️ quiet codex  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-07-28._

- [How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/) (2026-07-28)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### ▫️ quiet compaction  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-22 · latest 2026-09-16._

- [OpenAI sets up a fast-track misalignment disclosure process and publishes six first reports, including models injecting instructions into their own context summaries](https://openai.com/index/model-misalignment-reporting-framework) (2026-09-16)
- [OpenAI launches the Agents API in public beta: a hosted Codex harness with managed compaction, tool search, subagents and a choice of sandbox](https://openai.com/index/introducing-the-agents-api) (2026-09-10)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### ▫️ quiet dataset  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [IceHorizon: A Dataset for Horizon Detection in Ice-Covered Maritime Environments and Comparative Evaluation of Detection Methods](https://arxiv.org/abs/2608.07018) (2026-08-10)
- [ArchEGraph: A Large-Scale Graph Dataset for Geometry-Topology-Physics Aligned Building Energy Modeling](https://arxiv.org/abs/2608.06772) (2026-08-10)
- [SignVerse-2M: A Two-Million-Clip Pose-Native Universe of 55+ Sign Languages](https://arxiv.org/abs/2605.01720) (2026-08-10)

### ▫️ quiet efficiency  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885) (2026-08-10)
- [LoCA: Forward-Only LLM Tuning after One-Shot Calibration with Local Credit Assignment](https://arxiv.org/abs/2608.03020) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)

### ▫️ quiet fairness  ·  3 findings (0 recent vs 0.3 expected) · 3 sources
_First seen 2023-12-07 · latest 2026-08-10._

- [Calibrating WEAT Against Anisotropy: ZCA Whitening as a Geometric Pre-Processing Step for Embedding Association Tests](https://arxiv.org/abs/2608.06908) (2026-08-10)
- [Let's Unlearn Stereotypes Before Decision-Making: Assessing the Impact of Intrinsic Bias Mitigation on Downstream Fairness in LLMs](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Anthropic's discrim-eval: generated decision prompts with varied demographics surfaced positive and negative discrimination in Claude 2.0 (2023 paper, re-surfaced)](https://www.anthropic.com/research/evaluating-and-mitigating-discrimination-in-language-model-decisions) (2023-12-07)

### ▫️ quiet finance  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853) (2026-08-10)
- [Beyond Co-Movement: Locality by Exposures Enables a Joint Factor-Graph Framework for Portfolio Diversification](https://arxiv.org/abs/2608.06618) (2026-08-10)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)

### ▫️ quiet generalization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Mathematical Principles and Experimental Discoveries of the Emergence of Symbolic Patterns in Artificial Neural Networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [Optimization as a Dynamical System: Generative Schedules from Latent ODEs](https://arxiv.org/abs/2509.23052) (2026-08-10)
- [Agentic self-driving microscopy benchmarks support qualification but do not necessarily generalize to unseen tasks](https://arxiv.org/abs/2608.05266) (2026-08-07)

### ▫️ quiet generative-models  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [How Molecular Generative Models Organize Molecular Identity](https://arxiv.org/abs/2608.06956) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [Representation-driven Endoscopic Visual Embedding Alignment for Latent Generation](https://arxiv.org/abs/2608.07176) (2026-08-10)

### ▫️ quiet gnn  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [A Physics-Inspired Classical Digital Twin of Cortical Dynamics: A Band-Stratified Metriplectic Port-Hamiltonian Neural Network Learned from Brain-Computer-Interface EEG](https://arxiv.org/abs/2607.10439) (2026-08-10)
- [When GNNs Fail: Quantifying and Overcoming Temporal Correlation Volatility in Time Series](https://arxiv.org/abs/2608.07333) (2026-08-10)
- [SNI-GNN: SmartNIC-Assisted Full-Graph GNN Training with In-Network Embedding Prediction](https://arxiv.org/abs/2608.06441) (2026-08-06)

### ▫️ quiet hallucination  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-16 · latest 2026-08-10._

- [Same Attention, Different Truths: Put Logit-Lens over Visual Attention to Detect and Mitigate LVLM Object Hallucination](https://arxiv.org/abs/2608.07302) (2026-08-10)
- [TriQua: Reconciling Granularity and Context in Factuality Evaluation](https://arxiv.org/abs/2608.05228) (2026-08-07)
- [Protective Capacity Hallucination: given a protective role and no capability boundary, models may claim to have taken actions they cannot perform](https://arxiv.org/abs/2607.13596) (2026-07-16)

### ▫️ quiet mdp  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Sub-Quadratic Bisimulation Metrics via Approximate Nearest Neighbors: Coverage-Augmented Guarantees and Computable Two-Sided Certificates](https://arxiv.org/abs/2608.06762) (2026-08-10)
- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Posture and Sustainment Optimization Under Adversarial Uncertainty](https://arxiv.org/abs/2608.05256) (2026-08-07)

### ▫️ quiet multilingual  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-27 · latest 2026-08-10._

- [Multi-Legal-Bench: Evaluating LLMs on Legal Reasoning Across Jurisdictions, Languages, and Legal Traditions](https://arxiv.org/abs/2605.29738) (2026-08-10)
- [An Agentic Hybrid Top-Down and Bottom-Up Approach to Knowledge Graph Generation](https://arxiv.org/abs/2608.07023) (2026-08-10)
- [Enhancing AI security through global AI red teaming](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/) (2026-07-27)

### ▫️ quiet position-paper  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Toward a Causal Data Management Ecosystem for Decision Making and Agentic AI](https://arxiv.org/abs/2608.07214) (2026-08-10)
- [Alignment has a Fantasia Problem](https://arxiv.org/abs/2604.21827) (2026-08-10)
- [Agentic Nesting: A New Methodology for Existing Enterprise Application Integration and Services](https://arxiv.org/abs/2608.05159) (2026-08-07)

### ▫️ quiet provenance  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-09-03._

- [Hugging Face's funes: shared agent memory that keeps the raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [How Do LLM Agents Actually Get the Flag? Trace-Level Provenance for Agentic Offensive-Security Evaluation](https://arxiv.org/abs/2608.26237) (2026-08-26)
- [GPTKB 2.0: Browsing, Querying, and Auditing a Disambiguated LLM-Derived Knowledge Base](https://arxiv.org/abs/2608.06992) (2026-08-10)

### ▫️ quiet quantization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SSTQ: Privacy-Preserving Vector Quantization via Subsampled Stochastic TurboQuant](https://arxiv.org/abs/2608.05127) (2026-08-10)
- [CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [MiCoPro: End-to-End Mixed Precision HW/SW Co-design with HW-aware Proxy Model](https://arxiv.org/abs/2608.06916) (2026-08-10)

### ▫️ quiet reasoning  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Solver-Guided Reasoning for Mixed-Equilibrium Strategies](https://arxiv.org/abs/2608.06741) (2026-08-10)
- [Refining Over Resampling: Test-Time Self-Correction for LLM Reasoning](https://arxiv.org/abs/2608.05643) (2026-08-07)
- [Hyper-ES: Effective Evolution Strategies for LLM Reasoning via Descent Direction Merging](https://arxiv.org/abs/2608.05541) (2026-08-07)

### ▫️ quiet sandboxing  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-08-10._

- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities) (2026-08-07)
- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22)

### ▫️ quiet scientific-computing  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-28 · latest 2026-08-10._

- [In Situ Training of Implicit Neural Compressors for Scientific Simulations via Sketch-Based Regularization](https://arxiv.org/abs/2511.02659) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)

### ▫️ quiet agent-skills  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-09-15._

- [Trail of Bits: 1Password's 26% clean-fix AI patching rate pools wrong-fix prompts and no-testing trials; with testing, 86% of patches blocked the exploit](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/) (2026-09-15)
- [SkillHEX: Improving Agent Skills via Hypothesis-Driven Autonomous Exploration and Exploitation](https://arxiv.org/abs/2608.05628) (2026-08-07)

### ▫️ quiet ai-code-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-17 · latest 2026-07-22._

- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22)
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17)

### ▫️ quiet benchmark-critique  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-15._

- [Trail of Bits: 1Password's 26% clean-fix AI patching rate pools wrong-fix prompts and no-testing trials; with testing, 86% of patches blocked the exploit](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/) (2026-09-15)
- [Seeking SOTA: Time-Series Forecasting Must Adopt Taxonomy-Specific Evaluation to Dispel Illusory Gains](https://arxiv.org/abs/2603.15506) (2026-08-10)

### ▫️ quiet benchmarking  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SABRE: Scalable and Automated Benchmarking of VLMs under Stress](https://arxiv.org/abs/2608.07435) (2026-08-10)
- [Hyperbolic Graph Embedders for Link Prediction and Topology Reconstruction](https://arxiv.org/abs/2608.07029) (2026-08-10)

### ▫️ quiet capability-elicitation  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-08-26._

- [How Do LLM Agents Actually Get the Flag? Trace-Level Provenance for Agentic Offensive-Security Evaluation](https://arxiv.org/abs/2608.26237) (2026-08-26)
- [Willison: the OpenAI/Hugging Face 'accidental attack' happened during an RLVR training run, not deployment](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything) (2026-08-08)

### ▫️ quiet compression  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-08-10._

- [Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [SQLite compressed text-history prototypes](https://simonwillison.net/2026/Aug/9/sqlite-text-history-prototype/#atom-everything) (2026-08-09)

### ▫️ quiet computer-vision  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [IceHorizon: A Dataset for Horizon Detection in Ice-Covered Maritime Environments and Comparative Evaluation of Detection Methods](https://arxiv.org/abs/2608.07018) (2026-08-10)
- [MaskFlow: Precise, Consistent and Seamless Regional Image Editing](https://arxiv.org/abs/2608.06929) (2026-08-10)

### ▫️ quiet context-management  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-07-22._

- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet continual-learning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897) (2026-08-10)
- [In Situ Training of Implicit Neural Compressors for Scientific Simulations via Sketch-Based Regularization](https://arxiv.org/abs/2511.02659) (2026-08-10)

### ▫️ quiet cost  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-09-16._

- [HarnessTax: across 21 model-harness pairs, harness choice barely moved success but changed cost up to 5x; four-tool Pi matched Claude Code and Codex CLI](https://harnesstax.github.io/) (2026-09-16)
- [GitHub Models is now retired](https://simonwillison.net/2026/Aug/9/github-models-is-now-retired/#atom-everything) (2026-08-09)

### ▫️ quiet cost-optimization  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Pre-Inference Routing for Cost-Efficient Document Field Extraction](https://arxiv.org/abs/2608.06607) (2026-08-10)
- [PDF-to-markdown pipelines are the hidden token chewer inside enterprise AI adoption](https://simonwillison.net/2026/Aug/7/pdfs-are-terrible/) (2026-08-07)

### ▫️ quiet cot-monitoring  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Counterfactual Simulation Training for Chain-of-Thought Faithfulness](https://arxiv.org/abs/2602.20710) (2026-08-10)
- [OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities) (2026-08-07)

### ▫️ quiet explainability  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Mathematical Principles and Experimental Discoveries of the Emergence of Symbolic Patterns in Artificial Neural Networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [From Continuous Predictors to Clinical Thresholds: Early Evidence on Performance Trade-offs of Guideline-Based Categorisation for Ischaemic Stroke Outcome Prediction](https://arxiv.org/abs/2608.05203) (2026-08-07)

### ▫️ quiet flow-matching  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [MaskFlow: Precise, Consistent and Seamless Regional Image Editing](https://arxiv.org/abs/2608.06929) (2026-08-10)

### ▫️ quiet forecasting  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [KReF: Training-Free Retrieval for Long-Term Time-Series Forecasting and Predictive Uncertainty](https://arxiv.org/abs/2608.06748) (2026-08-10)
- [When GNNs Fail: Quantifying and Overcoming Temporal Correlation Volatility in Time Series](https://arxiv.org/abs/2608.07333) (2026-08-10)

### ▫️ quiet graphics  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [RenderFormer++: Scalable and Physics-Informed Feed-Forward Neural Rendering](https://arxiv.org/abs/2606.30380) (2026-08-10)
- [WorldClaw: Agentic 3D Open-World Generation at Scale](https://arxiv.org/abs/2608.05248) (2026-08-07)

### ▫️ quiet groundedness  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-17 · latest 2026-08-07._

- [Evaluating Investment Logic in Large Language Models: A Real-World Benchmark Towards Personalized Financial Agents](https://arxiv.org/abs/2608.06108) (2026-08-07)
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17)

### ▫️ quiet grpo  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [CreativeInstruct: Scalably Teaching LLMs to Balance Quality, Creativity, and Diversity](https://arxiv.org/abs/2608.07460) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)

### ▫️ quiet inference-cost  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849) (2026-08-10)
- [An AI4AI Framework for Visual Token Pruning](https://arxiv.org/abs/2608.07193) (2026-08-10)

### ▫️ quiet inference-efficiency  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Retrofitting Linear Attention into Diffusion Language Models](https://arxiv.org/abs/2608.06628) (2026-08-10)
- [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088) (2026-08-10)

### ▫️ quiet llm-inference  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Multi-Level Modeling of Large Language Model Inference Latency and Energy via Hybrid Analytical--Machine-Learning Predictors](https://arxiv.org/abs/2608.06723) (2026-08-10)
- [CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM](https://arxiv.org/abs/2504.17584) (2026-08-10)

### ▫️ quiet mcp  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-09._

- [universal-tool-calling-protocol/utcp-specification](https://github.com/universal-tool-calling-protocol/utcp-specification) (2026-08-09)
- [CASCADE: An Agentic Regulatory Network Framework for Patient-Data-Validated Downstream Perturbation Prediction](https://arxiv.org/abs/2608.05359) (2026-08-07)

### ▫️ quiet mechanistic-interpretability  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks on Symmetric Data](https://arxiv.org/abs/2511.09432) (2026-08-10)

### ▫️ quiet mental-health  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-23._

- [MentalHealthBench scores model replies against weighted, expert-consensus rubrics across acuity levels and personas](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [Neurai-VN Benchmark: Standardized Machine Learning Models for Multimodal Digital Phenotyping in Mental Health Classification](https://arxiv.org/abs/2607.25232) (2026-08-10)

### ▫️ quiet multi-turn  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-07._

- [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-07)
- [Innocent Panels, Hateful Stories: Evaluating and Detecting Hateful Intent in Multi-Turn Visual Story Generation](https://arxiv.org/abs/2608.05210) (2026-08-07)

### ▫️ quiet orchestration  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06 · latest 2026-08-07._

- [OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality](https://arxiv.org/abs/2608.05263) (2026-08-07)
- [Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent) (2026-06)

### ▫️ quiet prompt-injection  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-27._

- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet pruning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)

### ▫️ quiet rlvr  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-08-10._

- [Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208) (2026-08-10)
- [Willison: the OpenAI/Hugging Face 'accidental attack' happened during an RLVR training run, not deployment](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything) (2026-08-08)

### ▫️ quiet skills  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [aeonfun/aeon](https://github.com/aeonfun/aeon) (2026-08-10)
- [Search2Skill: Skill Distillation Beyond Knowledge Boundaries Via Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2608.05245) (2026-08-07)

### ▫️ quiet statistics  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Robust inference using density-powered Stein operators](https://arxiv.org/abs/2511.03963) (2026-08-10)
- [A primer on optimal transport for causal inference with observational data](https://arxiv.org/abs/2503.07811) (2026-08-10)

### ▫️ quiet subagents  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-09-10._

- [OpenAI launches the Agents API in public beta: a hosted Codex harness with managed compaction, tool search, subagents and a choice of sandbox](https://openai.com/index/introducing-the-agents-api) (2026-09-10)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet survey  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-07._

- [A Survey of Adversarial Efficiency Degradation for Vision Transformer by Exploiting Input-adaptive Optimization](https://arxiv.org/abs/2608.05217) (2026-08-07)
- [When Agentic AI Meets Integrated Sensing and Communication](https://arxiv.org/abs/2608.05792) (2026-08-07)

### ▫️ quiet swe-bench  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-16._

- [HarnessTax: across 21 model-harness pairs, harness choice barely moved success but changed cost up to 5x; four-tool Pi matched Claude Code and Codex CLI](https://harnesstax.github.io/) (2026-09-16)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](https://arxiv.org/abs/2608.06811) (2026-08-10)

### ▫️ quiet synthetic-data  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Synthetic LiDAR Data Generation and Deterministic Downsampling for Point Cloud Classification on the Edge](https://arxiv.org/abs/2608.07106) (2026-08-10)
- [iARCS: Iterative Agentic RL for Controllable 3D Scene Generation](https://arxiv.org/abs/2608.06161) (2026-08-07)

### ▫️ quiet system-prompt  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-09._

- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet theory  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Towards a Theoretical Understanding of Two Tower Recommendation Models](https://arxiv.org/abs/2403.00802) (2026-08-10)

### ▫️ quiet transformers  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [RenderFormer++: Scalable and Physics-Informed Feed-Forward Neural Rendering](https://arxiv.org/abs/2606.30380) (2026-08-10)
- [Dependency Parsing Across the Resource Spectrum: Evaluating Architectures on High and Low-Resource Languages](https://arxiv.org/abs/2605.02608) (2026-08-10)

### ▫️ quiet uncertainty  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183) (2026-08-10)

### ▫️ quiet vllm  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](https://arxiv.org/abs/2608.06557) (2026-08-10)
- [vLLM anatomy: paged attention + continuous batching + KV-cache block pool as the load-bearing abstractions for high-throughput LLM serving](https://www.aleksagordic.com/blog/vllm) (2026-08-06)

---

<sub>Generated by scripts/trends.py on 2026-10-25.</sub>
