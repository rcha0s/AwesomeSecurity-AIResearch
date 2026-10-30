# Paper proves models can hide capabilities that audits cannot find

**Published:** Oct 9, 2026

> **Takeaway:** A clean capability evaluation cannot prove a model lacks a dangerous capability if the model's builder is adversarial.

## TL;DR

Draguns, Motwani, Douglas and Schroeder de Witt (arXiv 2610.13928, accepted at NeurIPS 2026) build backdoors that embed an encrypted neural network inside a host model's weights. It decrypts and runs only on a secret trigger, and under cryptographic assumptions it stays hard to elicit even with full weight access. Fine-tuning, weight noising, gradient-based trigger search and latent adversarial training did not surface it on a small chemical-reaction proxy task.

## Lessons

- The construction hides an arbitrary computation, not just a fixed string, behind a secret trigger. - _"constructing backdoor attacks that embed encrypted neural networks within host model weights, decrypting and executing them only upon receiving a secret trigger"_
- The result bounds what elicitation-based audits can promise when the model provider is untrusted. - _"reveal a limit of elicitation-based capability audits"_

---

**Topic:** AI Security  ·  **Domain:** Red-Teaming & Threat Modeling  
**Source:** [arxiv.org](https://arxiv.org/abs/2610.13928)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 19 · Novelty 75 · Relevance 70 · Credibility 50 · **Composite 56** _(each 0-100)_  
**Tags:** `backdoor`, `capability-evals`, `model-audits`, `cryptography`, `neurips-2026`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier work hid fixed strings behind digital lockers (planted backdoors); this paper extends the idea to arbitrary computations.

_Source: [https://arxiv.org/abs/2610.13928](https://arxiv.org/abs/2610.13928)_  ·  [← back to index](../README.md)
