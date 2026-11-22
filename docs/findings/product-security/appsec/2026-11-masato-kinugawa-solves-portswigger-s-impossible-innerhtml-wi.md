# Masato Kinugawa solves PortSwigger's impossible innerHTML-without-equals XSS using the selectedcontent element

**Published:** Nov 18, 2026

> **Takeaway:** New HTML elements create new XSS paths; sanitizers and filters that block characters or script tags need re-testing against them.

## TL;DR

The new HTML selectedcontent element clones the selected option's children into itself, and the clone of an SVG script element can run even when the original was inserted through innerHTML. That gives JavaScript execution without an equals sign, and a variant needs no whitespace, slash or equals. Chromium has since changed the behaviour (Chrome 153), but the payload still works in Safari 27.2.

## Lessons

- A new element that clones DOM nodes can execute scripts that the parser would otherwise leave inert. - _"Previously, no HTML element could perform this kind of cloning operation on its own without executing JavaScript."_
- The innerHTML trick needs both an SVG-namespace script and the selectedcontent clone; removing either stops execution. - _"This tells us that both conditions are necessary for JavaScript execution in this vector"_
- The root cause was an inconsistent already-started flag between HTML and SVG scripts, which cloning exposed. - _"This cloning behavior seems to have been the key to making this vector work."_
- The fix is browser-specific, so Safari users remained exposed at the time of writing. - _"However, it still works in Safari 27.2."_

## Threat · Conditions · Mitigations

- **Threat:** Cross-site scripting through innerHTML injection and character-filtered contexts using the selectedcontent element.
- **Conditions:** Pages that assign attacker-influenced HTML to innerHTML or filter characters like equals, in browsers that still run cloned SVG scripts (Safari 27.2 at time of writing; Chrome before 153).
- **Mitigations:** Update browsers, keep sanitizers such as DOMPurify current, apply a strict Content Security Policy, and avoid assigning untrusted markup to innerHTML.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [PortSwigger Research](https://portswigger.net/research/achieving-the-impossible-xss-in-innerhtml-without-equals)  ·  **Retrieved:** 2026-11-20  
**Scores:** Newness 30 · Novelty 78 · Relevance 78 · Credibility 72 · **Composite 65** _(each 0-100)_  
**Tags:** `xss`, `innerhtml`, `selectedcontent`, `svg`, `browser-quirks`, `safari`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Kabir Acharya's May 2026 DOMPurify selectedcontent bypass (DOMPurify wiki, Engine Deferred Mutation) and Gareth Heyes's 2020 impossible-labs list; the new part is script execution via SVG script cloning under innerHTML and the no-whitespace, slash or equals vector.

_Source: [https://portswigger.net/research/achieving-the-impossible-xss-in-innerhtml-without-equals](https://portswigger.net/research/achieving-the-impossible-xss-in-innerhtml-without-equals)_  ·  [← back to index](../README.md)
