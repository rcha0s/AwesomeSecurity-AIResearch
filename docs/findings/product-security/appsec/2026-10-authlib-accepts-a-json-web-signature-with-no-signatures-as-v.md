# Authlib accepts a JSON web signature with no signatures as verified

**Published:** Oct 27, 2026

> **Takeaway:** Any verifier that loops over signatures must reject an empty list; test your JWS and JWT code for that case.

## TL;DR

Authlib before 1.9.0 returns the payload of a JSON Web Signature (JWS) object in JSON serialization as verified when its `signatures` array is empty. The validity flag starts as true and only the per-signature loop can clear it, so an empty list skips every check. Any service that calls `JsonWebSignature.deserialize_json()` on outside input accepts a forged payload, even when it passes the correct key; upgrade to 1.9.0.

## Lessons

- The bug is a fail-open default: the validity flag starts true and only the loop body can clear it, so zero signatures means zero checks. - _"`is_valid` is initialised to `True` and only ever set to `False` from inside the loop."_
- Holding the correct key does not protect the caller, because no signature is ever examined. - _"and [B] shows that holding the correct key does not"_
- Normal tests still pass, so the flaw hides in a deployment that looks healthy. - _"[C] proves the verifier works normally on a genuine object, so a deployment looks healthy."_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated remote attacker forges identity or authorization claims that the relying party accepts as signed.
- **Conditions:** A service calls Authlib's JsonWebSignature.deserialize_json() on input it did not produce, with Authlib before 1.9.0.
- **Mitigations:** Upgrade to Authlib 1.9.0 or joserfc, and reject JWS objects whose signatures array is empty.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-6v38-4h7w-rj9h)  ·  **Retrieved:** 2026-10-27  
**Scores:** Newness 21 · Novelty 30 · Relevance 75 · Credibility 70 · **Composite 47** _(each 0-100)_  
**Tags:** `jws`, `jwt`, `authentication-bypass`, `fail-open`, `python`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Fail-open signature checks such as JWT alg=none bypasses are a known bug class; this is a new instance in Authlib's JWS JSON path, not a new technique.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://github.com/advisories/GHSA-6v38-4h7w-rj9h](https://github.com/advisories/GHSA-6v38-4h7w-rj9h)_  ·  [← back to index](../README.md)
