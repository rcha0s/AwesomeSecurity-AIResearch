# LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials

**Published:** Sep 9, 2026

> **Takeaway:** Treat AI gateways as Tier-1 infrastructure: change default keys, gate admin features, validate outbound URLs, and give them least-privilege cloud roles.

## TL;DR

Wiz found that LiteLLM's MCP endpoint accepts any invalid Bearer token (CVE-2026-59822, exploited in the wild). Custom code guardrails could run unsandboxed Python (CVE-2026-59821). Wiz also found that 9.6% of 3,074 public instances used the default master key or no auth. Combined with an unvalidated pass-through endpoint that can reach cloud metadata, a gateway compromise becomes cloud credential theft.

## Lessons

- The MCP auth fallback treated every failed token as a pass-through OAuth token and returned an empty auth object, so authentication failure became access. - _"Any garbage token fails validation with a 401, and the handler proceeds as if nothing happened."_
- The sandbox existed only on the test endpoint. The registration path, which actually executes code, skipped both the forbidden-pattern check and the builtins strip. - _"Python repopulates `__builtins__` automatically when it's absent, so submitted code gets the full standard library."_
- Default credentials from documentation examples left a large share of public gateways effectively unauthenticated. - _"Nearly 1 in 10 instances accepted a default master key or required no authentication at all"_
- Unvalidated pass-through routes let an admin-level caller reach cloud metadata and steal IAM credentials, and header forwarding defeats IMDSv2. - _"The target URL is never validated; there are no checks against private IP ranges, localhost, or cloud metadata endpoints."_

## Threat · Conditions · Mitigations

- **Threat:** Unauthenticated MCP tool access, root-level RCE through custom code guardrails, and cloud IAM credential theft via pass-through endpoints.
- **Conditions:** Internet-exposed or internally reachable LiteLLM with default or missing master key, or versions before the fixes; IMDS reachable from the container.
- **Mitigations:** Strong master key, upgrade to patched versions, admin-gate guardrail and config endpoints, validate pass-through URLs, restrict egress, least-privilege IAM.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [Wiz Research](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 4 · Novelty 45 · Relevance 90 · Credibility 72 · **Composite 52** _(each 0-100)_  
**Tags:** `litellm`, `mcp-auth-bypass`, `ai-gateway`, `default-credentials`, `imds`, `rce`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Archive has 'LLM Heist: Hijacking LiteLLM' and a LiteLLM/RAGFlow/Kestra control-point entry, plus the trojanized LiteLLM 1.107.0 item; the MCP auth fallback bypass and guardrail-registration sandbox gap are new details. Verifier: archive.json: 'LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection' and 'When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points'; ai-security.json: 'LiteLLM 1.107.0 trojanized'  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise)_  ·  [← back to index](../README.md)
