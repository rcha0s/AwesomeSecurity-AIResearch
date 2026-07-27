# 📰 Security & AI Research — Daily Snapshot (2026-07-26)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

42 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md) · [all learnings](LEARNINGS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54)** · _source_ · composite 65.4
  Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.
  → **Do:** (harness) SSRF-guard every host-side fetch in an agent/MCP runtime
- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](https://arxiv.org/abs/2607.17503)** · _source_ · composite 60.22
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.
  → **Do:** (tool) Regression-test your model scanner with PickleBench
- **[Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](https://arxiv.org/abs/2607.13987)** · _source_ · composite 59.85
  When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) — a runtime-only check misses where most of the risk actually lives.
  → **Do:** (tool) Lifecycle-aware skill scanning
- **[A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](https://arxiv.org/abs/2606.27511)** · _source_ · composite 53.8
  In federated training the aggregator is a trust boundary, not a neutral party - protect gradients and test the global model for triggers.
  → **Do:** (takeaway) Treat the FL aggregator as untrusted
- **[QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](https://arxiv.org/abs/2606.29239)** · _source_ · composite 53.2
  Audit models at deployment precision, not the precision you were handed - some backdoors only exist after you quantize.
  → **Do:** (takeaway) Treat quantization as part of the model supply chain

**📈 Emerging trends**

- **agent-security** (🔺 rising) — 11 findings from 11 sources since 2026-02.
- **prompt-injection** (🔺 rising) — 7 findings from 7 sources since 2026-02.
- **model-supply-chain** (🔺 rising) — 5 findings from 5 sources since 2026-06-25.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/)** · _source_ · composite 70.12
  Import-time malware makes --ignore-scripts useless and a valid provenance attestation is not a trust signal when the pipeline itself is hijacked.
  → **Do:** (takeaway) Don't treat provenance/--ignore-scripts as sufficient supply-chain defenses
- **[Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/)** · _Palo Alto Networks Unit 42_ · composite 66.3
  LLM hallucinations are a predictable supply-chain attack surface: attackers pre-register the domains/packages models invent.
  → **Do:** (tool) Enumerate & monitor your brand's hallucinated domains
- **[Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](https://snyk.io/blog/symlinks-are-still-scary/)** · _Snyk Blog_ · composite 59.85
  A symlink committed to a repo can turn an AI coding agent into a write primitive for ~/.ssh/authorized_keys — resolve paths to canonical form and confirm they stay inside the workspace before any read/write.
  → **Do:** (harness) Enforce workspace containment on every agent file operation
- **[GigaWiper: modular destructive malware that fakes ransomware](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/)** · _Microsoft Security Blog_ · composite 59.25
  Wiper malware is consolidating into modular platforms, and 'ransomware' may be undecryptable destruction in disguise — plan recovery accordingly.
  → **Do:** (takeaway) Assume fake-ransomware; harden recovery
- **[TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/)** · _@Unit42_Intel_ · composite 58.65
  Today's AI-assisted commodity malware is sloppy and self-labelling; budget for the version where someone spends ten more minutes prompting.
  → **Do:** (tool) Hunt for LLM residue in malware source and samples
- **[Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)** · _GitHub Advisory Database_ · composite 58.5
  Anything that renders your prompt, status bar or editor title is executing attacker-controlled repository metadata - treat it as a parser, not decoration.
  → **Do:** (skill) Audit renderers for double evaluation of untrusted data

**📈 Emerging trends**

- **supply-chain** (🔺 rising) — 6 findings from 5 sources since 2026-06-30.
- **phishing** (🔺 rising) — 2 findings from 2 sources since 2026-06-30.
- **unit42** (🔺 rising) — 2 findings from 2 sources since 2026-06-30.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything)** · _Simon Willison's Weblog_ · composite 65.25
  Newer ≠ better for YOUR tools: match your harness's tool schemas to what the target model was trained on.
  → **Do:** (harness) Offer model-matched edit tools
- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)** · _@simonw_ · composite 62.25
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous actions.
  → **Do:** (harness) Adopt incident-driven evals + a context-aware permission gate in your scan harness
- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](https://github.com/algal/pi-openai-server-compaction)** · _@kunchenguid_ · composite 62.25
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity — but treat 'it's better' as unproven at…
  → **Do:** (harness) Wire OpenAI server-side compaction into your agent harness
- **[Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)** · _source_ · composite 61.65
  When you hand an agent a durable goal plus strict 'what counts as a real finding' rules, it will plan multi-step tooling and self-filter noise — the rules, not the model alone, are what make the output actionable.
  → **Do:** (harness) Pair a durable goal with explicit reportability criteria
- **[Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor](https://github.com/omnigent-ai/omnigent)** · _omnigent-ai/omnigent_ · composite 57.1
  The 'meta-harness' is emerging as an abstraction layer above individual coding agents — orchestrate many, swap freely, enforce policy centrally.
  → **Do:** (harness) Consider a meta-harness for multi-agent work

**📈 Emerging trends**

- **agents** (🔺 rising) — 7 findings from 6 sources since 2026-05.
- **evals** (🔺 rising) — 7 findings from 7 sources since 2026-05.
- **harness** (🔺 rising) — 6 findings from 6 sources since 2026-05.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurityResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-07-26.</sub>
