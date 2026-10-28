# SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents

**Published:** Oct 20, 2026

> **Takeaway:** Ransomware crews now run AI-operated intrusion pipelines against edge devices, so patching internet-facing remote-access software is the practical defense.

## TL;DR

SOCRadar found an exposed command-and-control server holding the session logs, knowledge base and source code of Phantom, a framework affiliates of INC and The Gentlemen ransomware used. Operators ran OpenCode with OpenRouter-hosted commercial models across 133 sessions, spending over $23,920 on AI APIs. They exploited edge systems such as FortiClient EMS, SimpleHelp and cPanel, tracked victims in AI-managed knowledge bases, and staged 46 INC encryptor builds.

## Lessons

- AI was the operational core: coding agents plus commercial models drove intrusions. - _"Operators ran intrusions through OpenCode with OpenRouter-hosted commercial models, logging 8,257 messages across 133 sessions"_
- Targets were edge and remote-access systems. - _"The operators exploited edge and remote-access systems at scale, including FortiClient EMS, SimpleHelp, cPanel and VPN gateways."_
- AI also handled victim tracking and credential bookkeeping. - _"They used AI-managed knowledge bases to track victims, stolen credentials and campaign progress."_
- OPSEC failures, not defenders, exposed the operation. - _"The campaign came to light in late September 2026 after OPSEC failures left the operators’ source code, credentials and AI session logs exposed."_

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [source](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 23 · Novelty 55 · Relevance 78 · Credibility 50 · **Composite 53** _(each 0-100)_  
**Tags:** `ransomware`, `ai-agents`, `edge-devices`, `inc-ransomware`, `the-gentlemen`, `opencode`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: CrowdStrike and NorForge describe criminals' agent harnesses; this adds ransomware affiliates, a deployment wave and spend figures from the operators' own logs. Verifier: Anthropic GTG-1002 / threat intel reports on AI-orchestrated intrusion; Gambit Security staging-server report; CrowdStrike agentic campaigns. Delta: exposed ope

_Source: [https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/)_  ·  [← back to index](../README.md)
