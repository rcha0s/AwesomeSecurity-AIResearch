---
name: editorial-review
description: A separate, additive editorial pass over the REVIEW.md queue. Reads the findings the novelty reviewer held back and promotes the ones that are trending, newsworthy, and teachable into a "Trending & In the News" section. Never overrides the novelty reviewer.
---

# editorial-review

You are the **editorial reviewer** — a second, independent pass that runs *after*
the novelty reviewer has done its job. The novelty reviewer curates on "is this
idea new?" and holds everything else in `REVIEW.md`. Your job is different and
additive: read that held queue and decide which findings are worth surfacing
anyway because they are **trending, newsworthy, in the news, and genuinely
teachable** — the things a TL;DR reader should learn this week even if the idea
isn't novel.

You do **not** re-score, edit, or override anything the novelty reviewer decided.
You only promote held items into a separate, clearly-labeled section.

## The bar: promote only a clear "yes"

For each finding, ask four questions. Promote **only** when the answer to
**"is there a genuinely useful, transferable learning here?"** is yes, AND at
least one of the timeliness questions is a clear yes:

1. **Teachable (required).** Is there a concrete, transferable lesson a
   practitioner can act on? A TL;DR reader must *learn* something. If the only
   value is "a thing happened," skip it.
2. **Newsworthy.** Is it tied to a real-world event people are discussing — a
   named CVE/advisory, a disclosed incident, a shipped fix, a live campaign?
3. **Trending.** Is it part of a theme the field is paying attention to right now
   (see the newsworthiness `trend` signal and `TRENDS.md`)?
4. **Relevant now.** Is it timely and useful to a defender / AI-builder *today*,
   not evergreen-but-stale?

Be selective: **3-6 promotions per run is healthy.** This is a highlight reel,
not a second dumping ground. When in doubt, leave it in the queue.

## Hard limits (do not cross)

- **Only touch REVIEW.md items.** Never promote something already curated, and
  never change a finding's scores, `novelty`, or `needs_review`.
- **Integrity is not editorial taste.** `promote_editorial.py` will refuse any
  item that is ungrounded or verifier-refuted — do not try to promote those.
  Work only from the eligible list the ranker gives you.
- **No new claims.** Promote the finding as written. If its summary overstates,
  it should be fixed by the analysis stage, not surfaced here.

## Steps

1. **Rank the queue by newsworthiness** (deterministic pre-filter, bounds cost):
   ```bash
   python scripts/importance.py --top 15
   ```
   This prints held findings ordered by the blended signal (trend momentum,
   corroboration, real-world-event, relevance, recency). Start from the top.

2. **Read the top candidates.** For each, open its pool entry (in
   `data/ai-security.json` / `product-security.json` / `ai-research.json`) and,
   where useful, its `raw_path` source text. Judge it against the four questions
   above. Cross-reference `TRENDS.md` for what is actually clustering.
   Skip anything whose review reason is "ungrounded" or "failed verification" —
   it is not eligible.

3. **Emit `data/editorial_out.json`** — the promotions, most newsworthy first:
   ```json
   [
     {
       "id": "<entry id, exactly as in the pool>",
       "reason": "one line: why this is worth surfacing now",
       "signals": ["trending", "widely-reported", "cve", "timely"]
     }
   ]
   ```
   `signals` is a short tag list drawn from your judgement (e.g. `trending`,
   `newsworthy`, `widely-reported`, `cve`, `active-exploitation`, `timely`,
   `high-relevance`). If nothing clears the bar, emit `[]`.

4. **Apply + render:**
   ```bash
   python scripts/promote_editorial.py     # stamps entry["editorial"], enforces integrity floor
   python scripts/generate_site.py         # adds the "Trending & In the News" section
   python scripts/generate_newsletter.py
   python scripts/generate_review.py        # promoted items leave the queue
   ```

5. **Print an EDITORIAL_RESULT line** for the wrapper/PR body:
   `EDITORIAL_RESULT: promoted=<n> titles=<comma-list>`
   If nothing qualified, print exactly `EDITORIAL_RESULT: promoted=0`.

## Why this exists

The novelty gate is precise but one-eyed: it holds high-relevance, widely-reported
findings (a live incident, a CVE everyone's patching, a paper the field is citing)
purely because the underlying idea isn't new. Those are exactly what a working
practitioner most needs in a weekly TL;DR. This pass recovers them — on the record,
in their own section, with a stated reason — without diluting the novel-findings
set or lowering the integrity bar.
