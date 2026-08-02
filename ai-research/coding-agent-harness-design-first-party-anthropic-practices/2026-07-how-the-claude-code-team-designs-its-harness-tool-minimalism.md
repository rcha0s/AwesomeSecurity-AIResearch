# How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier

**Topic:** AI Research  ·  **Domain:** coding-agent harness design (first-party Anthropic practices)  
**Source:** [@simonw](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)  ·  **Author:** simonw  ·  **Published:** Jul 21, 2026  ·  **Retrieved:** 2026-07-26  
**Scores:** 🆕 Newness 18 · ✨ Novelty 60 · 🎯 Relevance 90 · 🏛️ Credibility 75 · **Composite 60.75**  
**Tags:** `coding-agents`, `harness-design`, `tool-design`, `evals`, `system-prompt`, `prompt-injection`, `permissions`, `subagents`, `dogfooding`, `context-management`  
**Verification:** ✓ independently verified · closest prior art: Anthropic's own engineering guidance ('Building effective agents', 'Writing effective tools for agents') and Claude Code best-practices docs, which already advocate small distinct toolsets and eval-driven iteration; the analyst's cited benchmarks/taxonomies (PawBench, harness taxonomy) are third-party and not equivalent to this first-party account.

> **Takeaway:** Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier that gates dangerous actions.

## TL;DR

_The gist, not every detail - read the [full source](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) for the complete write-up._

An annotated transcript of Simon Willison's interview with Cat Wu and Thariq from Anthropic's Claude Code team, giving a first-party account of how they actually build and dogfood a coding agent. Key transferable practices: keep the tool set small and each tool functionally distinct (they removed grep/glob in favor of bash), grow eval sets from real production incidents rather than speculation, and shrink the system prompt by removing examples and replacing hard rules with nuanced context. Security is enforced by a Sonnet 'auto mode' classifier that reads the tool call plus conversation context to grant dynamic permissions, plus credential injection and red-teamed sandbox evals.

## What to learn

- Keep the tool set small and make each tool functionally distinct so the model can unambiguously pick one; prefer general tools (native bash) over specialized ones (grep/glob), and keep a tool mainly when it powers a dedicated UI (e.g. the file-edit approval prompt). Tool design is empirical ('models are more of a biology than a physics'), so validate with evals rather than rules. - _"every tool we add has a distinct function from every other tool, so that Claude can very easily distinguish when to call each"_ ✅
- Grow eval sets from real incidents, not speculation: when a bug ships, take the PRs that caused it and add them to the eval suite so the regression is caught next time. Complement capability evals with behavioral evals that catch UX annoyances (Claude declaring 'time to go to sleep' or stopping partway to ask if it should continue), and re-run the full suite on every model upgrade before dropping in a new model. - _"we look at the PRs that caused the incident and say, okay, how do we update code review to catch that"_ ✅
- Compact the system prompt by removing in-context examples (frontier models are 'more creative than the examples we gave it') and by replacing hard 'don't do X' constraints with nuanced reasoning the model can apply with judgment (explain WHY to run the app locally for front-end changes rather than a blanket 'always verify'). Pressure-test prompt wording for the ~10% of cases a well-intentioned human could misread. - _"because it was just more creative than the examples we gave it"_ ✅
- Enforce agent permissions with a model-in-the-loop classifier ('auto mode'): a Sonnet model evaluates the proposed tool call AND the conversation context to grant or deny dynamically, honoring user intent (no standing git-push rights, but allow it right after the user says 'push this to GitHub'). Pair this with credential injection via a proxy so secrets are usable-by but not readable-by the agent, and harden it against sandbox-escape / prompt-injection with commissioned red-team environments turned into regression evals. - _"the Datadog credentials are only usable by the agent but not accessible by the agent"_ ✅
- Let models write the prompts for downstream agents/tools: an orchestrator gives each specialized subagent 'a very detailed prompt', and modern models are now trusted to author those prompts ('a year ago I did not trust a model to write a prompt. Today the good models are very good at prompting'). Ship features to employees first and gate public release on internal active-user and retention bars ('ant fooding'); their own Claude Tag bot lands ~65% of product-engineering PRs. - _"Claude not just prompting a single subagent, but prompting the orchestration of many subagents"_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Prompt injection and sandbox escape against coding agents that are 'influenced by anyone who can talk to it' (public Slack/feedback channels), and secret exposure when credentials are stored in agent-readable memory.
- **Conditions:** Agent runs with auto-approval / auto mode; Agent is reachable by untrusted parties (public channels, custom bots); Credentials stored in agent-accessible context rather than injected at request time
- **Mitigations:** Sonnet auto-mode classifier that reads tool call + conversation context for dynamic permissioning; Credential injection via proxy so secrets are usable-but-not-readable by the agent; Red-team-generated adversarial environments converted into regression evals; Avoid hand-rolling custom bots with many attack vectors; rely on hardened auto mode

---

_Source: [https://simonwillison.net/2026/Jul/21/cat-and-thariq/](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)_  ·  [← back to index](../README.md)
