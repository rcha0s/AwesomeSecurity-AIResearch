# Hardware Keystores for AI Agent Signing Workflows: A Zero-Trust MCP Enforcement Architecture

**Published:** Aug 7, 2026

> **Takeaway:** Hardware confinement of agent signing keys, combined with content-aware authorisation, cut prompt-injection-driven Attack Success Rate from 19.3% baseline to 0% (Wilson 95% CI upper bound 2.0%) with zero false positives on benign tasks.

## TL;DR

Proposes replacing software-resident private keys used by AI agents (Git signing, API auth, cert issuance) with hardware-confined keys accessed via PKCS#11 and surrounded by a five-layer Zero-Trust stack (SAGA identity, Smax scope bounds, RAV semantic validation, taint tracking, hardware execution boundary). Evaluated on 12 injection scenarios derived from AgentDojo's ImportantInstructionsAttack across four LLMs.

## What to learn

- Agents holding private keys in plaintext files, env vars, or container memory are a demonstrated exfiltration target under prompt injection. - _"AI agents performing cryptographic operations (signing Git commits, authenticating API calls, issuing certificates) currently store private keys in software-accessible locations: plaintext files, environment variables, or container memory. Any process with sufficient read privileges can extract the raw key material. A recent production incident demonstrated the practical severity: private keys were exfiltrated from a widely deployed framework via email injection in under five minutes."_ ✅
- PKCS#11-fronted HSM/TPM/smart-card execution moves signing off the host so the agent only ever handles opaque handles, not raw key material. - _"we replace software-resident keys with hardware-confined keys accessible through a vendor-neutral PKCS#11 interface. A hardware keystore (HSM, TPM, smart card) executes cryptographic operations on-device; the host receives only the result via opaque handles."_ ✅
- Reported effect size against injection is large: 19.3% baseline ASR to 0% with the full stack, across three of four evaluated LLMs following injections in baseline mode. - _"Baseline Attack Success Rate (ASR): 19.3% [14.3%, 25.4%]; protected ASR: 0% (Wilson 95% CI upper bound 2.0%). Zero false positives across four benign task scenarios."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** AI agent private keys stored in host-accessible memory can be exfiltrated via indirect prompt injection (e.g., email content) in minutes, letting an attacker sign commits, calls, or certificates on the agent's identity.
- **Conditions:** Applies when an LLM agent (a) holds a private key in software-accessible form, and (b) ingests untrusted content (email, docs, MCP tool responses) that can steer its tool calls.
- **Mitigations:** Move signing keys into an HSM/TPM/smart card exposed via PKCS#11, restrict operations to opaque handles, add session identity, scope bounds, semantic validation, and taint tracking around the hardware boundary; evaluate with an AgentDojo-style injection corpus.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://arxiv.org/abs/2608.06130)  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 20 · ✨ Novelty 62 · 🎯 Relevance 78 · 🏛️ Credibility 52 · **Composite 54.78**  
**Tags:** `mcp`, `agent-security`, `prompt-injection`, `hsm`, `pkcs11`, `zero-trust`  
**Verification:** ✓ independently verified · closest prior art: AgentDojo (Debenedetti et al., arXiv:2406.13352) supplies the ImportantInstructionsAttack template used here; classic HSM/TPM literature and PKCS#11 predate this work by decades.

_Source: [https://arxiv.org/abs/2608.06130](https://arxiv.org/abs/2608.06130)_  ·  [← back to index](../README.md)
