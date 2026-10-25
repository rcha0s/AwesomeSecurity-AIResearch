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
data/news_stories.json    # STORY LEDGER — one row per story + every covering source; never pruned
data/taxonomy.yaml        # THE vocabulary: 3 topics x fixed domain IDs (ais.* ps.* air.*)
data/taxonomy_migration.json # one-time label -> ID table (every pre-migration label)
data/taxonomy_proposals.json # verified new-domain proposals (taxonomy_proposals.py)
data/archive.json         # aged-out findings (preserved, not shown)
data/sources.json         # ranked source registry (add via add_source.py; reviewed PRs only)
data/source_stats.json    # per-source hit-rate counts written by scans (overlaid on the registry)
data/candidates.json      # transient ingest staging (gitignored)
data/_raw/                # transient fetched article text (gitignored)
scripts/common.py         # shared helpers, TOPICS, schema, scoring, Jina fetch
scripts/sources_registry.py # source registry + hybrid ranking
scripts/aggregate.py · ingest_github.py · ingest_youtube.py · add.py  # ingest → candidates
scripts/ingest_json_feeds.py # CISA KEV (exploited in the wild) + HF Daily Papers (keyless JSON, no RSS)
scripts/ingest_curator_links.py # stories tl;dr sec's recent issues link to (article = citation)
scripts/paper_gate.py     # paper admission gate: venue acceptance | HF Daily Papers | trusted-curator link
scripts/add_source.py     # register a source (x/blog/newsletter/github/youtube); `deactivate <id> --reason`
scripts/select_batch.py   # scan pre: cut staged candidates to this run's batch (rest -> data/_scan_backlog.json)
scripts/backfill.sh       # backfill a past window in chunks via a one-shot launchd job (issue #52)
scripts/merge_analysis.py # validate + domain-ID gate + dedup + route + ground + rerank
scripts/taxonomy.py       # the only taxonomy loader (`taxonomy.py list` = analyzer's domain list)
scripts/migrate_taxonomy.py # free-text domain -> ID (idempotent; rerank runs it too)
scripts/taxonomy_proposals.py # record verified proposals; recurring -> `taxonomy` issue
scripts/verify_citations.py # ground each lesson excerpt vs its source (hallucinated quote → review)
scripts/readability.py    # deterministic readability check of each brief (title..action; never excerpts)
scripts/rewrite_guard.py  # restores any rewritten brief field whose facts changed (vs data/_analysis_draft.json)
scripts/rerank.py         # decay + composite + sort + prune stale → archive
scripts/generate_site.py  # README.md + the 3 topic trees + per-entry pages
scripts/story_ledger.py   # story ledger: shortlist, judge verdicts (same/update/new), ledgering
scripts/replay_stories.py # replay a window of pool history through the story matcher (ISC-21)
scripts/claims.py         # claim model: validation, supersession edges, ordering, lineage
scripts/add_claim.py      # the ONLY sanctioned writer for data/claims.json (CLI)
scripts/generate_claims.py# claims/ — standing answers on top, retired ones underneath
scripts/generate_html.py  # docs/index.html — THE SITE (filterable, self-contained, no Jekyll)
scripts/templates/site.html # the site template (__DATA__ placeholder; a code asset, not data)
scripts/trends.py         # data/trends.json + TRENDS.md (emerging themes)
scripts/generate_newsletter.py # NEWSLETTER.md (rolling, 3 topic sections)
scripts/generate_review.py# REVIEW.md (non-vetted queue: needs_review or below composite floor)
scripts/eval_integrity.py · eval_recall.py · eval_golden.py · eval_history.py · eval_readability.py  # Phase 3 evals (see Evals)
scripts/run_golden_local.sh # weekly golden-set analyzer run; scan_containment.sh = the shared session lockdown
data/evals/               # golden.json (answer key), recall-<week>.json, golden-<date>.json, history.json
scripts/importance.py     # newsworthiness signal — ranks the REVIEW.md queue (editorial track)
scripts/newsworthy.py     # pre-analysis big-story signal for batch selection: markers + same-story corroboration
scripts/promote_editorial.py # applies the editorial agent's promotions (integrity floor enforced)
scripts/merge_guard.py    # auto-merge security boundary: is this PR content-only? (pure)
scripts/automerge.py      # drives .github/workflows/automerge.yml (REST gh api only)
scripts/merge_gate.py     # checks a scan PR must pass to auto-merge; the Phase 3 eval hook
scripts/content_checks.py # http(s)-only URLs, render equality, claim history (used by the gate)
.claude/skills/           # /research-scan /add-resource /add-source /editorial-review — the LLM stages
docs/                     # GENERATED site served by GitHub Pages (branch main, folder /docs)
README.md · NEWSLETTER.md · TRENDS.md · REVIEW.md · ai-security/ product-security/ ai-research/ claims/  # GENERATED
# Curated view = VETTED findings (novelty gate) PLUS a separate "Trending & In the News"
# section from the editorial track; everything else waits in REVIEW.md.
```

## Domains are IDs

Every entry's `domain` is an ID from `data/taxonomy.yaml` that belongs to its topic
(`ais.prompt-injection` on an `ai-security` entry). `merge_analysis.py` holds anything
else for review; rerank normalizes old free-text labels through the alias map. Claim
work follows the domain's `claim_eligible` flag (it replaced the 13 interests.yaml
clusters). Add or rename a domain only in the YAML, and never reuse or change an ID:
retire it into `aliases`. A recurring verified `proposed_domain` opens a `taxonomy` issue.
Ingestors emit `guess_domain` as an ID too: the `sources.yaml` keyword router still makes
every ingest decision and topic guess (its class is kept as `guess_label`); the ID is
picked from the taxonomy's keyword hints within that topic.

## How far back a scan looks

A daily scan ingests only the last `ingest_days` (7): older stories were
covered by earlier scans. Claim work follows the same week: each scan weighs
its findings against the whole ledger, so a new result that supports, contests
or refutes an old claim is still caught. A backfill uses its own window;
`add.py` keeps `max_age_days`. A feed or sitemap date can be a republish or a
site rebuild, so the page's own `Published Time` decides wherever the text is
fetched: `ingest_sitemap.py` drops a page it can't fetch (tried twice) instead
of dating it by `<lastmod>`, `fetch_raw.py` refuses a page older than the
window with `STALE` and writes no text, and `merge_analysis.py` refuses a new
entry whose saved page is older than `max_age_days`.

## What ages out

Findings age out after `max_age_days` into `data/archive.json`. Claims and
news never do: news stories (editorial promotions and news-gated items) stay in
their pools, and rerank pulls any archived news back. Keeping is not showing:
the front page's "Trending & In the News" lane shows only the last
`news_front_page_days` (7), newest first, at most `news_front_page_max` (30).
Every kept story is on the site's News tab, grouped by month. Retired claims
fold into a collapsed section under the live ones.

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
python scripts/ingest_json_feeds.py       # CISA KEV + Hugging Face Daily Papers
python scripts/ingest_curator_links.py    # tl;dr sec issue links (--dry-run [--misses R])
```

### Curator links (tl;dr sec)

tl;dr sec links the week's best security research, much of it on small blogs with
no feed of their own; those were most of the recall eval's misses. Its RSS feed is
gone (`tldrsec.com/feed` redirects to a 404; its registry row is deactivated with
`add_source.py deactivate`), so `ingest_curator_links.py` reads the public issue pages
listed in `tldrsec.com/sitemap.xml` (the recall eval's source too; the `/t/Newsletter`
archive page skipped an issue when probed). It takes the newest
`curator_links.max_issues` (2) issues **by issue number** and dates each by the page's
own publish date (its JSON-LD `datePublished`, else `article:published_time`), never by
sitemap lastmod: that is an edit date (#126, from 2022, carried 2026-05-28; most issues
share one 2025-04 bulk touch). Of those, issues published in the last
`curator_links.lookback_days` (14) go through `eval_recall`'s issue parser, which stages each lead story link that is on-thesis (taxonomy hints, excluded
terms, news deny-list), not on a paywalled host (`curator_links.paywall_hosts`: never
staged, so never fetched), not a sponsor placement, and not already in the pools, the
archive or the story ledger. The citation is the article, with tracking params
stripped; the candidate carries `source_id: curator:tldrsec`, `curated_by: tldrsec`
and `curator_issue`, which `merge_analysis.py` copies onto the pool entry. Follow-on
paragraphs (supporting links under a headline) are not staged. A staged link's
credibility is `curator_links.source_rank` (70): the linked blog is usually unknown to
the registry, so the curator's pick lifts it above the neutral 50 and the 45
`min_credibility` bar, but below tl;dr sec's own 80.

### Conference ingestion

The approved venues (USENIX Security, NDSS, IEEE S&P, IEEE SaTML, ACM AISec, ACM CCS, plus
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

### Paper admission gate

A paper (arXiv/OpenReview/IACR preprint) enters the queue only with a quality signal,
checked deterministically by `scripts/paper_gate.py`: accepted at a registered venue,
listed on Hugging Face Daily Papers, or linked by a trusted curator (tl;dr sec, Simon
Willison, Project Zero). tl;dr sec's links come from its issue pages:
`ingest_curator_links.py` runs first in `run_scan.sh` and records the arXiv ids they
link to in `data/_curator_arxiv.json` (gitignored), which `aggregate.py` adds to the
gate's curator signal. An id vouches only while its issue is inside the same
`curator_links.lookback_days` window (14 days). The raw arXiv cs.AI/cs.LG feeds were removed; cs.CR stays but
only yields papers that pass the gate. If a signal source is unreachable the gate fails
closed (papers dropped, never admitted).

Black Hat and DEF CON are **not** covered — they aren't on arXiv and still need
an archive scraper. `research_index` sources (Anthropic) are registered but
likewise unharvested.

## Daily automation (unattended scan -> PR)

One entrypoint, two runners. Both run the `/daily-scan` skill
(`.claude/skills/daily-scan/SKILL.md`), which wraps `scripts/run_scan.sh`:
`pre` (budget guard, then every ingestor, then the batch cut) → LLM analysis →
`post` (story cap, render, spend record, PR on `claude/scan-<date>-<runner>`). A
failed run opens or comments on the `scan-failure` issue (`scripts/scan_alert.sh`).

- **Batch:** the session's budget is sized for `limits.max_stories_per_run` stories,
  so `scripts/select_batch.py` leaves only `max_stories_per_run + batch_margin`
  candidates in `data/candidates.json`. Prefilter drops stay out; slots are dealt
  round-robin across ingestor classes (KEV, HN, GHSA, RSS, ...) by newness + source
  credibility, with a small `batch_routed_bonus` and at most `batch_per_source`
  slots per source (`batch_class_slots` lets plain RSS deal 2 a round). First,
  a big-story lane (`scripts/newsworthy.py`) of up to `batch_story_max` slots
  takes stories that 2+ independent publishers staged this run with a severity or
  AI-incident marker (rce, critical, exploited, compromise, agent hijack, ...).
  Publishers are registrable domains (all GitHub ingestors are one, HN another,
  neither counts as independent), and one copy must come from a source ranked
  `batch_story_min_rank` or more. A copy naming only other CVEs never joins a
  story. Each story gets one slot, tagged `batch_priority: story`; its other copies
  wait in the backlog (`batch_same_story_as`), and stories the ledger already
  holds never qualify. Markers and corroboration also add `batch_marker_bonus`
  and `batch_corroboration_bonus` to the deal's score. Then
  a must-not-miss lane of up to `batch_priority_max` slots takes new CISA KEV
  entries and critical GHSA advisories (plus high ones in AI tooling), tagged
  `batch_priority`; the session analyzes those first. Then a lab lane of up to
  `batch_lab_max` slots (at most `batch_lab_per_source` per feed) takes recent posts
  from the major AI labs (`batch_lab_hosts`: OpenAI, Anthropic, Google/DeepMind,
  Meta, Microsoft, ...) that name one of `batch_lab_terms` (security and safety
  words), tagged `batch_priority: lab`. Lab posts carry no severity marker, so they
  used to sink below the cut. A relevant lab post the prefilter dropped only as a
  catch-all without a marker is let back in; excluded-term and duplicate drops stand. Next, `batch_class_min`
  guarantees named classes a floor: `curator: 1` puts one tl;dr sec curator link
  in every batch (two at most, by the per-source cap). The rest go to
  `data/_scan_backlog.json` for diagnosis
  (Edit- and Read-denied to the Mac session; a convention only in the cloud);
  tomorrow's ingest re-stages any that are still fresh.
- **News tier:** the batch above is the DEEP tier (full analysis, at most
  `max_stories_per_run`). Every leftover candidate that is relevant news (the head
  of a big-story group the lane had no slot for, a KEV / critical GHSA the
  must-not-miss lane had no slot for, or a severity / AI-incident marker from a
  non-GitHub/HN source ranked `batch_story_min_rank`+, or a lab-lane post the lane
  had no slot for, published in the last
  `batch_story_days`, not deny-listed, not a story the ledger holds) joins
  `data/candidates.json` tagged `batch_tier: "news"`, at most `max_news_per_run`
  and `batch_news_per_source` per source. Each gets a short news brief
  (research-scan step 3c: title, one-sentence takeaway, 1-2 sentence summary,
  domain, primary URL, ONE verbatim excerpt). `select_batch.py` records the tiers
  in the code-owned `data/_scan_tiers.json`; `merge_analysis.py` accepts a brief
  only for a news-tier candidate named there, stamps `news_brief`, attaches the
  story group's other copies as covering sources, and grounds the excerpt: a brief
  publishes (news lane only, never as a vetted finding) only when its quote is
  confirmed against the fetched text; unverifiable or ungrounded briefs wait in
  REVIEW.md. `post` caps briefs at `max_news_per_run` apart from the story cap.
  A brief's citation and source text come from the tier record and the run's own
  fetch (a brief whose `source_url` isn't its candidate's is rejected). Retention:
  a held or ungrounded brief ages out at `max_age_days` like a finding; a grounded
  one is kept like news for `brief_news_days` (60), then moves to the archive (still
  on the Archive tab). The Mac session's cap prices briefs at the pessimistic
  `budget.session_news_ratio`, and a session stopped by `--max-budget-usd` or
  `--max-turns` still gets `post` on what it merged (ledger outcome `session-capped`).
- **No analysis = failed run:** `post` refuses a run where `merge_analysis.py`
  merged nothing (its code-owned `data/_merge_outcomes.json`) and applied no
  `same`/`update` verdict (`data/_story_outcomes.md`), raises `analysis-empty`,
  and opens no PR. The story count excludes entries rerank restored from main's
  archive. The Mac wrapper logs the session's final message, scrubbed, to
  `data/_scan.log` (grep `session result`), and retries once the same day when the
  failure was analysis-empty and cost under `budget.retry_max_usd`.

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
  run's ceiling (story units, `max_stories_per_run` + `news_cost_ratio` ×
  `max_news_per_run`, × the worst per-unit cost of the last
  `calibration_runs` measured runs × `ceiling_headroom`, or
  `uncalibrated_run_usd` for a first local run) before any LLM work, so a failed
  run is still charged. Local runs replace the reservation with the measured
  `total_cost_usd`, recorded by the wrapper before `post` so the PR body and the
  history row show it; cloud runs are charged the ceiling. One finished scan per UTC
  day: a failed cloud run doesn't block the Mac fallback, but a runner never
  retries its own failed day unattended, except the Mac's one retry after a cheap
  analysis-empty failure (the retry's own reservation blocks any further one). The
  settings come from `origin/main`, and ledger rows are appended to a fresh copy of
  the remote branch, never read from the working tree the model shares. The cap
  is $400/month since 2026-10-23 (`null` makes every run skip).
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
  human merge (in auto-merge's `merge` mode, content-only PRs excepted; see below).
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
  **Promotions are sticky:** a run only adds them. One leaves only by an explicit
  demotion with a reason (`{"id", "demote": true, "reason"}`) or when its
  integrity fails (refuted or ungrounded). Every promotion and removal goes into
  the code-owned `data/_editorial_outcomes.md`, which `post` puts in the PR body.

### Backfill (issue #52): a past window, same pipeline

A backfill chunk is a local scan with `SCAN_BACKFILL_FROM`/`SCAN_BACKFILL_TO` set:
same lockdown, skill, story ledger, evals and PR gate; only ingest changes. Each
ingestor pulls items published inside the window where its source can say so
(`common.ingest_window`): KEV by `dateAdded`, GHSA by the REST `published` filter (the
newest `per_run` of each day plus the window's critical ones), arXiv venues by
`submittedDate`, HN by `created_at_i` on both sides, HF Daily Papers for each window
day, tl;dr sec issues whose own publish date is in the window, RSS items the feed
still carries, sitemap pages whose own date is in the window, GitHub repos *created*
in it. Staging and batch newness judge freshness at the window's end
(`common.freshness_now`), so nothing is stale on arrival. Rerank keeps scoring on the
wall clock (the live ranking is untouched) and, in a backfill, does not prune the
entries this run merged (`rerank.kept_for`: not on origin/main). The next normal
rerank archives backfilled findings past `max_age_days`, still vetted, and keeps
news, as for any old story.

- **Guard:** `budget.py check_backfill` replaces the day rules. A chunk must sit
  inside the campaign `config.yaml backfill:` approves on main, span at most
  `max_chunk_days`, not overlap a finished chunk, and fit `max_runs` (every started
  run counts) and `max_usd` (charged so far plus this run's ceiling), then the month's
  cap. Local runner only, no same-day retry. Its ledger rows carry `backfill:
  "FROM..TO"`, so they never finish or try the day: the daily cloud/Mac run is
  unaffected. The PR goes on `claude/scan-<date>-backfill-<FROM>-<TO>`.
- **Run it:** `scripts/backfill.sh start 2026-09-09 2026-10-18 8` (after
  `install_launchd.sh` made the runner clone). It pulls the clone to main, prints the
  chunks and the guard's verdict for the first, and boots a one-shot launchd job
  (`com.rcha0s.awesomesecurity.backfill`: RunAtLoad, no schedule, no KeepAlive, plist
  outside `~/Library/LaunchAgents`). The job runs each chunk once, in its own worktree
  (`~/.local/share/awesomesec-backfill-worktree`), and waits up to 48h for that
  chunk's PR to be merged or closed before the next, so chunks dedupe against each
  other and never conflict. A guard skip passes to the next chunk; a failure stops it.
- **Watch / stop:** `scripts/backfill.sh status` (job state, the last `[backfill]`
  lines of `<runner>/data/_scan.log`, SPEND.md with the campaign total);
  `scripts/backfill.sh stop` unloads the job. Starting again resumes: finished
  chunks are refused by the guard.

### Auto-merge (Phase 4): content merges itself, the pipeline never does

`.github/workflows/automerge.yml` runs every 30 minutes (and on manual dispatch
from main) with main's code and main's config only. It looks at every open PR
on a `claude/scan-*` branch.

- **What can auto-merge:** a PR whose every changed path, including both sides
  of a rename and every deletion, is content: `data/`, `docs/`, the topic trees
  (`ai-security/`, `product-security/`, `ai-research/`, `claims/`) or the
  generated `README.md`, `NEWSLETTER.md`, `TRENDS.md`, `REVIEW.md`. Inside those
  directories only `.json`, `.md` and `.png` regular files count, plus exactly
  `docs/index.html` and `docs/.nojekyll`: no other HTML, because HTML runs
  script on the site's origin.
- **It must also pass `scripts/merge_gate.py`**, run inside the workflow on main
  merged with the PR head: pytest, the claim ledger, the analysis eval, any eval
  listed under `automerge.evals`, and these content checks
  (`scripts/content_checks.py`):
  - every `url` / `*_url` field in `data/*.json` is an `http(s)://` URL;
  - `docs/index.html` is byte-equal to main's `generate_html.render()` applied to
    the payload and stamp the page carries, so the page is main's template plus
    data, never hand-written HTML. The payload itself is still PR-shaped, so
    the template treats every payload value as hostile: text through
    `esc()`/`txt()`, links through `safeUrl()`, numbers through `num()`, and
    `generate_html` coerces trend numbers, dropping rows that fail;
  - every claim on main still exists, and **a scan PR may add new claims and
    append evidence to existing ones (bumping `last_reviewed`), nothing more.**
    Any other change to an existing claim, live or retired (status,
    statement, title, guidance, supersession fields, confidence, scope, a
    rewritten evidence item), is refused with "claim change needs human
    review": the PR stays open for a human to merge. Superseding a claim is
    therefore always a human merge;
  - every entry promoted on main (pools + archive) stays promoted, in every
    copy, unless main's copy had already failed integrity (refuted or
    ungrounded). `verified` and `grounding_score` are session-writable, so
    integrity that fails inside the PR doesn't count. Any other removal (an
    explicit demotion, an in-PR integrity flip, a vanished entry) is refused
    with "editorial demotion needs human review".
- **What never auto-merges, whatever the branch name or author:** anything
  else. That covers `scripts/`, `.github/`, `.claude/`, `tests/`, `evals/`,
  `config.yaml`, `requirements*.txt`, `*.toml`, `*.cfg`, `ISA.md`, `AGENTS.md`,
  `CLAUDE.md`, any dotfile, the source registry (`data/sources.json`,
  `data/source_proposals.json`: what scans fetch changes only through reviewed
  add-source PRs), the pipeline tuning under `data/` (`cluster_keywords.yaml`,
  `interests.yaml`, `source_blocklist.json`, any `.yaml`), staging files
  (`data/_*`, `candidates.json`, `analysis_out.json`, `editorial_out.json`),
  symlinks, submodules, executables and type changes. So does a PR from a fork,
  one not based on main, a draft, one labelled `automerge:hold`, and one whose
  head moved after it was tested: the merge call pins `sha=<tested head>`.
- **Source stats:** scans used to rewrite `data/sources.json` with hit-rate
  counts. Those now go to `data/source_stats.json` (allowed), which
  `sources_registry.load_sources()` lays over the registry, recomputing rank.
- **The boundary** is `scripts/merge_guard.py`, a pure module with exhaustive
  tests (`tests/test_merge_guard.py`). When it was built, a hand-run mutation
  pass (each rule loosened in turn) was killed by those tests; that pass is not
  in CI. Widening the allowlist is a security change: review it as one.
- **Shadow mode:** `automerge.mode` in `config.yaml` ships as `shadow`. The
  workflow evaluates every scan PR and reports its verdict in the job summary and
  one PR comment per head and verdict ("would merge", "refused" + reasons), and
  merges nothing. Anything other than exactly `merge` reads as shadow.
- **Merge mode needs owner-side settings the workflow cannot provide:** branch
  protection that restricts pushes to main to the owner only, `enforce_admins`
  on, a merge credential scoped to a main-only Environment, and scan identities
  (cloud routine, Mac runner) that can neither push workflow files nor merge.
  Without them a hijacked scan can go around this gate entirely. See ISA.md.
- **Flipping it:** set `automerge.mode: merge` in a normal reviewed PR to main,
  after the settings above are in place. That's Rohan's decision, recorded in
  ISA.md, once ISC-26's eval gate holds. To stop it again, set it back to
  `shadow`, or label one PR `automerge:hold`.
- **Phase 3 hook:** add an eval under `automerge.evals` in `config.yaml`. A
  listed script that doesn't exist yet is skipped until `required: true`; from
  then on a missing script fails the gate.
- In `merge` mode it also clears what main's protection needs: a branch that is
  behind main gets `update-branch` (the new head is judged on the next run), and
  a judged head missing the `pytest` check gets `tests.yml` dispatched, only
  after re-confirming the head hasn't moved. After merging it dispatches
  `update.yml` and requests a Pages build, because merges made with
  `GITHUB_TOKEN` start neither on their own.

## Evals (Phase 3: the reviewer nobody has to be)

Every eval is a CLI: exit 0 = pass, and its last stdout line is
`EVAL <name> PASS|FAIL key=value ...`. Results live in `data/evals/`.

- **Integrity** (`scripts/eval_integrity.py`, ISC-24): deterministic, no network. Every
  story the site shows has grounded excerpts (re-checked against `data/_raw/` when the
  text is on disk), an article citation (not a homepage), a taxonomy ID of its topic,
  and no duplicate id/URL in its lane; every pool + archive entry has a valid ID and
  http(s) URLs. Runs in the Tests workflow on every PR and in `merge_gate.py`
  (`automerge.evals`, required).
- **Readability** (`scripts/eval_readability.py`): deterministic. The share of
  published briefs (title, takeaway, summary, lesson points, action) that pass
  `scripts/readability.py` with no issue, plus how many have mild issues and how many
  merge would hold. Listed under `automerge.evals` as optional: it fails only below
  `readability.eval_min_pass` (0 = report only).
  - **The rewrite** is research-scan step 3b: a small model rewrites each brief for
    clarity BEFORE the factual verifier, so the verifier checks the published text. The
    skill first saves `data/_analysis_draft.json`.
  - **Facts are enforced in code:** `merge_analysis.py` matches each entry to its draft
    by `source_url` and `scripts/rewrite_guard.py` restores, field by field, any rewrite
    that changed a number or what it counts, a negation/version-range/severity word, a
    mid-sentence name, or added or dropped a CVE/GHSA id, number or code span (and any
    excerpt change). The entry records `readability_rewrite: reverted <fields>`; a
    revert never holds it. No draft for a non-empty analysis is a warning in merge and
    in the scan PR body. This guards against small-model rewrite error, not a hostile
    session (the session authors the draft).
  - **Holds:** merge records every brief's score (`readability`). Only a severe length
    or structure failure holds it in REVIEW.md (`readability_hold`, reason
    `readability: …`); acronyms, noun chains and long words are mild-only. Rerank
    re-judges holds under the current config and releases what it no longer supports.
  - **A readability hold never silently pulls a published entry:** merge doesn't hold an entry the
    site already shows (it reports `hold_skipped`), and `merge_gate.py`
    (`content_checks.readability_problems`) refuses a scan PR in which a shown-on-main
    entry gains a hold ("readability hold of a published entry needs human review").
    A sticky editorial promotion stays shown whatever its readability.
  - Code-owned notes (reverts, skipped holds, a missing draft) go to
    `data/_readability_outcomes.md`, which `post` puts in the PR body.
- **Recall** (`scripts/eval_recall.py --live [--write | --out PATH]`, ISC-22): this
  week's headlines from tl;dr sec, Simon Willison (security + prompt-injection tags),
  critical GHSA and new CISA KEV entries, kept when on-thesis by taxonomy keyword hints,
  matched against the pools + archive by canonical URL, CVE/GHSA id, or title +
  entities. Prints the misses and their hosts (the source-tuning signal). It writes no
  result when any curator errored. `post` fetches it fresh every run into a temp file
  (never into the tree). tl;dr sec headlines skip sponsor sections and paid links
  (a `utm_medium` other than `referral`).
  **Recall per curator, and independent:** the result carries `recall_by_curator` and
  an `independent` figure (also on the summary line). Because `ingest_curator_links.py`
  stages tl;dr sec's own links, a tl;dr sec headline can be held only because we
  ingested that curator: partly circular. Independent recall counts a headline as held
  only when its matching entry was not staged via a curator link (`curated_by` set or a
  `curator:` source_id). The 7-run gate keeps the overall figure, but in it a
  curator-staged match counts only when the analyzer vetted the entry: not
  `needs_review`, grounded (`publishable_grounding`, the rendered lanes' bar) and not
  `verified: false`. Every analyzed candidate lands in a pool, so presence alone would
  let the ingestor grade itself; an unvetted match is reported as a miss with
  `unvetted: <entry id>`. Matches by entries from our own sources are counted as
  before. The independent figure is the source-tuning signal: a widening gap between
  the two means our own sources are slipping behind the curator. tl;dr sec issues are
  picked like the ingestor's (newest `evals.recall.tldrsec_max_issues` by number,
  dated by the page itself).
- **Golden** (`data/evals/golden.json` + `scripts/eval_golden.py`, ISC-23): ~30 past
  stories with checked keep/drop, on-topic, domain ID and key facts. `score` grades an
  analyzer output file deterministically; `scripts/run_golden_local.sh` is the weekly
  LLM run: a rotating slice staged in a throwaway worktree that `stage` scrubs of every
  trace of those stories (entries, fields naming them, claim evidence, rendered site,
  `data/evals/`, story ledger; it refuses if a title or URL survives), under the scan's
  lockdown plus Read denies on `data/evals/`, `data/_golden*` and `.git/`. It opens a
  `claude/golden-<date>` PR with the result. **A wrong answer in a real run adds a
  case:** copy the story's entry into `cases` with the checked answer, a `reason`, and
  1-3 `facts` (each with `any` phrases), mark doubts in `unsure`, and run
  `eval_golden.py check`.
- **Cost + gate** (`scripts/eval_history.py`, ISC-25/26): `post` appends one row per
  scan PR to `data/evals/history.json` (candidates, stories, kept, integrity, this run's
  recall with its independent and per-curator figures, the newest golden result, the ledger charge with its basis) and puts the
  numbers and the 7-run trend in the PR body. `eval_history.py gate` passes when the
  last `evals.gate_runs` rows all clear `evals.thresholds`: a measured charge against
  the per-run cap, a reservation against its own ceiling, and staleness judged at each
  run's date. **A scan can't grade itself:** `post` resets `data/evals/` to main's copy
  before appending; `merge_guard.py` lets a scan PR change only `data/evals/history.json`
  there; and `merge_gate.py` (`content_checks.history_problems`) requires main's rows
  to be an exact prefix, at most one new row, and that row's charge to be the run's
  charge on the budget ledger (its latest `actual` row, else its reservation; a
  measured basis only on a local run) and its integrity, golden result and cap to
  match what the gate recomputes.
  The recall figures (overall, independent, per curator) are the values taken on trust
  (they need the network); `content_checks.recall_shape_problems` checks only their
  shape. The PR body's trend table shows recall with the independent figure beside it,
  and a "Recall by curator" line for this run.

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
