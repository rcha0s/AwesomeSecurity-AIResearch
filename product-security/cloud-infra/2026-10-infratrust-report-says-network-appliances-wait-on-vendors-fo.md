# InfraTrust report says network appliances wait on vendors for PHP2Shell fixes

**Published:** Oct 28, 2026

> **Takeaway:** On appliances, patch speed depends on the vendor's firmware schedule, so limit exposure of management interfaces now instead of waiting.

## TL;DR

Eclypsium's October InfraTrust Pulse tracked 133 advisories from 18 vendors covering 2,813 vulnerabilities. Sixteen of those advisories include flaws already being exploited, and the report highlights exploited flaws in Citrix NetScaler, Ivanti Connect Secure, FortiMail and PAN-OS. Many firewalls, VPNs and storage appliances build PHP into their management interfaces. Customers cannot apply the PHP2Shell fixes (CVE-2026-109618/109619) themselves and must wait for vendor firmware.

## Lessons

- PHP compiled into appliance firmware means the fix depends on each vendor, not the customer. - _"Because vendors compile PHP into appliance firmware, customers commonly cannot install the recent PHP security updates themselves and must instead wait for each vendor to release updated firmware."_
- Until firmware arrives, take PHP-backed management interfaces off the internet. - _"InfraTrust therefore recommends that administrators make sure PHP-backed management interfaces are not exposed to the Internet while waiting for PHP2Shell patches."_
- Bundled components keep spreading flaws across vendors. The Copy Fail Linux kernel bug keeps showing up in more advisories. - _"has now appeared in 29 advisories across eight vendors, up from 19 advisories from six vendors last month."_

## Threat · Conditions · Mitigations

- **Threat:** Attackers exploit edge and management appliances, including through PHP2Shell unauthenticated RCE in PHP-based management interfaces, to get initial access to corporate networks.
- **Conditions:** Appliances with PHP built into their firmware management interface that are reachable from the internet, or unpatched NetScaler, Ivanti, Check Point, Cisco, Arista, FortiMail, F5 or PAN-OS products listed in the report.
- **Mitigations:** Do not expose PHP-backed management interfaces to the internet until vendor firmware arrives, and prioritize the NetScaler and Ivanti Connect Secure patches, then Fortinet's October 22 updates.

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/)  ·  **Retrieved:** 2026-10-28  
**Scores:** Newness 19 · Novelty 35 · Relevance 70 · Credibility 50 · **Composite 44** _(each 0-100)_  
**Tags:** `php2shell`, `network-appliances`, `edge-devices`, `firmware`, `kev`, `bundled-components`, `vpn`, `firewall`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Many PHP2Shell entries in product-security.json ('PHP2Shell hits every PHP since 5.4', 'Patch PHP and inventory PHP runtimes', AWS-logged exploitation). New: appliances with PHP built into firmware depend on vendor rebuilds.

_Source: [https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/)_  ·  [← back to index](../README.md)
