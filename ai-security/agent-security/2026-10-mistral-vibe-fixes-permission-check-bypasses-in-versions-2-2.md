# Mistral Vibe fixes permission-check bypasses in versions 2.25.4 and 2.25.5

**Published:** Oct 13, 2026

> **Takeaway:** A permission gate that approves a command from a parser that disagrees with the shell is a bypass; upgrade Vibe and fail closed on parse errors.

## TL;DR

VulnCheck's 2026-10-13 advisory for CVE-2026-109428 shows Mistral Vibe approving a command from the part tree-sitter-bash extracted (an allowlisted cd) while bash joins a backslash-newline into a hidden curl, CVSS 4.0 of 8.7; fixed in 2.25.5. CVE-2026-109429 (command substitution hidden in a single-quoted variable value) is fixed in 2.25.4. HiddenLayer's 2026-09-11 advisories added CVE-2026-87984 to CVE-2026-87988, including unparsable shell syntax approved without a prompt (CVE-2026-87986, CVSS 4.0 of 10). All ids were confirmed at NVD.

## Lessons

- The approval check and the shell read the same string differently, so an allowlisted prefix hid an unapproved command. - _"Attackers can craft a command string where tree-sitter-bash extracts only an allowlisted prefix such as cd while bash joins the line continuation into a materially different and hidden command such as a curl request"_
- Mistral Vibe versions before 2.25.5 are affected, so the fix is an upgrade. - _"Mistral Vibe before 2.25.5 contains a permission validation bypass vulnerability"_

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [vulncheck.com](https://www.vulncheck.com/advisories/mistral-vibe-permission-bypass-via-bash-line-continuation)  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 19 · Novelty 60 · Relevance 85 · Credibility 55 · **Composite 56** _(each 0-100)_  
**Tags:** `mistral-vibe`, `coding-agents`, `permission-bypass`, `tree-sitter`, `command-allowlist`, `cve`  
**Also reported by:** [HiddenLayer: unparsable shell constructs auto-approved (CVE-2026-87986)](https://www.hiddenlayer.com/sai-security-advisory/2026-09-mistral-vibe4) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Roo Code's seven auto-approve bypasses in the same pool show the same parser-differential pattern in another coding agent.

_Source: [https://www.vulncheck.com/advisories/mistral-vibe-permission-bypass-via-bash-line-continuation](https://www.vulncheck.com/advisories/mistral-vibe-permission-bypass-via-bash-line-continuation)_  ·  [← back to index](../README.md)
