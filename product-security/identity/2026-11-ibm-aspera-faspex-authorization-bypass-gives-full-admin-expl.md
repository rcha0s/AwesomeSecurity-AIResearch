# IBM Aspera Faspex authorization bypass gives full admin, exploited in the wild

**Published:** Nov 9, 2026

> **Takeaway:** Patch internet-facing Aspera Faspex 5.0.0 through 5.0.19 per IBM's advisory now and review admin accounts for unexpected changes.

## TL;DR

The Cybersecurity and Infrastructure Security Agency (CISA) added CVE-2026-123218, an incorrect-authorization flaw (CWE-863, from the Common Weakness Enumeration) in IBM Aspera Faspex 5.0.0 through 5.0.19, to its Known Exploited Vulnerabilities (KEV) catalog on November 9, 2026. A user can craft a specific message to bypass authorization and gain full administrative privileges; IBM's CVE Numbering Authority (CNA) vector rates it network-reachable with no privileges required. CISA set a due date of November 12, 2026, only three days after listing.

## Lessons

- A crafted message lets a user skip authorization checks and become a full Faspex administrator, so a single foothold account (or less) becomes control of the file-transfer server. - _"IBM Aspera Faspex 5.0.0 through 5.0.19 could allow an authorized user to craft a specific message to bypass user authorization and gain full administrative privileges."_
- IBM's own Common Vulnerability Scoring System (CVSS) vector says no privileges are required (PR:N), which conflicts with the description's 'authorized user'; treat it as potentially reachable without an account until the vendor clarifies. - _"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"_
- The Cybersecurity and Infrastructure Security Agency (CISA) set a remediation due date only three days after listing the flaw. - _"IBM Aspera Faspex Incorrect Authorization Vulnerability | November 09, 2026 | November 12, 2026"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker with a Faspex account (possibly none, per the CNA vector) sends a crafted message to gain full administrative privileges on the file-transfer server.
- **Conditions:** IBM Aspera Faspex versions 5.0.0 through 5.0.19 reachable by the attacker.
- **Mitigations:** Apply IBM's fix per its vendor advisory, limit internet exposure of Faspex, and audit admin accounts and transfer logs for abuse.

---

**Topic:** Product Security  ·  **Domain:** Identity & Access  
**Source:** [CISA Known Exploited Vulnerabilities](https://nvd.nist.gov/vuln/detail/CVE-2026-123218)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 52 · Novelty 25 · Relevance 60 · Credibility 69 · **Composite 49** _(each 0-100)_  
**Tags:** `kev`, `exploited-in-the-wild`, `authorization-bypass`, `privilege-escalation`, `file-transfer`, `ibm`  
**Also reported by:** [The Hacker News](https://thehackernews.com/2026/11/cisa-warns-of-active-exploitation-of.html) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Routine CISA KEV listings already tracked (e.g. Plex Media Server, Fortinet, GitLab KEV entries in product-security.json); file-transfer appliance exploitation is a well-known pattern. No prior Aspera Faspex entry.

_Source: [https://nvd.nist.gov/vuln/detail/CVE-2026-123218](https://nvd.nist.gov/vuln/detail/CVE-2026-123218)_  ·  [← back to index](../README.md)
