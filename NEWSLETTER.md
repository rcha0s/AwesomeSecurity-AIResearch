# 📰 Security & AI Research — Daily Snapshot (2026-11-21)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

26 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Dragos canary prompts found three AI hosting providers breached](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens)** · _www.dragos.com_ · composite 72.25
  Assume every router and host on the path can read and keep your prompt, so keep live credentials and private URLs out of prompts, whatever privacy flag is set.
- **[Anthropic releases FlashProve to prove responses came from hidden model weights](https://www.anthropic.com/research/provable-inference)** · _Anthropic Research_ · composite 60.19
  Cryptographic proof that a specific model produced an output is now a working prototype, though still about 70-95x the cost of inference, so it is an audit tool rather than a per-request default.
- **[Apiiro finds Claude Code permission allowlists leak secrets into public GitHub repos](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)** · _@shmulc via Hacker News_ · composite 58.0
  Treat agent permission files, transcripts and memory files as secret-bearing like .env, and approve command patterns that reference $VARS rather than literal commands with secrets in them.
- **[MCP Inspector fixes two critical one-click RCE flaws in version 1.0.3](https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-4fc4-wcmh-4g86)** · _github.com_ · composite 57.75
  Treat MCP debugging tools as code-execution surfaces: update Inspector to 1.0.3 and never point it at servers you do not trust.
- **[MobileProbe red-teams mobile GUI agents by placing injections along their actual route](http://arxiv.org/abs/2611.16693v1)** · _NDSS (via arXiv)_ · composite 57.55
  If your mobile or GUI agent security eval injects payloads at fixed steps, it probably undercounts risk, because injections must follow each agent's actual route to test it.
- **[Poisoned reference answers can plant backdoor rules in optimized agent Skills](http://arxiv.org/abs/2611.09348v1)** · _NeurIPS (via arXiv)_ · composite 54.55
  Whoever controls the reference answers used to optimize a Skill can plant a hidden trigger rule in it without touching the model, the optimizer or the Skill file, so treat that feedback as untrusted input.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Todoist MCP HTTP server lets websites edit Todoist data via DNS rebinding](https://github.com/advisories/GHSA-833v-v58w-294h)**
  Binding an MCP server to loopback is not authentication: HTTP-mode MCP servers need Host and Origin validation plus a per-run caller secret.
  _Why now: Second critical MCP HTTP-mode DNS-rebinding bug: loopback binding is not authentication, so a caller secret is needed. · trending · cve · high-relevance_
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

**📈 Emerging trends**

- **mcp** (🔺 rising) — 39 findings from 20 sources since 2026-02.
- **prompt-injection** (🔺 rising) — 49 findings from 25 sources since 2026-02.
- **coding-agents** (🔺 rising) — 23 findings from 16 sources since 2026-08-06.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[OpenJDK Base64 decoder flaw Java4Shell corrupts memory on AVX-512 CPUs](https://securitylabs.datadoghq.com/articles/java4shell-remote-code-execution-in-openjdk-cve-2026-114938/)** · _Datadog Security Labs_ · composite 68.97
  Patch JDK 17, 21, 25 and 27 (including bundled runtimes and container images), prioritizing x86-64 hosts whose CPUs report avx512vbmi.
- **[OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/)** · _tl;dr sec (curator link)_ · composite 67.6
  Kernel LPE discovery and exploitation is now cheap and fast, so local-user access on an unpatched Linux host should be treated as close to root, and AI vulnerability pipelines need independent checks on how each result…
- **[Google Project Zero shortens its disclosure deadline to 30 days by 2028](https://projectzero.google/2026/11/disclosure-policy.html)** · _Google Project Zero_ · composite 65.5
  A major research team now treats AI-accelerated exploitation as the default, so vendors need to fix every reported bug within 30 to 60 days and close the patch gap, whatever the bug's severity.
- **[Masato Kinugawa solves PortSwigger's impossible innerHTML-without-equals XSS using the selectedcontent element](https://portswigger.net/research/achieving-the-impossible-xss-in-innerhtml-without-equals)** · _PortSwigger Research_ · composite 65.29
  New HTML elements create new XSS paths; sanitizers and filters that block characters or script tags need re-testing against them.
- **[Anthropic's unreleased model built five attack chains against major software](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)** · _Anthropic Research_ · composite 60.64
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.
- **[Malicious npm package installs Hermes Agent as a Telegram-controlled backdoor](https://safedep.io/blog/malicious-npm-leadstack-crm-connect-hermes-agent-backdoor)** · _SafeDep_ · composite 58.26
  A malicious package can drop a legitimate AI agent as the implant, so treat unexpected agent installs and agent services as compromise signals.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[CISA adds Apache Axis 1.x unsafe reflection flaw to exploited vulnerabilities list](https://nvd.nist.gov/vuln/detail/CVE-2026-90436)**
  Find any Axis 1.x in your dependency trees and replace it or patch it yourself, because the vendor will not ship a fix.
  _Why now: CISA says an Apache Axis 1.x flaw is exploited and the project will not ship a fix, so owners must find and replace or patch the library themselves. · cve · active-exploitation · timely_
- **[CISA adds REDCap unauthenticated code execution flaw to exploited vulnerabilities list](https://nvd.nist.gov/vuln/detail/CVE-2026-90817)**
  If you run REDCap 13.3.0 or later, upgrade to a fixed build now and review who can reach your public survey links.
  _Why now: CISA added unauthenticated REDCap code execution to its exploited list with fixed builds on three release lines and a three-day federal deadline. · cve · active-exploitation · timely_
- **[Malicious Microsoft agent-framework PyPI versions steal Azure and CI credentials](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi)**
  Teams building agents on Python SDKs should pin versions, scan site-packages for unexpected .pth files, and treat any host that ran 1.26.1 or 1.26.2 as having leaked its cloud identities.
  _Why now: Live supply-chain incident in a widely used agent SDK: malicious PyPI releases 1.26.1 and 1.26.2 steal Azure and CI credentials, with concrete checks (pin versions, scan for unexpected .pth files). · newsworthy · active-exploitation · timely · high-relevance_
- **[Malicious WPPConnect npm and Docker releases steal secrets and WhatsApp sessions](https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions)**
  Do not treat a trusted publisher or provenance check as proof of review; add release-age delays, environment approval gates on publish workflows, and egress allowlists in CI.
  _Why now: Malicious npm and Docker releases from a trusted publisher steal secrets and WhatsApp sessions; trusted provenance did not mean reviewed, so release-age delays and publish approval gates apply. · newsworthy · active-exploitation · timely_
- **[NSA's classified network goes down after patching, with no sign of attack](https://www.cnn.com/2026/11/17/politics/highly-classified-national-security-communications-network-goes-down)**
  Stage and canary emergency patches, and keep tested fallback paths, because a rushed fix can take down critical systems as an attack would.
  _Why now: Reported outage of a classified US national-security network after patching, with no sign of attack, amid attack speculation; the teachable point is to stage and canary emergency patches and keep tested fallbacks. · newsworthy · widely-reported · timely_

**📈 Emerging trends**

- **exploited-in-the-wild** (🔺 rising) — 26 findings from 4 sources since 2026-09-23.
- **supply-chain** (🔺 rising) — 50 findings from 28 sources since 2026-06-30.
- **rce** (🔺 rising) — 25 findings from 17 sources since 2026-06-29.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Microsoft finds 8% of coding sessions account for 44% of costs](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)** · _Microsoft Research Blog_ · composite 54.73
  If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.
- **[Claude Code team explains how it verifies agent-written code at scale](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)** · _@craigmart via Hacker News_ · composite 53.5
  Treat the verification layer as a system of its own: run the real app, keep the checks out of reach of the change, and measure the checks against past incidents.
- **[UC Berkeley finds harness overhead can double agent cost at similar accuracy](https://arxiv.org/abs/2611.12122)** · _UC Berkeley Sky Lab (Park et al.)_ · composite 52.75
  Measure how much of your agent spend is context rereads and harness overhead before tuning anything else.
- **[York University's FlowPlan cuts Claude Code tokens by planning edits first](https://arxiv.org/abs/2611.13241)** · _York University (Sepidband et al.)_ · composite 52.75
  Replacing post-edit re-reading and re-testing with a stated plan cut coding agent tokens with no significant loss in fix rate.
- **[Researchers find agents keep accuracy with short, frequently compacted contexts](https://arxiv.org/abs/2611.05306)** · _Belcak et al._ · composite 45.25
  Short, frequently compacted contexts kept accuracy here; on hosted APIs, test that against the cache hits each compaction gives up.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)**
  Tool-call quality depends on how the model is served, not only on the model. Turn on constrained decoding per model, check it with a tool-call benchmark, and re-check after engine upgrades.
  _Why now: Concrete production numbers (92% to 100%, back to 91% after a vLLM default change) that any team self-hosting open-weight models for agents can act on immediately. · high-relevance · timely_
- **[Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents)**
  Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.
  _Why now: Directly usable harness change: a model-invoked compaction tool plus a fire/suppress rubric beats fixed token-threshold compaction across seven models. · trending · high-relevance_

**📈 Emerging trends**

- **coding-agents** (🔺 rising) — 16 findings from 12 sources since 2026-07-21.
- **evals** (🔺 rising) — 33 findings from 18 sources since 2023-12-07.
- **benchmarks** (🔺 rising) — 16 findings from 12 sources since 2026-07-09.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-11-21.</sub>
