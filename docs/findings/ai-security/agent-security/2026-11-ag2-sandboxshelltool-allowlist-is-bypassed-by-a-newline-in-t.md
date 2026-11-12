# AG2 SandboxShellTool allowlist is bypassed by a newline in the command

**Published:** Nov 10, 2026

> **Takeaway:** Upgrade AG2 past the fix, and treat any agent shell allowlist that passes commands to sh -c as a denylist that will miss some separator.

## TL;DR

AG2's SandboxShellTool checks allowed=[...] and readonly=True commands against a denylist of shell operators that omits newline and carriage return, then runs the raw string through sh -c, where a newline acts like a semicolon. A command such as 'cat file\nrm -rf ...' passes both the prefix check and the operator check, and with the default LocalEnvironment() backend the second statement runs on the host, not in a container. The advisory (GHSA-2h4w-29cv-2cmv, CVE-2026-113663, rated HIGH, affects pip packages ag2 and autogen) was tested on ag2 1.0.5 and links a fix commit and the v1.1.1 release.

## Lessons

- A filter that lists shell operators but passes the string to a shell can be bypassed by any separator missing from the list. Here, that separator is the newline. - _"The filter only inspects a single-line set of shell metacharacters, but execution runs the raw string through"_
- The bypass can be reached through indirect prompt injection: the model writes tool arguments from content the agent reads. - _"Because tool arguments are LLM-generated and can be steered by content the agent processes"_
- The robust fix is to drop the shell in restricted mode (split the arguments and execute directly) so every separator is inert by construction. - _"execute allowlisted/readonly commands without invoking a shell in restricted mode"_
- A tool named 'sandbox' may not isolate anything: the default backend runs commands as host subprocesses. - _"With the default LocalEnvironment() backend, this is command execution on the host process running the agent, not confined to a container."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker who can put text in front of an AG2 agent (fetched document, tool output) steers it into a newline-joined command that runs arbitrary shell commands on the host despite allowed=[...] or readonly=True.
- **Conditions:** AG2 SandboxShellTool configured with allowed=[...] or readonly=True, on a version before the fix; the default LocalEnvironment() backend makes the impact host command execution.
- **Mitigations:** Upgrade to the fixed AG2 release (the advisory links v1.1.1), run restricted commands without a shell wrapper, add newline and carriage return to any remaining operator denylist, and run the tool in a real container or microVM backend.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-2h4w-29cv-2cmv)  ·  **Retrieved:** 2026-11-10  
**Scores:** Newness 52 · Novelty 35 · Relevance 78 · Credibility 70 · **Composite 57** _(each 0-100)_  
**Tags:** `command-injection`, `agent-tools`, `allowlist-bypass`, `prompt-injection`, `ag2`, `sandbox`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: CVE-2026-109428, the Mistral Vibe allowlist bypass via backslash-newline; Shescape per-shell bypasses.

_Source: [https://github.com/advisories/GHSA-2h4w-29cv-2cmv](https://github.com/advisories/GHSA-2h4w-29cv-2cmv)_  ·  [← back to index](../README.md)
