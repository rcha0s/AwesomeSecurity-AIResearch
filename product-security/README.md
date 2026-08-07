# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_7 vetted findings · updated 2026-08-07 · ranked by composite · latest 31 days only · [6 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now, surfaced by the editorial pass._

- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

| Domain | Findings |
| --- | --- |
| Supply Chain & Dependencies | 1 |
| Supply Chain | 1 |
| AI coding assistant sandbox escape / path traversal | 1 |
| Malware & Wipers | 1 |
| Malware & Threat Intel | 1 |
| Developer Tooling & Template Injection | 1 |
| browser-delivered malware / malvertising | 1 |
| AI-Generated Code Risk | 1 |

## Supply Chain & Dependencies

- **[AsyncAPI npm compromise: import-time payload defeats --ignore-scripts](supply-chain-dependencies/2026-07-asyncapi-npm-compromise-import-time-payload-defeats-ignore-s.md)** · composite **68.62** · Jul 16, 2026 · 🔗 +2 sources  
  Import-time malware makes --ignore-scripts useless and a valid provenance attestation is not a trust signal when the pipeline itself is hijacked.  
  _[source](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/)_

## Supply Chain

- **[Phantom Squatting: attackers register the domains LLMs hallucinate](supply-chain/2026-07-phantom-squatting-attackers-register-the-domains-llms-halluc.md)** · composite **64.8** · Jun 30, 2026  
  LLM hallucinations are a predictable supply-chain attack surface: attackers pre-register the domains/packages models invent.  
  _[Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/)_

## AI coding assistant sandbox escape / path traversal

- **[Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')](ai-coding-assistant-sandbox-escape-path-traversal/2026-07-committed-git-symlinks-misleading-approval-dialogs-let-ai-co.md)** · composite **58.35** · Jul 9, 2026  
  A symlink committed to a repo can turn an AI coding agent into a write primitive for ~/.ssh/authorized_keys - resolve paths to canonical form and confirm they stay inside the workspace before any…  
  _[Snyk Blog](https://snyk.io/blog/symlinks-are-still-scary/)_

## Malware & Wipers

- **[GigaWiper: modular destructive malware that fakes ransomware](malware-wipers/2026-07-gigawiper-modular-destructive-malware-that-fakes-ransomware.md)** · composite **57.75** · Jul 9, 2026  
  Wiper malware is consolidating into modular platforms, and 'ransomware' may be undecryptable destruction in disguise - plan recovery accordingly.  
  _[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/)_

## Malware & Threat Intel

- **[TuxBot v3: an LLM-assisted IoT botnet shipped with the model's safety disclaimer and raw chain-of-thought still in the source](malware-threat-intel/2026-07-tuxbot-v3-an-llm-assisted-iot-botnet-shipped-with-the-model.md)** · composite **57.15** · Jul 17, 2026  
  Today's AI-assisted commodity malware is sloppy and self-labelling; budget for the version where someone spends ten more minutes prompting.  
  _[@Unit42_Intel](https://unit42.paloaltonetworks.com/tuxbot-v3-evolution-iot-botnet/)_

## Developer Tooling & Template Injection

- **[Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](developer-tooling-template-injection/2026-07-oh-my-posh-a-directory-name-runs-commands-because-the-prompt.md)** · composite **57.0** · Jul 24, 2026  
  Anything that renders your prompt, status bar or editor title is executing attacker-controlled repository metadata - treat it as a parser, not decoration.  
  _[GitHub Advisory Database](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)_

## browser-delivered malware / malvertising

- **[SourTrade: browser reassembles a Bun-based executable from split parts, defeating hash-based detection with per-session builds](browser-delivered-malware-malvertising/2026-07-sourtrade-browser-reassembles-a-bun-based-executable-from-sp.md)** · composite **55.2** · Jul 25, 2026  
  Client-side payload assembly (split parts + per-session hashing) breaks hash-based detection, so hunt the whole delivery chain and behavioral signals, not the final-file signature.  
  _[@TheHackersNews](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html)_

## AI-Generated Code Risk

- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](ai-generated-code-risk/2026-07-38-9-of-agent-generated-prs-carry-a-security-smell-but-human.md)** · composite **56.62** · Jul 19, 2026 · ⚠️ _review_  
  Gate agent PRs with automated secret and dependency-integrity checks - human review demonstrably does not catch this class, and the humans are introducing most of it.  
  _[source](https://arxiv.org/abs/2607.12428)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
