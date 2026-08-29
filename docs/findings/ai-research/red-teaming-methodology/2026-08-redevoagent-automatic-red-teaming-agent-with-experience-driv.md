# RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution

**Topic:** AI Research  ·  **Domain:** Red-Teaming Methodology  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27439)  ·  **Published:** Aug 27, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 72 · 🎯 Relevance 80 · 🏛️ Credibility 60 · **Composite 59.6**  
**Tags:** `red-teaming`, `jailbreak`, `llm-agents`, `harness-security`, `skill-evolution`, `black-box`  
**Verification:** ✓ independently verified · closest prior art: Fixed-attack automatic red-teaming and agentic attackers using trajectory-based retrieval; contribution is skill distillation with Deciding-Tool Attribution and a validation ratchet.

> **Takeaway:** Effective automated red-teaming of agent harnesses should evolve reusable, attributable attack skills rather than replay fixed attacks or full trajectories.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.27439) for the complete write-up._

Because LLM agents in product execution harnesses turn jailbreaks into harmful tool use and persistent state changes, red-teaming must target harnesses, not just text output. RedEvoAgent is a black-box red-teaming agent that distills cross-case attack trajectories into a concise human-readable 'attack skill' which evolves via tool-effectiveness profiling, Deciding-Tool Attribution, and a validation ratchet that keeps only improving updates.

## What to learn

- In agent harnesses jailbreaks are more dangerous than in chat because they cause real tool use and durable state changes. - _"jailbreaks can trigger harmful tool use and persistent state changes, creating greater risks than unsafe text generation alone"_ ✅
- Distilling attack experience into a compact, human-readable skill beats retrieving full trajectories, which suffer retrieval bias and unclear tool credit. - _"distills cross-case attack trajectories into a concise, human-readable attack skill"_ ✅
- A validation ratchet that only keeps improving updates prevents skill regression during evolution. - _"a validation ratchet that retains only updates improving validation performance"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Adaptive jailbreaks that trigger harmful tool actions and persistent state changes in deployed agent harnesses.
- **Conditions:** Black-box access to target LLM agents deployed in product execution harnesses.
- **Mitigations:** Defensive use for continuous harness red-teaming and coverage measurement.

---

_Source: [https://arxiv.org/abs/2608.27439](https://arxiv.org/abs/2608.27439)_  ·  [← back to index](../README.md)
