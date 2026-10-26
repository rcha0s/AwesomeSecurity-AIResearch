# Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs

**Published:** Oct 22, 2026

> **Takeaway:** If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.

## TL;DR

Anthropic and Theorem had Claude prove, in Rocq, that 239 OSS-Fuzz entry points in 123 open-source libraries never crash (no memory-safety error or failed assertion) for any input up to 64 MB, after patching the bugs it found along the way. The spec is derived mechanically from the existing fuzz harness plus formal RISC-V and Linux-process semantics, so the ~180M lines of proof need no human review: trust reduces to the semantics, the theorem statements and the Rocq checker. Scope is narrow (single-threaded static RISC-V binaries, fixed memory budget) and compute is large, but it moves formal verification from niche to a pipeline step.

## Lessons

- LLM-written formal proofs now scale to production libraries at the binary level, not just toy programs. - _"proved that there are no crashes on any input (up to 64 MB) for 239 entry points across 123 different OSS-Fuzz libraries"_
- The spec problem is sidestepped by reusing what developers already wrote: an existing fuzz harness becomes the property to prove. - _"automatically converting their preexisting compilable test suites into a spec"_
- Machine checking replaces review of the AI output: the trusted base is the semantics, the theorem statements and the checker, not the 600k-line proofs. - _"virtually none of it needs to be manually reviewed"_
- The guarantee is scoped: it holds only for single-threaded static RISC-V binaries on Linux under a memory budget, and bugs may remain in the trusted components. - _"assume that the program runs as a single-threaded static binary with a fixed memory budget on a RISC-V CPU using Linux OS"_
- Attempting proofs is itself a bug finder: failures pointed at real bugs that fuzzing had missed. - _"the process of attempting to prove these specs discovered hundreds of bugs"_

## Threat · Conditions · Mitigations

- **Threat:** AI-accelerated bug discovery and exploit chaining outpacing test-based assurance for memory-unsafe code.
- **Conditions:** C/C++ libraries with existing fuzz harnesses; proofs currently limited to single-threaded static RISC-V Linux binaries.
- **Mitigations:** Turn fuzz harnesses into no-crash specs and have an LLM produce checker-verified proofs; review the theorem statements and trusted semantics rather than proof text.

---

**Topic:** Product Security  ·  **Domain:** AI in the SDLC  
**Source:** [source](https://www.anthropic.com/research/formal-verification)  ·  **Author:** Keane Lucas et al. (Anthropic, Theorem)  ·  **Retrieved:** 2026-10-23  
**Scores:** Newness 24 · Novelty 75 · Relevance 75 · Credibility 55 · **Composite 59** _(each 0-100)_  
**Tags:** `formal-verification`, `fuzzing`, `memory-safety`, `rocq`, `llm-proofs`, `oss-fuzz`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: seL4 and CompCert (human-written verification at 10x code effort), binary-level verifiers like Alive2, LLM proof assistants (Baldur, AlphaProof), and AI bug finding (Big Sleep, AIxCC). None showed LLM-written, machine-checked binary-level proofs at this scale.

_Source: [https://www.anthropic.com/research/formal-verification](https://www.anthropic.com/research/formal-verification)_  ·  [← back to index](../README.md)
