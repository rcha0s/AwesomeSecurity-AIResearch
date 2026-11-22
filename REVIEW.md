# 🔍 Review Queue

> Everything held back from the site, with the reason. Findings that are **not yet vetted** (low confidence/novelty/relevance, or below the composite floor (20)), and news stories whose excerpt is not grounded in its source. Nothing here is deleted; promote a finding by raising its scores or clearing `needs_review`, or fix a news story's excerpt, then regenerate.

_Updated 2026-11-22._

## AI Security (69)

- **[OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident)** · composite 66.0 · _news story: excerpt not grounded in source (only 75% of quotes verified)_
  Treat a model eval with production classifiers off as a live agent that may try to escape, where a package-manager proxy is a plausible sandbox-escape primitive.
- **[Researchers find no agent framework defends against MCP tool poisoning](http://arxiv.org/abs/2611.03555v1)** · composite 65.1 · _failed independent verification — Lessons hold, but the verifier put novelty at 42 vs 70: MCP tool poisoning is well covered; the delta is the cross-framework measurement. It also flagged the takeaway's 'only defenses measured to matter' as overstating the abstract._
  Do not expect your agent framework to stop poisoned MCP tool metadata; model choice and your own controls are the only defenses measured to matter.
- **[Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585)** · composite 59.1 · _news story: excerpt not grounded in source_
  The critical attack surface for agent apps is the framework layer around the model, where old bug classes get re-exposed as prompt-injected code paths — not the model's ability to…
- **[Human reviewers miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)** · composite 53.7 · _news story: excerpt not grounded in source_
  Human-in-the-loop is a fatigue-limited primitive: engineer approvals as classifier + sandbox + hooks, not as a UX prompt.
- **[ai-dfir-toolkit ships open detection rules and forensic artifacts for AI attacks](https://github.com/depalmar/ai-dfir-toolkit)** · composite 53.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Defenders get a free, open-format starting set of AI-specific detections and a triage artifact list for agent hosts, but must tune them, since the README shows no measured…
- **[MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027)** · composite 53.1 · _news story: excerpt not grounded in source_
  MCP's enterprise turn adds iss validation and a stateless design that removes one session-poisoning surface but leans on standard load-balancer trust boundaries.
- **[Jupyter MCP Server management routes skip Host checks, enabling DNS rebinding hijack](https://github.com/advisories/GHSA-9x8x-crjq-g64h)** · composite 52.5 · _failed independent verification — Lesson 3 overstates: the 'tokens' the MCP server sends to the attacker-chosen backend are the attacker-supplied ATTACKER_TOKEN values, so no credential leak is shown. 'Sending tokens to attacker infrastructure' is not supported by the advisory._
  Origin and Host protection must cover every route on an MCP server's HTTP app, not only the /mcp endpoint, and state-changing routes need their own authentication.
- **[lend runs remote agents' commands on the user's laptop after Touch ID approval](https://blog.antonio.cx/running-agents-with-lend)** · composite 52.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Keep long-lived credentials on a trusted host, expose only an allow-listed, human-approved command channel to agents, and remember that approving a shell approves everything.
- **[ShadowBench-MCP: task-preserving rewordings can push an LLM tool router onto riskier paths](http://arxiv.org/abs/2611.11720v1)** · composite 51.9 · _flagged needs_review (low confidence / novelty / relevance)_
  If an LLM chooses which tools run, mandatory safety steps should be enforced outside the router, and the routing prompt should state security policy, not just efficiency.
- **[OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/)** · composite 51.0 · _news story: excerpt not grounded in source_
  Rogue-agent incidents are foundational-security failures with known fixes: zero-trust boundaries, isolated eval hosts, egress control and active monitoring.
- **[LeanGuard checks every agent tool call against a Lean4-verified policy](https://arxiv.org/abs/2611.02332)** · composite 50.46 · _flagged needs_review (low confidence / novelty / relevance)_
  A deterministic, history-aware policy check in front of tool execution stops forbidden actions regardless of what the model was tricked into proposing, at little cost to task…
- **[Anthropic Fellows find Claude agent teams rarely catch a teammate told to sabotage](https://www.anthropic.com/research/project-eve-claude-plays-mmorpgs)** · composite 48.12 · _failed independent verification — All lessons supported, but the verifier rated novelty 30 vs 62: a live multi-agent game demo of known prompted-sabotage capability (SHADE-Arena-style evals)._
  In multi-agent systems, an agent's reports and proposals are untrusted input, and peer agents are not a reliable sabotage detector.
- **[Adan Alvarez tested which AWS attacks 14 LLMs propose with stolen keys](https://medium.com/@adan.alvarez/i-gave-14-llms-aws-keys-heres-what-they-wanted-to-do-next-48585761a11b)** · composite 47.75 · _failed independent verification — Medium returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the article._
  If LLM-driven attackers open with predictable AWS calls, those calls can become detections.
- **[IDEA flags backdoor triggers in graphical-interface agents at inference time](https://arxiv.org/abs/2611.24102)** · composite 47.66 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run a downloaded computer-use agent, add a per-step runtime check that asks whether the instruction or a screen region drove the action.
- **[Logit Laundering lets LLM providers hide training-data watermarks at inference time](http://arxiv.org/abs/2611.09446v1)** · composite 46.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Watermark-based data-use audits that only query model outputs can be defeated by a dishonest provider, so they are weak evidence on their own.
- **[MLflow servers without authentication can be hijacked through third-party scorer loading](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)** · composite 46.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  If you run MLflow 3.12.0 or later, never expose it without authentication, and track the advisory for a fixed version.
- **[Agent Name Service spec anchors AI agent identity to verified domain names](https://github.com/agentnameservice/ans-spec)** · composite 46.01 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent-to-agent trust needs identity tied to a verified domain and to the running code version, not just a name.
- **[Brazilian labor court fines lawyers for hidden prompt injection in a filing](https://jetstream.security/insights/brazilian-court-sanctions-prompt-injection-filing/)** · composite 44.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Hidden-text injection in documents from outside parties is now a sanctionable act in at least one court, and any pipeline that has AI read outside documents should check for…
- **[Devlab's mcp-scanner reports UNKNOWN instead of SAFE when an analyzer fails](https://github.com/devlab-group/mcp-scanner)** · composite 44.1 · _failed independent verification — Lesson 4 says live scans are read-only by default, but the README says the default probe mode sends malformed protocol messages and tools/call probes that a loose server may dispatch._
  When you gate MCP servers in CI, treat a scan that did not finish as a failure, and pick a scanner that makes that state visible.
- **[OCC framework guides bank examiners on tiering AI use cases by risk](https://www.debevoisedatablog.com/2026/11/10/occs-new-super-intelligence-supervisory-framework-key-takeaways-and-how-it-compares-to-the-fsbs-ai-sound-practices/)** · composite 41.25 · _flagged needs_review (low confidence / novelty / relevance)_
  US bank examiners will now look at agent autonomy, reversibility and controls on external agents, so defenders at banks need an inventory that captures those fields.
- **[Red-Team AI reads an agent app's source code to tailor attacks](https://github.com/votal-ai-hq/ai-red-teaming)** · composite 41.02 · _flagged needs_review (low confidence / novelty / relevance)_
  Feeding a red-team tool your agent's source finds tool-chain paths that black-box prompt lists miss.
- **[SkillCODER fingerprints agent skill files to trace leaks to a buyer](http://arxiv.org/abs/2611.11308v1)** · composite 40.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Sellers of proprietary skills can embed per-buyer traceable marks, but the mark is itself a hidden conditional instruction that a skill reviewer should know to look for.
- **[AgentLint checks coding-agent file writes and shell commands through local hooks](https://github.com/mauhpr/agentlint)** · composite 40.01 · _flagged needs_review (low confidence / novelty / relevance)_
  Hook-based linting of agent actions catches common mistakes cheaply, but treat it as feedback, not as a security boundary.
- **[Cybozu's Prompt Hardener models prompt-injection risk from an agent spec file](https://github.com/cybozu/prompt-hardener)** · composite 40.01 · _flagged needs_review (low confidence / novelty / relevance)_
  The spec-plus-three-layers threat model is worth copying, but the tool itself is unmaintained and its prompt-level hardening only helps contain injection, it does not stop it.
- **[laya-guard checks coding-agent tool calls locally with regex and a small model](https://github.com/scs0209/laya-guard)** · composite 39.95 · _ungrounded excerpt — only 75% of quotes verified against the source_
  A local regex-plus-small-model guard at the tool-call hook is cheap and works offline, but it sees only what a command declares, not what scripts do at runtime.
- **[Innovaccer's Healthcare MCP extension binds tool calls to an opaque patient handle](https://github.com/innovaccer/Healthcare-MCP)** · composite 39.75 · _failed independent verification — The verifier found lesson 2 and the takeaway overstated the default exposure; they now say token verification is opt-in but patient-scoped calls fail closed by default._
  Healthcare MCP (HMCP) offers a useful per-patient scoping pattern for MCP, but its auth is opt-in and its guardrails best-effort, and the README says the building blocks do not by…
- **[Chainguard sandboxes agent CI with microVMs, egress proxying and sealed tokens](https://www.chainguard.dev/unchained/microvms-egress-mitm-and-sealed-tokens-sandboxing-untrusted-code-at-scale)** · composite 39.22 · _flagged needs_review (low confidence / novelty / relevance)_
  Keep secrets out of the agent's guest: inject credentials at an out-of-guest egress proxy and seal any token the guest must hold so it is useless elsewhere.
- **[DailySafe benchmark tests if multimodal LLMs notice risks building across turns](https://arxiv.org/abs/2611.26298)** · composite 38.59 · _failed independent verification — Lesson 3 says the benchmark is hand-annotated rather than a large automated set. The abstract gives 195 interactions and case-specific safety annotations but never says hand-annotated; that is inference._
  Single-turn harmful-request tests miss risk that emerges over a conversation, so evals should replay context, not just prompts.
- **[api-relay-audit tests third-party LLM proxies for prompt injection and model swaps](https://github.com/toby-bridges/api-relay-audit)** · composite 37.78 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat any third-party LLM relay as a trusted middlebox you must test, and keep inconclusive probe results visible instead of reading them as clean.
- **[hoop.dev ships a wire-level sidecar that masks data and blocks agent SQL](https://github.com/hoophq/hoop)** · composite 37.65 · _flagged needs_review (low confidence / novelty / relevance)_
  Putting data controls on the database wire, not in the prompt, is a sound pattern; check which hoop features are actually built before relying on it.
- **[AbliteratedOutTheBox strips open-weight model refusals at inference without weight edits](https://github.com/heterodoxin/AbliteratedOutTheBox)** · composite 37.5 · _failed independent verification — Verifier rated novelty 25 (refusal-direction ablation per Arditi et al. 2024, moved to runtime steering) and relevance 40; results are single-model and self-reported. Lesson 3's original claim that benign checks cannot reveal the runtime was extrapolation and has been cut back to the source's figure._
  Treat refusal in any self-hosted open-weight model as optional, and put the controls that matter outside the model.
- **[OpenRouter drops three providers and 125 endpoints after Dragos data-policy findings](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/)** · composite 36.75 · _flagged needs_review (low confidence / novelty / relevance)_
  A zero-data-retention label from an inference gateway is only as good as the provider behind it; verify data handling rather than trusting the badge.
- **[Goldman Sachs limits Claude Code and GitHub coding tools to engineers](https://www.thestateofai.com/news/goldman-sachs-claude-code-traders-bankers)** · composite 36.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Code that non-engineers build with agents needs a named engineering owner and the same review, entitlement and information-barrier controls as any other code.
- **[Chainguard serves sandboxed --help output for 63,000 executables to agents over MCP](https://www.chainguard.dev/unchained/help-every-tool-that-never-had-a-manual-page)** · composite 36.72 · _flagged needs_review (low confidence / novelty / relevance)_
  Any MCP server that relays third-party text, even documentation, should fence it as data and bind it to signed provenance, because the agent will otherwise trust it on the…
- **[Agno agent framework ran Python eval on a function call's field type](https://github.com/advisories/GHSA-m4w4-3r8h-jw98)** · composite 36.35 · _failed independent verification — Novelty disagreement: verifier rated 12 against my 35 (a routine eval-injection bug class, cf. LangChain CVE-2023-29374). It also noted the tool/model-output path is only an example and the advisory does offer a partial workaround._
  An agent framework that evals strings shaped by model output turns prompt injection into code execution, so upgrade Agno and search your agent code for eval on schema fields.
- **[PersonaHate builds a 791K-sample synthetic hate speech corpus for detectors](http://arxiv.org/abs/2611.21951v1)** · composite 36.3 · _flagged needs_review (low confidence / novelty / relevance)_
  Persona-conditioned synthetic data with multi-judge labels is a cheap way to widen coverage for content-safety classifiers.
- **[Repo Forensics is an offline scanner for agent skills, plugins and MCP servers](https://github.com/alexgreensh/repo-forensics)** · composite 36.07 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat third-party skills and MCP servers like dependencies: scan before install and on every update, ideally from a hook, and do not trust a single vendor's detection claims.
- **[MSafeTemp authors show English-only safety evaluation misses multilingual jailbreaks](https://arxiv.org/abs/2610.40516)** · composite 35.69 · _flagged needs_review (low confidence / novelty / relevance)_
  If your product serves non-English users, refusal testing done only in English leaves translated and localized jailbreaks untested.
- **[humanbound-firewall screens every input to an agent by who authored it](https://github.com/humanbound/humanbound-firewall)** · composite 35.57 · _flagged needs_review (low confidence / novelty / relevance)_
  The useful idea is to label every model input by author (request, outside content, own records); treat the tool as a preview filter, not a security boundary.
- **[Snyk Agent Scan finds and scans local agents, MCP servers and skills](https://github.com/snyk/agent-scan)** · composite 35.52 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent Scan gives a quick inventory of agent supply-chain risk on a machine, but the scan itself can run code and send data out, so plan for that.
- **[AegisGate is a self-hosted proxy that filters LLM API traffic](https://github.com/ax128/AegisGate)** · composite 35.43 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful reference design for an LLM egress proxy, but its default detection is regex and its default redaction is narrow.
- **[Cisco AI Defense mcp-scanner checks MCP servers with YARA, LLM and API engines](https://github.com/cisco-ai-defense/mcp-scanner)** · composite 34.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Use mcp-scanner as a gate when admitting MCP servers, but remember that scan-time checks do not prove anything about runtime authorization.
- **[NuGuard is an open-source AI-SBOM and red-team pipeline for agentic apps](https://github.com/NuGuardAI/nuguard)** · composite 34.14 · _flagged needs_review (low confidence / novelty / relevance)_
  It is a candidate all-in-one CI red-team harness for agent apps. It's young (67 stars), so treat the comparison claims as unverified marketing until you've benchmarked it against…
- **[openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator)** · composite 34.07 · _ungrounded excerpt — only 75% of quotes verified against the source_
  Auto-generated MCP servers expose your whole API to an agent by default, so filter operations and turn on inbound auth before you deploy one.
- **[c-goosen releases PwnGPT, an open-source 16-level prompt injection CTF](https://github.com/c-goosen/ai-prompt-ctf)** · composite 33.87 · _flagged needs_review (low confidence / novelty / relevance)_
  A ready-made range for teaching prompt injection and testing guardrails, but its defaults are not safe to expose to players.
- **[Agent Plugins spec adds a 1.1.0 working draft to its packaging standard](https://github.com/agentplugins/agent-plugins-spec)** · composite 33.84 · _failed independent verification — Verifier: the README cannot show that the 1.1.0 draft is the only change since the 2026-08-10 entry, and lesson 2's trust-and-consent reading goes beyond the source._
  A plugin bundles skill prompts and MCP server configs into one artifact, so review and pin it as one supply-chain unit; this README update adds no new security content.
- **[mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6)** · composite 32.75 · _failed independent verification — Refuted: the saved source holds only generic CVSS definitions, so the SQL injection, version range and Databricks details are unsupported by it. Needs a re-fetch of the advisory._
  Agent memory content is attacker-influenced input, so memory backends must use parameterized queries like any other data layer.
- **[mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins)** · composite 32.57 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat a Jenkins MCP server as code execution on your CI: give it a token without script rights, enable read-only mode, and keep it off the network.
- **[Brave Search API lets AI agents pay per query through x402](https://brave.com/blog/search-api-agentic-payments/)** · composite 32.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent wallets that pay per call are now a real, high-traffic integration path, so treat the wallet as a credential with hard spend limits.
- **[MCP specification repository now points to a 2026-07-28 schema revision](https://github.com/modelcontextprotocol/modelcontextprotocol)** · composite 31.74 · _flagged needs_review (low confidence / novelty / relevance)_
  Check MCP clients and servers against the 2026-07-28 schema; the README itself carries no new security content.
- **[OpenGuardrails proposes one vendor-neutral wire protocol for agent guardrails](https://github.com/openguardrails/openguardrails)** · composite 31.67 · _flagged needs_review (low confidence / novelty / relevance)_
  A common guardrail interface could cut integration work, but its fail-open default means an attacker who can block the runtime turns the guardrail off.
- **[mcp-openapi-server exposes OpenAPI endpoints to agents as MCP tools](https://github.com/ivo-toby/mcp-openapi-server)** · composite 31.39 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful OpenAPI-to-MCP bridge, but its filters narrow what the model sees, not what it can do; keep authorization in the API.
- **[Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus)** · composite 31.25 · _flagged needs_review (low confidence / novelty / relevance)_
  If your LLM app keeps client-controlled chat history, test it with multi-turn and backtracking attacks, not just single-prompt jailbreak lists.
- **[mcp-watch is an open-source static scanner for MCP server repositories](https://github.com/kapilduraphe/mcp-watch)** · composite 30.82 · _flagged needs_review (low confidence / novelty / relevance)_
  Another unevaluated MCP repository scanner; trial it beside established scanners rather than relying on it.
- **[Microsoft launches Perception and agent-governance tools at Ignite, framing agents as insiders](https://www.microsoft.com/en-us/security/blog/2026/11/17/security-for-the-agentic-era-powered-by-microsoft-perception/)** · composite 30.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Vendor roadmap, not evidence: it signals that agent identity, discovery and scoped access are becoming standard enterprise controls, but verify preview claims before relying on…
- **[United Airlines bans third-party AI agents from booking flights for travelers](https://www.cbsnews.com/news/united-airlines-bans-ai-agents-booking-flights/)** · composite 30.75 · _failed independent verification — The verifier found lesson 1 inferred (platform cannot tell agent from owner); it now states only the risks United cites, and the summary and takeaway were trimmed to the source._
  United is blocking credential-sharing AI agents, which pushes agent builders toward scoped, sanctioned access instead of password reuse.
- **[Tamga's prompt-injection rules caught 27 of 203 attacks written by others](https://github.com/yatuk/tamga)** · composite 28.84 · _failed independent verification — Lessons hold, but the verifier judged novelty 18 vs 45: the held-out collapse of phrase-matching injection filters is known (e.g. Hackett et al. 2025 on bypassing guardrail detectors); Tamga's two held-out sets are small and Turkish-only._
  Tamga's own numbers show a wording-based injection filter catching few attacks that someone else wrote, so test any such filter on independent attack sets.
- **[Starlingly's repo collects extracted LLM system prompts and injections](https://github.com/starlingly/system_prompts_and_injections)** · composite 28.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is one more leaked-prompt collection, notable only for its comparison script, and it confirms that system prompts are not secret.
- **[HirePanel is a resume screener with injection shield and quote-checked scores](https://github.com/punit2911/Hirepanel)** · composite 27.91 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful small example of layering deterministic checks, untrusted-data labelling, a read-only MCP surface and human approval around an LLM, but evidence of effectiveness is thin.
- **[MCP ZAP Server blocks private-network targets and binds scan credentials server-side](https://github.com/dtkmn/mcp-zap-server)** · composite 27.17 · _ungrounded excerpt — only 67% of quotes verified against the source_
  If you expose a scanner or other outbound tool to agents, block internal destinations by default and keep credentials server-side behind opaque profile IDs, so the agent chooses…
- **[LLMVault offers a self-hosted training range for OWASP LLM Top 10 attacks](https://github.com/CyberSunil/LLMVault)** · composite 26.54 · _flagged needs_review (low confidence / novelty / relevance)_
  A hands-on teaching range for LLM attack classes, already covered in an earlier entry and not a source of new findings.
- **[Microsoft says Gartner named it a leader in agent management platforms](https://www.microsoft.com/en-us/security/blog/2026/11/03/microsoft-named-a-leader-in-the-2026-gartner-magic-quadrant-for-ai-agent-management-platforms/)** · composite 26.47 · _flagged needs_review (low confidence / novelty / relevance)_
  This is vendor marketing whose only reusable idea is to keep an inventory of agents, each with its own identity and a named owner.
- **[Microsoft tells CISOs to put agent identity and data controls first](https://www.microsoft.com/en-us/security/blog/2026/10/28/the-cisos-evolving-role-protecting-and-defending-in-the-agentic-era/)** · composite 26.09 · _flagged needs_review (low confidence / novelty / relevance)_
  Familiar guidance (inventory agents, give each one its own least-privilege identity, classify the data it can reach), and the 15-fold growth figure is the only new data point.
- **[NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp)** · composite 25.77 · _flagged needs_review (low confidence / novelty / relevance)_
  Mostly a generic MCP wrapper. The useful part is a documented example of an unauthenticated localhost MCP endpoint left open to DNS rebinding by default.
- **[CollieAi's LLM Firewall filters prompts and responses through a hosted proxy](https://github.com/CollieAi/llm-firewall)** · composite 25.59 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a routine filtering proxy with no published detection rates, so treat it as one containment layer, not as a fix for prompt injection.
- **[X user @_rybaz mocks OpenAI for pitching cyber tools after sandbox-escape claims](https://x.com/_rybaz/status/2121292650594631741)** · composite 24.3 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an opinion post with no new facts, though its implied question, how much infrastructure access to give an AI vendor's security agents, is a fair one.
- **[Anthropic's Security news page is an index of security announcements](https://www.anthropic.com/news/security)** · composite 14.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Useful only as a pointer. The linked incident and threat-report posts carry the substance.
- **[MCP TypeScript SDK HTTP servers set no limit on request body size](https://github.com/advisories/GHSA-f897-62hf-6gxq)** · composite 10.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  MCP servers exposed over HTTP can be overloaded by oversized or batched requests until the SDK is updated.
- **[Check Point: infostealer adds collection routines for AI desktop apps](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/)** · composite 8.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  AI desktop apps and coding tools now sit next to browsers and wallets on infostealer target lists, so their tokens and data need the same protection.

## Product Security (81)

- **[Researchers brute-force Windows Hello PINs by rolling back firmware TPM lockout counters](http://arxiv.org/abs/2611.18126v1)** · composite 58.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat short device PINs as weak against anyone with physical access and lab tools; for high-risk fleets, prefer longer PINs or passphrases over short TPM-guarded ones.
- **[Ruby case-mapping heap overflow reaches Rails and Sinatra through string upcasing](https://verialabs.com/ruby2shell/)** · composite 57.75 · _failed independent verification — Lesson 3 says the one-byte overflow gives control over what sits next to it and so is hard to exploit; the source only says the attacker controls buffer size through input length and that the byte written is S or s._
  Upgrade Ruby to 3.3.14, 3.4.13 or 4.0.10 and check the Ruby bundled in GitLab and GitHub Enterprise Server before the proof of concept lands.
- **[PortSwigger shows HTML injection stealing passwords under a script-blocking CSP](https://portswigger.net/research/blind-trust-stealing-credentials-through-csp)** · composite 57.38 · _failed independent verification — Lessons hold, but the verifier scored novelty 20 vs 55: AFINE published the same technique first and the article credits it; the new part is mainly packaging it as an automated Burp skill._
  CSP does not fix reflected HTML injection, so escape the output, and do not rate a script-blocking policy as safe against credential theft.
- **[Apache HTTP Server HTTP/2 race condition allows unauthenticated remote code execution](https://www.wiz.io/blog/cve-2026-119618-rce-apache-http-server-vulnerability)** · composite 56.51 · _failed independent verification — Verifier found the AI-discovery lesson unsupported (the source never says Anthropic used AI); lesson and tag removed, threat softened, held for a human check._
  Upgrade httpd to 2.4.71 or set 'Protocols http/1.1' now; no exploit is public yet, but the bug is pre-authentication remote code execution (RCE) in a ubiquitous server.
- **[Datadog traces the ARTEX agentic attack framework inside real AWS accounts](https://securitylabs.datadoghq.com/articles/artex-agentic-attacks-aws-environments/)** · composite 54.69 · _flagged needs_review (low confidence / novelty / relevance)_
  Agentic attack tools leave repeatable, huntable habits in CloudTrail, but their cloud playbook depends on whatever model drives them, so hunt behavior rather than one fixed…
- **[StepSecurity finds wfx stealer now exfiltrates CI secrets only to Telegram](https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer)** · composite 52.92 · _flagged needs_review (low confidence / novelty / relevance)_
  Hunt for missing Actions run numbers after unexpected commits, and put an egress allowlist on CI runners, since the stealer no longer uses a fixed collection IP.
- **[Microsoft sees attack agents turn leaked GitHub secrets into Azure breaches](https://www.microsoft.com/en-us/security/blog/2026/11/05/threat-actors-use-agentic-ai-tooling-to-find-and-abuse-exposed-secrets/)** · composite 52.53 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat any secret that reaches a public repository as compromised within minutes. Detect agentic attackers by their machine-speed retry behavior, not by IP addresses or user…
- **[Anthropic cuts its vulnerability disclosure window from 90 days to 30](https://www.anthropic.com/research/coordinated-vulnerability-disclosure-timelines)** · composite 49.36 · _flagged needs_review (low confidence / novelty / relevance)_
  Plan patch and triage for a 30-day clock on high and critical reports from AI-assisted researchers, and assume the bug can be found by someone else before you ship the fix.
- **[PortSwigger turns its CRLF desync research into an automated Burp AT skill](https://portswigger.net/research/making-http-header-injection-critical-with-one-prompt)** · composite 47.94 · _flagged needs_review (low confidence / novelty / relevance)_
  Header injection findings used to be triaged as low severity, but tools can now escalate them to critical desyncs automatically, so they deserve full follow-up.
- **[Callix finds 819 access-control flaws at sensitive callsites in Android firmware apps](http://arxiv.org/abs/2611.00594v1)** · composite 46.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Checking that an access check exists in original equipment manufacturer (OEM) firmware apps is not enough; judge whether it is strong enough for the data a generic call operates…
- **[A new index tracks which open-source offensive AI harnesses attackers actually used](https://offsecharnesses.ai)** · composite 46.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Use the index as a lookup for which agent harnesses to hunt for, but remember it is a single curated list built from other people's reports.
- **[Argus, an open-source security platform, has AI agents that only propose actions](https://github.com/thomasunise/argus)** · composite 46.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Argus is a concrete reference design for agentic SecOps, with read-only agents, a propose-only path to a policy broker, agent-targeted canaries and autonomy that is reversible and…
- **[Imperva tracks StyleSmuggler Magento exploitation dropping the PSK Agent Go RAT](https://www.imperva.com/blog/stylesmuggler-exploitation-deploys-psk-agent-rat-against-magento-stores/)** · composite 46.44 · _failed independent verification — Lesson 3 says the FFI webshell survives disable_functions hardening; Imperva only says it is 'potentially preserving command execution'._
  Patching StyleSmuggler does not evict PSK Agent, so hunt for the dropper, webshell and DNS beacons on any Magento host that was exposed.
- **[Perforce Puppet Server flaw lets any agent certificate holder run code](https://nvd.nist.gov/vuln/detail/CVE-2026-115731)** · composite 45.61 · _failed independent verification — Summary claim 'CISA added it to the KEV catalog on 2026-11-17' is not in the raw NVD page._
  Patch Puppet Enterprise and Server, and replace open autosigning with verified certificate signing, since the control server is a high-value target.
- **[Engineer lists three AWS IAM anti-patterns coding agents keep writing](https://engseclabs.com/blog/things-llms-get-wrong-about-aws-iam)** · composite 45.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Review agent-generated IAM for cargo-cult patterns: needless Deny, misused permissions boundaries and no-op GetCallerIdentity grants.
- **[Kat Traxler used AI and security principles to find cloud design flaws](https://github.com/KatTraxler/presentations/tree/main/security-constitution)** · composite 44.75 · _failed independent verification — Source page returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the talk itself._
  Pointing an AI at design principles, not bug classes, may surface design flaws that pattern-based hunting misses.
- **[Next.js has unauthenticated RCE in use cache functions returning typed arrays](https://github.com/advisories/GHSA-673q-mjm6-r5xr)** · composite 44.75 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Upgrade Next.js now if any `use cache` function returns typed arrays; there is no workaround.
- **[Microsoft finds 78% of exploited CVEs are takeover-class bugs](https://www.microsoft.com/en-us/security/blog/2026/11/02/exploited-vulnerabilities-common-data-driven-analysis-real-world-attacks/)** · composite 44.52 · _failed independent verification — Lesson 3 attributes faster KEV listing partly to AI-assisted exploit development as Microsoft's finding; the post only says 'industry research suggests' it, and the timing figures come from CISA data._
  Prioritize takeover-class bugs on exposed, highly privileged servers and appliances first, because those are both the most exploited and the slowest patched.
- **[Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/)** · composite 43.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Run pathrunner in a sandbox (Pathfinding Labs) and use its CloudTrail report to test that every payload, not just one, trips a detection.
- **[SenTrojan researchers hid analog hardware Trojans in sensors triggered by physical signals](http://arxiv.org/abs/2611.06103v1)** · composite 43.8 · _flagged needs_review (low confidence / novelty / relevance)_
  In safety-critical cyber-physical systems, a sensor's readings can only be trusted as far as its hardware supply chain can be trusted, and functional tests alone may not reveal an…
- **[Nuxt Content query endpoint lets unauthenticated users stall servers with SQLite functions](https://github.com/advisories/GHSA-xxrh-5hgg-gj4h)** · composite 43.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Any endpoint that accepts raw SQL from the browser needs an allowlist of exact query shapes, plus query time and memory limits, not a keyword denylist.
- **[Microsoft Outlook spoofing flaw that skips unsafe-action warnings is exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-124194)** · composite 43.39 · _failed independent verification — Verifier found two lessons went beyond the NVD text (phishing framing, auto-update advice) and a named November update the source lacks; text trimmed, held for a human check._
  Move every Outlook client to Microsoft's fixed builds for this CVE; it is an exploited spoofing bug that needs user interaction.
- **[Next.js Image Optimization has unauthenticated RCE via SVG through sharp](https://github.com/advisories/GHSA-2464-fhr4-w9xw)** · composite 43.25 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Pin a patched sharp under Next.js and consider disabling SVG optimization; image pipelines are unauthenticated RCE surface.
- **[Google declines to fix zero-click SMS that crashes Android telephony](https://smsofdeath.com/)** · composite 42.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Any Android device reachable by SMS can be knocked off telephony, emergency calling included, and the vendor treats it as a non-security bug with no fix scheduled.
- **[A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/)** · composite 42.22 · _news story: excerpt not grounded in source_
  Enclave-to-KMS attestation only closes the gap if you also hardcode the CMK ARN, attest the IAM role, and initiate TLS from inside the enclave; without that, active-attacker…
- **[SonicWall SonicOS SSLVPN flaw lets alternate credentials bypass SAML-enforced MFA](https://nvd.nist.gov/vuln/detail/CVE-2026-19868)** · composite 41.77 · _failed independent verification — The fetched source is only the KEV listing table; the SAML and MFA bypass mechanism in the summary, title and takeaway is not in it._
  Enforcing MFA through SAML on a SonicWall SSLVPN does not protect you if another login method on the same VPN still accepts just a password.
- **[OpenSSL patch proposed for EVP_EncodeBlock buffer overflow CVE-2026-121481](https://github.com/openssl/openssl/pull/33652)** · composite 41.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Fixing an overflow by adding an error return pushes work onto every caller, so check call sites and wait for the official advisory.
- **[Rikugan embeds a reverse-engineering agent inside IDA Pro and Binary Ninja](https://github.com/buzzer-re/rikugan)** · composite 40.85 · _flagged needs_review (low confidence / novelty / relevance)_
  An in-disassembler agent with parallel subagents and per-profile data and tool limits is a ready-made base for AI-assisted reverse engineering, but plan for hostile binaries…
- **[Attackers host AntiFox pentest platform on Alibaba Cloud to steal AWS secrets](https://www.bleepingcomputer.com/news/security/hackers-use-antifox-ai-agents-in-aws-credential-theft-attacks/)** · composite 40.54 · _failed independent verification — Verifier found lesson 4 (long-term keys in app config as the root exposure) unsupported by the source and deleted it, and softened lesson 2 and the summary wording._
  Hunt for successful AWS calls hidden in bursts of denials that follow web-tier compromise.
- **[America bans imported robots due to supply chain and security risks](https://www.theregister.com/security/2026/07/29/america-bans-imported-robots-due-to-supply-chain-and-security-risks/5280145)** · composite 40.5 · _news story: excerpt not grounded in source_
  US regulators are treating networked physical robots as a critical-infrastructure supply-chain risk category on par with telecom gear.
- **[@_rybaz and @GrahamHelton3 publish their vulnerability-research harness workshop materials](https://x.com/_rybaz/status/2119828361044246643)** · composite 40.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A pointer to public workshop material on building agent harnesses for vulnerability research; the content is unreviewed here, so read it before relying on it.
- **[Backdoored fragment-api-py release drains users' crypto wallets when the client opens](https://safedep.io/blog/fragment-api-py-pypi-ton-wallet-drainer)** · composite 40.12 · _flagged needs_review (low confidence / novelty / relevance)_
  A package that holds secrets such as wallet seeds can steal them through a single version bump, so pin versions and treat untagged releases as suspect.
- **[StepSecurity launches scanning for files planted by supply chain campaigns](https://www.stepsecurity.io/blog/malicious-files-find-what-supply-chain-attacks-leave-behind-in-your-github-repositories-and-on-developer-machines)** · composite 40.02 · _flagged needs_review (low confidence / novelty / relevance)_
  Scan every ref, not just the default branch, for planted editor, agent and workflow files, because dependency scanners never see them.
- **[Cisco BroadWorks XML external entity flaw is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-20320)** · composite 39.64 · _flagged needs_review (low confidence / novelty / relevance)_
  Patch BroadWorks per Cisco advisory cisco-sa-bworks-xxe-uwUd7CEt; CISA lists the flaw as exploited.
- **[VibeRaven statically checks AI-built Supabase apps for row-level security gaps](https://github.com/ohad6k/VibeRaven)** · composite 38.51 · _failed independent verification — Verifier rated novelty 12 vs 45: the RLS, service_role and dashboard-blind-spot points are standard Supabase docs and Security Advisor lints; only the vendor's 512-repo statistic is new, and the push-to-main point is an unsupported README assertion._
  For AI-built Supabase apps, the common gaps are database authorization mistakes such as missing row-level security (RLS), anon-callable definer functions and leaked service_role…
- **[AWS security practitioners rank the top 10 AWS research of 2026](https://awssecuritydigest.com/top-research/2026/)** · composite 38.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Use the list as a reading queue: two of the four visible items show multi-tenant and sandbox boundaries failing on one missed check.
- **[vibe-shield scans AI-written Next.js and Supabase apps for agent-typical bugs](https://github.com/avivgerz-hue/vibe-shield)** · composite 38.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent-written web apps fail in predictable ways, like missing auth, RLS and secret boundaries, so a narrow rule set aimed at those shapes is a cheap pre-merge gate.
- **[CVM-Store paper protects confidential VM storage at near-raw disk speed](http://arxiv.org/abs/2610.34560v1)** · composite 37.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Running in a confidential VM does not protect data on disk; stored data needs its own integrity and rollback protection.
- **[Google Cloud says Advanced Micro Devices (AMD) Turin VMs need guest patches](https://thehackernews.com/2026/11/google-cloud-warns-three-amd-turin-cpu.html)** · composite 37.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Google tells all affected Turin-based Google Cloud Platform (GCP) VMs to install the guest kernel fix and stop-and-start the VM; rebooting the guest OS is not enough.
- **[UnrealIRCd flaw lets any user inject server-to-server commands](https://nvd.nist.gov/vuln/detail/CVE-2026-114713)** · composite 37.36 · _failed independent verification — Summary claim 'CISA added it to its KEV catalog on 2026-11-13' is not in the raw NVD page; it only comes from entry metadata or a corroborating article._
  If you run linked UnrealIRCd servers, upgrade to 6.2.7.1 or later now, since the bug is on CISA's exploited list.
- **[Datadog explains how Entra access packages can become a privilege-escalation path](https://securitylabs.datadoghq.com/articles/entra-access-packages-part-1-privileges/)** · composite 36.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Audit who can manage catalogs and access packages in both Entra and ID Governance, and treat role-assignable groups in catalogs as privileged.
- **[CISA adds exploited Synology DSM code-execution flaw CVE-2024-10441 to its KEV catalog](https://nvd.nist.gov/vuln/detail/CVE-2024-10441)** · composite 36.59 · _flagged needs_review (low confidence / novelty / relevance)_
  If any Synology NAS is reachable from the internet, update DSM or BeeStation OS to the fixed builds immediately, since this is now a confirmed exploited bug.
- **[CISA adds 2024 Apple pointer authentication bypass to exploited catalog](https://nvd.nist.gov/vuln/detail/CVE-2024-27834)** · composite 35.77 · _failed independent verification — The fetched source is only the NVD reference table; it does not describe the pointer authentication bypass or say APT29 exploited this CVE, and the CVE is already covered by the Midnight Blizzard entry._
  Devices still on pre-mid-2024 Apple builds are exposed to a pointer authentication bypass that a nation-state group uses in exploit chains.
- **[F5 patches two critical NGINX HTTP/2 flaws, Imperva tells customers](https://www.imperva.com/blog/critical-nginx-http-2-vulnerabilities-cve-2026-123633-and-cve-2026-123007-what-imperva-customers-need-to-know/)** · composite 35.71 · _failed independent verification — The fetched page is truncated after the title and byline; the body says nothing about WAF coverage, customer exposure or Imperva protection. The lesson is the extractor's own generalisation, supported by neither the title nor the excerpt._
  Patch NGINX to the F5 fixed releases and check the Wiz and F5 advisories for exact affected configurations; this Imperva page adds little beyond the notice.
- **[VibeRaven checks AI-built Supabase apps for missing row-level security](https://github.com/ohad6k/VibeRaven)** · composite 34.61 · _flagged needs_review (low confidence / novelty / relevance)_
  Vibe-coded Supabase apps fail in a handful of predictable ways, and a static check in CI can catch several of them before launch.
- **[X post claims Mirage2FA stole 4,561 Microsoft 365 session cookies](https://x.com/Dinosn/status/2116946099059511340)** · composite 34.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Adversary-in-the-middle proxies keep beating one-time-code multi-factor authentication; phishing-resistant sign-in is the fix, but this claim needs a primary source.
- **[raml-kql runs one KQL query across workspaces without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql)** · composite 34.25 · _flagged needs_review (low confidence / novelty / relevance)_
  MSSPs without a Defender MTO can hunt across customer Sentinel workspaces from one query with delegated access only.
- **[Semgrep Guardian adds an adversarial reviewer and blocks risky lockfile changes](https://semgrep.dev/blog/2026/semgrep-guardian-policies-ai-detection)** · composite 33.95 · _flagged needs_review (low confidence / novelty / relevance)_
  A product update that applies two known patterns to coding agents: an independent adversarial reviewer and write-time gating of lockfile changes. No efficacy data is given.
- **[Mozilla says Apple's iOS rules still block any non-WebKit browser engine](https://blog.mozilla.org/en/mozilla/internet-policy/apple-ios-browser-engine-rules/)** · composite 33.75 · _failed independent verification — Lesson 4 (one engine's bugs affect every iPhone browser) is the extractor's inference; the post says nothing about shared bugs or security. The takeaway about engine-level fixes and security staying in Apple's hands is likewise not in the source._
  On iOS, every browser still runs on WebKit, so engine-level fixes and security behaviour stay in Apple's hands.
- **[SpecterOps announced Sage, an AI assistant for red teams inside Mythic](https://specterops.io/blog/2026/11/10/sage-ai-for-assumed-breach-operations-built-into-mythic/)** · composite 33.75 · _failed independent verification — Fetched page was an ad-tracker redirect with no article text; the summary rests on the feed teaser only._
  Unverified: refetch the SpecterOps post before relying on any description of Sage's human-approval or memory design.
- **[Sublime Security reports email attacks moving to calendar invites and QR codes](https://www.carriermanagement.com/news/2026/11/13/294121.htm)** · composite 33.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Email defenses that only scan text and URLs miss calendar invites, QR images and hijacked threads, so extend inspection to those channels.
- **[Splunk patches nearly 140 flaws in Enterprise, Enterprise Security and SOAR](https://www.securityweek.com/splunk-patches-nearly-140-flaws-across-three-core-products/)** · composite 32.97 · _failed independent verification — Lesson 4 says three smaller products were patched, but the source names only two (App for Stream with 3 flaws and AI Assistant with 4)._
  Move Splunk Enterprise to 10.6.1, 10.4.5, 10.2.9, 10.0.12 or 9.4.17, Enterprise Security to 8.7.0 and SOAR to 8.8.0, and restrict admin roles until then.
- **[CISA says a low-severity VMware ESX logging gap is being exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-41709)** · composite 32.75 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Do not deprioritize low-CVSS ESX logging bugs: attackers who already hold admin access use them to hide what they do.
- **[Chainguard rebuilds every buildable Linux distribution font from source](https://www.chainguard.dev/unchained/this-shit-is-hard-nobody-has-ever-been-pwned-by-helvetica-or-have-they)** · composite 32.64 · _flagged needs_review (low confidence / novelty / relevance)_
  Container images and distributions ship prebuilt fonts that rendering libraries execute, so treat them as unverified binaries in the supply chain. The concrete payoff of building…
- **[Socket finds 319 Chrome extensions that hijacked searches through operator servers](https://www.malwarebytes.com/blog/news/2026/10/fake-pdf-and-search-tools-hijacked-searches-for-13-4-million-chrome-users)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat an official-store listing as no trust signal for browser extensions, because unlisted, ad-promoted extensions can quietly proxy every search a user makes.
- **[Unit 42 post on the OPTIMJACK supply chain attack, body not captured](https://unit42.paloaltonetworks.com/optimjack-supply-chain-attack/)** · composite 31.23 · _failed independent verification — Summary says the feed blurb states OPTIMJACK is an attack where a compromised vendor script can expose websites and that strict segmentation is the lesson. The raw file contains no such blurb: grep for segmentation and vendor script finds nothing, and the file holds only the title, URL and site navi_
  Re-fetch the full Unit 42 article before drawing any lessons; the stored copy is navigation only.
- **[Chainguard describes a harness that replays AI-found exploits before reporting them](https://www.chainguard.dev/unchained/how-chainguards-frontier-ai-harness-keeps-your-code-safe)** · composite 31.18 · _flagged needs_review (low confidence / novelty / relevance)_
  The reusable idea is the reporting rule: only surface AI-found bugs that reproduce every time and whose fix is shown to stop the exploit.
- **[Unit 42 publishes defender guidance on attacker use of ARTEX](https://unit42.paloaltonetworks.com/artex-and-ai-powered-red-teaming-tools/)** · composite 30.6 · _failed independent verification — The capture holds only the title and site navigation; the lesson's claim that Unit 42 tracks attacker use of these tools is inferred from the title, not stated._
  As captured, it adds nothing beyond the ARTEX coverage already on file, so re-fetch it before use.
- **[Openwave Webtop Media Transcoder file-type restriction bypass is exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-111793)** · composite 29.14 · _failed independent verification — Verifier found the 'low score' label wrong (the vector computes to 4.3, Medium) and the UI-only enforcement mechanism inferred; text corrected, held for a human check._
  Operators of Openwave Webtop should upgrade the Media Transcoder to 1.1.22.0 and enforce file-type policy server-side.
- **[A new verifiable PIR protocol matches SimplePIR's online costs](http://arxiv.org/abs/2611.22911v1)** · composite 28.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Niche cryptography result: relevant only if you build private-retrieval systems; it changes nothing for AI or product security practice.
- **[Russian hackers reportedly use stealthy Exchange malware against government email](https://cyberinsider.com/russian-hackers-cereal-malware-microsoft-exchange-attacks/)** · composite 28.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Only a headline is available, so wait for the full CyberInsider or vendor report before acting on it.
- **[macOS 27 breaks normal access to encrypted HFS+ volumes on CoreStorage](https://wadetregaskis.com/macos-27-golden-gate-does-not-actually-support-corestorage-or-hfs-volumes/)** · composite 28.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Migrate CoreStorage and encrypted HFS+ volumes to APFS before upgrading to macOS 27, and have backups ready.
- **[Joost de Valk's open website specification covers security headers and agent readiness](https://github.com/jdevalk/specification.website)** · composite 27.8 · _flagged needs_review (low confidence / novelty / relevance)_
  A sourced, general web-standards checklist with a security section; useful as a reference, not new security research.
- **[PHP2Shell hits every PHP since 5.4, no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run PHP 8.1 or older, there is no patch: upgrade to 8.2+ or put network-level protection in front now.
- **[Researcher reports Samsung Tizen runs AlexNet on screen captures to identify games](https://twitter.com/mike64_t/status/2114150399406202896)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  When auditing TV/IoT firmware, check whether on-device ML screen capture runs before user consent, even if the output is dropped; here the evidence is a single unverified tweet.
- **[Microsoft Research podcast profiles Cyber Grand Challenge lead Mike Walker](https://www.microsoft.com/en-us/research/podcast/learn-the-rules-the-hacker-mindset/)** · composite 27.38 · _flagged needs_review (low confidence / novelty / relevance)_
  A career-profile podcast with little technical content, useful mainly as background on how autonomous hacking competitions began.
- **[Check Point weekly digest covers cPGuard supply-chain attack and ARTEX campaigns](https://research.checkpoint.com/2026/9th-november-threat-intelligence-report/)** · composite 27.29 · _flagged needs_review (low confidence / novelty / relevance)_
  A roundup with little new analysis; follow its links to the primary reports for anything actionable.
- **[Antithesis engineer Sean Allen says supply chain attacks have no simple fix](https://newsletter.pragmaticengineer.com/p/software-correctness)** · composite 25.88 · _flagged needs_review (low confidence / novelty / relevance)_
  Mostly a software-correctness conversation; its supply chain point (no simple fix) is a restatement with no new defense.
- **[Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/)** · composite 24.27 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated 'unpatched' (the source says 'did not indicate patched versions') and 'millions' (a reported figure). Text corrected; a secondary digest of already-covered stories._
  A news digest with nothing new, so use it as a checklist: PHP2Shell, LiteLLM 1.107.0, GitLab CVE-2026-110264, VeloCloud CVE-2026-114625, and AI-tool token theft.
- **[Citizen Lab and Princeton researchers win IRTF prize for Android network security](https://citizenlab.ca/citizen-lab-researchers-win-irtf-applied-networking-research-prize/)** · composite 24.12 · _flagged needs_review (low confidence / novelty / relevance)_
  An award announcement with no new findings; read the underlying paper on proprietary encryption in Android apps instead.
- **[Northstar Security leaves stealth with $7M to find risky issue combinations](https://www.securityweek.com/northstar-security-exits-stealth-with-7m-to-expose-toxic-risk-combinations/)** · composite 23.82 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding announcement: the idea of scoring combined exposures, not single findings, is established, and the source has no results to judge.
- **[MagicSword markets automatic application-control policies built from LOLDrivers research](https://www.magicsword.io/application-control)** · composite 23.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Marketing for a product; the useful idea is blocking known-abused legitimate tools by default, which the free LOL catalogs already support.
- **[Iris Plaza says a cloud breach exposed data on 7.7 million customers](https://cyberinsider.com/iris-plaza-cloud-breach-7-7-million-people/)** · composite 23.25 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a thin breach notice with no root cause or lessons, so it is useful only as a data point.
- **[Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a public, live test of PHP2Shell exploitability; a non-zero hack counter would be a signal to speed up PHP patching, but the page itself contains no technical detail.
- **[Brava Security raises seed funding for AI attack-telemetry simulation](https://www.securityweek.com/brava-security-emerges-from-stealth-with-15-million-in-funding/)** · composite 22.05 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a funding story, but its point holds: AI-driven SOC (security operations center) triage only covers what your detections actually fire on.
- **[Wiz says it is not yet listed on Japan's government cloud registry](https://www.wiz.io/blog/wiz-and-ismap-for-japan-public-sector)** · composite 22.05 · _flagged needs_review (low confidence / novelty / relevance)_
  For Japanese public-sector buyers, Wiz is not on the ISMAP list and will not be before its 2027 audit; otherwise this is vendor compliance news with no security findings.
- **[GoSQLX, a Go SQL parser, ships an injection scanner and MCP server](https://github.com/ajitpratap0/GoSQLX)** · composite 22.01 · _flagged needs_review (low confidence / novelty / relevance)_
  A handy SQL parser with an agent interface, but nothing new for security; its injection scanner is unmeasured.
- **[Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise)** · composite 21.75 · _flagged needs_review (low confidence / novelty / relevance)_
  General incident-readiness advice that works as a checklist, with nothing new.
- **[Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto)** · composite 20.09 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated features (CI/CD and mirrored traffic partly Enterprise-only; SSRF and JWT tests only named as examples) and inferred JVM code execution. Text corrected; a vendor README with marketing tagline._
  A known open-source API-testing tool with an AI-security tagline, but its README shows no AI- or MCP-specific capability, so judge it as an API testing tool.
- **[Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8)** · composite 20.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A possible cross-runtime RCE is circulating, but this capture has no details; get the primary Aikido or vendor advisory before acting.
- **[Book claims Dutch government hacked Jared Kushner's phone, which Kushner denies](https://twitter.com/jaredkushner/status/2113376217415958767)** · composite 15.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a disputed political allegation with no technical content; treat it as unconfirmed news, not threat intelligence.

## AI Research (112)

- **[How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/)** · composite 59.62 · _news story: excerpt not grounded in source (only 0% of quotes verified)_
  In AI bug hunting, outcome definition and per-agent scoping drive output quality most, with a threat-model file as the highest-leverage input.
- **[METR finds frontier models can reliably tell alignment evals from capability evals](https://metr.org/notes/2026-11-16-measuring-alignment-eval-tells/)** · composite 54.54 · _flagged needs_review (low confidence / novelty / relevance)_
  If you build alignment or propensity evals by mocking real tasks, test whether a model can spot them, because a detectable eval may overstate how safe the model is.
- **[Anthropic tests which agent memory practices help Claude across sessions](https://www.anthropic.com/research/components-of-agent-memory)** · composite 53.52 · _failed independent verification — Lessons hold, but the verifier rated novelty 33 vs 68 (sleep-time compute, Karpathy's LLM wiki, Letta tiers) and flagged single-run evidence; the summary was corrected to keep the wiki-only caveat and the small search-plus-wiki gain._
  Tell the agent what memory is for, keep the always-loaded layer small, and regularly check notes against transcripts so wrong notes do not carry forward.
- **[Eugene Yan finds graders failed valid work in eight of twelve evals](https://eugeneyan.com/writing/public-evals)** · composite 51.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Read a benchmark score as a model-plus-harness-plus-grader result, and audit the grader before trusting the ranking.
- **[Anthropic shares how it designs, runs and grades model safety evaluations](https://www.anthropic.com/research/building-strong-safety-evaluations)** · composite 51.51 · _failed independent verification — Lessons hold, but the verifier rated novelty 30 vs 55: the post mostly consolidates known eval practice (Anthropic's earlier agent-evals guide, XSTest/OR-Bench over-refusal work); the 'refusal rate is wrong' point is scoped to self-harm in the source._
  A safety claim is only as sound as the eval behind it, so measure appropriate behavior across whole conversations and watch the grader as closely as the model.
- **[METR says AI R&D capabilities rise fast as evals get harder](https://metr.org/blog/2026-11-20-q4-2026-capability-update/)** · composite 50.04 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat easy-to-run benchmark scores as an upper bound on real-world ability, and expect weaker results on tasks with long feedback loops.
- **[UK AISI releases Transect to review long agent evaluation transcripts](https://www.aisi.gov.uk/blog/transect-making-large-scale-agentic-evaluations-easier-to-understand)** · composite 48.48 · _flagged needs_review (low confidence / novelty / relevance)_
  When you review agent eval runs, keep judge labels linked to transcript evidence and look at where judges disagree.
- **[Apple finds the strongest LLM judges do not best match humans](https://machinelearning.apple.com/research/evaluating-evaluators-llm-judges)** · composite 47.82 · _flagged needs_review (low confidence / novelty / relevance)_
  Pick and validate LLM judges against human labels for each task and criterion, use pairwise comparison, and don't assume the biggest model judges best.
- **[ScrapeBench measures whether web agents honor terms of service and robots.txt](https://arxiv.org/abs/2611.11306)** · composite 46.27 · _flagged needs_review (low confidence / novelty / relevance)_
  The paper reports low compliance for most agents; as the tracker's recommendation, do not assume a web agent respects robots.txt or terms of service (ToS) on its own, enforce…
- **[Legora evaluates legal agent on simulated work because it cannot read traces](https://latent.space/p/building-ai-for-lawyers-jacob-lauritzen-cto-of-legora/)** · composite 44.94 · _flagged needs_review (low confidence / novelty / relevance)_
  When you cannot read customer traces, build simulated task worlds with domain experts and track results per task type, because a new model can regress on some tasks while…
- **[Anthropic study finds analysts follow an agent's hidden lean on judgment calls](https://www.anthropic.com/research/agents-judgment-calls)** · composite 44.78 · _flagged needs_review (low confidence / novelty / relevance)_
  If your harness relies on a human to make or check judgment calls, the agent's framing will often make the call instead, so design for that.
- **[DeepStress finds deep search agents trust low-credibility and wrong evidence](https://arxiv.org/abs/2607.13920)** · composite 44.74 · _flagged needs_review (low confidence / novelty / relevance)_
  Before trusting a search or RAG agent's accuracy score, test it on deliberately degraded evidence and check whether it is answering from memory instead of its sources.
- **[MASTA multi-agent system turns protocol descriptions into Tamarin formal models](http://arxiv.org/abs/2611.20671v1)** · composite 43.8 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent builders, a verifier-driven scheduler with separate author and auditor roles is a concrete pattern for tasks where a tool gives a hard pass or fail signal.
- **[Apple researchers train small networks that speed up vector retrieval for RAG](https://machinelearning.apple.com/research/faster-retrieval)** · composite 43.62 · _flagged needs_review (low confidence / novelty / relevance)_
  If your RAG system serves a stable query distribution, a small learned query mapper can cut retrieval latency without replacing your vector index.
- **[Token-Goat hooks coding agents to cut repeat reads and bulky tool output](https://github.com/DFKHelper/token-goat)** · composite 43.08 · _flagged needs_review (low confidence / novelty / relevance)_
  Most agent token waste is repeat reads and noisy tool output, which hooks can trim without changing the model.
- **[Cisco's MAS Lab builds and traces multi-agent systems from YAML specs](https://github.com/ioc-project/mas-lab)** · composite 43.01 · _flagged needs_review (low confidence / novelty / relevance)_
  Keeping MCP and A2A in an adapter layer lets you test agent logic locally and review protocol security in one place.
- **[OpenAI ships cheaper GPT-6.2 Astra and Sol to mixed early reviews](https://latent.space/p/ainews-gpt-6-2-astra-the-2-frontier-model-is-better-and-20-600-cheaper-but-has-mixed-reviews-6-2-sol/)** · composite 41.55 · _flagged needs_review (low confidence / novelty / relevance)_
  A cheaper new model is not automatically a better fit for your harness; re-measure cost per passing task and rerun your harness before switching.
- **[Google ships Gemini 4 Carbon to trusted cyber defenders first](https://latent.space/p/ainews-gemini-4-carbon/)** · composite 39.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A strong new model for vulnerability work, but its cyber scores come from Google and its hallucination rate went up, so validate it on your own triage tasks before you trust its…
- **[Microsoft evaluates Copilot on fully synthetic, time-evolving enterprise tenants](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/)** · composite 39.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For assistants that work over private workspace data, a reproducible synthetic world with a timeline lets you regression-test without touching customer data.
- **[TRACES.md proposes a plain-text format for recording what coding agents did](https://github.com/MaxonT/TRACES.md)** · composite 39.14 · _flagged needs_review (low confidence / novelty / relevance)_
  If you log agent tool calls from hooks, register the failure event as well as the success event and check that a forced failure shows up.
- **[Ratel loads agent tools and skills per turn through BM25 search](https://github.com/ratel-ai/ratel)** · composite 38.77 · _flagged needs_review (low confidence / novelty / relevance)_
  A packaged version of on-demand tool loading; the idea is not new and the repo was covered earlier, so evaluate it only if you need a drop-in library.
- **[Rubric Curriculum RL uses pairwise rubric judging to make reward hacking harder](http://arxiv.org/abs/2611.06244v1)** · composite 37.8 · _flagged needs_review (low confidence / novelty / relevance)_
  When an LLM judge grades open-ended output against a rubric, pairwise comparison with rotating criteria is more discriminative and harder to game than a fixed absolute score.
- **[Matt Pocock's dictionary says to keep AGENTS.md short](https://www.aihero.dev/ai-coding-dictionary/agents-md)** · composite 37.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat AGENTS.md as a short brief of things that apply everywhere, and move everything else to progressive disclosure.
- **[Sean Goedecke argues Astra's weight editing matches what a skilled researcher would do](https://www.seangoedecke.com/llms-are-not-superhuman-at-reading-and-writing-neural-network-weights/)** · composite 37.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Read the weight-space-programming result as an LLM running a known interpretability-and-steering recipe, not as evidence that models can now improve other models better than…
- **[Handshake AI demos the agent benchmarks it builds for frontier labs](https://latent.space/p/handshake/)** · composite 37.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Grade agents on their tool-call trace and intermediate actions, not only the final answer, and test graders for gaming.
- **[Nvidia RTX Spark laptops throttle local LLMs on Linux when plugged in](https://www.mindstudio.ai/blog/linux-nvidia-rtx-spark-laptop)** · composite 36.75 · _flagged needs_review (low confidence / novelty / relevance)_
  On RTX Spark laptops, benchmark local inference under WSL or on battery; native Linux on wall power is throttled.
- **[ICML authors certify graph neural networks against label and structure poisoning](http://arxiv.org/abs/2611.03350v1)** · composite 36.3 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a theoretical robustness advance for GNN training, with little direct use for LLM, agent, or appsec defenders.
- **[Fowler links CodeScene study on code health and agent review cost](https://martinfowler.com/fragments/2026-11-20.html)** · composite 35.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Code quality may lower the cost of agent work, but this is a secondhand summary of one vendor experiment and the post does not give full method details.
- **[EEP proposes signed push events so agents can follow entities](https://github.com/eep-dev/EEP)** · composite 35.51 · _ungrounded excerpt — only 50% of quotes verified against the source_
  Another early agent protocol; the useful idea is signed, replay-bounded push events instead of scraping.
- **[Output caching saves little because most output tokens are invisible, says Goedecke](https://seangoedecke.com/why-output-caching-doesnt-work/)** · composite 35.25 · _flagged needs_review (low confidence / novelty / relevance)_
  To cut output-token cost, reduce reasoning and tool-call tokens (smarter model, better harness) rather than deduplicating visible output.
- **[Matt Pocock's dictionary splits hallucinations into factuality and faithfulness](https://www.aihero.dev/ai-coding-dictionary/hallucination)** · composite 35.25 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful diagnostic framing for coding agents (add context vs compact), stated as opinion with no data.
- **[Simon Willison folds agent-written PR descriptions under a human summary](https://simonwillison.net/2026/Nov/9/details-summary/)** · composite 35.22 · _flagged needs_review (low confidence / novelty / relevance)_
  Lead agent PRs with a short, human-vetted opener and collapse the agent's full write-up under a label that names the model.
- **[Arca's wealth agents run ten-day tasks while human advisors move money](https://latent.space/p/arca/)** · composite 34.97 · _flagged needs_review (low confidence / novelty / relevance)_
  For long, stop-start agent work in a regulated field, keep state in a shared memory and put every risky action behind deterministic rules, not model judgment.
- **[Anthropic study finds scientists use Claude mostly for data analysis and writing](https://www.anthropic.com/research/how-researchers-use-claude)** · composite 34.48 · _flagged needs_review (low confidence / novelty / relevance)_
  Researchers adopt AI where it already works well, and specialized tool-connected setups shift use toward harder tasks, but this is adoption measurement, not a harness technique.
- **[Apple researchers derive the maximum reward gain KL-regularized alignment can achieve](https://machinelearning.apple.com/research/theoretical-limits-alignment)** · composite 34.44 · _flagged needs_review (low confidence / novelty / relevance)_
  This theory mostly serves people training reward-tuned models, and for agent builders it only confirms that best-of-N with a good scorer is a strong baseline.
- **[Rivet runs each agent loop outside the sandbox as a lightweight actor](https://github.com/rivet-dev/rivet)** · composite 34.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Separating the agent loop from the code sandbox is a sound pattern for cost and blast radius, but the performance figures come from the vendor.
- **[SpecForge compiles team rules into checks that agents cannot skip](https://github.com/leaderiop/SpecForge)** · composite 33.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Move the rules an agent must obey out of the prompt and into a deterministic check that fails, the same way tests gate code.
- **[Flide is an inference engine that serves Jev-style decision models faster](https://github.com/OmniJev/Flide)** · composite 33.75 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run many classification-style decisions over the same context, state forking and session caching can cut latency without changing answers, though the speedups are…
- **[Huawei open-sources MACaQ, a model-agnostic quantizer for GGUF and vLLM](https://github.com/huawei-csl/MACaQ)** · composite 33.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Another open quantizer with self-reported gains; worth a benchmark if you serve local GGUF or W4A4 (4-bit weights and activations) models.
- **[Ricapar runs a Claude coding agent harness natively on an 8088 PC](http://ricapar.net/ClawDOS/)** · composite 33.75 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful agent harness needs little more than a message loop, a small tool set, cached prompts and a confirm step for writes.
- **[SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench)** · composite 32.87 · _failed independent verification — Verifier: excerpts verbatim and dataset sizes correct, but the draft over-reached (author attribution, regression-catching inference, filler lesson). Text corrected; held as an old 2024 benchmark README with low novelty._
  If your coding agent claims it reproduced a bug, require a test that fails before the fix and passes after. SWT-Bench is a ready-made harness for measuring how often it can.
- **[Workshop paper proposes retrieval as local traversal through a memory address space](http://arxiv.org/abs/2610.40545v1)** · composite 31.55 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an early architecture hypothesis that stateful retrieval is easier to learn than stateless retrieval, not something harness builders can use yet.
- **[Tencent's Hy4 system card includes a third-party loss-of-control evaluation](https://x.com/NeelNanda5/status/2123889182301139248)** · composite 31.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Third-party pre-release safety evals are now appearing in system cards from Chinese labs, but this post gives no results.
- **[A Thomson Reuters engineer runs a coding agent fully offline with Qwen](https://latent.space/p/offline-coding/)** · composite 31.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A 9B local model with OpenCode can handle small, test-backed fixes offline, but the source shows only one trivial task.
- **[Paper finds shared activation directions behind LLM abstention across three causes](https://arxiv.org/abs/2611.20441)** · composite 31.21 · _flagged needs_review (low confidence / novelty / relevance)_
  Interesting interpretability result, but it offers no direct change to harness, agent or defensive practice; track it as background.
- **[A former Meta engineer argues AI coding makes codebases fragile](https://evanxmerz.com/post/ai-usage-generates-a-fragile-codebase/)** · composite 30.75 · _flagged needs_review (low confidence / novelty / relevance)_
  One engineer's anecdotal case that AI coding raises incidents; track incident counts and recovery time yourself rather than trusting output volume.
- **[SAFT adversarially trains only robustness-critical parameters and beats LoRA](http://arxiv.org/abs/2610.39455v1)** · composite 30.05 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a model-training result for classic adversarial robustness and has little direct use for agent or harness builders.
- **[Latent Space roundup highlights LLMs reading and editing other models' weights](https://latent.space/p/ainews-llms-can-read-write-neural-network-weights-weight-space-programming-cuts-autoresearch-out-of/)** · composite 29.82 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a news roundup with little detail of its own on weight-space programming, so the paper and the existing critique of it are the better sources.
- **[Daniel Miessler argues harnesses should describe what you want, not steps](https://danielmiessler.com/blog/models-how-harnesses-what)** · composite 29.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Spend harness effort on user context and definitions of done rather than step-by-step scripts, as a heuristic, not a measured result.
- **[Amazon Science blog says proof-checking tools let AI help mathematics without hallucinations](https://www.amazon.science/blog/mathematical-proof-powered-by-ai-and-no-hallucinations)** · composite 28.62 · _failed independent verification — The captured text is only site navigation and the title. 'Machine-checked' and any method are not in the source, so it cannot support the lesson._
  The idea is to pair a generative model with a proof checker so wrong output is caught mechanically, but details were not captured.
- **[Workshop paper proposes retrieval as a local walk through memory](http://arxiv.org/abs/2610.40545v1)** · composite 28.55 · _flagged needs_review (low confidence / novelty / relevance)_
  An interesting idea for stateful agent memory, but a single toy experiment gives a harness builder nothing to use yet.
- **[Poteto's pstack v0.15.46 shortens skills and adds Gemini reviewer](https://x.com/poteto/status/2123824683862855898)** · composite 28.5 · _failed independent verification — Source is a 3-line tweet. Lesson 1 (skill bloat is a maintenance cost) is an inference; the tweet only says skills were pruned and gives no reason or evidence._
  A skill pack can trim its own prompts and route review work across several models, but this post gives no measurements.
- **[Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193)** · composite 28.34 · _flagged needs_review (low confidence / novelty / relevance)_
  If your agent rewrites its own prompts, memory or tools, re-verify after each change against a held-out evaluation it cannot edit.
- **[Titus Winters says AI raised code output and outages, not features shipped](https://newsletter.pragmaticengineer.com/p/software-engineering-at-google-and)** · composite 28.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Judge AI-assisted engineering by outages and delivered features, not code volume, and wrap large AI rewrites in the coexist, shard and block-the-old discipline Google used before…
- **[Context-Regularized Cross-Entropy makes image classifiers rely less on background context](http://arxiv.org/abs/2611.08157v1)** · composite 27.9 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a vision-training result about spurious background cues in convolutional neural networks (CNNs), with no direct use for LLM harness or agent builders.
- **[Bengio and collaborators publish a 182-page survey on mechanistic interpretability](https://x.com/askalphaxiv/status/2119836067591573781)** · composite 27.6 · _flagged needs_review (low confidence / novelty / relevance)_
  A broad reading map for model internals, not a practical change for anyone building agents or harnesses.
- **[CANTraj benchmark shows vehicle CAN signals can rebuild driving routes without GPS](https://arxiv.org/abs/2611.18442)** · composite 27.31 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat vehicle telemetry such as speed and steering as location data when judging whether a dataset is anonymized.
- **[Daniel Miessler frames AI work as hill-climbing against ideal-state evals](https://danielmiessler.com/blog/general-hill-climbing)** · composite 27.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat the written ideal state as the source of your verification criteria, and update the evals whenever passing output still feels wrong.
- **[Simon Willison's Claude-run review finds webframe fast but rough for scraping](https://simonwillison.net/2026/Oct/26/webframe-evaluation/)** · composite 27.05 · _flagged needs_review (low confidence / novelty / relevance)_
  webframe is a lightweight way to run page JavaScript from scripts, but do not treat it as a sandbox without your own isolation.
- **[Sparse Adversarial Fine-Tuning (SAFT) updates only about 5% of a network's parameters](http://arxiv.org/abs/2610.39455v1)** · composite 27.05 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful efficiency result for adversarial robustness research, with no direct bearing on securing LLM agents.
- **[Matthew Berman tells coding agents to show video mocks of UI changes](https://x.com/MatthewBerman/status/2117670441380966696)** · composite 26.4 · _failed independent verification — The source is a one-line instruction; lesson 1's claim that humans review behavior, not just diffs, is the analyst's inference, not in the post._
  Asking the agent for visual evidence of UI changes is a cheap review habit, but the post adds nothing beyond the instruction.
- **[Amazon Science published Mitra-v2, a synthetically pretrained tabular foundation model](https://www.amazon.science/blog/mitra-v2-scaling-synthetic-pretraining-for-tabular-foundation-models)** · composite 25.88 · _failed independent verification — Fetched page held only navigation; claims come from the feed teaser._
  Off-thesis tabular ML research with no usable captured text; record as news only.
- **[Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges)** · composite 25.85 · _failed independent verification — Verifier refuted 'interviewees agree public rankings only shortlist candidates' (one Sonar quote) and 'harness matters as much as the model' (Dream's view alone); Sonar's leaderboard measures quality and security, not secure generation only._
  Choose models for security work with your own task evaluations and a defined failure budget; leaderboards are only a shortlist.
- **[Matt Pocock's AI Coding Dictionary defines an agent as model plus harness](https://www.aihero.dev/ai-coding-dictionary/agent)** · composite 25.65 · _flagged needs_review (low confidence / novelty / relevance)_
  A vocabulary page, useful for team terminology but with no new finding.
- **[Bound-conditioned latent inference cuts progressive image codec BD-rate on Kodak](http://arxiv.org/abs/2610.30966v1)** · composite 25.55 · _flagged needs_review (low confidence / novelty / relevance)_
  A solid image-compression result, but it has no bearing on securing or building AI agents and harnesses.
- **[PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1)** · composite 25.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Medical ML result, off-thesis here: the general point is not to treat an accuracy leaderboard as a stand-in for calibration under low labels or domain shift.
- **[Addy Osmani argues that working with coding agents is a management job](https://x.com/addyosmani/status/2119332146485891501)** · composite 25.5 · _flagged needs_review (low confidence / novelty / relevance)_
  The framing is useful but the captured source is a teaser with no concrete practices behind it.
- **[Theo reacts to the Gemini 4 Neon launch before testing it](https://x.com/theo/status/2123207527064318174)** · composite 25.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A new model claim to check on your own task set, not a finding to cite.
- **[Moonshot's Kimi K3.1 Pro nears frontier scores, with open weights promised](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/)** · composite 25.49 · _flagged needs_review (low confidence / novelty / relevance)_
  A near-frontier open-weight option at half Opus pricing is worth benchmarking on your own agent tasks once the weights ship.
- **[Researchers' VA-TDM method improves four-step image and video diffusion generation](https://arxiv.org/abs/2611.06796)** · composite 25.44 · _flagged needs_review (low confidence / novelty / relevance)_
  This off-thesis diffusion research matters only if you serve image or video generation and want fewer sampling steps.
- **[FAF registers YAML media types for portable AI project context files](https://github.com/Wolfe-Jam/faf)** · composite 24.7 · _failed independent verification — Not sent to a verifier: a promotional README with no testable finding; low scores, held for review._
  A context-file format with marketing but no evidence; existing AGENTS.md-style files do the same job.
- **[Hacker News developers describe fatigue from AI-era coding and agent review](https://news.ycombinator.com/item?id=50301479)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Human review capacity, not agent output, is now the bottleneck, so harnesses should cut what humans must read and prove that tests actually test something.
- **[CurvDelta constrains LLM weight updates to low-curvature directions to preserve capabilities](https://arxiv.org/abs/2611.24654)** · composite 24.2 · _flagged needs_review (low confidence / novelty / relevance)_
  Model-internals research on fine-tuning and unlearning; little direct use for harness or agent builders.
- **[MCP Explained site walks through how the Model Context Protocol works](https://mcp-explained.com/)** · composite 24.15 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful primer for newcomers, but the captured text adds nothing new for security or harness builders.
- **[Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)** · composite 23.98 · _flagged needs_review (low confidence / novelty / relevance)_
  Governance news only: Agent Skills is now a Linux Foundation-hosted standard like MCP, and nothing changes technically today.
- **[Anthropic reports early results from Claude-driven drug development partnerships](https://www.anthropic.com/research/early-progress-drug-development)** · composite 23.64 · _flagged needs_review (low confidence / novelty / relevance)_
  The reusable idea in this off-field vendor report is to check agent review against known human findings before relying on it.
- **[Show HN game puts you in the role of an LLM manager's subagent](https://github.com/gulivan/worker755)** · composite 23.25 · _flagged needs_review (low confidence / novelty / relevance)_
  A playful way to feel how an orchestrator treats a subagent's output; no research claims or measurements.
- **[Theo endorses a quick guide on which coding-agent harness to use](https://x.com/theo/status/2119329490568691717)** · composite 22.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a biased opinion with no measurements, so treat it as a list of options to try rather than a recommendation.
- **[Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models)** · composite 22.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A hands-on resource for understanding the reasoning model inside agents; teaching material, not a new finding.
- **[alphaXiv says its 4B decision model nearly matches Jev except sarcasm](https://x.com/askalphaxiv/status/2116199951835582507)** · composite 22.25 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an unverified vendor claim, and small decision models still have to be benchmarked on your own data, as earlier pool entries showed.
- **[Claude Opus 5.5 ports a Three.js scene to plain WebGL](https://simonwillison.net/2026/Nov/9/hn-50421091/)** · composite 21.72 · _flagged needs_review (low confidence / novelty / relevance)_
  One anecdote shows a frontier model can drop a 3D library dependency, and it says little a harness builder can act on.
- **[A tensor-train method solves constrained combinatorial optimization with symmetric tensors](http://arxiv.org/abs/2611.22557v1)** · composite 21.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Off-thesis optimization paper: nothing here for AI security, product security or agent builders.
- **[Theo reposts his week-old take that Gemini 4 Carbon hallucinates](https://x.com/theo/status/2123889748100169862)** · composite 21.6 · _flagged needs_review (low confidence / novelty / relevance)_
  A single influencer reaction is not evidence about Gemini 4 Carbon, so judge it on your own tasks.
- **[A spacecraft pose study finds calibrated confidence fails on real images](https://arxiv.org/abs/2611.20321)** · composite 21.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Off-thesis vision result: the one portable idea is to check calibration on real data, never only on the simulator.
- **[Datasette stops sending Firefox rel=next link headers that trigger prefetches](https://simonwillison.net/2026/Nov/7/link-rel-next/)** · composite 21.48 · _flagged needs_review (low confidence / novelty / relevance)_
  If your app sends rel=next link headers on costly paginated HTML pages, Firefox may be making your server render pages nobody looks at.
- **[Jimmy Miller explains partial evaluation and ships a JavaScript partial evaluator](https://jimmyhmiller.com/magic-of-partial-evaluation)** · composite 21.15 · _failed independent verification — Lessons hold, but the verifier scored novelty 12 against 30 and relevance 8: a textbook programming-language explainer with no agent-harness content._
  Interesting programming-language background, but off-thesis for security or harness work.
- **[Anthropic resolved a two-hour Claude login outage on November 13](https://status.claude.com/incidents/nn11wk485zfn)** · composite 20.25 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a short outage notice with no root cause, useful only as a reminder to plan provider fallbacks for agent workflows.
- **[Framework-free Colab notebooks teach the applied LLM engineering stack](https://github.com/calmrocks/ai-engineer-notebooks)** · composite 19.84 · _flagged needs_review (low confidence / novelty / relevance)_
  A reasonable onboarding course for engineers new to LLM apps; no new technique.
- **[@_rybaz argues agent solutions alone do not make a good business](https://x.com/_rybaz/status/2117660118682923408)** · composite 19.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Thin opinion post with no technical content; skip unless tracking conference sentiment.
- **[Inference.net advertises spare B200/B300 GPU capacity for hosting open models](https://x.com/MatthewBerman/status/2123594970502414493)** · composite 19.8 · _failed independent verification — Lesson 1 asserts the ad 'hints at looser supply'; the tweet only says a provider has capacity available. The looser-supply reading is speculation not in the source._
  A sales post with no technical content; at most a weak signal that GPU supply for hosting open models is loosening.
- **[0xMovez shares Afterglow, a gallery of animated themes for Claude Code](https://afterglow-themes.vercel.app/)** · composite 19.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Cosmetic theming for a coding agent client; nothing to act on for a security or harness reader.
- **[alphaXiv tally ranks Together AI first in 2026 AI-cloud publications](https://x.com/askalphaxiv/status/2120927603385331926)** · composite 19.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Industry trivia with no method; not actionable for harness builders.
- **[Anthropic expands AI for Science credits to 20 foundations and institutions](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions)** · composite 18.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding and partnership announcement with nothing to change in a harness, apart from noting the Model Hardware Standard for agents that drive physical instruments.
- **[HackerBooks lists 16,543 books mentioned in Hacker News comments](https://hackerbooks.org)** · composite 18.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Off-topic for security and agent builders: a book directory with no technique to learn from.
- **[Theo posts that he loves his iPhone Duo and cannot go back](https://x.com/theo/status/2122856187729424869)** · composite 17.4 · _failed independent verification — Summary calls the author 'a developer'; the three-line post never says so (minor, from author context only)._
  Off-thesis personal gadget opinion; nothing here for security or AI practitioners.
- **[Tunguz posted a one-line jab at local AI enthusiasts](https://x.com/tunguz/status/2118051184779076026)** · composite 17.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Nothing here to act on.
- **[Venus-DefakerOne2 detects image and video forgeries with one forensics model](https://arxiv.org/abs/2610.37918)** · composite 16.91 · _flagged needs_review (low confidence / novelty / relevance)_
  It is a candidate forgery detector for fraud and identity teams, and has little bearing on agent or harness work.
- **[Bojan Tunguz jokes that people should walk more, like in Japan](https://x.com/tunguz/status/2121277109712601321)** · composite 16.8 · _flagged needs_review (low confidence / novelty / relevance)_
  This post is off-topic, and the X-list source needs a stronger relevance filter.
- **[Theo video on running Claude for weeks, transcript not captured](https://www.youtube.com/watch?v=NBCM_ZoWZo8)** · composite 15.5 · _failed independent verification — Verifier: the description is truncated, so 'gives no method' cannot be confirmed from the captured text._
  Nothing usable was captured. Watch the video or fetch its transcript before treating it as a source on long-running agents.
- **[X user shares a custom instruction said to curb Gemini sycophancy](https://x.com/realWeZZard/status/2124540611495911631)** · composite 15.0 · _flagged needs_review (low confidence / novelty / relevance)_
  An anecdote only: no prompt text or evaluation is captured, so it cannot be reused or trusted as evidence.
- **[Anthropic News Product index page lists 41 product announcements](https://www.anthropic.com/news/product)** · composite 14.94 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page with no analysis; the only signal is that Agent Skills is moving to a neutral foundation with broad cross-vendor adoption.
- **[Anthropic expands its GSA deal to discount Claude for governments](https://www.anthropic.com/news/expanding-partnership-gsa)** · composite 14.76 · _flagged needs_review (low confidence / novelty / relevance)_
  This procurement news only matters if you buy Claude for a US government organization.
- **[Post touts an AI pentest harness but links a Windows Bluetooth CVE](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-95996)** · composite 14.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat the harness claims as unverified: the saved source is only a Microsoft CVE page, so nothing here shows how the harness works or what it found.
- **[Anthropic's Security news page is an index of earlier posts](https://www.anthropic.com/news/security)** · composite 13.95 · _flagged needs_review (low confidence / novelty / relevance)_
  Nothing new here; read the linked posts on their own dates.
- **[Daniel Miessler lists his current software, models, cloud and hardware stack](https://danielmiessler.com/blog/current-stack)** · composite 13.62 · _flagged needs_review (low confidence / novelty / relevance)_
  A lifestyle/tool-list post with no analysis; useful only as a snapshot of one practitioner's setup.
- **[Riley Goodside mocks the claim that model collapse halted LLM progress](https://x.com/goodside/status/2115825541244760315)** · composite 13.55 · _failed independent verification — Verifier: the text carries no explicit sarcasm marker, so the 'mocks' reading of lesson 1 is inference from tone._
  A joke, not a finding, and it signals only that practitioners see model collapse as an overblown prediction so far.
- **[Amp releases an Android app for its coding agent](https://ampcode.com/news/amp-on-android)** · composite 13.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Amp users can now check agent threads and diffs from a phone, but there is nothing to learn about building agents.
- **[Anthropic's partnerships index lists business deals and holds no new security news](https://www.anthropic.com/news/partnerships)** · composite 13.32 · _flagged needs_review (low confidence / novelty / relevance)_
  A listing page of business announcements, with nothing for a security engineer or agent builder to act on.
- **[Anthropic's Policy news page is an index of policy announcements](https://www.anthropic.com/news/policy)** · composite 13.05 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat this as a pointer to follow individual posts, such as the independent-evaluator update, not as a finding.
- **[Anthropic's Models index shows Claude Haiku 5.5 as the newest release](https://www.anthropic.com/news/models)** · composite 12.31 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page picked up by the sitemap harvester; the releases it lists were covered when announced.
- **[Amp adds a hands-free car mode for talking to its Puck agent](https://ampcode.com/news/puck-in-the-car)** · composite 11.78 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Product announcement only; little transferable insight for security or agent practice.
- **[Anthropic's Features index lists three stories, newest from September](https://www.anthropic.com/news/features)** · composite 11.71 · _flagged needs_review (low confidence / novelty / relevance)_
  An index page picked up by the sitemap harvester; no finding.

---

<sub>Generated by scripts/generate_review.py on 2026-11-22. 262 item(s) awaiting review.</sub>
