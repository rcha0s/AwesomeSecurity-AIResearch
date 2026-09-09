# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_5 vetted findings · updated 2026-09-09 · ranked by composite · latest 31 days only · [13 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Application Security | 2 |
| software supply chain | 1 |
| web security | 1 |
| Supply Chain & Dependencies | 1 |

## Application Security

- **[phpseclib's Pure-PHP X25519 Implementation Leaks the Full Private Key via a Single Cross-Process libgmp Call-Count Observation](application-security/2026-09-phpseclib-s-pure-php-x25519-implementation-leaks-the-full-pr.md)** · composite **63.15** · Sep 8, 2026  
  This isn't a low-order-input vulnerability that input validation can fix - it's a genuine implementation-level timing/call-count side channel triggered by ordinary use with the standard base point,…  
  _[source](https://github.com/advisories/GHSA-q97c-8qh3-fpc6)_
- **[Citrix NetScaler Pre-Auth Heap Overflow (CVE-2026-8452) Traced to an Unchecked Fixed-Size Buffer Copy During SAML Signature Canonicalization](application-security/2026-08-citrix-netscaler-pre-auth-heap-overflow-cve-2026-8452-traced.md)** · composite **58.17** · Aug 14, 2026  
  A classic, decades-old bug class (unchecked fixed-size buffer copy of attacker-controlled data) is still shipping in 2026 in a security-critical XML/SAML signature-parsing path of a widely deployed…  
  _[source](https://labs.watchtowr.com/youre-back-in-the-room-citrix-netscaler-pre-auth-rce-cve-2026-8452/)_

## software supply chain

- **[This Shit is Hard: Patching a vulnerability that has no fix](software-supply-chain/2026-08-this-shit-is-hard-patching-a-vulnerability-that-has-no-fix.md)** · composite **64.4** · Aug 17, 2026  
  When remediating (including AI-generated) fixes, gate every patch on feasibility, regression testing, and an independent exploit test, batch interdependent fixes, re-validate on each backported…  
  _[Chainguard](https://www.chainguard.dev/unchained)_

## web security

- **[Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](web-security/2026-08-show-don-t-tell-what-evo-continuous-offensive-security-found.md)** · composite **61.4** · Aug 10, 2026  
  Enforce server-side role/permission checks and key allowlists on every write endpoint (including legacy admin ones), actually validate HMAC signatures, and lock down credentialed CORS, then test for…  
  _[Snyk](https://snyk.io/blog/)_

## Supply Chain & Dependencies

- **[Rust Supply-Chain Compromise Used Cargo's Own Yank Warning to Socially Engineer Developers Into the Malicious Version](supply-chain-dependencies/2026-08-rust-supply-chain-compromise-used-cargo-s-own-yank-warning-t.md)** · composite **51.5** · Aug 20, 2026  
  Yanking prior clean versions of a compromised crate is a novel, low-effort social-engineering step that weaponizes the package manager's own UX (Cargo's "consider updating to a version that is not…  
  _[source](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
