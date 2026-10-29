# MCP Inspector fixes two critical one-click RCE flaws in version 1.0.3

**Published:** Oct 21, 2026

> **Takeaway:** Treat MCP debugging tools as code-execution surfaces: update Inspector to 1.0.3 and never point it at servers you do not trust.

## TL;DR

On 2026-10-21 the MCP project published two critical advisories (CVSS 9.6 each, no CVE id yet) for MCP Inspector, the debugging tool many developers run against untrusted MCP servers. GHSA-4fc4-wcmh-4g86: a malicious remote server redirects the OAuth callback with transport=stdio and serverCommand parameters, and Inspector runs that command locally. GHSA-6x67-4w4w-9f3w: a malicious MCP App steals the proxy auth token through a same-origin sandbox and then calls the stdio endpoint. Both affect versions up to 1.0.2 and are fixed in 1.0.3.

## Lessons

- The OAuth callback trusted configuration read from its own URL, so an attacker-controlled authorization server could switch the transport to a local command. - _"The OAuth callback must not read any Inspector configuration from the callback URL."_
- Connecting to a hostile MCP server was enough: no tool call and no further click was needed for command execution. - _"Connecting to an unknown MCP can immediately trigger RCE without any futher interaction with tools."_

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [github.com](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 0 · Novelty 70 · Relevance 90 · Credibility 55 · **Composite 56** _(each 0-100)_  
**Tags:** `mcp`, `mcp-inspector`, `rce`, `oauth`, `ghsa`, `developer-tools`  
**Also reported by:** [GitHub advisory GHSA-6x67-4w4w-9f3w](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-6x67-4w4w-9f3w) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: CVE-2025-49596 (proxy without authentication) and CVE-2025-58444 (XSS to command execution) hit the same tool earlier; these two are new attack paths (OAuth callback parameters, MCP App sandbox token theft).

_Source: [https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)_  ·  [← back to index](../README.md)
