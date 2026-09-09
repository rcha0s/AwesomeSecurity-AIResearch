# Multidimensional Item-Response-Theory Auditing Reveals Some 'Safety' Benchmarks Are Actually Measuring General Reasoning

**Published:** Sep 1, 2026

> **Takeaway:** A benchmark's stated purpose (e.g. "safety") doesn't guarantee its score is actually driven by that capability, or even in the direction you'd assume - a model that scores well on WMDP's dual-use-knowledge "safety" metric may just be a weaker reasoner that couldn't produce the dangerous answer anyway, not one that made a deliberate safety-aligned choice, so treating the raw score as a safety signal is misleading.

## TL;DR

AllenAI's BenchMIRT applies multidimensional Item Response Theory to 100 LLMs across 16 benchmarks and 34,000+ questions to independently discover which latent capabilities actually drive a benchmark's score, without being told the benchmarks' intended categories. It found that WMDP - a benchmark for dangerous dual-use knowledge, commonly treated as a safety metric - correlates more strongly with general reasoning ability than with safety, and in the opposite direction from what you'd expect: stronger-reasoning models score LOWER on WMDP, because the benchmark counts refusing or failing to produce the dangerous knowledge as the 'safe' desired response.

## What to learn

- BenchMIRT independently recovered exactly two dominant capability dimensions (safety and general reasoning) across 16 mixed benchmarks without being told which benchmark measured which, and the result was stable across repeated from-scratch analyses. - _"Crucially, we didn’t tell BenchMIRT which benchmarks were measuring which capabilities. It independently recovered two dominant dimensions: safety and general reasoning. When we repeated our analysis from scratch, those same two dimensions emerged each time, suggesting the result was stable rather than specific to one analysis."_
- WMDP, a benchmark for dangerous dual-use knowledge commonly grouped with safety benchmarks, was found by BenchMIRT to correlate more strongly with general reasoning than with safety - and counterintuitively, stronger reasoning is associated with LOWER WMDP scores, because the benchmark treats refusing or failing to produce the dangerous knowledge as the desired 'safe' response, so a better reasoner is more likely to actually produce the (unsafe) correct answer. - _"WMDP behaves differently from most safety benchmarks. It tests dangerous dual-use knowledge in areas such as biology, chemistry, and cybersecurity - for example, knowledge that could help someone misuse a biological agent or exploit a computer system. BenchMIRT found that WMDP scores were more strongly associated with general reasoning than with safety."_
- The direction of the WMDP/reasoning relationship is counterintuitive: stronger general reasoning is associated with LOWER (not higher) WMDP scores, since the benchmark scores refusing or failing to provide the dangerous knowledge as the desired outcome. - _"Stronger general reasoning, however, was associated with lower WMDP scores, because the benchmark counts refusing or failing to provide the dangerous knowledge as the desired response."_
- BBQ, a bias-focused benchmark also commonly grouped with safety metrics, was likewise found to align more strongly with general reasoning, meaning a low BBQ score may partly reflect reasoning difficulty rather than a genuine safety/bias failure. - _"BBQ, which evaluates social bias and is commonly grouped with safety benchmarks, aligned much more strongly with general reasoning in BenchMIRT’s analysis. That means a low BBQ score may partly reflect difficulty understanding or reasoning through certain questions, rather than safety behavior alone."_

---

**Topic:** AI Security  ·  **Domain:** LLM Red-Teaming  
**Source:** [source](https://huggingface.co/blog/allenai/benchmirt)  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 63 · Novelty 65 · Relevance 62 · Credibility 80 · **Composite 65.85**  
**Tags:** `evals`, `benchmarks`, `item-response-theory`, `safety-evals`, `wmdp`  
**Verification:** ✓ independently verified · closest prior art: AllenAI's own prior single-dimensional 'Fluid Benchmarking' work and the IRT-for-benchmark-compression line (Polo et al.'s tinyBenchmarks) are close prior art for the methodology.

_Source: [https://huggingface.co/blog/allenai/benchmirt](https://huggingface.co/blog/allenai/benchmirt)_  ·  [← back to index](../README.md)
