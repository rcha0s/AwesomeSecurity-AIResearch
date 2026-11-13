# Google Project Zero shortens its disclosure deadline to 30 days by 2028

**Published:** Nov 13, 2026

> **Takeaway:** A major research team now treats AI-accelerated exploitation as the default, so vendors need to fix every reported bug within 30 to 60 days and close the patch gap, whatever the bug's severity.

## TL;DR

Project Zero is replacing its '90 + 30' policy with 'Full X': details are disclosed X days after the bug is reported to the vendor, and whether it is fixed is no longer a decision point. X is 90 days now, 60 days from February 2, 2027 and 30 days from January 3, 2028. The team says LLMs speed up both bug discovery and exploit-from-patch, so patch soak time no longer protects users; it drops most special cases, including the grace period and variant rules, and stops using severity to decide disclosure.

## Lessons

- Project Zero now assumes attackers can build an exploit from a patch almost immediately, so the window after a patch ships gives no secrecy. Defenders should work to close the patch gap (the time between a fix shipping and users installing it) instead of counting on soak time. - _"zero patch-to-exploitation time is a reasonable, though imperfect, model of attacker behavior"_
- With LLM help, Project Zero's own bug-finding rate has jumped by orders of magnitude. Per-bug negotiation with vendors no longer scales, so the policy is built to be automated. - _"We are finding several vulnerabilities a week in targets where we once found a few vulnerabilities a year."_
- Severity no longer changes the deadline, because a low-severity bug is just as likely to be found by attackers. Vendors that triage only by severity will see low-severity bugs disclosed on the same schedule. - _"does not affect the likelihood that it will be discovered by attackers, only its impact on users."_
- Whether a bug is fixed no longer affects when it is disclosed. Disclosure happens at day X regardless, and fix status is only reported alongside. - _"We still plan to track whether bugs are fixed and communicate if they are not, however, this will not be a decision point in our policy."_

## Threat · Conditions · Mitigations

- **Threat:** LLMs let attackers find the same bugs independently and turn patches into exploits almost at once, so an embargo or soak period protects users less and less.
- **Conditions:** This applies to vendors receiving Project Zero reports, and more broadly to any software whose patches attackers can diff.
- **Mitigations:** Shorten remediation timelines for all severities, cut patch rollout time and the patch gap, prepare non-patch mitigations such as temporarily disabling code paths, and automate tracking of disclosure deadlines.

---

**Topic:** Product Security  ·  **Domain:** Vulnerability Research & Red Teaming  
**Source:** [Google Project Zero](https://projectzero.google/2026/11/disclosure-policy.html)  ·  **Retrieved:** 2026-11-13  
**Scores:** Newness 49 · Novelty 70 · Relevance 85 · Credibility 75 · **Composite 70** _(each 0-100)_  
**Tags:** `vulnerability-disclosure`, `patch-gap`, `ai-assisted-vuln-discovery`, `project-zero`, `remediation-sla`, `n-day`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Project Zero's own 90+30 policy (2021); OpenAI's coordinated-disclosure framework for AI-found bugs (keeps vendor-negotiated timelines). No existing entry records a major disclosure-policy change driven by LLMs.

_Source: [https://projectzero.google/2026/11/disclosure-policy.html](https://projectzero.google/2026/11/disclosure-policy.html)_  ·  [← back to index](../README.md)
