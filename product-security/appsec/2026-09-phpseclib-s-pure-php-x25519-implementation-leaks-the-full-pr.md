# phpseclib's Pure-PHP X25519 Implementation Leaks the Full Private Key via a Single Cross-Process libgmp Call-Count Observation

**Published:** Sep 8, 2026

> **Takeaway:** This isn't a low-order-input vulnerability that input validation can fix - it's a genuine implementation-level timing/call-count side channel triggered by ordinary use with the standard base point, and it demonstrates that counting a shared library's internal function calls (via cache-timing techniques) can be a strictly more powerful side channel than wall-clock timing, extracting a full key from a single observed operation instead of dozens.

## TL;DR

phpseclib's pure-PHP X25519 scalar multiplication performs data-dependent conditional modular reductions whose cost is a function of the secret scalar's prefix. A timing side-channel recovers the full 251-bit clamped private key from 32 observed operations using ordinary RFC 7748 base-point input (u=9) - no attacker-chosen input required, and rejecting low-order inputs does not close it. Critically, counting libgmp function calls instead of timing (e.g. via a Flush+Reload cache spy on the shared libgmp.so mapping) recovers a key from a single operation, tolerating 20-30% wrong per-step counts.

## What to learn

- The attack recovers the full private key using the standard RFC 7748 base point (u=9) with no attacker-chosen input at all, and explicitly is not a low-order-input issue - rejecting low-order public values does not mitigate it. - _"This is not a low-order-input issue. Recovery works with the RFC 7748 base point `u = 9`, with no attacker-chosen input at all. Rejecting low-order public values does not close it."_
- An observer that counts libgmp function calls instead of measuring timing recovers a full key from a single observed operation, and tolerates 20-30% of individual per-step counts being wrong, compared to 32 observations needed for the timing-based variant. - _"libgmp call counts | either | **1** | 20/20 keys; tolerates 20 - 30% of per-step counts being wrong"_
- The vulnerable code path in the common key-loading APIs is reachable only when PHP's bundled ext-sodium extension is absent, since the safe sodium implementation is used instead whenever it's available. - _"`PKCS8` / `PublicKeyLoader::load` / `EC::createKey` run the ladder **only when ext-sodium is absent** - `PKCS8.php:194` gates on `sodium_crypto_box_publickey_from_secretkey`. OpenSSL does not help here."_
- Because ext-sodium is bundled and enabled by default in PHP 7.2+, most default installations are not exposed via the common code paths - but hardened or stripped-down PHP builds (disable_functions hardening, --disable-sodium builds, common in shared hosting) are. - _"ext-sodium is bundled and enabled by default in PHP 7.2+, so the reachable configurations are a minority - though `disable_functions` hardening and `--disable-sodium` builds do occur, particularly in shared hosting."_

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [source](https://github.com/advisories/GHSA-q97c-8qh3-fpc6)  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 63 · Novelty 68 · Relevance 55 · Credibility 70 · **Composite 63.15**  
**Tags:** `phpseclib`, `x25519`, `timing-side-channel`, `cryptography`, `ghsa`  
**Verification:** ✓ independently verified · closest prior art: Non-constant-time EC/RSA timing side channels and cache-based operation-counting attacks (Percival 2005, Flush+Reload) are an established class; using library call-counting to cut required observations from dozens to one is a novel specific contribution.

_Source: [https://github.com/advisories/GHSA-q97c-8qh3-fpc6](https://github.com/advisories/GHSA-q97c-8qh3-fpc6)_  ·  [← back to index](../README.md)
