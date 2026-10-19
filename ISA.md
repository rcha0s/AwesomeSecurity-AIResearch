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
- [x] ISC-8: A run that finds no credit budget left exits before any LLM work and says so. — `tests/test_run_scan.py` (no cap → SCAN_SKIP before ingest; working-tree config and a tampered local ledger can't open it; reserve recorded before ingest) + `tests/test_budget.py`; mutation-checked. In the cloud the session boot and reading the skill still cost a few thousand tokens before `pre` runs.
- [x] ISC-9: A failed run opens a GitHub issue. — live: `run_scan.sh fail` opened #60 (label scan-failure), a second failure commented on it; probe issue closed
- [x] ISC-10: The credits question is answered and recorded here with sources: can a cloud routine read the remaining credit balance or be limited to credits only, and how is per-run token usage measured? (probe: Decisions row citing the docs; ISC-8's guard built on the answer). — Decisions 2026-10-19 (routines.md L389/L403, headless.md L121)
- [ ] ISC-11: (BLOCKED on Rohan: approve creating the routine + its Custom environment) The cloud routine is created only after ISC-8 holds, and is reported to Rohan before its first scheduled run (probe: routine listed via `/schedule list`; creation PR/Log row dated after ISC-8).
- [x] ISC-12: An issue exists for X/Twitter ingest as a future local-only runner (probe: `gh issue list`). — #57
- [x] ISC-13: The render job opens its PR when it has drift (probe: the open-PR check uses `gh pr list --state open --head`; a dispatch run with drift opens one). — #55 via `scripts/ensure_pr.sh` (all 3 call sites); run 39213841133 opened #56, run 39214161882 reused it; pytest check-run green on #56 head 23fd86e
- [x] Anti ISC-A2: No F1 change merges without `/security-review`, `/code-review` and a green Tests check (probe: each PR's checks + review notes). — #55, #59, #61: `/security-review` + `/code-review` dispositioned in Decisions, Tests green at merge

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

- 2026-10-19: #61 reviews dispositioned. Security (3): ADOPTED all. (1) Local `claude -p` containment: reads blocked outside the repo plus secret-dir denies, edits only `data/`, exact per-script Bash rules, no curl/git/gh, and `fetch_raw.py` fetches only a staged candidate's own URL. (2) The alert posts no log text, and the PR body passes `scrub.py`. (3) Spend settings come from `origin/main`, ledger rows are appended to a fresh remote copy, and rows are validated (fail closed). Code review (10): ADOPTED 9: the `git add` of ignored files (reproduced, now tested), stale-ledger overwrite, failed and zero-story runs going unrecorded (reserve-first; local `actual` always recorded), the uncalibrated no-ceiling run, same-day repeats (one scan per UTC day), the swallowed label error, SCAN_READY parsing. PARTIAL: a missing `analysis_out.json` reads as 0 stories, but the ceiling is already reserved, so only a hijacked model can exceed the cap. Residual: in the cloud the model has unrestricted Bash in its VM. The VM holds no readable secrets, but a fully hijacked cloud run could forge a ledger push, so the ledger branch should block force pushes.

- 2026-10-19: #61 security re-review of the fix (5 findings), all ADOPTED. The deeper fix is structural: on the Mac the wrapper, not the model, runs check → pre → analysis → post → actual. (1) `acceptEdits` approved edits anywhere (e.g. `.venv` .pth → code execution), so the session now runs `dontAsk` with edits only in `data/` and denies for `.venv`, tests, configs and agent docs. (2) `fetch_raw` took URLs from model-editable `candidates.json`; it now reads a snapshot `pre` writes. (3) The model could re-run `pre` and suppress the cost record; phases are off its allowlist and the wrapper records `actual` on every outcome. (4) No hard per-run cap: `--max-budget-usd` = 80% of the reservation plus `--max-turns`, and calibration uses the worst per-story run so padding can't lower it. (5) Unscrubbed commits: data/ is staged tracked-only and the staged diff passes `scrub.py --diff` before push. Also found while building: the repo's committed `.claude/settings.json` allows `aws ssm get-parameter`, Drive, Slack and internal MCP tools. Those would merge into the scan session, so the local run loads `--setting-sources local` with no MCP servers. That file has been public since #14 (2026-08-01); Rohan to review.
- 2026-10-19: #61 final security pass (3 findings), all ADOPTED. (1) `verify_citations.source_text_for` read `ROOT / raw_path`, and an absolute model-written path escaped ROOT (a grounding-score oracle for files outside the repo); now `common.raw_file` resolves only inside `data/_raw/`. (2) Its re-fetch hit any model-written URL; now `common.fetch_readable` refuses unstaged URLs under `SCAN_LOCKED=1`, which only the model's session gets. Both are mutation-checked. (3) `--setting-sources local` doesn't load project skills, so the wrapper passes the skill via `--append-system-prompt-file`. Verdicts after the fixes: spend bound (b) holds, publish-scrub (c) holds, local containment (a) fixed as reviewed. Python-level reads/writes aren't covered by Claude Code's Read/Edit rules (permissions.md), so every allowlisted script is part of the boundary: adding one to ALLOWED_TOOLS needs the same review.
- 2026-10-19: final `/code-review` of #61 (10 findings), all ADOPTED. (1) The same-day rule blocked the Mac fallback after a failed cloud run: `post` now writes a `done` row, a finished day blocks both runners, and a runner only skips its own failed day. (2) A failed local run left a dirty tree that blocked every later run: the Mac scan now runs in its own worktree, reset to origin/main and cleaned each run. (3) `guard || rc` turned off errexit, so a failed ledger fetch could read as GO: every git step checks itself, and budget.py refuses a missing ledger file. (4) A retry after a lost race skipped the re-check: check and reserve now share one retry loop. (5) Several merges could pass the story cap: `scan_count.py` counts entries new since main. (6) A stale `analysis_out.json` survived into the next run: `pre` clears it. (7) Import order. (8) Under the scan lock, a source that can't be read now counts as ungrounded (supersedes the curation note in Remaining Work for scan runs). (9) The double alert on a `pre` failure. (10) The session limits moved into config (`budget.session_cap_fraction`, `limits.max_turns`), read from origin/main.
- 2026-10-19: verification of the final fixes confirmed all 10, and found that fix 8 introduced a regression: re-grounding the pools mid-scan would have pushed every published entry out of the curated view, because old entries' raw text isn't staged and their URLs sit outside the lock. Fail-closed now applies only to entries not on origin/main; published entries keep their stored grounding (`common.main_entry_ids`, regression-tested). Also adopted: `git worktree prune` before re-adding a deleted worktree, and the local log moved out of the worktree so the next run's clean doesn't erase it. Residual: a tampered entry that reuses a published entry's id is judged as published. The last delta was verified by tests only (427 passed), with no separate review, because nothing runs until Rohan opens the budget.
- 2026-10-19: residuals, stated plainly. The CLOUD routine has none of the local containment: the model has unrestricted Bash in its VM, no `--max-budget-usd` exists for routines, and its spend is charged at the estimated ceiling, not measured. The VM holds no readable secrets (the GitHub proxy injects credentials). The scrubbers catch known token shapes and exact env values, not encoded secrets.

## Verification

## Remaining Work

- [ ] Rohan, to unblock ISC-7/11: (1) merge #59 then the entrypoint PR; (2) set `budget.monthly_cap_usd` and `budget.uncalibrated_run_usd` in config.yaml, and add a ruleset blocking force-push/deletion on `budget-ledger`; (3) run one local calibration scan: `scripts/run_scan_local.sh` (or `scripts/install_launchd.sh` for daily); (4) approve creating the cloud routine: prompt `/daily-scan`, this repo, daily, Custom network = `python scripts/allowlist.py` + default packages, setup script `pip install -r requirements.txt`; (5) delete the old Windows scheduled task; (6) review the public `.claude/settings.json` (internal tool names + broad allows, committed in #14).
- [ ] Unverified until the first cloud run: the proxy remote URL parses in `repo_slug`; `python` resolves in the VM; the routine loads the project's `/daily-scan` skill; pushes to `budget-ledger` pass the proxy.

- [ ] Repo-wide lint pass (main has 19 ruff errors and 26 black-unformatted files; one is real: `tests/test_ingest.py` defines `test_classify_domain_does_not_false_positive_on_bare_hyperlinks` twice, so the first copy never runs), then add ruff + black to `tests.yml`. Kept out of the Phase 0 PR so the clock fix stays reviewable.
- [ ] Bot PRs show no checks in their PR checks list: a workflow_dispatch check run lands on the head commit (green on #56) but GitHub doesn't roll it into the PR, and the bot-push `pull_request` run waits at `action_required`. Harmless while main requires no checks; Phase 4 auto-merge needs a GitHub App or fine-grained PAT token for bot PRs (Rohan: create the secret).
- [ ] Render PR #56 prunes every pool entry (all older than 31 days) to an empty briefing. Do not merge it; Phase 1's first scan supplies fresh content.
