# Skimmers hijacked Convertr's self-hosted analytics script to steal checkout card data

**Published:** Oct 27, 2026

> **Takeaway:** Any script loaded on checkout pages, even self-hosted analytics, belongs in the payment attack surface and needs patching and integrity checks.

## TL;DR

A Brazilian card-skimming (Magecart) gang changed the Plausible analytics tracker that Convertr hosts on its own servers. That script loads on the checkout pages of every merchant on the platform. Sansec suspects the way in was CVE-2026-8467, an unauthenticated command-execution flaw in Convertr's outdated Plausible Community Edition, but this is not confirmed. The skimmer stole card numbers, expiry dates, CVVs, cardholder names and CPF tax IDs, and Convertr has since removed it and patched Plausible.

## Lessons

- A single shared third-party script served from platform infrastructure exposes every downstream merchant's checkout at once. - _"which loads on the checkout pages of all merchants using the platform."_
- An outdated self-hosted analytics server was the suspected entry point, so its patch level directly affects payment security. - _"an unauthenticated command-execution vulnerability affecting"_
- Attackers tuned the skimmer to the platform's own payment field names after the first wave. - _"the attackers pushed a more refined version that specifically targeted"_
- Browser caching can keep serving the malicious script after cleanup. - _"browser caching could keep the malicious script active on impacted sites for up to 24 hours after cleanup"_

## Threat · Conditions · Mitigations

- **Threat:** Attackers compromise a shared analytics script served from the platform's infrastructure and inject a skimmer that steals card data and CPF tax IDs from every merchant's checkout.
- **Conditions:** An e-commerce platform that serves an outdated, self-hosted Plausible Community Edition tracker on checkout pages (suspected CVE-2026-8467).
- **Mitigations:** Patch or upgrade self-hosted analytics, monitor the integrity of checkout-page scripts, notify affected merchants and payment providers, and account for browser caching after cleanup.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/)  ·  **Retrieved:** 2026-10-28  
**Scores:** Newness 19 · Novelty 28 · Relevance 60 · Credibility 50 · **Composite 39** _(each 0-100)_  
**Tags:** `magecart`, `web-skimming`, `supply-chain`, `plausible-analytics`, `e-commerce`, `payment-card`, `third-party-scripts`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No Magecart or Plausible entries in the pools. Compromising a shared third-party script to skim cards is a well-known Magecart pattern; the new detail is a self-hosted analytics server as the injection point.

_Source: [https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/)_  ·  [← back to index](../README.md)
