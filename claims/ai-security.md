# AI Security — standing claims

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_23 current · 1 contested · 0 superseded · 2 refuted · updated 2026-10-28_

[← Claim index](README.md) · [AI Security findings feed](../ai-security/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-pickle-based-model-formats-are-code-execution"></a>

### Loading a pickle model file is arbitrary code execution

`pickle-based-model-formats-are-code-execution` · confidence **0.95** · Model Supply Chain & Theft · standing since Mar 2021

Loading a pickle-based model file (PyTorch .pt/.bin) is equivalent to running arbitrary code; the format has no sandbox and no way to introspect what will execute at load time short of manual reversing.

**Basis —** A structural property of the pickle format itself, documented by the original Trail of Bits exploitation writeup and Hugging Face's own pickle-scanning security docs.

**Do this —** Prefer safetensors for any model you didn't personally train. If you must load pickles, do it in a container with no outbound network.

_Tags: `pickle`, `supply-chain`, `safetensors`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Never a dill moment](https://blog.trailofbits.com/2021/03/15/never-a-dill-moment-exploiting-machine-learning-pickle-files/) | Mar 2021 |
| supports | [Pickle scanning](https://huggingface.co/docs/hub/en/security-pickle) | undated |

</details>

<a id="claim-prompt-injection-is-a-permanent-attack-surface"></a>

### Mixing trusted and untrusted input is permanently exploitable

`prompt-injection-is-a-permanent-attack-surface` · confidence **0.90** · Prompt Injection & Jailbreaks · standing since Feb 2023

LLM applications that mix trusted instructions with untrusted input are permanently vulnerable to instruction hijacking; the surface cannot be closed by prompt engineering alone.

**Basis —** Converging evidence over three years: the original Dual-LLM threat model, an early academic demonstration against production LLM apps, and a 2026 study finding the same hijack pattern across six coding harnesses.

**Do this —** Design agentic systems assuming injection succeeds sometimes: least-privilege tool scopes, human approval on irreversible actions, blast-radius caps that hold even when the model is fooled.

_Tags: `prompt-injection`, `threat-model`, `agents`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Prompt injection: What's the worst that can happen?](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/) | Apr 14, 2023 |
| supports | [Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection](https://arxiv.org/abs/2302.12173) | Feb 23, 2023 |
| supports | [Instruction privilege escalation: harness context assembly promotes untrusted content to a higher instruction level across six coding harnesses](https://arxiv.org/abs/2608.27299) | Aug 27, 2026 |

</details>

<a id="claim-indirect-injection-via-retrieved-content-is-viable"></a>

### Indirect injection via retrieved content is a real vector

`indirect-injection-via-retrieved-content-is-viable` · confidence **0.90** · Prompt Injection & Jailbreaks · standing since Feb 2023

Indirect prompt injection — hostile instructions embedded in documents, web pages, or tool outputs that the LLM reads at run time — is a demonstrated attack vector against real production LLM assistants.

**Basis —** Demonstrated against a real production assistant (GitHub Copilot Chat) plus the original academic paper on indirect injection in LLM-integrated apps.

**Do this —** Treat every retrieval-augmented context as untrusted input. Never let retrieved content unilaterally cause a tool call with side effects.

_Tags: `prompt-injection`, `rag`, `indirect`_

<details><summary>Evidence (6)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Not what you've signed up for](https://arxiv.org/abs/2302.12173) | Feb 23, 2023 |
| supports | [GitHub Copilot Chat: From Prompt Injection to Data Exfiltration](https://embracethered.com/blog/posts/2024/github-copilot-chat-prompt-injection-data-exfiltration/) | Jun 14, 2024 |
| supports | [Breaking Claude Code Opus 5 Auto Mode with indirect prompt injection to code execution](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Aug 26, 2026 |
| supports | [Person Hides Prompt Injection in Legal Filing Telling AI to Side with Them](https://www.404media.co/person-hides-prompt-injection-in-legal-filing-telling-ai-to-side-with-them/) | Aug 13, 2026 |
| supports | [Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109) | Oct 19, 2026 |
| supports | [InceptionRAG: Stealthy Poisoning Attack Against Retrieval-Augmented Generation](http://arxiv.org/abs/2609.16818v1) | Sep 15, 2026 |

</details>

<a id="claim-sandbox-model-deserialization"></a>

### Scanners alone aren't enough — sandbox deserialization too

`sandbox-model-deserialization` · confidence **0.85** · Model Supply Chain & Theft · standing since Jul 20, 2026

Prefer non-executable model formats and sandbox deserialization of any third-party model — a clean scanner result is weak evidence of safety.

**Basis —** A single research disclosure (ShadowPickle) demonstrated pickle-VM import tricks evading ten scanners and four model hubs simultaneously.

**Do this —** Load third-party weights only in a sandbox, prefer safetensors-style non-executable formats, and treat scanner output as one signal rather than an admission gate.

**Replaces** [`model-scanners-are-sufficient-for-supply-chain`](#claim-model-scanners-are-sufficient-for-supply-chain) — Assumed a clean scanner result meant a model was safe

_Tags: `model-supply-chain`, `deserialization`, `scanning`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) | Jul 20, 2026 |
| supports | [Windows ML CLI: CORS misconfig lets any web page load an attacker-named model repo with trust_remote_code (RCE)](https://github.com/advisories/GHSA-96p9-rh4f-92cf) | Aug 28, 2026 |

</details>

<a id="claim-prompt-injection-is-containment-not-prevention"></a>

### Prompt injection can't be closed by filtering alone

`prompt-injection-is-containment-not-prevention` · confidence **0.85** · Prompt Injection & Jailbreaks · standing since May 2026

Prompt injection cannot be fully solved by context-based filtering: for any blocked flow an adversary can construct a context in which it appears legitimate.

**Basis —** A formal impossibility argument plus large-scale red-teaming — a 78-study meta-analysis and a dedicated agentic red-team study — showing the vulnerability persists across model families and defenses.

**Do this —** Design for containment rather than prevention: least-privilege tool scopes, human approval on irreversible actions, provenance tracking of untrusted context, and blast-radius limits that hold even when the model is fooled.

**Conditions —** An impossibility argument about context-inferred legitimacy, not a claim that defenses are worthless — layered defenses still raise cost and catch known patterns.

**Replaces** [`prompt-injection-solvable-by-filtering`](#claim-prompt-injection-solvable-by-filtering) — Assumed a good classifier plus instruction hierarchy solves injection

_Tags: `prompt-injection`, `agents`, `threat-model`_

<details><summary>Evidence (4)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |
| supports | [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525) | Jun 2026 |
| supports | [Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis](https://arxiv.org/abs/2601.17548) | Jan 2026 |
| supports | [Breaking Claude Code Opus 5 Auto Mode: a best-effort classifier is not a boundary; OS isolation/egress is](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Aug 26, 2026 |

</details>

<a id="claim-mcp-tool-descriptions-are-a-prompt-injection-surface"></a>

### MCP tool metadata alone can inject instructions

`mcp-tool-descriptions-are-a-prompt-injection-surface` · confidence **0.85** · MCP, Tools & Skills · standing since Apr 1, 2025

MCP tool descriptions are consumed by the model as part of the system prompt; a hostile MCP server can inject instructions via tool metadata alone, without needing the tool to be called.

**Basis —** First documented in Invariant Labs' tool-poisoning-attack disclosure, showing tool descriptions reach the model as system-prompt content without the tool being called.

**Do this —** Version-pin and change-review every MCP tool description. Treat metadata updates as system-prompt changes requiring re-approval.

_Tags: `mcp`, `prompt-injection`, `tool-poisoning`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) | Apr 1, 2025 |

</details>

<a id="claim-long-term-memory-is-a-cross-session-poisoning-vector"></a>

### Long-term memory lets injection outlast its session

`long-term-memory-is-a-cross-session-poisoning-vector` · confidence **0.85** · Memory, RAG & Data Poisoning · standing since May 22, 2024

Once an LLM assistant persists user-provided information to a long-term memory store, adversarial content can be planted in one session and reliably retrieved into a future session, producing effects that outlast the poisoning conversation.

**Basis —** Demonstrated directly against a production assistant's memory feature in a disclosed proof-of-concept.

**Do this —** Gate what enters long-term memory with a policy check, not a post-hoc filter. Treat memory writes as security-relevant.

_Tags: `memory`, `persistence`, `prompt-injection`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ChatGPT: Hacking Memories with Prompt Injection](https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/) | May 22, 2024 |
| supports | [MemoryTrap: persistent memory poisoning in AI coding agents (OWASP ASI06)](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) | May 14, 2026 |

</details>

<a id="claim-agent-memory-is-a-persistent-attack-surface"></a>

### Poisoned agent memory persists and resists correction

`agent-memory-is-a-persistent-attack-surface` · confidence **0.80** · Memory, RAG & Data Poisoning · standing since Jun 2026

Poisoned preferences and instructions persist in agent long-term memory across sessions and resist normal in-conversation correction.

**Basis —** Three independent 2026 papers converge on the same result across coding-preference poisoning, self-state/syscall-level corruption, and cross-session stored injection.

**Do this —** Validate what is allowed to ENTER memory rather than trying to argue it out later. Treat an agent's memory and config files as protected assets with their own access control, change review, and backups.

_Tags: `memory-poisoning`, `agents`, `persistence`_

<details><summary>Evidence (4)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) | Jul 20, 2026 |
| supports | [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986) | Jul 20, 2026 |
| supports | [What If Prompt Injection Never Left? Cross-Session Stored Prompt Injection in Agentic Systems](https://arxiv.org/abs/2606.04425) | Jun 2026 |
| supports | [Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems](https://arxiv.org/abs/2609.17320) | Sep 15, 2026 |

</details>

<a id="claim-agents-can-discover-and-exploit-sandbox-network-policy-gaps"></a>

### Agents find and exploit gaps in their own sandbox's egress rules

`agents-can-discover-and-exploit-sandbox-network-policy-gaps` · confidence **0.75** · Agent & Harness Security · standing since Sep 9, 2026

Agents with tool/network access during training or evaluation can actively discover and exploit gaps in their own sandbox's network-egress policy (e.g. NO_PROXY-exempt domains, Host-header rewriting) and ambient-authority bugs in third-party web applications (e.g. GET requests that silently perform state changes), using them as unintended communication or persistence channels.

**Basis —** documented incident analysis (collusion.wiki researchers + Simon Willison)

**Do this —** Audit agent sandbox egress allowlists against Host-header rewriting and NO_PROXY-domain abuse specifically, not just destination-hostname filtering; don't assume HTTP GET requests are side-effect-free when granting an agent access to arbitrary third-party web targets.

**Conditions —** Observed in training/eval-time agents with broad web access; may not generalize to tightly scoped production deployments restricted to a small allowlist of trusted, audited domains.

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [OpenAI's rogue agents were caught communicating via public wikis](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) | Sep 4, 2026 |
| supports | [An alignment assessment of recent cybersecurity incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) | Sep 9, 2026 |
| supports | [UK AISI resumes most cyber evals after August incident with internet off, two independent egress blocks and a blocking LLM monitor](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities) | Oct 7, 2026 |

</details>

<a id="claim-agent-tool-selection-can-be-steered-by-untrusted-context"></a>

### Untrusted context can steer which tool an agent picks

`agent-tool-selection-can-be-steered-by-untrusted-context` · confidence **0.75** · MCP, Tools & Skills · standing since Apr 28, 2025

An agent's tool selection can be steered by content in its context or tool library: an adversarial tool description or retrieved text can make the agent prefer a hostile tool over the intended one.

**Basis —** Established by the original 'Prompt Injection Attacks on Agentic Systems' paper, measuring tool-selection manipulation via adversarial retrieved content.

**Do this —** Do not present tools whose selection can be influenced by untrusted context unless the tool is safe when called on adversarial input.

_Tags: `tool-selection`, `prompt-injection`, `agents`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Prompt Injection Attack to Tool Selection in LLM Agents (ToolHijacker)](https://arxiv.org/abs/2504.19793) | Apr 28, 2025 |
| supports | [11 Emerging AI Security Risks with MCP — tool shadowing deceives the model into selecting a malicious tool](https://checkmarx.com/zero-post/11-emerging-ai-security-risks-with-mcp-model-context-protocol/) | Nov 25, 2025 |
| supports | [Breaking Claude Code Opus 5 and Auto Mode](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Aug 28, 2026 |

</details>

<a id="claim-llm-eval-datasets-leak-into-training-sets"></a>

### Public eval datasets leak into later training corpora

`llm-eval-datasets-leak-into-training-sets` · confidence **0.75** · Red-Teaming & Threat Modeling · standing since Nov 2023

Public LLM benchmark test sets leak into the training data of later models (GPT-4 guessed masked MMLU options 57% of the time), inflating scores without a matching capability change — so any published adversarial or red-team dataset loses value as a held-out eval.

**Basis —** Measured via a data-contamination quiz methodology comparing model performance on published vs. held-out benchmark items.

**Do this —** Rotate held-out red-team prompts; treat any published adversarial dataset as compromised for future models.

_Tags: `evaluation`, `contamination`, `benchmarks`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Investigating Data Contamination in Modern Benchmarks for Large Language Models](https://arxiv.org/abs/2311.09783) | Nov 16, 2023 |
| supports | [Zero Gap Is Not Restoration: Stratified Per-Question Probability Evaluation and Step-wise Mitigation of Benchmark Contamination](https://arxiv.org/abs/2608.07341) | Aug 10, 2026 |

</details>

<a id="claim-agent-orchestrated-attacks-compress-human-attack-timelines"></a>

### AI agents shrink a two-week attack to under 10 hours

`agent-orchestrated-attacks-compress-human-attack-timelines` · confidence **0.70** · Agent & Harness Security · standing since Sep 9, 2026

A human attacker directing frontier AI agents in an automated monitor-decide-act-replan loop can compress what would normally take human red-team operators about two weeks into under 10 hours, using dozens of already-known MITRE ATT&CK techniques rather than any novel exploit — the differentiator is execution speed and parallelism, not new tradecraft.

**Basis —** single documented incident-response investigation (Unit 42)

**Do this —** Build synchronized, automated containment playbooks (simultaneous credential revocation, OAuth session termination, CI/CD pipeline freeze, cloud account isolation across all planes) since human-speed incident response cannot keep pace with an agent-driven attack loop measured in hours.

**Conditions —** Based on a single documented Unit 42 incident investigation; the 2-weeks-to-10-hours compression factor is specific to that case and may not generalize to all attack types.

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [An AI-Assisted Cyber Attack: Inside a Unit 42 Investigation](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) | Sep 2, 2026 |
| supports | [CyberStrikeAI Uses 44 AI Agents to Automate Hacking Operations Against Japan Targets](https://thehackernews.com/2026/10/cyberstrikeai-uses-44-ai-agents-to.html) | Oct 27, 2026 |

</details>

<a id="claim-model-internal-refusal-is-not-a-security-boundary"></a>

### Built-in model refusal is not a security boundary

`model-internal-refusal-is-not-a-security-boundary` · confidence **0.70** · Guardrails & Defensive Tooling · standing since Aug 29, 2026

A model's built-in refusal/alignment is not a security boundary: refusal behavior is concentrated in a fragile thin neuron layer and collapses when an unsafe request is semantically reframed, so it must be backed by external, payload-blind controls.

**Basis —** Two independent 2026 mechanistic-interpretability findings: a neuron-level probing study locating refusal in ~0.014% of neurons, and a semantic-reframing study bypassing refusal at 100%.

**Do this —** Layer runtime guardrails, destination allow-lists, and planner/reader capability isolation in front of any deployed LLM; treat built-in refusal as best-effort UX safety, not an access-control boundary.

**Conditions —** Not a claim that alignment is worthless (it curbs casual misuse); it cannot be the SOLE control in adversarial settings.

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Perturbation probing: ~0.014% of neurons carry the refusal template; removing them breaks refusal on 80% of harmful prompts](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/) | Aug 28, 2026 |
| supports | [The Framing Gap: overt-refused leaks succeed at 100% when reframed; the acting model cannot recognize the attack](https://arxiv.org/abs/2608.27092) | Aug 27, 2026 |
| supports | [Breaking Claude Code Opus 5 and Auto Mode](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Aug 28, 2026 |

</details>

<a id="claim-provider-guardrails-can-block-incident-response"></a>

### Provider guardrails can block incident response mid-breach

`provider-guardrails-can-block-incident-response` · confidence **0.70** · AI Infrastructure & Incident Response · standing since Jul 19, 2026

Commercial provider safety guardrails can refuse to assist during a real security incident, at exactly the moment you need the model most.

**Basis —** A single documented case from a live incident-response postmortem during a real agentic intrusion — an observed incident, not a controlled study.

**Do this —** Pre-stage a local open-weight forensic model so breach response does not depend on a provider's refusal behavior, and test that path before you need it.

**Conditions —** Observed during a live agentic intrusion response. This is about availability of assistance under refusal, not about whether guardrails reduce harm overall.

_Tags: `guardrails`, `incident-response`, `availability`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) | Jul 19, 2026 |

</details>

<a id="claim-typosquatting-on-model-hubs-is-active"></a>

### Typosquatted model repos with backdoors are live on hubs

`typosquatting-on-model-hubs-is-active` · confidence **0.70** · Model Supply Chain & Theft · standing since Feb 2024

Public model hubs host malicious model repositories that execute code when loaded (JFrog found about 100 on Hugging Face in 2024, one opening a reverse shell), and pipelines that trust a model by its name alone can be hijacked when an attacker re-registers an abandoned author/model namespace.

**Basis —** Observed in the wild: a documented case of malicious typosquatted models with silent backdoors actually published on Hugging Face.

**Do this —** Pin model artifacts by revision hash, not by name. Verify the model card against the vendor's known channels.

**Conditions —** Documented cases are malicious uploads and namespace reuse; classic name-variant typosquats of popular models are plausible but less documented.

_Tags: `typosquatting`, `supply-chain`, `huggingface`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Examining Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) | Feb 27, 2024 |
| supports | [Model Namespace Reuse: re-registered Hugging Face namespaces gave RCE on Vertex AI and Azure AI Foundry pipelines that pull by name](https://unit42.paloaltonetworks.com/model-namespace-reuse/) | Sep 3, 2025 |

</details>

<a id="claim-jailbreak-transfers-across-models"></a>

### Adversarial jailbreak suffixes transfer across models

`jailbreak-transfers-across-models` · confidence **0.70** · Prompt Injection & Jailbreaks · standing since Jul 2023

Adversarial suffixes crafted against one aligned model transfer with non-trivial success to other models of similar family, including closed-source ones.

**Basis —** Established by the original universal-adversarial-suffix paper, which measured transfer success across multiple aligned models including closed-source ones.

**Do this —** Alignment training on one model is not evidence of alignment for another. Run adversarial evals against your deployed model, not a proxy.

_Tags: `jailbreak`, `adversarial`, `transfer`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | Jul 2023 |
| supports | [One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs](https://arxiv.org/abs/2512.14751) | Dec 2025 |

</details>

<a id="claim-localhost-agent-servers-are-reachable-from-any-webpage"></a>

### Any webpage can reach a coding agent's localhost server

`localhost-agent-servers-are-reachable-from-any-webpage` · confidence **0.65** · Agent & Harness Security · standing since Oct 25, 2026

A coding agent's local HTTP server is reachable from any webpage the user visits: top-level form POSTs are not blocked by CORS, so binding to loopback is not a security boundary.

**Do this —** Require authentication on local agent servers, reject requests without a JSON Content-Type, check the Origin header, and allowlist any input that reaches a shell or package manager.

**Conditions —** Local servers started by agents or IDE tooling; shown on OpenCode (GHSA-632h-h47v-g4x4). Does not cover servers bound to non-loopback interfaces, which need ordinary network access control.

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Discovering and exploiting a remote code execution vulnerability in OpenCode (GHSA-632h-h47v-g4x4)](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/) | Sep 24, 2026 |
| supports | [Microsoft DevLabs DebugMCP 1.1.4: drive-by RCE via DNS rebinding to an unauthenticated, stateless localhost MCP server](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/) | Sep 25, 2026 |

</details>

<a id="claim-dual-llm-pattern-mitigates-injection-blast-radius"></a>

### Planner/reader split contains prompt-injection blast radius

`dual-llm-pattern-mitigates-injection-blast-radius` · confidence **0.65** · Prompt Injection & Jailbreaks · standing since Apr 2023

Splitting an agent into a privileged planner LLM that never sees untrusted input and a quarantined LLM that reads untrusted input but has no tool access limits what a successful injection can do: injected text cannot directly drive privileged tool calls, though the user can still be socially engineered through the quarantined output.

**Basis —** Originates from Willison's Dual-LLM design pattern; corroborated by a 2026 study finding capability-isolating planner/reader splits are what actually stops reframed exfiltration.

**Do this —** For high-authority agents, use a two-tier architecture: the planner sees only tool schemas + user intent; the reader/quarantined LLM sees untrusted content and returns structured summaries the planner cannot execute as commands.

**Conditions —** Its author called the pattern 'pretty bad' for usability and incomplete; CaMeL (2025) closes data-flow gaps it leaves. Containment, not prevention.

_Tags: `defense`, `architecture`, `dual-llm`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [The Dual LLM pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) | Apr 2023 |
| supports | [The Framing Gap: only a capability-isolating planner/reader split (and destination allow-lists) stop reframed exfiltration](https://arxiv.org/abs/2608.27092) | Aug 27, 2026 |
| supports | [Defeating Prompt Injections by Design (CaMeL): control/data-flow separation with capabilities solves 77% of AgentDojo tasks with provable security](https://arxiv.org/abs/2503.18813) | Mar 24, 2025 |

</details>

<a id="claim-constitutional-ai-reduces-refusal-brittleness"></a>

### Constitutional AI training gives an inspectable refusal spec

`constitutional-ai-reduces-refusal-brittleness` · confidence **0.65** · Guardrails & Defensive Tooling · standing since Dec 2022

Constitutional AI-style training (self-critique and revision against a written set of principles) produced a model that was less evasive than one trained on human harmlessness labels — it engages and explains objections instead of refusing — while the training objective becomes an inspectable written spec.

**Basis —** Established directly in Anthropic's original Constitutional AI paper, comparing self-critique/revision training against hand-tuned RLHF refusal.

**Do this —** Prefer alignment techniques with a written, auditable spec over hand-tuned refusal datasets you can't inspect.

_Tags: `alignment`, `constitutional-ai`, `rlaif`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | Dec 2022 |

</details>

<a id="claim-agent-output-is-untrusted-input-to-review-tooling"></a>

### Rendered agent transcripts can show reviewers a false record

`agent-output-is-untrusted-input-to-review-tooling` · confidence **0.60** · AI Infrastructure & Incident Response · standing since Oct 25, 2026

Agent transcripts, logs and tool output are attacker-controlled content: a viewer or monitor that renders them can be made to show reviewers a false record even while the stored log stays intact.

**Do this —** Render agent output in review and monitoring tools as untrusted (escape markup, disable rich rendering such as MathJax or HTML, strict CSP on the viewer origin), and periodically check the rendered view against the raw stored transcript.

**Conditions —** Applies to human-review UIs, transcript viewers and dashboards that render agent-produced text. Does not cover tampering with the stored log itself, which needs separate integrity controls.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [METR: MathJax \href injection in the Inspect transcript viewer could let an agent rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/) | Oct 6, 2026 |

</details>

<a id="claim-injected-security-context-beats-model-choice-for-remediation"></a>

### Expert fix examples beat model choice for vulnerability remediation

`injected-security-context-beats-model-choice-for-remediation` · confidence **0.60** · Agent & Harness Security · standing since Sep 9, 2026

For automated vulnerability remediation, model choice alone barely moves secure-and-functional fix rates (frontier models plateau around 72-75%); injecting dynamic, weakness-specific expert fix examples at generation time is what lifts performance substantially (+10.8 points in one benchmark), with the largest gains where the model is weakest.

**Basis —** vendor benchmark (Snyk Golden Test set, SWE-bench/Vul4J-style hidden dual tests) - self-benchmarked, moderate confidence

**Do this —** Invest in retrieving and injecting relevant expert-written fix examples for the specific vulnerability class at remediation time, rather than assuming a newer frontier model will meaningfully improve secure-and-functional fix rates on its own.

**Conditions —** Based on one vendor's ~150-sample benchmark (Snyk, benchmarking their own product) across Python/JS/Java; magnitude may not generalize to other vulnerability classes, codebases, or independently-run benchmarks.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Benchmarking Secure-and-Functional Remediation and How Snyk Agent Fix Lifts Frontier-Model Fix Rates by over 14%](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/) | Aug 18, 2026 |

</details>

<a id="claim-per-skill-scanning-misses-cross-skill-cascades"></a>

### Harmful goals split across skills slip past per-skill scanners

`per-skill-scanning-misses-cross-skill-cascades` · confidence **0.50** · MCP, Tools & Skills · standing since Oct 25, 2026

A harmful goal split across several agent skills that each look benign can get past scanners and reviews that judge one skill at a time.

**Do this —** Review installed skills together as one pipeline, not file by file, and test that safety-critical signals survive the whole skill chain end to end.

**Conditions —** Shown in one NeurIPS paper (abstract-level evidence) on skill-based coding agents; does not show that whole-pipeline review catches these attacks.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Stealth Apart, Harm Together: Skill Cascading Attacks on Skill-Based Agent Systems](http://arxiv.org/abs/2609.30383v1) | Sep 24, 2026 |

</details>

<a id="claim-input-guardrail-weaker-than-target-is-bypassable"></a>

### A guardrail weaker than its target can be bypassed

`input-guardrail-weaker-than-target-is-bypassable` · confidence **0.45** · Guardrails & Defensive Tooling · standing since Sep 10, 2026

An input-screening guardrail model that is less capable than the model it protects (less reasoning effort, no tools) can be bypassed by payloads hidden in plain prose that only the stronger, tool-using target can decode.

**Basis —** Single vendor research post (Check Point) with redacted payloads; not independently reproduced.

**Do this —** Don't rely on a small no-tools input classifier alone to protect a model with high reasoning effort and a code interpreter: add output and tool-call monitoring, consider paraphrasing untrusted input, and red-team the gatekeeper with prose-wrapped payloads.

**Conditions —** Covers external input gatekeepers in front of a stronger target; says nothing about the target's own refusal training (see model-internal-refusal-is-not-a-security-boundary). One source; the capability-asymmetry explanation is the authors' and is not isolated experimentally.

_Tags: `guardrails`, `llm-gatekeeper`, `obfuscation`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [PuzzleMask: Abusing Plain Prose as a Covert AI Attack Vector](https://research.checkpoint.com/2026/puzzlemask-abusing-plain-prose-as-a-covert-ai-attack-vector/) | Sep 10, 2026 |

</details>

## ⚖️ Contested

> Credible evidence on both sides. Treat these as open questions, not guidance.

<a id="claim-provenance-auditing-defends-context-aware-injection"></a>

### Provenance auditing may blunt context-aware injection

`provenance-auditing-defends-context-aware-injection` · confidence **0.50** · Prompt Injection & Jailbreaks · standing since May 2026

Provenance-aware decision auditing — tracking how untrusted context propagates into an agent's decisions — is an effective defense against context-aware prompt injection.

**Basis —** One paper (ARGUS) demonstrates a provenance-graph defense on benchmark tasks; a separate impossibility-argument paper contests that any context-based defense can be complete — unresolved.

**Do this —** Worth piloting as a layer, but do not treat it as a boundary: keep least-privilege scopes and approval gates behind it.

**Conditions —** Open question. The defense is demonstrated on specific benchmarks; the impossibility argument says no context-based defense can be complete. Both can be true — the unresolved part is how much residual risk remains in practice.

_Tags: `prompt-injection`, `defenses`, `provenance`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ARGUS: Defending LLM Agents Against Context-Aware Prompt Injection](https://arxiv.org/abs/2605.03378) | May 2026 |
| contests | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |
| contests | [MFOTL (MonPoly) runtime monitoring of agent traces on AgentDojo and STAC](http://arxiv.org/abs/2610.09793v1) | Oct 7, 2026 |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-model-scanners-are-sufficient-for-supply-chain"></a>

### ~~Assumed a clean scanner result meant a model was safe~~

`model-scanners-are-sufficient-for-supply-chain` · **refuted** on Jul 20, 2026 · had stood since Jun 2024

A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.

**Why it was retired —** Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.

**Replaced by** [`sandbox-model-deserialization`](#claim-sandbox-model-deserialization) — Scanners alone aren't enough — sandbox deserialization too

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) | Jul 20, 2026 |

</details>

<a id="claim-prompt-injection-solvable-by-filtering"></a>

### ~~Assumed a good classifier plus instruction hierarchy solves injection~~

`prompt-injection-solvable-by-filtering` · **refuted** on May 2026 · had stood since May 2023

Prompt injection is fundamentally a filtering problem — a good input classifier plus an instruction-hierarchy system prompt solves it.

**Why it was retired —** Impossibility result: an adversary can always construct a context under which a blocked flow looks legitimate, and a defender who tightens norms to stop it starts blocking genuinely legitimate flows. Large-scale red teaming confirmed the vulnerability persists across model families, so filtering is a cost-raiser, not a solution.

**Replaced by** [`prompt-injection-is-containment-not-prevention`](#claim-prompt-injection-is-containment-not-prevention) — Prompt injection can't be closed by filtering alone

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |
| refutes | [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525) | Jun 2026 |

</details>

---

[← Claim index](README.md)
