# Decoy Direction Optimization edits open-weight models so that refusal-direction ablation removes a decoy instead of the real safety mechanism

**Published:** Sep 14, 2026

> **Takeaway:** If you ship open weights, refusal behavior is trivially removable; a cheap post-hoc decoy edit raises attacker cost but is a mitigation, not a guarantee.

## TL;DR

Refusal Feature Ablation removes a linear refusal direction from a model's activations and strips its safety behavior. The authors add a high-magnitude nonlinear decoy signal in MLP neurons (a weight edit, no finetuning) so the attacker's estimator picks a harmless direction. They report under 10% attack success under standard ablation across six model families, and Heretic weight-level attack success on Llama-3-8B-Instruct dropping from 88.7% to 18%.

## Lessons

- Open-weight safety can be bypassed cheaply by ablating one refusal direction, and trained defenses must be repeated for every checkpoint. - _"Defending against these attacks typically requires computationally expensive safety finetuning for every new checkpoint."_
- The defense misleads the attacker's estimator rather than hiding the refusal circuitry. - _"DDO actively injects a high-magnitude, nonlinear decoy signal into the network's MLP neurons."_
- Against adaptive multi-phase attacks the post-hoc edit comes at much lower cost. - _"reduces Heretic weight-level attack ASR from 88.7% to 18%, all at 30 to 450 times lower optimization cost per configuration than the trained baselines."_

## Threat · Conditions · Mitigations

- **Threat:** Refusal Feature Ablation and weight-level attacks (Heretic) remove safety behavior from open-weight models while keeping capability.
- **Conditions:** Attacker has the model weights and can estimate the refusal direction with contrastive estimators.
- **Mitigations:** Decoy Direction Optimization: post-hoc weight edit injecting a nonlinear decoy signal in MLP neurons, no base-model finetuning; still leaves 65% worst-case ASR under adaptive attacks on Llama-3-8B-Instruct.

---

**Topic:** AI Security  ·  **Domain:** Guardrails & Defensive Tooling  
**Source:** [Hugging Face Daily Papers](https://arxiv.org/abs/2609.16204)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 5 · Novelty 60 · Relevance 60 · Credibility 51 · **Composite 45** _(each 0-100)_  
**Tags:** `abliteration`, `refusal-direction`, `open-weight-models`, `weight-editing`, `safety-defense`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Nearest in pool is the Perturbation Probing entry on fragility of LLM safety; no equivalent post-hoc anti-abliteration weight-edit defense found in pool. Verifier: No equivalent in the four files; nearest is archive.json 'Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety' (loosely related). Anti-abliteration defense not covered.

_Source: [https://arxiv.org/abs/2609.16204](https://arxiv.org/abs/2609.16204)_  ·  [← back to index](../README.md)
