# Azure API Management flaw exposed secrets, tied to Norwegian energy firm incidents

**Published:** Nov 23, 2026

> **Takeaway:** If you run Azure API Management Classic, rotate every secret and named value stored in it and check access logs.

## TL;DR

Microsoft says a flaw in Azure API Management Classic let an unauthorized party reach secrets stored in some instances, and it appears to explain incidents at Equinor and Skagerak Energi. Microsoft found it on November 18 and closed the path the next day. Norway's NSM tells users to treat APIM secrets and named values as compromised and replace them.

## Lessons

- Microsoft told customers that an outsider could have reached secrets in Azure API Management Classic instances before the fix. - _"Our investigation found that customers were exposed and an unauthorized party could have used the issue to access secrets stored in Azure API Management Classic instances before Microsoft identified the security issue"_
- Norway's security authority advises rotating all APIM secrets and named values. - _"APIM users have been advised by NSM to treat their secrets and named values as compromised and replace them."_
- Equinor reported its attack a day before Microsoft identified the flaw, which is why the link between them is described as probable rather than proven. - _"Equinor reported the attack on November 17, one day before Microsoft identified the APIM flaw."_

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [SecurityWeek](https://www.securityweek.com/azure-flaw-exploited-to-target-secrets-at-norwegian-energy-firms/)  ·  **Retrieved:** 2026-11-24  
**Scores:** Newness 26 · Novelty 55 · Relevance 70 · Credibility 50 · **Composite 52** _(each 0-100)_  
**Tags:** `azure`, `apim`, `secrets`, `energy-sector`, `cloud`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier Azure credential-theft flaws (an August 2026 API credential bug); this adds a named vendor flaw tied to energy-sector incidents, with the link still unconfirmed.

_Source: [https://www.securityweek.com/azure-flaw-exploited-to-target-secrets-at-norwegian-energy-firms/](https://www.securityweek.com/azure-flaw-exploited-to-target-secrets-at-norwegian-energy-firms/)_  ·  [← back to index](../README.md)
