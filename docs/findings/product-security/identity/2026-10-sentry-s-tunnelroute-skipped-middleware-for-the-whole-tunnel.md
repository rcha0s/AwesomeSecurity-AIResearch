# Sentry's tunnelRoute skipped middleware for the whole tunnel path, not just rewrites

**Published:** Oct 22, 2026

> **Takeaway:** Any SDK or framework that exempts paths from middleware is a potential authz bypass: if middleware is your only authorization check, grep your dependencies for middleware skips.

## TL;DR

@sentry/nextjs's tunnelRoute option forwards browser events through a path on your own Next.js server and tells the SDK to skip middleware for them. The skip matched every path under the tunnel prefix, while the rewrite only served the exact tunnel path with the o and p parameters, so any app route that resolves under that prefix (a direct collision or a root dynamic segment like app/[locale]) ran without middleware. It is only an authorization bypass where middleware is the sole authz layer; fixed in 9.47.2, 10.75.2 and 11.0.0-rc.1.

## Lessons

- The bug is a scope mismatch: an exemption (skip middleware) was matched more broadly than the thing it existed to protect (the rewrite). - _"The middleware skip was wider than the rewrite."_
- Requests in the gap reach application routes with middleware never executed. - _"Requests in that gap go to your application instead of Sentry, and your middleware never runs on them."_
- It is only exploitable when middleware is the sole authorization layer for the colliding routes; server-side session checks still hold. - _"your middleware is the only place that enforces authorization for those routes"_
- The durable fix is defense in depth: enforce authorization in the route, layout or data-access layer as well as middleware. - _"Enforce authorization in the route, layout or data-access path as well as in middleware."_
- Only webpack builds are affected. - _"Turbopack builds are not affected"_

## Threat · Conditions · Mitigations

- **Threat:** Unauthenticated access to Next.js routes whose only authorization check lives in middleware, by requesting them under the Sentry tunnel prefix.
- **Conditions:** tunnelRoute set; webpack build; an app route resolving under the tunnel path (including a root dynamic segment); middleware-only authorization.
- **Mitigations:** Upgrade @sentry/nextjs to 9.47.2 / 10.75.2 / 11.0.0-rc.1; move tunnelRoute to a path no route can resolve under; build with Turbopack; enforce authz in routes or data access, not only middleware.

---

**Topic:** Product Security  ·  **Domain:** Identity & Access  
**Source:** [source](https://github.com/advisories/GHSA-mchm-gjx6-7h55)  ·  **Retrieved:** 2026-10-23  
**Scores:** Newness 20 · Novelty 40 · Relevance 78 · Credibility 70 · **Composite 51** _(each 0-100)_  
**Tags:** `nextjs`, `middleware`, `authorization-bypass`, `sentry`, `ghsa`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Next.js CVE-2025-29927 (x-middleware-subrequest middleware bypass) established that middleware-only authorization in Next.js is fragile; this is a new, SDK-introduced instance of the same class.

_Source: [https://github.com/advisories/GHSA-mchm-gjx6-7h55](https://github.com/advisories/GHSA-mchm-gjx6-7h55)_  ·  [← back to index](../README.md)
