# SkillTrace: Multi-Trace Provenance Auditing for LLM-Agent Skill Reuse

**Published:** Aug 7, 2026

> **Takeaway:** Auditing reuse of agent 'skills' is not the same problem as code-clone detection: reuse can survive when only one of expression, code, or operational structure is preserved, so provenance needs multi-trace comparison across all three.

## TL;DR

SKILLTRACE audits reuse in the emerging LLM-agent 'skills' marketplace. It extracts three provenance traces (Expression = natural-language authored text, Implementation = code, Operational = a Skill Operational Graph over activation/procedure/resource-flow) and compares them deterministically against per-function negatives. On SKILLTRACE-BENCH (820 transformed positives, 751 negative controls over 100 marketplace anchors) it reaches AUROC 0.938 / F1 0.898, and a 36,446-skill wild audit produces trace-attributed review queues beyond repository-similarity baselines.

## What to learn

- Existing code-clone / package-similarity detectors miss skill reuse because reuse can preserve only one modality (text, code, or operational structure). - _"Existing detectors target single-modality source code or whole-package similarity, yet skill reuse evidence is distributed across authored text, implementation fragments, and operational structure. As a result, they can miss reuse that preserves only one part of a skill."_
- SkillTrace uses three named provenance traces plus a Skill Operational Graph for the operational trace. - _"SKILLTRACE extracts three provenance traces: Expression, Implementation, and Operational. It represents the Operational Trace as a Skill Operational Graph (SOG) that captures activation, procedure, and resource-flow structure."_
- Benchmark numbers: AUROC 0.938 / F1 0.898 on 820 positives / 751 negatives over 100 marketplace anchors, plus a 36k-skill wild audit. - _"On SKILLTRACE-BENCH, with 820 transformed reuse positives over 100 marketplace anchors and 751 negative controls, SKILLTRACE achieves AUROC 0.938 and F1 0.898. A 36,446-skill wild audit further shows that trace-attributed evidence surfaces actionable reuse review queues beyond repository-level baselines."_

## Threat · Conditions · Mitigations

- **Threat:** Reused/plagiarised or backdoored 'skill' packages laundered into a marketplace can slip past single-modality clone detectors when the attacker preserves only text, only code, or only operational structure of an original skill, breaking provenance and enabling supply-chain trust laundering.
- **Conditions:** Agent runtime that installs third-party skills as opaque packages; provenance check limited to filename, hash, or single-modality similarity; no operational-graph comparison; no calibration against same-function negatives.
- **Mitigations:** Compute Expression / Implementation / Operational traces at ingestion; store deterministic-comparable representations for later audit; calibrate against same-function strict negatives; require attributable reuse evidence before admitting a skill; queue mismatched-provenance skills for manual review.

---

**Topic:** AI Security  ·  **Domain:** Skills & Supply Chain  
**Source:** [source](https://arxiv.org/abs/2608.05204)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 62 · Relevance 60 · Credibility 55 · **Composite 49.85**  
**Tags:** `skills`, `provenance`, `supply-chain`, `clone-detection`, `agent-marketplace`  
**Verification:** ✓ independently verified · closest prior art: Code-clone detection literature (Deckard, SourcererCC, CCFinder) and package-similarity tools; SkillTrace's contribution is the multi-modality framing plus operational-graph structure specific to LLM-agent skill packages.

_Source: [https://arxiv.org/abs/2608.05204](https://arxiv.org/abs/2608.05204)_  ·  [← back to index](../README.md)
