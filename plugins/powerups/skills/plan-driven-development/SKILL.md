---
name: plan-driven-development
description: Use when starting a multi-milestone feature, resuming work after context loss, or unsure if a feature plan already exists
---

# Plan-Driven Development

## Overview

Large features get a versioned plan file in `plans/` that serves as the **single source of truth** — what's been done, what's in progress, and what's left. The plan persists across context windows so any agent (or agent team) can pick up where the last one left off.

## When to Use

**Create a plan when:**
- Feature spans multiple milestones or will take more than one session
- Multiple files/modules need coordinated changes
- You need to track progress across context resets
- Multiple agents will work on different pieces in parallel

**Skip the plan when:**
- Single-file change, small bugfix, quick refactor
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

## Investigate Before You Design

**Before designing anything, understand what already exists.** Spawn an `Explore` subagent to investigate the codebase — its architecture, services, third-party dependencies, and existing infrastructure. The goal is to discover what the project already has that's relevant to the new feature, so you don't reinvent things or ignore capabilities that are already there.

### Why this matters

A common failure mode: you know about a service (e.g., "we use Nango for OAuth") but when designing a new feature (e.g., webhooks), you treat it as a separate problem and build from scratch — without checking whether that existing service already handles it. **Existing infrastructure is the first place to look for solutions, not the last.**

### What to investigate

**All investigation MUST happen in subagents.** Codebase exploration, reading config files, reading existing plans, and reading large source files consume enormous amounts of context. The main conversation should stay lean — receive concise summaries, not raw file contents.

Spawn one or more `Explore` subagents (thoroughness: "very thorough") to answer:

1. **What services/dependencies does this project use?** Read CLAUDE.md, package configs, config files, `.env.example`. Understand the full tech stack — not just the parts you've touched before.
2. **Does any existing service already solve part of this problem?** If the feature involves webhooks, check if the OAuth provider (e.g., Nango) already handles webhook forwarding. If the feature involves background jobs, check if there's already a scheduler. Don't assume you need to build new infrastructure.
3. **What's the current architecture for similar features?** Read existing implementations of related functionality. How does data flow? What patterns are used? What would break if you changed them?
4. **What third-party capabilities are available but unused?** Check the docs of services the project depends on. They may offer features the project hasn't leveraged yet that solve the problem directly.

**Subagent prompt template for investigation:**
> "Investigate the codebase for [feature area]. Read CLAUDE.md, relevant source files, config, and existing plans in plans/. Return a concise summary (not raw file contents): (1) what services/infra already exist for this, (2) what third-party dependencies are used and what capabilities they offer beyond what's currently used, (3) the current architecture pattern for similar features, (4) any existing plan files and their status. Keep the summary under 50 lines."

### Rules

- **Always investigate the codebase BEFORE asking the user design questions.** Your questions will be better informed.
- **Always check existing third-party service capabilities BEFORE designing custom solutions.** If Nango/Supabase/Svix/etc. already handles something, use it.
- **Spawn an Explore subagent** for thorough investigation. Don't rely on partial knowledge from earlier in the conversation — it may be stale or incomplete.
- **Report findings to the user** before proposing a design. "I found that Nango already supports webhook forwarding, so we don't need to build our own per-provider webhook infrastructure."

### Anti-pattern: Inventing When You Should Be Discovering

| What you assumed | What was already there | How to avoid |
|-----------------|----------------------|-------------|
| "We need per-provider webhook registration" | Nango already forwards provider webhooks | Check existing service docs first |
| "We need a custom job queue" | Project already has a scheduler service | Read the codebase before designing |
| "We need to build OAuth token refresh" | Nango handles token refresh automatically | Understand what dependencies provide |

## Design Phase: Ask Before You Assume

**After investigating the codebase, interrogate the requirements with the user.** Use `AskUserQuestion` liberally. Do not assume the simpler solution is what the user wants — present options with honest tradeoffs and recommend the better approach even if it's harder.

### What to ask about

- **User experience**: "Who performs this action — you, your customer, or their end user? That changes the design significantly."
- **Scope**: "Should this handle just Zendesk, or be generic for any future provider?"
- **Architecture tradeoffs**: Present multiple approaches with pros/cons. Recommend the better one, not the easier one. Example:
  > "Option A: Manual webhook setup (simpler, ships faster, but every customer has to configure it themselves).
  > Option B: Auto-registration via API during connection (more work upfront, but zero friction for customers).
  > I recommend Option B — the upfront cost is worth it for the UX."
- **Existing infrastructure**: Share what you found in the investigation. "Nango already supports webhook forwarding — should we use that instead of building our own?" Don't bury this — lead with it.
- **Backwards compatibility**: When a new feature replaces an existing one, ask: "Do you want backwards compatibility with the old approach, or should I remove it entirely?" Most of the time the answer is no — they want the old code gone. **When the answer is no, delete everything**: old implementation code, old tests, old config, old docs references. Don't leave dead code "just in case." A clean codebase is worth more than a safety net nobody asked for.
- **Edge cases**: "What happens when X fails? Should we retry, alert, or silently skip?"
- **Integration points**: "Does this affect the frontend? Other services? Docs?"
- **UI/UX work**: If the feature involves frontend changes, use the **frontend-design** skill for UI implementation. Mention this in the plan's milestones so agents know to invoke it.

### Rules

- **Never default to the easy path without presenting the better path.** If there's a harder approach that produces a better product, recommend it explicitly and explain why.
- **Don't make product decisions silently.** If you're choosing between approaches, surface the decision to the user. What feels obvious to you may not match their priorities.
- **Ask early, not late.** A 30-second question now prevents a multi-hour rewrite later.
- **It's OK to ask multiple questions at once.** Batch related questions into one message rather than drip-feeding them.
- **If the user's request is ambiguous, do NOT pick an interpretation and run with it.** Ask which interpretation they mean.
- **Lead with investigation findings.** If you discovered that existing infrastructure solves the problem, tell the user before asking design questions. It reframes the entire conversation.

### Anti-patterns

| Anti-pattern | What to do instead |
|-------------|-------------------|
| Silently choosing the simpler approach | Present both, recommend the better one |
| Assuming who the "user" is | Ask: developer, customer, or end-user? |
| Making scope decisions (generic vs specific) | Ask the user's intent |
| Guessing at UX requirements | Ask what the experience should feel like |
| Writing the full plan then asking "looks good?" | Ask clarifying questions BEFORE writing the plan |
| Designing new infrastructure without checking existing services | Investigate codebase and third-party capabilities first |
| Treating a known dependency as only doing one thing | Check its full feature set — it may already solve your problem |
| Keeping old code/tests "for backwards compatibility" without asking | Ask the user — most of the time they want the old code deleted |

## Workflow

### Starting a new feature
1. Check `plans/` — find the next version number
2. **Investigate the codebase** — spawn an `Explore` subagent to understand existing architecture, services, and third-party dependencies relevant to the feature. Check if existing infrastructure already solves part of the problem. Do not skip this step.
3. **Ask clarifying questions** — share investigation findings with the user, then use `AskUserQuestion` to resolve ambiguities, scope, and tradeoffs BEFORE writing the plan. Lead with what you discovered ("I found that X already handles Y — should we use it?"). Do not skip this step.
4. Create `plans/v{N}-{description}.md`
5. Write Context, Design, and Milestones sections
6. Get user approval on the plan before coding
7. Identify which milestones/tasks can be parallelized
8. Begin work — spawn subagents for independent pieces

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

### Rolling back work
If code is reverted or the developer isn't happy with the implementation:
- Uncheck tasks back to the rolled-back state: `- [x]` → `- [ ]`
- Update the progress summary table to reflect the actual state
- The plan must always match reality — if code was reverted, the checkboxes must revert too

### Completing a plan
- All checkboxes checked
- Progress summary shows all milestones as "Done"
- Plan stays in `plans/` as historical record

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting to code without checking `plans/` | Always check first — you may be mid-feature |
| Vague tasks ("set up auth") | Be specific: file paths, endpoint names, model fields |
| Forgetting to check off tasks | Update immediately — the plan is only useful if current |
| Creating a plan for a 10-minute fix | Only for multi-milestone features |
| Tracking progress elsewhere (todos, comments) | The plan file is the single source of truth |
| Running all tasks sequentially | Identify independent work and spawn subagents |
| Defaulting to the easier solution without asking | Present options, recommend the better one even if harder |
| Making product/scope decisions without asking | Use `AskUserQuestion` — the user's priorities may differ from yours |
| Writing the full plan then asking "looks good?" | Ask clarifying questions BEFORE writing the plan |
| Assuming who "the user" is in a multi-stakeholder system | Ask: is this the developer, their customer, or the end-user? |
| Designing new infrastructure without investigating existing stack | Spawn an Explore subagent first — existing services may already solve it |
| Knowing about a dependency but not checking its full capabilities | A service you use for OAuth may also handle webhooks, syncing, etc. |
| Skipping codebase investigation because "I already know the codebase" | Your knowledge may be partial or stale — always verify before designing |
| Keeping old implementation alongside the replacement "just in case" | Ask about backwards compatibility — if no, delete old code, tests, and config completely |
