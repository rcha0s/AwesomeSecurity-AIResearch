# 📰 Security & AI Research — Daily Snapshot (2026-10-29)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

22 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 62.09
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[MCP Inspector fixes two critical one-click RCE flaws in version 1.0.3](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)** · _github.com_ · composite 61.25
  Treat MCP debugging tools as code-execution surfaces: update Inspector to 1.0.3 and never point it at servers you do not trust.
- **[METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/)** · _METR_ · composite 60.98
  Agent transcripts are attacker-controlled input, so the viewers, log pipelines and monitors that display them are security-critical and need the same output-encoding and tamper-resistance work as any other app that…
- **[Mistral Vibe fixes permission-check bypasses in versions 2.25.4 and 2.25.5](https://www.vulncheck.com/advisories/mistral-vibe-permission-bypass-via-bash-line-continuation)** · _vulncheck.com_ · composite 56.75
  A permission gate that approves a command from a parser that disagrees with the shell is a bypass; upgrade Vibe and fail closed on parse errors.
- **[NVIDIA OpenShell runs coding agents in kernel-enforced sandboxes under YAML policy](https://docs.nvidia.com/openshell/latest/about/overview.html)** · _docs.nvidia.com_ · composite 56.0
  A declarative, kernel-level sandbox for coding agents now exists as an open-source option; compare its policy model before writing your own.
- **[Paper proves models can hide capabilities that audits cannot find](https://arxiv.org/abs/2610.13928)** · _arxiv.org_ · composite 56.0
  A clean capability evaluation cannot prove a model lacks a dangerous capability if the model's builder is adversarial.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[One crafted medical image file crashes or silently corrupts MONAILabel inference](https://github.com/advisories/GHSA-6hp3-vr39-rqw8)**
  Machine learning pipelines that read numbers from uploaded files need explicit finiteness checks, because one NaN can corrupt medical output with no error.
  _Why now: Critical advisory in a medical AI server showing why ML pipelines need finiteness checks on untrusted file metadata. · cve · timely_
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

**📈 Emerging trends**

- **coding-agents** (🔺 rising) — 14 findings from 9 sources since 2026-08-06.
- **prompt-injection** (🔺 rising) — 38 findings from 20 sources since 2026-02.
- **sandbox-escape** (🔺 rising) — 12 findings from 11 sources since 2026-07-15.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)** · _Anthropic Research_ · composite 64.14
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.
- **[Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)** · _watchTowr Labs_ · composite 62.84
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.
- **[watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)** · _watchTowr Labs_ · composite 59.54
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.
- **[pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape)** · _source_ · composite 59.0
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 58.25
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.
- **[PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers](https://portswigger.net/research/scalable-vector-grief)** · _PortSwigger Research_ · composite 56.88
  If you accept SVG uploads, sanitize with DOMPurify or darylldoyle/svg-sanitizer, serve user files from a separate origin, and never let users influence response headers.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Alpine Linux rebuilt GitLab after its upgrade missed a Ruby patch](https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html)**
  If you build GitLab yourself, check what runtime patches its official packages carry, and log outbound traffic so you can rule a compromise in or out.
  _Why now: First-hand incident on a CVSS 10.0 GitLab bug: the fix lived in a bundled Ruby patch that self-built installs miss, and missing egress logs forced a full rebuild. · newsworthy · cve · active-exploitation · timely · high-relevance_
- **[Exploited Linux kernel flaw lets IPsec decryption overwrite page-cache data](https://nvd.nist.gov/vuln/detail/CVE-2026-46300)**
  A kernel bug disclosed in May is now exploited in the wild, so any Linux host still on an unpatched kernel needs the vendor update now.
  _Why now: CISA confirms in-the-wild exploitation of a Linux kernel page-cache bug disclosed in May; patch and reboot kernels, IPsec hosts first. · cve · active-exploitation · timely_
- **[Exploited Adobe Commerce and Magento upload flaw can lead to code execution](https://nvd.nist.gov/vuln/detail/CVE-2026-48356)**
  An actively exploited file-upload flaw spans every supported Commerce and Magento line, so storefront operators should patch now rather than wait for a maintenance window.
  _Why now: CISA-listed exploited upload flaw spanning every Commerce and Magento Open Source line from 2.4.4 to 2.4.9; storefronts should patch and check upload directories. · cve · active-exploitation · timely_
- **[Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html)**
  Treating loopback as trusted makes any request-forgery bug a way past the perimeter, so patch rather than relying on path-based firewall rules.
  _Why now: ShinyHunters has exploited this PeopleSoft chain since May. It teaches two things that transfer: a default loopback allowlist turns server-side request forgery into unauthenticated RCE, and path-matching WAF rules fall to a single… · active-exploitation · cve · newsworthy · high-relevance_
- **[InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/)**
  On appliances, patch speed depends on the vendor's firmware schedule, so limit exposure of management interfaces now instead of waiting.
  _Why now: PHP2Shell is the theme of the week. This adds a lesson that changes what defenders do: appliances with PHP compiled into their firmware cannot be patched by customers, so pull their management interfaces off the internet now. · trending · active-exploitation · timely_

**📈 Emerging trends**

- **rce** (🔺 rising) — 19 findings from 15 sources since 2026-06-29.
- **exploited-in-the-wild** (🔺 rising) — 13 findings from 3 sources since 2026-09-23.
- **php2shell** (🔺 rising) — 7 findings from 6 sources since 2026-10-22.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 57.18
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 56.75
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964)** · _source_ · composite 53.75
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/)** · _OpenAI Alignment Blog_ · composite 51.35
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

- **evals** (🔺 rising) — 24 findings from 12 sources since 2023-12-07.
- **benchmarks** (🔺 rising) — 10 findings from 8 sources since 2026-07-09.
- **human-in-the-loop** (🔺 rising) — 4 findings from 3 sources since 2026-08-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-29.</sub>
