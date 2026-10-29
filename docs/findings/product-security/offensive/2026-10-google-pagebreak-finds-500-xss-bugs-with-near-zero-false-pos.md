# Google PageBreak finds 500+ XSS bugs with near-zero false positives

**Published:** Oct 1, 2026

> **Takeaway:** Let the AI agent propose bugs, report only what a non-AI validator confirms by exploitation, and treat safe-by-default frameworks as the stronger defense.

## TL;DR

PageBreak is Google Product Security's internal agent, mostly running on Gemini models, that hunts bugs in Google's own web apps. The agent only proposes a bug. Hand-written (not AI-written) validators then fire a real payload per bug class (XSS, SQL injection, path traversal, RCE, server-side request forgery) against a running environment, and only confirmed findings reach product teams. That produced 500+ XSS bugs at near-zero false positives, while apps built on Google's secure-by-design frameworks yielded just 2.

## Lessons

- The agent only proposes a bug. A separate deterministic validator confirms it by actually running an exploit payload. - _"When the agent identifies a potential flaw, it passes the hypothesis to a validator which then executes a real payload to confirm the exploit."_
- Testing against a running environment cuts false positives and keeps 'AI slop' away from product teams. - _"This approach results in a near-zero false positive rate, ensuring that we avoid overloading product teams with unverified vulnerability reports."_
- Unverified findings are not thrown away. They seed later runs and show where validators are missing, but they never go to developers. - _"Crucially, we do not send these unverified candidates to product teams, preserving their focus for high-confidence alerts."_
- Asking the agent to report which capability or access it lacked turns failed validations into a roadmap for the harness. - _"We let the PageBreak agent report what capabilities or environment access it is missing in order to validate a report."_
- Secure-by-design web frameworks held up against the agent: only 2 XSS bugs across hundreds of apps built on them, both in internal or debug endpoints. - _"As of September 4, 2026, the scanner identified only 2 XSS vulnerabilities across hundreds of web applications built on these frameworks and those were limited to internal applications or debug endpoints with hardening gaps."_

## Threat · Conditions · Mitigations

- **Threat:** Noisy, unverified LLM vulnerability reports overwhelm product teams. Real XSS and similar bugs remain in large first-party web estates.
- **Conditions:** Needs running test environments, scanning infrastructure that can authenticate to the apps, and validators for each bug class. Google also relies on its mono-repo and traffic-to-code mapping (Security Signals), which most organizations do not have.
- **Mitigations:** Use secure-by-design web frameworks. Gate AI findings on deterministic exploit validation. Run agents across many iterations with identical seeds to improve the odds of finding a working exploit path.

---

**Topic:** Product Security  ·  **Domain:** Vulnerability Research & Red Teaming  
**Source:** [tl;dr sec (curator link)](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 21 · Novelty 45 · Relevance 75 · Credibility 70 · **Composite 52** _(each 0-100)_  
**Tags:** `ai-vulnerability-discovery`, `exploit-validation`, `xss`, `false-positives`, `secure-by-design`, `google`, `agent-harness`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Chainguard Athena write-up ('Gate agent-found vulnerabilities on host-side replay', archive.json); the general generate-then-verify pattern used by AI pentest agents such as XBOW and Google Big Sleep. New here: production-scale numbers (500+ XSS) and the framework-hardening comparison. Verifier's closest: Chainguard Athena host-side replay gate; XBOW and Big Sleep generate-then-verify.

_Source: [https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project)_  ·  [← back to index](../README.md)
