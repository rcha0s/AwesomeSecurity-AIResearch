# 📰 Security & AI Research — Daily Snapshot (2026-10-25)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

11 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 63.59
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[Skill cascading attacks: a harmful goal split across several benign-looking agent skills evades per-skill scanners and runtime monitors](http://arxiv.org/abs/2609.30383v1)** · _NeurIPS (via arXiv)_ · composite 57.65
  A clean per-skill scan does not show that a set of installed skills is safe together, so review and monitoring have to cover the whole pipeline of skills.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

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
- **[obsidian-tc tool server: any valid token could read, write, or delete any configured vault (CVE-2026-77366)](https://github.com/advisories/GHSA-84c9-qqpq-2pq5)**
  Multi-tenant tool servers must enforce the caller's tenant once at dispatch and never trust a caller-supplied vault or workspace parameter.
  _Why now: Critical GHSA in an agent tool server: missing tenant binding let any token reach every vault; the central dispatch-check fix is a transferable pattern for MCP-style servers. · cve · high-relevance_

**📈 Emerging trends**

- **coding-agents** (🔺 rising) — 10 findings from 6 sources since 2026-08-06.
- **multi-turn** (🔺 rising) — 2 findings from 2 sources since 2026-09-29.
- **windows** (🔺 rising) — 2 findings from 2 sources since 2026-10-13.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Claude found 493 attack-surface issues in 25 projects; OpenSSH made ML-DSA parsing unreachable before auth](https://www.anthropic.com/research/attack-surface-reduction)** · _Anthropic Research_ · composite 64.22
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.
- **[PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](https://pwn.ai/blog/pwnescape)** · _source_ · composite 60.5
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 59.75
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.
- **[Citizen Lab: AdFection, zero-click Candiru spyware delivered through targeted ads bought via Discover-Tech](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)** · _source_ · composite 53.0
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.
- **[333 Tor exit relays hijacked with the Ebury backdoor to intercept SSH passwords and unencrypted mail](https://kaba.cx/posts/20261020_Tor/)** · _source_ · composite 49.25
  Never accept a changed SSH host key over Tor or any untrusted path; use key auth, and expect backdoored infrastructure hosts to be turned into traffic interceptors.
- **[SourceHut account takeover via OSC 8 hyperlink XSS in ansi2html-rendered build logs (CVE-2026-92973; ansi2html >=1.7.0,<1.9.4, builds.sr.ht >=0.40.0,<0.105.1)](https://blog.arusekk.pl/posts/srht-account-takeover/)** · _@arusekk via Hacker News_ · composite 47.0
  Treat CI log output as untrusted HTML input: sanitize the output of any ANSI-to-HTML converter and back it with a strict Content-Security-Policy, because one injected escape sequence can become wormable account takeover.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Citrix NetScaler ADC/Gateway pre-auth command injection (CVE-2026-88771): Perl script shells out logged input; zero-day in default configuration, fixed in 14.1-73.37 and 13.1-64.23](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/)**
  Patch NetScaler ADC and Gateway to 14.1-73.37 / 13.1-64.23 (or the FIPS/NDcPP equivalents) now, enable Enhanced ISN Generation, and hunt for compromise, because this root-level pre-auth bug was…
  _Why now: Pre-auth root command injection in NetScaler ADC/Gateway exploited as a zero-day in default configuration; concrete fixed builds, a sibling bug the upgrade alone doesn't fix, and log-hunting guidance. · cve · active-exploitation · timely · high-relevance_
- **[Google PageBreak: non-AI exploit validators gate AI web-testing agent: 500+ XSS bugs, near-zero false positives, but only 2 in apps on Google's high-assurance frameworks](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project)**
  Let the AI agent propose bugs, report only what a non-AI validator confirms by exploitation, and treat safe-by-default frameworks as the stronger defense.
  _Why now: Google's production-scale numbers for AI web testing gated by non-AI exploit validators (500+ XSS, near-zero false positives, only 2 on its high-assurance frameworks) teach how to make agent-found bugs trustworthy. · trending · newsworthy · timely_
- **[F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/)**
  Edge appliances keep shipping pre-auth memory-corruption bugs in authentication paths (here, a missing length check on an Authorization header), so they need emergency patching, minimal exposure and…
  _Why now: Pre-auth RCE in an internet-facing BIG-IP edge appliance, exploited in the wild; teaches emergency patching and minimal exposure for auth-path parsing on edge devices. · cve · active-exploitation · timely · high-relevance_
- **[JFrog Artifactory auth-bypass chain exploited in the wild, leaving Groovy plugin backdoors that survive patching and stolen token-signing keys](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201)**
  For an exposed artifact registry, patching is not remediation: hunt for rogue admins and plugins and rotate token-signing keys and every stored credential.
  _Why now: In-the-wild exploitation of a JFrog Artifactory auth-bypass chain leaving Groovy plugin backdoors; teaches what to hunt for on a core build-infrastructure system. · cve · active-exploitation · newsworthy_
- **[ITRES Labs used ChatGPT to rebuild two BruCON Windows kernel techniques, whose source was never released, in about 24 hours](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/)**
  The author argues LLMs make partially disclosed exploit research much cheaper to reproduce, so release decisions for talks, binaries and repos should assume others can rebuild it.
  _Why now: tl;dr sec-featured case of an LLM-assisted researcher rebuilding Windows kernel techniques from slides and a binary in about 24 hours; it changes how to weigh partial disclosure. · trending · newsworthy_

**📈 Emerging trends**

- **rce** (🔺 rising) — 15 findings from 12 sources since 2026-06-29.
- **command-injection** (🔺 rising) — 7 findings from 6 sources since 2026-07-20.
- **exploited-in-the-wild** (🔺 rising) — 7 findings from 3 sources since 2026-09-23.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 58.68
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 58.25
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964)** · _source_ · composite 55.25
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.

**📈 Emerging trends**

- **llm-as-judge** (🔺 rising) — 4 findings from 3 sources since 2026-08-07.
- **red-teaming** (🔺 rising) — 6 findings from 6 sources since 2025-03-13.
- **evals** (🔺 rising) — 21 findings from 10 sources since 2023-12-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-25.</sub>
