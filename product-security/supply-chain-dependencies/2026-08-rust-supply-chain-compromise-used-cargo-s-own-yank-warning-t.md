# Rust Supply-Chain Compromise Used Cargo's Own Yank Warning to Socially Engineer Developers Into the Malicious Version

**Published:** Aug 20, 2026

> **Takeaway:** Yanking prior clean versions of a compromised crate is a novel, low-effort social-engineering step that weaponizes the package manager's own UX (Cargo's "consider updating to a version that is not yanked" warning) to actively push developers toward the malicious release, rather than passively waiting for auto-upgrades - a supply-chain defense that only watches for new/anomalous versions misses this.

## TL;DR

A compromised maintainer account published a malicious arrayref 0.3.10 (245M+ all-time downloads, used transitively through tiny-skia/winit/egui/iced) depending on a typosquatted proc-macro1 crate impersonating dtolnay. The attacker yanked the prior clean releases (0.3.5-0.3.9), which makes Cargo print a warning nudging developers toward the only non-yanked version - the malicious one. proc-macro1's build script fetched a certificate-validation-free, base64-fragment-obfuscated payload URL and ran an architecture-specific binary detached from the build process at compile time.

## What to learn

- The attacker yanked all prior clean releases (0.3.5 through 0.3.9), which causes Cargo to print a warning nudging developers to update to the only remaining, non-yanked (malicious) version - turning the package manager's own UX into part of the attack. - _"The owner account yanked the older `arrayref` releases 0.3.5 through 0.3.9. Yanking a crate makes Cargo print a “consider updating to a version that is not yanked” warning, which nudges developers toward the only non-yanked release, the malicious 0.3.10. The reporter who filed the RustSec advisory noted this is how they hit it."_
- The malicious proc-macro1 crate impersonated a well-known Rust maintainer via a lookalike username (dtolney vs. the real dtolnay) and forged the authors metadata field with that maintainer's real name. - _"A separate account, `dtolney`, published `proc-macro1`. The username closely resembles David Tolnay’s real `dtolnay` account. Its metadata forges `authors = ["David Tolnay <rchaitm@gmail.com>"]`"_
- The malicious crate's actual source code was a genuine, unmodified copy of the legitimate proc-macro2 crate, specifically so that builds kept working normally while the separate build-time payload ran undetected. - _"The `src/` of the malicious `proc-macro1` is a genuine copy of `proc-macro2`, so builds kept working while the build script ran."_
- The build-time payload fetches an architecture-specific binary over TLS with no certificate validation, using a URL reassembled from base64-encoded fragments embedded in the build script, then runs it detached so the compiler doesn't wait for it to finish. - _"The script fetches an architecture-specific binary over a TLS connection that accepts any certificate without validation, then runs it detached from the build. On Unix it drops and runs `/tmp/rust-setup`."_

---

**Topic:** Product Security  ·  **Domain:** Supply Chain & Dependencies  
**Source:** [source](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/)  ·  **Author:** abhisek  ·  **Retrieved:** 2026-09-09  
**Scores:** Newness 11 · Novelty 65 · Relevance 70 · Credibility 55 · **Composite 51.5**  
**Tags:** `rust`, `cargo`, `supply-chain`, `typosquatting`, `build-time-malware`, `arrayref`  
**Verification:** ✓ independently verified · closest prior art: Build-time RCE via a typosquatted crate's build.rs is a known pattern; using the registry's own yank-warning UX as an active lure toward the malicious version is the genuinely new wrinkle.

_Source: [https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/)_  ·  [← back to index](../README.md)
