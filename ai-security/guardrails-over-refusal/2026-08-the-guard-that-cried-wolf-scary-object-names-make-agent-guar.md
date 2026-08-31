# The Guard That Cried Wolf: scary object names make agent guardrails over-refuse legitimate actions

**Published:** Aug 27, 2026

> **Takeaway:** Guardrails that key on scary-sounding surface labels will over-refuse legitimate work; evaluate over-safety with policy-derived benchmarks.

## TL;DR

Agent guardrails suffer over-safety: they refuse authorized, genuinely safe actions, blocking deployment. The authors build Cautious Bench, the first benchmark that makes over-safety the measured construct, codesigning each sample with a stated authorization policy and mechanically re-deriving labels. Measuring six guardrails, they find a 'name-superstition effect' - the same authorized action is over-refused more often when the object simply has a scary-looking name.

## What to learn

- Over-safety (refusing authorized, safe actions) is a real deployment blocker and must be measured against a stated authorization policy. - _"This over-safety blocks deployment when a guardrail refuses an authorized task."_
- Guardrail decisions are swayed by superficial cues - scary object names - rather than the actual authorization context. - _"the guardrails read the surface label, not the authorization context"_
- Reliable over-safety benchmarks need mechanically re-derived labels tied to policy, not per-sample annotator verdicts. - _"each label is a mechanical consequence of the policy rather than an annotator's per-sample verdict"_

## Threat · Conditions · Mitigations

- **Threat:** Not an attack: usability/availability failure where guardrails block legitimate authorized agent actions.
- **Conditions:** Guardrail evaluates an authorized action whose object bears a threatening-sounding name.
- **Mitigations:** Authorization-context-aware guardrails and policy-derived over-safety benchmarking (Cautious Bench).

---

**Topic:** AI Security  ·  **Domain:** Guardrails / Over-Refusal  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27009)  ·  **Retrieved:** 2026-08-29  
**Scores:** Newness 18 · Novelty 74 · Relevance 82 · Credibility 60 · **Composite 60.3**  
**Tags:** `guardrails`, `over-refusal`, `agent-safety`, `benchmark`, `authorization-policy`, `false-positives`  
**Verification:** ✓ independently verified · closest prior art: Prior over-refusal/exaggerated-safety studies (e.g., XSTest-style) for chat models; extends the construct to agent action guardrails with a policy-certified benchmark.

_Source: [https://arxiv.org/abs/2608.27009](https://arxiv.org/abs/2608.27009)_  ·  [← back to index](../README.md)
