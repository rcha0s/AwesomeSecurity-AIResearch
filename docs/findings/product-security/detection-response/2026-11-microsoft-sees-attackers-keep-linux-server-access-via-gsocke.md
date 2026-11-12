# Microsoft sees attackers keep Linux server access via GSocket relays after patching

**Published:** Nov 11, 2026

> **Takeaway:** After any web remote code execution (RCE) on a Linux server, hunt for GSocket and layered persistence and enforce egress filtering; a patch alone leaves the attacker in.

## TL;DR

Microsoft reports multiple unrelated threat actors installing GSocket, an open-source relay-based remote access tool, on Linux servers compromised through web application remote code execution (RCE). Access survives patching of the original bug. Both the host and the operator connect outbound to the public Global Socket Relay Network and authenticate with a shared secret, which leaves no attacker-owned IP or domain to block. Deployments use /dev/shm for staging, process names that look like kernel threads, and layered cron, systemd and shell-profile persistence. GSocket-related detections rose 356.2% from March to August 2026, mostly on PHP (Hypertext Preprocessor), cPanel and Apache hosting. In a few observed incidents, attackers attempted to gain root through CVE-2026-43284 (Dirty Frag).

## Lessons

- Patching the exploited web app is not remediation: the relay client and its persistence live independently of the vulnerable application. - _"Because GSocket runs independently of the exploited application, patching the vulnerability does not remove the relay client or its persistence."_
- A relay command-and-control (C2) channel keyed by a shared secret has no attacker-owned IP or domain to block and the operator can reconnect from anywhere, but defenders can still restrict access to the relay itself, and Microsoft publishes hashes, paths and distribution hosts. - _"GSocket identifies endpoints by a shared secret instead of an IP address or hostname."_
- Egress control is the lever: inbound rules never see the traffic, so deny-by-default outbound plus monitoring of relay endpoints is the network defense. - _"Apply deny-by-default egress rules, allow only required destinations, and monitor connections to relay infrastructure."_
- This is a growing, multi-actor trend rather than a single campaign. - _"From March through August 2026, devices with GSocket-related detections increased 356.2%, although the increase was not consistent month to month."_

## Threat · Conditions · Mitigations

- **Threat:** After exploiting an internet-facing web application, attackers deploy GSocket for encrypted outbound relay C2 with masquerading and redundant persistence, retaining access after the vulnerability is patched and attempting local root escalation.
- **Conditions:** Linux server with an exploitable internet-facing application (commonly PHP, cPanel or Apache hosting); outbound traffic to the Global Socket Relay Network permitted; writable or memory-backed staging paths such as /dev/shm.
- **Mitigations:** Remediate the host and not just the app by removing the GSocket client, persistence and staged files, enforce deny-by-default egress and monitor relay connections, mount temp and memory-backed directories noexec, audit cron, systemd and shell profiles, and prioritize kernel privilege-escalation patches on internet-facing servers.

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 52 · Novelty 35 · Relevance 65 · Credibility 70 · **Composite 53** _(each 0-100)_  
**Tags:** `gsocket`, `linux`, `c2`, `persistence`, `egress-filtering`, `web-rce`, `living-off-the-land`, `threat-hunting`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Abuse of legitimate relay/tunnel tools for C2 (ngrok, Cloudflare Tunnel, gs-netcat use reported in earlier cryptojacking and Linux intrusions) and generic 'patching is not eviction' guidance; tracker has related relay-network entries (Volt Typhoon relays) but nothing on GSocket. New: Microsoft telemetry on scale and sector, concrete deployment tradecraft and KQL hunts. Verifier's closest: CL-UNK-1211 Linux persistence entry; Volt Typhoon rotating relays.

_Source: [https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/](https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/)_  ·  [← back to index](../README.md)
