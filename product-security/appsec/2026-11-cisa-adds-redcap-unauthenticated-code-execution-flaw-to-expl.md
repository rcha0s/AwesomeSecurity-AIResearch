# CISA adds REDCap unauthenticated code execution flaw to exploited vulnerabilities list

**Published:** Nov 18, 2026

> **Takeaway:** If you run REDCap 13.3.0 or later, upgrade to a fixed build now and review who can reach your public survey links.

## TL;DR

CISA added REDCap (Research Electronic Data Capture) CVE-2026-90817 to its Known Exploited Vulnerabilities catalog on November 18, 2026. An unauthenticated attacker can run code on the server by sending crafted requests to an unintended controller route from a public survey, then supplying a crafted file path during data import. The attacker must know a valid public survey hash; REDCap 13.3.0 and higher is affected and fixed builds are 16.0.49, 17.3.10 and 17.4.4.

## Lessons

- The flaw sits in survey passthrough routing and data import handling and needs no login, so any public survey link is an entry point. - _"An unauthenticated Remote Code Execution vulnerability was found in the survey passthrough routing and Data Import processing logic"_
- Exploitation needs a valid public survey hash, which limits blind scanning but not anyone who has a survey link. - _"exploitation requires knowledge of a valid public survey hash"_
- Fixed builds exist on three release lines, and the affected range starts at 13.3.0. - _"Affected 13.3.0 Unaffected 16.0.49 Unaffected 17.3.10 Unaffected 17.4.4"_
- CISA gave federal agencies three days, until November 21, 2026, to apply mitigations. - _"Vanderbilt University Research Electronic Data Capture (REDCap) Code Injection Vulnerability | November 18, 2026 | November 21, 2026"_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated attacker reaches an unintended controller route from a public survey context and abuses import file-path handling to run code on the REDCap server.
- **Conditions:** REDCap 13.3.0 or higher without the fixed build, and the attacker knows a valid public survey hash.
- **Mitigations:** Upgrade to 16.0.49, 17.3.10 or 17.4.4, and follow CISA's required action and forensics triage requirements for exposed servers.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [CISA Known Exploited Vulnerabilities](https://nvd.nist.gov/vuln/detail/CVE-2026-90817)  ·  **Retrieved:** 2026-11-19  
**Scores:** Newness 31 · Novelty 20 · Relevance 40 · Credibility 69 · **Composite 36** _(each 0-100)_  
**Tags:** `cisa-kev`, `redcap`, `remote-code-execution`, `code-injection`, `exploited-in-the-wild`  
**Also reported by:** [The Hacker News](https://thehackernews.com/2026/11/cisa-warns-of-4-exploited-flaws-linked.html) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No REDCap entry exists in the pools. Closest are this week's other unauthenticated code execution advisories (Apache Roller, Apache Axis); none cover survey routing.

_Source: [https://nvd.nist.gov/vuln/detail/CVE-2026-90817](https://nvd.nist.gov/vuln/detail/CVE-2026-90817)_  ·  [← back to index](../README.md)
