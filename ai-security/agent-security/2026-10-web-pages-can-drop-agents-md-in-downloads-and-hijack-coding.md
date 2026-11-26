# Web pages can drop AGENTS.md in ~/Downloads and hijack coding agents

**Published:** Oct 25, 2026

> **Takeaway:** The agent's working directory is its trust boundary for instructions, so any folder the web can write to, like ~/Downloads, works as a drive-by prompt-injection drop zone that vendors won't patch.

## TL;DR

Forever Security found a malicious AGENTS.md in a customer's ~/Downloads folder, which was also the coding agent's working directory. The file made the agent try to install the rogue npm package 'function-color'. Browsers like Chrome, Edge and Firefox save downloads to ~/Downloads without asking, so a web page can plant an instruction file there. Agents then auto-load it as trusted project instructions. In the researchers' tests a harmless Codex payload ran 90% of the time, and a malicious CLAUDE.md redirected Claude Code's API traffic to an attacker server, leaking its OAuth token and getting code executed in about 50% of runs.

## Lessons

- Agents auto-load instruction files from their working directory and treat them as authoritative, so whoever can write a file there controls the agent. - _"Agents automatically load applicable files from their working directory and use the contained instructions to guide their actions."_
- ~/Downloads is a uniquely dangerous working directory because browsers write to it without asking, so the attack needs no repo access. - _"~/Downloads is special. It is the one folder the web can write to on its own"_
- This is intended behavior working as designed, not a vendor bug. Defense falls on scoping where agents run. - _"There is nothing here for OpenAI or Anthropic to patch."_
- The exposure is real in practice. Telemetry shows many agent sessions started from Downloads. - _"Claude Code alone launched more than 1,300 sessions from that location"_

## Threat · Conditions · Mitigations

- **Threat:** A web page silently downloads a malicious AGENTS.md/CLAUDE.md into ~/Downloads. A coding agent later launched there follows its instructions to install malicious npm packages, run code, or redirect API traffic to steal OAuth tokens.
- **Conditions:** The browser auto-saves downloads to ~/Downloads without a prompt (default in Chrome/Edge/Firefox). The user launches Claude Code, Codex, Cursor CLI or similar with ~/Downloads as the working directory. Instruction files are auto-loaded without review.
- **Mitigations:** Launch agents only from the specific project root. Never use ~/Downloads or $HOME as the working directory. Review unfamiliar AGENTS.md/CLAUDE.md before letting the agent follow them. Keep approval prompts and sandboxing enabled. Enable browser 'ask where to save' prompts. Test untrusted code in an isolated environment.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 4 · Novelty 55 · Relevance 88 · Credibility 60 · **Composite 53** _(each 0-100)_  
**Tags:** `agents-md`, `claude-md`, `instruction-files`, `coding-agents`, `indirect-prompt-injection`, `drive-by-download`, `npm`, `oauth-token-theft`, `working-directory`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The pool already has repo-borne instruction-file injection (TrojanBench-style poisoned repos and the 'rules-file / AGENTS.md backdoors' noted in ai-security.json), the SSMS Copilot CVE where db_owner-written AGENTS.md properties escalate privilege, and harness-config scanners that flag CLAUDE.md as persistent prompt injection. What's new here is the delivery vector: no repo or DB write access is needed, because a browser drive-by download into ~/Downloads is enough. The report also includes an in-the-wild observation, telemetry on how common Downloads-as-cwd is, and a CLAUDE.md API-redirect variant that steals OAuth tokens.

_Source: [https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/)_  ·  [← back to index](../README.md)
