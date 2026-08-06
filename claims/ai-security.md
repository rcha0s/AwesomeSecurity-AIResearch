# AI Security — standing claims

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_15 current · 1 contested · 0 superseded · 2 refuted · updated 2026-08-06_

[← Claim index](README.md) · [AI Security findings feed](../ai-security/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-pickle-based-model-formats-are-code-execution"></a>

### Loading a pickle-based model file (PyTorch .pt/.bin) is equivalent to running arbitrary code; the format has no sandbox and no way to introspect what will execute at load time short of manual reversing.

`pickle-based-model-formats-are-code-execution` · confidence **0.95** · Model Supply Chain · standing since Mar 2021

**Do this —** Prefer safetensors for any model you didn't personally train. If you must load pickles, do it in a container with no outbound network.

_Tags: `pickle`, `supply-chain`, `safetensors`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Never a dill moment](https://blog.trailofbits.com/2021/03/15/never-a-dill-moment-exploiting-machine-learning-pickle-files/) | Mar 2021 |
| supports | [Pickle scanning](https://huggingface.co/docs/hub/en/security-pickle) | undated |

</details>

<a id="claim-prompt-injection-is-a-permanent-attack-surface"></a>

### LLM applications that mix trusted instructions with untrusted input are permanently vulnerable to instruction hijacking; the surface cannot be closed by prompt engineering alone.

`prompt-injection-is-a-permanent-attack-surface` · confidence **0.90** · Prompt Injection · standing since Feb 2023

**Do this —** Design agentic systems assuming injection succeeds sometimes: least-privilege tool scopes, human approval on irreversible actions, blast-radius caps that hold even when the model is fooled.

_Tags: `prompt-injection`, `threat-model`, `agents`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [The Dual LLM pattern](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/) | Apr 14, 2023 |
| supports | [Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection](https://arxiv.org/abs/2302.12173) | Feb 23, 2023 |

</details>

<a id="claim-indirect-injection-via-retrieved-content-is-viable"></a>

### Indirect prompt injection — hostile instructions embedded in documents, web pages, or tool outputs that the LLM reads at run time — is a demonstrated attack vector against real production LLM assistants.

`indirect-injection-via-retrieved-content-is-viable` · confidence **0.90** · Prompt Injection · standing since Feb 2023

**Do this —** Treat every retrieval-augmented context as untrusted input. Never let retrieved content unilaterally cause a tool call with side effects.

_Tags: `prompt-injection`, `rag`, `indirect`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Not what you've signed up for](https://arxiv.org/abs/2302.12173) | Feb 2023 |
| supports | [Hacking GitHub Copilot Chat via indirect prompt injection](https://embracethered.com/blog/posts/2024/hacking-github-copilot-chat-prompt-injection/) | undated |

</details>

<a id="claim-sandbox-model-deserialization"></a>

### Prefer non-executable model formats and sandbox deserialization of any third-party model — a clean scanner result is weak evidence of safety.

`sandbox-model-deserialization` · confidence **0.85** · Model Supply Chain · standing since Jul 20, 2026

**Do this —** Load third-party weights only in a sandbox, prefer safetensors-style non-executable formats, and treat scanner output as one signal rather than an admission gate.

**Replaces** [`model-scanners-are-sufficient-for-supply-chain`](#claim-model-scanners-are-sufficient-for-supply-chain) — A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.

_Tags: `model-supply-chain`, `deserialization`, `scanning`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) | Jul 20, 2026 |

</details>

<a id="claim-prompt-injection-is-containment-not-prevention"></a>

### Prompt injection cannot be fully solved by context-based filtering: for any blocked flow an adversary can construct a context in which it appears legitimate.

`prompt-injection-is-containment-not-prevention` · confidence **0.85** · Prompt Injection · standing since May 2026

**Do this —** Design for containment rather than prevention: least-privilege tool scopes, human approval on irreversible actions, provenance tracking of untrusted context, and blast-radius limits that hold even when the model is fooled.

**Limits —** An impossibility argument about context-inferred legitimacy, not a claim that defenses are worthless — layered defenses still raise cost and catch known patterns.

**Replaces** [`prompt-injection-solvable-by-filtering`](#claim-prompt-injection-solvable-by-filtering) — Prompt injection is fundamentally a filtering problem — a good input classifier plus an instruction-hierarchy system prompt solves it.

_Tags: `prompt-injection`, `agents`, `threat-model`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |
| supports | [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525) | Jun 2026 |
| supports | [Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis](https://arxiv.org/abs/2601.17548) | Jan 2026 |

</details>

<a id="claim-mcp-tool-descriptions-are-a-prompt-injection-surface"></a>

### MCP tool descriptions are consumed by the model as part of the system prompt; a hostile MCP server can inject instructions via tool metadata alone, without needing the tool to be called.

`mcp-tool-descriptions-are-a-prompt-injection-surface` · confidence **0.85** · MCP & Tools · standing since Mar 2025

**Do this —** Version-pin and change-review every MCP tool description. Treat metadata updates as system-prompt changes requiring re-approval.

_Tags: `mcp`, `prompt-injection`, `tool-poisoning`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) | Mar 2025 |

</details>

<a id="claim-long-term-memory-is-a-cross-session-poisoning-vector"></a>

### Once an LLM assistant persists user-provided information to a long-term memory store, adversarial content can be planted in one session and reliably retrieved into a future session, producing effects that outlast the poisoning conversation.

`long-term-memory-is-a-cross-session-poisoning-vector` · confidence **0.85** · Memory & Context Poisoning · standing since Sep 2024

**Do this —** Gate what enters long-term memory with a policy check, not a post-hoc filter. Treat memory writes as security-relevant.

_Tags: `memory`, `persistence`, `prompt-injection`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ChatGPT: Hacking Memories with Prompt Injection](https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/) | Sep 2024 |

</details>

<a id="claim-agent-memory-is-a-persistent-attack-surface"></a>

### Poisoned preferences and instructions persist in agent long-term memory across sessions and resist normal in-conversation correction.

`agent-memory-is-a-persistent-attack-surface` · confidence **0.80** · Memory & Context Poisoning · standing since Jun 2026

**Do this —** Validate what is allowed to ENTER memory rather than trying to argue it out later. Treat an agent's memory and config files as protected assets with their own access control, change review, and backups.

_Tags: `memory-poisoning`, `agents`, `persistence`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619) | Jul 20, 2026 |
| supports | [Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986) | Jul 20, 2026 |
| supports | [What If Prompt Injection Never Left? Cross-Session Stored Prompt Injection in Agentic Systems](https://arxiv.org/abs/2606.04425) | Jun 2026 |

</details>

<a id="claim-typosquatting-on-model-hubs-is-active"></a>

### Adversaries publish typosquatted model repositories on public hubs (name variants of popular models) that ship with malicious pickle payloads or exfiltration hooks; several have been observed in the wild on Hugging Face.

`typosquatting-on-model-hubs-is-active` · confidence **0.75** · Model Supply Chain · standing since Feb 2024

**Do this —** Pin model artifacts by revision hash, not by name. Verify the model card against the vendor's known channels.

_Tags: `typosquatting`, `supply-chain`, `huggingface`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Malicious ML models with silent backdoor found on Hugging Face](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) | Feb 2024 |

</details>

<a id="claim-llm-eval-datasets-leak-into-training-sets"></a>

### Public benchmark datasets used to evaluate LLM security leak into the training corpora of later models, inflating scores without corresponding capability change.

`llm-eval-datasets-leak-into-training-sets` · confidence **0.75** · Evaluation · standing since Nov 2023

**Do this —** Rotate held-out red-team prompts; treat any published adversarial dataset as compromised for future models.

_Tags: `evaluation`, `contamination`, `benchmarks`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Data Contamination Quiz](https://arxiv.org/abs/2311.09783) | Nov 2023 |

</details>

<a id="claim-provider-guardrails-can-block-incident-response"></a>

### Commercial provider safety guardrails can refuse to assist during a real security incident, at exactly the moment you need the model most.

`provider-guardrails-can-block-incident-response` · confidence **0.70** · Harness & Agent Security · standing since Jul 19, 2026

**Do this —** Pre-stage a local open-weight forensic model so breach response does not depend on a provider's refusal behavior, and test that path before you need it.

**Limits —** Observed during a live agentic intrusion response. This is about availability of assistance under refusal, not about whether guardrails reduce harm overall.

_Tags: `guardrails`, `incident-response`, `availability`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/) | Jul 19, 2026 |

</details>

<a id="claim-agent-tool-selection-can-be-steered-by-untrusted-context"></a>

### An agent's tool selection can be influenced by content in its context window; adversarial content in retrieved documents can cause the agent to prefer a hostile tool over the intended one.

`agent-tool-selection-can-be-steered-by-untrusted-context` · confidence **0.70** · MCP & Tools · standing since Jul 2024

**Do this —** Do not present tools whose selection can be influenced by untrusted context unless the tool is safe when called on adversarial input.

_Tags: `tool-selection`, `prompt-injection`, `agents`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Prompt Injection Attacks on Agentic Systems](https://arxiv.org/abs/2407.09164) | Jul 2024 |

</details>

<a id="claim-jailbreak-transfers-across-models"></a>

### Adversarial suffixes crafted against one aligned model transfer with non-trivial success to other models of similar family, including closed-source ones.

`jailbreak-transfers-across-models` · confidence **0.70** · Prompt Injection · standing since Jul 2023

**Do this —** Alignment training on one model is not evidence of alignment for another. Run adversarial evals against your deployed model, not a proxy.

_Tags: `jailbreak`, `adversarial`, `transfer`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | Jul 2023 |

</details>

<a id="claim-dual-llm-pattern-mitigates-injection-blast-radius"></a>

### Splitting agent architecture into a privileged planner LLM that never sees untrusted input, and a quarantined LLM that processes untrusted input but has no tool access, contains prompt injection to non-privileged operations.

`dual-llm-pattern-mitigates-injection-blast-radius` · confidence **0.70** · Prompt Injection · standing since Apr 2023

**Do this —** For high-authority agents, use a two-tier architecture: the planner sees only tool schemas + user intent; the reader/quarantined LLM sees untrusted content and returns structured summaries the planner cannot execute as commands.

_Tags: `defense`, `architecture`, `dual-llm`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [The Dual LLM pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) | Apr 2023 |

</details>

<a id="claim-constitutional-ai-reduces-refusal-brittleness"></a>

### Constitutional AI-style training (self-critique + revision against a written set of principles) reduces the fragility of hand-tuned refusal training and gives the training process an inspectable specification.

`constitutional-ai-reduces-refusal-brittleness` · confidence **0.65** · Alignment · standing since Dec 2022

**Do this —** Prefer alignment techniques with a written, auditable spec over hand-tuned refusal datasets you can't inspect.

_Tags: `alignment`, `constitutional-ai`, `rlaif`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | Dec 2022 |

</details>

## ⚖️ Contested

> Credible evidence on both sides. Treat these as open questions, not guidance.

<a id="claim-provenance-auditing-defends-context-aware-injection"></a>

### Provenance-aware decision auditing — tracking how untrusted context propagates into an agent's decisions — is an effective defense against context-aware prompt injection.

`provenance-auditing-defends-context-aware-injection` · confidence **0.50** · Prompt Injection · standing since May 2026

**Do this —** Worth piloting as a layer, but do not treat it as a boundary: keep least-privilege scopes and approval gates behind it.

**Limits —** Open question. The defense is demonstrated on specific benchmarks; the impossibility argument says no context-based defense can be complete. Both can be true — the unresolved part is how much residual risk remains in practice.

_Tags: `prompt-injection`, `defenses`, `provenance`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ARGUS: Defending LLM Agents Against Context-Aware Prompt Injection](https://arxiv.org/abs/2605.03378) | May 2026 |
| contests | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-model-scanners-are-sufficient-for-supply-chain"></a>

### ~~A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.~~

`model-scanners-are-sufficient-for-supply-chain` · **refuted** on Jul 20, 2026 · had stood since Jun 2024

**Why it was retired —** Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.

**Replaced by** [`sandbox-model-deserialization`](#claim-sandbox-model-deserialization) — Prefer non-executable model formats and sandbox deserialization of any third-party model — a clean scanner result is weak evidence of safety.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503) | Jul 20, 2026 |

</details>

<a id="claim-prompt-injection-solvable-by-filtering"></a>

### ~~Prompt injection is fundamentally a filtering problem — a good input classifier plus an instruction-hierarchy system prompt solves it.~~

`prompt-injection-solvable-by-filtering` · **refuted** on May 2026 · had stood since May 2023

**Why it was retired —** Impossibility result: an adversary can always construct a context under which a blocked flow looks legitimate, and a defender who tightens norms to stop it starts blocking genuinely legitimate flows. Large-scale red teaming confirmed the vulnerability persists across model families, so filtering is a cost-raiser, not a solution.

**Replaced by** [`prompt-injection-is-containment-not-prevention`](#claim-prompt-injection-is-containment-not-prevention) — Prompt injection cannot be fully solved by context-based filtering: for any blocked flow an adversary can construct a context in which it appears legitimate.

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [AI Agents May Always Fall for Prompt Injections](https://arxiv.org/abs/2605.17634) | May 2026 |
| refutes | [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525) | Jun 2026 |

</details>

---

[← Claim index](README.md)
