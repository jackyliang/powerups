---
name: update-docs
description: Invoke after completing a feature to sync documentation for the current branch's changes. Updates local/project docs by default. Use /update-docs --public to also include public skills/plugins and downstream project docs.
---

# Update Docs

## Overview

After shipping a feature, documentation drifts. This skill finds what's stale **for the current branch's changes** and updates it.

## Scope Modes

| Mode | What it covers | When to use |
|------|---------------|-------------|
| **Default** (no flags) | Local project docs only, scoped to current branch changes | After completing a feature on a branch |
| **`--public`** | Local docs + public skills/plugins + downstream project docs | When changes affect APIs that external agents/projects consume |

### What counts as "local" vs "public"

- **Local docs** — files in the current repo that only this project's developers see:
  - `CLAUDE.md` — project instructions for Claude Code
  - `README.md` — project readme
  - `docs/` — in-repo guides
  - `.env.example` — env var reference
  - `plans/` — plan files with outdated status

- **Public docs** — files in other repos that external agents or projects consume:
  - Public skill plugins (sibling directories with skill files) — other agents read these to integrate
  - Downstream project docs — other projects that reference this one
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

### Step 2: Identify Doc Locations

Spawn an `Explore` subagent to find relevant doc files. **Start by reading the project's CLAUDE.md** — look for a "Documentation Locations" section that declares where this project's docs live, including cross-repo locations. If it exists, use it as the authoritative list. If not, discover locations manually:

**Always check (local):**
1. **CLAUDE.md** — project instructions (look for a doc locations section)
2. **README.md** — project readme
3. **`docs/`** — in-repo guides
4. **`.env.example`** — env var reference

**Only if `--public`:**
5. **Public skills/plugins** — sibling directories with skill files referenced in CLAUDE.md
6. **Downstream project docs** — other projects that integrate with this one, referenced in CLAUDE.md
7. **Integration guides** — shared docs that cover cross-repo flows, referenced in CLAUDE.md

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

- **Default scope is local + branch changes only.** Don't touch public/downstream docs unless asked.
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
| Downstream integration notes | Upstream API changed, downstream docs stale | Use `--public` flag to catch |
| Scattered integration docs | Each repo partially explains the same flow | Look for the same webhook/API/flow described in 2+ places |
