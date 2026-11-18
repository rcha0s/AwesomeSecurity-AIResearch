# DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs

**Published:** Oct 20, 2026

> **Takeaway:** Evaluate routers and guardrail judges on paired contrast cases, not only item accuracy.

## TL;DR

DecisionPivot benchmarks the decision models used for routing, guardrails and output verification in LLM systems, with 48 tasks and 40,033 items, including contrast groups whose answers come from independent solvers. Two 27B models 2.6 points apart on aggregate score reach 70.1% vs 44.2% contrast-group accuracy, and one model ranks the positive item above the negative in 92.3% of pairs but answers both correctly in only 74.1%. Reasoning-effort settings also move accuracy substantially.

## Lessons

- Aggregate accuracy can hide large differences in whether a decision model gets controlled variations right. - _"two 27B models separated by only 2.6 points on the reference track achieve contrast-group accuracies of 70.1% and 44.2%"_
- Ranking the positive above the negative is not the same as deciding both correctly; threshold-based use needs decision-level evaluation. - _"exposing a gap between probability ordering and decision correctness"_
- The reasoning-effort setting is a material variable for decision-model accuracy and must be pinned in evals. - _"compared with 81.5% at its lowest effort"_

---

**Topic:** AI Research  ·  **Domain:** Evaluation & Benchmarks  
**Source:** [source](https://arxiv.org/abs/2610.28522)  ·  **Retrieved:** 2026-10-22  
**Scores:** Newness 7 · Novelty 55 · Relevance 65 · Credibility 55 · **Composite 46** _(each 0-100)_  
**Tags:** `evals`, `guardrails`, `routing`, `llm-as-judge`, `calibration`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Contrast sets (Gardner et al. 2020) and CheckList-style minimal-pair testing; judge/reward-model benchmarks (RewardBench). Applying contrast groups to router and guardrail decision models is the variation.

_Source: [https://arxiv.org/abs/2610.28522](https://arxiv.org/abs/2610.28522)_  ·  [← back to index](../README.md)
