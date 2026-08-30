# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_7 vetted findings · updated 2026-08-30 · ranked by composite · latest 31 days only · [20 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| web security | 2 |
| cloud & infrastructure | 1 |
| software supply chain | 1 |
| Web Application Security | 1 |
| Malware & Threat Intel | 1 |
| Application Security | 1 |

## web security

- **[What's in a tag name? JavaScript, apparently](web-security/2026-08-what-s-in-a-tag-name-javascript-apparently.md)** · composite **65.15** · Aug 25, 2026  
  Do not rely on WAFs or character blocklists to stop XSS; enforce context-aware output encoding, a strict Content-Security-Policy, and trusted HTML sanitization, since exotic tag-name and DOM-property…  
  _[PortSwigger Research](https://portswigger.net/research)_
- **[Show, Don't Tell: What Evo Continuous Offensive Security Found in a Real Enterprise SaaS](web-security/2026-08-show-don-t-tell-what-evo-continuous-offensive-security-found.md)** · composite **63.65** · Aug 10, 2026  
  Enforce server-side role/permission checks and key allowlists on every write endpoint (including legacy admin ones), actually validate HMAC signatures, and lock down credentialed CORS, then test for…  
  _[Snyk](https://snyk.io/blog/)_

## cloud & infrastructure

- **[VMs won't contain cyber-capable agents](cloud-infrastructure/2026-08-vms-won-t-contain-cyber-capable-agents.md)** · composite **67.85** · Aug 26, 2026  
  Treat capable AI agents as an advanced persistent threat: isolate them with hardened microVMs, enforce least privilege, monitor actively, and keep host and hypervisor dependencies fully patched.  
  _[Trail of Bits](https://blog.trailofbits.com/)_

## software supply chain

- **[This Shit is Hard: Patching a vulnerability that has no fix](software-supply-chain/2026-08-this-shit-is-hard-patching-a-vulnerability-that-has-no-fix.md)** · composite **66.65** · Aug 17, 2026  
  When remediating (including AI-generated) fixes, gate every patch on feasibility, regression testing, and an independent exploit test, batch interdependent fixes, re-validate on each backported…  
  _[Chainguard](https://www.chainguard.dev/unchained)_

## Web Application Security

- **[CSS the bomb: sanitized webmail CSS steals tokens, keylogs Outlook, and turns Atlas AI browser into an exfil bot](web-application-security/2026-08-css-the-bomb-sanitized-webmail-css-steals-tokens-keylogs-out.md)** · composite **66.05** · Aug 6, 2026  
  CSS sanitizers built as feature allow-lists are not a trust boundary; the only durable defense is strict iframe sandboxing plus killing dangerous selectors, select, and free-form image URLs.  
  _[source](https://portswigger.net/research/css-the-bomb-inside-your-inbox)_

## Malware & Threat Intel

- **[Measuring AI-enabled malware: ~97% of samples never reach production; AI changes how malware is authored, not how it executes](malware-threat-intel/2026-08-measuring-ai-enabled-malware-97-of-samples-never-reach-produ.md)** · composite **57.02** · Aug 25, 2026  
  Don't over-index on 'AI malware' hype: your existing behavioral/sandbox detection still catches it - but expect faster variant iteration.  
  _[Unit 42 (Palo Alto Networks)](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/)_

## Application Security

- **[go-git worktree wrapper vetoed dangerous strings but still followed symlinks that were already there (GHSA-hc8v-wwc9-vgxm)](application-security/2026-08-go-git-worktree-wrapper-vetoed-dangerous-strings-but-still-f.md)** · composite **56.0** · Aug 7, 2026  
  A path-string allowlist is not a symlink-safe boundary; you have to make the filesystem wrapper itself reject symlink escapes at open time.  
  _[source](https://github.com/advisories/GHSA-hc8v-wwc9-vgxm)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
