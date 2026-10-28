# EDK2 network boot flaw lets attackers run code before Secure Boot

**Published:** Oct 27, 2026

> **Takeaway:** Any server fleet that network-boots on EDK2-based firmware has a pre-OS code-execution hole, so disable PXE where you can and push your firmware vendors for updates.

## TL;DR

CVE-2026-97631 (severity 9.5) is a 16-year-old buffer overflow in the network boot (PXE) driver of TianoCore EDK2. EDK2 is the open source base most UEFI (Unified Extensible Firmware Interface) firmware is built on. During network boot, an oversized ICMP error message overflows a 504-byte field, which can let an attacker run code at the highest CPU privilege before Secure Boot and TPM (Trusted Platform Module) protections apply. The planned coordinated disclosure broke early when a vendor's public pull request published the fix, and the article says an attacker needs some control over a local network and an exploit tuned to each target.

## Lessons

- The bug is a bounds error in copying ICMP error messages during PXE boot. - _"for a message longer than 504 bytes it still copies bytes into the field"_
- Fuzzing campaigns started after the similar PixieFail bug did not find this flaw. - _"It appears those efforts failed to find this latest flaw."_
- Exploits must be tuned to each firmware build, which limits mass exploitation. - _"but it needs to be tuned for each target model/version/configuration since the addresses will change based on those"_
- Turning off network boot is the main interim mitigation, since Secure Boot and TPM do not stop this bug. - _"they should consider turning off network boot capabilities at least temporarily if possible"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker on the local network sends an oversized ICMP error during PXE boot and overflows the driver buffer. This gives ring-0 code execution before Secure Boot and TPM protections, which could defeat disk encryption, or simply hangs the boot.
- **Conditions:** Machines whose firmware is built on EDK2 with PXE network boot enabled (on by default) and that boot from the network, with the attacker on the network and knowing the target firmware build. Machines that boot only from disk are not affected.
- **Mitigations:** Apply the BIOS/UEFI update from your firmware vendor, temporarily disable network boot where possible, keep TPM and Secure Boot enabled, and monitor logs for exploitation attempts.

---

**Topic:** Product Security  ·  **Domain:** Cloud, Network & Infrastructure  
**Source:** [Ars Technica Security](https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/)  ·  **Retrieved:** 2026-10-28  
**Scores:** Newness 21 · Novelty 60 · Relevance 70 · Credibility 52 · **Composite 52** _(each 0-100)_  
**Tags:** `uefi`, `edk2`, `pxe`, `firmware`, `secure-boot`, `buffer-overflow`, `embargo-break`, `servers`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No UEFI, EDK2 or PXE entries in the pools. The source names PixieFail, an earlier EDK2 PXE flaw class, as the closest precedent.

_Source: [https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/](https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/)_  ·  [← back to index](../README.md)
