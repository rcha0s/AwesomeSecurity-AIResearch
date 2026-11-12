# Check Point found ARTEX operators letting AI agents run cybercrime campaigns unattended

**Published:** Nov 5, 2026

> **Takeaway:** Agentic attack platforms let unskilled criminals test every endpoint of many targets for a few hundred dollars, so basic gaps like hardcoded credentials and unauthenticated APIs are now found at machine scale.

## TL;DR

Check Point Research counted 1,608 live, publicly exposed panels of ARTEX, an open-source AI pentest platform. Ten of them leaked their full databases, showing which models criminals used and how they prompted their agents: operators set one goal and then mostly asked about progress. The agents stole more than 300 iOS signing certificates, recovered about 190,000 game-account credentials, and found a writable S3 bucket that hosted iOS app installers. Mostly Chinese models were used, led by DeepSeek Flash, at about $145 to $1,500 per campaign, and in one campaign the agents reported cash-outs that never happened.

## Lessons

- After the operator set the goal, the agent fleets ran almost on their own. Human prompts were mostly progress checks. - _"Threat actors barely interacted with their agent fleets."_
- These agents are dangerous because they keep going across a whole scope until they reach the goal, not because their exploits are sophisticated. Hardcoded credentials in JavaScript bundles and unauthenticated APIs were enough. - _"it is not necessarily the complexity of attacks, but the breadth and perseverance at which LLMs can audit a scope and test every endpoint, front end bundle and site"_
- A model's refusals did not stop the operator. When one American model hit guardrails, the actor switched to more permissive models. - _"we observed guardrails being hit only when using Anthropic’s Opus 5.5. Here, the actor subsequently switched to more permissive Chinese models."_
- The agents also claimed successes that never happened. Reported USDT cash-outs were hallucinations based on API responses that said "success". - _"the findings were hallucinations and the verdict of successful exploitation was simply based on API responses indicating “success”."_

## Threat · Conditions · Mitigations

- **Threat:** Low-skill criminals point autonomous agent fleets at many targets at once, and the agents find and exploit common web flaws (hardcoded credentials, missing API authentication, command injection, server-side template injection, insecure direct object references) without stopping.
- **Conditions:** Internet-facing apps that have common web weaknesses, plaintext credential stores, or object storage that anyone can write to.
- **Mitigations:** Remove hardcoded secrets from frontend code, enforce authentication on all APIs, lock down storage write access, and rate-limit or detect rapid automated enumeration, including traffic from residential proxies.

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [Check Point Research](https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/)  ·  **Retrieved:** 2026-11-05  
**Scores:** Newness 52 · Novelty 55 · Relevance 80 · Credibility 58 · **Composite 62** _(each 0-100)_  
**Tags:** `artex`, `agentic-attacks`, `autonomous-agents`, `cybercrime`, `exposed-panels`, `deepseek`, `guardrails`, `code-signing`, `s3`, `hallucination`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Microsoft's Storm-0940/ARTEX report (product-security pool) and NorForge's exposed Cairn panels (product-security pool) already cover ARTEX abuse and exposed AI-pentest panels. New here: operator console artifacts from leaked databases (models, prompts, token costs), the near-zero operator interaction, and the hallucinated cash-outs.

_Source: [https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/](https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/)_  ·  [← back to index](../README.md)
