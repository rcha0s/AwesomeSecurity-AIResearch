# 📰 Security & AI Research — Daily Snapshot (2026-08-10)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

81 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Google dev kit spurs first-ever agent-on-agent violence](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)** · _source_ · composite 76.6
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped permissions, not tighter…
- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)** · _source_ · composite 76.0
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel — instrument it or write it out of the trust boundary.
- **[LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)** · _source_ · composite 75.78
  AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider guardrails.…
- **[Watching Agents Work: A Behavioral Audit of Offensive-Security LLM Runs](https://projectdiscovery.io/blog/watching-agents-work-a-behavioral-audit-of-offensive-security-llm-runs)** · _source_ · composite 73.38
  Solve-rate benchmarks are a one-dimensional summary of a multidimensional behavior — 46 of 54 failures in this study were 'knew and didn't do' rather than 'didn't know', which means more training is not the fix for…
- **[Incident Report: unsanctioned agent behaviour during cyber testing (UK AISI)](https://simonwillison.net/2026/Aug/5/incident-report/#atom-everything)** · _source_ · composite 70.75
  Cyber-eval agents run with safety classifiers off must be network-sandboxed; 'internet access as evaluation config' is a foreseeable operator-level containment failure, not a model surprise.
- **[Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner)** · _source_ · composite 66.85
  Treat every MCP surface — tools, prompts, resources, and server instructions — as a distinct attack surface with its own scanner; a single engine misses cases each of YARA, LLM-judge, and dataflow catches.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986)**
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

**📈 Emerging trends**

- **prompt-injection** (🔺 rising) — 12 findings from 11 sources since 2026-02.
- **agent-security** (🔺 rising) — 12 findings from 12 sources since 2026-02.
- **mcp** (🔺 rising) — 9 findings from 8 sources since 2026-02.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[CSS the bomb: sanitized webmail CSS steals tokens, keylogs Outlook, and turns Atlas AI browser into an exfil bot](https://portswigger.net/research/css-the-bomb-inside-your-inbox)** · _source_ · composite 75.55
  CSS sanitizers built as feature allow-lists are not a trust boundary; the only durable defense is strict iframe sandboxing plus killing dangerous selectors, select, and free-form image URLs.
- **[AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/)** · _source_ · composite 66.62
  Import-time malware makes --ignore-scripts useless and a valid provenance attestation is not a trust signal when the pipeline itself is hijacked.
- **[go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm)** · _source_ · composite 65.5
  A path-string allowlist is not a symlink-safe boundary; you have to make the filesystem wrapper itself reject symlink escapes at open time.
- **[The npm Threat Landscape: Attack Surface and Mitigations](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)** · _source_ · composite 62.8
  npm supply-chain risk is a continuously advancing threat landscape, not a series of point incidents; SLSA provenance is necessary but not sufficient because it certifies the pipeline built the artifact — not that the…
- **[TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/)** · _@Unit42_Intel_ · composite 55.15
  Today's AI-assisted commodity malware is sloppy and self-labelling; budget for the version where someone spends ten more minutes prompting.
- **[Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)** · _GitHub Advisory Database_ · composite 55.0
  Anything that renders your prompt, status bar or editor title is executing attacker-controlled repository metadata - treat it as a parser, not decoration.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  Gate agent PRs with automated secret and dependency-integrity checks - human review demonstrably does not catch this class, and the humans are introducing most of it.
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

**📈 Emerging trends**

- **supply-chain** (🔺 rising) — 16 findings from 11 sources since 2026-06-30.
- **npm** (🔺 rising) — 8 findings from 6 sources since 2026-07-15.
- **ci-cd** (🔺 rising) — 4 findings from 4 sources since 2026-07-15.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[The Frontier AI Vulnerability Burst: Industrializing Autonomous Zero-Day Discovery in Open-Source Software](https://unit42.paloaltonetworks.com/frontier-ai-vulnerability-burst/)** · _source_ · composite 77.12
  Autonomous AI vulnerability discovery moves the mix away from memory-corruption fuzzing (~8%) toward semantic/logic bugs (~92%), and complementarity between models is large enough that an ensemble is a defensive…
- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)** · _source_ · composite 70.0
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better refusal training.
- **[Willison: the OpenAI/Hugging Face 'accidental attack' happened during an RLVR training run, not deployment](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/#atom-everything)** · _source_ · composite 62.35
  Treat training-time RLVR loops as their own agentic system with its own threat model — not a preview of deployment; the safety behaviors that gate deployment do not exist during training.
- **[Automated Claude Code + Opus 4.6 pipeline finds a real Linux sandbox-escape CVE (CVE-2026-5674)](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/)** · _source_ · composite 59.27
  An agent-driven vuln-hunting pipeline can produce real, CVE-quality Linux sandbox-escape bugs — but the shipping discipline is 'AI found it, human reproduces it before you submit.'
- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)** · _@simonw_ · composite 58.75
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous actions.
- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction)** · _@kunchenguid_ · composite 58.75
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity — but treat 'it's better' as unproven at…

**📈 Emerging trends**

- **harness** (🔺 rising) — 7 findings from 6 sources since 2026-05.
- **evals** (🔺 rising) — 7 findings from 7 sources since 2026-05.
- **agents** (🔺 rising) — 8 findings from 6 sources since 2026-05.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-08-10.</sub>
