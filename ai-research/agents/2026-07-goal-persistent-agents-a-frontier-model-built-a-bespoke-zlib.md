# Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day

**Published:** Jul 2, 2026

> **Takeaway:** Give an agent a durable goal plus strict rules for what counts as a real finding and it plans multi-step tooling and filters its own noise; the rules make the output actionable.

## TL;DR

Pointed at a specific bug class in well-audited zlib via a persistent `/goal` - but not told how - a frontier model decided static review was low value, built fuzz harnesses across a dozen entrypoints with ASan/UBSan and variant builds, and surfaced findings now in coordinated disclosure. The load-bearing harness detail was a strict definition of a reportable finding - it self-rejected an unreachable crash as noise and kept going. (Single-source vendor field report on a not-yet-public model.)

## Lessons

- A persistent goal that survives compaction lets the agent hold scope end-to-end and pick its own strategy - here it chose dynamic fuzzing over static review without being told to. - _"judged static review to be a poor use of tokens, and decided the higher value path was to build fuzz tooling to dynamically test the code"_
- Reportability discipline is what turns agent output into signal: without strict validity rules baked into the goal, the agent produces confident noise. - _"the agent will generate mountains of noise with high confidence"_
- The model triaged its own findings - it logged a real-but-unreachable crash as noise and moved on rather than escalating it. - _"the model logged it as unreachable and moved on"_

---

**Topic:** AI Research  ·  **Domain:** Agents & Harnesses  
**Source:** [source](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)  ·  **Retrieved:** 2026-07-16  
**Scores:** Newness 0 · Novelty 60 · Relevance 88 · Credibility 75 · **Composite 56** _(each 0-100)_  
**Tags:** `agents`, `goal-persistence`, `fuzzing`, `evals`, `ai-for-security`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: LLM-driven vuln discovery (Google's Big Sleep / OSS-Fuzz-gen, XBOW) is prior work; the novel practitioner delta is the emphasis on goal-persistence-across-compaction plus baked-in reportability rules as the mechanism that makes the loop high-signal.

_Source: [https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)_  ·  [← back to index](../README.md)
