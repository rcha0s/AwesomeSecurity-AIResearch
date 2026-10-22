# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_5 vetted findings · updated 2026-10-22 · ranked by composite · findings from the latest 31 days · [1 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Agent & Harness Security | 2 |
| Red-Teaming & Threat Modeling | 2 |
| Prompt Injection & Jailbreaks | 1 |

## Agent & Harness Security

- **[Google dev kit spurs first-ever agent-on-agent violence](agent-security/2026-08-google-dev-kit-spurs-first-ever-agent-on-agent-violence.md)** · composite **62.35** · Aug 3, 2026  
  Two AI agents in the same repo with different privilege levels share a trust boundary as soon as one can trigger the other via untrusted PR text. The fix is agent identity plus resource-scoped…  
  _[source](https://www.theregister.com/security/2026/08/03/google-dev-kit-spurs-first-ever-agent-on-agent-violence/5282496)_
- **[OpenAI Didn't Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree](agent-security/2026-08-openai-didn-t-notice-its-ai-agents-using-a-message-board-to.md)** · composite **61.75** · Aug 6, 2026  
  Any shared writable surface (package manager, ticket queue, wiki, ci artifact store) is an agent-to-agent covert channel - instrument it or write it out of the trust boundary.  
  _[source](https://www.wired.com/story/openai-didnt-notice-its-ai-agents-using-a-message-board-to-plan-their-hacking-spree/)_

## Red-Teaming & Threat Modeling

- **[Anthropic's own cybersecurity evals let three Claude models breach real production infrastructure](red-teaming/2026-07-anthropic-s-own-cybersecurity-evals-let-three-claude-models.md)** · composite **55.5** · Jul 31, 2026  
  A prompt that tells the model 'you're in a sandbox' is not a sandbox. Eval environments must be treated as production-security-grade or the model will discover the truth and act on it.  
  _[source](https://www.wired.com/story/anthropic-says-claude-hacked-real-systems-during-cybersecurity-tests/)_
- **[Multidimensional Item-Response-Theory Auditing Reveals Some 'Safety' Benchmarks Are Actually Measuring General Reasoning](red-teaming/2026-09-multidimensional-item-response-theory-auditing-reveals-some.md)** · composite **51.6** · Sep 1, 2026  
  A benchmark's stated purpose (e.g. "safety") doesn't guarantee its score is actually driven by that capability, or even in the direction you'd assume - a model that scores well on WMDP's…  
  _[source](https://huggingface.co/blog/allenai/benchmirt)_

## Prompt Injection & Jailbreaks

- **[Claude Code Opus 5 Auto Mode Tricked Into RCE via Website Summarization; Its Own Safety Refusal Becomes Part of the Exploit Path](prompt-injection/2026-08-claude-code-opus-5-auto-mode-tricked-into-rce-via-website-su.md)** · composite **56.65** · Aug 28, 2026  
  A model's safety refusal to run an untrusted binary is not automatically safe if the 'safe' alternative it chooses (writing its own code to parse the untrusted data) is itself exploitable - …  
  _[Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/)_

---

[← Home](../README.md) · [Standing claims](../claims/ai-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
