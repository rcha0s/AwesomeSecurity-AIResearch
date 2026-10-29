# Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI

**Published:** Oct 21, 2026

> **Takeaway:** Patch PHP now: the flaws are in the engine, not your app, and AI has cut the cost of turning old memory bugs into working exploits.

## TL;DR

Wiz Research reported memory-safety bugs in the PHP engine itself (CVE-2026-109618 and CVE-2026-109619, up to CVSS 9.2), so every PHP version back to 5.4 is hit by at least one of them. The bugs sit in how PHP handles fatal errors such as out-of-memory, so a hello-world app is exposed. The bugs had existed for years; frontier models made the multi-step exploit chain practical to build and adapt per target in hours. PHP shipped the patch on October 21, 2026.

## Lessons

- The bugs are in core PHP, so every app on an affected version is exposed, including a plain Hello World app. - _"Every PHP version released in the last decade is affected by at least one of these vulnerabilities, going back to version 5.4."_
- The root cause is stale internal state left behind after fatal errors such as out-of-memory, which a later request or worker reuses. - _"All of the disclosed vulnerabilities are memory-safety issues that stem from bugs in how PHP handles fatal errors while processing requests, particularly out-of-memory errors."_
- Frontier models made the exploit chain practical: they adapted exploits to different targets in hours. - _"Frontier models were critical to making this process practical, enabling us to develop and adapt working exploits across multiple applications in hours."_
- Exploit complexity may no longer be a reliable barrier, so old memory bugs deserve faster patching. - _"As the time and expertise required for this work decrease, complexity may no longer provide a meaningful barrier, changing how we define what is vulnerable in practice."_

---

**Topic:** Product Security  ·  **Domain:** Vulnerability Research & Red Teaming  
**Source:** [source](https://www.wiz.io/blog/php2shell-php-rce)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 21 · Novelty 58 · Relevance 80 · Credibility 70 · **Composite 57** _(each 0-100)_  
**Tags:** `php`, `rce`, `memory-safety`, `ai-assisted-exploitation`, `wordpress`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Core-language RCE disclosures exist (for example PHP-CGI), but a core PHP memory-corruption chain exploited pre-auth across three CMSs with frontier-model-built exploits has no equal in the pools. Verifier: Google Big Sleep / Project Zero AI-found bugs, DARPA AIxCC, XBOW; earlier frontier-model exploit-development reports. Delta is AI-built multi-bug chain on core 

_Source: [https://www.wiz.io/blog/php2shell-php-rce](https://www.wiz.io/blog/php2shell-php-rce)_  ·  [← back to index](../README.md)
