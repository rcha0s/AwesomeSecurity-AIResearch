# Todoist MCP HTTP server lets websites edit Todoist data via DNS rebinding

**Published:** Nov 19, 2026

> **Takeaway:** Binding an MCP server to loopback is not authentication: HTTP-mode MCP servers need Host and Origin validation plus a per-run caller secret.

## TL;DR

The optional self-hosted todoist-mcp-http server dispatches POST /mcp without checking Host or Origin, and its middleware checks only the server's own Todoist token, not the caller. A malicious website can use DNS rebinding to reach the loopback server and call tools such as add-tasks, complete-tasks and delete-object using the operator's TODOIST_API_KEY. Fixed in release 10.3.3 (CVE-2026-76807, rated critical); the stdio entrypoint is not affected.

## Lessons

- Token middleware that validates the server's backend credential does not authenticate the browser caller; both checks are needed. - _"The middleware validates the server's Todoist backend token, not the browser caller."_
- Host and Origin checks reduce rebinding exposure but are not a replacement for a caller secret, even on loopback. - _"Host and Origin validation reduce DNS-rebinding exposure, but they are not caller authentication."_
- Only the HTTP transport is browser-reachable; the stdio transport avoids this attack class, making it the safer default for local MCP servers. - _"Keep stdio as the safest default local transport."_
- The server holds the real API key, so a rebound browser request inherits the operator's full tool surface, including writes and deletes. - _"Tool execution uses the server-held `TODOIST_API_KEY` to mutate Todoist state."_

## Threat · Conditions · Mitigations

- **Threat:** A public website the victim visits can use DNS rebinding to operate the victim's local todoist-mcp-http server with the operator's Todoist API key, creating, completing, updating and deleting tasks, comments, reminders and other Todoist objects.
- **Conditions:** @doist/todoist-mcp 10.3.1 (before 10.3.3) with the optional Streamable HTTP server todoist-mcp-http running; the stdio entrypoint is not affected, and the default loopback bind does not prevent rebinding.
- **Mitigations:** Upgrade to 10.3.3 or later, validate Host and reject untrusted Origin before MCP dispatch, require a per-run local bearer token, enable the SDK's DNS rebinding protection with explicit allowlists, and prefer the stdio transport.

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-833v-v58w-294h)  ·  **Retrieved:** 2026-11-20  
**Scores:** Newness 28 · Novelty 25 · Relevance 70 · Credibility 70 · **Composite 46** _(each 0-100)_  
**Tags:** `mcp`, `dns-rebinding`, `todoist`, `streamable-http`, `loopback`, `api-key`, `ghsa`, `cve-2026-76807`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: data/ai-security.json DNS-rebinding MCP entries (DebugMCP, NextDNS MCP, mysql-mcp-server SSE, obsidian-tc) and the claim localhost-agent-servers-are-reachable-from-any-webpage; this is the same class applied to the Todoist MCP HTTP server, with the minor additional point that the middleware checks the backend token rather than the caller.

_Source: [https://github.com/advisories/GHSA-833v-v58w-294h](https://github.com/advisories/GHSA-833v-v58w-294h)_  ·  [← back to index](../README.md)
