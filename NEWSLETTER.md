# 📰 Security & AI Research — Daily Snapshot (2026-11-18)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

30 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Anthropic releases FlashProve to prove responses came from hidden model weights](https://www.anthropic.com/research/provable-inference)** · _Anthropic Research_ · composite 61.94
  Cryptographic proof that a specific model produced an output is now a working prototype, though still about 70-95x the cost of inference, so it is an audit tool rather than a per-request default.
- **[Apiiro finds Claude Code permission allowlists leak secrets into public GitHub repos](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)** · _@shmulc via Hacker News_ · composite 59.75
  Treat agent permission files, transcripts and memory files as secret-bearing like .env, and approve command patterns that reference $VARS rather than literal commands with secrets in them.
- **[MobileProbe red-teams mobile GUI agents by placing injections along their actual route](http://arxiv.org/abs/2611.16693v1)** · _NDSS (via arXiv)_ · composite 59.3
  If your mobile or GUI agent security eval injects payloads at fixed steps, it probably undercounts risk, because injections must follow each agent's actual route to test it.
- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 58.84
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.
- **[MCP Inspector fixes two critical one-click RCE flaws in version 1.0.3](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)** · _github.com_ · composite 58.0
  Treat MCP debugging tools as code-execution surfaces: update Inspector to 1.0.3 and never point it at servers you do not trust.
- **[Poisoned reference answers can plant backdoor rules in optimized agent Skills](http://arxiv.org/abs/2611.09348v1)** · _NeurIPS (via arXiv)_ · composite 56.3
  Whoever controls the reference answers used to optimize a Skill can plant a hidden trigger rule in it without touching the model, the optimizer or the Skill file, so treat that feedback as untrusted input.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Microsoft shows phished device codes can hijack GitHub Copilot CLI sessions](https://www.microsoft.com/en-us/security/blog/2026/11/17/the-risks-of-device-code-authentication-for-ai-coding-agents/)**
  Treat agent OAuth grants as high-value credentials: restrict remote control, session sync and memory, and teach developers to approve only device codes they started.
  _Why now: Microsoft shows phished OAuth device codes can hijack GitHub Copilot CLI sessions; the lesson is to treat agent OAuth grants as high-value credentials. · trending · newsworthy · timely · high-relevance_
- **[Microsoft shows poisoned fine-tuning data and checkpoints hijack coding agents' tools](https://www.microsoft.com/en-us/security/blog/2026/11/12/trained-to-betray-how-post-training-supply-chain-attacks-hijack-coding-agents/)**
  Treat third-party checkpoints and fine-tuning datasets as untrusted code, and rely on limiting and authorizing the agent's tool permissions, the control that holds whatever the model learned.
  _Why now: Microsoft shows 1% poisoned fine-tuning data teaches coding agents to misuse whatever command tool exists, and RL hides the utility loss; actionable for anyone fine-tuning or adopting open checkpoints. · trending · newsworthy · high-relevance_
- **[AG2 SandboxShellTool allowlist is bypassed by a newline in the command](https://github.com/advisories/GHSA-2h4w-29cv-2cmv)**
  Upgrade AG2 past the fix, and treat any agent shell allowlist that passes commands to sh -c as a denylist that will miss some separator.
  _Why now: Second agent shell-tool allowlist bypass in weeks (after Mistral Vibe): a newline beats AG2's allowed=[...] and readonly=True, a concrete audit check for any agent shell tool that validates a string and then runs sh -c. · trending · cve · high-relevance_
- **[GPUStack treated spoofable loopback requests as admin, and attackers exploited it](https://nvd.nist.gov/vuln/detail/CVE-2026-102895)**
  Upgrade GPUStack to 2.2.0 now and treat any AI serving control plane that trusts loopback or a client IP header as unauthenticated.
  _Why now: CISA lists GPUStack's loopback-trust auth bypass as exploited in the wild; anyone running AI model-serving control planes should patch to 2.2.0 and stop trusting loopback or client real-IP headers as authentication. · active-exploitation · cve · timely · high-relevance_
- **[Fireworks AI discloses second breach reached through a third-party cloud provider](https://www.bleepingcomputer.com/news/security/fireworks-ai-discloses-new-breach-after-cloud-provider-hack/)**
  Fireworks AI's second breach in weeks came through a third-party cloud host, and exposed customer data and incomplete model weights.
  _Why now: An AI inference provider's second breach in weeks came through a third-party cloud host; a live incident with a teachable third-party-host lesson for AI infrastructure teams. · newsworthy · incident-response · timely_

**📈 Emerging trends**

- **mcp** (🔺 rising) — 36 findings from 20 sources since 2026-02.
- **coding-agents** (🔺 rising) — 22 findings from 15 sources since 2026-08-06.
- **prompt-injection** (🔺 rising) — 48 findings from 25 sources since 2026-02.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[OpenJDK Base64 decoder flaw Java4Shell corrupts memory on AVX-512 CPUs](https://securitylabs.datadoghq.com/articles/java4shell-remote-code-execution-in-openjdk-cve-2026-114938/)** · _Datadog Security Labs_ · composite 70.72
  Patch JDK 17, 21, 25 and 27 (including bundled runtimes and container images), prioritizing x86-64 hosts whose CPUs report avx512vbmi.
- **[OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/)** · _tl;dr sec (curator link)_ · composite 69.35
  Kernel LPE discovery and exploitation is now cheap and fast, so local-user access on an unpatched Linux host should be treated as close to root, and AI vulnerability pipelines need independent checks on how each result…
- **[Google Project Zero shortens its disclosure deadline to 30 days by 2028](https://projectzero.google/2026/11/disclosure-policy.html)** · _Google Project Zero_ · composite 67.25
  A major research team now treats AI-accelerated exploitation as the default, so vendors need to fix every reported bug within 30 to 60 days and close the patch gap, whatever the bug's severity.
- **[Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)** · _Anthropic Research_ · composite 60.89
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.
- **[Malicious native apps can hijack browser Native Messaging to steal password vaults](http://arxiv.org/abs/2611.04291v1)** · _IEEE S&P (via arXiv)_ · composite 58.4
  If your extension talks to a native helper, authenticate and encrypt that channel yourself; the browser does not.
- **[Microsoft FORGE Lab finds soundness bugs in Rust's standard library](https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/)** · _Microsoft Security Blog_ · composite 56.24
  Even Rust's standard library has soundness bugs of the three kinds the post names, and the authors say agents make the environment-dependent OS-boundary area practical to search.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Malicious Microsoft agent-framework PyPI versions steal Azure and CI credentials](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi)**
  Teams building agents on Python SDKs should pin versions, scan site-packages for unexpected .pth files, and treat any host that ran 1.26.1 or 1.26.2 as having leaked its cloud identities.
  _Why now: Live supply-chain incident in a widely used agent SDK: malicious PyPI releases 1.26.1 and 1.26.2 steal Azure and CI credentials, with concrete checks (pin versions, scan for unexpected .pth files). · newsworthy · active-exploitation · timely · high-relevance_
- **[Malicious WPPConnect npm and Docker releases steal secrets and WhatsApp sessions](https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions)**
  Do not treat a trusted publisher or provenance check as proof of review; add release-age delays, environment approval gates on publish workflows, and egress allowlists in CI.
  _Why now: Malicious npm and Docker releases from a trusted publisher steal secrets and WhatsApp sessions; trusted provenance did not mean reviewed, so release-age delays and publish approval gates apply. · newsworthy · active-exploitation · timely_
- **[NSA's classified network goes down after patching, with no sign of attack](https://www.cnn.com/2026/11/17/politics/highly-classified-national-security-communications-network-goes-down)**
  Stage and canary emergency patches, and keep tested fallback paths, because a rushed fix can take down critical systems as an attack would.
  _Why now: Reported outage of a classified US national-security network after patching, with no sign of attack, amid attack speculation; the teachable point is to stage and canary emergency patches and keep tested fallbacks. · newsworthy · widely-reported · timely_
- **[Chainguard details wfx stealer that backdoors cloud roles and can forge checks](https://www.chainguard.dev/unchained/wfx-loot-stolen-github-tokens-pushed-a-ci-secret-stealer-into-60-000-repositories-november-2026)**
  With a stolen write token, pinning and pull request review do nothing, so limit what a CI runner holds and audit cloud trust after any wfx hit.
  _Why now: Live campaign across 60,000+ repositories; concrete detection steps (missing run numbers, AWS Principal * trust, Azure wfx-ci credentials) and the lesson that secret rotation alone leaves cloud backdoors. · active-exploitation · widely-reported · trending · high-relevance_
- **[StepSecurity finds fake-interview npm look-alikes stayed on npm for seven months](https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines)**
  Interview assignments run on work laptops are an employer supply-chain risk, and the malware hides in build-time code and blockchain-resolved servers that install-script controls and static…
  _Why now: Live DPRK fake-interview campaign whose loader runs at CSS build time, so install-script controls and short cooldowns miss it; gives an IOC hunt for developer laptops. · active-exploitation · timely · high-relevance_

**📈 Emerging trends**

- **exploited-in-the-wild** (🔺 rising) — 23 findings from 4 sources since 2026-09-23.
- **supply-chain** (🔺 rising) — 50 findings from 28 sources since 2026-06-30.
- **rce** (🔺 rising) — 21 findings from 16 sources since 2026-06-29.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Microsoft finds 8% of coding sessions account for 44% of costs](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)** · _Microsoft Research Blog_ · composite 56.48
  If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.
- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 53.93
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 53.5
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits](https://arxiv.org/abs/2610.25964)** · _source_ · composite 50.5
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](https://alignment.openai.com/beyond-gmean-squared/)** · _OpenAI Alignment Blog_ · composite 48.1
  If you use a monitor as a deployment gate, compare monitors and models on matched instances and measure what still gets through after rejection-and-retry, not raw discrimination alone.
- **[GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227)** · _Hugging Face Daily Papers_ · composite 46.27
  If your harness edits skills automatically, assign credit by comparing repeated runs (group-relative), not by co-occurrence with success, or harmful skills will survive.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)**
  Tool-call quality depends on how the model is served, not only on the model. Turn on constrained decoding per model, check it with a tool-call benchmark, and re-check after engine upgrades.
  _Why now: Concrete production numbers (92% to 100%, back to 91% after a vLLM default change) that any team self-hosting open-weight models for agents can act on immediately. · high-relevance · timely_
- **[Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents)**
  Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.
  _Why now: Directly usable harness change: a model-invoked compaction tool plus a fire/suppress rubric beats fixed token-threshold compaction across seven models. · trending · high-relevance_

**📈 Emerging trends**

- **evals** (🔺 rising) — 33 findings from 18 sources since 2023-12-07.
- **coding-agents** (🔺 rising) — 14 findings from 10 sources since 2026-07-21.
- **opinion** (🔺 rising) — 6 findings from 3 sources since 2026-10-25.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-11-18.</sub>
