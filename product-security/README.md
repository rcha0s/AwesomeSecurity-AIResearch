# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_6 vetted findings · updated 2026-07-26 · ranked by composite · latest 31 days only · [5 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas — what the field is watching now, surfaced by the editorial pass._

- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

| Domain | Findings |
| --- | --- |
| Supply Chain & Dependencies | 1 |
| Supply Chain | 1 |
| AI coding assistant sandbox escape / path traversal | 1 |
| Malware & Wipers | 1 |
| Application Security | 1 |
| browser-delivered malware / malvertising | 1 |

## Supply Chain & Dependencies

- **[AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](supply-chain-dependencies/2026-07-asyncapi-npm-compromise-import-time-payload-defeats-ignore-s.md)** · composite **70.38** · Jul 16, 2026 · 🔗 +2 sources  
  Import-time malware makes --ignore-scripts useless and a valid provenance attestation is not a trust signal when the pipeline itself is hijacked.  
  _[source](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/)_

## Supply Chain

- **[Phantom Squatting: attackers register the domains LLMs hallucinate](supply-chain/2026-07-phantom-squatting-attackers-register-the-domains-llms-halluc.md)** · composite **66.55** · Jun 30, 2026  
  LLM hallucinations are a predictable supply-chain attack surface: attackers pre-register the domains/packages models invent.  
  _[Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/)_

## AI coding assistant sandbox escape / path traversal

- **[Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](ai-coding-assistant-sandbox-escape-path-traversal/2026-07-committed-git-symlinks-misleading-approval-dialogs-let-ai-co.md)** · composite **60.1** · Jul 9, 2026  
  A symlink committed to a repo can turn an AI coding agent into a write primitive for ~/.ssh/authorized_keys — resolve paths to canonical form and confirm they stay inside the workspace before any…  
  _[Snyk Blog](https://snyk.io/blog/symlinks-are-still-scary/)_

## Malware & Wipers

- **[GigaWiper: modular destructive malware that fakes ransomware](malware-wipers/2026-07-gigawiper-modular-destructive-malware-that-fakes-ransomware.md)** · composite **59.5** · Jul 9, 2026  
  Wiper malware is consolidating into modular platforms, and 'ransomware' may be undecryptable destruction in disguise — plan recovery accordingly.  
  _[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/)_

## Application Security

- **[Kemp LoadMaster pre-auth RCE: uninitialized heap + missing null byte (CVE-2026-8037)](application-security/2026-06-kemp-loadmaster-pre-auth-rce-uninitialized-heap-missing-null.md)** · composite **58.1** · Jun 29, 2026  
  A minimal 'just null-terminate the buffer' patch can hide a pre-auth RCE — diff patches carefully, and treat missing null-termination next to attacker-controlled heap data as exploitable, not…  
  _[source](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/)_

## browser-delivered malware / malvertising

- **[SourTrade: browser reassembles a Bun-based executable from split parts, defeating hash-based detection with per-session builds](browser-delivered-malware-malvertising/2026-07-sourtrade-browser-reassembles-a-bun-based-executable-from-sp.md)** · composite **56.95** · Jul 25, 2026  
  Client-side payload assembly (split parts + per-session hashing) breaks hash-based detection, so hunt the whole delivery chain and behavioral signals, not the final-file signature.  
  _[@TheHackersNews](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html)_

---

[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md) · [Learnings](../LEARNINGS.md)
