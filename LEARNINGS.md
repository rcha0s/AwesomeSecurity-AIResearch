# Learnings digest

> Ranked, source-cited takeaways across Security and AI. Updated 2026-07-26.

## 📈 Ranked findings

### AsyncAPI npm compromise: import-time payload defeats --ignore-scripts · `70.38`
- **Topic:** product-security / Supply Chain & Dependencies
- **Takeaway:** Import-time malware makes --ignore-scripts useless and a valid provenance attestation is not a trust signal when the pipeline itself is hijacked.
- **Action (takeaway):** Don't treat provenance/--ignore-scripts as sufficient supply-chain defenses — Add a CI check that diffs a dependency's published tarball against its tagged source before promotion, and audit any pull_request_target workflow that checks out and runs untrusted PR code with access to secrets.
- **Source:** [source](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/)

### Phantom Squatting: attackers register the domains LLMs hallucinate · `66.55`
- **Topic:** product-security / Supply Chain
- **Takeaway:** LLM hallucinations are a predictable supply-chain attack surface: attackers pre-register the domains/packages models invent.
- **Action (tool):** Enumerate & monitor your brand's hallucinated domains — Query LLMs for your brand's URLs/packages at scale, then pre-register or block-list the hallucinated ones and monitor for adversary registration.
- **Source:** [Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/)

### ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces · `65.65`
- **Topic:** ai-security / MCP & Tools
- **Takeaway:** Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.
- **Action (harness):** SSRF-guard every host-side fetch in an agent/MCP runtime — For any outbound request whose URL derives from a tool/server response, enforce a private-IP dialer deny-list AND a CheckRedirect that re-applies it to each hop; treat `#nosec`/lint suppressions on such sinks as findings to review against the threat model, not settled decisions.
- **Source:** [source](https://github.com/advisories/GHSA-pr64-jmmf-jp54)

### Better Models, Worse Tools: SOTA models regress on non-native tool schemas · `65.5`
- **Topic:** ai-research / Tooling & Infrastructure
- **Takeaway:** Newer ≠ better for YOUR tools: match your harness's tool schemas to what the target model was trained on.
- **Action (harness):** Offer model-matched edit tools — In a multi-model harness, provide the edit-tool format each model was trained on (Claude str-replace, OpenAI apply_patch) instead of one custom schema, and validate/repair malformed tool calls.
- **Source:** [Simon Willison's Weblog](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/#atom-everything)

### How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier · `62.5`
- **Topic:** ai-research / coding-agent harness design (first-party Anthropic practices)
- **Takeaway:** Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous actions.
- **Action (harness):** Adopt incident-driven evals + a context-aware permission gate in your scan harness — Two concrete moves for the scan/analysis harness: (1) When a scan produces a bad or hallucinated finding, capture that exact input and expected output as a regression eval case so future runs are checked against it, mirroring 'take the PRs that caused the incident and add them to an eval set.' (2) For any auto-run tooling (PR creation, pushes), gate risky actions behind a small classifier/rule step that reads both the requested action and the surrounding task context rather than a static allowlist, and inject any credentials via env/proxy so they are usable-but-not-readable by the agent. Also audit the analyzer system prompt to remove redundant examples and convert blanket 'always/never' rules into short WHY-reasoning.
- **Source:** [@simonw](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)

### Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi) · `62.5`
- **Topic:** ai-research / Harness / context management
- **Takeaway:** If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity — but treat 'it's better' as unproven at equal token budget…
- **Action (harness):** Wire OpenAI server-side compaction into your agent harness — For openai/* models, on your compaction event call POST /v1/responses with the full history plus a trailing compaction_trigger, mirroring your normal request's reasoning/tool/text config; store the returned opaque `compaction` item and replay it only for compatible OpenAI turns. Set store:true and use previous_response_id for between-compaction continuity, and generate a portable text summary in parallel so forks/exports/other models keep working. Budget for the cost: this policy emitted ~4.58x compaction output tokens and a ~29% larger billed context, so gate it behind a config/threshold and measure recall-per-token on your own tasks before trusting it.
- **Source:** [@kunchenguid](https://github.com/algal/pi-openai-server-compaction)

### Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day · `61.9`
- **Topic:** ai-research / Agents & Harnesses
- **Takeaway:** When you hand an agent a durable goal plus strict 'what counts as a real finding' rules, it will plan multi-step tooling and self-filter noise — the rules, not the model alone, are what make the output actionable.
- **Action (harness):** Pair a durable goal with explicit reportability criteria — For autonomous security/analysis agents, encode the objective so it persists across turns/compactions AND specify hard validity rules (what is reachable, in-scope, and reportable) inside the goal — this is what suppresses high-confidence noise and lets the agent self-reject weak findings.
- **Source:** [source](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)

### ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs · `60.47`
- **Topic:** ai-security / Model Supply Chain
- **Takeaway:** A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.
- **Action (tool):** Regression-test your model scanner with PickleBench — If PickleBench is released, run your model-scanning gate against injected variants of your own known-good models to measure real evasion rate before relying on it in CI. Independent of the paper: where the format allows, migrate ingestion to safetensors and make pickle loading an explicitly sandboxed, opt-in path.
- **Source:** [source](https://arxiv.org/abs/2607.17503)

### Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval) · `60.1`
- **Topic:** ai-security / Skill Supply Chain
- **Takeaway:** When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) — a runtime-only check misses where most of the risk actually lives.
- **Action (tool):** Lifecycle-aware skill scanning — Extend a skill/marketplace scanner beyond runtime: check repository-admission provenance, semantic-retrieval poisoning (does a crafted description win retrieval?), planner-selection hijacking, and skill-evolution drift between approved and current versions.
- **Source:** [source](https://arxiv.org/abs/2607.13987)

### Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval') · `60.1`
- **Topic:** product-security / AI coding assistant sandbox escape / path traversal
- **Takeaway:** A symlink committed to a repo can turn an AI coding agent into a write primitive for ~/.ssh/authorized_keys — resolve paths to canonical form and confirm they stay inside the workspace before any read/write.
- **Action (harness):** Enforce workspace containment on every agent file operation — In the agent harness, before any Read/Write/Edit, resolve the path to its canonical location (realpath / openat2 with RESOLVE_BENEATH or RESOLVE_NO_SYMLINKS on Linux) and reject anything outside the workspace root. Surface the RESOLVED absolute target in approval prompts, not the in-repo filename, so a write to ~/.ssh/authorized_keys looks alarming. After cloning untrusted repos, scan with `find . -type l` or `git ls-files -s | grep ^120000` and quarantine symlinks pointing outside the tree.
- **Source:** [Snyk Blog](https://snyk.io/blog/symlinks-are-still-scary/)

### GigaWiper: modular destructive malware that fakes ransomware · `59.5`
- **Topic:** product-security / Malware & Wipers
- **Takeaway:** Wiper malware is consolidating into modular platforms, and 'ransomware' may be undecryptable destruction in disguise — plan recovery accordingly.
- **Action (takeaway):** Assume fake-ransomware; harden recovery — Treat ransomware incidents as potentially unrecoverable: prioritize offline/immutable backups and rapid detection of raw disk writes / partition-metadata tampering.
- **Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/)

### Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037) · `58.1`
- **Topic:** product-security / Application Security
- **Takeaway:** A minimal 'just null-terminate the buffer' patch can hide a pre-auth RCE — diff patches carefully, and treat missing null-termination next to attacker-controlled heap data as exploitable, not cosmetic.
- **Action (takeaway):** Prioritize edge-appliance patches and read the diff, not the CVE title — When a vendor ships a one-line string-handling fix on an internet-facing appliance, assume memory-corruption impact until proven otherwise and patch on the critical track; missing null-termination adjacent to attacker-sprayable heap data is an RCE primitive, not a hardening nit.
- **Source:** [source](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/)

### Omnigent: an open-source meta-harness over Claude Code, Codex, Cursor · `57.35`
- **Topic:** ai-research / Meta-Harness
- **Takeaway:** The 'meta-harness' is emerging as an abstraction layer above individual coding agents — orchestrate many, swap freely, enforce policy centrally.
- **Action (harness):** Consider a meta-harness for multi-agent work — Evaluate an orchestration layer (like Omnigent) when running multiple coding agents, so policy/sandboxing/routing live in one place instead of per-agent.
- **Source:** [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent)

### SourTrade: browser reassembles a Bun-based executable from split parts, defeating hash-based detection with per-session builds · `56.95`
- **Topic:** product-security / browser-delivered malware / malvertising
- **Takeaway:** Client-side payload assembly (split parts + per-session hashing) breaks hash-based detection, so hunt the whole delivery chain and behavioral signals, not the final-file signature.
- **Action (takeaway):** Detect browser-assembled malware by chain, not by final-file hash — Do not rely on hashing the downloaded executable: SourTrade rotates a per-session AES-CTR seed so every build differs. Instead correlate the delivery chain: ad/malvertising referral -> cloaked landing page -> ServiceWorker registration at /sw.js -> a /config request returning Base64 PE headers and a .bun bytecode section -> a secondary-domain fetch of a legitimate Bun runtime -> a same-origin worker download with Content-Disposition attachment. Flag pages that register ServiceWorkers and then trigger attachment downloads via a hidden iframe, and alert on standalone Bun executables assembled from downloaded parts. Block the published domains/hashes as IOCs but treat them as low-shelf-life. User-facing control: install trading/wallet software only from the vendor's own site, never from an ad.
- **Source:** [@TheHackersNews](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html)


---

<sub>Generated by scripts/generate_skills.py on 2026-07-26.</sub>
