# watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE

**Published:** Oct 9, 2026

> **Takeaway:** When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.

## TL;DR

PaperCut 26.0.3 was exploited in the wild through an auth bypass (CVE-2026-81578) chained with a post-auth RCE (CVE-2026-82078). The root cause is that PaperCut, built on Apache Tapestry 3, checks authorization only on the root page in the `service` parameter: `direct/1/<public page>/<private page>/<form>` reaches authenticated forms. PaperCut patched page by page, and watchTowr bypassed each fix. The final bypass (WT-2026-0143) reaches Setup Wizard forms through `Home`, resets the admin password in four POSTs, and is chained with a new Scan to Fax command-execution bug (CVE-2026-82077), fixed in 26.0.5.

## Lessons

- The core flaw: Tapestry lets one `service` parameter chain several pages, but PaperCut only authorized the first (root) page. - _"However, the code only checks authorization for the root page, so `LogonMessage` in our case, this page does not require authentication."_
- Fixing individual pages and forms instead of adding a global authorization check left other reachable forms, like the Setup Wizard, unprotected. - _"Still, without a global authorization check implemented for all pages, it is hard to keep track and manually verify every page in the codebase."_
- Routing setup forms through `Home` skips their own guard, so the 'setup already completed' flag never stops an attacker from re-running setup and resetting the admin password. - _"Setup pages `pageValidate` method will never be called (thanks to the bypass), so the `system.setup-completed` value is irrelevant for the attacker."_
- PaperCut assigned fewer CVEs than distinct bugs, folding patch bypasses into existing IDs, so CVE-based tracking undercounts the fix rounds needed. - _"due to PaperCut bundling vulnerabilities and then patch bypasses for those same vulnerabilities into singular CVE IDs"_

## Threat · Conditions · Mitigations

- **Threat:** Unauthenticated attacker resets the PaperCut admin password via re-run setup forms, then executes OS commands through admin functionality (Scan to Fax command path).
- **Conditions:** PaperCut NG/MF up to 26.0.4-PO build 76508 for the WT-2026-0143 plus CVE-2026-82077 chain; 26.0.3 for the in-the-wild chain; web interface reachable by the attacker.
- **Mitigations:** Upgrade to 26.0.5 or later; restrict the admin web interface to trusted networks; apply PaperCut's IOCs and hunt for multi-page `service` requests and unexpected admin credential changes.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [watchTowr Labs](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 19 · Novelty 65 · Relevance 80 · Credibility 74 · **Composite 59** _(each 0-100)_  
**Tags:** `papercut`, `patch-bypass`, `authentication-bypass`, `rce`, `apache-tapestry`, `exploited-in-the-wild`, `patch-diffing`, `watchtowr`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: watchTowr's SolarWinds Web Help Desk chain (WebObjects multi-step auth bypasses) and the earlier PaperCut KEV bugs CVE-2023-27350/27351. This adds a concrete legacy-framework pattern (Tapestry 3 multi-page `service` routing skipping per-page auth) plus a documented series of per-page patches failing in sequence.

_Source: [https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)_  ·  [← back to index](../README.md)
