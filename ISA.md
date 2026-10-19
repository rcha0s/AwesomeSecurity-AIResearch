---
phase: climbing
progress: 3/9
principal_stated_goal: "Create a plan for what needs to be done here in terms of making this more sustainable. Auto-deployed so I don't need to even review it on a day-to-day basis. But I want to do some evaluation that the generation as well as testing code is very reliable and is cost-efficient. And is also capturing all the important stories that are relevant on a day-to-day basis. And I want to run this on the cloud ... but have an option of running it locally on this machine and not on the Windows machine. So basically, remove that configuration completely."
---

# AwesomeSecurity-AIResearch — sustainable, auto-deployed pipeline

## Problem

The pipeline stalled on 2026-09-09: the daily scan was a Windows Scheduled Task, and the
weekly render CI has failed every run since 2026-09-21 because tests read the real clock.
87% of LLM-analyzed findings are discarded, the same story appears as many findings, and
the `domain` field has drifted to 127 free-text labels across 246 entries.

## Vision

Every morning the site shows a short, deduplicated set of the stories a security engineer
must not miss, plus the claim ledger of what to do now. It runs on Claude cloud within the
granted credits, falls back to this Mac, merges itself when evals pass, and nobody has to
review it day to day.

## Out of Scope

- X/Twitter ingestion (future, local-only runner; tracked separately).
- UI redesign (#50), re-evaluating held findings (#51), backfilling the Sept→now gap (#52).

## Constraints

- Repo stays public; no private data in commits.
- Scan PRs may auto-merge only when they touch data/rendered files; code PRs get
  `/security-review` + `/code-review` before merge.
- Cloud runs spend granted credits only.

## Features

### F0 · Phase 0 — CI green
Why: nothing else is safe to build while the gate that protects main is broken.

- [x] ISC-1: `pytest` passes on Python 3.12 with the system clock set to any date after 2026-10-18 (probe: run suite under a faked far-future clock). — 375 passed at real clock and under time-machine 2031-03-01
- [x] ISC-2: No Python code or test reads the wall clock except `common.utcnow()`, which `tests/conftest.py` pins (probe: `rg 'datetime.now' scripts tests` → only the seam). — 🧹 CLASS-SWEEP: wall-clock reads — 34 sites via rg; 33 routed through the seam, 1 is the seam
- [ ] ISC-3: A pull_request workflow runs pytest on every PR (probe: the PR shows a passing `Tests / pytest` check).
- [x] ISC-4: No doc or prompt references a script that does not exist (probe: every `scripts/*.py` named in `daily_scan_prompt.md` exists; `rg --hidden generate_skills` → 0). — 🧹 CLASS-SWEEP: generate_skills refs — 9 via `rg --hidden` in 6 files (first pass missed `.claude/`; caught by code review); 9 fixed
- [ ] ISC-5: The render workflow passes on main after merge (probe: `gh run list --workflow update.yml` latest = success).
- [ ] Anti ISC-A1: Phase 0 does not publish an emptied site — every pool entry is older than `max_age_days`, so a re-render now would prune the whole briefing (probe: `docs/index.html` findings count unchanged by this PR).

### F1 · Phase 1 — one entrypoint, cloud + local (after: ISC-5)
Why: the run must happen without a human or a Windows box.

- [ ] ISC-6: No Windows/WSL scan configuration remains in the repo (probe: no `*.ps1`, no `wsl`/`Agent Reach` references outside history).
- [ ] ISC-7: One cloud routine run and one local `claude -p` run each open a scan PR of the same shape.
- [ ] ISC-8: A run that finds no credit budget left exits before any LLM work and says so.
- [ ] ISC-9: A failed run opens a GitHub issue.

## Not yet specified

- Can a cloud routine read the remaining credit balance, or be limited to credits only?
- Can per-run token usage be read inside a cloud session?
- Phases 2–6 (taxonomy IDs, story ledger, evals, gated auto-merge, sources, README/site)
  graduate into claims when Phase 1 closes. Full plan: the "AwesomeSecurity-AIResearch
  Sustainability Plan" doc.

## Decisions

- 2026-10-18: the site's JS `Date.now()` (`scripts/templates/site.html`, "days ago" display) stays on the viewer's clock by design; ISC-2 scopes to the Python pipeline.
- 2026-10-18: AGENTS.md documents ruff + black + coverage as the PR suite; CI runs pytest only until the lint pass lands (Remaining Work).

- 2026-10-18: Phase 0 does not re-render the site. All pool entries are older than 31 days,
  so a re-render would publish an empty briefing; the first Phase 1 scan re-renders with
  fresh content instead.
- 2026-10-18: the clock fix is one seam (`common.utcnow()`) pinned by an autouse fixture, not per-test `now=` arguments: the per-call approach would leave every future test one forgotten argument away from the same failure.
- 2026-10-18: no PR-triggered test workflow existed (only main-push render), so ISC-3 adds one;
  it is also the check Phase 4 auto-merge will gate on.

## Verification

## Remaining Work

- [ ] Repo-wide lint pass (main has 19 ruff errors and 26 black-unformatted files), then add ruff + black to `tests.yml`. Kept out of the Phase 0 PR so the clock fix stays reviewable.
- [ ] As soon as this merges, the push-triggered render job will prune every pool entry (all older than 31 days) and open a render PR with an empty briefing. Do not merge it; Phase 1's first scan supplies fresh content.
