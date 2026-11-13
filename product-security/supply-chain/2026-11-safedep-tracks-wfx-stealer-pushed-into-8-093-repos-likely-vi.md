# SafeDep tracks wfx stealer pushed into 8,093+ repos, likely via stolen tokens

**Published:** Nov 12, 2026

> **Takeaway:** If any repo you own got a wfx-docs PR or a reverted 'ci: refresh build cache' commit, revoke the author's tokens, rotate all reachable secrets and hunt for AWS/Entra backdoors.

## TL;DR

Between November 10 and 12, 2026, an attacker pushed the wfx credential stealer into at least 8,093 public repositories, likely using stolen GitHub tokens (unsigned commits point to them). The count is a lower bound (public default branches only, campaign still active); most pushes injected steps into existing workflows, 771 used an npm `postinstall` hook, and the attacker usually reverted the commit minutes later so the branch looked clean. The payload exfiltrates all repository secrets, Actions runtime tokens, in-memory API keys and local credential files, requests OpenID Connect (OIDC) tokens for AWS, Azure and Google Cloud Platform (GCP), and tries to leave AWS access keys and Entra federated credentials as backdoors that would survive secret rotation. Poisoned versions also shipped on Packagist (neuronai-studio v3.14.3) and the Go proxy (gocurl, redock), though normal `composer require` or `go get` does not run the payload.

## Lessons

- Push-run-revert hides the compromise from anyone looking at the current branch; detection has to use commit history, Actions run logs and audit events. - _"In almost all repositories the attacker then reverts the commit, so the branch looks clean."_
- Rotating secrets is not enough: an OpenID Connect (OIDC) federated credential added to an Entra app keeps granting access to any workflow on main. - _"Any workflow on the repository’s `main` branch can then log in to Azure as that app, even after you rotate client secrets."_
- The payload tries cloud OpenID Connect (OIDC) exchange blindly; `id-token: write` appeared in the attacker's new-workflow file, while whether code injected elsewhere gets an OIDC token depends on the host workflow's permissions. - _"it requests GitHub OIDC tokens for AWS, Azure and GCP and tries to use them, even when the repository has no cloud setup."_
- The `wfx-docs` probe pull request is itself an indicator of a stolen token, even where no payload followed. - _"A probe pull request on its own means the account is compromised, even if no payload commit followed."_

## Threat · Conditions · Mitigations

- **Threat:** Likely stolen GitHub tokens are used to inject a CI and npm postinstall stealer that exfiltrates repository secrets and cloud credentials and tries to leave persistent AWS and Azure backdoors, then reverts the commit to hide it.
- **Conditions:** A GitHub account token with write access to a repository; workflows that run on push, or npm install of an affected commit; cloud OIDC trust configured for the repository increases impact.
- **Mitigations:** Revoke the commit author's tokens and sessions and enforce 2FA, rotate all repository, environment and organization secrets, delete wfx-docs branches and probe PRs, republish packages built during the window from clean commits, audit AWS keys and trust policies and Entra federated credentials, and treat machines that ran npm install on affected commits as compromised.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [SafeDep](https://safedep.io/blog/github-actions-wfx-credential-stealer)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 49 · Novelty 40 · Relevance 85 · Credibility 57 · **Composite 58** _(each 0-100)_  
**Tags:** `github-actions`, `supply-chain`, `credential-theft`, `stolen-tokens`, `oidc`, `postinstall`, `cloud-backdoor`, `packagist`, `go-modules`  
**Also reported by:** [StepSecurity](https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Wiz's Gheist campaign (stolen GitHub tokens pushing secret-dumping workflows across 850+ accounts), Shai-Hulud worms and tj-actions/changed-files secret exfiltration already in the tracker. New here: commit-then-revert concealment at 8,000+ repo scale, blind OIDC exchange to AWS/Azure/GCP/Vault/Kubernetes, and rotation-surviving Entra federated-credential and AWS key backdoors, plus poisoned Packagist/Go releases. Verifier's closest: Wiz Gheist entry (stolen GitHub tokens dumping secrets via Actions); GhostAction; Mini Shai-Hulud.

_Source: [https://safedep.io/blog/github-actions-wfx-credential-stealer](https://safedep.io/blog/github-actions-wfx-credential-stealer)_  ·  [← back to index](../README.md)
