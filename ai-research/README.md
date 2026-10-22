# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_5 vetted findings · updated 2026-10-22 · ranked by composite · findings from the latest 31 days · [2 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Evaluation & Benchmarks | 2 |
| Alignment & Reliability | 1 |
| Models & Capabilities | 1 |
| Agents & Harnesses | 1 |

## Evaluation & Benchmarks

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](evals/2026-10-harness-delta-attribution-dissecting-gains-from-harness-evol.md)** · composite **59.93** · Oct 19, 2026  
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.  
  _[arXiv cs.AI (Artificial Intelligence)](https://arxiv.org/abs/2610.22466)_
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](evals/2026-10-pope-yes-no-readout-uses-token-ids-the-model-never-emits-mov.md)** · composite **56.5** · Oct 19, 2026  
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.  
  _[source](https://arxiv.org/abs/2610.25964)_

## Alignment & Reliability

- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](alignment/2026-10-metr-anthropic-s-low-misalignment-risk-holds-because-models.md)** · composite **59.5** · Oct 20, 2026  
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.  
  _[source](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)_

## Models & Capabilities

- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](models/2026-08-openai-astra-preliminary-evals-can-t-rule-out-critical-cyber.md)** · composite **55.75** · Aug 7, 2026  
  The Preparedness Framework's Critical threshold is now a real trigger, not a hypothetical; the announced response leans on CoT-based universal monitoring and isolated environments rather than better…  
  _[source](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)_

## Agents & Harnesses

- **[Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](agents/2026-07-goal-persistent-agents-a-frontier-model-built-a-bespoke-zlib.md)** · composite **55.65** · Jul 2, 2026  
  When you hand an agent a durable goal plus strict 'what counts as a real finding' rules, it will plan multi-step tooling and self-filter noise - the rules, not the model alone, are what make the…  
  _[source](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
