---
name: plan-driven-development
description: Use when starting a multi-milestone feature, resuming work after context loss, or unsure if a feature plan already exists
---

# Plan-Driven Development

## Overview

Large features get a versioned plan file in `plans/` that serves as the **single source of truth** — what's been done, what's in progress, and what's left. The plan persists across context windows so any agent (or agent team) can pick up where the last one left off.

**PDD builds on `best-practices`.** Everything in the `best-practices` skill applies here automatically — TDD, investigation, clarifying questions, DRY, branching, frontend-design for UI, update-docs when done. PDD adds planning infrastructure on top.

## When to Use

**Create a plan when:**
- Feature spans multiple milestones or will take more than one session
- Multiple files/modules need coordinated changes
- You need to track progress across context resets
- Multiple agents will work on different pieces in parallel

**Skip the plan when:**
- Single-file change, small bugfix, quick refactor — use `best-practices` directly instead
- Work fits in one session with no risk of context loss

**On every session start for feature work:**
- Spawn an `Explore` subagent to check `plans/` for an existing plan. Plan files are large and consume significant context — **never read them directly in the main conversation**. The subagent should read the plan and return a concise summary: current milestone, next unchecked task, any blockers, and key design decisions.
- If the subagent finds an active plan, use its summary to orient yourself. Only read specific sections of the plan directly if you need exact task wording or file paths.
- Update the progress summary table and check off completed tasks (these edits are small and fine in the main context).

## Plan Location & Naming

```
plans/
├── v0-initial-build.md
├── v1-auth-and-production-readiness.md        ← initial plan
├── v1-auth-and-production-readiness-r2.md     ← revised (approach changed)
├── v2-multi-provider-support.md
└── ...
```

**Naming:** `v{N}-{short-action-description}.md` (initial), `v{N}-{description}-r{R}.md` (revisions)
- `v{N}` — Sequential version number (check existing files for the next number)
- `{short-action-description}` — Lowercase, hyphens, action-oriented (e.g., `auth-and-production-readiness`, `multi-provider-support`)
- `-r{R}` — Revision suffix, appended when the plan undergoes a major change (r2, r3, etc.). The initial version has no suffix (implicitly r1).
- If `plans/` doesn't exist, create it

**Title inside the file** should match: `# v1-r2: Auth & Production Readiness (WorkOS)`

**When to create a revision (new file with `-r{R}` suffix):**
- Core technical approach changes (e.g., DIY JWT → WorkOS)
- Major scope added or removed (e.g., dropping a whole milestone)
- Architecture fundamentally shifts

**Do NOT create a revision for:**
- Checking off tasks (normal progress)
- Adding/removing small tasks
- Clarifying wording

Previous revision files stay in `plans/` as historical record — don't delete the original when creating a revision.

## Plan Structure

Every plan must have these sections:

### 1. Context
What problem this solves, why it's being built, key relationships and constraints. Written so an agent with zero prior context understands the full picture.

### 2. Design / Architecture
Data models, API endpoints, flow diagrams, key decisions and their rationale. Include enough detail that implementation doesn't require guessing.

### 3. Milestones with Task Checkboxes
The core of the plan. Each milestone is a logical chunk of work with:

```markdown
### Milestone N: Short Name
**Goal:** One sentence.

- [ ] Task 1 description
- [ ] Task 2 description
- [x] Task 3 (completed)

**Verification:**
- [ ] How to confirm this milestone is done
```

Rules:
- Tasks are concrete and actionable ("Create `sync_hq/auth/models.py`" not "Set up auth")
- Include file paths where relevant
- TDD: list test tasks before implementation tasks
- Check off tasks (`- [x]`) as they are completed
- Never remove completed tasks — they're the history

### 4. Progress Summary Table
Quick at-a-glance status at the bottom of the file:

```markdown
| Milestone | Status | Notes |
|-----------|--------|-------|
| 1. Name   | Done   |       |
| 2. Name   | In progress | Blocked on X |
| 3. Name   | Not started | |
```

Update this table as milestones progress.

## Multi-Agent Development

Plans are designed for parallel work. When a feature has independent milestones or tasks, **spawn agent teams or subagents** to work on different pieces concurrently.

**How it works:**
- The plan file is the shared coordination point — all agents read from and write to it
- Identify independent milestones/tasks that have no dependencies between them
- Spawn subagents for independent work (e.g., one agent builds auth models while another builds rate limiting)
- Each agent checks off its tasks in the plan as it completes them
- Sequential tasks (where one depends on another) should NOT be parallelized

**When to parallelize:**
- Multiple milestones with no shared dependencies
- Independent modules within a milestone (e.g., OTP service + JWT service)
- Tests and implementation across separate files

**Agent task prompts should include:**
- Reference to the plan file: "Read `plans/v{N}-{description}.md` for full context"
- Which specific milestone/tasks the agent owns
- TDD requirement: write failing tests first, then implement

## Workflow

### Starting a new feature
1. Check `plans/` — find the next version number
2. **Follow `best-practices` steps 1–3** — create branch, investigate the codebase (subagent), ask clarifying questions (scope, tradeoffs, backwards compat, stakeholders). Do not skip this.
3. Create `plans/v{N}-{description}.md`
4. Write Context, Design, and Milestones sections
5. Get user approval on the plan before coding
6. Identify which milestones/tasks can be parallelized
7. Begin work — spawn subagents for independent pieces

### After planning (before coding)
Run `/update-docs` to check if the plan itself revealed stale documentation (e.g., the investigation found outdated CLAUDE.md entries, incorrect API references in sibling repos, or drift in integration guides). Fix any staleness before starting implementation.

### Resuming work (new context, no memory)
1. Spawn an `Explore` subagent to read `plans/` and return a summary: which plan is active, what milestone you're on, what the next unchecked task is, and any key design context. **Do not read plan files directly** — they are large and will bloat your context.
2. Use the subagent's summary to orient yourself
3. Find the first unchecked task — that's where to resume
4. Continue working, checking off tasks as you go

### During implementation
- Check off each task immediately when done: `- [ ]` → `- [x]`
- Update the progress summary table when a milestone completes
- If you discover new work, add tasks to the appropriate milestone
- Commit the plan file alongside code changes
- If the approach fundamentally changes (e.g., switching auth strategy), create a new revision file (`-r2`) rather than editing in place — keep the original as history

### After each major milestone — pause for user testing
When a milestone is complete (all tasks checked), **stop and let the user test manually** before moving on:

1. **Provide step-by-step test instructions:**
   - Prerequisites (env vars, server running, etc.)
   - Exact commands to run (curl, browser URLs, SQL queries)
   - Expected output for each step
   - How to verify success vs. failure
2. **Include setup steps** if the milestone introduced new dependencies, env vars, or configuration
3. **Wait for user confirmation** that testing passed before starting the next milestone
4. **Clear context** after successful testing — the plan file has all the state needed to resume in a fresh context

This ensures the user validates each milestone incrementally rather than discovering issues after everything is built.

### After all milestones complete
- Run the `update-docs` skill to sync all documentation
- Run the project's linter
- Create PR

### Rolling back work
If code is reverted or the developer isn't happy with the implementation:
- Uncheck tasks back to the rolled-back state: `- [x]` → `- [ ]`
- Update the progress summary table to reflect the actual state
- The plan must always match reality — if code was reverted, the checkboxes must revert too

### Completing a plan
- All checkboxes checked
- Progress summary shows all milestones as "Done"
- Plan stays in `plans/` as historical record

## UI Work

When any milestone involves user-facing text or UI changes, use the `simple-design-principles` skill. Flag these tasks in the plan — copy should be reviewed with the same rigor as code.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting to code without checking `plans/` | Always check first — you may be mid-feature |
| Vague tasks ("set up auth") | Be specific: file paths, endpoint names, model fields |
| Forgetting to check off tasks | Update immediately — the plan is only useful if current |
| Creating a plan for a 10-minute fix | Use `best-practices` directly for small changes |
| Tracking progress elsewhere (todos, comments) | The plan file is the single source of truth |
| Running all tasks sequentially | Identify independent work and spawn subagents |
| Skipping investigation/questions because "I know the codebase" | Always follow `best-practices` steps — investigate and ask first |
