# Northflank breach exposed customer secrets, and stolen AI API keys were used

**Published:** Oct 31, 2026

> **Takeaway:** AI API keys stored as platform environment variables are now a primary target, so scope them narrowly, cap their spend and be ready to rotate them in minutes.

## TL;DR

Cloud hosting platform Northflank told all customers on October 30, 2026 to assume their environment variables were decrypted and to rotate every secret, after Wiz alerted it to a breach. Customers then reported unauthorized use of AI API keys they had stored on the platform. Northflank has not said how attackers got in or how many customers were affected; Wiz counts at least nine incidents at AI developer platforms in October, several aimed at AI service credentials.

## Lessons

- The platform told customers to treat every stored environment variable as stolen, not only the ones known to be abused. - _""Assume all environment variables have been decrypted. Disable/rotate all keys," Northflank warned in an October 30 update."_
- Customers reported unauthorized use of the AI API keys they had stored on the platform. - _""Users have reported unauthorised use of AI API keys supplied to the Northflank platform," the company said."_
- Wiz frames Northflank as one of at least nine October incidents at AI developer platforms, several targeting AI credentials. - _"Wiz identified at least nine security incidents affecting AI development platforms during the month, including Northflank,"_
- In two separate LLMjacking cases Wiz investigated, not tied to Northflank, stolen enterprise credentials ran up about $100,000 of Bedrock usage. - _"compromised enterprise credentials were used to make approximately 2.5 million Amazon Bedrock API calls, generating approximately $100,000 in AI usage"_

## Threat · Conditions · Mitigations

- **Threat:** Platform breach exposing customer secrets, with AI API keys abused for paid inference.
- **Conditions:** AI provider keys stored as environment variables or secrets on a third-party hosting platform.
- **Mitigations:** Rotate all platform-stored secrets, enable audit logs, set provider spend caps and model allowlists, and prefer short-lived credentials.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [X list](https://www.bleepingcomputer.com/news/security/northflank-security-breach-leads-to-abuse-of-customers-ai-api-keys/)  ·  **Author:** @Dinosn  ·  **Retrieved:** 2026-10-31  
**Scores:** Newness 12 · Novelty 30 · Relevance 78 · Credibility 60 · **Composite 44** _(each 0-100)_  
**Tags:** `llmjacking`, `api-keys`, `secrets`, `paas-breach`, `incident-response`, `black-october`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier Black October disclosures in the pool (Railway, OpenCode, Warp) and Unit 42's token-jacking and Datadog's Bedrock key-validation reports; Northflank is a new victim of the same pattern.

_Source: [https://www.bleepingcomputer.com/news/security/northflank-security-breach-leads-to-abuse-of-customers-ai-api-keys/](https://www.bleepingcomputer.com/news/security/northflank-security-breach-leads-to-abuse-of-customers-ai-api-keys/)_  ·  [← back to index](../README.md)
