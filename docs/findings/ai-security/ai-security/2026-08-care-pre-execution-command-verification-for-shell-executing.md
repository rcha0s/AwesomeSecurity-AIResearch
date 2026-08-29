# CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2607.21642)  ·  **Published:** Aug 7, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 20 · ✨ Novelty 60 · 🎯 Relevance 75 · 🏛️ Credibility 52 · **Composite 53.28**  
**Tags:** `shell`, `command-verification`, `agent-sandbox`, `static-analysis`, `llm-judge`  
**Verification:** ✓ independently verified · closest prior art: Extends generic LLM-judge guardrails and shell parsers with a shell-specific canonicalization and provenance-backed static pattern layer; accepted at ISSRE 2026.

> **Takeaway:** A static-first, LLM-judge-only-for-borderline pattern for shell-command mediation gives near-parity F1 (~85%) at sub-millisecond latency versus an always-on LLM judge. This is a viable design template for cheap, auditable pre-execution gates on any high-stakes tool call, not just shell. Still not a full harm eliminator: static-only profile leaves ~37% harm on RedCode-gen.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2607.21642) for the complete write-up._

CARE (Canonicalization, Attribution, and Resolution Engine) is a shell-specific, static-first verifier for individual shell commands produced by LLM agents. It canonicalizes commands, derives deterministic evidence over syntax/semantics/path context/provenance-backed risk patterns, and escalates only underdetermined cases to an LLM judge. On the balanced main split it reaches 85.64% F1 with 0.91% FPR at 2.32 ms mean latency; in static-only enforcement it retains 84.99% F1 at 0.34 ms and reduces realized harm on RedCode-gen to 37.33%.

## What to learn

- A static-first shell verifier escalating only borderline commands to an LLM judge preserves most of the LLM-judge accuracy at a fraction of the latency and cost. - _"escalates only underdetermined cases to an LLM judge. This design keeps the common case fast, reproducible, and auditable while reserving neural adjudication for borderline commands."_ ✅
- Static-only enforcement retains ~85% F1 at 0.34 ms and reduces realized harm on RedCode-gen to 37.33%. - _"When deployed in its static enforcement profile, CARE retains 84.99% F1 at 0.34 ms and reduces realised harm on RedCode-gen to 37.33%."_ ✅
- Generic guardrails do not model shell structure in enough detail, and always-on LLM judges are costly and variable. - _"generic guardrails do not model shell structure in sufficient detail, always-on LLM judges are relatively costly and variable"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** LLM agents dispatch shell commands that were steered by untrusted context (indirect prompt injection, poisoned tool output); command executes with the agent's ambient permissions, causing filesystem, network, or credential harm.
- **Conditions:** Agent has shell-execution capability; guardrails are prompt-level or generic (not shell-aware); always-on LLM-judge mediation is too expensive to run on every command.
- **Mitigations:** Insert a static-first shell verifier at the dispatch boundary; canonicalize commands before matching against a provenance-backed risk-pattern list; reserve LLM-judge adjudication for borderline cases; combine with sandboxing since static-only leaves meaningful harm (37% on RedCode-gen).

---

_Source: [https://arxiv.org/abs/2607.21642](https://arxiv.org/abs/2607.21642)_  ·  [← back to index](../README.md)
