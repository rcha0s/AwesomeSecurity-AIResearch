# SEAL: A Router-Independent 'Shared Expert' Anchor Cuts Jailbreak Success on Mixture-of-Experts Models by Up to 60%

**Published:** Sep 2, 2026

> **Takeaway:** Router-hardening defenses for MoE model safety can still be bypassed because routing itself is nondeterministic and manipulable - anchoring safety to the always-activated shared-expert component instead sidesteps that uncertainty entirely, since it's not subject to the same routing-path manipulation.

## TL;DR

A CCS 2026 paper identifies that Mixture-of-Experts (MoE) LLM safety is structurally vulnerable because it hinges on which sparse experts get activated per token, and adversaries can subvert routing via jailbreak prompts, malicious fine-tuning, or pruning safety-critical neurons - defenses that only harden the router can still be bypassed since routing is nondeterministic. SEAL instead trains a plug-and-play adapter on the always-activated shared-expert component (which holds a small proportion of safety-critical neurons) as a router-independent safety anchor, reducing attack success rate by up to 60% across six attack scenarios at a capability cost of at most 1.4%.

## What to learn

- MoE safety is structurally tied to which sparse experts activate per token, and existing router-hardening defenses can still be bypassed because an adversary can manipulate or evade the routing trajectory itself, given its nondeterministic nature. - _"MoE safety hinges on which experts are activated, and adversaries can subvert this selection through jailbreak prompts, malicious fine-tuning, and weight-level pruning of safety-critical neurons. Existing defenses primarily focus on hardening the router, but an adversary may still manipulate or bypass the routing trajectory due to the routing process's nondeterministic nature, thereby collapsing the defense."_
- SEAL anchors safety to the shared expert - a component that is always activated regardless of routing decisions and already holds a small proportion of safety-critical neurons - making it a router-independent defense point that sidesteps the routing-manipulation problem entirely. - _"shared expert, an always-activated component containing a small proportion of safety-critical neurons, can overcome the uncertainty of sparsely activated routing path and serve as a router-independent anchor to enhance global safety alignment."_
- Across six attack scenarios combining three adversarial input types (harmful prompting, jailbreak, malicious fine-tuning) with and without neuron pruning, SEAL reduced attack success rate by up to 60% at a capability cost of at most 1.4% on a five-benchmark average. - _"We evaluate SEAL and SEAL++ across six attack scenarios that combine three adversarial inputs (harmful prompting, jailbreak, malicious fine-tuning) with and without neuron pruning."_

---

**Topic:** AI Security  ·  **Domain:** LLM Red-Teaming  
**Source:** [source](http://arxiv.org/abs/2609.02293v1)  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 63 · Novelty 65 · Relevance 55 · Credibility 72 · **Composite 62.55**  
**Tags:** `mixture-of-experts`, `jailbreak-defense`, `alignment`, `ccs2026`, `safety-training`  
**Verification:** ✓ independently verified · closest prior art: Router-hardening defenses for MoE jailbreaks (the paper's own contrasted baseline) and general dense-model safety-alignment/circuit-breaker techniques; MoE-specific shared-expert anchoring is this paper's distinct contribution.

_Source: [http://arxiv.org/abs/2609.02293v1](http://arxiv.org/abs/2609.02293v1)_  ·  [← back to index](../README.md)
