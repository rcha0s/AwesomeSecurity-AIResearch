# CSS the bomb: sanitized webmail CSS steals tokens, keylogs Outlook, and turns Atlas AI browser into an exfil bot

**Topic:** Product Security  ·  **Domain:** Web Application Security  
**Source:** [source](https://portswigger.net/research/css-the-bomb-inside-your-inbox)  ·  **Published:** Aug 6, 2026  ·  **Retrieved:** 2026-08-10  
**Scores:** 🆕 Newness 58 · ✨ Novelty 78 · 🎯 Relevance 88 · 🏛️ Credibility 75 · **Composite 75.55**  
**Tags:** `css`, `webmail`, `sanitization`, `prompt-injection`, `keylogger`, `atlas`, `outlook`  
**Verification:** ✓ independently verified · closest prior art: Apple ANSI-DNS-exfil chain (embracethered) covers CLI-side prompt-injection exfil; CSS-side webmail attacks trace back to Heiderich's mutation XSS and Gerste's font-based CSS exfil. The AI-browser-via-CSS-hidden-content angle is materially new relative to the pool.

> **Takeaway:** CSS sanitizers built as feature allow-lists are not a trust boundary; the only durable defense is strict iframe sandboxing plus killing dangerous selectors, select, and free-form image URLs.

## TL;DR

_The gist, not every detail - read the [full source](https://portswigger.net/research/css-the-bomb-inside-your-inbox) for the complete write-up._

Gareth Heyes chains allowed HTML/CSS features across Fastmail, Outlook, AOL/Yahoo/Gmail/ProtonMail and OpenAI's Atlas AI browser to defeat webmail CSS sanitization. Techniques include HTML labels that trigger arbitrary UI actions, invisible :before/:after content that feeds one story to the human and another to an AI browser (indirect prompt injection), attribute-selector nesting to brute-force login tokens after a paste-into-draft, CSS hotwiring to hijack any click, and a real-time keylogger via select+opacity plus Chrome interest invokers.

## What to learn

- Invisible :before/:after content lets an attacker present two different messages to the human and to an AI browser reading the same email, enabling indirect prompt injection through webmail. - _"you could use the `:before` and `:after` pseudo-elements to hide the text from the LLM and you could use opacity to hide it from the victim. This creates a disparity between what the victim sees and what the LLM sees, potentially altering the email's context."_ ✅
- CSS attribute selectors, combined with nesting, can brute-force secret URL parameters (e.g. Medium's 12-char login token) inside a webmail draft after a single paste, without JavaScript. - _"using nesting we can match the start with one selector that's outputted only once and then nest the other selectors to brute-force the token with a smaller amount of CSS"_ ✅
- The only defense that actually holds is strict iframe sandboxing plus removing dangerous selectors and select elements; feature-level CSS/HTML allow lists get bypassed by gadgets and mutation. - _"One of the best methods to protect against these attacks is strict isolation. If you isolate the email message using sandboxed iframes you restrict the ability to break out of trusted boundaries."_ ✅
- CSS hotwiring lets an attacker with allow-listed CSS force the victim's next click, anywhere on the page, to fire a chosen UI action, including multi-step ones. - _"CSS hotwiring is a technique that allows you to force the victim to click a specific UI action when clicking anywhere on the page **including multi-step actions** using just CSS."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** A single crafted email lets an attacker (a) spoof or hijack UI actions in Outlook/Fastmail via HTML labels + CSS hotwiring, (b) exfiltrate login tokens and passwords from third-party sites the victim pastes into a webmail draft, (c) inject instructions that only the AI browser sees, causing an AI email assistant to open attacker-controlled tabs and leak the victim's name, and (d) keylog Outlook via CSS/select gadgets. All from allow-listed HTML/CSS with no JavaScript.
- **Conditions:** Webmail client renders untrusted HTML/CSS in the same DOM as the trusted UI (no sandboxed iframe isolation), or the user pastes clipboard HTML into a contenteditable draft on Firefox, or an AI browser (e.g. Atlas) processes the email body as prompt context.
- **Mitigations:** Sandbox untrusted email content in an iframe with a strict CSP that blocks external image requests and data: URLs. Strip select, dangerous selectors (:has, :checked, :focus, :not), and image URLs pointing to attacker-controllable domains. When an image proxy is available, force all image requests through it. In AI-browser layers, treat CSS-hidden or opacity-zero content as untrusted content the model should not act on.

---

_Source: [https://portswigger.net/research/css-the-bomb-inside-your-inbox](https://portswigger.net/research/css-the-bomb-inside-your-inbox)_  ·  [← back to index](../README.md)
