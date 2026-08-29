# Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS

**Topic:** Product Security  ·  **Domain:** web security  
**Source:** [Snyk](https://snyk.io/blog/)  ·  **Published:** Aug 10, 2026  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 74 · 🎯 Relevance 85 · 🏛️ Credibility 73 · **Composite 63.65**  
**Tags:** `broken-access-control`, `mass-assignment`, `authorization`, `cors`, `multi-tenant`, `saas`, `ai-pentesting`, `business-logic`  
**Verification:** ✓ independently verified · closest prior art: OWASP broken object/function-level authorization (BOLA/BFLA), mass-assignment, and credentialed CORS misconfiguration research.

> **Takeaway:** Enforce server-side role/permission checks and key allowlists on every write endpoint (including legacy admin ones), actually validate HMAC signatures, and lock down credentialed CORS, then test for authorization and business-logic chains that signature scanners miss.

## TL;DR

_The gist, not every detail - read the [full source](https://snyk.io/blog/) for the complete write-up._

Snyk's autonomous offensive-security agent (Evo COS) black-box tested a multi-tenant SaaS and found 33 validated issues, including a legacy admin JSON endpoint that did an unbounded key/value upsert with no role check and no enforcement of its HMAC signature/timestamp, letting the lowest-privilege user rewrite tenant-wide security settings for full compromise. It also proved a credentialed CORS origin-reflection flaw enabling zero-interaction token theft. The lessons are classic broken-authorization and CORS defenses: enforce server-side role checks, allowlist settable keys, actually verify signatures, and lock down cross-origin credentialed responses.

## What to learn

- Server-side authorization must be enforced on every write, especially legacy/admin endpoints, not assumed from the UI. - _"performed an unbounded key/value upsert with no server-side role or permission check"_ ✅
- Restrict mass-assignment by allowlisting settable keys rather than accepting arbitrary input. - _"No allowlist of settable keys; the endpoint accepts any key string"_ ✅
- Business-logic/authorization chains are invisible to signature-based scanners and need reasoning-driven testing. - _"This is the reasoning layer that traditional scanners cannot reach: recognizing an ungated write, understanding what each setting means for the business, and chaining a handful of them into tenant-wide compromise"_ ✅

---

_Source: [https://snyk.io/blog/](https://snyk.io/blog/)_  ·  [← back to index](../README.md)
