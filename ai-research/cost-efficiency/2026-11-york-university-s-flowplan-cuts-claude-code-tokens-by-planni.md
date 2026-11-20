# York University's FlowPlan cuts Claude Code tokens by planning edits first

**Published:** Nov 9, 2026

> **Takeaway:** Replacing post-edit re-reading and re-testing with a stated plan cut coding agent tokens with no significant loss in fix rate.

## TL;DR

FlowPlan has a coding agent localize the fault, state its intended change as a delta on per-function control-flow or data-flow graphs, and then check the actual change against that plan. On SWE-bench Pro, SWE-bench Verified and SecBench with Claude Code on Haiku 4.5 and Sonnet 5, resolution rate did not change significantly while token use fell in every setting, to as low as about a third of baseline. The baseline spent 3.7 million tokens per issue, 98% of them cache reads.

## Lessons

- In these long coding runs, 98% of tokens were cache reads of the growing trajectory, so each extra turn adds cost. - _"the vanilla Claude Code consumes an average of 3.7 million tokens per issue, 98% of which are cache reads."_
- An explicit plan the agent verifies against can replace much of the re-reading and re-testing that inflates trajectories. - _"saves tokens by replacing much of the costly post-edit re-reading and testing with explicit verification"_
- The saving held without hurting fix rate on these benchmarks. - _"does not significantly change resolution rate relative to the vanilla agent"_
- Gains shrink when baseline runs are already short, so this pays most on long repairs. - _"The smaller reduction on SecBench reflects its substantially shorter baseline trajectories"_

---

**Topic:** AI Research  ·  **Domain:** Cost Efficiency  
**Source:** [York University (Sepidband et al.)](https://arxiv.org/abs/2611.13241)  ·  **Author:** York University (Sepidband et al.)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 33 · Novelty 50 · Relevance 75 · Credibility 50 · **Composite 53** _(each 0-100)_  
**Tags:** `cost-efficiency`, `coding-agents`, `planning`, `verification`, `prompt-caching`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest pool items are the stable-prefix and compaction claims; FlowPlan is a new mechanism (graph-delta planning) with SWE-bench measurements.

_Source: [https://arxiv.org/abs/2611.13241](https://arxiv.org/abs/2611.13241)_  ·  [← back to index](../README.md)
