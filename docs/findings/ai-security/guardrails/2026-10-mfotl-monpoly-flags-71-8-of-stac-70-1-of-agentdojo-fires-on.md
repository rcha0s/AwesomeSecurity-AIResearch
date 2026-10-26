# MFOTL (MonPoly) flags 71.8% of STAC, 70.1% of AgentDojo, fires on 29.3% of benign; one planted line beats provenance 94-99% of flagged runs

**Published:** Oct 7, 2026

> **Takeaway:** A declarative policy monitor is only as good as the trace it reads: log approvals, timestamps and provenance that the agent cannot forge, or temporal guardrails turn into coarse action-type blocklists.

## TL;DR

The authors express agent safety policies in metric first-order temporal logic (MFOTL) and replay the recorded AgentDojo, STAC and R-Judge trajectories through the unmodified MonPoly monitor. Five generic obligations catch about 70% of attacks but also fire on 29.3% of benign runs, mostly because the benchmark traces lack approvals and timestamps, so history-based rules reduce to flagging risky action types. Provenance-aware policies do better, but one planted line defeats a naive provenance check on 94-99% of flagged runs. Binding provenance to the lookup that produced it closes that gap at no cost.

## Lessons

- Generic temporal obligations catch most attacks but with a high benign firing rate. - _"five generic obligations flag 71.8% of STAC attack chains and 70.1% of successful AgentDojo attacks, but also fire on 29.3% of benign runs"_
- The false positives come from thin traces, not from the logic, so logging is the bottleneck. - _"they rarely record approvals and never record timestamps, so history-dependent obligations reduce to detecting risky action types"_
- Provenance carried in agent-visible data can be forged by injected content. - _"one planted line defeats a naive provenance check on 94-99% of the runs it would otherwise flag"_
- Tie provenance to the tool call that fetched the data, not to labels in the content. - _"Binding provenance to the lookup that produced it closes this evasion at no cost in detection or benign firing"_

---

**Topic:** AI Security  ·  **Domain:** Guardrails & Defensive Tooling  
**Source:** [CCS (via arXiv)](http://arxiv.org/abs/2610.09793v1)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 24 · Novelty 62 · Relevance 70 · Credibility 72 · **Composite 56** _(each 0-100)_  
**Tags:** `runtime-verification`, `guardrails`, `agentdojo`, `temporal-logic`, `provenance`, `agent-traces`, `prompt-injection`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: AgentDojo and STAC are the benchmarks. Earlier guardrails are mostly per-app rules or LLM classifiers, and CaMeL-style capability tracking enforces data flow inside the interpreter. This paper measures off-the-shelf formal temporal monitoring on existing traces, shows the benchmarks' logging is what limits it, and gives a concrete forged-provenance evasion and its fix. That adds evidence to the contested provenance-auditing claim: it works only when provenance is bound by the harness.

_Source: [http://arxiv.org/abs/2610.09793v1](http://arxiv.org/abs/2610.09793v1)_  ·  [← back to index](../README.md)
