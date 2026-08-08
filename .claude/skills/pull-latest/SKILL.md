---
name: pull-latest
description: Ingest-first refresh with a model-judged gate before delegating the expensive analysis + render + PR pass to /research-scan. Use when the user says "pull the latest", "refresh the repo", "update articles", or "check for new claims". Model decides — no human approval prompt.
---

# pull-latest

Refreshes the knowledge base end-to-end. Thin front-door for
`/research-scan` — this skill owns two things:

1. Running the network-safe ingest scripts first so we know what's on
   the runway.
2. **Judging** whether the runway is worth the LLM spend of a full
   analysis pass. That judgement is made by you (the model), not by
   asking the user. The rubric is spelled out below.

Everything else — analysis, claim reconciliation, render, commit, PR —
belongs to `/research-scan`.

## Preconditions

- Run from the repo root.
- Python deps installed: `pip install -r requirements.txt`. If any
  ingest script errors with "Missing dependencies", stop and install;
  don't retry.
- **One refresh PR is in flight at a time.** The repo's convention is
  a single `chore/research-scan-refresh` branch. `/research-scan`
  step 8 pushes to that fixed branch and reuses the existing PR if
  present. There is no coordination needed against concurrent refresh
  PRs; assume you're the only writer.

## Steps

### 1. Ingest — five network-safe scripts

Each is idempotent (dedupes by URL + title against the pool + existing
candidates), so re-running is safe. Individual failures don't halt
the loop — log the failure and continue.

```bash
python scripts/aggregate.py            # RSS/Atom from the ranked registry
python scripts/ingest_hn.py            # HN keyword queries + top-stories tap
python scripts/ingest_ghsa.py          # GitHub Security Advisories (needs `gh` authed)
python scripts/ingest_conferences.py   # USENIX/NDSS/SaTML/AISec/CCS via arXiv
python scripts/ingest_github.py        # trending/novel security repos (needs `gh` authed)
```

**Not run here:** `ingest_twitter.py` (needs WSL2 + burner cookies —
out of scope for a headless refresh; if the user wants Twitter,
invoke `/research-scan` directly). `ingest_youtube.py` (not in
`/research-scan` either — track separately if you want it).

Report per script: candidates added, and any failure. Then read
`data/candidates.json` and note the running total.

### 2. Model-as-judge — decide whether to proceed to analysis

Analysis is the expensive step (one LLM pass per candidate — several
minutes to hours). Do not run it reflexively. Apply this rubric:

**Proceed to step 3 if ALL of these hold:**
- Total candidates in `data/candidates.json` is **≥5**.
- Any single track (ai-security, product-security, ai-research) has
  **≥3 credible-looking titles** — skim the titles, discard obvious
  spam/puff/duplicate coverage before counting.
- At least one candidate is published **<7 days old** (freshness
  bar — an old backlog isn't a reason to burn a scan).

**Stop if any of the following:**
- Total candidates <5 — no material to work with; a future run will
  accumulate more.
- Every track fails the sniff-test — titles are all spam/marketing/
  stock news / off-topic. `data/candidates.json` persists; run again
  in a day or two.
- No candidate <7 days old — nothing fresh. Same recovery.

**Never** stop silently. Log your reasoning:
- If proceeding: "Proceeding to /research-scan — N candidates,
  freshest is X days old, top titles: [top 5]."
- If skipping: "Skipping analysis — [reason]. Candidates staged in
  data/candidates.json for the next run."

This is the audit trail for the model's judgement. A human reading
the run log later should see why you made the call.

**Note on dedup:** `candidates.json` is gitignored and not durable —
a future run will re-ingest and dedupe. This is expected. Dedup
against the *actual persisted database* (`data/*.json` pool + archive
+ claim ledger) happens at merge time in `merge_analysis.py` and at
story-key time in `dedupe_stories.py`. `candidates.json` is a
staging area, not storage.

### 3. Delegate to `/research-scan` (only if step 2 said proceed)

One line: invoke `/research-scan`. That skill owns analysis, merge,
claim reconciliation, render, commit, and PR against `main` on the
fixed `chore/research-scan-refresh` branch.

Do NOT re-run render commands here. Do NOT try to commit, push, or
open a PR here. Those are `/research-scan`'s job.

Note: `/research-scan` step 1 re-runs the ingest scripts (including
Twitter if WSL2 is set up). The re-ingest is idempotent, so no harm.
The Twitter concern is deliberately not raised at the gate — users
who invoke `pull-latest` are assumed to know that the full pipeline
delegates to `/research-scan`.

### 4. Report back

Whatever step 2/3 did, print a summary:

- **Ingest results** — per script, candidates added. Any failures.
- **Judgement** — proceeded or skipped, with the specific reason
  from step 2's rubric.
- **If proceeded** — the summary `/research-scan` step 8 prints on
  its own PR. Include the PR URL.
- **If skipped** — running total in `data/candidates.json` and the
  suggested next check (e.g., "run again in 2–3 days").

## When NOT to invoke this skill

- **The user asked "what's trending" or "what's in the news"** —
  that's a read of the live site, not a refresh. Don't run ingest.
- **The user asked to add a single article** — use `/add-resource`.
- **The user asked to add a source** — use `/add-source`.
- **The user wants Twitter/social included** — invoke `/research-scan`
  directly; this skill's ingest step deliberately skips Twitter.
- **A `chore/research-scan-refresh` PR is already open with today's
  changes** — running again would push another commit onto the same
  branch; that's fine if there's real drift, but check first.

## Failure modes

- **Any single ingest script fails mid-run** — log it, continue with
  the rest. Report failed ingesters at step 4.
- **Step 2 rubric edge cases** — when in doubt, skip. Analysis is
  expensive; the cost of a false-negative (waiting an extra day for
  a bigger backlog) is much smaller than a false-positive (burning
  an analysis pass on marketing puff).
- **`/research-scan` cancels mid-analysis** — that's its concern,
  not ours. `data/candidates.json` persists and the next
  `/research-scan` invocation resumes.
