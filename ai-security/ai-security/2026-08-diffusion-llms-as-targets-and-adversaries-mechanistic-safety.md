# Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits

**Published:** Aug 10, 2026

> **Takeaway:** Safety alignment in diffusion LLMs is sparse enough to be located by neuron mapping and cheaply bypassed - and the resulting attack transfers across families, including to a closed frontier model.

## TL;DR

The authors show diffusion-based LLMs inherit a sparse, mappable set of 'safety neurons' from their autoregressive predecessors, so pruning those neurons (self- or transfer-pruning from models like Qwen2.5) drives attack success rates from single digits to 70 - 86 percent. They then build SN-Guided Diffusion, an offline black-box jailbreak that steers denoising away from safety-triggering regions and transfers to Llama-3-8B-Instruct, Qwen2.5-7B-Instruct, and Gemini-2.5-Flash-Lite with only 20 generation episodes per prompt.

## What to learn

- Diffusion LLMs inherit the same sparse safety neurons as their autoregressive predecessors, enabling transfer attacks by direct neuron mapping and pruning. - _"DLLMs initialized from autoregressive predecessors inherit the same mechanistic safety footprint as their source models, enabling transfer attacks via direct safety neuron mapping and pruning."_ ✅
- Self- or transfer-pruning of these safety neurons lifts attack success rates dramatically on multiple DLLMs. - _"Self-pruning increases attack success rates (ASR) from 2.6% to 73.8% on LLaDA and from 1.9% to 86.6% on Dream, while transfer pruning from Qwen2.5 increases ASR from 1.9% to 73.2% on Dream and from 7.0% to 86.3% on Fast-dLLM."_ ✅
- SN-Guided Diffusion is an offline black-box jailbreak whose transfer generalizes to proprietary autoregressive frontier models with very few queries. - _"Our method achieves a transfer ASR of up to 77.1% on Llama-3-8B-Instruct, 86.9% on Qwen2.5-7B-Instruct, and 74.3% against Gemini-2.5-Flash-Lite, while requiring only 20 generation episodes per prompt."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Sparse and inherited safety neurons in diffusion LLMs let attackers cheaply locate and disable alignment, then reuse the same guidance to jailbreak unrelated autoregressive and proprietary models with tens of queries.
- **Conditions:** Attacker needs (1) a source model or its safety-neuron map to seed the attack, (2) an offline pipeline to steer diffusion sampling with a safety-neuron loss, and (3) black-box query access to the target; results are demonstrated on LLaDA, Dream, Fast-dLLM, Llama-3-8B-Instruct, Qwen2.5-7B-Instruct, and Gemini-2.5-Flash-Lite.
- **Mitigations:** Do not treat sparse safety-neuron alignment as sufficient; combine mechanistic alignment with prompt-level classifiers and output filters; monitor for pruning-signature or SN-guided attack patterns; assume any DLLM derived from a known base model inherits its jailbreak surface and gate deployment accordingly.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2608.07430)  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 20 · ✨ Novelty 70 · 🎯 Relevance 78 · 🏛️ Credibility 55 · **Composite 57.65**  
**Tags:** `jailbreak`, `diffusion-llm`, `safety-neurons`, `transfer-attack`, `black-box`  
**Verification:** ✓ independently verified · closest prior art: Extends prior work on safety-neuron identification and pruning in autoregressive LLMs (Wei et al., 'Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications') and mechanistic-interpretability-driven jailbreaks; novelty is showing the property transfers into diffusion LLMs and gives a cheap black-box jailbreak with cross-family reach.

_Source: [https://arxiv.org/abs/2608.07430](https://arxiv.org/abs/2608.07430)_  ·  [← back to index](../README.md)
