# SPA: Securing Persistent LLM Agents Across Queries with Plan-First Information-Flow Control

**Topic:** AI Security  ·  **Domain:** Agents / Information-Flow Control  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.27234)  ·  **Published:** Aug 27, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 78 · 🎯 Relevance 85 · 🏛️ Credibility 60 · **Composite 62.9**  
**Tags:** `llm-agents`, `information-flow-control`, `prompt-injection`, `agentdojo`, `persistence`, `confidentiality`  
**Verification:** ✓ independently verified · closest prior art: AgentDojo benchmark and prior planning- or tool-level injection defenses; extends to cross-query persistence with dual-lattice IFC and AgentDojo-MQ.

> **Takeaway:** Plan-first execution plus information-flow labels that persist across queries can nearly eliminate tool-knowledge injection in stateful agents, at some utility cost.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.27234) for the complete write-up._

Persistent LLM agents face threats beyond single tool calls: attacker data can alter control flow, poison tool arguments, or compromise later queries via reused state. SPA generates a full executable plan once per query in a declarative DSL, then applies dual-lattice information-flow control over confidentiality and integrity, storing results as labeled artifacts that expose only metadata to later planning. It reduces 'tool_knowledge' attack success to zero on AgentDojo and 0.2% on a new multi-query extension, at a security-utility cost.

## What to learn

- Persistent agents need defenses that span planning, execution, and cross-query state, not just individual tool calls. - _"attacker-controlled data can alter control flow, enter security-sensitive tool arguments, or compromise later queries"_ ✅
- Storing results as labeled artifacts and exposing only metadata to later planning prevents re-injection of untrusted payloads across queries. - _"SPA stores execution results as labeled artifacts and reveals only semantic metadata during later planning"_ ✅
- Dual-lattice information-flow control can drive prompt-injection attack success to near zero, but strict integrity enforcement costs utility. - _"revealing an important security-utility tradeoff introduced by strict integrity enforcement"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Indirect prompt injection and delayed attacks that corrupt control flow, tool arguments, or reused state in persistent agents.
- **Conditions:** Agent operates over untrusted web/document/tool inputs while reusing state across multiple queries.
- **Mitigations:** Plan-first declarative execution with dual-lattice information-flow control and label-preserving artifact persistence.

---

_Source: [https://arxiv.org/abs/2608.27234](https://arxiv.org/abs/2608.27234)_  ·  [← back to index](../README.md)
