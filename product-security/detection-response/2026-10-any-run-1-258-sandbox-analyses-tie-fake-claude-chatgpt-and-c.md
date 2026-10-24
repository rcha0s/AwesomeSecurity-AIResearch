# ANY.RUN: 1,258 sandbox analyses tie fake Claude, ChatGPT and Copilot tools to infostealers, session theft and account phishing

**Published:** Oct 14, 2026

> **Takeaway:** Hunt on the commands and scheduled tasks these lures produce, not on domains, and train developers that AI install commands are a phishing vector.

## TL;DR

ANY.RUN linked 1,258 public sandbox analyses (April 15 to October 5, 2026) to campaigns impersonating AI brands, with Claude (48%) and ChatGPT/Codex (33%) the most copied. At least 45% tell the user to paste a command into Run, PowerShell or Terminal. Lures live on trusted platforms and ads, and commands and backend paths stayed steadier than the rotating lure domains.

## Lessons

- The user performs the decisive step, which sidesteps email controls. - _"At least 45% of the analyses belong to campaigns that tell the user to paste a command into the Run dialog, PowerShell, or Terminal"_
- Claude and ChatGPT are the most imitated brands. - _"Together they account for 81% of those analyses: Claude 601 (48%) and OpenAI ChatGPT and Codex 418 (33%)"_
- Lures sit on trusted platforms, so domain blocking is weak. - _"We saw lures on GitHub, GitLab Pages, Cloudflare Pages, Google Sites, claude.ai, and chatgpt.com"_
- Behavior is a steadier detection anchor than domains. - _"Commands, backend paths, scheduled tasks, and other behavioral patterns remained more stable than the frequently rotating lure domains"_

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [source](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 27 · Novelty 35 · Relevance 65 · Credibility 50 · **Composite 44** _(each 0-100)_  
**Tags:** `fake-ai-tools`, `clickfix`, `infostealer`, `malvertising`, `claude`, `any-run`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: ClickFix and fake-installer campaigns are well documented; this contributes brand-level statistics for AI lures. Verifier: ClickFix / InstallFix write-ups (Push Security, Microsoft, Proofpoint); Mandiant UNC6032 fake AI video-generator lures; Cisco Talos fake AI installers. Delta: v  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/)_  ·  [← back to index](../README.md)
