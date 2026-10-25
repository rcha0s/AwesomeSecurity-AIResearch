# obsidian-tc tool server: any valid token could read, write, or delete any configured vault (CVE-2026-77366)

**Published:** Oct 23, 2026

> **Takeaway:** Multi-tenant tool servers must enforce the caller's tenant once at dispatch and never trust a caller-supplied vault or workspace parameter.

## TL;DR

obsidian-tc, an npm tool server for Obsidian vaults, did not check the vault named in a tool call against the vault the caller's token was bound to. The JSON Web Token (JWT) carried no vault claim and the folder access list was one global instance, so any valid token could reach every vault across about 90 tool sites. Only the `resources/read` surface had the check; version 1.3.1 adds one central guard in dispatch.

## Lessons

- Tenant binding was missing at every layer: the token had no vault claim and the ACL was global. - _"the folder ACL was a single global instance and the JWT carried no vault claim"_
- Per-tool authorization drifts; one surface had the check while about 90 tool sites did not. - _"`resources/read` was the only surface that already guarded this."_
- The fix is a single central check in dispatch, before the scope check, instead of per-tool checks. - _"A central `input.vault === ctx.vaultId` guard was added in dispatch before the scope check."_
- Without the patch, isolate tenants by process or credential. - _"Run a single vault per server process, or isolate each tenant on a separate process/credential."_

## Threat · Conditions · Mitigations

- **Threat:** Any holder of a valid token reads, writes, or deletes data in other tenants' vaults by setting `input.vault`.
- **Conditions:** obsidian-tc < 1.3.1 serving more than one configured vault to different callers.
- **Mitigations:** Upgrade to 1.3.1+; or run one vault per server process / separate credential per tenant.

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-84c9-qqpq-2pq5)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 25 · Novelty 30 · Relevance 65 · Credibility 70 · **Composite 45** _(each 0-100)_  
**Tags:** `authorization`, `idor`, `multi-tenant`, `tool-server`, `jwt`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Classic insecure direct object reference / CWE-639 in a new setting; nearest pool items are MCP server security entries (e.g. BurpMCP-Ultra per-session token and scope gate), none covering cross-tenant tool dispatch. Verifier: Classic IDOR / CWE-639 cross-tenant authorization bypass; tracker already covers MCP server authz/fail-open bugs (e.g. AWS API MCP Server fail-open CVE-2026-16584, BurpMCP scope-gate pattern), so the delta is a small npm tool server's missing tenant binding.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://github.com/advisories/GHSA-84c9-qqpq-2pq5](https://github.com/advisories/GHSA-84c9-qqpq-2pq5)_  ·  [← back to index](../README.md)
