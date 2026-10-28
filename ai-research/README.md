# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_4 vetted findings · updated 2026-10-27 · ranked by composite · findings from the latest 31 days · [24 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://huggingface.co/blog/allenai/novelty-bench)**
- **[Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)**
  _Why now: Concrete production numbers (92% to 100%, back to 91% after a vLLM default change) that any team self-hosting open-weight models for agents can act on immediately. · high-relevance · timely_
- **[Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents)**
  _Why now: Directly usable harness change: a model-invoked compaction tool plus a fire/suppress rubric beats fixed token-threshold compaction across seven models. · trending · high-relevance_
- **[Anthropic describes presenting MCP servers as code APIs to save tokens](https://www.anthropic.com/research/code-execution-with-mcp)**
- **[Hugging Face launches an Open TTS Leaderboard ranking open text-to-speech models](https://huggingface.co/blog/open-tts-leaderboard)**
- **[MentalHealthBench scores model replies against weighted expert-consensus rubrics](https://openai.com/index/introducing-mentalhealthbench)**
- **[UK AISI publishes verified benchmark results showing scores shift with inference compute](https://huggingface.co/blog/evaleval-aisi)**
- **[OpenAI proposes US-led international technical standards for frontier AI](https://openai.com/index/building-standards-next-phase-ai)**
- **[OpenAI sets up fast-track misalignment disclosure and publishes six first reports](https://openai.com/index/model-misalignment-reporting-framework)**
- **[Trail of Bits says 1Password's AI patching benchmark is misleading](https://blog.trailofbits.com/2026/09/15/1passwords-ai-patching-benchmark-is-misleading/)**
- **[OpenAI launches the Agents API in public beta, a hosted Codex harness](https://openai.com/index/introducing-the-agents-api)**
- **[Hugging Face's funes shares agent memory from raw session text, not summaries](https://huggingface.co/blog/funes)**
- **[OpenAI's Astra preliminary evals can't rule out 'Critical' cyber capability](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)**
- **[Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai)**
- **[A frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)**

| Domain | Findings |
| --- | --- |
| Evaluation & Benchmarks | 3 |
| Alignment & Reliability | 1 |

## Evaluation & Benchmarks

- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](evals/2026-10-harness-delta-attribution-dissecting-gains-from-harness-evol.md)** · composite **57.93** · Oct 19, 2026  
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.  
  _[arXiv cs.AI (Artificial Intelligence)](https://arxiv.org/abs/2610.22466)_
- **[POPE yes/no readout uses token IDs the model never emits](evals/2026-10-pope-yes-no-readout-uses-token-ids-the-model-never-emits.md)** · composite **54.5** · Oct 19, 2026  
  If your eval or classifier reads yes/no from logits, check that the token IDs you read are the ones the model actually emits.  
  _[source](https://arxiv.org/abs/2610.25964)_
- **[OpenAI finds dataset-level g-mean² can misrank model monitorability](evals/2026-10-openai-finds-dataset-level-g-mean-can-misrank-model-monitora.md)** · composite **52.1** · Oct 20, 2026  
  If you use a monitor as a deployment gate, compare monitors and models on matched instances and measure what still gets through after rejection-and-retry, not raw discrimination alone.  
  _[OpenAI Alignment Blog](https://alignment.openai.com/beyond-gmean-squared/)_

## Alignment & Reliability

- **[METR: Anthropic's 'low misalignment risk' holds because models are weak, not monitoring](alignment/2026-10-metr-anthropic-s-low-misalignment-risk-holds-because-models.md)** · composite **57.5** · Oct 20, 2026  
  Test agent monitors end to end against a red team that argues its actions are legitimate; proxy covert-capability benchmarks are not evidence the monitor works.  
  _[source](https://metr.org/blog/2026-10-20-misalignment-risk-report-august-2026-review/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
