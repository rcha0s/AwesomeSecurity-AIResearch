# Microsoft dissects the SSH backdoor in a trojanized Claude Code extension

**Published:** Oct 31, 2026

> **Takeaway:** Uninstalling the extension does not clean the machine: hunt for the svc-telemetry key and the disguised startup entries on every developer machine that took the update.

## TL;DR

Tampered builds 2.1.312 and 2.1.313 of the anthropic.claude-code extension were served from Cursor's extension marketplace on October 29, 2026, from about 2:27 AM to 1:35 PM Pacific time. Microsoft says the Visual Studio Marketplace and the npm package were not affected. The injected loader runs when the extension loads, adds an attacker SSH key tagged svc-telemetry, opens a reverse SSH tunnel and installs startup persistence named like SysMon or com.apple.sysmond.

## Lessons

- The payload runs as soon as the extension module loads, before the extension's own code, and tries to plant an SSH key, enable SSH, open a reverse tunnel, persist and report the host. - _"The injected loader runs when the extension module loads and attempts to add an attacker-controlled Secure Shell (SSH) key, enable the local SSH service, establish reverse SSH forwarding, configure persistence, and report host details."_
- Removing or updating the extension leaves the backdoor in place; keys, tunnel identities, scripts and startup entries must be removed separately. - _"Removing or updating the extension does not remove artifacts written outside its installation directory."_
- The loader reports only the names of secret-looking environment variables, not their values, so the report alone shows reconnaissance, not proven secret theft. - _"The callback sends matching environment-variable names, not values."_
- The tunnel starts with an outbound connection from the workstation instead of waiting for an inbound one, so egress monitoring matters as much as inbound rules. - _"This design starts with an outbound connection from the workstation rather than waiting for a direct inbound connection to it."_
- Microsoft points Cursor users to a publisher allowlist and an install cooldown to limit exposure to newly published malicious versions. - _"including restricting extensions to approved publishers and configuring an extension installation cooldown to delay installation of newly published versions"_

## Threat · Conditions · Mitigations

- **Threat:** A trojanized auto-updating editor extension runs attacker JavaScript at load time on developer machines and installs a persistent reverse SSH backdoor.
- **Conditions:** The machine installed or auto-updated anthropic.claude-code 2.1.312 or 2.1.313 from the Cursor marketplace during the October 29 window; remote access also depends on host privileges and SSH configuration.
- **Mitigations:** Check authorized_keys for the svc-telemetry key, remove the com.apple.sysmond LaunchAgent, the @reboot crontab entry, the SysMon task and Startup sysmon.cmd and the .smt, .smtk and .stk_ files after preserving evidence, look for connections to 134.209.82.225, rotate credentials where telemetry shows exposure, and set a publisher allowlist and install cooldown for editor extensions.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/10/30/inside-malicious-claude-code-branded-cursor-extension-persistent-ssh-backdoor/)  ·  **Retrieved:** 2026-11-01  
**Scores:** Newness 14 · Novelty 22 · Relevance 80 · Credibility 91 · **Composite 48** _(each 0-100)_  
**Tags:** `ide-extension`, `supply-chain`, `cursor`, `claude-code`, `ssh-backdoor`, `persistence`, `developer-workstation`  
**Also reported by:** [Wired Security](https://www.wired.com/story/trojan-malware-targets-thousands-of-anthropic-claude-developer-systems/), [DoublePulsar (Kevin Beaumont)](https://doublepulsar.com/anthropic-hacked-to-deliver-remote-access-trojan-to-claude-developer-laptops-worldwide-1148a92baae2?source=rss----8343faddf0ec---4), [Ars Technica Security](https://arstechnica.com/security/2026/10/anthropic-vs-code-extension-on-cursor-backdoored-for-nearly-12-hours/), [The Register - Security](https://www.theregister.com/cyber-crime/2026/10/30/anthropic-that-claude-code-extension-compromise-couldnt-be-us/5306682), [BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-claude-code-extension-on-cursor-planted-ssh-backdoors/) _(+5 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier tracker story on the same incident from a Hacker News report (s-bf5aaab63512); earlier malicious VS Code and Open VSX extension campaigns such as GlassWorm and the 2025 fake Solidity extensions on Open VSX.

_Source: [https://www.microsoft.com/en-us/security/blog/2026/10/30/inside-malicious-claude-code-branded-cursor-extension-persistent-ssh-backdoor/](https://www.microsoft.com/en-us/security/blog/2026/10/30/inside-malicious-claude-code-branded-cursor-extension-persistent-ssh-backdoor/)_  ·  [← back to index](../README.md)
