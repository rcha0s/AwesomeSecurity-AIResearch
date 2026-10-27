# Guardrail safety benchmarks mostly measure the training label policy

**Published:** Oct 18, 2026

> **Takeaway:** A guardrail's benchmark numbers are uninterpretable unless you know the 'unsafe' definition it was trained and graded on, its contamination, and its seed variance. Evaluate any vendor guardrail against your own policy.

## TL;DR

In one industrial deployment, the same ~53k prompts were labelled twice: once for 'is this a request for harmful content?' and once for 'would a moderator block this?'. The authors trained ten guardrail arms on these labels with the same architecture and optimizer family. Two over-refusal benchmarks were already 82-88% present in the training pools. Some benchmarks such as HarmBench-copyright swing 0-100 purely with the label policy, while detection capability stays the same. Validation accuracy tracked agreement with the annotators' policy (rho=+0.74), not detection capability (rho=+0.34). Soft labels from a distilled teacher can carry the teacher's policy even when every hard label carries the other one.

## Lessons

- Over-refusal benchmarks that guardrails cite to show they don't over-block were largely already in the training data. - _"JailbreakBench-benign is 88% and OR-Bench-hard 82% present in the training pools"_
- How much the label definition swings scores differs by benchmark, by about 23x, so some benchmarks mostly measure policy and others capability. - _"the range across the ten arms is 0.99 on HarmBench-copyright and 0.043 on WildGuard-benign, a 23x spread"_
- Distillation leaks policy: soft labels from the teacher override the hard labels, so the policy embedded in a released checkpoint can be undocumented. - _"so teacher provenance is an unrecorded confound in any released checkpoint"_
- Proposed reporting standard for guardrail evaluations. - _"We argue that guardrail evaluations should report contamination, a seed floor and the definition they were graded against as first-class variables."_

---

**Topic:** AI Security  ·  **Domain:** Guardrails & Defensive Tooling  
**Source:** [Hugging Face Daily Papers](https://arxiv.org/abs/2610.25060)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 23 · Novelty 62 · Relevance 78 · Credibility 51 · **Composite 55** _(each 0-100)_  
**Tags:** `guardrails`, `safety-benchmarks`, `label-policy`, `benchmark-contamination`, `over-refusal`, `eval-methodology`, `distillation`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The pool's closest entries are the WMDP/BBQ IRT entry behind the benchmark-category-labels claim (safety benchmarks track reasoning) and the archive over-safety benchmark entry ('Test guardrails for name-superstition over-refusal', policy-derived labels). This paper adds a controlled natural experiment: same prompts, two label policies, fixed architecture. It shows that policy, contamination, and teacher soft labels drive guardrail benchmark scores while detection capability stays the same.

_Source: [https://arxiv.org/abs/2610.25060](https://arxiv.org/abs/2610.25060)_  ·  [← back to index](../README.md)
