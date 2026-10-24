# OVHcloud CLI: attacker swapped binaries on five GitHub releases for 94 minutes, delivering the GlassWorm loader

**Published:** Oct 24, 2026

> **Takeaway:** Release binaries can be replaced after publication, so pin and verify checksums or provenance for downloaded CLIs instead of trusting the release tag.

## TL;DR

An attacker replaced the binaries on five OVHcloud CLI GitHub releases, kept them live for 94 minutes, then deleted the evidence. StepSecurity rebuilt the attacker's build, recovered the GlassWorm loader from an orphaned commit, and ran the full chain in isolation. Their replay shows the install.sh script never served arm64 Linux, Homebrew was not an infection path, and running the CLI's version command was enough to spot the malicious build.

## Lessons

- Release assets can be swapped after publication and the evidence deleted, so a short exposure window can leave few traces. - _"An attacker swapped the binaries on five OVHcloud CLI releases, stayed live for 94 minutes, and deleted the evidence."_
- Deleted malicious code could still be recovered from an orphaned commit, which made a full detonation possible. - _"recovered the GlassWorm loader from an orphaned commit, and detonated the full chain in an isolated chamber"_
- Exposure depends on install channel: Homebrew was not affected, and a simple version check identifies the bad build. - _"Homebrew was never a path in, and a single ovhcloud version command was enough to spot the malicious build"_

## Threat · Conditions · Mitigations

- **Threat:** Attacker with release-write access replaces signed-off binaries on existing GitHub releases with builds that drop the GlassWorm loader, then deletes traces.
- **Conditions:** Users or CI pipelines that downloaded OVHcloud CLI binaries from the affected GitHub releases (or via install.sh on exposed platforms) during the 94-minute window.
- **Mitigations:** Check the installed build with `ovhcloud version`; reinstall from a known-good release; pin checksums or verify provenance for release-asset downloads; restrict and monitor release-edit permissions.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [StepSecurity](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 27 · Novelty 45 · Relevance 75 · Credibility 60 · **Composite 52** _(each 0-100)_  
**Tags:** `github-releases`, `release-asset-swap`, `glassworm`, `cli-supply-chain`, `incident-response`  
**Also reported by:** [www.darkreading.com](https://www.darkreading.com/cyberattacks-data-breaches/ovhcloud-github-compromise-glassworm-threat-actors) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest pool entry is the LiteLLM 1.107.0 trojanized PyPI/Docker release (built from a lookalike repo); release-asset swaps on GitHub are a known vector, but the reconstructed detonation and per-channel exposure analysis are new. Verifier: Release/tag tampering of trusted artifacts is well established (tj-actions/changed-files tag repoint 2025, Codecov bash uploader 2021, GlassWorm campaigns on OpenVSX/npm); the delta is a mutated GitHub release asset swap on a cloud vendor CLI plus a forensic replay recovering the loader from an orphaned commit.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm)_  ·  [← back to index](../README.md)
