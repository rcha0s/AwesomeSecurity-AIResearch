# sinewaveai/agent-security-scanner-mcp

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://github.com/sinewaveai/agent-security-scanner-mcp)  ·  **Published:** Aug 9, 2026  ·  **Retrieved:** 2026-08-14  
**Scores:** 🆕 Newness 46 · ✨ Novelty 62 · 🎯 Relevance 75 · 🏛️ Credibility 55 · **Composite 60.85**  
**Tags:** `package-hallucination`, `mcp`, `ai-generated-code`, `sbom`, `coding-agent`  
**Verification:** ✓ independently verified · closest prior art: Overlaps with npm audit (dependency CVEs) but explicitly positioned as complementary rather than replacement. Package-hallucination detection echoes findings around slopsquatting; MCP tool-poisoning rules echo the Invariant Labs tool-poisoning taxonomy.

> **Takeaway:** Package-hallucination detection is the piece normal SAST tools miss: AI-generated code invents plausible dependency names that attackers can then squat. Verifying every AI-suggested import against a canonical name set closes the gap between generation and the install step.

## TL;DR

_The gist, not every detail - read the [full source](https://github.com/sinewaveai/agent-security-scanner-mcp) for the complete write-up._

Multi-purpose scanner exposed both as a CLI and an MCP server for AI coding agents. Combines rule-based SAST/taint analysis over generated code, MCP-server auditing (tool poisoning, name spoofing, env exfil), prompt-injection and action-safety checks, and package-hallucination detection against 4.3M+ package names across seven ecosystems. Also emits CycloneDX SBOMs and runs OSV.dev CVE checks.

## What to learn

- AI-generated code introduces categories of risk that traditional SAST does not cover: hallucinated dependency names, MCP tool-description injection, unsafe agent actions, and prompt-injection surfaces in ingested content. - _"It complements npm audit by catching AI-specific risks: hallucinated packages, prompt injection, MCP tool poisoning, unsafe agent actions, and vulnerable generated code."_ ✅
- MCP tool descriptions are themselves prompt-injection surfaces. Imperative language in a tool description is a signal that the MCP author (or someone who edited the manifest) is trying to steer the calling LLM. - _""rule": "mcp.description-injection",
      "severity": "ERROR",
      "message": "Tool description contains imperative language directed at the LLM.""_ ✅
- Package-hallucination detection needs a broad, cross-ecosystem name set to be useful. Checking against a curated 4.3M+ package corpus covers the ecosystems AI coding agents actually emit imports for. - _"Package hallucination detection checks 4.3M+ package names across npm, PyPI, RubyGems, crates.io, pub.dev, CPAN, and raku.land."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** AI coding agents produce vulnerable generated code, invent plausible-but-nonexistent package names that attackers pre-squat, install untrusted MCP servers whose tool descriptions contain imperative injection payloads or spoof well-known tool names, and execute shell/file/network actions that a human developer would have caught. Traditional SAST and dependency scanners miss most of that.
- **Conditions:** Codebase is authored or heavily edited by an AI coding agent (Claude Code, Cursor, Windsurf, Cline, OpenCode, etc.); agent installs its own MCP servers; agent proposes new dependencies as part of edits; agent has permission to run shell/file/network actions without a scanner-in-the-loop.
- **Mitigations:** Install the scanner as an MCP tool inside the agent client so the agent is prompted to run it; gate PRs on scan-diff results; verify every AI-suggested import via check-package/scan-packages against the 4.3M-name corpus before install; run scan-mcp on every new MCP server before adding it; generate an SBOM per release and cross-check with OSV.dev.

---

_Source: [https://github.com/sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp)_  ·  [← back to index](../README.md)
