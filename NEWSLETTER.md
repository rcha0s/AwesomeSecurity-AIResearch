# 📰 Security & AI Research — Daily Snapshot (2026-08-29)

> A daily-refreshed digest of the most teachable, **vetted** security and AI research from the last 31 days, curated and source-cited. Three tracks: AI Security, Product Security, AI Research.

339 vetted findings in window · [← home](README.md) · [full trends](TRENDS.md)

---

## AI Security

_Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming._

**🔬 Latest research**

- **[Google dev kit spurs first-ever agent-on-agent violence](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)** · _source_ · composite 67.1
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped permissions, not tighter…
- **[Breaking Claude Code Opus 5 Auto Mode with indirect prompt injection to code execution](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)** · _Embrace The Red (Johann Rehberger)_ · composite 66.92
  A benign-looking summary request drove a 60-80% code-execution rate against Claude Code Opus 5 Auto Mode, showing classifier 'zero-injection' claims and OS sandboxing are not interchangeable.
- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)** · _source_ · composite 66.5
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel — instrument it or write it out of the trust boundary.
- **[LLM Heist: Hijacking LiteLLM for Traffic Interception, Key Theft, and Tool-Call Injection](https://embracethered.com/blog/posts/2026/hijacking-litellm-for-fun-and-profit/)** · _source_ · composite 66.28
  AI gateways sit downstream of the model, so a proxy-admin credential compromise lets an attacker inject arbitrary tool calls into agent clients without ever touching the model prompt or its provider guardrails.…
- **[The Framing Gap: reframed indirect prompt-injection exfiltration defeats surface-level defenses](https://arxiv.org/abs/2608.27092)** · _arXiv cs.CR_ · composite 65.6
  Don't rely on the acting model to recognize injection; constrain where data can go and isolate the capability that can send it.
- **[Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141)** · _arXiv cs.CR_ · composite 65.0
  Agent safety must accumulate state across the whole loop; per-trajectory monitors that reset each iteration are blind to slow, fragmented attacks.

**📈 Emerging trends**

- **prompt-injection** (🔺 rising) — 22 findings from 11 sources since 2026-04.
- **mcp** (🔺 rising) — 17 findings from 10 sources since 2026-06-30.
- **supply-chain** (🔺 rising) — 13 findings from 10 sources since 2026-06-23.

[→ Full AI Security database](ai-security/README.md)

---

## Product Security

_Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not)._

**🔬 Latest research**

- **[VMs won't contain cyber-capable agents](https://blog.trailofbits.com/)** · _Trail of Bits_ · composite 67.85
  Treat capable AI agents as an advanced persistent threat: isolate them with hardened microVMs, enforce least privilege, monitor actively, and keep host and hypervisor dependencies fully patched.
- **[This Shit is Hard: Patching a vulnerability that has no fix](https://www.chainguard.dev/unchained)** · _Chainguard_ · composite 66.65
  When remediating (including AI-generated) fixes, gate every patch on feasibility, regression testing, and an independent exploit test, batch interdependent fixes, re-validate on each backported version, rebuild from…
- **[CSS the bomb: sanitized webmail CSS steals tokens, keylogs Outlook, and turns Atlas AI browser into an exfil bot](https://portswigger.net/research/css-the-bomb-inside-your-inbox)** · _source_ · composite 66.05
  CSS sanitizers built as feature allow-lists are not a trust boundary; the only durable defense is strict iframe sandboxing plus killing dangerous selectors, select, and free-form image URLs.
- **[What's in a tag name? JavaScript, apparently](https://portswigger.net/research)** · _PortSwigger Research_ · composite 65.15
  Do not rely on WAFs or character blocklists to stop XSS; enforce context-aware output encoding, a strict Content-Security-Policy, and trusted HTML sanitization, since exotic tag-name and DOM-property tricks bypass…
- **[Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](https://snyk.io/blog/)** · _Snyk_ · composite 63.65
  Enforce server-side role/permission checks and key allowlists on every write endpoint (including legacy admin ones), actually validate HMAC signatures, and lock down credentialed CORS, then test for authorization and…
- **[Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/)** · _Unit 42 (Palo Alto Networks)_ · composite 57.02
  Don't over-index on 'AI malware' hype: your existing behavioral/sandbox detection still catches it — but expect faster variant iteration.

**📈 Emerging trends**

- **supply-chain** (🔺 rising) — 17 findings from 12 sources since 2026-06-30.
- **npm** (🔺 rising) — 8 findings from 6 sources since 2026-07-15.
- **provenance** (🔺 rising) — 4 findings from 4 sources since 2026-07-16.

[→ Full Product Security database](product-security/README.md)

---

## AI Research

_Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research._

**🔬 Latest research**

- **[The Frontier AI Vulnerability Burst: Industrializing Autonomous Zero-Day Discovery in Open-Source Software](https://unit42.paloaltonetworks.com/frontier-ai-vulnerability-burst/)** · _source_ · composite 67.62
  Autonomous AI vulnerability discovery moves the mix away from memory-corruption fuzzing (~8%) toward semantic/logic bugs (~92%), and complementarity between models is large enough that an ensemble is a defensive…
- **[When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299)** · _arXiv cs.CR_ · composite 65.6
  How a harness assembles context is a privilege boundary; if it can promote untrusted data, model-side instruction hierarchy provides little protection.
- **[When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057)** · _source_ · composite 61.25
  History reliability is a distinct tool-use bottleneck: harnesses that just accumulate turns are silently letting old, wrong state overwrite the current task.
- **[How Do LLM Agents Actually Get the Flag? Trace-Level Provenance for Agentic Offensive-Security Evaluation](https://arxiv.org/abs/2608.26237)** · _arXiv cs.CR_ · composite 60.8
  Judge security agents on evidence of exploitation in the trace, not on whether the flag string appeared.
- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)** · _source_ · composite 60.5
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better refusal training.
- **[RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439)** · _arXiv cs.CR_ · composite 59.6
  Effective automated red-teaming of agent harnesses should evolve reusable, attributable attack skills rather than replay fixed attacks or full trajectories.

**📈 Emerging trends**

- **arxiv** (🔺 rising) — 76 findings from 2 sources since 2026-08-07.
- **agents** (🔺 rising) — 22 findings from 7 sources since 2026-06.
- **benchmark** (🔺 rising) — 14 findings from 4 sources since 2026-08-07.

[→ Full AI Research database](ai-research/README.md)

---

_Every finding links its original source. Curated by the AwesomeSecurity-AIResearch analyzer; low-confidence or unverified items are held for review and not shown here._

<sub>Generated by scripts/generate_newsletter.py on 2026-08-29.</sub>
