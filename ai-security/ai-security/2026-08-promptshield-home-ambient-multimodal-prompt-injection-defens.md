# PromptShield Home: Ambient Multimodal Prompt Injection Defense for Smart-Home Agents

**Published:** Aug 7, 2026

> **Takeaway:** Ambient multimodal prompt injection is a distinct threat class from text-only IPI: detectors over-act and MLLMs over-refuse, and no single layer dominates. Home-agent safety points toward learned routing plus sensor fusion, not a monolithic MLLM guardrail. Note this is an upper-bound analysis; no router is actually built.

## TL;DR

Pilot benchmark for smart-home MLLM agents that must distinguish genuine user commands from ambient content (TV audio, on-screen text, overheard speech). Compares traditional detectors (L0), single MLLM agent (L1), and multi-agent mediation (L2); reports opposite failure modes and a 94.1% oracle upper bound versus 76.5% for the best single layer.

## What to learn

- Smart-home MLLM agents face a specific safety question: telling genuine commands from ambient or externally-sourced audio/video content that merely looks like a command. - _"This raises a safety question specific to the home: can the agent tell a genuine user command from ambient or externally-sourced content, television speech, on-screen text, or an overheard conversation, that merely looks like a command?"_
- Aggregate accuracy is misleading under skewed label distributions - a constant always-block predictor scores 82% - so unsafe-execution and safe-completion rates must be reported separately. - _"Because the label distribution is skewed toward inaction, aggregate accuracy is misleading, a constant always-block predictor scores 82%, so we report unsafe-execution and safe-completion rates separately."_
- Detectors and MLLMs fail in opposite ways with disjoint correct sets - an oracle picking the right layer reaches 94.1% versus 76.5% for the best single layer. - _"The two paradigms fail in opposite ways: detectors act on everything, while every MLLM configuration over-refuses, completing almost no genuine command and missing a true fall in every case. Crucially, their correct sets are disjoint: an oracle that always picks the right layer reaches 94.1%, against 76.5% for the best single layer."_
- The paper's own scope: an upper-bound analysis, not a shipped router. - _"We report this as an upper bound, not a system - no router is implemented - and argue that home-agent safety is best served by learned routing and sensor fusion, not by replacing detectors with an MLLM."_

## Threat · Conditions · Mitigations

- **Threat:** Ambient multimodal prompt injection: a smart-home MLLM agent treats TV speech, on-screen text, or overheard conversation as a legitimate user command, or conversely blocks all input to be safe and misses genuine commands including health emergencies.
- **Conditions:** MLLM home agent that ingests raw audio/video streams and can trigger actions. Ambient sources are present and label distribution is heavily skewed toward inaction.
- **Mitigations:** Do not rely on a single detector or a single MLLM layer; combine layers with learned routing and sensor fusion. Report unsafe-execution and safe-completion separately from aggregate accuracy. Benchmark against realistic scenarios (addressee ambiguity, screen/audio injection, health-monitor false triggers, mixed occupancy) rather than text-only IPI sets.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2608.05495)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 65 · Relevance 70 · Credibility 52 · **Composite 53.28**  
**Tags:** `prompt-injection`, `multimodal`, `smart-home`, `mllm`, `benchmark`, `sensor-fusion`  
**Verification:** ✓ independently verified · closest prior art: ['InjecAgent / BIPIA text-only indirect prompt injection benchmarks', 'PromptGuard / LlamaGuard-style prompt-injection detectors']

_Source: [https://arxiv.org/abs/2608.05495](https://arxiv.org/abs/2608.05495)_  ·  [← back to index](../README.md)
