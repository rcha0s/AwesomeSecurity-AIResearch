# 🔍 Review Queue

> Findings in the last 31 days that are **not yet vetted** — held out of the topic pages and newsletter. Flagged for low confidence/novelty/relevance, or below the composite floor (20). Nothing here is deleted; promote an item by raising its scores or clearing `needs_review`, then regenerate.

_Updated 2026-07-26._

## AI Security (8)

- **[AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728)** · composite 58.15 · _ungrounded excerpt — only 50% of quotes verified against the source_
  An MCP server's in-app allow/deny policy is worthless as a security boundary if a startup load failure makes it silently fail open — enforce fail-closed and always back it with…
- **[Provider safety guardrails blocked incident response during the Hugging Face agentic intrusion](https://embracethered.com/blog/posts/2026/ai-intrusion-are-now-real/)** · composite 58.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Assume your commercial AI provider may refuse to help you during a breach - pre-stage a local open-weight forensic model the same way you pre-stage backups.
- **[Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619)** · composite 55.67 · _flagged needs_review (low confidence / novelty / relevance)_
  Validate what goes into LLM memory - a poisoned preference outlives the conversation and can't be argued away.
- **[AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8)** · composite 53.65 · _failed independent verification — novelty disagreement (analyst 68 vs verifier 47); Advisory confirms package name, CVE-2026-16796, CVSS 8.4, CWE-88, fix 1.18.1, and workaround verbatim; all four lessons faithfully reflect the source, though the underlying lesson is a known vuln class applied to a fresh SDK._
  In agent SDKs, any helper that shells out (pip install, git, curl) from model- or user-influenced arguments is an RCE sink unless argument delimiters are neutralized — treat…
- **[Apple fixed the macOS Terminal ANSI DNS-exfiltration sink used to chain prompt injection](https://embracethered.com/blog/posts/2026/macos-terminal-dillma-dns-exfil-ansi-escape-code-fix/)** · composite 52.9 · _flagged needs_review (low confidence / novelty / relevance)_
  Sanitize model output at the rendering boundary - both the terminal emulator and your CLI's own output path are execution surfaces, and only the former got patched.
- **[Treat MCP tool descriptions as system prompts: silent re-trust poisoning](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)** · composite 52.7 · _flagged needs_review (low confidence / novelty / relevance)_
  Version and change-review every MCP tool description as if it were a system prompt, and force re-approval whenever tool metadata changes.
- **[Self-state attacks: corrupting an agent's own memory and config uses legitimate syscalls](https://arxiv.org/abs/2607.17986)** · composite 52.38 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat an agent's memory and config files as protected assets with their own access-control and backup policy - once an attacker can write them, the corruption step itself looks…
- **[TOCTOU race condition in computer-use agents: the screen changes between screenshot and click](https://embracethered.com/blog/posts/2026/toctou-agent-what-you-click-is-not-what-you-get/)** · composite 52.1 · _ungrounded excerpt — only 80% of quotes verified against the source_
  A computer-use agent that clicks coordinates it decided on seconds ago is exploitable by TOCTOU: re-check the UI at action time, because what the model saw is not necessarily what…

## Product Security (6)

- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)** · composite 58.38 · _flagged needs_review (low confidence / novelty / relevance)_
  Gate agent PRs with automated secret and dependency-integrity checks - human review demonstrably does not catch this class, and the humans are introducing most of it.
- **[Four stacked evasion techniques hide device-code phishing from scanners: blob URLs, client-side CAPTCHA gates, multi-hop SaaS flows, and source-code confusables](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt)** · composite 58.0 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Modern phishing defeats URL reputation, static content scanning, and signature matching simultaneously - detection has to execute JS, render the DOM, and normalize Unicode…
- **[Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/)** · composite 56.8 · _flagged needs_review (low confidence / novelty / relevance)_
  Never build a shell command from user input inside a root process - the same command-injection class that plagues web apps turns critical OT switches into attacker-controlled…
- **[Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr)** · composite 50.95 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Escaping untrusted input for a shell is a leaky abstraction — prefer passing arguments as an argv array to a shell-less exec over trusting any escape library, because each shell…
- **[A working taxonomy of open-source AI code-security harnesses: exploitgen, skill-boosting, SAST+LLM](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses)** · composite 47.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Choose an AI code-security harness by category and operating constraint, check maintenance status - and note the comparison is authored by a competing vendor.
- **[@redhat-cloud-services npm namespace compromise (32+ packages)](https://access.redhat.com/security/vulnerabilities/RHSB-2026-006)** · composite 8.75 · _not yet scored (no novelty/relevance — needs analysis)_
  Attackers compromised at least 32 packages under the @redhat-cloud-services scope, bypassing code review to push a payload dubbed Miasma.

## AI Research (3)

- **[Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark)** · composite 57.4 · _flagged needs_review (low confidence / novelty / relevance)_
  Score AI security scanners on groundedness and run-to-run stability, not just F1 - and don't expect stacking models to fix deep-authorization recall. Vendor-run, single-repo…
- **[GPT-5.6 (Luna/Terra/Sol): three tiers, 1M context, agentic benchmark claims](https://simonwillison.net/2026/Jul/9/gpt-5-6/#atom-everything)** · composite 53.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate the tiers on your own agentic task — per-token price means less now that reasoning-token counts dominate cost.
- **[Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision)** · composite 48.7 · _ungrounded excerpt — only 80% of quotes verified against the source_
  When you pick an LLM for security scanning, weigh precision and per-repo behavior on repos like yours, not a headline F1/recall - false positives move the cost onto human triage.

---

<sub>Generated by scripts/generate_review.py on 2026-07-26. 17 item(s) awaiting review.</sub>
