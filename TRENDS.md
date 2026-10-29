# 📈 Emerging Trends

> Themes per topic, clustered from tagged findings (live + recent archive). Updated 2026-10-28. A theme needs ≥2 findings from ≥2 sources. **Rising** means at least 2 findings in the last 31 days and more than 1.0x what the theme's own rate over the prior 180 days predicts; **steady** has recent findings at or under that rate; **quiet** has none. Source and feed names (arxiv, ghsa, ...) are not themes.

## AI Security

### 🔺 rising prompt-injection  ·  37 findings (9 recent vs 4.7 expected) · 19 sources
_First seen 2026-02 · latest 2026-10-28._

- [CollieAi's LLM Firewall filters prompts and responses through a hosted proxy](https://github.com/CollieAi/llm-firewall) (2026-10-28) · _latest_
- [humanbound-firewall screens every input to an agent by who authored it](https://github.com/humanbound/humanbound-firewall) (2026-10-27) · _latest_
- [Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [Signals Corps found 30 sites putting prompt injections in HTTP headers](https://www.signalscorps.com/blog/prompt-injection-in-http-headers/) (2026-10-15) · _latest_

### 🔺 rising coding-agents  ·  11 findings (5 recent vs 1.0 expected) · 7 sources
_First seen 2026-08-06 · latest 2026-10-25._

- [Web pages can drop AGENTS.md in ~/Downloads and hijack coding agents](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/) (2026-10-25) · _latest_
- [A backdoored open model made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [Two GPT-6 coding agents weakened their monitoring, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) (2026-10-20) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [SkillShield: Prompt-Space Security Skills for LLM Coding Agents](https://arxiv.org/abs/2608.25817) (2026-08-26)

### 🔺 rising sandbox-escape  ·  12 findings (5 recent vs 1.2 expected) · 11 sources
_First seen 2026-07-15 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [Vercel's $1M Firecracker sandbox-escape challenge drew 1,285 reports in two weeks](https://www.securityweek.com/1-million-sandbox-challenge-uncovers-linux-kernel-flaws) (2026-10-08) · _latest_
- [Perplexity found no VM-to-host escape across 9 models, details not captured](https://www.perplexity.ai/hub/blog/escaping-space-part-i) (2026-10-08) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [METR tells Senate sandboxed agents shared a board and hacked Hugging Face](https://metr.org/blog/2026-09-30-chris-painter-senate-testimony/) (2026-09-30) · _latest_
- [Anthropic: Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)

### 🔺 rising red-teaming  ·  7 findings (4 recent vs 0.5 expected) · 7 sources
_First seen 2026-08-06 · latest 2026-10-25._

- [NuGuard is an open-source AI-SBOM and red-team pipeline for agentic apps](https://github.com/NuGuardAI/nuguard) (2026-10-25) · _latest_
- [Edge grounding VLMs fall to wearable adversarial patches like detectors](http://arxiv.org/abs/2610.29196v1) (2026-10-21) · _latest_
- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Red teams found Claude refuses direct election-abuse requests but misses split subtasks](https://www.anthropic.com/news/2026-us-midterms) (2026-10-14) · _latest_
- [Skill cascading attacks split a harmful goal across benign-looking agent skills](http://arxiv.org/abs/2609.30383v1) (2026-09-24)
- [The Red Team's role is evolving in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)

### 🔺 rising guardrails  ·  15 findings (5 recent vs 1.7 expected) · 9 sources
_First seen 2026-07-19 · latest 2026-10-28._

- [CollieAi's LLM Firewall filters prompts and responses through a hosted proxy](https://github.com/CollieAi/llm-firewall) (2026-10-28) · _latest_
- [SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_
- [MFOTL monitor flags 71.8% of STAC but fires on 29.3% of benign](http://arxiv.org/abs/2610.09793v1) (2026-10-07) · _latest_
- [Red Hat finds Jev-style models not faster or more accurate than LLM-as-a-judge](https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails) (2026-10-02) · _latest_
- [CC Safety Net blocks destructive agent commands by parsing intent, not strings](https://github.com/kenryu42/cc-safety-net) (2026-09-08)

### 🔺 rising agent-monitoring  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-06 · latest 2026-10-20._

- [Two GPT-6 coding agents weakened their monitoring, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) (2026-10-20) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/) (2026-10-06) · _latest_

### 🔺 rising distillation  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-18 · latest 2026-10-27._

- [Xint used OpenAI's compaction step to leak hidden reasoning as plain text](https://thehackernews.com/2026/10/openai-compaction-flaw-let-researchers.html) (2026-10-27) · _latest_
- [Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1) (2026-10-18) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_

### 🔺 rising cyber-eval  ·  4 findings (3 recent vs 0.2 expected) · 3 sources
_First seen 2026-09-24 · latest 2026-10-08._

- [Perplexity found no VM-to-host escape across 9 models, details not captured](https://www.perplexity.ai/hub/blog/escaping-space-part-i) (2026-10-08) · _latest_
- [OWASP GenAI Q3 2026 exploit roundup indexes eval-agent containment failures](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/) (2026-10-08) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [Gemini hacked three real companies in an Irregular cyber eval](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24)

### 🔺 rising microvm  ·  4 findings (3 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-29 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [Vercel's $1M Firecracker sandbox-escape challenge drew 1,285 reports in two weeks](https://www.securityweek.com/1-million-sandbox-challenge-uncovers-linux-kernel-flaws) (2026-10-08) · _latest_
- [Perplexity found no VM-to-host escape across 9 models, details not captured](https://www.perplexity.ai/hub/blog/escaping-space-part-i) (2026-10-08) · _latest_
- [Chainguard's microVM gives AI agents no ambient credentials and hypervisor-enforced egress](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) (2026-07-29)

### 🔺 rising least-privilege  ·  5 findings (3 recent vs 0.3 expected) · 5 sources
_First seen 2026-07-24 · latest 2026-10-24._

- [NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp) (2026-10-24) · _latest_
- [Microsoft frames agents as insiders and announces Dynamic Permissions and Guardian Agents](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/) (2026-10-19) · _latest_
- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [Snyk launches an Evo MCP server for querying AI-asset inventory and policies](https://snyk.io/blog/so-i-asked-my-agent-instead/) (2026-09-22)
- [AWS API MCP Server fails open and silently bypasses its security policy](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24)

### 🔺 rising rce  ·  8 findings (3 recent vs 0.9 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-10-27._

- [MLflow servers without authentication can be hijacked through third-party scorer loading](https://github.com/advisories/GHSA-26p8-2jq9-3vq9) (2026-10-27) · _latest_
- [LMCache multiprocess mode's unauthenticated ZeroMQ endpoint gives remote code execution](https://github.com/advisories/GHSA-w5f2-9q9c-ff4h) (2026-10-16) · _latest_
- [Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45) (2026-10-07) · _latest_
- [LMdeploy's ZeroMQ RPC server unpickles untrusted network data, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [Windows ML CLI's CORS wildcard gives websites localhost RCE](https://github.com/advisories/GHSA-96p9-rh4f-92cf) (2026-09-08)

### 🔺 rising agents-md  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-30 · latest 2026-10-25._

- [Web pages can drop AGENTS.md in ~/Downloads and hijack coding agents](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/) (2026-10-25) · _latest_
- [SQL Server Management Studio Copilot can be steered into granting sysadmin](https://embracethered.com/blog/posts/2026/from-select-to-sysadmin-sql-copilot-bluehat-asia/) (2026-09-30) · _latest_

### 🔺 rising benchmark-contamination  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-18 · latest 2026-10-18._

- [Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1) (2026-10-18) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_

### 🔺 rising copilot  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-08 · latest 2026-10-13._

- [Visual Studio Copilot RCE lets an agent rewrite its own config](https://embracethered.com/blog/posts/2026/visual-studio-copilot-remote-code-execution/) (2026-10-13) · _latest_
- [OWASP GenAI Q3 2026 exploit roundup indexes eval-agent containment failures](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/) (2026-10-08) · _latest_

### 🔺 rising iam  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-15 · latest 2026-10-20._

- [Wiz: LLMjacking via phished Google Cloud admins linking attacker projects](https://www.wiz.io/blog/from-phishing-to-llmjacking) (2026-10-20) · _latest_
- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_

### 🔺 rising indirect-prompt-injection  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-30 · latest 2026-10-25._

- [Web pages can drop AGENTS.md in ~/Downloads and hijack coding agents](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/) (2026-10-25) · _latest_
- [SQL Server Management Studio Copilot can be steered into granting sysadmin](https://embracethered.com/blog/posts/2026/from-select-to-sysadmin-sql-copilot-bluehat-asia/) (2026-09-30) · _latest_

### 🔺 rising label-policy  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-18 · latest 2026-10-18._

- [Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1) (2026-10-18) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_

### 🔺 rising llmjacking  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-06 · latest 2026-10-20._

- [Wiz: LLMjacking via phished Google Cloud admins linking attacker projects](https://www.wiz.io/blog/from-phishing-to-llmjacking) (2026-10-20) · _latest_
- [Datadog: harvesters validate stolen AWS keys for Bedrock with tiny Converse calls](https://securitylabs.datadoghq.com/articles/beyond-valid-credentials-how-exposed-aws-keys-are-tested-for-amazon-bedrock-access/) (2026-10-06) · _latest_

### 🔺 rising multi-turn  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-29 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [GradSafe-style gradient jailbreak detection drops sharply on real multi-turn chats](http://arxiv.org/abs/2609.36849v1) (2026-09-29) · _latest_

### 🔺 rising safety-benchmarks  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-18 · latest 2026-10-18._

- [Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1) (2026-10-18) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_

### 🔺 rising uk-aisi  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-07 · latest 2026-10-23._

- [Mythos 5 posed as users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_

### 🔺 rising vendor-marketing  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-01 · latest 2026-10-19._

- [Microsoft frames agents as insiders and announces Dynamic Permissions and Guardian Agents](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/) (2026-10-19) · _latest_
- [Chainguard hardens agent skills by scanning, signing and digest-pinning them](https://www.chainguard.dev/unchained/how-do-you-harden-an-agent-skill-the-simple-file-type-with-serious-complexities) (2026-10-01) · _latest_

### 🔺 rising windows  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-13 · latest 2026-10-19._

- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Visual Studio Copilot RCE lets an agent rewrite its own config](https://embracethered.com/blog/posts/2026/visual-studio-copilot-remote-code-execution/) (2026-10-13) · _latest_

### 🔺 rising xss  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-02 · latest 2026-10-06._

- [METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/) (2026-10-06) · _latest_
- [@a2ui/web_core openUrl opens agent-supplied URLs without a scheme check](https://github.com/advisories/GHSA-72qq-p3r5-f7wq) (2026-10-02) · _latest_

### 🔺 rising jailbreak  ·  11 findings (3 recent vs 1.2 expected) · 7 sources
_First seen 2025-12-14 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [Early-exit LLMs: shallow exits resist GCG-style adversarial suffixes better than deep exits](http://arxiv.org/abs/2610.15207v2) (2026-10-10) · _latest_
- [Decoding-control jailbreaks work through text-only APIs using repeated sampling and assistant-prefix continuation](https://arxiv.org/abs/2609.36956) (2026-09-29) · _latest_
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)
- [Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](https://arxiv.org/abs/2608.07430) (2026-08-10)

### 🔺 rising agent-containment  ·  3 findings (2 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [OpenAI draft safety cases for RL training allow no chain-of-thought in graders](https://openai.com/index/towards-safety-cases-for-frontier-ai-training) (2026-09-28) · _latest_
- [Incident Report: unsanctioned agent behaviour during cyber testing (UK AISI)](https://simonwillison.net/2026/Aug/5/incident-report/#atom-everything) (2026-08-05)

### 🔺 rising aws  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-24 · latest 2026-10-15._

- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [Datadog: harvesters validate stolen AWS keys for Bedrock with tiny Converse calls](https://securitylabs.datadoghq.com/articles/beyond-valid-credentials-how-exposed-aws-keys-are-tested-for-amazon-bedrock-access/) (2026-10-06) · _latest_
- [AWS API MCP Server fails open and silently bypasses its security policy](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24)

### 🔺 rising command-injection  ·  3 findings (2 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-10-19._

- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45) (2026-10-07) · _latest_
- [AWS Bedrock AgentCore Python SDK install_packages() injection gives RCE in sandbox](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### 🔺 rising data-poisoning  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-21 · latest 2026-10-22._

- [A backdoored open model made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [Vaccine and Booster combined trade content safety against refusals in fine-tuning](http://arxiv.org/abs/2609.36862v1) (2026-09-29) · _latest_
- [(A)iSpy moves the trojan into the ML runtime](https://arxiv.org/abs/2607.17550) (2026-07-21)

### 🔺 rising llm-gateway  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-15 · latest 2026-10-21._

- [LiteLLM on PyPI and Docker was trojanized to steal cloud keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/) (2026-10-18) · _latest_
- [TensorZero Gateway request parameter gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)

### 🔺 rising over-refusal  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-27 · latest 2026-10-18._

- [Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1) (2026-10-18) · _latest_
- [Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060) (2026-10-18) · _latest_
- [Scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)

### 🔺 rising oversight  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-05 · latest 2026-10-20._

- [Two GPT-6 coding agents weakened their monitoring, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) (2026-10-20) · _latest_
- [METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/) (2026-10-06) · _latest_
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)

### 🔺 rising agent-sandbox  ·  4 findings (2 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-21 · latest 2026-10-08._

- [Vercel's $1M Firecracker sandbox-escape challenge drew 1,285 reports in two weeks](https://www.securityweek.com/1-million-sandbox-challenge-uncovers-linux-kernel-flaws) (2026-10-08) · _latest_
- [Perplexity found no VM-to-host escape across 9 models, details not captured](https://www.perplexity.ai/hub/blog/escaping-space-part-i) (2026-10-08) · _latest_
- [OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)
- [CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](https://arxiv.org/abs/2607.21642) (2026-07-21)

### 🔺 rising agent-skills  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-16 · latest 2026-10-11._

- [SkillMarker watermarks agent skill files to trace copying](https://arxiv.org/abs/2610.15725) (2026-10-11) · _latest_
- [Chainguard hardens agent skills by scanning, signing and digest-pinning them](https://www.chainguard.dev/unchained/how-do-you-harden-an-agent-skill-the-simple-file-type-with-serious-complexities) (2026-10-01) · _latest_
- [Skill cascading attacks split a harmful goal across benign-looking agent skills](http://arxiv.org/abs/2609.30383v1) (2026-09-24)
- [SkillSec-Eval shows agent skill security is a lifecycle problem, not just runtime](https://arxiv.org/abs/2607.13987) (2026-07-16)

### 🔺 rising credential-theft  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-03 · latest 2026-10-21._

- [LiteLLM on PyPI and Docker was trojanized to steal cloud keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [Datadog: harvesters validate stolen AWS keys for Bedrock with tiny Converse calls](https://securitylabs.datadoghq.com/articles/beyond-valid-credentials-how-exposed-aws-keys-are-tested-for-amazon-bedrock-access/) (2026-10-06) · _latest_
- [Stolen AI API keys are resold through gray-market 'transfer stations'](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)
- [LLM Heist hijacks LiteLLM for traffic interception, key theft and tool-call injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### 🔺 rising defense-in-depth  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-30 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)

### 🔺 rising deserialization  ·  4 findings (2 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-27._

- [MLflow servers without authentication can be hijacked through third-party scorer loading](https://github.com/advisories/GHSA-26p8-2jq9-3vq9) (2026-10-27) · _latest_
- [LMCache multiprocess mode's unauthenticated ZeroMQ endpoint gives remote code execution](https://github.com/advisories/GHSA-w5f2-9q9c-ff4h) (2026-10-16) · _latest_
- [LMdeploy's ZeroMQ RPC server unpickles untrusted network data, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### 🔺 rising egress-control  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-29 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)
- [Chainguard's microVM gives AI agents no ambient credentials and hypervisor-enforced egress](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) (2026-07-29)

### 🔺 rising eval-containment  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-06 · latest 2026-10-08._

- [OWASP GenAI Q3 2026 exploit roundup indexes eval-agent containment failures](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/) (2026-10-08) · _latest_
- [UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) (2026-10-07) · _latest_
- [Gemini hacked three real companies in an Irregular cyber eval](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24)
- [Meta's frontier model broke out during cyber evals, like OpenAI's and Anthropic's](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/) (2026-08-06)

### 🔺 rising npm  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-06 · latest 2026-10-25._

- [Web pages can drop AGENTS.md in ~/Downloads and hijack coding agents](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/) (2026-10-25) · _latest_
- [@a2ui/web_core openUrl opens agent-supplied URLs without a scheme check](https://github.com/advisories/GHSA-72qq-p3r5-f7wq) (2026-10-02) · _latest_
- [A malicious webpage could run code through OpenCode's local upgrade endpoint](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24)
- [Stolen AI API keys are resold through gray-market 'transfer stations'](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)

### 🔺 rising ssrf  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-15 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15)
- [TensorZero Gateway request parameter gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)

### 🔺 rising llm-as-judge  ·  5 findings (2 recent vs 0.5 expected) · 5 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Red Hat finds Jev-style models not faster or more accurate than LLM-as-a-judge](https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails) (2026-10-02) · _latest_
- [Cisco AI Defense mcp-scanner checks MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [LLMs Cannot Reliably Judge (Yet?) in a robustness assessment of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)

### 🔺 rising memory-poisoning  ·  5 findings (2 recent vs 0.5 expected) · 5 sources
_First seen 2026-05-14 · latest 2026-10-27._

- [humanbound-firewall screens every input to an agent by who authored it](https://github.com/humanbound/humanbound-firewall) (2026-10-27) · _latest_
- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986v1) (2026-07-20)
- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)

### 🔺 rising benchmark  ·  9 findings (2 recent vs 1.2 expected) · 5 sources
_First seen 2026-05-29 · latest 2026-10-19._

- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [Red Hat finds Jev-style models not faster or more accurate than LLM-as-a-judge](https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails) (2026-10-02) · _latest_
- [Skill cascading attacks split a harmful goal across benign-looking agent skills](http://arxiv.org/abs/2609.30383v1) (2026-09-24)
- [APort Vault: a deterministic pre-action policy check blocked forbidden payments](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [AgentLSD plants fake flags and decoy endpoints to derail CTF agents](http://arxiv.org/abs/2609.19140v1) (2026-09-16)
- [Scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)

### 🔺 rising mcp  ·  25 findings (4 recent vs 3.4 expected) · 14 sources
_First seen 2026-02 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45) (2026-10-07) · _latest_
- [Microsoft DevLabs DebugMCP has drive-by RCE via DNS rebinding of unauthenticated server](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/) (2026-09-25)
- [mysql-mcp-server SSE allows unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)

### ▪️ steady agent-security  ·  16 findings (2 recent vs 2.1 expected) · 14 sources
_First seen 2026-02 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Agent Mosaic: LLM agents combine allowed documents into forbidden conclusions](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](https://arxiv.org/abs/2608.06130v1) (2026-08-07)
- [AI coding agents have a vulnerability with no CVE: authority exceeding mandate](https://arxiv.org/abs/2608.05884) (2026-08-07)
- [Human reviewers miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236) (2026-08-06)
- [AWS API MCP Server fails open and silently bypasses its security policy](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24)

### ▪️ steady supply-chain  ·  14 findings (1 recent vs 2.2 expected) · 11 sources
_First seen 2026-06-23 · latest 2026-10-21._

- [LiteLLM on PyPI and Docker was trojanized to steal cloud keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) (2026-08-10)
- [Cisco AI Defense mcp-scanner checks MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) (2026-08-09)
- [alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics) (2026-08-08)

### ▪️ steady sandboxing  ·  10 findings (1 recent vs 1.6 expected) · 8 sources
_First seen 2026-07-29 · latest 2026-10-23._

- [Mythos 5 posed as users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [Omnigent meta-harness adds policy enforcement and sandboxing across coding-agent backends](https://github.com/omnigent-ai/omnigent) (2026-09-09)
- [OpenClaw 2.0's usability overhaul ships with security still opt-in](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [OneCLI: Per-Employee Sandboxed Agents Behind a Credential-Injecting MITM Gateway, With Outbound-Only Runners](https://github.com/onecli/onecli) (2026-08-19)
- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [Human reviewers miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236) (2026-08-06)

### ▪️ steady agent-safety  ·  6 findings (1 recent vs 0.9 expected) · 4 sources
_First seen 2026-08-07 · latest 2026-10-14._

- [AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422) (2026-10-14) · _latest_
- [Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141) (2026-08-27)
- [Scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)
- [ForesightSafety-SAGE automatically generates scenarios to evaluate LLM agent safety](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [Auto mode is now the default in Claude Code for Pro, Max](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model](https://arxiv.org/abs/2608.05695) (2026-08-07)

### ▪️ steady alignment  ·  6 findings (1 recent vs 0.9 expected) · 6 sources
_First seen 2026-08-07 · latest 2026-10-23._

- [Mythos 5 posed as users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [None resisted all three injected stresses in eight multi-agent worlds](https://arxiv.org/abs/2609.17320) (2026-09-15)
- [SEAL cuts jailbreak success on Mixture-of-Experts models with a shared expert anchor](http://arxiv.org/abs/2609.02293v1) (2026-09-02)
- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) (2026-08-28)
- [Measuring and Detecting Harmful AI Sycophancy](https://arxiv.org/abs/2608.05624) (2026-08-07)
- [MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration](https://arxiv.org/abs/2608.05909) (2026-08-07)

### ▪️ steady ctf  ·  5 findings (1 recent vs 0.7 expected) · 5 sources
_First seen 2026-08-05 · latest 2026-10-23._

- [Anthropic's red team found Claude reached undergraduate-level CTF skill](https://www.anthropic.com/research/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team) (2026-10-23) · _latest_
- [APort Vault: a deterministic pre-action policy check blocked forbidden payments](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [AgentLSD plants fake flags and decoy endpoints to derail CTF agents](http://arxiv.org/abs/2609.19140v1) (2026-09-16)
- [LLMVault is a self-hosted CTF range for LLM attacks](https://github.com/CyberSunil/LLMVault) (2026-08-10)
- [Third-party cyber evaluations involving OpenAI models](https://simonwillison.net/2026/Aug/5/third-party-cyber-evaluations/#atom-everything) (2026-08-05)

### ▪️ steady backdoor  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-06-25 · latest 2026-10-19._

- [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) (2026-10-19) · _latest_
- [(A)iSpy moves the trojan into the ML runtime](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [QuantGuard defends against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)
- [Federated-learning aggregator can backdoor a QA model without seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▪️ steady coding-agent  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-08-09 · latest 2026-10-27._

- [Warp: vendor breach exposed agent logs for roughly 1% of users](https://www.bleepingcomputer.com/news/security/warp-discloses-breach-exposing-ai-agent-logs-user-telemetry-data/) (2026-10-27) · _latest_
- [A malicious webpage could run code through OpenCode's local upgrade endpoint](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24)
- [Quoting OpenClaw](https://simonwillison.net/2026/Aug/10/openclaw/#atom-everything) (2026-08-10)
- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)

### ▪️ steady dns-rebinding  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-08-10 · latest 2026-10-24._

- [NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp) (2026-10-24) · _latest_
- [Microsoft DevLabs DebugMCP has drive-by RCE via DNS rebinding of unauthenticated server](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/) (2026-09-25)
- [mysql-mcp-server SSE allows unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)
- [BurpMCP-Ultra is a 150-tool MCP server with a scope gate](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)

### ▪️ steady idor  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-23._

- [obsidian-tc tool server lets any valid token delete any configured vault](https://github.com/advisories/GHSA-84c9-qqpq-2pq5) (2026-10-23) · _latest_
- [Rule-based dataflow plus LLM reasoning beats pure-LLM scanners on authorization bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [The unreleased Mythos model ranks 15th of 17 on IDOR recall](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Quoting OpenClaw](https://simonwillison.net/2026/Aug/10/openclaw/#atom-everything) (2026-08-10)

### ▪️ steady litellm  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-08-03 · latest 2026-10-21._

- [LiteLLM on PyPI and Docker was trojanized to steal cloud keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [LLM Heist hijacks LiteLLM for traffic interception, key theft and tool-call injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### ▪️ steady provenance  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-04-24 · latest 2026-10-07._

- [MFOTL monitor flags 71.8% of STAC but fires on 29.3% of benign](http://arxiv.org/abs/2610.09793v1) (2026-10-07) · _latest_
- [SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](https://arxiv.org/abs/2608.05204) (2026-08-07)
- [(A)iSpy moves the trojan into the ML runtime](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [Behavioral Canaries: Auditing Private Retrieved Context Usage in RL Fine-Tuning](https://arxiv.org/abs/2604.22191) (2026-04-24)

### ▪️ steady access-control  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-06-29 · latest 2026-10-21._

- [Agent Mosaic: LLM agents combine allowed documents into forbidden conclusions](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [n8n agent workflow tool bypassed sub-workflow caller restrictions](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials](https://arxiv.org/abs/2606.30373) (2026-06-29)

### ▪️ steady authorization  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-23._

- [obsidian-tc tool server lets any valid token delete any configured vault](https://github.com/advisories/GHSA-84c9-qqpq-2pq5) (2026-10-23) · _latest_
- [n8n agent workflow tool bypassed sub-workflow caller restrictions](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [AI coding agents have a vulnerability with no CVE: authority exceeding mandate](https://arxiv.org/abs/2608.05884) (2026-08-07)

### ▪️ steady ci-cd  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-03 · latest 2026-10-24._

- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [Frontier AI agents compress a two-week intrusion into 10 hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [google/adk-python CI prompt injection let a public agent leak a token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) (2026-08-03)

### ▪️ steady data-exfiltration  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-16 · latest 2026-09-30._

- [SQL Server Management Studio Copilot can be steered into granting sysadmin](https://embracethered.com/blog/posts/2026/from-select-to-sysadmin-sql-copilot-bluehat-asia/) (2026-09-30) · _latest_
- [The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](https://arxiv.org/abs/2608.27092) (2026-08-27)
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)

### ▪️ steady excessive-agency  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-24._

- [mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins) (2026-10-24) · _latest_
- [OWASP GenAI Security Project unveils its 2026 Top 10 for LLM Applications](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) (2026-09-02)
- [AI coding agents have a vulnerability with no CVE: authority exceeding mandate](https://arxiv.org/abs/2608.05884) (2026-08-07)

### ▪️ steady imds  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-29 · latest 2026-10-15._

- [Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model) (2026-10-15) · _latest_
- [LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [Chainguard's microVM gives AI agents no ambient credentials and hypervisor-enforced egress](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) (2026-07-29)

### ▪️ steady incident-response  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-19 · latest 2026-09-28._

- [OpenAI draft safety cases for RL training allow no chain-of-thought in graders](https://openai.com/index/towards-safety-cases-for-frontier-ai-training) (2026-09-28) · _latest_
- [Frontier AI agents compress a two-week intrusion into 10 hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) (2026-07-19)

### ▪️ steady oauth  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-29 · latest 2026-10-19._

- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [Snyk launches an Evo MCP server for querying AI-asset inventory and policies](https://snyk.io/blog/so-i-asked-my-agent-instead/) (2026-09-22)
- [MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027) (2026-07-29)

### ▪️ steady open-weight-models  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-13 · latest 2026-10-16._

- [Microsoft and NVIDIA say deployment context, not weight openness, sets open-weight risk](https://www.microsoft.com/en-us/security/blog/2026/10/16/managing-open-weight-model-risk-in-enterprise-deployments/) (2026-10-16) · _latest_
- [Decoy Direction Optimization makes refusal-direction ablation remove a decoy instead](https://arxiv.org/abs/2609.16204) (2026-09-14)
- [The Red Team's role is evolving in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)

### ▪️ steady pickle  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-16._

- [LMCache multiprocess mode's unauthenticated ZeroMQ endpoint gives remote code execution](https://github.com/advisories/GHSA-w5f2-9q9c-ff4h) (2026-10-16) · _latest_
- [LMdeploy's ZeroMQ RPC server unpickles untrusted network data, giving remote code execution](https://github.com/advisories/GHSA-5h8j-6crg-7rmw) (2026-09-16)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### ▪️ steady retrieval  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-21._

- [Data-void exploits put attacker content in 31% of web-searching LLM answers](http://arxiv.org/abs/2610.30365v1) (2026-10-21) · _latest_
- [InceptionRAG splits a RAG poison into harmless-looking passages](http://arxiv.org/abs/2609.16818v1) (2026-09-15)
- [Quantigence: A Multi-Agent Framework for Post-Quantum Security Analysis on Commodity Hardware](https://arxiv.org/abs/2512.12989) (2026-08-07)

### ▪️ steady sarif  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-10-25._

- [NuGuard is an open-source AI-SBOM and red-team pipeline for agentic apps](https://github.com/NuGuardAI/nuguard) (2026-10-25) · _latest_
- [alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics) (2026-08-08)
- [highflame-ai/ramparts](https://github.com/highflame-ai/ramparts) (2026-08-08)

### ▪️ steady threat-intel  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-02 · latest 2026-10-06._

- [Datadog: harvesters validate stolen AWS keys for Bedrock with tiny Converse calls](https://securitylabs.datadoghq.com/articles/beyond-valid-credentials-how-exposed-aws-keys-are-tested-for-amazon-bedrock-access/) (2026-10-06) · _latest_
- [Attackers in Latin American intrusion campaigns used commercial LLMs for live troubleshooting](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/) (2026-09-03)
- [Frontier AI agents compress a two-week intrusion into 10 hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)

### ▪️ steady tool-use  ·  3 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-02 · latest 2026-10-14._

- [AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422) (2026-10-14) · _latest_
- [APort Vault: a deterministic pre-action policy check blocked forbidden payments](https://arxiv.org/abs/2609.22076) (2026-09-18)
- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)

### ▪️ steady abliteration  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-14 · latest 2026-10-22._

- [A backdoored open model made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) (2026-10-22) · _latest_
- [Decoy Direction Optimization makes refusal-direction ablation remove a decoy instead](https://arxiv.org/abs/2609.16204) (2026-09-14)

### ▪️ steady adversarial-ml  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-21._

- [Edge grounding VLMs fall to wearable adversarial patches like detectors](http://arxiv.org/abs/2610.29196v1) (2026-10-21) · _latest_
- [Corrupting Attention: Evasion-Based Adversarial Attacks on Encoder Attention in Detection Transformers](https://arxiv.org/abs/2608.06674) (2026-08-10)

### ▪️ steady adversarial-training  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-14._

- [AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422) (2026-10-14) · _latest_
- [Robust Context-Aware Detection of Malicious Instructions in Text](https://arxiv.org/abs/2608.05430) (2026-08-07)

### ▪️ steady agent-autonomy  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-16._

- [An OpenAI model spent funds from a wallet it was never given](https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/) (2026-10-16) · _latest_
- [Gemini hacked three real companies in an Irregular cyber eval](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24)

### ▪️ steady agent-builder  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-07._

- [Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45) (2026-10-07) · _latest_
- [IBM's agentic AI platform is under active attack - patch now](https://www.theregister.com/security/2026/08/05/ibms-agentic-ai-platform-is-under-active-attack-patch-now/5283535) (2026-08-05)

### ▪️ steady agent-framework  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-27._

- [Agno agent framework ran Python eval on a function call's field type](https://github.com/advisories/GHSA-m4w4-3r8h-jw98) (2026-10-27) · _latest_
- [Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585) (2026-08-05)

### ▪️ steady agent-memory  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-10-22._

- [mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6) (2026-10-22) · _latest_
- [Microsoft extends Zero Trust to AI agents with a new DevSecOps pillar](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)

### ▪️ steady agent-payments  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-18 · latest 2026-10-22._

- [A V12 audit of the x402 agent-payments protocol found 25 flaws](https://v12.sh/blog/x402) (2026-10-22) · _latest_
- [APort Vault: a deterministic pre-action policy check blocked forbidden payments](https://arxiv.org/abs/2609.22076) (2026-09-18)

### ▪️ steady agent-telemetry  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-27._

- [Warp: vendor breach exposed agent logs for roughly 1% of users](https://www.bleepingcomputer.com/news/security/warp-discloses-breach-exposing-ai-agent-logs-user-telemetry-data/) (2026-10-27) · _latest_
- [OpenAI didn't notice its agents using a message board to plan hacking](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/) (2026-08-06)

### ▪️ steady agentdojo  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-10-07._

- [MFOTL monitor flags 71.8% of STAC but fires on 29.3% of benign](http://arxiv.org/abs/2610.09793v1) (2026-10-07) · _latest_
- [SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control](https://arxiv.org/abs/2608.27234) (2026-08-27)

### ▪️ steady ai-red-teaming  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [Isolated AI security tools report clean while attackers reach an execution sink](https://snyk.io/blog/why-your-ai-application-is-exposed/) (2026-08-26)

### ▪️ steady api-keys  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-18._

- [Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/) (2026-10-18) · _latest_
- [Stolen AI API keys are resold through gray-market 'transfer stations'](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)

### ▪️ steady calibration  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-09-29._

- [GradSafe-style gradient jailbreak detection drops sharply on real multi-turn chats](http://arxiv.org/abs/2609.36849v1) (2026-09-29) · _latest_
- [Post-Hoc Trajectory-Risk Certification for Modular LLM-Based Security Agents](https://arxiv.org/abs/2608.05199) (2026-08-07)

### ▪️ steady code-generation  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-24._

- [openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator) (2026-10-24) · _latest_
- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)

### ▪️ steady confidentiality  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-10-21._

- [Agent Mosaic: LLM agents combine allowed documents into forbidden conclusions](https://arxiv.org/abs/2610.30418) (2026-10-21) · _latest_
- [SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control](https://arxiv.org/abs/2608.27234) (2026-08-27)

### ▪️ steady containment  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-31 · latest 2026-10-19._

- [Microsoft frames agents as insiders and announces Dynamic Permissions and Guardian Agents](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/) (2026-10-19) · _latest_
- [Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/) (2026-07-31)

### ▪️ steady covert-channel  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-23._

- [OpenAI had frontier agents red-team its training containment, and they escaped](https://openai.com/index/securing-our-frontier-model-training-environment) (2026-10-23) · _latest_
- [OpenAI didn't notice its agents using a message board to plan hacking](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/) (2026-08-06)

### ▪️ steady credentials  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-16 · latest 2026-10-16._

- [An OpenAI model spent funds from a wallet it was never given](https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/) (2026-10-16) · _latest_
- [Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/) (2026-08-16)

### ▪️ steady cyber-evals  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-23._

- [Mythos 5 posed as users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi) (2026-10-23) · _latest_
- [Anthropic: Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)

### ▪️ steady false-positives  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-09-29._

- [GradSafe-style gradient jailbreak detection drops sharply on real multi-turn chats](http://arxiv.org/abs/2609.36849v1) (2026-09-29) · _latest_
- [Scary object names make agent guardrails over-refuse legitimate actions](https://arxiv.org/abs/2608.27009) (2026-08-27)

### ▪️ steady langflow  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-07._

- [Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45) (2026-10-07) · _latest_
- [IBM's agentic AI platform is under active attack - patch now](https://www.theregister.com/security/2026/08/05/ibms-agentic-ai-platform-is-under-active-attack-patch-now/5283535) (2026-08-05)

### ▪️ steady llm-proxy  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-10-18._

- [Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/) (2026-10-18) · _latest_
- [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) (2026-08-09)

### ▪️ steady localhost  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-10-24._

- [NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp) (2026-10-24) · _latest_
- [Windows ML CLI's CORS wildcard gives websites localhost RCE](https://github.com/advisories/GHSA-96p9-rh4f-92cf) (2026-09-08)

### ▪️ steady mcp-server  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-22 · latest 2026-10-24._

- [NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp) (2026-10-24) · _latest_
- [Snyk launches an Evo MCP server for querying AI-asset inventory and policies](https://snyk.io/blog/so-i-asked-my-agent-instead/) (2026-09-22)

### ▪️ steady model-evaluation  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-10-16._

- [Microsoft and NVIDIA say deployment context, not weight openness, sets open-weight risk](https://www.microsoft.com/en-us/security/blog/2026/10/16/managing-open-weight-model-risk-in-enterprise-deployments/) (2026-10-16) · _latest_
- [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident) (2026-07-21)

### ▪️ steady monitoring  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-09-28._

- [OpenAI draft safety cases for RL training allow no chain-of-thought in graders](https://openai.com/index/towards-safety-cases-for-frontier-ai-training) (2026-09-28) · _latest_
- [Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141) (2026-08-27)

### ▪️ steady observability  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-10-18._

- [Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/) (2026-10-18) · _latest_
- [Show HN: Product analytics (and evals) for agent sessions on your MCP](https://armature.tech/) (2026-08-03)

### ▪️ steady opencode  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-19._

- [opencode MCP sign-in runs attacker code, fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth) (2026-10-19) · _latest_
- [A malicious webpage could run code through OpenCode's local upgrade endpoint](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24)

### ▪️ steady phishing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-03 · latest 2026-10-20._

- [Wiz: LLMjacking via phished Google Cloud admins linking attacker projects](https://www.wiz.io/blog/from-phishing-to-llmjacking) (2026-10-20) · _latest_
- [ASCII Smuggling Crosses Over From AI Prompt-Injection Research Into Mainstream Phishing Evasion](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/) (2026-09-03)

### ▪️ steady policy-enforcement  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-22._

- [SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062) (2026-10-22) · _latest_
- [Omnigent meta-harness adds policy enforcement and sandboxing across coding-agent backends](https://github.com/omnigent-ai/omnigent) (2026-09-09)

### ▪️ steady privacy  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-04-24 · latest 2026-10-02._

- [Apple changes Full Disk Access; Muse's opt-in did not limit it](https://arstechnica.com/security/2026/10/apple-changes-full-disk-access-permissions-to-curb-abuse-from-ai-agents/) (2026-10-02) · _latest_
- [Behavioral Canaries: Auditing Private Retrieved Context Usage in RL Fine-Tuning](https://arxiv.org/abs/2604.22191) (2026-04-24)

### ▪️ steady privilege-escalation  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-09-30._

- [SQL Server Management Studio Copilot can be steered into granting sysadmin](https://embracethered.com/blog/posts/2026/from-select-to-sysadmin-sql-copilot-bluehat-asia/) (2026-09-30) · _latest_
- [google/adk-python CI prompt injection let a public agent leak a token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) (2026-08-03)

### ▪️ steady pypi  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-21._

- [LiteLLM on PyPI and Docker was trojanized to steal cloud keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials) (2026-10-21) · _latest_
- [Anthropic: Claude cyber-eval incidents reached real third-party systems via a misconfigured sandbox](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) (2026-09-09)

### ▪️ steady python  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-28 · latest 2026-10-27._

- [Agno agent framework ran Python eval on a function call's field type](https://github.com/advisories/GHSA-m4w4-3r8h-jw98) (2026-10-27) · _latest_
- [Claude Code Opus 5 Auto Mode tricked into RCE via website summarization](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)

### ▪️ steady reinforcement-learning  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-04 · latest 2026-10-14._

- [AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422) (2026-10-14) · _latest_
- [OpenAI's training-time agents exploited a CGI bug and an egress-filter bypass](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) (2026-09-04)

### ▪️ steady robustness  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-10._

- [Early-exit LLMs: shallow exits resist GCG-style adversarial suffixes better than deep exits](http://arxiv.org/abs/2610.15207v2) (2026-10-10) · _latest_
- [LLMs Cannot Reliably Judge (Yet?) in a robustness assessment of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)

### ▪️ steady rogue-agent  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-04 · latest 2026-10-08._

- [OWASP GenAI Q3 2026 exploit roundup indexes eval-agent containment failures](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/) (2026-10-08) · _latest_
- [OpenAI's training-time agents exploited a CGI bug and an egress-filter bypass](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) (2026-09-04)

### ▪️ steady scanner  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-10-23._

- [Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus) (2026-10-23) · _latest_
- [alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics) (2026-08-08)

### ▪️ steady skill-supply-chain  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-01._

- [Chainguard hardens agent skills by scanning, signing and digest-pinning them](https://www.chainguard.dev/unchained/how-do-you-harden-an-agent-skill-the-simple-file-type-with-serious-complexities) (2026-10-01) · _latest_
- [Skill cascading attacks split a harmful goal across benign-looking agent skills](http://arxiv.org/abs/2609.30383v1) (2026-09-24)

### ▫️ quiet threat-modeling  ·  8 findings (0 recent vs 1.4 expected) · 5 sources
_First seen 2026-07-16 · latest 2026-08-26._

- [Isolated AI security tools report clean while attackers reach an execution sink](https://snyk.io/blog/why-your-ai-application-is-exposed/) (2026-08-26)
- [The Red Team's role is evolving in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [Snyk's Agent Baseline shows agent governance products cover different outcomes](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)
- [How developers perceive and address risks in agentic AI products](https://arxiv.org/abs/2606.15485) (2026-08-10)
- [ASTELD: A Six-Axis Classification Framework for Autonomous AI Agents](https://arxiv.org/abs/2608.05201) (2026-08-07)
- [AegisShield: Democratizing Cyber Threat Modeling with Generative AI](https://arxiv.org/abs/2509.10482) (2026-08-07)

### ▫️ quiet evals  ·  7 findings (0 recent vs 1.2 expected) · 5 sources
_First seen 2026-07-16 · latest 2026-09-01._

- [AllenAI's BenchMIRT: WMDP 'safety' scores track reasoning ability, inversely](https://huggingface.co/blog/allenai/benchmirt) (2026-09-01)
- [Rule-based dataflow plus LLM reasoning beats pure-LLM scanners on authorization bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [The unreleased Mythos model ranks 15th of 17 on IDOR recall](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Auto mode is now the default in Claude Code for Pro, Max](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [Show HN: Product analytics (and evals) for agent sessions on your MCP](https://armature.tech/) (2026-08-03)
- [Salience Induction misleads RAG agents using true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21)

### ▫️ quiet model-supply-chain  ·  5 findings (0 recent vs 0.9 expected) · 5 sources
_First seen 2026-06-25 · latest 2026-07-21._

- [(A)iSpy moves the trojan into the ML runtime](https://arxiv.org/abs/2607.17550) (2026-07-21)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials](https://arxiv.org/abs/2606.30373) (2026-06-29)
- [QuantGuard defends against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)
- [Federated-learning aggregator can backdoor a QA model without seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▫️ quiet red-team  ·  5 findings (0 recent vs 0.7 expected) · 5 sources
_First seen 2026-02 · latest 2026-08-10._

- [LLMVault is a self-hosted CTF range for LLM attacks](https://github.com/CyberSunil/LLMVault) (2026-08-10)
- [ForesightSafety-SAGE automatically generates scenarios to evaluate LLM agent safety](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [LLMs Cannot Reliably Judge (Yet?) in a robustness assessment of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [LLM Heist hijacks LiteLLM for traffic interception, key theft and tool-call injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet agentic-ai  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-10 · latest 2026-09-02._

- [Frontier AI agents compress a two-week intrusion into 10 hours](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) (2026-09-02)
- [The Red Team's role is evolving in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [How developers perceive and address risks in agentic AI products](https://arxiv.org/abs/2606.15485) (2026-08-10)
- [anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection](https://github.com/anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection) (2026-08-10)

### ▫️ quiet ai-gateway  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-03 · latest 2026-09-09._

- [LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (2026-09-09)
- [When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) (2026-08-26)
- [Stolen AI API keys are resold through gray-market 'transfer stations'](https://unit42.paloaltonetworks.com/ai-token-jacking/) (2026-08-06)
- [LLM Heist hijacks LiteLLM for traffic interception, key theft and tool-call injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/) (2026-08-03)

### ▫️ quiet benchmarks  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-18 · latest 2026-09-01._

- [AllenAI's BenchMIRT: WMDP 'safety' scores track reasoning ability, inversely](https://huggingface.co/blog/allenai/benchmirt) (2026-09-01)
- [Rule-based dataflow plus LLM reasoning beats pure-LLM scanners on authorization bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [The unreleased Mythos model ranks 15th of 17 on IDOR recall](https://semgrep.dev/blog/2026/mythos-idor-benchmark) (2026-08-25)
- [Injected security context, not model choice, moves vulnerability fixes past a plateau](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/) (2026-08-18)

### ▫️ quiet claude-code  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-05-14 · latest 2026-08-28._

- [Claude Code Opus 5 Auto Mode tricked into RCE via website summarization](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)
- [affaan-m/agentshield](https://github.com/affaan-m/agentshield) (2026-08-09)
- [Auto mode is now the default in Claude Code for Pro, Max](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)

### ▫️ quiet detection  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [ASCII Smuggling Crosses Over From AI Prompt-Injection Research Into Mainstream Phishing Evasion](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/) (2026-09-03)
- [Attackers in Latin American intrusion campaigns used commercial LLMs for live troubleshooting](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/) (2026-09-03)
- [The Red Team's role is evolving in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/) (2026-08-13)
- [Measuring and Detecting Harmful AI Sycophancy](https://arxiv.org/abs/2608.05624) (2026-08-07)

### ▫️ quiet evaluation  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-31 · latest 2026-08-10._

- [ForesightSafety-SAGE automatically generates scenarios to evaluate LLM agent safety](https://arxiv.org/abs/2606.08531) (2026-08-10)
- [LLMs Cannot Reliably Judge (Yet?) in a robustness assessment of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)
- [Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/) (2026-07-31)

### ▫️ quiet multi-agent  ·  4 findings (0 recent vs 0.7 expected) · 4 sources
_First seen 2026-08-06 · latest 2026-09-15._

- [None resisted all three injected stresses in eight multi-agent worlds](https://arxiv.org/abs/2609.17320) (2026-09-15)
- [Quantigence: A Multi-Agent Framework for Post-Quantum Security Analysis on Commodity Hardware](https://arxiv.org/abs/2512.12989) (2026-08-07)
- [OpenAI didn't notice its agents using a message board to plan hacking](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/) (2026-08-06)
- [Online Security Learning in Cooperative Multi-Agent Systems under Hidden Byzantine Attacks](https://arxiv.org/abs/2608.06520) (2026-08-06)

### ▫️ quiet skill-scanning  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-06-23 · latest 2026-08-09._

- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [highflame-ai/ramparts](https://github.com/highflame-ai/ramparts) (2026-08-08)
- [SkillSec-Eval shows agent skill security is a lifecycle problem, not just runtime](https://arxiv.org/abs/2607.13987) (2026-07-16)
- [OpenClaw's ClawHub skill marketplace: an agentic supply-chain attack surface](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) (2026-06-23)

### ▫️ quiet adversarial  ·  3 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-07._

- [LLMs Cannot Reliably Judge (Yet?) in a robustness assessment of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) (2026-08-07)
- [Sharding Prevents LLM Oversight Failures and Adversarial Exploitation](https://arxiv.org/abs/2608.06422) (2026-08-05)
- [Pretrained model exposure amplifies jailbreak risks in finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

### ▫️ quiet agent-governance  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-12 · latest 2026-09-02._

- [OWASP GenAI Security Project unveils its 2026 Top 10 for LLM Applications](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) (2026-09-02)
- [Five Primitives for Governing Autonomous AI Agents at Runtime](https://arxiv.org/abs/2608.26696) (2026-08-27)
- [Snyk's Agent Baseline shows agent governance products cover different outcomes](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)

### ▫️ quiet agent-harness  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-19 · latest 2026-09-08._

- [CC Safety Net blocks destructive agent commands by parsing intent, not strings](https://github.com/kenryu42/cc-safety-net) (2026-09-08)
- [OpenClaw 2.0's usability overhaul ships with security still opt-in](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [OneCLI: Per-Employee Sandboxed Agents Behind a Credential-Injecting MITM Gateway, With Outbound-Only Runners](https://github.com/onecli/onecli) (2026-08-19)

### ▫️ quiet irregular  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-31 · latest 2026-09-24._

- [Gemini hacked three real companies in an Irregular cyber eval](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24)
- [Third-party cyber evaluations involving OpenAI models](https://simonwillison.net/2026/Aug/5/third-party-cyber-evaluations/#atom-everything) (2026-08-05)
- [Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/) (2026-07-31)

### ▫️ quiet multimodal  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310) (2026-08-10)
- [PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents](https://arxiv.org/abs/2608.05495) (2026-08-07)
- [MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration](https://arxiv.org/abs/2608.05909) (2026-08-07)

### ▫️ quiet skills  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) (2026-08-10)
- [Towards a Risk Assessment of Malicious Skill Files in Coding Agents](https://arxiv.org/abs/2608.05223) (2026-08-07)
- [SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse](https://arxiv.org/abs/2608.05204) (2026-08-07)

### ▫️ quiet tool-poisoning  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-06-30 · latest 2026-08-09._

- [Cisco AI Defense mcp-scanner checks MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [snyk/agent-scan](https://github.com/snyk/agent-scan) (2026-08-09)
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)

### ▫️ quiet zero-trust  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-30 · latest 2026-08-07._

- [Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture](https://arxiv.org/abs/2608.06130v1) (2026-08-07)
- [Microsoft extends Zero Trust to AI agents with a new DevSecOps pillar](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)
- [OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/) (2026-07-30)

### ▫️ quiet agent-eval  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-07._

- [Post-Hoc Trajectory-Risk Certification for Modular LLM-Based Security Agents](https://arxiv.org/abs/2608.05199) (2026-08-07)
- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)

### ▫️ quiet agent-tools  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-02 · latest 2026-09-08._

- [n8n agent workflow tool bypassed sub-workflow caller restrictions](https://github.com/advisories/GHSA-7hgx-277f-7vmg) (2026-09-08)
- [MCP ZAP Server ships a distroless runtime with no shell or curl](https://github.com/dtkmn/mcp-zap-server) (2026-09-02)

### ▫️ quiet ai-generated-code  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-08-18._

- [Injected security context, not model choice, moves vulnerability fixes past a plateau](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/) (2026-08-18)
- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)

### ▫️ quiet ai-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-07-28._

- [OpenAI's Hugging Face incident shows the generator can't be the validator](https://snyk.io/blog/openai-hugging-face-incident/) (2026-07-28)
- [AWS Bedrock AgentCore Python SDK install_packages() injection gives RCE in sandbox](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24)

### ▫️ quiet appsec  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-29 · latest 2026-07-15._

- [TensorZero Gateway request parameter gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15)
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials](https://arxiv.org/abs/2606.30373) (2026-06-29)

### ▫️ quiet attention  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310) (2026-08-10)
- [Corrupting Attention: Evasion-Based Adversarial Attacks on Encoder Attention in Detection Transformers](https://arxiv.org/abs/2608.06674) (2026-08-10)

### ▫️ quiet auto-mode  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-08-28._

- [Claude Code Opus 5 Auto Mode tricked into RCE via website summarization](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372) (2026-08-28)
- [Auto mode is now the default in Claude Code for Pro, Max](https://simonwillison.net/2026/Aug/8/auto-mode/#atom-everything) (2026-08-08)

### ▫️ quiet dast  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-08-26._

- [Isolated AI security tools report clean while attackers reach an execution sink](https://snyk.io/blog/why-your-ai-application-is-exposed/) (2026-08-26)
- [ANSI escape injection in MCP servers: hidden from humans, visible to AI](https://brightsec.com/research/detecting-ansi-escape-sequence-injection-in-mcp-servers-with-dast/) (2026-07-20)

### ▫️ quiet defenses  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-28 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [QuantGuard defends against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239v1) (2026-06-28)

### ▫️ quiet drive-by-rce  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-09-25._

- [Microsoft DevLabs DebugMCP has drive-by RCE via DNS rebinding of unauthenticated server](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/) (2026-09-25)
- [A malicious webpage could run code through OpenCode's local upgrade endpoint](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) (2026-09-24)

### ▫️ quiet enterprise  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-29 · latest 2026-08-27._

- [Five Primitives for Governing Autonomous AI Agents at Runtime](https://arxiv.org/abs/2608.26696) (2026-08-27)
- [MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027) (2026-07-29)

### ▫️ quiet federated-learning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-25 · latest 2026-08-10._

- [TOFD: Target-Oriented Feature Decoupling against Poisoning Attacks in Split Federated Learning](https://arxiv.org/abs/2608.07274) (2026-08-10)
- [Federated-learning aggregator can backdoor a QA model without seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25)

### ▫️ quiet framework  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-12 · latest 2026-08-17._

- [Pydantic AI Ships Official First-Party Guardrails, Upstreaming a Community Library](https://github.com/pydantic/pydantic-ai-harness) (2026-08-17)
- [Snyk's Agent Baseline shows agent governance products cover different outcomes](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/) (2026-08-12)

### ▫️ quiet gemini-cli  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-07._

- [Towards a Risk Assessment of Malicious Skill Files in Coding Agents](https://arxiv.org/abs/2608.05223) (2026-08-07)
- [google/adk-python CI prompt injection let a public agent leak a token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) (2026-08-03)

### ▫️ quiet governance  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-10._

- [Taxonomy-Driven Analysis of Open-Source AI Risk Mitigation Tools](https://arxiv.org/abs/2608.07446) (2026-08-10)
- [Microsoft extends Zero Trust to AI agents with a new DevSecOps pillar](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/) (2026-08-04)

### ▫️ quiet incident  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-09-24._

- [Gemini hacked three real companies in an Irregular cyber eval](https://www.cnn.com/2026/09/19/business/gemini-ai-hack-internet) (2026-09-24)
- [Meta's frontier model broke out during cyber evals, like OpenAI's and Anthropic's](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/) (2026-08-06)

### ▫️ quiet llm-security  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2026-02 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet offensive-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-03 · latest 2026-08-10._

- [BurpMCP-Ultra is a 150-tool MCP server with a scope gate](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)
- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)

### ▫️ quiet open-weights  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-03._

- [Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs) (2026-08-03)
- [Pretrained model exposure amplifies jailbreak risks in finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

### ▫️ quiet openclaw  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-31._

- [OpenClaw 2.0's usability overhaul ships with security still opt-in](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) (2026-08-31)
- [ASTELD: A Six-Axis Classification Framework for Autonomous AI Agents](https://arxiv.org/abs/2608.05201) (2026-08-07)

### ▫️ quiet package-hallucination  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-01 · latest 2026-08-09._

- [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) (2026-08-09)
- [AI Coding Agents Skip Package Verification, and Attackers Are Exploiting It](https://www.techtimes.com/articles/319457/20260701/ai-coding-agents-skip-package-verification-attackers-are-exploiting-it.htm) (2026-07-01)

### ▫️ quiet rag  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-09-15._

- [InceptionRAG splits a RAG poison into harmless-looking passages](http://arxiv.org/abs/2609.16818v1) (2026-09-15)
- [Salience Induction misleads RAG agents using true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21)

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

- [Rule-based dataflow plus LLM reasoning beats pure-LLM scanners on authorization bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) (2026-08-27)
- [affaan-m/agentshield](https://github.com/affaan-m/agentshield) (2026-08-09)

### ▫️ quiet scanner-evasion  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-24._

- [Skill cascading attacks split a harmful goal across benign-looking agent skills](http://arxiv.org/abs/2609.30383v1) (2026-09-24)
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20)

### ▫️ quiet sse-transport  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-11._

- [mysql-mcp-server SSE allows unauthenticated SQL execution via DNS rebinding](https://github.com/advisories/GHSA-rqfv-2mw9-78g2) (2026-09-11)
- [BurpMCP-Ultra is a 150-tool MCP server with a scope gate](https://github.com/Cy-S3c/BurpMCP-Ultra) (2026-08-10)

### ▫️ quiet static-analysis  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-09._

- [Cisco AI Defense mcp-scanner checks MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner) (2026-08-09)
- [CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents](https://arxiv.org/abs/2607.21642) (2026-07-21)

### ▫️ quiet tooling-2026  ·  2 findings (0 recent vs 0.0 expected) · 2 sources
_First seen 2026-02 · latest 2026-02._

- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### ▫️ quiet transfer-attack  ·  2 findings (0 recent vs 0.2 expected) · 2 sources
_First seen 2025-12-14 · latest 2026-08-10._

- [Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits](https://arxiv.org/abs/2608.07430) (2026-08-10)
- [Pretrained model exposure amplifies jailbreak risks in finetuned LLMs](https://arxiv.org/abs/2512.14751) (2025-12-14)

## Product Security

### 🔺 rising rce  ·  19 findings (12 recent vs 1.2 expected) · 15 sources
_First seen 2026-06-29 · latest 2026-10-28._

- [Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html) (2026-10-28) · _latest_
- [Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/) (2026-10-24) · _latest_
- [New unpatched PHP RCE (CVE-2026-115560) is separate from PHP2Shell](https://www.bleepingcomputer.com/news/security/php-shares-mitigation-for-new-and-unpatched-rce-vulnerability/) (2026-10-23) · _latest_
- [Collabora CODE Server for Nextcloud command injection exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447) (2026-10-23) · _latest_
- [Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Next.js has unauthenticated RCE in use cache functions returning typed arrays](https://github.com/advisories/GHSA-673q-mjm6-r5xr) (2026-10-22) · _latest_

### 🔺 rising exploited-in-the-wild  ·  11 findings (8 recent vs 0.5 expected) · 3 sources
_First seen 2026-09-23 · latest 2026-10-22._

- [Arista VeloCloud Orchestrator SQL injection (CVE-2026-114625) is exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) (2026-10-22) · _latest_
- [CISA KEV: Plex Media Server CVE-2026-96654 is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96654) (2026-10-20) · _latest_
- [Plex CVE-2026-96652 SSRF lets the /player/timeline protocol parameter force server POSTs](https://nvd.nist.gov/vuln/detail/CVE-2026-96652) (2026-10-20) · _latest_
- [CISA KEV: Plex Media Server file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656) (2026-10-20) · _latest_
- [watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/) (2026-10-09) · _latest_
- [CISA adds a 2021 ONLYOFFICE Docs path traversal bug to KEV](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) (2026-10-08) · _latest_

### 🔺 rising php2shell  ·  7 findings (7 recent vs 0.0 expected) · 6 sources
_First seen 2026-10-22 · latest 2026-10-28._

- [InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/) (2026-10-28) · _latest_
- [Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/) (2026-10-26) · _latest_
- [Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/) (2026-10-24) · _latest_
- [New unpatched PHP RCE (CVE-2026-115560) is separate from PHP2Shell](https://www.bleepingcomputer.com/news/security/php-shares-mitigation-for-new-and-unpatched-rce-vulnerability/) (2026-10-23) · _latest_
- [PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611) (2026-10-22) · _latest_
- [Wired: AWS logged PHP2Shell exploitation attempts days before the patch](https://www.wired.com/story/hackers-exploited-the-php-vulnerabilities-days-before-they-were-patched/) (2026-10-22) · _latest_

### 🔺 rising php  ·  8 findings (7 recent vs 0.2 expected) · 8 sources
_First seen 2026-09-08 · latest 2026-10-24._

- [Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/) (2026-10-24) · _latest_
- [New unpatched PHP RCE (CVE-2026-115560) is separate from PHP2Shell](https://www.bleepingcomputer.com/news/security/php-shares-mitigation-for-new-and-unpatched-rce-vulnerability/) (2026-10-23) · _latest_
- [Wired: AWS logged PHP2Shell exploitation attempts days before the patch](https://www.wired.com/story/hackers-exploited-the-php-vulnerabilities-days-before-they-were-patched/) (2026-10-22) · _latest_
- [PHP2Shell hits every PHP since 5.4, no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/) (2026-10-22) · _latest_
- [Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_
- [Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/) (2026-10-15) · _latest_

### 🔺 rising credential-theft  ·  7 findings (6 recent vs 0.2 expected) · 5 sources
_First seen 2026-09-23 · latest 2026-10-26._

- [Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets) (2026-10-26) · _latest_
- [Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/) (2026-10-15) · _latest_
- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_
- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_
- [Wiz Blue Agent traces a stolen GitHub token to hardcoded AWS keys](https://www.wiz.io/blog/blue-agent-data-exfiltration-investigation) (2026-09-29) · _latest_

### 🔺 rising zero-day  ·  6 findings (5 recent vs 0.2 expected) · 5 sources
_First seen 2026-08-17 · latest 2026-10-28._

- [Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html) (2026-10-28) · _latest_
- [Apple patches 286 flaws and backports exploited CoreGraphics fix to iOS 18](https://www.securityweek.com/ios-macos-27-2-patch-286-bugs-fix-for-exploited-flaw-backported-to-ios-18/) (2026-10-27) · _latest_
- [watchTowr turns Citrix NetScaler DTLS overflow (CVE-2026-88772) into RCE](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/) (2026-09-29) · _latest_
- [CISA KEV: Apple CoreGraphics out-of-bounds write exploited in targeted attacks](https://nvd.nist.gov/vuln/detail/CVE-2026-86950) (2026-09-29) · _latest_
- [Citrix NetScaler CVE-2026-88771 is a pre-auth command injection zero-day in default configuration](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/) (2026-09-28) · _latest_
- [This Shit is Hard: Patching a vulnerability that has no fix](https://www.chainguard.dev/unchained/this-shit-is-hard-patching-a-vulnerability-that-has-no-fix) (2026-08-17)

### 🔺 rising incident-response  ·  7 findings (5 recent vs 0.3 expected) · 5 sources
_First seen 2026-09-10 · latest 2026-10-27._

- [Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise) (2026-10-27) · _latest_
- [OVHcloud CLI GitHub releases carried attacker binaries for 94 minutes, delivering GlassWorm](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm) (2026-10-24) · _latest_
- [Wiz CIRT describes what an AI-driven cloud intrusion looks like](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks) (2026-10-19) · _latest_
- [Cisco Talos says lab-agent attacks are loud now but will get quieter](https://blog.talosintelligence.com/one-breach-please-and-make-no-mistakes/) (2026-10-07) · _latest_
- [Wiz Blue Agent traces a stolen GitHub token to hardcoded AWS keys](https://www.wiz.io/blog/blue-agent-data-exfiltration-investigation) (2026-09-29) · _latest_
- [Semgrep adds incident-specific rescans and automated response playbooks for compromised-package events](https://semgrep.dev/blog/2026/introducing-malware-detection-and-response-automation) (2026-09-24)

### 🔺 rising command-injection  ·  8 findings (5 recent vs 0.5 expected) · 6 sources
_First seen 2026-07-20 · latest 2026-10-23._

- [Collabora CODE Server for Nextcloud command injection exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447) (2026-10-23) · _latest_
- [HPE bulletin HPESBNW05162 lists CVSS 10.0 unauthenticated RCE flaws in ArubaOS](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US) (2026-10-23) · _latest_
- [CISA KEV: SiteGuard Server Edition OS command injection exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931) (2026-10-20) · _latest_
- [CISA adds a 2016 Apache Struts DMI command injection bug to KEV](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) (2026-10-08) · _latest_
- [Citrix NetScaler CVE-2026-88771 is a pre-auth command injection zero-day in default configuration](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/) (2026-09-28) · _latest_
- [Composer passed a package's Perforce source URL to the p4 CLI](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3) (2026-09-08)

### 🔺 rising detection-engineering  ·  6 findings (4 recent vs 0.3 expected) · 5 sources
_First seen 2026-09-21 · latest 2026-10-27._

- [Check Point uses OpenAI Daybreak to turn vulnerability research into signatures](https://openai.com/index/check-point-daybreak) (2026-10-27) · _latest_
- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Wiz CIRT describes what an AI-driven cloud intrusion looks like](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks) (2026-10-19) · _latest_
- [Cisco Talos says lab-agent attacks are loud now but will get quieter](https://blog.talosintelligence.com/one-breach-please-and-make-no-mistakes/) (2026-10-07) · _latest_
- [Datadog publishes GitHub audit-log hunting queries for stolen tokens and bulk clones](https://securitylabs.datadoghq.com/articles/mapping-out-your-unknown-threat-hunters-guide-to-github) (2026-09-24)
- [AWS attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to GitHub](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### 🔺 rising xss  ·  6 findings (4 recent vs 0.3 expected) · 6 sources
_First seen 2026-08-25 · latest 2026-10-28._

- [Adobe patches eight critical flaws in Campaign Classic](https://thehackernews.com/2026/10/adobe-fixes-8-critical-campaign-classic.html) (2026-10-28) · _latest_
- [PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers](https://portswigger.net/research/scalable-vector-grief) (2026-10-27) · _latest_
- [Contao comments-bundle unauthenticated comment XSS runs in back end with no CSP](https://github.com/advisories/GHSA-628f-v4f6-p37r) (2026-10-09) · _latest_
- [Google PageBreak finds 500+ XSS bugs with near-zero false positives](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project) (2026-10-01) · _latest_
- [SourceHut account takeover via OSC 8 hyperlink XSS in rendered build logs](https://blog.arusekk.pl/posts/srht-account-takeover/) (2026-09-24)
- [What's in a tag name? JavaScript, apparently](https://portswigger.net/research) (2026-08-25)

### 🔺 rising threat-intel  ·  7 findings (4 recent vs 0.5 expected) · 6 sources
_First seen 2026-07-15 · latest 2026-10-26._

- [Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/) (2026-10-26) · _latest_
- [Wired: AWS logged PHP2Shell exploitation attempts days before the patch](https://www.wired.com/story/hackers-exploited-the-php-vulnerabilities-days-before-they-were-patched/) (2026-10-22) · _latest_
- [Cisco Talos says lab-agent attacks are loud now but will get quieter](https://blog.talosintelligence.com/one-breach-please-and-make-no-mistakes/) (2026-10-07) · _latest_
- [Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/) (2026-10-07) · _latest_
- [Snyk: the system creating a change must not be its only validator](https://snyk.io/blog/ai-hurricane-is-here/) (2026-09-15)
- [AI changes malware authoring, not execution, and most samples never ship](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/) (2026-08-25)

### 🔺 rising python  ·  8 findings (4 recent vs 0.7 expected) · 7 sources
_First seen 2026-08-31 · latest 2026-10-27._

- [Authlib accepts a JSON web signature with no signatures as verified](https://github.com/advisories/GHSA-6v38-4h7w-rj9h) (2026-10-27) · _latest_
- [Pillow EPS handling lets attacker-controlled filenames inject Ghostscript arguments (GHSA-w889-685w-c8fh)](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Pillow DoS: a 5.6 KB MIC file hangs n_frames](https://github.com/advisories/GHSA-22hg-r758-rrw9) (2026-10-21) · _latest_
- [SourceHut account takeover via OSC 8 hyperlink XSS in rendered build logs](https://blog.arusekk.pl/posts/srht-account-takeover/) (2026-09-24)
- [plone.app.portlets TALES expression injection gives authenticated users RCE](https://github.com/advisories/GHSA-rr49-f9g6-c9r5) (2026-09-23)

### 🔺 rising path-traversal  ·  9 findings (4 recent vs 0.9 expected) · 7 sources
_First seen 2026-07-09 · latest 2026-10-20._

- [Horizon3 shows FortiSIEM CVE-2026-106173 unauthenticated gRPC path traversal leads to RCE](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/) (2026-10-20) · _latest_
- [CISA KEV: exploited Fortinet CVE-2025-61624 lets read-write admins write or delete files](https://nvd.nist.gov/vuln/detail/CVE-2025-61624) (2026-10-16) · _latest_
- [CISA adds a 2021 ONLYOFFICE Docs path traversal bug to KEV](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) (2026-10-08) · _latest_
- [Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/) (2026-10-06) · _latest_
- [WSO2 API Manager path traversal to RCE is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) (2026-09-24)
- [Hono's Path-Traversal Fix Only Blocked One Parent-Directory Segment](https://github.com/advisories/GHSA-gqvv-2mrq-wpjv) (2026-09-08)

### 🔺 rising authentication-bypass  ·  3 findings (3 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-02 · latest 2026-10-27._

- [Authlib accepts a JSON web signature with no signatures as verified](https://github.com/advisories/GHSA-6v38-4h7w-rj9h) (2026-10-27) · _latest_
- [watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/) (2026-10-09) · _latest_
- [Trigger.dev self-host uses a hardcoded default secret most operators never change](https://github.com/advisories/GHSA-gg6r-gp4c-89hp) (2026-10-02) · _latest_

### 🔺 rising infostealer  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-02 · latest 2026-10-26._

- [Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/) (2026-10-26) · _latest_
- [ANY.RUN ties 1,258 sandbox analyses to fake Claude, ChatGPT and Copilot](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/) (2026-10-14) · _latest_
- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_

### 🔺 rising linux-kernel  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-19 · latest 2026-10-27._

- [Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) (2026-10-27) · _latest_
- [Two KSMBD RCE flaws hit public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html) (2026-10-22) · _latest_
- [pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_

### 🔺 rising network-appliance  ·  3 findings (3 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-28 · latest 2026-10-16._

- [CISA KEV: exploited Fortinet CVE-2025-61624 lets read-write admins write or delete files](https://nvd.nist.gov/vuln/detail/CVE-2025-61624) (2026-10-16) · _latest_
- [watchTowr turns Citrix NetScaler DTLS overflow (CVE-2026-88772) into RCE](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/) (2026-09-29) · _latest_
- [Citrix NetScaler CVE-2026-88771 is a pre-auth command injection zero-day in default configuration](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/) (2026-09-28) · _latest_

### 🔺 rising nextjs  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-22 · latest 2026-10-22._

- [Sentry's tunnelRoute skipped middleware for the whole tunnel path, not just rewrites](https://github.com/advisories/GHSA-mchm-gjx6-7h55) (2026-10-22) · _latest_
- [Next.js has unauthenticated RCE in use cache functions returning typed arrays](https://github.com/advisories/GHSA-673q-mjm6-r5xr) (2026-10-22) · _latest_
- [Next.js Image Optimization has unauthenticated RCE via SVG through sharp](https://github.com/advisories/GHSA-2464-fhr4-w9xw) (2026-10-22) · _latest_

### 🔺 rising waf  ·  3 findings (3 recent vs 0.0 expected) · 3 sources
_First seen 2026-10-20 · latest 2026-10-22._

- [Imperva shows a Node.js Brotli decoder bug (CVE-2026-111497) runs attacker code](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/) (2026-10-22) · _latest_
- [Cloudflare pairs Daybreak findings with live traffic to draft WAF rules](https://openai.com/index/cloudflare-cyber) (2026-10-21) · _latest_
- [CISA KEV: SiteGuard Server Edition OS command injection exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931) (2026-10-20) · _latest_

### 🔺 rising patch-diffing  ·  4 findings (3 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-23 · latest 2026-10-22._

- [PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611) (2026-10-22) · _latest_
- [watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/) (2026-10-09) · _latest_
- [watchTowr turns Citrix NetScaler DTLS overflow (CVE-2026-88772) into RCE](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/) (2026-09-29) · _latest_
- [F5 BIG-IP APM pre-auth heap overflow RCE (CVE-2026-94127) is exploited](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)

### 🔺 rising agentic-ai  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-21._

- [Microsoft says Storm-0940 used the ARTEX pentest framework against 2,250+ tenants](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/) (2026-10-21) · _latest_
- [CrowdStrike: four newly seen actors ran agentic Claude Code intrusions](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/) (2026-10-21) · _latest_

### 🔺 rising ai-assisted-exploitation  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-22._

- [With ChatGPT, ITRES rebuilt two BruCON techniques whose source was never released](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/) (2026-10-22) · _latest_
- [Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_

### 🔺 rising atlassian  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-06 · latest 2026-10-23._

- [Atlassian October 2026 bulletin lists 75 unique third-party CVEs](https://www.securityweek.com/atlassian-patches-75-third-party-flaws-in-data-center-and-server-products/) (2026-10-23) · _latest_
- [Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/) (2026-10-06) · _latest_

### 🔺 rising buffer-overflow  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-29 · latest 2026-10-27._

- [EDK2 network boot flaw lets attackers run code before Secure Boot](https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/) (2026-10-27) · _latest_
- [watchTowr turns Citrix NetScaler DTLS overflow (CVE-2026-88772) into RCE](https://labs.watchtowr.com/here-we-go-again-citrix-netscaler-dtls-preauth-memory-overflow-cve-2026-88772/) (2026-09-29) · _latest_

### 🔺 rising cloud  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-07 · latest 2026-10-25._

- [CVM-Store paper protects confidential VM storage at near-raw disk speed](http://arxiv.org/abs/2610.34560v1) (2026-10-25) · _latest_
- [Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/) (2026-10-07) · _latest_

### 🔺 rising edge-devices  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-20 · latest 2026-10-28._

- [InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/) (2026-10-28) · _latest_
- [SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/) (2026-10-20) · _latest_

### 🔺 rising false-positives  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-28 · latest 2026-10-01._

- [Google PageBreak finds 500+ XSS bugs with near-zero false positives](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project) (2026-10-01) · _latest_
- [GitHub Security Lab found 24 Android vulnerabilities with its AI agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/) (2026-09-28) · _latest_

### 🔺 rising firmware  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-27 · latest 2026-10-28._

- [InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/) (2026-10-28) · _latest_
- [EDK2 network boot flaw lets attackers run code before Secure Boot](https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/) (2026-10-27) · _latest_

### 🔺 rising fortinet  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-16 · latest 2026-10-20._

- [Horizon3 shows FortiSIEM CVE-2026-106173 unauthenticated gRPC path traversal leads to RCE](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/) (2026-10-20) · _latest_
- [CISA KEV: exploited Fortinet CVE-2025-61624 lets read-write admins write or delete files](https://nvd.nist.gov/vuln/detail/CVE-2025-61624) (2026-10-16) · _latest_

### 🔺 rising ios  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-09-29 · latest 2026-10-27._

- [Apple patches 286 flaws and backports exploited CoreGraphics fix to iOS 18](https://www.securityweek.com/ios-macos-27-2-patch-286-bugs-fix-for-exploited-flaw-backported-to-ios-18/) (2026-10-27) · _latest_
- [CISA KEV: Apple CoreGraphics out-of-bounds write exploited in targeted attacks](https://nvd.nist.gov/vuln/detail/CVE-2026-86950) (2026-09-29) · _latest_

### 🔺 rising mfa-bypass  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-08 · latest 2026-10-20._

- [Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass GlobalProtect MFA](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/) (2026-10-20) · _latest_
- [UAT-11985 lured Taiwan researchers with likely AI-templated invitations and live MFA relay](https://blog.talosintelligence.com/uat-11985/) (2026-10-08) · _latest_

### 🔺 rising patch-tuesday  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-13 · latest 2026-10-27._

- [Apple patches 286 flaws and backports exploited CoreGraphics fix to iOS 18](https://www.securityweek.com/ios-macos-27-2-patch-286-bugs-fix-for-exploited-flaw-backported-to-ios-18/) (2026-10-27) · _latest_
- [Microsoft's October 2026 Patch Tuesday fixes one exploited Windows Shell bypass](https://blog.talosintelligence.com/microsoft-patch-tuesday-for-october-2026/) (2026-10-13) · _latest_

### 🔺 rising pillow  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-23._

- [Pillow EPS handling lets attacker-controlled filenames inject Ghostscript arguments (GHSA-w889-685w-c8fh)](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [Pillow DoS: a 5.6 KB MIC file hangs n_frames](https://github.com/advisories/GHSA-22hg-r758-rrw9) (2026-10-21) · _latest_

### 🔺 rising pre-auth  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-06 · latest 2026-10-20._

- [Claude found 493 attack-surface issues across 25 open-source projects](https://www.anthropic.com/research/attack-surface-reduction) (2026-10-20) · _latest_
- [Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/) (2026-10-06) · _latest_

### 🔺 rising ssrf  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-20 · latest 2026-10-28._

- [Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html) (2026-10-28) · _latest_
- [Plex CVE-2026-96652 SSRF lets the /player/timeline protocol parameter force server POSTs](https://nvd.nist.gov/vuln/detail/CVE-2026-96652) (2026-10-20) · _latest_

### 🔺 rising variant-analysis  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-06 · latest 2026-10-27._

- [Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) (2026-10-27) · _latest_
- [CheckerBench gives agents 300 CVE-derived tasks to write static-analysis checkers](https://arxiv.org/abs/2610.07557) (2026-10-06) · _latest_

### 🔺 rising vulnerability-management  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-08 · latest 2026-10-21._

- [Cloudflare pairs Daybreak findings with live traffic to draft WAF rules](https://openai.com/index/cloudflare-cyber) (2026-10-21) · _latest_
- [Chainguard Athena agents deduplicate private zero-day reports without leaking reporters](https://www.chainguard.dev/unchained/this-shit-is-hard-building-a-vulnerability-database-from-private-reports) (2026-10-08) · _latest_

### 🔺 rising web3  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-05 · latest 2026-10-07._

- [Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/) (2026-10-07) · _latest_
- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_

### 🔺 rising wordpress  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-21 · latest 2026-10-26._

- [Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/) (2026-10-26) · _latest_
- [Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_

### 🔺 rising ai-agents  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-26 · latest 2026-10-20._

- [SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/) (2026-10-20) · _latest_
- [OpenAI says Sophos MDR agents cut average case time to ~89 seconds](https://openai.com/index/sophos) (2026-10-09) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### 🔺 rising ai-vulnerability-discovery  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-09-15 · latest 2026-10-22._

- [PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611) (2026-10-22) · _latest_
- [Google PageBreak finds 500+ XSS bugs with near-zero false positives](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project) (2026-10-01) · _latest_
- [Chainguard starts disclosing Athena's silent-fix vulnerabilities](https://www.chainguard.dev/unchained/the-flood-is-coming-and-the-pipes-were-already-full) (2026-09-15)

### 🔺 rising blockchain-c2  ·  3 findings (2 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-21 · latest 2026-10-08._

- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/) (2026-10-07) · _latest_
- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)

### 🔺 rising bola  ·  3 findings (2 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-27 · latest 2026-10-26._

- [Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto) (2026-10-26) · _latest_
- [Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/) (2026-10-01) · _latest_
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### 🔺 rising cloudtrail  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-09-21 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Wiz Blue Agent traces a stolen GitHub token to hardcoded AWS keys](https://www.wiz.io/blog/blue-agent-data-exfiltration-investigation) (2026-09-29) · _latest_
- [AWS attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to GitHub](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### 🔺 rising coding-agents  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-14 · latest 2026-10-06._

- [CheckerBench gives agents 300 CVE-derived tasks to write static-analysis checkers](https://arxiv.org/abs/2610.07557) (2026-10-06) · _latest_
- [Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/) (2026-10-01) · _latest_
- [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) (2026-07-14)

### 🔺 rising kubernetes  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-24 · latest 2026-10-05._

- [Datadog: 3,500+ RBAC bindings give dangerous permissions to groups like system:unauthenticated](https://securitylabs.datadoghq.com/articles/kubernetes-rbac-built-in-principals-dangerous-permissions/) (2026-10-05) · _latest_
- [CiliumHound graphs Cilium Kubernetes network policies as a BloodHound OpenGraph extension](https://specterops.io/blog/2026/09/17/ciliumhound-graphing-kubernetes-network-policies) (2026-10-01) · _latest_
- [etcd Watch API skipped the range authorization that Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### 🔺 rising least-privilege  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-26 · latest 2026-10-27._

- [Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise) (2026-10-27) · _latest_
- [Datadog: 3,500+ RBAC bindings give dangerous permissions to groups like system:unauthenticated](https://securitylabs.datadoghq.com/articles/kubernetes-rbac-built-in-principals-dangerous-permissions/) (2026-10-05) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### 🔺 rising macos  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-05 · latest 2026-10-27._

- [Apple patches 286 flaws and backports exploited CoreGraphics fix to iOS 18](https://www.securityweek.com/ios-macos-27-2-patch-286-bugs-fix-for-exploited-flaw-backported-to-ios-18/) (2026-10-27) · _latest_
- [CISA KEV: Apple CoreGraphics out-of-bounds write exploited in targeted attacks](https://nvd.nist.gov/vuln/detail/CVE-2026-86950) (2026-09-29) · _latest_
- [macOS ClickFix campaign now cloaks its payload behind browser-fingerprinting gates](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/) (2026-08-05)

### 🔺 rising red-teaming  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [NorForge found exposed Cairn AI-pentest panels used by criminals and red teams](https://norforge.com/blog/inside_cairn) (2026-10-19) · _latest_
- [Can AI do novel security research? Meet the HTTP Terminator](https://portswigger.net/research/can-ai-do-novel-security-research) (2026-08-05)

### 🔺 rising sql-injection  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-09-14 · latest 2026-10-28._

- [Adobe patches eight critical flaws in Campaign Classic](https://thehackernews.com/2026/10/adobe-fixes-8-critical-campaign-classic.html) (2026-10-28) · _latest_
- [Arista VeloCloud Orchestrator SQL injection (CVE-2026-114625) is exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) (2026-10-22) · _latest_
- [Cisco Secure Email Gateway SQL injection reaches root command execution](https://nvd.nist.gov/vuln/detail/CVE-2026-76461) (2026-09-14)

### 🔺 rising android  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-04 · latest 2026-10-27._

- [Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) (2026-10-27) · _latest_
- [GitHub Security Lab found 24 Android vulnerabilities with its AI agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/) (2026-09-28) · _latest_
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### 🔺 rising aws  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-05 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [Wiz Blue Agent traces a stolen GitHub token to hardcoded AWS keys](https://www.wiz.io/blog/blue-agent-data-exfiltration-investigation) (2026-09-29) · _latest_
- [AWS attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to GitHub](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)
- [A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/) (2026-08-05)

### 🔺 rising nodejs  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-10-23._

- [Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8) (2026-10-23) · _latest_
- [Imperva shows a Node.js Brotli decoder bug (CVE-2026-111497) runs attacker code](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/) (2026-10-22) · _latest_
- [morgan's log-forging fix missed Unicode line-separator code points](https://github.com/advisories/GHSA-jxfw-x594-9x9m) (2026-09-08)
- [Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr) (2026-07-24)

### 🔺 rising ransomware  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-07-09 · latest 2026-10-20._

- [Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass GlobalProtect MFA](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/) (2026-10-20) · _latest_
- [SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/) (2026-10-20) · _latest_
- [AI changes malware authoring, not execution, and most samples never ship](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/) (2026-08-25)
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### 🔺 rising memory-safety  ·  5 findings (2 recent vs 0.5 expected) · 4 sources
_First seen 2026-04 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://www.wiz.io/blog/php2shell-php-rce) (2026-10-21) · _latest_
- [F5 BIG-IP APM pre-auth heap overflow RCE (CVE-2026-94127) is exploited](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### 🔺 rising privilege-escalation  ·  5 findings (2 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-20 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [CISA KEV: Zammad local privilege escalation to root exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-102490) (2026-10-02) · _latest_
- [plone.app.portlets TALES expression injection gives authenticated users RCE](https://github.com/advisories/GHSA-rr49-f9g6-c9r5) (2026-09-23)
- [Acronis Backup plugins have insecure file permissions exploited for privilege escalation](https://nvd.nist.gov/vuln/detail/CVE-2026-87886) (2026-09-16)
- [Siemens Ruggedcom ROX II three-CVE chain yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### 🔺 rising supply-chain  ·  33 findings (6 recent vs 4.7 expected) · 21 sources
_First seen 2026-06-30 · latest 2026-10-27._

- [Skimmers hijacked Convertr's self-hosted analytics script to steal checkout card data](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/) (2026-10-27) · _latest_
- [Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets) (2026-10-26) · _latest_
- [Trail of Bits: only Go and vcpkg verified every downloaded package](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/) (2026-10-14) · _latest_
- [Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/) (2026-10-07) · _latest_
- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_
- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_

### 🔺 rising npm  ·  13 findings (3 recent vs 1.7 expected) · 9 sources
_First seen 2026-07-15 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time to catch compromises](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_
- [MemTensor packages shipped the 'sckit' Go worm after stolen publish tokens](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop self-propagating npm worm mints valid Sigstore provenance, exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)

### 🔺 rising shai-hulud  ·  6 findings (2 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-15 · latest 2026-10-08._

- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_
- [Mini Shai-Hulud still spreads four months on via hijacked actions-cool/issues-helper tags](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24)
- [keyv/cacheable Mini Shai-Hulud is a self-propagating worm with Ethereum-resolved C2](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)
- [The npm Threat Landscape: Attack Surface and Mitigations](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/) (2026-07-15)

### 🔺 rising github-actions  ·  7 findings (2 recent vs 0.9 expected) · 6 sources
_First seen 2026-07-16 · latest 2026-10-26._

- [Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets) (2026-10-26) · _latest_
- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_
- [Mini Shai-Hulud still spreads four months on via hijacked actions-cool/issues-helper tags](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24)
- [MemTensor packages shipped the 'sckit' Go worm after stolen publish tokens](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [Org-wide GitHub Actions SHA-pinning enforcement has non-obvious failure modes](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)
- [Disrupting supply chain attacks on NPM and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) (2026-07-29)

### ▪️ steady provenance  ·  5 findings (1 recent vs 0.7 expected) · 5 sources
_First seen 2026-07-16 · latest 2026-10-08._

- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [This Shit is Hard: Patching a vulnerability that has no fix](https://www.chainguard.dev/unchained/this-shit-is-hard-patching-a-vulnerability-that-has-no-fix) (2026-08-17)
- [The keyv npm compromise shipped a poisoned build with valid provenance](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) (2026-08-04)
- [keyv/cacheable Mini Shai-Hulud is a self-propagating worm with Ethereum-resolved C2](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16)

### ▪️ steady worm  ·  5 findings (1 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-04 · latest 2026-10-08._

- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [Mini Shai-Hulud still spreads four months on via hijacked actions-cool/issues-helper tags](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24)
- [MemTensor packages shipped the 'sckit' Go worm after stolen publish tokens](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [ChainDrop self-propagating npm worm mints valid Sigstore provenance, exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [keyv/cacheable Mini Shai-Hulud is a self-propagating worm with Ethereum-resolved C2](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)

### ▪️ steady ai-pentesting  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-27 · latest 2026-10-19._

- [NorForge found exposed Cairn AI-pentest panels used by criminals and red teams](https://norforge.com/blog/inside_cairn) (2026-10-19) · _latest_
- [Wiz's AI pentest agent found exposures at hospitals, archives and platforms](https://www.wiz.io/blog/scan-for-good-critical-ai-exposures) (2026-09-24)
- [Show, Don't Tell: Evo found issues in a real enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### ▪️ steady oauth  ·  4 findings (1 recent vs 0.5 expected) · 4 sources
_First seen 2026-07-24 · latest 2026-10-21._

- [Microsoft says Storm-0940 used the ARTEX pentest framework against 2,250+ tenants](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/) (2026-10-21) · _latest_
- [Datadog publishes GitHub audit-log hunting queries for stolen tokens and bulk clones](https://securitylabs.datadoghq.com/articles/mapping-out-your-unknown-threat-hunters-guide-to-github) (2026-09-24)
- [F5 BIG-IP APM pre-auth heap overflow RCE (CVE-2026-94127) is exploited](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Four stacked evasion techniques hide device-code phishing from scanners](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt) (2026-07-24)

### ▪️ steady ai-generated-code  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-10-01._

- [Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/) (2026-10-01) · _latest_
- [Snyk: the system creating a change must not be its only validator](https://snyk.io/blog/ai-hurricane-is-here/) (2026-09-15)
- [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▪️ steady claude-code  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-04 · latest 2026-10-21._

- [CrowdStrike: four newly seen actors ran agentic Claude Code intrusions](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/) (2026-10-21) · _latest_
- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [The keyv npm compromise shipped a poisoned build with valid provenance](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) (2026-08-04)

### ▪️ steady edge-appliance  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-06-29 · latest 2026-10-15._

- [BeyondTrust Remote Support flaw lets a remote attacker perform file operations](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05) (2026-10-15) · _latest_
- [F5 BIG-IP APM pre-auth heap overflow RCE (CVE-2026-94127) is exploited](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/) (2026-09-23)
- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29)

### ▪️ steady exploit-chain  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-05 · latest 2026-10-02._

- [CISA KEV: Zammad local privilege escalation to root exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-102490) (2026-10-02) · _latest_
- [Siemens Ruggedcom ROX II three-CVE chain yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)

### ▪️ steady fuzzing  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-09-23 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [GitHub Security Lab's Fuzzing Taskflow has an LLM agent write AFL++ harnesses](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/) (2026-09-24)
- [Turbo Intruder adds an HTTP/3 engine and HTTP/3 race-condition techniques](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)

### ▪️ steady malware  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-09 · latest 2026-10-27._

- [Check Point: fake ChatGPT and Claude apps sideload malware via signed installers](https://research.checkpoint.com/2026/tricks-from-the-past-deployed-via-signed-chatgpt-and-claude-binaries/) (2026-10-27) · _latest_
- [LLM-assisted IoT botnet TuxBot v3 left the model's safety disclaimer in source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-15)
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### ▪️ steady multi-tenant  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-22._

- [raml-kql runs one KQL query across workspaces without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql) (2026-10-22) · _latest_
- [Moquette MQTT broker clientId wildcard injection gives cross-tenant read/write](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [Show, Don't Tell: Evo found issues in a real enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)

### ▪️ steady phishing  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-06-30 · latest 2026-10-08._

- [UAT-11985 lured Taiwan researchers with likely AI-templated invitations and live MFA relay](https://blog.talosintelligence.com/uat-11985/) (2026-10-08) · _latest_
- [Four stacked evasion techniques hide device-code phishing from scanners](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt) (2026-07-24)
- [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) (2026-06-30)

### ▪️ steady prompt-injection  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-09 · latest 2026-10-02._

- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_
- [Sanitized webmail CSS steals tokens and keylogs Outlook](https://portswigger.net/research/css-the-bomb-inside-your-inbox) (2026-08-06)
- [Wiz 'GhostApproval': git symlinks let AI coding assistants write outside the workspace](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▪️ steady pypi  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-10-02._

- [Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud) (2026-10-02) · _latest_
- [MemTensor packages shipped the 'sckit' Go worm after stolen publish tokens](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)
- [Snyk Evo Agentic AppSec launches with autonomous remediation and package scanning](https://snyk.io/blog/remediation-agent-malicious-code-defense/) (2026-08-04)

### ▪️ steady sandbox-escape  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-09 · latest 2026-10-27._

- [Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) (2026-10-27) · _latest_
- [Markdown Preview Enhanced, a VS Code extension, chained flaws into RCE](https://projectdiscovery.io/blog/a-9-5m-install-vs-code-extension-one-markdown-file-and-a-supply-chain-foothold) (2026-08-16)
- [Wiz 'GhostApproval': git symlinks let AI coding assistants write outside the workspace](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

### ▪️ steady sast  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-20 · latest 2026-10-06._

- [CheckerBench gives agents 300 CVE-derived tasks to write static-analysis checkers](https://arxiv.org/abs/2610.07557) (2026-10-06) · _latest_
- [Introducing Semgrep Agentic Workflows: Automate Deep Vulnerability Hunting at Scale](https://semgrep.dev/blog/2026/introducing-semgrep-agentic-workflows-automate-deep-vulnerability-hunting-at-scale) (2026-07-28)
- [A working taxonomy of open-source AI code-security harnesses](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses) (2026-07-20)

### ▪️ steady tooling  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-20 · latest 2026-10-01._

- [CiliumHound graphs Cilium Kubernetes network policies as a BloodHound OpenGraph extension](https://specterops.io/blog/2026/09/17/ciliumhound-graphing-kubernetes-network-policies) (2026-10-01) · _latest_
- [Turbo Intruder adds an HTTP/3 engine and HTTP/3 race-condition techniques](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)
- [A working taxonomy of open-source AI code-security harnesses](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses) (2026-07-20)

### ▪️ steady wiper  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-09 · latest 2026-10-23._

- [ESET: UAC-0099 used MythicRatatoskr with C2 inside Yggdrasil before Sandworm struck](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html) (2026-10-23) · _latest_
- [Mini Shai-Hulud still spreads four months on via hijacked actions-cool/issues-helper tags](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24)
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09)

### ▪️ steady agent-harness  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-01._

- [Google PageBreak finds 500+ XSS bugs with near-zero false positives](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project) (2026-10-01) · _latest_
- [Can AI do novel security research? Meet the HTTP Terminator](https://portswigger.net/research/can-ai-do-novel-security-research) (2026-08-05)

### ▪️ steady api-security  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-10-26._

- [Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto) (2026-10-26) · _latest_
- [etcd Watch API skipped the range authorization that Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### ▪️ steady apt  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-08._

- [UAT-11985 lured Taiwan researchers with likely AI-templated invitations and live MFA relay](https://blog.talosintelligence.com/uat-11985/) (2026-10-08) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady arbitrary-file-read  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-06._

- [Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/) (2026-10-06) · _latest_
- [Siemens Ruggedcom ROX II three-CVE chain yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### ▪️ steady authorization-bypass  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-22._

- [Sentry's tunnelRoute skipped middleware for the whole tunnel path, not just rewrites](https://github.com/advisories/GHSA-mchm-gjx6-7h55) (2026-10-22) · _latest_
- [Adobe Commerce and Magento flaw gives elevated access without user interaction](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) (2026-09-24)

### ▪️ steady broken-access-control  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-01._

- [Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/) (2026-10-01) · _latest_
- [Show, Don't Tell: Evo found issues in a real enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)

### ▪️ steady browser-security  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-25 · latest 2026-10-27._

- [Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) (2026-10-27) · _latest_
- [SourTrade reassembles a Bun-based executable in the browser to defeat hash-based detection](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html) (2026-07-25)

### ▪️ steady c2  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-23._

- [ESET: UAC-0099 used MythicRatatoskr with C2 inside Yggdrasil before Sandworm struck](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html) (2026-10-23) · _latest_
- [ChainDrop self-propagating npm worm mints valid Sigstore provenance, exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)

### ▪️ steady clickfix  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-10-14._

- [ANY.RUN ties 1,258 sandbox analyses to fake Claude, ChatGPT and Copilot](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/) (2026-10-14) · _latest_
- [macOS ClickFix campaign now cloaks its payload behind browser-fingerprinting gates](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/) (2026-08-05)

### ▪️ steady composer  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-10-14._

- [Trail of Bits: only Go and vcpkg verified every downloaded package](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/) (2026-10-14) · _latest_
- [Composer passed a package's Perforce source URL to the p4 CLI](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3) (2026-09-08)

### ▪️ steady containment  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-10 · latest 2026-10-27._

- [Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise) (2026-10-27) · _latest_
- [A self-replicating worm on stolen compute infected a lab network](https://derekjames.substack.com/p/adaptive-agentic-worms) (2026-09-10)

### ▪️ steady coordinated-disclosure  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-14 · latest 2026-10-22._

- [PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611) (2026-10-22) · _latest_
- [Black Duck consumes Chainguard's Athena OSV feed to alert customers](https://www.chainguard.dev/unchained/athena-spotlight-black-duck-on-the-importance-of-flagging-zero-days-at-scale) (2026-09-14)

### ▪️ steady csp  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-25 · latest 2026-10-09._

- [Contao comments-bundle unauthenticated comment XSS runs in back end with no CSP](https://github.com/advisories/GHSA-628f-v4f6-p37r) (2026-10-09) · _latest_
- [What's in a tag name? JavaScript, apparently](https://portswigger.net/research) (2026-08-25)

### ▪️ steady dast  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-27 · latest 2026-10-26._

- [Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto) (2026-10-26) · _latest_
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### ▪️ steady ddos  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-08._

- [Imperva publishes a DDoS readiness checklist covering BGP and GRE tunnel health](https://www.imperva.com/blog/ddos-readiness-is-your-ddos-protection-actually-on/) (2026-10-08) · _latest_
- [A large-scale forecasting benchmark for anomaly detection in research networks](https://arxiv.org/abs/2608.05605) (2026-08-07)

### ▪️ steady denial-of-service  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-23 · latest 2026-10-06._

- [Valid SQL crashes SQLGlot and SQLFluff with huge memory amplification](https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/) (2026-10-06) · _latest_
- [Moquette MQTT broker clientId wildcard injection gives cross-tenant read/write](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)

### ▪️ steady dependency-cooldown  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-31 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time to catch compromises](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [A One-Week Dependency Cooldown Produces Outsized Supply-Chain Protection for Minimal Developer Friction](https://semgrep.dev/blog/2026/rolling-out-dependency-cooldowns-org-wide) (2026-08-31)

### ▪️ steady disclosure  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-15 · latest 2026-10-22._

- [Two KSMBD RCE flaws hit public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html) (2026-10-22) · _latest_
- [Chainguard starts disclosing Athena's silent-fix vulnerabilities](https://www.chainguard.dev/unchained/the-flood-is-coming-and-the-pipes-were-already-full) (2026-09-15)

### ▪️ steady e-commerce  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-27._

- [Skimmers hijacked Convertr's self-hosted analytics script to steal checkout card data](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/) (2026-10-27) · _latest_
- [Adobe Commerce and Magento flaw gives elevated access without user interaction](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) (2026-09-24)

### ▪️ steady file-upload  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-23._

- [Pillow EPS handling lets attacker-controlled filenames inject Ghostscript arguments (GHSA-w889-685w-c8fh)](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) (2026-10-23) · _latest_
- [WSO2 API Manager path traversal to RCE is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) (2026-09-24)

### ▪️ steady formal-verification  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-09 · latest 2026-10-22._

- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification) (2026-10-22) · _latest_
- [A Lean 4 string-slice mismatch let native_decide 'prove' Fermat's Last Theorem](https://blog.trailofbits.com/2026/09/09/a-proof-of-fermats-last-theorem-that-fits-the-margin/) (2026-09-09)

### ▪️ steady gitlab  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-10 · latest 2026-10-21._

- [GitLab patches CVE-2026-110264, a CVSS 10.0 unauthenticated RCE in the regex compiler](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/) (2026-10-21) · _latest_
- [Wiz poster maps incident response logs for GitHub, GitLab and Bitbucket](https://www.wiz.io/blog/vcs-dfir-threat-hunting-github-gitlab-azure-devops) (2026-09-10)

### ▪️ steady iam  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-21 · latest 2026-10-22._

- [Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/) (2026-10-22) · _latest_
- [AWS attached AWSCompromisedKeyQuarantineV3 within 10 seconds of a key pushed to GitHub](https://unit42.paloaltonetworks.com/detecting-exposed-aws-iam-credentials/) (2026-09-21)

### ▪️ steady idor  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-10-01._

- [Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/) (2026-10-01) · _latest_
- [etcd Watch API skipped the range authorization that Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### ▪️ steady image-processing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-10-22._

- [Next.js Image Optimization has unauthenticated RCE via SVG through sharp](https://github.com/advisories/GHSA-2464-fhr4-w9xw) (2026-10-22) · _latest_
- [Astro's default image optimizer allowed remote code execution via malicious AVIF images](https://github.com/advisories/GHSA-26w7-cxv4-gfx2) (2026-09-08)

### ▪️ steady import-time-payload  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-23 · latest 2026-10-05._

- [@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised) (2026-10-05) · _latest_
- [MemTensor packages shipped the 'sckit' Go worm after stolen publish tokens](https://safedep.io/memtensor-sckit-worm-npm-pypi) (2026-09-23)

### ▪️ steady incident  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-21._

- [Railway says encrypted environment variables may have been accessed](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) (2026-10-21) · _latest_
- [Faulty Samsung SmartThings firmware push bricked Bespoke AI fridges in Korea](https://arstechnica.com/gadgets/2026/09/owners-mourn-spoiled-food-after-firmware-update-bricks-samsung-smart-fridges/) (2026-09-24)

### ▪️ steady kvm  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-19._

- [pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady llm-agents  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-08._

- [Chainguard Athena agents deduplicate private zero-day reports without leaking reporters](https://www.chainguard.dev/unchained/this-shit-is-hard-building-a-vulnerability-database-from-private-reports) (2026-10-08) · _latest_
- [GitHub Security Lab's Fuzzing Taskflow has an LLM agent write AFL++ harnesses](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/) (2026-09-24)

### ▪️ steady log-injection  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-09-28._

- [Citrix NetScaler CVE-2026-88771 is a pre-auth command injection zero-day in default configuration](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/) (2026-09-28) · _latest_
- [morgan's log-forging fix missed Unicode line-separator code points](https://github.com/advisories/GHSA-jxfw-x594-9x9m) (2026-09-08)

### ▪️ steady malicious-packages  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-19._

- [Wiz scans every new npm version at publish time to catch compromises](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication) (2026-10-19) · _latest_
- [Semgrep adds incident-specific rescans and automated response playbooks for compromised-package events](https://semgrep.dev/blog/2026/introducing-malware-detection-and-response-automation) (2026-09-24)

### ▪️ steady malvertising  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-25 · latest 2026-10-14._

- [ANY.RUN ties 1,258 sandbox analyses to fake Claude, ChatGPT and Copilot](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/) (2026-10-14) · _latest_
- [SourTrade reassembles a Bun-based executable in the browser to defeat hash-based detection](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html) (2026-07-25)

### ▪️ steady open-source  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-10-08._

- [Chainguard Athena agents deduplicate private zero-day reports without leaking reporters](https://www.chainguard.dev/unchained/this-shit-is-hard-building-a-vulnerability-database-from-private-reports) (2026-10-08) · _latest_
- [A working taxonomy of open-source AI code-security harnesses](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses) (2026-07-20)

### ▪️ steady opinion  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-15 · latest 2026-10-27._

- [Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise) (2026-10-27) · _latest_
- [Snyk: the system creating a change must not be its only validator](https://snyk.io/blog/ai-hurricane-is-here/) (2026-09-15)

### ▪️ steady rbac  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-10-05._

- [Datadog: 3,500+ RBAC bindings give dangerous permissions to groups like system:unauthenticated](https://securitylabs.datadoghq.com/articles/kubernetes-rbac-built-in-principals-dangerous-permissions/) (2026-10-05) · _latest_
- [etcd Watch API skipped the range authorization that Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### ▪️ steady secrets  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-10-21._

- [Railway says encrypted environment variables may have been accessed](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) (2026-10-21) · _latest_
- [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▪️ steady side-channel  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-06 · latest 2026-10-15._

- [A client's 1-bit reply leaks the full CKKS secret key](http://arxiv.org/abs/2610.21127v1) (2026-10-15) · _latest_
- [Consumer smart glasses enable a video-based password-cracking pipeline](http://arxiv.org/abs/2609.06539v1) (2026-09-06)

### ▪️ steady spyware  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-28 · latest 2026-10-15._

- [Citizen Lab: Candiru spyware reached Al Jazeera devices through targeted ads](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/) (2026-10-15) · _latest_
- [Co-Founder of Controversial Spyware Firm Had Israeli Diplomatic Passport](https://citizenlab.ca/co-founder-of-controversial-spyware-firm-had-israeli-diplomatic-passport/) (2026-07-28)

### ▪️ steady static-analysis  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-10-06._

- [CheckerBench gives agents 300 CVE-derived tasks to write static-analysis checkers](https://arxiv.org/abs/2610.07557) (2026-10-06) · _latest_
- [Snyk Evo Agentic AppSec launches with autonomous remediation and package scanning](https://snyk.io/blog/remediation-agent-malicious-code-defense/) (2026-08-04)

### ▪️ steady token-theft  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-24 · latest 2026-10-26._

- [Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets) (2026-10-26) · _latest_
- [Datadog publishes GitHub audit-log hunting queries for stolen tokens and bulk clones](https://securitylabs.datadoghq.com/articles/mapping-out-your-unknown-threat-hunters-guide-to-github) (2026-09-24)

### ▪️ steady trusted-publishing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-29 · latest 2026-10-08._

- [tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud) (2026-10-08) · _latest_
- [Disrupting supply chain attacks on NPM and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) (2026-07-29)

### ▪️ steady vm-escape  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-26 · latest 2026-10-19._

- [pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape) (2026-10-19) · _latest_
- [VMs won't contain cyber-capable agents](https://blog.trailofbits.com/) (2026-08-26)

### ▪️ steady waf-bypass  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-25 · latest 2026-10-28._

- [Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html) (2026-10-28) · _latest_
- [What's in a tag name? JavaScript, apparently](https://portswigger.net/research) (2026-08-25)

### ▪️ steady zero-click  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-05 · latest 2026-10-15._

- [Citizen Lab: Candiru spyware reached Al Jazeera devices through targeted ads](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/) (2026-10-15) · _latest_
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)

### ▫️ quiet ci-cd  ·  7 findings (0 recent vs 1.2 expected) · 6 sources
_First seen 2026-07-15 · latest 2026-09-24._

- [Wiz's AI pentest agent found exposures at hospitals, archives and platforms](https://www.wiz.io/blog/scan-for-good-critical-ai-exposures) (2026-09-24)
- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [Org-wide GitHub Actions SHA-pinning enforcement has non-obvious failure modes](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)
- [ChainDrop self-propagating npm worm mints valid Sigstore provenance, exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [Disrupting supply chain attacks on NPM and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) (2026-07-29)
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16)

### ▫️ quiet authorization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-24 · latest 2026-09-23._

- [Moquette MQTT broker clientId wildcard injection gives cross-tenant read/write](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [Show, Don't Tell: Evo found issues in a real enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [etcd Watch API skipped the range authorization that Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8) (2026-07-24)

### ▫️ quiet go  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-24 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [go-git reference names as path traversal: refs/heads/../../config overwrites .git metadata (GHSA-qgq7-7hm3-q39j)](https://github.com/advisories/GHSA-qgq7-7hm3-q39j) (2026-08-07)
- [Oh My Posh runs commands from a directory name](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq) (2026-07-24)

### ▫️ quiet iot  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-15 · latest 2026-09-24._

- [Faulty Samsung SmartThings firmware push bricked Bespoke AI fridges in Korea](https://arstechnica.com/gadgets/2026/09/owners-mourn-spoiled-food-after-firmware-update-bricks-samsung-smart-fridges/) (2026-09-24)
- [Moquette MQTT broker clientId wildcard injection gives cross-tenant read/write](https://github.com/advisories/GHSA-5f42-97gr-vfhq) (2026-09-23)
- [LLM-assisted IoT botnet TuxBot v3 left the model's safety disclaimer in source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-15)

### ▫️ quiet request-smuggling  ·  3 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-02-05 · latest 2026-09-23._

- [Turbo Intruder adds an HTTP/3 engine and HTTP/3 race-condition techniques](https://portswigger.net/research/http3-in-burp-suite) (2026-09-23)
- [CRLF header injection escalates to CDN-wide response queue poisoning](https://portswigger.net/research/crlf-powered-desync-attacks) (2026-08-05)
- [PortSwigger's Top 10 Web Hacking Techniques of 2025](https://portswigger.net/research/top-10-web-hacking-techniques-of-2025) (2026-02-05)

### ▫️ quiet bun-runtime  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-04._

- [keyv/cacheable Mini Shai-Hulud is a self-propagating worm with Ethereum-resolved C2](https://www.chainguard.dev/unchained/the-keyv-and-cacheable-npm-supply-chain-attack-inside-the-mini-shai-hulud-campaign) (2026-08-04)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet business-logic  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-27 · latest 2026-08-10._

- [Show, Don't Tell: Evo found issues in a real enterprise SaaS](https://snyk.io/blog/what-evo-cos-found-real-enterprise-saas/) (2026-08-10)
- [What Is AI Pentesting and How Does It Work?](https://snyk.io/blog/what-is-ai-pentesting/) (2026-07-27)

### ▫️ quiet chaindrop  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-21._

- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet code-review  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-14 · latest 2026-07-30._

- [Cryptographic advisories are dominated by skipped code checks, not broken math](https://semgrep.dev/blog/2026/crypto-is-fine-the-code-is-not) (2026-07-30)
- [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) (2026-07-14)

### ▫️ quiet cryptography  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-30 · latest 2026-09-08._

- [phpseclib's X25519 leaks its private key through a libgmp side channel](https://github.com/advisories/GHSA-q97c-8qh3-fpc6) (2026-09-08)
- [Cryptographic advisories are dominated by skipped code checks, not broken math](https://semgrep.dev/blog/2026/crypto-is-fine-the-code-is-not) (2026-07-30)

### ▫️ quiet git  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [go-git reference names as path traversal: refs/heads/../../config overwrites .git metadata (GHSA-qgq7-7hm3-q39j)](https://github.com/advisories/GHSA-qgq7-7hm3-q39j) (2026-08-07)

### ▫️ quiet incomplete-fix  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-09-08 · latest 2026-09-08._

- [Hono's Path-Traversal Fix Only Blocked One Parent-Directory Segment](https://github.com/advisories/GHSA-gqvv-2mrq-wpjv) (2026-09-08)
- [morgan's log-forging fix missed Unicode line-separator code points](https://github.com/advisories/GHSA-jxfw-x594-9x9m) (2026-09-08)

### ▫️ quiet mcp  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-05 · latest 2026-09-24._

- [GitHub Security Lab's Fuzzing Taskflow has an LLM agent write AFL++ harnesses](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/) (2026-09-24)
- [Can AI do novel security research? Meet the HTTP Terminator](https://portswigger.net/research/can-ai-do-novel-security-research) (2026-08-05)

### ▫️ quiet oidc  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-21._

- [ChainDrop npm worm targeted Claude Code configs and stole OIDC tokens](https://unit42.paloaltonetworks.com/sdlc-supply-chain/) (2026-08-21)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet persistence  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-20 · latest 2026-09-10._

- [JFrog Artifactory auth bypass chain exploited in the wild leaves persistent backdoors](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201) (2026-09-10)
- [Siemens Ruggedcom ROX II three-CVE chain yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20)

### ▫️ quiet rust  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-04 · latest 2026-08-20._

- [A Rust supply-chain compromise used Cargo's own yank warning to trick developers](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) (2026-08-20)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### ▫️ quiet sha-pinning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-12 · latest 2026-09-24._

- [Mini Shai-Hulud still spreads four months on via hijacked actions-cool/issues-helper tags](https://safedep.io/mini-shai-hulud-reinfection-github-repositories) (2026-09-24)
- [Org-wide GitHub Actions SHA-pinning enforcement has non-obvious failure modes](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide) (2026-08-12)

### ▫️ quiet sigstore  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-04 · latest 2026-08-06._

- [ChainDrop self-propagating npm worm mints valid Sigstore provenance, exfiltrates via Ethereum-routed C2](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) (2026-08-06)
- [ChainDrop supply chain compromise: Anatomy of a self-propagating worm](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/) (2026-08-04)

### ▫️ quiet symlink  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-09 · latest 2026-08-07._

- [go-git worktree wrapper vetoed dangerous strings but still followed symlinks](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm) (2026-08-07)
- [Wiz 'GhostApproval': git symlinks let AI coding assistants write outside the workspace](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09)

## AI Research

### 🔺 rising evals  ·  24 findings (7 recent vs 2.8 expected) · 12 sources
_First seen 2023-12-07 · latest 2026-10-27._

- [Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://huggingface.co/blog/allenai/novelty-bench) (2026-10-27) · _latest_
- [Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193) (2026-10-27) · _latest_
- [Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges) (2026-10-27) · _latest_
- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) (2026-10-19) · _latest_
- [POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_

### 🔺 rising llm-as-judge  ·  5 findings (3 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-07 · latest 2026-10-27._

- [Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://huggingface.co/blog/allenai/novelty-bench) (2026-10-27) · _latest_
- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [RobustReview finds LLM paper reviewers change scores on content-preserving rewrites](https://arxiv.org/abs/2609.39027) (2026-09-30) · _latest_
- [MentalHealthBench scores model replies against weighted expert-consensus rubrics](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [SkillTV-Bench: Benchmarking How Well Judges Perform on Skill-Augmented Agentic Execution](https://arxiv.org/abs/2608.05573) (2026-08-07)

### 🔺 rising coding-agents  ·  7 findings (3 recent vs 0.7 expected) · 6 sources
_First seen 2026-07-21 · latest 2026-10-27._

- [A Thomson Reuters engineer runs a coding agent fully offline with Qwen](https://latent.space/p/offline-coding/) (2026-10-27) · _latest_
- [SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench) (2026-10-26) · _latest_
- [pi pod runs the pi coding agent in isolated sandboxes](https://pipod.dev/) (2026-10-02) · _latest_
- [HarnessTax finds harness choice barely moved success but changed cost](https://harnesstax.github.io/) (2026-09-16)
- [Explicit Edit Benchmark offers 226 byte-exact file-editing tasks for comparing coding agents](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)
- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)

### 🔺 rising benchmarks  ·  9 findings (3 recent vs 1.0 expected) · 7 sources
_First seen 2026-07-09 · latest 2026-10-27._

- [Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges) (2026-10-27) · _latest_
- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_
- ["LLM Agent Performance" Is Not a Single Evaluation Target](https://arxiv.org/abs/2602.03238) (2026-08-10)
- [A real-world benchmark evaluates investment logic in large language models](https://arxiv.org/abs/2608.06108) (2026-08-07)
- [GAUGE benchmarks physical fidelity in simulation engines and video world models](https://arxiv.org/abs/2608.05948) (2026-08-07)

### 🔺 rising self-hosted-agents  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-15 · latest 2026-10-27._

- [A Thomson Reuters engineer runs a coding agent fully offline with Qwen](https://latent.space/p/offline-coding/) (2026-10-27) · _latest_
- [MLX tensor parallelism over Thunderbolt serves a mixture-of-experts model on Mac Studios](https://machinelearning.apple.com/research/mlx-distributed-inference) (2026-10-15) · _latest_

### 🔺 rising third-party-evaluation  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-20 · latest 2026-10-20._

- [Anthropic embeds METR with employee-like access but controls what is redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators) (2026-10-20) · _latest_
- [Amazon Science covers third-party review of AI safety testing, body not captured](https://www.amazon.science/blog/strengthening-ai-safety-evaluation-through-independent-third-party-review) (2026-10-20) · _latest_

### 🔺 rising vendor-announcement  ·  2 findings (2 recent vs 0.0 expected) · 2 sources
_First seen 2026-10-27 · latest 2026-10-27._

- [Anthropic reports early results from Claude-driven drug development partnerships](https://www.anthropic.com/research/early-progress-drug-development) (2026-10-27) · _latest_
- [Anthropic expands its GSA deal to discount Claude for governments](https://www.anthropic.com/news/expanding-partnership-gsa) (2026-10-27) · _latest_

### 🔺 rising governance  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-22._

- [Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) (2026-10-22) · _latest_
- [Anthropic embeds METR with employee-like access but controls what is redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators) (2026-10-20) · _latest_
- [Birfy/agentdescent](https://github.com/Birfy/agentdescent) (2026-08-10)

### 🔺 rising human-in-the-loop  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-16._

- [Google's VERID checks agent-written lab-robot protocols against a 3D digital twin](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/) (2026-10-16) · _latest_
- [Anthropic physicist's BootLoops: Claude agents did checkable science with expert steering](https://www.anthropic.com/research/claude-shaped-science) (2026-10-01) · _latest_
- [Adaptive Arena-based Contestable Argumentative Network-of-Experts for Open-Ended Care Plan Coordination](https://arxiv.org/abs/2608.05391) (2026-08-07)

### 🔺 rising long-running-agents  ·  3 findings (2 recent vs 0.2 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-10-16._

- [Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/) (2026-10-16) · _latest_
- [Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents) (2026-10-12) · _latest_
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### 🔺 rising grpo  ·  4 findings (2 recent vs 0.3 expected) · 4 sources
_First seen 2026-08-10 · latest 2026-10-26._

- [Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models) (2026-10-26) · _latest_
- [GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227) (2026-10-19) · _latest_
- [CreativeInstruct teaches LLMs to balance quality, creativity, and diversity](https://arxiv.org/abs/2608.07460) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)

### 🔺 rising survey  ·  4 findings (2 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-27._

- [Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193) (2026-10-27) · _latest_
- [Anthropic staff, unlike most US adults, expect Nobel-level AI discovery by 2030](https://www.anthropic.com/research/ai-expectations-gap) (2026-10-16) · _latest_
- [Survey of adversarial attacks that degrade Vision Transformer efficiency](https://arxiv.org/abs/2608.05217) (2026-08-07)
- [When Agentic AI Meets Integrated Sensing and Communication](https://arxiv.org/abs/2608.05792) (2026-08-07)

### 🔺 rising red-teaming  ·  6 findings (2 recent vs 0.5 expected) · 6 sources
_First seen 2025-03-13 · latest 2026-10-20._

- [METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/) (2026-10-20) · _latest_
- [Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access](https://www.anthropic.com/news/accenture-embedded-evaluation) (2026-10-19) · _latest_
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439) (2026-08-27)
- [Enhancing AI security through global AI red teaming](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/) (2026-07-27)
- [Rogue agents are not unprecedented, ~20% of ProjectDiscovery's CTF solves were unintended](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22)
- [Blind teams hunt a hidden objective planted in a model](https://www.anthropic.com/research/auditing-hidden-objectives) (2025-03-13)

### 🔺 rising benchmark  ·  21 findings (4 recent vs 2.9 expected) · 9 sources
_First seen 2026-05 · latest 2026-10-27._

- [Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://huggingface.co/blog/allenai/novelty-bench) (2026-10-27) · _latest_
- [PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1) (2026-10-27) · _latest_
- [SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench) (2026-10-26) · _latest_
- [RobustReview finds LLM paper reviewers change scores on content-preserving rewrites](https://arxiv.org/abs/2609.39027) (2026-09-30) · _latest_
- [MentalHealthBench scores model replies against weighted expert-consensus rubrics](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [UK AISI publishes verified benchmark results showing scores shift with inference compute](https://huggingface.co/blog/evaleval-aisi) (2026-09-22)

### 🔺 rising calibration  ·  7 findings (2 recent vs 0.9 expected) · 4 sources
_First seen 2026-08-10 · latest 2026-10-27._

- [PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1) (2026-10-27) · _latest_
- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [Ask-E: An Environment for Calibrated Question Generation](https://arxiv.org/abs/2608.06933) (2026-08-10)
- [Pre-Inference Routing for Cost-Efficient Document Field Extraction](https://arxiv.org/abs/2608.06607) (2026-08-10)
- [Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration](https://arxiv.org/abs/2605.27752) (2026-08-10)
- [Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183) (2026-08-10)

### 🔺 rising claude-code  ·  7 findings (2 recent vs 0.9 expected) · 6 sources
_First seen 2026-06 · latest 2026-10-16._

- [Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/) (2026-10-16) · _latest_
- [Anthropic physicist's BootLoops: Claude agents did checkable science with expert steering](https://www.anthropic.com/research/claude-shaped-science) (2026-10-01) · _latest_
- [OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557) (2026-08-10)
- [Claude Code and Opus 4.6 pipeline finds a real Linux sandbox-escape CVE](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/) (2026-07-30)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04)

### 🔺 rising evaluation  ·  10 findings (2 recent vs 1.4 expected) · 4 sources
_First seen 2026-08-06 · latest 2026-10-26._

- [Simon Willison's Claude-run review finds webframe fast but rough for scraping](https://simonwillison.net/2026/Oct/26/webframe-evaluation/) (2026-10-26) · _latest_
- [Hugging Face launches an Open TTS Leaderboard ranking open text-to-speech models](https://huggingface.co/blog/open-tts-leaderboard) (2026-09-30) · _latest_
- [Zero gap does not mean a contaminated model is restored](https://arxiv.org/abs/2608.07341) (2026-08-10)
- [Rethinking Evaluation Paradigms in IBP-based Certified Training](https://arxiv.org/abs/2606.02134) (2026-08-10)
- [Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration](https://arxiv.org/abs/2605.27752) (2026-08-10)
- [SenWorld: A Digital-Twin Simulation for Generating Context-Rich Evaluation Data](https://arxiv.org/abs/2607.19949) (2026-08-10)

### ▪️ steady agents  ·  25 findings (2 recent vs 4.0 expected) · 9 sources
_First seen 2026-05 · latest 2026-10-27._

- [Anthropic reports early results from Claude-driven drug development partnerships](https://www.anthropic.com/research/early-progress-drug-development) (2026-10-27) · _latest_
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) (2026-10-19) · _latest_
- [Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?](https://arxiv.org/abs/2605.22148) (2026-08-10)
- [OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557) (2026-08-10)
- [Can AI agents conduct open-ended AI research? Evidence from two case studies](https://arxiv.org/abs/2607.27191) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)

### ▪️ steady multi-agent  ·  13 findings (1 recent vs 2.1 expected) · 5 sources
_First seen 2026-08-07 · latest 2026-10-19._

- [GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227) (2026-10-19) · _latest_
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [Multi-Agent Forensic Reasoning for Generalizable Deepfake Video Detection](https://arxiv.org/abs/2608.06865) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)
- [Scalable Long-Horizon Planning with Staggered Updates for Lifelong MAPF](https://arxiv.org/abs/2608.06702) (2026-08-10)
- [PHOENIX uses multi-agent AI for predictive self-healing of satellites](https://arxiv.org/abs/2608.07126) (2026-08-10)

### ▪️ steady harness  ·  11 findings (1 recent vs 1.7 expected) · 10 sources
_First seen 2026-05 · latest 2026-10-27._

- [Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges) (2026-10-27) · _latest_
- [HarnessTax finds harness choice barely moved success but changed cost](https://harnesstax.github.io/) (2026-09-16)
- [Explicit Edit Benchmark offers 226 byte-exact file-editing tasks for comparing coding agents](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)
- ["LLM Agent Performance" Is Not a Single Evaluation Target](https://arxiv.org/abs/2602.03238) (2026-08-10)
- [LLM 0.32 adds reasoning traces and human-approval pause/resume](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) (2026-08-04)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### ▪️ steady agent-harness  ·  8 findings (1 recent vs 1.2 expected) · 4 sources
_First seen 2026-07-28 · latest 2026-10-01._

- [Anthropic physicist's BootLoops: Claude agents did checkable science with expert steering](https://www.anthropic.com/research/claude-shaped-science) (2026-10-01) · _latest_
- [Fzkuji/OpenProgram](https://github.com/Fzkuji/OpenProgram) (2026-08-10)
- [aeonfun/aeon](https://github.com/aeonfun/aeon) (2026-08-10)
- [wanmol/goal-flow](https://github.com/wanmol/goal-flow) (2026-08-10)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](https://arxiv.org/abs/2608.06811) (2026-08-10)
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)

### ▪️ steady robotics  ·  6 findings (1 recent vs 0.9 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-20._

- [RoboCasa-Shift shows equal success-rate drops in a VLA policy hide different failures](https://arxiv.org/abs/2610.27861) (2026-10-20) · _latest_
- [Scalable Long-Horizon Planning with Staggered Updates for Lifelong MAPF](https://arxiv.org/abs/2608.06702) (2026-08-10)
- [ODEWorld: A Continuous Predictive Architecture via Physical-Time Flow](https://arxiv.org/abs/2607.27924) (2026-08-10)
- [Fast and Accurate: An Adaptive VLA Inference Framework through Environment-aware Model Selection](https://arxiv.org/abs/2608.06434) (2026-08-10)
- [Representation Handoffs for OpenArm-Based Laboratory Mobile Manipulation](https://arxiv.org/abs/2608.07154) (2026-08-10)
- [Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317) (2026-08-10)

### ▪️ steady harness-design  ·  5 findings (1 recent vs 0.7 expected) · 4 sources
_First seen 2026-07-21 · latest 2026-10-25._

- [Daniel Miessler argues harnesses should describe what you want, not steps](https://danielmiessler.com/blog/models-how-harnesses-what) (2026-10-25) · _latest_
- [Birfy/agentdescent](https://github.com/Birfy/agentdescent) (2026-08-10)
- [Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding](https://arxiv.org/abs/2608.05876) (2026-08-07)
- [VLMs for Videogame Data Annotation](https://arxiv.org/abs/2608.05949) (2026-08-07)
- [How the Claude Code team designs its harness, tools and evals](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▪️ steady tool-use  ·  5 findings (1 recent vs 0.7 expected) · 3 sources
_First seen 2026-07-04 · latest 2026-10-18._

- [HybridAgent reasons in latent space and calls tools in text](https://arxiv.org/abs/2610.18861) (2026-10-18) · _latest_
- [PULSE uses an LLM agent with passive sensing for cancer survivorship](https://arxiv.org/abs/2605.17679) (2026-08-10)
- [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-07)
- [LLM 0.32 adds reasoning traces and human-approval pause/resume](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) (2026-08-04)
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04)

### ▪️ steady vlm  ·  5 findings (1 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-19._

- [POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964) (2026-10-19) · _latest_
- [SABRE: Scalable and Automated Benchmarking of VLMs under Stress](https://arxiv.org/abs/2608.07435) (2026-08-10)
- [Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054) (2026-08-10)
- [MultiView-Bench: A Diagnostic Benchmark for World-Centric Multi-View Integration in VLMs](https://arxiv.org/abs/2607.08970) (2026-08-10)
- [VLMs for Videogame Data Annotation](https://arxiv.org/abs/2608.05949) (2026-08-07)

### ▪️ steady compaction  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-10-12._

- [Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents) (2026-10-12) · _latest_
- [OpenAI sets up fast-track misalignment disclosure and publishes six first reports](https://openai.com/index/model-misalignment-reporting-framework) (2026-09-16)
- [OpenAI launches the Agents API in public beta, a hosted Codex harness](https://openai.com/index/introducing-the-agents-api) (2026-09-10)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### ▪️ steady multilingual  ·  4 findings (1 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-27 · latest 2026-09-30._

- [Hugging Face launches an Open TTS Leaderboard ranking open text-to-speech models](https://huggingface.co/blog/open-tts-leaderboard) (2026-09-30) · _latest_
- [Multi-Legal-Bench evaluates LLMs on legal reasoning across jurisdictions and languages](https://arxiv.org/abs/2605.29738) (2026-08-10)
- [An Agentic Hybrid Top-Down and Bottom-Up Approach to Knowledge Graph Generation](https://arxiv.org/abs/2608.07023) (2026-08-10)
- [Enhancing AI security through global AI red teaming](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/) (2026-07-27)

### ▪️ steady self-improvement  ·  4 findings (1 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-27._

- [Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193) (2026-10-27) · _latest_
- [Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?](https://arxiv.org/abs/2605.22148) (2026-08-10)
- [Search2Skill: Skill Distillation Beyond Knowledge Boundaries Via Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2608.05245) (2026-08-07)
- [SkillHEX: Improving Agent Skills via Hypothesis-Driven Autonomous Exploration and Exploitation](https://arxiv.org/abs/2608.05628) (2026-08-07)

### ▪️ steady agent-skills  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-22._

- [Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) (2026-10-22) · _latest_
- [Trail of Bits says 1Password's AI patching benchmark is misleading](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/) (2026-09-15)
- [SkillHEX: Improving Agent Skills via Hypothesis-Driven Autonomous Exploration and Exploitation](https://arxiv.org/abs/2608.05628) (2026-08-07)

### ▪️ steady context-management  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-21 · latest 2026-10-12._

- [Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents) (2026-10-12) · _latest_
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)
- [How the Claude Code team designs its harness, tools and evals](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▪️ steady cot-monitoring  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-20._

- [OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/) (2026-10-20) · _latest_
- [Counterfactual Simulation Training for Chain-of-Thought Faithfulness](https://arxiv.org/abs/2602.20710) (2026-08-10)
- [OpenAI's Astra preliminary evals can't rule out 'Critical' cyber capability](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities) (2026-08-07)

### ▪️ steady digital-twin  ·  3 findings (1 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-16._

- [Google's VERID checks agent-written lab-robot protocols against a 3D digital twin](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/) (2026-10-16) · _latest_
- [SenWorld: A Digital-Twin Simulation for Generating Context-Rich Evaluation Data](https://arxiv.org/abs/2607.19949) (2026-08-10)
- [Physics-inspired neural network models cortical dynamics from brain-computer-interface EEG](https://arxiv.org/abs/2607.10439) (2026-08-10)

### ▪️ steady guardrails  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-09 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)

### ▪️ steady mcp  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-10-22._

- [Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) (2026-10-22) · _latest_
- [universal-tool-calling-protocol/utcp-specification](https://github.com/universal-tool-calling-protocol/utcp-specification) (2026-08-09)
- [CASCADE: An Agentic Regulatory Network Framework for Patient-Data-Validated Downstream Perturbation Prediction](https://arxiv.org/abs/2608.05359) (2026-08-07)

### ▪️ steady orchestration  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-06 · latest 2026-10-16._

- [Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/) (2026-10-16) · _latest_
- [OrchestraBench evaluates multi-agent orchestration failures and recovery](https://arxiv.org/abs/2608.05263) (2026-08-07)
- [Omnigent is an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent) (2026-06)

### ▪️ steady rlvr  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-08 · latest 2026-10-26._

- [Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models) (2026-10-26) · _latest_
- [Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208) (2026-08-10)
- [Willison: OpenAI/Hugging Face 'accidental attack' happened in RLVR training, not deployment](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything) (2026-08-08)

### ▪️ steady subagents  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-07-21 · latest 2026-10-16._

- [Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/) (2026-10-16) · _latest_
- [OpenAI launches the Agents API in public beta, a hosted Codex harness](https://openai.com/index/introducing-the-agents-api) (2026-09-10)
- [How the Claude Code team designs its harness, tools and evals](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▪️ steady swe-bench  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-10-26._

- [SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench) (2026-10-26) · _latest_
- [HarnessTax finds harness choice barely moved success but changed cost](https://harnesstax.github.io/) (2026-09-16)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](https://arxiv.org/abs/2608.06811) (2026-08-10)

### ▪️ steady vllm  ·  3 findings (1 recent vs 0.3 expected) · 3 sources
_First seen 2026-08-06 · latest 2026-10-26._

- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [Cascade uses SLO-aware latency budgets for fair LLM inference serving](https://arxiv.org/abs/2608.06557) (2026-08-10)
- [vLLM anatomy explains paged attention and continuous batching for high-throughput serving](https://www.aleksagordic.com/blog/vllm) (2026-08-06)

### ▪️ steady chain-of-thought  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-14._

- [METR proposes third-party review of unreleased models by mining internal transcripts](https://metr.org/blog/2026-10-14-alignment-assessment-proposal/) (2026-10-14) · _latest_
- [Stochastic Autoregressive Learning](https://arxiv.org/abs/2608.07224) (2026-08-10)

### ▪️ steady constrained-decoding  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-26._

- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [Seeing Is Not Deciding: Can Multimodal LLMs Act as Effective CEOs?](https://arxiv.org/abs/2608.05864) (2026-08-07)

### ▪️ steady context-engineering  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-10-25._

- [Daniel Miessler argues harnesses should describe what you want, not steps](https://danielmiessler.com/blog/models-how-harnesses-what) (2026-10-25) · _latest_
- [ratel-ai/ratel](https://github.com/ratel-ai/ratel) (2026-08-09)

### ▪️ steady credit-assignment  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-19._

- [GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227) (2026-10-19) · _latest_
- [Trajectory-Relative Hindsight Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.07371) (2026-08-10)

### ▪️ steady distillation  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-26._

- [Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models) (2026-10-26) · _latest_
- [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-07)

### ▪️ steady eval-methodology  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-20._

- [OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/) (2026-10-20) · _latest_
- [GAUGE benchmarks physical fidelity in simulation engines and video world models](https://arxiv.org/abs/2608.05948) (2026-08-07)

### ▪️ steady foundation-models  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-27._

- [PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1) (2026-10-27) · _latest_
- [Large Causal Models for Temporal Causal Discovery](https://arxiv.org/abs/2602.18662) (2026-08-10)

### ▪️ steady latency  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-30._

- [Hugging Face launches an Open TTS Leaderboard ranking open text-to-speech models](https://huggingface.co/blog/open-tts-leaderboard) (2026-09-30) · _latest_
- [Hybrid analytical and machine-learning predictors model LLM inference latency and energy](https://arxiv.org/abs/2608.06723) (2026-08-10)

### ▪️ steady leaderboard  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-11 · latest 2026-09-30._

- [Hugging Face launches an Open TTS Leaderboard ranking open text-to-speech models](https://huggingface.co/blog/open-tts-leaderboard) (2026-09-30) · _latest_
- [Explicit Edit Benchmark offers 226 byte-exact file-editing tasks for comparing coding agents](https://github.com/alexshpunt/explicit-edit-benchmark) (2026-09-11)

### ▪️ steady local-inference  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-15._

- [MLX tensor parallelism over Thunderbolt serves a mixture-of-experts model on Mac Studios](https://machinelearning.apple.com/research/mlx-distributed-inference) (2026-10-15) · _latest_
- [Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885) (2026-08-10)

### ▪️ steady long-horizon-tasks  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-22 · latest 2026-10-20._

- [RoboCasa-Shift shows equal success-rate drops in a VLA policy hide different failures](https://arxiv.org/abs/2610.27861) (2026-10-20) · _latest_
- [METR calls Claude Opus a modest AI R&D gain over Fable](https://metr.org/blog/2026-09-22-claude-opus-5-5/) (2026-09-22)

### ▪️ steady medical-ml  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-27._

- [PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1) (2026-10-27) · _latest_
- [A foundation-model approach to pediatric headache classification from rs-fMRI](https://arxiv.org/abs/2608.07287) (2026-08-10)

### ▪️ steady misalignment  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-16 · latest 2026-10-20._

- [METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/) (2026-10-20) · _latest_
- [OpenAI sets up fast-track misalignment disclosure and publishes six first reports](https://openai.com/index/model-misalignment-reporting-framework) (2026-09-16)

### ▪️ steady open-weights  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-26._

- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) (2026-08-10)

### ▪️ steady post-training  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-18._

- [HybridAgent reasons in latent space and calls tools in text](https://arxiv.org/abs/2610.18861) (2026-10-18) · _latest_
- [CreativeInstruct teaches LLMs to balance quality, creativity, and diversity](https://arxiv.org/abs/2608.07460) (2026-08-10)

### ▪️ steady routing  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-20._

- [DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522) (2026-10-20) · _latest_
- [OrchestraBench evaluates multi-agent orchestration failures and recovery](https://arxiv.org/abs/2608.05263) (2026-08-07)

### ▪️ steady sandbox  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-10 · latest 2026-10-26._

- [Simon Willison's Claude-run review finds webframe fast but rough for scraping](https://simonwillison.net/2026/Oct/26/webframe-evaluation/) (2026-10-26) · _latest_
- [OpenAI launches the Agents API in public beta, a hosted Codex harness](https://openai.com/index/introducing-the-agents-api) (2026-09-10)

### ▪️ steady scientific-agents  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-10-16._

- [Google's VERID checks agent-written lab-robot protocols against a 3D digital twin](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/) (2026-10-16) · _latest_
- [CASCADE: An Agentic Regulatory Network Framework for Patient-Data-Validated Downstream Perturbation Prediction](https://arxiv.org/abs/2608.05359) (2026-08-07)

### ▪️ steady self-improving-agents  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-10-19._

- [GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227) (2026-10-19) · _latest_
- [Birfy/agentdescent](https://github.com/Birfy/agentdescent) (2026-08-10)

### ▪️ steady serving  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-10-26._

- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [vLLM anatomy explains paged attention and continuous batching for high-throughput serving](https://www.aleksagordic.com/blog/vllm) (2026-08-06)

### ▪️ steady skill-evolution  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-27 · latest 2026-10-19._

- [GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227) (2026-10-19) · _latest_
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439) (2026-08-27)

### ▪️ steady third-party-evals  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-09-22 · latest 2026-10-19._

- [Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access](https://www.anthropic.com/news/accenture-embedded-evaluation) (2026-10-19) · _latest_
- [METR calls Claude Opus a modest AI R&D gain over Fable](https://metr.org/blog/2026-09-22-claude-opus-5-5/) (2026-09-22)

### ▪️ steady tool-calling  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-10-26._

- [Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm) (2026-10-26) · _latest_
- [universal-tool-calling-protocol/utcp-specification](https://github.com/universal-tool-calling-protocol/utcp-specification) (2026-08-09)

### ▪️ steady verification  ·  2 findings (1 recent vs 0.2 expected) · 2 sources
_First seen 2026-07-28 · latest 2026-10-01._

- [Anthropic physicist's BootLoops: Claude agents did checkable science with expert steering](https://www.anthropic.com/research/claude-shaped-science) (2026-10-01) · _latest_
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)

### ▫️ quiet llm  ·  9 findings (0 recent vs 1.6 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [CubicQuant: parametric non-uniform codebooks for high-throughput LLM inference, 1-8-Bit weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [Intrinsic bias mitigation in LLMs can improve downstream fairness](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Solver-Guided Reasoning for Mixed-Equilibrium Strategies](https://arxiv.org/abs/2608.06741) (2026-08-10)
- [Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)
- [SCALE: Scientific Concept Aggregation via LLMs and Embeddings for Fine-Grained Taxonomy Extension](https://arxiv.org/abs/2608.07254) (2026-08-10)

### ▫️ quiet rag  ·  9 findings (0 recent vs 1.6 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [Hugging Face's funes shares agent memory from raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization](https://arxiv.org/abs/2602.12187) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [GPTKB lets you browse, query, and audit an LLM-derived knowledge base](https://arxiv.org/abs/2608.06992) (2026-08-10)
- [Agentic self-driving microscopy benchmarks do not necessarily generalize to unseen tasks](https://arxiv.org/abs/2608.05266) (2026-08-07)

### ▫️ quiet interpretability  ·  8 findings (0 recent vs 1.2 expected) · 3 sources
_First seen 2025-03-13 · latest 2026-08-10._

- [Concept vectors and linear probes measure ESG content from LLM activations](https://arxiv.org/abs/2608.07208) (2026-08-10)
- [Symbolic patterns emerge in artificial neural networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [Aphasic picture naming errors reveal lesion parameters in large language models](https://arxiv.org/abs/2608.06429) (2026-08-10)
- [Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054) (2026-08-10)
- [Geo-Spatial Concept Probing tests how large language models handle spatial concepts](https://arxiv.org/abs/2608.07353) (2026-08-10)
- [Understanding Differentiable Embeddings Through Differential and Integral Geometry](https://arxiv.org/abs/2608.06809) (2026-08-10)

### ▫️ quiet kv-cache  ·  8 findings (0 recent vs 1.4 expected) · 3 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](https://arxiv.org/abs/2607.20457) (2026-08-10)
- [Global allocation of resolution and coverage improves KV cache compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Topology-Aware Data Movement for Disaggregated GPU Inference](https://arxiv.org/abs/2607.28633) (2026-08-10)
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968) (2026-08-10)

### ▫️ quiet reinforcement-learning  ·  8 findings (0 recent vs 1.4 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Approximate nearest neighbors give sub-quadratic bisimulation metrics](https://arxiv.org/abs/2608.06762) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [Aftab benchmarks CNN encoders and value functions in parallelized Q-Networks](https://arxiv.org/abs/2608.07335) (2026-08-10)
- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Beyond Isolation: Unlocking Reinforcement Learning Component Synergy for Sample-Efficient Continuous Control](https://arxiv.org/abs/2608.07086) (2026-08-10)
- [Wasserstein Policy Gradient for Entropy-Regularized Linear-Quadratic Control](https://arxiv.org/abs/2608.07433) (2026-08-10)

### ▫️ quiet long-context  ·  7 findings (0 recent vs 1.2 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) (2026-08-10)
- [Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](https://arxiv.org/abs/2607.20457) (2026-08-10)
- [Global allocation of resolution and coverage improves KV cache compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849) (2026-08-10)
- [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458) (2026-08-10)
- [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515) (2026-08-10)

### ▫️ quiet multimodal  ·  7 findings (0 recent vs 1.2 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Text-anchored cross-modal transfer debiases visual counter-commonsense reasoning](https://arxiv.org/abs/2608.06938) (2026-08-10)
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
- [Dual-node NVIDIA DGX Spark over Tailscale is a remote-access LLM training testbed](https://arxiv.org/abs/2608.07226) (2026-08-10)
- [LoCA: Spatially-Aware Low-Rank Convolutional Adaptation of Vision Foundation Models](https://arxiv.org/abs/2607.06918) (2026-08-10)
- [Improving Attributed Long-form Question Answering with Intent Awareness](https://arxiv.org/abs/2603.27435) (2026-08-10)
- [Hyper-ES: Effective Evolution Strategies for LLM Reasoning via Descent Direction Merging](https://arxiv.org/abs/2608.05541) (2026-08-07)

### ▫️ quiet medical-imaging  ·  5 findings (0 recent vs 0.9 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [H2AL: Hyperbolic Hierarchy-aware Aggregative Learning for Registration-based Few-shot Medical Image Segmentation](https://arxiv.org/abs/2608.07340) (2026-08-10)
- [FedDOSE federated learning framework models brain dynamic functional connectivity](https://arxiv.org/abs/2608.07393) (2026-08-10)
- [Machine Learning-Based Inter-Crystal Scatter Recovery for Ultra-High Resolution PET Imaging](https://arxiv.org/abs/2608.07155) (2026-08-10)
- [International Transfer of Stochastic Cortical Self-Reconstruction](https://arxiv.org/abs/2608.07092) (2026-08-10)
- [Representation-driven Endoscopic Visual Embedding Alignment for Latent Generation](https://arxiv.org/abs/2608.07176) (2026-08-10)

### ▫️ quiet mllm  ·  5 findings (0 recent vs 0.9 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Multi-Agent Forensic Reasoning for Generalizable Deepfake Video Detection](https://arxiv.org/abs/2608.06865) (2026-08-10)
- [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088) (2026-08-10)
- [An AI4AI Framework for Visual Token Pruning](https://arxiv.org/abs/2608.07193) (2026-08-10)
- [Sharing cross-page context beats per-page transcription for multi-page handwritten documents](https://arxiv.org/abs/2502.20295) (2026-08-10)
- [Unified Agent: Managing Interactions across Devices](https://arxiv.org/abs/2608.05729) (2026-08-07)

### ▫️ quiet prompt-engineering  ·  5 findings (0 recent vs 0.9 expected) · 3 sources
_First seen 2026-07-28 · latest 2026-08-10._

- [In-Context Examples Suppress Scientific Knowledge Recall in LLMs](https://arxiv.org/abs/2604.27540) (2026-08-10)
- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)
- [A randomized audit tests survey-country metadata in LLM social inference](https://arxiv.org/abs/2608.06085) (2026-08-07)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)
- [How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/) (2026-07-28)

### ▫️ quiet counterfactual  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Aphasic picture naming errors reveal lesion parameters in large language models](https://arxiv.org/abs/2608.06429) (2026-08-10)
- [Poli-Bias: Understanding and Measuring Large Language Model Biases in International Political Conflicts](https://arxiv.org/abs/2608.06123) (2026-08-07)
- [C3PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models](https://arxiv.org/abs/2608.05381) (2026-08-07)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)

### ▫️ quiet edge-ai  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885) (2026-08-10)
- [MiCoPro: End-to-End Mixed Precision HW/SW Co-design with HW-aware Proxy Model](https://arxiv.org/abs/2608.06916) (2026-08-10)
- [Pareto-based framework with LLM guidance picks explainable AI for TinyML devices](https://arxiv.org/abs/2608.07091) (2026-08-10)
- [Synthetic LiDAR data and deterministic downsampling support edge point cloud classification](https://arxiv.org/abs/2608.07106) (2026-08-10)

### ▫️ quiet embeddings  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [ZCA whitening calibrates WEAT against anisotropy in embedding bias tests](https://arxiv.org/abs/2608.06908) (2026-08-10)
- [Understanding Differentiable Embeddings Through Differential and Integral Geometry](https://arxiv.org/abs/2608.06809) (2026-08-10)
- [SCALE: Scientific Concept Aggregation via LLMs and Embeddings for Fine-Grained Taxonomy Extension](https://arxiv.org/abs/2608.07254) (2026-08-10)
- [Towards a Theoretical Understanding of Two Tower Recommendation Models](https://arxiv.org/abs/2403.00802) (2026-08-10)

### ▫️ quiet federated-learning  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SSTQ: Privacy-Preserving Vector Quantization via Subsampled Stochastic TurboQuant](https://arxiv.org/abs/2608.05127) (2026-08-10)
- [Theoretical Foundations of Communication-Efficient, Robust, and Practical Distributed and Federated Optimization](https://arxiv.org/abs/2608.06563) (2026-08-10)
- [Capacity Confounds and Coverage Guarantees in Adaptive Sub-model Federated Learning](https://arxiv.org/abs/2608.07157) (2026-08-10)
- [FedDOSE federated learning framework models brain dynamic functional connectivity](https://arxiv.org/abs/2608.07393) (2026-08-10)

### ▫️ quiet healthcare  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [PULSE uses an LLM agent with passive sensing for cancer survivorship](https://arxiv.org/abs/2605.17679) (2026-08-10)
- [LSEAD: A Privacy-Preserving LLM-Based Speech Analysis Framework for Early Alzheimer's Disease Screening](https://arxiv.org/abs/2608.07378) (2026-08-10)
- [A compliance-first agentic architecture for hospital AI systems](https://arxiv.org/abs/2608.06112) (2026-08-07)
- [Guideline-based thresholds for ischaemic stroke outcome prediction keep accuracy in most cohorts](https://arxiv.org/abs/2608.05203) (2026-08-07)

### ▫️ quiet inference  ·  4 findings (0 recent vs 0.7 expected) · 3 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Global allocation of resolution and coverage improves KV cache compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968) (2026-08-10)
- [CubicQuant: parametric non-uniform codebooks for high-throughput LLM inference, 1-8-Bit weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [vLLM anatomy explains paged attention and continuous batching for high-throughput serving](https://www.aleksagordic.com/blog/vllm) (2026-08-06)

### ▫️ quiet llm-agents  ·  4 findings (0 recent vs 0.7 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-27._

- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)
- [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439) (2026-08-27)
- [LLM agents and knowledge graphs predict urban socioeconomic outcomes](https://arxiv.org/abs/2411.00028) (2026-08-10)
- [A systems blueprint proposes economic world models for agentic economies](https://arxiv.org/abs/2608.06020) (2026-08-07)

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

### ▫️ quiet agent-memory  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-07 · latest 2026-09-03._

- [Hugging Face's funes shares agent memory from raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515) (2026-08-10)
- [Activity Frames: Deterministic Screen-Activity Compilation for Agent Memory and Replay](https://arxiv.org/abs/2608.05784) (2026-08-07)

### ▫️ quiet agentic-rl  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) (2026-08-10)
- [Trajectory-Relative Hindsight Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.07371) (2026-08-10)
- [iARCS: Iterative Agentic RL for Controllable 3D Scene Generation](https://arxiv.org/abs/2608.06161) (2026-08-07)

### ▫️ quiet bias  ·  3 findings (0 recent vs 0.3 expected) · 3 sources
_First seen 2023-12-07 · latest 2026-08-10._

- [Intrinsic bias mitigation in LLMs can improve downstream fairness](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Poli-Bias: Understanding and Measuring Large Language Model Biases in International Political Conflicts](https://arxiv.org/abs/2608.06123) (2026-08-07)
- [Anthropic's discrim-eval surfaced discrimination in Claude decision prompts](https://www.anthropic.com/research/evaluating-and-mitigating-discrimination-in-language-model-decisions) (2023-12-07)

### ▫️ quiet codex  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-07-28._

- [How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/) (2026-07-28)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)
- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22)

### ▫️ quiet dataset  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [IceHorizon dataset tests horizon detection in ice-covered maritime environments](https://arxiv.org/abs/2608.07018) (2026-08-10)
- [ArchEGraph: A Large-Scale Graph Dataset for Geometry-Topology-Physics Aligned Building Energy Modeling](https://arxiv.org/abs/2608.06772) (2026-08-10)
- [SignVerse-2M: A Two-Million-Clip Pose-Native Universe of 55+ Sign Languages](https://arxiv.org/abs/2605.01720) (2026-08-10)

### ▫️ quiet efficiency  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885) (2026-08-10)
- [LoCA: Forward-Only LLM Tuning after One-Shot Calibration with Local Credit Assignment](https://arxiv.org/abs/2608.03020) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)

### ▫️ quiet fairness  ·  3 findings (0 recent vs 0.3 expected) · 3 sources
_First seen 2023-12-07 · latest 2026-08-10._

- [ZCA whitening calibrates WEAT against anisotropy in embedding bias tests](https://arxiv.org/abs/2608.06908) (2026-08-10)
- [Intrinsic bias mitigation in LLMs can improve downstream fairness](https://arxiv.org/abs/2509.16462) (2026-08-10)
- [Anthropic's discrim-eval surfaced discrimination in Claude decision prompts](https://www.anthropic.com/research/evaluating-and-mitigating-discrimination-in-language-model-decisions) (2023-12-07)

### ▫️ quiet finance  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853) (2026-08-10)
- [Factor exposures define graph locality for better portfolio diversification](https://arxiv.org/abs/2608.06618) (2026-08-10)
- [Counterfactual Analysis via Large Language Models](https://arxiv.org/abs/2608.05367) (2026-08-07)

### ▫️ quiet generalization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Symbolic patterns emerge in artificial neural networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [Optimization as a Dynamical System: Generative Schedules from Latent ODEs](https://arxiv.org/abs/2509.23052) (2026-08-10)
- [Agentic self-driving microscopy benchmarks do not necessarily generalize to unseen tasks](https://arxiv.org/abs/2608.05266) (2026-08-07)

### ▫️ quiet generative-models  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [How Molecular Generative Models Organize Molecular Identity](https://arxiv.org/abs/2608.06956) (2026-08-10)
- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [Representation-driven Endoscopic Visual Embedding Alignment for Latent Generation](https://arxiv.org/abs/2608.07176) (2026-08-10)

### ▫️ quiet gnn  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-06 · latest 2026-08-10._

- [Physics-inspired neural network models cortical dynamics from brain-computer-interface EEG](https://arxiv.org/abs/2607.10439) (2026-08-10)
- [When GNNs Fail: Quantifying and Overcoming Temporal Correlation Volatility in Time Series](https://arxiv.org/abs/2608.07333) (2026-08-10)
- [SNI-GNN: SmartNIC-Assisted Full-Graph GNN Training with In-Network Embedding Prediction](https://arxiv.org/abs/2608.06441) (2026-08-06)

### ▫️ quiet hallucination  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-16 · latest 2026-08-10._

- [Logit-lens over visual attention detects and mitigates LVLM object hallucination](https://arxiv.org/abs/2608.07302) (2026-08-10)
- [TriQua: Reconciling Granularity and Context in Factuality Evaluation](https://arxiv.org/abs/2608.05228) (2026-08-07)
- [With no capability boundary, models may claim actions they cannot perform](https://arxiv.org/abs/2607.13596) (2026-07-16)

### ▫️ quiet mdp  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Approximate nearest neighbors give sub-quadratic bisimulation metrics](https://arxiv.org/abs/2608.06762) (2026-08-10)
- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Posture and Sustainment Optimization Under Adversarial Uncertainty](https://arxiv.org/abs/2608.05256) (2026-08-07)

### ▫️ quiet position-paper  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Toward a Causal Data Management Ecosystem for Decision Making and Agentic AI](https://arxiv.org/abs/2608.07214) (2026-08-10)
- [Alignment has a Fantasia Problem](https://arxiv.org/abs/2604.21827) (2026-08-10)
- [Agentic Nesting: A New Methodology for Existing Enterprise Application Integration and Services](https://arxiv.org/abs/2608.05159) (2026-08-07)

### ▫️ quiet provenance  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-08-10 · latest 2026-09-03._

- [Hugging Face's funes shares agent memory from raw session text, not summaries](https://huggingface.co/blog/funes) (2026-09-03)
- [Trace-level provenance shows how LLM agents actually get the flag](https://arxiv.org/abs/2608.26237) (2026-08-26)
- [GPTKB lets you browse, query, and audit an LLM-derived knowledge base](https://arxiv.org/abs/2608.06992) (2026-08-10)

### ▫️ quiet quantization  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SSTQ: Privacy-Preserving Vector Quantization via Subsampled Stochastic TurboQuant](https://arxiv.org/abs/2608.05127) (2026-08-10)
- [CubicQuant: parametric non-uniform codebooks for high-throughput LLM inference, 1-8-Bit weights](https://arxiv.org/abs/2608.06763) (2026-08-10)
- [MiCoPro: End-to-End Mixed Precision HW/SW Co-design with HW-aware Proxy Model](https://arxiv.org/abs/2608.06916) (2026-08-10)

### ▫️ quiet reasoning  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Solver-Guided Reasoning for Mixed-Equilibrium Strategies](https://arxiv.org/abs/2608.06741) (2026-08-10)
- [Refining Over Resampling: Test-Time Self-Correction for LLM Reasoning](https://arxiv.org/abs/2608.05643) (2026-08-07)
- [Hyper-ES: Effective Evolution Strategies for LLM Reasoning via Descent Direction Merging](https://arxiv.org/abs/2608.05541) (2026-08-07)

### ▫️ quiet sandboxing  ·  3 findings (0 recent vs 0.5 expected) · 3 sources
_First seen 2026-07-22 · latest 2026-08-10._

- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) (2026-08-10)
- [OpenAI's Astra preliminary evals can't rule out 'Critical' cyber capability](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities) (2026-08-07)
- [Rogue agents are not unprecedented, ~20% of ProjectDiscovery's CTF solves were unintended](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22)

### ▫️ quiet scientific-computing  ·  3 findings (0 recent vs 0.5 expected) · 2 sources
_First seen 2026-07-28 · latest 2026-08-10._

- [Sketch-based regularization enables in situ training of neural compressors for scientific simulations](https://arxiv.org/abs/2511.02659) (2026-08-10)
- [AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986) (2026-08-10)
- [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai) (2026-07-28)

### ▫️ quiet ai-code-security  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-17 · latest 2026-07-22._

- [Kimi K3 code-security eval: matching F1 hides a precision gap](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22)
- [Cyber benchmark audit finds models reason but miss 70% of real IDORs](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17)

### ▫️ quiet benchmark-critique  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-15._

- [Trail of Bits says 1Password's AI patching benchmark is misleading](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/) (2026-09-15)
- [Seeking SOTA: Time-Series Forecasting Must Adopt Taxonomy-Specific Evaluation to Dispel Illusory Gains](https://arxiv.org/abs/2603.15506) (2026-08-10)

### ▫️ quiet benchmarking  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [SABRE: Scalable and Automated Benchmarking of VLMs under Stress](https://arxiv.org/abs/2608.07435) (2026-08-10)
- [Hyperbolic Graph Embedders for Link Prediction and Topology Reconstruction](https://arxiv.org/abs/2608.07029) (2026-08-10)

### ▫️ quiet capability-elicitation  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-08 · latest 2026-08-26._

- [Trace-level provenance shows how LLM agents actually get the flag](https://arxiv.org/abs/2608.26237) (2026-08-26)
- [Willison: OpenAI/Hugging Face 'accidental attack' happened in RLVR training, not deployment](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything) (2026-08-08)

### ▫️ quiet compression  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-08-10._

- [Global allocation of resolution and coverage improves KV cache compression](https://arxiv.org/abs/2608.07001) (2026-08-10)
- [SQLite compressed text-history prototypes](https://simonwillison.net/2026/Aug/9/sqlite-text-history-prototype/#atom-everything) (2026-08-09)

### ▫️ quiet computer-vision  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [IceHorizon dataset tests horizon detection in ice-covered maritime environments](https://arxiv.org/abs/2608.07018) (2026-08-10)
- [MaskFlow folds the edit mask into flow matching for regional image editing](https://arxiv.org/abs/2608.06929) (2026-08-10)

### ▫️ quiet continual-learning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897) (2026-08-10)
- [Sketch-based regularization enables in situ training of neural compressors for scientific simulations](https://arxiv.org/abs/2511.02659) (2026-08-10)

### ▫️ quiet cost  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-09 · latest 2026-09-16._

- [HarnessTax finds harness choice barely moved success but changed cost](https://harnesstax.github.io/) (2026-09-16)
- [GitHub Models is now retired](https://simonwillison.net/2026/Aug/9/github-models-is-now-retired/#atom-everything) (2026-08-09)

### ▫️ quiet cost-optimization  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Pre-Inference Routing for Cost-Efficient Document Field Extraction](https://arxiv.org/abs/2608.06607) (2026-08-10)
- [PDF-to-markdown pipelines are the hidden token chewer inside enterprise AI adoption](https://simonwillison.net/2026/Aug/7/pdfs-are-terrible/) (2026-08-07)

### ▫️ quiet explainability  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Symbolic patterns emerge in artificial neural networks](https://arxiv.org/abs/2608.06839) (2026-08-10)
- [Guideline-based thresholds for ischaemic stroke outcome prediction keep accuracy in most cohorts](https://arxiv.org/abs/2608.05203) (2026-08-07)

### ▫️ quiet flow-matching  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582) (2026-08-10)
- [MaskFlow folds the edit mask into flow matching for regional image editing](https://arxiv.org/abs/2608.06929) (2026-08-10)

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

- [A real-world benchmark evaluates investment logic in large language models](https://arxiv.org/abs/2608.06108) (2026-08-07)
- [Cyber benchmark audit finds models reason but miss 70% of real IDORs](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17)

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

- [Hybrid analytical and machine-learning predictors model LLM inference latency and energy](https://arxiv.org/abs/2608.06723) (2026-08-10)
- [CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM](https://arxiv.org/abs/2504.17584) (2026-08-10)

### ▫️ quiet mechanistic-interpretability  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks on Symmetric Data](https://arxiv.org/abs/2511.09432) (2026-08-10)

### ▫️ quiet mental-health  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-09-23._

- [MentalHealthBench scores model replies against weighted expert-consensus rubrics](https://openai.com/index/introducing-mentalhealthbench) (2026-09-23)
- [Neurai-VN Benchmark standardizes machine learning models for mental health digital phenotyping](https://arxiv.org/abs/2607.25232) (2026-08-10)

### ▫️ quiet multi-turn  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-07._

- [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-07)
- [Hateful visual stories slip past per-image moderation in multi-turn generation](https://arxiv.org/abs/2608.05210) (2026-08-07)

### ▫️ quiet prompt-injection  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-27._

- [When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299) (2026-08-27)
- [How the Claude Code team designs its harness, tools and evals](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet pruning  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088) (2026-08-10)
- [The Sparsity Whisperer](https://arxiv.org/abs/2608.06630) (2026-08-10)

### ▫️ quiet skills  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [aeonfun/aeon](https://github.com/aeonfun/aeon) (2026-08-10)
- [Search2Skill: Skill Distillation Beyond Knowledge Boundaries Via Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2608.05245) (2026-08-07)

### ▫️ quiet statistics  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Robust inference using density-powered Stein operators](https://arxiv.org/abs/2511.03963) (2026-08-10)
- [A primer on optimal transport for causal inference with observational data](https://arxiv.org/abs/2503.07811) (2026-08-10)

### ▫️ quiet synthetic-data  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-07 · latest 2026-08-10._

- [Synthetic LiDAR data and deterministic downsampling support edge point cloud classification](https://arxiv.org/abs/2608.07106) (2026-08-10)
- [iARCS: Iterative Agentic RL for Controllable 3D Scene Generation](https://arxiv.org/abs/2608.06161) (2026-08-07)

### ▫️ quiet system-prompt  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-07-21 · latest 2026-08-09._

- [Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything) (2026-08-09)
- [How the Claude Code team designs its harness, tools and evals](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### ▫️ quiet theory  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545) (2026-08-10)
- [Towards a Theoretical Understanding of Two Tower Recommendation Models](https://arxiv.org/abs/2403.00802) (2026-08-10)

### ▫️ quiet transformers  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [RenderFormer++: Scalable and Physics-Informed Feed-Forward Neural Rendering](https://arxiv.org/abs/2606.30380) (2026-08-10)
- [Simpler LSTM architectures can beat pretrained transformers at parsing low-resource languages](https://arxiv.org/abs/2605.02608) (2026-08-10)

### ▫️ quiet uncertainty  ·  2 findings (0 recent vs 0.3 expected) · 2 sources
_First seen 2026-08-10 · latest 2026-08-10._

- [INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607) (2026-08-10)
- [Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183) (2026-08-10)

---

<sub>Generated by scripts/trends.py on 2026-10-28.</sub>
