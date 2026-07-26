# AI Security

> Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.

_5 vetted findings · updated 2026-07-26 · ranked by composite · latest 31 days only · [9 held for review](../REVIEW.md)._

| Domain | Findings |
| --- | --- |
| Model Supply Chain | 3 |
| MCP & Tools | 1 |
| Skill Supply Chain | 1 |

## Model Supply Chain

- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](model-supply-chain/2026-07-shadowpickle-pickle-vm-import-tricks-evade-ten-model-scanner.md)** · composite **60.47** · Jul 20, 2026  
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.  
  _[source](https://arxiv.org/abs/2607.17503)_
- **[A malicious federated-learning aggregator can backdoor a QA model without ever seeing client data](model-supply-chain/2026-06-a-malicious-federated-learning-aggregator-can-backdoor-a-qa.md)** · composite **54.05** · Jun 25, 2026  
  In federated training the aggregator is a trust boundary, not a neutral party - protect gradients and test the global model for triggers.  
  _[source](https://arxiv.org/abs/2606.27511)_
- **[QuantGuard: a pre-quantization defense against backdoors that only wake up after you quantize](model-supply-chain/2026-06-quantguard-a-pre-quantization-defense-against-backdoors-that.md)** · composite **53.45** · Jun 28, 2026  
  Audit models at deployment precision, not the precision you were handed - some backdoors only exist after you quantize.  
  _[source](https://arxiv.org/abs/2606.29239)_

## MCP & Tools

- **[ToolHive MCP SSRF: host-side discovery runs outside the sandbox it enforces](mcp-tools/2026-07-toolhive-mcp-ssrf-host-side-discovery-runs-outside-the-sandb.md)** · composite **65.65** · Jul 15, 2026  
  Put SSRF guards on every outbound client that touches untrusted input, re-validate redirect targets, and never suppress a taint warning on a 'trusted config' premise your threat model calls untrusted.  
  _[source](https://github.com/advisories/GHSA-pr64-jmmf-jp54)_

## Skill Supply Chain

- **[Agent skill security is a lifecycle problem, not just a runtime one (SkillSec-Eval)](skill-supply-chain/2026-07-agent-skill-security-is-a-lifecycle-problem-not-just-a-runti.md)** · composite **60.1** · Jul 16, 2026  
  When you scan or admit agent skills, cover the whole lifecycle (admission, retrieval, planner selection, evolution) — a runtime-only check misses where most of the risk actually lives.  
  _[source](https://arxiv.org/abs/2607.13987)_

---

[← Home](../README.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md) · [Learnings](../LEARNINGS.md)
