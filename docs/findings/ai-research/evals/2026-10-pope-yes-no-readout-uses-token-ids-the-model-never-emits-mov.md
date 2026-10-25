# POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains

**Published:** Oct 19, 2026

> **Takeaway:** If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.

## TL;DR

Reproducing a POPE hallucination result, the authors found the two-token logit readout compares 'yes'/'no' token IDs that LLaVA-1.5 never generates, because SentencePiece emits space-prefixed ' Yes'/' No'. Fixing the readout shifts adversarial F1 by 6.13 points, more than the gain five of six surveyed papers report, and none of those papers states its readout. Porting token IDs across tokenizer families drops F1 to 0.00, while a tokenizer-derived readout stays at 0.80-0.92.

## Lessons

- Logit-based yes/no scoring can silently read token IDs the model never produces. - _"Across 9,000 greedy-decode questions spanning all three splits, neither ID is generated even once."_
- The readout choice alone moves the score by more than most claimed improvements, and papers don't report it, so their gains aren't comparable. - _"That 6.13-point adversarial shift exceeds the adversarial gain reported by five of the six papers we surveyed. None of them states its readout"_
- Hard-coded token IDs break completely across tokenizer families; derive the readout set from each model's tokenizer. - _"porting the LLaVA-1.5 IDs verbatim drops F1 to 0.00 on the two disjoint-vocabulary models"_

---

**Topic:** AI Research  ·  **Domain:** Evaluation & Benchmarks  
**Source:** [source](https://arxiv.org/abs/2610.25964)  ·  **Retrieved:** 2026-10-22  
**Scores:** Newness 25 · Novelty 70 · Relevance 65 · Credibility 55 · **Composite 55** _(each 0-100)_  
**Tags:** `evals`, `benchmarks`, `tokenization`, `reproducibility`, `vlm`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Known prompt-format and tokenization sensitivity of evals (few-shot formatting brittleness, lm-eval-harness answer-extraction differences); the specific never-emitted POPE readout IDs and their size of effect are new.

_Source: [https://arxiv.org/abs/2610.25964](https://arxiv.org/abs/2610.25964)_  ·  [← back to index](../README.md)
