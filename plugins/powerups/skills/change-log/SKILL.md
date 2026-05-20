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

## Finding the existing CHANGELOG (do this BEFORE writing)

Creating a duplicate `CHANGELOG.md` is the most common failure mode of this skill. **You must exhaustively search for an existing one before creating a new file.** Run all of these steps in order and only fall through to the next if the previous turned up nothing:

1. **Check CLAUDE.md for an explicit path.** Grep the repo's CLAUDE.md files for `CHANGELOG` — project owners often pin the canonical path there (e.g., "the canonical changelog is at `CHANGELOG.md` at the repo root"). If CLAUDE.md names a path, use that path and skip the rest.

   ```bash
   grep -nH -i "changelog" CLAUDE.md ./**/CLAUDE.md 2>/dev/null
   ```

2. **Find the repo root, then look for `CHANGELOG.md` at the root.** Do not assume your current working directory is the root — skills are often invoked from a subdirectory (e.g., `chat-ui/`, `frontend/`, `apps/web/`).

   ```bash
   ROOT="$(git rev-parse --show-toplevel)"
   ls "$ROOT"/CHANGELOG.md 2>/dev/null
   ```

3. **Glob the entire repo for any `CHANGELOG.md`** (case variants included), excluding vendored dirs. If matches exist, the canonical one is almost always at the repo root — pick that one. If multiple non-vendored copies exist, **stop and ask the user** which is canonical; do not silently pick one or create a third.

   ```bash
   find "$ROOT" -iname "CHANGELOG*.md" \
     -not -path "*/node_modules/*" \
     -not -path "*/.next/*" \
     -not -path "*/.venv/*" \
     -not -path "*/venv/*" \
     -not -path "*/dist/*" \
     -not -path "*/build/*" \
     -not -path "*/.claude/*"
   ```

4. **Only if all of the above return nothing** may you create `CHANGELOG.md` at the repo root (`$ROOT/CHANGELOG.md`) with the `# Change Log` heading and today's entry. Never create it in a subdirectory like `chat-ui/CHANGELOG.md` or `frontend/CHANGELOG.md` — the root is the canonical location.

**Do not** create a new `CHANGELOG.md` just because the existing one isn't where you expected, or because your cwd is a subdirectory and you didn't find one there. A "missing" changelog almost always means you searched the wrong directory.

## Rules

- **One entry per feature or fix.** One sentence. Two sentences max for small features. Up to three sentences for large features.
- **Use `simple-design-principles` language.** No jargon, no technical terms. Write what the user can now do or what got better, not what code changed.
- **Date format:** `YYYY-MM-DD`. Use today's date.
- **File location:** `CHANGELOG.md` at the repo root. See "Finding the existing CHANGELOG" above — always search first, never create a duplicate.
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
