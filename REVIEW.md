# 🔍 Review Queue

> Findings in the last 31 days that are **not yet vetted** — held out of the topic pages and newsletter. Flagged for low confidence/novelty/relevance, or below the composite floor (20). Nothing here is deleted; promote an item by raising its scores or clearing `needs_review`, then regenerate.

_Updated 2026-09-09._

## AI Security (42)

- **[Windows ML CLI's CORS Wildcard + trust_remote_code Combo Gives Any Website Localhost RCE](https://github.com/advisories/GHSA-96p9-rh4f-92cf)** · composite 63.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Binding a local tooling server to localhost is not a security boundary by itself if it also sets a wildcard CORS policy — the loopback bind stops remote network attackers, but a…
- **[Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141)** · composite 62.75 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Agent safety must accumulate state across the whole loop; per-trajectory monitors that reset each iteration are blind to slow, fragmented attacks.
- **[Commercial LLMs Used as Live Troubleshooting Backends in Latin American Intrusion Campaigns — OpSec Failures Remain the Best Detection Signal](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/)** · composite 62.67 · _flagged needs_review (low confidence / novelty / relevance)_
  AI-enabled attackers are cutting the skill floor for post-exploitation tooling, but their operational security has not caught up to their new capability — exposed NextChat…
- **[n8n Agent Workflow Tool Bypassed Sub-Workflow Caller Restrictions, Letting Agents Read Data Their Owner Restricted](https://github.com/advisories/GHSA-7hgx-277f-7vmg)** · composite 59.25 · _flagged needs_review (low confidence / novelty / relevance)_
  A permission check enforced on one invocation path (a manual node) is not automatically enforced on a newer invocation path (agent tool-calling) added later to the same underlying…
- **[When AI infrastructure becomes the target: attacks on LiteLLM/RAGFlow/Kestra control points](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)** · composite 58.49 · _ungrounded excerpt — only 75% of quotes verified against the source_
  Attackers are already treating AI gateways like LiteLLM as a credential-rich control plane, so these services need the same scrutiny as any critical enterprise infrastructure.
- **[Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety/)** · composite 57.47 · _ungrounded excerpt — only 75% of quotes verified against the source_
  LLM refusal safety lives in a razor-thin neural layer, so external guardrails and a measurable fragility score are essential rather than optional.
- **[funes: A Cross-Agent Memory Layer That Preserves Raw Session Evidence Instead of Distilling It Into Facts at Write Time](https://github.com/huggingface/funes)** · composite 57.15 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent memory systems, preserving raw evidence with exact provenance rather than summarizing into distilled facts at write time avoids the lossy-compression failure mode of…
- **[OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)** · composite 57.0 · _failed independent verification — Lessons are accurately quoted, but this is a PR announcement of a versioned refresh and a donated standard, not new research; independent reviewer scored novelty/relevance lower (25/55 vs 55/75) — sent to review as a scoring disagreement, not a factual refutation._
  Excessive Agency jumped to #3 in the OWASP LLM Top 10 once the ranking was checked against real incident data instead of just expert consensus — validating that the actual failure…
- **[Cisco AI Defense mcp-scanner: multi-engine scanner (YARA + LLM-judge + inspect API) for MCP tools, prompts, resources, and server instructions](https://github.com/cisco-ai-defense/mcp-scanner)** · composite 55.1 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Treat every MCP surface — tools, prompts, resources, and server instructions — as a distinct attack surface with its own scanner; a single engine misses cases each of YARA,…
- **[BurpMCP-Ultra: 150-tool MCP server for Burp with scope-gate, host allowlist, and per-session token](https://github.com/Cy-S3c/BurpMCP-Ultra)** · composite 53.0 · _ungrounded excerpt — only 50% of quotes verified against the source_
  If you must expose an offensive toolkit via MCP, the operator-only scope gate and per-session token are load-bearing controls; loopback binding is not a trust boundary.
- **[snyk/agent-scan](https://github.com/snyk/agent-scan)** · composite 53.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Any 'MCP scanner' that reads tool descriptions from stdio servers is executing third-party code as a side effect of scanning. Treat scan-time as install-time from a threat-model…
- **[Omnigent: A Widely-Adopted (9,800+ Star) Meta-Harness Adds Policy Enforcement and Sandboxing Across Multiple Coding-Agent Backends](https://github.com/omnigent-ai/omnigent)** · composite 52.88 · _flagged needs_review (low confidence / novelty / relevance)_
  The rapid adoption of a meta-harness abstraction layer (9.8k stars in roughly six months) signals that teams increasingly want harness-agnostic policy and sandboxing enforcement…
- **[Recovering plaintext from 'encrypted' LLM reasoning traces via cross-model replay](https://embracethered.com/blog/posts/2026/recovering-encrypted-llm-thoughts/)** · composite 51.17 · _ungrounded excerpt — only 75% of quotes verified against the source_
  So-called encrypted LLM reasoning traces are recoverable by cross-model replay, so session files containing them can leak passwords, API keys and PII.
- **[PrismorSec/prismor](https://github.com/PrismorSec/prismor)** · composite 50.0 · _ungrounded excerpt — only 25% of quotes verified against the source_
  Prismor is the fuller-featured cousin of the same 'runtime chokepoint for coding agents' pattern, with additions that matter to enterprise buyers: MCP gateway with response-side…
- **[fu351/Doberman-Core](https://github.com/fu351/Doberman-Core)** · composite 50.0 · _ungrounded excerpt — only 0% of quotes verified against the source_
  A concrete implementation of the 'containment on the execution path' pattern for AI-coding-agent guardrails, with explicitly stated invariants (fail-closed, raise-only) that most…
- **[MCP ZAP Server Hardens Its Own Attack Surface by Shipping a Distroless Runtime With No Shell or curl](https://github.com/dtkmn/mcp-zap-server)** · composite 49.12 · _flagged needs_review (low confidence / novelty / relevance)_
  An MCP server that gives an agent guided access to a powerful security tool (a web vulnerability scanner) is itself a high-value attack target, and hardening its own runtime…
- **[Taxonomy-Driven Analysis of Open-Source AI Risk Mitigation Tools](https://arxiv.org/abs/2608.07446)** · composite 49.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Open-source AI risk tooling clusters heavily on technical guardrails; governance and regulatory controls are still overwhelmingly the human's job.
- **[LLMVault: a WebGoat for the OWASP LLM Top 10, with a scripted Play Mode and a live-model Live Mode](https://github.com/CyberSunil/LLMVault)** · composite 48.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Reproducible scripted labs teach the shape of an LLM attack; live-model mode with per-session secrets is what actually validates the skill.
- **[The Perils of Agency: How Developers Perceive, Prioritize, and Address Risks in Agentic AI Products](https://arxiv.org/abs/2606.15485)** · composite 48.5 · _flagged needs_review (low confidence / novelty / relevance)_
  There is a structural capability-vs-risk-control tension in current agentic-AI development: the only controls developers currently reach for are constraints on autonomy and goal…
- **[toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit)** · composite 48.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Third-party LLM proxies are an under-audited middlebox that can inject prompts, swap models, rewrite tool output, and leak errors. An operator-run 14-step audit with an explicit…
- **[CC Safety Net Blocks Destructive Agent Commands by Parsing Command Intent, Not Pattern-Matching Strings](https://github.com/kenryu42/cc-safety-net)** · composite 47.62 · _flagged needs_review (low confidence / novelty / relevance)_
  String/regex-based command blocklists for agent tool calls are trivially evaded by wrapping, flag-reordering, or aliasing; a command-intent parser that determines what a command…
- **[The evolving role of the Red Team in the era of agentic security](https://blog.google/technology/safety-security/the-evolving-role-of-the-red-team-in-the-era-of-agentic-security/)** · composite 47.3 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Prepare for machine-speed agentic attacks by building your own iterative red-teaming agents and ensuring detection/response is near real-time.
- **[Injected Security Context, Not Model Choice, Is What Moves Frontier Models Past a 72-75% Plateau on Secure-and-Functional Vulnerability Fixes](https://snyk.io/blog/snyk-agent-fix-remediation-benchmark/)** · composite 46.97 · _flagged needs_review (low confidence / novelty / relevance)_
  Model choice barely moved the needle on secure-and-functional vulnerability remediation (all frontier models plateaued at 72-75%), but injecting relevant, expert-written fix…
- **[Rule-Based Dataflow + LLM Reasoning Beats Pure-LLM Scanners 4-5x on Recall for Authorization Bugs](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal)** · composite 46.19 · _flagged needs_review (low confidence / novelty / relevance)_
  For a specific, well-defined vulnerability class (IDOR/authorization bugs), a hybrid approach that uses deterministic dataflow analysis to narrow the search space and lets an LLM…
- **[CASA: Classification Augmented with Safety Attention for Robust Multimodal Alignment](https://arxiv.org/abs/2604.00310)** · composite 45.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A single internal, attention-gated safety decision over the shared multimodal representation lets text-only alignment transfer to image and audio inputs without modality-specific…
- **[Making private AI practical with homomorphic encryption (HEIR)](https://blog.google/technology/safety-security/how-google-is-making-private-ai-practical-with-homomorphic-encryption/)** · composite 44.0 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Homomorphic-encryption compilers like HEIR make encrypted AI inference (and encrypted-traffic detection) practical, protecting both user data and proprietary model weights.
- **[agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec)** · composite 44.0 · _ungrounded excerpt — only 67% of quotes verified against the source_
  A packaging-layer spec sitting above MCP that bundles skills and MCP servers together — worth tracking as a new supply-chain distribution unit for agents, because a compromised…
- **[Snyk's Agent Baseline: Agent Governance Products Cover Different Outcomes, and the Right Control Sequence Depends on Deployment Pattern](https://snyk.io/blog/agent-baseline-35-controls-where-should-you-start/)** · composite 42.77 · _flagged needs_review (low confidence / novelty / relevance)_
  Two 'agent governance' products can both be accurately described and non-overlapping, yet still leave a whole outcome (e.g. Validate: has anyone tested the agent behaves safely…
- **[Quoting OpenClaw](https://simonwillison.net/2026/Aug/10/openclaw/#atom-everything)** · composite 42.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Autonomous agents pointed at live third-party sites will actively exploit missing-authorization bugs, not merely describe them — treating agents as a distinct actor in…
- **[OneCLI: Per-Employee Sandboxed Agents Behind a Credential-Injecting MITM Gateway, With Outbound-Only Runners](https://github.com/onecli/onecli)** · composite 41.9 · _flagged needs_review (low confidence / novelty / relevance)_
  A viable production pattern for agent-fleet credential security is architectural, not policy-based: route all outbound agent traffic through a MITM gateway that injects…
- **[Despite Heavy Hype, the Unreleased 'Mythos' Model Ranks 15th of 17 on IDOR Recall; a $4.29/run Open-Weight Model Beats It on Both Axes](https://semgrep.dev/blog/2026/mythos-idor-benchmark)** · composite 40.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Marketing hype around a frontier model's capability class doesn't survive contact with an independent, labeled benchmark — on this specific task, several cheaper open-weight…
- **[ForesightSafety-SAGE: A Fully Automated Scenario Generation and Safety Evaluation Framework for LLM Agents](https://arxiv.org/abs/2606.08531)** · composite 39.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Process-level, automatically-generated scenario suites reveal high behavioral safety failure rates in current LLM agents (average ASR 47.1%, some models >70%) that…
- **[Litigant Hides Prompt Injection in Real Court Filing Telling AI Reviewers to Rule in Their Favor](https://www.404media.co/person-hides-prompt-injection-in-legal-filing-telling-ai-to-side-with-them/)** · composite 39.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Prompt injection has moved from a technical curiosity into real adversarial legal process, and courts are already building doctrine around it: a judge explicitly framed hidden…
- **[Minimal, Local, Causal Explanations for Jailbreak Success in Large Language Models](https://arxiv.org/abs/2605.00123)** · composite 39.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Jailbreak success is not one global mechanism; per-attack, per-category local causal explanations require far fewer interpretable interventions to force refusal than global…
- **[OpenClaw 2.0's Usability Overhaul Ships With Security Still Opt-In: Unencrypted Secrets, Sandbox Off by Default](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)** · composite 38.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Naming a feature 'protected' or shipping a 'sandbox' does not make it secure by default — both of OpenClaw 2.0's new security features require the operator to opt in to the actual…
- **[TOFD: Target-Oriented Feature Decoupling against Poisoning Attacks in Split Federated Learning](https://arxiv.org/abs/2608.07274)** · composite 36.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Split Federated Learning has attack surfaces (the split boundary and smashed activations) that generic FL defenses miss; TOFD exploits the split paradigm itself for detection.
- **[Isolated AI Security Tools Each Report Clean While an Attacker Bridges an Untrusted Prompt to a Backend Execution Sink](https://snyk.io/blog/why-your-ai-application-is-exposed/)** · composite 35.57 · _flagged needs_review (low confidence / novelty / relevance)_
  Chained risk in AI applications breaks the traditional isolated-vulnerability security model: a system where every component — scanner, eval framework, static analyzer —…
- **[Corrupting Attention: Evasion-Based Adversarial Attacks on Encoder Attention in Detection Transformers](https://arxiv.org/abs/2608.06674)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Attacking the encoder-attention structure itself in detection transformers is a stronger evasion strategy than perturbing outputs, and the weakness generalizes across corruption…
- **[Trustworthy Agent Network: Trust in Agent Networks Must Be Baked In, Not Bolted On](https://arxiv.org/abs/2605.19035)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A2A network trust is a coordination-layer problem: individual-agent alignment does not compose, so agent-network protocols need trust primitives designed in from the beginning.
- **[modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)** · composite 32.0 · _ungrounded excerpt — only 50% of quotes verified against the source_
  Reference pointer for anything that touches MCP tool-description or schema-level security work — the canonical source-of-truth for what the protocol actually says.
- **[Pydantic AI Ships Official First-Party Guardrails, Upstreaming a Community Library](https://github.com/pydantic/pydantic-ai-harness)** · composite 29.87 · _flagged needs_review (low confidence / novelty / relevance)_
  A widely-used agent framework (Pydantic AI) absorbing community-built guardrail functionality into its official first-party harness is a maturity signal for the ecosystem —…
- **[anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection](https://github.com/anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection)** · composite 26.0 · _ungrounded excerpt — only 50% of quotes verified against the source_
  A popular community roadmap for AI/ML pentesting exists and now dedicates a phase to agentic-AI and MCP security — worth linking as a beginner ramp, but it's an index, not a…

## Product Security (13)

- **[VMs won't contain cyber-capable agents](https://blog.trailofbits.com/)** · composite 65.6 · _ungrounded excerpt — only 33% of quotes verified against the source_
  Treat capable AI agents as an advanced persistent threat: isolate them with hardened microVMs, enforce least privilege, monitor actively, and keep host and hypervisor dependencies…
- **[What's in a tag name? JavaScript, apparently](https://portswigger.net/research)** · composite 62.9 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Do not rely on WAFs or character blocklists to stop XSS; enforce context-aware output encoding, a strict Content-Security-Policy, and trusted HTML sanitization, since exotic…
- **[Consumer Smart Glasses Enable a General Video-Based Password-Cracking Pipeline That Cuts Human-Chosen Password Entropy by Up to 60 Bits](http://arxiv.org/abs/2609.06539v1)** · composite 60.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Consumer AI-enabled wearables (smart glasses with a built-in camera) turn a previously specialist side-channel attack (video-based keystroke inference) into something achievable…
- **[Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/)** · composite 54.77 · _ungrounded excerpt — only 33% of quotes verified against the source_
  Don't over-index on 'AI malware' hype: your existing behavioral/sandbox detection still catches it — but expect faster variant iteration.
- **[Composer Trusted a Package's Perforce Source URL Enough to Hand It to the p4 CLI as a Local Command](https://github.com/advisories/GHSA-rvx4-ffvw-m9q3)** · composite 51.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Passing user- or dependency-supplied configuration data unvalidated into a CLI tool's argument is dangerous whenever that CLI has any "local command" or "connect to this address"…
- **[A Widely-Used VS Code Extension (9.5M Installs) Chained a Markdown eval() Sink, an Untrusted Webview Message Dispatcher, and a vm.runInNewContext() Escape Into RCE](https://projectdiscovery.io/blog/a-9-5m-install-vs-code-extension-one-markdown-file-and-a-supply-chain-foothold)** · composite 50.93 · _flagged needs_review (low confidence / novelty / relevance)_
  Both root causes here are well-documented anti-patterns that keep recurring: evaluating any part of untrusted content as code (even a diagram-rendering "data" field) and trusting…
- **[A Hybrid Security Framework for Mini-Programs: Visual UI Compliance and Network Risk Assessment](https://arxiv.org/abs/2608.25877)** · composite 49.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Mini-program app vetting must combine visual UI-compliance checks with network-redirect analysis to catch mis-click-to-payment dark patterns.
- **[Astro's Default Image Optimizer Allowed Remote Code Execution via a Malicious AVIF Image, Through a libheif Bug in Sharp](https://github.com/advisories/GHSA-26w7-cxv4-gfx2)** · composite 47.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Image-processing pipelines are a recurring RCE vector because they sit at the boundary of parsing complex, attacker-influenced binary formats (here, AVIF via libheif) with native…
- **[Hono's Path-Traversal Fix Only Blocked One Parent-Directory Segment — a Longer Run of '..' Still Escapes the Output Directory](https://github.com/advisories/GHSA-gqvv-2mrq-wpjv)** · composite 47.85 · _flagged needs_review (low confidence / novelty / relevance)_
  A path-traversal fix that handles the exact reported payload but not the general pattern (arbitrarily many parent-directory segments, not just one) is a fix in name only —…
- **[morgan's Log-Forging Fix Missed Unicode Line-Separator Code Points, Letting Attacker-Controlled Headers Split Log Records](https://github.com/advisories/GHSA-jxfw-x594-9x9m)** · composite 46.65 · _flagged needs_review (low confidence / novelty / relevance)_
  A log-injection fix that escapes ASCII control characters but not Unicode line-separator code points is incomplete for any downstream consumer that is Unicode-aware rather than…
- **[A One-Week Dependency Cooldown Produces Outsized Supply-Chain Protection for Minimal Developer Friction](https://semgrep.dev/blog/2026/rolling-out-dependency-cooldowns-org-wide)** · composite 37.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Most malicious package versions are caught within hours to days of publication, so simply refusing to install anything published in the last week closes most of that attack window…
- **[Rolling Out Org-Wide GitHub Actions SHA-Pinning Enforcement Has Non-Obvious Failure Modes Beyond the Obvious Tag-Pinning Fix](https://semgrep.dev/blog/2026/sha-pinning-for-github-actions-org-wide)** · composite 32.09 · _flagged needs_review (low confidence / novelty / relevance)_
  Enforcing SHA-pinning for CI actions requires closing three distinct gaps — tag references, branch references (especially to internal actions), and transitively unpinned actions…
- **[Trail of Bits Runs an Independent, From-Scratch Auditor for Signal's Key Transparency System](https://blog.trailofbits.com/2026/08/11/how-trail-of-bits-helps-verify-the-integrity-of-your-signal-chats/)** · composite 31.73 · _flagged needs_review (low confidence / novelty / relevance)_
  A key-transparency system's actual security guarantee is bounded by its auditor-signature freshness window, not by the cryptography alone — Signal's design means a compromised or…

## AI Research (166)

- **[ratel-ai/ratel](https://github.com/ratel-ai/ratel)** · composite 50.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Progressive disclosure of tool schemas via an in-process BM25 index is a concrete implementation of the 'few-distinct-tools-beat-many' guidance — it moves tool-selection out of…
- **[Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?](https://arxiv.org/abs/2605.22148)** · composite 47.0 · _ungrounded excerpt — only 50% of quotes verified against the source_
  In self-editing agent skill libraries, the judge's false-pass rate (not its overall accuracy) determines whether eviction can ever converge; asymmetric judge errors are the…
- **[Birfy/agentdescent](https://github.com/Birfy/agentdescent)** · composite 45.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  The right abstraction for self-improving agent systems is not 'run and reflect' but a discrete-space optimizer over diffs with explicit conflict resolution, staleness policies,…
- **[OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557)** · composite 44.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The core architectural move is decoupling training from inference by intercepting the model call at the harness proxy layer. That lets an existing RL stack train against a…
- **[Counterfactual Simulation Training for Chain-of-Thought Faithfulness](https://arxiv.org/abs/2602.20710)** · composite 42.5 · _flagged needs_review (low confidence / novelty / relevance)_
  CoT faithfulness can be trained for by rewarding CoTs that enable counterfactual simulation, materially improving CoT monitors — but the effect does not transfer symmetrically…
- **[Fzkuji/OpenProgram](https://github.com/Fzkuji/OpenProgram)** · composite 42.5 · _ungrounded excerpt — only 75% of quotes verified against the source_
  The load-bearing idea is 'a code gate can't be talked past' — when a model's answer fails validation, it is sent back to re-decide, so critical steps cannot be skipped by prompt…
- **["LLM Agent Performance" Is Not a Single Evaluation Target](https://arxiv.org/abs/2602.03238)** · composite 41.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent benchmark scores are only interpretable relative to a declared candidate boundary (model vs. full system) and condition policy (robustness scope); collapsing all three into…
- **[Can AI agents conduct open-ended AI research? Early evidence from two case studies](https://arxiv.org/abs/2607.27191)** · composite 41.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The methodological contribution (author-graded shadow evaluations of unpublished work) is more durable than the point-in-time verdict. The findings themselves argue against strong…
- **[In-Context Examples Suppress Scientific Knowledge Recall in LLMs](https://arxiv.org/abs/2604.27540)** · composite 41.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Few-shot examples don't just 'reinforce' knowledge; they can displace it. On tasks where the pretrained closed-form answer is better than curve-fitting to the demos, few-shot…
- **[Zero Gap Is Not Restoration: Stratified Per-Question Probability Evaluation and Step-wise Mitigation of Benchmark Contamination](https://arxiv.org/abs/2608.07341)** · composite 41.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Zero G-AP is not proof a contaminated model has been restored. Evaluate mitigation with per-question probability gaps stratified by clean-model solve probability; averaged…
- **[aeonfun/aeon](https://github.com/aeonfun/aeon)** · composite 39.5 · _flagged needs_review (low confidence / novelty / relevance)_
  The interesting bit isn't the marketing ('most autonomous') but the health loop: rate every run 1-5 with a small model, then auto-route low-scorers to a repair skill. Independent…
- **[universal-tool-calling-protocol/utcp-specification](https://github.com/universal-tool-calling-protocol/utcp-specification)** · composite 39.5 · _ungrounded excerpt — only 33% of quotes verified against the source_
  UTCP treats MCP as one transport among many; for defenders, this means threat models built around 'MCP tools' need to generalize to any tool-calling transport, and…
- **[INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation](https://arxiv.org/abs/2603.21607)** · composite 36.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  For RAG systems, naive token-entropy hallucination detectors are miscalibrated in a predictable way: the same circuit that grounds the answer inflates entropy. Gating on…
- **[Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653)** · composite 36.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Adjacent-bucket frontier-model release: relevant as context for the open-weights landscape, but not a security or harness-design claim.
- **[wanmol/goal-flow](https://github.com/wanmol/goal-flow)** · composite 36.5 · _flagged needs_review (low confidence / novelty / relevance)_
  The interesting artifact here is not the framework — it's the openly documented incident: even production teams shipping agent frameworks leak credentials into git history. Any…
- **[Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](https://arxiv.org/abs/2608.06811)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  For long-horizon coding agents, treating planning and memory as coupled substrate (with an external execution-verified done-signal) reduces repeated failed edits, empty-patch…
- **[Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](https://arxiv.org/abs/2607.20457)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Content-aware summaries chosen by rare-token statistics beat content-blind anchors for distributed long-context attention, at identical KV-cache footprint.
- **[Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression](https://arxiv.org/abs/2608.07001)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Framing KV-cache compression as a global resource-allocation problem across layers, heads, and slots outperforms fixed-rule eviction or merging, especially at aggressive…
- **[SSTQ: Privacy-Preserving Vector Quantization via Subsampled Stochastic TurboQuant](https://arxiv.org/abs/2608.05127)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  For local-DP distributed optimization, tight-frame quantization plus subsampling beats vqSGD-style geometric constructions on communication-utility trade-off.
- **[openai/openai-agents-python](https://github.com/openai/openai-agents-python)** · composite 35.0 · _ungrounded excerpt — only 33% of quotes verified against the source_
  Modern agent SDKs converge on a small handful of primitives (agent, handoff, guardrail, session, tracing) plus a first-class sandbox client — sandbox-by-default is now…
- **[Ask-E: An Environment for Calibrated Question Generation](https://arxiv.org/abs/2608.06933)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Generating calibrated questions is itself an eval signal; hard-to-generate problems require capability beyond the target — useful framing for keeping red-team/eval sets ahead of…
- **[Beyond Scaffold Splits: Structural-Frontier Evaluation Reveals Hidden Failures in ADMET Models](https://arxiv.org/abs/2607.10729)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  OOD splits chosen by convention can hide model failure at the true generalization frontier; the same critique likely applies to LLM benchmarks, though the paper is…
- **[Equivariant Sparse Autoencoders: Mechanistic Interpretability of Neural Networks on Symmetric Data](https://arxiv.org/abs/2511.09432)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Reconstruction quality can be inversely correlated with feature usefulness for SAEs under symmetries, which weakens reconstruction-based interpretability benchmarks even though…
- **[Multi-Level Modeling of Large Language Model Inference Latency and Energy via Hybrid Analytical--Machine-Learning Predictors](https://arxiv.org/abs/2608.06723)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Cost/latency estimation for LLM inference is being reframed as a hardware-free predictor problem, decoupled from actually running the model. For deployment decisions this is…
- **[Rethinking Evaluation Paradigms in IBP-based Certified Training](https://arxiv.org/abs/2606.02134)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Single-config accuracy numbers over-state progress in certified-training research; Pareto-front comparisons after multi-objective tuning are the more honest bar. Relevant to…
- **[SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization](https://arxiv.org/abs/2602.12187)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  SAGEO is the SEO of the LLM era. Realistic end-to-end evaluation shows most optimization tricks that look good on toy benchmarks hurt real retrieval/reranking. Adjacent to…
- **[Topology-Aware Data Movement for Disaggregated GPU Inference](https://arxiv.org/abs/2607.28633)** · composite 33.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Uniform RDMA for KV-cache transfer wastes up to 72x bandwidth headroom; topology-aware transport selection and pipelining reclaim most of it.
- **[Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](https://arxiv.org/abs/2608.06849)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Head function (retrieval vs streaming) can be diagnosed from static QK weight geometry rather than from runtime traffic, which removes the calibration-data dependency of prior…
- **[CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](https://arxiv.org/abs/2608.07458)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Sub-chunk KV cache reuse targeted at query-relevant nuggets outperforms coarse chunk-level cache reuse for long-context RAG on multi-hop QA under fixed prefill latency budgets.
- **[FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specialized harness plus leakage-guarded benchmarks materially outperform general-purpose deep-research pipelines on finance tasks, and the ceiling is still low.
- **[Multi-Agent Forensic Reasoning for Generalizable Deepfake Video Detection](https://arxiv.org/abs/2608.06865)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  For generalizable deepfake video detection, specialist-agent decomposition across independent forensic perspectives with a judge-agent reconciliation can let small open-source…
- **[Pre-Inference Routing for Cost-Efficient Document Field Extraction](https://arxiv.org/abs/2608.06607)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Pre-inference routing pays off only under two joint conditions: the cheap model fails often enough to matter and its failures are predictable from cheap signals; without both,…
- **[Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration](https://arxiv.org/abs/2605.27752)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Whether verbalized confidence beats token-likelihood confidence is not a property of the model; it is a property of the (answer, context, readout) protocol, and published…
- **[Same Attention, Different Truths: Put Logit-Lens over Visual Attention to Detect and Mitigate LVLM Object Hallucination](https://arxiv.org/abs/2608.07302)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  For LVLM reliability work, attention magnitude is a weak signal because real and hallucinated targets attract comparable attention; what the attended-to features decode to under a…
- **[Semantic Adapter Routing with Fine-Tuning Task Embeddings](https://arxiv.org/abs/2606.19079)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Routing at inference time can be done training-free by task-embedding-nearest-neighbor over adapters. The under-the-radar bit is GRACE: an adapter's fine-tuning data is…
- **[Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885)** · composite 31.1 · _flagged needs_review (low confidence / novelty / relevance)_
  A large fraction of real-world queries can be redistributed to local inference on power-constrained hardware, and IPW is a compact way to track that shift over time.
- **[Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897)** · composite 31.1 · _flagged needs_review (low confidence / novelty / relevance)_
  On-policy self-distillation from ICL-conditioned teachers offers a reward-free path to continual learning from demonstrations, with the practical implication that SFT-only…
- **[Calibrating WEAT Against Anisotropy: ZCA Whitening as a Geometric Pre-Processing Step for Embedding Association Tests](https://arxiv.org/abs/2608.06908)** · composite 30.5 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Bias measurements produced by WEAT on modern anisotropic embedding spaces are unreliable in both directions; prior fairness-audit numbers should be re-examined with a geometric…
- **[LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Long-lived agent memory research keeps moving from retrieval-plus-summarization toward intrinsic persistent state — an architectural shift worth tracking for the agent-memory…
- **[Provable Training Data Identification for Large Language Models](https://arxiv.org/abs/2510.09717)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Treating training-data identification as set-level inference with FIR control gives statistically defensible answers rather than instance-wise scores whose error rate is opaque.
- **[SABRE: Scalable and Automated Benchmarking of VLMs under Stress](https://arxiv.org/abs/2608.07435)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A red-team methodology for VLM stress tests: filter out anything a reference VLM solves, keep only samples that force reliance on visual evidence over language priors.
- **[Conditioning Protein Generation via Hopfield Pattern Multiplicity](https://arxiv.org/abs/2603.20115)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A single scalar on the logits gives closed-form control over which subfamily a Hopfield sampler emits, cleanly separating latent-space conditioning from downstream sampling /…
- **[Debias in Text, Believe Your Eyes: Text-Anchored Cross-Modal Transfer for Visual Counter-Commonsense Reasoning](https://arxiv.org/abs/2608.06938)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  When multimodal outputs contradict the image, the fix is often at the language decoder, not the vision encoder — a text-only debiasing pass can transfer to visual reasoning.
- **[Inference-Time Scaling of Diffusion Language Models via Trajectory Refinement](https://arxiv.org/abs/2507.08390)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Diffusion LMs get an inference-time steering knob (trajectory refinement iterations) that stays useful after parallel-sample gains flatten; adaptive iteration allocation saves…
- **[Measuring Concept Content in Text from LLM Activations: ESG Evidence from Concept Vectors and Linear Probes](https://arxiv.org/abs/2608.07208)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Frozen-LLM activation probes on ESG text nearly match a fine-tuned classifier and outperform the model's own answer, suggesting activation-level readers extract judgments the…
- **[Predictive Multi-Tier Memory Management for KV Cache in Large-Scale GPU Inference](https://arxiv.org/abs/2604.26968)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  KV-cache sizing today is architecture-agnostic and over-provisions MLA by up to 57x; unified sizing + tiered storage + a Bayesian reuse predictor is the proposed replacement, but…
- **[Toward a Causal Data Management Ecosystem for Decision Making and Agentic AI](https://arxiv.org/abs/2608.07214)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The authors argue autonomous-agent trustworthiness depends on an explicit shared causal layer over the fragmented data sources feeding an AI ecosystem, not just better integration.
- **[Trajectory-Relative Hindsight Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.07371)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Training-side agent-RL technique. Adjacent to cluster B (agents and harnesses) but strictly about RL credit assignment during training, not about production harness design, tool…
- **[In Situ Training of Implicit Neural Compressors for Scientific Simulations via Sketch-Based Regularization](https://arxiv.org/abs/2511.02659)** · composite 28.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Sketched replay buffers plus limited full-sample memory let an online-trained neural compressor for scientific data approximately match an offline-trained equivalent at high…
- **[Newton-Schulz Retraction-Based Inference Enables Hidden Quantum Markov Models to Outperform Classical HMMs](https://arxiv.org/abs/2608.06554)** · composite 28.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Quantum probabilistic sequence models can now be trained scalably; not a security paper.
- **[RenderFormer++: Scalable and Physics-Informed Feed-Forward Neural Rendering](https://arxiv.org/abs/2606.30380)** · composite 28.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Graphics/vision paper on scalable neural rendering; unrelated to LLM security or agentic AI.
- **[Retrofitting Linear Attention into Diffusion Language Models](https://arxiv.org/abs/2608.06628)** · composite 28.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Efficiency paper for diffusion LLMs; no security relevance.
- **[KReF: Training-Free Retrieval for Long-Term Time-Series Forecasting and Predictive Uncertainty](https://arxiv.org/abs/2608.06748)** · composite 28.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Retrieval-as-inductive-bias is showing up outside LLM RAG contexts — in this case as a training-free predictor for time-series forecasting. Useful as a reminder that 'retrieval'…
- **[Large Causal Models for Temporal Causal Discovery](https://arxiv.org/abs/2602.18662)** · composite 27.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Applies the pretrain-once-run-anywhere playbook to causal discovery on time series, which is orthogonal to security but signals continued spread of foundation-model methodology…
- **[AutoMOOSE: An Agentic AI for Autonomous Phase-Field Simulation](https://arxiv.org/abs/2603.20986)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A domain-specific harness with an explicit adversarial 'Skeptic' role that checks outputs against physics invariants stabilizes an otherwise-flaky code-generating agent. The…
- **[CreativeInstruct: Scalably Teaching LLMs to Balance Quality, Creativity, and Diversity](https://arxiv.org/abs/2608.07460)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Post-training collapses diversity; a controllable [StartCreativity] span learned via instruction tuning restores base-model creativity without a second model at inference and…
- **[CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](https://arxiv.org/abs/2608.06763)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  You can keep the dense integer code stream that GPU kernels want while gaining non-uniform reconstruction flexibility by parameterizing a monotonic cubic mapping.
- **[GPTKB 2.0: Browsing, Querying, and Auditing a Disambiguated LLM-Derived Knowledge Base](https://arxiv.org/abs/2608.06992)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  LLM-materialized KBs can carry per-fact provenance including disambiguation decisions — a shape worth borrowing when you need auditable grounding rather than opaque retrieval.
- **[IFCLoRA: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2607.22251)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Global information-flow topology, not just local gradient stats, is a useful structural prior for allocating scarce LoRA rank capacity.
- **[Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276)** · composite 27.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Another open-weights multimodal frontier model release; interesting orchestration hook (parallel agent swarm) but no security angle unless you're building agent-runtime defenses.
- **[Let's Unlearn Stereotypes Before Decision-Making: Assessing the Impact of Intrinsic Bias Mitigation on Downstream Fairness in LLMs](https://arxiv.org/abs/2509.16462)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Bias/fairness paper, not security. Contributes evidence that intrinsic bias mitigation can meaningfully move downstream fairness metrics without tanking predictive performance — a…
- **[Mathematical Principles and Experimental Discoveries of the Emergence of Symbolic Patterns in Artificial Neural Networks](https://arxiv.org/abs/2608.06839)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Under two implicit criteria satisfied by most inputs, ANN inference reduces to a sparse symbolic-interaction representation that transfers across samples and models.
- **[Multi-Legal-Bench: Evaluating LLMs on Legal Reasoning Across Jurisdictions, Languages, and Legal Traditions](https://arxiv.org/abs/2605.29738)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Legal-domain multilingual benchmark. The methodological finding — label-set alignment beats language proximity for cross-lingual transfer — is the only durable takeaway; the rest…
- **[Recovering Lesion Parameters from Aphasic Picture Naming Error Profiles in Large Language Models](https://arxiv.org/abs/2608.06429)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Behavior-to-parameter inverse mapping in LLMs shows that some perturbation parameters are recoverable while layer index is not, evidence of functional redundancy across…
- **[RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](https://arxiv.org/abs/2608.07088)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Notable inference-efficiency result for MLLMs (Pareto-good visual-token pruning), but nothing security-relevant.
- **[Scalable Long-Horizon Planning with Staggered Updates for Lifelong MAPF](https://arxiv.org/abs/2608.06702)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  The word 'agent' collides across communities: LMAPF papers are about robots and warehouse fleets, not LLM agent harnesses. When triaging RSS from cs.AI, filter on whether 'agent'…
- **[Solver-Guided Reasoning for Mixed-Equilibrium Strategies](https://arxiv.org/abs/2608.06741)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For domains with computable ground truth (game equilibria), replacing human demonstrations with solver output yields substantially better LLM reasoning traces.
- **[Stochastic Autoregressive Learning](https://arxiv.org/abs/2608.07224)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Stochastic autoregressive learning is not a straight extension of the deterministic theory: CoT vs base vs end-to-end sample complexity cannot be universally ordered at fixed…
- **[Sub-Quadratic Bisimulation Metrics via Approximate Nearest Neighbors: Coverage-Augmented Guarantees and Computable Two-Sided Certificates](https://arxiv.org/abs/2608.06762)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  You can trade quadratic pairwise work for ANN-guided restricted updates while retaining computable enclosure certificates, at the cost of a coverage-dependent residual error.
- **[Theoretical Foundations of Communication-Efficient, Robust, and Practical Distributed and Federated Optimization](https://arxiv.org/abs/2608.06563)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  One chapter touches Byzantine robustness in federated learning, a tangential AI-security topic, but the piece is fundamentally a theory thesis rather than a security artifact.
- **[jdevalk/specification.website](https://github.com/jdevalk/specification.website)** · composite 27.5 · _ungrounded excerpt — only 50% of quotes verified against the source_
  Not an AI-security artifact; primary value here is the MCP server pattern of exposing an authoritative reference corpus to agents, and the 'agent readiness' rubric as a checklist…
- **[MetaSICL: Globalizing Auditory LLMs for Underserved Speakers and Languages via Meta Speech In-Context Learning](https://arxiv.org/abs/2601.18904)** · composite 27.2 · _flagged needs_review (low confidence / novelty / relevance)_
  Meta-learning-style post-training on high-resource speech data can install a durable in-context adaptation ability that transfers to unseen low-resource languages and tasks.
- **[An AI4AI Framework for Visual Token Pruning](https://arxiv.org/abs/2608.07193)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Framing algorithm design as residual edits over a strong base policy, in a task-specific DSL, is the load-bearing trick that lets an LLM's general reasoning translate into…
- **[Capacity Confounds and Coverage Guarantees in Adaptive Sub-model Federated Learning](https://arxiv.org/abs/2608.07157)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  In sub-model federated learning, parameter coverage and capacity budgeting explain the accuracy wins usually credited to adaptive per-client capacity allocation; update-based…
- **[Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](https://arxiv.org/abs/2608.06557)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  A single per-request latency-budget signal can jointly govern scheduler ordering and KV-cache tiering; treating budget as a shared coordination variable outperforms deadline-only…
- **[LoCA: Forward-Only LLM Tuning after One-Shot Calibration with Local Credit Assignment](https://arxiv.org/abs/2608.03020)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Amortize LLM adaptation cost by doing one backward calibration pass, then keep tuning forward-only. Interesting only if you're building on-device or backward-restricted adaptation…
- **[Optimization as a Dynamical System: Generative Schedules from Latent ODEs](https://arxiv.org/abs/2509.23052)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Framing LR schedules as trajectories of a learned latent ODE gives generative, non-parametric schedules that outperform hand-tuned baselines, but the contribution is training-side…
- **[Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054)** · composite 26.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Interpretability finding on VLMs: object presence is linearly encoded but object orientation is not, and distance degrades separability. Useful mental model, not a security…
- **[Diffusion-MF: Approximate Structured Diffusion for Sequence Labelling](https://arxiv.org/abs/2606.18856)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  NLP structured-prediction paper; not about LLM harness or agent security.
- **[FutureBridge: Token Selection Beyond Local Preference in Collaborative Decoding](https://arxiv.org/abs/2608.06819)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  In small-model / large-model collaborative decoding, the LLM's locally preferred token is not always the token the SLM can build on; selecting tokens by downstream SLM usability…
- **[Geo-Spatial Concept Probing of Large Language Models: Abstraction, Compositionality, and Grounding](https://arxiv.org/abs/2608.07353)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  LLM spatial-concept probing is an interpretability topic; the guess_topic label of ai-security is a mislabel. There is no adversarial framing, no defender playbook, and no cluster…
- **[ODEWorld: A Continuous Predictive Architecture via Physical-Time Flow](https://arxiv.org/abs/2607.27924)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Video/robotics world-model paper with no security angle; noteworthy only as another data point in the continuous-time vs discrete-time world-modeling debate.
- **[Quoting Claude Opus 5 system prompt](https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/#atom-everything)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Concrete example of using the system prompt to patch a knowledge-cutoff gap on politically sensitive current events, rather than relying on training or RAG. Interesting for…
- **[Robust inference using density-powered Stein operators](https://arxiv.org/abs/2511.03963)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Pure statistical-ML methods paper. No AI-security or agent-design content; only tangential relevance via 'robust to contamination' framing.
- **[SenWorld: A Digital-Twin Simulation for Generating Context-Rich Evaluation Data](https://arxiv.org/abs/2607.19949)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The paper's contribution is a labels-by-construction evaluation methodology: instead of asking an LLM judge whether an answer is right, the correct answer is a pointer into a…
- **[A Physics-Inspired Classical Digital Twin of Cortical Dynamics: A Band-Stratified Metriplectic Port-Hamiltonian Neural Network Learned from Brain-Computer-Interface EEG](https://arxiv.org/abs/2607.10439)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Neuroscience/BCI modelling paper. Not in the AI-security lane. Interesting mainly as an example of imposing physical invariants on a neural network by construction rather than by…
- **[Dirac-Frenkel dynamics with inertia for nonlinearly parametrized solutions of evolution problems](https://arxiv.org/abs/2606.24769)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Numerical-analysis result about parameter dynamics with redundant parametrizations; not relevant to AI security or harness practitioners.
- **[Evaluating Useful Surrogate Models for Configuration Tuning Beyond Accuracy: A Fitness Landscape Analysis Perspective](https://arxiv.org/abs/2509.21945)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Accuracy is not sufficient to judge whether a surrogate model will help tune a system; a landscape-aware selector picks better model-tuner pairs than random in 79-82% of cases.
- **[H2AL: Hyperbolic Hierarchy-aware Aggregative Learning for Registration-based Few-shot Medical Image Segmentation](https://arxiv.org/abs/2608.07340)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Purely a medical imaging segmentation contribution; not adjacent to any cluster in the interests taxonomy.
- **[How Molecular Generative Models Organize Molecular Identity](https://arxiv.org/abs/2608.06956)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Latent spaces of molecular generative models are not automatically chemically navigable; internal organization must be characterized before treating them as such.
- **[Optimized Certainty Equivalent Risk Minimization Using Samples: Algorithms, Convergence Rates, and Applications](https://arxiv.org/abs/2608.07113)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Risk-minimization theory (finance + UQ); tangential to AI safety, not directly security-relevant.
- **[Playing Games with My Heart: An Evaluation of AI Companion Apps](https://arxiv.org/abs/2605.08093)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Consumer-protection / dark-patterns critique of AI companion apps; policy and sociotechnical, not agent-security. Belongs in the news lane.
- **[Symbolic Graphics Programming with Large Language Models](https://arxiv.org/abs/2509.05208)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A concrete example of RL-with-verifiable-rewards using a format gate plus a cross-modal similarity signal to align a small open model to a proprietary-model target. Interesting…
- **[The Sparsity Whisperer](https://arxiv.org/abs/2608.06630)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  For LLM sparsification, preserving differences between neuron outputs is a composable signal that improves post-training pruning quality over activation-only criteria.
- **[CrystalGRPO: Target-Aligned and Coverage-Preserving Reinforcement Learning for Flow-Based Crystal Structure Prediction](https://arxiv.org/abs/2608.06582)** · composite 25.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Materials-science generative-model paper; no AI security angle.
- **[Seeking SOTA: Time-Series Forecasting Must Adopt Taxonomy-Specific Evaluation to Dispel Illusory Gains](https://arxiv.org/abs/2603.15506)** · composite 24.8 · _flagged needs_review (low confidence / novelty / relevance)_
  The 'deep-learning time-series SOTA' picture is mostly an artifact of benchmark selection. Same lesson recurs elsewhere in ML: pick harder eval sets and require simple baselines.…
- **[Aftab: A Comprehensive Benchmark of CNN Encoders and Advanced Value Functions in Parallelized Q-Networks](https://arxiv.org/abs/2608.07335)** · composite 24.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  This is a deep-RL architectural benchmark for value-based, buffer-free Q-learning. It does not overlap with LLM agent harness design or any AI-security surface; treat as news-lane…
- **[Boundary Density Likelihood for Direct Event-Time Supervision](https://arxiv.org/abs/2408.12792)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For sparse-event detection tasks, training directly on the evaluated output (event times) beats training on a proxy (samplewise segmentation) — the framing is a generic reminder…
- **[Conformal Fusion Under Missing Modalities](https://arxiv.org/abs/2608.07183)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Coverage under arbitrary modality availability can be achieved architecturally rather than by post-hoc recalibration; absent-modality vacuity localises uncertainty to the missing…
- **[IceHorizon: A Dataset for Horizon Detection in Ice-Covered Maritime Environments and Comparative Evaluation of Detection Methods](https://arxiv.org/abs/2608.07018)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specific CV benchmark with a small hybrid vs. classical comparison; irrelevant to AI security.
- **[Judge a Book by its Cover: Investigating Multi-Modal LLMs for Multi-Page Handwritten Document Transcription](https://arxiv.org/abs/2502.20295)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For multi-page HTR, sharing cross-page context in the prompt beats per-page transcription. Useful only if you actually transcribe handwriting.
- **[Mitigating Gradient Pathology in PINNs through Aligned Constraint](https://arxiv.org/abs/2605.25001)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Optimization-landscape fix for a well-known PINN training pathology; interesting for scientific ML but has no direct bearing on AI security.
- **[MultiView-Bench: A Diagnostic Benchmark for World-Centric Multi-View Integration in VLMs](https://arxiv.org/abs/2607.08970)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  VLM capability-benchmark paper. Adjacent to the security lane only in the sense that VLM capability gaps set the ceiling for agentic vision-based tools. Not a claim candidate.
- **[Online Conformal Prediction Beyond Feedback](https://arxiv.org/abs/2608.07139)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Coverage-guaranteed online uncertainty quantification is achievable without ever observing feedback on deployed predictions, by casting the setting as a partial-monitoring game…
- **[PULSE: Agentic Investigation with Passive Sensing for Proactive Affective Intervention in Cancer Survivorship](https://arxiv.org/abs/2605.17679)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain application of tool-using LLM agents to passive sensing; interesting harness pattern (fixed 8-tool set, self-directed tool choice) but the paper is HCI/clinical, not…
- **[Understanding Differentiable Embeddings Through Differential and Integral Geometry](https://arxiv.org/abs/2608.06809)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Trust diagnostics for nonlinear embeddings need both a differential and an integral view; no amount of local derivative measurement can substitute for path-based analysis.
- **[Vector Space of Cycles](https://arxiv.org/abs/2606.08202)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Statistical ML for neuroscience-style dynamical systems; no bearing on AI security or practitioner harness design.
- **[aristoteleo/PantheonOS](https://github.com/aristoteleo/PantheonOS)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A biology-oriented agent framework is out of scope for security claim work, but its own June-2026 trojanized-PyPI incident is a real-world data point for the ongoing pattern of…
- **[ArchEGraph: A Large-Scale Graph Dataset for Geometry-Topology-Physics Aligned Building Energy Modeling](https://arxiv.org/abs/2608.06772)** · composite 23.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Building energy modeling now has a large-scale geometry-topology-physics graph benchmark for training and evaluating surrogate models.
- **[MiCoPro: End-to-End Mixed Precision HW/SW Co-design with HW-aware Proxy Model](https://arxiv.org/abs/2608.06916)** · composite 23.9 · _flagged needs_review (low confidence / novelty / relevance)_
  For edge accelerators, a target-specific latency proxy plus MPQ search closes the gap between algorithm-side quantization and actual deployable C code.
- **[Optimization-based Online Conformal Prediction for Multi-step Forecasting](https://arxiv.org/abs/2508.13362)** · composite 23.9 · _flagged needs_review (low confidence / novelty / relevance)_
  For multi-step time-series forecasts, jointly optimizing across horizons within admissible-set constraints keeps CP coverage guarantees while producing sharper intervals than…
- **[Harnessing the Synergy between LLM Agents and Knowledge Graphs for Urban Socioeconomic Prediction](https://arxiv.org/abs/2411.00028)** · composite 23.3 · _flagged needs_review (low confidence / novelty / relevance)_
  LLM-agents plus KG meta-path selection can replace hand-crafted feature extraction for graph-based prediction. Pattern is transferable but the paper itself is domain-specific.
- **[CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM](https://arxiv.org/abs/2504.17584)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Hardware-systems work on cheaper long-context inference; interesting for LLM infra cost curves but no direct security or agent-design content.
- **[Dual-Node NVIDIA DGX Spark over Tailscale: A Remote-Access Testbed for Distributed LLM Training and Cyber-Threat-Intelligence Fine-Tuning](https://arxiv.org/abs/2608.07226)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A tiny CTI-only SFT dataset (77 advisories) narrowly shifts a judge score (2.06 to 2.29 on 0-10) while regressing general-knowledge categories, a familiar catastrophic-forgetting…
- **[GitHub Models is now retired](https://simonwillison.net/2026/Aug/9/github-models-is-now-retired/#atom-everything)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A subsidized-token product died because agent workloads outgrew the subsidy. Reinforces that free/cheap LLM APIs bundled into developer platforms are not a durable dependency,…
- **[LoCA: Spatially-Aware Low-Rank Convolutional Adaptation of Vision Foundation Models](https://arxiv.org/abs/2607.06918)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  PEFT method paper for vision foundation models. No adversarial, agentic, or supply-chain angle; not relevant to the AI-security lane beyond generic ML fine-tuning literacy.
- **[Robust Average-Reward Markov Decision Processes: Minimax-Optimal Learning via Plug-in Reductions](https://arxiv.org/abs/2608.06545)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Pure RL theory result; no direct security implication for AI systems.
- **[SCALE: Scientific Concept Aggregation via LLMs and Embeddings for Fine-Grained Taxonomy Extension](https://arxiv.org/abs/2608.07254)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  LLM + embeddings + graph community detection can compress noisy author-keyword vocabularies into a stable intermediate 'Concept' taxonomy layer between Topics and documents.
- **[SignVerse-2M: A Two-Million-Clip Pose-Native Universe of 55+ Sign Languages](https://arxiv.org/abs/2605.01720)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Sign-language dataset release; no security or agent-engineering angle. Track only if you build pose-conditioned multimodal pipelines.
- **[Tensor Network Kernel Machines: A JAX Framework for Machine Learning and Nonlinear System Identification](https://arxiv.org/abs/2608.07043)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Open-source JAX kernel-methods library; not security-relevant.
- **[Beyond Post-Hoc Temperature Scaling: Bilevel Optimization for LLM Calibration](https://arxiv.org/abs/2608.07419)** · composite 22.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Preference-aligned LLMs are overconfident and post-hoc temperature scaling does not transfer across domains; training-time entropy-maximization via bilevel optimization offers…
- **[Certified Feedforward Tracking for Unknown Nonlinear Systems via Invertible Neural Networks](https://arxiv.org/abs/2608.06419)** · composite 22.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Invertibility plus conformal prediction can reduce data-driven control certification to a surrogate-modeling problem with probabilistic tracking-error guarantees.
- **[Residual Algebra for Representation-Preserving Learning](https://arxiv.org/abs/2608.07349)** · composite 22.4 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Domain-specific quantitative-finance learning method; no security relevance.
- **[Human-Centered Explainable AI for TinyML Edge Devices: A Pareto-Based Selection Framework with LLM-Guided Design](https://arxiv.org/abs/2608.07091)** · composite 22.1 · _flagged needs_review (low confidence / novelty / relevance)_
  The 'LLM as preference-to-method mapper, then deterministic filter + Pareto' pattern is a reasonable design-space technique but has no security posture attached.
- **[MAC: A Conversion Rate Prediction Benchmark Featuring Labels Under Multiple Attribution Mechanisms](https://arxiv.org/abs/2603.02184)** · composite 22.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Recommender/ad-tech benchmark for multi-attribution CVR prediction. Off-topic for the security research feed.
- **[PHOENIX: Fine-Tuned SLM-Powered Autonomous Satellite Lifetime Extension via Predictive Self-Healing and Multi-Agent AI Recovery](https://arxiv.org/abs/2608.07126)** · composite 22.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Interesting multi-agent orchestration case for constrained-connectivity edge deployment, but no security posture, threat model, or measured harness lessons transferable to…
- **[Certified Interpolation Oversampling: Per-Instance Safety Guarantees for Imbalanced Learning](https://arxiv.org/abs/2501.15790)** · composite 21.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Despite the word 'safety' in the title, this is a class-imbalance oversampling paper; the certified property is a geometric distance from the majority class, unrelated to…
- **[Dependency Parsing Across the Resource Spectrum: Evaluating Architectures on High and Low-Resource Languages](https://arxiv.org/abs/2605.02608)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  In low-resource regimes, simpler (LSTM) architectures can outperform pretrained transformers on syntactic tasks. Useful reminder that 'transformer everywhere' is not a default,…
- **[Fast and Accurate: An Adaptive VLA Inference Framework through Environment-aware Model Selection](https://arxiv.org/abs/2608.06434)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For embodied dual-system architectures, RL-based environment-aware switching between decoupled slow and fast modules can preserve success rate while sharply raising control…
- **[FedDOSE: Federated Learning Framework Decomposing Site Effects for Modeling Brain Dynamic Functional Connectivity](https://arxiv.org/abs/2608.07393)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Medical-imaging federated learning method. Federated learning is only tangentially adjacent to AI privacy/security here; nothing new about privacy attacks or defences is claimed.
- **[MAUPITI: On-Device Prototype-Based Learning on a Smart Infrared Sensor](https://arxiv.org/abs/2608.07192)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For ultra-constrained embedded ML, prototype-based streaming updates on a quantized frozen encoder buy continual adaptation at negligible latency and memory cost.
- **[MEDLEY-BENCH: Benchmarking Behavioural Metacognition and Belief Revision Under Social Pressure in Large Language Models](https://arxiv.org/abs/2604.16009)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Sycophancy/belief-revision-under-pressure varies wildly across models, and the benchmark authors themselves caution the current v1.0 results are not evidence of a stable absolute…
- **[MaskFlow: Precise, Consistent and Seamless Regional Image Editing](https://arxiv.org/abs/2608.06929)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Diffusion/flow-matching image-editing paper with no direct security or agent-harness angle.
- **[Neurai-VN Benchmark: Standardized Machine Learning Models for Multimodal Digital Phenotyping in Mental Health Classification](https://arxiv.org/abs/2607.25232)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specific benchmark for mental-health digital phenotyping; no AI/product security implications beyond standard privacy concerns for sensor data, which the paper does not…
- **[Optimal Neural Network Approximation via Empirical Least Squares with Deterministic Samples](https://arxiv.org/abs/2608.06687)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Pure approximation theory for neural networks solving PDEs on the sphere; no security or agent-engineering content.
- **[PACE: Primitive-Aware Code Evolution for Automated Algorithm Design](https://arxiv.org/abs/2608.07395)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Code-evolution research about preserving reusable snippets across LLM search — no security angle.
- **[Representation Handoffs for OpenArm-Based Laboratory Mobile Manipulation](https://arxiv.org/abs/2608.07154)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Constraining language requests to a registered skill vocabulary with dry-run traces is a reasonable pre-execution validation pattern; the paper frames it as debugging, but it is…
- **[When GNNs Fail: Quantifying and Overcoming Temporal Correlation Volatility in Time Series](https://arxiv.org/abs/2608.07333)** · composite 21.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Time-series forecasting result with no direct AI-security relevance despite the batch's guess_topic label.
- **[Hyperbolic Graph Embedders for Link Prediction and Topology Reconstruction](https://arxiv.org/abs/2608.07029)** · composite 20.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Choose a hyperbolic embedder by paradigm (maximum-likelihood, representation-learning, hybrid) and target network regime, not by disciplinary origin; expect regime-specific…
- **[Improving Attributed Long-form Question Answering with Intent Awareness](https://arxiv.org/abs/2603.27435)** · composite 20.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Intent tags for citation/writing behavior appear to help long-form report quality more for small distilled models than for large ones.
- **[Synthetic LiDAR Data Generation and Deterministic Downsampling for Point Cloud Classification on the Edge](https://arxiv.org/abs/2608.07106)** · composite 20.9 · _flagged needs_review (low confidence / novelty / relevance)_
  For edge 3D perception, sensor-aware synthetic training data and deterministic feature-driven downsampling replace expensive distance-sorting preprocessing while preserving usable…
- **[Towards a Theoretical Understanding of Two Tower Recommendation Models](https://arxiv.org/abs/2403.00802)** · composite 20.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Theoretical treatment of two-tower recommender convergence. Off-topic for AI security work.
- **[Weak Adversarial Neural Pushforward Method for Boltzmann Equation](https://arxiv.org/abs/2608.06823)** · composite 20.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Physics-informed neural PDE solver; not relevant to AI security.
- **[A primer on optimal transport for causal inference with observational data](https://arxiv.org/abs/2503.07811)** · composite 20.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Optimal-transport formulation is a unifying lens for counterfactual estimation, but this is a survey primer; no direct engineering artifact.
- **[Scalable High-Fidelity Macromolecular Docking for GPU-Accelerated Supercomputers](https://arxiv.org/abs/2608.07078)** · composite 20.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Pure HPC docking optimization work; no AI-security relevance whatsoever.
- **[Cascading Through the Hierarchy: Regularizer-Induced Feature Detection as Phase Transitions in Deep Linear Neural Networks](https://arxiv.org/abs/2608.06597)** · composite 20.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Feature emergence in a solvable deep-linear model can be described as a cascade of regularizer-driven phase transitions, providing a statistical-physics-style order-parameter…
- **[Machine Learning-Based Inter-Crystal Scatter Recovery for Ultra-High Resolution PET Imaging](https://arxiv.org/abs/2608.07155)** · composite 20.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Feed-forward NN-based ICS event recovery restores sensitivity in ultra-high-resolution PET without the resolution penalty of conventional acceptance strategies, enabling reduced…
- **[Alignment has a Fantasia Problem](https://arxiv.org/abs/2604.21827)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Position paper, no measurements. Frames a real UX failure mode (assistants finishing tasks users haven't finished thinking about) as an alignment problem. Interesting frame but no…
- **[An Agentic Hybrid Top-Down and Bottom-Up Approach to Knowledge Graph Generation](https://arxiv.org/abs/2608.07023)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Interesting KG-grounded agent architecture for a narrow HR use case, but no security threat model or defender pattern; not action-relevant for AI-security briefings.
- **[Embedded Variational Neural Stochastic Differential Equations for Learning Heterogeneous Dynamics](https://arxiv.org/abs/2604.00669)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specific socioeconomic time-series paper with no security angle; useful only as a reference for probabilistic latent-dynamics modeling, not for the ai-security or…
- **[Is SwiGLU's Open Positive Tail Necessary? Evidence from Closed-Tail Gating with MemGLU](https://arxiv.org/abs/2608.07323)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Gate geometry choice may matter less than assumed for FFN performance at small scales, but does not appear to have any security-engineering relevance.
- **[SQLite compressed text-history prototypes](https://simonwillison.net/2026/Aug/9/sqlite-text-history-prototype/#atom-everything)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Neat compression ratio for revision-history storage, plus an incidental data point on voice-conversation-driven long-horizon code generation. Not security-relevant.
- **[A foundation-model approach to pediatric headache classification from rs-fMRI](https://arxiv.org/abs/2608.07287)** · composite 19.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Under small-data medical conditions, a pretrained rs-fMRI foundation model can beat hand-engineered functional-connectivity features on binary headache classification, but subtype…
- **[Beyond Foundation Models: Dimension-Aware Neural Architecture Search with Small-Data Representation Models for Cryocooler Lifetime Prediction](https://arxiv.org/abs/2608.06993)** · composite 19.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Time-series industrial-ML paper. Not applicable to a security-engineering briefing.
- **[Beyond Isolation: Unlocking Reinforcement Learning Component Synergy for Sample-Efficient Continuous Control](https://arxiv.org/abs/2608.07086)** · composite 19.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Classical RL methodology; not applicable to LLM-agent security work.
- **[Cluster Attention for Graph Machine Learning](https://arxiv.org/abs/2604.07492)** · composite 19.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Community-based cluster attention widens receptive field for graph nets while preserving topology-aware inductive bias.
- **[Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317)** · composite 19.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Applied robotics work with a light multi-agent framing. Multi-agent here means resource coordination between robot subsystems, not the security-relevant sense of orchestrated…
- **[UAV3DCrop: Benchmarking 3D Reconstruction in Repeated Multi-Angle UAV Crop Surveys](https://arxiv.org/abs/2608.06404)** · composite 18.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Modern 3D reconstruction methods that look strong on generic benchmarks are not yet interchangeable for agronomic use; strong rendered appearance often hides scale failures that…
- **[Beyond Co-Movement: Locality by Exposures Enables a Joint Factor-Graph Framework for Portfolio Diversification](https://arxiv.org/abs/2608.06618)** · composite 18.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Portfolio construction gains by redefining graph locality via factor exposures rather than pairwise correlations, unifying factor and graph views under a single ADMM optimization.
- **[Homebot: A Personal AI Agent for Conversational Home Assistance and Automation](https://arxiv.org/abs/2608.02254)** · composite 18.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Systems paper describing a home-assistant agent architecture. Nothing methodologically novel; the design choice of scoping session state to channel vs. wake-word window is a…
- **[Wasserstein Policy Gradient for Entropy-Regularized Linear-Quadratic Control](https://arxiv.org/abs/2608.07433)** · composite 18.5 · _ungrounded excerpt — only 50% of quotes verified against the source_
  Theoretical RL/control result; no security implications.
- **[LSEAD: A Privacy-Preserving LLM-Based Speech Analysis Framework for Early Alzheimer's Disease Screening](https://arxiv.org/abs/2608.07378)** · composite 17.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Health screening pipeline whose 'privacy' story is 'run the LLM locally' — no adversarial or governance content, minimal security signal.
- **[Momba: Network Modernization Improves Multi-Objective Reinforcement Learning](https://arxiv.org/abs/2608.07180)** · composite 17.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Architecture-side gains in multi-objective RL; not relevant to AI-security briefings.
- **[Reading Copom's Tone: A Weighted LLM Framework for Hawkish-Dovish Sentiment, Forward Guidance, and Uncertainty](https://arxiv.org/abs/2608.07251)** · composite 17.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The paper is a domain-specific finance-NLP pipeline (LLM-scored sentence sentiment plus a document-level guidance/uncertainty overlay) with limited direct relevance to security or…
- **[International Transfer of Stochastic Cortical Self-Reconstruction](https://arxiv.org/abs/2608.07092)** · composite 16.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specific medical ML transfer study; not relevant to AI-security briefings.
- **[Representation-driven Endoscopic Visual Embedding Alignment for Latent Generation](https://arxiv.org/abs/2608.07176)** · composite 16.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Domain-specific medical generative model; not relevant to AI-security briefings.

---

<sub>Generated by scripts/generate_review.py on 2026-09-09. 221 item(s) awaiting review.</sub>
