---
name: pull-latest
description: Refresh the repo with the latest articles and claims. Runs the deterministic ingest step end-to-end (RSS + HN + GHSA + arXiv conferences), then hands off to /research-scan for the LLM analysis + merge + claim reconciliation. Use when the user says "pull the latest", "refresh the repo", "update articles", or "check for new claims".
---

# pull-latest

Refreshes the knowledge base end-to-end. The pipeline has two parts and this
skill runs them in order:

1. **Deterministic ingest** — polls the ranked source registry (RSS, HN, GHSA,
   arXiv conferences). Fast (~10s), no LLM, idempotent. Stages new items in
   `data/candidates.json`.
2. **Agentic analyze + merge** — reads each candidate, extracts lessons with
   grounded excerpts, scores novelty/relevance, does adversarial verification,
   merges into the pool, reconciles the claim ledger. This part is expensive
   (one LLM pass per candidate) and non-idempotent; the user can stop it early
   and resume later.

If the user just wants "what's new upstream, no analysis yet," run step 1 only
and stop.

## Preconditions

- Run from the repo root.
- Python deps installed: `pip install -r requirements.txt`. If any ingest
  script errors with "Missing dependencies", stop and install; don't retry.
- Twitter ingest is **skipped by default** here — it lives in WSL2 with a
  burner account and datacenter IPs risk the account. The user can invoke
  the full `/research-scan` skill separately if they want Twitter.

## Steps

### 1. Deterministic ingest

Run the four network-safe ingest scripts. Each is idempotent (dedupes by URL
+ title against the pool + existing candidates), so re-running is safe.

```bash
python scripts/aggregate.py            # RSS/Atom sources (the registry)
python scripts/ingest_hn.py            # Hacker News (keyword queries + top-stories tap)
python scripts/ingest_ghsa.py          # GitHub Security Advisories (needs `gh` authed)
python scripts/ingest_conferences.py   # USENIX/NDSS/SaTML/AISec/CCS via arXiv
```

Report a one-line summary per script (candidates added), and the running
total in `data/candidates.json` at the end.

If `ingest_ghsa.py` fails with a `gh` auth error, run `gh auth status` — the
user's PAT may have expired. Continue with the other three; GHSA is not
load-bearing.

### 2. Ask before running the analysis pass

Analysis is the expensive step and takes several minutes to an hour depending
on the candidate count. Before starting it:

- **Report the candidate count** and the top 5–10 titles so the user sees
  what's on the runway.
- **Ask if they want to proceed** with analysis, or stop here so they can
  triage which candidates to keep.

If they want to stop, that's a valid outcome. `data/candidates.json` persists
and analysis can resume later.

### 3. Agentic analyze + merge + reconcile (if approved)

Invoke the existing `/research-scan` skill for the analysis loop. That skill
handles:

- Reading each candidate + its `raw_path` clean text.
- Topic + domain classification, lesson extraction with grounded excerpts.
- Novelty/relevance scoring with the topic-specific rubric.
- Adversarial verification (fresh subagent tries to refute; take the lower
  novelty score).
- Emitting `data/analysis_out.json`.
- Running `python scripts/merge_analysis.py` (validates, dedupes, grounds
  excerpts, routes by topic, flags needs_review, reranks).
- Reconciling the claim ledger via `scripts/add_claim.py` (new claim, evidence
  attach, superseded, or contested).

The `/research-scan` skill has the full protocol; don't try to re-implement it
here.

### 4. Regenerate the site

After merge, regenerate all rendered artifacts so `docs/index.html`, the
per-topic READMEs, the newsletter, trends, review queue, and the claim
ledger reflect the new state:

```bash
python scripts/rerank.py
python scripts/generate_site.py
python scripts/generate_claims.py
python scripts/generate_html.py
python scripts/generate_og.py
python scripts/trends.py
python scripts/generate_newsletter.py
python scripts/generate_review.py
```

### 5. Open a PR (do NOT push to main directly)

`main` is branch-protected. Stage changes on `chore/pull-latest-<date>` and
open a PR against main so the user reviews the diff before merge. Never
`git push origin main` directly.

```bash
branch="chore/pull-latest-$(date -u +%Y-%m-%d)"
git checkout -B "$branch"
git add data/ ai-security/ ai-research/ product-security/ claims/ docs/ \
        README.md NEWSLETTER.md TRENDS.md REVIEW.md
git commit -m "chore: pull latest ($(date -u +%Y-%m-%d)) — <N> new findings, <M> claim edits"
git push --force origin "HEAD:$branch"
gh pr create --base main --head "$branch" \
  --title "chore: pull latest ($(date -u +%Y-%m-%d))" \
  --body "<summary of new findings + claim reconciliations>"
```

### 6. Report back

Tell the user:

- **How many candidates ingested** in step 1.
- **How many merged into the pool** (analysis wasn't run OR N of M passed the
  gate).
- **What changed in the claim ledger** (new / evidence-attached / superseded /
  contested).
- **PR URL** if step 5 opened one, or "no changes to commit" if the ingest
  produced nothing new.

## When NOT to invoke this skill

- **The user asked "what's trending" or "what's in the news"** — that's a
  read of the live site or the latest render, not a refresh. Don't run ingest.
- **The user asked to add a single article** — use `/add-resource` instead
  (single-item flow, no full ingest).
- **The user asked to add a source** — use `/add-source`.
- **CI already ran today and merged a PR** — the pool is fresh; running again
  is churn. Check the last `chore/pull-latest-*` PR date before starting.

## Failure modes

- **`aggregate.py` fails on one feed.** Continue with the others; report the
  bad feed at the end. Don't retry — it's a source-side issue.
- **`ingest_ghsa.py` gh auth error.** Continue with the other three.
- **Analysis pass times out mid-candidate.** `data/candidates.json` persists;
  the next `/research-scan` invocation resumes.
- **User cancels between step 1 and step 3.** That's fine — candidates stage,
  no site state changes, PR isn't opened. Next invocation starts from step 2.
