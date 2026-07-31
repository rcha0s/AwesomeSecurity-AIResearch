# AI Research — standing claims

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_5 current · 0 contested · 2 superseded · 1 refuted · updated 2026-07-31_

[← Claim index](README.md) · [AI Research findings feed](../ai-research/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-match-tool-schemas-to-the-target-model"></a>

### A newer SOTA model can be WORSE at your harness's custom tool schema than its older siblings, because it was RL-trained on a different harness's tools.

`match-tool-schemas-to-the-target-model` · confidence **0.80** · Tooling & Infrastructure · standing since Jul 4, 2026

**Do this —** Match your harness's tool schemas to what the target model was trained on — Claude on str-replace-style edits, OpenAI on apply_patch — and offer a model-matched edit tool in multi-model harnesses. Re-run tool-calling evals on every model upgrade.

**Limits —** Observed on custom edit-tool schemas in third-party harnesses. First-party harnesses whose tools the model was trained on do not show the regression.

**Replaces** [`newer-model-is-always-an-upgrade`](#claim-newer-model-is-always-an-upgrade) — Swapping in the newest frontier model is a strict improvement for an existing harness.

_Tags: `harness`, `tool-use`, `agents`, `evals`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/) | Jul 4, 2026 |

</details>

<a id="claim-score-evals-on-groundedness-not-headline-f1"></a>

### Headline benchmark F1 hides what actually matters for security scanning: groundedness, precision, and run-to-run stability.

`score-evals-on-groundedness-not-headline-f1` · confidence **0.75** · Evaluation · standing since Jul 17, 2026

**Do this —** Score scanners on groundedness and run-to-run stability as first-class metrics, and evaluate precision on repos like yours — a matching F1 can still hide a precision gap that shifts cost onto human triage. Do not expect stacking models to fix a groundedness problem.

_Tags: `evals`, `benchmarks`, `security-scanning`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) | Jul 17, 2026 |
| supports | [Kimi K3 code-security eval: matching F1 hides a precision gap](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) | Jul 22, 2026 |

</details>

<a id="claim-toon-cuts-input-tokens-vs-json"></a>

### For large uniform arrays, TOON serializes to 30-60% fewer input tokens than JSON at comparable retrieval accuracy.

`toon-cuts-input-tokens-vs-json` · confidence **0.75** · Architecture & Optimization · standing since Nov 2025

**Do this —** Use TOON for the big uniform/tabular payloads you feed INTO the model (tool results, row sets, retrieved records). Keep JSON where data is deeply nested or irregular.

**Limits —** Input side only, and only for uniform arrays. Nested or irregular objects show much smaller or negative gains, and on short payloads the 'prompt tax' of explaining the format to the model can erase the saving entirely. Says nothing about generation — see constrained-decoding-for-structured-output.

**Replaces** [`json-default-for-all-agent-io`](#claim-json-default-for-all-agent-io) — JSON is the natural default for all agent I/O; serialization format is not a meaningful optimization lever.

_Tags: `tokens`, `serialization`, `context`, `cost`_

<details><summary>Evidence (4)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [toon-format/toon — reference implementation, spec and benchmarks](https://github.com/toon-format/toon) | undated |
| supports | [Notation Matters: A Benchmark Study of Token-Optimized Formats in Agentic AI Systems](https://arxiv.org/abs/2605.29676) | May 2026 |
| supports | [New Token-Oriented Object Notation (TOON) Hopes to Cut LLM Costs by Reducing Token Consumption](https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/) | Nov 2025 |
| contests | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Mar 2026 |

</details>

<a id="claim-few-distinct-tools-beat-many"></a>

### Coding-agent harnesses work better with few distinct tools and a lean system prompt of reasoning rather than rules.

`few-distinct-tools-beat-many` · confidence **0.70** · Agents & Harnesses · standing since Jul 21, 2026

**Do this —** Keep the tool count small and the tools clearly distinct; write the system prompt as reasoning rather than rule lists; grow your eval suite out of real incidents; gate dangerous actions with a context-aware permission classifier rather than a static allowlist.

**Limits —** Described from first-party practice on one coding agent, not a controlled comparison — treat as a strong prior, not a measured result.

_Tags: `harness`, `agents`, `prompting`, `evals`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [How the Claude Code team designs its harness](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) | Jul 21, 2026 |

</details>

<a id="claim-constrained-decoding-for-structured-output"></a>

### For structured model OUTPUT, constrained decoding gives the lowest token usage and plain JSON generation the best accuracy — token-optimized notations do not win here.

`constrained-decoding-for-structured-output` · confidence **0.70** · Architecture & Optimization · standing since Mar 2026

**Do this —** Split the decision by direction. Use a token-optimized notation for what you feed in; use constrained decoding (or plain JSON) for what you ask the model to emit.

**Limits —** Benchmarked on one-shot in-context generation. Constrained decoding requires a serving stack that supports it — without one, plain JSON generation is the accuracy-preserving fallback.

**Replaces** [`toon-best-for-structured-output-generation`](#claim-toon-best-for-structured-output-generation) — Because TOON is more token-efficient than JSON, asking the model to GENERATE TOON is also better than asking it to generate JSON.

_Tags: `tokens`, `serialization`, `structured-output`, `decoding`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Mar 2026 |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-newer-model-is-always-an-upgrade"></a>

### ~~Swapping in the newest frontier model is a strict improvement for an existing harness.~~

`newer-model-is-always-an-upgrade` · **superseded** on Jul 4, 2026 · had stood since Jan 2024

**Why it was retired —** Measured on a third-party harness's custom edit tool, newer Claude models invented made-up fields that their older siblings got right. Model upgrades can regress harness-specific tool calling, so an upgrade is a change to re-evaluate, not a free win.

**Replaced by** [`match-tool-schemas-to-the-target-model`](#claim-match-tool-schemas-to-the-target-model) — A newer SOTA model can be WORSE at your harness's custom tool schema than its older siblings, because it was RL-trained on a different harness's tools.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/) | Jul 4, 2026 |

</details>

<a id="claim-json-default-for-all-agent-io"></a>

### ~~JSON is the natural default for all agent I/O; serialization format is not a meaningful optimization lever.~~

`json-default-for-all-agent-io` · **superseded** on May 2026 · had stood since Jan 2023

**Why it was retired —** Format choice measurably moves cost: uniform arrays serialize 30-60% smaller in TOON at comparable retrieval accuracy, which makes serialization a real optimization lever on the input side rather than an aesthetic preference.

**Replaced by** [`toon-cuts-input-tokens-vs-json`](#claim-toon-cuts-input-tokens-vs-json) — For large uniform arrays, TOON serializes to 30-60% fewer input tokens than JSON at comparable retrieval accuracy.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Notation Matters: A Benchmark Study of Token-Optimized Formats in Agentic AI Systems](https://arxiv.org/abs/2605.29676) | May 2026 |

</details>

<a id="claim-toon-best-for-structured-output-generation"></a>

### ~~Because TOON is more token-efficient than JSON, asking the model to GENERATE TOON is also better than asking it to generate JSON.~~

`toon-best-for-structured-output-generation` · **refuted** on Mar 2026 · had stood since Nov 2025

**Why it was retired —** Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on simple structures. The input-side token saving does not transfer to the output side.

**Replaced by** [`constrained-decoding-for-structured-output`](#claim-constrained-decoding-for-structured-output) — For structured model OUTPUT, constrained decoding gives the lowest token usage and plain JSON generation the best accuracy — token-optimized notations do not win here.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Mar 2026 |

</details>

---

[← Claim index](README.md)
