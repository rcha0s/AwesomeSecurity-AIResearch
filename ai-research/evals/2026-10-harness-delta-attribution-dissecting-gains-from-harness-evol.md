# Harness-Delta Attribution: Dissecting Gains From Harness Evolution

**Published:** Oct 19, 2026

> **Takeaway:** Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.

## TL;DR

Automatic harness evolution, which optimizes the prompts, skills, tools and orchestration around a fixed model, reports gains on its search set. Harness-Delta Attribution splits those gains into overfitting, test-time scaling and a residual. Across 21 settings with significant gains, overfitting averaged 54% and extra compute 14% of the gain, gains often failed to transfer to held-out tasks, and validation signals did not prevent overfitting.

## Lessons

- Most of a harness-evolution gain is usually not generalizable improvement: on average 54% is overfitting and 14% is extra inference compute. - _"overfitting and test-time scaling account for 54% and 14% of the gain on average; their combined share exceeds 50% in 14 settings"_
- A better score on the set you optimized against is weak evidence; evolved harnesses often don't transfer to held-out tasks. - _"search-set gains often fail to transfer to held-out tasks"_
- A validation split alone does not stop harness evolution from overfitting. - _"validation-based signals are insufficient to prevent overfitting"_

---

**Topic:** AI Research  ·  **Domain:** Evaluation & Benchmarks  
**Source:** [arXiv cs.AI (Artificial Intelligence)](https://arxiv.org/abs/2610.22466)  ·  **Retrieved:** 2026-10-19  
**Scores:** Newness 19 · Novelty 65 · Relevance 87 · Credibility 44 · **Composite 57** _(each 0-100)_  
**Tags:** `harness-evolution`, `evals`, `overfitting`, `test-time-compute`, `agents`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Benchmark-overfitting and adaptive-data-analysis literature, prompt-optimization overfitting studies, and test-time-compute scaling analyses; the delta is a quantified decomposition applied to harness evolution across 11 models and 3 frameworks.

_Source: [https://arxiv.org/abs/2610.22466](https://arxiv.org/abs/2610.22466)_  ·  [← back to index](../README.md)
