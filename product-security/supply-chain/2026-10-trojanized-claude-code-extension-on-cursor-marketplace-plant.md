# Trojanized Claude Code extension on Cursor Marketplace plants persistent SSH backdoor

**Published:** Oct 30, 2026

> **Takeaway:** An AI coding-assistant extension from the official vendor, served by an editor marketplace, ran with full user rights when loaded, so hunt for integrated development environment (IDE) extension hosts writing to ~/.ssh and LaunchAgents and do not treat uninstalling as remediation.

## TL;DR

Phorion found that Claude Code for VS Code version 2.1.313 on the Cursor Marketplace carried injected code. The code runs as soon as the extension file loads, appends an attacker key to ~/.ssh/authorized_keys and opens a reverse SSH tunnel to 134.209.82.225. It also sets up persistence on macOS, Linux and Windows and sends a report on the host back to the operator. That report includes the names, but not the values, of environment variables that look like secrets. A bug in the macOS check often stops it from turning on SSH, but the key and persistence still get installed, and removing the extension does not remove them.

## Lessons

- The payload is an immediately invoked function prepended to extension.js. It runs when Node loads the module, before activate(), and needs no user action. - _"executes as soon as Node loads the file, before the extension’s normal `activate` callback even runs"_
- Rules that only watch processes miss this, because the key is written with Node's fs API rather than shell tools. Defenders need file telemetry that flags IDE helper processes writing to authorized_keys. - _"process-only rules watching for shell commands like `echo` or `tee` touching `authorized_keys` won’t catch it"_
- Hunt by key fingerprint, not by the 'svc-telemetry' comment, because the malware itself only checks the comment string. - _"When hunting for this activity, it’s worth checking the public-key fingerprint rather than relying solely on the comment string."_
- Uninstalling the extension does not clean up. Responders must kill the tunnel loop, remove the LaunchAgent, cron or scheduled-task persistence, remove the planted key and rotate credentials. - _"uninstalling the extension alone won’t remove the backdoor"_

## Threat · Conditions · Mitigations

- **Threat:** A backdoored official Claude Code extension bundle (2.1.313) on the Cursor Marketplace runs a payload when the module loads. The payload plants an attacker SSH key, opens a reverse SSH tunnel to 134.209.82.225 for interactive access, persists through a LaunchAgent, cron job or scheduled task, and reports host details and the names of secret-looking environment variables.
- **Conditions:** A developer installs or auto-updates to Claude Code for VS Code 2.1.313 from the Cursor Marketplace. Full inbound access on macOS also needs Remote Login (SSH) to be already on or turned on later, or passwordless sudo.
- **Mitigations:** Find and remove 2.1.313. Kill the tunnel processes. Remove com.apple.sysmond.plist, the @reboot cron entry or the SysMon task and Startup script, and the ~/.config/.smt, .smtk and /tmp/.stk_* files. Remove the svc-telemetry key and confirm Remote Login is off. Rotate credentials if SSH was on or an inbound login appears. Alert on IDE extension hosts modifying ~/.ssh.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [@_chall via Hacker News](https://phorion.io/blog/offical-claude-code-vsx-compromise/)  ·  **Author:** _chall  ·  **Retrieved:** 2026-10-30  
**Scores:** Newness 19 · Novelty 55 · Relevance 88 · Credibility 75 · **Composite 59** _(each 0-100)_  
**Tags:** `supply-chain`, `ide-extension`, `cursor`, `open-vsx`, `claude-code`, `ssh-backdoor`, `reverse-tunnel`, `macos-persistence`, `incident-response`  
**Also reported by:** [Socket](https://socket.dev/blog/claude-code-extension-compromise?utm_medium=feed), [StepSecurity](https://www.stepsecurity.io/blog/claude-code-extension-trojanized), [The Register - Security](https://www.theregister.com/cyber-crime/2026/10/30/anthropic-that-claude-code-extension-compromise-couldnt-be-us/5306682), [BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-claude-code-extension-on-cursor-planted-ssh-backdoors/), [The Hacker News](https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html) _(+5 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The nearest pool entries are archive 'Cursor's VS Code import drops extension versions and installs latest' (Open VSX identity and versions), archive 'Markdown Preview Enhanced, a VS Code extension, chained flaws into RCE' and product-security 'OVHcloud CLI GitHub releases carried attacker binaries ... GlassWorm'. None covers a trojanized official AI coding-assistant extension with this kind of detection detail.

_Source: [https://phorion.io/blog/offical-claude-code-vsx-compromise/](https://phorion.io/blog/offical-claude-code-vsx-compromise/)_  ·  [← back to index](../README.md)
