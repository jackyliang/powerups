---
name: drift-audit
description: Reconcile shipped code with the plan in both directions — additive drift (unplanned work that landed) and subtractive drift (dead files, stale TODOs, completed deferred items). Run as part of PDD's post-completion audit, before /simplify.
---

# Drift Audit

## Overview

Plans get written before the work. Reality happens during. By the time the PR is open, two kinds of drift have set in:

- **Additive drift** — things that got built but were never in the plan. New widgets a user asked for mid-build, dependencies you had to add, heuristics you layered on, bug fixes worth recording. The PR description and CHANGELOG carry some of this for external readers; the plan file, which is supposed to be the historical record for *future agents*, loses it.
- **Subtractive drift** — things that should be gone but aren't. A component file you replaced but didn't delete. A redirect stub for a URL nobody bookmarks anymore. A "Post-MVP" section in the plan listing items the new launch milestone now covers. A TODO comment referencing a feature that shipped. A feature flag that's permanently on. Six months later these stragglers look like maintained code and nobody dares delete them.

Run this audit between marking the last milestone done and step 1 of the post-completion audit. It produces two outputs: a new section in the plan file documenting additive drift, and a list of subtractive cleanups to apply.

## When to Use

- **Always**, as part of the post-completion audit for any feature that used `powerups:plan-driven-development`. Run before `/simplify` so the cleanup is informed by both directions of drift.
- For PDD **lightweight mode** (no plan file): run a slimmed-down version — skip the plan-file edit, but still do the subtractive sweep on the code.
- For pure refactors with no plan: skip the additive pass, do the subtractive sweep.

## How to Run

### Step 1 — Get both diffs

Spawn an `Explore` (or `general-purpose`) subagent to run two passes against the branch. Plan files are large; reading them in the main context wastes tokens. The subagent should return a structured list, not raw diffs.

Subagent prompt template:

```
This branch finished implementing the feature described in plans/v{N}-{description}.md.
I need a drift audit in two parts.

PART A — ADDITIVE drift. List everything that landed in the code but isn't
described in the plan's Design / Architecture or Milestones. Group by:

1. New endpoints / widgets / API surfaces (paths + brief description)
2. New data model additions (tables, columns, indexes, RPCs, views)
3. New dependencies (package.json, requirements.txt, or any other manifest)
4. Heuristics or quality work not in the original spec (filters, ranking,
   dedup, validation)
5. Frontend infrastructure changes (UX patterns, component conventions,
   layout decisions)
6. Backend infrastructure changes (model bumps, helper modules, gating,
   migrations)
7. Bug fixes or gotchas worth recording for the next person who touches
   this code
8. Operational milestones completed during build (backfills run, data
   seeded, etc.)

PART B — SUBTRACTIVE drift / loose ends. List what should be gone but isn't:

1. Dead code — component files, modules, or functions left orphaned after
   a replacement landed. Look for files no other module imports.
2. Stale redirect stubs — URL aliases for paths that no longer have
   bookmarks worth keeping (e.g. an internal-only path the team migrated
   off two releases ago).
3. Completed-but-still-listed deferred items — "Post-MVP" / "Open
   decisions" / TODO sections in the plan file enumerating things that
   actually shipped. The plan should reflect reality.
4. Orphaned feature flags — flags that are now permanently on or
   permanently off; the conditional branches should collapse.
5. TODO comments / FIXME comments referencing things that have shipped.
6. Unused imports introduced during refactor pivots.
7. Deprecated database objects — tables/columns/views from a previous
   approach that the final implementation no longer uses.
8. Tests or fixtures that exercise the old behavior.

For each item, include: file path + line number (where applicable), brief
description, and whether you're confident it's truly dead (high / medium /
low confidence). Low-confidence ones go on a "verify before deleting" list.

Be specific. Skip cosmetic differences. Return under 1200 words total.
```

If a category is empty in either part, the subagent should say so explicitly — don't pad.

### Step 2 — Apply the subtractive cleanups

Walk Part B with the user:
- **High-confidence dead code, orphaned imports, completed TODOs** — delete in this commit.
- **Stale redirect stubs, orphaned feature flags** — confirm with the user before deleting (they may have product context like analytics bookmarks).
- **Completed "Post-MVP" / "Open decisions" items** — edit the plan file to remove or move them.
- **Deprecated DB objects** — flag for a separate migration; don't drop in the same PR unless the user signs off.

Commit:

```
git commit -m "chore(plan-drift): remove stragglers from {feature-name}"
```

### Step 3 — Document the additive drift in the plan

Insert a `## What changed from the initial plan` section between the **Context** section and the **Design / Architecture** section of the plan file. Use this structure:

```markdown
## What changed from the initial plan

The initial v{N} plan covered {one-line summary of original scope}. During
implementation the scope grew. This section is the diff between the v{N}
plan as originally written and what actually landed.

### New widgets / endpoints (not in original plan)

| Added | Where in code | Why |
|---|---|---|
| ... | ... | user-requested mid-build / required for X / etc. |

### Data model additions (not in original plan)

- `{table.column}` — one line on why it was needed.

### Dependencies added

- `{package@version}` — one line on what it's for.

### Quality / heuristics not in the original spec

- **{Heuristic name}** — what it does and what edge case it closes.

### Frontend infrastructure changes

- **{Pattern name}** — what it is, where it lives.

### Backend infrastructure changes

- **{Pattern name}** — what it is, where it lives.

### Bug fixes worth recording for next time

- **{Bug summary}.** Root cause + fix.

### Operational milestones already completed

- {Backfill / seed / migration run in prod, with counts}.
```

Skip categories that are empty. If only 3 of 8 categories have entries, the section is short — that's fine.

### Step 4 — Commit the plan update

```
git add plans/v{N}-{description}.md
git commit -m "docs(plan): record drift on v{N}"
```

### Step 5 — Reference in PR

In the PR body, link to the drift section: *"See `plans/v{N}.md#what-changed-from-the-initial-plan` for the full diff between the original plan and what shipped."* Saves reviewers from reverse-engineering scope creep.

## Worked example

A real v20 audit found ~30 additive items (7 unplanned endpoints/widgets, 3 data model additions, 3 new dependencies, heuristics, infra changes, bug fixes, ops milestones) and ~5 subtractive items (two components replaced by a new Insights page but never deleted, an orphaned `GeoMapCard.tsx` from a mid-build pivot, a completed Post-MVP item still listed as deferred, a resolved "Open decision" still listed as open). Without the audit, the plan would have looked like the original 9-milestone spec was what shipped, and three orphan files would have stayed in the repo for the next dev to wonder about.

## How this hooks into PDD

`powerups:plan-driven-development` invokes this skill during its post-completion audit — PDD owns the full sequence. The one ordering rule that matters here: **drift-audit runs before `/simplify`**, because drift informs everything downstream — `/simplify` shouldn't refactor code that's about to be deleted, the CHANGELOG should reflect the shipped product, and `update-docs` needs to know which docs reference paths that just got cleaned up.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping drift because "the plan was followed closely" | Run it anyway — almost every shipped feature has invisible drift on both axes. The 5-minute audit beats reading every commit six months later. |
| Pasting a giant raw `git log` into the plan | The drift section should be a curated narrative grouped by category, not a commit dump. The subagent's job is to summarize, not list. |
| Listing items already in the plan | The audit is for what's *additive*. A milestone task that grew slightly mid-build isn't drift — only net-new things or substituted approaches count. |
| Deleting low-confidence orphan code without confirming | Subtractive drift gets confirmed before deletion. Some "dead-looking" code is actually referenced by tests, cron, or deploy scripts. |
| Treating drift as a "lessons learned" diary | Drift documents what changed in the *built artifact*. It's not a retrospective on what went well or badly. Save process feedback for elsewhere. |
| Burying the additive section at the bottom of the plan | Put it right after Context so anyone reading the plan top-down learns the diff before reading the (possibly stale) Design section. |
| Writing prose paragraphs instead of tables/bullets | Drift sections get scanned, not read. Use tables for the dense categories (endpoints, data model, deps), bullets for the rest. |
| Skipping the subtractive sweep because "/simplify handles it" | `/simplify` catches code-quality issues; it doesn't reliably find every orphaned-file-after-a-replacement or every completed-but-still-listed Post-MVP entry. The subagent prompt above is targeted at exactly those cases. |
| Running drift after the PR is open | Then the PR description can't reference it, and subtractive deletions land in follow-up commits that look unmotivated. Run drift first, then audit, then PR. |
