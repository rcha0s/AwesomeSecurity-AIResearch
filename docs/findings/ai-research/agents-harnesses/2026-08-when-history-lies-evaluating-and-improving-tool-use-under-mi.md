# When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories

**Published:** Aug 7, 2026

> **Takeaway:** History reliability is a distinct tool-use bottleneck: harnesses that just accumulate turns are silently letting old, wrong state overwrite the current task.

## TL;DR

Stale-but-plausible tool traces in a persistent agent history hijack the model even when the current request is unchanged. On Qwen3-1.7B, polluted history flips 32.1% of decisions that were correct under the original trajectory. A teacher-student distillation from an oracle-state policy recovers most of the lost accuracy and transfers across models and benchmarks.

## What to learn

- Structurally-valid but stale history is enough to flip roughly a third of an agent's tool-use decisions on Qwen3-1.7B, primarily via reuse of corrupted entities or old interface conventions. - _"on Qwen3-1.7B, pollution flips 32.1% of decisions that are correct under the original trajectory and frequently induces reuse of corrupted entities or interface conventions"_
- The paper isolates the failure modes with paired Original/Polluted/Oracle views and eleven gold-preserving interventions covering decision state, entity binding, and interface execution. - _"Eleven gold-preserving interventions isolate failures in decision state, entity binding, and interface execution across complete calls and non-call decisions"_
- Reliable-state policy transfer (soft supervision on student-generated prefixes from an oracle-conditioned teacher) beats Gold-SFT, oracle-sequence distillation, and off-policy token distillation and transfers to unseen functions and external tool-use benchmarks. - _"ours achieves 87.0% Balanced Tool-Use Accuracy, outperforming Gold-SFT (66.3%), Oracle sequence distillation (82.3%), and off-policy token distillation (85.0%)"_

---

**Topic:** AI Research  ·  **Domain:** Agents & Harnesses  
**Source:** [source](https://arxiv.org/abs/2608.06057)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 78 · Relevance 82 · Credibility 55 · **Composite 61.25**  
**Tags:** `tool-use`, `multi-turn`, `agent-evals`, `history-poisoning`, `distillation`  
**Verification:** ✓ independently verified · closest prior art: Multi-turn tool-use benchmarks (BFCL, ToolBench) test accuracy but not history reliability. Related but distinct: memory-poisoning threat models on long-term agent memory and 'lost-in-the-middle' long-context degradation. The oracle-teacher / polluted-student distillation formulation is novel to this paper.

_Source: [https://arxiv.org/abs/2608.06057](https://arxiv.org/abs/2608.06057)_  ·  [← back to index](../README.md)
