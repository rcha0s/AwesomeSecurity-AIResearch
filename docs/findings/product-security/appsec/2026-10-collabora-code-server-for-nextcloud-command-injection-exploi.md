# Collabora CODE Server for Nextcloud command injection exploited in the wild (CVE-2026-110447)

**Published:** Oct 23, 2026

> **Takeaway:** Nextcloud instances using the built-in CODE server need richdocumentscode 26.4.303 or later now, plus a check for signs of compromise.

## TL;DR

The Built-in CODE Server app for Nextcloud (richdocumentscode) before 26.4.303 has an OS command injection in proxy.php that gives remote code execution. It triggers when the CODE server is not running, for example right after a restart. It was exploited in September and October 2026, and CISA added it to the Known Exploited Vulnerabilities (KEV) catalog with a three-day due date; standalone Collabora Online servers are not affected.

## Lessons

- The bug sits in the Nextcloud-bundled CODE server app, not in standalone Collabora Online. - _"The vulnerability is not present in standalone Collabora Online servers; only this deployment with CODE Server is affected."_
- The injectable path is reachable when the CODE server is not running, such as after a restart. - _"This is an OS command injection in proxy.php when the CODE server isn't running (e.g., the product was recently restarted)."_
- Exploitation is confirmed, and versions before 26.4.303 are affected. - _"allows remote code execution, as exploited in the wild in September and October 2026"_

## Threat · Conditions · Mitigations

- **Threat:** Unauthenticated-style remote code execution via OS command injection in richdocumentscode proxy.php on Nextcloud servers.
- **Conditions:** Nextcloud with the Collabora Built-in CODE Server app before 26.4.303, at a time when the CODE server is not running (e.g., after restart).
- **Mitigations:** Upgrade richdocumentscode to 26.4.303 or later; disable the app if patching is not possible; investigate for compromise per CISA forensic triage guidance.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [CISA Known Exploited Vulnerabilities](https://nvd.nist.gov/vuln/detail/CVE-2026-110447)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 20 · Novelty 30 · Relevance 65 · Credibility 70 · **Composite 44** _(each 0-100)_  
**Tags:** `cisa-kev`, `command-injection`, `nextcloud`, `collabora`, `rce`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Standard KEV-listed web-app command injection; the NVD record notes it is distinct from the earlier CVE-2025-66208, and no pool entry covers Collabora/Nextcloud. Verifier: Standard KEV-listed unauthenticated OS command injection in a self-hosted collaboration add-on; closest prior is the earlier richdocumentscode/Collabora CVE-2025-66208 that NVD explicitly distinguishes; no prior entry in the tracker data.

_Source: [https://nvd.nist.gov/vuln/detail/CVE-2026-110447](https://nvd.nist.gov/vuln/detail/CVE-2026-110447)_  ·  [← back to index](../README.md)
