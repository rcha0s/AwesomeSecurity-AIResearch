# affaan-m/agentshield

**Published:** Aug 9, 2026

> **Takeaway:** For agent-config SAST to stay useful, findings need a runtimeConfidence dimension separating what is actually enabled from what a repo merely ships as an example. Blanket rules produce noise; source-aware reclassification is the accuracy lever.

## TL;DR

Static scanner for Claude Code and adjacent agent-harness configs. 102 rules across secrets, permissions, hooks, MCP servers, and agent config, graded A-F with a 0-100 score. Notably distinguishes active-runtime findings from template-example, docs-example, plugin-cache, plugin-manifest, and hook-code sources with a runtimeConfidence field, and weights scores accordingly so a template catalog cannot dominate the grade.

## What to learn

- Agent-config scanners must distinguish active runtime configuration from templates, docs, and plugin caches. Without a runtimeConfidence dimension, a single risky catalog file scores like dozens of enabled servers. - _"JSON, markdown, terminal, and HTML outputs now expose source context via `runtimeConfidence: active-runtime | project-local-optional | template-example | docs-example | plugin-cache | plugin-manifest | hook-code`."_
- Score weighting must reflect that same distinction. Non-secret template findings at 0.25x with a per-file cap keeps a catalog from dominating the grade; real secrets stay at full weight regardless of source kind. - _"Non-secret `template-example` MCP findings are score-weighted at `0.25x`, and one template file is capped at `10` deduction points per score category so a single MCP catalog cannot score like dozens of enabled servers."_
- Hook injection is a real class of finding to scan for at agent-harness install time: shell variable interpolation, silent-failure patterns, exfil via curl in hooks, and SessionStart hooks that download remote code are all in the rule set. - _"| Command injection | `${file}` interpolation in shell commands - attacker-controlled filenames become code |"_

## Threat · Conditions · Mitigations

- **Threat:** Agent-harness configuration files (settings.json, CLAUDE.md, MCP configs, hooks) are a large, under-scanned attack surface: hardcoded provider keys, Bash(*) allow rules, hook scripts that curl-and-exec remote URLs, MCP servers pinned via npx -y, and CLAUDE.md files with auto-run or hidden-instruction directives that behave as persistent prompt injection.
- **Conditions:** Developer installs community skills, community MCP servers, or shares a .claude/ directory in a repo; harness config is not routinely audited; hooks fire on tool use without a review gate; secrets get committed inline rather than referenced via env vars.
- **Mitigations:** Run AgentShield in CI with JSON output; act on active-runtime findings before template-example ones; enforce deny lists for rm -rf / sudo / chmod 777; replace hardcoded keys with env-var references (auto-fix); prefer scoped Bash allowlists over Bash(*); pin MCP package versions and refuse npx -y auto-install for MCP tools.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://github.com/affaan-m/agentshield)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 65 · Relevance 72 · Credibility 55 · **Composite 54.35**  
**Tags:** `agent-config`, `sast`, `claude-code`, `mcp`, `hooks`, `secrets`, `runtime-confidence`  
**Verification:** ✓ independently verified · closest prior art: Adjacent to Praetorian augustus (LLM red-team) and sinewaveai agent-security-scanner-mcp (repo/package scanner), but scoped specifically to Claude Code / agent-harness configuration files rather than runtime LLM behavior. Ships alongside a false-positive-audit.md workflow.

_Source: [https://github.com/affaan-m/agentshield](https://github.com/affaan-m/agentshield)_  ·  [← back to index](../README.md)
