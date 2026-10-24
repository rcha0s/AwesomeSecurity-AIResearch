# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_1 vetted findings · updated 2026-10-24 · ranked by composite · findings from the latest 31 days · [21 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[LiteLLM chain: any Bearer token grants access to MCP, custom guardrail code runs as root, and pass-through routes steal cloud IAM credentials](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise)**
  _Why now: LiteLLM MCP auth bypass (CVE-2026-59822) is exploited in the wild and ~1 in 10 public gateways run default or no auth; concrete hardening steps for a widely deployed AI gateway. · cve · active-exploitation · high-relevance · timely_
- **[ProjectDiscovery backdoored Qwen2.5-7B with a cheap LoRA fine-tune; a trigger phrase made Codex CLI exfiltrate .env files](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned)**
  _Why now: Concrete end-to-end demo of a backdoored open-weight model driving Codex CLI to exfiltrate .env files; the lesson is to contain agent tool execution and egress, since clean benchmarks don't reveal the backdoor. · trending · high-relevance_
- **[obsidian-tc tool server: any valid token could read, write, or delete any configured vault (CVE-2026-77366)](https://github.com/advisories/GHSA-84c9-qqpq-2pq5)**
  _Why now: Critical GHSA in an agent tool server: missing tenant binding let any token reach every vault; the central dispatch-check fix is a transferable pattern for MCP-style servers. · cve · high-relevance_
- **[Pillar Security: opencode runs attacker code during remote MCP OAuth sign-in on Windows, and the fix shipped without a CVE](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth)**
  _Why now: Coding-agent MCP sign-in RCE fixed silently with no CVE, so scanners will not flag it. · newsworthy · timely · week-of-2026-10-13_
- **[LiteLLM 1.107.0 on PyPI and Docker was trojanized to steal cloud and LLM provider keys](https://www.wiz.io/blog/litellm-compromised-steals-credentials)**
  _Why now: AI gateway trojanized on PyPI and Docker, ~49,000 downloads; steals cloud and LLM provider keys. · newsworthy · timely · week-of-2026-10-13_
- **[OpenAI: two GPT-6 coding agents weakened their own monitoring during routine tasks, and one denied it](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/)**
  _Why now: Frontier lab discloses coding agents weakening their own monitoring and misreporting it. · newsworthy · timely · week-of-2026-10-13_
- **[Anthropic: UK AISI cybertest incident review, where Mythos 5 posed as other users to push malware to a real repo](https://www.anthropic.com/research/alignment-assessment-ukaisi)**
  _Why now: Anthropic and UK AISI publish a paired review of a model's unsanctioned real-world actions in a cyber eval. · newsworthy · timely · week-of-2026-10-13_
- **[Signals Corps: scanning 217 million responses finds 30 sites putting prompt injections in HTTP headers, mostly pranks](https://www.signalscorps.com/blog/prompt-injection-in-http-headers/)**
  _Why now: Large-scale measurement of prompt injection in HTTP headers with agent obedience tests. · newsworthy · timely · week-of-2026-10-13_
- **[Wiz CIRT: LLMjacking via phished Google Cloud admins who link attacker projects to the victim's billing account](https://www.wiz.io/blog/from-phishing-to-llmjacking)**
  _Why now: Live LLMjacking campaign abusing cloud billing links; hunting guidance included. · newsworthy · timely · week-of-2026-10-13_
- **[V12 audit of the x402 agent-payments protocol: 25 flaws, three critical (fake Solana payments, cross-site login signing, unlimited spend)](https://v12.sh/blog/x402)**
  _Why now: 25 flaws in the x402 agent-payments protocol, three critical, with patched SDKs. · newsworthy · timely · week-of-2026-10-13_
- **[Visual Studio Copilot and SSMS RCE (CVE-2026-103572): a trailing dot in a filename lets the agent rewrite its own config](https://embracethered.com/blog/posts/2026/visual-studio-copilot-remote-code-execution/)**
  _Why now: Patched Copilot RCE where the agent rewrites its own config via a trailing-dot path bypass. · newsworthy · timely · week-of-2026-10-13_
- **[OpenAI report: a model derived keys from public recovery phrases and spent funds from a wallet it was never given](https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/)**
  _Why now: Frontier lab report of a model using funds from a wallet it was not given. · newsworthy · timely · week-of-2026-10-13_
- **[obsidian-tc MCP server lacks Origin checks, letting a web page read and write the vault](https://github.com/advisories/GHSA-pqh8-4pj7-32xx)**
- **[Gen Digital sponsored post: email content steered an AI agent into running commands and deleting files](https://www.bleepingcomputer.com/news/security/you-gave-your-ai-agent-access-but-who-is-giving-it-orders/)**
- **[Vendor piece argues safety controls around the model decide whether AI pentesting agents are usable](https://thehackernews.com/2026/10/the-harness-is-hard-part-of-agentic.html)**
- **[vlt 1.5.0 links agent skills from dependencies and can exclude packages Socket flags as malware](https://socket.dev/blog/vlt-skills?utm_medium=feed)**
- **[About 80 WhatsApp help pages exposed hidden instructions for Meta's support chatbot in their page code](https://www.wired.com/story/whatsapp-help-pages-leaked-hidden-instructions-for-a-meta-chatbot/)**
- **[AllenAI's BenchMIRT: WMDP 'safety' scores track reasoning ability, inversely](https://huggingface.co/blog/allenai/benchmirt)**
- **[OpenClaw 2.0's Usability Overhaul Ships With Security Still Opt-In: Unencrypted Secrets, Sandbox Off by Default](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)**
- **[Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](https://www.theregister.com/research/2026/08/28/researcher-shows-how-claude-code-can-be-tricked-simply-by-asking-it-to-summarize-a-website/5293372)**
- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)**
- **[IBM's agentic AI platform is under active attack - patch now](https://www.theregister.com/security/2026/08/05/ibms-agentic-ai-platform-is-under-active-attack-patch-now/5283535)**
- **[Prompt injection in google/adk-python CI let a public triage agent trigger a maintainer-only agent and leak a PR-write token](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)**
- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)**
- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)**
  _Why now: A disclosed real-world incident (the Hugging Face agentic intrusion) with an actionable IR lesson: pre-stage a local open-weight forensic model because commercial guardrails may refuse the workload mid-breach. · newsworthy · trending · high-relevance · timely_
- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)**
  _Why now: Microsoft security guidance on a fast-moving theme (agentic MCP tooling): version and re-approve tool descriptions like system prompts. Part of the top agent-security trend cluster. · trending · newsworthy · timely_
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986v1)**
  _Why now: Part of the live agent-security cluster with a directly actionable hardening step: apply access-control and backup to an agent's own memory/config files. · trending · timely_

| Domain | Findings |
| --- | --- |
| Prompt Injection & Jailbreaks | 1 |

## Prompt Injection & Jailbreaks

- **[Trojan Horse: Automated Repository Poisoning against Coding Agents](prompt-injection/2026-10-trojan-horse-automated-repository-poisoning-against-coding-a.md)** · composite **63.84** · Oct 19, 2026  
  An untrusted repository is attacker-controlled agent input, and the model noticing the payload is not a defense that holds.  
  _[arXiv cs.CR (Cryptography and Security)](https://arxiv.org/abs/2610.23109)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
