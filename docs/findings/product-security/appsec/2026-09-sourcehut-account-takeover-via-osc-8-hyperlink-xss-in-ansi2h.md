# SourceHut account takeover via OSC 8 hyperlink XSS in ansi2html-rendered build logs (CVE-2026-92973; ansi2html >=1.7.0,<1.9.4, builds.sr.ht >=0.40.0,<0.105.1)

**Published:** Sep 24, 2026

> **Takeaway:** Treat CI log output as untrusted HTML input: sanitize the output of any ANSI-to-HTML converter and back it with a strict Content-Security-Policy, because one injected escape sequence can become wormable account takeover.

## TL;DR

The ansi2html Python library turned terminal OSC 8 hyperlink escape sequences into HTML links without proper escaping. A crafted sequence could break out of the href attribute or use a javascript: URL. builds.sr.ht rendered CI logs with it. So anyone who could get bytes into a build log, even by mailing a patch to a public list with CI enabled, got script execution in every viewer's browser. The page already held the CSRF token, so the script could resubmit builds as the viewer, including admins with access to deploy keys.

## Lessons

- Terminal escape sequences in CI logs are attacker input; converting them to HTML without sanitization yields stored XSS. - _"executes your payload in every browser that views it"_
- Attackers did not need an account: CI triggered by patches sent to a public mailing list, or any remote resource printed to the log, was enough to inject. - _"by sending a patch to a public mailing list with continuous integration turned on"_
- XSS on a page that embeds a CSRF token defeats CSRF protection and lets the attacker act as the viewer. - _"The build log page already contains the CSRF token."_
- A one-time dependency audit is not enough; the bug was introduced upstream after adoption and stayed exploitable for years. - _"Note how even carefully auditing ansi2html would not save SourceHut, unless redone on every bump."_

## Threat · Conditions · Mitigations

- **Threat:** Stored XSS in CI build logs via crafted OSC 8 hyperlink escapes, leading to CSRF-token theft and actions (build resubmission with deploy keys, admin changes) as the viewing user.
- **Conditions:** Log viewer renders output with ansi2html >=1.7.0,<1.9.4 without extra sanitization; attacker can get bytes into a build log; victim views it with JavaScript enabled.
- **Mitigations:** Upgrade ansi2html to 1.9.4 and builds.sr.ht to 0.105.1; sanitize converter output; tighten Content-Security-Policy.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [@arusekk via Hacker News](https://blog.arusekk.pl/posts/srht-account-takeover/)  ·  **Author:** arusekk  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 5 · Novelty 60 · Relevance 65 · Credibility 55 · **Composite 47** _(each 0-100)_  
**Tags:** `xss`, `ci-logs`, `ansi-escape-injection`, `osc-8`, `csrf-token-theft`, `dependency-risk`, `python`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: ANSI escape injection in MCP servers and terminals; no prior OSC 8-to-HTML log XSS.

_Source: [https://blog.arusekk.pl/posts/srht-account-takeover/](https://blog.arusekk.pl/posts/srht-account-takeover/)_  ·  [← back to index](../README.md)
