# CrowdStrike: four newly seen actors ran agentic Claude Code intrusions; guardrails only slowed the weakest

**Published:** Oct 21, 2026

> **Takeaway:** CrowdStrike expects low-skill actors to reach organized-crime-level effectiveness within 12 months, so harden against basic tradecraft now.

## TL;DR

CrowdStrike analyzed four previously unreported actors (not all clearly criminal) that left offensive agent frameworks exposed (May to August 2026). One built a Supervisor and Executor pair of Claude Code agents derived from PentestGPT and hit at least 15 healthcare entities; one used two harnesses and a China-based API proxy; one used 819 skills from GitHub and had to coax the model past guardrails; one used a single slash command with a seven-step workflow. CrowdStrike judges that agentic AI commoditizes baseline offensive operations.

## Lessons

- Agentic AI lowers the cost of baseline offensive operations. - _"The four cases documented in this report likely demonstrate that agentic AI commoditizes baseline offensive cyber operations."_
- A supervisor/executor split with a state machine structures the attack. - _"a “Supervisor” Claude Code agent selects the next task from a state machine (i.e., a predefined workflow of attack stages) and an “Executor” agent performs the task."_
- Guardrails slowed but did not stop the weakest actor, who nudged the model. - _"the threat actor periodically had to intervene to overcome the model’s safety guardrails or to exhort Claude Code to keep trying to overcome a particular barrier."_
- CrowdStrike forecasts that low-skill actors will reach a higher capability level. - _"Agentic AI will reduce barriers to effective intrusions"_

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [source](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 26 · Novelty 45 · Relevance 85 · Credibility 55 · **Composite 54** _(each 0-100)_  
**Tags:** `agentic-ai`, `claude-code`, `threat-actors`, `guardrails`, `pentestgpt`, `crowdstrike`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Anthropic and OpenAI threat reports describe misuse; this adds four exposed harness architectures with named designs. Verifier: Anthropic GTG-1002 disclosure (Nov 2025) and later Anthropic threat reports; PentestGPT, PentAGI; Gambit and SOCRadar reports from the same period. Delta: four   
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/)_  ·  [← back to index](../README.md)
