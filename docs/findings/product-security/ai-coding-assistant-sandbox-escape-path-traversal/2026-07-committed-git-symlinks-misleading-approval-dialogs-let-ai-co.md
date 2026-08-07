# Committed git symlinks + misleading approval dialogs let AI coding assistants read/write files outside the workspace (Wiz 'GhostApproval')

**Topic:** Product Security  ·  **Domain:** AI coding assistant sandbox escape / path traversal  
**Source:** [Snyk Blog](https://snyk.io/blog/symlinks-are-still-scary/)  ·  **Published:** Jul 9, 2026  ·  **Retrieved:** 2026-07-26  
**Scores:** 🆕 Newness 12 · ✨ Novelty 70 · 🎯 Relevance 82 · 🏛️ Credibility 55 · **Composite 56.85**  
**Tags:** `prompt-injection`, `supply-chain`, `path-traversal`, `symlink`, `ai-coding-assistant`, `sandbox-escape`, `agent-security`  
**Verification:** ✓ independently verified · closest prior art: Classic symlink path-traversal / TOCTOU (CWE-59) and git's long-known preservation of symlinks; the new delta is the class-wide application to AI coding-assistant sandbox escapes plus the misleading approval-dialog (Wiz 'GhostApproval') trust gap across six assistants.

> **Takeaway:** A symlink committed to a repo can turn an AI coding agent into a write primitive for ~/.ssh/authorized_keys - resolve paths to canonical form and confirm they stay inside the workspace before any read/write.

## TL;DR

_The gist, not every detail - read the [full source](https://snyk.io/blog/symlinks-are-still-scary/) for the complete write-up._

Git faithfully recreates symlinks stored in a repo (file mode 120000, blob is just the target path as text), so a file with an innocent name like project_settings.json can secretly point at ~/.ssh/authorized_keys or ~/.zshrc. When an AI coding assistant is asked to 'set up the workspace' and follows repo instructions, it follows the symlink transparently out of the sandbox, and the human approval dialog shows the benign in-repo name rather than the true resolved target. Wiz Research's GhostApproval tested six major assistants - Amazon Q Developer, Claude Code, Augment, Cursor, Google Antigravity, and Windsurf - and found all vulnerable.

## What to learn

- Git preserves symlinks: mode 120000 stores only the target path as plain text, so a cloned repo can drop a pointer into your home directory under an innocent filename. - _"git faithfully recreates the symlink on your disk. You now have a file in your working copy, with an innocent JSON name, that is secretly a pointer into your home directory."_ ✅
- The exploit chains three failures: prompt injection in repo instructions, symlink-following without canonical path resolution, and an approval dialog that misrepresents the real target. - _"project_settings.json is a file whose entire contents are the string"_ ✅
- The agent's own reasoning identified the true target, but the human was shown only the benign in-repo filename - a UI/trust gap, not just a parsing bug. - _"the human said, simply: "Make this edit to project_settings.json ?" The agent knew. You didn"_ ✅
- All six tested AI coding assistants were affected, making this a class-wide weakness rather than a single-vendor bug. - _"Amazon Q Developer, Claude Code, Augment, Cursor, Google Antigravity, and Windsurf"_ ✅
- Mitigation is canonical path resolution plus a containment check; on Linux openat2() with RESOLVE_BENEATH/RESOLVE_NO_SYMLINKS enforces it atomically. - _"Resolve every path to its canonical location before you open it, and check that the resolved path is still inside the workspace you meant to operate in."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** A malicious or compromised public repo ships symlinks (mode 120000) under benign names; an AI coding assistant following repo/README instructions reads secrets or writes attacker-controlled content (SSH authorized_keys, shell rc files) outside its workspace, yielding credential theft or code execution - while the approval dialog shows only the harmless in-repo path.
- **Conditions:** Developer clones an untrusted repo and asks the assistant to 'set up the workspace' or follow README instructions; The assistant follows filesystem symlinks without resolving/validating the canonical path against the workspace boundary; Filesystem supports symlinks and core.symlinks is enabled (default on Unix)
- **Mitigations:** Canonicalize paths and enforce workspace-containment before every file open (openat2 RESOLVE_BENEATH / RESOLVE_NO_SYMLINKS on Linux); Show the resolved absolute target (not the repo-relative alias) in approval dialogs; Scan freshly cloned untrusted repos for symlinks: `find . -type l`, `git ls-files -s | grep ^120000`; Disable or gate symlink following for agent file tools; treat out-of-tree targets as high-risk requiring explicit confirmation; Reference precedent: CVE-2024-32002 (git submodule symlink RCE), CVE-2021-32803 (tar symlink extraction)

---

_Source: [https://snyk.io/blog/symlinks-are-still-scary/](https://snyk.io/blog/symlinks-are-still-scary/)_  ·  [← back to index](../README.md)
