# 📈 Emerging Trends

> Rising themes per topic, clustered from tagged findings (live + recent archive). Updated 2026-07-26. A theme needs ≥2 findings from ≥2 sources; **recent activity is weighted highest**.

## AI Security

### 🔺 agent-security  ·  11 findings (6 recent) · 11 sources · momentum 17.0
_First seen 2026-02 · latest 2026-07-24._

- [AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24) · _latest_
- [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986) (2026-07-20) · _latest_
- [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) (2026-07-19) · _latest_
- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15) · _latest_
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30) · _latest_
- [TOCTOU race condition in computer-use agents: the screen changes between screenshot and click](https://embracethered.com/blog/posts/2026/toctou-agent-what-you-click-is-not-what-you-get/) (2026-06-25) · _latest_

### 🔺 prompt-injection  ·  7 findings (4 recent) · 7 sources · momentum 11.0
_First seen 2026-02 · latest 2026-07-21._

- [Salience Induction: steering a multi-hop RAG agent to the wrong answer using only true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21) · _latest_
- [Apple fixed the macOS Terminal ANSI DNS-exfiltration sink used to chain prompt injection](https://embracethered.com/blog/posts/2026/macos-terminal-dillma-dns-exfil-ansi-escape-code-fix/) (2026-07-16) · _latest_
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30) · _latest_
- [TOCTOU race condition in computer-use agents: the screen changes between screenshot and click](https://embracethered.com/blog/posts/2026/toctou-agent-what-you-click-is-not-what-you-get/) (2026-06-25) · _latest_
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)
- [Prompt injection in the wild: Google on the current state](http://security.googleblog.com/2026/04/ai-threats-in-wild-current-state-of.html) (2026-04)

### 🔺 model-supply-chain  ·  5 findings (5 recent) · 5 sources · momentum 10.0
_First seen 2026-06-25 · latest 2026-07-21._

- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21) · _latest_
- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20) · _latest_
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29) · _latest_
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239) (2026-06-28) · _latest_
- [A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25) · _latest_

### 🔺 supply-chain  ·  5 findings (4 recent) · 5 sources · momentum 9.0
_First seen 2026-06-23 · latest 2026-07-24._

- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24) · _latest_
- [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) (2026-07-19) · _latest_
- [Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987) (2026-07-16) · _latest_
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30) · _latest_
- [OpenClaw's ClawHub skill marketplace: an agentic supply-chain attack surface](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) (2026-06-23)

### 🔺 mcp  ·  4 findings (3 recent) · 4 sources · momentum 7.0
_First seen 2026-02 · latest 2026-07-24._

- [AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728) (2026-07-24) · _latest_
- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15) · _latest_
- [Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30) · _latest_
- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)

### 🔺 backdoor  ·  3 findings (3 recent) · 3 sources · momentum 6.0
_First seen 2026-06-25 · latest 2026-07-21._

- [(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550) (2026-07-21) · _latest_
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239) (2026-06-28) · _latest_
- [A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511) (2026-06-25) · _latest_

### 🔺 memory-poisoning  ·  3 findings (2 recent) · 3 sources · momentum 5.0
_First seen 2026-05-14 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20) · _latest_
- [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986) (2026-07-20) · _latest_
- [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) (2026-05-14)

### 🔺 ssrf  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-15 · latest 2026-07-15._

- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15) · _latest_
- [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15) · _latest_

### 🔺 sandbox-escape  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-15 · latest 2026-07-24._

- [AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8) (2026-07-24) · _latest_
- [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) (2026-07-15) · _latest_

### 🔺 huggingface  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-29 · latest 2026-07-20._

- [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) (2026-07-20) · _latest_
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29) · _latest_

### 🔺 threat-modeling  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-16 · latest 2026-07-20._

- [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986) (2026-07-20) · _latest_
- [Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987) (2026-07-16) · _latest_

### 🔺 appsec  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-29 · latest 2026-07-15._

- [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) (2026-07-15) · _latest_
- [Over 970,000 AI-Apps on model hubs measured: thousands leak credentials, some carry embedded backdoors](https://arxiv.org/abs/2606.30373) (2026-06-29) · _latest_

### 🔺 defenses  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-28 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20) · _latest_
- [QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239) (2026-06-28) · _latest_

### 🔺 skill-scanning  ·  2 findings (1 recent) · 2 sources · momentum 3.0
_First seen 2026-06-23 · latest 2026-07-16._

- [Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987) (2026-07-16) · _latest_
- [OpenClaw's ClawHub skill marketplace: an agentic supply-chain attack surface](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) (2026-06-23)

### 🔺 llm-security  ·  2 findings (1 recent) · 2 sources · momentum 3.0
_First seen 2026-02 · latest 2026-07-20._

- [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) (2026-07-20) · _latest_
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

### 🔺 agents  ·  2 findings (1 recent) · 2 sources · momentum 3.0
_First seen 2000-01-01 · latest 2026-07-21._

- [Salience Induction: steering a multi-hop RAG agent to the wrong answer using only true statements and no instructions](https://arxiv.org/abs/2607.17535) (2026-07-21) · _latest_
- [stale](https://a/stale) (2000-01-01)

### ▪️ tooling-2026  ·  2 findings (0 recent) · 2 sources · momentum 2.0
_First seen 2026-02 · latest 2026-02._

- [Prismor: a runtime firewall that blocks rogue AI-agent tool calls](https://github.com/PrismorSec/prismor) (2026-02)
- [Augustus: a production LLM vulnerability scanner (210+ probes)](https://github.com/praetorian-inc/augustus) (2026-02)

## Product Security

### 🔺 supply-chain  ·  6 findings (6 recent) · 5 sources · momentum 12.0
_First seen 2026-06-30 · latest 2026-07-24._

- [Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq) (2026-07-24) · _latest_
- [Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr) (2026-07-24) · _latest_
- [38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428) (2026-07-19) · _latest_
- [AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) (2026-07-16) · _latest_
- [Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/) (2026-07-09) · _latest_
- [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) (2026-06-30) · _latest_

### 🔺 phishing  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-30 · latest 2026-07-24._

- [Four stacked evasion techniques hide device-code phishing from scanners: blob URLs, client-side CAPTCHA gates, multi-hop SaaS flows, and source-code confusables](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt) (2026-07-24) · _latest_
- [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) (2026-06-30) · _latest_

### 🔺 unit42  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-30 · latest 2026-07-20._

- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20) · _latest_
- [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) (2026-06-30) · _latest_

### 🔺 malware  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-09 · latest 2026-07-17._

- [TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/) (2026-07-17) · _latest_
- [GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) (2026-07-09) · _latest_

### 🔺 rce  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06-29 · latest 2026-07-24._

- [Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq) (2026-07-24) · _latest_
- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29) · _latest_

### 🔺 command-injection  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-20 · latest 2026-07-24._

- [Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr) (2026-07-24) · _latest_
- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20) · _latest_

### 🔺 memory-safety  ·  2 findings (1 recent) · 2 sources · momentum 3.0
_First seen 2026-04 · latest 2026-06-29._

- [Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) (2026-06-29) · _latest_
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

### 🔺 exploit-chain  ·  2 findings (1 recent) · 2 sources · momentum 3.0
_First seen 2026-05 · latest 2026-07-20._

- [Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/) (2026-07-20) · _latest_
- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)

### ▪️ android  ·  2 findings (0 recent) · 2 sources · momentum 2.0
_First seen 2026-04 · latest 2026-05._

- [Project Zero: a 0-click exploit chain for the Pixel 10](https://projectzero.google/2026/05/pixel-10-exploit.html) (2026-05)
- [Google brings Rust (memory safety) to the Pixel baseband](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html) (2026-04)

## AI Research

### 🔺 agents  ·  7 findings (6 recent) · 6 sources · momentum 13.0
_First seen 2026-05 · latest 2026-07-22._

- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22) · _latest_
- [Protective Capacity Hallucination: given a protective role and no capability boundary, models may claim to have taken actions they cannot perform](https://arxiv.org/abs/2607.13596) (2026-07-16) · _latest_
- [GPT-5.6 (Luna/Terra/Sol): three tiers, 1M context, agentic benchmark claims](https://simonwillison.net/2026/Jul/9/gpt-5-6/#atom-everything) (2026-07-09) · _latest_
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04) · _latest_
- [Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/) (2026-07-02) · _latest_
- [Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent) (2026-06) · _latest_

### 🔺 evals  ·  7 findings (6 recent) · 7 sources · momentum 13.0
_First seen 2026-05 · latest 2026-07-22._

- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22) · _latest_
- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22) · _latest_
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21) · _latest_
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17) · _latest_
- [Protective Capacity Hallucination: given a protective role and no capability boundary, models may claim to have taken actions they cannot perform](https://arxiv.org/abs/2607.13596) (2026-07-16) · _latest_
- [Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/) (2026-07-02) · _latest_

### 🔺 harness  ·  6 findings (5 recent) · 6 sources · momentum 11.0
_First seen 2026-05 · latest 2026-07-22._

- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22) · _latest_
- [Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent) (2026-07-22) · _latest_
- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22) · _latest_
- [Protective Capacity Hallucination: given a protective role and no capability boundary, models may claim to have taken actions they cannot perform](https://arxiv.org/abs/2607.13596) (2026-07-16) · _latest_
- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04) · _latest_
- [PawBench: benchmarking LLM x harness performance](https://github.com/agentscope-ai/PawBench) (2026-05)

### 🔺 benchmarks  ·  3 findings (3 recent) · 3 sources · momentum 6.0
_First seen 2026-07-09 · latest 2026-07-22._

- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22) · _latest_
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17) · _latest_
- [GPT-5.6 (Luna/Terra/Sol): three tiers, 1M context, agentic benchmark claims](https://simonwillison.net/2026/Jul/9/gpt-5-6/#atom-everything) (2026-07-09) · _latest_

### 🔺 claude-code  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-06 · latest 2026-07-04._

- [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything) (2026-07-04) · _latest_
- [Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent) (2026-06) · _latest_

### 🔺 context-management  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-21 · latest 2026-07-22._

- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22) · _latest_
- [How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21) · _latest_

### 🔺 openai  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-09 · latest 2026-07-22._

- [Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction) (2026-07-22) · _latest_
- [GPT-5.6 (Luna/Terra/Sol): three tiers, 1M context, agentic benchmark claims](https://simonwillison.net/2026/Jul/9/gpt-5-6/#atom-everything) (2026-07-09) · _latest_

### 🔺 ai-code-security  ·  2 findings (2 recent) · 2 sources · momentum 4.0
_First seen 2026-07-17 · latest 2026-07-22._

- [Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) (2026-07-22) · _latest_
- [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) (2026-07-17) · _latest_

---

<sub>Generated by scripts/trends.py on 2026-07-26.</sub>
