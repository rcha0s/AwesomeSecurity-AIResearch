# Microsoft shows phished device codes can hijack GitHub Copilot CLI sessions

**Published:** Nov 17, 2026

> **Takeaway:** Treat agent OAuth grants as high-value credentials: restrict remote control, session sync and memory, and teach developers to approve only device codes they started.

## TL;DR

Microsoft researchers ran a lab simulation where a victim approved an attacker-started OAuth device-code request for GitHub Copilot CLI. With that one approval they could steer a remote-enabled agent session, plant false memory entries, read synced sessions and reach private repositories. These are proof-of-concept results, not attacks seen in the wild, and each depends on account permissions and enabled features.

## Lessons

- Device-code phishing works on any public client that supports the device flow, and the attacker picks the scopes, so AI agent CLIs inherit the risk. - _"any public client that supports the device flow can be abused the same way, and the attacker chooses the requested scopes when starting the flow"_
- A real github.com verification page proves nothing about who started the request, so domain checks do not help users. - _"the legitimate domain alone does not establish who initiated the request"_
- Agent memory gives the attacker persistence: planted entries can influence later sessions after the sign-in is revoked, and disabling memory does not delete them. - _"does not automatically delete entries already stored, so review the saved content during incident response"_
- Findings are lab proof-of-concepts using features working as designed, bounded by local approvals and account permissions. - _"proof-of-concept results showing how existing features, working as designed, could be abused after a phished authorization"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker starts an OAuth device-code request with a device-flow client, lures the victim into approving it on the real GitHub page, then acts with the granted scopes against the Copilot CLI agent and the account.
- **Conditions:** Victim must approve the attacker's code. Steering needs remote control enabled and an active online session allowed by org policy. Session reads need cloud session storage. Memory edits need Copilot Memory enabled. Repo access follows requested scopes and account permissions.
- **Mitigations:** Approve device codes only for sign-ins you started, restrict Copilot remote control, session sync and memory to what is needed, revoke unexpected OAuth authorizations, limit repo roles, and connect GitHub to Defender for Cloud Apps for detections.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/17/the-risks-of-device-code-authentication-for-ai-coding-agents/)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 24 · Novelty 50.0 · Relevance 78 · Credibility 69 · **Composite 55** _(each 0-100)_  
**Tags:** `device-code-phishing`, `oauth`, `coding-agents`, `github-copilot-cli`, `agent-memory`, `remote-control`, `identity`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Unit 42 'Four stacked evasion techniques hide device-code phishing' and the Skyw4lker device-code campaign entry cover the phishing side; no prior entry covers device-code abuse of a coding-agent CLI with remote steering and memory planting.

_Source: [https://www.microsoft.com/en-us/security/blog/2026/11/17/the-risks-of-device-code-authentication-for-ai-coding-agents/](https://www.microsoft.com/en-us/security/blog/2026/11/17/the-risks-of-device-code-authentication-for-ai-coding-agents/)_  ·  [← back to index](../README.md)
