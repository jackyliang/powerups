---
name: update-docs
description: Invoke after completing a feature to sync all documentation — local docs, sibling repos, skill plugins, and downstream project docs. Scans everything by default.
---

# Update Docs

## Overview

After shipping a feature, documentation drifts. This skill finds what's stale and updates it — across ALL repos, not just the current one.

## When to Use

**Invoke this skill:**
- After completing a feature or milestone
- After merging a PR that changes APIs, behavior, or architecture
- When you suspect docs are stale
- Before creating a release or PR that touches public interfaces

**The user can invoke this directly with `/update-docs`.**

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

### Step 2: Identify ALL Doc Locations

Spawn an `Explore` subagent to discover every doc file that might need updating. **Scan everything — local and cross-repo.** The whole point of this skill is comprehensive coverage.

**Local docs (current repo):**
1. **CLAUDE.md** — project instructions, key files tables, env var sections
2. **README.md** — project readme
3. **`docs/`** — in-repo guides (glob for `docs/**/*.md`)
4. **`.env.example`** — env var reference
5. **`plans/`** — plan files with status tables or task checkboxes

**Sibling repos (always scan):**

Grep CLAUDE.md for `../` paths to find sibling repos. For EVERY sibling repo found:
6. **CLAUDE.md** — check for stale references to this project
7. **README.md** — check for stale API descriptions, ports, defaults
8. **Skill/plugin docs** — API references, recipes, guides, integration docs
9. **Any `docs/` directory** — in-repo guides in sibling repos

**This is not optional.** If CLAUDE.md references `../other-project/`, scan that project's docs too. Documentation drifts most at repo boundaries.

The subagent should return the list of ALL doc files found and what each covers.

### Step 3: Diff Each Doc Against Reality

For each doc file, spawn subagents (in parallel where possible) to:

1. **Read the doc file**
2. **Compare against the actual codebase** — are the described APIs, defaults, patterns, env vars, and behaviors still accurate?
3. **Flag stale content** — list specific lines/sections that are wrong or outdated
4. **Propose updates** — concrete edits, not vague suggestions

Return findings as a checklist:
```
- [ ] CLAUDE.md line 45: says interval_minutes defaults to 5, should be 60
- [ ] ../sibling-repo/api-reference.md: missing new webhook fields
- [ ] README.md: port 8000 should be 8001
- [x] docs/guide.md: already up to date
```

### Step 4: Clarify With the User

Before touching any docs, present the full checklist and use `AskUserQuestion` to clarify:

- **Scope**: "I found 6 stale doc files across 3 repos. Want me to update all of them, or just specific ones?"
- **Depth**: "The API reference is missing the new webhook fields. Should I add a full description with examples, or just add the fields?"
- **What to remove**: "The old recipes show outdated defaults. Should I remove those entirely, or update them?"

**Don't assume you know how the user wants their docs written.** Ask.

**Never silently skip a finding.** If a doc file is stale, present it to the user — even if you think the update is minor or optional. Let the user decide what to skip, not you.

### Step 5: Apply Updates

After getting user direction:
- Edit each file with the proposed changes
- Commit per-repo (don't mix commits across repos)
- Use commit message: `docs: update for [feature name]`

### Step 6: Verify

After applying updates:
- Grep for obviously stale terms across ALL doc files (old endpoint names, old defaults, removed features)
- Confirm no doc file references something that no longer exists
- Report any remaining issues

## What to Check in Each Doc Type

### CLAUDE.md
- Env vars table: any new vars? Any removed?
- Project structure: any new modules or files?
- Key patterns: any changed conventions?
- Key files table: function names still match code?
- Service IDs, ports, URLs: still correct?

### README.md
- Setup instructions: still work?
- API examples: still valid? Ports correct?
- Feature descriptions: still accurate?
- Dependencies: any added or removed?

### In-Repo Guides (`docs/`)
- Implementation guides: still match current code patterns?
- **Pipeline/flow descriptions**: if you added a new step to a pipeline (e.g., a new stage in a data processing flow), check that any docs listing those steps are updated. Numbered step lists go stale silently.
- Reference tables: still accurate (e.g., provider support matrix)?
- "How to add a new X" guides: do they still describe the full process, including any new automatic behaviors the developer should know about?

### Sibling Repo Skill/Plugin Docs
- API reference: endpoints, request/response formats, payload schemas
- Workflow guides: step-by-step instructions still valid?
- Recipes: example code still works? Default values correct?
- Integration guides: end-to-end flow still accurate?

### Plan Files
- Progress/status tables: do they reflect actual completion state?
- Task checkboxes: checked off for completed work?

## Reducing Doc Scatter

When multiple repos are involved in a feature (e.g., a service + its SDK, or two services that integrate), documentation naturally fragments. Each repo partially explains the integration, and none tells the full story. This is the most common source of confusion.

**The fix: single source of truth for cross-repo concerns.**

### The Pattern

1. **Pick one location** for the integration guide — typically a shared skills/docs repo, or the repo that orchestrates the integration.
2. **Write one document** that covers the full end-to-end flow: what each system owns, how they communicate, the data contract (payloads, schemas), and key files in each repo.
3. **Each repo's own docs (CLAUDE.md, README) just link to it** with a one-liner: "For how this integrates with X, see `../shared-docs/integration-guide.md`."
4. **Never partially explain the same integration in two places.** If you find two repos each describing half the story, recommend consolidating into one guide and replacing the other with a link.

### When to Flag Scatter

During Step 3 (diffing docs against reality), watch for:
- Two or more docs explaining the same cross-repo flow differently
- CLAUDE.md in repo A describing repo B's internals (and vice versa)
- Webhook/API contracts documented in the sender AND receiver with different details
- The same payload or schema described in multiple places

When you find this, **recommend consolidation** before making edits. Ask the user: "I found the X integration partially described in N places. Want me to consolidate into one guide and replace the others with links?"

### What Goes Where

| Doc type | Scope | Example |
|----------|-------|---------|
| **Integration guide** (shared) | End-to-end flow across repos, data contracts, what each system owns | "How Service A + Service B work together" |
| **CLAUDE.md** (per-repo) | How to work in THIS codebase — key files, commands, conventions | Links to integration guide for cross-repo context |
| **README.md** (per-repo) | What this repo IS, how to set it up, how to run it | Does not explain other repos |
| **API reference** (per-repo) | Endpoints, request/response formats for THIS service | Payload schemas for events this service sends |
| **Skill docs** (shared) | How to USE a service from another codebase | Recipes, workflow steps, troubleshooting |

## Rules

- **Scan everything.** Local docs AND all sibling repos. No opt-in flags. Comprehensive coverage is the whole point.
- **All investigation in subagents.** Reading docs consumes context. Subagents read and return concise diffs.
- **Ask before editing.** Show the user what's stale and get approval before making changes.
- **Ask about framing and depth.** Use `AskUserQuestion` to clarify scope, audience, tone, and what to remove vs. keep.
- **Commit per repo.** Don't mix changes across repos in one commit.
- **Don't add docs that don't exist.** This skill updates existing docs, not creates new ones. If a doc is missing entirely, flag it and ask the user if they want it created.
- **Flag scatter, don't perpetuate it.** If the same integration is partially documented in multiple places, recommend consolidation before adding more partial docs.

## Common Drift Patterns

| What drifts | Why | How to catch |
|------------|-----|-------------|
| API defaults (interval_minutes, schedule_enabled) | Changed in code, not in docs | Grep docs for old default values |
| Endpoint additions | New endpoint added, docs not updated | Compare router files against API reference |
| Removed features | Code deleted, docs still reference it | Grep docs for removed function/endpoint names |
| Env vars | New var added to config.py but not to CLAUDE.md or .env.example | Compare config.py against env var tables |
| Downstream integration notes | Upstream API changed, downstream docs stale | Scan sibling repos for stale references |
| Scattered integration docs | Each repo partially explains the same flow | Look for the same webhook/API/flow described in 2+ places |
| Ports and URLs | Changed in code, old values in docs/README | Grep all docs for port numbers and URLs |
