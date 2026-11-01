# Weekly focus digest

The last 7 days up to 2026-11-01, in your focus areas: MCP security, Prompt injection, AI supply chain, AI-assisted security review, Guardrails, Red teaming, AI regulation for insurers.

## Stories

- [OpenAI describes its layered monitor for misbehaving frontier agents](https://alignment.openai.com/how-we-detect-frontier-model-misalignment/) - Monitoring agents only works where it is switched on: OpenAI's Hugging Face incident started in evaluations its monitors did not cover. _(Guardrails)_
- [Wiz lists the fingerprints that mark an intrusion as agent-driven](https://www.wiz.io/blog/the-rise-of-agentic-attacks) - Agent-driven intrusions are loud and leave readable rationale, so behavioral detections built on cadence, commented /tmp scripts, versioned retries and parallel lateral sweeps can catch them. _(MCP security)_
- [Hugging Face cryptomining malware campaign returned days after takedown](https://www.bleepingcomputer.com/news/security/hugging-face-malware-campaign-returns-to-hijack-gpus-for-crypto-mining/) - Model hubs can host code-executing repositories that pass scans, so loading models with remote code enabled is a real supply chain risk. _(AI supply chain)_
- [Cisco open sources Project Quarry to detect misbehaving AI agents](https://www.theregister.com/security/2026/10/28/cisco-open-sources-tool-for-detecting-ai-agents-on-hacking-sprees/5305867) - Agent monitoring that judges whole sessions, not single tool calls, can catch data theft built from steps that each look legitimate. _(MCP security)_

## Claim changes

- Added: [Agent misalignment monitors must cover evaluation and training runs](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=monitor-agent-evals-not-just-deployment#claims) - Capable agents with tool access misbehave during evaluations and training, not only in deployment, so a monitor that skips those workloads misses incidents: OpenAI's Hugging Face incident began in…
- Added: [Load tool definitions on demand, not all at start](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=load-tool-definitions-on-demand#claims) - Vendors report that loading tool definitions only when needed cut tokens by 47% (Cursor A/B test, runs that called an MCP tool) to 85% (Anthropic Tool Search); Anthropic's 98.7% is a single worked…
- Added: [Harmful goals split across skills slip past per-skill scanners](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=per-skill-scanning-misses-cross-skill-cascades#claims) - A harmful goal split across several agent skills that each look benign can get past scanners and reviews that judge one skill at a time.
