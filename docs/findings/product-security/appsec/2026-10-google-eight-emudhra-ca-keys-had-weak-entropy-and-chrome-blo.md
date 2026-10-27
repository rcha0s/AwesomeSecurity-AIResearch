# Google: eight eMudhra CA keys had weak entropy and Chrome blocked them

**Published:** Oct 20, 2026

> **Takeaway:** Weak randomness in CA key generation is catastrophic; Certificate Transparency and fast key-hash blocks are what contained this one.

## TL;DR

On October 17, 2026 Google's Chrome Root Program got a report that private keys for eight eMudhra subordinate CA certificates were generated with insufficient randomness, which would let anyone forge trusted HTTPS certificates. Chrome blocked the keys by public-key hash within about 100 minutes, with no browser update needed. No certificates from the intermediates were logged to Certificate Transparency before the block. Chrome will also remove the emSign ECC Root CA - G3 root.

## Lessons

- Weak entropy means anyone can derive the CA keys and forge certificates for any site. - _"The private keys for these certificates were generated with insufficient randomness (i.e., weak cryptographic entropy), enabling anyone to forge trusted HTTPS certificates to impersonate any website"_
- A key-hash block protected users immediately, with no update. - _"Chrome users were immediately protected against all certificates sharing those keys, without requiring a browser update or restart."_
- Certificate Transparency enforcement limited the damage window. - _"no fraudulent certificates issued by these CAs could have been used against CT-enforcing clients."_
- Site operators must move off the removed root before the Chrome Root Store change. - _"must immediately acquire and install a new TLS certificate from another PKI hierarchy"_

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [source](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 23 · Novelty 40 · Relevance 68 · Credibility 70 · **Composite 49** _(each 0-100)_  
**Tags:** `pki`, `certificate-authority`, `entropy`, `chrome-root-program`, `certificate-transparency`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Past CA incidents (DigiNotar, Symantec) involve compromise or mis-issuance; a weak-entropy intermediate key set blocked in hours is a distinct case. Verifier: Debian OpenSSL weak-key incident (2008); Trustico/DigiCert key-exposure revocation (2018); Symantec and Entrust distrust. Delta: SPKI-hash CRLSet block within ~  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/)_  ·  [← back to index](../README.md)
