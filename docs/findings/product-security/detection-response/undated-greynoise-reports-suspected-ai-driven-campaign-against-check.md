# GreyNoise reports suspected AI-driven campaign against Check Point management servers

**Published:** Nov 25, 2026

> **Takeaway:** Treat firewall management servers as crown-jewel assets: patch them, restrict who can reach them, and watch for policy unloads.

## TL;DR

GreyNoise tracks an unattributed campaign, GT13, that hit Check Point Security Management servers at 22 organizations between October 17 and November 2, 2026. The attackers used a script for a patched Check Point flaw (CVE-2026-16232) to steal firewall databases and certificate authority files and to unload security policies. GreyNoise suspects AI-driven tooling, but that is an assessment, and Check Point says this is not a new vulnerability.

## Lessons

- GreyNoise suspects, but did not prove, that the attackers ran agentic tooling for scanning, exploitation and interaction with compromised hosts. - _"the attackers are relying on agentic harnesses and systems for vulnerability scanning, exploitation"_
- With management-server access, the attackers ran over 100 management tasks, stealing firewall databases and certificate authority files and unloading security policies, which disables firewall protection. - _"Unload security policies, effectively disabling firewall protections"_
- The attackers already had access to the Check Point servers before the later steps, and GreyNoise could not tell when or how they got in. - _"We could not determine when or how the attacker gained access to those Check Point assets."_
- Check Point says the activity uses a previously disclosed, already patched flaw and is not a new vulnerability or technique. - _"does not represent a new vulnerability or exploitation technique"_

## Threat · Conditions · Mitigations

- **Threat:** Attackers with management-server access can steal certificate authority material, mint certificates and unload firewall policies.
- **Conditions:** Check Point Security Management servers exposed to the attackers and not patched for CVE-2026-16232; initial access method unknown.
- **Mitigations:** Apply Check Point updates, restrict management access per its hardening guidance, and hunt for suspicious management tasks and unexpected policy unloads.

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [The Hacker News](https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html)  ·  **Retrieved:** 2026-11-25  
**Scores:** Newness 0 · Novelty 35 · Relevance 70 · Credibility 45 · **Composite 38** _(each 0-100)_  
**Tags:** `check-point`, `firewall`, `agentic-attacks`, `greynoise`, `campaign`, `management-plane`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Pool has "Check Point ships hotfixes for a zero-day exploited for root access" and "Check Point found ARTEX operators letting AI agents run cybercrime campaigns unattended"; this adds a GreyNoise-tracked campaign on the same product with suspected, unproven AI tooling.

_Source: [https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html](https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html)_  ·  [← back to index](../README.md)
