# SkillShield: Prompt-Space Security Skills for LLM Coding Agents

**Published:** Aug 26, 2026

> **Takeaway:** API-only deployers can harden coding agents with offline-synthesized, always-on system-prompt security skills instead of extra runtime classifiers.

## TL;DR

A coding agent runs shell commands and edits files with developer privileges, so malicious requests become real harmful actions; weight-level alignment isn't available to API-only deployers and monitors need extra classifiers. SkillShield synthesizes security 'skills' offline from known attacks or recorded failures and injects them into the system prompt for the whole tool-use loop, needing no runtime classification. On RedCode it cuts harmful-generation severity from 3.37 to 0.58 and matches Llama Guard 3 without a separate 8B classifier, at a 0.14% benign refusal rate.

## What to learn

- Coding agents are high-risk because malicious prompts become privileged file and shell actions. - _"allowing malicious requests to translate directly into harmful actions"_ ✅
- System-prompt security skills can approximate a guardrail classifier's protection without a separate model on the trajectory. - _"comparable to Llama Guard 3's 42.7% without its separate 8B classifier"_ ✅
- Prompt-space defenses can be tuned to strong protection with very low benign over-refusal. - _"SkillShield yields a mean safety-refusal rate of 0.14%"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Malicious or jailbroken requests driving a privileged coding agent to perform harmful actions.
- **Conditions:** API-only coding-agent deployment without access to model weights or an auxiliary guard model.
- **Mitigations:** Offline-synthesized security skills injected into the system prompt and active across the tool-use loop.

---

**Topic:** AI Security  ·  **Domain:** Coding Agents / Prompt-Space Defense  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.25817)  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 70 · 🎯 Relevance 84 · 🏛️ Credibility 60 · **Composite 60.2**  
**Tags:** `coding-agents`, `system-prompt-defense`, `redcode`, `llama-guard`, `guardrails`  
**Verification:** ✓ independently verified · closest prior art: Weight-level alignment, input filters, execution-boundary monitors, and Llama Guard 3; contribution is a classifier-free prompt-space skill defense evaluated on RedCode.

_Source: [https://arxiv.org/abs/2608.25817](https://arxiv.org/abs/2608.25817)_  ·  [← back to index](../README.md)
