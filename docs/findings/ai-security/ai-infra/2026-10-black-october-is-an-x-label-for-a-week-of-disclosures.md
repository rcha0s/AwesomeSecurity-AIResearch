# "Black October" is an X label for a week of disclosures

**Published:** Oct 23, 2026

> **Takeaway:** Read the label as a backlog of old defects being dated, not as one new attack; the AI angle is faster discovery and AI credentials as loot.

## TL;DR

"Black October" is the name an X post by the AISafetyMemes account gave on 2026-10-22 to the disclosures of Oct 19 to 22. They include PHP2Shell (CVE-2026-109618 and CVE-2026-109619, found by Wiz with frontier AI models), a GitLab 10.0 flaw, a Node.js Brotli RCE, the eMudhra certificate keys and a poisoned LiteLLM 1.107.0. Forkast's reading is that this was a disclosure wave, not an attack wave: most flaws and intrusions are months or years old, and AI models both found the worst bugs and were the target of the credential theft.

## Lessons

- The label compresses events of very different ages into one week; the disclosure date is not the exposure date. - _"This was a disclosure wave, not an attack wave."_
- Frontier models found several of the week's worst flaws, so patch windows will keep shrinking. - _"Models and agents found this week’s worst flaws: PHP2Shell through frontier models, Brotli through OpenAI Codex Security researchers."_
- Dating exposure from the disclosure week hides how long the weak keys, bugs and intrusions were live. - _"The week of Oct 19 to 22 is when the bills were dated, not when they were incurred."_

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [forkast.news](https://forkast.news/black-october-is-a-disclosure-wave-the-label-hides-the-clock/)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 0 · Novelty 60 · Relevance 80 · Credibility 60 · **Composite 51** _(each 0-100)_  
**Tags:** `black-october`, `php2shell`, `litellm`, `disclosure`, `ai-found-vulnerabilities`, `x-discourse`  
**Also reported by:** [AISafetyMemes on X (the post that named it)](https://x.com/AISafetyMemes/status/2113113711644737835), [Wiz Research: PHP2Shell](https://www.wiz.io/blog/php2shell-php-rce) _(+2 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The pool holds the Wiz and Talos PHP2Shell items; no entry covers the label, its X origin, or the 'disclosure wave, not attack wave' reading of the cluster.

_Source: [https://forkast.news/black-october-is-a-disclosure-wave-the-label-hides-the-clock/](https://forkast.news/black-october-is-a-disclosure-wave-the-label-hides-the-clock/)_  ·  [← back to index](../README.md)
