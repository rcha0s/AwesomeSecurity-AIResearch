# Caper approves coding-agent commands after running them in a snapshot sandbox

**Published:** Oct 29, 2026

> **Takeaway:** Judge an agent's command by what it actually does in a sandbox, not by how the command reads.

## TL;DR

Coding-agent approvers today judge a shell command by its text, but harm can hide in the code the command invokes. Caper runs each command first in a snapshotted sandbox, shows an independent approver a bounded report of what changed, then commits or rolls back. Against six existing approvers it had the lowest harmful-outcome rate on SABER (6.7% versus at least 14.8%) and on the authors' YoloFS-Ext benchmark (7.8% versus at least 35.3%), while blocking 1.0% of safe tasks.

## Lessons

- Rule checkers, guardrail models and permission classifiers all judge the command text, which misses behavior hidden in invoked code. - _"Existing approvers, from rule-based checkers to guardrail models and deployed permission classifiers, base their decisions on the text of the request and command."_
- The fix is to run first, observe effects, and approve or roll back with a reason the agent can use. - _"pre-executes each command in a snapshotted sandbox, provides an independent approver with a bounded report of its observed effects, commits allowed commands, and rolls back blocked ones with a reason the agent can act on"_
- When harm sits inside invoked tools, the best of six existing approvers still let 35.3% of harmful outcomes through. - _"YoloFS-Ext, a benchmark we build in which harmful behavior is hidden inside invoked tools (7.8% versus at least 35.3%)"_
- Effect-based approval blocks few safe tasks: 1.0% of the safe twins of the dangerous tasks in YoloFS-Ext. - _"while blocking 1.0% of the safe twins of the dangerous tasks in YoloFS-Ext"_

## Threat · Conditions · Mitigations

- **Threat:** A coding agent runs a command that looks harmless as text but invokes a script, test or tool whose code deletes, leaks or corrupts data.
- **Conditions:** An automated approver decides from the command text, and the harmful behavior lives in code the command calls or in workspace state.
- **Mitigations:** Pre-execute commands in a snapshotted sandbox, give an independent approver a report of observed effects, commit or roll back, and block network egress during the pre-run.

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [Hugging Face Daily Papers](https://arxiv.org/abs/2610.40753)  ·  **Retrieved:** 2026-11-04  
**Scores:** Newness 11 · Novelty 50 · Relevance 85 · Credibility 50 · **Composite 51** _(each 0-100)_  
**Tags:** `coding-agents`, `approval`, `permission-classifier`, `sandbox`, `rollback`, `human-in-the-loop`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Text-based approvers such as CC Safety Net (command-intent parsing), guardrail models and Claude Code's permission classifier; YoloFS-style snapshot and rollback filesystems restore state after the fact. Caper's delta is deciding before commit from observed effects, with an independent approver.

_Source: [https://arxiv.org/abs/2610.40753](https://arxiv.org/abs/2610.40753)_  ·  [← back to index](../README.md)
