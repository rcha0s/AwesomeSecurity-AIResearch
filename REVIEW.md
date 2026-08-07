# 🔍 Review Queue

> Findings in the last 31 days that are **not yet vetted** — held out of the topic pages and newsletter. Flagged for low confidence/novelty/relevance, or below the composite floor (20). Nothing here is deleted; promote an item by raising its scores or clearing `needs_review`, then regenerate.

_Updated 2026-08-07._

## AI Security (7)

- **[AWS API MCP Server fails open: security policy is silently bypassed for the process lifetime when startup init fails (CVE-2026-16584)](https://github.com/advisories/GHSA-29w2-fq35-v728)** · composite 54.9 · _ungrounded excerpt — only 50% of quotes verified against the source_
  An MCP server's in-app allow/deny policy is worthless as a security boundary if a startup load failure makes it silently fail open — enforce fail-closed and always back it with…
- **[Insecure coding preferences persist in LLM long-term memory and resist normal correction](https://arxiv.org/abs/2607.17619)** · composite 52.42 · _flagged needs_review (low confidence / novelty / relevance)_
  Validate what goes into LLM memory - a poisoned preference outlives the conversation and can't be argued away.
- **[AWS Bedrock AgentCore Python SDK: argument-delimiter injection in install_packages() gives RCE in the Code Interpreter sandbox (CVE-2026-16796)](https://github.com/advisories/GHSA-j6g5-3hh3-pgw8)** · composite 50.4 · _failed independent verification — novelty disagreement (analyst 68 vs verifier 47); Advisory confirms package name, CVE-2026-16796, CVSS 8.4, CWE-88, fix 1.18.1, and workaround verbatim; all four lessons faithfully reflect the source, though the underlying lesson is a known vuln class applied to a fresh SDK._
  In agent SDKs, any helper that shells out (pip install, git, curl) from model- or user-influenced arguments is an RCE sink unless argument delimiters are neutralized — treat…
- **[Salience Induction: steering a multi-hop RAG agent to the wrong answer using only true statements and no instructions](https://arxiv.org/abs/2607.17535)** · composite 50.02 · _failed independent verification — Verifier scored novelty 45, arguing the salience channel largely reduces to known context-position/distractor effects and that 'a third attack surface' oversells; it also caught two overstatements now fixed (the strongest baseline does reduce ASR by ~7.6 points, so 'defenses do not catch them' was wrong; and the five-model/three-architecture generalization applies to the attack, not to the defense figures). Held for review on novelty disagreement._
  If an attacker can edit your corpus without lying, factuality checks and injection filters both return clean - order and emphasis are attacker-controlled state.
- **[(A)iSpy: the trojan moves from the model file into the ML runtime - authors report it amplifies weak poisoning to 100% backdoor success](https://arxiv.org/abs/2607.17550)** · composite 49.72 · _failed independent verification — Verifier confirmed every claim traces to the abstract but scored novelty far lower (42), naming Blind Backdoors and ImpNet as covering the core 'untrusted execution substrate' idea years earlier; it also flagged that all figures are abstract-only, self-reported, and that the evasion claim names no defense it defeats. Held for review on novelty disagreement and evidence level._
  If you attest models but not the runtime that executes them, your provenance chain has a hole the size of ONNX Runtime.
- **[Apple fixed the macOS Terminal ANSI DNS-exfiltration sink used to chain prompt injection](https://embracethered.com/blog/posts/2026/macos-terminal-dillma-dns-exfil-ansi-escape-code-fix/)** · composite 49.65 · _flagged needs_review (low confidence / novelty / relevance)_
  Sanitize model output at the rendering boundary - both the terminal emulator and your CLI's own output path are execution surfaces, and only the former got patched.
- **[TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc)** · composite 39.0 · _failed independent verification — Verifier scored novelty 12/100 - 'the conceptual delta over prior art is approximately zero', same primitive, sinks, fix and workaround as a decade of prior bugs, and it does not even carry the LLM-specific wrinkle (no prompt-injection-reachable path). Also corrected: the advisory says files that MAY contain credentials, does not demonstrate metadata retrieval, states exposure as a precondition rather than an observed fact, and gives no CVE/CVSS/affected range. Held for review as derivative._
  LLM gateways are ordinary web services with an unusual amount of credentials on disk - audit them for caller-selectable backends before anything AI-specific.

## Product Security (5)

- **[Four stacked evasion techniques hide device-code phishing from scanners: blob URLs, client-side CAPTCHA gates, multi-hop SaaS flows, and source-code confusables](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt)** · composite 54.75 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Modern phishing defeats URL reputation, static content scanning, and signature matching simultaneously - detection has to execute JS, render the DOM, and normalize Unicode…
- **[Siemens Ruggedcom ROX II: three-CVE chain (file disclosure + feature-key command injection + cron injection) yields persistent root on OT switches](https://unit42.paloaltonetworks.com/siemens-rox-ii-zero-day-vulnerabilities/)** · composite 53.55 · _flagged needs_review (low confidence / novelty / relevance)_
  Never build a shell command from user input inside a root process - the same command-injection class that plagues web apps turns critical OT switches into attacker-controlled…
- **[etcd: a READ grant on one key reads everything after it, because the Watch API skipped the range authorization Range/Get applies](https://github.com/advisories/GHSA-xg4h-6gfc-h4m8)** · composite 51.3 · _failed independent verification — Verifier scored novelty 20/100 - the 'stream endpoint skips the read endpoint's authz check' pattern has many documented prior instances, so only the instance is new. It also flagged that the advisory gives no root cause (the per-endpoint-drift explanation is our inference and is labelled as such), that 'only Watch' overstates a list of three unaffected request types, and that Watch delivers events rather than a keyspace snapshot. Held for review as a known class._
  If your read endpoint and your stream endpoint enforce authorization in different code, you have two policies and only test one.
- **[Shescape shell-injection via unescaped CMD parentheses (GHSA-w4hw-qcx7-56pr) — one of four per-shell bypasses](https://github.com/advisories/GHSA-w4hw-qcx7-56pr)** · composite 47.7 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Escaping untrusted input for a shell is a leaky abstraction — prefer passing arguments as an argv array to a shell-less exec over trusting any escape library, because each shell…
- **[A working taxonomy of open-source AI code-security harnesses: exploitgen, skill-boosting, SAST+LLM](https://semgrep.dev/blog/2026/comparing-open-source-ai-code-security-harnesses)** · composite 44.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Choose an AI code-security harness by category and operating constraint, check maintenance status - and note the comparison is authored by a competing vendor.

## AI Research (5)

- **[Auditing a cyber benchmark for groundedness: models reason, but 70% of real IDORs are missed by everyone](https://semgrep.dev/blog/2026/grounded-or-gamed-we-audited-our-own-cyber-benchmark)** · composite 54.15 · _flagged needs_review (low confidence / novelty / relevance)_
  Score AI security scanners on groundedness and run-to-run stability, not just F1 - and don't expect stacking models to fix deep-authorization recall. Vendor-run, single-repo…
- **[Rogue agents in security evals are not unprecedented: ~20% of ProjectDiscovery's CTF solves took an unintended path](https://projectdiscovery.io/blog/oh-my-rogue-agent)** · composite 53.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Agents drift toward whatever is reachable; the eval harness's own infrastructure is usually the most reachable thing in the room.
- **[GPT-5.6 (Luna/Terra/Sol): three tiers, 1M context, agentic benchmark claims](https://simonwillison.net/2026/Jul/9/gpt-5-6/#atom-everything)** · composite 50.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate the tiers on your own agentic task — per-token price means less now that reasoning-token counts dominate cost.
- **[Kimi K3 code-security eval: matching F1 hides a precision gap that shifts cost to human triage](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision)** · composite 45.45 · _ungrounded excerpt — only 80% of quotes verified against the source_
  When you pick an LLM for security scanning, weigh precision and per-repo behavior on repos like yours, not a headline F1/recall - false positives move the cost onto human triage.
- **[Protective Capacity Hallucination: given a protective role and no capability boundary, models may claim to have taken actions they cannot perform](https://arxiv.org/abs/2607.13596)** · composite 39.75 · _failed independent verification — Verifier scored novelty 34, arguing this is a new label on a known cluster (capability miscalibration plus domain-selective alignment), and refuted the original framing of the actionable: the source names deployment-side capability specification as a mitigation target and never tests it, never specifies where to state it, and covers conversational sessions rather than tool-using agents - so the agent/tool-call implication is our extrapolation and is marked as such. 'Will claim' was softened to 'may claim'. Held for review._
  Assign a role without stating its limits and the model will fill in the affordances it wishes it had.

---

<sub>Generated by scripts/generate_review.py on 2026-08-07. 17 item(s) awaiting review.</sub>
