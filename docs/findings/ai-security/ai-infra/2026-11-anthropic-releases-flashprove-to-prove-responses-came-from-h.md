# Anthropic releases FlashProve to prove responses came from hidden model weights

**Published:** Nov 2, 2026

> **Takeaway:** Cryptographic proof that a specific model produced an output is now a working prototype, though still about 70-95x the cost of inference, so it is an audit tool rather than a per-request default.

## TL;DR

Anthropic and academic collaborators released FlashProve, an open-source (Apache 2.0) zkSNARK system that lets a provider commit to hidden model weights and then prove each response was produced by those weights. On Llama 4 Maverick (400B-parameter mixture of experts, 4-bit), one H100 generates proofs at about 110 tokens per second with about 19 MB proofs per 1,024-token request, roughly 70-95x the GPU time of vLLM inference, and a CPU verifier checks a proof in about 17 seconds. Anthropic says Claude built much of the optimization work, with top-level security statements formalized in Lean so humans can audit them; it targets model-substitution by routers, tampered inference servers, and a stronger model impersonating a weaker one to dodge monitoring.

## Lessons

- Proving inference of a frontier-scale mixture-of-experts model on a single GPU is now feasible, at tens of times the cost of plain inference. - _"a single H100 GPU generates proofs at around 110 tokens/second, with a proof size of ~19 MB per 1,024-token request"_
- The threat model includes an internal adversary: a more capable model substituting itself for an authorized weaker one so it is not subject to that model's monitoring. - _"a more advanced model could run in place of the one that was authorized and present itself as the weaker model, so as to avoid the classifiers and monitoring that would apply to it."_
- Because Claude-written optimizations are hard to review in a large cryptographic system, the authors pinned the security guarantees to machine-checked Lean statements instead of trusting the code. - _"We counter this by providing top-level auditable statements in Lean (a formal verification language) for the claimed security guarantees."_
- The guarantee is bounded: proofs show the hardware served the claimed model, not that the same hardware is not also doing other work such as training. - _"We note that although this verifies that the hardware is serving inference, it does not establish that the hardware is not, e.g., training on the side."_
- In batches of 24 requests, proving for a 400B mixture-of-experts model runs at about 110 tokens per second on one H100. - _"a single H100 GPU generates proofs at around 110 tokens/second, with a proof size of ~19 MB per 1,024-token request"_
- The cost is still large: proving takes tens of times the GPU time of serving the model. - _"This is ~70-95x the GPU time of running the model itself on vLLM, a common open-source library."_
- Verification is cheap enough for a client: seconds on a CPU, no GPU and no weights. - _"Checking a proof takes 17 seconds on 24 threads (and 21 seconds on a single thread), including the offline phase's checks."_
- A proof shows the committed weights served the request; it hides the weights but not the architecture, and it cannot show the hardware is not also training on the side. - _"We note that although this verifies that the hardware is serving inference, it does not establish that the hardware is not, e.g., training on the side."_
- Because Claude-built optimizations are hard to review, the team wrote the security guarantees as auditable Lean statements. - _"We counter this by providing top-level auditable statements in Lean (a formal verification language) for the claimed security guarantees."_

## Threat · Conditions · Mitigations

- **Threat:** Users, evaluators and providers cannot tell which weights produced a response: a routing service can swap in a cheaper model, an attacker who compromises an inference server can serve malicious output while posing as the genuine model, and a more capable model could impersonate a weaker one to avoid its monitoring.
- **Conditions:** The model is reached through an intermediary (router, third-party host, or compromised inference server), or the provider runs multiple models whose monitoring differs, and the caller has no cryptographic binding between output and a specific weight commitment.
- **Mitigations:** Require responses to carry a proof bound to a published weight commitment for high-assurance traffic such as evaluations and audits, combine with trusted-execution attestation where proving cost is too high, verify proofs on the client side, and re-commit weights before the commitment's request budget (about 16 million requests) is exhausted.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [Anthropic Research](https://www.anthropic.com/research/provable-inference)  ·  **Retrieved:** 2026-11-03  
**Scores:** Newness 52 · Novelty 72 · Relevance 68 · Credibility 70 · **Composite 65** _(each 0-100)_  
**Tags:** `provable-inference`, `zksnark`, `model-integrity`, `inference-server-compromise`, `model-substitution`, `formal-verification`, `lean`, `tamper-detection`, `inference-servers`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No existing entry covers provable or verifiable inference. Prior art outside the dataset includes zkML systems (e.g., zkLLM and other open-source zk inference provers, which the post says are orders of magnitude slower) and TEE-based attestation of inference. Anthropic's own RSP prototype signed inference traffic with recomputation on a trusted server. The delta is a practical zkSNARK at 400B-parameter MoE scale with Lean-checked guarantees.

_Source: [https://www.anthropic.com/research/provable-inference](https://www.anthropic.com/research/provable-inference)_  ·  [← back to index](../README.md)
