---
name: update-docs
description: Invoke after completing a feature to sync documentation for the current branch's changes. Updates local/project docs by default. Use /update-docs --full for a complete project scan, or /update-docs --public to include public skills/plugins.
---

# Update Docs

## Overview

After shipping a feature, documentation drifts. This skill finds what's stale **for the current branch's changes** and updates it.

## Scope Modes

| Mode | What it covers | When to use |
|------|---------------|-------------|
| **Default** (no flags) | Local project docs only, scoped to current branch changes | After completing a feature on a branch |
| **`--public`** | Local docs + public skills/plugins + downstream project docs | When changes affect APIs that external agents/projects consume |
| **`--full`** | Complete scan of all docs regardless of branch changes | Periodic cleanup, rarely needed |

### What counts as "local" vs "public"

- **Local docs** — files in the current repo that only this project's developers see:
  - `CLAUDE.md` — project instructions for Claude Code
  - `README.md` — project readme
  - `docs/` — in-repo guides
  - `.env.example` — env var reference
  - `plans/` — plan files with outdated status

- **Public docs** — files in other repos that external agents or projects consume:
  - Public skill plugins (e.g., `../sync-hq-skills/`) — other agents read these to integrate
  - Downstream project docs (e.g., `../answerhq/chat-ui/CLAUDE.md`) — other projects that reference this one
  - Any sibling repo referenced in CLAUDE.md

**Default behavior: local only.** Public docs are not touched unless `--public` or `--full` is specified.

## How It Works

### Step 1: Discover What Changed on This Branch

Spawn an `Explore` subagent to understand the current branch's changes:

1. **Read git diff** — `git diff main...HEAD --stat` to see what files changed on this branch
2. **Categorize changes** by type:
   - **API changes** — new/modified/removed endpoints, request/response format changes
   - **Behavior changes** — different defaults, new features, removed features
   - **Config changes** — new env vars, changed settings
   - **Architecture changes** — new services, new modules, renamed files
   - **Model/schema changes** — new columns, new tables, changed fields

Return a concise summary of what changed and what categories apply.

**If `--full` mode:** Skip git diff. Scan the entire codebase against all docs.

### Step 2: Identify Doc Locations

Spawn an `Explore` subagent to find relevant doc files:

**Always check (local):**
1. **CLAUDE.md** — project instructions
2. **README.md** — project readme
3. **`docs/`** — in-repo guides
4. **`.env.example`** — env var reference

**Only if `--public` or `--full`:**
5. **Public skills/plugins** — sibling directories with skill files (e.g., `../sync-hq-skills/`)
6. **Downstream project docs** — other projects that integrate with this one (e.g., `../answerhq/chat-ui/CLAUDE.md`)

The subagent should return the list of doc files and what each covers.

### Step 3: Diff Each Doc Against Reality

For each doc file, spawn subagents (in parallel where possible) to:

1. **Read the doc file**
2. **Compare against the branch's changes** — are the described APIs, defaults, patterns, env vars, and behaviors still accurate given what changed?
3. **Flag stale content** — list specific lines/sections that are wrong or outdated
4. **Propose updates** — concrete edits, not vague suggestions

Return findings as a checklist:
```
- [ ] CLAUDE.md line 45: says interval_minutes defaults to 5, should be 60
- [ ] README.md: still references manual schedule setup, should mention auto-scheduling
- [x] docs/new-connector-guide.md: already up to date
```

### Step 4: Clarify With the User

Before touching any docs, use `AskUserQuestion` to clarify:

- **Scope**: "I found 3 stale doc files. Want me to update all of them, or just specific ones?"
- **Audience**: "The README describes this feature for external developers. Should the updated docs target the same audience, or has that changed?"
- **Depth**: "The API reference is missing the new webhook endpoint. Should I add a full description with examples, or just a one-liner?"
- **Tone/framing**: "The old docs describe polling as the primary sync mechanism. Should the updated docs frame webhooks as the primary and polling as a fallback, or present them as equals?"
- **What to remove**: "The old recipes show manual schedule setup. Should I remove those entirely, or keep them as an 'advanced override' section?"

**Don't assume you know how the user wants their docs written.** Ask.

### Step 5: Apply Updates

After getting user direction:
- Edit each file with the proposed changes
- Commit per-repo (don't mix commits across repos)
- Use commit message: `docs: update for [feature name]`

### Step 6: Verify

After applying updates:
- Grep for obviously stale terms across updated doc files (old endpoint names, old defaults, removed features)
- Confirm no doc file references something that no longer exists
- Report any remaining issues

## What to Check in Each Doc Type

### CLAUDE.md
- Env vars table: any new vars? Any removed?
- Project structure: any new modules or files?
- Key patterns: any changed conventions?
- Skills table: any new skills or changed "when to use"?
- Service IDs, ports, URLs: still correct?

### README.md
- Setup instructions: still work?
- API examples: still valid?
- Feature descriptions: still accurate?
- Dependencies: any added or removed?

### In-Repo Guides (`docs/`)
- Implementation guides: still match current code patterns?
- Reference tables: still accurate (e.g., provider support matrix)?

### Public Skills/Plugins (only with `--public` or `--full`)
- API reference: endpoints, request/response formats, status codes
- Workflow guides: step-by-step instructions still valid?
- Recipes: example code still works?
- Default values: intervals, flags, settings

### Downstream Project Docs (only with `--public` or `--full`)
- Integration sections: still accurate?
- API URLs and env vars: still correct?
- Behavior descriptions: match current implementation?

## Rules

- **Default scope is local + branch changes only.** Don't touch public/downstream docs unless asked.
- **All investigation in subagents.** Reading docs consumes context. Subagents read and return concise diffs.
- **Ask before editing.** Show the user what's stale and get approval before making changes.
- **Ask about framing and depth.** Use `AskUserQuestion` to clarify scope, audience, tone, and what to remove vs. keep.
- **Commit per repo.** Don't mix changes across repos in one commit.
- **Don't add docs that don't exist.** This skill updates existing docs, not creates new ones. If a doc is missing entirely, flag it and ask the user if they want it created.

## Common Drift Patterns

| What drifts | Why | How to catch |
|------------|-----|-------------|
| API defaults (interval_minutes, schedule_enabled) | Changed in code, not in docs | Grep docs for old default values |
| Endpoint additions | New endpoint added, docs not updated | Compare router files against API reference |
| Removed features | Code deleted, docs still reference it | Grep docs for removed function/endpoint names |
| Env vars | New var added to config.py but not to CLAUDE.md or .env.example | Compare config.py against env var tables |
| Downstream integration notes | Upstream API changed, downstream docs stale | Only caught with `--public` flag |
