# Anthropic's unreleased model built five attack chains against major software

**Published:** Oct 27, 2026

> **Takeaway:** Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.

## TL;DR

Anthropic used an unreleased internal research model to find and chain vulnerabilities in Chrome, Safari, Android, Windows and Linux. The results included a one-click Chrome sandbox escape (62 CVEs patched in Chrome 156), a Safari same-origin policy bypass, an Android lock screen bypass, a remote Windows QUIC crash (CVE-2026-33096) and a zero-click Linux multipath TCP root exploit (CVE-2026-98432). Anthropic calls two of its lessons particularly important: run many different scanning agents in parallel, and scan at pull-request time to stop new bugs.

## Lessons

- Running more compute and a wider mix of scanning strategies finds substantially more vulnerabilities than a single scanner. - _"Test-time compute scaling and scanner diversity substantially increase how many vulnerabilities you find."_
- Judge each scanner by how many new findings it adds to the combined set, not by its raw count. - _"measures each scanner by how many additional vulnerabilities it contributes to the mix"_
- Model-built chains can combine intended behaviors that are harmless on their own into a full exploit, as in the data-only Safari chain. - _"Several of the weaknesses are not vulnerabilities on their own but intended behaviors that become exploitable when combined."_
- Clearing the existing backlog is not enough. Scanning at pull-request time cuts the rate at which new bugs enter the code. - _"For that, we recommend scanning at PR time."_

## Threat · Conditions · Mitigations

- **Threat:** Frontier models can now discover and chain several vulnerabilities into working one-click or zero-click exploits against browsers, phones and kernels, work that used to need specialist teams.
- **Conditions:** An attacker needs a model with comparable capability and code, binaries or a live device to analyze. The Linux exploit also needs a reachable multipath TCP listener, and the Windows crash needs a native HTTP/3 (QUIC) listener.
- **Mitigations:** Apply the Chrome 156, Apple, Android, Windows (CVE-2026-33096) and Linux kernel (CVE-2026-98432) fixes, scan your own code with diverse AI scanners plus variant analysis, and add security scanning at pull-request time.

---

**Topic:** Product Security  ·  **Domain:** Vulnerability Research & Red Teaming  
**Source:** [Anthropic Research](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)  ·  **Retrieved:** 2026-10-28  
**Scores:** Newness 20 · Novelty 70 · Relevance 90 · Credibility 74 · **Composite 64** _(each 0-100)_  
**Tags:** `ai-vulnerability-research`, `exploit-chains`, `browser-security`, `sandbox-escape`, `linux-kernel`, `android`, `variant-analysis`, `pr-scanning`, `anthropic`  
**Also reported by:** [The Hacker News](https://thehackernews.com/2026/10/anthropics-unreleased-ai-model-chains.html) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest pool entries: 'Claude found 493 attack-surface issues across 25 open-source projects' (finds issues but builds no exploit chains), 'GitHub Security Lab found 24 Android vulnerabilities with its AI agent', and the Mythos 5 AISI incident (a cyber-capability incident, not vulnerability research). New here: end-to-end exploit chains against Chrome, Safari, Android, Windows and Linux.

_Source: [https://www.anthropic.com/research/discovering-vulnerabilities-with-claude](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)_  ·  [← back to index](../README.md)
