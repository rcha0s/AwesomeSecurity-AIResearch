# Moquette MQTT broker: clientId wildcard injection into pattern ACLs gives cross-tenant read/write, plus pre-auth broker crash, Will-message authorization bypass and fail-open auth (GHSA-5f42-97gr-vfhq, CVE-2026-85724)

**Published:** Sep 23, 2026

> **Takeaway:** Anywhere a user-controlled identity goes into a pattern-matched access rule, escape or reject the pattern's metacharacters, or one tenant can claim everyone's data.

## TL;DR

The Moquette MQTT broker substitutes the raw client ID and username into pattern access-control rules, then wildcard-matches them. A client that connects with client ID "+" turns the rule sensor/%c/# into sensor/+/#, and gets read and write access to every tenant's topics. The same audit found a broker-wide crash from malformed input, Will messages published without authorization checks, and authentication that fails open if its class cannot load.

## Lessons

- Substituting an untrusted identifier into an access rule that is later pattern-matched is an injection bug: MQTT wildcard characters in the client ID widen the rule to every tenant. - _"the clientId/username is substituted raw into a pattern ACL rule and then wildcard-matched, and the clientId is never validated for MQTT wildcard characters +/# at CONNECT"_
- One uncaught exception on a shared, never-restarted event loop takes down every client on the broker, so trivially malformed packets become a whole-broker denial of service. - _"catches only InterruptedException and is never restarted (SessionEventLoopGroup), so any uncaught exception on it wedges every co-located client"_
- Side channels for publishing (the Last-Will message) skipped the authorization checks applied to normal PUBLISH, so every publish path must go through the same check. - _"Last-Will topic is published (PostOffice.publishWill) without canWrite/reserved-topic checks used for normal PUBLISH."_
- If the configured authenticator or authorizer class fails to load, the broker silently falls back to permit-all instead of refusing to start. - _"Fail-open if authenticator/authorizator class fails to load -> PermitAll/AcceptAll"_

## Threat · Conditions · Mitigations

- **Threat:** Any MQTT client, including anonymous ones, reads and injects messages on other tenants' topics, crashes the broker, or corrupts another client's durable queue.
- **Conditions:** Pattern ACL rules using %c/%u configured (for the cross-tenant bypass); network reachability to the broker. DoS needs no special config.
- **Mitigations:** Upgrade to 0.18.1; reject +/# in client IDs and usernames at CONNECT; apply authorization to Will publishes; add resource caps; fail closed on auth-class load errors.

---

**Topic:** Product Security  ·  **Domain:** Identity & Access  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-5f42-97gr-vfhq)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 5 · Novelty 60 · Relevance 65 · Credibility 70 · **Composite 49** _(each 0-100)_  
**Tags:** `mqtt`, `iot`, `multi-tenant`, `acl-bypass`, `authorization`, `wildcard-injection`, `denial-of-service`, `fail-open`, `java`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: etcd Watch API skipped the range authorization Range/Get apply (archive); no MQTT/Moquette entry.

_Source: [https://github.com/advisories/GHSA-5f42-97gr-vfhq](https://github.com/advisories/GHSA-5f42-97gr-vfhq)_  ·  [← back to index](../README.md)
