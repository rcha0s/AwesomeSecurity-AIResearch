# Malicious WPPConnect npm and Docker releases steal secrets and WhatsApp sessions

**Published:** Nov 17, 2026

> **Takeaway:** Do not treat a trusted publisher or provenance check as proof of review; add release-age delays, environment approval gates on publish workflows, and egress allowlists in CI.

## TL;DR

On November 15-16, 2026, two WPPConnect npm packages were published with a hidden module that copies environment variables, config files and WhatsApp session tokens to a Telegram bot. The releases came from the project's own GitHub Actions pipeline, using a trusted-publisher identity and (for the library) valid SLSA provenance, but the commits behind them were never reviewed. After a researcher opened public issues, the maintainer account force-pushed the branches and the release tag was moved to a look-alike commit without the payload, so GitHub no longer matched npm.

## Lessons

- The payload runs when the library is imported or the server starts, so install-script blocking does not help. - _"The code fires when the library is loaded or the server starts."_
- A valid trusted-publisher identity and SLSA provenance prove where a build ran, not that the source was reviewed. The publish workflow had no environment gate requiring human approval. - _"Provenance proves where a package was built, not whether anyone reviewed the source."_
- Attackers with maintainer access can rewrite tags and history so the code on GitHub differs from the code in the published tarball. Compare the tarball or image digest, not the tag. - _"Anyone reviewing the tagged source on GitHub did not find the code that shipped in the tarball."_
- A release-age delay would have blocked this incident, since the bad library version was the latest for only about 4.5 hours. - _"A 24-hour delay would have kept 2.4.1 out."_

## Threat · Conditions · Mitigations

- **Threat:** A compromised maintainer account pushed unreviewed commits and used the project's own release automation to publish npm packages, Docker images and a nightly release that exfiltrate secrets and WhatsApp session tokens to a Telegram bot.
- **Conditions:** A host or CI job loaded @wppconnect-team/wppconnect 2.4.1 (or 2.4.3) or ran @wppconnect/server 2.10.82/2.10.83 or an affected Docker image; the server variant skips CI and sandbox hosts, the library variant does not.
- **Mitigations:** Pin clean versions (library 2.4.0, server 2.10.81) with a lockfile, compare Docker digests instead of tags, rotate every secret reachable by the process, unlink WhatsApp sessions, and enforce release-age delays plus an egress allowlist.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [StepSecurity](https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 22 · Novelty 45.0 · Relevance 80 · Credibility 48 · **Composite 50** _(each 0-100)_  
**Tags:** `npm`, `supply-chain`, `github-actions`, `provenance`, `trusted-publishing`, `credential-theft`, `docker`, `telegram-exfiltration`, `release-cooldown`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Existing product-security entries on import-time payloads, Socket's GitHub Actions hardening/cooldown guidance and release-age delay entries; the valid-SLSA-provenance-on-unreviewed-commit plus tag-rewrite-after-disclosure detail is the new part (minor nit: the lesson says 'attackers with maintainer access' while the source says it did not establish how the account was accessed).

_Source: [https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions](https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions)_  ·  [← back to index](../README.md)
