# Malicious Microsoft agent-framework PyPI versions steal Azure and CI credentials

**Published:** Nov 17, 2026

> **Takeaway:** Teams building agents on Python SDKs should pin versions, scan site-packages for unexpected .pth files, and treat any host that ran 1.26.1 or 1.26.2 as having leaked its cloud identities.

## TL;DR

On November 17, 2026, two malicious versions (1.26.1 and 1.26.2) of Microsoft's agent-framework package were uploaded to PyPI and pulled within about an hour. They drop a .pth file that runs a credential stealer every time Python starts, even if the package is never imported. The stealer collects environment variables, credential files, Azure managed-identity tokens and OIDC tokens, and posts them to a free webhook.site URL that capped how much was captured.

## Lessons

- A .pth file in site-packages runs on every interpreter start, so the package does not have to be imported and removing the import does not help. - _"so the credential stealer runs whenever Python starts in that environment"_
- The upload looks like it bypassed the normal release process: no tag, no sdist, wheel only. A mismatch with a project's usual release shape is a detection signal. - _"This indicates 1.26.1 may have been built outside the project's normal release process and uploaded directly to PyPI."_
- The second version changed file names and trigger, so hunting only for the first version's indicators misses it. - _"Searching only for the 1.26.1 file names will miss this version."_
- Stolen cloud identity tokens stay usable for up to a day, so exposed hosts need identity log review as well as secret rotation. The attacker's free-tier webhook limited capture to at most 50 requests, but those can hold working credentials. - _"Stolen managed-identity and OIDC-exchanged tokens are valid for up to 24 hours."_

## Threat · Conditions · Mitigations

- **Threat:** A malicious wheel uploaded directly to PyPI installs a .pth persistence hook that runs a credential stealer on every Python start and exfiltrates environment secrets, credential files, Azure managed-identity tokens and OIDC tokens to webhook.site.
- **Conditions:** Any environment, VM, container or CI runner that installed agent-framework 1.26.1 or 1.26.2 and then started Python; 1.26.2 also targets GitHub Actions workflows with id-token: write.
- **Mitigations:** Pin to 1.26.0, remove the malicious files, rotate all reachable secrets and tokens, audit Azure sign-in and federated credential logs, and check egress logs for the webhook.site endpoint.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Wiz Research](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 38 · Novelty 40.0 · Relevance 82 · Credibility 66 · **Composite 56** _(each 0-100)_  
**Tags:** `pypi`, `supply-chain`, `pth-file`, `credential-stealer`, `azure`, `oidc`, `agent-framework`, `managed-identity`, `ci-cd`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The LiteLLM 1.107.0 compromise entry in data/ai-security.json (.pth plus sitecustomize.py stealer at interpreter start, Wiz); this adds the Azure managed-identity/ADO/OIDC targeting, the wheel-only no-tag release-shape signal and the repacked second version.

_Source: [https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi)_  ·  [← back to index](../README.md)
