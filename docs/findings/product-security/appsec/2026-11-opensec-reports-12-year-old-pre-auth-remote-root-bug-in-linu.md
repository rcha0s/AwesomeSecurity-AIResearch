# OpenSec reports 12-year-old pre-auth remote root bug in Linux NFS server

**Published:** Nov 25, 2026

> **Takeaway:** Patch and reboot every Linux NFS server on the fixed kernel branches (or confirm your distribution backport), and until then limit tcp/2049 to the storage network or turn off NFSv4.1 and 4.2.

## TL;DR

OpenSec disclosed CVE-2026-99362 (CVSS 9.8), a heap overflow in the Linux kernel NFS server (nfsd) that an unauthenticated client can trigger over tcp/2049 on hosts serving NFSv4.1 or 4.2. A client sets its per-slot reply cache to zero bytes, then the server copies a full reply into it and writes 61 bytes past a kernel heap object. OpenSec says its Antara harness chained this into a root shell (exploit not published); fixes are in Linux 6.12.117, 6.18.61, 7.3.2 and 7.4-rc1, and the bug dates to Linux 3.16 (2014).

## Lessons

- The bug is reachable before login because the in-kernel NFS server parses network input before it knows who the client is. - _"The NFS server runs inside the kernel and parses network input before it knows who you are."_
- The root cause is a client-controlled size: the client picks the reply cache size, and the server shrinks its reply buffer to that limit before accepting the slot. - _"Each NFSv4.1 session slot caches its last reply, so a retried request is answered exactly once. The client decides how big that cache is."_
- OpenSec says its own AI harness found the bug and built the root shell, but this is a vendor self-report and the exploit is private. - _"We pointed OpenSec's Antara at it. It came back with a root shell."_
- The attack is ordinary NFS traffic, so network signatures will not catch it; detection relies on host signals such as kernel warnings. - _"The attack is valid NFS, so there is no network signature. Look for:"_

## Threat · Conditions · Mitigations

- **Threat:** An unauthenticated attacker with network access to tcp/2049 sends NFSv4.1 requests that overflow the nfsd reply cache, leak kernel memory (including the KASLR slide), free a chosen object and run a command as root.
- **Conditions:** Kernel older than 6.12.117, 6.18.61, 7.3.2 or 7.4-rc1 with no backport; in-kernel nfsd loaded; NFSv4.1 or 4.2 enabled (the default); tcp/2049 reachable on a non-loopback address.
- **Mitigations:** Update the kernel and reboot (or install the distribution update listing CVE-2026-99362); until then firewall tcp/2049 to the storage network or disable NFSv4.1 and 4.2 (this turns off pNFS and some 4.2 features); the source says kernel hardening does not remove the overflow.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [@dm via Hacker News](https://opensec.in/blog/nfs2root-cve-2026-99362)  ·  **Author:** dm  ·  **Retrieved:** 2026-11-26  
**Scores:** Newness 23 · Novelty 60 · Relevance 72 · Credibility 60 · **Composite 54** _(each 0-100)_  
**Tags:** `linux-kernel`, `nfsd`, `heap-overflow`, `pre-auth-rce`, `cve-2026-99362`, `ai-found-vuln`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Existing product-security entries on Linux kernel flaws (e.g. 'Two KSMBD RCE flaws hit public kernel lists with no patch', 'OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs') cover remote kernel RCE and AI-found kernel bugs, but not this nfsd reply-cache overflow.

_Source: [https://opensec.in/blog/nfs2root-cve-2026-99362](https://opensec.in/blog/nfs2root-cve-2026-99362)_  ·  [← back to index](../README.md)
