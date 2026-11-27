# Apiiro finds Claude Code permission allowlists leak secrets into public GitHub repos

**Published:** Nov 7, 2026

> **Takeaway:** Treat agent permission files, transcripts and memory files as secret-bearing like .env, and approve command patterns that reference $VARS rather than literal commands with secrets in them.

## TL;DR

When a user picks "Yes, and don't ask again", Claude Code saves the exact approved shell command, including any password or token in it, to .claude/settings.local.json in the project folder. Claude Code adds that file only to the user's global gitignore, not the repo's own, so it often gets committed. Apiiro found 1,122 real secrets in 104,185 public copies of the file, and 2,539 secrets across all agent files and git history. Common secret scanners missed 215 of the affected files because passwords inside commands do not look like known key formats.

## Lessons

- About 1.1% of public Claude Code local settings files hold a real secret, so this is a measurable leak at scale. - _"Out of 104,185 public copies of this file on GitHub, 1,122 hold a real secret."_
- Format-based secret scanners miss passwords typed inside commands (PGPASSWORD=, sshpass -p, bearer headers), so agent files need command-aware detection. - _"Of the 1,122 files with a real secret, gitleaks flagged 564 and TruffleHog 643; 215 were flagged by neither."_
- The agent itself often commits the file, because its commit instructions do not exclude its own settings file. - _"In 539 of the 1,105 repos with a real secret that we traced, a commit co-authored by Claude changed the file."_
- Approval fatigue makes it worse: larger allowlists, built up from long use of don't-ask-again, are far more likely to hold a secret. - _"One in ten files over 8 KB holds a real secret, against fewer than one in 500 under 500 bytes."_

## Threat · Conditions · Mitigations

- **Threat:** Secrets embedded in approved agent commands persist in plaintext project files. They get committed to public repos, forks and git history, or are collected by infostealer malware on developer machines.
- **Conditions:** A developer types or keeps credentials in commands the agent runs, picks "Yes, and don't ask again", and the settings file is not in the repo's own .gitignore.
- **Mitigations:** Untrack and gitignore the file per repo, rotate exposed credentials, reference secrets through environment variables or a secrets manager, approve command patterns rather than literal commands, and extend secret scanning to agent folders with rules that catch passwords inside commands.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [@shmulc via Hacker News](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)  ·  **Author:** shmulc  ·  **Retrieved:** 2026-11-08  
**Scores:** Newness 23 · Novelty 55 · Relevance 85 · Credibility 55 · **Composite 56** _(each 0-100)_  
**Tags:** `claude-code`, `secret-leakage`, `permission-allowlist`, `secret-scanning`, `coding-agents`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Claude Code GitHub issues (#5544 and others) on the mechanism; ironPeak's 100-repo sample; Lakera's credentials in npm packages; tracked Shai-Hulud and StepSecurity agent-config entries

_Source: [https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)_  ·  [← back to index](../README.md)
