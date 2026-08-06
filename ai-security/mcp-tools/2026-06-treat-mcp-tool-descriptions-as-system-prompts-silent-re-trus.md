# Treat MCP tool descriptions as system prompts: silent re-trust poisoning

**Topic:** AI Security  ·  **Domain:** MCP & Tools  
**Source:** [source](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)  ·  **Published:** Jun 30, 2026  ·  **Retrieved:** 2026-07-16  
**Scores:** 🆕 Newness 3 · ✨ Novelty 50 · 🎯 Relevance 84 · 🏛️ Credibility 75 · **Composite 52.2**  
**Tags:** `mcp`, `tool-poisoning`, `prompt-injection`, `agent-security`, `supply-chain`  
**Verification:** ✓ independently verified · closest prior art: Invariant Labs' April 2025 MCP tool-poisoning disclosure and OWASP's ASI02/ASI04 categories; this piece is a practical defender playbook on that known class, with the 'silent re-trust' on dynamic metadata as the sharpest incremental point.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

> **Takeaway:** Version and change-review every MCP tool description as if it were a system prompt, and force re-approval whenever tool metadata changes.

## TL;DR

_The gist, not every detail - read the [full source](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) for the complete write-up._

Once agents move from reading to acting, a poisoned MCP tool description turns prompt injection into an action. An approved third-party tool's description is silently modified to tell the agent to collect and exfiltrate data; because metadata updates don't re-trigger approval, the poisoned instructions go live with no review, and every individual agent action looks legitimate.

## What to learn

- MCP mixes instructions and data in the same channel, so editing a tool's description reprograms the agent as effectively as editing its system prompt. - _"The MCP blends instructions (tool descriptions) with data, so a change to a tool's metadata can redirect the agent's behavior as effectively as a change to its system prompt."_ ✅
- The dangerous gap is 'silent re-trust' (Microsoft's term): in configurations where a tool's description change doesn't re-trigger the approval workflow, poisoned instructions become active without review. - _"In configurations where description changes do not trigger a re-approval workflow, the updated instructions become active without additional review."_ ✅
- The vulnerability is the trust boundary between systems, not any one system - each action (approved tool, inherited permissions, allowlisted endpoint) is individually legitimate. - _"The vulnerability is not in any single system; it is in the trust boundary between them"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** An upstream tool maintainer modifies a tool description to redirect an agent into collecting and exfiltrating data, with no prompt, credential, or user action involved.
- **Mitigations:** Change-review tool descriptions like system prompts; require re-approval on metadata changes; disable 'Allow all' tools; human-in-the-loop for high-impact actions; apply least agency, not just least privilege.

---

_Source: [https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)_  ·  [← back to index](../README.md)
