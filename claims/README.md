# 📒 Standing claims

> The findings feed tracks **what was published**. This ledger tracks **what we currently believe** — one durable claim per question, each with the evidence behind it, and each superseded answer kept underneath with the reason it fell.

_53 claims tracked · updated 2026-08-30_

**Status meanings**

| Status | Meaning |
| --- | --- |
| ✅ `current` | The standing answer. Follow this. |
| ⚖️ `contested` | Credible evidence both ways — an open question, not guidance. |
| 🪦 `superseded` | A better answer replaced it. Kept, with the reason. |
| 🪦 `refuted` | Shown to be wrong, not merely improved on. |

| Topic | Current | Contested | Retired |
| --- | --- | --- | --- |
| [AI Security](ai-security.md) | 16 | 1 | 2 |
| [Product Security](product-security.md) | 11 | 0 | 2 |
| [AI Research](ai-research.md) | 18 | 0 | 3 |

## 🔁 What changed recently

> Every time the field moved and we retired an answer. Newest first.

- **Jul 20, 2026** · refuted · [~~Assumed a clean scanner result meant a model was safe~~](ai-security.md#claim-model-scanners-are-sufficient-for-supply-chain)  
  ↳ Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.  
  ↳ **Now:** [Scanners alone aren't enough — sandbox deserialization too](ai-security.md#claim-sandbox-model-deserialization)
- **Jul 19, 2026** · superseded · [~~Assumed normal review was enough for agent PR risk~~](product-security.md#claim-human-review-catches-agent-pr-risk)  
  ↳ Measured across agent-generated PRs, 38.9% carried a security smell and human review demonstrably did not catch the secret and dependency-integrity class. Review remains valuable for logic and design, but it is not the control for this risk.  
  ↳ **Now:** [Automated gates catch what human review misses on agent PRs](product-security.md#claim-gate-agent-prs-with-automated-checks)
- **Jul 15, 2026** · refuted · [~~Assumed --ignore-scripts plus provenance was adequate~~](product-security.md#claim-ignore-scripts-blocks-npm-supply-chain)  
  ↳ The AsyncAPI compromise delivered its payload at import time, which --ignore-scripts does not prevent, and it shipped with a valid provenance attestation. Both controls target the wrong stage of the lifecycle.  
  ↳ **Now:** [Import-time npm payloads defeat --ignore-scripts and provenance](product-security.md#claim-import-time-payloads-defeat-install-time-controls)
- **Jul 4, 2026** · superseded · [~~Assumed newest model is a strict upgrade for any harness~~](ai-research.md#claim-newer-model-is-always-an-upgrade)  
  ↳ Measured on a third-party harness's custom edit tool, newer Claude models invented made-up fields that their older siblings got right. Model upgrades can regress harness-specific tool calling, so an upgrade is a change to re-evaluate, not a free win.  
  ↳ **Now:** [Model upgrades can regress on non-native tool schemas](ai-research.md#claim-match-tool-schemas-to-the-target-model)
- **May 2026** · superseded · [~~JSON assumed a neutral default for agent I/O~~](ai-research.md#claim-json-default-for-all-agent-io)  
  ↳ Format choice measurably moves cost: uniform arrays serialize 30-60% smaller in TOON at comparable retrieval accuracy, which makes serialization a real optimization lever on the input side rather than an aesthetic preference.  
  ↳ **Now:** [TOON beats JSON on input-side token cost](ai-research.md#claim-toon-cuts-input-tokens-vs-json)
- **May 2026** · refuted · [~~Assumed a good classifier plus instruction hierarchy solves injection~~](ai-security.md#claim-prompt-injection-solvable-by-filtering)  
  ↳ Impossibility result: an adversary can always construct a context under which a blocked flow looks legitimate, and a defender who tightens norms to stop it starts blocking genuinely legitimate flows. Large-scale red teaming confirmed the vulnerability persists across model families, so filtering is a cost-raiser, not a solution.  
  ↳ **Now:** [Prompt injection can't be closed by filtering alone](ai-security.md#claim-prompt-injection-is-containment-not-prevention)
- **Mar 2026** · refuted · [~~Assumed TOON's input savings would carry to generation~~](ai-research.md#claim-toon-best-for-structured-output-generation)  
  ↳ Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on simple structures. The input-side token saving does not transfer to the output side.  
  ↳ **Now:** [Constrained decoding wins for structured output, not TOON](ai-research.md#claim-constrained-decoding-for-structured-output)

---

[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md)
