# Token jacking: stolen AI API keys resold through gray-market 'transfer stations', costing victims up to ~$1M

**Topic:** AI Security  ·  **Domain:** AI Gateway & Credential Theft  
**Source:** [Unit 42 (Palo Alto Networks)](https://unit42.paloaltonetworks.com/ai-token-jacking/)  ·  **Author:** Unit 42  ·  **Published:** Aug 6, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 64 · 🎯 Relevance 76 · 🏛️ Credibility 77 · **Composite 58.52**  
**Tags:** `credential-theft`, `ai-gateway`, `supply-chain`, `api-keys`, `npm`, `agentic-identity`  
**Verification:** ✓ independently verified · closest prior art: Classic cloud access-key theft and cryptojacking (e.g. stolen AWS keys spun up for mining); token jacking is the AI-billing analogue, with the transfer-station resale market and npm-worm harvesting as the newer elements.

> **Takeaway:** Stolen AI tokens have a liquid resale market now; cap spend, alert on usage anomalies, and move from long-lived keys to short-lived gateway-brokered tokens.

## TL;DR

_The gist, not every detail - read the [full source](https://unit42.paloaltonetworks.com/ai-token-jacking/) for the complete write-up._

Unit 42 documents a rising incident class where attackers steal developers' AI API keys (tokens) and route them through gray-market proxy 'transfer stations' (e.g. new-api/one-api) that resell frontier-model access at a discount. Because most providers bill cyclically and don't cap usage by default, victims can accrue enormous charges before noticing. Keys are increasingly harvested by self-propagating npm supply-chain worms.

## What to learn

- AI API keys are now a directly monetizable asset: stolen tokens are resold through proxy 'transfer stations', so treat model-access credentials as high-value secrets, not convenience tokens. - _"More recently, attackers have stolen these keys using poisoned, self-propagating npm packages downloaded by unsuspecting developers."_ ✅
- Default uncapped, cyclically-billed AI usage turns a leaked key into an open-ended financial liability discovered only after the bill. - _"This led to nearly a million dollars in charges before discovery and containment."_ ✅
- The concrete defensive move is to kill long-lived keys in favor of short-lived tokens behind a governed AI gateway. - _"Migrate from long-term access keys to short-term bearer tokens to limit the potential window of damage."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Attackers steal developer AI API keys and resell programmatic model access via gray-market proxy 'transfer stations', generating large fraudulent usage billed to the victim.
- **Conditions:** Applies where AI provider keys are long-lived, embedded in dev/build environments or repos, and accounts allow uncapped usage with weak anomaly alerting; risk is amplified by npm supply-chain worms that harvest environment secrets.
- **Mitigations:** Short-lived bearer tokens brokered by an AI gateway tied to a managed machine identity; hard spend limits with baseline-deviation alerts; review of privileged accounts that can raise limits or disable logging; egress/network boundaries so stolen keys can't be used off-net; dependency hygiene to keep credential-stealing packages out of the pipeline.

---

_Source: [https://unit42.paloaltonetworks.com/ai-token-jacking/](https://unit42.paloaltonetworks.com/ai-token-jacking/)_  ·  [← back to index](../README.md)
