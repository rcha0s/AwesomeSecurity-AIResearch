# OpenJDK Base64 decoder flaw Java4Shell corrupts memory on AVX-512 CPUs

**Published:** Nov 17, 2026

> **Takeaway:** Patch JDK 17, 21, 25 and 27 (including bundled runtimes and container images), prioritizing x86-64 hosts whose CPUs report avx512vbmi.

## TL;DR

CVE-2026-114938 is an out-of-bounds write in OpenJDK's optimized Base64 decoder, rated 9.2 (Critical) under CVSS 4.0. Malformed padding makes the output length negative, and an AVX-512 masked store then writes 62 bytes past the array. Denial of service is easy to reach, but reliable remote code execution needs extra per-application work, and the bug only fires on x86-64 CPUs with AVX-512 VBMI support.

## Lessons

- Exposure needs three things at once: an affected JDK, a CPU with AVX-512 VBMI, and attacker-controlled data reaching the basic or URL Base64 decoder. Use this to rank patching. - _"Systems running on processors that lack AVX-512 VBMI support are not affected."_
- Expect crashes (denial of service) before code execution. The overwrite is a constrained repeating byte pattern, and its damage depends on what sits next to the array in memory. - _"Denial of service is the more readily achievable impact where attacker-controlled input reaches the vulnerable decoder."_
- Catching the IllegalArgumentException does not make the input safe: the native routine already wrote outside the array, so symptoms such as a garbage-collection crash can appear far from the decoder call. - _"Catching the decoding exception leaves that damage in place."_
- If patching is delayed, -XX:-UseBASE64Intrinsics is the narrower workaround. -XX:UseAVX=2 also works on x86-64 but affects other AVX-512 code and must not be applied to ARM64 JVMs, which will not start. - _"Disabling the Base64 intrinsics is the narrower workaround."_

## Threat · Conditions · Mitigations

- **Threat:** Malformed Base64 input (for example 128 'A' characters followed by '=') drives the AVX-512 tail handler to a negative output count, so a full 64-byte masked store lands outside the destination array and corrupts adjacent heap memory.
- **Conditions:** Java 17.0.6 and later before the fixed builds (17.0.21.1, 21.0.13.1, 25.0.5.1, 27.0.1.1); x86-64 CPU with AVX-512 VBMI; the application passes attacker-controlled data to the basic or URL decoder (the MIME decoder bypasses the path). Native ARM64 JVMs are not affected.
- **Mitigations:** Update to a fixed JDK build (including bundled runtimes and container images) and restart, or temporarily start the JVM with -XX:-UseBASE64Intrinsics or, on x86-64 only, -XX:UseAVX=2.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/java4shell-remote-code-execution-in-openjdk-cve-2026-114938/)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 27 · Novelty 75.0 · Relevance 85 · Credibility 88 · **Composite 68** _(each 0-100)_  
**Tags:** `openjdk`, `java`, `memory-corruption`, `out-of-bounds-write`, `avx-512`, `base64`, `jvm-intrinsics`, `patch-prioritization`, `cve-2026-114938`  
**Also reported by:** [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/critical-java4shell-flaw-allows-rce-attacks-on-major-java-applications/), [chainguard.dev](https://www.chainguard.dev/unchained/java4shell-how-a-malformed-base64-string-breaks-the-jvm-on-avx-512), [semgrep.dev](https://semgrep.dev/blog/2026/java4shell-openjdk-base64-vulnerability), [wiz.io](https://www.wiz.io/blog/cve-2026-114938-rce-java4shell-openjdk), [thehackernews.com](https://thehackernews.com/2026/11/oracle-to-patch-11-java-flaws-today-as.html), [calif.io](https://calif.io/java4shell/), [aikido.dev](https://www.aikido.dev/blog/java-17-rce-vulnerability-cve-2026-114938) _(+7 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No earlier OpenJDK, Base64 or AVX-512 intrinsic bug in tracked data (only unrelated base64 mentions); this is a new vulnerability class with a concrete triage method (CPU flag check, intrinsic-specific flag).

_Source: [https://securitylabs.datadoghq.com/articles/java4shell-remote-code-execution-in-openjdk-cve-2026-114938/](https://securitylabs.datadoghq.com/articles/java4shell-remote-code-execution-in-openjdk-cve-2026-114938/)_  ·  [← back to index](../README.md)
