# WordPress blocks six backdoored WP Connect plugins after suspected developer account compromise

**Published:** Nov 25, 2026

> **Takeaway:** A hijacked maintainer account can push a backdoor into a trusted registry; release holds and cooldowns are what stopped this one.

## TL;DR

Malicious releases of six WP Connect plugins were committed on November 22, 2026, after a suspected compromise of the developer's WordPress.org account. WordPress's release hold caught them before they went live, so sites are unlikely to be affected. The backdoor runs PHP code sent by a remote server, and Wordfence says the plugins had 3,600+ installs in total.

## Lessons

- WordPress's plugin review caught the malicious versions before release, which limited the damage. - _"The WordPress plugins team has independently detected and blocked the threat before it could be officially released."_
- This was deliberate code, not a bug, so there is no patch; the likely cause is a stolen developer account. - _"this was not a coding mistake, and there is no patch: the malicious code was added deliberately"_
- The backdoor fetches and runs PHP from an attacker-controlled server on every request, which gives full control of the site. - _"runs PHP code returned by the server via eval()"_
- Web shells and cron hooks planted by the backdoor would survive removing the plugin. - _"facilitating credential theft and persistence through web shells and cron hooks that outlast the plugin removal."_

## Threat · Conditions · Mitigations

- **Threat:** Backdoored plugin releases give an attacker remote PHP code execution, shell commands, password hash theft and web shells.
- **Conditions:** The site runs one of the malicious plugin versions; because WordPress blocked the releases, exposure is believed to be limited.
- **Mitigations:** Remove the six plugins, and hunt for web shells and WP-Cron hooks if a malicious version was ever installed.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [The Hacker News](https://thehackernews.com/2026/11/wordpress-blocks-six-backdoored-wp.html)  ·  **Retrieved:** 2026-11-25  
**Scores:** Newness 0 · Novelty 40 · Relevance 65 · Credibility 45 · **Composite 38** _(each 0-100)_  
**Tags:** `wordpress`, `supply-chain`, `plugin-backdoor`, `account-compromise`, `webshell`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: product-security.json: 'Attackers target unpatched CryptoPayment Gateway WordPress plugin flaw exposing wallet credentials' and 'Attackers exploit new WordPress remote code execution flaw within hours of patch'; neither covers a pre-release block of a compromised developer account.

_Source: [https://thehackernews.com/2026/11/wordpress-blocks-six-backdoored-wp.html](https://thehackernews.com/2026/11/wordpress-blocks-six-backdoored-wp.html)_  ·  [← back to index](../README.md)
