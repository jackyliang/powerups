---
name: change-log
description: Use after completing a feature or bug fix to log the change in CHANGELOG.md using plain, business-user-friendly language
---

# Change Log

## Overview

After every feature or bug fix is complete, add an entry to `CHANGELOG.md`. The log is written for business users, not developers — it powers the product updates blog. Use plain language that a non-technical person would understand.

## When to Use

- After completing a feature (invoked by `plan-driven-development` and `bug-fix` automatically)
- After any user-facing change ships
- Do NOT log internal refactors, test-only changes, or dev tooling updates

## Format

```markdown
# Change Log

## 2026-03-20
- You can now see exactly which articles were added, updated, or deleted after each sync

## 2026-03-18
- Fixed an issue where disconnecting a connector would sometimes leave behind stale data
```

## Rules

- **One entry per feature or fix.** One sentence. Two sentences max for small features. Up to three sentences for large features.
- **Use `simple-design-principles` language.** No jargon, no technical terms. Write what the user can now do or what got better, not what code changed.
- **Date format:** `YYYY-MM-DD`. Use today's date.
- **File location:** `CHANGELOG.md` at the project root. **Always search for an existing `CHANGELOG.md` first** (e.g., using Glob) before creating a new one — never create a duplicate.
- **Append new dates at the top** (most recent first), below the `# Change Log` heading.
- **Group entries under the same date** if multiple changes ship on the same day.
- **Don't log the same change twice.** If a feature spans multiple milestones, log it once when the full feature is complete.

## Language Examples

| Don't | Do |
|-------|-----|
| "Added `sync_run_changes` table and API endpoint" | "You can now see which articles changed after each sync" |
| "Fixed null pointer in webhook handler" | "Fixed an issue where syncs would sometimes fail silently" |
| "Refactored connector registry to use ABC pattern" | (Don't log — internal refactor, not user-facing) |
| "Implemented incremental reindexing with changed_records" | "Syncs are now faster — only changed articles are re-processed" |
