# Researchers find agents keep accuracy with short, frequently compacted contexts

**Published:** Nov 3, 2026

> **Takeaway:** Short, frequently compacted contexts kept accuracy here; on hosted APIs, test that against the cache hits each compaction gives up.

## TL;DR

This paper argues that generating later tokens in a long context costs more than earlier ones, by up to 7x on frontier open-weight models, and tests whether agents need long context at all. With Claude Opus 4.5 and GPT 5.6 Sol, frequent compaction and reading long inputs selectively as stored documents kept task accuracy largely intact on long-horizon and long-input tasks. It also proposes semantic state space models, which would need a trained model.

## Lessons

- Keeping contexts short costs little accuracy on frontier models. - _"frontier language models sacrifice little to no task accuracy when maintaining short contexts."_
- Frequent compaction kept contexts short while broadly holding accuracy. - _"Frequent compaction keeps the context short while broadly maintaining task accuracy."_
- Store long inputs as documents the agent reads on demand instead of pasting them into context. - _"We enable selective input reading by storing each long input as one or more documents"_
- On frontier open-weight models the cost gap between short and long contexts can reach 7x. - _"On frontier open weight models, the disparity in cost may rise to as much as 7x."_

---

**Topic:** AI Research  ·  **Domain:** Cost Efficiency  
**Source:** [Belcak et al.](https://arxiv.org/abs/2611.05306)  ·  **Author:** Belcak et al.  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 31 · Novelty 30 · Relevance 70 · Credibility 50 · **Composite 45** _(each 0-100)_  
**Tags:** `cost-efficiency`, `context-compaction`, `long-context`, `harness-design`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: compact-first-reset-only-if-the-model-needs-it and Microsoft's compaction-cost finding cover when to compact; this adds evidence that compacting early and often keeps accuracy.

_Source: [https://arxiv.org/abs/2611.05306](https://arxiv.org/abs/2611.05306)_  ·  [← back to index](../README.md)
