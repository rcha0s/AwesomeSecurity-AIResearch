# NVIDIA OpenShell runs coding agents in kernel-enforced sandboxes under YAML policy

**Published:** Oct 27, 2026

> **Takeaway:** A declarative, kernel-level sandbox for coding agents now exists as an open-source option; compare its policy model before writing your own.

## TL;DR

NVIDIA OpenShell is an open-source runtime (about 20,600 GitHub stars; v0.1.6 on 2026-10-27, the version of the docs read) that runs agents such as Claude Code, Codex, OpenCode and GitHub Copilot CLI in sandboxes. Landlock restricts files, seccomp and an unprivileged identity block escalation, network egress is allow-listed and hot-reloadable, and provider credentials are resolved from placeholders only at authorized endpoints.

## Lessons

- Filesystem and process limits are fixed at sandbox creation, while network policy can change at runtime. - _"Filesystem restrictions (Landlock) confine access to declared paths only."_
- Egress is deny-by-default, which is the control that stops exfiltration by a compromised agent. - _"Network policies allow only approved destinations; other outbound traffic is denied."_

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [docs.nvidia.com](https://docs.nvidia.com/openshell/latest/about/overview.html)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 19 · Novelty 60 · Relevance 85 · Credibility 50 · **Composite 56** _(each 0-100)_  
**Tags:** `sandbox`, `coding-agents`, `landlock`, `seccomp`, `egress-policy`, `nvidia`, `openshell`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Other agent sandboxes (containers, microVMs, Claude Code's own sandbox) isolate similarly; OpenShell's difference is the declarative policy with hot-reloadable network rules and credential placeholders.

_Source: [https://docs.nvidia.com/openshell/latest/about/overview.html](https://docs.nvidia.com/openshell/latest/about/overview.html)_  ·  [← back to index](../README.md)
