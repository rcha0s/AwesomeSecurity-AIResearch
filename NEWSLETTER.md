# 📰 Security & AI Research — Daily Snapshot (2026-10-22)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

27 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Google dev kit spurs first-ever agent-on-agent violence](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)** · _source_ · composite 62.35
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped permissions, not tighter…
- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)** · _source_ · composite 61.75
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel — instrument it or write it out of the trust boundary.
- **[Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)** · _Embrace The Red (Johann Rehberger)_ · composite 56.65
  A model's safety refusal to run an untrusted binary is not automatically safe if the 'safe' alternative it chooses (writing its own code to parse the untrusted data) is itself exploitable — containment has to hold at…
- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)** · _source_ · composite 55.5
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.
- **[Multidimensional Item-Response-Theory Auditing Reveals Some 'Safety' Benchmarks Are Actually Measuring General Reasoning](https://huggingface.co/blog/allenai/benchmirt)** · _source_ · composite 51.6
  A benchmark's stated purpose (e.g. "safety") doesn't guarantee its score is actually driven by that capability, or even in the direction you'd assume — a model that scores well on WMDP's dual-use-knowledge "safety"…

**📈 Emerging trends**

- **prompt-injection** (watching) — 25 findings from 13 sources since 2026-02.
- **mcp** (watching) — 19 findings from 12 sources since 2026-02.
- **agent-security** (watching) — 14 findings from 13 sources since 2026-02.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- _Nothing new in the current window._

**📈 Trending & In the News**

_Not new ideas, but what the field is watching right now — held back by the novelty gate, surfaced by the editorial pass for being timely and teachable._

- **[Pillow MIC images hang n_frames forever: an inherited method that depends on an overridden tell() (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  Parse untrusted images under a timeout and restrict Image.open to the formats you expect.
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_

**📈 Emerging trends**

- **supply-chain** (watching) — 22 findings from 16 sources since 2026-06-30.
- **npm** (watching) — 8 findings from 6 sources since 2026-07-15.
- **ci-cd** (watching) — 5 findings from 5 sources since 2026-07-15.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)** · _source_ · composite 59.5
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](https://arxiv.org/abs/2610.25964)** · _source_ · composite 56.5
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.
- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)** · _source_ · composite 55.75
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better refusal training.
- **[Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)** · _source_ · composite 55.65
  When you hand an agent a durable goal plus strict 'what counts as a real finding' rules, it will plan multi-step tooling and self-filter noise — the rules, not the model alone, are what make the output actionable.

**📈 Emerging trends**

- **arxiv** (watching) — 76 findings from 2 sources since 2026-08-07.
- **agents** (watching) — 23 findings from 8 sources since 2026-05.
- **evals** (🔺 rising) — 17 findings from 9 sources since 2026-05.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-10-22.</sub>
