# Five Primitives for Governing Autonomous AI Agents at Runtime

**Published:** Aug 27, 2026

> **Takeaway:** Govern agents at runtime with per-action policy mediation, per-tenant action vocabularies, verifiable ledgers, and explicit availability tradeoffs.

## TL;DR

Enterprise access-control models built for human users and long-lived services fail for agents that are ephemeral, act via model choice rather than fixed programs, and are discovered rather than provisioned. The authors argue agent governance is a runtime problem and derive five primitives - discovery, identity, governance, attestation, supply chain - mediating each action against policy before it takes effect and recording it in a verifiable hash-linked signed ledger.

## What to learn

- Human/service access-control models fail for agents because agents are ephemeral, model-driven, and self-created via any API caller. - _"agent principals are ephemeral, appearing and vanishing faster than provisioning"_
- Agent governance is fundamentally a runtime enforcement problem, distinct from model alignment or build-time controls. - _"governing such agents is a runtime problem -- not a model-alignment problem and not a build-time problem"_
- Mediating each action against policy and recording it in a verifiable signed ledger enables third-party audit without trusting the vendor. - _"recorded in a hash-linked signed ledger a third party can verify with the vendor out of the loop"_
- Runtime mediation has real costs: critical-path latency, per-workload identity sidecars, and fail-closed denial during outages. - _"fail-closed mediation converts availability incidents into denial"_

## Threat · Conditions · Mitigations

- **Threat:** Ungoverned autonomous agents taking unauthorized actions with no verifiable accountability.
- **Conditions:** Enterprise runs autonomous agents whose principals are ephemeral and dynamically created.
- **Mitigations:** Runtime action mediation, agent identity, per-tenant action vocabulary, attestation, and a verifiable signed ledger.

---

**Topic:** AI Security  ·  **Domain:** Agent Governance / Runtime  
**Source:** [arXiv cs.CR](https://arxiv.org/abs/2608.26696)  ·  **Retrieved:** 2026-08-29  
**Scores:** Newness 20 · Novelty 68 · Relevance 83 · Credibility 60 · **Composite 59.3**  
**Tags:** `agent-governance`, `runtime-enforcement`, `identity`, `attestation`, `audit-ledger`, `enterprise`  
**Verification:** ✓ independently verified · closest prior art: IAM/RBAC for humans and services, workload identity (SPIFFE-style sidecars), and transparency-log designs; contribution is the agent-specific five-primitive runtime decomposition.

_Source: [https://arxiv.org/abs/2608.26696](https://arxiv.org/abs/2608.26696)_  ·  [← back to index](../README.md)
