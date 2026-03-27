---
name: plan-driven-development
description: Use when starting any feature (small or large), resuming work after context loss, or unsure if a feature plan already exists. For smaller features, use lightweight mode (no plan file, but all PDD rules still apply).
---

# Plan-Driven Development

## Overview

Large features get a versioned plan file in `plans/` that serves as the **single source of truth** — what's been done, what's in progress, and what's left. The plan persists across context windows so any agent (or agent team) can pick up where the last one left off.

**PDD requires `powerups:best-practices` — invoke it, don't just reference it.** Every practice in `powerups:best-practices` is mandatory here: TDD (tests before implementation), branching (never develop on main), investigation (subagent before building), clarifying questions (ask before assuming), DRY, frontend-design for UI, self-documenting APIs, update-docs when done. PDD adds planning infrastructure on top — it does NOT replace or relax any of those practices.

**If you're unsure whether a best-practice applies:** it does. PDD is `powerups:best-practices` + plans, not plans instead of `powerups:best-practices`.

## When to Use

PDD can be invoked for features of any size. The difference is whether you write a plan file.

**Write a plan file (`plans/v{N}-*.md`) when:**
- Feature spans multiple milestones or will take more than one session
- Multiple files/modules need coordinated changes
- You need to track progress across context resets
- Multiple agents will work on different pieces in parallel

**Use PDD in lightweight mode (plan inline, no file) when:**
- Feature is smaller but still touches multiple files
- Work fits in one session with no risk of context loss
- No milestones needed — it's a single logical chunk of work

In lightweight mode, still write a plan — but present it inline in the conversation for user review instead of writing it to a markdown file. The inline plan should cover: what you're changing, which files are affected, the impact scan results, and the implementation approach. Get user approval before coding. All other PDD rules still apply: invoke `powerups:best-practices` (including the impact scan), run the skill audit, create a branch, ask clarifying questions, TDD, and run all post-completion steps (simplify, changelog, update-docs, full test suite, lint).

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

Tests first (these will fail until implementation):
- [ ] Write failing tests for X
- [ ] Write failing tests for Y

Then implement to make tests pass:
- [ ] Implement X
- [ ] Implement Y

**Verification:**
- [ ] How to confirm this milestone is done
```

**TDD is required by default.** Every milestone that adds or changes behavior MUST list test tasks before implementation tasks. Tests are written first, confirmed to fail, then implementation makes them pass. This is non-negotiable unless the user explicitly opts out (e.g., "skip tests", "no tests for this"). If the user hasn't said to skip tests, include them.

Milestones that are pure refactors of already-tested code (e.g., moving code without changing behavior) don't need new tests — but existing tests must still pass.

Rules:
- Tasks are concrete and actionable ("Create `sync_hq/auth/models.py`" not "Set up auth")
- Include file paths where relevant
- **Test tasks come before implementation tasks within each milestone** — this is the TDD ordering
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
1. **Set `/effort max`** — planning requires deep reasoning. Always use max effort during the planning phase.
2. Check `plans/` — find the next version number
3. **Create a feature branch FIRST** — `git checkout -b feat/{description}`. **NEVER write plans or implement code on `main`.** This applies to the plan file itself — even the plan commit goes on a branch.
4. **Invoke `powerups:best-practices`** — this is not optional. Run the skill to ensure branching, codebase investigation (subagent), impact scan, and clarifying questions all happen before any code or plan is written. Do not just reference it — actually invoke it.
5. **Skill audit — MANDATORY before writing the plan.** List every available powerups skill by name, then for each one, explicitly state whether it applies to this feature and why. Output this analysis to the user before proceeding. This ensures no skill is forgotten during planning or implementation.

   Example output:
   ```
   Skill audit for v10-sync-change-details:
   - best-practices: YES — always applies (already invoked)
   - test-driven-development: YES — new backend logic needs tests
   - simple-design-principles: YES — frontend UI with user-facing copy
   - self-documenting-apis: YES — new API endpoint
   - database-branching: NO — not using Ghost DB
   - update-docs: YES — run after all milestones complete
   - bug-fix: NO — this is a new feature, not a bug fix
   ```

   **Every skill marked YES must appear as an explicit task or note in the relevant milestone.** If `update-docs` applies, it MUST appear as a task in the final milestone or as a post-completion step. Do not rely on remembering — write it into the plan.
6. Create `plans/v{N}-{description}.md`
7. Write Context, Design, and Milestones sections — include skill-specific tasks identified in step 5
8. Get user approval on the plan before coding
9. Identify which milestones/tasks can be parallelized
10. Begin work — spawn subagents for independent pieces

### After planning (before coding)
Run `/update-docs` to check if the plan itself revealed stale documentation (e.g., the investigation found outdated CLAUDE.md entries, incorrect API references in sibling repos, or drift in integration guides). Fix any staleness before starting implementation.

### Resuming work (new context, no memory)
1. Spawn an `Explore` subagent to read `plans/` and return a summary: which plan is active, what milestone you're on, what the next unchecked task is, and any key design context. **Do not read plan files directly** — they are large and will bloat your context.
2. Use the subagent's summary to orient yourself
3. Find the first unchecked task — that's where to resume
4. Continue working, checking off tasks as you go

### During implementation
- **Invoke `powerups:best-practices` at the task level** — TDD (write failing test, then implement), DRY (search before building), investigation (understand before changing). The plan organizes the work; `powerups:best-practices` governs how each task is executed. Actually invoke the skill, don't just follow it from memory.
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
- **Execute every skill marked YES in the skill audit.** Go back to your skill audit output and confirm each one was actually used. If any was missed, execute it now before creating the PR.
- **Run `/simplify`** — review all changed code for reuse, quality, and efficiency. Fix issues found.
- **Run `powerups:change-log`** — add an entry to `CHANGELOG.md` describing the feature in plain, business-user-friendly language. This is NOT optional for user-facing changes.
- Run the `update-docs` skill to sync all documentation — this is NOT optional
- Run the project's linter
- **Run the full test suite** — `pytest` (or the project's test command). ALL tests must pass before creating the PR. This catches regressions where new code breaks existing tests, or where tests and code were updated inconsistently (e.g., table name changes that affect both production code and test fixtures). Do not skip this step — a green test suite is a hard gate for PR creation.
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

## API Work

When any milestone involves creating or modifying API endpoints, use the `self-documenting-apis` skill. Every endpoint should have docstrings and typed response models so auto-generated docs (`/docs`, `/redoc`) are the single source of truth — no separate API reference file to maintain.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting to code without checking `plans/` | Always check first — you may be mid-feature |
| Vague tasks ("set up auth") | Be specific: file paths, endpoint names, model fields |
| Forgetting to check off tasks | Update immediately — the plan is only useful if current |
| Creating a plan for a 10-minute fix | Use PDD lightweight mode — no plan file, but still follow all PDD rules |
| Tracking progress elsewhere (todos, comments) | The plan file is the single source of truth |
| Running all tasks sequentially | Identify independent work and spawn subagents |
| Skipping investigation/questions because "I know the codebase" | Always follow `best-practices` steps — investigate and ask first |
| Listing implementation tasks before test tasks in milestones | TDD is the default — test tasks come first. Only skip if the user explicitly opts out |
| Writing a plan with no tests at all | Every milestone that adds behavior needs test tasks. If you forgot them, add them before starting implementation |
| Treating PDD as a replacement for best-practices | PDD = `powerups:best-practices` + plans. Actually invoke the skill — don't just follow it from memory |
| Jumping straight to coding after writing the plan | Follow best-practices: create branch, investigate codebase, ask clarifying questions FIRST |
| Writing the plan file or implementing on `main` | **Always create a feature branch before writing anything** — plans and code both go on branches, never `main` |
| Skipping the skill audit before writing the plan | **Always run the skill audit (step 4)** — list every powerups skill, decide YES/NO for each, and write YES skills into the plan as tasks |
| Forgetting to run `update-docs` or other skills after completion | Go back to the skill audit and check off each YES skill. If you didn't run it, run it now |
| Skipping the full test suite before creating the PR | **Always run all tests after the final milestone.** Tests and code can drift independently (e.g., fixtures use old table names while code uses new ones). A full suite run is the only way to catch this. |
