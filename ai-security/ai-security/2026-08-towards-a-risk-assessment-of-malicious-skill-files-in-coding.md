# Towards a Risk Assessment of Malicious Skill Files in Coding Agents

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2608.05223)  ·  **Published:** Aug 7, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 46 · ✨ Novelty 72 · 🎯 Relevance 82 · 🏛️ Credibility 52 · **Composite 65.48**  
**Tags:** `coding-agents`, `skills`, `prompt-injection`, `mitre-attck`, `gemini-cli`, `qwen-code`  
**Verification:** ✓ independently verified · closest prior art: Builds on prompt-injection and MCP tool-poisoning literature; extends by targeting the skill-file interface specifically and quantifying exploitation across two production agents.

> **Takeaway:** Enterprise coding agents that load skill folders dynamically are highly exploitable via natural-language skill files: Gemini CLI is exploited in 95.5-96.1% of runs and Qwen Code in 71.6-74.0%, with explicit safety recognition in only 1.99% of runs.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.05223) for the complete write-up._

Builds an adversarial skill-synthesis pipeline (six LLMs, four families) that turns 471 real shell commands into 2,826 benign-appearing skill files mapped to 11 MITRE ATT&CK tactics. Evaluates Gemini CLI and Qwen Code across 5,629 runs using a three-judge LLM-as-a-judge panel validated against human labels (kappa 0.85).

## What to learn

- The skill-file interface is a first-class attack surface because malicious shell commands can be hidden inside natural-language instructions the agent loads dynamically. - _"Central to this architecture is the agent skills interface: folders of instructions and scripts that agents load dynamically to specialize their behavior. This interface also widens the attack surface, letting malicious shell commands hide within natural-language skill files."_ ✅
- Exploitation rates in enterprise-grade coding agents are extremely high and nearly independent of which model generated the malicious skill. - _"Gemini CLI is exploited in 95.5-96.1% of runs and Qwen Code in 71.6-74.0% (raw majority vote to declared-intent-corrected estimate, both within the human gold standard), nearly invariant to the generating model."_ ✅
- Coding agents almost never recognize the safety issue on their own: 1.99% explicit safety recognition across 5,629 runs. - _"Explicit safety recognition occurs in only 1.99% of runs. Enterprises must assess and mitigate skill-interface risk before adopting coding agents."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Malicious skill files loaded into coding agents (Gemini CLI, Qwen Code, and similar) can hide shell commands inside natural-language instructions and drive the agent to execute attacker-chosen actions in the developer's environment.
- **Conditions:** Requires a coding agent that dynamically loads a folder of instructions/scripts as skills, and an attacker path to place a skill file (repo checkout, marketplace, MCP server, shared workspace).
- **Mitigations:** Signed/allowlisted skill sources, static scanning of skill files for shell/tool invocations before load, isolation of the agent's execution environment, LLM-as-judge or human review on new skills, and telemetry mapped to MITRE ATT&CK tactics.

---

_Source: [https://arxiv.org/abs/2608.05223](https://arxiv.org/abs/2608.05223)_  ·  [← back to index](../README.md)
