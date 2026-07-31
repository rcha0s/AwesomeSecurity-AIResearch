# Product Security — standing claims

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_2 current · 0 contested · 1 superseded · 1 refuted · updated 2026-07-31_

[← Claim index](README.md) · [Product Security findings feed](../product-security/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-import-time-payloads-defeat-install-time-controls"></a>

### npm supply-chain payloads delivered at IMPORT time defeat --ignore-scripts, and a valid provenance attestation does not indicate the package is trustworthy.

`import-time-payloads-defeat-install-time-controls` · confidence **0.85** · Supply Chain & Dependencies · standing since Jul 15, 2026

**Do this —** Do not treat --ignore-scripts or provenance attestation as the control. Pin and review dependency updates, run untrusted first-import in a sandbox, and monitor runtime egress from build and test jobs.

**Replaces** [`ignore-scripts-blocks-npm-supply-chain`](#claim-ignore-scripts-blocks-npm-supply-chain) — Installing with --ignore-scripts, plus checking for a provenance attestation, is adequate protection against npm supply-chain compromise.

_Tags: `supply-chain`, `npm`, `provenance`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Unpacking the AsyncAPI npm supply-chain compromise: import-time payload delivery](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) | Jul 15, 2026 |

</details>

<a id="claim-gate-agent-prs-with-automated-checks"></a>

### Agent-generated PRs need automated secret and dependency-integrity gates — human review demonstrably does not catch that class of issue.

`gate-agent-prs-with-automated-checks` · confidence **0.75** · AI-Generated Code Risk · standing since Jul 19, 2026

**Do this —** Put automated secret scanning and dependency-integrity checks in the required-checks set for agent PRs, and keep human review for design and logic where it actually performs.

**Limits —** Measured on agent-generated PRs; 38.9% carried a security smell, though humans still introduce most of the severe defects overall.

**Replaces** [`human-review-catches-agent-pr-risk`](#claim-human-review-catches-agent-pr-risk) — Normal human code review is sufficient to catch the security problems in agent-generated pull requests.

_Tags: `ai-generated-code`, `code-review`, `ci`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [38.9% of agent-generated PRs carry a security smell — but humans introduce most of the real ones](https://arxiv.org/abs/2607.12428) | Jul 19, 2026 |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-human-review-catches-agent-pr-risk"></a>

### ~~Normal human code review is sufficient to catch the security problems in agent-generated pull requests.~~

`human-review-catches-agent-pr-risk` · **superseded** on Jul 19, 2026 · had stood since Jun 2025

**Why it was retired —** Measured across agent-generated PRs, 38.9% carried a security smell and human review demonstrably did not catch the secret and dependency-integrity class. Review remains valuable for logic and design, but it is not the control for this risk.

**Replaced by** [`gate-agent-prs-with-automated-checks`](#claim-gate-agent-prs-with-automated-checks) — Agent-generated PRs need automated secret and dependency-integrity gates — human review demonstrably does not catch that class of issue.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) | Jul 19, 2026 |

</details>

<a id="claim-ignore-scripts-blocks-npm-supply-chain"></a>

### ~~Installing with --ignore-scripts, plus checking for a provenance attestation, is adequate protection against npm supply-chain compromise.~~

`ignore-scripts-blocks-npm-supply-chain` · **refuted** on Jul 15, 2026 · had stood since Jan 2022

**Why it was retired —** The AsyncAPI compromise delivered its payload at import time, which --ignore-scripts does not prevent, and it shipped with a valid provenance attestation. Both controls target the wrong stage of the lifecycle.

**Replaced by** [`import-time-payloads-defeat-install-time-controls`](#claim-import-time-payloads-defeat-install-time-controls) — npm supply-chain payloads delivered at IMPORT time defeat --ignore-scripts, and a valid provenance attestation does not indicate the package is trustworthy.

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Unpacking the AsyncAPI npm supply-chain compromise: import-time payload delivery](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) | Jul 15, 2026 |

</details>

---

[← Claim index](README.md)
