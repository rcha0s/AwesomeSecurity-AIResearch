# 📰 Security & AI Research — Daily Snapshot (2026-10-28)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

19 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 62.34
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[METR: MathJax injection in Inspect let agents rewrite what reviewers see](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/)** · _METR_ · composite 61.23
  Agent transcripts are attacker-controlled input, so the viewers, log pipelines and monitors that display them are security-critical and need the same output-encoding and tamper-resistance work as any other app that…
- **[UK AISI resumes most cyber evals with the internet turned off](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)** · _UK AI Security Institute Blog_ · composite 58.5
  A concrete, reusable control set for anyone running agentic cyber evals: two independent egress layers, a blocking monitor, preflight checks, and flag-terminated escape tests run from weaker to stronger models.
- **[MFOTL monitor flags 71.8% of STAC but fires on 29.3% of benign](http://arxiv.org/abs/2610.09793v1)** · _CCS (via arXiv)_ · composite 55.65
  A declarative policy monitor is only as good as the trace it reads: log approvals, timestamps and provenance that the agent cannot forge, or temporal guardrails turn into coarse action-type blocklists.
- **[Guardrail safety benchmarks mostly measure the training label policy](https://arxiv.org/abs/2610.25060)** · _Hugging Face Daily Papers_ · composite 54.87
  A guardrail's benchmark numbers are uninterpretable unless you know the 'unsafe' definition it was trained and graded on, its contamination, and its seed variance. Evaluate any vendor guardrail against your own policy.

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

- **prompt-injection** (🔺 rising) — 37 findings from 19 sources since 2026-02.
- **coding-agents** (🔺 rising) — 11 findings from 7 sources since 2026-08-06.
- **sandbox-escape** (🔺 rising) — 12 findings from 11 sources since 2026-07-15.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)** · _Anthropic Research_ · composite 64.39
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.
- **[Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)** · _watchTowr Labs_ · composite 63.09
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.
- **[Claude found 493 attack-surface issues across 25 open-source projects](https://www.anthropic.com/research/attack-surface-reduction)** · _Anthropic Research_ · composite 62.97
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.
- **[watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)** · _watchTowr Labs_ · composite 59.79
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.
- **[pwn.ai found a new Linux networking bug class escaping KVM guests](https://pwn.ai/blog/pwnescape)** · _source_ · composite 59.25
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 58.5
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html)**
  Treating loopback as trusted makes any request-forgery bug a way past the perimeter, so patch rather than relying on path-based firewall rules.
  _Why now: ShinyHunters has exploited this PeopleSoft chain since May. It teaches two things that transfer: a default loopback allowlist turns server-side request forgery into unauthenticated RCE, and path-matching WAF rules fall to a single… · active-exploitation · cve · newsworthy · high-relevance_
- **[InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/)**
  On appliances, patch speed depends on the vendor's firmware schedule, so limit exposure of management interfaces now instead of waiting.
  _Why now: PHP2Shell is the theme of the week. This adds a lesson that changes what defenders do: appliances with PHP compiled into their firmware cannot be patched by customers, so pull their management interfaces off the internet now. · trending · active-exploitation · timely_
- **[Skimmers hijacked Convertr's self-hosted analytics script to steal checkout card data](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/)**
  Any script loaded on checkout pages, even self-hosted analytics, belongs in the payment attack surface and needs patching and integrity checks.
  _Why now: A live Magecart incident in which one self-hosted analytics script skimmed every merchant's checkout. The lesson is concrete: treat every script loaded on checkout pages, analytics included, as payment-critical and check its integrity. · newsworthy · timely · high-relevance_
- **[Authlib accepts a JSON web signature with no signatures as verified](https://github.com/advisories/GHSA-6v38-4h7w-rj9h)**
  Any verifier that loops over signatures must reject an empty list; test your JWS and JWT code for that case.
  _Why now: Critical authentication bypass in a widely used Python library; the fail-open empty-loop pattern is a test every verifier should have. · cve · timely · high-relevance_
- **[Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets)**
  A stolen GitHub token turns your own CI into a secrets-theft channel, so hunt for the sync-check pattern and replace long-lived personal access tokens with short-lived, scoped ones.
  _Why now: Active campaign hitting private enterprise repos past GitHub's public-repo safeguard, with concrete hunt indicators and a token-lifetime fix. · active-exploitation · newsworthy · timely · high-relevance_

**📈 Emerging trends**

- **rce** (🔺 rising) — 19 findings from 15 sources since 2026-06-29.
- **exploited-in-the-wild** (🔺 rising) — 11 findings from 3 sources since 2026-09-23.
- **php2shell** (🔺 rising) — 7 findings from 6 sources since 2026-10-22.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 57.43
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 57.0
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964)** · _source_ · composite 54.0
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/)** · _OpenAI Alignment Blog_ · composite 51.6
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
- **llm-as-judge** (🔺 rising) — 5 findings from 4 sources since 2026-08-07.
- **coding-agents** (🔺 rising) — 7 findings from 6 sources since 2026-07-21.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-28.</sub>
