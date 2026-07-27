# Contributing

Thanks for helping keep this pool credible, current, and teachable. The bar for
inclusion is deliberately high, and every finding must cite a real source.

## Two tracks

Findings live in one of three growing topic pools (the source of truth):

- **AI Security** (`data/ai-security.json`) — securing AI: harness/agent security, MCP,
  skill scanning, prompt injection, memory poisoning, model supply chain, LLM red-teaming.
- **Product Security** (`data/product-security.json`) — appsec, supply chain, cloud/infra,
  identity, mobile, plus red teaming and threat modeling (AI-assisted or not).
- **AI Research** (`data/ai-research.json`) — *practitioner* AI: improving your harness,
  understanding, or architecture for using LLMs/agents. Not model internals / ML-research.

`domain` within a topic is a free-text sub-grouping label. The rendered `README.md`,
`NEWSLETTER.md`, `TRENDS.md`, the three topic dirs, `skills/`, and `LEARNINGS.md` are
**generated** — never hand-edit them. Edit the pools and regenerate.

## What belongs here

1. **Credible, first-party source** — a recognized research team, vendor lab,
   standards body, CERT advisory, peer-reviewed/preprint venue, or a substantive
   practitioner post. No marketing or unattributed claims.
2. **New (hard rule)** — the source must have been published within the freshness window (`max_age_days` in `config.yaml`, ~1 month). We track only the latest research; older entries age out to `data/archive.json` automatically and are no longer shown.
3. **In scope** — one of the two tracks above.
4. **Teachable & actionable** — you can state the lessons and a concrete action.

## The easy way: let the skills do it

- One resource: `python scripts/add.py "<url>"` then run the **`/add-resource`** skill.
  (LinkedIn/auth-walled? paste it: `add.py "<url>" --text "<body>"`.)
- A batch from your X feed + RSS: run the **`/research-scan`** skill.

Both extract lessons, score novelty/relevance, derive an actionable leverage, merge
into the right pool, re-rank, and regenerate the site.

## The manual way: add an entry directly

Add an object to `entries` in the right pool file (schema v2). Key fields:

| Field | Notes |
| --- | --- |
| `track` | `security` \| `ai`. |
| `domain` / `subtype` | Valid domain for the track (see `scripts/common.py`). |
| `title` | Concise, specific. |
| `date` | `YYYY-MM` of disclosure. |
| `summary` | Teachable 2-3 sentences. |
| `lessons` | List of `{point, excerpt, confidence}` (excerpt anchors to the source). |
| `takeaway` | One-line "so what". |
| `actionable` | `{type, title, detail, skill_slug?}`, type ∈ takeaway/skill/harness/tool/other. |
| `tags` | Cross-cutting topics. |
| `scores` | `{novelty, relevance}` 0-100 (newness + composite are computed). |
| `source_name` / `source_type` / `source_url` | Attribution + link. |
| `needs_review` | `false` for verified entries. |

Security entries may also carry `threat` / `conditions` / `mitigations`. Then:

```bash
pip install -r requirements.txt
python scripts/rerank.py
python scripts/generate_site.py
python scripts/generate_claims.py
python scripts/generate_html.py
python scripts/generate_skills.py
```

Open a PR (direct-PR mode — see [AGENTS.md](AGENTS.md)). Keep lint + tests green.

## Updating the claim ledger

An **entry** is one article. A **claim** is the durable answer to a question — "which
serialization should agents use?", "is prompt injection a filtering problem?" — and it
never ages out. Claims live in [`data/claims.json`](data/claims.json) and render to
[`claims/`](claims/README.md).

**Never hand-edit the JSON.** Use the CLI; it re-validates the whole ledger before saving:

```bash
# a new standing answer (guidance = what to DO, scope = where it does NOT apply)
python scripts/add_claim.py new code-graph-beats-lexical-search \
  --topic ai-research --domain "Architecture & Optimization" \
  --statement "Graph-based code retrieval beats lexical search on multi-hop tasks." \
  --guidance "Build a call/import graph for repo-wide reasoning; keep grep for literals." \
  --scope "Multi-hop navigation only; single-symbol lookup is still faster with grep." \
  --confidence 0.7 --evidence "supports|https://arxiv.org/abs/…|Paper title|2026-07-01"

# retire the answer it replaces — both ends of the edge are written for you
python scripts/add_claim.py supersede grep-is-enough code-graph-beats-lexical-search \
  --reason "Lexical search misses cross-file call relationships."

python scripts/add_claim.py supersede old new --reason "…" --refuted  # wrong, not just replaced
python scripts/add_claim.py evidence <id> --evidence "contests|<url>|<title>|<date>"
python scripts/add_claim.py status <id> --set contested   # credible evidence both ways
python scripts/add_claim.py validate
```

House rules:

- **The reason is the product.** "Graph retrieval beat lexical search on multi-hop recall"
  is a reason; "newer research" is not. Someone should be able to read only the retired
  claims and understand how the field moved.
- **Nothing is deleted.** A superseded claim keeps its statement, its evidence, and its
  history. Demote, never remove.
- **One claim per question.** If two claims say the same thing, supersede one into the other.
- **`contested` is a valid answer.** When credible evidence cuts both ways, say so rather
  than forcing a winner — and record the contesting source with a `contests`/`refutes` stance.
- **Be conservative.** A single blog post rarely overturns a standing claim. `confidence`
  should track the strength and independence of the evidence.

## Adding a source (X user, blog, newsletter, GitHub user/query, YouTube channel)

Sources live in the **ranked registry** [`data/sources.json`](data/sources.json), not in
`sources.yaml` anymore. Add one with `scripts/add_source.py` (or the `/add-source` skill):

```bash
python scripts/add_source.py x_account @simonw --topics ai-research --tier high
python scripts/add_source.py blog https://blog.trailofbits.com --topics product-security
python scripts/add_source.py github_user praetorian-inc --topics ai-security,product-security
python scripts/add_source.py youtube https://youtube.com/@LiveOverflow --topics product-security
python scripts/add_source.py newsletter https://tldrsec.com --topics product-security
```

Each source is **ranked** `rank = 0.5·tier + 0.25·reach-signal + 0.25·hit-rate`, and the
hit-rate rises as the source yields *curated* findings — so good sources climb over time. For
X accounts, also **follow them on the burner**. `sources.yaml` now holds only classification
rules + `home_feed`/`min_stars` knobs.
