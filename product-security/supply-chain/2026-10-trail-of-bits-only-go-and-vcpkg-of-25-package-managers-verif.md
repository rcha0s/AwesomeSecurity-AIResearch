# Trail of Bits: only Go and vcpkg of 25 package managers verified every download from malicious repositories; only Go checked signatures by default

**Published:** Oct 14, 2026

> **Takeaway:** A committed lockfile doesn't protect you from a compromised registry unless your package manager actually enforces its hashes; check yours and turn on the strict flag.

## TL;DR

Trail of Bits built a Docker and mitmproxy harness that played a compromised package repository and injected malware into real packages. Of 25 package managers, fewer than half verified lockfile hashes by default, and only Go and vcpkg verified every package they downloaded. Some lockfiles carry hashes that don't protect integrity: Pub warns on a mismatch but installs anyway, Conan's MD5 revision is an identifier, and CocoaPods and Composer hashes don't cover the fetched code.

## Lessons

- Integrity by default is rare: only two of 25 package managers verified every package they downloaded. - _"fewer than half used lockfiles that checked for tampering by default, and only two verified the integrity of every package they downloaded"_
- A hash in the lockfile is not enough: Pub detects a mismatch, rewrites the lockfile and installs the tampered package unless you pass --enforce-lockfile. - _"If there is a mismatch, Pub detects the error, but installs the package anyway."_
- pnpm had the same overwrite-on-mismatch default until version 11.4 in May 2026. - _"Overwriting the lockfile after a hash mismatch was also the default behavior in pnpm until version"_
- Commit or tag hashes that don't cover the downloaded artifact give no protection: Composer pins a commit but downloads a ZIP that can't be checked against it. - _"Once again, GitHub could serve a malicious ZIP archive without detection by Composer."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker who compromises a package repository or its web front end can serve modified packages that most package managers install without detecting tampering.
- **Conditions:** Package managers that lack lockfile hashes, don't verify them by default, or whose hashes don't cover the downloaded artifact; cpanminus additionally fetches over plain HTTP.
- **Mitigations:** Commit lockfiles and install in strict or frozen mode, enable signature verification where supported, mirror or vendor dependencies for ecosystems without integrity checks, and switch cpanminus to HTTPS mirrors.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Trail of Bits](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 25 · Novelty 50 · Relevance 80 · Credibility 70 · **Composite 56** _(each 0-100)_  
**Tags:** `supply-chain`, `package-managers`, `lockfiles`, `integrity`, `signatures`, `registry-compromise`, `pnpm`, `pub`, `composer`, `cpanminus`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Prior work covers maintainer compromise and install-time code execution (pool claim package-installers-run-arbitrary-code-by-default) and the Gamage et al. lockfile study; this is the first cross-ecosystem dynamic test of 25 managers against a malicious repository, with per-manager verdicts.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)_  ·  [← back to index](../README.md)
