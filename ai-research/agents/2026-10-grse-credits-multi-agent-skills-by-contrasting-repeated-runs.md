# GRSE credits multi-agent skills by contrasting repeated runs, not presence

**Published:** Oct 19, 2026

> **Takeaway:** If your harness edits skills automatically, assign credit by comparing repeated runs (group-relative), not by co-occurrence with success, or harmful skills will survive.

## TL;DR

Multi-agent teams that improve by revising reusable skills need to know which agent's skill caused a shared team reward. Existing methods credit any skill that appears in a successful trajectory, so a harmful skill can still earn positive credit. GRSE borrows the idea from GRPO: it runs each question several times with the same skill libraries and contrasts the runs to credit agent-skill pairs, with structured failure diagnosis. It beats MASkills on HotpotQA and on every LoCoMo category except open-domain (up to +6.7 F1 on multi-hop). Starting from a library with planted harmful skills, it assigns the right sign to every one and recovers clean-library performance; MASkills misattributes two of them.

## Lessons

- Crediting skills by co-occurrence is broken: a skill that hurts can still get rewarded if it shows up in successful runs. - _"presence is not responsibility: a harmful skill active in successful runs still earns positive credit"_
- Mechanism: repeat each question under identical libraries and contrast the outcomes to attribute credit, as in GRPO. - _"it executes each question several times under the same skill libraries and contrasts the executions to credit agent--skill pairs"_
- Contrastive credit makes self-evolution robust to poisoned skill libraries, where presence-based credit gets worse than where it started. - _"starting from planted harmful skills, it credits every planted skill with the correct sign and recovers the score of a clean library (+6.3points), whereas MASkills misattributes two and falls below its starting point."_
- The authors attribute the gains to better-grounded retrieval rather than unsupported answers. - _"Its gains rest on better-grounded retrieval rather than answers given without evidence"_

---

**Topic:** AI Research  ·  **Domain:** Agents & Harnesses  
**Source:** [Hugging Face Daily Papers](https://arxiv.org/abs/2610.27227)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 7 · Novelty 58 · Relevance 65 · Credibility 51 · **Composite 46** _(each 0-100)_  
**Tags:** `skill-evolution`, `credit-assignment`, `multi-agent`, `self-improving-agents`, `skill-poisoning`, `grpo`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The archive has 'Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?' (per-skill contribution eviction, judge false-pass threshold) and 'Pre-Commit Gating against Skill Contamination' (verifier gatekeeper). GRSE differs by solving multi-agent credit assignment with GRPO-style contrastive reruns instead of judge or verifier gating, and shows it recovers from planted harmful skills. The evidence here is abstract-level only.

_Source: [https://arxiv.org/abs/2610.27227](https://arxiv.org/abs/2610.27227)_  ·  [← back to index](../README.md)
