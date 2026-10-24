# AI Research — standing claims

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_18 current · 2 contested · 2 superseded · 1 refuted · updated 2026-10-24_

[← Claim index](README.md) · [AI Research findings feed](../ai-research/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-coding-agents-produce-plausible-but-hallucinated-apis"></a>

### Coding agents hallucinate plausible but nonexistent APIs

`coding-agents-produce-plausible-but-hallucinated-apis` · confidence **0.90** · Agents & Harnesses · standing since Jul 13, 2024

Coding assistants generate calls to functions and APIs that do not exist in the target library or version — plausible spelling, correct-looking signature, no runtime existence.

**Basis —** Measured in an academic study of code-generation hallucination rates against real library/version ground truth.

**Do this —** Any LLM-suggested import or API call must be validated against the actual library documentation for the pinned version.

_Tags: `coding-agents`, `hallucination`, `apis`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [On Mitigating Code LLM Hallucinations with API Documentation (CloudAPIBench)](https://arxiv.org/abs/2407.09726) | Jul 13, 2024 |
| supports | [Library Hallucinations in LLM-Generated Code: A Risk Analysis Grounded in Developer Queries](https://arxiv.org/abs/2509.22202) | Sep 2025 |

</details>

<a id="claim-capability-elicitation-lags-training"></a>

### Standard prompting understates a model's real capability ceiling

`capability-elicitation-lags-training` · confidence **0.80** · Models & Capabilities · standing since Dec 12, 2023

A model's actual capability ceiling is typically higher than what standard prompting elicits; targeted prompting or scaffolding can unlock capabilities the base eval missed.

**Basis —** Referenced from Anthropic's Responsible Scaling Policy work on capability elicitation.

**Do this —** Do not build a safety case on 'the model can't do X' from a base-eval measurement alone.

_Tags: `capabilities`, `elicitation`, `safety`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Anthropic: Announcing our updated Responsible Scaling Policy (notes evaluations that could elicit more with chain-of-thought or best-of-N)](https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy) | Oct 15, 2024 |
| supports | [AI capabilities can be significantly improved without expensive retraining: most post-training enhancements equal >5x training compute](https://arxiv.org/abs/2312.07413) | Dec 12, 2023 |

</details>

<a id="claim-long-context-does-not-eliminate-retrieval-need"></a>

### Long context windows don't remove the need for retrieval

`long-context-does-not-eliminate-retrieval-need` · confidence **0.80** · Retrieval, Prompting & Context · standing since Jul 2023

Long-context models do not eliminate the need for retrieval: they exhibit lost-in-the-middle effects, cost grows linearly with context size, and per-token attention drops on distant tokens.

**Basis —** Grounded in the 'Lost in the Middle' study measuring attention degradation on distant tokens as context length grows.

**Do this —** Retrieval + a short, relevant context still beats stuffing a long context on cost, latency, and accuracy for most tasks.

_Tags: `long-context`, `rag`, `lost-in-the-middle`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Lost in the Middle](https://arxiv.org/abs/2307.03172) | Jul 2023 |
| supports | [Context Length Alone Hurts LLM Performance Despite Perfect Retrieval](https://arxiv.org/abs/2510.05381) | Oct 2025 |

</details>

<a id="claim-hybrid-search-beats-pure-vector-for-most-domains"></a>

### Hybrid BM25 + vector search beats pure vector retrieval

`hybrid-search-beats-pure-vector-for-most-domains` · confidence **0.80** · Retrieval, Prompting & Context · standing since Jun 2023

Hybrid search (BM25 + dense vectors) outperforms pure vector retrieval on most enterprise/technical corpora, because vector embeddings underweight exact term matches that carry high signal.

**Basis —** A vendor benchmark comparison of hybrid vs. pure-vector search across enterprise/technical corpora.

**Do this —** Default to hybrid retrieval unless you've measured that pure-vector wins on your specific corpus.

_Tags: `rag`, `hybrid-search`, `bm25`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Hybrid Search Explained](https://weaviate.io/blog/hybrid-search-explained) | Jan 27, 2025 |
| supports | [From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents](https://arxiv.org/abs/2604.01733) | Apr 2026 |

</details>

<a id="claim-quantization-preserves-most-benchmark-scores"></a>

### 8/4-bit quantization preserves most benchmark accuracy

`quantization-preserves-most-benchmark-scores` · confidence **0.80** · Tooling & Serving · standing since Jun 2023

8-bit and 4-bit quantization of open-weights models preserves most benchmark accuracy (within 1–3 points) while cutting memory footprint proportionally.

**Basis —** Measured directly in the SpQR quantization paper, comparing quantized vs. full-precision benchmark scores.

**Do this —** Default to quantized weights for local inference of models ≥7B on consumer hardware.

_Tags: `quantization`, `deployment`, `inference`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [SpQR](https://arxiv.org/abs/2306.03078) | Jun 2023 |

</details>

<a id="claim-score-evals-on-groundedness-not-headline-f1"></a>

### Headline F1 hides scanner groundedness and precision gaps

`score-evals-on-groundedness-not-headline-f1` · confidence **0.75** · Evaluation & Benchmarks · standing since Jul 17, 2026

Headline benchmark F1 hides what actually matters for security scanning: groundedness, precision, and run-to-run stability.

**Basis —** Semgrep audited its own benchmark against real-world IDOR findings, plus a separate model's code-security eval, both showing F1 masking large groundedness/precision gaps.

**Do this —** Score scanners on groundedness and run-to-run stability as first-class metrics, and evaluate precision on repos like yours — a matching F1 can still hide a precision gap that shifts cost onto human triage. Do not expect stacking models to fix a groundedness problem.

_Tags: `evals`, `benchmarks`, `security-scanning`_

<details><summary>Evidence (5)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark) | Jul 17, 2026 |
| supports | [Kimi K3 code-security eval: matching F1 hides a precision gap](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision) | Jul 22, 2026 |
| supports | [BenchMIRT: What are LLM benchmarks actually measuring?](https://huggingface.co/blog/allenai/benchmirt) | Sep 1, 2026 |
| supports | [Semgrep Multimodal Goes Beyond Authentication](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal) | Aug 27, 2026 |
| supports | [We benchmarked A LOT of models](https://semgrep.dev/blog/2026/mythos-idor-benchmark) | Aug 25, 2026 |

</details>

<a id="claim-retrieval-quality-dominates-generation-quality-in-rag"></a>

### Retrieval quality dominates generator quality in RAG

`retrieval-quality-dominates-generation-quality-in-rag` · confidence **0.75** · Retrieval, Prompting & Context · standing since Dec 2023

In production RAG systems, retrieval quality dominates generation quality as a determinant of end-task accuracy; larger models cannot compensate for a bad retriever.

**Basis —** Synthesized from a broad academic survey of RAG systems comparing retrieval and generation as accuracy determinants.

**Do this —** Invest in retrieval evals (recall@k, reranker quality) before spending on bigger generator models.

_Tags: `rag`, `retrieval`, `evals`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Retrieval-Augmented Generation for LLMs: A Survey](https://arxiv.org/abs/2312.10997) | Dec 2023 |
| supports | [Deeper insights into retrieval augmented generation: the role of sufficient context](https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/) | May 14, 2025 |

</details>

<a id="claim-llm-as-judge-is-biased-toward-longer-answers"></a>

### LLM-as-judge is biased toward longer answers

`llm-as-judge-is-biased-toward-longer-answers` · confidence **0.75** · Evaluation & Benchmarks · standing since Jun 2023

LLM-as-judge evaluators systematically favor longer, more elaborate answers independent of quality, with bias strength varying sharply by judge model; naive judging needs an explicit length control.

**Basis —** Measured directly in the MT-Bench/Chatbot Arena LLM-judge evaluation paper, controlling for answer length against human preference.

**Do this —** Cross-check LLM-judge scores with pairwise human eval on a small sample.

_Tags: `llm-as-judge`, `eval-bias`, `evals`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | Jun 2023 |
| supports | [LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge](https://arxiv.org/abs/2506.09443) | Jun 2025 |
| supports | [Length-Controlled AlpacaEval: LLM auto-annotators favor longer outputs; regressing out length raises agreement with Chatbot Arena (0.94 to 0.98)](https://arxiv.org/abs/2404.04475) | Apr 6, 2024 |

</details>

<a id="claim-benchmark-category-labels-can-mask-conflated-capabilities"></a>

### A benchmark's stated capability category (e.g. 'safety') doesn't guarantee its score is actually driven by that capability, or even moves in the direction you'd assume — independent multidimensional decomposition (multidimensional Item Response Theory) can reveal that a nominally 'safety' benchmark like WMDP actually correlates more strongly with general reasoning than safety, and in the inverse direction (stronger reasoners score LOWER, since WMDP scores refusing/failing to answer as the desired outcome).

`benchmark-category-labels-can-mask-conflated-capabilities` · confidence **0.70** · Evaluation & Benchmarks · standing since Sep 9, 2026

**Basis —** empirical study (AllenAI BenchMIRT, multidimensional IRT across 100 models / 16 benchmarks)

**Do this —** Before citing a benchmark score as evidence of a specific capability, check whether independent capability-decomposition analysis supports that the benchmark actually isolates that capability and moves in the expected direction, rather than assuming the category label is accurate.

**Conditions —** Demonstrated specifically for WMDP and BBQ within one 16-benchmark, 100-model study; may not generalize to all benchmarks labeled 'safety'.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [BenchMIRT: What are LLM benchmarks actually measuring?](https://huggingface.co/blog/allenai/benchmirt) | Sep 1, 2026 |

</details>

<a id="claim-few-distinct-tools-beat-many"></a>

### Lean tool sets and reasoning-first prompts work best

`few-distinct-tools-beat-many` · confidence **0.70** · Agents & Harnesses · standing since Jul 21, 2026

Coding-agent harnesses work better with few distinct tools and a lean system prompt of reasoning rather than rules.

**Basis —** A first-party design account from the Claude Code team describing their own harness choices — a practitioner report, not a controlled comparison.

**Do this —** Keep the tool count small and the tools clearly distinct; write the system prompt as reasoning rather than rule lists; grow your eval suite out of real incidents; gate dangerous actions with a context-aware permission classifier rather than a static allowlist.

**Conditions —** Described from first-party practice on one coding agent, not a controlled comparison — treat as a strong prior, not a measured result.

_Tags: `harness`, `agents`, `prompting`, `evals`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [HarnessTax: How Much Does the Harness Matter for Coding Agents?](https://harnesstax.github.io/) | Sep 16, 2026 |
| supports | [How the Claude Code team designs its harness](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) | Jul 21, 2026 |

</details>

<a id="claim-tool-count-degrades-agent-performance"></a>

### Too many tools degrade agent tool-selection accuracy

`tool-count-degrades-agent-performance` · confidence **0.70** · Agents & Harnesses · standing since Jul 2023

Showing an agent more candidate tools than the task needs degrades tool-selection accuracy: short, query-adapted tool lists select better than a fixed longer list (93.1% vs 87.1% on BFCL with Claude Sonnet 4.6).

**Basis —** Measured in the ToolLLM benchmark paper, evaluating tool-selection accuracy as available tool count scales up.

**Do this —** Curate the tool set. Retire tools whose calls the eval suite shows agents get wrong more than they get right.

**Conditions —** No single universal threshold: the right list length depends on the registry and the query.

_Tags: `agents`, `harness`, `tools`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [ToolLLM](https://arxiv.org/abs/2307.16789) | Jul 2023 |
| supports | [How Many Tools Should an LLM Agent See? A Chance-Corrected Answer](https://arxiv.org/abs/2605.24660) | Jun 2026 |

</details>

<a id="claim-system-prompts-should-be-versioned-like-code"></a>

### System prompts are load-bearing config — version them like code

`system-prompts-should-be-versioned-like-code` · confidence **0.70** · Retrieval, Prompting & Context · standing since Jan 2023

Production system prompts are load-bearing configuration and should be version-controlled, code-reviewed, and evaluated on regression suites.

**Basis —** A practitioner argument treating production prompts as a security-relevant, version-controlled artifact rather than throwaway text.

**Do this —** Store prompts in the same repo as the code that calls them. Run eval on every prompt change and every model change.

**Conditions —** A practice recommendation backed by vendor guidance and first-party practice, not a controlled study.

_Tags: `prompting`, `deployment`, `regression`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Claude docs: Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Jul 2024 |
| supports | [Claude Code team: incident PRs become eval cases, and the system prompt was cut 80% as models changed](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) | Jul 21, 2026 |

</details>

<a id="claim-few-shot-prompting-brittle-on-format-changes"></a>

### Few-shot prompting is brittle to formatting choices

`few-shot-prompting-brittle-on-format-changes` · confidence **0.70** · Retrieval, Prompting & Context · standing since Feb 2021

Few-shot prompting accuracy is highly sensitive to example ordering, whitespace, and demarcation choices, in ways that look like model regressions if not controlled for.

**Basis —** Established in the 'Calibrate Before Use' paper, which measured accuracy swings from example ordering and formatting alone.

**Do this —** Freeze prompt formatting when evaluating model changes.

_Tags: `prompting`, `few-shot`, `brittleness`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Calibrate Before Use](https://arxiv.org/abs/2102.09690) | Feb 2021 |

</details>

<a id="claim-chain-of-thought-does-not-transfer-to-multi-turn"></a>

### Single-turn CoT gains don't transfer to multi-turn tasks

`chain-of-thought-does-not-transfer-to-multi-turn` · confidence **0.65** · Agents & Harnesses · standing since May 9, 2025

Single-turn benchmark gains, including from chain-of-thought reasoning, do not reliably carry over to multi-turn agent tasks: top models lose about 39% from single- to multi-turn settings, and reasoning models degrade the same way.

**Basis —** Derived from chain-of-thought reasoning research measuring the gap between single-turn benchmark gains and multi-step task performance.

**Do this —** Evaluate agents on the multi-turn task, not a single-turn proxy.

_Tags: `chain-of-thought`, `agents`, `evals`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) | May 9, 2025 |
| supports | [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) | Aug 6, 2026 |

</details>

<a id="claim-harness-evolution-gains-need-held-out-attribution"></a>

### Auto-evolved harness gains are mostly overfitting

`harness-evolution-gains-need-held-out-attribution` · confidence **0.60** · Evaluation & Benchmarks · standing since Oct 19, 2026

Gains from automatically evolving an agent harness (prompts, skills, tools, orchestration around a fixed model) are mostly search-set overfitting and extra inference compute: across 21 settings with significant gains, those two explained 54% and 14% of the gain on average, search-set gains often failed to transfer to held-out tasks, and a validation split did not prevent the overfitting.

**Basis —** single preprint: 11 executor models x 3 harness-evolution frameworks; in 21 settings with significant gains, overfitting and test-time scaling averaged 54% and 14% of the gain

**Do this —** Accept an auto-evolved harness change only on its delta over a held-out task set the optimizer never saw, measured at matched inference budget; don't trust search-set or validation-set improvement.

**Conditions —** Covers automated harness-evolution frameworks on math, coding, creativity and agentic benchmarks; the share varies widely by task, model and framework, and it says nothing about hand-engineered harness changes.

_Tags: `harness-evolution`, `evals`, `overfitting`, `test-time-compute`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) | Oct 19, 2026 |

</details>

<a id="claim-match-tool-schemas-to-the-target-model"></a>

### Model upgrades can regress on non-native tool schemas

`match-tool-schemas-to-the-target-model` · confidence **0.60** · Agents & Harnesses · standing since Jul 4, 2026

A newer SOTA model can be WORSE at your harness's custom tool schema than its older siblings — Opus 4.8 and Sonnet 5 invented fields in a third-party edit tool that older models got right — plausibly because RL training tuned them to their own harness's tools.

**Basis —** Observed directly on one third-party coding harness's custom edit-tool schema across model versions — a single reported case, not a controlled multi-harness study.

**Do this —** Match your harness's tool schemas to what the target model was trained on — Claude on str-replace-style edits, OpenAI on apply_patch — and offer a model-matched edit tool in multi-model harnesses. Re-run tool-calling evals on every model upgrade.

**Conditions —** One practitioner report on one third-party harness's edit tool; the RL-training explanation is the reporter's theory, not a measured cause.

**Replaces** [`newer-model-is-always-an-upgrade`](#claim-newer-model-is-always-an-upgrade) — Assumed newest model is a strict upgrade for any harness

_Tags: `harness`, `tool-use`, `agents`, `evals`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/) | Jul 4, 2026 |

</details>

<a id="claim-constrained-decoding-for-structured-output"></a>

### Constrained decoding wins for structured output, not TOON

`constrained-decoding-for-structured-output` · confidence **0.60** · Model I/O & Cost · standing since Feb 8, 2026

For structured model OUTPUT, constrained decoding gives the lowest token usage and plain JSON generation the best accuracy — token-optimized notations do not win here.

**Basis —** Benchmarked head-to-head on one-shot in-context generation: plain JSON had the best accuracy and constrained decoding used the fewest tokens.

**Do this —** Split the decision by direction. Use a token-optimized notation for what you feed in; use constrained decoding (or plain JSON) for what you ask the model to emit.

**Conditions —** Benchmarked on one-shot in-context generation. Constrained decoding requires a serving stack that supports it — without one, plain JSON generation is the accuracy-preserving fallback.

**Replaces** [`toon-best-for-structured-output-generation`](#claim-toon-best-for-structured-output-generation) — Assumed TOON's input savings would carry to generation

_Tags: `tokens`, `serialization`, `structured-output`, `decoding`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Feb 8, 2026 |

</details>

<a id="claim-swe-bench-doesnt-generalize-to-production-tasks"></a>

### SWE-bench scores don't predict production task performance

`swe-bench-doesnt-generalize-to-production-tasks` · confidence **0.60** · Evaluation & Benchmarks · standing since Oct 2023

SWE-bench scores do not linearly predict agent performance on production engineering tasks; the benchmark rewards a specific style of small-diff bug-fix.

**Basis —** Argued from the structure of the SWE-bench benchmark itself, which rewards a narrow small-diff bug-fix style.

**Do this —** Treat SWE-bench as one data point, not a complete picture. Build in-house evals on your task mix.

**Conditions —** Indirect evidence: SWE-bench's own scope (small issue-fix diffs in 12 Python repos) plus a randomized trial where AI tools slowed experienced developers on real tasks by 19%.

_Tags: `evals`, `swe-bench`, `benchmarks`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [SWE-bench](https://arxiv.org/abs/2310.06770) | Oct 2023 |
| supports | [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | Jul 10, 2025 |

</details>

## ⚖️ Contested

> Credible evidence on both sides. Treat these as open questions, not guidance.

<a id="claim-toon-cuts-input-tokens-vs-json"></a>

### TOON beats JSON on input-side token cost

`toon-cuts-input-tokens-vs-json` · confidence **0.55** · Model I/O & Cost · standing since Nov 2025

For large uniform arrays, TOON serializes to 30-60% fewer input tokens than JSON at comparable retrieval accuracy.

**Basis —** The format's own benchmarks (42.6% fewer tokens at 72.2% vs JSON's 71.4% retrieval accuracy) and an InfoQ write-up support the input-side saving; an independent agentic-loop benchmark found only up to 18% fewer tokens at a ~9pp accuracy cost, and a generation benchmark found the prompt tax erases the gain on short payloads.

**Do this —** Use TOON for the big uniform/tabular payloads you feed INTO the model (tool results, row sets, retrieved records). Keep JSON where data is deeply nested or irregular.

**Conditions —** Input side only, and only for uniform arrays. Nested or irregular objects show much smaller or negative gains, and on short payloads the 'prompt tax' of explaining the format to the model can erase the saving entirely. Says nothing about generation — see constrained-decoding-for-structured-output.

**Replaces** [`json-default-for-all-agent-io`](#claim-json-default-for-all-agent-io) — JSON assumed a neutral default for agent I/O

_Tags: `tokens`, `serialization`, `context`, `cost`_

<details><summary>Evidence (4)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [toon-format/toon — reference implementation, spec and benchmarks](https://github.com/toon-format/toon) | undated |
| contests | [Notation Matters: A Benchmark Study of Token-Optimized Formats in Agentic AI Systems](https://arxiv.org/abs/2605.29676) | May 28, 2026 |
| supports | [New Token-Oriented Object Notation (TOON) Hopes to Cut LLM Costs by Reducing Token Consumption](https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/) | Nov 2025 |
| contests | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Feb 8, 2026 |

</details>

<a id="claim-diff-review-catches-more-than-full-file-review"></a>

### Diff review catches more LLM-introduced defects than full-file review

`diff-review-catches-more-than-full-file-review` · confidence **0.35** · Agents & Harnesses · standing since Jul 31, 2026

Reviewing an LLM's proposed change as a diff catches more defects than reviewing the resulting full file.

**Basis —** Derived from a GitClear study on AI's impact on developer productivity, comparing defect detection across review styles.

**Do this —** Prefer tools that present LLM changes as diffs. Reviewer must sign off on the specific lines that changed.

**Conditions —** No controlled study compares diff review with full-file review for defect yield. The ledger's earlier citation for this claim was a mis-attributed paper and has been replaced.

_Tags: `code-review`, `diffs`, `coding-agents`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [From Code Review to Code Critique (ARCTIC): ranking the diff regions that most need human scrutiny beat a baseline AI reviewer 2.4x](https://arxiv.org/abs/2607.29516) | Jul 31, 2026 |
| contests | [Diff-only review misses cross-file breakage that full-repository context catches (vendor analysis)](https://www.cubic.dev/blog/why-ai-code-assistants-break-your-build-the-full-repository-context-problem) | undated |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-newer-model-is-always-an-upgrade"></a>

### ~~Assumed newest model is a strict upgrade for any harness~~

`newer-model-is-always-an-upgrade` · **superseded** on Jul 4, 2026 · had stood since Jan 2024

Swapping in the newest frontier model is a strict improvement for an existing harness.

**Why it was retired —** Measured on a third-party harness's custom edit tool, newer Claude models invented made-up fields that their older siblings got right. Model upgrades can regress harness-specific tool calling, so an upgrade is a change to re-evaluate, not a free win.

**Replaced by** [`match-tool-schemas-to-the-target-model`](#claim-match-tool-schemas-to-the-target-model) — Model upgrades can regress on non-native tool schemas

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/) | Jul 4, 2026 |

</details>

<a id="claim-json-default-for-all-agent-io"></a>

### ~~JSON assumed a neutral default for agent I/O~~

`json-default-for-all-agent-io` · **superseded** on May 2026 · had stood since Jan 2023

JSON is the natural default for all agent I/O; serialization format is not a meaningful optimization lever.

**Why it was retired —** Format choice measurably moves cost: uniform arrays serialize 30-60% smaller in TOON at comparable retrieval accuracy, which makes serialization a real optimization lever on the input side rather than an aesthetic preference.

**Replaced by** [`toon-cuts-input-tokens-vs-json`](#claim-toon-cuts-input-tokens-vs-json) — TOON beats JSON on input-side token cost

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Notation Matters: A Benchmark Study of Token-Optimized Formats in Agentic AI Systems](https://arxiv.org/abs/2605.29676) | May 2026 |

</details>

<a id="claim-toon-best-for-structured-output-generation"></a>

### ~~Assumed TOON's input savings would carry to generation~~

`toon-best-for-structured-output-generation` · **refuted** on Mar 2026 · had stood since Nov 2025

Because TOON is more token-efficient than JSON, asking the model to GENERATE TOON is also better than asking it to generate JSON.

**Why it was retired —** Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on simple structures. The input-side token saving does not transfer to the output side.

**Replaced by** [`constrained-decoding-for-structured-output`](#claim-constrained-decoding-for-structured-output) — Constrained decoding wins for structured output, not TOON

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) | Mar 2026 |

</details>

---

[← Claim index](README.md)
