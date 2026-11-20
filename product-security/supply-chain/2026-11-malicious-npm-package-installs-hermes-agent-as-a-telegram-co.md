# Malicious npm package installs Hermes Agent as a Telegram-controlled backdoor

**Published:** Nov 19, 2026

> **Takeaway:** A malicious package can drop a legitimate AI agent as the implant, so treat unexpected agent installs and agent services as compromise signals.

## TL;DR

The npm package @leadstack/crm-connect posed as a CRM client and, on install, set up Hermes Agent, an open-source agent that can run shell commands, edit files and drive a browser. It fetched the agent's keys and instructions from the attacker's server, connected it to an attacker-run Telegram bot, and registered it as a systemd service renamed to look like a CRM daemon. SafeDep says the account published nine versions on 16 November 2026 and the package has been removed, though the publisher is still active.

## Lessons

- The implant is a real open-source agent, not custom malware, so tool allowlists and signature checks may miss it. - _"On install it set up Hermes Agent, an open-source agent from Nous Research that can run shell commands, edit files and drive a browser."_
- The agent's default approval prompts do not help when the attacker controls the chat that approves them. - _"Commands that Hermes treats as dangerous wait for approval in the chat. By default, any member allowed into the chat can approve them, and the attacker is that member."_
- The publisher changed the trigger across versions, moving from install-time scripts to code that runs when the library is used, so blocking install scripts alone is not enough. - _"From 1.0.19 on, the tarball holds no agent code. It runs code fetched at install or run time, with the full environment of the process that loaded it."_
- Running npm install as root gives the implant root; the agent needed an explicit flag to be installed as a root service. - _"Hermes Agent does not install its gateway as a root service by default."_

## Threat · Conditions · Mitigations

- **Threat:** A package disguised as a CRM client installs a general-purpose AI agent with shell, file, browser and scheduling tools and hands control to the attacker over Telegram. Later versions download and run code or a binary with the install environment.
- **Conditions:** Victim installs @leadstack/crm-connect versions 1.0.15, 1.0.18 to 1.0.21, 1.0.29, 1.0.30, 1.1.0 or 1.1.1. The agent runs as root when npm install runs as root; version 1.0.18 falls back to a user service with linger. SafeDep did not recover the attacker's .env or SOUL.md, so exact permissions of the Telegram control are not confirmed.
- **Mitigations:** Block or review install scripts and unexpected new dependencies, avoid running npm install as root, alert on new agent runtimes and systemd units created during installs, and hunt for the listed indicators of compromise.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [SafeDep](https://safedep.io/blog/malicious-npm-leadstack-crm-connect-hermes-agent-backdoor)  ·  **Retrieved:** 2026-11-20  
**Scores:** Newness 33 · Novelty 60 · Relevance 85 · Credibility 47 · **Composite 59** _(each 0-100)_  
**Tags:** `npm`, `malicious-package`, `hermes-agent`, `ai-agent-implant`, `telegram-c2`, `systemd-persistence`, `postinstall`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: data/product-security.json has the Offsec Harness Index entry listing Hermes Agent as tied to a confirmed breach, and the page cites ThreatDown's September 2026 Carbonato botnet that runs Hermes Agent via exposed Docker APIs. This is the first npm-install delivery SafeDep has seen, with the agent persona fetched at install time so it can change without a new release.

_Source: [https://safedep.io/blog/malicious-npm-leadstack-crm-connect-hermes-agent-backdoor](https://safedep.io/blog/malicious-npm-leadstack-crm-connect-hermes-agent-backdoor)_  ·  [← back to index](../README.md)
