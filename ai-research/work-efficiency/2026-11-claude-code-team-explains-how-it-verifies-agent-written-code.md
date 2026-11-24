# Claude Code team explains how it verifies agent-written code at scale

**Published:** Nov 17, 2026

> **Takeaway:** Treat the verification layer as a system of its own: run the real app, keep the checks out of reach of the change, and measure the checks against past incidents.

## TL;DR

The Claude Code team says about 90% of its code is written and reviewed by Claude, so verification loops are what let one person run many agents in parallel. The post recommends end-to-end, property and differential tests, a verify skill that boots and drives the app, and review gates that the change under review cannot edit. It also covers rolling out new gates in observe mode and turning missed bugs into review rules.

## Lessons

- Having the agent run the real app end to end is worth more than adding more tests, and a repo-local verify skill codifies how to do it. - _"Running the app end to end matters more than tests."_
- A gate that the change can rewrite is not a gate: review rules must be read from the base branch, not from the pull request. - _"If a change can modify the check that judges it, the check is broken."_
- Bound autonomous fix loops: after a fixed number of failed rounds the agent stops and hands the problem to a person. - _"If a check is still failing after three rounds, Claude stops and brings in a human."_
- Roll out a new verification gate in observe mode first, logging what it would block, before switching to enforce. - _"Observe mode will log what would have been blocked, so that we can review any false positives and ensure no one is impacted."_

---

**Topic:** AI Research  ·  **Domain:** Work Efficiency  
**Source:** [@craigmart via Hacker News](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)  ·  **Retrieved:** 2026-11-18  
**Scores:** Newness 27 · Novelty 40.0 · Relevance 85 · Credibility 55 · **Composite 52** _(each 0-100)_  
**Tags:** `verification-loops`, `claude-code`, `agent-harness`, `code-review`, `testing`, `evals`, `vendor-blog`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Corpus entries on verification loops and separate grader (ai-research.json mentions of verification loops, claim separate-grader-from-generator); the post's novel parts are first-party base-branch rule loading, observe-mode commit gates and reviewing the reviewers, but much of the E2E/property/differential testing advice is generic and the post itself links earlier Anthropic code-review and verification-loop posts.

_Source: [https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)_  ·  [← back to index](../README.md)
