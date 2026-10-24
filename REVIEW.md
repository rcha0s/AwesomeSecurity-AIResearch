# 🔍 Review Queue

> Everything held back from the site, with the reason. Findings that are **not yet vetted** (low confidence/novelty/relevance, or below the composite floor (20)), and news stories whose excerpt is not grounded in its source. Nothing here is deleted; promote a finding by raising its scores or clearing `needs_review`, or fix a news story's excerpt, then regenerate.

_Updated 2026-10-24._

## AI Security (7)

- **[OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident)** · composite 66.0 · _news story: excerpt not grounded in source (only 75% of quotes verified)_
  Treat a model eval with production classifiers off as a live agent that may try to escape, where a package-manager proxy is a plausible sandbox-escape primitive.
- **[Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585)** · composite 59.35 · _news story: excerpt not grounded in source_
  The critical attack surface for agent apps is the framework layer around the model, where old bug classes get re-exposed as prompt-injected code paths — not the model's ability to…
- **[Humans in the loop miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)** · composite 53.95 · _news story: excerpt not grounded in source_
  Human-in-the-loop is a fatigue-limited primitive: engineer approvals as classifier + sandbox + hooks, not as a UX prompt.
- **[MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027)** · composite 53.1 · _news story: excerpt not grounded in source_
  MCP's enterprise turn adds iss validation and a stateless design that removes one session-poisoning surface but leans on standard load-balancer trust boundaries.
- **[SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062)** · composite 51.25 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent policy enforcement, prefer a compiled program of narrow predicates over one guardrail model or one LLM judge: cheaper, steadier and auditable (authors' claims, abstract…
- **[OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/)** · composite 51.0 · _news story: excerpt not grounded in source_
  Rogue-agent incidents are foundational-security failures with known fixes: zero-trust boundaries, isolated eval hosts, egress control and active monitoring.
- **[Edge grounding VLMs fall to wearable adversarial patches like detectors, often with confident wrong boxes](http://arxiv.org/abs/2610.29196v1)** · composite 46.3 · _flagged needs_review (low confidence / novelty / relevance)_
  When red-teaming vision models in safety-critical systems, score where the box lands, not just whether one exists.

## Product Security (8)

- **[Next.js App Router: unauthenticated RCE in `use cache` functions that return multiple typed arrays (GHSA-673q-mjm6-r5xr)](https://github.com/advisories/GHSA-673q-mjm6-r5xr)** · composite 50.5 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Upgrade Next.js now if any `use cache` function returns typed arrays; there is no workaround.
- **[Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/)** · composite 49.6 · _flagged needs_review (low confidence / novelty / relevance)_
  Run pathrunner in a sandbox (Pathfinding Labs) and use its CloudTrail report to test that every payload, not just one, trips a detection.
- **[Next.js Image Optimization API: unauthenticated RCE via SVG through an upstream sharp memory bug on glibc Linux (GHSA-2464-fhr4-w9xw)](https://github.com/advisories/GHSA-2464-fhr4-w9xw)** · composite 49.0 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Pin a patched sharp under Next.js and consider disabling SVG optimization; image pipelines are unauthenticated RCE surface.
- **[A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/)** · composite 42.47 · _news story: excerpt not grounded in source_
  Enclave-to-KMS attestation only closes the gap if you also hardcode the CMK ARN, attest the IAM role, and initiate TLS from inside the enclave; without that, active-attacker…
- **[America bans imported robots due to supply chain and security risks](https://www.theregister.com/security/2026/07/29/america-bans-imported-robots-due-to-supply-chain-and-security-risks/5280145)** · composite 40.5 · _news story: excerpt not grounded in source_
  US regulators are treating networked physical robots as a critical-infrastructure supply-chain risk category on par with telecom gear.
- **[raml-kql: one KQL query across many Log Analytics workspaces and Entra tenants without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql)** · composite 40.0 · _flagged needs_review (low confidence / novelty / relevance)_
  MSSPs without a Defender MTO can hunt across customer Sentinel workspaces from one query with delegated access only.
- **[CISA KEV: Plex Media Server arbitrary file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656)** · composite 38.88 · _failed independent verification — Source text not captured (NVD page empty); lessons rest on the KEV catalog text only._
  Treat the four Plex KEV CVEs as one chain and patch together.
- **[CISA KEV: SiteGuard Server Edition OS command injection (CVE-2026-106931) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931)** · composite 31.75 · _failed independent verification — Fetched NVD page was empty; the only lesson rests on the KEV catalog description and cannot be grounded in the saved source._
  If you run SiteGuard Server Edition, patch now: CISA lists this command injection as actively exploited.

## AI Research (3)

- **[How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/)** · composite 59.62 · _news story: excerpt not grounded in source (only 0% of quotes verified)_
  In AI bug hunting, outcome definition and per-agent scoping drive output quality most, with a threat-model file as the highest-leverage input.
- **[DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522)** · composite 51.25 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate routers and guardrail judges on paired contrast cases, not only item accuracy.
- **[Anthropic embeds METR with employee-like access, but keeps control of what counts as redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators)** · composite 49.75 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded third-party evaluation is now a concrete arrangement at one frontier lab; when you weigh its outputs, look at the redaction terms.

---

<sub>Generated by scripts/generate_review.py on 2026-10-24. 18 item(s) awaiting review.</sub>
