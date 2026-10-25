# Zenity AgentCorruption: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials; its default role reached every agent in the region

**Published:** Oct 15, 2026

> **Takeaway:** Treat an agent's HTTP tool as an SSRF primitive and give every agent its own least-privilege role; a shared default role turns one injected agent into a region-wide breach.

## TL;DR

AgentCore agents run in Firecracker microVMs that didn't block the instance metadata service (IMDS), so any HTTP-capable tool became a server-side request forgery (SSRF) path to the agent role's credentials. The default execution role was scoped to all AgentCore resources in the region: it could list agents, pull their images, invoke them, read all conversations, write long-term memories and read Secrets Manager. AWS moved AgentCore to IMDSv2-only in February 2026 and tightened the default role by late September, while calling the behavior documented and expected.

## Lessons

- An agent tool that makes HTTP requests from inside the runtime is an SSRF primitive, and prompt injection is enough to aim it at the metadata service. - _"any agent tool capable of making HTTP requests would send those requests directly from within the instance itself"_
- The blast radius came from the default role, not the SSRF: it was scoped region-wide, not to the single agent. - _"The default AgentCore role wasn’t scoped to the specific agent."_
- Write access to agent memory gives persistence: an attacker can plant memories that steer other users' agents in later sessions. - _"create new memories across different agents and users"_
- Credential brokering by a gateway doesn't help if the agent's own role can read the broker's secrets. - _"enabling an attacker to access all credentials AgentCore has meant to keep away from the agent"_

## Threat · Conditions · Mitigations

- **Threat:** An external user with chat access to one exposed AgentCore agent uses prompt injection to make it fetch IMDS credentials, then uses the overprivileged default role to invoke other agents, read all conversations, plant memories and read stored secrets.
- **Conditions:** Agent deployed on AWS Bedrock AgentCore with an HTTP-capable tool and the pre-September-2026 default execution role; agent reachable by untrusted users.
- **Mitigations:** Use per-agent least-privilege execution roles, enforce IMDSv2 and block link-local egress from agent tools, isolate customer-facing agents in separate accounts, and monitor agent roles for discovery and cross-agent API calls.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [tl;dr sec (curator link)](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 25 · Novelty 35 · Relevance 88 · Credibility 70 · **Composite 54** _(each 0-100)_  
**Tags:** `aws`, `bedrock-agentcore`, `imds`, `ssrf`, `prompt-injection`, `iam`, `least-privilege`, `memory-poisoning`, `secrets-manager`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Classic cloud SSRF-to-IMDS (Capital One 2019) and pool claims imdsv1-must-be-disabled-on-agent-workloads and ssrf-guards-must-cover-agent-outbound-calls; new here is a managed agent platform whose shared default role turned one agent's credentials into cross-agent conversation reading, memory poisoning and secret theft.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model)_  ·  [← back to index](../README.md)
