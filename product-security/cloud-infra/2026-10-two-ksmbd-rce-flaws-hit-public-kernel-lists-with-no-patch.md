# Two KSMBD RCE flaws hit public kernel lists with no patch

**Published:** Oct 22, 2026

> **Takeaway:** If you run KSMBD, check whether it is loaded and limit port 445 exposure until fixes land; AI-found bugs now arrive on public lists.

## TL;DR

Trend Micro's Zero Day Initiative sent two KSMBD reports (ZDI-CAN-33774 and ZDI-CAN-33549) to public kernel mailing lists without patches. ZDI-CAN-33774 is an unauthenticated race in protocol dispatch on port 445; ZDI-CAN-33549 is an integer underflow in the SMB Direct path needing RDMA. Neither had a mainline fix or a CVE, and the reports credit Trend Micro's AI scanner. The kernel's rules treat AI-found bugs as public, which explains the routing. The primary posts are on lore.kernel.org, which blocks automated fetches, so this cites The Hacker News.

## Lessons

- One flaw is reachable before login on any KSMBD server. - _"ZDI-CAN-33774 requires no authentication, exposing any server running KSMBD on port 445."_
- An AI scanner was credited with the discovery. - _"The ZDI reports credit TrendAI, Trend Micro's AI scanner, as the finder."_
- No fix and no CVE at disclosure time. - _"neither flaw has a named fix in the mainline kernel"_
- A simple check shows whether you are exposed. - _"Running systemctl status ksmbd or lsmod | grep ksmbd confirms whether the module is active."_

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [source](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 19 · Novelty 45 · Relevance 60 · Credibility 50 · **Composite 44** _(each 0-100)_  
**Tags:** `ksmbd`, `linux-kernel`, `smb`, `zdi`, `ai-found-vulnerabilities`, `disclosure`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Public disclosure before a patch is unusual; the kernel's policy that AI-found bugs go to public lists is the new process point. Verifier: Prior KSMBD CVEs (CVE-2022-47939, CVE-2023-3866, ZDI-found ksmbd bugs); Linux kernel May 2026 AI-bug-is-public policy and Big Sleep style AI-found kernel bugs

_Source: [https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html)_  ·  [← back to index](../README.md)
