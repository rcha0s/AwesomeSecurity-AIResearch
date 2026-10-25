# Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads, PHP auto_prepend_file persistence, a sudo-alias password stealer and a Go RAT

**Published:** Oct 15, 2026

> **Takeaway:** AI-assisted intrusions still rely on ordinary Linux tradecraft, so defenders should hunt for PHP config tampering, shell rc file aliases and outbound reverse shells, and can treat conversational reasoning comments inside dropped scripts as a triage signal.

## TL;DR

Unit 42 tracked CL-UNK-1211 attacking government and state-affiliated Linux infrastructure from October 2025 to April 2026; payloads carried conversational, step-by-step reasoning comments, which suggests they were produced by an LLM or run by an AI agent. The attackers persisted by setting auto_prepend_file in every PHP config, stole passwords with a .bashrc sudo alias and a PHP login logger, and ran a Go RAT called SysGoRAT over WebSocket C2. They searched qmail mailboxes for social media account emails and tried to kill Cortex XDR processes. One dropped script had a syntax error and would have failed.

## Lessons

- LLM-generated payloads leave a fingerprint: conversational reasoning comments addressed to the operator, which can be used as a hunting and triage indicator. - _"Multiple artifacts deployed throughout the intrusion contained AI-made conversational annotations and developer reasoning comments"_
- Persistence came from editing auto_prepend_file in every PHP config, which loads a web shell before every PHP request. Monitor these directories for integrity changes. - _"the attackers modified the auto_prepend_file value across all PHP configurations under the directories /etc/php/ and /opt/plesk/php/."_
- Credentials were harvested by a .bashrc sudo alias that fakes the password prompt, logs the password and then passes it to the real sudo. - _"In one instance, they created an alias for the sudo command that was designed to execute each time a user attempted to run it."_
- The attackers planted fake red-team markers so responders would mistake the intrusion for an authorized security assessment. - _"plant deceptive red-team markers to disguise activity as a legitimate security assessment"_

## Threat · Conditions · Mitigations

- **Threat:** A state-interest espionage cluster gets into government Linux web and mail servers through web shells, keeps access with PHP config persistence and a Go RAT, steals credentials and mailboxes to take over social media accounts, dumps databases, and tampers with EDR and logs.
- **Conditions:** Internet-facing Linux servers running PHP or Plesk and qmail, with cleartext credentials in config and history files, permissive outbound network access and EDR that can be killed by a local process.
- **Mitigations:** Monitor PHP configuration and shell rc files for integrity changes, remove cleartext credentials from configs and history, enforce strict outbound firewall rules on servers, enable EDR tamper protection, forward logs off-host, and hunt for the published indicators.

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 25 · Novelty 42 · Relevance 70 · Credibility 75 · **Composite 51** _(each 0-100)_  
**Tags:** `unit42`, `espionage`, `linux`, `web-shell`, `php`, `ai-generated-malware`, `credential-theft`, `anti-forensics`, `go-rat`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest pool entry is archive 'Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes'. This report is a concrete in-the-wild case consistent with that finding: the payloads were AI-authored, but the tradecraft is conventional and one script was broken. What is new is the specific TTP set (auto_prepend_file persistence, sudo-alias stealer, SysGoRAT, mailbox-to-social-media targeting, fake red-team markers). No earlier entry covers CL-UNK-1211 or SysGoRAT.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/)_  ·  [← back to index](../README.md)
