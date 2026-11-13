# Datadog reproduces pre-auth MongoDB crash planted with two ping requests

**Published:** Nov 11, 2026

> **Takeaway:** Patch every MongoDB replica set member now; auth does not block the pre-login setup, and network restriction only narrows who can plant it.

## TL;DR

CVE-2026-118383 (CVSS v4.0 score 9.5) is a use-after-free bug in MongoDB Server's replica set primary catch-up: two unauthenticated `ping` requests with `readConcern.afterOpTime` plant stale waiters, and the member crashes when it later wins an election while lagging. Datadog reproduced the crash on 8.0.34 but did not achieve the code execution the vendor lists as possible. Standalone `mongod` is unaffected, enabling authentication does not prevent the setup, and fixed releases include 9.0.7, 8.0.37, 7.0.48 and 6.0.30. Depending on logging settings, the planted requests can appear in slow-query logs that may predate the crash.

## Lessons

- Commands accepted before login (here `ping`) are pre-auth attack surface, so turning on authentication is not a mitigation for this bug. - _"An unauthenticated client can set up the crash with two `ping` requests, because vulnerable servers accept `ping` before login. Turning on authentication does not prevent this."_
- The attacker plants the trigger in advance and must wait for a natural lagging-member election, so exploitation is opportunistic rather than on-demand. - _"Remote unauthenticated exploitation is possible, but only during a specific window that the attacker does not have visibility into."_
- Detection must look back before the crash: hunt for unauthenticated ping commands with afterOpTime and expired waits in older logs of the same member. - _"The requests may arrive before the failover. Review earlier logs from the same member, not just events around the crash."_
- The demonstrated impact is denial of service; code execution remains a vendor-stated possibility, not a reproduced result. - _"The vendor also identifies arbitrary code execution as a possible impact under certain conditions; our tests did not demonstrate it."_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated network client can plant two waiters on a reachable replica set member that crash it when it next completes primary catch-up, potentially leaving the cluster without a primary.
- **Conditions:** Vulnerable MongoDB replica set member reachable on the network; the member must later win an election while behind another member, which the attacker cannot cause.
- **Mitigations:** Upgrade to 9.0.7, 8.3.16, 8.0.37, 7.0.48, 6.0.30, 5.0.35 or 4.4.32 or later, verify versions on all members including containers and offline members, restrict network access to MongoDB, and retain command objects in logs to detect afterOpTime ping requests.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/cve-2026-118383-mongodb-server-use-after-free/)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 49 · Novelty 45 · Relevance 70 · Credibility 74 · **Composite 58** _(each 0-100)_  
**Tags:** `mongodb`, `use-after-free`, `pre-auth`, `denial-of-service`, `database`, `detection`  
**Also reported by:** [The Hacker News](https://thehackernews.com/2026/11/critical-pre-auth-mongodb-flaw-cve-2026.html) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No prior MongoDB server entry in the tracker; general pattern of critical pre-auth memory-safety bugs in network daemons (e.g. CVE-2025-14847-style MongoDB pre-auth issues, OpenSSH regreSSHion). The plant-then-wait election trigger and the log-level detection guidance are the specific new content. Verifier's closest: no MongoDB entries in the tracker; generic pre-auth memory-safety bugs in network daemons.

_Source: [https://securitylabs.datadoghq.com/articles/cve-2026-118383-mongodb-server-use-after-free/](https://securitylabs.datadoghq.com/articles/cve-2026-118383-mongodb-server-use-after-free/)_  ·  [← back to index](../README.md)
