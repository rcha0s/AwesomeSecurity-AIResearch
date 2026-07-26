# Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)

**Topic:** AI Research  ·  **Domain:** Harness / context management  
**Source:** [@kunchenguid](https://github.com/algal/pi-openai-server-compaction)  ·  **Author:** kunchenguid  ·  **Published:** Jul 22, 2026  ·  **Retrieved:** 2026-07-26  
**Scores:** 🆕 Newness 25 · ✨ Novelty 70 · 🎯 Relevance 80 · 🏛️ Credibility 75 · **Composite 62.5**  
**Tags:** `harness`, `context-management`, `compaction`, `responses-api`, `openai`, `codex`, `long-running-agents`  
**Verification:** ✓ independently verified · closest prior art: OpenAI Responses API stateful continuation (store:true + previous_response_id) and generic context/tool-output compaction (the pool's 'Compact tool outputs' note); no public equivalent describes reverse-engineering Codex's encrypted server-side `compaction_trigger` protocol and porting it into another harness.

> **Takeaway —** If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity — but treat 'it's better' as unproven at equal token budget and keep a portable text summary as fallback.

## TL;DR

_The gist, not every detail — read the [full source](https://github.com/algal/pi-openai-server-compaction) for the complete write-up._

OpenAI's Codex compacts long-running sessions by calling the Responses API's server-side compaction protocol — sending a `compaction_trigger` through `POST /v1/responses` and getting back an opaque, encrypted `compaction` artifact instead of a text summary — which reportedly lets it 'keep hammering' on long tasks as if context were infinite. Because the endpoint is public and Codex is open source, a third party reconstructed exactly how Codex uses it and packaged it as a Pi extension, running it alongside a portable Pi text summary so non-OpenAI models and session forking still work. The author's own held-out benchmark shows this native/remote policy recalling more old state (78% vs 48% exact recall) but at 4.58x more compaction output tokens and a 29% larger billed context, with high run-to-run variance — so it is not shown to be better at an equal token budget.

## What to learn

- OpenAI exposes a server-side compaction protocol on the Responses API: a `compaction_trigger` sent to POST /v1/responses returns an encrypted, provider-native `compaction` item rather than a text summary, and this is the mechanism behind Codex's strong long-task continuity. — _"That protocol sends a `compaction_trigger` through `POST /v1/responses` and receives an encrypted `compaction` item."_ ✅
- Between compactions, continuity is maintained by setting `store: true` and passing `previous_response_id`, so the model resumes from server-retained encrypted state instead of replaying full history — the core trick enabling effectively-infinite-context behavior on long tasks. — _"Uses `previous_response_id` for live continuation when safe"_ ✅
- A provider's opaque compaction can be reproduced in a different harness by mimicking the open-source client's exact endpoint usage, but you should keep a portable text summary in parallel so forking, exports, and non-provider models still function. — _"since codex is an open source, we can mimic exactly how codex itself uses the endpoint"_ ✅
- The claim that this compaction 'works better than anything else' is weakly supported: the measured recall advantage came with 4.58x more output tokens and a 29% larger downstream context, was highly variable (small artifacts failed), and an earlier same-budget win was retracted as methodologically asymmetric. — _"Native did this while emitting 4.58x as many compaction output tokens and leaving a 29% larger billed downstream context."_ ✅
- The compaction request must mirror the surrounding normal requests (reasoning effort, tools, text config) rather than using endpoint defaults, and the encrypted blobs may just be encrypted text/structured state rather than a clever latent representation. — _"The compaction request mirrors the shape of surrounding normal requests (reasoning effort, text settings, tool definitions) rather than using endpoint defaults."_ ✅

## Threat · Conditions · Mitigations

- **Conditions —** Requires OpenAI Responses-API models (e.g. gpt-5.6) and a harness you can extend; sets store:true (OpenAI retains conversation data server-side) and sends full context to OpenAI's compaction protocol — a data-handling consideration. Artifacts are provider-native and opaque, reusable only on compatible OpenAI turns.

## Actionable leverage

**[harness]** Wire OpenAI server-side compaction into your agent harness — For openai/* models, on your compaction event call POST /v1/responses with the full history plus a trailing compaction_trigger, mirroring your normal request's reasoning/tool/text config; store the returned opaque `compaction` item and replay it only for compatible OpenAI turns. Set store:true and use previous_response_id for between-compaction continuity, and generate a portable text summary in parallel so forks/exports/other models keep working. Budget for the cost: this policy emitted ~4.58x compaction output tokens and a ~29% larger billed context, so gate it behind a config/threshold and measure recall-per-token on your own tasks before trusting it.

---

_Source: [https://github.com/algal/pi-openai-server-compaction](https://github.com/algal/pi-openai-server-compaction)_  ·  [← back to index](../README.md)
