# highflame-ai/ramparts

**Topic:** AI Security  ·  **Domain:** MCP & Skill Scanning  
**Source:** [source](https://github.com/highflame-ai/ramparts)  ·  **Published:** Aug 8, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 46 · ✨ Novelty 62 · 🎯 Relevance 82 · 🏛️ Credibility 55 · **Composite 62.95**  
**Tags:** `mcp`, `skill-scanning`, `sarif`, `yara`, `owasp-mcp-top-10`  
**Verification:** ✓ independently verified · closest prior art: OWASP MCP Top 10 tagging; NVIDIA SkillSpector YARA rules (adapted); overlaps with Snyk Agent Scan, Cisco AI Defense MCP Scanner, and Invariant Labs MCP-Scan.

> **Takeaway:** The MCP-scanner ecosystem is converging on 'MCP + skills' as a single scanning target rather than treating them as separate problems. If you scan MCP servers today, extend the same detectors to skill bundles - the trust surface is symmetric.

## TL;DR

_The gist, not every detail - read the [full source](https://github.com/highflame-ai/ramparts) for the complete write-up._

Ramparts (Rust CLI, ~96 stars) is a scanner that applies one YARA + LLM-analysis + OWASP MCP Top 10 pipeline to two agent-trust surfaces at once: MCP servers reached over HTTP/SSE/stdio, and skill files on disk (Claude Code slash commands, agentskills.io bundles, and Cursor/Codex/Windsurf/Gemini equivalents). It bundles 35+ static rules, walks agentskills.io bundles' sibling scripts/ and references/ directories, checks CVEs via OSV.dev for npx/uvx-launched stdio servers, and emits SARIF for GitHub/GitLab/Azure DevOps code-scanning. It also validates agentskills.io spec fields: a directory-vs-name mismatch surfaces as a HIGH-severity deception finding.

## What to learn

- MCP tool descriptions and skill markdown deliver untrusted instructions into the same agent loop, so a single scanning pipeline can cover both. - _"Ramparts scans the two surfaces an AI agent trusts most: the **MCP servers** it talks to over the network, and the **skill files** it loads from disk and executes by name. Both deliver untrusted instructions and tool grants into the agent's loop; ramparts applies the same security pipeline (YARA, LLM analysis, OWASP MCP Top 10 tagging) to both."_ ✅
- Skill files carry MCP-style risks plus their own: overbroad allowed-tools grants, @-path references that inline credentials into prompts, name-collision shadowing in the agent's router, and bundled executable scripts. - _"Agent skills carry the same risk profile (untrusted instructions an agent may follow) plus their own twists: skill-file `allowed-tools` grants that hand out unrestricted `Bash`, sensitive `@<path>` references that inline credentials into prompt context, name collisions that let one skill shadow another in the agent's router, and bundled scripts that ship arbitrary executable code."_ ✅
- The scanner treats a mismatch between the SKILL.md declared name and its parent directory as a deception finding, since agentskills.io requires them to match. - _"[HIGH] AgentskillsNameMismatch [OWASP: MCP02]
        SKILL.md declares `name: evil-skill` but its parent directory is `my-skill/`.
        agentskills.io requires the name to match the parent directory; the mismatch may
        indicate a deceptively-named bundle."_ ✅
- The tool acknowledges static-metadata scanning is insufficient on its own and must be layered with runtime guardrails. - _"Ramparts analyzes static metadata, configurations, and skill files. For comprehensive security, combine with runtime MCP guardrails and adopt a layered security approach. The MCP+skills threat landscape is rapidly evolving, and ramparts is not perfect - inaccuracies are inevitable."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Untrusted MCP servers or skill bundles feed instructions and executable code into an agent's loop. A skill directory can be swapped under a deceptive name, or a bundle's scripts/ directory can ship a reverse shell or credential-harvester that runs when the agent invokes the skill.
- **Conditions:** Team installs third-party skill bundles or connects to third-party MCP servers without gating changes through code-scanning. CI does not consume SARIF output from any MCP/skill scanner. Static metadata scanning is treated as sufficient without runtime guardrails.
- **Mitigations:** Add a Ramparts (or equivalent) scan to CI for any repo that ships skills or MCP configs, and consume SARIF in code-scanning. Validate agentskills.io spec fields, especially the SKILL.md name vs. parent directory. Combine with runtime MCP guardrails; do not rely on static-metadata scanning alone. Version-pin skill bundles and MCP server versions so untracked metadata changes fail the gate.

---

_Source: [https://github.com/highflame-ai/ramparts](https://github.com/highflame-ai/ramparts)_  ·  [← back to index](../README.md)
