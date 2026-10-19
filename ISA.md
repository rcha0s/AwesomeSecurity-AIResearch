---
phase: climbing
progress: 11/13
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
- [x] ISC-3: A pull_request workflow runs pytest on every PR (probe: the PR shows a passing `Tests / pytest` check). — PR #53 run 39212143946 pass
- [x] ISC-4: No doc or prompt references a script that does not exist (probe: every `scripts/*.py` named in the scan prompt (now `.claude/skills/daily-scan/SKILL.md`) exists; `rg --hidden generate_skills` → 0). — 🧹 CLASS-SWEEP: generate_skills refs — 9 via `rg --hidden` in 6 files (first pass missed `.claude/`; caught by code review); 9 fixed
- [x] ISC-5: The render workflow passes on main after merge (probe: `gh run list --workflow update.yml` latest = success). — run 39212192388 success, first green since 2026-09-21
- [x] Anti ISC-A1: Phase 0 does not publish an emptied site — every pool entry is older than `max_age_days`, so a re-render now would prune the whole briefing (probe: `docs/index.html` findings count unchanged by this PR). — `git diff 2111d67 HEAD -- docs data` = 0 files

### F1 · Phase 1 — one entrypoint, cloud + local (after: ISC-5)
Why: the run must happen without a human or a Windows box.

- [x] ISC-6: No Windows/WSL scan configuration remains in the repo (probe: no `*.ps1`, no `wsl`/`Agent Reach` references outside history). — 🧹 CLASS-SWEEP: Windows/WSL/Agent Reach/X-ingest refs — 18 files via `rg -i --hidden`; 3 deleted, 15 edited; left by design: findings text, `data/backlog.md` idea lines (Rohan's text), and the `.agent-reach/` ignore line (keeps leftover cookies unstageable)
- [ ] ISC-7: One cloud routine run and one local `claude -p` run each open a scan PR of the same shape. — built (`/daily-scan` + `run_scan.sh`, branch `claude/scan-<date>-<runner>`); BLOCKED on Rohan: both runs spend his subscription and need `budget.monthly_cap_usd` set
- [x] ISC-8: A run that finds no credit budget left exits before any LLM work and says so. — `tests/test_run_scan.py` (no cap / month spent → SCAN_SKIP, no ingest) + `tests/test_budget.py`; mutation-checked. In the cloud the session boot and reading the skill still cost a few thousand tokens before `pre` runs.
- [x] ISC-9: A failed run opens a GitHub issue. — live: `run_scan.sh fail` opened #60 (label scan-failure), a second failure commented on it; probe issue closed
- [x] ISC-10: The credits question is answered and recorded here with sources: can a cloud routine read the remaining credit balance or be limited to credits only, and how is per-run token usage measured? (probe: Decisions row citing the docs; ISC-8's guard built on the answer). — Decisions 2026-10-19 (routines.md L389/L403, headless.md L121)
- [ ] ISC-11: (BLOCKED on Rohan: approve creating the routine + its Custom environment) The cloud routine is created only after ISC-8 holds, and is reported to Rohan before its first scheduled run (probe: routine listed via `/schedule list`; creation PR/Log row dated after ISC-8).
- [x] ISC-12: An issue exists for X/Twitter ingest as a future local-only runner (probe: `gh issue list`). — #57
- [x] ISC-13: The render job opens its PR when it has drift (probe: the open-PR check uses `gh pr list --state open --head`; a dispatch run with drift opens one). — #55 via `scripts/ensure_pr.sh` (all 3 call sites); run 39213841133 opened #56, run 39214161882 reused it; pytest check-run green on #56 head 23fd86e
- [ ] Anti ISC-A2: No F1 change merges without `/security-review`, `/code-review` and a green Tests check (probe: each PR's checks + review notes).

Handoff: Rohan still has to delete the old Windows scheduled task; note it, never block on it. Commit attribution per harness settings. Every change lands as branch + PR.

## Not yet specified

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

- 2026-10-19 (ISC-10, from code.claude.com/docs/en/routines.md § Usage and limits, read this session): routines "draw down subscription usage the same way interactive sessions do"; usage credits only take over as "metered overage" once the subscription limit is hit, and "without usage credits, additional runs are rejected". So cloud runs spend Rohan's subscription allowance FIRST, not granted credits. No documented way for a run to read its remaining balance or its own token use; the only aggregate view is claude.ai/settings/usage. Local `claude -p --output-format json` reports `total_cost_usd` (headless.md). ISC-8's guard therefore takes the plan's "no" branch: a repo budget ledger plus a per-run story cap, with per-story cost measured locally and applied to cloud story counts.
- 2026-10-19: code review on #55 (6 findings) dispositioned. Adopted: sibling `gh pr view` sites in source-scout.yml + research-scan skill (one helper, `scripts/ensure_pr.sh`); Tests dispatch for GITHUB_TOKEN-made PRs; numeric guard on `gh pr list` output; drift check scoped to staged paths (pre-existing bug); progress counter. Lesson: ISC-13's first pass fixed one file without the `rg 'gh pr view'` sweep.

- 2026-10-19: code review on the ISC-6 commit (#58→#59, 8 findings) dispositioned. Adopted: add-source skill's burner/harvest promise, AGENTS "scans X/Twitter" line, the acceptEdits bullet restated as an entrypoint requirement plus the stall fix, `.agent-reach/` ignore restored, CONTRIBUTING x_account example marked not-harvested, skills say "not batch-ingested; ad-hoc add.py works". Deferred to the entrypoint PR: orphaned `scripts/daily_scan_prompt.md` (becomes the /daily-scan skill). Rebutted: ISC-6 "probe fails" — the remaining hits are data and Rohan's backlog ideas, not scan configuration; `DISCOVERED_VIA=twitter` stays because ad-hoc x.com adds still use it.
- 2026-10-19 (cloud-environments.md § GitHub proxy, read this session): in cloud sessions `gh pr` and `gh issue` get 403 (the proxy blocks GraphQL); REST via `gh api repos/...` works. So `ensure_pr.sh` and the failure alert (ISC-9) must use `gh api`, not `gh pr`/`gh issue`.

- 2026-10-19: entrypoint design. The budget ledger lives on its own `budget-ledger` branch, written with git plumbing, so a run's spend counts before its scan PR merges (Phase 4 isn't live yet). Each run's cost is bounded by `max_stories_per_run` × measured per-story cost. The first local run calibrates it; cloud runs refuse until a calibration exists. The Mac fallback is idle on days a cloud ledger row exists. The cap ships `null` (every run skips) so spending starts only when Rohan sets it.

## Verification

## Remaining Work

- [ ] Rohan, to unblock ISC-7/11: (1) merge #59 then the entrypoint PR; (2) set `budget.monthly_cap_usd` in config.yaml; (3) run one local calibration scan: `scripts/run_scan_local.sh` (or `scripts/install_launchd.sh` for daily); (4) approve creating the cloud routine: prompt `/daily-scan`, this repo, daily, Custom network = `python scripts/allowlist.py` + default packages, setup script `pip install -r requirements.txt`; (5) delete the old Windows scheduled task.
- [ ] Unverified until the first cloud run: the proxy remote URL parses in `repo_slug`; `python` resolves in the VM; the routine loads the project's `/daily-scan` skill; pushes to `budget-ledger` pass the proxy.

- [ ] Repo-wide lint pass (main has 19 ruff errors and 26 black-unformatted files), then add ruff + black to `tests.yml`. Kept out of the Phase 0 PR so the clock fix stays reviewable.
- [ ] Bot PRs show no checks in their PR checks list: a workflow_dispatch check run lands on the head commit (green on #56) but GitHub doesn't roll it into the PR, and the bot-push `pull_request` run waits at `action_required`. Harmless while main requires no checks; Phase 4 auto-merge needs a GitHub App or fine-grained PAT token for bot PRs (Rohan: create the secret).
- [ ] Render PR #56 prunes every pool entry (all older than 31 days) to an empty briefing. Do not merge it; Phase 1's first scan supplies fresh content.
