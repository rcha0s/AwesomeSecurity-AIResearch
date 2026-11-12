# 🔍 Review Queue

> Everything held back from the site, with the reason. Findings that are **not yet vetted** (low confidence/novelty/relevance, or below the composite floor (20)), and news stories whose excerpt is not grounded in its source. Nothing here is deleted; promote a finding by raising its scores or clearing `needs_review`, or fix a news story's excerpt, then regenerate.

_Updated 2026-11-12._

## AI Security (59)

- **[Researchers find no agent framework defends against MCP tool poisoning](http://arxiv.org/abs/2611.03555v1)** · composite 70.6 · _failed independent verification — Lessons hold, but the verifier put novelty at 42 vs 70: MCP tool poisoning is well covered; the delta is the cross-framework measurement. It also flagged the takeaway's 'only defenses measured to matter' as overstating the abstract._
  Do not expect your agent framework to stop poisoned MCP tool metadata; model choice and your own controls are the only defenses measured to matter.
- **[OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident)** · composite 66.0 · _news story: excerpt not grounded in source (only 75% of quotes verified)_
  Treat a model eval with production classifiers off as a live agent that may try to escape, where a package-manager proxy is a plausible sandbox-escape primitive.
- **[Apiiro finds Claude Code permission allowlists leak secrets into public GitHub repos](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)** · composite 63.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat agent permission files, transcripts and memory files as secret-bearing like .env, and approve command patterns that reference $VARS rather than literal commands with secrets…
- **[Poisoned reference answers can plant backdoor rules in optimized agent Skills](http://arxiv.org/abs/2611.09348v1)** · composite 59.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Whoever controls the reference answers used to optimize a Skill can plant a hidden trigger rule in it without touching the model, the optimizer or the Skill file, so treat that…
- **[Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585)** · composite 59.1 · _news story: excerpt not grounded in source_
  The critical attack surface for agent apps is the framework layer around the model, where old bug classes get re-exposed as prompt-injected code paths — not the model's ability to…
- **[ai-dfir-toolkit ships open detection rules and forensic artifacts for AI attacks](https://github.com/depalmar/ai-dfir-toolkit)** · composite 58.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Defenders get a free, open-format starting set of AI-specific detections and a triage artifact list for agent hosts, but must tune them, since the README shows no measured…
- **[ShadowBench-MCP: task-preserving rewordings can push an LLM tool router onto riskier paths](http://arxiv.org/abs/2611.11720v1)** · composite 57.4 · _flagged needs_review (low confidence / novelty / relevance)_
  If an LLM chooses which tools run, mandatory safety steps should be enforced outside the router, and the routing prompt should state security policy, not just efficiency.
- **[LeanGuard checks every agent tool call against a Lean4-verified policy](https://arxiv.org/abs/2611.02332)** · composite 55.96 · _flagged needs_review (low confidence / novelty / relevance)_
  A deterministic, history-aware policy check in front of tool execution stops forbidden actions regardless of what the model was tricked into proposing, at little cost to task…
- **[Human reviewers miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)** · composite 53.7 · _news story: excerpt not grounded in source_
  Human-in-the-loop is a fatigue-limited primitive: engineer approvals as classifier + sandbox + hooks, not as a UX prompt.
- **[Anthropic Fellows find Claude agent teams rarely catch a teammate told to sabotage](https://www.anthropic.com/research/project-eve-claude-plays-mmorpgs)** · composite 53.62 · _failed independent verification — All lessons supported, but the verifier rated novelty 30 vs 62: a live multi-agent game demo of known prompted-sabotage capability (SHADE-Arena-style evals)._
  In multi-agent systems, an agent's reports and proposals are untrusted input, and peer agents are not a reliable sabotage detector.
- **[MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027)** · composite 53.1 · _news story: excerpt not grounded in source_
  MCP's enterprise turn adds iss validation and a stateless design that removes one session-poisoning surface but leans on standard load-balancer trust boundaries.
- **["Black October" is an X label for a week of disclosures](https://forkast.news/black-october-is-a-disclosure-wave-the-label-hides-the-clock/)** · composite 52.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Read the label as a backlog of old defects being dated, not as one new attack; the AI angle is faster discovery and AI credentials as loot.
- **[Logit Laundering lets LLM providers hide training-data watermarks at inference time](http://arxiv.org/abs/2611.09446v1)** · composite 52.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Watermark-based data-use audits that only query model outputs can be defeated by a dishonest provider, so they are weak evidence on their own.
- **[Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1)** · composite 52.05 · _flagged needs_review (low confidence / novelty / relevance)_
  Before picking a guardrail classifier by benchmark score, ask which policy its labels encode, whether the benchmark leaked into training, and what the seed-to-seed variance is, or…
- **[Agent Name Service spec anchors AI agent identity to verified domain names](https://github.com/agentnameservice/ans-spec)** · composite 51.51 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent-to-agent trust needs identity tied to a verified domain and to the running code version, not just a name.
- **[OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/)** · composite 51.0 · _news story: excerpt not grounded in source_
  Rogue-agent incidents are foundational-security failures with known fixes: zero-trust boundaries, isolated eval hosts, egress control and active monitoring.
- **[Brazilian labor court fines lawyers for hidden prompt injection in a filing](https://jetstream.security/insights/brazilian-court-sanctions-prompt-injection-filing/)** · composite 49.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Hidden-text injection in documents from outside parties is now a sanctionable act in at least one court, and any pipeline that has AI read outside documents should check for…
- **[Adan Alvarez tested which AWS attacks 14 LLMs propose with stolen keys](https://medium.com/@adan.alvarez/i-gave-14-llms-aws-keys-heres-what-they-wanted-to-do-next-48585761a11b)** · composite 48.75 · _failed independent verification — Medium returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the article._
  If LLM-driven attackers open with predictable AWS calls, those calls can become detections.
- **[Data-void exploits put attacker content in 31% of web-searching LLM answers](http://arxiv.org/abs/2610.30365v1)** · composite 47.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Web-search grounding is an input channel attackers can write to, especially on niche topics, so answers on such topics need signals about how thin or reliable the sources are.
- **[MLflow servers without authentication can be hijacked through third-party scorer loading](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)** · composite 47.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  If you run MLflow 3.12.0 or later, never expose it without authentication, and track the advisory for a fixed version.
- **[Red-Team AI reads an agent app's source code to tailor attacks](https://github.com/votal-ai-hq/ai-red-teaming)** · composite 46.52 · _flagged needs_review (low confidence / novelty / relevance)_
  Feeding a red-team tool your agent's source finds tool-chain paths that black-box prompt lists miss.
- **[SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062)** · composite 46.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent policy enforcement, prefer a compiled program of narrow predicates over one guardrail model or one LLM judge: cheaper, steadier and auditable (authors' claims, abstract…
- **[SkillCODER fingerprints agent skill files to trace leaks to a buyer](http://arxiv.org/abs/2611.11308v1)** · composite 46.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Sellers of proprietary skills can embed per-buyer traceable marks, but the mark is itself a hidden conditional instruction that a skill reviewer should know to look for.
- **[AgentLint checks coding-agent file writes and shell commands through local hooks](https://github.com/mauhpr/agentlint)** · composite 45.51 · _flagged needs_review (low confidence / novelty / relevance)_
  Hook-based linting of agent actions catches common mistakes cheaply, but treat it as feedback, not as a security boundary.
- **[Innovaccer's Healthcare MCP extension binds tool calls to an opaque patient handle](https://github.com/innovaccer/Healthcare-MCP)** · composite 45.25 · _failed independent verification — The verifier found lesson 2 and the takeaway overstated the default exposure; they now say token verification is opt-in but patient-scoped calls fail closed by default._
  Healthcare MCP (HMCP) offers a useful per-patient scoping pattern for MCP, but its auth is opt-in and its guardrails best-effort, and the README says the building blocks do not by…
- **[Agent Mosaic: LLM agents combine allowed documents into forbidden conclusions](https://arxiv.org/abs/2610.30418)** · composite 44.73 · _flagged needs_review (low confidence / novelty / relevance)_
  Document-level access control is not enough for agents serving users with mixed clearances, because the model can derive restricted conclusions from documents each user may read.
- **[hoop.dev ships a wire-level sidecar that masks data and blocks agent SQL](https://github.com/hoophq/hoop)** · composite 43.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Putting data controls on the database wire, not in the prompt, is a sound pattern; check which hoop features are actually built before relying on it.
- **[Goldman Sachs limits Claude Code and GitHub coding tools to engineers](https://www.thestateofai.com/news/goldman-sachs-claude-code-traders-bankers)** · composite 42.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Code that non-engineers build with agents needs a named engineering owner and the same review, entitlement and information-barrier controls as any other code.
- **[Edge grounding VLMs fall to wearable adversarial patches like detectors](http://arxiv.org/abs/2610.29196v1)** · composite 41.55 · _flagged needs_review (low confidence / novelty / relevance)_
  When red-teaming vision models in safety-critical systems, score where the box lands, not just whether one exists.
- **[Snyk Agent Scan finds and scans local agents, MCP servers and skills](https://github.com/snyk/agent-scan)** · composite 41.02 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent Scan gives a quick inventory of agent supply-chain risk on a machine, but the scan itself can run code and send data out, so plan for that.
- **[LMCache multiprocess mode's unauthenticated ZeroMQ endpoint gives remote code execution](https://github.com/advisories/GHSA-w5f2-9q9c-ff4h)** · composite 40.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat every internal transport in an LLM serving stack as a network attack surface: if it unpickles socket data with no authentication, anyone who can reach the port can run code…
- **[Cisco AI Defense mcp-scanner checks MCP servers with YARA, LLM and API engines](https://github.com/cisco-ai-defense/mcp-scanner)** · composite 40.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Use mcp-scanner as a gate when admitting MCP servers, but remember that scan-time checks do not prove anything about runtime authorization.
- **[Agent Plugins spec adds a 1.1.0 working draft to its packaging standard](https://github.com/agentplugins/agent-plugins-spec)** · composite 39.34 · _failed independent verification — Verifier: the README cannot show that the 1.1.0 draft is the only change since the 2026-08-10 entry, and lesson 2's trust-and-consent reading goes beyond the source._
  A plugin bundles skill prompts and MCP server configs into one artifact, so review and pin it as one supply-chain unit; this README update adds no new security content.
- **[Agno agent framework ran Python eval on a function call's field type](https://github.com/advisories/GHSA-m4w4-3r8h-jw98)** · composite 37.35 · _failed independent verification — Novelty disagreement: verifier rated 12 against my 35 (a routine eval-injection bug class, cf. LangChain CVE-2023-29374). It also noted the tool/model-output path is only an example and the advisory does offer a partial workaround._
  An agent framework that evals strings shaped by model output turns prompt injection into code execution, so upgrade Agno and search your agent code for eval on schema fields.
- **[MCP specification repository now points to a 2026-07-28 schema revision](https://github.com/modelcontextprotocol/modelcontextprotocol)** · composite 37.24 · _flagged needs_review (low confidence / novelty / relevance)_
  Check MCP clients and servers against the 2026-07-28 schema; the README itself carries no new security content.
- **[mcp-openapi-server exposes OpenAPI endpoints to agents as MCP tools](https://github.com/ivo-toby/mcp-openapi-server)** · composite 36.89 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful OpenAPI-to-MCP bridge, but its filters narrow what the model sees, not what it can do; keep authorization in the API.
- **[MSafeTemp authors show English-only safety evaluation misses multilingual jailbreaks](https://arxiv.org/abs/2610.40516)** · composite 36.69 · _flagged needs_review (low confidence / novelty / relevance)_
  If your product serves non-English users, refusal testing done only in English leaves translated and localized jailbreaks untested.
- **[humanbound-firewall screens every input to an agent by who authored it](https://github.com/humanbound/humanbound-firewall)** · composite 36.57 · _flagged needs_review (low confidence / novelty / relevance)_
  The useful idea is to label every model input by author (request, outside content, own records); treat the tool as a preview filter, not a security boundary.
- **[mcp-watch is an open-source static scanner for MCP server repositories](https://github.com/kapilduraphe/mcp-watch)** · composite 36.33 · _flagged needs_review (low confidence / novelty / relevance)_
  Another unevaluated MCP repository scanner; trial it beside established scanners rather than relying on it.
- **[United Airlines bans third-party AI agents from booking flights for travelers](https://www.cbsnews.com/news/united-airlines-bans-ai-agents-booking-flights/)** · composite 36.25 · _failed independent verification — The verifier found lesson 1 inferred (platform cannot tell agent from owner); it now states only the risks United cites, and the summary and takeaway were trimmed to the source._
  United is blocking credential-sharing AI agents, which pushes agent builders toward scoped, sanctioned access instead of password reuse.
- **[NuGuard is an open-source AI-SBOM and red-team pipeline for agentic apps](https://github.com/NuGuardAI/nuguard)** · composite 35.14 · _flagged needs_review (low confidence / novelty / relevance)_
  It is a candidate all-in-one CI red-team harness for agent apps. It's young (67 stars), so treat the comparison claims as unverified marketing until you've benchmarked it against…
- **[openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator)** · composite 35.07 · _ungrounded excerpt — only 75% of quotes verified against the source_
  Auto-generated MCP servers expose your whole API to an agent by default, so filter operations and turn on inbound auth before you deploy one.
- **[AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422)** · composite 33.87 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a training-time hardening approach for agent model builders that does not replace runtime containment, and the abstract gives no figures to judge how large the gain is.
- **[mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6)** · composite 33.75 · _failed independent verification — Refuted: the saved source holds only generic CVSS definitions, so the SQL injection, version range and Databricks details are unsupported by it. Needs a re-fetch of the advisory._
  Agent memory content is attacker-influenced input, so memory backends must use parameterized queries like any other data layer.
- **[mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins)** · composite 33.57 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat a Jenkins MCP server as code execution on your CI: give it a token without script rights, enable read-only mode, and keep it off the network.
- **[OpenGuardrails proposes one vendor-neutral wire protocol for agent guardrails](https://github.com/openguardrails/openguardrails)** · composite 32.67 · _flagged needs_review (low confidence / novelty / relevance)_
  A common guardrail interface could cut integration work, but its fail-open default means an attacker who can block the runtime turns the guardrail off.
- **[Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus)** · composite 32.25 · _flagged needs_review (low confidence / novelty / relevance)_
  If your LLM app keeps client-controlled chat history, test it with multi-turn and backtracking attacks, not just single-prompt jailbreak lists.
- **[LLMVault offers a self-hosted training range for OWASP LLM Top 10 attacks](https://github.com/CyberSunil/LLMVault)** · composite 32.03 · _flagged needs_review (low confidence / novelty / relevance)_
  A hands-on teaching range for LLM attack classes, already covered in an earlier entry and not a source of new findings.
- **[Microsoft says Gartner named it a leader in agent management platforms](https://www.microsoft.com/en-us/security/blog/2026/11/03/microsoft-named-a-leader-in-the-2026-gartner-magic-quadrant-for-ai-agent-management-platforms/)** · composite 31.97 · _flagged needs_review (low confidence / novelty / relevance)_
  This is vendor marketing whose only reusable idea is to keep an inventory of agents, each with its own identity and a named owner.
- **[Microsoft frames agents as insiders and announces Dynamic Permissions and Guardian Agents](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/)** · composite 31.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Graduated containment is a useful design pattern to copy: when agent risk rises, keep reads, revoke writes, require approval, then isolate. Treat the rest as vendor positioning.
- **[Tamga's prompt-injection rules caught 27 of 203 attacks written by others](https://github.com/yatuk/tamga)** · composite 29.84 · _failed independent verification — Lessons hold, but the verifier judged novelty 18 vs 45: the held-out collapse of phrase-matching injection filters is known (e.g. Hackett et al. 2025 on bypassing guardrail detectors); Tamga's two held-out sets are small and Turkish-only._
  Tamga's own numbers show a wording-based injection filter catching few attacks that someone else wrote, so test any such filter on independent attack sets.
- **[MCP ZAP Server blocks private-network targets and binds scan credentials server-side](https://github.com/dtkmn/mcp-zap-server)** · composite 28.17 · _flagged needs_review (low confidence / novelty / relevance)_
  If you expose a scanner or other outbound tool to agents, block internal destinations by default and keep credentials server-side behind opaque profile IDs, so the agent chooses…
- **[Microsoft tells CISOs to put agent identity and data controls first](https://www.microsoft.com/en-us/security/blog/2026/10/28/the-cisos-evolving-role-protecting-and-defending-in-the-agentic-era/)** · composite 27.09 · _flagged needs_review (low confidence / novelty / relevance)_
  Familiar guidance (inventory agents, give each one its own least-privilege identity, classify the data it can reach), and the 15-fold growth figure is the only new data point.
- **[NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp)** · composite 26.77 · _flagged needs_review (low confidence / novelty / relevance)_
  Mostly a generic MCP wrapper. The useful part is a documented example of an unauthenticated localhost MCP endpoint left open to DNS rebinding by default.
- **[CollieAi's LLM Firewall filters prompts and responses through a hosted proxy](https://github.com/CollieAi/llm-firewall)** · composite 26.59 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a routine filtering proxy with no published detection rates, so treat it as one containment layer, not as a fix for prompt injection.
- **[Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/)** · composite 25.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A self-hosted LLM gateway gives per-agent key isolation and an audit trail, but it also concentrates every provider key in one place and has to be hardened accordingly.
- **[Anthropic's Security news page is an index of security announcements](https://www.anthropic.com/news/security)** · composite 14.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Useful only as a pointer. The linked incident and threat-report posts carry the substance.
- **[MCP TypeScript SDK HTTP servers set no limit on request body size](https://github.com/advisories/GHSA-f897-62hf-6gxq)** · composite 10.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  MCP servers exposed over HTTP can be overloaded by oversized or batched requests until the SDK is updated.
- **[Check Point: infostealer adds collection routines for AI desktop apps](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/)** · composite 8.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  AI desktop apps and coding tools now sit next to browsers and wallets on infostealer target lists, so their tokens and data need the same protection.

## Product Security (70)

- **[Malicious native apps can hijack browser Native Messaging to steal password vaults](http://arxiv.org/abs/2611.04291v1)** · composite 61.9 · _flagged needs_review (low confidence / novelty / relevance)_
  If your extension talks to a native helper, authenticate and encrypt that channel yourself; the browser does not.
- **[Apache HTTP Server HTTP/2 race condition allows unauthenticated remote code execution](https://www.wiz.io/blog/cve-2026-119618-rce-apache-http-server-vulnerability)** · composite 60.51 · _failed independent verification — Verifier found the AI-discovery lesson unsupported (the source never says Anthropic used AI); lesson and tag removed, threat softened, held for a human check._
  Upgrade httpd to 2.4.71 or set 'Protocols http/1.1' now; no exploit is public yet, but the bug is pre-authentication remote code execution (RCE) in a ubiquitous server.
- **[Datadog traces the ARTEX agentic attack framework inside real AWS accounts](https://securitylabs.datadoghq.com/articles/artex-agentic-attacks-aws-environments/)** · composite 60.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Agentic attack tools leave repeatable, huntable habits in CloudTrail, but their cloud playbook depends on whatever model drives them, so hunt behavior rather than one fixed…
- **[Microsoft FORGE Lab finds soundness bugs in Rust's standard library](https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/)** · composite 59.74 · _flagged needs_review (low confidence / novelty / relevance)_
  Even Rust's standard library has soundness bugs of the three kinds the post names, and the authors say agents make the environment-dependent OS-boundary area practical to search.
- **[Microsoft sees attack agents turn leaked GitHub secrets into Azure breaches](https://www.microsoft.com/en-us/security/blog/2026/11/05/threat-actors-use-agentic-ai-tooling-to-find-and-abuse-exposed-secrets/)** · composite 58.03 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat any secret that reaches a public repository as compromised within minutes. Detect agentic attackers by their machine-speed retry behavior, not by IP addresses or user…
- **[PortSwigger turns its CRLF desync research into an automated Burp AT skill](https://portswigger.net/research/making-http-header-injection-critical-with-one-prompt)** · composite 53.44 · _flagged needs_review (low confidence / novelty / relevance)_
  Header injection findings used to be triaged as low severity, but tools can now escalate them to critical desyncs automatically, so they deserve full follow-up.
- **[Argus, an open-source security platform, has AI agents that only propose actions](https://github.com/thomasunise/argus)** · composite 52.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Argus is a concrete reference design for agentic SecOps, with read-only agents, a propose-only path to a policy broker, agent-targeted canaries and autonomy that is reversible and…
- **[Engineer lists three AWS IAM anti-patterns coding agents keep writing](https://engseclabs.com/blog/things-llms-get-wrong-about-aws-iam)** · composite 50.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Review agent-generated IAM for cargo-cult patterns: needless Deny, misused permissions boundaries and no-op GetCallerIdentity grants.
- **[Microsoft finds 78% of exploited CVEs are takeover-class bugs](https://www.microsoft.com/en-us/security/blog/2026/11/02/exploited-vulnerabilities-common-data-driven-analysis-real-world-attacks/)** · composite 50.02 · _failed independent verification — Lesson 3 attributes faster KEV listing partly to AI-assisted exploit development as Microsoft's finding; the post only says 'industry research suggests' it, and the timing figures come from CISA data._
  Prioritize takeover-class bugs on exposed, highly privileged servers and appliances first, because those are both the most exploited and the slowest patched.
- **[SenTrojan researchers hid analog hardware Trojans in sensors triggered by physical signals](http://arxiv.org/abs/2611.06103v1)** · composite 49.3 · _flagged needs_review (low confidence / novelty / relevance)_
  In safety-critical cyber-physical systems, a sensor's readings can only be trusted as far as its hardware supply chain can be trusted, and functional tests alone may not reveal an…
- **[Nuxt Content query endpoint lets unauthenticated users stall servers with SQLite functions](https://github.com/advisories/GHSA-xxrh-5hgg-gj4h)** · composite 49.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Any endpoint that accepts raw SQL from the browser needs an allowlist of exact query shapes, plus query time and memory limits, not a keyword denylist.
- **[Microsoft Outlook spoofing flaw that skips unsafe-action warnings is exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-124194)** · composite 48.89 · _failed independent verification — Verifier found two lessons went beyond the NVD text (phishing framing, auto-update advice) and a named November update the source lacks; text trimmed, held for a human check._
  Move every Outlook client to Microsoft's fixed builds for this CVE; it is an exploited spoofing bug that needs user interaction.
- **[VOLTA infostealer uses an LLM to rank victims' assets by value](https://blog.talosintelligence.com/appraisal-by-ai-model-driven-victim-prioritization-in-the-volta-infostealer/)** · composite 48.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Crimeware now uses LLMs as the analyst who decides which victims to work first, and is built to route around refusals.
- **[Callix finds 819 access-control flaws at sensitive callsites in Android firmware apps](http://arxiv.org/abs/2611.00594v1)** · composite 47.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Checking that an access check exists in original equipment manufacturer (OEM) firmware apps is not enough; judge whether it is strong enough for the data a generic call operates…
- **[SonicWall SonicOS SSLVPN flaw lets alternate credentials bypass SAML-enforced MFA](https://nvd.nist.gov/vuln/detail/CVE-2026-19868)** · composite 47.27 · _failed independent verification — The fetched source is only the KEV listing table; the SAML and MFA bypass mechanism in the summary, title and takeaway is not in it._
  Enforcing MFA through SAML on a SonicWall SSLVPN does not protect you if another login method on the same VPN still accepts just a password.
- **[@_rybaz and @GrahamHelton3 publish their vulnerability-research harness workshop materials](https://x.com/_rybaz/status/2119828361044246643)** · composite 46.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A pointer to public workshop material on building agent harnesses for vulnerability research; the content is unreviewed here, so read it before relying on it.
- **[Kat Traxler used AI and security principles to find cloud design flaws](https://github.com/KatTraxler/presentations/tree/main/security-constitution)** · composite 45.75 · _failed independent verification — Source page returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the talk itself._
  Pointing an AI at design principles, not bug classes, may surface design flaws that pattern-based hunting misses.
- **[Next.js has unauthenticated RCE in use cache functions returning typed arrays](https://github.com/advisories/GHSA-673q-mjm6-r5xr)** · composite 45.75 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Upgrade Next.js now if any `use cache` function returns typed arrays; there is no workaround.
- **[Backdoored fragment-api-py release drains users' crypto wallets when the client opens](https://safedep.io/blog/fragment-api-py-pypi-ton-wallet-drainer)** · composite 45.62 · _flagged needs_review (low confidence / novelty / relevance)_
  A package that holds secrets such as wallet seeds can steal them through a single version bump, so pin versions and treat untagged releases as suspect.
- **[StepSecurity launches scanning for files planted by supply chain campaigns](https://www.stepsecurity.io/blog/malicious-files-find-what-supply-chain-attacks-leave-behind-in-your-github-repositories-and-on-developer-machines)** · composite 45.52 · _flagged needs_review (low confidence / novelty / relevance)_
  Scan every ref, not just the default branch, for planted editor, agent and workflow files, because dependency scanners never see them.
- **[Cisco BroadWorks XML external entity flaw is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-20320)** · composite 45.14 · _flagged needs_review (low confidence / novelty / relevance)_
  Patch BroadWorks per Cisco advisory cisco-sa-bworks-xxe-uwUd7CEt; CISA lists the flaw as exploited.
- **[Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/)** · composite 44.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Run pathrunner in a sandbox (Pathfinding Labs) and use its CloudTrail report to test that every payload, not just one, trips a detection.
- **[Next.js Image Optimization has unauthenticated RCE via SVG through sharp](https://github.com/advisories/GHSA-2464-fhr4-w9xw)** · composite 44.25 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Pin a patched sharp under Next.js and consider disabling SVG optimization; image pipelines are unauthenticated RCE surface.
- **[Google declines to fix zero-click SMS that crashes Android telephony](https://smsofdeath.com/)** · composite 43.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Any Android device reachable by SMS can be knocked off telephony, emergency calling included, and the vendor treats it as a non-security bug with no fix scheduled.
- **[Google Cloud says Advanced Micro Devices (AMD) Turin VMs need guest patches](https://thehackernews.com/2026/11/google-cloud-warns-three-amd-turin-cpu.html)** · composite 43.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Google tells all affected Turin-based Google Cloud Platform (GCP) VMs to install the guest kernel fix and stop-and-start the VM; rebooting the guest OS is not enough.
- **[A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/)** · composite 42.22 · _news story: excerpt not grounded in source_
  Enclave-to-KMS attestation only closes the gap if you also hardcode the CMK ARN, attest the IAM role, and initiate TLS from inside the enclave; without that, active-attacker…
- **[Rikugan embeds a reverse-engineering agent inside IDA Pro and Binary Ninja](https://github.com/buzzer-re/rikugan)** · composite 41.85 · _flagged needs_review (low confidence / novelty / relevance)_
  An in-disassembler agent with parallel subagents and per-profile data and tool limits is a ready-made base for AI-assisted reverse engineering, but plan for hostile binaries…
- **[CISA adds 2024 Apple pointer authentication bypass to exploited catalog](https://nvd.nist.gov/vuln/detail/CVE-2024-27834)** · composite 41.27 · _failed independent verification — The fetched source is only the NVD reference table; it does not describe the pointer authentication bypass or say APT29 exploited this CVE, and the CVE is already covered by the Midnight Blizzard entry._
  Devices still on pre-mid-2024 Apple builds are exposed to a pointer authentication bypass that a nation-state group uses in exploit chains.
- **[America bans imported robots due to supply chain and security risks](https://www.theregister.com/security/2026/07/29/america-bans-imported-robots-due-to-supply-chain-and-security-risks/5280145)** · composite 40.5 · _news story: excerpt not grounded in source_
  US regulators are treating networked physical robots as a critical-infrastructure supply-chain risk category on par with telecom gear.
- **[X post claims Mirage2FA stole 4,561 Microsoft 365 session cookies](https://x.com/Dinosn/status/2116946099059511340)** · composite 40.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Adversary-in-the-middle proxies keep beating one-time-code multi-factor authentication; phishing-resistant sign-in is the fix, but this claim needs a primary source.
- **[A probability-scoring model matches employee accounts to one person at 0.95 F1](https://vincenzoiozzo.com/blog/jev-identity-resolution)** · composite 39.75 · _flagged needs_review (low confidence / novelty / relevance)_
  In identity governance (IGA) and identity-security products, a cheap probability model with a tuned cut-off, plus a frontier-model check only on the 'maybe' band, beats rules and…
- **[VibeRaven statically checks AI-built Supabase apps for row-level security gaps](https://github.com/ohad6k/VibeRaven)** · composite 39.51 · _failed independent verification — Verifier rated novelty 12 vs 45: the RLS, service_role and dashboard-blind-spot points are standard Supabase docs and Security Advisor lints; only the vendor's 512-repo statistic is new, and the push-to-main point is an unsupported README assertion._
  For AI-built Supabase apps, the common gaps are database authorization mistakes such as missing row-level security (RLS), anon-callable definer functions and leaked service_role…
- **[Semgrep Guardian adds an adversarial reviewer and blocks risky lockfile changes](https://semgrep.dev/blog/2026/semgrep-guardian-policies-ai-detection)** · composite 39.45 · _flagged needs_review (low confidence / novelty / relevance)_
  A product update that applies two known patterns to coding agents: an independent adversarial reviewer and write-time gating of lockfile changes. No efficacy data is given.
- **[SpecterOps announced Sage, an AI assistant for red teams inside Mythic](https://specterops.io/blog/2026/11/10/sage-ai-for-assumed-breach-operations-built-into-mythic/)** · composite 39.25 · _failed independent verification — Fetched page was an ad-tracker redirect with no article text; the summary rests on the feed teaser only._
  Unverified: refetch the SpecterOps post before relying on any description of Sage's human-approval or memory design.
- **[A client's 1-bit reply leaks the full CKKS secret key](http://arxiv.org/abs/2610.21127v1)** · composite 38.55 · _flagged needs_review (low confidence / novelty / relevance)_
  If you deploy homomorphic encryption with an untrusted server, any client behaviour the server can observe on decryption, such as errors, retries or a 1-bit validity signal, is a…
- **[CVM-Store paper protects confidential VM storage at near-raw disk speed](http://arxiv.org/abs/2610.34560v1)** · composite 38.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Running in a confidential VM does not protect data on disk; stored data needs its own integrity and rollback protection.
- **[Wiz scans every new npm version at publish time to catch compromises](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication)** · composite 36.6 · _flagged needs_review (low confidence / novelty / relevance)_
  CVE-based dependency scanning is blind to hijacked trusted packages; you need publish-time behavioral analysis or a cooldown before new versions reach builds.
- **[VibeRaven checks AI-built Supabase apps for missing row-level security](https://github.com/ohad6k/VibeRaven)** · composite 35.61 · _flagged needs_review (low confidence / novelty / relevance)_
  Vibe-coded Supabase apps fail in a handful of predictable ways, and a static check in CI can catch several of them before launch.
- **[raml-kql runs one KQL query across workspaces without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql)** · composite 35.25 · _flagged needs_review (low confidence / novelty / relevance)_
  MSSPs without a Defender MTO can hunt across customer Sentinel workspaces from one query with delegated access only.
- **[Plex CVE-2026-96652 SSRF lets the /player/timeline protocol parameter force server POSTs](https://nvd.nist.gov/vuln/detail/CVE-2026-96652)** · composite 35.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Upgrade Plex to 1.43.3.10861 or later: this endpoint turns the server into a POST relay with almost no authentication, and it is exploited in the wild as part of the plex2shell…
- **[Openwave Webtop Media Transcoder file-type restriction bypass is exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-111793)** · composite 34.64 · _failed independent verification — Verifier found the 'low score' label wrong (the vector computes to 4.3, Medium) and the UI-only enforcement mechanism inferred; text corrected, held for a human check._
  Operators of Openwave Webtop should upgrade the Media Transcoder to 1.1.22.0 and enforce file-type policy server-side.
- **[CISA KEV: Plex Media Server file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656)** · composite 34.12 · _failed independent verification — Source text not captured (NVD page empty); lessons rest on the KEV catalog text only._
  Treat the four Plex KEV CVEs as one chain and patch together.
- **[Russian hackers reportedly use stealthy Exchange malware against government email](https://cyberinsider.com/russian-hackers-cereal-malware-microsoft-exchange-attacks/)** · composite 34.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Only a headline is available, so wait for the full CyberInsider or vendor report before acting on it.
- **[macOS 27 breaks normal access to encrypted HFS+ volumes on CoreStorage](https://wadetregaskis.com/macos-27-golden-gate-does-not-actually-support-corestorage-or-hfs-volumes/)** · composite 33.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Migrate CoreStorage and encrypted HFS+ volumes to APFS before upgrading to macOS 27, and have backups ready.
- **[CISA says a low-severity VMware ESX logging gap is being exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-41709)** · composite 33.75 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Do not deprioritize low-CVSS ESX logging bugs: attackers who already hold admin access use them to hide what they do.
- **[Chainguard rebuilds every buildable Linux distribution font from source](https://www.chainguard.dev/unchained/this-shit-is-hard-nobody-has-ever-been-pwned-by-helvetica-or-have-they)** · composite 33.64 · _flagged needs_review (low confidence / novelty / relevance)_
  Container images and distributions ship prebuilt fonts that rendering libraries execute, so treat them as unverified binaries in the supply chain. The concrete payoff of building…
- **[Joost de Valk's open website specification covers security headers and agent readiness](https://github.com/jdevalk/specification.website)** · composite 33.3 · _flagged needs_review (low confidence / novelty / relevance)_
  A sourced, general web-standards checklist with a security section; useful as a reference, not new security research.
- **[Socket finds 319 Chrome extensions that hijacked searches through operator servers](https://www.malwarebytes.com/blog/news/2026/10/fake-pdf-and-search-tools-hijacked-searches-for-13-4-million-chrome-users)** · composite 33.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat an official-store listing as no trust signal for browser extensions, because unlisted, ad-promoted extensions can quietly proxy every search a user makes.
- **[Microsoft Research podcast profiles Cyber Grand Challenge lead Mike Walker](https://www.microsoft.com/en-us/research/podcast/learn-the-rules-the-hacker-mindset/)** · composite 32.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A career-profile podcast with little technical content, useful mainly as background on how autonomous hacking competitions began.
- **[Check Point weekly digest covers cPGuard supply-chain attack and ARTEX campaigns](https://research.checkpoint.com/2026/9th-november-threat-intelligence-report/)** · composite 32.78 · _flagged needs_review (low confidence / novelty / relevance)_
  A roundup with little new analysis; follow its links to the primary reports for anything actionable.
- **[Antithesis engineer Sean Allen says supply chain attacks have no simple fix](https://newsletter.pragmaticengineer.com/p/software-correctness)** · composite 31.38 · _flagged needs_review (low confidence / novelty / relevance)_
  Mostly a software-correctness conversation; its supply chain point (no simple fix) is a restatement with no new defense.
- **[Citizen Lab and Princeton researchers win IRTF prize for Android network security](https://citizenlab.ca/citizen-lab-researchers-win-irtf-applied-networking-research-prize/)** · composite 29.62 · _flagged needs_review (low confidence / novelty / relevance)_
  An award announcement with no new findings; read the underlying paper on proprietary encryption in Android apps instead.
- **[Northstar Security leaves stealth with $7M to find risky issue combinations](https://www.securityweek.com/northstar-security-exits-stealth-with-7m-to-expose-toxic-risk-combinations/)** · composite 29.32 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding announcement: the idea of scoring combined exposures, not single findings, is established, and the source has no results to judge.
- **[Iris Plaza says a cloud breach exposed data on 7.7 million customers](https://cyberinsider.com/iris-plaza-cloud-breach-7-7-million-people/)** · composite 28.75 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a thin breach notice with no root cause or lessons, so it is useful only as a data point.
- **[PHP2Shell hits every PHP since 5.4, no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/)** · composite 28.5 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run PHP 8.1 or older, there is no patch: upgrade to 8.2+ or put network-level protection in front now.
- **[Researcher reports Samsung Tizen runs AlexNet on screen captures to identify games](https://twitter.com/mike64_t/status/2114150399406202896)** · composite 28.5 · _flagged needs_review (low confidence / novelty / relevance)_
  When auditing TV/IoT firmware, check whether on-device ML screen capture runs before user consent, even if the output is dropped; here the evidence is a single unverified tweet.
- **[Brava Security raises seed funding for AI attack-telemetry simulation](https://www.securityweek.com/brava-security-emerges-from-stealth-with-15-million-in-funding/)** · composite 27.55 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a funding story, but its point holds: AI-driven SOC (security operations center) triage only covers what your detections actually fire on.
- **[Wiz says it is not yet listed on Japan's government cloud registry](https://www.wiz.io/blog/wiz-and-ismap-for-japan-public-sector)** · composite 27.55 · _flagged needs_review (low confidence / novelty / relevance)_
  For Japanese public-sector buyers, Wiz is not on the ISMAP list and will not be before its 2027 audit; otherwise this is vendor compliance news with no security findings.
- **[CISA KEV: SiteGuard Server Edition OS command injection exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931)** · composite 27.0 · _failed independent verification — Fetched NVD page was empty; the only lesson rests on the KEV catalog description and cannot be grounded in the saved source._
  If you run SiteGuard Server Edition, patch now: CISA lists this command injection as actively exploited.
- **[Microsoft's October 2026 Patch Tuesday fixes one exploited Windows Shell bypass](https://blog.talosintelligence.com/microsoft-patch-tuesday-for-october-2026/)** · composite 26.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Patch the exploited Windows Shell bypass and the AD DS and Exchange RCEs first, since the rest is a long routine list.
- **[Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/)** · composite 25.27 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated 'unpatched' (the source says 'did not indicate patched versions') and 'millions' (a reported figure). Text corrected; a secondary digest of already-covered stories._
  A news digest with nothing new, so use it as a checklist: PHP2Shell, LiteLLM 1.107.0, GitLab CVE-2026-110264, VeloCloud CVE-2026-114625, and AI-tool token theft.
- **[MagicSword markets automatic application-control policies built from LOLDrivers research](https://www.magicsword.io/application-control)** · composite 24.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Marketing for a product; the useful idea is blocking known-abused legitimate tools by default, which the free LOL catalogs already support.
- **[Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/)** · composite 24.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a public, live test of PHP2Shell exploitability; a non-zero hack counter would be a signal to speed up PHP patching, but the page itself contains no technical detail.
- **[GoSQLX, a Go SQL parser, ships an injection scanner and MCP server](https://github.com/ajitpratap0/GoSQLX)** · composite 23.01 · _flagged needs_review (low confidence / novelty / relevance)_
  A handy SQL parser with an agent interface, but nothing new for security; its injection scanner is unmeasured.
- **[Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise)** · composite 22.75 · _flagged needs_review (low confidence / novelty / relevance)_
  General incident-readiness advice that works as a checklist, with nothing new.
- **[Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto)** · composite 21.09 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated features (CI/CD and mirrored traffic partly Enterprise-only; SSRF and JWT tests only named as examples) and inferred JVM code execution. Text corrected; a vendor README with marketing tagline._
  A known open-source API-testing tool with an AI-security tagline, but its README shows no AI- or MCP-specific capability, so judge it as an API testing tool.
- **[Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8)** · composite 21.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A possible cross-runtime RCE is circulating, but this capture has no details; get the primary Aikido or vendor advisory before acting.
- **[Book claims Dutch government hacked Jared Kushner's phone, which Kushner denies](https://twitter.com/jaredkushner/status/2113376217415958767)** · composite 16.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a disputed political allegation with no technical content; treat it as unconfirmed news, not threat intelligence.
- **[CISA KEV: Plex Media Server SSRF exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96655)** · composite 11.94 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Any logged-in Plex user can make the server fetch arbitrary addresses, and attackers are chaining it with other Plex bugs.
- **[CISA KEV: Siemens Software Center DLL search-path flaw exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-110936)** · composite 10.44 · _ungrounded excerpt — only 0% of quotes verified against the source_
  A local attacker who can drop a DLL where Siemens Software Center looks for one gets code execution; CISA says this is being exploited.

## AI Research (88)

- **[How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/)** · composite 59.62 · _news story: excerpt not grounded in source (only 0% of quotes verified)_
  In AI bug hunting, outcome definition and per-agent scoping drive output quality most, with a threat-model file as the highest-leverage input.
- **[Anthropic tests which agent memory practices help Claude across sessions](https://www.anthropic.com/research/components-of-agent-memory)** · composite 59.02 · _failed independent verification — Lessons hold, but the verifier rated novelty 33 vs 68 (sleep-time compute, Karpathy's LLM wiki, Letta tiers) and flagged single-run evidence; the summary was corrected to keep the wiki-only caveat and the small search-plus-wiki gain._
  Tell the agent what memory is for, keep the always-loaded layer small, and regularly check notes against transcripts so wrong notes do not carry forward.
- **[ScrapeBench measures whether web agents honor terms of service and robots.txt](https://arxiv.org/abs/2611.11306)** · composite 51.77 · _flagged needs_review (low confidence / novelty / relevance)_
  The paper reports low compliance for most agents; as the tracker's recommendation, do not assume a web agent respects robots.txt or terms of service (ToS) on its own, enforce…
- **[Legora evaluates legal agent on simulated work because it cannot read traces](https://latent.space/p/building-ai-for-lawyers-jacob-lauritzen-cto-of-legora/)** · composite 50.44 · _flagged needs_review (low confidence / novelty / relevance)_
  When you cannot read customer traces, build simulated task worlds with domain experts and track results per task type, because a new model can regress on some tasks while…
- **[Apple researchers train small networks that speed up vector retrieval for RAG](https://machinelearning.apple.com/research/faster-retrieval)** · composite 49.12 · _flagged needs_review (low confidence / novelty / relevance)_
  If your RAG system serves a stable query distribution, a small learned query mapper can cut retrieval latency without replacing your vector index.
- **[Token-Goat hooks coding agents to cut repeat reads and bulky tool output](https://github.com/DFKHelper/token-goat)** · composite 48.58 · _flagged needs_review (low confidence / novelty / relevance)_
  Most agent token waste is repeat reads and noisy tool output, which hooks can trim without changing the model.
- **[Cisco's MAS Lab builds and traces multi-agent systems from YAML specs](https://github.com/ioc-project/mas-lab)** · composite 48.51 · _flagged needs_review (low confidence / novelty / relevance)_
  Keeping MCP and A2A in an adapter layer lets you test agent logic locally and review protocol security in one place.
- **[GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227)** · composite 46.77 · _flagged needs_review (low confidence / novelty / relevance)_
  If your harness edits skills automatically, assign credit by comparing repeated runs (group-relative), not by co-occurrence with success, or harmful skills will survive.
- **[DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522)** · composite 46.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate routers and guardrail judges on paired contrast cases, not only item accuracy.
- **[Anthropic study finds analysts follow an agent's hidden lean on judgment calls](https://www.anthropic.com/research/agents-judgment-calls)** · composite 45.78 · _flagged needs_review (low confidence / novelty / relevance)_
  If your harness relies on a human to make or check judgment calls, the agent's framing will often make the call instead, so design for that.
- **[Anthropic embeds METR with employee-like access but controls what is redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators)** · composite 45.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded third-party evaluation is now a concrete arrangement at one frontier lab; when you weigh its outputs, look at the redaction terms.
- **[Ratel loads agent tools and skills per turn through BM25 search](https://github.com/ratel-ai/ratel)** · composite 44.27 · _flagged needs_review (low confidence / novelty / relevance)_
  A packaged version of on-demand tool loading; the idea is not new and the repo was covered earlier, so evaluate it only if you need a drop-in library.
- **[Rubric Curriculum RL uses pairwise rubric judging to make reward hacking harder](http://arxiv.org/abs/2611.06244v1)** · composite 43.3 · _flagged needs_review (low confidence / novelty / relevance)_
  When an LLM judge grades open-ended output against a rubric, pairwise comparison with rotating criteria is more discriminative and harder to game than a fixed absolute score.
- **[Sean Goedecke argues Astra's weight editing matches what a skilled researcher would do](https://www.seangoedecke.com/llms-are-not-superhuman-at-reading-and-writing-neural-network-weights/)** · composite 42.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Read the weight-space-programming result as an LLM running a known interpretability-and-steering recipe, not as evidence that models can now improve other models better than…
- **[Handshake AI demos the agent benchmarks it builds for frontier labs](https://latent.space/p/handshake/)** · composite 42.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Grade agents on their tool-call trace and intermediate actions, not only the final answer, and test graders for gaming.
- **[Nvidia RTX Spark laptops throttle local LLMs on Linux when plugged in](https://www.mindstudio.ai/blog/linux-nvidia-rtx-spark-laptop)** · composite 42.25 · _flagged needs_review (low confidence / novelty / relevance)_
  On RTX Spark laptops, benchmark local inference under WSL or on battery; native Linux on wall power is throttled.
- **[ICML authors certify graph neural networks against label and structure poisoning](http://arxiv.org/abs/2611.03350v1)** · composite 41.8 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a theoretical robustness advance for GNN training, with little direct use for LLM, agent, or appsec defenders.
- **[EEP proposes signed push events so agents can follow entities](https://github.com/eep-dev/EEP)** · composite 41.01 · _flagged needs_review (low confidence / novelty / relevance)_
  Another early agent protocol; the useful idea is signed, replay-bounded push events instead of scraping.
- **[Google ships Gemini 4 Carbon to trusted cyber defenders first](https://latent.space/p/ainews-gemini-4-carbon/)** · composite 40.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A strong new model for vulnerability work, but its cyber scores come from Google and its hallucination rate went up, so validate it on your own triage tasks before you trust its…
- **[Matt Pocock's dictionary splits hallucinations into factuality and faithfulness](https://www.aihero.dev/ai-coding-dictionary/hallucination)** · composite 40.75 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful diagnostic framing for coding agents (add context vs compact), stated as opinion with no data.
- **[Simon Willison folds agent-written PR descriptions under a human summary](https://simonwillison.net/2026/Nov/9/details-summary/)** · composite 40.72 · _flagged needs_review (low confidence / novelty / relevance)_
  Lead agent PRs with a short, human-vetted opener and collapse the agent's full write-up under a label that names the model.
- **[METR proposes third-party review of unreleased models by mining internal transcripts](https://metr.org/blog/2026-10-14-alignment-assessment-proposal/)** · composite 40.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Evidence of misalignment is only as good as the logs and detection methods behind it, and agents can tamper with logs while training against detectors can teach models to evade…
- **[Microsoft evaluates Copilot on fully synthetic, time-evolving enterprise tenants](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/)** · composite 40.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For assistants that work over private workspace data, a reproducible synthetic world with a timeline lets you regression-test without touching customer data.
- **[Anthropic study finds scientists use Claude mostly for data analysis and writing](https://www.anthropic.com/research/how-researchers-use-claude)** · composite 39.98 · _flagged needs_review (low confidence / novelty / relevance)_
  Researchers adopt AI where it already works well, and specialized tool-connected setups shift use toward harder tasks, but this is adoption measurement, not a harness technique.
- **[Rivet runs each agent loop outside the sandbox as a lightweight actor](https://github.com/rivet-dev/rivet)** · composite 39.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Separating the agent loop from the code sandbox is a sound pattern for cost and blast radius, but the performance figures come from the vendor.
- **[Flide is an inference engine that serves Jev-style decision models faster](https://github.com/OmniJev/Flide)** · composite 39.25 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run many classification-style decisions over the same context, state forking and session caching can cut latency without changing answers, though the speedups are…
- **[Huawei open-sources MACaQ, a model-agnostic quantizer for GGUF and vLLM](https://github.com/huawei-csl/MACaQ)** · composite 39.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Another open quantizer with self-reported gains; worth a benchmark if you serve local GGUF or W4A4 (4-bit weights and activations) models.
- **[MLX tensor parallelism over Thunderbolt serves a mixture-of-experts model on Mac Studios](https://machinelearning.apple.com/research/mlx-distributed-inference)** · composite 39.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A small Mac cluster can now serve a near-trillion-parameter open model to a local coding agent at usable speed, but tensor parallelism helps decode far more than pipeline…
- **[A former Meta engineer argues AI coding makes codebases fragile](https://evanxmerz.com/post/ai-usage-generates-a-fragile-codebase/)** · composite 36.25 · _flagged needs_review (low confidence / novelty / relevance)_
  One engineer's anecdotal case that AI coding raises incidents; track incident counts and recovery time yourself rather than trusting output volume.
- **[Arca's wealth agents run ten-day tasks while human advisors move money](https://latent.space/p/arca/)** · composite 35.97 · _flagged needs_review (low confidence / novelty / relevance)_
  For long, stop-start agent work in a regulated field, keep state in a shared memory and put every risky action behind deterministic rules, not model judgment.
- **[Latent Space roundup highlights LLMs reading and editing other models' weights](https://latent.space/p/ainews-llms-can-read-write-neural-network-weights-weight-space-programming-cuts-autoresearch-out-of/)** · composite 35.32 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a news roundup with little detail of its own on weight-space programming, so the paper and the existing critique of it are the better sources.
- **[Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/)** · composite 34.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Large subagent workflows can finish big, test-backed builds without supervision, so the bottleneck moves to human review; plan for verification artifacts such as conformance…
- **[SpecForge compiles team rules into checks that agents cannot skip](https://github.com/leaderiop/SpecForge)** · composite 34.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Move the rules an agent must obey out of the prompt and into a deterministic check that fails, the same way tests gate code.
- **[Google's VERID checks agent-written lab-robot protocols against a 3D digital twin](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/)** · composite 34.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent actions on the physical world need validation against live state, not just syntax, and agents optimizing a proxy metric will exploit artifacts until real-world readouts…
- **[Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access](https://www.anthropic.com/news/accenture-embedded-evaluation)** · composite 34.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded evaluation is starting with a lab-funded commercial partner and no shared standards, so judge its independence by the access and reporting terms once they are published.
- **[SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench)** · composite 33.87 · _failed independent verification — Verifier: excerpts verbatim and dataset sizes correct, but the draft over-reached (author attribution, regression-catching inference, filler lesson). Text corrected; held as an old 2024 benchmark README with low novelty._
  If your coding agent claims it reproduced a bug, require a test that fails before the fix and passes after. SWT-Bench is a ready-made harness for measuring how often it can.
- **[Context-Regularized Cross-Entropy makes image classifiers rely less on background context](http://arxiv.org/abs/2611.08157v1)** · composite 33.4 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a vision-training result about spurious background cues in convolutional neural networks (CNNs), with no direct use for LLM harness or agent builders.
- **[Bengio and collaborators publish a 182-page survey on mechanistic interpretability](https://x.com/askalphaxiv/status/2119836067591573781)** · composite 33.1 · _flagged needs_review (low confidence / novelty / relevance)_
  A broad reading map for model internals, not a practical change for anyone building agents or harnesses.
- **[Workshop paper proposes retrieval as local traversal through a memory address space](http://arxiv.org/abs/2610.40545v1)** · composite 32.55 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an early architecture hypothesis that stateful retrieval is easier to learn than stateless retrieval, not something harness builders can use yet.
- **[A Thomson Reuters engineer runs a coding agent fully offline with Qwen](https://latent.space/p/offline-coding/)** · composite 32.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A 9B local model with OpenCode can handle small, test-backed fixes offline, but the source shows only one trivial task.
- **[Matthew Berman tells coding agents to show video mocks of UI changes](https://x.com/MatthewBerman/status/2117670441380966696)** · composite 31.9 · _failed independent verification — The source is a one-line instruction; lesson 1's claim that humans review behavior, not just diffs, is the analyst's inference, not in the post._
  Asking the agent for visual evidence of UI changes is a cheap review habit, but the post adds nothing beyond the instruction.
- **[Amazon Science published Mitra-v2, a synthetically pretrained tabular foundation model](https://www.amazon.science/blog/mitra-v2-scaling-synthetic-pretraining-for-tabular-foundation-models)** · composite 31.38 · _failed independent verification — Fetched page held only navigation; claims come from the feed teaser._
  Off-thesis tabular ML research with no usable captured text; record as news only.
- **[Matt Pocock's AI Coding Dictionary defines an agent as model plus harness](https://www.aihero.dev/ai-coding-dictionary/agent)** · composite 31.15 · _flagged needs_review (low confidence / novelty / relevance)_
  A vocabulary page, useful for team terminology but with no new finding.
- **[SAFT adversarially trains only robustness-critical parameters and beats LoRA](http://arxiv.org/abs/2610.39455v1)** · composite 31.05 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a model-training result for classic adversarial robustness and has little direct use for agent or harness builders.
- **[Addy Osmani argues that working with coding agents is a management job](https://x.com/addyosmani/status/2119332146485891501)** · composite 31.0 · _flagged needs_review (low confidence / novelty / relevance)_
  The framing is useful but the captured source is a teaser with no concrete practices behind it.
- **[Researchers' VA-TDM method improves four-step image and video diffusion generation](https://arxiv.org/abs/2611.06796)** · composite 30.94 · _flagged needs_review (low confidence / novelty / relevance)_
  This off-thesis diffusion research matters only if you serve image or video generation and want fewer sampling steps.
- **[FAF registers YAML media types for portable AI project context files](https://github.com/Wolfe-Jam/faf)** · composite 30.2 · _failed independent verification — Not sent to a verifier: a promotional README with no testable finding; low scores, held for review._
  A context-file format with marketing but no evidence; existing AGENTS.md-style files do the same job.
- **[Amazon Science covers third-party review of AI safety testing, body not captured](https://www.amazon.science/blog/strengthening-ai-safety-evaluation-through-independent-third-party-review)** · composite 30.0 · _failed independent verification — Verifier refuted lessons 1-2: the raw capture is navigation only, so nothing beyond the headline is supported; 'AVERI' comes from the feed excerpt, not the page. Needs a re-fetch of the article body._
  Only the headline can be verified: a frontier lab used an outside party to audit its safety-eval process. Re-fetch the article before taking any lessons from it.
- **[Daniel Miessler argues harnesses should describe what you want, not steps](https://danielmiessler.com/blog/models-how-harnesses-what)** · composite 30.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Spend harness effort on user context and definitions of done rather than step-by-step scripts, as a heuristic, not a measured result.
- **[MCP Explained site walks through how the Model Context Protocol works](https://mcp-explained.com/)** · composite 29.65 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful primer for newcomers, but the captured text adds nothing new for security or harness builders.
- **[Workshop paper proposes retrieval as a local walk through memory](http://arxiv.org/abs/2610.40545v1)** · composite 29.55 · _flagged needs_review (low confidence / novelty / relevance)_
  An interesting idea for stateful agent memory, but a single toy experiment gives a harness builder nothing to use yet.
- **[Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193)** · composite 29.34 · _flagged needs_review (low confidence / novelty / relevance)_
  If your agent rewrites its own prompts, memory or tools, re-verify after each change against a held-out evaluation it cannot edit.
- **[Titus Winters says AI raised code output and outages, not features shipped](https://newsletter.pragmaticengineer.com/p/software-engineering-at-google-and)** · composite 29.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Judge AI-assisted engineering by outages and delivered features, not code volume, and wrap large AI rewrites in the coexist, shard and block-the-old discipline Google used before…
- **[HybridAgent reasons in latent space and calls tools in text](https://arxiv.org/abs/2610.18861)** · composite 28.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a model architecture and training change, not a harness technique, so it only matters if you train or serve your own open-weight agent models.
- **[Daniel Miessler frames AI work as hill-climbing against ideal-state evals](https://danielmiessler.com/blog/general-hill-climbing)** · composite 28.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat the written ideal state as the source of your verification criteria, and update the evals whenever passing output still feels wrong.
- **[Simon Willison's Claude-run review finds webframe fast but rough for scraping](https://simonwillison.net/2026/Oct/26/webframe-evaluation/)** · composite 28.05 · _flagged needs_review (low confidence / novelty / relevance)_
  webframe is a lightweight way to run page JavaScript from scripts, but do not treat it as a sandbox without your own isolation.
- **[Sparse Adversarial Fine-Tuning (SAFT) updates only about 5% of a network's parameters](http://arxiv.org/abs/2610.39455v1)** · composite 28.05 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful efficiency result for adversarial robustness research, with no direct bearing on securing LLM agents.
- **[Theo endorses a quick guide on which coding-agent harness to use](https://x.com/theo/status/2119329490568691717)** · composite 28.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a biased opinion with no measurements, so treat it as a list of options to try rather than a recommendation.
- **[Claude Opus 5.5 ports a Three.js scene to plain WebGL](https://simonwillison.net/2026/Nov/9/hn-50421091/)** · composite 27.22 · _flagged needs_review (low confidence / novelty / relevance)_
  One anecdote shows a frontier model can drop a 3D library dependency, and it says little a harness builder can act on.
- **[Datasette stops sending Firefox rel=next link headers that trigger prefetches](https://simonwillison.net/2026/Nov/7/link-rel-next/)** · composite 26.98 · _flagged needs_review (low confidence / novelty / relevance)_
  If your app sends rel=next link headers on costly paginated HTML pages, Firefox may be making your server render pages nobody looks at.
- **[Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges)** · composite 26.85 · _failed independent verification — Verifier refuted 'interviewees agree public rankings only shortlist candidates' (one Sonar quote) and 'harness matters as much as the model' (Dream's view alone); Sonar's leaderboard measures quality and security, not secure generation only._
  Choose models for security work with your own task evaluations and a defined failure budget; leaderboards are only a shortlist.
- **[Bound-conditioned latent inference cuts progressive image codec BD-rate on Kodak](http://arxiv.org/abs/2610.30966v1)** · composite 26.55 · _flagged needs_review (low confidence / novelty / relevance)_
  A solid image-compression result, but it has no bearing on securing or building AI agents and harnesses.
- **[PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1)** · composite 26.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Medical ML result, off-thesis here: the general point is not to treat an accuracy leaderboard as a stand-in for calibration under low labels or domain shift.
- **[Moonshot's Kimi K3.1 Pro nears frontier scores, with open weights promised](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/)** · composite 26.49 · _flagged needs_review (low confidence / novelty / relevance)_
  A near-frontier open-weight option at half Opus pricing is worth benchmarking on your own agent tasks once the weights ship.
- **[Hacker News developers describe fatigue from AI-era coding and agent review](https://news.ycombinator.com/item?id=50301479)** · composite 25.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Human review capacity, not agent output, is now the bottleneck, so harnesses should cut what humans must read and prove that tests actually test something.
- **[@_rybaz argues agent solutions alone do not make a good business](https://x.com/_rybaz/status/2117660118682923408)** · composite 25.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Thin opinion post with no technical content; skip unless tracking conference sentiment.
- **[RoboCasa-Shift shows equal success-rate drops in a VLA policy hide different failures](https://arxiv.org/abs/2610.27861)** · composite 25.23 · _flagged needs_review (low confidence / novelty / relevance)_
  Aggregate success rate can hide outcome flips and which task stage fails; the study covers one robot policy on four simulated tasks.
- **[alphaXiv tally ranks Together AI first in 2026 AI-cloud publications](https://x.com/askalphaxiv/status/2120927603385331926)** · composite 25.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Industry trivia with no method; not actionable for harness builders.
- **[Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)** · composite 24.98 · _flagged needs_review (low confidence / novelty / relevance)_
  Governance news only: Agent Skills is now a Linux Foundation-hosted standard like MCP, and nothing changes technically today.
- **[Anthropic reports early results from Claude-driven drug development partnerships](https://www.anthropic.com/research/early-progress-drug-development)** · composite 24.64 · _flagged needs_review (low confidence / novelty / relevance)_
  The reusable idea in this off-field vendor report is to check agent review against known human findings before relying on it.
- **[HackerBooks lists 16,543 books mentioned in Hacker News comments](https://hackerbooks.org)** · composite 23.65 · _flagged needs_review (low confidence / novelty / relevance)_
  Off-topic for security and agent builders: a book directory with no technique to learn from.
- **[Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models)** · composite 23.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A hands-on resource for understanding the reasoning model inside agents; teaching material, not a new finding.
- **[alphaXiv says its 4B decision model nearly matches Jev except sarcasm](https://x.com/askalphaxiv/status/2116199951835582507)** · composite 23.25 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an unverified vendor claim, and small decision models still have to be benchmarked on your own data, as earlier pool entries showed.
- **[Tunguz posted a one-line jab at local AI enthusiasts](https://x.com/tunguz/status/2118051184779076026)** · composite 22.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Nothing here to act on.
- **[Framework-free Colab notebooks teach the applied LLM engineering stack](https://github.com/calmrocks/ai-engineer-notebooks)** · composite 20.84 · _flagged needs_review (low confidence / novelty / relevance)_
  A reasonable onboarding course for engineers new to LLM apps; no new technique.
- **[Anthropic expands AI for Science credits to 20 foundations and institutions](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions)** · composite 19.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding and partnership announcement with nothing to change in a harness, apart from noting the Model Hardware Standard for agents that drive physical instruments.
- **[Anthropic staff, unlike most US adults, expect Nobel-level AI discovery by 2030](https://www.anthropic.com/research/ai-expectations-gap)** · composite 18.15 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an economics and public-opinion survey with little practical value for builders, though its one practical data point is that regular AI users at work rank data privacy and…
- **[Venus-DefakerOne2 detects image and video forgeries with one forensics model](https://arxiv.org/abs/2610.37918)** · composite 17.91 · _flagged needs_review (low confidence / novelty / relevance)_
  It is a candidate forgery detector for fraud and identity teams, and has little bearing on agent or harness work.
- **[Theo video on running Claude for weeks, transcript not captured](https://www.youtube.com/watch?v=NBCM_ZoWZo8)** · composite 16.5 · _failed independent verification — Verifier: the description is truncated, so 'gives no method' cannot be confirmed from the captured text._
  Nothing usable was captured. Watch the video or fetch its transcript before treating it as a source on long-running agents.
- **[Anthropic expands its GSA deal to discount Claude for governments](https://www.anthropic.com/news/expanding-partnership-gsa)** · composite 15.76 · _flagged needs_review (low confidence / novelty / relevance)_
  This procurement news only matters if you buy Claude for a US government organization.
- **[Anthropic News Product index page lists 41 product announcements](https://www.anthropic.com/news/product)** · composite 14.94 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page with no analysis; the only signal is that Agent Skills is moving to a neutral foundation with broad cross-vendor adoption.
- **[Riley Goodside mocks the claim that model collapse halted LLM progress](https://x.com/goodside/status/2115825541244760315)** · composite 14.55 · _failed independent verification — Verifier: the text carries no explicit sarcasm marker, so the 'mocks' reading of lesson 1 is inference from tone._
  A joke, not a finding, and it signals only that practitioners see model collapse as an overblown prediction so far.
- **[Amp releases an Android app for its coding agent](https://ampcode.com/news/amp-on-android)** · composite 14.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Amp users can now check agent threads and diffs from a phone, but there is nothing to learn about building agents.
- **[Anthropic's Security news page is an index of earlier posts](https://www.anthropic.com/news/security)** · composite 13.95 · _flagged needs_review (low confidence / novelty / relevance)_
  Nothing new here; read the linked posts on their own dates.
- **[Anthropic's partnerships index lists business deals and holds no new security news](https://www.anthropic.com/news/partnerships)** · composite 13.32 · _flagged needs_review (low confidence / novelty / relevance)_
  A listing page of business announcements, with nothing for a security engineer or agent builder to act on.
- **[Anthropic's Policy news page is an index of policy announcements](https://www.anthropic.com/news/policy)** · composite 13.05 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat this as a pointer to follow individual posts, such as the independent-evaluator update, not as a finding.
- **[Anthropic's Models index shows Claude Haiku 5.5 as the newest release](https://www.anthropic.com/news/models)** · composite 12.31 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page picked up by the sitemap harvester; the releases it lists were covered when announced.
- **[Anthropic's Features index lists three stories, newest from September](https://www.anthropic.com/news/features)** · composite 11.71 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page picked up by the sitemap harvester; no finding.

---

<sub>Generated by scripts/generate_review.py on 2026-11-12. 217 item(s) awaiting review.</sub>
