# When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses

**Published:** Aug 27, 2026

> **Takeaway:** How a harness assembles context is a privilege boundary; if it can promote untrusted data, model-side instruction hierarchy provides little protection.

## TL;DR

Model-side instruction hierarchy assigns privilege by source, but the agent harness reassembles context each turn and can silently promote low-privilege attacker content into a higher instruction level. The authors call this 'instruction privilege escalation' and achieve all 13 attack objectives (confidentiality, integrity, availability, RCE) across six coding-agent harnesses, even under automatic permission review.

## What to learn

- Instruction-hierarchy defenses can be defeated at the harness layer, before the model even sees the content, by promoting untrusted input to a higher privilege tier. - _"This construction can elevate low-level content to a higher instruction level and grant it greater model-facing privilege."_
- Automatic permission review is not a sufficient backstop against privilege escalation in agent harnesses. - _"Under automatic permission review, the attacks achieve all 13 objectives on all three harnesses that provide this mode."_
- Persistent goals and scheduled tasks provided by a harness are additional vectors for the same escalation. - _"We further reproduce the vulnerability using harness-provided persistent goals and scheduled tasks."_

## Threat · Conditions · Mitigations

- **Threat:** Attacker-controlled low-privilege content is promoted to trusted instruction level, enabling confidentiality/integrity/availability/RCE compromise.
- **Conditions:** Agent harness ingests attacker-influenced content and reconstructs it into higher-trust context regions across six evaluated coding harnesses.
- **Mitigations:** Provenance-preserving context assembly and boundaries that prevent relabeling of untrusted input; permission review alone is insufficient.

---

**Topic:** AI Research  ·  **Domain:** Agents / Harnesses  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27299)  ·  **Retrieved:** 2026-08-29  
**Scores:** Newness 20 · Novelty 82 · Relevance 90 · Credibility 60 · **Composite 65.6**  
**Tags:** `llm-agents`, `harness-security`, `instruction-hierarchy`, `privilege-escalation`, `coding-agents`, `prompt-injection`  
**Verification:** ✓ independently verified · closest prior art: Builds on instruction-hierarchy defenses (e.g., OpenAI instruction hierarchy) and indirect prompt injection; novel framing is escalation via harness context construction.

_Source: [https://arxiv.org/abs/2608.27299](https://arxiv.org/abs/2608.27299)_  ·  [← back to index](../README.md)
