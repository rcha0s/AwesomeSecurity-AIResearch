# OpenSSH ships an emergency workaround for a critical musl-specific vulnerability

**Published:** Nov 5, 2026

> **Takeaway:** Find every musl-based SSH host, especially Alpine containers and appliances, and turn off password authentication now, because maintainers no longer wait out long embargoes.

## TL;DR

OpenSSH 10.6p2 adds a workaround for a critical vulnerability. It affects Linux systems that use the musl C library and do not use PAM (Pluggable Authentication Modules) for password authentication. Alpine Linux is one example. Damien Miller, an OpenSSH developer, says the root cause is outside OpenSSH and withheld details. He says the project released the fix the day after it learned of the bug because AI agents have been rediscovering bugs within hours, which makes long embargoes dangerous.

## Lessons

- If you cannot upgrade right away on musl systems without PAM, turn off SSH password authentication or SSH itself. - _"If you operate a Linux system that uses musl libc without PAM (Alpine Linux is one example) then stop reading and set PasswordAuthentication=no or disable SSH for these systems IMMEDIATELY."_
- The exposure is narrow. glibc systems, non-Linux systems and systems that use PAM for password authentication are not affected. - _"This vulnerability does not exist on non-Linux systems, Linux/glibc systems and Linux systems that use PAM for password authentication."_
- A maintainer of core infrastructure has cut embargo time because AI agents rediscover bugs quickly. Defenders should expect less warning before disclosure. - _"we have recently observed multiple cases of rapid bug rediscovery by AI agents, sometimes within hours"_

## Threat · Conditions · Mitigations

- **Threat:** A critical, undisclosed vulnerability reachable through SSH password authentication on Linux systems that use musl libc without PAM.
- **Conditions:** Linux with musl libc (for example Alpine Linux), OpenSSH password authentication enabled, and PAM not used for password authentication.
- **Mitigations:** Upgrade to OpenSSH 10.6p2 or the patched distribution package, set PasswordAuthentication=no, or disable SSH on affected systems.

---

**Topic:** Product Security  ·  **Domain:** Identity & Access  
**Source:** [@Animux via Hacker News](https://hachyderm.io/@damienmiller/117563026759098135)  ·  **Author:** Animux  ·  **Retrieved:** 2026-11-05  
**Scores:** Newness 65 · Novelty 52 · Relevance 75 · Credibility 55 · **Composite 63** _(each 0-100)_  
**Tags:** `openssh`, `musl`, `alpine-linux`, `password-authentication`, `embargo`, `ai-bug-rediscovery`, `emergency-patch`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Product-security pool entry 'PHP says Chainguard broke the PHP2Shell embargo with patched images', which covers AI rediscovery shortening embargoes, and an earlier OpenSSH 10.6 hardening entry. No prior entry covers this musl/no-PAM bug.

_Source: [https://hachyderm.io/@damienmiller/117563026759098135](https://hachyderm.io/@damienmiller/117563026759098135)_  ·  [← back to index](../README.md)
