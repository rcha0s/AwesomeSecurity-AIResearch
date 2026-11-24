# Highflame's Ramparts scans MCP servers and agent skills for attack paths

**Published:** Nov 24, 2026

> **Takeaway:** Gate skill and MCP changes with a scanner that also detects drift, and keep runtime controls too, since static scans cannot see behavior.

## TL;DR

Ramparts is an open-source Rust scanner that audits MCP servers and agent skill files with YARA rules, LLM analysis and OWASP MCP and skill Top 10 tagging. It re-scans normalized and decoded views to catch hidden text, and flags post-approval changes to server configs, tool definitions and skills. The authors warn it checks static content only.

## Lessons

- Skills are scanned like MCP servers: each skill body is turned into a synthetic MCP prompt and passed through the same analyzers. - _"Each skill body becomes a synthetic MCP prompt that runs through the same analyzers"_
- It fingerprints server configs, tool definitions and skill files against a baseline to catch a swap after approval (a rug pull). - _"content-fingerprints MCP server configs, individual tool definitions, and skill files against a stored baseline; flags any post-approval swap"_
- The project says it reads only static metadata and files, so it needs runtime guardrails alongside it. - _"Ramparts analyzes static metadata, configurations, and skill files."_

---

**Topic:** AI Security  ·  **Domain:** MCP, Tools & Skills  
**Source:** [highflame-ai/ramparts](https://github.com/highflame-ai/ramparts)  ·  **Retrieved:** 2026-11-24  
**Scores:** Newness 27 · Novelty 30 · Relevance 60 · Credibility 54 · **Composite 42** _(each 0-100)_  
**Tags:** `mcp`, `skills`, `scanner`, `rug-pull`, `owasp`, `yara`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Devlab mcp-scanner and Snyk Agent Scan already cover MCP and skill scanning; Ramparts adds drift baselines and evasion-resistant rescans.

_Source: [https://github.com/highflame-ai/ramparts](https://github.com/highflame-ai/ramparts)_  ·  [← back to index](../README.md)
