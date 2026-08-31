# Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety

**Published:** Aug 28, 2026

> **Takeaway:** LLM refusal safety lives in a razor-thin neural layer, so external guardrails and a measurable fragility score are essential rather than optional.

## TL;DR

Unit 42 introduces 'perturbation probing', a two-forward-pass method that pinpoints the tiny set of feed-forward neurons carrying an aligned LLM's refusal behavior. On Qwen3-4B, just 50 of 350,208 neurons (~0.014%) control the safety refusal template, and removing them breaks refusal formatting on 80% of harmful prompts. A derived FFN/Skip ratio predicts 81% of the variance in each model's steerability, offering a quantitative safety fragility score.

## What to learn

- An aligned model's refusal behavior can be concentrated in a vanishingly small number of neurons, making it fragile to internal manipulation or even routine fine-tuning. - _"just 50 neurons out of 350,208 - about 0.014% of the model's feed-forward neurons - control the safety refusal template"_
- Model-internal alignment is a thin layer, not a robust distributed defense, so it should not be the only safety control. - _"It lives in a thin template layer - a tiny fraction of the network that an attacker who can manipulate internals could disable"_
- Defenders must layer external filters and runtime guardrails on top of the base model's built-in safety. - _"True AI safety demands a defense-in-depth strategy, with external content filters and runtime guardrails layered on top of whatever the base model was trained to do"_
- A cheap computable metric can predict how easily a model's safety can be steered, enabling pre-deployment fragility scoring without full red-team campaigns. - _"this ratio explained 81% of the variance in how vulnerable each model's safety behavior was to a small targeted change"_

## Threat · Conditions · Mitigations

- **Threat:** Safety alignment can be disabled or shifted by altering a tiny neuron set or via ordinary optimization runs.
- **Conditions:** Anyone deploying open-weight or fine-tunable aligned LLMs where model internals or fine-tuning can be influenced.
- **Mitigations:** Defense-in-depth: external content filters, runtime guardrails, and fragility scoring before deployment.

---

**Topic:** AI Security  ·  **Domain:** LLM Safety / Alignment Robustness  
**Source:** [Unit 42 (Palo Alto Networks)](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/)  ·  **Retrieved:** 2026-08-29  
**Scores:** Newness 18 · Novelty 72 · Relevance 72 · Credibility 77 · **Composite 59.22**  
**Tags:** `llm-safety`, `jailbreak`, `alignment`, `mechanistic-interpretability`, `guardrails`, `defense-in-depth`  
**Verification:** ✓ independently verified · closest prior art: Unit 42 logit-gap steering research; broader RLHF-refusal and mechanistic-interpretability work

_Source: [https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/)_  ·  [← back to index](../README.md)
