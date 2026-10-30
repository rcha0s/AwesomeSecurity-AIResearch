# Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws

**Published:** Oct 28, 2026

> **Takeaway:** Treating loopback as trusted makes any request-forgery bug a way past the perimeter, so patch rather than relying on path-based firewall rules.

## TL;DR

The PeopleSoft bug that ShinyHunters has exploited since May, patched as CVE-2026-35273 (CVSS 9.8), is really three flaws chained together. A server-side request forgery (the server can be made to send requests for the attacker) in the Integration Gateway reaches the internal Environment Management Hub. That hub trusts 127.0.0.1 by default, and from there an attacker can write a web shell or plant a malicious XML file, giving remote code execution with no login. Attackers got past web application firewall rules by URL-encoding one character of the blocked path.

## Lessons

- A default allowlist entry for the loopback address turns any server-side request forgery into full access to internal admin interfaces. - _"That file ships with the local loopback address, 127.0.0.1, already on the list."_
- Path-matching web application firewall rules can be bypassed by URL-encoding a single character, because the server decodes the path before serving it. - _"Many WAF rules match the path's plain text, while the PeopleSoft server decodes it and serves the page."_
- The XMLDecoder code-execution path leaves no web shell behind, so web-shell hunting alone can miss it. - _"The second path leaves less for standard detection to catch."_
- Patching does not remove an attacker who is already inside. Hunt for web shells and rotate credentials as well. - _"Patching closes the door; it does not by itself evict someone already inside."_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated attacker chains a server-side request forgery in PSIGW to the PSEMHUB admin interface, which trusts loopback, then gets code execution through a log-write web shell or an XMLDecoder payload. This leads to data theft and extortion.
- **Conditions:** PeopleSoft Enterprise PeopleTools 8.61 or 8.62 without Oracle's June 10 fix, with the PSIGW listening connector reachable and PSEMHUB deployed using the default allowedhosts.properties.
- **Mitigations:** Apply Oracle's CVE-2026-35273 fix, disable or remove PSEMHUB if you cannot patch, do not treat path-based WAF blocking as a fix, and on suspected hosts preserve evidence, hunt for web shells and rotate all reachable credentials.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [The Hacker News](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html)  ·  **Retrieved:** 2026-10-28  
**Scores:** Newness 19 · Novelty 50 · Relevance 75 · Credibility 51 · **Composite 50** _(each 0-100)_  
**Tags:** `oracle-peoplesoft`, `ssrf`, `loopback-trust`, `waf-bypass`, `shinyhunters`, `zero-day`, `rce`, `kev`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No PeopleSoft or ShinyHunters entries in the pools. Closest: the ai-security entry on loopback MCP servers needing Host/Origin checks, the same loopback-trust failure in a different product.

_Source: [https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html)_  ·  [← back to index](../README.md)
