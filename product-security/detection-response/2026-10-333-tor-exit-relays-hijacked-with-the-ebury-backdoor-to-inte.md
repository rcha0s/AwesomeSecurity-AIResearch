# 333 Tor exit relays hijacked with the Ebury backdoor to intercept SSH

**Published:** Oct 20, 2026

> **Takeaway:** Never accept a changed SSH host key over Tor or any untrusted path; use key auth, and expect backdoored infrastructure hosts to be turned into traffic interceptors.

## TL;DR

A researcher who goes by kaba found that attackers had taken over about 333 Tor exit relays (roughly 10% of exits) and set them to redirect SSH on port 22 to 12 interception servers, stealing passwords, watching sessions and infecting the real server with Ebury. They had gained access to the servers in August and deployed Ebury 1.8.3 on them. Tor's network health team flagged the relays as bad exits on October 4 and all were offline by October 5. The attack also favored unencrypted mail traffic.

## Lessons

- SSH on port 22 was silently redirected to attacker servers on infected exits. - _"if you attempt an SSH connection over Port 22, you're unknowingly redirected to one of 12 SSH interception servers."_
- The infection started two months earlier with a Linux credential-stealing backdoor. - _"The attackers had gained access to the servers two months earlier, in August, and quietly deployed their Ebury 1.8.3 payload (an OpenSSH backdoor and credential stealer for Linux)."_
- Scale: roughly a tenth of Tor's exit capacity. - _"To give you a sense of scale, all of Tor has around 3000 exit relays, so roughly 10% were under their control."_
- A victim who ignored the host-key warning also got their server infected. - _"Opens a second connection to your server and infects it with Ebury"_

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [source](https://kaba.cx/posts/20261020_Tor/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 20 · Novelty 60 · Relevance 55 · Credibility 55 · **Composite 48** _(each 0-100)_  
**Tags:** `tor`, `ssh`, `mitm`, `ebury`, `exit-relays`, `host-key`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Malicious Tor exit relays are a known threat (sslstrip, bitcoin-swapping); mass port-22 redirection with a backdoored relay fleet is new. Verifier: Malicious Tor exit sniffing/sslstrip (Josh Pitts 2014, 'Spoiled Onions' 2016, KAX17 relays 2020-21); ESET Ebury research (Windigo 2014, 2024 report)

_Source: [https://kaba.cx/posts/20261020_Tor/](https://kaba.cx/posts/20261020_Tor/)_  ·  [← back to index](../README.md)
