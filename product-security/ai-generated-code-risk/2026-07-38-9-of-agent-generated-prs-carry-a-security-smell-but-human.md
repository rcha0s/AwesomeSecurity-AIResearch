# 38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets

**Topic:** Product Security  ·  **Domain:** AI-Generated Code Risk  
**Source:** [source](https://arxiv.org/abs/2607.12428)  ·  **Author:** A H M Nazmus Sakib et al.  ·  **Published:** Jul 19, 2026  ·  **Retrieved:** 2026-07-21  
**Scores:** 🆕 Newness 8 · ✨ Novelty 57 · 🎯 Relevance 88 · 🏛️ Credibility 58 · **Composite 54.12**  
**Tags:** `ai-generated-code`, `coding-agents`, `secrets`, `supply-chain`, `code-review`  
**Verification:** ✓ independently verified · closest prior art: That LLM-generated code contains vulnerabilities is well documented (Copilot-era studies onward). The delta is scale and attribution on real agent PRs - the 67.6% human-origin secrets finding inverts the 'the agent is the risk' framing. Methodologically it applies an existing technique (LLM-as-judge + manual coding) to a new dataset rather than introducing a new method. Accepted at the KDD 2026 AgenticSE workshop.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

> **Takeaway:** Gate agent PRs with automated secret and dependency-integrity checks - human review demonstrably does not catch this class, and the humans are introducing most of it.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2607.12428) for the complete write-up._

A large-scale study of the AIDev dataset classified security smells across 16,112 file changes in 4,022 agent-generated pull requests. 38.9% of agent PRs contain at least one security smell and supply-chain integrity issues make up 82.3% of them - but the counterintuitive result is that human collaborators introduce 67.6% of the genuine leaked secrets in these agent-assisted workflows, and review catches almost none of them. All percentages are downstream of an LLM-as-a-judge classification pipeline plus manual review, so treat the precision of the figures accordingly.

## What to learn

- Supply-chain integrity dominates the detected smell taxonomy (82.3%); the abstract does not enumerate the remaining categories, so everything else combined is a small residual - point provenance and dependency controls at agent output. - _"38.9% of agent-generated PRs contain at least one security smell, with supply chain integrity issues accounting for 82.3% of all detected security smells"_ ✅
- Blaming the agent misreads the data: humans introduced most genuine leaked secrets, which the authors describe only as suggesting a *potential* reduction in developer vigilance - an association, not a causal finding. - _"human collaborators are responsible for introducing 67.6% of genuine leaked secrets within these agent-assisted workflows"_ ✅
- Existing review is not a control here - automated and human review together missed 81.1% of these credentials before integration. - _"existing automated and human review processes fail to detect 81.1% of these credentials prior to integration"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Security debt accumulates in high-impact file paths faster than human review capacity, with hard-coded credentials making up 99.6% of critical-severity smells.
- **Conditions:** Repositories that accept autonomous coding-agent pull requests through a conventional human review process.
- **Mitigations:** Enforce secret scanning as a merge gate rather than a review step; apply provenance/dependency-integrity checks to agent PRs; add context-aware guardrails at the human-AI collaboration point rather than at final review.

---

_Source: [https://arxiv.org/abs/2607.12428](https://arxiv.org/abs/2607.12428)_  ·  [← back to index](../README.md)
