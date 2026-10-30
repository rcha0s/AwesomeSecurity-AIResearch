# PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers

**Published:** Oct 27, 2026

> **Takeaway:** If you accept SVG uploads, sanitize with DOMPurify or darylldoyle/svg-sanitizer, serve user files from a separate origin, and never let users influence response headers.

## TL;DR

Gareth Heyes tested eight sanitizers for Scalable Vector Graphics (SVG) uploads and bypassed six, using tricks such as switching one element's namespace to XHTML, animating a link into a JavaScript URL, and pointing a stylesheet instruction at a data URL. He also showed Firefox running JavaScript from a stylesheet delivered in a `Link` response header over a harmless XML body, and Safari importing a GIF as SVG through `<use>`. DOMPurify and darylldoyle/svg-sanitizer resisted every technique.

## Lessons

- Two libraries held up against every technique in the post. - _"Both DOMPurify and darylldoyle/svg-sanitizer held up against everything in this post, which is quite impressive."_
- A namespace switch on one element brings HTML into an SVG without foreignObject. - _"Switch the XML namespace on a single element to XHTML and the browser renders it as HTML directly inside the SVG."_
- Response headers can load stylesheets in Firefox, so a clean body is not enough. - _"Firefox lets you load external CSS files using a Link response header."_
- An uploaded GIF can carry an SVG payload that Safari imports. - _"if you can upload a GIF that contains the payload, it won't render when you open it in the browser, but it can still be imported with a `<use>` element!"_

## Threat · Conditions · Mitigations

- **Threat:** Stored XSS through uploaded SVG or image files that pass a sanitizer.
- **Conditions:** Applications that accept SVG or image uploads and serve them from the main origin using one of the six bypassed sanitizers.
- **Mitigations:** Use DOMPurify or darylldoyle/svg-sanitizer, serve uploads from a separate origin with a strict CSP, and keep user input out of response headers.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [PortSwigger Research](https://portswigger.net/research/scalable-vector-grief)  ·  **Retrieved:** 2026-10-27  
**Scores:** Newness 20 · Novelty 62 · Relevance 75 · Credibility 72 · **Composite 57** _(each 0-100)_  
**Tags:** `xss`, `svg`, `sanitizer-bypass`, `xslt`, `browser-quirks`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: SVG XSS and sanitizer bypasses are a long-running topic, and the post cites Kevin Mizu's animateTransform trick; the Link-header stylesheet execution in Firefox and Safari's GIF-as-SVG import are new.

_Source: [https://portswigger.net/research/scalable-vector-grief](https://portswigger.net/research/scalable-vector-grief)_  ·  [← back to index](../README.md)
