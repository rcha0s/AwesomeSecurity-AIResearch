# Fireworks AI discloses second breach reached through a third-party cloud provider

**Published:** Nov 10, 2026

> **Takeaway:** Fireworks AI's second breach in weeks came through a third-party cloud host, and exposed customer data and incomplete model weights.

## TL;DR

Inference provider Fireworks AI, already handling an early-October incident in which attackers read environment variables holding API keys and tokens (which it tied to a financially motivated group reselling stolen LLM access, called LLMjacking), disclosed a second breach. A third-party cloud provider hosting its research and development machines was compromised on October 23, and on October 24 the intruder used that access to reach Fireworks development machines and run an unauthorized workload, exposing resource metadata, billing information, and incomplete model weights and datasets for some customers. Fireworks says it revoked credentials and service accounts, restricted network pathways, isolated systems and tightened storage access, and is working with Palo Alto Networks Unit 42.

## Lessons

- Environment variables used as a secrets store are a high-value target at AI inference providers. - _"attackers accessed environment variables containing API keys and tokens stored as secrets for a limited number of accounts"_
- Fireworks attributes the first incident to a group that sells stolen LLM access through illicit routing gateways, a financial motive distinct from data theft. - _"aimed at selling tokens from unauthorized access to Large Language Models (LLMs) to illicit routing gateways"_
- Development and research machines hosted at a third-party cloud provider became the path in, so they belong in the same threat model as production. - _"A third-party cloud provider that hosted Fireworks R&D machines experienced a security incident on October 23."_

## Threat · Conditions · Mitigations

- **Threat:** A financially motivated actor steals API keys and tokens from an AI inference provider, and separately pivots from a compromised third-party cloud host to development machines to reach customer metadata, billing data, model weights and datasets.
- **Conditions:** Secrets stored as environment variables readable by the attacker; development machines at an outside cloud provider with network paths to internal data storage and analytics systems.
- **Mitigations:** Revoke and replace credentials and service accounts, restrict unauthorized network pathways, isolate affected systems, tighten access to data storage and analytics systems, and have customers rotate API keys and watch usage.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [X list](https://www.bleepingcomputer.com/news/security/fireworks-ai-discloses-new-breach-after-cloud-provider-hack/)  ·  **Author:** @Dinosn  ·  **Retrieved:** 2026-11-10  
**Scores:** Newness 49 · Novelty 30 · Relevance 60 · Credibility 60 · **Composite 48** _(each 0-100)_  
**Tags:** `llmjacking`, `api-keys`, `third-party-risk`, `incident-response`, `ai-infrastructure`, `model-weights`, `breach`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Google and Wiz LLMjacking reports.

_Source: [https://www.bleepingcomputer.com/news/security/fireworks-ai-discloses-new-breach-after-cloud-provider-hack/](https://www.bleepingcomputer.com/news/security/fireworks-ai-discloses-new-breach-after-cloud-provider-hack/)_  ·  [← back to index](../README.md)
