# 📰 Security & AI Research — Daily Snapshot (2026-10-23)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

5 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](https://arxiv.org/abs/2610.23109)** · _arXiv cs.CR (Cryptography and Security)_ · composite 64.09
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)**
  Version and change-review every MCP tool description as if it were a system prompt, and force re-approval whenever tool metadata changes.
  _Why now: Microsoft security guidance on a fast-moving theme (agentic MCP tooling): version and re-approve tool descriptions like system prompts. Part of the top agent-security trend cluster. · trending · newsworthy · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986v1)**
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks legitimate.
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

**📈 Emerging trends**

- **prompt-injection** (🔺 rising) — 26 findings from 13 sources since 2026-02.
- **mcp** (watching) — 19 findings from 12 sources since 2026-02.
- **agent-security** (🔺 rising) — 15 findings from 14 sources since 2026-02.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](https://www.anthropic.com/research/formal-verification)** · _source_ · composite 60.25
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Sentry's Next.js tunnelRoute skipped middleware for everything under the tunnel path, not just the requests its rewrite served (GHSA-mchm-gjx6-7h55)](https://github.com/advisories/GHSA-mchm-gjx6-7h55)**
  Any SDK or framework that exempts paths from middleware is a potential authz bypass: if middleware is your only authorization check, grep your dependencies for middleware skips.
  _Why now: Critical GHSA in a ubiquitous Next.js SDK with a transferable lesson: middleware exemptions are authz bypasses wherever middleware is the only authorization check. · cve · newsworthy · high-relevance · timely_
- **[CISA KEV: Plex Media Server encoded-URI-scheme flaw CVE-2026-96654 exploited in the wild, part of a four-CVE chain](https://nvd.nist.gov/vuln/detail/CVE-2026-96654)**
  Patch Plex Media Server now: four chained CVEs are in KEV with a public plex2shell write-up.
  _Why now: Exploited-in-the-wild Plex chain added to CISA KEV with a due date of today and a public plex2shell write-up; patch now. · active-exploitation · cve · timely_
- **[Pillow MIC images hang n_frames forever: an inherited method that depends on an overridden tell() (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  Parse untrusted images under a timeout and restrict Image.open to the formats you expect.
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_
- **[How we found 24 Android vulnerabilities using our open source AI security agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)**
  Scaffolded, platform-specific taskflows make LLMs effective Android bug hunters, but severity and exploitability still need a PoC and a human.
  _Why now: 24 real, disclosed Android vulnerabilities (OsmAnd location tracking, a WebView account-takeover chain) found with an open-source agent you can run today, plus candid lessons on LLM severity misjudgment and false positives. · newsworthy · trending · timely · high-relevance_
- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  Gate agent PRs with automated secret and dependency-integrity checks - human review demonstrably does not catch this class, and the humans are introducing most of it.
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

**📈 Emerging trends**

- **supply-chain** (watching) — 23 findings from 16 sources since 2026-06-30.
- **ghsa** (🔺 rising) — 8 findings from 8 sources since 2026-09-08.
- **npm** (watching) — 9 findings from 6 sources since 2026-07-15.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · _arXiv cs.AI (Artificial Intelligence)_ · composite 59.18
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 58.75
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964)** · _source_ · composite 55.75
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.

**📈 Emerging trends**

- **arxiv** (watching) — 76 findings from 2 sources since 2026-08-07.
- **agents** (🔺 rising) — 24 findings from 8 sources since 2026-05.
- **evals** (🔺 rising) — 19 findings from 10 sources since 2023-12-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-23.</sub>
