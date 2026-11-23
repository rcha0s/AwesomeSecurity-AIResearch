# Microsoft FORGE Lab finds soundness bugs in Rust's standard library

**Published:** Nov 9, 2026

> **Takeaway:** Even Rust's standard library has soundness bugs of the three kinds the post names, and the authors say agents make the environment-dependent OS-boundary area practical to search.

## TL;DR

Microsoft's FORGE Lab reports memory-safety bugs in Rust's core and standard (std) libraries, some of which were found with help from Hyenas, a research version of its AI vulnerability scanner codenamed MDASH; humans did the investigation and impact assessment. The bugs include cases where purely safe Rust triggers undefined behavior. The bugs fall into three patterns of misplaced trust in unsafe code: assuming code will not panic (MapWindows::clone, BTreeMap::insert with unwinding allocators), trusting user-provided trait implementations (str::replace with a custom Pattern producing non-UTF-8 (Unicode Transformation Format 8-bit) strings), and trusting process-wide system state (process::exit from a child thread unmapping the main thread's signal stack). The team says AI agents make the third, environment-dependent class practical to search where static analyzers struggled.

## Lessons

- Unsafe-code bugs in the standard library (std) cluster into three trust failures, which make a useful review checklist for any unsafe Rust. - _"three recurring patterns of misplaced trust in unsafe code: trusting code not to panic, trusting user-provided implementations to be correct, and trusting the underlying system"_
- For panic safety, either do all panicking work before breaking an invariant or make the half-built state safe to unwind (ManuallyDrop or a guard). - _"Either finish the work that may panic before breaking an invariant, or make the broken state safe to unwind through"_
- When unsafe code depends on a property of a caller-supplied implementation that cannot be validated, the trait should be unsafe to implement. - _"If none of those work, make the trait unsafe so implementors explicitly promise to uphold it."_
- The authors claim, without comparison evidence, that AI agents make OS-boundary bugs such as signal stacks and memory mappings practical to search where static analyzers struggled. - _"AI agents change the picture: they understand enough about the environment the code runs in to make this area practical to search."_

## Threat · Conditions · Mitigations

- **Threat:** Safe Rust code that calls affected std APIs with adversarial or buggy trait implementations, panicking clones, unwinding allocators, or child-thread process::exit can reach undefined behavior.
- **Conditions:** Mostly nightly or newly stabilized APIs (map_windows, Pattern, Allocator) or uncommon call patterns; two issues remained open at publication.
- **Mitigations:** Track and upgrade to fixed Rust releases, avoid unwinding from custom allocators as the Rust 1.100 stabilization requires, and apply panic-safety guards and once-and-validate handling to user-supplied implementations in your own unsafe code.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 28 · Novelty 55 · Relevance 66 · Credibility 70 · **Composite 54** _(each 0-100)_  
**Tags:** `rust`, `memory-safety`, `unsafe-code`, `ai-vulnerability-research`, `soundness`, `panic-safety`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Rudra (2021) and CVE-2020-36323 by the same team covered Rust ecosystem and std soundness bugs; the tracker has no prior entry on AI-assisted std-library soundness findings (nearest: 'Google brings Rust (memory safety) to the Pixel baseband', archive.json). New here is the three-pattern taxonomy with fresh 2026 std bugs and the claim that agents make OS-boundary unsafe bugs searchable. Verifier's closest: OpenAI pipeline for Linux kernel root bugs; the team's earlier Rudra work.

_Source: [https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/](https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/)_  ·  [← back to index](../README.md)
