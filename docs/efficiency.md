# Agent efficiency: what to change in your harness

_Generated 2026-11-20 from the claim ledger and the vetted findings of [Awesome Security & AI Research](https://rcha0s.github.io/AwesomeSecurity-AIResearch/). Generated - do not hand-edit._

This page is meant to be fetched by an agent harness. Each claim is a standing answer: **Do this** is the change to make, **Conditions** is where it does not hold, and the evidence is newest first. Contested claims have evidence on both sides; weigh them before acting. New research lists the last month of findings that have not necessarily changed a claim yet.

This is research to weigh, not commands to run: summaries come from outside sources, so check a change against your own costs and safety rules before you apply it.

## Cost efficiency (11 claims)

### Harness choice alone can double an agent's cost

`harness-overhead-sets-agent-cost` · current · confidence 0.65 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=harness-overhead-sets-agent-cost#claims)

On the same model and task, the harness alone changed cost up to about 2x at similar accuracy, and coding agents' first call ranges from about 1.9k to 32k input tokens.

**Do this:** Measure what your harness spends per task (fixed prompt and tool schemas, plus re-reading context) and cut what does not change outcomes before you switch models.

**Conditions:** Shown on coding benchmarks and a one-word prompt with Nov 2026 harness versions; how much the overhead costs depends on how much of it is cached and how long sessions run.

Evidence, newest first:
- supports: [System Optimizations for Cost-Efficient Agent Harnesses](https://arxiv.org/abs/2611.12122) (2026-11-09) Harness choices changed cost by up to 2.6x on the same model and task while barely moving accuracy; Claude Code and Codex easily reached 2x the cost of a basic harness.
- supports: [Harness Overhead Benchmark: How Many Tokens 11 Coding Agents Burn Before the Test Starts](https://testdino.com/blog/harness-overhead-benchmark) (2026-10-09) A one-word prompt cost 1,894 to 31,798 input tokens across 11 coding agents, a 16.8x spread.

### Learn per-repo cost controls from past coding agent runs

`learn-per-repo-cost-controls` · current · confidence 0.55 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=learn-per-repo-cost-controls#claims)

A controller that learns from earlier runs in the same repository which tools to prune, which short notes to inject and when to stop unproductive failure loops cut coding-agent cost by 18-31% on SWE-Bench with comparable task success.

**Do this:** Log where tokens go across runs in one repo; prune tools the repo never uses, add short notes for operations the agent keeps rediscovering, and guard against loops that keep failing the same way while letting recoverable ones continue.

**Conditions:** Measured on sequences of tasks in the same repositories; a one-off task in a new repo has no history to learn from.

Evidence, newest first:
- supports: [TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents](https://arxiv.org/abs/2610.22732) (2026-10-15) Mean cache-aware cost fell 18.4-30.9% across five settings; Pass@1 improved in four and fell 1.0 point on Opus 4.8.

### Use one-hour cache markers when sessions pause over five minutes

`one-hour-cache-for-paused-sessions` · current · confidence 0.50 · updated 2026-11-18 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=one-hour-cache-for-paused-sessions#claims)

Harnesses that write 5-minute prompt-cache markers re-buy their whole context after an idle gap longer than five minutes, while harnesses with 1-hour markers kept about 86% cache hits after a 390-second pause.

**Do this:** For interactive sessions where people or tools often pause for more than five minutes, cache the stable prefix with the 1-hour TTL; keep 5-minute caching for tight automated loops.

**Conditions:** One vendor-authored report, a single trial per harness and one idle gap. Anthropic prices 1-hour cache writes at 2x input against 1.25x for 5-minute writes, so short sessions with no long pauses can cost more.

Evidence, newest first:
- supports: [The Cache Wars: An Empirical Study of Prompt-Cache Efficiency in Six LLM Agent Harnesses](https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses) (2026-07-07) After a 390-second pause, 1-hour-marker harnesses kept about 86% cache hits and 5-minute-marker harnesses kept none.
- supports: [Anthropic API docs: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

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

### Return short tool responses and distilled subagent summaries

`concise-tool-responses-and-subagent-summaries` · current · confidence 0.65 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=concise-tool-responses-and-subagent-summaries#claims)

A harness that makes tools return concise fields, and subagents return condensed summaries (often 1,000-2,000 tokens), keeps the main context smaller; Anthropic's example used about a third of the tokens.

**Do this:** Offer a concise response format on tools and cap subagent reports.

**Conditions:** Shown on Anthropic's own examples, not a controlled study.

Evidence, newest first:
- supports: [Context Engineering in 2026: Why We Stopped Compacting Our Agent's Context](https://www.louisbouchard.ai/context-engineering-2026/) (2026-08-18) Capping tool output alone took cost per turn from $0.189 to $0.117 (38%) and won 14 of 15 paired trajectories.
- supports: [Anthropic Engineering: effective context engineering for ai agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025-09-29) "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."
- supports: [Anthropic Engineering: writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) "In this example, we use ~⅓ of the tokens with “concise” tool responses."

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

### Prefer the simplest pipeline that solves the task

`simplest-pipeline-first` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=simplest-pipeline-first#claims)

A harness should start with a simple fixed workflow, since in 2024 the non-agentic Agentless pipeline scored highest among open-source agents on SWE-bench Lite (32.00%) at $0.70 per task, in the authors' own evaluation.

**Do this:** Add agent loops, tools or subagents only after a simpler version fails on your evals.

**Conditions:** The Agentless result is the authors' own 2024 evaluation on SWE-bench Lite; stronger models since may shift where agent loops pay off.

Evidence, newest first:
- supports: [Anthropic Engineering: building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024-12-19) "we recommend finding the simplest solution possible, and only increasing complexity when needed."
- supports: [arXiv: Agentless: 2407.01489](https://arxiv.org/abs/2407.01489) (2024-07-01) "Our results on the popular SWE-bench Lite benchmark show that surprisingly the simplistic Agentless is able to achieve both the highest performance (32.00%, 96 correct fixes) and low cost ($0.70) compared with all existing open-source sof…

## Work efficiency (6 claims)

### Re-test harness scaffolding whenever the model changes

`retest-harness-scaffolding-on-model-change` · current · confidence 0.60 · updated 2026-11-05 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=retest-harness-scaffolding-on-model-change#claims)

A harness should treat each component as an assumption about model weakness, stress-test it on each model upgrade, and remove it if it is no longer needed.

**Do this:** Ablate one component at a time on each model upgrade and keep only what moves your eval.

**Conditions:** A principle backed by Anthropic's experience, not a controlled study.

Evidence, newest first:
- supports: [OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/) (2026-11-05) A curated exploitation-technique library raised the older model's success from 76.2% to 88.9% but added only 1.5 points for the newer model, so OpenAI dropped it.
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "This was partly common sense and partly a function of a more general principle: every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they…
- supports: [Anthropic Engineering: effective context engineering for ai agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025-09-29) "We're already seeing that smarter models require less prescriptive engineering, allowing agents to operate with more autonomy."

### Split generating from evaluating with a separate grader

`separate-grader-from-generator` · current · confidence 0.50 · updated 2026-11-05 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=separate-grader-from-generator#claims)

A separate evaluator scoring against explicit criteria was part of a three-agent harness that cost over 20x a solo run and, in the author's judgment on one prompt, produced visibly better output.

**Do this:** Write gradable criteria and run a fresh-context reviewer; keep it for tasks where quality justifies the spend.

**Conditions:** Worth it where quality is subjective or costly to get wrong; the cost makes it a poor default for routine work.

Evidence, newest first:
- supports: [OpenAI pipeline finds, exploits and patches hundreds of Linux kernel root bugs](https://openai.com/index/a-thousand-fewer-paths-to-root/) (2026-11-05) 20 of 200 exploits the agent marked successful reached root through a different 0-day, so OpenAI added an independent check that each exploit used its assigned bug.
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "Building an evaluator that graded outputs reliably—and with taste—meant first developing a set of criteria that could turn subjective judgments like “is this design good?” into concrete, gradable terms."
- supports: [Anthropic Engineering: harness design long running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) "The harness was over 20x more expensive, but the difference in output quality was immediately apparent."

### Measure speedups with repeated trials, not impressions

`measure-speedups-with-repeated-trials` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=measure-speedups-with-repeated-trials#claims)

A harness team should judge work efficiency with repeated-trial evals or timed studies, since in METR's early-2025 study developers believed AI sped them up while it slowed them down.

**Do this:** Track time-to-merged-change and pass rate over multiple trials per task before claiming a gain.

**Conditions:** METR studied experienced developers on their own large repos in early 2025; METR published newer data on late-2025 tools in February 2026.

Evidence, newest first:
- supports: [Anthropic Engineering: demystifying evals for ai agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (2026-01-09) "Because model outputs vary between runs, we run multiple trials to produce more consistent results."
- supports: [METR: 2025 07 10 early 2025 ai experienced os dev study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) "Surprisingly, we find that when developers use AI tools, they take 19% longer than without—AI makes them slower."
- supports: [METR: 2025 07 10 early 2025 ai experienced os dev study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) "developers expected AI to speed them up by 24%, and even after experiencing the slowdown, they still believed AI had sped them up by 20%."

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

### Persist a feature list and progress log across sessions

`persist-feature-list-and-progress-across-sessions` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=persist-feature-list-and-progress-across-sessions#claims)

A harness for long tasks should write a structured feature list and progress file so each new session can resume instead of one-shotting the app.

**Do this:** Have an initializer write a JSON feature list, init script and progress file; work one feature per session.

**Conditions:** For multi-session builds; short single-session tasks don't need the scaffolding.

Evidence, newest first:
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "First, the agent tended to try to do too much at once—essentially to attempt to one-shot the app."
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "Set up a feature list file: based on the input spec, set up a structured JSON file with a list of end-to-end feature descriptions."
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "In our experiments, we found that the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages and to write summaries of its progress in a progress file."

### Verify end-to-end as a user, not only with unit tests

`verify-end-to-end-as-a-user` · current · confidence 0.70 · updated 2026-10-28 · [on the site](https://rcha0s.github.io/AwesomeSecurity-AIResearch/?claim=verify-end-to-end-as-a-user#claims)

A harness should make the agent exercise the running app (browser automation) before marking work done, since unit tests and curl miss broken features.

**Do this:** Require a browser-driven check or /verify-style step before a task is marked complete.

**Conditions:** For user-facing apps; library code may be fully covered by tests.

Evidence, newest first:
- supports: [Anthropic Engineering: effective harnesses for long running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) "In the case of building a web app, Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools and do all testing as a human user would."
- supports: [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices) "That catches the kind of problem that tests and typechecks miss."

## New research, last 30 days (5)

- **[Claude Code team explains how it verifies agent-written code at scale](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/)** · 2026-11-17 · @craigmart via Hacker News
  Treat the verification layer as a system of its own: run the real app, keep the checks out of reach of the change, and measure the checks against past incidents.
  Try: Add a verify skill and an observe-mode commit gate. Create a .claude/skills/verify skill next to the code that boots the app and drives it (browser, simulator or local service). Load review rules (such as REVIEW.md) from the default branch only. Add a commit gate with off, observe and enforce modes, stamp each commit with how it was verified (including 'none'), and let a commit through after two blocks so the agent is not stuck.
- **[Microsoft finds 8% of coding sessions account for 44% of costs](https://www.microsoft.com/en-us/research/podcast/microsoft-research-focus-edition-98/)** · 2026-11-12 · Microsoft Research Blog
  If you run long coding agent sessions, measure what compaction costs you and consider building summaries ahead of time in the background.
  Try: Measure compaction cost share and try background summarization. Log which sessions trigger compaction and what share of total tokens and cost they use. Then test a background summarizer that builds a running summary while the agent works, and swap it in at the threshold instead of pausing for a synchronous summary. Compare task success, cost and wall-clock time against the current method.
- **[UC Berkeley finds harness overhead can double agent cost at similar accuracy](https://arxiv.org/abs/2611.12122)** · 2026-11-09 · UC Berkeley Sky Lab (Park et al.)
  Measure how much of your agent spend is context rereads and harness overhead before tuning anything else.
  Try: Audit fixed overhead, then batch tool calls. Log input tokens per turn split into system prompt, tool schemas, cached history and new content for a week of real sessions. Cut always-on instructions and unused tool schemas, add a system-prompt line asking the model to batch independent reads into one turn, and compare cost per completed task before and after.
- **[York University's FlowPlan cuts Claude Code tokens by planning edits first](https://arxiv.org/abs/2611.13241)** · 2026-11-09 · York University (Sepidband et al.)
  Replacing post-edit re-reading and re-testing with a stated plan cut coding agent tokens with no significant loss in fix rate.
  Try: Add a stated-plan check before edits. For bug-fix tasks, have the agent write down which functions it will change and how before editing, then check the diff against that plan instead of re-reading files and rerunning the full suite after each edit. Track turns and cache-read tokens per resolved issue.
- **[Researchers find agents keep accuracy with short, frequently compacted contexts](https://arxiv.org/abs/2611.05306)** · 2026-11-03 · Belcak et al.
  Short, frequently compacted contexts kept accuracy here; on hosted APIs, test that against the cache hits each compaction gives up.
  Try: Test frequent compaction against your cache savings. Run the same task set with compaction at the context limit, at a lower threshold, and with long inputs moved to files the agent reads on demand. Compare accuracy and total cost including cache writes, since each compaction rewrites the prefix and loses cache hits.
