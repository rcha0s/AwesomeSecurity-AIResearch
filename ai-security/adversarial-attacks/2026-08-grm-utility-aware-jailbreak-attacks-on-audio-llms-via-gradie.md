# GRM: Utility-Aware Jailbreak Attacks on Audio LLMs via Gradient-Ratio Masking

**Published:** Aug 10, 2026

> **Takeaway:** Full-band audio perturbations aren't needed for a strong ALLM jailbreak; a small selected set of Mel bands yields stronger stealthier attacks, undercutting simple bandwidth-based monitoring.

## TL;DR

Accepted at MM 2026. Studies universal audio perturbations that jailbreak audio LLMs. Observes that Jailbreak Success Rate is non-monotonic in perturbation bandwidth while utility degradation grows monotonically; ranks Mel bands by jailbreak-contribution / transcript-sensitivity and confines the perturbation to top bands, giving 88.46% average JSR across four ALLMs with less utility loss than full-band baselines. Code released.

## What to learn

- Jailbreak strength is non-monotonic in perturbation bandwidth while utility loss is monotonic in bandwidth. - _"Jailbreak Success Rate (JSR) varies non-monotonically, while utility degradation grows with coverage."_
- Mel bands can be ranked by contribution/sensitivity ratio and only the top bands need to carry the perturbation. - _"GRM, a utility-aware, frequency-selective jailbreak framework that ranks Mel bands by the ratio between jailbreak contribution and transcript sensitivity, confines a universal perturbation to selected bands"_
- The reported ASR is high across four different audio LLMs, suggesting cross-model transfer of the frequency-selective attack. - _"Experiments on four ALLMs show that GRM achieves an average JSR of 88.46\% while substantially reducing utility degradation across benign transcription and response tasks relative to baselines."_

## Threat · Conditions · Mitigations

- **Threat:** Audio LLMs can be jailbroken by a universal adversarial perturbation confined to a small set of Mel bands, achieving high jailbreak success (avg 88.46% across four ALLMs) while degrading benign transcription/response tasks much less than full-band attacks, making the attack harder to spot by users or automated monitoring.
- **Conditions:** Attacker can inject arbitrary audio into the ALLM input (e.g., a spoken command channel or audio file upload); attacker has enough model access to rank Mel bands by jailbreak-contribution and transcript-sensitivity gradients (paper suggests white-box or grey-box, code released); target is a modern audio-capable LLM.
- **Mitigations:** Do not rely on bandwidth-based or utility-drop-based anomaly detection alone since JSR is non-monotonic in bandwidth; add frequency-selective universal perturbations to the pre-release red-team set; run safety alignment on the audio representation directly (see CASA in this batch) rather than only on text; log input audio spectra for post-incident forensics and flag repeated Mel-band concentration patterns.

---

**Topic:** AI Security  ·  **Domain:** Adversarial Attacks  
**Source:** [source](https://arxiv.org/abs/2604.09222)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 18 · Novelty 62 · Relevance 65 · Credibility 55 · **Composite 50.85**  
**Tags:** `audio-llm`, `jailbreak`, `adversarial-perturbation`, `mel-bands`, `stealth`  
**Verification:** ✓ independently verified · closest prior art: Extends universal adversarial audio work (perturbation-based ALLM jailbreaks referenced in the abstract) with an explicit utility-vs-attack tradeoff via band selection. Novel contribution is the gradient-ratio band ranking and the empirical non-monotonicity of JSR in bandwidth.

_Source: [https://arxiv.org/abs/2604.09222](https://arxiv.org/abs/2604.09222)_  ·  [← back to index](../README.md)
