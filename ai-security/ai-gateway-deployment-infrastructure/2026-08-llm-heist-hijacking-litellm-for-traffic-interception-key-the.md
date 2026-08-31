# LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection

**Published:** Aug 3, 2026

> **Takeaway:** AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider guardrails. Prompt-level defenses do not see this attack.

## TL;DR

Johann Rehberger walks through a red-team TTP set against LiteLLM, showing that a compromised proxy-admin credential lets an attacker (a) reroute traffic through an attacker-controlled LiteLLM instance, (b) harvest resolved backend LLM provider keys, and (c) modify or forge responses and tool-calls downstream of inference, bypassing all prompt-level defenses. The `llm-heist` tool automates harvest, provision, hijack, inject.

## What to learn

- Tool-call injection at the gateway layer bypasses prompt-level defenses because it modifies responses after inference. - _"Even more interesting though, if the clients are AI agents with tool access, an injected response can carry a tool-call. Because the output is changed **after** inference, this bypasses prompt-level defenses."_
- A single AI-gateway admin credential compromises the whole org's LLM traffic centrally and stealthily, without touching any user machine. - _"*   **It is pretty stealthy.** No configuration changes to developer and user machines.
*   **It is central.** One gateway compromise might cover the entire organization.
*   **It operates after inference.** It's possible to modify requests to the LLM. But we can also inject messages and tool calls downstream of the model, so prompt-level defenses never see it."_
- Only two config settings (`api_base` and `use_litellm_proxy`) via a documented model-management API are needed to reroute all traffic to an attacker gateway; alerting on those changes is a concrete blue-team detection. - _"To achieve that, there are only two settings updated via the [`/model/update`](https://docs.litellm.ai/docs/proxy/model_management) API:

1.   `api_base` is changed to point to the attacker LiteLLM gateway
2.   `use_litellm_proxy` to `true`. This enables proxy mode to route traffic to another instance."_
- Prompt-and-response signing would let clients detect a hostile gateway in the middle; this is a design ask for model providers, not a config the operator can enable today. - _"*   **Prompt and Response Signing.** This is something for the AI labs to consider as a feature! Basically the idea is to enforce integrity and detect an AI gateway in the middle hijacking traffic."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker with LITELLM_MASTER_KEY (or an equivalent proxy-admin credential) reroutes an internal AI gateway through their own LiteLLM instance, harvests resolved backend provider keys from the Authorization header of forwarded requests, and injects arbitrary responses and tool calls (e.g., a Bash tool call) into legitimate agent clients like Claude Code.
- **Conditions:** AI gateway (LiteLLM or similar) deployed as a central proxy with virtual keys. Proxy-admin credential exposure (leaked .env, weak admin UI, unpatched CVE, prior host compromise). Agent clients accept tool calls returned by the gateway without a signature/integrity check (i.e., all current clients). Provider keys not restricted to approved gateway egress IPs; no anomaly detection on config changes.
- **Mitigations:** Alert on any `api_base` or `use_litellm_proxy` change; snapshot model config as code. Alert on new callback/guardrail/hook registrations on the gateway. Restrict provider API keys to source IPs of approved gateway hosts; rotate on a schedule. Independent billing reconciliation against provider dashboards. Lock down admin API/UI: no internet exposure, MFA, short-lived admin tokens. Patch LiteLLM aggressively (CVE-2026-42271 is on CISA KEV). Do not run agent clients in yolo/auto-approve mode; require per-tool confirmation for shell/write tools.

---

**Topic:** AI Security  ·  **Domain:** AI Gateway / Deployment Infrastructure  
**Source:** [source](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)  ·  **Retrieved:** 2026-08-10  
**Scores:** Newness 18 · Novelty 78 · Relevance 90 · Credibility 72 · **Composite 65.78**  
**Tags:** `ai-gateway`, `litellm`, `tool-call-injection`, `adversary-in-the-middle`, `credential-theft`, `red-team`  
**Verification:** ✓ independently verified · closest prior art: Rehberger's earlier writing on indirect prompt injection and MCP tool poisoning; Obsidian Security's LiteLLM privilege-escalation-to-RCE writeup; Sonatype coverage of the March 2026 compromised LiteLLM PyPI package; the wider AiTM literature (T1557).

_Source: [https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)_  ·  [← back to index](../README.md)
