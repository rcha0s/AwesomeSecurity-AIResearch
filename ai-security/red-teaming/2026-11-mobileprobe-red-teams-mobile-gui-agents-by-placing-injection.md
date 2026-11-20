# MobileProbe red-teams mobile GUI agents by placing injections along their actual route

**Published:** Nov 12, 2026

> **Takeaway:** If your mobile or GUI agent security eval injects payloads at fixed steps, it probably undercounts risk, because injections must follow each agent's actual route to test it.

## TL;DR

MobileProbe is an NDSS 2027 framework for red-teaming mobile GUI agents against environmental injection, meaning malicious instructions placed in ordinary on-screen app content. It uses automated pentesting to find content an attacker can control, locates the decision points along the agent's path through the app, and evolves context-aware payloads with a surrogate-filtered loop. On a benchmark of 83 long-horizon attacks across 12 apps, it beats human-written, zero-shot LLM and earlier automated red-teaming baselines on three agent architectures, though the abstract gives no success-rate numbers.

## Lessons

- Benchmarks that inject at a fixed step overstate safety. An agent that takes a different route never sees the payload, and the benchmark scores it as safe even though it was never tested. - _"agents given the same task may follow different routes, so an agent that never reaches the injected page is recorded as safe without being tested"_
- Adaptive red-teaming of GUI agents should first find the content surfaces an attacker controls, then target the decision points on the agent's real path. - _"discovers attacker-controllable content surfaces through automated pentesting, localizes vulnerable decision points along the agent's trajectory"_
- Evolved, context-aware payloads beat human-written and zero-shot ones, so a mobile agent's resistance to hand-written injections is a weak lower bound on its real risk. The abstract does not give the size of the gap. - _"MobileProbe attains higher attack success rates than human-written, zero-shot LLM, and prior automated red-teaming baselines"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker who controls ordinary in-app content, such as listings, messages or reviews, can redirect a mobile GUI agent toward confidentiality, integrity or availability goals.
- **Conditions:** The agent reads the phone screen and acts on what it shows across multi-step tasks in third-party apps.
- **Mitigations:** Red-team before deployment with route-aware adaptive payloads, separate untested runs from resisted ones in eval reports, and treat on-screen third-party content as untrusted input that cannot authorize actions.

---

**Topic:** AI Security  ·  **Domain:** Red-Teaming & Threat Modeling  
**Source:** [NDSS (via arXiv)](http://arxiv.org/abs/2611.16693v1)  ·  **Retrieved:** 2026-11-13  
**Scores:** Newness 33 · Novelty 55 · Relevance 75 · Credibility 72 · **Composite 58** _(each 0-100)_  
**Tags:** `prompt-injection`, `indirect-prompt-injection`, `gui-agents`, `mobile-agents`, `red-teaming`, `evals`, `computer-use`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: EIA (Liao et al. 2024, environmental injection on web agents); AEIA-MN and pop-up attacks on VLM computer agents, all fixed-step. New: trajectory-aware injection placement, automated attack-surface discovery, and the coverage critique of fixed-step benchmarks.

_Source: [http://arxiv.org/abs/2611.16693v1](http://arxiv.org/abs/2611.16693v1)_  ·  [← back to index](../README.md)
