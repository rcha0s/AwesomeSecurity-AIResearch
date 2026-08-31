# Product Security — standing claims

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

> **What this page is.** The current answer for each question in this topic, ranked by confidence — and underneath, every answer it replaced, kept on purpose with the date and reason it was retired.

_11 current · 0 contested · 1 superseded · 1 refuted · updated 2026-08-31_

[← Claim index](README.md) · [Product Security findings feed](../product-security/README.md) · [Home](../README.md)

## ✅ Current

<a id="claim-package-installers-run-arbitrary-code-by-default"></a>

### Package installs run arbitrary code by default

`package-installers-run-arbitrary-code-by-default` · confidence **0.98** · Supply Chain & Dependencies · standing since Jan 2020

Installing a package with pip, npm, or gem executes arbitrary code at install time by default. Treat 'installed a dep' as 'ran their code'.

**Basis —** General supply-chain best-practice guidance, corroborated by a real self-propagating npm worm (ChainDrop) that exploited exactly this default.

**Do this —** Do first-touch installs in a sandbox. Where possible, prefer --ignore-scripts + explicit build orchestration.

_Tags: `npm`, `pip`, `supply-chain`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Supply chain best practices](https://blog.trailofbits.com/2020/12/22/how-are-teams-currently-handling-web-attacks-at-scale/) | undated |
| supports | [ChainDrop: Inside a Self-Propagating npm Worm](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) | Aug 6, 2026 |

</details>

<a id="claim-imdsv1-must-be-disabled-on-agent-workloads"></a>

### IMDSv1 is trivially exploitable; disable it for agent workloads

`imdsv1-must-be-disabled-on-agent-workloads` · confidence **0.95** · Cloud & IAM · standing since Nov 2019

AWS IMDSv1 is trivially exploitable from any code that can cause an HTTP GET to 169.254.169.254; agent workloads that may fetch user-provided URLs must disable v1 in favor of v2.

**Basis —** AWS's own security guidance documenting the IMDSv1 SSRF-to-credential-theft path and why IMDSv2 closes it.

**Do this —** Set HttpTokens=required on all EC2 instances hosting agent runtimes.

_Tags: `aws`, `imds`, `ssrf`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Get the full benefits of IMDSv2](https://aws.amazon.com/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/) | undated |
| supports | [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) | Jul 15, 2026 |

</details>

<a id="claim-path-traversal-defenses-must-cover-symlink-resolution"></a>

### Path validation must canonicalize, not just check the string

`path-traversal-defenses-must-cover-symlink-resolution` · confidence **0.95** · Application Security · standing since Jan 2010

Any code that opens a file whose path derives from user input must canonicalize the resolved target and verify it stays within the intended sandbox; validating the raw path string is insufficient.

**Basis —** A structural argument from the CWE-22 canonical vulnerability definition — a class-level defense requirement, not a single incident.

**Do this —** Use realpath() then verify prefix. Never trust the input string alone.

_Tags: `path-traversal`, `symlinks`, `defense`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | undated |

</details>

<a id="claim-long-lived-cloud-credentials-are-obsolete"></a>

### Long-lived cloud credentials are the top breach root cause

`long-lived-cloud-credentials-are-obsolete` · confidence **0.90** · Cloud & IAM · standing since Jan 2021

Long-lived static cloud credentials in CI or on developer machines are the highest-frequency root cause of breach in cloud environments; short-lived OIDC / role-assumption flows should be used for every automated workload.

**Basis —** Cross-referenced across a cloud-identity vendor writeup and two 2026 incident reports (AI API key resale, LiteLLM gateway secret harvesting) that both trace back to long-lived credentials.

**Do this —** Migrate CI to OIDC federation. Enforce a max credential age on IAM users.

_Tags: `aws`, `credentials`, `oidc`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Workload identity federation](https://cloud.google.com/blog/products/identity-security/rip-secret-storage) | undated |
| supports | [Token jacking: stolen AI API keys resold via gray-market transfer stations, ~$1M losses](https://unit42.paloaltonetworks.com/ai-token-jacking/) | Aug 6, 2026 |
| supports | [Attackers harvest gateway secrets from /proc/1/environ on compromised LiteLLM AI infrastructure](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/) | Aug 26, 2026 |

</details>

<a id="claim-typosquatting-in-package-registries-is-an-active-threat"></a>

### Typosquatted registry packages remain an active threat

`typosquatting-in-package-registries-is-an-active-threat` · confidence **0.90** · Supply Chain & Dependencies · standing since Jan 2016

Typosquatted packages are regularly uploaded to public registries with malicious install-time payloads; the technique remains effective because dependency selection is often typed manually.

**Basis —** A documented incident analysis of a typosquatting attack targeting a cryptocurrency npm package via manually-typed dependency names.

**Do this —** Prefer install from lockfile only; audit any hand-added dependency's provenance.

_Tags: `typosquatting`, `npm`, `pypi`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Typosquatting on npm](https://checkmarx.com/blog/typosquatting-attack-on-npm-cryptocurrency-package/) | undated |

</details>

<a id="claim-mobile-webviews-are-a-persistent-cross-context-attack-surface"></a>

### WebView JS bridges turn web XSS into device RCE

`mobile-webviews-are-a-persistent-cross-context-attack-surface` · confidence **0.90** · Mobile Security · standing since Jan 2014

Mobile applications that render web content in a WebView with JS bridges exposed to native code create a persistent cross-context attack surface — any XSS in the rendered content becomes device-level RCE.

**Basis —** Structural platform-security guidance from Android's own developer security documentation on the WebView/native-bridge risk.

**Do this —** Never expose native bridges to WebViews that render third-party content.

_Tags: `mobile`, `webview`, `android`, `ios`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Insecure WebView native bridge](https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridge) | undated |

</details>

<a id="claim-import-time-payloads-defeat-install-time-controls"></a>

### Import-time npm payloads defeat --ignore-scripts and provenance

`import-time-payloads-defeat-install-time-controls` · confidence **0.85** · Supply Chain & Dependencies · standing since Jul 15, 2026

npm supply-chain payloads delivered at IMPORT time defeat --ignore-scripts, and a valid provenance attestation does not indicate the package is trustworthy.

**Basis —** A forensic breakdown of a real supply-chain compromise (the AsyncAPI npm package) showing the payload fired at import time and shipped with a valid provenance attestation.

**Do this —** Do not treat --ignore-scripts or provenance attestation as the control. Pin and review dependency updates, run untrusted first-import in a sandbox, and monitor runtime egress from build and test jobs.

**Replaces** [`ignore-scripts-blocks-npm-supply-chain`](#claim-ignore-scripts-blocks-npm-supply-chain) — Assumed --ignore-scripts plus provenance was adequate

_Tags: `supply-chain`, `npm`, `provenance`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Unpacking the AsyncAPI npm supply-chain compromise: import-time payload delivery](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) | Jul 15, 2026 |

</details>

<a id="claim-llm-generated-code-hallucinates-package-names"></a>

### LLM-hallucinated package names enable slopsquatting

`llm-generated-code-hallucinates-package-names` · confidence **0.85** · AI-Generated Code Risk · standing since Jun 2024

LLMs generate import statements for packages that do not exist ('slopsquatting'); attackers observe these hallucinated names and register malicious packages to catch the next developer who copies the generated code.

**Basis —** Established by the original 'package hallucinations' academic study, measuring how often LLM code suggests nonexistent import names.

**Do this —** Every LLM-suggested dependency must be verified against the actual registry before pinning.

_Tags: `ai-code-risk`, `slopsquatting`, `npm`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations](https://arxiv.org/abs/2406.10279) | Jun 2024 |
| supports | [Phantom Squatting: attackers register the domains LLMs hallucinate](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) | Jun 30, 2026 |
| supports | [AI Coding Agents Skip Package Verification, and Attackers Are Exploiting It](https://www.techtimes.com/articles/319457/20260701/ai-coding-agents-skip-package-verification-attackers-are-exploiting-it.htm) | Jul 1, 2026 |

</details>

<a id="claim-ssrf-guards-must-cover-agent-outbound-calls"></a>

### SSRF guards must cover every agent outbound call, not just user input

`ssrf-guards-must-cover-agent-outbound-calls` · confidence **0.85** · Application Security · standing since Jan 2020

SSRF guards on user-input URLs are not sufficient for agent applications: the agent can be steered into making outbound calls from tool responses, retrieval results, or MCP metadata.

**Basis —** Grounded in two 2026 GHSA advisories showing real agent/gateway processes making unguarded outbound requests from MCP server metadata and caller-controlled parameters, on top of the general OWASP SSRF threat model.

**Do this —** Apply the private-IP dialer guard to every outbound HTTP client in an agent runtime — not just the user-facing one. Re-validate on redirect.

_Tags: `ssrf`, `agents`, `defense`_

<details><summary>Evidence (3)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [SSRF (OWASP)](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery) | undated |
| supports | [ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](https://github.com/advisories/GHSA-pr64-jmmf-jp54) | Jul 15, 2026 |
| supports | [TensorZero Gateway: a request parameter that overrides the server's object-storage config gives arbitrary file read and SSRF](https://github.com/advisories/GHSA-824w-x939-6cmc) | Jul 15, 2026 |

</details>

<a id="claim-gate-agent-prs-with-automated-checks"></a>

### Automated gates catch what human review misses on agent PRs

`gate-agent-prs-with-automated-checks` · confidence **0.75** · AI-Generated Code Risk · standing since Jul 19, 2026

Agent-generated PRs need automated secret and dependency-integrity gates — human review demonstrably does not catch that class of issue.

**Basis —** Measured across a corpus of agent-generated pull requests: 38.9% carried a security smell that human review did not catch.

**Do this —** Put automated secret scanning and dependency-integrity checks in the required-checks set for agent PRs, and keep human review for design and logic where it actually performs.

**Conditions —** Measured on agent-generated PRs; 38.9% carried a security smell, though humans still introduce most of the severe defects overall.

**Replaces** [`human-review-catches-agent-pr-risk`](#claim-human-review-catches-agent-pr-risk) — Assumed normal review was enough for agent PR risk

_Tags: `ai-generated-code`, `code-review`, `ci`_

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [38.9% of agent-generated PRs carry a security smell — but humans introduce most of the real ones](https://arxiv.org/abs/2607.12428) | Jul 19, 2026 |

</details>

<a id="claim-signature-based-detection-fails-on-llm-authored-malware"></a>

### Signature detection underperforms on LLM-authored malware

`signature-based-detection-fails-on-llm-authored-malware` · confidence **0.70** · Detection & Response · standing since Jan 2024

Signature-based detection under-performs against LLM-authored malware because trivial regeneration produces novel binaries at zero cost, while behavior and delivery-chain signals remain stable.

**Basis —** Two Unit 42 studies: one showing LLM-based obfuscation defeating signatures, a second measuring ~97% of AI-assisted malware samples never reaching production.

**Do this —** Weight EDR and behavioral analytics over hash-based feeds for AI-authored threat classes.

_Tags: `malware`, `detection`, `ai-authored`_

<details><summary>Evidence (2)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| supports | [Using LLMs to obfuscate malicious JavaScript](https://unit42.paloaltonetworks.com/using-llms-obfuscate-malicious-javascript/) | undated |
| supports | [State of AI-Enabled Malware: ~97% of samples never reach production; AI changes authoring not execution](https://unit42.paloaltonetworks.com/ai-enabled-malware-analysis/) | Aug 25, 2026 |

</details>

## 🪦 Superseded & refuted

> Kept deliberately. Knowing what we used to believe — and why it stopped being true — is how you avoid re-adopting an answer the field has already moved past.

<a id="claim-human-review-catches-agent-pr-risk"></a>

### ~~Assumed normal review was enough for agent PR risk~~

`human-review-catches-agent-pr-risk` · **superseded** on Jul 19, 2026 · had stood since Jun 2025

Normal human code review is sufficient to catch the security problems in agent-generated pull requests.

**Why it was retired —** Measured across agent-generated PRs, 38.9% carried a security smell and human review demonstrably did not catch the secret and dependency-integrity class. Review remains valuable for logic and design, but it is not the control for this risk.

**Replaced by** [`gate-agent-prs-with-automated-checks`](#claim-gate-agent-prs-with-automated-checks) — Automated gates catch what human review misses on agent PRs

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428) | Jul 19, 2026 |

</details>

<a id="claim-ignore-scripts-blocks-npm-supply-chain"></a>

### ~~Assumed --ignore-scripts plus provenance was adequate~~

`ignore-scripts-blocks-npm-supply-chain` · **refuted** on Jul 15, 2026 · had stood since Jan 2022

Installing with --ignore-scripts, plus checking for a provenance attestation, is adequate protection against npm supply-chain compromise.

**Why it was retired —** The AsyncAPI compromise delivered its payload at import time, which --ignore-scripts does not prevent, and it shipped with a valid provenance attestation. Both controls target the wrong stage of the lifecycle.

**Replaced by** [`import-time-payloads-defeat-install-time-controls`](#claim-import-time-payloads-defeat-install-time-controls) — Import-time npm payloads defeat --ignore-scripts and provenance

<details><summary>Evidence (1)</summary>

| Stance | Source | Published |
| --- | --- | --- |
| refutes | [Unpacking the AsyncAPI npm supply-chain compromise: import-time payload delivery](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/) | Jul 15, 2026 |

</details>

---

[← Claim index](README.md)
