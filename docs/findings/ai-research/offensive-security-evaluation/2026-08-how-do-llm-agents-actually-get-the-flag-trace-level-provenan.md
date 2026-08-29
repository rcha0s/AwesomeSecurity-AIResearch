# How Do LLM Agents Actually Get the Flag? Trace-Level Provenance for Agentic Offensive-Security Evaluation

**Topic:** AI Research  ·  **Domain:** Offensive-Security Evaluation  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.26237)  ·  **Published:** Aug 26, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 76 · 🎯 Relevance 80 · 🏛️ Credibility 60 · **Composite 60.8**  
**Tags:** `ctf`, `offensive-security`, `agent-evaluation`, `provenance`, `benchmark-integrity`, `capability-elicitation`  
**Verification:** ✓ independently verified · closest prior art: Prior CTF agent benchmarks with binary/aggregate scoring; contribution is trace-based provenance auditing (CTF-ABACUS).

> **Takeaway:** Judge security agents on evidence of exploitation in the trace, not on whether the flag string appeared.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2608.26237) for the complete write-up._

CTF benchmarks score agents with binary pass/fail, conflating real exploitation with flag exposure, memorized recall, external lookup, and guessing - overstating cyber capability. CTF-ABACUS reconstructs each run as an evidence-grounded solve profile across pentest phases to check whether the recovered flag is actually supported by demonstrated behavior. Across 1,435 attempts on 240 challenges, only 62-87% of recovered flags were trace-verified exploits.

## What to learn

- Binary CTF scoring overstates agent offensive capability by conflating real exploitation with recall, lookup, and guessing. - _"actual exploitation is conflated with direct flag exposure, memorized recall, external lookup, guessing, and unsupported claims, potentially overstating the agent's cybersecurity capability"_ ✅
- Trace-level auditing should verify whether a recovered flag is actually supported by demonstrated exploit behavior. - _"whether the recovered flag is supported by demonstrated behavior"_ ✅
- Empirically, a substantial fraction of 'solves' are shortcuts, not intended exploits. - _"Trace-verified exploits account for only 62-87% of recovered flags across benchmarks"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Not an attack: risk of over-attributing cyber-offense capability to agents due to shortcut solves.
- **Conditions:** Evaluating autonomous LLM agents on CTF challenges with pass/fail flag scoring.
- **Mitigations:** Evidence-grounded solve profiles and challenge signatures that separate intended exploits from shortcuts.

---

_Source: [https://arxiv.org/abs/2608.26237](https://arxiv.org/abs/2608.26237)_  ·  [← back to index](../README.md)
