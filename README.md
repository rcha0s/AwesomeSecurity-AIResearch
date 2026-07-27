# Awesome Security & AI Research [![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

> An auto-updating, source-cited tracker of the most **teachable** security and AI research. It scans a ranked set of sources (X, GitHub, YouTube, blogs, newsletters, RSS), extracts the transferable lesson + a concrete action from each, curates hard, and files it into three rolling databases — **AI Security**, **Product Security**, and **AI Research** (practitioner).

![Updated](https://img.shields.io/badge/updated-2026--07--27-blue) ![Vetted findings](https://img.shields.io/badge/vetted-18-success) ![Window](https://img.shields.io/badge/window-last_31_days-orange) ![License](https://img.shields.io/badge/license-CC--BY--4.0-lightgrey)

## 📸 This week's snapshot

> The top curated findings published in the last 7 days. Every entry is a **TL;DR** — we track the gist (what's new + why it matters + what to do), and each links to its writeup here **and** the original source for the full detail. For the full digest see the [📰 newsletter](NEWSLETTER.md).

- **[How the Claude Code team designs its harness: tool minimalism, incident-driven evals, system-prompt compaction, and an auto-mode permission classifier](ai-research/coding-agent-harness-design-first-party-anthropic-practices/2026-07-how-the-claude-code-team-designs-its-harness-tool-minimalism.md)** · AI Research · Jul 21, 2026 · composite **62.25** · [source ↗](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)  
  Treat your coding agent like production infrastructure: few distinct tools, a lean prompt of reasoning-not-rules, evals grown from real incidents, and a context-aware classifier…
- **[Server-side encrypted compaction: porting Codex's Responses-API compaction protocol into other harnesses (Pi)](ai-research/harness-context-management/2026-07-server-side-encrypted-compaction-porting-codex-s-responses-a.md)** · AI Research · Jul 22, 2026 · composite **62.25** · [source ↗](https://github.com/algal/pi-openai-server-compaction)  
  If you run OpenAI models in your own harness, you can adopt Codex's server-side Responses compaction (compaction_trigger + previous_response_id) for better long-task continuity —…
- **[ShadowPickle: pickle-VM import tricks evade ten model scanners and four model hubs](ai-security/model-supply-chain/2026-07-shadowpickle-pickle-vm-import-tricks-evade-ten-model-scanner.md)** · AI Security · Jul 20, 2026 · composite **60.22** · [source ↗](https://arxiv.org/abs/2607.17503)  
  A clean model-scanner result is weak evidence - prefer non-executable formats and sandbox deserialization of any third-party model.
- **[Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd](product-security/developer-tooling-template-injection/2026-07-oh-my-posh-a-directory-name-runs-commands-because-the-prompt.md)** · Product Security · Jul 24, 2026 · composite **58.5** · [source ↗](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)  
  Anything that renders your prompt, status bar or editor title is executing attacker-controlled repository metadata - treat it as a parser, not decoration.
- **[SourTrade: browser reassembles a Bun-based executable from split parts, defeating hash-based detection with per-session builds](product-security/browser-delivered-malware-malvertising/2026-07-sourtrade-browser-reassembles-a-bun-based-executable-from-sp.md)** · Product Security · Jul 25, 2026 · composite **56.7** · [source ↗](https://thehackernews.com/2026/07/malvertising-sends-malware-in-pieces.html)  
  Client-side payload assembly (split parts + per-session hashing) breaks hash-based detection, so hunt the whole delivery chain and behavioral signals, not the final-file signature.

## 📚 The three databases

- 🤖🛡️ **[AI Security](ai-security/README.md)** — 5 vetted findings. Securing AI systems: harness & agent security, MCP, skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.
- 🛡️ **[Product Security](product-security/README.md)** — 8 vetted findings. Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).
- 🧠 **[AI Research](ai-research/README.md)** — 5 vetted findings. Practitioner AI: improving your harness, understanding, and architecture for using LLMs/agents on real tasks. Not model internals or ML-research.

Also generated every run: [📰 Newsletter](NEWSLETTER.md) (daily snapshot) · [📈 Trends](TRENDS.md) (emerging themes) · [🔍 Review queue](REVIEW.md) (not-yet-vetted) · [📓 Learnings](LEARNINGS.md) (takeaways + generated skills).

## How it works

```
X / GitHub / YouTube / LinkedIn / articles / RSS   (ranked source registry)
  └─ ingest + Jina Reader (clean text)      → data/candidates.json
     └─ analyze  (extract teachable lessons · score newness/novelty/relevance
                  · derive an actionable takeaway/skill/harness idea)
        └─ curate (vetted-only gate) → merge into the 3 topic pools → re-rank
           └─ render  README · topic pages · newsletter · trends · review · skills
```

- **Latest only.** Findings older than ~31 days age out to [`data/archive.json`](data/archive.json); the *snapshot* above is the last 7 days.
- **Vetted-only.** A finding is shown only if it isn't flagged for review and clears the composite floor; the rest wait in [REVIEW.md](REVIEW.md). Nothing is deleted.
- **Ranked sources.** Approved sources live in a registry and self-rank by how often they yield *curated* findings (tier + reach + hit-rate).
- **Emerging trends.** Tagged findings are clustered over time to surface waves early ([TRENDS.md](TRENDS.md)).

## How to use this repo

| I want to… | Do this |
| --- | --- |
| Read the latest, curated | Skim the snapshot above → open a topic database or [the newsletter](NEWSLETTER.md) |
| Track a new source | `python scripts/add_source.py <type> <handle> --topics …` (or the `/add-source` skill) — X user, blog, newsletter, GitHub user/query, YouTube |
| Capture one article now | `python scripts/add.py <url>` then the `/add-resource` skill — returns summary + takeaway + action and files it |
| Run a full scan | the `/research-scan` skill (self-pace with `/loop 12h /research-scan`) |
| Run it daily on autopilot | `powershell -File scripts/install_daily_scan.ps1` — a Scheduled Task ingests, runs Claude headless to analyze+verify, and opens a PR each day (never auto-merges). Remove with `-Uninstall`. |
| Regenerate the site | `rerank.py` → `generate_site.py` → `trends.py` → `generate_newsletter.py` → `generate_review.py` → `generate_skills.py` |

**Setup** (Agent Reach + burner X account in WSL2, one-time): see [PUBLISH.md](PUBLISH.md). **Contributing / how findings are structured:** [CONTRIBUTING.md](CONTRIBUTING.md). **Automation & dev workflow:** [AGENTS.md](AGENTS.md).

## Repo layout

```
data/{ai-security,product-security,ai-research}.json  the 3 rolling pools (source of truth)
data/archive.json · data/sources.json                 aged-out findings · ranked sources
scripts/                                               ingest · analyze-merge · rank · render
.claude/skills/                                        /research-scan /add-resource /add-source
ai-security/ product-security/ ai-research/            rendered per-topic pages (generated)
README.md NEWSLETTER.md TRENDS.md REVIEW.md LEARNINGS.md   generated — do not hand-edit
```

## License

Curated content under [CC BY 4.0](LICENSE); scripts under MIT. Linked research remains the property of its original authors — every finding cites its original source.

<sub>Generated by <code>scripts/generate_site.py</code> on 2026-07-27. Edit the pools in <code>data/</code> and regenerate — do not hand-edit rendered files.</sub>
