# Guardrail benchmark scores mostly measure the training labels' definition of unsafe

**Published:** Oct 18, 2026

> **Takeaway:** Before picking a guardrail classifier by benchmark score, ask which policy its labels encode, whether the benchmark leaked into training, and what the seed-to-seed variance is, or you are comparing policies, not detection quality.

## TL;DR

An industrial deployment labelled the same ~53k prompts twice, once as 'is this a request for harmful content?' and once as 'would a moderator block this?'. The authors trained ten guardrail arms at two scales with the same architecture, codebase and optimiser family. Two over-refusal benchmarks, JailbreakBench-benign and OR-Bench-hard, were 88% and 82% present in the training pools. After decontamination, the label policy alone moved HarmBench-copyright across 0-100 and OR-Bench-hard over-refusal across 3.4-56.4%, while detection capability stayed unchanged.

## Lessons

- Guardrail training corpora can already contain the over-refusal benchmarks that vendors report to show they don't over-block. - _"JailbreakBench-benign is 88% and OR-Bench-hard 82% present in the training pools"_
- Benchmarks differ in how sensitive they are to the label definition. Some mostly measure policy, others mostly measure the model. - _"the range across the ten arms is 0.99 on HarmBench-copyright and 0.043 on WildGuard-benign, a 23x spread"_
- A tiny parameter change carrying a different policy can move a benchmark score across its whole range. - _"a benchmark score can be moved across its entire range by 0.03% of the parameters"_
- In a distilled guardrail, the teacher's soft labels carry the teacher's policy even when every hard label carries the other policy. Released checkpoints do not record which teacher was used. - _"so teacher provenance is an unrecorded confound in any released checkpoint"_

## Threat · Conditions · Mitigations

- **Threat:** Teams pick or certify a guardrail on scores that reflect contamination and the labelling policy rather than detection ability. The deployed filter then over-blocks or under-blocks against their actual policy.
- **Conditions:** The guardrail is chosen by public safety or over-refusal benchmark scores, without disclosure of the training label definition, the overlap between benchmarks and training data, or the teacher model behind a distilled checkpoint.
- **Mitigations:** Require guardrail evaluations to report contamination, a seed floor and the policy they were graded against, and validate on a set labelled under your own policy before deployment.

---

**Topic:** AI Security  ·  **Domain:** Guardrails & Defensive Tooling  
**Source:** [NeurIPS (via arXiv)](http://arxiv.org/abs/2610.25060v1)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 7 · Novelty 55 · Relevance 75 · Credibility 72 · **Composite 52** _(each 0-100)_  
**Tags:** `guardrail-classifier`, `safety-benchmarks`, `benchmark-contamination`, `over-refusal`, `label-policy`, `distillation`, `eval-validity`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Nearest pool entries: DecisionPivot (ai-research), where guardrail and router models with near-equal accuracy diverge on contrast pairs, and the benchmark-contamination entry 'Zero Gap Is Not Restoration' (archive). The delta is a natural experiment with double-labelled data that isolates label policy from capability, plus measured contamination of over-refusal benchmarks inside a guardrail's own training data.

_Source: [http://arxiv.org/abs/2610.25060v1](http://arxiv.org/abs/2610.25060v1)_  ·  [← back to index](../README.md)
