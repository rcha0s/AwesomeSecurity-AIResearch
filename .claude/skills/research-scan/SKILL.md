---
name: research-scan
description: Scan the registered sources (RSS, sitemaps, GitHub, GHSA, HN, conferences) for AI and security material, extract teachable lessons, score newness/novelty/relevance, derive actionable leverage, and grow the security/ and ai/ knowledge pools. Use for a full batch refresh (self-pace with /loop).
---

# research-scan

Batch pipeline that turns fresh security/AI material into scored, source-cited,
actionable pool entries. You (the model) are the analysis engine — the Python
scripts handle deterministic ingestion, merging, ranking, and rendering.

Run everything from the repo root. X/Twitter is not batch-ingested (#57); ad-hoc `add.py <x.com URL>` still works.

## Steps

1. **Ingest → stage candidates** (writes `data/candidates.json`, gitignored).
   Run every ingestor each scan for breadth (no cookies; `gh` must be authed):
   ```bash
   python scripts/ingest_curator_links.py  # stories tl;dr sec's recent issues link to (first:
                                           # it records their arXiv ids for the paper gate)
   python scripts/aggregate.py       # RSS/Atom + newsletter feeds (the registry)
   python scripts/ingest_sitemap.py  # sitemap.xml for research_index sources with no feed (e.g. Anthropic)
   python scripts/ingest_github.py   # trending/novel repos (needs `gh` authed)
   python scripts/ingest_ghsa.py     # reviewed supply-chain advisories (needs `gh` authed)
   python scripts/ingest_hn.py       # Hacker News velocity signal (keyless, network)
   python scripts/ingest_conferences.py  # accepted papers at USENIX/NDSS/SaTML/AISec/CCS
                                         # (+security-gated NeurIPS/ICML/ISSTA) via arXiv
   python scripts/ingest_json_feeds.py   # CISA KEV (exploited in the wild) + HF Daily Papers
   ```

2. **Read the candidates.** Load `data/candidates.json`. In the daily scan it holds only this
   run's batch (`scripts/select_batch.py`), and the session's budget is sized for that batch:
   work through the whole batch, and never stop for budget reasons before analyzing. A weak
   candidate is analyzed with honest low scores (the curation gate holds it in REVIEW.md),
   never dropped, so a real analysis is never empty. For each candidate, read its `raw_path` file under `data/_raw/` for the full article text.
   If `raw_path` is null but `article_url` is set, fetch clean text yourself:
   `curl -s https://r.jina.ai/<url>`.

2b. **Match each candidate to a known story (small-model judge).** The story is the unit:
   one row per real-world story in `data/news_stories.json`, never expiring. Stage the
   deterministic shortlist (the daily scan's `pre` phase already did):
   ```bash
   python scripts/story_ledger.py shortlist   # -> data/story_shortlist.json
   ```
   It maps each staged candidate id (the batch, in the daily scan) to at most 5 stories
   from the last 90 days that it *might* be (tuned to over-match). Candidates with an empty
   list are new; skip them here. For the rest, spawn ONE fresh subagent on the smallest model (`model: haiku`) per batch of up
   to 10 candidates, given ONLY each candidate's title, source and first ~1,500 chars of
   text, plus its shortlisted stories (title, sources, latest update). Ask for one verdict
   per candidate:
   - `same` — another report of a story we have (same event, same facts). No new entry.
   - `update` — a real new development on that story (new facts, a new victim, a fix, a
     reversal). One-sentence `note` saying what changed; it becomes the story's dated
     "Updated" line.
   - `new` — none of the shortlisted stories; when unsure between `same` and `new`, `new`.
   Write its answers, unedited, to `data/story_verdicts.json`:
   `[{"candidate_id": "...", "verdict": "same|update|new", "story_id": "<from the shortlist>", "note": "..."}]`.
   Do NOT analyze `same` or `update` candidates in step 3; `merge_analysis.py` applies the
   verdicts (adds the covering source, the Updated line, drops those candidates) and rejects
   any `story_id` that wasn't on that candidate's shortlist (recomputed from the ledger, not
   read back from the file). Never edit `data/news_stories.json` or the shortlist yourself;
   merge_analysis.py writes its own record of every verdict to the PR body. An `update` prints
   `CLAIM REVIEW` lines for the story's linked claims: put them in the run summary and
   reconcile them in step 6 if the evidence warrants. Never auto-supersede on an update.

3. **Analyze each candidate** grounded in the source text (never invent facts):
   - **topic** — exactly one of three (see `scripts/common.py` `TOPICS`):
     - `ai-security` — securing AI systems: harness/agent security, MCP, skill scanning,
       prompt injection, memory poisoning, model supply chain, LLM red-teaming.
     - `product-security` — securing products: appsec, supply chain, cloud/infra, identity,
       mobile, **red teaming and threat modeling** (AI-assisted or not).
     - `ai-research` — **practitioner** AI: improving your harness, understanding, or
       architecture for using LLMs/agents on real tasks. NOT model internals / ML-research.
   - **domain** — exactly one domain **ID** of the entry's topic, copied from
     `python scripts/taxonomy.py list` (run it once before analyzing, or read the `domains`
     block of the file directly where that command is not allowed; the vocabulary lives in
     [`data/taxonomy.yaml`](../../../data/taxonomy.yaml)). Never free text: `merge_analysis.py`
     holds any entry whose `domain` is not an ID of its topic, files it under the nearest ID,
     and moves the label into `tags`. Assign by reasoning about the finding, not by keyword
     match. Claim work follows the domain: the list marks each domain `claims` or
     `news only` (frontier-model capability shifts, off-thesis ML, general appsec), so pick
     the honest domain rather than one that earns claim treatment. Do not emit the old
     `cluster` letter.
   - **proposed_domain** — only when NO domain fits: still set `domain` to the nearest ID,
     and add `{name, scope, nearest, why_different}` (`nearest` = that ID, `why_different` =
     one sentence on what the existing domain cannot hold). Step 4b verifies it.
   - **related_claims** — up to **3** claim IDs from the existing ledger that this
     finding bears on (supports, contests, refutes, or would supersede). Read the
     ledger via `python scripts/add_claim.py list` before analyzing. Leave empty if the
     finding stands alone. Extras beyond the cap of 3 belong in step 8's PR body under
     an audit-of-cap section.
   - **summary** — 2-3 sentence teachable summary.
   - **lessons** — the concrete, transferable takeaways. Each: `{point, excerpt,
     confidence}` where `excerpt` is a short quote/anchor from the source and
     `confidence` ∈ [0,1] reflects how well the source supports the point. Be honest —
     low confidence auto-flags the entry for review instead of publishing it as fact.
   - **takeaway** — one-line "so what."
   - **tags** — cross-cutting topics (e.g. `prompt-injection`, `mcp`, `rag`, `evals`).
   - **actionable** — `{type, title, detail, skill_slug?}`. `type` ∈ takeaway | skill |
     harness | tool | other. Choose whatever genuinely fits: a reusable **skill** (set a
     kebab `skill_slug`), a **harness** improvement, a **tool** idea, or just a
     **takeaway**. `detail` should be concrete enough to act on.
   - **scores** — `{novelty, relevance}` each 0-100 (newness + credibility are computed):
     - **novelty is a claim-level "delta vs prior art", NOT text similarity.** First state the
       finding's core *claim* (the specific technique/mechanism/result/implementation). Then
       skim the existing entries in `data/{ai-security,product-security,ai-research}.json` +
       recent `data/archive.json` for the nearest ones, and judge how much is genuinely new
       versus known prior work. Can't name an equivalent → high; a variation of something known
       → mid; a restatement/duplicate → low. Put the closest prior work in a `prior_art` field.
     - **relevance**: usefulness to the topic's audience (AI Security = a defender; Product
       Security = an appsec/red-team engineer; AI Research = a harness/agent builder).
   - Security findings may also include `threat`/`conditions`/`mitigations`.

3c. **News briefs (the news tier).** A candidate tagged `batch_tier: "news"` is relevant news
   the deep tier had no room for (`batch_news.reason`: `story`, `kev`, `ghsa-critical`,
   `ghsa-ai` or `marker`). It gets a short brief instead of step 3, and no verifier pass:
   ```json
   {"brief": "news", "topic": "...", "domain": "<an ID of the topic>",
    "title": "what happened, concretely", "source_url": "<the candidate's own URL>",
    "takeaway": "one sentence: so what, for the topic's reader",
    "summary": "1-2 sentences: who, what, how bad, what to do",
    "lessons": [{"point": "what the quote shows", "excerpt": "<ONE verbatim quote, 20+ chars>",
                 "confidence": 0.N}],
    "related_claims": []}
   ```
   plus the carried fields of step 5 (`article_url, published, raw_path, source_id,
   source_rank, discovered_via, source_name`). No `scores`, no `actionable`, exactly one
   lesson. Fetch every news candidate's text first (`python scripts/fetch_raw.py <id>`, several
   per turn), then write briefs in batches of up to 10 with ONE fresh subagent per batch
   (`model: sonnet`), given only each candidate's id, title, source, `raw_path` and this schema;
   it reads the raw files and returns the briefs. Keep the main context small: don't read
   news-tier raw files yourself. If two candidates in the session tell the same story, write
   one entry (deep beats brief) and put the other's URL in its `corroborating_sources`
   (`{"name", "url", "published"}`). `merge_analysis.py` accepts a brief only for a news-tier
   candidate of this run (`data/_scan_tiers.json`, code-owned), attaches the story group's
   covering sources from there, and grounds the excerpt itself: an ungrounded brief is held
   in REVIEW.md, never published. Briefs go through step 3b's readability rewrite like any
   brief, then show in the news lane (never as vetted findings).

3b. **Readability review (small model, before verification).** Readers are senior security
   engineers who skim: each brief must make sense on first read. Done means every brief
   leads with the concrete point, in plain words and short sentences, with every acronym
   outside `readability.allow_acronyms` (config.yaml) expanded on first use, no stacked
   hedges, no marketing tone, a one-sentence takeaway, and exactly the facts it had before.
   - Write the analyzed entries to `data/analysis_out.json` and copy that file to
     `data/_analysis_draft.json` (the before-picture `merge_analysis.py` checks against).
   - Spawn ONE fresh subagent (`model: haiku`) per batch of up to 10, given ONLY each
     entry's `title`, `takeaway`, `summary`, lesson `point`s and `actionable.title`/`detail`.
     It returns those fields rewritten for clarity: every number with what it counts, every
     negation, version bound and severity word, every name, CVE/GHSA id and code span kept;
     nothing added. It never sees or touches excerpts. Put its text back; change nothing else.
   - Run `python scripts/readability.py --analysis`. A `REWRITE:` line names a field whose
     facts changed: restore it from the draft now (merge would restore it anyway). Rewrite
     each `HOLD` entry once more yourself against its listed issues and check again; `MILD`
     entries keep their one rewrite. What still says `HOLD` stays: `merge_analysis.py` holds
     it in REVIEW.md with its `readability: …` reason.
   - Step 4's verifier then checks this final text, the text that gets published.

4. **Independent verification (adversarial second pass).** News briefs (3c) skip this step: their
   one excerpt is grounded in code. For each shortlisted finding, spawn a
   FRESH subagent (the Task tool) given ONLY the raw source text + the extracted claims — do NOT
   give it your scores. Prompt it to **refute**: (a) is every lesson actually supported by the
   source? (b) independently re-judge novelty as claim-level delta-vs-prior-art (name the closest
   prior work). (c) re-judge relevance. Then reconcile:
   - if the verifier refutes a claim, or its novelty is much lower than yours (disagreement),
     set `verified: false` and a short `verify_note` — the merge gate sends it to REVIEW.md;
   - otherwise set `verified: true`, take the **lower** of the two novelty scores, and record
     `prior_art`. This makes the score an independent judgment, not a self-grade.

4b. **Verify any `proposed_domain` (small model).** For each entry that carries one, spawn a
   FRESH subagent on the smallest model (`model: haiku`) given ONLY the entry's title + summary,
   the proposal's `name`/`scope`, and the output of `python scripts/taxonomy.py list`. Its job
   is to reject: it must (a) name the nearest EXISTING domain ID and (b) say in one sentence
   why the proposal is really different from it, or answer `fail` if that domain already
   covers the finding. Write its answer onto the proposal as
   `verifier: {verdict: pass|fail, nearest: <id>, reason: <sentence>}`. Do not edit the
   verdict. `merge_analysis.py` records only passing proposals (and only when `nearest` is a
   real ID of the entry's topic); `scripts/taxonomy_proposals.py` opens or comments on a
   `taxonomy` issue once the same proposal recurs on 3+ entries in 30 days.

5. **Emit** `data/analysis_out.json` — a JSON list of analyzed entries (each: at minimum
   `topic, domain, title, source_url, related_claims`, plus the fields above incl.
   `verified`, `prior_art` and any `proposed_domain`; carry over `article_url, tweet_url, author, date, published,
   raw_path, discovered_via, source_id, source_rank, source_topics, curated_by, curator_issue`
   from the candidate; `merge_analysis.py` re-stamps the last two from the candidate anyway).
   `source_id` lets `merge_analysis.py` credit the source's hit-rate; `raw_path` lets it
   ground the excerpts. `domain` must be an ID of the entry's topic (held for review
   otherwise); `related_claims` must be a list of at most 3 claim IDs (schema enforced by
   `common.validate_entry`).

6. **Reconcile the claim ledger** (`data/claims.json`) — the step that makes this a tracker
   of *what we believe* and not just *what was published*. A finding is one article; a **claim**
   is the durable answer to a question, and it never ages out.

   Read the ledger (`python scripts/add_claim.py list`) and, for each curated finding from
   this scan, decide which one of four things it is:

   - **Additive** — it supports an existing claim. Attach it as evidence:
     `python scripts/add_claim.py evidence <claim-id> --evidence "supports|<url>|<title>|<date>|<note>" --source-name "<publisher>"`
     (the note is optional: one sentence on what this source shows for the claim).
   - **New** — it answers a question the ledger has no claim for. Add one, with the
     `guidance` (what to DO) and `scope` (where it does *not* apply):
     `python scripts/add_claim.py new <kebab-id> --topic … --domain … --statement … --guidance … --scope … --confidence 0.N --evidence "supports|<url>|<title>|<date>"`
   - **Superseding** — it gives a *better answer* than a claim we already hold. Write the new
     claim first, then retire the old one; both ends of the edge are written for you:
     `python scripts/add_claim.py supersede <old-id> <new-id> --reason "<why the old answer no longer holds>"`
     Add `--refuted` when the old claim was shown to be **wrong**, not merely improved on.
   - **Contesting** — it cuts against a standing claim but doesn't settle the question.
     Attach it with a `contests`/`refutes` stance and move the claim to
     `status: contested` (`python scripts/add_claim.py status <id> --set contested`).
     Contested is an honest answer — do NOT force a winner.

   Never edit `data/claims.json` by hand (the Mac session is denied it): the CLI
   appends new evidence at the end, and a scan PR that reorders or rewrites an
   existing claim's evidence is refused by the merge gate.

   Rules: the `reason` on a supersession is the whole point, so make it specific and
   evidence-backed ("graph retrieval beat lexical search on multi-hop recall"), never
   vague ("newer research"). Never delete or edit a retired claim's history. One claim per
   question — if two claims say the same thing, supersede one into the other. Be
   conservative: a single blog post rarely overturns a standing claim, and `confidence`
   should reflect the strength and independence of the evidence, not your enthusiasm.

7. **Merge + rerank + render:**
   ```bash
   python scripts/merge_analysis.py       # story verdicts, validate, dedup, route by topic, GROUND excerpts, flag, rerank
   python scripts/verify_citations.py     # re-verify every lesson excerpt vs its source (persist grounding)
   python scripts/add_claim.py validate   # claim ledger integrity (edges resolve, no cycles)
   python scripts/generate_site.py        # README.md + ai-security/ product-security/ ai-research/
   python scripts/generate_claims.py      # claims/ — standing answers + what they replaced
   python scripts/trends.py               # data/trends.json + TRENDS.md (emerging themes)
   python scripts/generate_newsletter.py  # NEWSLETTER.md (rolling, 3 topic sections)
   python scripts/generate_review.py      # REVIEW.md (non-vetted queue)
   python scripts/generate_html.py        # docs/index.html — the GitHub Pages site
   ```
   Only **vetted** findings (not `needs_review`, composite ≥ `curation.min_composite`) appear on
   the topic pages/newsletter; borderline ones land in `REVIEW.md` for a human to promote.

8. **Commit (direct-PR mode).** Idempotent PR against a fixed branch so
   duplicate scans on the same day converge on one PR instead of
   proliferating. The convention is **one refresh PR in flight at a
   time** — this skill assumes it is the only writer and dedups against
   the persisted database (`data/*.json` pool + archive + claim ledger)
   rather than against other open PRs.

   **Fixed branch:** `chore/research-scan-refresh`. Bot-owned,
   disposable. Do NOT invent a per-run branch name.

   **Files to stage** (never commit `data/candidates.json`,
   `data/_raw/`, `data/analysis_out.json`, or cookies):

   ```bash
   git add data/*.json README.md NEWSLETTER.md TRENDS.md REVIEW.md \
     ai-security product-security ai-research claims docs
   ```

   **Early exit** — if `python scripts/scan_count.py --work` exits 3
   (no analyzed entry and no applied story verdict), print `no analysis;
   nothing to PR` and stop: a rerank alone is not a scan. Likewise if
   `git status --porcelain` is empty after the render pass in step 7,
   print `no drift; nothing to PR` and stop. Do not create an empty commit.

   **Push and PR** — mirror `.github/workflows/update.yml`'s pattern
   exactly (proven idempotent; `--force-with-lease` fails when the
   runner has no local ref, so plain `--force` on this bot-owned
   branch is correct):

   ```bash
   branch="chore/research-scan-refresh"
   git config user.name "github-actions[bot]"
   git config user.email "github-actions[bot]@users.noreply.github.com"
   git checkout -B "$branch"
   git commit -m "chore: research scan refresh ($(date -u +%Y-%m-%d))"
   git push --force origin "HEAD:$branch"

   # Reuse an open PR on this branch, else open one. Never `gh pr view`:
   # it matches merged PRs and silently skips the create.
   scripts/ensure_pr.sh "$branch" \
     "chore: research scan refresh ($(date -u +%Y-%m-%d))" \
     "<run summary — see below>"
   ```

   **Run summary** (printed to the user AND set as the PR body): lead
   with **every claim change** — added, evidence-attached, contested,
   superseded/refuted, with the reason for each retirement. Claim
   reversals are the headline of a scan. Then: candidates ingested,
   entries merged per topic, how many flagged needs_review, and the
   top movers by composite.

## Backfill mode

If asked to backfill, treat the existing pool entries that lack `lessons`/`scores` as
candidates: read their `source_url`, analyze with the same rubric, and re-emit them
through `analysis_out.json` (merge updates them in place by URL).
