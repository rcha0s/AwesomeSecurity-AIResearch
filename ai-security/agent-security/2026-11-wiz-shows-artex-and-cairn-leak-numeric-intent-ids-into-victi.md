# Wiz shows ARTEX and Cairn leak numeric intent IDs into victim logs

**Published:** Nov 25, 2026

> **Takeaway:** Agent harnesses leak their own bookkeeping into victim telemetry, giving defenders a cheap pacing and linking signal when paired with a tool-specific anchor.

## TL;DR

Wiz Research found that the ARTEX and Cairn offensive agent frameworks number each attack sub-goal (an "intent") and feed that number to the model, which then copies it into file names, accounts, workflow files, user agents and cloud resource names on the victim side. ARTEX never resets its counter by default, so the IDs climb across runs and targets and can link activity across rotating IPs and clouds; Cairn resets per project, so it only gives per-project markers. Wiz says the signal is lossy and should corroborate, not attribute.

## Lessons

- The leak is a harness implementation detail: the ID sits in the model's prompt and working paths, so the model reuses it in target-side artifacts. - _"When a harness places that ID in its prompts and workspace paths, it bleeds into the attack"_
- Climbing IDs can cluster activity that IP-based clustering misses because of residential proxy rotation. - _"Agentic campaigns often rotate through residential proxy pools, using a new exit IP on nearly every request."_
- In one intrusion, 36 IDs on the AWS side and 34 on the Azure side came from one sequence, tying two unrelated identity sets to one run. - _"In one intrusion the attacker used stolen IAM users in AWS and a service principal in Azure."_
- Wiz stresses limits: uneven climb rates, coincidental collisions in low ranges, and operator resets mean IDs are tool markers and pacing clues only. - _"Hits are useful tool markers and pacing clues, but not operator fingerprints."_

## Threat · Conditions · Mitigations

- **Threat:** Agentic offensive frameworks (the ARTEX family including Pojun and AntiFox forks, and the Cairn family including sapper-v2) expose operator infrastructure details through intent counters that the model copies into target artifacts.
- **Conditions:** The leaked ID is only useful when the model reuses the harness identifier in an artifact the defender can see; operators who rebuild the container, wipe the database or split targets across several ARTEX instances break the sequence, and Cairn resets per project.
- **Mitigations:** Pair intent-ID patterns with anchors before alerting, use climb rate and duplicates to cluster or separate installations, and treat the result as corroboration alongside other indicators rather than attribution.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [Wiz Research](https://www.wiz.io/blog/agentic-offensive-frameworks-intent-ids-artex-cairn)  ·  **Retrieved:** 2026-11-26  
**Scores:** Newness 24 · Novelty 70 · Relevance 70 · Credibility 66 · **Composite 58** _(each 0-100)_  
**Tags:** `artex`, `cairn`, `agentic-attacks`, `threat-hunting`, `attribution`, `wiz`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Wiz's earlier fingerprints-of-agent-driven-intrusions entry and Datadog's CloudTrail ARTEX hunting cover behavioral and parameter fingerprints, but none of the existing entries describe sequence-counter leakage from harness internals.

_Source: [https://www.wiz.io/blog/agentic-offensive-frameworks-intent-ids-artex-cairn](https://www.wiz.io/blog/agentic-offensive-frameworks-intent-ids-artex-cairn)_  ·  [← back to index](../README.md)
