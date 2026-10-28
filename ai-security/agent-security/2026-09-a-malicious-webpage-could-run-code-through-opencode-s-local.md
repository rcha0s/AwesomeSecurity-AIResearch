# A malicious webpage could run code through OpenCode's local upgrade endpoint

**Published:** Sep 24, 2026

> **Takeaway:** Any local HTTP server that a coding agent exposes is reachable from every webpage the developer visits, so it needs authentication, strict Content-Type checks, and allowlisted inputs before anything reaches a shell or package manager.

## TL;DR

OpenCode's local web server passed an unchecked upgrade target into `npm install -g opencode-ai@<target>`, and npm accepts a remote tarball URL there, so an attacker's package with a preinstall script runs on the developer's machine. The endpoint parsed any body as JSON without checking the Content-Type, so a cross-origin HTML form with enctype=text/plain, sent as a top-level navigation, reached 127.0.0.1:4096 without being stopped by CORS or Local Network Access prompts. Versions 1.14.30 through 1.18.21 installed via npm, pnpm or Bun are affected when `opencode serve` or `opencode web` runs without a password; 1.18.22 restricts the target to a semantic version and enforces the content type.

## Lessons

- npm install targets accept tarball URLs, not just versions, so passing user input into a package spec is code injection via lifecycle scripts. - _"accepts both semantic versions, such as 1.18.1, and remote tarballs as install targets."_
- A JSON endpoint that does not enforce Content-Type can be hit by a cross-origin text/plain form whose field name and value combine into valid JSON. - _"It therefore accepts a `text/plain` form submission if the body contains valid JSON."_
- Binding to loopback and relying on CORS or Local Network Access does not protect local agent servers from top-level navigation POSTs. - _"CORS and Local Network Access do not currently block top-level navigations, by design."_
- The fix was two-layered: validate the target as a semantic version and decode the body according to its declared content type. - _"it restricts the upgrade target to a semantic version and enforces the request's content type."_

## Threat · Conditions · Mitigations

- **Threat:** Drive-by webpage triggers npm install of an attacker tarball via the unauthenticated local OpenCode API, running a preinstall script as the developer.
- **Conditions:** OpenCode 1.14.30-1.18.21 installed via npm, pnpm or Bun; `opencode serve` or `opencode web` running without password authentication or with cached browser credentials; victim visits attacker page.
- **Mitigations:** Upgrade to 1.18.22+; set OPENCODE_SERVER_PASSWORD; stop the web server when not in use.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 4 · Novelty 50 · Relevance 80 · Credibility 75 · **Composite 51** _(each 0-100)_  
**Tags:** `coding-agent`, `opencode`, `localhost-server`, `csrf`, `content-type-confusion`, `npm`, `lifecycle-scripts`, `drive-by-rce`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Pillar Security opencode MCP OAuth RCE (same product, different bug); localhost service + wildcard CORS drive-by entry.

_Source: [https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/)_  ·  [← back to index](../README.md)
