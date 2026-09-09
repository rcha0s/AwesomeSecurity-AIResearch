# Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path

**Published:** Aug 28, 2026

> **Takeaway:** A model's safety refusal to run an untrusted binary is not automatically safe if the 'safe' alternative it chooses (writing its own code to parse the untrusted data) is itself exploitable - containment has to hold at the OS/network layer, because the model's own good-faith safety decisions can become an attacker's exploit path.

## TL;DR

Security researcher Johann Rehberger (wunderwuzzi) showed that Claude Code running Opus 5 in Auto Mode can be tricked into remote code execution 60-80% of the time simply by being asked to summarize a malicious website. The chain relies on a WebFetch failure forcing a curl fallback, a 303 redirect to a booby-trapped archive, Claude's own safety-motivated decision to write a custom decoder (rather than run the supplied binary) becoming the exploit trigger via Python module shadowing, and can spawn a fully separate nested `claude -p` agent with its own tool access.

## What to learn

- Claude refused, per its safety guardrails, to run the attacker-supplied binary decoder - but its fallback decision to write its own decoder script was itself the exploit path, since the attacker had planted a malicious struct.py file for Python's import-shadowing behavior to intercept. - _"Claude, per its safety guardrails, refuses to run the decoder: “This is planned and what the attacker wants,” Rehberger wrote. Instead of using the supplied binary, the AI decides to write its own decoder. “Ironically, that safety decision is the exploit path,” Rehberger explained"_
- The exploit uses Python module shadowing: a malicious local struct.py file (imported transitively by the standard base64 module) shadows the real standard-library struct module, so Claude's own generated code unknowingly executes attacker code. - _"Module shadowing occurs when a local file shares the same name as a Python standard-library module. The local file hides the official module, causing Python to load it instead. In this case, the standard-library base64 module imports the legitimate struct module, and the malicious ZIP contains a malicious file with the same name."_
- The compromise can spawn a fully separate, nested Claude Code agent (via `claude -p`) with its own independent tool access and context, which then performed reconnaissance and wrote to the local filesystem on its own. - _"struct.py launches a second, headless Claude Code via claude -p, meaning this prompt injection can be used not just to remotely execute code, but rather to create a whole new agent. “The nested Claude gets its own tool access and context,” Rehberger wrote."_
- Anthropic's stated position is that this is expected behavior for a convenience feature, not a security guarantee, and the real containment boundary is OS-level sandboxing and network egress control, not the model's own judgment. - _"“Auto Mode is a convenience feature backed by a best-effort classifier, not a security guarantee,” Rehberger wrote, paraphrasing Anthropic’s response to his security report. According to Rehberger, the classifier isn’t built to stop determined prompt-injection chains made up of individually benign-looking steps, and the real boundary is OS isolation and network egress control."_

## Threat · Conditions · Mitigations

- **Threat:** Indirect prompt injection from untrusted web content leading to code execution in an autonomous coding agent.
- **Conditions:** Developers running Claude Code Opus 5 in Auto Mode (now default) that processes untrusted external content without OS sandboxing.
- **Mitigations:** Container/VM sandbox, egress restrictions, remove sensitive credentials from runtime, explicit deny rules on process creation, monitoring.

---

**Topic:** AI Security  ·  **Domain:** Prompt Injection  
**Source:** [Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 11 · Novelty 75 · Relevance 88 · Credibility 50 · **Composite 59.15**  
**Tags:** `claude-code`, `prompt-injection`, `sandbox-escape`, `python`, `module-shadowing`, `auto-mode`  
**Verification:** ✓ independently verified · closest prior art: Rehberger's own prior Claude Code prompt-injection/exfiltration research plus long-documented Python import-shadowing attacks; the new specificity is chaining a safety-refusal fallback into the shadowing RCE and spawning a nested agent.

_Source: [https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)_  ·  [← back to index](../README.md)
