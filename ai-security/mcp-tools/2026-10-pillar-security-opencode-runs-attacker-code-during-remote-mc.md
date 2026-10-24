# Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE

**Published:** Oct 19, 2026

> **Takeaway:** Treat every remote MCP server response as untrusted input to your client, never pass it to a shell, and do not rely on CVE feeds to learn about agent-tool fixes.

## TL;DR

Pillar found that opencode (versions 1.0.137 to 1.18.32 on Windows and WSL) passed an unsanitized authorization URL from a remote MCP server into a PowerShell command, giving code execution during OAuth sign-in with no user interaction. A plain https URL carries the payload, so scheme validation does not help. The same defect class was already CVE-2025-6514. Anomaly fixed it in 1.18.33 as a refactor with no advisory or CVE, so scanners will not flag old installs.

## Lessons

- No malicious install, model exploit or prompt injection is needed; connecting to a bad MCP server is enough. - _"The attack does not require installing malicious software, exploiting the AI model or tricking it through prompt injection."_
- URL scheme validation is the usual fix and it does not stop this payload. - _"Normal scheme validation does not stop it"_
- A server can turn malicious after being configured, through compromise, a hijacked registry entry or an expired domain. - _"Crucially, the server did not need to be malicious when configured."_
- The fix shipped silently, so dependency scanners cannot find affected installs. - _"did not issue a security advisory or request a CVE. As a result, conventional vulnerability scanners and dependency alerts will not identify affected installations"_

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [source](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 27 · Novelty 55 · Relevance 85 · Credibility 55 · **Composite 57** _(each 0-100)_  
**Tags:** `opencode`, `mcp`, `oauth`, `command-injection`, `windows`, `coding-agents`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: CVE-2025-6514 (mcp-remote) is the same sink; the new points are the https-URL payload that defeats scheme checks and the silent-fix disclosure gap. Verifier: CVE-2025-6514 (JFrog, mcp-remote), CVE-2025-58062, CVE-2025-10619; tripodsan sindresorhus/open issue #323 (2023, https://$(calc.exe)). Delta: same class in open  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth)_  ·  [← back to index](../README.md)
