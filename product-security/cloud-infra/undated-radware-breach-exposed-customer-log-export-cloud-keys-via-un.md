# Radware breach exposed customer log-export cloud keys via unauthenticated management API

**Published:** Nov 24, 2026

> **Takeaway:** Static storage keys held by a vendor become your exposure when the vendor is breached; rotate them and scope them to write-only.

## TL;DR

On November 19, 2026, an unauthorized party reached an internal Radware Cloud WAF management API that was open to the internet without authentication. Exposed data included customer contact details and, for some customers, the credentials used to export logs to AWS S3, Azure Blob Storage or SFTP. Radware says WAF traffic inspection and end-user data were not affected; the report comes from a root cause analysis shared with BleepingComputer, and Radware has made no public statement yet.

## Lessons

- An internal-only management API was reachable from the internet with no authentication, which was the root cause. - _"an internal-only Cloud WAF management API that was reachable from the Public Internet without requiring authentication"_
- Customers using Cloud WAF log export should rotate those storage keys and check storage access logs back to November 19. - _"rotate Cloud WAF log export credentials (including Azure Blob Storage keys or SAS tokens, AWS S3 access keys, or SFTP credentials) as soon as possible"_
- The exposed keys may already be in use: customers reported AWS alerts for an unfamiliar IP address, though Radware says only that the credentials were potentially accessed. - _"has already received reports from customers about AWS alerts for an unfamiliar IP address attempting to access their log-export buckets"_

## Threat · Conditions · Mitigations

- **Threat:** Attackers who hold customers' log-export keys can read or tamper with the storage those keys reach.
- **Conditions:** Customer uses Radware Cloud WAF (AppSec WAF or bot protection) with log export to self-managed storage.
- **Mitigations:** Rotate the log-export credentials, review storage access logs since November 19, and restrict the keys to write-only access on a dedicated bucket.

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/radware-discloses-breach-exposing-customer-cloud-access-keys/)  ·  **Retrieved:** 2026-11-25  
**Scores:** Newness 0 · Novelty 40 · Relevance 65 · Credibility 45 · **Composite 38** _(each 0-100)_  
**Tags:** `radware`, `waf`, `cloud-credentials`, `vendor-breach`, `exposed-api`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest is the standing claim that long-lived cloud credentials are the common cause of cloud exposure; no pool entry covers a security vendor's exposed management API leaking customer log-export keys.

_Source: [https://www.bleepingcomputer.com/news/security/radware-discloses-breach-exposing-customer-cloud-access-keys/](https://www.bleepingcomputer.com/news/security/radware-discloses-breach-exposing-customer-cloud-access-keys/)_  ·  [← back to index](../README.md)
