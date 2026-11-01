# 🔍 Review Queue

> Everything held back from the site, with the reason. Findings that are **not yet vetted** (low confidence/novelty/relevance, or below the composite floor (20)), and news stories whose excerpt is not grounded in its source. Nothing here is deleted; promote a finding by raising its scores or clearing `needs_review`, or fix a news story's excerpt, then regenerate.

_Updated 2026-11-01._

## AI Security (45)

- **[OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident)** · composite 66.0 · _news story: excerpt not grounded in source (only 75% of quotes verified)_
  Treat a model eval with production classifiers off as a live agent that may try to escape, where a package-manager proxy is a plausible sandbox-escape primitive.
- **[Brazilian labor court fines lawyers for hidden prompt injection in a filing](https://jetstream.security/insights/brazilian-court-sanctions-prompt-injection-filing/)** · composite 60.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Hidden-text injection in documents from outside parties is now a sanctionable act in at least one court, and any pipeline that has AI read outside documents should check for…
- **[Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585)** · composite 59.35 · _news story: excerpt not grounded in source_
  The critical attack surface for agent apps is the framework layer around the model, where old bug classes get re-exposed as prompt-injected code paths — not the model's ability to…
- **["Black October" is an X label for a week of disclosures](https://forkast.news/black-october-is-a-disclosure-wave-the-label-hides-the-clock/)** · composite 54.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Read the label as a backlog of old defects being dated, not as one new attack; the AI angle is faster discovery and AI credentials as loot.
- **[Roo Code's command auto-approval can be bypassed in seven ways](https://www.vulncheck.com/advisories/roo-code-through-3.54.0-auto-approve-bypass-via-quote-masking-desynchronization)** · composite 54.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Allowlist-by-prefix approval for agent shell commands breaks whenever the checker and the shell parse differently; do not enable auto-approve on untrusted content.
- **[Guardrail benchmark scores mostly measure the training labels' definition of unsafe](http://arxiv.org/abs/2610.25060v1)** · composite 54.05 · _flagged needs_review (low confidence / novelty / relevance)_
  Before picking a guardrail classifier by benchmark score, ask which policy its labels encode, whether the benchmark leaked into training, and what the seed-to-seed variance is, or…
- **[Human reviewers miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)** · composite 53.95 · _news story: excerpt not grounded in source_
  Human-in-the-loop is a fatigue-limited primitive: engineer approvals as classifier + sandbox + hooks, not as a UX prompt.
- **[Vercel's $1M Firecracker sandbox-escape challenge drew 1,285 reports in two weeks](https://www.securityweek.com/1-million-sandbox-challenge-uncovers-linux-kernel-flaws)** · composite 53.75 · _flagged needs_review (low confidence / novelty / relevance)_
  In a microVM sandbox, the weak points are the shared host kernel and any control-plane input that comes from inside the guest, not the hypervisor itself.
- **[MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027)** · composite 53.1 · _news story: excerpt not grounded in source_
  MCP's enterprise turn adds iss validation and a stateless design that removes one session-poisoning surface but leans on standard load-balancer trust boundaries.
- **[Datadog: harvesters validate stolen AWS keys for Bedrock with tiny Converse calls](https://securitylabs.datadoghq.com/articles/beyond-valid-credentials-how-exposed-aws-keys-are-tested-for-amazon-bedrock-access/)** · composite 52.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Bedrock enumeration from a long-term key (multi-region ListFoundationModels, tiny Converse calls) is an early LLMjacking signal; alert on it and rotate the key before larger abuse.
- **[OpenAI's Hugging Face incident came down to skipped security basics](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/)** · composite 51.0 · _news story: excerpt not grounded in source_
  Rogue-agent incidents are foundational-security failures with known fixes: zero-trust boundaries, isolated eval hosts, egress control and active monitoring.
- **[Adan Alvarez tested which AWS attacks 14 LLMs propose with stolen keys](https://medium.com/@adan.alvarez/i-gave-14-llms-aws-keys-heres-what-they-wanted-to-do-next-48585761a11b)** · composite 50.75 · _failed independent verification — Medium returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the article._
  If LLM-driven attackers open with predictable AWS calls, those calls can become detections.
- **[Data-void exploits put attacker content in 31% of web-searching LLM answers](http://arxiv.org/abs/2610.30365v1)** · composite 49.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Web-search grounding is an input channel attackers can write to, especially on niche topics, so answers on such topics need signals about how thin or reliable the sources are.
- **[MLflow servers without authentication can be hijacked through third-party scorer loading](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)** · composite 49.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  If you run MLflow 3.12.0 or later, never expose it without authentication, and track the advisory for a fixed version.
- **[SCOPE compiles natural-language agent policies into predicate programs run by small models](https://arxiv.org/abs/2610.31062)** · composite 48.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent policy enforcement, prefer a compiled program of narrow predicates over one guardrail model or one LLM judge: cheaper, steadier and auditable (authors' claims, abstract…
- **[@a2ui/web_core openUrl opens agent-supplied URLs without a scheme check](https://github.com/advisories/GHSA-72qq-p3r5-f7wq)** · composite 47.75 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Treat UI that an agent generates as untrusted input: allowlist URL schemes (http/https) before any navigation or window.open call.
- **[Langflow before 1.10.3 runs commands placed in MCP config with no allowlist](https://github.com/advisories/GHSA-w794-rj3p-xv45)** · composite 47.75 · _ungrounded excerpt — only 0% of quotes verified against the source_
  In agent builders, an MCP stdio server entry is a shell command, so write access to MCP config is code execution on the host. Patch Langflow to 1.10.3 or later and limit who can…
- **[Agent Mosaic: LLM agents combine allowed documents into forbidden conclusions](https://arxiv.org/abs/2610.30418)** · composite 46.73 · _flagged needs_review (low confidence / novelty / relevance)_
  Document-level access control is not enough for agents serving users with mixed clearances, because the model can derive restricted conclusions from documents each user may read.
- **[Perplexity found no VM-to-host escape across 9 models, details not captured](https://www.perplexity.ai/hub/blog/escaping-space-part-i)** · composite 46.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Root inside a Firecracker microVM did not give these models a host escape, but the network-bypass results, which matter more in practice, were not captured.
- **[Red Hat finds Jev-style models not faster or more accurate than LLM-as-a-judge](https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails)** · composite 46.1 · _flagged needs_review (low confidence / novelty / relevance)_
  For prompt-injection screening, try a small trained classifier first and benchmark any LLM judge or decision model on your own data before paying for it.
- **[Edge grounding VLMs fall to wearable adversarial patches like detectors](http://arxiv.org/abs/2610.29196v1)** · composite 43.55 · _flagged needs_review (low confidence / novelty / relevance)_
  When red-teaming vision models in safety-critical systems, score where the box lands, not just whether one exists.
- **[LMCache multiprocess mode's unauthenticated ZeroMQ endpoint gives remote code execution](https://github.com/advisories/GHSA-w5f2-9q9c-ff4h)** · composite 42.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat every internal transport in an LLM serving stack as a network attack surface: if it unpickles socket data with no authentication, anyone who can reach the port can run code…
- **[Agno agent framework ran Python eval on a function call's field type](https://github.com/advisories/GHSA-m4w4-3r8h-jw98)** · composite 39.35 · _failed independent verification — Novelty disagreement: verifier rated 12 against my 35 (a routine eval-injection bug class, cf. LangChain CVE-2023-29374). It also noted the tool/model-output path is only an example and the advisory does offer a partial workaround._
  An agent framework that evals strings shaped by model output turns prompt injection into code execution, so upgrade Agno and search your agent code for eval on schema fields.
- **[Early-exit LLMs: shallow exits resist GCG-style adversarial suffixes better than deep exits](http://arxiv.org/abs/2610.15207v2)** · composite 39.05 · _flagged needs_review (low confidence / novelty / relevance)_
  If you serve an early-exit model, jailbreak robustness changes with the exit depth you pick, so test refusal behavior at each depth you deploy instead of assuming the full-depth…
- **[SkillMarker watermarks agent skill files to trace copying](https://arxiv.org/abs/2610.15725)** · composite 38.87 · _flagged needs_review (low confidence / novelty / relevance)_
  Skill publishers can now trace leaked or resold skills, but it is a provenance and ownership tool, not protection against malicious skills, and the abstract does not address…
- **[humanbound-firewall screens every input to an agent by who authored it](https://github.com/humanbound/humanbound-firewall)** · composite 38.57 · _flagged needs_review (low confidence / novelty / relevance)_
  The useful idea is to label every model input by author (request, outside content, own records); treat the tool as a preview filter, not a security boundary.
- **[NuGuard is an open-source AI-SBOM and red-team pipeline for agentic apps](https://github.com/NuGuardAI/nuguard)** · composite 37.14 · _flagged needs_review (low confidence / novelty / relevance)_
  It is a candidate all-in-one CI red-team harness for agent apps. It's young (67 stars), so treat the comparison claims as unverified marketing until you've benchmarked it against…
- **[openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers](https://github.com/harsha-iiiv/openapi-mcp-generator)** · composite 37.07 · _ungrounded excerpt — only 75% of quotes verified against the source_
  Auto-generated MCP servers expose your whole API to an agent by default, so filter operations and turn on inbound auth before you deploy one.
- **[OWASP GenAI Q3 2026 exploit roundup indexes eval-agent containment failures](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/)** · composite 36.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Use it as an index and a mitigation checklist for eval-agent containment failures, not as a source of new findings; its main point is that scope set only in the prompt is not a…
- **[AgentSafeEvo pits an RL attacker against a defender on adversarial agent tasks](https://arxiv.org/abs/2610.19422)** · composite 35.87 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a training-time hardening approach for agent model builders that does not replace runtime containment, and the abstract gives no figures to judge how large the gain is.
- **[mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6)** · composite 35.75 · _failed independent verification — Refuted: the saved source holds only generic CVSS definitions, so the SQL injection, version range and Databricks details are unsupported by it. Needs a re-fetch of the advisory._
  Agent memory content is attacker-influenced input, so memory backends must use parameterized queries like any other data layer.
- **[mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default](https://github.com/lanbaoshen/mcp-jenkins)** · composite 35.57 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat a Jenkins MCP server as code execution on your CI: give it a token without script rights, enable read-only mode, and keep it off the network.
- **[OpenGuardrails proposes one vendor-neutral wire protocol for agent guardrails](https://github.com/openguardrails/openguardrails)** · composite 34.67 · _flagged needs_review (low confidence / novelty / relevance)_
  A common guardrail interface could cut integration work, but its fail-open default means an attacker who can block the runtime turns the guardrail off.
- **[Praetorian's Augustus LLM scanner adds multi-turn attackers including Hydra](https://github.com/praetorian-inc/augustus)** · composite 34.25 · _flagged needs_review (low confidence / novelty / relevance)_
  If your LLM app keeps client-controlled chat history, test it with multi-turn and backtracking attacks, not just single-prompt jailbreak lists.
- **[Microsoft frames agents as insiders and announces Dynamic Permissions and Guardian Agents](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/)** · composite 33.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Graduated containment is a useful design pattern to copy: when agent risk rises, keep reads, revoke writes, require approval, then isolate. Treat the rest as vendor positioning.
- **[Chainguard hardens agent skills by scanning, signing and digest-pinning them](https://www.chainguard.dev/unchained/how-do-you-harden-an-agent-skill-the-simple-file-type-with-serious-complexities)** · composite 32.87 · _flagged needs_review (low confidence / novelty / relevance)_
  Manage agent skills like packages (scan, sign, pin, keep a private registry), but treat vendor 'hardening' claims as unmeasured until there are detection numbers.
- **[Tamga's prompt-injection rules caught 27 of 203 attacks written by others](https://github.com/yatuk/tamga)** · composite 31.84 · _failed independent verification — Lessons hold, but the verifier judged novelty 18 vs 45: the held-out collapse of phrase-matching injection filters is known (e.g. Hackett et al. 2025 on bypassing guardrail detectors); Tamga's two held-out sets are small and Turkish-only._
  Tamga's own numbers show a wording-based injection filter catching few attacks that someone else wrote, so test any such filter on independent attack sets.
- **[MCP ZAP Server blocks private-network targets and binds scan credentials server-side](https://github.com/dtkmn/mcp-zap-server)** · composite 30.17 · _flagged needs_review (low confidence / novelty / relevance)_
  If you expose a scanner or other outbound tool to agents, block internal destinations by default and keep credentials server-side behind opaque profile IDs, so the agent chooses…
- **[Microsoft tells CISOs to put agent identity and data controls first](https://www.microsoft.com/en-us/security/blog/2026/10/28/the-cisos-evolving-role-protecting-and-defending-in-the-agentic-era/)** · composite 29.09 · _flagged needs_review (low confidence / novelty / relevance)_
  Familiar guidance (inventory agents, give each one its own least-privilege identity, classify the data it can reach), and the 15-fold growth figure is the only new data point.
- **[NextDNS MCP server ships unauthenticated HTTP mode with DNS-rebinding protection off](https://github.com/dmeiser/nextdns-mcp)** · composite 28.77 · _flagged needs_review (low confidence / novelty / relevance)_
  Mostly a generic MCP wrapper. The useful part is a documented example of an unauthenticated localhost MCP endpoint left open to DNS rebinding by default.
- **[CollieAi's LLM Firewall filters prompts and responses through a hosted proxy](https://github.com/CollieAi/llm-firewall)** · composite 28.59 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a routine filtering proxy with no published detection rates, so treat it as one containment layer, not as a fix for prompt injection.
- **[Blogger argues teams should self-host an LLM proxy for per-key request logs](https://jrdsgl.com/if-you-dont-run-your-own-llm-proxy-how-the-fuck-do-you-even-know-whats-going-on/)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A self-hosted LLM gateway gives per-agent key isolation and an audit trail, but it also concentrates every provider key in one place and has to be hardened accordingly.
- **[Anthropic's Security news page is an index of security announcements](https://www.anthropic.com/news/security)** · composite 14.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Useful only as a pointer. The linked incident and threat-report posts carry the substance.
- **[MCP TypeScript SDK HTTP servers set no limit on request body size](https://github.com/advisories/GHSA-f897-62hf-6gxq)** · composite 10.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  MCP servers exposed over HTTP can be overloaded by oversized or batched requests until the SDK is updated.
- **[Check Point: infostealer adds collection routines for AI desktop apps](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/)** · composite 8.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  AI desktop apps and coding tools now sit next to browsers and wallets on infostealer target lists, so their tokens and data need the same protection.

## Product Security (50)

- **[@subql/common@5.8.3 npm package carried a backdoor that runs on install](https://www.stepsecurity.io/blog/subql-ecosystem-compromised)** · composite 52.62 · _flagged needs_review (low confidence / novelty / relevance)_
  A publish pipeline that builds from source and then fetches an external artifact is not building from source, and ignore-scripts does not help when the payload also fires on…
- **[X post claims Mirage2FA stole 4,561 Microsoft 365 session cookies](https://x.com/Dinosn/status/2116946099059511340)** · composite 51.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Adversary-in-the-middle proxies keep beating one-time-code multi-factor authentication; phishing-resistant sign-in is the fix, but this claim needs a primary source.
- **[VOLTA infostealer uses an LLM to rank victims' assets by value](https://blog.talosintelligence.com/appraisal-by-ai-model-driven-victim-prioritization-in-the-volta-infostealer/)** · composite 50.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Crimeware now uses LLMs as the analyst who decides which victims to work first, and is built to route around refusals.
- **[Datadog: 3,500+ RBAC bindings give dangerous permissions to groups like system:unauthenticated](https://securitylabs.datadoghq.com/articles/kubernetes-rbac-built-in-principals-dangerous-permissions/)** · composite 49.02 · _flagged needs_review (low confidence / novelty / relevance)_
  Audit for any RoleBinding or ClusterRoleBinding to system:anonymous, system:unauthenticated or system:authenticated beyond the defaults, especially on GKE and in…
- **[Kat Traxler used AI and security principles to find cloud design flaws](https://github.com/KatTraxler/presentations/tree/main/security-constitution)** · composite 47.75 · _failed independent verification — Source page returned HTTP 403 to fetch_raw twice; only the tl;dr sec blurb was read, so no lesson could be checked against the talk itself._
  Pointing an AI at design principles, not bug classes, may surface design flaws that pattern-based hunting misses.
- **[Next.js has unauthenticated RCE in use cache functions returning typed arrays](https://github.com/advisories/GHSA-673q-mjm6-r5xr)** · composite 47.75 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Upgrade Next.js now if any `use cache` function returns typed arrays; there is no workaround.
- **[Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths for defenders](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/)** · composite 46.85 · _flagged needs_review (low confidence / novelty / relevance)_
  Run pathrunner in a sandbox (Pathfinding Labs) and use its CloudTrail report to test that every payload, not just one, trips a detection.
- **[UAT-11985 lured Taiwan researchers with likely AI-templated invitations and live MFA relay](https://blog.talosintelligence.com/uat-11985/)** · composite 46.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Real-time relay kits defeat OTP and push MFA; only origin-bound factors (passkeys, security keys) stop this class, and lure quality is no longer a usable tell.
- **[Next.js Image Optimization has unauthenticated RCE via SVG through sharp](https://github.com/advisories/GHSA-2464-fhr4-w9xw)** · composite 46.25 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Pin a patched sharp under Next.js and consider disabling SVG optimization; image pipelines are unauthenticated RCE surface.
- **[Google declines to fix zero-click SMS that crashes Android telephony](https://smsofdeath.com/)** · composite 45.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Any Android device reachable by SMS can be knocked off telephony, emergency calling included, and the vendor treats it as a non-security bug with no fix scheduled.
- **[Hijacked coding assistant recommended a PyPI package that stole GitHub tokens](https://safedep.io/ai-coding-assistant-hijack-shai-hulud)** · composite 43.07 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat any package your coding assistant suggests as untrusted input. Check it against an allowlist and hashes in CI, and keep long-lived GitHub tokens and AI tool config secrets…
- **[A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/)** · composite 42.47 · _news story: excerpt not grounded in source_
  Enclave-to-KMS attestation only closes the gap if you also hardcode the CMK ARN, attest the IAM role, and initiate TLS from inside the enclave; without that, active-attacker…
- **[A probability-scoring model matches employee accounts to one person at 0.95 F1](https://vincenzoiozzo.com/blog/jev-identity-resolution)** · composite 41.75 · _flagged needs_review (low confidence / novelty / relevance)_
  In identity governance (IGA) and identity-security products, a cheap probability model with a tuned cut-off, plus a frontier-model check only on the 'maybe' band, beats rules and…
- **[VibeRaven statically checks AI-built Supabase apps for row-level security gaps](https://github.com/ohad6k/VibeRaven)** · composite 41.51 · _failed independent verification — Verifier rated novelty 12 vs 45: the RLS, service_role and dashboard-blind-spot points are standard Supabase docs and Security Advisor lints; only the vendor's 512-repo statistic is new, and the push-to-main point is an unsupported README assertion._
  For AI-built Supabase apps, the common gaps are database authorization mistakes such as missing row-level security (RLS), anon-callable definer functions and leaked service_role…
- **[Snyk: SAST cannot see missing ownership checks in agent-written endpoints](https://snyk.io/blog/ai-coding-agents-broken-access-control/)** · composite 41.44 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent-written endpoints need an explicit ownership question in review and a cross-tenant test per resource, because neither the agent nor SAST knows your tenancy rules.
- **[A client's 1-bit reply leaks the full CKKS secret key](http://arxiv.org/abs/2610.21127v1)** · composite 40.55 · _flagged needs_review (low confidence / novelty / relevance)_
  If you deploy homomorphic encryption with an untrusted server, any client behaviour the server can observe on decryption, such as errors, retries or a 1-bit validity signal, is a…
- **[CVM-Store paper protects confidential VM storage at near-raw disk speed](http://arxiv.org/abs/2610.34560v1)** · composite 40.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Running in a confidential VM does not protect data on disk; stored data needs its own integrity and rollback protection.
- **[America bans imported robots due to supply chain and security risks](https://www.theregister.com/security/2026/07/29/america-bans-imported-robots-due-to-supply-chain-and-security-risks/5280145)** · composite 40.5 · _news story: excerpt not grounded in source_
  US regulators are treating networked physical robots as a critical-infrastructure supply-chain risk category on par with telecom gear.
- **[Northstar Security leaves stealth with $7M to find risky issue combinations](https://www.securityweek.com/northstar-security-exits-stealth-with-7m-to-expose-toxic-risk-combinations/)** · composite 40.32 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding announcement: the idea of scoring combined exposures, not single findings, is established, and the source has no results to judge.
- **[Chainguard Athena agents deduplicate private zero-day reports without leaking reporters](https://www.chainguard.dev/unchained/this-shit-is-hard-building-a-vulnerability-database-from-private-reports)** · composite 40.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Version ranges, duplicate decisions and fixed-version claims in a vulnerability database are each judgments that can be wrong; keep agents advisory and let deterministic…
- **[Wiz scans every new npm version at publish time to catch compromises](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication)** · composite 38.6 · _flagged needs_review (low confidence / novelty / relevance)_
  CVE-based dependency scanning is blind to hijacked trusted packages; you need publish-time behavioral analysis or a cooldown before new versions reach builds.
- **[VibeRaven checks AI-built Supabase apps for missing row-level security](https://github.com/ohad6k/VibeRaven)** · composite 37.61 · _flagged needs_review (low confidence / novelty / relevance)_
  Vibe-coded Supabase apps fail in a handful of predictable ways, and a static check in CI can catch several of them before launch.
- **[raml-kql runs one KQL query across workspaces without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql)** · composite 37.25 · _flagged needs_review (low confidence / novelty / relevance)_
  MSSPs without a Defender MTO can hunt across customer Sentinel workspaces from one query with delegated access only.
- **[Plex CVE-2026-96652 SSRF lets the /player/timeline protocol parameter force server POSTs](https://nvd.nist.gov/vuln/detail/CVE-2026-96652)** · composite 37.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Upgrade Plex to 1.43.3.10861 or later: this endpoint turns the server into a POST relay with almost no authentication, and it is exploited in the wild as part of the plex2shell…
- **[Cisco ASA and FTD VPN crash bug is exploited, CISA gives three days](https://nvd.nist.gov/vuln/detail/CVE-2026-76418)** · composite 37.1 · _flagged needs_review (low confidence / novelty / relevance)_
  If your ASA or FTD VPN uses secondary authentication on a tunnel group, patch now, because attackers are already using this to knock VPNs offline.
- **[Exploited VMware ESX flaw lets attacker with admin rights act unlogged](https://nvd.nist.gov/vuln/detail/CVE-2026-41709)** · composite 37.1 · _flagged needs_review (low confidence / novelty / relevance)_
  ESX audit logs may be silent about what a hijacked admin did, so do not treat clean ESX logs as proof of no tampering.
- **[CISA KEV: Plex Media Server file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656)** · composite 36.12 · _failed independent verification — Source text not captured (NVD page empty); lessons rest on the KEV catalog text only._
  Treat the four Plex KEV CVEs as one chain and patch together.
- **[CISA says a low-severity VMware ESX logging gap is being exploited](https://nvd.nist.gov/vuln/detail/CVE-2026-41709)** · composite 35.75 · _ungrounded excerpt — only 67% of quotes verified against the source_
  Do not deprioritize low-CVSS ESX logging bugs: attackers who already hold admin access use them to hide what they do.
- **[Chainguard rebuilds every buildable Linux distribution font from source](https://www.chainguard.dev/unchained/this-shit-is-hard-nobody-has-ever-been-pwned-by-helvetica-or-have-they)** · composite 35.64 · _flagged needs_review (low confidence / novelty / relevance)_
  Container images and distributions ship prebuilt fonts that rendering libraries execute, so treat them as unverified binaries in the supply chain. The concrete payoff of building…
- **[Socket finds 319 Chrome extensions that hijacked searches through operator servers](https://www.malwarebytes.com/blog/news/2026/10/fake-pdf-and-search-tools-hijacked-searches-for-13-4-million-chrome-users)** · composite 35.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat an official-store listing as no trust signal for browser extensions, because unlisted, ad-promoted extensions can quietly proxy every search a user makes.
- **[Cisco Talos says lab-agent attacks are loud now but will get quieter](https://blog.talosintelligence.com/one-breach-please-and-make-no-mistakes/)** · composite 33.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Today's agent attacks are easy to see at the front door, so instrument for that now and assume the noise will drop.
- **[CiliumHound graphs Cilium Kubernetes network policies as a BloodHound OpenGraph extension](https://specterops.io/blog/2026/09/17/ciliumhound-graphing-kubernetes-network-policies)** · composite 31.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  If you run Cilium, a graph view of network policies may help find unintended reachability, but the source text here is too thin to judge the tool.
- **[PHP2Shell hits every PHP since 5.4, no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run PHP 8.1 or older, there is no patch: upgrade to 8.2+ or put network-level protection in front now.
- **[Researcher reports Samsung Tizen runs AlexNet on screen captures to identify games](https://twitter.com/mike64_t/status/2114150399406202896)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  When auditing TV/IoT firmware, check whether on-device ML screen capture runs before user consent, even if the output is dropped; here the evidence is a single unverified tweet.
- **[CISA KEV: SiteGuard Server Edition OS command injection exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931)** · composite 29.0 · _failed independent verification — Fetched NVD page was empty; the only lesson rests on the KEV catalog description and cannot be grounded in the saved source._
  If you run SiteGuard Server Edition, patch now: CISA lists this command injection as actively exploited.
- **[CISA KEV: Zammad local privilege escalation to root exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-102490)** · composite 28.66 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Patch Zammad for both CVE-2026-102489 and CVE-2026-102490 and check helpdesk hosts for signs of root compromise.
- **[CISA adds a 2021 ONLYOFFICE Docs path traversal bug to KEV](https://nvd.nist.gov/vuln/detail/CVE-2021-3199)** · composite 28.56 · _flagged needs_review (low confidence / novelty / relevance)_
  A five-year-old ONLYOFFICE bug with public PoCs is now confirmed exploited; any unpatched self-hosted Document Server should be patched or pulled offline now.
- **[Microsoft's October 2026 Patch Tuesday fixes one exploited Windows Shell bypass](https://blog.talosintelligence.com/microsoft-patch-tuesday-for-october-2026/)** · composite 28.19 · _flagged needs_review (low confidence / novelty / relevance)_
  Patch the exploited Windows Shell bypass and the AD DS and Exchange RCEs first, since the rest is a long routine list.
- **[Unit 42: threat actors use Web3 infrastructure to breach cloud environments](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks/)** · composite 27.66 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Read the original before acting; as captured, this item only signals that a major vendor is tracking the blockchain-C2 plus package-compromise pattern.
- **[Check Point digest: PHP2Shell attempts reportedly rose from thousands to millions](https://research.checkpoint.com/2026/26th-october-threat-intelligence-report/)** · composite 27.27 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated 'unpatched' (the source says 'did not indicate patched versions') and 'millions' (a reported figure). Text corrected; a secondary digest of already-covered stories._
  A news digest with nothing new, so use it as a checklist: PHP2Shell, LiteLLM 1.107.0, GitLab CVE-2026-110264, VeloCloud CVE-2026-114625, and AI-tool token theft.
- **[MagicSword markets automatic application-control policies built from LOLDrivers research](https://www.magicsword.io/application-control)** · composite 26.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Marketing for a product; the useful idea is blocking known-abused legitimate tools by default, which the free LOL catalogs already support.
- **[CISA adds a 2016 Apache Struts DMI command injection bug to KEV](https://nvd.nist.gov/vuln/detail/CVE-2016-3081)** · composite 26.16 · _flagged needs_review (low confidence / novelty / relevance)_
  Legacy Struts 2 apps with DMI on are still being hit a decade later; find them and patch or turn DMI off.
- **[Public bounty server runs pre-PHP2Shell PHP guarding a bitcoin key](https://stealmybitcoin.com/)** · composite 26.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a public, live test of PHP2Shell exploitability; a non-zero hack counter would be a signal to speed up PHP patching, but the page itself contains no technical detail.
- **[GoSQLX, a Go SQL parser, ships an injection scanner and MCP server](https://github.com/ajitpratap0/GoSQLX)** · composite 25.01 · _flagged needs_review (low confidence / novelty / relevance)_
  A handy SQL parser with an agent interface, but nothing new for security; its injection scanner is unmeasured.
- **[Semgrep argues containment and recovery matter as much as prevention](https://semgrep.dev/blog/2026/cybersecurity-readiness-after-compromise)** · composite 24.75 · _flagged needs_review (low confidence / novelty / relevance)_
  General incident-readiness advice that works as a checklist, with nothing new.
- **[Akto README pitches open-source API security testing with a new AI-agent tagline](https://github.com/akto-api-security/akto)** · composite 23.09 · _failed independent verification — Verifier: excerpts verbatim, but the draft overstated features (CI/CD and mirrored traffic partly Enterprise-only; SSRF and JWT tests only named as examples) and inferred JVM code execution. Text corrected; a vendor README with marketing tagline._
  A known open-source API-testing tool with an AI-security tagline, but its README shows no AI- or MCP-specific capability, so judge it as an API testing tool.
- **[Aikido claims an 'http2shell' RCE in Node and Python; no details captured](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8)** · composite 23.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A possible cross-runtime RCE is circulating, but this capture has no details; get the primary Aikido or vendor advisory before acting.
- **[Book claims Dutch government hacked Jared Kushner's phone, which Kushner denies](https://twitter.com/jaredkushner/status/2113376217415958767)** · composite 18.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a disputed political allegation with no technical content; treat it as unconfirmed news, not threat intelligence.
- **[CISA KEV: Plex Media Server SSRF exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96655)** · composite 11.94 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Any logged-in Plex user can make the server fetch arbitrary addresses, and attackers are chaining it with other Plex bugs.
- **[CISA KEV: Siemens Software Center DLL search-path flaw exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-110936)** · composite 10.44 · _ungrounded excerpt — only 0% of quotes verified against the source_
  A local attacker who can drop a DLL where Siemens Software Center looks for one gets code execution; CISA says this is being exploited.

## AI Research (52)

- **[How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/)** · composite 59.62 · _news story: excerpt not grounded in source (only 0% of quotes verified)_
  In AI bug hunting, outcome definition and per-agent scoping drive output quality most, with a threat-model file as the highest-leverage input.
- **[GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227)** · composite 48.77 · _flagged needs_review (low confidence / novelty / relevance)_
  If your harness edits skills automatically, assign credit by comparing repeated runs (group-relative), not by co-occurrence with success, or harmful skills will survive.
- **[DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522)** · composite 48.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate routers and guardrail judges on paired contrast cases, not only item accuracy.
- **[Anthropic study finds analysts follow an agent's hidden lean on judgment calls](https://www.anthropic.com/research/agents-judgment-calls)** · composite 47.78 · _flagged needs_review (low confidence / novelty / relevance)_
  If your harness relies on a human to make or check judgment calls, the agent's framing will often make the call instead, so design for that.
- **[Anthropic embeds METR with employee-like access but controls what is redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators)** · composite 47.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded third-party evaluation is now a concrete arrangement at one frontier lab; when you weigh its outputs, look at the redaction terms.
- **[Anthropic physicist's BootLoops: Claude agents did checkable science with expert steering](https://www.anthropic.com/research/claude-shaped-science)** · composite 43.37 · _flagged needs_review (low confidence / novelty / relevance)_
  Agents do best on problems where a known technique applies and the answer can be checked, inside a harness that keeps growing; plan for a domain expert to judge whether the…
- **[Google ships Gemini 4 Carbon to trusted cyber defenders first](https://latent.space/p/ainews-gemini-4-carbon/)** · composite 42.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A strong new model for vulnerability work, but its cyber scores come from Google and its hallucination rate went up, so validate it on your own triage tasks before you trust its…
- **[METR proposes third-party review of unreleased models by mining internal transcripts](https://metr.org/blog/2026-10-14-alignment-assessment-proposal/)** · composite 42.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Evidence of misalignment is only as good as the logs and detection methods behind it, and agents can tamper with logs while training against detectors can teach models to evade…
- **[Microsoft evaluates Copilot on fully synthetic, time-evolving enterprise tenants](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/)** · composite 42.5 · _flagged needs_review (low confidence / novelty / relevance)_
  For assistants that work over private workspace data, a reproducible synthetic world with a timeline lets you regression-test without touching customer data.
- **[MLX tensor parallelism over Thunderbolt serves a mixture-of-experts model on Mac Studios](https://machinelearning.apple.com/research/mlx-distributed-inference)** · composite 41.0 · _flagged needs_review (low confidence / novelty / relevance)_
  A small Mac cluster can now serve a near-trillion-parameter open model to a local coding agent at usable speed, but tensor parallelism helps decode far more than pipeline…
- **[Arca's wealth agents run ten-day tasks while human advisors move money](https://latent.space/p/arca/)** · composite 37.97 · _flagged needs_review (low confidence / novelty / relevance)_
  For long, stop-start agent work in a regulated field, keep state in a shared memory and put every risky action behind deterministic rules, not model judgment.
- **[Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/)** · composite 36.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Large subagent workflows can finish big, test-backed builds without supervision, so the bottleneck moves to human review; plan for verification artifacts such as conformance…
- **[SpecForge compiles team rules into checks that agents cannot skip](https://github.com/leaderiop/SpecForge)** · composite 36.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Move the rules an agent must obey out of the prompt and into a deterministic check that fails, the same way tests gate code.
- **[Google's VERID checks agent-written lab-robot protocols against a 3D digital twin](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/)** · composite 36.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Agent actions on the physical world need validation against live state, not just syntax, and agents optimizing a proxy metric will exploit artifacts until real-world readouts…
- **[Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access](https://www.anthropic.com/news/accenture-embedded-evaluation)** · composite 36.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded evaluation is starting with a lab-funded commercial partner and no shared standards, so judge its independence by the access and reporting terms once they are published.
- **[SWT-Bench is a Docker harness that scores LLM-written tests reproducing GitHub issues](https://github.com/logic-star-ai/swt-bench)** · composite 35.87 · _failed independent verification — Verifier: excerpts verbatim and dataset sizes correct, but the draft over-reached (author attribution, regression-catching inference, filler lesson). Text corrected; held as an old 2024 benchmark README with low novelty._
  If your coding agent claims it reproduced a bug, require a test that fails before the fix and passes after. SWT-Bench is a ready-made harness for measuring how often it can.
- **[HackerBooks lists 16,543 books mentioned in Hacker News comments](https://hackerbooks.org)** · composite 34.65 · _flagged needs_review (low confidence / novelty / relevance)_
  Off-topic for security and agent builders: a book directory with no technique to learn from.
- **[Workshop paper proposes retrieval as local traversal through a memory address space](http://arxiv.org/abs/2610.40545v1)** · composite 34.55 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an early architecture hypothesis that stateful retrieval is easier to learn than stateless retrieval, not something harness builders can use yet.
- **[A Thomson Reuters engineer runs a coding agent fully offline with Qwen](https://latent.space/p/offline-coding/)** · composite 34.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A 9B local model with OpenCode can handle small, test-backed fixes offline, but the source shows only one trivial task.
- **[SAFT adversarially trains only robustness-critical parameters and beats LoRA](http://arxiv.org/abs/2610.39455v1)** · composite 33.05 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a model-training result for classic adversarial robustness and has little direct use for agent or harness builders.
- **[Amazon Science covers third-party review of AI safety testing, body not captured](https://www.amazon.science/blog/strengthening-ai-safety-evaluation-through-independent-third-party-review)** · composite 32.0 · _failed independent verification — Verifier refuted lessons 1-2: the raw capture is navigation only, so nothing beyond the headline is supported; 'AVERI' comes from the feed excerpt, not the page. Needs a re-fetch of the article body._
  Only the headline can be verified: a frontier lab used an outside party to audit its safety-eval process. Re-fetch the article before taking any lessons from it.
- **[Daniel Miessler argues harnesses should describe what you want, not steps](https://danielmiessler.com/blog/models-how-harnesses-what)** · composite 32.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Spend harness effort on user context and definitions of done rather than step-by-step scripts, as a heuristic, not a measured result.
- **[Workshop paper proposes retrieval as a local walk through memory](http://arxiv.org/abs/2610.40545v1)** · composite 31.55 · _flagged needs_review (low confidence / novelty / relevance)_
  An interesting idea for stateful agent memory, but a single toy experiment gives a harness builder nothing to use yet.
- **[Survey maps how self-improving AI systems can fake gains or lose safeguards](https://arxiv.org/abs/2610.35193)** · composite 31.34 · _flagged needs_review (low confidence / novelty / relevance)_
  If your agent rewrites its own prompts, memory or tools, re-verify after each change against a held-out evaluation it cannot edit.
- **[Titus Winters says AI raised code output and outages, not features shipped](https://newsletter.pragmaticengineer.com/p/software-engineering-at-google-and)** · composite 31.1 · _flagged needs_review (low confidence / novelty / relevance)_
  Judge AI-assisted engineering by outages and delivered features, not code volume, and wrap large AI rewrites in the coexist, shard and block-the-old discipline Google used before…
- **[HybridAgent reasons in latent space and calls tools in text](https://arxiv.org/abs/2610.18861)** · composite 30.5 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a model architecture and training change, not a harness technique, so it only matters if you train or serve your own open-weight agent models.
- **[Daniel Miessler frames AI work as hill-climbing against ideal-state evals](https://danielmiessler.com/blog/general-hill-climbing)** · composite 30.12 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat the written ideal state as the source of your verification criteria, and update the evals whenever passing output still feels wrong.
- **[Simon Willison's Claude-run review finds webframe fast but rough for scraping](https://simonwillison.net/2026/Oct/26/webframe-evaluation/)** · composite 30.05 · _flagged needs_review (low confidence / novelty / relevance)_
  webframe is a lightweight way to run page JavaScript from scripts, but do not treat it as a sandbox without your own isolation.
- **[Sparse Adversarial Fine-Tuning (SAFT) updates only about 5% of a network's parameters](http://arxiv.org/abs/2610.39455v1)** · composite 30.05 · _flagged needs_review (low confidence / novelty / relevance)_
  A useful efficiency result for adversarial robustness research, with no direct bearing on securing LLM agents.
- **[Practitioners say public AI security benchmarks only shortlist models for real work](https://www.darkreading.com/cybersecurity-analytics/benchmarking-security-of-ai-models-poses-challenges)** · composite 28.85 · _failed independent verification — Verifier refuted 'interviewees agree public rankings only shortlist candidates' (one Sonar quote) and 'harness matters as much as the model' (Dream's view alone); Sonar's leaderboard measures quality and security, not secure generation only._
  Choose models for security work with your own task evaluations and a defined failure budget; leaderboards are only a shortlist.
- **[Bound-conditioned latent inference cuts progressive image codec BD-rate on Kodak](http://arxiv.org/abs/2610.30966v1)** · composite 28.55 · _flagged needs_review (low confidence / novelty / relevance)_
  A solid image-compression result, but it has no bearing on securing or building AI agents and harnesses.
- **[PRISM benchmark shows pathology model calibration breaks down with scarce labels](http://arxiv.org/abs/2610.36517v1)** · composite 28.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Medical ML result, off-thesis here: the general point is not to treat an accuracy leaderboard as a stand-in for calibration under low labels or domain shift.
- **[Moonshot's Kimi K3.1 Pro nears frontier scores, with open weights promised](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/)** · composite 28.49 · _flagged needs_review (low confidence / novelty / relevance)_
  A near-frontier open-weight option at half Opus pricing is worth benchmarking on your own agent tasks once the weights ship.
- **[Hacker News developers describe fatigue from AI-era coding and agent review](https://news.ycombinator.com/item?id=50301479)** · composite 27.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Human review capacity, not agent output, is now the bottleneck, so harnesses should cut what humans must read and prove that tests actually test something.
- **[RoboCasa-Shift shows equal success-rate drops in a VLA policy hide different failures](https://arxiv.org/abs/2610.27861)** · composite 27.23 · _flagged needs_review (low confidence / novelty / relevance)_
  Aggregate success rate can hide outcome flips and which task stage fails; the study covers one robot policy on four simulated tasks.
- **[Anthropic donates the Agent Skills standard to the Agentic AI Foundation](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)** · composite 26.98 · _flagged needs_review (low confidence / novelty / relevance)_
  Governance news only: Agent Skills is now a Linux Foundation-hosted standard like MCP, and nothing changes technically today.
- **[Anthropic reports early results from Claude-driven drug development partnerships](https://www.anthropic.com/research/early-progress-drug-development)** · composite 26.64 · _flagged needs_review (low confidence / novelty / relevance)_
  The reusable idea in this off-field vendor report is to check agent review against known human findings before relying on it.
- **[Sebastian Raschka releases a from-scratch video course on building reasoning models](https://magazine.sebastianraschka.com/p/building-reasoning-models)** · composite 25.4 · _flagged needs_review (low confidence / novelty / relevance)_
  A hands-on resource for understanding the reasoning model inside agents; teaching material, not a new finding.
- **[alphaXiv says its 4B decision model nearly matches Jev except sarcasm](https://x.com/askalphaxiv/status/2116199951835582507)** · composite 25.25 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an unverified vendor claim, and small decision models still have to be benchmarked on your own data, as earlier pool entries showed.
- **[pi pod runs the pi coding agent in isolated sandboxes](https://pipod.dev/)** · composite 24.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Another self-hosted option for sandboxing coding agents, but the page gives no isolation details, so treat it as a lead to evaluate, not a proven security control.
- **[Framework-free Colab notebooks teach the applied LLM engineering stack](https://github.com/calmrocks/ai-engineer-notebooks)** · composite 22.84 · _flagged needs_review (low confidence / novelty / relevance)_
  A reasonable onboarding course for engineers new to LLM apps; no new technique.
- **[Anthropic expands AI for Science credits to 20 foundations and institutions](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions)** · composite 21.88 · _flagged needs_review (low confidence / novelty / relevance)_
  A funding and partnership announcement with nothing to change in a harness, apart from noting the Model Hardware Standard for agents that drive physical instruments.
- **[Anthropic staff, unlike most US adults, expect Nobel-level AI discovery by 2030](https://www.anthropic.com/research/ai-expectations-gap)** · composite 20.15 · _flagged needs_review (low confidence / novelty / relevance)_
  This is an economics and public-opinion survey with little practical value for builders, though its one practical data point is that regular AI users at work rank data privacy and…
- **[Theo video on running Claude for weeks, transcript not captured](https://www.youtube.com/watch?v=NBCM_ZoWZo8)** · composite 18.5 · _failed independent verification — Verifier: the description is truncated, so 'gives no method' cannot be confirmed from the captured text._
  Nothing usable was captured. Watch the video or fetch its transcript before treating it as a source on long-running agents.
- **[Anthropic expands its GSA deal to discount Claude for governments](https://www.anthropic.com/news/expanding-partnership-gsa)** · composite 17.76 · _flagged needs_review (low confidence / novelty / relevance)_
  This procurement news only matters if you buy Claude for a US government organization.
- **[Riley Goodside mocks the claim that model collapse halted LLM progress](https://x.com/goodside/status/2115825541244760315)** · composite 16.55 · _failed independent verification — Verifier: the text carries no explicit sarcasm marker, so the 'mocks' reading of lesson 1 is inference from tone._
  A joke, not a finding, and it signals only that practitioners see model collapse as an overblown prediction so far.
- **[Amp releases an Android app for its coding agent](https://ampcode.com/news/amp-on-android)** · composite 16.4 · _flagged needs_review (low confidence / novelty / relevance)_
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

<sub>Generated by scripts/generate_review.py on 2026-11-01. 147 item(s) awaiting review.</sub>
