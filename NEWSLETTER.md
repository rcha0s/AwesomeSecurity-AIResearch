# 📰 Security & AI Research — Daily Snapshot (2026-11-10)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

18 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Anthropic releases FlashProve to prove responses came from hidden model weights](https://www.anthropic.com/research/provable-inference)** · _Anthropic Research_ · composite 66.94
  Cryptographic proof that a specific model produced an output is now a working prototype, though still about 70-95x the cost of inference, so it is an audit tool rather than a per-request default.
- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 59.59
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[MCP Inspector fixes two critical one-click RCE flaws in version 1.0.3](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)** · _github.com_ · composite 58.75
  Treat MCP debugging tools as code-execution surfaces: update Inspector to 1.0.3 and never point it at servers you do not trust.
- **[Mistral Vibe fixes permission-check bypasses in versions 2.25.4 and 2.25.5](https://www.vulncheck.com/advisories/mistral-vibe-permission-bypass-via-bash-line-continuation)** · _vulncheck.com_ · composite 54.25
  A permission gate that approves a command from a parser that disagrees with the shell is a bypass; upgrade Vibe and fail closed on parse errors.
- **[NVIDIA OpenShell runs coding agents in kernel-enforced sandboxes under YAML policy](https://docs.nvidia.com/openshell/latest/about/overview.html)** · _docs.nvidia.com_ · composite 53.5
  A declarative, kernel-level sandbox for coding agents now exists as an open-source option; compare its policy model before writing your own.
- **[Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060)** · _Hugging Face Daily Papers_ · composite 52.12
  A guardrail's benchmark numbers are uninterpretable unless you know the 'unsafe' definition it was trained and graded on, its contamination, and its seed variance. Evaluate any vendor guardrail against your own policy.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[AG2 SandboxShellTool allowlist is bypassed by a newline in the command](https://github.com/advisories/GHSA-2h4w-29cv-2cmv)**
  Upgrade AG2 past the fix, and treat any agent shell allowlist that passes commands to sh -c as a denylist that will miss some separator.
  _Why now: Second agent shell-tool allowlist bypass in weeks (after Mistral Vibe): a newline beats AG2's allowed=[...] and readonly=True, a concrete audit check for any agent shell tool that validates a string and then runs sh -c. · trending · cve · high-relevance_
- **[GPUStack treated spoofable loopback requests as admin, and attackers exploited it](https://nvd.nist.gov/vuln/detail/CVE-2026-102895)**
  Upgrade GPUStack to 2.2.0 now and treat any AI serving control plane that trusts loopback or a client IP header as unauthenticated.
  _Why now: CISA lists GPUStack's loopback-trust auth bypass as exploited in the wild; anyone running AI model-serving control planes should patch to 2.2.0 and stop trusting loopback or client real-IP headers as authentication. · active-exploitation · cve · timely · high-relevance_
- **[Fireworks AI discloses second breach reached through a third-party cloud provider](https://www.bleepingcomputer.com/news/security/fireworks-ai-discloses-new-breach-after-cloud-provider-hack/)**
  Fireworks AI's second breach in weeks came through a third-party cloud host, and exposed customer data and incomplete model weights.
  _Why now: An AI inference provider's second breach in weeks came through a third-party cloud host; a live incident with a teachable third-party-host lesson for AI infrastructure teams. · newsworthy · incident-response · timely_
- **[Caper approves coding-agent commands after running them in a snapshot sandbox](https://arxiv.org/abs/2610.40753)**
  Judge an agent's command by what it actually does in a sandbox, not by how the command reads.
  _Why now: Concrete pattern for approving coding-agent commands by their observed effects in a snapshot sandbox, on the week Apiiro showed don't-ask-again allowlists leaking secrets. · trending · high-relevance_
- **[Roo Code's command auto-approval can be bypassed in seven ways](https://www.vulncheck.com/advisories/roo-code-through-3.54.0-auto-approve-bypass-via-quote-masking-desynchronization)**
  Allowlist-by-prefix approval for agent shell commands breaks whenever the checker and the shell parse differently; do not enable auto-approve on untrusted content.
  _Why now: Named advisory with a transferable lesson for every coding-agent harness: prefix-allowlist auto-approval breaks whenever the checker and the shell parse a command differently. · newsworthy · high-relevance · timely · trending_

**📈 Emerging trends**

- **prompt-injection** (🔺 rising) — 44 findings from 23 sources since 2026-02.
- **coding-agents** (🔺 rising) — 17 findings from 12 sources since 2026-08-06.
- **mcp** (🔺 rising) — 32 findings from 18 sources since 2026-02.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/)** · _tl;dr sec (curator link)_ · composite 74.35
  Kernel LPE discovery and exploitation is now cheap and fast, so local-user access on an unpatched Linux host should be treated as close to root, and AI vulnerability pipelines need independent checks on how each result…
- **[Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)** · _Anthropic Research_ · composite 61.64
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.
- **[pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape)** · _source_ · composite 56.5
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 55.75
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.
- **[PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers](https://portswigger.net/research/scalable-vector-grief)** · _PortSwigger Research_ · composite 54.38
  If you accept SVG uploads, sanitize with DOMPurify or darylldoyle/svg-sanitizer, serve user files from a separate origin, and never let users influence response headers.
- **[Citizen Lab: Candiru spyware reached Al Jazeera devices through targeted ads](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)** · _source_ · composite 50.5
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Attackers used Ethersphere's own release pipeline to ship backdoored bee-js and Swarm Desktop](https://socket.dev/blog/bee-js-compromise)**
  Trusted publishing and valid provenance prove where a package was built, not that its source was reviewed, so release workflows need branch, tag and reviewer gates of their own.
  _Why now: Live npm and desktop-updater compromise reported by Socket, StepSecurity and SafeDep; teaches that valid trusted-publishing provenance does not prove review, and gives concrete release-workflow gates. · newsworthy · widely-reported · active-compromise · timely · high-relevance_
- **[Check Point found ARTEX operators letting AI agents run cybercrime campaigns unattended](https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/)**
  Agentic attack platforms let unskilled criminals test every endpoint of many targets for a few hundred dollars, so basic gaps like hardcoded credentials and unauthenticated APIs are now found at…
  _Why now: First look inside criminals' agent consoles (models, prompts, costs) shows autonomous fleets finding commodity web gaps at scale; it continues the ARTEX abuse story and gives concrete gaps to close. · trending · newsworthy · high-relevance_
- **[OpenSSH ships an emergency workaround for a critical musl-specific vulnerability](https://hachyderm.io/@damienmiller/117563026759098135)**
  Find every musl-based SSH host, especially Alpine containers and appliances, and turn off password authentication now, because maintainers no longer wait out long embargoes.
  _Why now: Critical OpenSSH bug on musl/no-PAM hosts (Alpine) with a fix released a day after discovery and a one-line mitigation (PasswordAuthentication=no) to apply now; the maintainer cites AI rediscovery as the reason for skipping a long embargo. · timely · newsworthy · high-relevance · actionable_
- **[Cisco ASA and FTD VPN crash bug is exploited, CISA gives three days](https://nvd.nist.gov/vuln/detail/CVE-2026-76418)**
  If your ASA or FTD VPN uses secondary authentication on a tunnel group, patch now, because attackers are already using this to knock VPNs offline.
  _Why now: Actively exploited unauthenticated VPN-edge DoS in CISA KEV with a three-day deadline; exposure is scoped by one config check (secondary authentication on a tunnel group). · cve · active-exploitation · timely_
- **[Exploited VMware ESX flaw lets attacker with admin rights act unlogged](https://nvd.nist.gov/vuln/detail/CVE-2026-41709)**
  ESX audit logs may be silent about what a hijacked admin did, so do not treat clean ESX logs as proof of no tampering.
  _Why now: Exploited ESX logging gap in KEV; the transferable lesson is that clean hypervisor logs are not proof of no tampering, so keep an out-of-band log source. · cve · active-exploitation · high-relevance_

**📈 Emerging trends**

- **rce** (🔺 rising) — 19 findings from 15 sources since 2026-06-29.
- **exploited-in-the-wild** (🔺 rising) — 17 findings from 4 sources since 2026-09-23.
- **php2shell** (🔺 rising) — 7 findings from 6 sources since 2026-10-22.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 54.68
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 54.25
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964)** · _source_ · composite 51.25
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/)** · _OpenAI Alignment Blog_ · composite 48.85
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

- **evals** (🔺 rising) — 29 findings from 16 sources since 2023-12-07.
- **opinion** (🔺 rising) — 6 findings from 3 sources since 2026-10-25.
- **mcp** (🔺 rising) — 8 findings from 6 sources since 2026-08-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-11-10.</sub>
