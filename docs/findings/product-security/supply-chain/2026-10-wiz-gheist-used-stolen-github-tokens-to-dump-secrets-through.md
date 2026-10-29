# Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs

**Published:** Oct 26, 2026

> **Takeaway:** A stolen GitHub token turns your own CI into a secrets-theft channel, so hunt for the sync-check pattern and replace long-lived personal access tokens with short-lived, scoped ones.

## TL;DR

Wiz Research tracked Gheist, active from September 15 and still running on October 24, which used stolen GitHub tokens to push more than 13,500 branches across more than 850 accounts, each adding a `sync-check` workflow that tries to print the repository's secrets into its own log. The tool downloads the log through the GitHub API and deletes the run seconds later, so no attacker domain is involved. GitHub's July safeguard covers only public repositories; Wiz saw private enterprise repositories hit and, within hours, the same organization's cloud credentials used to list AWS Secrets Manager.

## Lessons

- Secrets leave through GitHub's own API, so blocking outbound traffic does not help; detection has to use workflow and audit events. - _"Because the secrets leave through GitHub's own API, there is no attacker domain or outbound connection to block"_
- GitHub's public-repository safeguard does not apply once an enterprise credential is stolen. - _"once an enterprise credential is compromised, that control doesn’t apply"_
- Wiz gives concrete hunt indicators: short-lived workflow runs on ci-sync branches. - _"workflow runs on "ci-sync-*" branches that were deleted within a minute of completion"_
- Cloudsmith's security head notes that a token issued to a person months earlier still carried full write access. - _"a credential issued to a human months ago still carried full write authority"_

## Threat · Conditions · Mitigations

- **Threat:** Theft of repository and cloud secrets through malicious GitHub Actions workflows pushed with stolen tokens, followed by cloud enumeration.
- **Conditions:** A GitHub token, often from infostealer malware or an earlier supply chain compromise, with write access to repositories that hold secrets.
- **Mitigations:** Hunt for the ci-sync and sync-check indicators, rotate exposed secrets, use GitHub Apps or short-lived fine-grained tokens, and require reviewers on production environments.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Dark Reading](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets)  ·  **Retrieved:** 2026-10-27  
**Scores:** Newness 21 · Novelty 40 · Relevance 80 · Credibility 40 · **Composite 47** _(each 0-100)_  
**Tags:** `github-actions`, `token-theft`, `secrets-exfiltration`, `supply-chain`, `credential-theft`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Secrets-dumping workflows pushed with stolen tokens appeared in earlier campaigns such as GhostAction; Gheist adds log-then-delete theft with no attacker domain and reaches private enterprise repositories past GitHub's public-repository safeguard.

_Source: [https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets)_  ·  [← back to index](../README.md)
