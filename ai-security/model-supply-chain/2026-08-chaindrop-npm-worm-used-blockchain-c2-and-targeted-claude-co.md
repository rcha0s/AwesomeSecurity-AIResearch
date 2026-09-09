# ChainDrop npm Worm Used Blockchain C2 and Targeted Claude Code / VS Code Configs, Stealing OIDC Tokens from Live CI Runner Memory

**Published:** Aug 21, 2026

> **Takeaway:** Supply-chain worms are now targeting AI coding-agent configuration files as a persistence vector, not just credentials - and using decentralized blockchain C2 to resist takedown, which existing npm-hardening advice (--ignore-scripts, cooldowns) doesn't fully address once it establishes IDE-level persistence.

## TL;DR

Unit 42's SDLC supply-chain roundup details the ChainDrop npm worm, which infected 400+ packages (including popular ones like keyv and cacheable-request) via a preinstall script, then read live process memory on GitHub Actions runners to steal OIDC tokens, backdoored local Claude Code/VS Code configs for persistence, and ran its C2 over Ethereum blockchain transactions.

## What to learn

- ChainDrop's theft stage went beyond scraping files on disk - a hidden Python script read live process memory on GitHub Actions runners directly to steal temporary OIDC tokens and secrets. - _"Rather than just scraping disk files, a hidden Python script directly read live process memory from GitHub Actions runners to steal temporary OpenID Connect (OIDC) tokens and secrets, alongside a massive sweep for local developer credentials."_
- The worm secured long-term persistence by modifying local developer tool configs, specifically calling out Claude Code and VS Code, and ran its C2 infrastructure dynamically over Ethereum blockchain transactions to resist takedown. - _"ChainDrop secured long-term persistence by establishing cross-linked hooks directly inside developer tools like VS Code and Claude Code, while managing its entire command-and-control (C2) infrastructure dynamically through Ethereum blockchain transactions."_
- Unit 42's hardening recommendation acknowledges --ignore-scripts as one of several mitigations, alongside ephemeral CI/CD servers, dependency cooldowns, and SHA-pinning, rather than a standalone fix - consistent with the existing pool finding that install-time controls alone are insufficient against import-time or memory-resident payloads. - _"organizations must lock down the developer environment by disabling lifecycle install scripts (--ignore-scripts), enforcing package cooldown periods, restricting CI/CD egress traffic, using ephemeral CI/CD servers and pinning dependencies down to exact commit SHAs."_

---

**Topic:** AI Security  ·  **Domain:** Model Supply Chain  
**Source:** [source](https://unit42.paloaltonetworks.com/sdlc-supply-chain/)  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 11 · Novelty 62 · Relevance 78 · Credibility 77 · **Composite 56.27**  
**Tags:** `npm`, `supply-chain`, `chaindrop`, `blockchain-c2`, `oidc`, `ci-cd`, `claude-code`  
**Verification:** ✓ independently verified · closest prior art: Unit 42's own prior Shai-Hulud npm worm and Axios supply-chain writeups cover preinstall-script/credential-theft mechanics generally.

_Source: [https://unit42.paloaltonetworks.com/sdlc-supply-chain/](https://unit42.paloaltonetworks.com/sdlc-supply-chain/)_  ·  [← back to index](../README.md)
