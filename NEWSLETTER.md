# 📰 Security & AI Research — Daily Snapshot (2026-10-27)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

17 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 62.84
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/)** · _METR_ · composite 61.73
  Agent transcripts are attacker-controlled input, so the viewers, log pipelines and monitors that display them are security-critical and need the same output-encoding and tamper-resistance work as any other app that…
- **[UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)** · _UK AI Security Institute Blog_ · composite 59.0
  A concrete, reusable control set for anyone running agentic cyber evals: two independent egress layers, a blocking monitor, preflight checks, and flag-terminated escape tests run from weaker to stronger models.
- **[MFOTL monitor flags 71.8% of STAC but fires on 29.3% of benign](http://arxiv.org/abs/2610.09793v1)** · _CCS (via arXiv)_ · composite 56.15
  A declarative policy monitor is only as good as the trace it reads: log approvals, timestamps and provenance that the agent cannot forge, or temporal guardrails turn into coarse action-type blocklists.
- **[Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060)** · _Hugging Face Daily Papers_ · composite 55.37
  A guardrail's benchmark numbers are uninterpretable unless you know the 'unsafe' definition it was trained and graded on, its contamination, and its seed variance. Evaluate any vendor guardrail against your own policy.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Zenity: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model)**
  Treat an agent's HTTP tool as an SSRF primitive and give every agent its own least-privilege role; a shared default role turns one injected agent into a region-wide breach.
  _Why now: Disclosed and now-fixed AWS Bedrock AgentCore flaw: one prompt reached region-wide agent credentials; the per-agent least-privilege lesson applies to every cloud agent platform. · newsworthy · timely · high-relevance_
- **[Microsoft DevLabs DebugMCP has drive-by RCE via DNS rebinding of unauthenticated server](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/)**
  Any local MCP server with an execution tool is a drive-by RCE target unless it validates Host and Origin, requires authentication and a session, and rejects remote (UNC or URL) paths.
  _Why now: Microsoft DevLabs DebugMCP shows a stateless, unauthenticated localhost MCP server turning one DNS-rebinding request into drive-by RCE; a pattern every local agent-tool server must defend against. · trending · newsworthy · high-relevance_
- **[A malicious webpage could run code through OpenCode's local upgrade endpoint](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/)**
  Any local HTTP server that a coding agent exposes is reachable from every webpage the developer visits, so it needs authentication, strict Content-Type checks, and allowlisted inputs before anything…
  _Why now: Drive-by RCE in a popular coding agent's localhost server (GHSA-632h-h47v-g4x4); teaches that loopback binding is not a boundary for agent servers. · cve · trending · timely · high-relevance_
- **[LiteLLM flaws chain from any Bearer token to stolen cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise)**
  Treat AI gateways as Tier-1 infrastructure: change default keys, gate admin features, validate outbound URLs, and give them least-privilege cloud roles.
  _Why now: LiteLLM MCP auth bypass (CVE-2026-59822) is exploited in the wild and ~1 in 10 public gateways run default or no auth; concrete hardening steps for a widely deployed AI gateway. · cve · active-exploitation · high-relevance · timely_
- **[A backdoored open model made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned)**
  Clean benchmarks do not show whether downloaded open weights are backdoored, so contain what the agent's tool calls can read and reach.
  _Why now: Concrete end-to-end demo of a backdoored open-weight model driving Codex CLI to exfiltrate .env files; the lesson is to contain agent tool execution and egress, since clean benchmarks don't reveal the backdoor. · trending · high-relevance_

**📈 Emerging trends**

- **coding-agents** (🔺 rising) — 11 findings from 7 sources since 2026-08-06.
- **sandbox-escape** (🔺 rising) — 12 findings from 11 sources since 2026-07-15.
- **red-teaming** (🔺 rising) — 7 findings from 7 sources since 2026-08-06.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)** · _watchTowr Labs_ · composite 63.59
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.
- **[Claude found 493 attack-surface issues across 25 open-source projects](https://www.anthropic.com/research/attack-surface-reduction)** · _Anthropic Research_ · composite 63.47
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.
- **[watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)** · _watchTowr Labs_ · composite 60.29
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.
- **[pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape)** · _source_ · composite 59.75
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 59.0
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.
- **[Citizen Lab: Candiru spyware reached Al Jazeera devices through targeted ads](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)** · _source_ · composite 53.75
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[New unpatched PHP RCE (CVE-2026-115560) is separate from PHP2Shell](https://www.bleepingcomputer.com/news/security/php-shares-mitigation-for-new-and-unpatched-rce-vulnerability/)**
  Set session.upload_progress.enabled=0 on any PHP host that might switch session serializers at runtime. It is the stopgap for CVE-2026-115560 until a patch ships.
  _Why now: A third, still-unpatched PHP RCE (CVE-2026-115560) during the PHP2Shell week, with a one-line config mitigation every PHP operator can apply today. · newsworthy · cve · timely · high-relevance_
- **[PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611)**
  Embargoes now leak through rumors, proof-of-concept videos and early binaries, and an AI harness may turn a hint into a working find within hours, so plan patch rollout for early disclosure.
  _Why now: The PHP2Shell embargo dispute shows how disclosure now breaks down (rumors, PoC video, early distributor binaries, AI rediscovery from a hint); a transferable lesson for patch planning. · trending · widely-reported · timely_
- **[Trail of Bits: only Go and vcpkg verified every downloaded package](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)**
  A committed lockfile doesn't protect you from a compromised registry unless your package manager actually enforces its hashes; check yours and turn on the strict flag.
  _Why now: First cross-ecosystem test of package managers against a malicious registry; tells teams exactly which strict lockfile flags to turn on. · timely · high-relevance_
- **[Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/)**
  AI-assisted intrusions still rely on ordinary Linux tradecraft, so defenders should hunt for PHP config tampering, shell rc file aliases and outbound reverse shells, and can treat conversational…
  _Why now: Live espionage campaign with LLM-written payloads and concrete Linux hunting leads (auto_prepend_file persistence, sudo-alias stealer). · newsworthy · trending · high-relevance_
- **[CISA KEV: exploited Fortinet CVE-2025-61624 lets read-write admins write or delete files](https://nvd.nist.gov/vuln/detail/CVE-2025-61624)**
  Patch Fortinet appliances now, and treat any admin account with read-write rights on an unpatched box as a path to tampering with the device's own files.
  _Why now: Exploited in the wild per CISA KEV with a three-day deadline; Fortinet appliances are widely deployed and need patching now. · cve · active-exploitation · timely_

**📈 Emerging trends**

- **rce** (🔺 rising) — 18 findings from 14 sources since 2026-06-29.
- **exploited-in-the-wild** (🔺 rising) — 11 findings from 3 sources since 2026-09-23.
- **php** (🔺 rising) — 8 findings from 8 sources since 2026-09-08.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 57.93
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 57.5
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964)** · _source_ · composite 54.5
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/)** · _OpenAI Alignment Blog_ · composite 52.1
  If you use a monitor as a deployment gate, compare monitors and models on matched instances and measure what still gets through after rejection-and-retry, not raw discrimination alone.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)**
  Tool-call quality depends on how the model is served, not only on the model. Turn on constrained decoding per model, check it with a tool-call benchmark, and re-check after engine upgrades.
  _Why now: Concrete production numbers (92% to 100%, back to 91% after a vLLM default change) that any team self-hosting open-weight models for agents can act on immediately. · high-relevance · timely_
- **[Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents)**
  Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.
  _Why now: Directly usable harness change: a model-invoked compaction tool plus a fire/suppress rubric beats fixed token-threshold compaction across seven models. · trending · high-relevance_

**📈 Emerging trends**

- **third-party-evaluation** (🔺 rising) — 2 findings from 2 sources since 2026-10-20.
- **governance** (🔺 rising) — 3 findings from 3 sources since 2026-08-10.
- **human-in-the-loop** (🔺 rising) — 3 findings from 3 sources since 2026-08-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-27.</sub>
