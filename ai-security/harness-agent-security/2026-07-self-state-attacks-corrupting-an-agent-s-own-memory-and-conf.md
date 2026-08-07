# Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls

**Topic:** AI Security  ·  **Domain:** Harness & Agent Security  
**Source:** [source](https://arxiv.org/abs/2607.17986)  ·  **Author:** Yimeng Chen et al.  ·  **Published:** Jul 20, 2026  ·  **Retrieved:** 2026-07-21  
**Scores:** 🆕 Newness 12 · ✨ Novelty 45 · 🎯 Relevance 80 · 🏛️ Credibility 58 · **Composite 49.12**  
**Tags:** `agent-security`, `self-hosted`, `os-defenses`, `memory-poisoning`, `threat-modeling`  
**Verification:** ✓ independently verified · closest prior art: Agent memory poisoning and config tampering have been discussed piecemeal. The contribution is systematizing the space (four-axis, 23-cell matrix) and measuring which cells OS defenses cover - not a new attack capability, since it presumes existing local write access. 'Self-state attacks' is the authors' own coinage in this paper. Preprint, not peer-reviewed.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

> **Takeaway:** Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.

## TL;DR

_The gist, not every detail - read the [full source](https://arxiv.org/abs/2607.17986) for the complete write-up._

Self-hosted agents read and write their own memory and configuration files, so once an attacker can write to that state the corruption itself is performed with legitimate OS system calls - the malicious step does not look anomalous at the OS layer. The authors formalize a four-axis attack space, realize 43 operations on real self-state files injected into traces from a representative self-hosted agent, and find a layered defense covers most cells with a small residual that stays structurally indistinguishable. Note the precondition: this assumes the attacker already has local write access; the paper does not address how that access is obtained.

## What to learn

- Given an attacker who can already write to an agent's state files, the corruption step is performed with legitimate system calls - so the malicious action itself carries no distinguishing OS-level signal. This is a post-compromise finding, not a new access path. - _"An agent may get compromised via corruption of its own state -- a compromise realized via legitimate OS system call invocation."_ ✅
- Layer the defense by state type: access-control prevention on instruction and configuration layers, workload-conditioned detection on the memory layer, periodic backup for recovery. - _"a layered defense stack (access-control prevention on the instruction and configuration layers, workload-conditioned detection on the memory layer, and periodic backup for recovery) is effective on most attack cells"_ ✅
- For a small residual subset of attack cells, OS-level signals alone are structurally insufficient to separate malicious from legitimate state changes - even though the layered stack handles most cells. Plan for recovery, not prevention alone. - _"a small residual attack surface remains structurally indistinguishable at the OS level"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** An attacker with write access to an agent's instruction, configuration, or memory files redirects its behavior persistently, without exploiting the agent or the OS.
- **Conditions:** Self-hosted agents persisting memory and configuration to the local filesystem, AND an attacker who has already obtained local write access to those files (e.g. via prior code execution).
- **Mitigations:** Apply mandatory access control to instruction/config files, use workload-conditioned detection on memory files, and take periodic backups so recovery is possible for the undetectable residual.

---

_Source: [https://arxiv.org/abs/2607.17986](https://arxiv.org/abs/2607.17986)_  ·  [← back to index](../README.md)
