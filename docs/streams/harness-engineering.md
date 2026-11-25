# Harness Engineering

_How to build agent and coding harnesses that cost less, run faster, fail less and get more correct work done: measured results from papers, lab and practitioner engineering blogs, with the standing claims they support._

_Generated 2026-11-24 from the claim ledger, the pools and the archive of [Awesome Security & AI Research](https://rcha0s.github.io/AwesomeSecurity-AIResearch/) by the rules in `data/streams.yaml`. Generated - do not hand-edit._

This page is meant to be fetched by an agent harness, like [efficiency.md](https://rcha0s.github.io/AwesomeSecurity-AIResearch/efficiency.md), which covers the first two sub-categories. Each claim is a standing answer: **Do this** is the change to make, **Conditions** is where it does not hold, and the evidence is newest first. Findings are research from the last 120 days, newest first; **Worth a look** findings had their quotes checked against the source and passed, but sat below the Briefing's score bar. The same data as JSON Feed 1.1: [harness-engineering.json](https://rcha0s.github.io/AwesomeSecurity-AIResearch/streams/harness-engineering.json) (filter items by `_stream.subcategory`).

33 live claims, 15 vetted findings, 13 worth a look.

- [Cost efficiency](#cost-efficiency): 11 claims, 8 findings
- [Work efficiency](#work-efficiency): 6 claims, 1 finding
- [Speed and latency](#speed-latency): 0 claims, 0 findings
- [Reliability and recovery](#reliability): 0 claims, 1 finding
- [Context and memory](#context-memory): 5 claims, 1 finding
- [Tools and interfaces](#tools-interfaces): 3 claims, 3 findings
- [Orchestration and multi-agent](#orchestration): 0 claims, 2 findings
- [Evaluating harnesses](#harness-evals): 2 claims, 7 findings
- [Harness design](#harness-design): 6 claims, 5 findings

<a id="cost-efficiency"></a>

## Cost efficiency

_Token use and spend - prompt caching, context budgets, cheaper subagents and model routing, keeping tool output out of context, cost per task._

### Use one-hour cache markers when sessions pause over five minutes

`one-hour-cache-for-paused-sessions` · current · confidence 0.50 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=one-hour-cache-for-paused-sessions#claims)

Harnesses that write 5-minute prompt-cache markers re-buy their whole context after an idle gap longer than five minutes, while harnesses with 1-hour markers kept about 86% cache hits after a 390-second pause.

**Do this:** For interactive sessions where people or tools often pause for more than five minutes, cache the stable prefix with the 1-hour TTL; keep 5-minute caching for tight automated loops.

**Conditions:** One vendor-authored report, a single trial per harness and one idle gap. Anthropic prices 1-hour cache writes at 2x input against 1.25x for 5-minute writes, so short sessions with no long pauses can cost more.

Evidence, newest first:
- supports: [The Cache Wars: An Empirical Study of Prompt-Cache Efficiency in Six LLM Agent Harnesses](https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses) (2026-07-07) After a 390-second pause, 1-hour-marker harnesses kept about 86% cache hits and 5-minute-marker harnesses kept none.
- supports: [Anthropic API docs: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

### Learn per-repo cost controls from past coding agent runs

`learn-per-repo-cost-controls` · current · confidence 0.55 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=learn-per-repo-cost-controls#claims)

A controller that learns from earlier runs in the same repository which tools to prune, which short notes to inject and when to stop unproductive failure loops cut coding-agent cost by 18-31% on SWE-Bench with comparable task success.

**Do this:** Log where tokens go across runs in one repo; prune tools the repo never uses, add short notes for operations the agent keeps rediscovering, and guard against loops that keep failing the same way while letting recoverable ones continue.

**Conditions:** Measured on sequences of tasks in the same repositories; a one-off task in a new repo has no history to learn from.

Evidence, newest first:
- supports: [TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents](https://arxiv.org/abs/2610.22732) (2026-10-15) Mean cache-aware cost fell 18.4-30.9% across five settings; Pass@1 improved in four and fell 1.0 point on Opus 4.8.

### Harness choice alone can double an agent's cost

`harness-overhead-sets-agent-cost` · current · confidence 0.65 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-overhead-sets-agent-cost#claims)

On the same model and task, the harness alone changed cost up to about 2x at similar accuracy, and coding agents' first call ranges from about 1.9k to 32k input tokens.

**Do this:** Measure what your harness spends per task (fixed prompt and tool schemas, plus re-reading context) and cut what does not change outcomes before you switch models.

**Conditions:** Shown on coding benchmarks and a one-word prompt with Nov 2026 harness versions; how much the overhead costs depends on how much of it is cached and how long sessions run.

Evidence, newest first:
- supports: [System Optimizations for Cost-Efficient Agent Harnesses](https://arxiv.org/abs/2611.12122) (2026-11-09) Harness choices changed cost by up to 2.6x on the same model and task while barely moving accuracy; Claude Code and Codex easily reached 2x the cost of a basic harness.
- supports: [Harness Overhead Benchmark: How Many Tokens 11 Coding Agents Burn Before the Test Starts](https://testdino.com/blog/harness-overhead-benchmark) (2026-10-09) A one-word prompt cost 1,894 to 31,798 input tokens across 11 coding agents, a 16.8x spread.

### Keep the prompt prefix stable so cache reads dominate

`stable-prompt-prefix-keeps-cache-reads-cheap` · current · confidence 0.80 · updated 2026-11-09 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=stable-prompt-prefix-keeps-cache-reads-cheap#claims)

A harness that keeps its context append-only and its prefix stable gets cached input at roughly a tenth of the uncached price.

**Do this:** Never edit earlier turns or reorder the system prompt/tools mid-session; only append.

**Conditions:** Applies where the provider offers prefix caching; savings depend on cache lifetime and how often the prefix really repeats.

Evidence, newest first:
- supports: [FlowPlan: Reducing the Token Cost of Coding Agents with Abstraction-Guided Planning and Verification](https://arxiv.org/abs/2611.13241) (2026-11-09) Claude Code on SWE-bench Pro averaged 3.7 million tokens per issue, 98% of them cache reads, so cache price dominates long runs.
- supports: [Context Engineering in 2026: Why We Stopped Compacting Our Agent's Context](https://www.louisbouchard.ai/context-engineering-2026/) (2026-08-18) The cache only hits when the previous context is resent unchanged; a summary shortens the prefix by changing it, so the cache misses.
- supports: [The Cache Wars: An Empirical Study of Prompt-Cache Efficiency in Six LLM Agent Harnesses](https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses) (2026-07-07) Pause test across six harnesses: those with 1-hour cache markers kept about 86% cache hits after a 390-second idle gap, those with 5-minute markers re-bought their whole context. Single trial per cell; the author's company makes one of the…
- supports: [Manus: Context Engineering for AI Agents Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) (2025-07-18) "If I had to choose just one metric, I'd argue that the KV-cache hit rate is the single most important metric for a production-stage AI agent."
- supports: [Manus: Context Engineering for AI Agents Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) (2025-07-18) "Make your context append-only."
- supports: [Anthropic API docs: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)."
- supports: [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices) "That’s discounted while the cache is warm and full price once it expires."

### Keep intermediate tool results out of the model context

`keep-bulk-tool-output-out-of-context` · current · confidence 0.65 · updated 2026-11-09 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=keep-bulk-tool-output-out-of-context#claims)

In Anthropic's own measurement, processing tool output in code and passing only results to the model cut average tokens by 37% on complex research tasks.

**Do this:** Run bulk filtering in a code sandbox or write long output to a file and let the agent grep it.

**Conditions:** Needs a code sandbox or file access the agent can search; a single small tool result gains little.

Evidence, newest first:
- supports: [System Optimizations for Cost-Efficient Agent Harnesses](https://arxiv.org/abs/2611.12122) (2026-11-09) Rereading existing context was the largest cost in real executions even with caching; compacting tool output, batching tool calls and metadata-assisted search cut cost up to 35% on unmodified Claude Code and Codex (UC Berkeley).
- supports: [Anthropic Engineering: advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) (2025-11-24) "Average usage dropped from 43,588 to 27,297 tokens, a 37% reduction on complex research tasks."
- supports: [Manus: Context Engineering for AI Agents Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) (2025-07-18) "That's why we treat the file system as the ultimate context in Manus: unlimited in size, persistent by nature, and directly operable by the agent itself."
- supports: [Anthropic Engineering: writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) "In this example, we use ~⅓ of the tokens with “concise” tool responses."

### Load tool definitions on demand, not all at start

`load-tool-definitions-on-demand` · current · confidence 0.65 · updated 2026-11-08 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=load-tool-definitions-on-demand#claims)

Vendors report that loading tool definitions only when needed cut tokens by 47% (Cursor A/B test, runs that called an MCP tool) to 85% (Anthropic Tool Search); Anthropic's 98.7% is a single worked example.

**Do this:** Expose tool names only, and fetch a tool's schema when the task needs it.

**Conditions:** Measured by the vendors on their own harnesses; gains grow with the number of tools or MCP servers installed.

Evidence, newest first:
- supports: [ratel-ai/ratel](https://github.com/ratel-ai/ratel) (2026-11-08) Library that searches a BM25 tool and skill catalog per turn instead of loading every schema; its token savings are self-reported.
- supports: [TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents](https://arxiv.org/abs/2610.22732) (2026-10-15) An external controller that prunes unused tools, injects short micro-skills and stops failure loops cut mean cache-aware SWE-Bench cost 18.4-30.9% across Claude Code, Codex and Copilot CLI with comparable Pass@1 (Microsoft Research, UC Ber…
- supports: [Harness Overhead Benchmark: How Many Tokens 11 Coding Agents Burn Before the Test Starts](https://testdino.com/blog/harness-overhead-benchmark) (2026-10-09) A one-word prompt cost 1,894 to 31,798 input tokens across 11 coding agents (16.8x spread); the post recommends deferring tools and trimming always-on instructions. Three runs per agent, one repo.
- supports: [Cursor: dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery) (2026-01-06) "In an A/B test, we found that in runs that called an MCP tool, this strategy reduced total agent tokens by 46.9% (statistically significant, with high variance based on the number of MCPs installed)."
- supports: [Anthropic Engineering: advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) (2025-11-24) "This represents an 85% reduction in token usage while maintaining access to your full tool library."
- supports: [Anthropic Engineering: code execution with mcp](https://www.anthropic.com/engineering/code-execution-with-mcp) (2025-11-04) "This reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7% ."

### Compact near the context limit; reset only if the model needs it

`compact-first-reset-only-if-the-model-needs-it` · current · confidence 0.65 · updated 2026-11-03 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=compact-first-reset-only-if-the-model-needs-it#claims)

A harness should compact long sessions automatically, and add hard context resets only for models that wrap up early near the limit.

**Do this:** Enable auto-compaction first; test whether resets still help on your current model.

**Conditions:** Model-specific: whether resets still help changes with each model generation.

Evidence, newest first:
- supports: [You don't need long context](https://arxiv.org/abs/2611.05306) (2026-11-03) With Claude Opus 4.5 and GPT 5.6 Sol, frequent compaction kept contexts short while broadly maintaining accuracy on long-horizon and long-input tasks.
- contests: [Context Engineering in 2026: Why We Stopped Compacting Our Agent's Context](https://www.louisbouchard.ai/context-engineering-2026/) (2026-08-18) In paired trajectories a compacting preset sent about 41% fewer tokens yet paid roughly twice as much because each summary broke the cache; leaving the context untouched and capping tool output was cheapest.
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "Context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps—addresses both these issues."
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely."
- supports: [Anthropic Engineering: effective context engineering for ai agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025-09-29) "Compaction typically serves as the first lever in context engineering to drive better long-term coherence."

### Prefer the simplest pipeline that solves the task

`simplest-pipeline-first` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=simplest-pipeline-first#claims)

A harness should start with a simple fixed workflow, since in 2024 the non-agentic Agentless pipeline scored highest among open-source agents on SWE-bench Lite (32.00%) at $0.70 per task, in the authors' own evaluation.

**Do this:** Add agent loops, tools or subagents only after a simpler version fails on your evals.

**Conditions:** The Agentless result is the authors' own 2024 evaluation on SWE-bench Lite; stronger models since may shift where agent loops pay off.

Evidence, newest first:
- supports: [Anthropic Engineering: building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024-12-19) "we recommend finding the simplest solution possible, and only increasing complexity when needed."
- supports: [arXiv: Agentless: 2407.01489](https://arxiv.org/abs/2407.01489) (2024-07-01) "Our results on the popular SWE-bench Lite benchmark show that surprisingly the simplistic Agentless is able to achieve both the highest performance (32.00%, 96 correct fixes) and low cost ($0.70) compared with all existing open-source sof…

### Treat multi-agent as a token multiplier; use it where breadth pays

`multi-agent-multiplies-token-spend` · contested · confidence 0.60 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=multi-agent-multiplies-token-spend#claims)

A harness should use multi-agent runs only for breadth-first tasks, because they use about 15 times the tokens of chat.

**Do this:** Default to one agent; spawn parallel subagents only for independent, high-value branches and track tokens per run.

**Conditions:** Whether the multiplier pays depends on the task's breadth and value; the numbers are Anthropic's own.

Evidence, newest first:
- contests: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "The harness was over 20x more expensive, but the difference in output quality was immediately apparent."
- supports: [Anthropic Engineering: multi agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."
- supports: [Anthropic Engineering: multi agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) "Multi-agent architectures effectively scale token usage for tasks that exceed the limits of single agents."
- supports: [Anthropic Engineering: multi agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) "Our internal evaluations show that multi-agent research systems excel especially for breadth-first queries that involve pursuing multiple independent directions simultaneously."

### Return short tool responses and distilled subagent summaries

`concise-tool-responses-and-subagent-summaries` · current · confidence 0.65 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims)

A harness that makes tools return concise fields, and subagents return condensed summaries (often 1,000-2,000 tokens), keeps the main context smaller; Anthropic's example used about a third of the tokens.

**Do this:** Offer a concise response format on tools and cap subagent reports.

**Conditions:** Shown on Anthropic's own examples, not a controlled study.

Evidence, newest first:
- supports: [Context Engineering in 2026: Why We Stopped Compacting Our Agent's Context](https://www.louisbouchard.ai/context-engineering-2026/) (2026-08-18) Capping tool output alone took cost per turn from $0.189 to $0.117 (38%) and won 14 of 15 paired trajectories.
- supports: [Anthropic Engineering: effective context engineering for ai agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025-09-29) "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."
- supports: [Anthropic Engineering: writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) "In this example, we use ~⅓ of the tokens with “concise” tool responses."

### Send simple subagent jobs to a cheaper model

`cheaper-models-for-simple-subagent-jobs` · current · confidence 0.55 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=cheaper-models-for-simple-subagent-jobs#claims)

Anthropic's docs recommend routing simple subagent jobs to a cheaper model such as Haiku, and Aider's architect/editor split shows a reasoning model can pair with a weaker editor without losing quality.

**Do this:** Set Haiku-class models on search and summarizing subagents; keep the top model for the lead.

**Conditions:** No source here measures the cost saving; Aider's result is about quality, not cost.

Evidence, newest first:
- supports: [Does routing coding agent subtasks to cheaper models pay off? A benchmark of 63 runs per arm](https://dev.to/arthur031221/does-routing-coding-agent-subtasks-to-cheaper-models-pay-off-a-benchmark-of-63-runs-per-arm-4cdd) (2026-10-22) Routing subtasks to a cheaper worker model cut list-price cost 1.24x ($9.56 to $7.69 over 63 runs per arm) with quality 0.96 in both arms; routes were tuned on the same 21 tasks, by the author of the routing plugin.
- supports: [Aider: architect](https://aider.chat/2024/09/26/architect.html) (2024-09-26) "Using o1-preview as the Architect with either DeepSeek or o1-mini as the Editor produced the SOTA score of 85%."
- supports: [Claude Code docs: sub agents](https://code.claude.com/docs/en/sub-agents) "Control costs by routing tasks to faster, lower-cost models like Haiku"
- supports: [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices) "Haiku is a good fit for subagents doing simple jobs."

**New research** (5)

- **[Microsoft finds 8% of coding sessions account for 44% of costs](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)** · 2026-11-12 · Microsoft Research Blog
  If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.
  Try: Measure compaction cost share and try background summarization. Log which sessions trigger compaction and what share of total tokens and cost they use. Then test a background summarizer that builds a running summary while the agent works, and swap it in at the threshold instead of pausing for a synchronous summary. Compare task success, cost and wall-clock time against the current method.
- **[York University's FlowPlan cuts Claude Code tokens by planning edits first](https://arxiv.org/abs/2611.13241)** · 2026-11-09 · York University (Sepidband et al.)
  Replacing post-edit re-reading and re-testing with a stated plan cut coding agent tokens with no significant loss in fix rate.
  Try: Add a stated-plan check before edits. For bug-fix tasks, have the agent write down which functions it will change and how before editing, then check the diff against that plan instead of re-reading files and rerunning the full suite after each edit. Track turns and cache-read tokens per resolved issue.
- **[UC Berkeley finds harness overhead can double agent cost at similar accuracy](https://arxiv.org/abs/2611.12122)** · 2026-11-09 · UC Berkeley Sky Lab (Park et al.)
  Measure how much of your agent spend is context rereads and harness overhead before tuning anything else.
  Try: Audit fixed overhead, then batch tool calls. Log input tokens per turn split into system prompt, tool schemas, cached history and new content for a week of real sessions. Cut always-on instructions and unused tool schemas, add a system-prompt line asking the model to batch independent reads into one turn, and compare cost per completed task before and after.
- **[Researchers find agents keep accuracy with short, frequently compacted contexts](https://arxiv.org/abs/2611.05306)** · 2026-11-03 · Belcak et al.
  Short, frequently compacted contexts kept accuracy here; on hosted APIs, test that against the cache hits each compaction gives up.
  Try: Test frequent compaction against your cache savings. Run the same task set with compaction at the context limit, at a lower threshold, and with long inputs moved to files the agent reads on demand. Compare accuracy and total cost including cache writes, since each compaction rewrites the prefix and loses cache hits.
- **[Letting the agent choose when to compact matches fixed-interval summarization cheaply](https://machinelearning.apple.com/research/self-compacting-language-agents)** · 2026-10-12 · Apple Machine Learning Research
  Replace or supplement token-threshold compaction with a model-invoked compaction tool plus an explicit rubric for when to fire and when to hold off.
  Try: Add a model-invoked compact tool with a fire/suppress rubric. Expose a compact\_context tool that summarizes the trajectory so far and replaces it. In the system prompt, add the rubric: call it when a sub-task has just resolved or the solution is converging; do not call it mid-derivation or while stuck. Keep the token-threshold compaction as a hard fallback. A/B test against fixed-interval compaction on held-out tasks for accuracy and per-task cost.

**Worth a look** (3)

- **[Google adds Tool Retrieval to the Gemini API to defer tool schemas](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/)** · 2026-11-19 · Google AI Blog
  Deferring tool schemas is now a built-in API feature, so large tool libraries need not be sent in full on every request.
  Try: Defer tool schemas for large tool libraries. If your agent carries dozens of tools, keep names and one-line descriptions in context and load full parameter schemas only when a tool is chosen. In the Gemini Interactions API add a tool\_search tool and set defer\_loading true on the tools to hold back; it is in preview and needs Gemini 3.6 or later. Measure input tokens and tool-selection accuracy before and after, since the post reports no numbers in the text read.
- **[Token-Goat hooks coding agents to cut repeat reads and bulky tool output](https://github.com/DFKHelper/token-goat)** · 2026-11-04 · DFKHelper/token-goat
  Most agent token waste is repeat reads and noisy tool output, which hooks can trim without changing the model.
  Try: Deduplicate repeat reads and trim tool logs in hooks. Add PreToolUse and PostToolUse hooks that answer a re-read of an unchanged file with a pointer, strip passing tests and progress bars from build and test output, and downscale screenshots before they reach the model. Measure cost per task before and after rather than trusting the author's savings figures. A third-party hook sees every tool call, so review its code before installing it.
- **[Legora evaluates legal agent on simulated work because it cannot read traces](https://latent.space/p/building-ai-for-lawyers-jacob-lauritzen-cto-of-legora/)** · 2026-11-02 · Latent Space
  When you cannot read customer traces, build simulated task worlds with domain experts and track results per task type, because a new model can regress on some tasks while improving overall.
  Try: Track evals per task type and pilot bulk runs on a small sample. If production traces are off-limits, have domain experts build a few realistic simulated environments, such as a seeded document room with planted issues, and score each task type separately in a per-task heat map so a model swap that regresses one area is visible. Write down a fixed list of 10 to 20 failure modes and run a cheap LLM check for each behind a feature flag. For any fan-out extraction job, run the first 10 or so items and review them before launching the rest.


<a id="work-efficiency"></a>

## Work efficiency

_More correct work per hour - planning and spec steps, task decomposition, delegation, parallel agents, verification loops, measured productivity._

### Split generating from evaluating with a separate grader

`separate-grader-from-generator` · current · confidence 0.50 · updated 2026-11-05 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=separate-grader-from-generator#claims)

A separate evaluator scoring against explicit criteria was part of a three-agent harness that cost over 20x a solo run and, in the author's judgment on one prompt, produced visibly better output.

**Do this:** Write gradable criteria and run a fresh-context reviewer; keep it for tasks where quality justifies the spend.

**Conditions:** Worth it where quality is subjective or costly to get wrong; the cost makes it a poor default for routine work.

Evidence, newest first:
- supports: [OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/) (2026-11-05) 20 of 200 exploits the agent marked successful reached root through a different 0-day, so OpenAI added an independent check that each exploit used its assigned bug.
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "Building an evaluator that graded outputs reliably—and with taste—meant first developing a set of criteria that could turn subjective judgments like “is this design good?” into concrete, gradable terms."
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "The harness was over 20x more expensive, but the difference in output quality was immediately apparent."

### Re-test harness scaffolding whenever the model changes

`retest-harness-scaffolding-on-model-change` · current · confidence 0.60 · updated 2026-11-05 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=retest-harness-scaffolding-on-model-change#claims)

A harness should treat each component as an assumption about model weakness, stress-test it on each model upgrade, and remove it if it is no longer needed.

**Do this:** Ablate one component at a time on each model upgrade and keep only what moves your eval.

**Conditions:** A principle backed by Anthropic's experience, not a controlled study.

Evidence, newest first:
- supports: [OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/) (2026-11-05) A curated exploitation-technique library raised the older model's success from 76.2% to 88.9% but added only 1.5 points for the newer model, so OpenAI dropped it.
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "This was partly common sense and partly a function of a more general principle: every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they…
- supports: [Anthropic Engineering: effective context engineering for ai agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025-09-29) "We're already seeing that smarter models require less prescriptive engineering, allowing agents to operate with more autonomy."

### Verify end-to-end as a user, not only with unit tests

`verify-end-to-end-as-a-user` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=verify-end-to-end-as-a-user#claims)

A harness should make the agent exercise the running app (browser automation) before marking work done, since unit tests and curl miss broken features.

**Do this:** Require a browser-driven check or /verify-style step before a task is marked complete.

**Conditions:** For user-facing apps; library code may be fully covered by tests.

Evidence, newest first:
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "In the case of building a web app, Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools and do all testing as a human user would."
- supports: [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices) "That catches the kind of problem that tests and typechecks miss."

### Persist a feature list and progress log across sessions

`persist-feature-list-and-progress-across-sessions` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=persist-feature-list-and-progress-across-sessions#claims)

A harness for long tasks should write a structured feature list and progress file so each new session can resume instead of one-shotting the app.

**Do this:** Have an initializer write a JSON feature list, init script and progress file; work one feature per session.

**Conditions:** For multi-session builds; short single-session tasks don't need the scaffolding.

Evidence, newest first:
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "First, the agent tended to try to do too much at once—essentially to attempt to one-shot the app."
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "Set up a feature list file: based on the input spec, set up a structured JSON file with a list of end-to-end feature descriptions."
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "In our experiments, we found that the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages and to write summaries of its progress in a progress file."

### Parallelize independent reads; keep writes single-threaded

`parallel-reads-single-threaded-writes` · current · confidence 0.65 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=parallel-reads-single-threaded-writes#claims)

A harness should fan out parallel subagents for independent research but keep code-writing in one context, since Cognition argues parallel writers act on conflicting assumptions.

**Do this:** Parallelize search and review; serialize edits through one agent that holds the shared context.

**Conditions:** Research and search parallelize well; shared-state work like coding is where parallel writers conflict.

Evidence, newest first:
- supports: [Anthropic Engineering: multi agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) "We found that a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval."
- supports: [Anthropic Engineering: multi agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) "Further, some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today."
- supports: [Cognition: dont build multi agents](https://cognition.ai/blog/dont-build-multi-agents) (2025-06-12) "The simplest way to follow the principles is to just use a single-threaded linear agent: Here, the context is continuous."
- supports: [Cognition: dont build multi agents](https://cognition.ai/blog/dont-build-multi-agents) (2025-06-12) "The actions subagent 1 took and the actions subagent 2 took were based on conflicting assumptions not prescribed upfront."

### Measure speedups with repeated trials, not impressions

`measure-speedups-with-repeated-trials` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=measure-speedups-with-repeated-trials#claims)

A harness team should judge work efficiency with repeated-trial evals or timed studies, since in METR's early-2025 study developers believed AI sped them up while it slowed them down.

**Do this:** Track time-to-merged-change and pass rate over multiple trials per task before claiming a gain.

**Conditions:** METR studied experienced developers on their own large repos in early 2025; METR published newer data on late-2025 tools in February 2026.

Evidence, newest first:
- supports: [Anthropic Engineering: demystifying evals for ai agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (2026-01-09) "Because model outputs vary between runs, we run multiple trials to produce more consistent results."
- supports: [METR: 2025 07 10 early 2025 ai experienced os dev study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) "Surprisingly, we find that when developers use AI tools, they take 19% longer than without—AI makes them slower."
- supports: [METR: 2025 07 10 early 2025 ai experienced os dev study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) "developers expected AI to speed them up by 24%, and even after experiencing the slowdown, they still believed AI had sped them up by 20%."

**New research** (1)

- **[Claude Code team explains how it verifies agent-written code at scale](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)** · 2026-11-17 · @craigmart via Hacker News
  Treat the verification layer as a system of its own: run the real app, keep the checks out of reach of the change, and measure the checks against past incidents.
  Try: Add a verify skill and an observe-mode commit gate. Create a .claude/skills/verify skill next to the code that boots the app and drives it (browser, simulator or local service). Load review rules (such as REVIEW.md) from the default branch only. Add a commit gate with off, observe and enforce modes, stamp each commit with how it was verified (including 'none'), and let a commit through after two blocks so the agent is not stuck.


<a id="speed-latency"></a>

## Speed and latency

_Wall-clock time per task, agent-loop and tool latency, parallel and speculative tool calls, cache reuse for speed._

_Nothing yet: no live claim or finding in the window._


<a id="reliability"></a>

## Reliability and recovery

_Getting runs to finish correctly - error recovery, loop and stall detection, long-horizon drift, failure taxonomies, tracing, run-to-run variance._

**New research** (1)

- **[OrchestraBench evaluates multi-agent orchestration failures and recovery](https://arxiv.org/abs/2608.05263)** · 2026-08-07
  Multi-agent orchestration failures are not uniform: tool faults recover, ambiguous delegation partially recovers, latent/semantic faults essentially never self-heal. Blind retry hides latent faults and delays detection, so containment requires an external trusted-state signal, not just per-agent detection. Keyword/flag routers collapse on adversarially framed inputs where an intent-reasoning rout…
  Try: Add failure-mode breakdown and cascade radius to agent evals. For internal multi-agent evals, separate tool-fault, ambiguous-delegation, and latent/semantic-error rates instead of reporting a single task-success number, and record cascade radius across pipeline depths. Do not rely on blind-retry for containment; add a trusted-state signal (external verifier or ground-truth check) at the boundary between agents.


<a id="context-memory"></a>

## Context and memory

_What the model sees - context engineering, compaction, agent memory, retrieval for agents, long-context failure modes._

### System prompts are load-bearing config — version them like code

`system-prompts-should-be-versioned-like-code` · current · confidence 0.70 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=system-prompts-should-be-versioned-like-code#claims)

Production system prompts are load-bearing configuration and should be version-controlled, code-reviewed, and evaluated on regression suites.

**Do this:** Store prompts in the same repo as the code that calls them. Run eval on every prompt change and every model change.

**Conditions:** A practice recommendation backed by vendor guidance and first-party practice, not a controlled study.

Evidence, newest first:
- supports: [Claude Code team: incident PRs become eval cases, and the system prompt was cut 80% as models changed](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)
- supports: [Claude docs: Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) (2024-07)

### Retrieval quality dominates generator quality in RAG

`retrieval-quality-dominates-generation-quality-in-rag` · current · confidence 0.75 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=retrieval-quality-dominates-generation-quality-in-rag#claims)

In production RAG systems, retrieval quality dominates generation quality as a determinant of end-task accuracy; larger models cannot compensate for a bad retriever.

**Do this:** Invest in retrieval evals (recall@k, reranker quality) before spending on bigger generator models.

Evidence, newest first:
- supports: [Deeper insights into retrieval augmented generation: the role of sufficient context](https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/) (2025-05-14) Even frontier models fail to abstain on insufficient context and hallucinate confidently instead - generation quality cannot compensate for what retrieval didn't surface.
- supports: [Retrieval-Augmented Generation for LLMs: A Survey](https://arxiv.org/abs/2312.10997) (2023-12)

### Long context windows don't remove the need for retrieval

`long-context-does-not-eliminate-retrieval-need` · current · confidence 0.80 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=long-context-does-not-eliminate-retrieval-need#claims)

Long-context models do not eliminate the need for retrieval: they exhibit lost-in-the-middle effects, cost grows linearly with context size, and per-token attention drops on distant tokens.

**Do this:** Retrieval + a short, relevant context still beats stuffing a long context on cost, latency, and accuracy for most tasks.

Evidence, newest first:
- supports: [Context Length Alone Hurts LLM Performance Despite Perfect Retrieval](https://arxiv.org/abs/2510.05381) (2025-10) Performance degrades 13.9-85% as input length grows even when retrieval is perfect - context length itself is a cost independent of retrieval quality.
- supports: [Lost in the Middle](https://arxiv.org/abs/2307.03172) (2023-07)

### Hybrid BM25 + vector search beats pure vector retrieval

`hybrid-search-beats-pure-vector-for-most-domains` · current · confidence 0.80 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=hybrid-search-beats-pure-vector-for-most-domains#claims)

Hybrid search (BM25 + dense vectors) outperforms pure vector retrieval on most enterprise/technical corpora, because vector embeddings underweight exact term matches that carry high signal.

**Do this:** Default to hybrid retrieval unless you've measured that pure-vector wins on your specific corpus.

Evidence, newest first:
- supports: [From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents](https://arxiv.org/abs/2604.01733) (2026-04) Hybrid retrieval + reranking beat every single-stage method; BM25 alone beat state-of-the-art dense retrieval on financial documents.
- supports: [Hybrid Search Explained](https://weaviate.io/blog/hybrid-search-explained) (2025-01-27)

### Few-shot prompting is brittle to formatting choices

`few-shot-prompting-brittle-on-format-changes` · current · confidence 0.70 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=few-shot-prompting-brittle-on-format-changes#claims)

Few-shot prompting accuracy is highly sensitive to example ordering, whitespace, and demarcation choices, in ways that look like model regressions if not controlled for.

**Do this:** Freeze prompt formatting when evaluating model changes.

Evidence, newest first:
- supports: [Calibrate Before Use](https://arxiv.org/abs/2102.09690) (2021-02)

**Worth a look** (1)

- **[OpenAI launches the Agents API in public beta, a hosted Codex harness](https://openai.com/index/introducing-the-agents-api)** · 2026-09-10 · OpenAI Blog
  A managed harness removes orchestration work but shifts trust to the vendor's harness and to whichever sandbox and tools you attach.
  Try: Decide sandbox placement and tool trust before adopting a hosted agent harness. When evaluating a hosted agent API, list which sandbox option (vendor-managed, your virtual private cloud (VPC) or a partner) holds your files and secrets, which MCP servers and custom functions the agent can call, and how compaction summaries are logged. Pilot on a low-risk task during the public beta.


<a id="tools-interfaces"></a>

## Tools and interfaces

_How the harness exposes actions - tool design and descriptions, schemas and structured output, skills, MCP servers built for agents, sandboxes as tools._

### TOON beats JSON on input-side token cost

`toon-cuts-input-tokens-vs-json` · contested · confidence 0.55 · updated 2026-10-21 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=toon-cuts-input-tokens-vs-json#claims)

For large uniform arrays, TOON serializes to 30-60% fewer input tokens than JSON at comparable retrieval accuracy.

**Do this:** Use TOON for the big uniform/tabular payloads you feed INTO the model (tool results, row sets, retrieved records). Keep JSON where data is deeply nested or irregular.

**Conditions:** Input side only, and only for uniform arrays. Nested or irregular objects show much smaller or negative gains, and on short payloads the 'prompt tax' of explaining the format to the model can erase the saving entirely. Says nothing about generation — see constrained-decoding-for-structured-output.

Evidence, newest first:
- contests: [Notation Matters: A Benchmark Study of Token-Optimized Formats in Agentic AI Systems](https://arxiv.org/abs/2605.29676) (2026-05-28) Independent agentic-loop benchmark (BFCL, MCPToolBench++, MCP-Universe, StableToolBench; 5 open-weight models): TOON cut tokens by only up to 18% at a ~9pp accuracy cost, and cascaded on multi-turn parsing failures.
- contests: [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) (2026-02-08) Finds the advantage is often reduced by instructional overhead in shorter contexts.
- supports: [New Token-Oriented Object Notation (TOON) Hopes to Cut LLM Costs by Reducing Token Consumption](https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/) (2025-11)
- supports: [toon-format/toon — reference implementation, spec and benchmarks](https://github.com/toon-format/toon)

### Model upgrades can regress on non-native tool schemas

`match-tool-schemas-to-the-target-model` · current · confidence 0.60 · updated 2026-07-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=match-tool-schemas-to-the-target-model#claims)

A newer SOTA model can be WORSE at your harness's custom tool schema than its older siblings — Opus 4.8 and Sonnet 5 invented fields in a third-party edit tool that older models got right — plausibly because RL training tuned them to their own harness's tools.

**Do this:** Match your harness's tool schemas to what the target model was trained on — Claude on str-replace-style edits, OpenAI on apply\_patch — and offer a model-matched edit tool in multi-model harnesses. Re-run tool-calling evals on every model upgrade.

**Conditions:** One practitioner report on one third-party harness's edit tool; the RL-training explanation is the reporter's theory, not a measured cause.

Evidence, newest first:
- supports: [Better Models, Worse Tools: SOTA models regress on non-native tool schemas](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/) (2026-07-04)

### Constrained decoding wins for structured output, not TOON

`constrained-decoding-for-structured-output` · current · confidence 0.60 · updated 2026-07-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=constrained-decoding-for-structured-output#claims)

For structured model OUTPUT, constrained decoding gives the lowest token usage and plain JSON generation the best accuracy — token-optimized notations do not win here.

**Do this:** Split the decision by direction. Use a token-optimized notation for what you feed in; use constrained decoding (or plain JSON) for what you ask the model to emit.

**Conditions:** Benchmarked on one-shot in-context generation. Constrained decoding requires a serving stack that supports it — without one, plain JSON generation is the accuracy-preserving fallback.

Evidence, newest first:
- supports: [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and Constrained Decoding Generation](https://arxiv.org/abs/2603.03306) (2026-02-08)

**New research** (2)

- **[GRSE credits multi-agent skills by contrasting repeated runs, not presence](https://arxiv.org/abs/2610.27227)** · 2026-10-19 · Hugging Face Daily Papers
  If your harness edits skills automatically, assign credit by comparing repeated runs (group-relative), not by co-occurrence with success, or harmful skills will survive.
  Try: Group-relative credit check before promoting or retiring a skill. For each candidate skill edit, run the same task batch N times with and without the skill (same seeds and library otherwise). Use the outcome difference as the skill's credit, and require a consistent sign before committing. Include deliberately harmful skills as canaries to confirm the credit signal flags them.
- **[When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057)** · 2026-08-07
  History reliability is a distinct tool-use bottleneck: harnesses that just accumulate turns are silently letting old, wrong state overwrite the current task.
  Try: Add a stale-history eval slice to your agent harness. Fork or reimplement the paper's Original / Polluted / Oracle triad: for each production task, generate a corrupted-history variant that keeps the current request and system policy identical but swaps in stale entities and interface conventions, then track decision-flip rate as a first-class harness metric.

**Worth a look** (1)

- **[Kimi K2.6 on vLLM returned valid tool-calls 92% of the time](https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm)** · 2026-10-26 · @coffeemug via Hacker News
  Tool-call quality depends on how the model is served, not only on the model. Turn on constrained decoding per model, check it with a tool-call benchmark, and re-check after engine upgrades.
  Try: Enable and verify strict tool calling on self-hosted vLLM. For each open-weight model you serve with vLLM, enable tool-call strictness (--tool-strict-level) and run Moonshot's K2-Vendor-Verifier ToolCall benchmark, or a similar schema-accuracy test, before and after. If you use speculative decoding, test the two together. Add the benchmark to CI so a vLLM upgrade that changes defaults is caught.


<a id="orchestration"></a>

## Orchestration and multi-agent

_How work is split across agents and turns - subagents, planners, multi-agent coordination, long-running and background agents._

**Worth a look** (2)

- **[Claude Code's Ultracode subagents worked 12+ hours from a one-line prompt](https://simonwillison.net/2026/Oct/16/sqlite-sparql-rust/)** · 2026-10-16 · Simon Willison's Weblog
  Large subagent workflows can finish big, test-backed builds without supervision, so the bottleneck moves to human review; plan for verification artifacts such as conformance suites, differential fuzzing and documentation up front.
  Try: Define verification before launching a long subagent run. Before starting a multi-hour orchestrated run, name the oracle the output will be judged against, such as a standard conformance suite, differential fuzzing against a reference implementation, or a benchmark. Require per-component READMEs and a tutorial in the initial prompt, not as a follow-up, so the result can be evaluated without reading all the code.
- **[Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai)** · 2026-07-28
  Once agents are cheap, verification is the bottleneck: acceptance tests, parity references, and named maintainers are the new critical infrastructure — not more agent capability.
  Try: Verification-first harness pattern for agent-assisted engineering work. Codify the OpenAI field-report pattern for any team standing up an agent-assisted engineering loop: (1) before any agent runs, define an external reference — parity target, simulated dataset with known answers, or bounded statistical property — that will actually decide 'ship or not', (2) break the goal into small feedback-driven iterations with intermediate benchmarks so the agent's confident-but-wrong pattern gets caught early, (3) explicitly assign a human owner for last-mile edge cases (num…


<a id="harness-evals"></a>

## Evaluating harnesses

_Measuring a harness rather than a model - harness ablations, agent benchmarks, trajectory analysis, eval-to-production gaps._

### Auto-evolved harness gains are mostly overfitting

`harness-evolution-gains-need-held-out-attribution` · current · confidence 0.60 · updated 2026-10-27 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-evolution-gains-need-held-out-attribution#claims)

Gains from automatically evolving an agent harness (prompts, skills, tools, orchestration around a fixed model) are mostly search-set overfitting and extra inference compute: across 21 settings with significant gains, those two explained 54% and 14% of the gain on average, search-set gains often failed to transfer to held-out tasks, and a validation split did not prevent the overfitting.

**Do this:** Accept an auto-evolved harness change only on its delta over a held-out task set the optimizer never saw, measured at matched inference budget; don't trust search-set or validation-set improvement.

**Conditions:** Covers automated harness-evolution frameworks on math, coding, creativity and agentic benchmarks; the share varies widely by task, model and framework, and it says nothing about hand-engineered harness changes.

Evidence, newest first:
- supports: [Trustworthy Recursive Self-Improvement in the Era of Large Models: Foundation, Risks, Evaluation and Open Challenges](https://arxiv.org/abs/2610.35193) (2026-10-27) Survey warns that reported self-improvement gains may reflect flawed evaluations and that changing the improvement mechanism may invalidate earlier verification.
- supports: [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466) (2026-10-19)

### SWE-bench scores don't predict production task performance

`swe-bench-doesnt-generalize-to-production-tasks` · current · confidence 0.60 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=swe-bench-doesnt-generalize-to-production-tasks#claims)

SWE-bench scores do not linearly predict agent performance on production engineering tasks; the benchmark rewards a specific style of small-diff bug-fix.

**Do this:** Treat SWE-bench as one data point, not a complete picture. Build in-house evals on your task mix.

**Conditions:** Indirect evidence: SWE-bench's own scope (small issue-fix diffs in 12 Python repos) plus a randomized trial where AI tools slowed experienced developers on real tasks by 19%.

Evidence, newest first:
- supports: [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) Randomized trial: experienced developers using AI tools on real tasks in mature repos were 19% slower, despite believing AI made them faster - high benchmark-style capability does not predict production task performance.
- supports: [SWE-bench](https://arxiv.org/abs/2310.06770) (2023-10)

**New research** (3)

- **[OpenAI finds agents score worse on safety evals than in production](https://alignment.openai.com/eval-production-behavior-gap/)** · 2026-11-03 · OpenAI Alignment Blog
  Agent safety eval scores can swing on the model's guess about what is being tested, so builders should compare eval results against matched production traces and design evals whose objective is hard to infer.
  Try: Track the eval-to-production gap and objective guesses in agent safety evals. For each agent safety eval you run, classify the reasoning traces for (a) statements that this is a test and (b) guesses about what is being tested, using two separate rubrics. Report success separately for rollouts with correct and wrong objective guesses. Where you have production logs, pick matched production decisions based only on the context before the decision, grade them with the same rubric, and track the gap per model. Rewrite eval cases where the 'correct' behavior can be inferred fr…
- **[Harness-Delta Attribution: Dissecting Gains From Harness Evolution](https://arxiv.org/abs/2610.22466)** · 2026-10-19 · arXiv cs.AI (Artificial Intelligence)
  Before you adopt an auto-evolved harness, subtract overfitting and extra compute from its gain; the real improvement is usually under half of what was reported.
  Try: Attribution-aware acceptance test for harness changes. When a prompt or skill optimizer or a self-improving loop proposes a harness change, score it on a held-out task set the optimizer never saw. Compare at matched token and inference budgets so extra compute isn't counted as improvement. Accept the change only on the held-out delta, not the search-set or validation delta.
- **[RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](https://arxiv.org/abs/2608.27439)** · 2026-08-27 · arXiv cs.CR
  Effective automated red-teaming of agent harnesses should evolve reusable, attributable attack skills rather than replay fixed attacks or full trajectories.
  Try: Red-team the harness, not just the model. Adopt an evolving-skill red-team loop that profiles which jailbreak tools actually decide success (tool attribution), distills wins into concise reusable skills, and gates updates behind a validation ratchet; evaluate transfer across multiple target harnesses and attacker models to estimate real-world risk.

**Worth a look** (4)

- **[Hugging Face guide shows how to build and validate an agentic evaluation](https://huggingface.co/blog/agentic-evals)** · 2026-11-23 · Hugging Face Blog
  Before you trust an agent eval, run a do-nothing agent and a shortcut solution against the grader, and read the traces.
  Try: Test every grader with a null agent and a shortcut solution. Before running models, confirm the reference solution passes, a do-nothing agent fails, and a script that skips the required work fails; then report pass^k as well as pass@k.
- **[Eugene Yan finds graders failed valid work in eight of twelve evals](https://eugeneyan.com/writing/public-evals)** · 2026-11-19 · Eugene Yan
  Read a benchmark score as a model-plus-harness-plus-grader result, and audit the grader before trusting the ranking.
  Try: Audit your eval graders and report pass^k. Add a do-nothing agent and an adversarial agent as negative tests, review tasks that several strong models fail the same way, run each task k times and report pass^k next to average pass rate, and score models inside your own harness.
- **[UK AISI releases Transect to review long agent evaluation transcripts](https://www.aisi.gov.uk/blog/transect-making-large-scale-agentic-evaluations-easier-to-understand)** · 2026-11-17 · UK AI Security Institute Blog
  When you review agent eval runs, keep judge labels linked to transcript evidence and look at where judges disagree.
  Try: Try Transect on your long agent eval transcripts. Supply a transcript, the task context and your own activity categories (for example experiment design, coding, analysis). Use repeated or multiple judge models, check disagreements first, and export the tables for further analysis.
- **[Explicit Edit Benchmark offers 226 byte-exact file-editing tasks for comparing coding agents](https://github.com/alexshpunt/explicit-edit-benchmark)** · 2026-09-11 · alexshpunt/explicit-edit-benchmark
  If you build or tune an edit tool for a coding agent, test it on exact-match edit tasks, since this benchmark isolates that skill from reasoning.
  Try: Benchmark your agent's edit tool on explicit-edit-benchmark. Clone the repository, install the command-line interface (CLI) for your harness (adapters exist for Pi, Codex CLI, OpenCode, Oh My Pi, GitHub Copilot CLI and DeepSeek Harness), run the benchmark with --local and the --harness and --model flags, and compare your edit-tool variant against the baseline-agent (bash only) result on the public leaderboard.


<a id="harness-design"></a>

## Harness design

_Everything else about building the agent loop itself - architecture, prompts, control flow, autonomy and approval design._

### An agent's stated lean steers expert judgment calls

`agent-stated-lean-steers-expert-decisions` · current · confidence 0.60 · updated 2026-10-29 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=agent-stated-lean-steers-expert-decisions#claims)

When an agent states a preference on an open judgment call, experts mostly follow it: in Anthropic's randomized study analysts matched a coin-flip-assigned agent lean 86% of the time versus about 50% expected with no influence, often reusing the agent's arguments without crediting it.

**Do this:** At human decision points in a harness, have the agent present the strongest case for each option and capture the human's own preference before the agent states its lean; do not rely on the human's self-report to judge whether they were steered.

**Conditions:** Shown for open analytical choices with no clearly correct answer, in one study of expert analysts; not shown for decisions with a verifiable right answer or for permission prompts.

Evidence, newest first:
- supports: [Anthropic study finds analysts follow an agent's hidden lean on judgment calls](https://www.anthropic.com/research/agents-judgment-calls) (2026-10-27)

### Diff review catches more LLM-introduced defects than full-file review

`diff-review-catches-more-than-full-file-review` · contested · confidence 0.35 · updated 2026-10-21 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=diff-review-catches-more-than-full-file-review#claims)

Reviewing an LLM's proposed change as a diff catches more defects than reviewing the resulting full file.

**Do this:** Prefer tools that present LLM changes as diffs. Reviewer must sign off on the specific lines that changed.

**Conditions:** No controlled study compares diff review with full-file review for defect yield. The ledger's earlier citation for this claim was a mis-attributed paper and has been replaced.

Evidence, newest first:
- supports: [From Code Review to Code Critique (ARCTIC): ranking the diff regions that most need human scrutiny beat a baseline AI reviewer 2.4x](https://arxiv.org/abs/2607.29516) (2026-07-31) Indirect: supports focusing reviewer attention within the diff, but compares no full-file review.
- contests: [Diff-only review misses cross-file breakage that full-repository context catches (vendor analysis)](https://www.cubic.dev/blog/why-ai-code-assistants-break-your-build-the-full-repository-context-problem)

### Lean tool sets and reasoning-first prompts work best

`few-distinct-tools-beat-many` · current · confidence 0.70 · updated 2026-09-16 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=few-distinct-tools-beat-many#claims)

Coding-agent harnesses work better with few distinct tools and a lean system prompt of reasoning rather than rules.

**Do this:** Keep the tool count small and the tools clearly distinct; write the system prompt as reasoning rather than rule lists; grow your eval suite out of real incidents; gate dangerous actions with a context-aware permission classifier rather than a static allowlist.

**Conditions:** Described from first-party practice on one coding agent, not a controlled comparison — treat as a strong prior, not a measured result.

Evidence, newest first:
- supports: [HarnessTax: How Much Does the Harness Matter for Coding Agents?](https://harnesstax.github.io/) (2026-09-16) Cross-vendor comparison over 21 model-harness pairs: the four-tool Pi harness matched Claude Code and Codex CLI on success while harness choice changed cost up to 5x. Small sample (30 tasks, 3 repetitions).
- supports: [How the Claude Code team designs its harness](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) (2026-07-21)

### Too many tools degrade agent tool-selection accuracy

`tool-count-degrades-agent-performance` · current · confidence 0.70 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=tool-count-degrades-agent-performance#claims)

Showing an agent more candidate tools than the task needs degrades tool-selection accuracy: short, query-adapted tool lists select better than a fixed longer list (93.1% vs 87.1% on BFCL with Claude Sonnet 4.6).

**Do this:** Curate the tool set. Retire tools whose calls the eval suite shows agents get wrong more than they get right.

**Conditions:** No single universal threshold: the right list length depends on the registry and the query.

Evidence, newest first:
- supports: [How Many Tools Should an LLM Agent See? A Chance-Corrected Answer](https://arxiv.org/abs/2605.24660) (2026-06) Adaptive tool shortlists improved selection accuracy from 87.1% to 93.1% over always showing a fixed-size list, confirming tool-set size/composition materially affects selection accuracy.
- supports: [ToolLLM](https://arxiv.org/abs/2307.16789) (2023-07)

### Coding agents hallucinate plausible but nonexistent APIs

`coding-agents-produce-plausible-but-hallucinated-apis` · current · confidence 0.90 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=coding-agents-produce-plausible-but-hallucinated-apis#claims)

Coding assistants generate calls to functions and APIs that do not exist in the target library or version — plausible spelling, correct-looking signature, no runtime existence.

**Do this:** Any LLM-suggested import or API call must be validated against the actual library documentation for the pinned version.

Evidence, newest first:
- supports: [Library Hallucinations in LLM-Generated Code: A Risk Analysis Grounded in Developer Queries](https://arxiv.org/abs/2509.22202) (2025-09)
- supports: [On Mitigating Code LLM Hallucinations with API Documentation (CloudAPIBench)](https://arxiv.org/abs/2407.09726) (2024-07-13) GPT-4o made valid calls to low-frequency APIs only 38.58% of the time.

### Single-turn CoT gains don't transfer to multi-turn tasks

`chain-of-thought-does-not-transfer-to-multi-turn` · current · confidence 0.65 · updated 2026-08-06 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=chain-of-thought-does-not-transfer-to-multi-turn#claims)

Single-turn benchmark gains, including from chain-of-thought reasoning, do not reliably carry over to multi-turn agent tasks: top models lose about 39% from single- to multi-turn settings, and reasoning models degrade the same way.

**Do this:** Evaluate agents on the multi-turn task, not a single-turn proxy.

Evidence, newest first:
- supports: [When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories](https://arxiv.org/abs/2608.06057) (2026-08-06) Misleading multi-turn history flips 32.1% of otherwise-correct tool decisions.
- supports: [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) (2025-05-09) 15 LLMs drop 39% on average from single- to multi-turn; the reasoning models (o3, DeepSeek-R1) deteriorate the same way.

**New research** (3)

- **[When Context Gets Root: Instruction Privilege Escalation in LLM Harnesses](https://arxiv.org/abs/2608.27299)** · 2026-08-27 · arXiv cs.CR
  How a harness assembles context is a privilege boundary; if it can promote untrusted data, model-side instruction hierarchy provides little protection.
  Try: Preserve provenance labels through harness context assembly. Audit how your agent harness concatenates system prompts, tool outputs, files, memory, and scheduled tasks; ensure untrusted content keeps its low-privilege label end-to-end and cannot be relocated into higher-trust sections, and test with attacker-controlled tool/file content aiming for RCE and exfiltration objectives.
- **[The Frontier AI Vulnerability Burst: Industrializing Autonomous Zero-Day Discovery in Open-Source Software](https://unit42.paloaltonetworks.com/frontier-ai-vulnerability-burst/)** · 2026-08-04
  Autonomous AI vulnerability discovery moves the mix away from memory-corruption fuzzing (~8%) toward semantic/logic bugs (~92%), and complementarity between models is large enough that an ensemble is a defensive requirement, not an optimization.
  Try: Design point for autonomous vuln-discovery harnesses. Copy NOVA's shape: multi-model ensemble for the discovery phase, dedicated 'gatekeeper' agents for verification, clean-room PoC replay in gVisor-style sandbox, and explicit accounting of paths reviewed / paths ruled out / candidates pending proof. Do not rely on any single frontier model as the discovery engine — measure per-model unique-find share on your codebase before picking a champion.
- **[Claude Code and Opus 4.6 pipeline finds a real Linux sandbox-escape CVE](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/)** · 2026-07-30
  An agent-driven vuln-hunting pipeline can produce real, CVE-quality Linux sandbox-escape bugs — but the shipping discipline is 'AI found it, human reproduces it before you submit.'
  Try: Wrap agentic vuln-hunt pipelines with a 'human-reproduces-before-submit' gate. When running an agent loop against a target codebase, land findings into a queue that requires manual repro (including a negative-case check with the offending permission removed) before any external disclosure. This preserves the throughput advantage of agent scanning while blocking the well-known failure mode of confident-but-invalid AI reports flooding maintainers.

**Worth a look** (2)

- **[Anthropic study finds analysts follow an agent's hidden lean on judgment calls](https://www.anthropic.com/research/agents-judgment-calls)** · 2026-10-27 · Anthropic Research
  If your harness relies on a human to make or check judgment calls, the agent's framing will often make the call instead, so design for that.
  Try: Make the agent argue both options at human decision points. When an agent reaches a decision with more than one reasonable answer, have it state its own lean and also the strongest case for the alternative, ideally asking the human to commit to a choice before it voices its lean. Do not treat a human sign-off as independent review of agent-produced analysis, and do not rely on users' self-reported ownership or confidence as evidence they were not steered.
- **[HarnessTax finds harness choice barely moved success but changed cost](https://harnesstax.github.io/)** · 2026-09-16 · @matt\_d via Hacker News
  Compare cost and success of your model across more than one harness, because a default harness can carry a hidden cost premium for the same results.
  Try: Run a model-by-harness cost-success sweep before standardizing a coding agent. Pick 30 or so representative tasks, run each candidate harness 3 times with the same model and a fixed price list, and record mean cost, success rate and first-call input tokens. Try a minimal read/write/edit/bash harness as the baseline and adopt a richer harness only if it beats it on your tasks.
