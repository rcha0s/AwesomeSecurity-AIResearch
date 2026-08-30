# What's in a tag name? JavaScript, apparently

**Published:** Aug 25, 2026

> **Takeaway:** Do not rely on WAFs or character blocklists to stop XSS; enforce context-aware output encoding, a strict Content-Security-Policy, and trusted HTML sanitization, since exotic tag-name and DOM-property tricks bypass signature-based filters in every browser.

## TL;DR

Gareth Heyes shows that HTML tag names can carry XSS payloads: DOM properties like localName, part, and classList expose case-preserving or array-split versions of the tag name that can be fed back into event handlers, the Function constructor, or setHTMLUnsafe to execute JavaScript across every browser. Because these vectors use unusual, uppercase, or separator-character HTML, they readily bypass blocklists and WAF signatures. The defensive lesson is that WAF/blocklist filtering is fragile and should not be relied on in place of proper output encoding and CSP.

## What to learn

- Browsers are far more lenient with tag-name characters than filters assume, enabling novel XSS vectors. - _"browsers are far more lenient than you would expect"_
- Seemingly harmless DOM properties (localName, part, classList) can smuggle and transform payloads past blocklists/WAFs. - _"unusual HTML and seemingly harmless properties such as localName, part, and classList can become unexpected sources of hiding payloads and transformations that can bypass blocklists and WAF signatures"_
- WAF signature filtering is an unreliable primary XSS defense. - _"It's also a pretty nice way to bypass a WAF"_

---

**Topic:** Product Security  ·  **Domain:** web security  
**Source:** [PortSwigger Research](https://portswigger.net/research)  ·  **Retrieved:** 2026-08-29  
**Scores:** Newness 20 · Novelty 84 · Relevance 80 · Credibility 73 · **Composite 65.15**  
**Tags:** `xss`, `waf-bypass`, `html`, `javascript`, `blocklist-bypass`, `csp`, `dom`  
**Verification:** ✓ independently verified · closest prior art: PortSwigger XSS cheat sheet and prior WAF/blocklist-bypass research (unicode overflows, phantom Version cookie).

_Source: [https://portswigger.net/research](https://portswigger.net/research)_  ·  [← back to index](../README.md)
