# PrivacyPeek: Auditing What LLM-Based Agents Acquire, Not Just What They Say

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2606.00152)  ·  **Published:** Aug 7, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 20 · ✨ Novelty 70 · 🎯 Relevance 75 · 🏛️ Credibility 52 · **Composite 56.28**  
**Tags:** `agent-privacy`, `over-acquisition`, `tool-calls`, `audit`, `benchmark`  
**Verification:** ✓ independently verified · closest prior art: Extends privacy-leakage benchmarks that audit agent outputs (e.g., PrivacyLens, ConfAIde) to also cover the acquisition (tool-call ingestion) stage with 1,182 cases across 16 domains.

> **Takeaway:** Auditing agent output for privacy misses the bigger surface: over-acquired context sits one careless action or one prompt injection away from leakage. Prompt-level defenses barely dent this; the audit needs to inspect the tool-call trajectory itself. Capability and leakage correlate, so raw capability progress will make this worse.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2606.00152) for the complete write-up._

PrivacyPeek benchmarks LLM-agent privacy leakage at the acquisition stage (what the agent pulls into its context), not just what it outputs. It contains 1,182 cases across 7 acquisition behaviors and 16 application domains. Two evaluations run on 10 agents across 4 model families: Acquisition Inspection inspects tool-call trajectories, and Probe Elicitation issues follow-up probes to measure how easily an attacker could extract acquired-but-not-disclosed data. Findings: over-acquisition is widespread, task-completion capability correlates with acquisition-stage leakage, and prompt-level defenses only reduce a small fraction of it.

## What to learn

- LLM agents systematically acquire more sensitive information than the task requires, expanding blast radius beyond what output audits catch. - _"agents often acquire more sensitive information than the task requires"_ ✅
- Prompt-level defenses reduce only a small fraction of acquisition-stage leakage. - _"Prompt-level defences reduce only a small fraction of acquisition-stage leakage, leaving the majority unmitigated."_ ✅
- Task-completion capability correlates with acquisition-stage leakage, so more-capable agents leak more, not less. - _"we observe a correlation between the task-completion capability and acquisition-stage leakage"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** LLM agents pull sensitive data (PII, credentials, private business data) into context beyond task scope; a subsequent prompt injection, careless output, or tool call exfiltrates it. Existing output-only audits miss the acquisition step.
- **Conditions:** Agent has broad tool access (email, docs, calendars); task instructions do not explicitly scope required fields; monitoring focuses on output, not on tool-call responses.
- **Mitigations:** Instrument tool-call trajectory logging plus per-call scope classification; enforce least-privilege tool schemas that return only task-relevant fields; treat acquired-but-undisclosed data as an equally-valuable leakage class in audits; do not rely on prompt-level defenses as the sole control.

---

_Source: [https://arxiv.org/abs/2606.00152](https://arxiv.org/abs/2606.00152)_  ·  [← back to index](../README.md)
