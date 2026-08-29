# Chainguard's microVM primitive: hypervisor-enforced egress, no ambient credentials, and per-job destruction as the default posture for AI agents

**Topic:** AI Security  ·  **Domain:** Deployment Infra & Sandboxing  
**Source:** [source](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena)  ·  **Published:** Jul 29, 2026  ·  **Retrieved:** 2026-08-10  
**Scores:** 🆕 Newness 4 · ✨ Novelty 75 · 🎯 Relevance 90 · 🏛️ Credibility 55 · **Composite 58.75**  
**Tags:** `microvm`, `sandboxing`, `gvisor`, `egress-control`, `imds`, `ephemeral-credentials`, `chainguard`, `athena`, `slsa-l3`  
**Verification:** ✓ independently verified · closest prior art: Extends SLSA L3 build-isolation and Firecracker/gVisor microVM patterns; picks up the same 'containers don't contain' framing that Edera and others advance. Reinforces claims imdsv1-must-be-disabled-on-agent-workloads, long-lived-cloud-credentials-are-obsolete, ssrf-guards-must-cover-agent-outbound-calls.

> **Takeaway:** Sandboxing agents is a solved discipline reused from CI/cloud, not a new one. The load-bearing primitives are hypervisor-enforced egress with default-destroy, no ambient credentials, ephemeral per-job root filesystems, and treating the sandbox itself as a target under recurring adversarial audit.

## TL;DR

_The gist, not every detail - read the [full source](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena) for the complete write-up._

Chainguard describes how it extracted its Elastic Builds isolation layer into a standalone 'microVM' primitive that now hosts package builds, image builds, CI runs, and their internal AI agents (including Athena, which handles undisclosed vulns and working exploits). The design is explicit: containers are not a boundary, so every job runs in a hardware-virtualized QEMU/KVM guest with its own kernel. Egress is enforced at the hypervisor via a gVisor-based network stack with default-destroy on the first forbidden connection; cloud metadata, private ranges, and loopback are blocked even in relaxed configs. Pods hosting VMs have no service-account tokens; long-lived keys never enter the guest, and identity is minted per use. They also run recurring adversarial audits (including AI agents pointed at the codebase) and land every finding as a regression test.

## What to learn

- Containers are not treated as a security boundary; the boundary is a per-job hardware-virtualized VM with its own kernel. - _"We've never considered containers to be a security boundary ("containers don't contain"), so every build runs inside a hardware-virtualized QEMU/KVM guest with its own kernel."_ ✅
- Egress is enforced at the hypervisor, not inside the guest, and violations destroy the VM instantly rather than logging. - _"Egress control lives at the hypervisor layer. We replaced QEMU's user-mode networking with a gVisor-based network stack that enforces policy. The default posture is to destroy. The first forbidden connection causes the VM to be torn down."_ ✅
- A mandatory floor blocks cloud metadata, private ranges, and loopback regardless of workload policy, closing the classic IMDS / SSRF escalation path. - _"a mandatory floor blocks cloud metadata, private ranges, and loopback, even in relaxed configurations"_ ✅
- There are no ambient credentials in the guest; identity is minted per use or the authenticated call is proxied at the supervisor. - _"The pods hosting these VMs are inert. They have no service-account tokens and no mounted secrets. When a workload legitimately needs to authenticate, identity is synthetic and minted per use, as a short-lived token created at the moment it is read."_ ✅
- The sandbox itself is treated as an attack target under recurring adversarial audit - including AI agents instructed to break it - and findings are pinned as regression tests. - _"We run recurring adversarial audits against it, including pointing AI agents at the codebase with instructions to break it. Every finding lands as a failing test first, then the fix, pinned as a regression test in CI."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** An AI agent (or any untrusted-code runtime) with ambient cloud credentials, unrestricted egress, or a shared container-only boundary is one prompt injection / capability-elicitation moment away from touching cloud metadata, private networks, or long-lived tokens and pivoting outward - exactly the OpenAI/Anthropic incident pattern.
- **Conditions:** Any environment executing agent-generated code or third-party code without hypervisor-level isolation, without a default-destroy egress policy, or with mounted service-account tokens / metadata access inside the guest.
- **Mitigations:** Adopt microVM-style per-job hardware virtualization; enforce egress at the hypervisor with default-destroy on first violation; hardcode a floor that blocks cloud metadata, private ranges, and loopback; strip service-account tokens from the guest pod; mint short-lived identity per use or proxy the authenticated call at the supervisor; run recurring adversarial audits against the sandbox and pin each finding as a regression test.

---

_Source: [https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena](https://www.chainguard.dev/unchained/this-shit-is-hard-how-chainguard-is-sandboxing-athena)_  ·  [← back to index](../README.md)
