# Kimi K2.6 on vLLM returned valid tool-calls 92% of the time

**Published:** Oct 26, 2026

> **Takeaway:** Tool-call quality depends on how the model is served, not only on the model. Turn on constrained decoding per model, check it with a tool-call benchmark, and re-check after engine upgrades.

## TL;DR

Ubicloud measured tool-call schema accuracy with Moonshot AI's K2-Vendor-Verifier ToolCall benchmark (2,000 requests). Serving Kimi K2.6 on vLLM 0.28 without constrained decoding, they got the expected schema 92% of the time. With constrained decoding (XGrammar structural tags that mask invalid tokens), they report 100% across all served model versions, with negligible overhead. After they moved to upstream vLLM, accuracy fell back to 91%, because vLLM disables constrained decoding by default for requests that don't ask for it.

## Lessons

- Without constraints, a popular open-weight model served on a common engine still returned the wrong tool-call schema in 8% of calls. - _"For example, when we served Kimi K2.6 with vLLM version 0.28, we got the expected tool call schema only 92% of the time."_
- A serving-engine default undid their fix: accuracy fell back to 91% until they found vLLM had changed its default. Re-test tool-call accuracy after engine upgrades. - _"Instead, we found that vLLM changed its default behavior for requests that do not explicitly turn constrained decoding on."_
- One cause of malformed calls is the model reusing tool or field names from training. Schema-constrained decoding blocks those names at generation time. - _"For example, it may generate search_web when the available tool is web_search, or use city_name when the active schema expects location."_
- Constrained decoding has known problems, including a bug with speculative decoding that wrongly rejects tokens. Test it per model and per feature combination. - _"a bug in the interplay between constrained decoding and speculative decoding can result in speculative tokens being wrongly rejected by the grammar, leading to failing requests"_

---

**Topic:** AI Research  ·  **Domain:** Model I/O & Cost  
**Source:** [@coffeemug via Hacker News](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)  ·  **Author:** coffeemug  ·  **Retrieved:** 2026-10-26  
**Scores:** Newness 23 · Novelty 30 · Relevance 80 · Credibility 55 · **Composite 47** _(each 0-100)_  
**Tags:** `tool-calling`, `constrained-decoding`, `vllm`, `xgrammar`, `serving`, `open-weights`, `benchmarks`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Ledger claims constrained-decoding-for-structured-output (a format benchmark on one-shot generation) and match-tool-schemas-to-the-target-model (newer models invent fields in non-native tool schemas). New here: a production measurement of tool-call schema accuracy with and without constrained decoding on a common engine, and the default-off regression.

_Source: [https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)_  ·  [← back to index](../README.md)
