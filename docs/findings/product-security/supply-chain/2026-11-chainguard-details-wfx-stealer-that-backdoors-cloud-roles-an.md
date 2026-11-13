# Chainguard details wfx stealer that backdoors cloud roles and can forge checks

**Published:** Nov 12, 2026

> **Takeaway:** With a stolen write token, pinning and pull request review do nothing, so limit what a CI runner holds and audit cloud trust after any wfx hit.

## TL;DR

Starting November 10, 2026, an attacker used stolen GitHub tokens to open probe pull requests in 61,764 repositories from 4,837 accounts (Aikido's count). It pushed wfx, a 1,500-line shell stealer, wherever it could, then reverted the commit and deleted the workflow run within about a minute. The stealer takes Actions secrets, OIDC and runtime tokens, cloud, SSH and AI-tool credentials and runner memory. It swaps GitHub OIDC tokens for AWS, GCP and Azure sessions, and it carries code to post forged success results under the names of required checks, though StepSecurity found that feature switched off in all 101 copies it examined. For persistence it rewrites AWS role trust policies to allow any AWS account and adds wfx-ci federated credentials to Azure AD apps, both of which survive secret rotation.

## Lessons

- Required status checks are not a reliable gate against a token holder. The payload has code to post fake passing results under the required check names, so branch protection would let the change through; StepSecurity found it not yet switched on. - _"posts forged success status checks against the commit using the names of the repository's required checks"_
- The attacker deletes the workflow run and its logs, so detection depends on a gap in run numbers rather than on log content. - _"A missing run number in a workflow's history is often the only trace left."_
- Rotating secrets is not enough. Response has to audit cloud configuration too: AWS trust policies set to Principal * and Azure federated credentials let the attacker back in after rotation. - _"Rotating secrets alone does not remove a trust policy or a federated credential."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker holding stolen GitHub tokens pushes a CI stealer into every repository the tokens can write to, dumps secrets and runner memory, trades OIDC tokens for cloud sessions, forges required checks, plants cloud backdoors that survive rotation, and deletes its workflow runs.
- **Conditions:** The attacker needs a GitHub token with write access to the repository. The repository's workflows must hold secrets or have id-token permission and cloud roles that trust GitHub OIDC.
- **Mitigations:** Search for wfx-docs branches and the probe pull request title. Treat any probe author as compromised and revoke its tokens and grants. Rotate every secret the workflow could reach. Restore AWS trust policies, delete rogue IAM keys and Azure wfx-ci federated credentials, and re-run required checks. Block the exfiltration hosts. Give GITHUB_TOKEN minimal scope, keep long-lived credentials off runners, and restrict OIDC trust to specific repositories and branches.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Chainguard Unchained](https://www.chainguard.dev/unchained/wfx-loot-stolen-github-tokens-pushed-a-ci-secret-stealer-into-60-000-repositories-november-2026)  ·  **Retrieved:** 2026-11-13  
**Scores:** Newness 49 · Novelty 30 · Relevance 85 · Credibility 54 · **Composite 55** _(each 0-100)_  
**Tags:** `github-actions`, `supply-chain`, `credential-theft`, `stolen-tokens`, `oidc`, `branch-protection`, `cloud-backdoor`, `ci-runner`, `anti-forensics`  
**Also reported by:** [StepSecurity](https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: SafeDep's 'wfx stealer pushed into 8,093+ repos, likely via stolen tokens' (push-revert, OIDC exchange, Entra and AWS backdoors). Adds Aikido's larger count, forged required status checks, run deletion detectable by missing run numbers, and AWS Principal * trust rewrites.

_Source: [https://www.chainguard.dev/unchained/wfx-loot-stolen-github-tokens-pushed-a-ci-secret-stealer-into-60-000-repositories-november-2026](https://www.chainguard.dev/unchained/wfx-loot-stolen-github-tokens-pushed-a-ci-secret-stealer-into-60-000-repositories-november-2026)_  ·  [← back to index](../README.md)
