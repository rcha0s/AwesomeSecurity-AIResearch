# Weekly focus digest

The last 7 days up to 2026-10-29, in your focus areas: MCP security, Prompt injection, AI supply chain, AI-assisted security review, Guardrails, Red teaming, AI regulation for insurers.

## Stories

- [obsidian-tc tool server lets any valid token delete any configured vault](https://github.com/advisories/GHSA-84c9-qqpq-2pq5) - Multi-tenant tool servers must enforce the caller's tenant once at dispatch and never trust a caller-supplied vault or workspace parameter. _(MCP security)_
- [Anthropic's red team found Claude reached undergraduate-level CTF skill](https://www.anthropic.com/research/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team) - When estimating offensive AI capability, test with an attack toolkit and not only the bare model, though these March 2025 figures are now well out of date. _(Red teaming)_
- [obsidian-tc MCP server lacks Origin checks, letting web pages read its vault](https://github.com/advisories/GHSA-pqh8-4pj7-32xx) - Local MCP servers on loopback need Origin and Host validation, or any web page can drive them. _(MCP security)_
- [Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification) - If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope. _(AI-assisted security review)_
- [A backdoored open model made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned) - Clean benchmarks do not show whether downloaded open weights are backdoored, so contain what the agent's tool calls can read and reach. _(AI supply chain)_

## Claim changes

- Added: [Load tool definitions on demand, not all at start](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=load-tool-definitions-on-demand#claims) - Vendors report that loading tool definitions only when needed cut tokens by 47% (Cursor A/B test, runs that called an MCP tool) to 85% (Anthropic Tool Search); Anthropic's 98.7% is a single worked…
- Added: [Harmful goals split across skills slip past per-skill scanners](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=per-skill-scanning-misses-cross-skill-cascades#claims) - A harmful goal split across several agent skills that each look benign can get past scanners and reviews that judge one skill at a time.
- Added: [A guardrail weaker than its target can be bypassed](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=input-guardrail-weaker-than-target-is-bypassable#claims) - An input-screening guardrail model that is less capable than the model it protects (less reasoning effort, no tools) can be bypassed by payloads hidden in plain prose that only the stronger…
