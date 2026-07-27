# AI Security — standing claims

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_4 current · 1 contested · 0 superseded · 2 refuted · updated 2026-07-27_

[← Claim index](README.md) · [AI Security findings feed](../ai-security/README.md) · [Home](../README.md)

## ✅ Current

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
