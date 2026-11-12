# Microsoft's Lazarus backdoors an agent's model by editing fewer than 10 dormant neurons

**Published:** Nov 10, 2026

> **Takeaway:** Treat model weights like code: check their provenance and diff them against the publisher's original weights, and limit what the agent can run, because the backdoored model passes standard evals while scanning or diffing weights can catch the edits.

## TL;DR

Microsoft researchers show that editing the weights of fewer than 10 rarely-firing neurons in an LLM takes no training, only inference-level compute. The edited neurons become trigger detectors that make an agent emit attacker commands, for example a download-and-run command once the date passes into 2027. The backdoored model passes standard evals and behaves normally until the trigger appears. Frontier agents can spot such weight edits, but reliable detection needs a diff against the original weights. The post argues weight integrity and provenance are the real controls.

## Lessons

- A training-free weight edit of a handful of neurons is enough to backdoor an agent built on the model. - _"weight-reprogramming fewer than 10 dormant neurons in an LLM, is enough to backdoor an agent built on it, and requires no training"_
- Triggers can be mundane environmental facts such as the date, so the backdoor can stay dormant through testing and fire later in production. - _"The trigger can be as mundane as a date change, e.g., once the clock passes midnight into 2027"_
- The attack only needs write access to a checkpoint, so internal models stored in a compromised account, pipeline or bucket are as exposed as downloaded open weights. - _"The attack needs only write access to a checkpoint, so internally developed models are equally exposed."_
- Agent-based weight scanning can find anomalous edits but cannot prove a model clean; treat audits as one layer alongside limiting and monitoring agent actions. - _"frontier agents can spot anomalous weight modifications if you ask them to look. But no scan can prove beyond any doubt that a model is safe."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker with write access to a model checkpoint (a compromised account, pipeline, or storage, or an insider at a trusted provider) plants a dormant trigger that makes an agent run attacker commands with whatever access it has.
- **Conditions:** The agent has tool or terminal access, and the deployer does not verify that the loaded weights match the publisher's original.
- **Mitigations:** Know where models come from and verify their provenance and weight integrity, compare weights against a declared base model, audit weights with frontier agents as evidence rather than a guarantee, limit agent permissions, monitor agent actions, and review consequential actions before execution.

---

**Topic:** AI Security  ·  **Domain:** Model Supply Chain & Theft  
**Source:** [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/)  ·  **Retrieved:** 2026-11-12  
**Scores:** Newness 52 · Novelty 65 · Relevance 82 · Credibility 76 · **Composite 68** _(each 0-100)_  
**Tags:** `backdoor`, `model-provenance`, `weight-integrity`, `agent-security`, `sleeper-agent`, `model-supply-chain`  
**Also reported by:** [The Hacker News](https://thehackernews.com/2026/11/microsoft-researchers-show-ai-agents.html) _(+1 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: ProjectDiscovery's LoRA-poisoned Qwen2.5 that made Codex CLI exfiltrate .env files (ai-security.json, 'A backdoored open model made Codex CLI exfiltrate .env files') showed trigger-based agent backdoors via fine-tuning; Anthropic's sleeper-agents line is cited in the post. Lazarus differs by needing no training at all, only a sparse edit of fewer than 10 dormant neurons at inference-level compute, and by framing weight diffing as the detection method. Weight-editing-by-LLM context: 'Sean Goedecke argues Astra's weight editing matches what a skilled researcher would do' (ai-research.json). Verifier's closest: ProjectDiscovery LoRA-backdoored model making Codex CLI exfiltrate .env; QuantGuard quantization-activated backdoors.

_Source: [https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/)_  ·  [← back to index](../README.md)
