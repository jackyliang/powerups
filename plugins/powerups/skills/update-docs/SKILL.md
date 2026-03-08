---
name: update-docs
description: Invoke after completing a feature to sync all documentation — CLAUDE.md, README, public skills/plugins, and downstream project docs. Finds what's stale and updates it.
---

# Update Docs

## Overview

After shipping a feature, documentation drifts. CLAUDE.md references old patterns, READMEs describe removed endpoints, skill plugins advertise stale APIs, and downstream projects have outdated integration notes. This skill finds and fixes all of it.

## When to Use

**Invoke this skill:**
- After completing a feature or milestone
- After merging a PR that changes APIs, behavior, or architecture
- When you suspect docs are stale
- Before creating a release or PR that touches public interfaces

**The user can invoke this directly with `/update-docs`.**

## How It Works

### Step 1: Discover What Changed

Spawn an `Explore` subagent to understand the recent changes. The subagent should:

1. **Read git diff** — `git diff main...HEAD --stat` (or `git log --oneline -10`) to see what files changed
2. **Categorize changes** by type:
   - **API changes** — new/modified/removed endpoints, request/response format changes
   - **Behavior changes** — different defaults, new features, removed features
   - **Config changes** — new env vars, changed settings
   - **Architecture changes** — new services, new modules, renamed files
   - **Model/schema changes** — new columns, new tables, changed fields

Return a concise summary of what changed and what categories apply.

### Step 2: Identify All Doc Locations

Every project has documentation scattered across multiple locations. Spawn an `Explore` subagent to find them all:

1. **Project CLAUDE.md** — the main project instructions file
2. **README.md** — public-facing project documentation
3. **Public skills/plugins** — check for skill plugins installed in other projects that reference this project's API. Common patterns:
   - `../` sibling directories with skills (e.g., `../sync-hq-skills/`)
   - Plugin repos referenced in CLAUDE.md
4. **Downstream project docs** — other projects that integrate with this one. Check CLAUDE.md for references to sibling projects (e.g., `../answerhq/chat-ui/CLAUDE.md`)
5. **Plan files** — `plans/` directory may have outdated status or design notes
6. **In-repo guides** — `docs/` directory, implementation guides, connector guides

The subagent should return the list of doc files and what each covers.

### Step 3: Diff Each Doc Against Reality

For each doc file found in Step 2, spawn subagents (in parallel where possible) to:

1. **Read the doc file**
2. **Compare against the actual codebase** — are the described APIs, defaults, patterns, env vars, and behaviors still accurate?
3. **Flag stale content** — list specific lines/sections that are wrong or outdated
4. **Propose updates** — concrete edits, not vague suggestions

Return findings as a checklist:
```
- [ ] CLAUDE.md line 45: says interval_minutes defaults to 5, should be 60
- [ ] ../sync-hq-skills/api-reference.md: missing new POST /v1/webhooks/nango endpoint
- [ ] README.md: still references manual schedule setup, should mention auto-scheduling
- [x] ../answerhq/chat-ui/CLAUDE.md: already up to date
```

### Step 4: Clarify With the User

Before touching any docs, use `AskUserQuestion` to clarify:

- **Scope**: "I found 6 stale doc files. Want me to update all of them, or just specific ones?"
- **Audience**: "The README describes this feature for external developers. Should the updated docs target the same audience, or has that changed?"
- **Depth**: "The API reference is missing the new webhook endpoint. Should I add a full description with examples, or just a one-liner?"
- **Tone/framing**: "The old docs describe polling as the primary sync mechanism. Should the updated docs frame webhooks as the primary and polling as a fallback, or present them as equals?"
- **What to remove**: "The old recipes show manual schedule setup. Should I remove those entirely, or keep them as an 'advanced override' section?"
- **Cross-repo impact**: "This change affects the sync-hq-skills plugin that other agents read. Any specific way you want the new behavior described there?"

**Don't assume you know how the user wants their docs written.** The same feature can be documented very differently depending on who reads it and what they need. Ask.

### Step 5: Apply Updates

After getting user direction:
- Edit each file with the proposed changes
- Commit per-repo (don't mix commits across repos)
- Use commit message: `docs: update for [feature name]`

### Step 6: Verify

After applying updates:
- Grep for obviously stale terms across all doc files (old endpoint names, old defaults, removed features)
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

### Public Skills/Plugins
- API reference: endpoints, request/response formats, status codes
- Workflow guides: step-by-step instructions still valid?
- Recipes: example code still works?
- Default values: intervals, flags, settings

### Downstream Project Docs
- Integration sections: still accurate?
- API URLs and env vars: still correct?
- Behavior descriptions: match current implementation?

## Rules

- **Never skip a doc location.** If CLAUDE.md references a sibling project, check it.
- **All investigation in subagents.** Reading docs consumes context. Subagents read and return concise diffs.
- **Ask before editing.** Show the user what's stale and get approval before making changes.
- **Ask about framing and depth.** Don't assume how the user wants changes described. Use `AskUserQuestion` to clarify scope, audience, tone, and what to remove vs. keep.
- **Commit per repo.** Don't mix sync_hq and answerhq changes in one commit.
- **Don't add docs that don't exist.** This skill updates existing docs, not creates new ones. If a doc is missing entirely, flag it and ask the user if they want it created.

## Common Drift Patterns

| What drifts | Why | How to catch |
|------------|-----|-------------|
| API defaults (interval_minutes, schedule_enabled) | Changed in code, not in docs | Grep docs for old default values |
| Endpoint additions | New endpoint added, docs not updated | Compare router files against API reference |
| Removed features | Code deleted, docs still reference it | Grep docs for removed function/endpoint names |
| Env vars | New var added to config.py but not to CLAUDE.md or .env.example | Compare config.py against env var tables |
| Downstream integration notes | Upstream API changed, downstream docs stale | Check all CLAUDE.md files that reference this project |
