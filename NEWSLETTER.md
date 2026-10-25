# 📰 Security & AI Research — Daily Snapshot (2026-10-25)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

17 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 63.34
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[METR: MathJax \href injection in the Inspect transcript viewer let an agent rewrite what reviewers see (found in ~10 minutes, patched in a day)](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/)** · _METR_ · composite 62.23
  Agent transcripts are attacker-controlled input, so the viewers, log pipelines and monitors that display them are security-critical and need the same output-encoding and tamper-resistance work as any other app that…
- **[UK AISI resumes most cyber evals after August incident: internet off, two independent egress blocks, blocking LLM monitor, pre-run control checks, flag-based escape tests](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)** · _UK AI Security Institute Blog_ · composite 59.5
  A concrete, reusable control set for anyone running agentic cyber evals: two independent egress layers, a blocking monitor, preflight checks, and flag-terminated escape tests run from weaker to stronger models.
- **[Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1)** · _NeurIPS (via arXiv)_ · composite 57.65
  A clean per-skill scan does not show that a set of installed skills is safe together, so review and monitoring have to cover the whole pipeline of skills.
- **[MFOTL (MonPoly) flags 71.8% of STAC, 70.1% of AgentDojo, fires on 29.3% of benign; one planted line beats provenance 94-99% of flagged runs](http://arxiv.org/abs/2610.09793v1)** · _CCS (via arXiv)_ · composite 56.65
  A declarative policy monitor is only as good as the trace it reads: log approvals, timestamps and provenance that the agent cannot forge, or temporal guardrails turn into coarse action-type blocklists.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Zenity AgentCorruption: one prompt made an AWS Bedrock AgentCore agent leak metadata credentials; its default role reached every agent in the region](https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model)**
  Treat an agent's HTTP tool as an SSRF primitive and give every agent its own least-privilege role; a shared default role turns one injected agent into a region-wide breach.
  _Why now: Disclosed and now-fixed AWS Bedrock AgentCore flaw: one prompt reached region-wide agent credentials; the per-agent least-privilege lesson applies to every cloud agent platform. · newsworthy · timely · high-relevance_
- **[Microsoft DevLabs DebugMCP 1.1.4 drive-by RCE: DNS rebinding hits unauthenticated, stateless localhost MCP server; start_debugging runs Windows UNC path from attacker's SMB share](https://www.imperva.com/blog/from-debugging-to-code-execution-rce-in-microsoft-devlabs-debugmcp/)**
  Any local MCP server with an execution tool is a drive-by RCE target unless it validates Host and Origin, requires authentication and a session, and rejects remote (UNC or URL) paths.
  _Why now: Microsoft DevLabs DebugMCP shows a stateless, unauthenticated localhost MCP server turning one DNS-rebinding request into drive-by RCE; a pattern every local agent-tool server must defend against. · trending · newsworthy · high-relevance_
- **[Datadog: a malicious webpage could get code execution through OpenCode's local /global/upgrade endpoint (GHSA-632h-h47v-g4x4, 1.14.30-1.18.21, fixed in 1.18.22)](https://securitylabs.datadoghq.com/articles/opencode-upgrade-remote-code-execution/)**
  Any local HTTP server that a coding agent exposes is reachable from every webpage the developer visits, so it needs authentication, strict Content-Type checks, and allowlisted inputs before anything…
  _Why now: Drive-by RCE in a popular coding agent's localhost server (GHSA-632h-h47v-g4x4); teaches that loopback binding is not a boundary for agent servers. · cve · trending · timely · high-relevance_
- **[LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise)**
  Treat AI gateways as Tier-1 infrastructure: change default keys, gate admin features, validate outbound URLs, and give them least-privilege cloud roles.
  _Why now: LiteLLM MCP auth bypass (CVE-2026-59822) is exploited in the wild and ~1 in 10 public gateways run default or no auth; concrete hardening steps for a widely deployed AI gateway. · cve · active-exploitation · high-relevance · timely_
- **[ProjectDiscovery backdoored Qwen2.5-7B with a cheap LoRA fine-tune; a trigger phrase made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned)**
  Clean benchmarks do not show whether downloaded open weights are backdoored, so contain what the agent's tool calls can read and reach.
  _Why now: Concrete end-to-end demo of a backdoored open-weight model driving Codex CLI to exfiltrate .env files; the lesson is to contain agent tool execution and egress, since clean benchmarks don't reveal the backdoor. · trending · high-relevance_

**📈 Emerging trends**

- **coding-agents** (🔺 rising) — 10 findings from 6 sources since 2026-08-06.
- **agent-monitoring** (🔺 rising) — 3 findings from 3 sources since 2026-10-06.
- **sandbox-escape** (🔺 rising) — 11 findings from 10 sources since 2026-07-15.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Atlassian CVE-2026-21589: pre-auth file read via '::' path traversal in atlassian-plugins-webresource (Jira, Confluence, Bitbucket and 5 more Data Center products), chained to Crowd admin](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)** · _watchTowr Labs_ · composite 64.09
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.
- **[Claude found 493 attack-surface issues in 25 projects; OpenSSH made ML-DSA parsing unreachable before auth](https://www.anthropic.com/research/attack-surface-reduction)** · _Anthropic Research_ · composite 63.97
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.
- **[watchTowr breaks PaperCut NG/MF patches three times: Tapestry `service` auth bypass (CVE-2026-81578, bypasses WT-2026-0142/0143) chained with RCE (CVE-2026-82078, WT-2026-0141, CVE-2026-82077 via Scan to Fax)](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)** · _watchTowr Labs_ · composite 60.79
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.
- **[PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](https://pwn.ai/blog/pwnescape)** · _source_ · composite 60.25
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 59.5
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.
- **[Citizen Lab: AdFection, zero-click Candiru spyware delivered through targeted ads bought via Discover-Tech](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)** · _source_ · composite 54.25
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Trail of Bits: only Go and vcpkg of 25 package managers verified every download from malicious repositories; only Go checked signatures by default](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)**
  A committed lockfile doesn't protect you from a compromised registry unless your package manager actually enforces its hashes; check yours and turn on the strict flag.
  _Why now: First cross-ecosystem test of package managers against a malicious registry; tells teams exactly which strict lockfile flags to turn on. · timely · high-relevance_
- **[Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads, PHP auto_prepend_file persistence, a sudo-alias password stealer and a Go RAT](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/)**
  AI-assisted intrusions still rely on ordinary Linux tradecraft, so defenders should hunt for PHP config tampering, shell rc file aliases and outbound reverse shells, and can treat conversational…
  _Why now: Live espionage campaign with LLM-written payloads and concrete Linux hunting leads (auto_prepend_file persistence, sudo-alias stealer). · newsworthy · trending · high-relevance_
- **[CISA KEV: exploited Fortinet CVE-2025-61624 path traversal lets read-write admins write or delete any file on FortiOS, FortiProxy, FortiPAM, FortiSwitchManager](https://nvd.nist.gov/vuln/detail/CVE-2025-61624)**
  Patch Fortinet appliances now, and treat any admin account with read-write rights on an unpatched box as a path to tampering with the device's own files.
  _Why now: Exploited in the wild per CISA KEV with a three-day deadline; Fortinet appliances are widely deployed and need patching now. · cve · active-exploitation · timely_
- **[tensorlake@0.5.144 npm worm (Mini Shai-Hulud): hijacked admin account committed payload via GitHub UI, ran trusted-publishing workflow; revoking stolen GitHub token wipes home directory](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud)**
  Provenance attestations and 'verified' commit badges prove where a build came from, not that the source is clean; and in this worm family, revoking the stolen GitHub token before removing…
  _Why now: Live npm worm (two independent write-ups, SafeDep and StepSecurity) that published through the project's own trusted-publishing workflow and arms a home-directory wiper on token revocation: a concrete lesson that valid provenance doesn't… · newsworthy · widely-reported · active-exploitation · timely · high-relevance_
- **[Citrix NetScaler ADC/Gateway pre-auth command injection (CVE-2026-88771): Perl script shells out logged input; zero-day in default configuration, fixed in 14.1-73.37 and 13.1-64.23](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/)**
  Patch NetScaler ADC and Gateway to 14.1-73.37 / 13.1-64.23 (or the FIPS/NDcPP equivalents) now, enable Enhanced ISN Generation, and hunt for compromise, because this root-level pre-auth bug was…
  _Why now: Pre-auth root command injection in NetScaler ADC/Gateway exploited as a zero-day in default configuration; concrete fixed builds, a sibling bug the upgrade alone doesn't fix, and log-hunting guidance. · cve · active-exploitation · timely · high-relevance_

**📈 Emerging trends**

- **rce** (🔺 rising) — 16 findings from 12 sources since 2026-06-29.
- **exploited-in-the-wild** (🔺 rising) — 10 findings from 3 sources since 2026-09-23.
- **credential-theft** (🔺 rising) — 6 findings from 4 sources since 2026-09-23.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 58.43
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 58.0
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964)** · _source_ · composite 55.0
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Letting the agent choose when to compact, guided by a fire/suppress rubric, matches or beats fixed-interval summarization at a fraction of the token cost](https://machinelearning.apple.com/research/self-compacting-language-agents)**
  Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.
  _Why now: Directly usable harness change: a model-invoked compaction tool plus a fire/suppress rubric beats fixed token-threshold compaction across seven models. · trending · high-relevance_

**📈 Emerging trends**

- **human-in-the-loop** (🔺 rising) — 3 findings from 3 sources since 2026-08-07.
- **long-running-agents** (🔺 rising) — 3 findings from 3 sources since 2026-07-22.
- **llm-as-judge** (🔺 rising) — 4 findings from 3 sources since 2026-08-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-25.</sub>
