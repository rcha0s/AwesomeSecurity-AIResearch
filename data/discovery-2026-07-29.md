# Discovery run, 2026-07-29

A discovery (ingest) pass run from a web-search sweep across the three tracks. These are
raw candidates staged in `data/candidates.json`, not vetted findings. They have not been
scored, grounded against source text, or verified yet. Run the analyze and verify steps
locally (`/research-scan` or `/add-resource`) to turn any of these into curated entries.

7 candidates staged. 1 dropped as a duplicate of an existing pool entry (ShadowPickle),
which is a good sign the dedup is working.

## AI Security

**Balkanization of Execution-Security Research for AI Coding Agents (isolation, access control, TOCTOU)**
arXiv 2607.05743 (2026-07). Suggested domain: Harness & Agent Security.
Lesson: coding-agent execution security is fragmenting; a unified isolation / access-control /
time-of-check-to-time-of-use taxonomy (39 papers into 17 categories, 4 confirmed CVEs including
two in Claude Code) is the baseline to test your own agent against.
Do: map your agent's file and process isolation against the 17 categories and close the TOCTOU gaps.

**aiAuthZ: Off-Host, Identity-Bound Authorization for AI Agents**
arXiv 2607.05518 (2026-07). Suggested domain: Harness & Agent Security.
Lesson: bind an agent's authorization to a verifiable identity enforced off-host, so a
compromised agent cannot self-escalate its own permissions.
Do: move agent authorization decisions out of the agent process to an identity-bound policy service.

**Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents**
arXiv 2606.26479 (2026-06). Suggested domain: Prompt Injection.
Lesson: static tests overstate prompt-injection defenses; evaluate out-of-band defenses
adaptively and adversarially or you ship a false sense of safety.
Do: add an adaptive attacker to your injection eval before trusting any out-of-band filter.

## Product Security

**The npm Threat Landscape: Attack Surface and Mitigations (Unit 42, updated 2026-07-15)**
https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/ (2026-07). Domain: Supply Chain & Dependencies.
Lesson: npm attacks are continuous, not episodic; monitor the registry attack surface as a
living feed rather than a point-in-time scan.
Do: wire a continuous dependency-integrity monitor into CI rather than scanning at release only.
Note: newsworthy / trending, part of the ongoing supply-chain cluster.

**AI Coding Agents Skip Package Verification, and Attackers Are Exploiting It (TechTimes, 2026-07-01)**
https://www.techtimes.com/articles/319457/20260701/ (2026-07). Domain: AI-Generated Code Risk.
Lesson: agents resolve and install dependencies before any scanner sees them; gate agent
dependency resolution instead of trusting post-hoc scans.
Do: force agent-proposed dependencies through the same admission gate as human PRs.
Note: newsworthy / trending, pairs with the existing "agent PRs carry a security smell" finding.

## AI Research (practitioner)

**EPC: A Standardized Protocol for Measuring Evaluator Preference Dynamics in LLM Agent Systems**
arXiv 2607.00297 (2026-07). Suggested domain: Evaluation.
Lesson: LLM-judge preferences drift across time and model versions; version and measure your
evaluator, not just the agent it grades.
Do: pin and periodically re-baseline your judge model, and track its preference drift as a metric.

**TokenPilot: Cache-Efficient Context Management for LLM Agents**
arXiv 2606.17016 (2026-06). Suggested domain: Architecture & Optimization.
Lesson: structure agent context for KV-cache reuse to cut cost and latency on long-horizon
tasks; naive context churn silently burns tokens.
Do: order and pin the stable prefix of your prompt so the cache is reused across steps.

## Dropped as duplicate

**ShadowPickle** (arXiv 2607.17503) was skipped by the ingest dedup because an equivalent entry
already lives in the AI Security / Model Supply Chain pool.

## Next step

These are staged only. To promote any into the curated pools, run the analyze and verify
passes locally (they fetch each source, extract the lesson, score novelty and relevance, and
run the independent grounding and verification checks), then regenerate the site. Nothing here
should be merged into `data/*.json` pools without that pass. `data/candidates.json` is gitignored
and transient, so it will not be committed.
