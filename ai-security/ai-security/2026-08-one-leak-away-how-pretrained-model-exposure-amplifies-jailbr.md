# One Leak Away: How Pretrained Model Exposure Amplifies Jailbreak Risks in Finetuned LLMs

**Published:** Aug 7, 2026

> **Takeaway:** Anyone who ships a finetune on top of an openly released base model should assume attackers will craft jailbreaks against the base and transfer them; representation-level defenses at fine-tune time are a plausible mitigation but the burden falls on the deployer, not the base model publisher.

## TL;DR

In a threat model where the attacker has the released pretrained LLM but not its private finetuned derivative, adversarial prompts optimized on the pretrained model transfer strongly to the finetuned variants. Representation-level probing shows transferable prompts are linearly separable in pretrained hidden states, motivating a Probe-Guided Projection (PGP) attack that steers optimization toward transferability-relevant directions, and a lightweight representation-space defense. Accepted at ACM CCS.

## What to learn

- Adversarial prompts optimized on the pretrained model transfer most effectively to its finetuned derivatives. - _"adversarial prompts optimized on the pretrained model transfer most effectively to its finetuned variants, revealing inherited vulnerabilities from pretrained to finetuned LLMs"_
- Transferable jailbreak prompts are linearly separable in the pretrained model's hidden states, i.e. the transferability signal is already encoded in the base. - _"transferable prompts are linearly separable within the pretrained hidden states, suggesting that transferability-relevant structure is already encoded in pretrained representations"_
- A lightweight representation-level defense mitigates pretrain-to-finetune jailbreak transfer while preserving downstream utility. - _"we demonstrate that the same representation-level insights also enable a lightweight defense that mitigates pretrain-to-finetune jailbreak transfer while preserving downstream utility"_

## Threat · Conditions · Mitigations

- **Threat:** Attacker with access only to an open-weights base model crafts jailbreaks that transfer into a downstream private finetune, bypassing the deployer's safety training without ever touching the deployer's own weights.
- **Conditions:** Base model is publicly available (open weights); deployer's finetune derives from that base without changing the underlying representation geometry that carries transferable attacks.
- **Mitigations:** During finetuning, add a representation-space regularizer or projection that suppresses linearly-separable jailbreak directions from the base; supplement input filters with output-side refusal checks; run pre-deployment red-team runs that specifically use attacks optimized against the base weights.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2512.14751)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 70 · Relevance 80 · Credibility 52 · **Composite 57.78**  
**Tags:** `jailbreak`, `finetuning`, `transfer-attack`, `adversarial`, `open-weights`  
**Verification:** ✓ independently verified · closest prior art: Extends the general 'jailbreak transfer' line (Zou et al. universal adversarial suffixes; cross-model transfer studies) by specializing to the pretrain-to-finetune direction and probing the hidden-state structure that carries the transfer.

_Source: [https://arxiv.org/abs/2512.14751](https://arxiv.org/abs/2512.14751)_  ·  [← back to index](../README.md)
