# Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions

**Topic:** AI Security  ·  **Domain:** MCP Server Scanning & Defender Tooling  
**Source:** [source](https://github.com/cisco-ai-defense/mcp-scanner)  ·  **Published:** Aug 9, 2026  ·  **Retrieved:** 2026-08-10  
**Scores:** 🆕 Newness 46 · ✨ Novelty 65 · 🎯 Relevance 82 · 🏛️ Credibility 55 · **Composite 63.85**  
**Tags:** `mcp`, `mcp-scanner`, `tool-poisoning`, `llm-as-judge`, `yara`, `supply-chain`, `static-analysis`  
**Verification:** ✓ independently verified · closest prior art: Complements ToolHive MCP SSRF and 'Agent skill security is a lifecycle problem' (SkillSec-Eval) entries in the pool: both frame skill/tool metadata as needing lifecycle scanning, and this is the concrete tool that operationalizes it.

> **Takeaway:** Treat every MCP surface - tools, prompts, resources, and server instructions - as a distinct attack surface with its own scanner; a single engine misses cases each of YARA, LLM-judge, and dataflow catches.

## TL;DR

_The gist, not every detail - read the [full source](https://github.com/cisco-ai-defense/mcp-scanner) for the complete write-up._

mcp-scanner is a Python CLI/SDK that scans MCP servers for security issues across four surfaces - tools, prompts, resources, and the server's `InitializeResult` instructions - using three interchangeable engines: YARA rules, an LLM-as-judge, and Cisco's inspect API. It adds pip-audit-based vulnerable-dependency scanning, VirusTotal hash lookups for bundled binaries, and Docker-sandboxed PyPI/npm package downloads for behavioral analysis. Scanning `InitializeResult` instructions is called out as its own subcommand because those instructions are a first-class prompt-injection surface.

## What to learn

- MCP `InitializeResult` server instructions are their own scan target, not incidental metadata: they are consumed by the model and can carry prompt injection, tool poisoning, or misleading guidance. - _"Server instructions provide usage guidelines, security notes, and configuration details in the MCP `InitializeResult`. Scanning instructions helps detect prompt injection, tool poisoning, and misleading guidance."_ ✅
- Behavioral scanning that compares an MCP tool's docstring claim against its actual dataflow is the way to catch tool poisoning; string-match YARA rules are complementary but not sufficient. - _"The Behavioral Analyzer performs advanced static analysis of MCP server source code to detect behavioral mismatches between docstring claims and actual implementation. It uses LLM-powered alignment checking combined with cross-file dataflow tracking."_ ✅
- Layered engines matter: the scanner combines three independent detectors so a defender is not betting on one signal. - _"The MCP Scanner combines Cisco AI Defense inspect API, YARA rules and LLM-as-a-judge to detect malicious MCP tools."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** MCP tool descriptions, prompt templates, resource contents, and `InitializeResult` instructions all flow into the model context and can carry prompt injection or tool poisoning. Without dedicated scanning, a hostile or compromised MCP server gets admitted to an agent's tool set through normal `mcp add` flows, and behavioral mismatches between docstrings and implementations are invisible to human reviewers scanning READMEs.
- **Conditions:** An organization runs agents that connect to external or third-party MCP servers; scanning is not gated on admission; and human review is limited to the tool README rather than the tool's dataflow.
- **Mitigations:** Run mcp-scanner across all four MCP surfaces (tools, prompts, resources, instructions) at admission; add pip-audit and VirusTotal scans for bundled dependencies; keep pypi-scan/npm-scan sandboxed via Docker (default) and treat behavioral analyzer output as blocking for tools that mutate state.

---

_Source: [https://github.com/cisco-ai-defense/mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner)_  ·  [← back to index](../README.md)
