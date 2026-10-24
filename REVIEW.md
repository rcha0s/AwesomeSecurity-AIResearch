# 🔍 Review Queue

> Everything held back from the site, with the reason. Findings that are **not yet vetted** (low confidence/novelty/relevance, or below the composite floor (20)), and news stories whose excerpt is not grounded in its source. Nothing here is deleted; promote a finding by raising its scores or clearing `needs_review`, or fix a news story's excerpt, then regenerate.

_Updated 2026-10-24._

## AI Security (15)

- **[OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident)** · composite 66.0 · _news story: excerpt not grounded in source (only 75% of quotes verified)_
  Treat a model eval with production classifiers off as a live agent that may try to escape, where a package-manager proxy is a plausible sandbox-escape primitive.
- **[Prompt injection isn't the bug, AI agent frameworks are](https://www.theregister.com/security/2026/08/05/prompt-injection-isnt-the-bug-ai-agent-frameworks-are/5283585)** · composite 59.35 · _news story: excerpt not grounded in source_
  The critical attack surface for agent apps is the framework layer around the model, where old bug classes get re-exposed as prompt-injected code paths — not the model's ability to…
- **[Humans in the loop miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)** · composite 53.95 · _news story: excerpt not grounded in source_
  Human-in-the-loop is a fatigue-limited primitive: engineer approvals as classifier + sandbox + hooks, not as a UX prompt.
- **[MCP gets an enterprise makeover](https://www.theregister.com/ai-and-ml/2026/07/29/mcp-gets-an-enterprise-makeover/5280027)** · composite 53.1 · _news story: excerpt not grounded in source_
  MCP's enterprise turn adds iss validation and a stateless design that removes one session-poisoning surface but leans on standard load-balancer trust boundaries.
- **[Data-void exploits: attacker content showed up in 31% of web-searching LLM answers, sometimes from a single page](http://arxiv.org/abs/2610.30365v1)** · composite 52.05 · _flagged needs_review (low confidence / novelty / relevance)_
  Web-search grounding is an input channel attackers can write to, especially on niche topics, so answers on such topics need signals about how thin or reliable the sources are.
- **[OpenAI's Hugging Face incident reduces to skipped basics: zero-trust and defense-in-depth on the eval host](https://www.wired.com/story/openais-hacking-debacle-was-a-human-mistake/)** · composite 51.0 · _news story: excerpt not grounded in source_
  Rogue-agent incidents are foundational-security failures with known fixes: zero-trust boundaries, isolated eval hosts, egress control and active monitoring.
- **[SCOPE compiles natural-language agent policies into predicate programs run by small models, aiming for frontier-level accuracy with stable, interpretable verdicts](https://arxiv.org/abs/2610.31062)** · composite 51.0 · _flagged needs_review (low confidence / novelty / relevance)_
  For agent policy enforcement, prefer a compiled program of narrow predicates over one guardrail model or one LLM judge: cheaper, steadier and auditable (authors' claims, abstract…
- **[Agent Mosaic: LLM agents combine individually allowed documents into forbidden conclusions, even with classification headers](https://arxiv.org/abs/2610.30418)** · composite 49.23 · _flagged needs_review (low confidence / novelty / relevance)_
  Document-level access control is not enough for agents serving users with mixed clearances, because the model can derive restricted conclusions from documents each user may read.
- **[Edge grounding VLMs fall to wearable adversarial patches like detectors, often with confident wrong boxes](http://arxiv.org/abs/2610.29196v1)** · composite 46.05 · _flagged needs_review (low confidence / novelty / relevance)_
  When red-teaming vision models in safety-critical systems, score where the box lands, not just whether one exists.
- **[openapi-mcp-generator 5.0 turns OpenAPI specs into MCP servers; missing credentials now fail closed](https://github.com/harsha-iiiv/openapi-mcp-generator)** · composite 39.57 · _flagged needs_review (low confidence / novelty / relevance)_
  Auto-generated MCP servers expose your whole API to an agent by default, so filter operations and turn on inbound auth before you deploy one.
- **[mem0 Databricks vector store: crafted memory content reaches unescaped SQL (CVE-2026-115324)](https://github.com/advisories/GHSA-7587-9684-52r6)** · composite 38.25 · _failed independent verification — Refuted: the saved source holds only generic CVSS definitions, so the SQL injection, version range and Databricks details are unsupported by it. Needs a re-fetch of the advisory._
  Agent memory content is attacker-influenced input, so memory backends must use parameterized queries like any other data layer.
- **[mcp-jenkins exposes an arbitrary Groovy execution tool and binds 0.0.0.0 by default on streamable-http](https://github.com/lanbaoshen/mcp-jenkins)** · composite 38.07 · _flagged needs_review (low confidence / novelty / relevance)_
  Treat a Jenkins MCP server as code execution on your CI: give it a token without script rights, enable read-only mode, and keep it off the network.
- **[Praetorian's Augustus LLM scanner adds multi-turn attackers, including Hydra, which erases refused turns](https://github.com/praetorian-inc/augustus)** · composite 36.75 · _flagged needs_review (low confidence / novelty / relevance)_
  If your LLM app keeps client-controlled chat history, test it with multi-turn and backtracking attacks, not just single-prompt jailbreak lists.
- **[Anthropic Frontier Red Team (March 2025): Claude reached undergraduate-level CTF skill but failed autonomous network attacks](https://www.anthropic.com/research/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team)** · composite 32.37 · _flagged needs_review (low confidence / novelty / relevance)_
  When estimating offensive AI capability, test with an attack toolkit and not only the bare model, though these March 2025 figures are now well out of date.
- **[Check Point: an infostealer adds collection routines for Claude, ChatGPT Desktop, Codex, Cursor and Windsurf](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/)** · composite 8.25 · _ungrounded excerpt — only 0% of quotes verified against the source_
  AI desktop apps and coding tools now sit next to browsers and wallets on infostealer target lists, so their tokens and data need the same protection.

## Product Security (16)

- **[Next.js App Router: unauthenticated RCE in `use cache` functions that return multiple typed arrays (GHSA-673q-mjm6-r5xr)](https://github.com/advisories/GHSA-673q-mjm6-r5xr)** · composite 50.25 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Upgrade Next.js now if any `use cache` function returns typed arrays; there is no workaround.
- **[Datadog's pathrunner automates 80+ AWS IAM privilege-escalation paths and hands defenders the CloudTrail events each run should have produced](https://securitylabs.datadoghq.com/articles/introducing-pathrunner-aws-privilege-escalation-framework/)** · composite 49.35 · _flagged needs_review (low confidence / novelty / relevance)_
  Run pathrunner in a sandbox (Pathfinding Labs) and use its CloudTrail report to test that every payload, not just one, trips a detection.
- **[Next.js Image Optimization API: unauthenticated RCE via SVG through an upstream sharp memory bug on glibc Linux (GHSA-2464-fhr4-w9xw)](https://github.com/advisories/GHSA-2464-fhr4-w9xw)** · composite 48.75 · _failed independent verification — Advisory body not captured (fetched page holds only CVSS boilerplate); lessons rest on the GHSA feed summary._
  Pin a patched sharp under Next.js and consider disabling SVG optimization; image pipelines are unauthenticated RCE surface.
- **[A few notes on AWS Nitro Enclaves: KMS integration](https://blog.trailofbits.com/2026/08/05/a-few-notes-on-aws-nitro-enclaves-kms-integration/)** · composite 42.47 · _news story: excerpt not grounded in source_
  Enclave-to-KMS attestation only closes the gap if you also hardcode the CMK ARN, attest the IAM role, and initiate TLS from inside the enclave; without that, active-attacker…
- **[Wiz scans every new npm version at publish time with diffing, sandboxed execution and an AI classifier to catch compromises pre-CVE](https://www.wiz.io/blog/detect-supply-chain-zero-days-at-publication)** · composite 41.1 · _flagged needs_review (low confidence / novelty / relevance)_
  CVE-based dependency scanning is blind to hijacked trusted packages; you need publish-time behavioral analysis or a cooldown before new versions reach builds.
- **[America bans imported robots due to supply chain and security risks](https://www.theregister.com/security/2026/07/29/america-bans-imported-robots-due-to-supply-chain-and-security-risks/5280145)** · composite 40.5 · _news story: excerpt not grounded in source_
  US regulators are treating networked physical robots as a critical-infrastructure supply-chain risk category on par with telecom gear.
- **[raml-kql: one KQL query across many Log Analytics workspaces and Entra tenants without a Defender multi-tenant org](https://github.com/luca-ramseyer/raml-kql)** · composite 39.75 · _flagged needs_review (low confidence / novelty / relevance)_
  MSSPs without a Defender MTO can hunt across customer Sentinel workspaces from one query with delegated access only.
- **[CISA KEV: Plex Media Server arbitrary file write CVE-2026-96656 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96656)** · composite 38.62 · _failed independent verification — Source text not captured (NVD page empty); lessons rest on the KEV catalog text only._
  Treat the four Plex KEV CVEs as one chain and patch together.
- **[Talos newsletter: PHP2Shell RCEs hit every PHP build since 5.4; no patch for 8.1 or older](https://blog.talosintelligence.com/i-had-plans-for-that-second/)** · composite 33.0 · _flagged needs_review (low confidence / novelty / relevance)_
  If you run PHP 8.1 or older, there is no patch: upgrade to 8.2+ or put network-level protection in front now.
- **[CISA KEV: SiteGuard Server Edition OS command injection (CVE-2026-106931) exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-106931)** · composite 31.5 · _failed independent verification — Fetched NVD page was empty; the only lesson rests on the KEV catalog description and cannot be grounded in the saved source._
  If you run SiteGuard Server Edition, patch now: CISA lists this command injection as actively exploited.
- **[Aikido post claims 'http2shell' RCE affects Node, Python and more; captured source has no technical details](https://nitter.click/AikidoSecurity/status/2113759110625906950?__galadriel=lPmlGl9id4oAd5UeBwMhlYKArHyr6lR2IDGujPwB5HV2kQ1aLoPWFd5A9sGuzNcmrp8fUso8qygmHcKTDZ8MNHWqQ3bDJcycV87xp_0VypzQLYj6O_RRHlZuQqj33oASGY2YLSoAiMjeOZN40h7Stf8AG7DPrGZbAPVKUXy36HoMudRbvwF3_r2uYNmfJMhpKzywQDM6Ab8)** · composite 25.5 · _flagged needs_review (low confidence / novelty / relevance)_
  A possible cross-runtime RCE is circulating, but this capture has no details; get the primary Aikido or vendor advisory before acting.
- **[Unverified book claim that Dutch government hacked Jared Kushner's phone; Kushner denies it](https://twitter.com/jaredkushner/status/2113376217415958767)** · composite 21.0 · _flagged needs_review (low confidence / novelty / relevance)_
  This is a disputed political allegation with no technical content; treat it as unconfirmed news, not threat intelligence.
- **[CISA KEV: Plex Media Server SSRF CVE-2026-96655 exploited in the wild, chainable with three other Plex CVEs](https://nvd.nist.gov/vuln/detail/CVE-2026-96655)** · composite 11.94 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Any logged-in Plex user can make the server fetch arbitrary addresses, and attackers are chaining it with other Plex bugs.
- **[Storybook dev server lacks origin validation; malicious sites can change project files](https://github.com/advisories/GHSA-f2ph-cmg5-wxc8)** · composite 10.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Local dev servers reachable from the browser are an attack surface; patch and avoid opening untrusted sites meanwhile.
- **[uv before 0.13.4 trusts the emSign root behind eight compromised eMudhra intermediate CAs (GHSA-hq85-5cpj-mr62)](https://github.com/advisories/GHSA-hq85-5cpj-mr62)** · composite 10.5 · _ungrounded excerpt — only 0% of quotes verified against the source_
  Python installs through uv could accept certificates signed with the leaked eMudhra keys until you upgrade to 0.13.4.
- **[CISA KEV: Siemens Software Center DLL search-path flaw CVE-2026-110936 exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-110936)** · composite 10.44 · _ungrounded excerpt — only 0% of quotes verified against the source_
  A local attacker who can drop a DLL where Siemens Software Center looks for one gets code execution; CISA says this is being exploited.

## AI Research (6)

- **[How we use /goal to find bugs in Patch the Planet](https://blog.trailofbits.com/2026/07/28/how-we-use-goal-to-find-bugs-in-patch-the-planet/)** · composite 59.62 · _news story: excerpt not grounded in source (only 0% of quotes verified)_
  In AI bug hunting, outcome definition and per-agent scoping drive output quality most, with a threat-model file as the highest-leverage input.
- **[DecisionPivot: router/guardrail decision models with near-equal accuracy diverge sharply on contrast pairs](https://arxiv.org/abs/2610.28522)** · composite 51.0 · _flagged needs_review (low confidence / novelty / relevance)_
  Evaluate routers and guardrail judges on paired contrast cases, not only item accuracy.
- **[Anthropic embeds METR with employee-like access, but keeps control of what counts as redactable](https://www.anthropic.com/news/an-update-on-independent-evaluators)** · composite 49.5 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded third-party evaluation is now a concrete arrangement at one frontier lab; when you weigh its outputs, look at the redaction terms.
- **[Anthropic funds Accenture's Faculty as an embedded evaluator with employee-level access; each expects to invest at least $1B](https://www.anthropic.com/news/accenture-embedded-evaluation)** · composite 38.62 · _flagged needs_review (low confidence / novelty / relevance)_
  Embedded evaluation is starting with a lab-funded commercial partner and no shared standards, so judge its independence by the access and reporting terms once they are published.
- **[Bound-conditioned latent inference cuts progressive image codec BD-rate 7.96% vs CTC on Kodak with 5.3x fewer parameters](http://arxiv.org/abs/2610.30966v1)** · composite 31.05 · _flagged needs_review (low confidence / novelty / relevance)_
  A solid image-compression result, but it has no bearing on securing or building AI agents and harnesses.
- **[RoboCasa-Shift: equal success-rate drops in a VLA robot policy hide very different failure stages](https://arxiv.org/abs/2610.27861)** · composite 29.73 · _flagged needs_review (low confidence / novelty / relevance)_
  Aggregate success rate can hide outcome flips and which task stage fails; the study covers one robot policy on four simulated tasks.

---

<sub>Generated by scripts/generate_review.py on 2026-10-24. 37 item(s) awaiting review.</sub>
