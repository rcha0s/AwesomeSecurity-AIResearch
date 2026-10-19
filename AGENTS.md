# AGENTS.md — operating manual for firstmate & coding agents

This repo is a **firstmate**-managed project. Ongoing development runs as `ship`
(→ PR) and `scout` (→ report) tasks in **direct-PR mode**: every change lands on a
branch and a PR you review/merge on GitHub. Nothing is merged unseen.

## What this project is

An auto-updating analyzer that scans RSS, research sitemaps, GitHub, GHSA, HN and
peer-reviewed venues (plus ad-hoc LinkedIn/X/article adds) for
**AI and security** material, extracts the most *teachable* lessons, scores them by
newness / novelty / relevance, derives an actionable leverage per finding, and grows
three source-cited public knowledge directories — **`ai-security/`**, **`product-security/`**,
**`ai-research/`** — plus a rolling **`NEWSLETTER.md`** and **`TRENDS.md`**.

## Repo layout

```
config.yaml               # scoring weights, decay half-life, thresholds, freshness window
data/ai-security.json     # AI Security pool (source of truth)
data/product-security.json# Product Security pool (source of truth)
data/ai-research.json     # AI Research (practitioner) pool (source of truth)
data/claims.json          # CLAIM LEDGER — durable standing answers + supersession edges
data/archive.json         # aged-out findings (preserved, not shown)
data/sources.json         # ranked source registry (add via add_source.py)
data/candidates.json      # transient ingest staging (gitignored)
data/_raw/                # transient fetched article text (gitignored)
scripts/common.py         # shared helpers, TOPICS, schema, scoring, Jina fetch
scripts/sources_registry.py # source registry + hybrid ranking
scripts/aggregate.py · ingest_github.py · ingest_youtube.py · add.py  # ingest → candidates
scripts/add_source.py     # register a source (x/blog/newsletter/github/youtube)
scripts/merge_analysis.py # validate + dedup + route by topic + ground excerpts + rerank
scripts/verify_citations.py # ground each lesson excerpt vs its source (hallucinated quote → review)
scripts/rerank.py         # decay + composite + sort + prune stale → archive
scripts/generate_site.py  # README.md + the 3 topic trees + per-entry pages
scripts/claims.py         # claim model: validation, supersession edges, ordering, lineage
scripts/add_claim.py      # the ONLY sanctioned writer for data/claims.json (CLI)
scripts/generate_claims.py# claims/ — standing answers on top, retired ones underneath
scripts/generate_html.py  # docs/index.html — THE SITE (filterable, self-contained, no Jekyll)
scripts/templates/site.html # the site template (__DATA__ placeholder; a code asset, not data)
scripts/trends.py         # data/trends.json + TRENDS.md (emerging themes)
scripts/generate_newsletter.py # NEWSLETTER.md (rolling, 3 topic sections)
scripts/generate_review.py# REVIEW.md (non-vetted queue: needs_review or below composite floor)
scripts/importance.py     # newsworthiness signal — ranks the REVIEW.md queue (editorial track)
scripts/promote_editorial.py # applies the editorial agent's promotions (integrity floor enforced)
.claude/skills/           # /research-scan /add-resource /add-source /editorial-review — the LLM stages
docs/                     # GENERATED site served by GitHub Pages (branch main, folder /docs)
README.md · NEWSLETTER.md · TRENDS.md · REVIEW.md · ai-security/ product-security/ ai-research/ claims/  # GENERATED
# Curated view = VETTED findings (novelty gate) PLUS a separate "Trending & In the News"
# section from the editorial track; everything else waits in REVIEW.md.
```

## What ages out

Findings age out after `max_age_days` into `data/archive.json`. Claims and
news never do: news stories (editorial promotions and news-gated items) stay in
their pools and in the "Trending & In the News" lane, newest first, and rerank
pulls any archived news back.

## Findings vs claims (two different questions)

The pools answer **"what was published lately"** — a rolling feed that ages out after
`max_age_days`. The **claim ledger** (`data/claims.json`) answers **"what should I do
right now, and what did that replace"**. It is durable: claims never age out.

- A claim has a `status`: `current` · `contested` · `superseded` · `refuted`.
- Supersession is an **edge written on both ends** — the retired claim gets
  `superseded_by` + `superseded_on` + `supersession_reason`; the winner gets `supersedes`.
  `scripts/add_claim.py supersede` writes both, so they can never drift apart.
- `claims.py` enforces the invariants: unique kebab ids, edges resolve, edges are
  reciprocal, the graph is acyclic, retired claims must name a successor AND a reason,
  live claims cannot already be superseded, every claim needs at least one evidence URL.
- **Never hand-edit `data/claims.json`** — use `scripts/add_claim.py` (it re-validates the
  whole ledger before saving). Never delete or rewrite a retired claim's history; the
  record of what we used to believe is the product, not clutter.
- Renderer contract: live claims on top ordered `current` → `contested` by confidence;
  retired ones pushed to the bottom, most recently retired first, each struck through
  with its reason and a link to the claim that replaced it.

## How to run

The pools are the source of truth; the LLM analysis lives in the two skills.

```bash
# Ingest
python scripts/aggregate.py
python scripts/add.py "<url>"          # ad-hoc; --text/--file fallback for LinkedIn

# Analysis is done by the /research-scan or /add-resource skill, which writes
# data/analysis_out.json, then:
python scripts/merge_analysis.py
python scripts/add_claim.py validate    # ledger integrity (edges resolve, no cycles)
python scripts/generate_site.py
python scripts/generate_claims.py
python scripts/generate_html.py

# Other ingestors (no cookies; `gh` must be authed for GitHub/GHSA):
python scripts/ingest_github.py --max 5
python scripts/ingest_ghsa.py --max 25    # reviewed supply-chain advisories (gh)
python scripts/ingest_hn.py --max 6       # Hacker News velocity signal
python scripts/ingest_conferences.py --max 20  # peer-reviewed venues via arXiv
```

### Conference ingestion

The approved venues (USENIX Security, NDSS, IEEE SaTML, ACM AISec, CCS, plus
security-gated NeurIPS/ICML/ISSTA) publish no usable feed, and some proceedings
are paywalled — which we never fetch. Authors record acceptance in the arXiv
`comments` field, so `ingest_conferences.py` searches that (`co:"<venue>"`) via
the free keyless arXiv API and always lands on a free full text. Two gates:

- **Acceptance, not submission** — `"Submitted to NeurIPS"` is an unreviewed
  preprint wearing a venue's name and is filtered out. This is the peer-review
  signal raw arXiv `cs.CR` cannot provide.
- **On-thesis only** — broad ML/SE venues (`broad_venues` in `sources.yaml`)
  must additionally match a `security_terms` keyword, so venue acceptance alone
  can't drag the whole ML firehose into scope.

Black Hat and DEF CON are **not** covered — they aren't on arXiv and still need
an archive scraper. `research_index` sources (Anthropic) are registered but
likewise unharvested.

## Daily automation (unattended scan -> PR)

One entrypoint, two runners. Both run the `/daily-scan` skill
(`.claude/skills/daily-scan/SKILL.md`), which wraps `scripts/run_scan.sh`:
`pre` (budget guard, then every ingestor) → LLM analysis → `post` (story cap,
render, spend record, PR on `claude/scan-<date>-<runner>`). A failed run opens or
comments on the `scan-failure` issue (`scripts/scan_alert.sh`).

- **Cloud (default):** a Claude Code routine with prompt `/daily-scan`, this repo
  attached, scheduled daily. Environment: Custom network access with the hosts from
  `python scripts/allowlist.py` plus the default package list; setup script
  `pip install -r requirements.txt`.
- **Mac fallback:** `scripts/install_launchd.sh [HOUR MINUTE]` installs a launchd job
  that runs `scripts/run_scan_local.sh` from its own clone in
  `~/.local/share/awesomesec-runner` (macOS won't let launchd jobs read
  `~/Desktop`), pulled to main before each run. The wrapper runs every guarding phase
  itself in its own worktree (`~/.local/share/awesomesec-worktree`, reset each run), and
  the model session only analyzes. It is idle on days a scan already finished;
  `--uninstall` removes it.
- **Spend guard:** `scripts/budget.py` keeps a ledger on the `budget-ledger` branch.
  Routines draw subscription usage first and can't read their balance, so `pre`
  checks the month's spend against `budget.monthly_cap_usd`, then **reserves** the
  run's ceiling (`max_stories_per_run` × measured per-story cost, or
  `uncalibrated_run_usd` for a first local run) before any LLM work, so a failed
  run is still charged. Local runs replace the reservation with the measured
  `total_cost_usd`; cloud runs are charged the ceiling. One finished scan per UTC
  day: a failed cloud run doesn't block the Mac fallback, but a runner never
  retries its own failed day unattended. The
  settings come from `origin/main`, and ledger rows are appended to a fresh copy of
  the remote branch, never read from the working tree the model shares. The cap
  is $100/month (`null` makes every run skip).
- **Spend visibility:** every ledger write also rewrites `SPEND.md` on the
  `budget-ledger` branch (month total vs cap, one row per run, measured or
  reserved). Each scan PR body carries the month's total, and
  `scripts/run_scan.sh status` prints the report locally.
- **Containment:** the local `claude -p` session reads only inside the repo,
  edits only `data/`, runs only the named scripts, and fetches only a staged
  candidate's own URL (`scripts/fetch_raw.py`). Alerts carry no log text, and the
  PR body passes `scripts/scrub.py` (secret patterns + secret env values).
  The cloud routine can't be scoped per tool: routines have no permission-mode
  picker and run shell commands without approval (routines.md). Its limits are
  the environment's: Custom network allowlist, no connectors, a GitHub proxy
  scoped to this repo, no readable secrets in the VM, and PRs that still need a
  human merge.
- **GitHub in cloud sessions:** `gh pr` / `gh issue` are GraphQL and get a 403 there;
  the scripts use `gh api` (REST) only.
- Requirement for every runner: headless Claude runs with
  `--permission-mode acceptEdits` + an explicit `--allowedTools` list, never
  `--dangerously-skip-permissions`. If a tool prompt stalls an unattended run,
  widen the allowlist rather than skipping permissions.
- The curation gate still holds weak/ungrounded findings in `REVIEW.md`; only
  genuinely novel, grounded, verified items land in the curated view.
- After the novelty gate, a **separate editorial pass** (the `editorial-review`
  skill + `promote_editorial.py`) reads the held `REVIEW.md` queue and promotes
  the trending/newsworthy/teachable ones into a "Trending & In the News" section.
  It never overrides the novelty reviewer and never surfaces an ungrounded or
  verifier-refuted item — `promote_editorial.py` re-checks eligibility. Its
  staging file `data/editorial_out.json` is gitignored like `analysis_out.json`.

## How to validate a change end-to-end

A change is only "done" when the pipeline runs clean on real data — not just units:

1. `python scripts/aggregate.py --dry-run` — feeds parse, candidates classify.
2. Round-trip a sample: stage a candidate (`add.py … --text "…"`), hand-write a
   one-entry `data/analysis_out.json`, run `merge_analysis.py` → confirm it lands in
   the correct pool, low-confidence flags `needs_review`, and re-adding is idempotent.
3. `python scripts/rerank.py && python scripts/generate_site.py && python scripts/generate_html.py`
   — confirm the 3 topic trees regenerate, per-entry pages + `TRENDS.md`/`NEWSLETTER.md` exist,
   and the pools ↔ rendered site stay in sync (a second run is a no-op diff).
4. `python scripts/add_claim.py validate && python scripts/generate_claims.py` — the ledger's
   edges resolve both ways and `claims/` regenerates. Then spot-check one retired claim on its
   topic page: it must be struck through, below the live ones, and carry both a reason and a
   working link to the claim that replaced it.

## Standard test suite (must be green before a PR)

```bash
ruff check scripts tests
black --check scripts tests
pytest --cov=scripts --cov-report=term-missing   # ≥80% on deterministic modules
```

## PR requirements

- Conventional commit messages (`feat:`, `fix:`, `chore:`, `docs:`).
- **No committed secrets** — cookies, `.env`, `data/candidates.json`, `data/_raw/`,
  `data/analysis_out.json` stay gitignored.
- Regenerate the site + skills from the pools and commit them in sync (CI enforces).
- Tests + lint green. Every published finding cites a real source URL.

## Escalation policy

Stop and ask the captain when: a source can't be verified, scoring weights/schema need to
change, or a change would delete/relicense existing curated findings.

## Conventions

- Data pools are the single source of truth; regenerate rendered files, never edit them.
- Keep functions <40 lines, named constants in `config.yaml`, PEP 8 + type hints.
- X/Twitter ingestion is out of scope for now (#57: future local-only runner,
  never CI or cloud).
