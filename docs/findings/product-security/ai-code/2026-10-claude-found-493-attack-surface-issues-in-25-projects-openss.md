# Claude found 493 attack-surface issues in 25 projects; OpenSSH made ML-DSA parsing unreachable before auth

**Published:** Oct 20, 2026

> **Takeaway:** Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.

## TL;DR

Anthropic ran Claude over 25 open-source projects (over five million lines) to find code reachable without need, rather than individual bugs. It found 493 issues, including 94 configuration combinations that silently turned off a security control, and a pattern in four projects where hostname-based deny rules fail open when reverse DNS lookups are off. In OpenSSH, about 4,500 lines of ML-DSA-44 post-quantum code were reachable before authentication even when the algorithm was disabled; after several rounds of fixes, OpenSSH 10.6 checks the allow lists before parsing.

## Lessons

- Option combinations are a large blind spot: many were accepted silently and undocumented. - _"Claude found 162 security sensitive configuration combinations that were accepted both without an error or warning and without any documentation of the expected behavior of their interaction."_
- sshd parsed attacker-chosen key types before checking whether they were allowed. - _"The daemon parsed whichever key type the client sent, (and, for certificates, it also verified the embedded CA signature). Only then did it check whether that key type was allowed."_
- Hostname deny rules compared against a bare IP never match, so the list fails open. - _"This means that a deny rule would never fire, and the list would fail open."_
- For the default-configuration pass, a gate is accepted only when the project's own tests give identical results. - _"it requires modified builds to have identical results."_

## Threat · Conditions · Mitigations

- **Threat:** Complex, memory-unsafe or security-sensitive code reachable by unauthenticated clients, and configuration combinations that silently disable controls administrators believe are on.
- **Conditions:** Default configurations exposing unused features, checks that run after parsing, and option pairs accepted without warnings, such as hostname deny rules with reverse DNS off or certificate requirements dropped by a conflicting option.
- **Mitigations:** Upgrade OpenSSH to 10.6; check allow lists before deserialization; reject conflicting security options at config load; use IP-based access rules or enable DNS lookups when using hostname rules.

---

**Topic:** Product Security  ·  **Domain:** AI in the SDLC  
**Source:** [Anthropic Research](https://www.anthropic.com/research/attack-surface-reduction)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 24 · Novelty 72 · Relevance 85 · Credibility 71 · **Composite 64** _(each 0-100)_  
**Tags:** `attack-surface-reduction`, `openssh`, `configuration-security`, `ai-assisted-review`, `pre-auth`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Pool entries on frontier-model vulnerability discovery (Mythos-era bug finding, AI-built PHP pre-auth chains) and classic attack-surface reduction guidance; this shifts from finding individual bugs to systematic reachability and config-interaction reduction with measured results and an upstream OpenSSH fix. Verifier: Attack-surface reduction (Howard/Manadhata attack-surface metrics, OpenSSH privsep and pre-auth minimization) is classic, and Anthropic's prior LLM vuln-finding posts (Firefox, OSS-Scanner) cover LLM bug finding. What is new is LLM-driven reachability and config-interaction auditing at scale, with the concrete OpenSSH 10.6 pre-auth fix.

_Source: [https://www.anthropic.com/research/attack-surface-reduction](https://www.anthropic.com/research/attack-surface-reduction)_  ·  [← back to index](../README.md)
