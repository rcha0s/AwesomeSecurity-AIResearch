# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_3 vetted findings · updated 2026-10-24 · ranked by composite · findings from the latest 31 days · [3 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[Hugging Face's funes: shared agent memory that keeps the raw session text, not summaries](https://huggingface.co/blog/funes)**
- **[OpenAI: Astra preliminary evals can't rule out 'Critical' cyber capability; new controls include CoT-based universal monitoring](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)**
- **[Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai)**
- **[Goal-persistent agents: a frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)**

| Domain | Findings |
| --- | --- |
| Evaluation & Benchmarks | 2 |
| Alignment & Reliability | 1 |

## Evaluation & Benchmarks

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](evals/2026-10-harness-delta-attribution-dissecting-gains-from-harness-evol.md)** · composite **59.18** · Oct 19, 2026  
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.  
  _[arXiv cs.AI (Artificial Intelligence)](https://arxiv.org/abs/2610.22466)_
- **[POPE yes/no readout uses token IDs the model never emits, moving F1 more than most published gains](evals/2026-10-pope-yes-no-readout-uses-token-ids-the-model-never-emits-mov.md)** · composite **55.75** · Oct 19, 2026  
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.  
  _[source](https://arxiv.org/abs/2610.25964)_

## Alignment & Reliability

- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not because the monitoring would catch it](alignment/2026-10-metr-anthropic-s-low-misalignment-risk-holds-because-models.md)** · composite **58.75** · Oct 20, 2026  
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.  
  _[source](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
