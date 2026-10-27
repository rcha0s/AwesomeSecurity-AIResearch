# Microsoft DevLabs DebugMCP has drive-by RCE via DNS rebinding

**Published:** Sep 25, 2026

> **Takeaway:** Any local MCP server with an execution tool is a drive-by RCE target unless it validates Host and Origin, requires authentication and a session, and rejects remote (UNC or URL) paths.

## TL;DR

DebugMCP, Microsoft's VS Code extension that lets AI agents drive the debugger, starts an unauthenticated MCP server on port 3001 as soon as it is installed. It used a custom Express setup without the MCP SDK's Host and Origin header checks, and ran in stateless mode, so one no-cors request from a DNS-rebound webpage could call start_debugging directly. Given a Windows UNC path, the Python launcher fetched and ran a script from the attacker's SMB share. Microsoft fixed it quietly in 1.2.0 with no advisory.

## Lessons

- Installing the extension starts a network listener with no authentication. No further step by the user is needed. - _"From this single installation click,the server is automatically started and listening on port 3001 without authentication,opening the door to RCE."_
- The MCP SDK's DNS-rebinding protection only applies if you use its preconfigured app. Custom Express servers have to add the Host and Origin checks themselves. - _"However,the library still relies on maintainers to use header validation middleware functions in case of custom express configuration."_
- Stateless transport mode skips the initialize handshake and session checks, so a single blind request can call a tool. - _"When sessionIdGenerator is undefined,validateSession returns immediately without checking anything."_
- A file-path argument passed to an execution primitive becomes remote code loading on Windows via UNC paths, so the attacker needs no prior file on disk. - _"This feature enabled us to make DebugMCP pass the path to VS Code’s debugging infrastructure, which passed it to the Python launcher, which reached out to the attacker’s SMB share and loaded the file."_
- The fix shipped without a version bump or advisory, so users and scanners had no signal to upgrade. - _"The fix was silently shipped (no version bump, no advisory) and is included in version 1.2.0 and later."_

## Threat · Conditions · Mitigations

- **Threat:** Visiting a malicious webpage runs code on the developer's machine via DNS rebinding to the local DebugMCP server. That exposes cloud keys, SSH keys, GitHub tokens and VPN sessions. Indirect prompt injection could also make an agent open files outside VS Code workspace trust, which the authors say the fix does not address.
- **Conditions:** DebugMCP 1.1.4 or earlier is installed and running. The victim uses a browser without Local Network Access protection (the demo used Firefox 150; Firefox 153 added it). Windows, for the UNC/SMB payload path. Outbound SMB must be allowed.
- **Mitigations:** Upgrade to 1.2.0 or later. Use the SDK's Host and Origin validation middleware. Require authentication and stateful sessions. Validate path inputs and reject UNC and remote schemes. Block outbound SMB. Audit loopback listeners. Govern which MCP servers may run.

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [Imperva Threat Research](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 4 · Novelty 40 · Relevance 80 · Credibility 75 · **Composite 48** _(each 0-100)_  
**Tags:** `mcp`, `dns-rebinding`, `localhost-exposure`, `drive-by-rce`, `unc-path`, `vscode-extension`, `silent-fix`, `developer-workstation`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: mysql-mcp-server SSE transport skipping the MCP SDK's Origin/Host checks (DNS rebinding, archive.json); Windows ML CLI wildcard CORS localhost RCE (archive.json); Imperva's earlier CVE-2025-53967 MCP RCE; MCP TypeScript SDK fix CVE-2025-66414. New here: stateless mode turning the attack into a single request, and the UNC-path-to-SMB execution trick. Verifier's closest: mysql-mcp-server SSE DNS-rebinding entry; CVE-2025-53967; CVE-2025-66414.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/)_  ·  [← back to index](../README.md)
