# LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys

**Published:** Oct 21, 2026

> **Takeaway:** An AI gateway holds every provider key you own: pin and verify its releases, and keep its logs and admin surface away from tokens and the internet.

## TL;DR

On October 21, 2026 a malicious LiteLLM 1.107.0 was uploaded to PyPI (about 49,000 downloads before quarantine) and shipped in the Docker images. It runs at interpreter start through both a .pth file and sitecustomize.py, steals browser, cloud, SSH and AI-provider secrets, and reads the LiteLLM proxy's stored provider keys from its database. LiteLLM says the attacker used stolen GitHub CLI OAuth tokens and believes they came from the logs of an internal LiteLLM deployment that was exposed to the internet; how the attacker got in is not yet confirmed. The last safe version is 1.106.2.

## Lessons

- The release pipeline was abused with stolen developer OAuth tokens: one account triggered the release run and another approved it. - _"malicious actions were taken through three engineers' GitHub accounts, appearing to be by way of stolen GitHub CLI OAuth tokens."_
- LiteLLM suspects tokens leaked through logging: in some cases a coding agent embedded a GitHub CLI token in a response body, and response bodies were logged. - _"specific situations in which Claude Code will embed a user’s GitHub CLI OAuth token into a response body"_
- The payload runs on every Python start by combining a .pth file and sitecustomize.py, which Wiz calls the first documented case of both in the wild. - _"The dual-technique approach, using both `.pth` files and `sitecustomize.py` simultaneously, appears to be the first documented case in the wild."_
- The stealer goes straight for the gateway's stored upstream API keys, so a compromised gateway exposes every provider account behind it. - _"The stealer queries this database directly"_
- Exposure was wide before PyPI quarantined the release. - _"the malicious version received approximately 49,000 downloads."_

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [source](https://www.wiz.io/blog/litellm-compromised-steals-credentials)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 24 · Novelty 52 · Relevance 90 · Credibility 55 · **Composite 57** _(each 0-100)_  
**Tags:** `litellm`, `pypi`, `supply-chain`, `credential-theft`, `llm-gateway`, `oauth-tokens`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: August research on hijacking LiteLLM (Embrace The Red) and Microsoft's gateway-as-target post covered the attack surface; this is the first observed trojanized release with the .pth plus sitecustomize combination. Verifier: Shai-Hulud/tj-actions/PyPI .pth malware, earlier LiteLLM-style gateway targeting; delta is token theft via coding-agent token leakage into proxy logs, dual .pth  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.wiz.io/blog/litellm-compromised-steals-credentials](https://www.wiz.io/blog/litellm-compromised-steals-credentials)_  ·  [← back to index](../README.md)
