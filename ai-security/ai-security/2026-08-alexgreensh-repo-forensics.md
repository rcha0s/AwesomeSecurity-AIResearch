# alexgreensh/repo-forensics

**Published:** Aug 8, 2026

> **Takeaway:** There is a small but real category of local, hook-driven vetting tools for AI-agent extensions; borrow the pattern of pairing an offline scanner with signed rule feeds and PreToolUse blocking rather than trusting hub-side review.

## TL;DR

Offline, zero-dependency Python scanner that vets AI-agent repos, skills, MCP servers, and plugins before they are installed. Runs 27 scanners in parallel, correlates findings via 41 rules, ships with 190+ package IOCs and an Ed25519-signed daily rule feed, and integrates with Claude Code / Codex CLI / OpenClaw via PreToolUse, PostToolUse, and SessionStart hooks that block known-malicious packages and audit cloned/updated code.

## What to learn

- Agent-ecosystem code (skills, MCP servers, plugins) is installed without vetting and inherits full user credentials at runtime. - _"You find something useful, you install it. It runs with your credentials, your file access, your session context. If it's designed to exfiltrate data, it does it quietly while you're using it for something else entirely."_
- Practical AI-agent vetting couples an offline scanner with PreToolUse blocking of known-malicious packages plus a full audit on install/update. - _"PreToolUse | Before any `npm install`, `pip install`, `uv add`, `bun install`, `pnpm add`, shell command | Blocks known-malicious packages before execution. IOC-only, <10ms."_
- A single scanner finding is often ambiguous; correlation across scanners is what surfaces compound threats like deferred payload loading or data exfiltration. - _"A dynamic import paired with a network fetch becomes a deferred payload loading finding. An environment variable read combined with an outbound POST becomes a data exfiltration finding."_
- Rule-feed refresh is treated as a freshness layer over an offline-first core, using Ed25519 signing and rollback protection rather than a cloud API call at scan time. - _"Those rule packs refresh daily through an Ed25519-signed feed. New behavioral detection rules reach every install without a code release or reinstall. The feed is cryptographically verified on every load, rollback-protected with a version floor, and degrades safely to the shipped packs if unreachable."_

## Threat · Conditions · Mitigations

- **Threat:** Malicious AI-agent skills, MCP servers, and npm/pip packages install with user credentials and can exfiltrate secrets or persist through session hooks; supply-chain worms like Shai-Hulud, IRONWORM, and SANDWORM_MODE actively target this surface.
- **Conditions:** User installs untrusted agent extension or third-party package; agent host (Claude Code / Codex / Cursor / OpenClaw) runs install/update commands; no PreToolUse or admission gate is in place.
- **Mitigations:** Run an offline scanner (repo-forensics or equivalent) as a PreToolUse hook to block known-malicious packages; do full 27-scanner audits on PostToolUse; treat scanner rule feeds as signed and rollback-protected; export SARIF to GitHub Security tab for CI gating.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://github.com/alexgreensh/repo-forensics)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 18 · Novelty 62 · Relevance 82 · Credibility 55 · **Composite 55.95**  
**Tags:** `mcp`, `supply-chain`, `scanner`, `hooks`, `sarif`, `prompt-injection`, `yara`  
**Verification:** ✓ independently verified · closest prior art: Sits alongside mcp-scan (cloud-uploaded), NVIDIA SkillSpector (skill files only), and generic secrets scanners (Gitleaks, TruffleHog); the differentiator claimed is offline operation with correlation, live IOC + CISA KEV enrichment, and named-campaign IOCs.

_Source: [https://github.com/alexgreensh/repo-forensics](https://github.com/alexgreensh/repo-forensics)_  ·  [← back to index](../README.md)
