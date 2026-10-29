# Letting the agent choose when to compact matches fixed-interval summarization cheaply

**Published:** Oct 12, 2026

> **Takeaway:** Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.

## TL;DR

SELFCOMPACT gives the model a compaction tool plus a short rubric saying when to use it: fire when a sub-task has resolved or the trajectory is converging, and hold off mid-derivation or when stuck. Across six math and agentic-search benchmarks and seven models, it matches or beats fixed-interval token-threshold summarization at a fraction of the token cost. It beats a no-summarization baseline by up to 18.1 points on math and 5-9 points on search; neither part works alone, since models use the tool unevenly without the rubric and the rubric cannot act without the tool. No fine-tuning is needed.

## Lessons

- Fixed token-threshold compaction ignores task structure and risks discarding partial work. - _"Such triggers pay no heed to trajectory structure, risking discard of partial results mid-derivation or mid-search."_
- A compaction tool alone does not work. Open-weight models fire it at bad moments or never. - _"The tool alone is unevenly used across open-weight models, often invoked at unhelpful moments or not at all; the rubric alone cannot act."_
- The rubric is lightweight: fire at sub-task boundaries or convergence, suppress mid-derivation or when stuck. - _"when to fire (a sub-task has resolved, or the trajectory is converging) and when to suppress (mid-derivation, or when stuck)"_
- Against a no-summarization baseline, the gains come at 30-70% lower per-question cost. - _"improving over a no-summarization baseline by up to 18.1 points on math and 5 - 9 points on agentic search at 30 - 70% lower per-question cost"_

---

**Topic:** AI Research  ·  **Domain:** Agents & Harnesses  
**Source:** [Apple Machine Learning Research](https://machinelearning.apple.com/research/self-compacting-language-agents)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 20 · Novelty 55 · Relevance 80 · Credibility 75 · **Composite 57** _(each 0-100)_  
**Tags:** `compaction`, `context-management`, `long-running-agents`, `scaffolding`, `summarization`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Several pool entries treat compaction as harness infrastructure: the Claude Code harness design entry (system-prompt compaction), the Codex/Pi encrypted compaction port, and the OpenAI Agents API with managed compaction. All of them trigger on fixed thresholds or leave the trigger unspecified. What is new: evidence that the timing of compaction matters, and that a prompt-level rubric, not training, lets the model choose that timing well.

_Source: [https://machinelearning.apple.com/research/self-compacting-language-agents](https://machinelearning.apple.com/research/self-compacting-language-agents)_  ·  [← back to index](../README.md)
