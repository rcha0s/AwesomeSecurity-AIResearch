# Signals Corps found 30 sites putting prompt injections in HTTP headers

**Published:** Oct 15, 2026

> **Takeaway:** Header injection is real but rare; the thing to watch is whether sites serve AI agents different content, so test your agents against it.

## TL;DR

Signals Corps read headers from 217,097,223 page responses (10% of Common Crawl's September 2026 crawl) and found 7,959 sites sending headers aimed at AI. Thirty tried injection, 24 of them in an X-AI header, and most were pranks. In tests, Claude models in Claude Code ignored the header unless the user's prompt gave the site authority; with such prompts 7 of 9 runs obeyed. The bigger finding is cloaking: 136 sites sent a header saying they had classified the crawler as an AI bot, a step that makes serving agents different content possible; the crawl itself cannot show whether they did.

## Lessons

- Injection attempts in headers are rare and mostly harmless pranks. - _"30 sites sent an injection attempt, 24 of them in a header named `X-AI`."_
- Exposure depends on the agent's fetch tool passing headers into the model context. - _"A header can only influence an agent if the agent’s fetch tool copies it into the model’s context."_
- In tests the models obeyed only when the user's prompt gave the site authority. - _"Claude Opus, Claude Sonnet, and Claude Haiku in Claude Code ignored our test header unless the user’s prompt gave the site authority, and with such prompts 7 of 9 runs obeyed."_
- Detecting AI clients by user-agent makes cloaking possible; the crawl cannot show whether sites did it. - _"That only takes a user-agent match"_

---

**Topic:** AI Security  ·  **Domain:** Prompt Injection & Jailbreaks  
**Source:** [source](https://www.signalscorps.com/blog/prompt-injection-in-http-headers/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 19 · Novelty 55 · Relevance 70 · Credibility 55 · **Composite 50** _(each 0-100)_  
**Tags:** `prompt-injection`, `http-headers`, `web-agents`, `cloaking`, `common-crawl`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Indirect injection through page bodies is well documented; large-scale measurement of header channels and agent-only cloaking is new. Verifier: SPLX AI-targeted cloaking study (Atlas); Cloudflare Markdown for Agents; earlier indirect prompt injection research (Greshake et al. 2023). Delta: first large-s

_Source: [https://www.signalscorps.com/blog/prompt-injection-in-http-headers/](https://www.signalscorps.com/blog/prompt-injection-in-http-headers/)_  ·  [← back to index](../README.md)
