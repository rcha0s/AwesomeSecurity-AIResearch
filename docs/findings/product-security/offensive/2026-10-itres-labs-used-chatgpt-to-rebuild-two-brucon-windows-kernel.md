# ITRES Labs used ChatGPT to rebuild two BruCON Windows kernel techniques, whose source was never released, in about 24 hours

**Published:** Oct 22, 2026

> **Takeaway:** The author argues LLMs make partially disclosed exploit research much cheaper to reproduce, so release decisions for talks, binaries and repos should assume others can rebuild it.

## TL;DR

A researcher with no recent kernel experience used ChatGPT, conference slide photos, Git history and a compiled executable to rebuild two Windows kernel execution-redirection techniques shown at BruCON 2026. The original author had spent about four months on them and never released source. Both techniques reached SYSTEM on Windows 11 with VBS (virtualization-based security), HVCI (hypervisor-protected code integrity) and kernel shadow stacks enabled, after about 24 hours of recorded work. The model refused 39 times and broke working code late in the project, so the last integration step was finished by hand.

## Lessons

- Partial public material (slides, Git history, a compiled binary) was enough to reconstruct unreleased techniques with LLM help. - _"Using public research, Git history and a compiled executable, we went on to reconstruct and reproduce two of his techniques: Native SSDT and Shadow SSDT."_
- The author argues researchers should rethink how hard it is for others to weaponize partial disclosures. - _"But the assumptions about how difficult it is for someone else to turn partial published information into custom working code may no longer be valid."_
- Model refusals were frequent but inconsistent: it helped build similar functionality earlier, then refused the final integration. - _"That is approximately 13.8% of the 282 final assistant responses."_
- Offline test harnesses validated parsing logic only; real kernel effects needed a protected Windows lab with A/B/A restore checks. - _"They didn’t prove that we could modify kernel execution, restore the original state or obtain a SYSTEM identity."_

## Threat · Conditions · Mitigations

- **Threat:** Attackers with modest expertise can rebuild unreleased exploitation techniques from conference talks, deleted repos and compiled PoCs using general-purpose LLMs.
- **Conditions:** Partial technical material is public (slides, Git history, a compiled executable); the reproduced techniques still require administrator privileges to load or use the tooling.
- **Mitigations:** Researchers: avoid publishing compiled PoCs or history you do not intend to release; coordinate defensive guidance with disclosure. Defenders: keep VBS/HVCI enabled and monitor for vulnerable driver loading and admin-to-kernel paths.

---

**Topic:** Product Security  ·  **Domain:** Vulnerability Research & Red Teaming  
**Source:** [tl;dr sec (curator link)](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 26 · Novelty 55 · Relevance 72 · Credibility 70 · **Composite 55** _(each 0-100)_  
**Tags:** `windows-kernel`, `ai-assisted-exploitation`, `ssdt`, `disclosure-opsec`, `llm-refusals`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Closest pool work covers frontier AI agents compressing intrusion timelines (archive: 'Frontier AI Agents Compress a Two-Week Intrusion Into 10 Hours') and LLM research harnesses finding bugs (PwnEscape); this adds a measured case of LLM-assisted reproduction of unreleased kernel exploitation research from partial artifacts, plus refusal counts. Verifier: Earlier work showed LLMs speeding up exploit reproduction from partial information (e.g., GPT-4 one-day exploitation from CVE descriptions, Fang et al. 2024; AI-assisted n-day patch-diff reproduction). This adds a concrete kernel/HVCI case study with refusal counts, but the thesis itself is not new.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/)_  ·  [← back to index](../README.md)
