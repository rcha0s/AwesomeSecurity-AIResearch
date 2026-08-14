# OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality

**Topic:** AI Research  ·  **Domain:** Agents and Harnesses  
**Source:** [source](https://arxiv.org/abs/2608.05263)  ·  **Published:** Aug 7, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 46 · ✨ Novelty 60 · 🎯 Relevance 65 · 🏛️ Credibility 55 · **Composite 57.25**  
**Tags:** `multi-agent`, `orchestration`, `failure-modes`, `cascade-radius`, `routing`  
**Verification:** ✓ independently verified · closest prior art: Extends MAST (multi-agent failure taxonomy) and prior orchestration benchmarks by adding cascade radius, per-failure-mode recovery, and a failure-injection harness rather than raw task accuracy.

> **Takeaway:** Multi-agent orchestration failures are not uniform: tool faults recover, ambiguous delegation partially recovers, latent/semantic faults essentially never self-heal. Blind retry hides latent faults and delays detection, so containment requires an external trusted-state signal, not just per-agent detection. Keyword/flag routers collapse on adversarially framed inputs where an intent-reasoning router does not.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.05263) for the complete write-up._

OrchestraBench is a seed-reproducible failure-injection harness for multi-agent orchestration that introduces cascade radius and per-failure-mode recovery as primary metrics. On a 26-case diagnostic, a keyword/flag router scored 0% on adversarial cases with misleading or missing surface flags while an intent-reasoning model router scored 100%. Mechanism probes with a real Claude agent revealed three failure-handling tiers across five MAST modes: tool faults recovered fully (1.0), ambiguous delegation recovered partially (0.30), and three latent or semantic modes never recovered (0.0). Cascade radius grew from ~0.9 at depth 3 to ~4.7 at depth 7. A trusted-state ablation showed apparent containment gains came from the trusted-state signal, not autonomous detection.

## What to learn

- Latent and semantic failure modes in multi-agent pipelines are not self-healing even with retries; only tool-fault modes recover reliably. - _"tool faults recovered fully (1.0), ambiguous delegation recovered partially (0.30), and three latent or semantic modes never recovered (0.0)"_ ✅
- Keyword/flag routers fail catastrophically on adversarial inputs with misleading or missing surface flags; intent-reasoning routers do not. - _"a keyword/flag router scored 0% on adversarial cases with misleading or missing surface flags, whereas an intent-reasoning model router scored 100%, matching the oracle"_ ✅
- Blind retry masks latent faults and increases time-to-detection, so containment requires detection and attribution rather than more retries. - _"Blind retry reproduced latent faults and increased time to detection, indicating that detection and attribution are necessary for containment."_ ✅
- Apparent containment gains come from an external trusted-state signal rather than autonomous per-agent detection. - _"A trusted-state repair ablation showed that apparent containment gains primarily came from the trusted-state signal rather than autonomous detection."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Adversarial or malformed inputs at router surface flags collapse keyword-based orchestrators; latent semantic errors propagate through pipelines undetected, with cascade radius growing with depth, so a single fooled agent can silently degrade a chain of downstream agents.
- **Conditions:** Multi-agent orchestration with pipeline depth greater than 3; routing based on surface flags rather than intent; retry-only recovery without an external trusted-state or ground-truth check.
- **Mitigations:** Use intent-reasoning routers rather than keyword/flag routers; break out per-failure-mode metrics in evals; add an external trusted-state signal at agent boundaries; measure cascade radius as a first-class metric so deeper pipelines are gated on failure-attribution capability, not just accuracy.

---

_Source: [https://arxiv.org/abs/2608.05263](https://arxiv.org/abs/2608.05263)_  ·  [← back to index](../README.md)
