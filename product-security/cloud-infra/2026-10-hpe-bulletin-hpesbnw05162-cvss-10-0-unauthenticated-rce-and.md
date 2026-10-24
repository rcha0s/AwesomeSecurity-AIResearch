# HPE bulletin HPESBNW05162: CVSS 10.0 unauthenticated RCE and auth bypass flaws across ArubaOS AOS-10 and AOS-8

**Published:** Oct 23, 2026

> **Takeaway:** Patch ArubaOS and isolate management interfaces on a dedicated VLAN.

## TL;DR

HPE Networking bulletin HPESBNW05162 lists multiple critical flaws in AOS-10 and AOS-8, each scored CVSS 10.0. They include authentication bypass leading to remote code execution, bypass of PAPI protocol controls, unauthenticated command injection and an unauthenticated buffer overflow. HPE says the bugs were generally found by internal research and it knows of no public exploit code, and tells customers to patch quickly and to restrict management interfaces.

## Lessons

- The flaws were found internally and no exploit was known at release. - _"HPE Networking is not aware of any public discussion or exploit code that targets the listed vulnerabilities as of the release date of this advisory."_
- Workaround: put management on a dedicated segment with firewall controls. - _"HPE Networking recommends that the CLI and web-based management interfaces be restricted to a dedicated layer 2 segment/VLAN"_
- Unauthenticated memory corruption reaches RCE in AOS-10. - _"Unauthenticated Buffer Overflow Vulnerabilities leads to Remote Code Execution in AOS-10 (CVE-2026-79847)"_
- Discovery was in-house. - _"These vulnerabilities were generally discovered by internal security research at HPE Networking."_

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [source](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 27 · Novelty 20 · Relevance 60 · Credibility 50 · **Composite 38** _(each 0-100)_  
**Tags:** `arubaos`, `hpe`, `network-devices`, `unauthenticated-rce`, `command-injection`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Large vendor advisory batches are routine; no novel technique reported. Verifier: Routine Aruba/HPE multi-CVE bulletins (e.g., ArubaOS PAPI buffer overflow advisories 2022-2025); only the all-10.0 scoring is notable  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US)_  ·  [← back to index](../README.md)
