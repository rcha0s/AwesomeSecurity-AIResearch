# Evaluating Investment Logic in Large Language Models: A Real-World Benchmark Towards Personalized Financial Agents

**Published:** Aug 7, 2026

> **Takeaway:** Terminal-P&L and static QA are the wrong ruler for consequential agents: score the P→E→R→D→O trace and you can see how weakly grounded 'logical' answers actually are.

## TL;DR

InvestLogicBench introduces a process-native benchmark of 201,247 documented decisions from 151 real-world investors, structured as a Profile→Events→Reasoning→Decision→Outcome (P→E→R→D→O) trace. Across four leading LLMs, logical plausibility scores near 4/5 while event grounding is 0.8 - 2.8/5 - outcome-only evaluation hides polished-but-ungrounded reasoning.

## What to learn

- Static QA omits agency and terminal P&L can't distinguish a grounded, profile-consistent action from a lucky one; both are the wrong evaluation shape for consequential agents. - _"The former omits agency; the latter cannot reveal whether a profitable action was grounded, profile-consistent, or merely lucky"_ ✅
- Across four leading LLMs, logical plausibility hovers near 4/5 while event grounding is only 0.8 - 2.8/5 - a large, systematic gap between how coherent an answer sounds and whether it is actually anchored in the observed events. - _"logical plausibility remains near 4/5 while event grounding is only 0.8--2.8/5; return and process quality also disagree"_ ✅
- The authors argue P→E→R→D→O should be a data-system interface, requiring versioned profiles, temporal provenance, inspectable retrieval, decision ledgers, and replayable outcomes. - _"P→E→R→D→O should be a data-system interface, requiring versioned profiles, temporal provenance, inspectable retrieval, decision ledgers, and replayable outcomes"_ ✅

---

**Topic:** AI Research  ·  **Domain:** Agent Evals  
**Source:** [source](https://arxiv.org/abs/2608.06108)  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 20 · ✨ Novelty 72 · 🎯 Relevance 78 · 🏛️ Credibility 55 · **Composite 58.25**  
**Tags:** `agent-evals`, `groundedness`, `process-native`, `decision-ledger`, `benchmarks`  
**Verification:** ✓ independently verified · closest prior art: General 'process reward' / 'reasoning-trace' evals (PRM, ORM), plus finance-specific benchmarks (FinBench, FinQA) that stop at QA or terminal P&L. The specific 5-tuple P→E→R→D→O framing plus 201k real-investor decisions is new.

_Source: [https://arxiv.org/abs/2608.06108](https://arxiv.org/abs/2608.06108)_  ·  [← back to index](../README.md)
