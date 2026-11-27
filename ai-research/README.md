# AI Research

> Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

_6 vetted findings · updated 2026-11-27 · ranked by composite · findings from the latest 31 days · [135 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[Hugging Face starts a series on training small multi-agent swarms](https://huggingface.co/blog/training-swarms)**
- **[NVIDIA releases Nemotron 3.5 Parse datasets, fine-tuning recipe and decoder](https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin)**
- **[ggml-org launches llama.cpp benchmark dashboard for AMD Ryzen and Radeon](https://huggingface.co/blog/ggml-org/llamacpp-amd-bench)**
- **[Hugging Face agent tunes Inkling 2 Mini, raising decode speed 40%](https://huggingface.co/blog/inkling-2-mini-inference-hillclimb)**
- **[OpenAI says GPT-6 models can design proteins that bind targets in lab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities)**
- **[Hugging Face guide shows how to build and validate an agentic evaluation](https://huggingface.co/blog/agentic-evals)**
- **[OpenAI proposes perplexity as a shared metric for pacing frontier model development](https://openai.com/index/perplexity-and-intelligence)**
- **[Google explains how Duplex phone-calling moved from narrow models to Gemini](https://research.google/blog/how-google-duplex-evolved-to-also-call-businesses-for-you-in-gemini/)**
- **[Hebbia says GPT-6 Astra beat rivals on citations and slides](https://openai.com/business/customer-stories/hebbia)**
- **[Google adds Tool Retrieval to the Gemini API to defer tool schemas](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/)**
- **[Google posts a Kent Walker and Walter Isaacson talk on creativity](https://blog.google/innovation-and-ai/technology/ai/dialogues-walter-isaacson/)**
- **[OpenAI says its Astra for Law configuration tops legal benchmarks](https://openai.com/index/astra-law-6-2)**
- **[OpenAI signs Apollo, METR, Transluce and Goodfire for embedded safety assessments](https://openai.com/index/our-first-phase-of-embedded-assessments)**
- **[JioStar architect says production evals need a validated judge and monitoring](https://openai.com/index/jiostar-vijay-seshadri)**
- **[Latent Space newsletter covers doubts about an Anthropic initial public offering (IPO)](https://latent.space/p/ainews-anthropic-ipo-whither-now/)**
- **[Ai2's ToyBlocks shows agent-written skill descriptions beat expert-written ones](https://huggingface.co/blog/allenai/toyblocks)**
- **[Gradium releases Phonon, a small on-device text-to-speech model](https://huggingface.co/blog/phonon-tts)**
- **[OpenAI releases GPT-6 Cyber, a vulnerability-hunting model limited to approved customers](https://www.theregister.com/security/2026/11/05/openai-releases-gpt-6-cyber-and-promises-this-one-stays-within-rules-of-engagement/5307855)**
- **[OpenAI says GPT-6 Astra quietly underperformed on AI safety research tasks](https://www.securityweek.com/openai-finds-gpt-6-astra-quietly-holding-back-on-internal-red-teaming-exploit-tasks/)**
- **[OpenAI finds agents score worse on safety evals than in production](https://alignment.openai.com/eval-production-behavior-gap/)**
- **[Ai2: LLM novelty judges flip verdicts when prompt wording changes slightly](https://huggingface.co/blog/allenai/novelty-bench)**
- **[OpenAI and Oracle expand their partnership to bring Oracle apps into ChatGPT](https://openai.com/index/oracle-apps-in-chatgpt)**
- **[Steve Francia runs Game Boy emulators on a GitHub Universe badge](https://simonwillison.net/2026/Oct/27/game-boy-color-on-my-conference-badge/)**
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
- **[Enhancing AI security through global AI red teaming](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/)**
- **[A frontier model built a bespoke zlib fuzzing lab in a day](https://blog.trailofbits.com/2026/07/02/field-reports-from-patch-the-planet/)**

| Domain | Findings |
| --- | --- |
| Cost Efficiency | 4 |
| Work Efficiency | 2 |

## Cost Efficiency

- **[Microsoft finds 8% of coding sessions account for 44% of costs](cost-efficiency/2026-11-microsoft-finds-8-of-coding-sessions-account-for-44-of-costs.md)** · composite **52.73** · Nov 12, 2026  
  If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.  
  _[Microsoft Research Blog](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)_
- **[UC Berkeley finds harness overhead can double agent cost at similar accuracy](cost-efficiency/2026-11-uc-berkeley-finds-harness-overhead-can-double-agent-cost-at.md)** · composite **50.75** · Nov 9, 2026  
  Measure how much of your agent spend is context rereads and harness overhead before tuning anything else.  
  _[UC Berkeley Sky Lab (Park et al.)](https://arxiv.org/abs/2611.12122)_
- **[York University's FlowPlan cuts Claude Code tokens by planning edits first](cost-efficiency/2026-11-york-university-s-flowplan-cuts-claude-code-tokens-by-planni.md)** · composite **50.75** · Nov 9, 2026  
  Replacing post-edit re-reading and re-testing with a stated plan cut coding agent tokens with no significant loss in fix rate.  
  _[York University (Sepidband et al.)](https://arxiv.org/abs/2611.13241)_
- **[Researchers find agents keep accuracy with short, frequently compacted contexts](cost-efficiency/2026-11-researchers-find-agents-keep-accuracy-with-short-frequently.md)** · composite **43.25** · Nov 3, 2026  
  Short, frequently compacted contexts kept accuracy here; on hosted APIs, test that against the cache hits each compaction gives up.  
  _[Belcak et al.](https://arxiv.org/abs/2611.05306)_

## Work Efficiency

- **[Anthropic verified its Python-to-Rust API migration against production traffic](work-efficiency/2026-11-anthropic-verified-its-python-to-rust-api-migration-against.md)** · composite **54.94** · Nov 25, 2026  
  When agents can generate changes faster than you can check them, invest in a production-shaped verifier plus a human gate between the agent sandbox and deployment.  
  _[Anthropic Research](https://www.anthropic.com/research/migrating-api-to-rust)_
- **[Claude Code team explains how it verifies agent-written code at scale](work-efficiency/2026-11-claude-code-team-explains-how-it-verifies-agent-written-code.md)** · composite **51.5** · Nov 17, 2026  
  Treat the verification layer as a system of its own: run the real app, keep the checks out of reach of the change, and measure the checks against past incidents.  
  _[@craigmart via Hacker News](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-research.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
