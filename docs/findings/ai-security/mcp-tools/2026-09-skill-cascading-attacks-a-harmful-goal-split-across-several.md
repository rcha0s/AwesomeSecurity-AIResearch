# Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors

**Published:** Sep 24, 2026

> **Takeaway:** A clean per-skill scan does not show that a set of installed skills is safe together, so review and monitoring have to cover the whole pipeline of skills.

## TL;DR

An attacker can spread one malicious goal across several agent skills so that each edit looks harmless alone but the chain is harmful. In the paper's example, three skills in a prescription-review pipeline each weaken a signal a little, and a severe drug-interaction warning never reaches the physician. The authors built SkillCascade, an automated red-teaming framework, and a 213-case benchmark; they report that cascades work on agents like Claude Code and Codex and slip past per-skill scanners and runtime monitors.

## Lessons

- The attack unit is the composition of skills, not one skill: each change is benign alone and harmful only when the skills run together. - _"a malicious objective is distributed across multiple skills so that each modification looks benign in isolation, yet their combined execution is harmful"_
- Scanning skills one at a time, and existing runtime monitors, did not catch the cascades in the authors' tests. - _"cascaded interactions reliably induce harmful behaviors while evading existing per-skill scanners and runtime monitors"_
- A reusable benchmark exists for testing cross-skill defenses. - _"a benchmark of 213 validated cascading test cases across multiple agent systems and domains"_
- Defenses need to reason about how skills interact, not just inspect each one. - _"call for defenses that reason over cross-skill interactions rather than individual skills in isolation"_

## Threat · Conditions · Mitigations

- **Threat:** Attacker-modified third-party skills that are each individually benign combine at runtime to suppress safety-critical information or cause harmful actions.
- **Conditions:** Agent loads multiple third-party skills that operate on a shared data flow; defenses scan or monitor skills individually.
- **Mitigations:** Provenance and pinning for all skills; cross-skill dataflow review; end-to-end invariant tests on critical signals; monitors that reason over full skill chains.

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [NeurIPS (via arXiv)](http://arxiv.org/abs/2609.30383v1)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 5 · Novelty 70 · Relevance 82 · Credibility 72 · **Composite 58** _(each 0-100)_  
**Tags:** `agent-skills`, `skill-supply-chain`, `compositional-attack`, `red-teaming`, `benchmark`, `scanner-evasion`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Towards a Risk Assessment of Malicious Skill Files in Coding Agents (single-skill); cross-skill composition is new.

_Source: [http://arxiv.org/abs/2609.30383v1](http://arxiv.org/abs/2609.30383v1)_  ·  [← back to index](../README.md)
