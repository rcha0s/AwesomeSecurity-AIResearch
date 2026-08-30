# Google dev kit spurs first-ever agent-on-agent violence

**Topic:** AI Security  ·  **Domain:** Agent-to-Agent Security / CI Prompt Injection  
**Source:** [source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)  ·  **Published:** Aug 3, 2026  ·  **Retrieved:** 2026-08-10  
**Scores:** 🆕 Newness 20 · ✨ Novelty 80 · 🎯 Relevance 92 · 🏛️ Credibility 70 · **Composite 67.1**  
**Tags:** `agent-to-agent`, `prompt-injection`, `ci-cd`, `adk-python`, `gemini-cli`, `privilege-escalation`, `github-actions`  
**Verification:** ✓ independently verified · closest prior art: General prompt-injection literature (Greshake et al., Rehberger); Invariant Labs' MCP tool-poisoning taxonomy; prior CI-injection findings in GitHub Actions review-bot workflows; Simon Willison's writing on agent-to-agent trust boundaries.

> **Takeaway:** Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped permissions, not tighter isolation - because 'isolation' still lets one agent produce input the other treats as trusted.

## TL;DR

_The gist, not every detail - read the [full source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496) for the complete write-up._

Pillar Security's Dan Lisichkin found a prompt-injection chain in google/adk-python's CI workflows where a low-privilege public-facing triage agent could be manipulated to hand off to a high-privilege maintainer-only agent (@gemini-cli) via a poisoned PR text, exfiltrating a GitHub token with `pull-requests: write`. Google fixed the underlying workflow but classified it as social-engineering-adjacent and not bounty-eligible. Lisichkin's remediation ask: give agents their own identities and threat-model agent identity + agent resource access explicitly.

## What to learn

- A public-facing low-privilege agent that can trigger a higher-privilege agent via natural-language handoff creates a prompt-injection privilege boundary crossing. - _"Pillar's team found that the low-privilege, public-facing agent could be manipulated via prompt injection into triggering a maintainer-only agent that can execute malicious actions."_ ✅
- The attacker manufactures a false review provenance trail - the artifacts on disk look like a legitimate maintainer-requested review that never happened. - _""Strung together, they manufacture a complete, believable 'a human asked for a review, gemini ran it, gemini approved' trail on the poisoned PR, none of which ever happened," Lisichkin wrote."_ ✅
- Agent isolation is not enough - the remediation is per-agent identity with scoped resource access, wired into the threat model. - _""Agents should have their own identity, which mandates what resources they are allowed to access and in what they are allowed to interact with these resources," he said. "In this case, if Google had just given a bot identity to the initial triaging agent, most of the attack could have been prevented. Security teams need to start modeling agent identity and agent resource access within their threat models.""_ ✅
- Google's rationale for not paying a bounty (social engineering) is itself a threat-model gap: it assumes the human-in-the-loop merge step provides meaningful review of an agent-approved PR. - _""This report demonstrates exfiltration of a GitHub token with a 'pull-requests: write' permission, which enables tampering with a PR but still requires a maintainer to take an action to merge the malicious PR as PRs are not automatically merged after a bot review," Google explained."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** In a repo where a public-facing triage agent and a maintainer-only agent share a trust boundary, an attacker files a PR whose text prompt-injects the triage agent into emitting the `@gemini-cli` handoff. The privileged agent runs the injected instructions with the maintainer PAT, exfiltrating a GitHub token with `pull-requests: write` and producing a fake 'human requested review, gemini approved' provenance trail.
- **Conditions:** Two automated AI agents in the same repo with different privilege levels. The lower-privilege agent reads attacker-controlled PR text. The higher-privilege agent is triggered by a string the lower-privilege agent can emit. Both agents use overlapping identity (collaborator PAT vs bot identity). Attacker has built enough repo trust to get initial CI runs.
- **Mitigations:** Distinct bot identity per agent, not a shared collaborator PAT. Least-privilege GitHub token scopes per agent workflow. Explicit allowlist for who can trigger the privileged agent - never derived from untrusted text. Treat inter-agent handoff strings as untrusted; require signed/scoped invocation. Threat-model 'agent A can invoke agent B' edges as first-class trust boundaries.

---

_Source: [https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_  ·  [← back to index](../README.md)
