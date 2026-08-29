# 📒 Standing claims

> The findings feed tracks **what was published**. This ledger tracks **what we currently believe** — one durable claim per question, each with the evidence behind it, and each superseded answer kept underneath with the reason it fell.

_52 claims tracked · updated 2026-08-29_

**Status meanings**

| Status | Meaning |
| --- | --- |
| ✅ `current` | The standing answer. Follow this. |
| ⚖️ `contested` | Credible evidence both ways — an open question, not guidance. |
| 🪦 `superseded` | A better answer replaced it. Kept, with the reason. |
| 🪦 `refuted` | Shown to be wrong, not merely improved on. |

| Topic | Current | Contested | Retired |
| --- | --- | --- | --- |
| [AI Security](ai-security.md) | 15 | 1 | 2 |
| [Product Security](product-security.md) | 11 | 0 | 2 |
| [AI Research](ai-research.md) | 18 | 0 | 3 |

## 🔁 What changed recently

> Every time the field moved and we retired an answer. Newest first.

- **Jul 20, 2026** · refuted · [~~A clean model-scanner result is adequate evidence that a third-party model artifact is safe to load.~~](ai-security.md#claim-model-scanners-are-sufficient-for-supply-chain)  
  ↳ Pickle-VM import tricks evaded ten separate model scanners and four model hubs. A clean scan result no longer distinguishes a safe artifact from an evasive one, so scanning cannot be the admission gate.  
  ↳ **Now:** [Prefer non-executable model formats and sandbox deserialization of any third-party model — a clean scanner result is weak evidence of safety.](ai-security.md#claim-sandbox-model-deserialization)
- **Jul 19, 2026** · superseded · [~~Normal human code review is sufficient to catch the security problems in agent-generated pull requests.~~](product-security.md#claim-human-review-catches-agent-pr-risk)  
  ↳ Measured across agent-generated PRs, 38.9% carried a security smell and human review demonstrably did not catch the secret and dependency-integrity class. Review remains valuable for logic and design, but it is not the control for this risk.  
  ↳ **Now:** [Agent-generated PRs need automated secret and dependency-integrity gates — human review demonstrably does not catch that class of issue.](product-security.md#claim-gate-agent-prs-with-automated-checks)
- **Jul 15, 2026** · refuted · [~~Installing with --ignore-scripts, plus checking for a provenance attestation, is adequate protection against npm supply-chain compromise.~~](product-security.md#claim-ignore-scripts-blocks-npm-supply-chain)  
  ↳ The AsyncAPI compromise delivered its payload at import time, which --ignore-scripts does not prevent, and it shipped with a valid provenance attestation. Both controls target the wrong stage of the lifecycle.  
  ↳ **Now:** [npm supply-chain payloads delivered at IMPORT time defeat --ignore-scripts, and a valid provenance attestation does not indicate the package is trustworthy.](product-security.md#claim-import-time-payloads-defeat-install-time-controls)
- **Jul 4, 2026** · superseded · [~~Swapping in the newest frontier model is a strict improvement for an existing harness.~~](ai-research.md#claim-newer-model-is-always-an-upgrade)  
  ↳ Measured on a third-party harness's custom edit tool, newer Claude models invented made-up fields that their older siblings got right. Model upgrades can regress harness-specific tool calling, so an upgrade is a change to re-evaluate, not a free win.  
  ↳ **Now:** [A newer SOTA model can be WORSE at your harness's custom tool schema than its older siblings, because it was RL-trained on a different harness's tools.](ai-research.md#claim-match-tool-schemas-to-the-target-model)
- **May 2026** · superseded · [~~JSON is the natural default for all agent I/O; serialization format is not a meaningful optimization lever.~~](ai-research.md#claim-json-default-for-all-agent-io)  
  ↳ Format choice measurably moves cost: uniform arrays serialize 30-60% smaller in TOON at comparable retrieval accuracy, which makes serialization a real optimization lever on the input side rather than an aesthetic preference.  
  ↳ **Now:** [For large uniform arrays, TOON serializes to 30-60% fewer input tokens than JSON at comparable retrieval accuracy.](ai-research.md#claim-toon-cuts-input-tokens-vs-json)
- **May 2026** · refuted · [~~Prompt injection is fundamentally a filtering problem — a good input classifier plus an instruction-hierarchy system prompt solves it.~~](ai-security.md#claim-prompt-injection-solvable-by-filtering)  
  ↳ Impossibility result: an adversary can always construct a context under which a blocked flow looks legitimate, and a defender who tightens norms to stop it starts blocking genuinely legitimate flows. Large-scale red teaming confirmed the vulnerability persists across model families, so filtering is a cost-raiser, not a solution.  
  ↳ **Now:** [Prompt injection cannot be fully solved by context-based filtering: for any blocked flow an adversary can construct a context in which it appears legitimate.](ai-security.md#claim-prompt-injection-is-containment-not-prevention)
- **Mar 2026** · refuted · [~~Because TOON is more token-efficient than JSON, asking the model to GENERATE TOON is also better than asking it to generate JSON.~~](ai-research.md#claim-toon-best-for-structured-output-generation)  
  ↳ Benchmarked head-to-head, plain JSON generation had the best one-shot and final accuracy while constrained decoding used the fewest tokens; TOON was outperformed by constrained decoding even on simple structures. The input-side token saving does not transfer to the output side.  
  ↳ **Now:** [For structured model OUTPUT, constrained decoding gives the lowest token usage and plain JSON generation the best accuracy — token-optimized notations do not win here.](ai-research.md#claim-constrained-decoding-for-structured-output)

---

[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md)
