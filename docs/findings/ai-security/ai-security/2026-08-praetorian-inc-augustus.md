# praetorian-inc/augustus

**Published:** Aug 9, 2026

> **Takeaway:** Multi-turn adversarial testing needs distinct engines for distinct target profiles. Backtracking (Hydra) hides refused turns from the target, while gradual escalation (Crescendo) exploits models that track conversation tone; picking the wrong one wastes budget on the wrong failure mode.

## TL;DR

Praetorian's Go-based LLM vulnerability scanner. 210+ probes across 47 attack categories (jailbreaks, prompt injection, adversarial examples, data extraction, agent attacks), 28 providers, 90+ detectors including LLM-as-judge. Adds multi-turn attack engines: Crescendo (gradual escalation), GOAT (adaptive technique switching), Hydra (turn-level backtracking on refusal), and Mischievous User (rapport-first drift).

## What to learn

- Multi-turn attacks succeed because models will disclose incrementally across turns what they refuse in a single prompt. The three-LLM pattern (attacker, target, judge) is the current baseline for automated evaluation of that failure. - _"Multi-turn attacks maintain a persistent conversation with the target LLM, exploiting the fact that models may disclose information incrementally across turns that they would refuse in a single prompt. The multi-turn engine uses three LLMs: an **attacker** (generates questions), a **target** (the system under test), and a **judge** (scores progress and detects refusals)."_
- Hydra's backtracking is structurally different from Crescendo/GOAT: refused turns are erased so the target never sees failed approaches, which prevents the target's own defensive escalation. - _"Hydra maintains a single conversation path and rolls back entire turns when the target refuses, asking the attacker for a completely different approach. Unlike Crescendo/GOAT (which rephrase on refusal), Hydra's backtracking completely removes refused turns from the target's view."_
- A casual-user persona (Mischievous User) is effective against models trained specifically to resist adversarial patterns. The subtle framing bypasses attack-detection heuristics that pattern-match on obvious jailbreak language. - _"Effective against models trained to resist obvious adversarial patterns - the casual persona bypasses "attack detection" heuristics"_

## Threat · Conditions · Mitigations

- **Threat:** LLM applications that pass single-prompt safety filters still fail under multi-turn adversarial pressure. An attacker with an automated attacker+judge stack can extract prohibited content, system prompts, secrets, or unsafe tool calls by gradually shifting the conversation, adaptively switching techniques, backtracking on refusal, or role-playing a benign curious user.
- **Conditions:** Target exposes a conversational API where message history is retained; attacker has ~10 turns of budget and access to a judge model; refusal detection is available but returns simple refusal signals rather than escalating full context defenses.
- **Mitigations:** Test the target with all four strategies (Crescendo, GOAT, Hydra, Mischievous User) rather than a single one; log full turn history and refusal events; add turn-limit and topic-drift monitors on production conversational endpoints; treat single-prompt safety benchmarks as necessary but not sufficient.

---

**Topic:** AI Security  ·  **Domain:** AI Security  
**Source:** [source](https://github.com/praetorian-inc/augustus)  ·  **Retrieved:** 2026-08-14  
**Scores:** Newness 20 · Novelty 60 · Relevance 78 · Credibility 55 · **Composite 54.65**  
**Tags:** `red-team`, `jailbreak`, `multi-turn`, `crescendo`, `goat`, `hydra`, `llm-scanner`  
**Verification:** ✓ independently verified · closest prior art: Overlaps with garak (research-oriented, Python) and promptfoo (TypeScript, more providers). Cites Russinovich et al. arXiv:2404.01833 for Crescendo and Pavlova et al. arXiv:2410.01606 for GOAT. Mischievous User is inspired by Tau-bench and promptfoo's mischievous-user strategy.

_Source: [https://github.com/praetorian-inc/augustus](https://github.com/praetorian-inc/augustus)_  ·  [← back to index](../README.md)
