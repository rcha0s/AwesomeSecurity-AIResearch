# Roo Code's command auto-approval can be bypassed in seven ways

**Published:** Oct 13, 2026

> **Takeaway:** Allowlist-by-prefix approval for agent shell commands breaks whenever the checker and the shell parse differently; do not enable auto-approve on untrusted content.

## TL;DR

VulnCheck published seven CVEs for Roo Code through 3.54.0 (checked at NVD): CVE-2026-82536 and CVE-2026-82537 on 2026-09-08, and CVE-2026-110202 to CVE-2026-110206 on 2026-10-13. Each lets indirect prompt injection run a denied shell command in an auto-approve setup by exploiting a gap between Roo's regex parser and bash: quote masking, glob tokens, redirects, ${ cmd; } substitutions, pipes, comments, or a substitution in command position. The advisories name no fixed version.

## Lessons

- An allowlisted prefix like echo hides a command separator when the approval regex and the shell disagree about quotes. - _"Attackers can use indirect prompt injection with escaped or single-quoted double quotes to hide command separators behind allowlisted prefixes like echo, executing commands without user approval."_

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [vulncheck.com](https://www.vulncheck.com/advisories/roo-code-through-3.54.0-auto-approve-bypass-via-quote-masking-desynchronization)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 0 · Novelty 60 · Relevance 85 · Credibility 55 · **Composite 52** _(each 0-100)_  
**Tags:** `roo-code`, `coding-agents`, `auto-approve`, `command-allowlist`, `prompt-injection`, `cve`  
**Also reported by:** [NVD CVE-2026-110203](https://nvd.nist.gov/vuln/detail/CVE-2026-110203) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: CVE-2026-30307 (March 2026, MITRE) reported Roo Code's regex whitelist as ineffective in general; these seven are distinct parser differentials (quote masking, glob tokens, redirects, funsub, pipes, comments, command position), each with its own CVE.

_Source: [https://www.vulncheck.com/advisories/roo-code-through-3.54.0-auto-approve-bypass-via-quote-masking-desynchronization](https://www.vulncheck.com/advisories/roo-code-through-3.54.0-auto-approve-bypass-via-quote-masking-desynchronization)_  ·  [← back to index](../README.md)
