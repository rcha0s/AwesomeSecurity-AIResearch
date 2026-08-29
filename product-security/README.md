# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_3 vetted findings · updated 2026-08-29 · ranked by composite · latest 31 days only · [19 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Web Application Security | 1 |
| Malware & Threat Intel | 1 |
| Application Security | 1 |

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
