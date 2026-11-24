# Dragos canary prompts found three AI hosting providers breached

**Published:** Nov 19, 2026

> **Takeaway:** Assume every router and host on the path can read and keep your prompt, so keep live credentials and private URLs out of prompts, whatever privacy flag is set.

## TL;DR

From July to November 2026, Dragos sent about two million prompts to AI services, each carrying unique canary URLs and AWS keys, and logged every later use of them. Attackers were copying requests at three hosting providers, marketplace resellers logged and used customer prompts, and some providers fetched prompt URLs even when the request was marked Zero Data Retention. Dragos also built a route tracer that lists the routers and hosts that handled a request.

## Lessons

- Attackers copied Dragos's bait requests at three AI hosting providers, and none of the three knew until Dragos told them. Dragos says real customer requests were almost certainly copied too. - _"none of the three providers knew about their breach until we notified them"_
- In the largest breach, Dragos concluded requests were copied at the provider's front door, because some stolen keys came from requests rejected before any model ran. - _"Some of the stolen keys came from requests that the provider rejected before a model ever ran"_
- A Zero Data Retention flag did not protect a request once the attacker was inside: in two breaches, some stolen requests carried it. - _"In the other two breaches, some of the stolen requests were marked as ZDR."_
- Stolen bait keys were used to list S3 buckets and search Secrets Manager and Parameter Store, and the attacker tried to add their own IAM users. - _"listing S3 buckets and searching Secrets Manager and Parameter Store"_
- Marketplace sellers needed no exploit to read customer prompts: they listed a model at the lowest price and turned on request logging. - _"only had to list a model at the lowest price, enable request logging, and wait"_
- From July to October, one Chinese AI lab fetched the secret URLs from over half the prompts sent to its models, and U.S. hosts that resell its models triggered the same scraper. - _"fetched the secret URLs from more than half of the prompts that we sent to its models between July and October"_
- A unique canary per prompt ties any later use back to the exact prompt, model, router and privacy setting that carried it. - _"Every request that touches a token is tied back to the exact prompt, model, router, and privacy setting that carried it."_
- Route tracing found a hop the marketplace did not disclose; in one traced route it was an OpenRouter hop. - _"The OpenRouter hop was discovered by tracing and was not disclosed in the marketplace"_

## Threat · Conditions · Mitigations

- **Threat:** A router, reseller or host on the inference path can read and keep every prompt, and an attacker who breaches one can copy requests even when they carry a Zero Data Retention flag.
- **Conditions:** Applies where prompts carry credentials, private URLs or sensitive data and pass through routers, marketplaces or resold models. The providers are not named, and the findings rest on Dragos's own telemetry; one provider has since published a preliminary security notice.
- **Mitigations:** Keep live credentials and private URLs out of prompts, test each provider and router with canary prompts, and add the artex-agent and artex-judge-r121 user agents to AWS CloudTrail detections.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [www.dragos.com](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens)  ·  **Author:** HD Moore  ·  **Retrieved:** 2026-11-20  
**Scores:** Newness 73 · Novelty 60 · Relevance 85 · Credibility 50 · **Composite 69** _(each 0-100)_  
**Tags:** `canary-tokens`, `ai-routers`, `zero-data-retention`, `prompt-leakage`, `credential-theft`, `ai-supply-chain`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: arXiv 2604.08407 measured LLM API routers injecting code and stealing credentials (1 paid, 8 free). New here: canary measurement of providers, ignored Zero Data Retention flags, and route tracing.

_Source: [https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens)_  ·  [← back to index](../README.md)
