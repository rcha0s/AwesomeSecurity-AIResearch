# The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses

**Topic:** AI Security  ·  **Domain:** Prompt Injection & Adversarial  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27092)  ·  **Published:** Aug 27, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 80 · 🎯 Relevance 92 · 🏛️ Credibility 60 · **Composite 65.6**  
**Tags:** `prompt-injection`, `data-exfiltration`, `tool-using-agents`, `allow-list`, `capability-isolation`, `secalign`  
**Verification:** ✓ independently verified · closest prior art: SecAlign (CCS 2025), channel-separation and output-normalization defenses, AgentDojo-style injection benchmarks; contribution is the framing-gap characterization and payload-blind mitigations.

> **Takeaway:** Don't rely on the acting model to recognize injection; constrain where data can go and isolate the capability that can send it.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.27092) for the complete write-up._

Overt injection to exfiltrate a secret is refused (gpt-4o 0%), but reframing the identical leak as a mandatory 'integrity signature', config field, or look-alike trusted host drives success to 100%. The reusable asset is the template, not the mechanism, and the root cause is instruction/data confusion rather than defeated alignment. Only payload-blind controls - destination allow-lists and a planner/reader capability split - close the gap; SecAlign fine-tuning, channel separation, and output-normalizing guards do not.

## What to learn

- Attacks the model refuses when overt succeed fully when reframed as benign-sounding requirements - alignment does not recognize the semantics. - _"reframing the identical leak as a mandatory integrity signature, config field, or look-alike "trusted" host drives gpt-4o 0% to 100%"_ ✅
- The reusable attack asset is a template, so paraphrase and field-swap make injection cheap to scale. - _"the reusable asset is the template, not the mechanism"_ ✅
- Only payload-blind architectural controls - destination allow-lists and planner/reader capability isolation - reliably stop exfiltration. - _"What closes the gap is payload-blind checks: a destination allow-list (0%, when destinations are closed) and a capability-isolating planner/reader split (0%)."_ ✅
- Fine-tuning defenses, channel separation, and output normalization all fail against reframing or held-out encodings like ROT13. - _"an output-normalizing guard loses to a held-out encoding (ROT13, 100%)"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Indirect prompt-injection exfiltration of a held secret via semantically reframed leak requests.
- **Conditions:** Tool-using LLM agent holds a secret and processes attacker-controlled web content with an open outbound channel.
- **Mitigations:** Closed destination allow-lists and capability-isolating planner/reader split; surface-level model defenses are inadequate.

---

_Source: [https://arxiv.org/abs/2608.27092](https://arxiv.org/abs/2608.27092)_  ·  [← back to index](../README.md)
