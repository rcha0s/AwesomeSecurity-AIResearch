# GPUStack treated spoofable loopback requests as admin, and attackers exploited it

**Published:** Nov 9, 2026

> **Takeaway:** Upgrade GPUStack to 2.2.0 now and treat any AI serving control plane that trusts loopback or a client IP header as unauthenticated.

## TL;DR

GPUStack, an open-source GPU cluster manager for AI model serving, treated any request that appeared to come from 127.0.0.1 as the built-in administrator before version 2.2.0, because force_auth_localhost defaulted to false. A remote attacker could look local through a same-host reverse proxy or a client-supplied X-GPUStack-Real-IP header, gaining admin API keys, worker and cloud-provider secrets, and code execution via POST /v2/inference-backends/from-yaml. CISA added CVE-2026-102895 to its Known Exploited Vulnerabilities catalog on 2026-11-09 after exploitation of a 2.1.1 deployment, with a 2026-11-12 due date.

## Lessons

- Trusting a loopback origin gives remote attackers admin access once a reverse proxy sits on the same host or clients can set the source-IP header. - _"A remote request could appear to originate from 127.0.0.1 because client_ip_getter accepted a same-host reverse proxy peer or a client-supplied X-GPUStack-Real-IP loopback value."_
- The insecure behavior was the default. Deployments that did not enable localhost authentication were exposed by default. - _"treated a loopback request source as the built-in administrator when force_auth_localhost was false, which was the default"_
- An admin bypass on a model-serving control plane yields secrets and code execution, not just model tampering. - _"disclosure of worker and cloud-provider secrets, and code execution through POST /v2/inference-backends/from-yaml"_
- Exploitation is confirmed in the wild, not just a theoretical advisory. - _"Exploitation was observed in the wild against a 2.1.1 deployment. This issue is fixed in version 2.2.0."_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated remote attacker spoofs a loopback source to become GPUStack administrator, then steals secrets, creates persistent admin API keys and runs code through a custom inference backend.
- **Conditions:** GPUStack before 2.2.0 with force_auth_localhost left at its default of false, reachable through a same-host reverse proxy or accepting the X-GPUStack-Real-IP header from clients.
- **Mitigations:** Upgrade to 2.2.0, enable force_auth_localhost, drop client-supplied real-IP headers at the proxy, keep the management API off the internet, revoke unknown admin API keys and rotate cloud and worker secrets.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [CISA Known Exploited Vulnerabilities](https://nvd.nist.gov/vuln/detail/CVE-2026-102895)  ·  **Retrieved:** 2026-11-10  
**Scores:** Newness 49 · Novelty 25 · Relevance 80 · Credibility 64 · **Composite 53** _(each 0-100)_  
**Tags:** `kev`, `exploited-in-the-wild`, `authentication-bypass`, `model-serving`, `ip-spoofing`, `gpustack`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Loopback-trust bugs in coding-agent and MCP localhost servers; classic X-Forwarded-For authentication bypass.

_Source: [https://nvd.nist.gov/vuln/detail/CVE-2026-102895](https://nvd.nist.gov/vuln/detail/CVE-2026-102895)_  ·  [← back to index](../README.md)
