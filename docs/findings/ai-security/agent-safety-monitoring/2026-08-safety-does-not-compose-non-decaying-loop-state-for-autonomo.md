# Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents

**Published:** Aug 27, 2026

> **Takeaway:** Agent safety must accumulate state across the whole loop; per-trajectory monitors that reset each iteration are blind to slow, fragmented attacks.

## TL;DR

Autonomous agents run as loops but their safety monitors are scoped to a single trajectory and reset each iteration, so attacks whose evidence is fragmented across iterations are invisible - the authors prove a trajectory-scoped monitor's true-positive rate equals its false-positive rate. A decaying risk score doesn't help because a patient adversary's cooling-off wait is constant. LoopHarness maintains persistent, non-decaying loop-level safety state and bounds unauthorized irreversible actions by a constant independent of horizon N.

## What to learn

- Single-trajectory safety monitors provably cannot detect attacks whose evidence spans multiple agent iterations. - _"every trajectory-scoped monitor has a true-positive rate equal to its false-positive rate"_ ✅
- A geometrically decaying risk score does not fix this because a patient attacker only needs a constant cooling-off wait. - _"the cooling-off period a patient adversary must wait is a constant that does not grow with the horizon N"_ ✅
- Persistent, non-decaying loop-level safety state can bound unauthorized irreversible actions by a constant independent of horizon. - _"it bounds the expected number of unauthorized irreversible actions by a constant in N"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Patient adversary spreads attack evidence across many iterations to stay under per-trajectory monitor thresholds.
- **Conditions:** Autonomous agent runs unattended loops with safety state reset at each new trajectory.
- **Mitigations:** Persistent non-decaying loop-level safety state with mediated commits and a model-free action bound.

---

**Topic:** AI Security  ·  **Domain:** Agent Safety / Monitoring  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27141)  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 84 · 🎯 Relevance 86 · 🏛️ Credibility 60 · **Composite 65.0**  
**Tags:** `agent-safety`, `autonomous-agents`, `monitoring`, `cross-iteration-attacks`, `irreversible-actions`, `loopharness`  
**Verification:** ✓ independently verified · closest prior art: Trajectory-scoped agent monitors and Agent-SafetyBench; contribution is the impossibility separation and non-decaying loop-level state (LoopHarness).

_Source: [https://arxiv.org/abs/2608.27141](https://arxiv.org/abs/2608.27141)_  ·  [← back to index](../README.md)
