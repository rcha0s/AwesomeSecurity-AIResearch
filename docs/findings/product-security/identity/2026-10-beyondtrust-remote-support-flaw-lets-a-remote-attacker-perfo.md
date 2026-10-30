# BeyondTrust Remote Support flaw lets a remote attacker perform file operations

**Published:** Oct 15, 2026

> **Takeaway:** Patch self-hosted Remote Support now and treat remote-support appliances as top-priority edge assets.

## TL;DR

BeyondTrust advisory BT26-05 (CVE-2026-102764, CWE-290) covers a critical flaw in an internal messaging component of Remote Support that did not validate message origin, allowing file operations on the appliance. SaaS customers were patched by October 9, 2026; self-hosted customers on versions 24.3.1 through 26.2.3 must apply the BT26-05-RS patch, and older versions must upgrade first. The advisory does not say whether the flaw is being exploited.

## Lessons

- Root cause: messages were accepted without origin validation. - _"The components did not adequately validate the origin of the messages it received."_
- SaaS is already fixed; self-hosted needs a manual patch. - _"As of Oct 9, 2026, a patch that remediates this vulnerability has been applied to all Remote Support SaaS customers."_
- Old versions must upgrade first. - _"Customers on a Remote Support version older than 24.3.1 will need to upgrade to a newer version to apply this patch."_

---

**Topic:** Product Security  ·  **Domain:** Identity & Access  
**Source:** [source](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 19 · Novelty 20 · Relevance 55 · Credibility 55 · **Composite 36** _(each 0-100)_  
**Tags:** `beyondtrust`, `remote-support`, `origin-validation`, `cwe-290`, `edge-appliance`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: BeyondTrust Remote Support has a recurring history of critical pre-auth bugs; this advisory adds nothing technique-wise. Verifier: BeyondTrust Remote Support CVE-2024-12356/12686 and CVE-2025-1094 advisories; generic remote-support appliance flaws (ScreenConnect, Ivanti)

_Source: [https://www.beyondtrust.com/trust-center/security-advisories/bt26-05](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05)_  ·  [← back to index](../README.md)
