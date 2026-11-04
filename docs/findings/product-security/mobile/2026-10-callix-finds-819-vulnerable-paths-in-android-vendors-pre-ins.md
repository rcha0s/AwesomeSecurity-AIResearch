# Callix finds 819 vulnerable paths in Android vendors' pre-installed apps

**Published:** Oct 31, 2026

> **Takeaway:** An access check being present is not the same as being sufficient; audit checks against what the callsite actually touches.

## TL;DR

Scanners for pre-installed Android apps look for calls to a fixed list of sensitive APIs, so they miss generic calls such as database reads that touch protected data with weak access checks. Callix, an NDSS 2027 tool, judges each callsite's sensitivity from the API and the data, then checks whether the guarding checks are sufficient for that operation. Across 1,750 pre-installed apps from the 10 largest Android vendors it found 819 vulnerable paths, 42.1% exposing private user data through generic database operations, at 95.1% precision on a sampled check.

## Lessons

- Sensitive-API lists miss generic APIs that become sensitive because of the data they operate on. - _"this misses a class of vulnerabilities in which a generic API, such as a database read, appears benign in general but becomes security-sensitive when operating on protected data, yet is left without sufficient access control"_
- Prior analyses only asked whether a check exists, not whether it is strong enough for that operation. - _"existing studies focus only on the presence of checks, not on whether those checks enforce sufficient protection for the operation at a given callsite"_
- Of the 819 vulnerable paths found, 42.1% allow reading or modifying private user data through generic database operations. - _"Callix discovered 819 vulnerable paths across these vendors, 42.1% of which allow reading or modifying private user data through generic database operations"_

## Threat · Conditions · Mitigations

- **Threat:** A malicious app on the device reads or modifies private user data through a pre-installed vendor app's exported component guarded by an insufficient check.
- **Conditions:** A vendor app exposes a generic operation, such as a database query, over protected data with a weak or mismatched permission check.
- **Mitigations:** Audit exported components by callsite and data sensitivity, require signature-level or strong permissions for operations on protected data, and verify the caller in every path.

---

**Topic:** Product Security  ·  **Domain:** Mobile & Device Security  
**Source:** [NDSS (via arXiv)](http://arxiv.org/abs/2611.00594v1)  ·  **Retrieved:** 2026-11-04  
**Scores:** Newness 14 · Novelty 62 · Relevance 60 · Credibility 72 · **Composite 51** _(each 0-100)_  
**Tags:** `android`, `pre-installed-apps`, `access-control`, `static-analysis`, `firmware`, `content-providers`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier pre-installed-app studies flag calls to curated sensitive-API sets and check for presence of permission checks (Woodpecker, PScout, Kratos, ACMiner-style analyses). Callix adds callsite-level sensitivity and sufficiency checking.

_Source: [http://arxiv.org/abs/2611.00594v1](http://arxiv.org/abs/2611.00594v1)_  ·  [← back to index](../README.md)
