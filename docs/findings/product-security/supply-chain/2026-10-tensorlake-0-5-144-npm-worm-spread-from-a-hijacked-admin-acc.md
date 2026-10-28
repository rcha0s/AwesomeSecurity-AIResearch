# tensorlake@0.5.144 npm worm spread from a hijacked admin account

**Published:** Oct 8, 2026

> **Takeaway:** Provenance attestations and 'verified' commit badges prove where a build came from, not that the source is clean; and in this worm family, revoking the stolen GitHub token before removing gh-token-monitor wipes the victim's home directory.

## TL;DR

On 7 October 2026 an attacker using a tensorlake repository admin account committed a Mini Shai-Hulud payload to main through the GitHub web UI (so every commit showed as 'verified'), then started the release workflow by hand. Version 0.5.144 (about 106,000 monthly downloads) shipped through npm trusted publishing with valid provenance and no stolen npm token. Its preinstall loader skips CI, downloads Bun, and runs an 856 KB worm. The worm steals cloud, GitHub, npm, SSH, browser and wallet credentials and republishes the victim's npm packages. It plants Claude Code and VS Code hooks, resolves its command-and-control (C2) server through an Ethereum contract, and installs a gh-token-monitor service that runs rm -rf ~/ when the stolen GitHub token stops working.

## Lessons

- No registry credential was needed: control of a repo admin account plus the project's own release workflow was enough to publish. - _"The attacker did not need an npm token. They used a repository administrator account to commit the payload to `main` through the GitHub web interface."_
- Trusted publishing and SLSA provenance faithfully attest a poisoned build; they do not indicate the source is safe. - _"The provenance is valid for a build of poisoned source."_
- Commits made in the GitHub web UI are signed by GitHub, so the 'verified' badge gives no signal about account compromise. - _"GitHub signs web interface commits, so all eight show as verified."_
- Incident response order matters: the dead-man switch fires on revocation, so remove the monitor service first, then rotate tokens. - _"If GitHub returns 40x, for example after revocation, it deletes the home directory."_

## Threat · Conditions · Mitigations

- **Threat:** Compromised maintainer/admin GitHub account publishes a credential-stealing, self-propagating npm worm through the project's legitimate release pipeline.
- **Conditions:** Developer workstation (loader exits on CI) runs npm install of tensorlake@0.5.144 with install scripts enabled; the destructive watcher arms when a stolen GitHub token belongs to an account with no organizations.
- **Mitigations:** Pin tensorlake to 0.5.143 or upgrade to the reverted 0.5.145; set ignore-scripts for installs; remove gh-token-monitor before rotating credentials; enforce branch protection and release approvals so an admin account alone cannot ship from main.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [SafeDep](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 21 · Novelty 40 · Relevance 85 · Credibility 53 · **Composite 51** _(each 0-100)_  
**Tags:** `npm`, `shai-hulud`, `worm`, `trusted-publishing`, `provenance`, `account-takeover`, `credential-theft`, `blockchain-c2`, `dead-mans-switch`, `claude-code-hooks`  
**Also reported by:** [StepSecurity](https://www.stepsecurity.io/blog/tensorlake-npm-compromised-hostage-token-worm) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Same worm family as the keyv/cacheable Mini Shai-Hulud compromise and ChainDrop already in the archive (valid provenance, Bun loader, Ethereum-resolved C2, Claude Code/VS Code hooks). New here: delivery through an admin account's web-UI commits and a manually started trusted-publishing run instead of a stolen npm token, a new C2 domain and Ethereum contract, a browser password stealer, eval of C2 responses, and an identified rm -rf ~/ handler that arms only for tokens whose account has no organizations.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud)_  ·  [← back to index](../README.md)
