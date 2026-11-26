# Poisoned reference answers can plant backdoor rules in optimized agent Skills

**Published:** Nov 6, 2026

> **Takeaway:** Whoever controls the reference answers used to optimize a Skill can plant a hidden trigger rule in it without touching the model, the optimizer or the Skill file, so treat that feedback as untrusted input.

## TL;DR

This NeurIPS workshop paper studies text-space Skill optimization (SkillOpt), where reference answers act as feedback that shapes reusable Skill text. On SearchQA, poisoning those reference answers left an exact trigger-to-payload rule in the final Skill in all three seeds, firing on 200/200 triggered and 0/200 clean questions with clean accuracy close to a benign run. On SpreadsheetBench, which needs an extra workbook edit, no natural run kept the exact rule, because the optimizer dropped required literals and edit-budget ranking removed exact edits.

## Lessons

- The attacker only needs to poison the reference answers used as feedback, not the model, optimizer or Skill file. - _"Poisoning those answers can induce a persistent trigger-conditioned rule without giving the attacker access to the model, optimizer, or Skill file."_
- On a short-answer task the backdoor fired perfectly on triggered inputs and never on clean ones. - _"each final Skill emits the payload on 200/200 triggered questions and 0/200 clean questions"_
- In one seed, clean accuracy barely moved, so a utility check alone would not reveal the poisoned Skill. - _"an in-run comparison shows similar clean accuracy to benign SkillOpt (169/200 versus 171/200)"_
- When the payload needs a more complex action, the optimizer's own abstraction and edit limits can stop the rule from surviving. - _"In SpreadsheetBench, where the payload requires an additional workbook edit, no natural run retains an exact rule across three seeds."_
- Exposure to poisoned feedback does not guarantee a backdoor; the rule must also be formed, selected and retained. - _"exposure alone does not ensure that the induced rule is formed, selected, and retained"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker who supplies reference answers to a Skill optimizer plants a persistent trigger-conditioned rule in the resulting Skill.
- **Conditions:** Shown on SkillOpt only; the attack held for short-answer payloads on SearchQA but not naturally for payloads needing an extra edit on SpreadsheetBench; results are from three seeds in a workshop paper.
- **Mitigations:** Use trusted reference answers, diff and review optimized Skills for literal trigger-payload rules, and test Skills on trigger-like inputs in addition to clean accuracy.

---

**Topic:** AI Security  ·  **Domain:** Memory, RAG & Data Poisoning  
**Source:** [NeurIPS (via arXiv)](http://arxiv.org/abs/2611.09348v1)  ·  **Retrieved:** 2026-11-09  
**Scores:** Newness 24 · Novelty 55 · Relevance 65 · Credibility 72 · **Composite 53** _(each 0-100)_  
**Tags:** `agent-skills`, `skill-optimization`, `backdoor`, `data-poisoning`, `feedback-poisoning`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Instruction-backdoor work on customized coding LLMs (ARIA-style red teaming) and the archive's external-evidence step for self-evolving skill libraries; this paper moves the poisoning point to optimizer feedback

_Source: [http://arxiv.org/abs/2611.09348v1](http://arxiv.org/abs/2611.09348v1)_  ·  [← back to index](../README.md)
