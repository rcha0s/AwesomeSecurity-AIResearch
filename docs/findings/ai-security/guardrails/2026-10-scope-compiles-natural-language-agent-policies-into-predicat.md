# SCOPE compiles natural-language agent policies into predicate programs run by small models

**Published:** Oct 22, 2026

> **Takeaway:** For agent policy enforcement, prefer a compiled program of narrow predicates over one guardrail model or one LLM judge: cheaper, steadier and auditable (authors' claims, abstract only).

## TL;DR

SCOPE targets compound, application-specific policies evaluated over multi-turn transcripts and tool-call trajectories. It compiles a policy into an executable program of narrow neural predicates (small models), deterministic extractors and composing code, optimized jointly with adversarially generated counterexamples. The authors report the best average accuracy against prompt-optimization, decomposition and workflow-generation baselines, accuracy comparable to frontier reasoning models on inexpensive executors, and more stable, per-predicate interpretable verdicts. Abstract only, unreviewed arXiv v1, no numbers in the captured text.

## Lessons

- Fine-tuned guardrail classifiers are a poor fit for compound, multi-turn agent policies. - _"Fine-tuned guardrail models are efficient but degrade on compound policies"_
- LLM-as-judge enforcement is costly and gives unstable verdicts, which is a problem for a security control that must be repeatable. - _"LLM-as-a-judge approaches achieve higher accuracy, they incur high inference cost and tend to produce unstable predictions"_
- Decompose the policy into narrow predicates composed under explicit code logic instead of asking one model for one verdict. - _"compiles a policy into an executable program of neural predicates executed by small models, deterministic extractors, and code that composes their outputs"_
- A program optimized on the weakest executor transfers to other models, so the enforcement layer can run on cheap models. - _"Programs optimized with the weakest executor transfer to other models without further optimization."_
- Per-predicate outputs make each block or allow decision auditable. - _"each verdict is interpretable through the predicate outputs that produced it"_

## Threat · Conditions · Mitigations

- **Threat:** Agents violating compound application policies across multi-turn trajectories where single-shot classifiers miss and LLM judges are inconsistent.
- **Mitigations:** Express policies as explicit predicate programs with deterministic composition; run predicates on small models; log predicate outputs per verdict.

---

**Topic:** AI Security  ·  **Domain:** Guardrails & Defensive Tooling  
**Source:** [source](https://arxiv.org/abs/2610.31062)  ·  **Author:** Elad Levi et al.  ·  **Retrieved:** 2026-10-23  
**Scores:** Newness 5 · Novelty 55 · Relevance 65 · Credibility 55 · **Composite 46** _(each 0-100)_  
**Tags:** `guardrails`, `policy-enforcement`, `neurosymbolic`, `llm-as-judge`, `agent-security`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: NeMo Guardrails (Colang), LlamaGuard-style guardrail models, AgentSpec/ShieldAgent (policy-to-rule compilation), GuardAgent, DSPy-style program optimization.

_Source: [https://arxiv.org/abs/2610.31062](https://arxiv.org/abs/2610.31062)_  ·  [← back to index](../README.md)
