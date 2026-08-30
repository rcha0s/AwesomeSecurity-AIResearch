# When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points

**Published:** Aug 26, 2026

> **Takeaway:** Attackers are already treating AI gateways like LiteLLM as a credential-rich control plane, so these services need the same scrutiny as any critical enterprise infrastructure.

## TL;DR

Microsoft details in-the-wild compromises of three AI workloads - a LiteLLM gateway, a RAGFlow deployment, and a Kestra orchestration environment - where attackers converged on credential theft, persistence, and cryptomining. For LiteLLM, code execution in the gateway process led to harvesting /proc/1/environ secrets and dumping virtual-key/model tables. The report frames AI gateways/retrieval/orchestration as a high-value control plane needing dedicated monitoring.

## What to learn

- AI gateways, retrieval, and orchestration services concentrate credentials, data access and execution privileges, making them high-value targets. - _"These systems concentrate credentials, data access, model connectivity, and execution privileges, making them some of the most powerful components in the AI stack."_ ✅
- Different AI workloads with different intrusion paths converge on the same objectives: credential theft, persistence, and compute monetization. - _"attackers treated AI infrastructure as a control plane where credential theft, host compromise, and downstream data access can converge"_ ✅
- Containerized gateways running as PID 1 leak their whole secret-bearing environment via /proc/1/environ once code execution is achieved. - _"In containerized LiteLLM deployments where the gateway runs as PID 1, /proc/1/environ exposes the environment block for the gateway process."_ ✅
- Monitor AI workloads by their control-plane role, correlating app-origin shells with secret access and outbound callbacks. - _"Defenders should monitor AI workloads according to their control-plane role, not only as isolated applications."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Exploitation of exposed AI gateway/retrieval/orchestration services for credential theft, persistence, data access, and cryptomining.
- **Conditions:** Organizations exposing LiteLLM, RAGFlow, Kestra or similar AI infrastructure to the network, especially in default/containerized configs.
- **Mitigations:** Patch known CVEs, remove public exposure, least-privilege secrets, secure Docker socket, monitor control-plane-origin execution and secret access.

---

**Topic:** AI Security  ·  **Domain:** AI Gateway & Infrastructure  
**Source:** [Microsoft Threat Intelligence (Microsoft Security Blog)](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)  ·  **Retrieved:** 2026-08-29  
**Scores:** 🆕 Newness 20 · ✨ Novelty 62 · 🎯 Relevance 88 · 🏛️ Credibility 72 · **Composite 60.74**  
**Tags:** `litellm`, `ai-gateway`, `ragflow`, `kestra`, `credential-harvesting`, `cryptomining`, `supply-chain`  
**Verification:** ✓ independently verified · closest prior art: Public LiteLLM CVE research; Embrace The Red's LiteLLM hijack post; general cryptomining intrusions

_Source: [https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)_  ·  [← back to index](../README.md)
