# Trojan Horse: Automated Repository Poisoning against Coding Agents

**Published:** Oct 19, 2026

> **Takeaway:** An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.

## TL;DR

TrojanForge automates repository poisoning against coding agents: it maps agent execution traces onto AST nodes, has a security-review agent pick the least conspicuous payload locations, and refines disguises through adversarial play against the target agent. It reaches over 60% stable poisoning success and over 90% backdoor injection, and on a 384-repo benchmark across 4 harnesses and 12 models even commercial agents fail to defend.

## Lessons

- Attackers can place repository payloads where the agent's own execution traces will reach them, choosing the spots a security review is least likely to flag. - _"TrojanForge parses repository structure through abstract syntax trees (AST) and maps agent execution traces onto AST nodes. A security review agent ranks these candidates and selects the least conspicuous ones for payload mounting."_
- Disguises improve automatically: the attacker learns why the agent detected a payload, inverts that cause, and reuses what worked across repositories. - _"iteratively refines disguise strategies by inverting the causes of agent detection, and transfers accumulated success experience across repositories"_
- Automated repository poisoning is reliable, not anecdotal: over 60% poisoning success and over 90% backdoor injection. - _"TrojanForge achieves a stable poisoning success rate of over 60% with backdoor injection exceeding 90%"_
- Agent-side detection doesn't hold up as a defense: across 4 harnesses and 12 models, commercial agents included, none defended against repository-level poisoning. - _"even commercial agents fail to defend against repository-level poisoning"_

## Threat · Conditions · Mitigations

- **Threat:** Poisoned repository content steers a coding agent into executing or committing a backdoor.
- **Conditions:** A coding agent works autonomously inside a repository an attacker can contribute to or publish.
- **Mitigations:** Sandbox with no secrets and allowlisted egress; deterministic gates on sensitive file changes; don't count model-side detection as a control.

---

**Topic:** AI Security  ·  **Domain:** Prompt Injection & Jailbreaks  
**Source:** [arXiv cs.CR (Cryptography and Security)](https://arxiv.org/abs/2610.23109)  ·  **Retrieved:** 2026-10-19  
**Scores:** Newness 24 · Novelty 75 · Relevance 90 · Credibility 51 · **Composite 63** _(each 0-100)_  
**Tags:** `coding-agents`, `repository-poisoning`, `prompt-injection`, `backdoor`, `red-teaming`, `benchmark`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Indirect prompt injection via repo files (rules-file / AGENTS.md backdoors) and manual coding-agent red-teaming; the delta is automated AST-guided payload placement plus adversarial disguise refinement that transfers across repositories.

_Source: [https://arxiv.org/abs/2610.23109](https://arxiv.org/abs/2610.23109)_  ·  [← back to index](../README.md)
