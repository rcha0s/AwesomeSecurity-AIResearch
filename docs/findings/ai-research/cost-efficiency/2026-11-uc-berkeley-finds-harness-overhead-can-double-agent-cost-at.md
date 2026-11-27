# UC Berkeley finds harness overhead can double agent cost at similar accuracy

**Published:** Nov 9, 2026

> **Takeaway:** Measure how much of your agent spend is context rereads and harness overhead before tuning anything else.

## TL;DR

UC Berkeley researchers profiled Claude Code, Codex and a plain ReAct harness on SWE-bench, SWE-bench Pro and Terminal-Bench 2 across five models. Harness choices barely moved accuracy but changed cost by up to 2.6x, and rereading existing context was the largest cost even with caching. Their interposition layer, Agency, applied fixes such as compacting tool output, batching tool calls and metadata-assisted search to unmodified harnesses and cut cost by up to 35% without losing accuracy.

## Lessons

- Rereading context already in the window is the biggest cost line, even when it is cached. - _"reading existing context is the largest source of agent cost in real-world executions even with caching"_
- On the same task, Claude Code and Codex can cost about twice a bare agent loop; the paper traces this to their extra system prompts and tools. - _"Claude Code and Codex easily reaching 2× the cost of Basic harnesses"_
- Batching independent tool calls into one turn cut turns, and every turn re-sends the context. - _"yielding up to a 30% reduction in agent turns with 1.8 batched tool calls per turn on average"_
- Metadata-assisted search removed most exploratory search calls in its isolated test. - _"metadata-assisted search in isolation reduces search calls by up to 80%"_

---

**Topic:** AI Research  ·  **Domain:** Cost Efficiency  
**Source:** [UC Berkeley Sky Lab (Park et al.)](https://arxiv.org/abs/2611.12122)  ·  **Author:** UC Berkeley Sky Lab (Park et al.)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 23 · Novelty 40 · Relevance 85 · Credibility 50 · **Composite 51** _(each 0-100)_  
**Tags:** `cost-efficiency`, `harness-design`, `prompt-caching`, `tool-batching`, `coding-agents`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The ledger already holds keep-bulk-tool-output-out-of-context and load-tool-definitions-on-demand from vendor posts. This adds a controlled cross-harness measurement showing harness overhead, not the model, sets much of the cost.

_Source: [https://arxiv.org/abs/2611.12122](https://arxiv.org/abs/2611.12122)_  ·  [← back to index](../README.md)
