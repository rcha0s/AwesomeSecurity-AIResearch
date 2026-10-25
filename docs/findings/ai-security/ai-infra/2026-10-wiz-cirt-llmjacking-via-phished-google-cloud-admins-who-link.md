# Wiz CIRT: LLMjacking via phished Google Cloud admins who link attacker projects to the victim's billing account

**Published:** Oct 20, 2026

> **Takeaway:** LLMjacking is a billing and IAM problem: watch who can link projects to billing and keep the org policy that limits IAM members to company domains.

## TL;DR

Wiz CIRT describes intrusions where attackers phish Google Cloud users through sponsored search ads, then enable the Gemini API, mint service-account keys, delete the domain-restriction policy, and attach attacker-controlled projects to the victim's billing account. The AI workloads run in foreign projects, so the victim sees the bill (hundreds of thousands of dollars) but never the prompts or outputs. The post gives hunting guidance for each step.

## Lessons

- The goal is to spend the victim's money on LLM calls, not to steal data. - _"threat actors hijacking cloud billing accounts to fund unauthorized AI usage."_
- Prompts and outputs stay in the attacker's project, so the victim cannot see what the usage was. - _"Because the AI workloads were processed in foreign projects, prompt contents and model outputs remained completely hidden from the victim organization, leaving the nature of the mass AI usage unknown."_
- Attackers delete the policy that limits IAM members to verified domains, then add personal accounts. - _"This action removed the guardrail that restricts Identity and Access Management (IAM) membership to verified company domains"_
- Phishing began with paid search ads for admin terms, and user awareness alone did not stop it. - _"The threat actor purchased Google Search ads for common administrative search terms such as “google cloud” and “gcp”."_
- Monitor workspace login logs for suspicious-login flags and forced re-authentication. - _"organizations should not rely on user awareness alone, but ingest and monitor Google Workspace User Log Events for suspicious login flags and anomalous re-authentication triggers."_

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [source](https://www.wiz.io/blog/from-phishing-to-llmjacking)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 26 · Novelty 48 · Relevance 75 · Credibility 50 · **Composite 51** _(each 0-100)_  
**Tags:** `llmjacking`, `gcp`, `billing-fraud`, `phishing`, `gemini-api`, `iam`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier LLMjacking write-ups focus on stolen API keys and cloud accounts; the cross-tenant billing-link variant is new in the pools. Verifier: Sysdig LLMjacking (2024) and subsequent cloud LLM abuse reports. Delta is billing-account linking to attacker-owned foreign projects, which hides prompts from t  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.wiz.io/blog/from-phishing-to-llmjacking](https://www.wiz.io/blog/from-phishing-to-llmjacking)_  ·  [← back to index](../README.md)
