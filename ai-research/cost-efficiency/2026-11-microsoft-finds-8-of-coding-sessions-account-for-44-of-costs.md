# Microsoft finds 8% of coding sessions account for 44% of costs

**Published:** Nov 12, 2026

> **Takeaway:** If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.

## TL;DR

This digest's most practitioner-relevant item is a Microsoft study of 13.5 million coding agent sessions: fewer than 8% needed context compaction, yet those sessions made up 44% of total AI processing costs. The researchers released COMPACTIONBENCH to evaluate compaction and APEC, a method that prepares summaries in the background, which cut costs by up to 25.4% and execution time by 9.6%.

## Lessons

- A small share of long sessions drives a large share of spend, so compaction is a key cost lever. - _"A new study looked at 13.5 million coding sessions and found fewer than 8% required context compaction. Yet those sessions accounted for 44% of total AI processing costs."_
- Building the summary in the background, instead of pausing the agent, improved both cost and speed. - _"APEC, a method that prepares summaries in the background instead of interrupting an agent’s work"_
- The reported gains are modest but concrete. - _"APEC improved coding performance while reducing costs by up to 25.4% and execution time by 9.6%"_

---

**Topic:** AI Research  ·  **Domain:** Cost Efficiency  
**Source:** [Microsoft Research Blog](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)  ·  **Retrieved:** 2026-11-14  
**Scores:** Newness 31 · Novelty 55 · Relevance 65 · Credibility 73 · **Composite 55** _(each 0-100)_  
**Tags:** `context-compaction`, `coding-agents`, `cost-efficiency`, `benchmark`, `harness-design`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The pool already covers when to trigger compaction (a model-invoked compaction tool with a fire/hold rubric), encrypted Codex compaction and compaction as an injection path. This adds large-scale cost data and a background, non-blocking compaction method.

_Source: [https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)_  ·  [← back to index](../README.md)
