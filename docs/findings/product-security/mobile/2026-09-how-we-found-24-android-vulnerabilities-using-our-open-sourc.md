# How we found 24 Android vulnerabilities using our open source AI security agent

**Published:** Sep 28, 2026

> **Takeaway:** Scaffolded, platform-specific taskflows make LLMs effective Android bug hunters, but severity and exploitability still need a PoC and a human.

## TL;DR

GitHub Security Lab extended its open-source Taskflow Agent with Android-specific audit steps. One taskflow separates mobile from non-mobile entry points, and another checks a fixed list of vulnerability classes against each entry point. Together they found 24 vulnerabilities, including OsmAnd location tracking and a WebView account-takeover chain. The post is candid that LLMs over-report low-severity bugs, misjudge severity, and need PoC runs plus expert review.

## Lessons

- Give the model a per-entry-point checklist of vulnerability classes so non-determinism doesn't skip the essential bug classes on less familiar platforms like Android. - _"Since mobile application vulnerabilities are less widely known and LLMs are non-deterministic, we should ensure the LLM checks for certain essential vulnerabilities classes."_
- Run a strict checklist prompt several times alongside a broad open-ended prompt: the first catches the obvious bugs and the second finds the creative ones. - _"By combining both prompts across multiple runs, we get the best of each"_
- LLM auditors over-report low-impact or unrealistic-state bugs, even when told not to, so every finding needs expert triage. - _"it often reported low-severity vulnerabilities, even when specifically told not to do so"_
- Making the model write a proof of concept surfaces mitigating factors it otherwise misses; a debugger is the stronger fix for the false positives that remain. - _"the only way to fix these issue is to give the LLM a debugger to run the proof of concept and original code"_

---

**Topic:** Product Security  ·  **Domain:** Mobile & Device Security  
**Source:** [GitHub Security Lab](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)  ·  **Retrieved:** 2026-10-19  
**Scores:** Newness 5 · Novelty 45 · Relevance 82 · Credibility 75 · **Composite 51** _(each 0-100)_  
**Tags:** `android`, `ai-vuln-discovery`, `taskflows`, `webview`, `llm-triage`, `false-positives`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Earlier GHSL Taskflow Agent posts on generic audit taskflows, and LLM-assisted SAST triage; the delta is the Android-specific entry-point and checklist decomposition plus its field results.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)_  ·  [← back to index](../README.md)
