---
name: best-practices
description: Use for any code change — bug fix, small feature, refactor, or improvement. Ensures TDD, clarifying questions, codebase investigation, DRY, proper branching/worktrees, UI skills, and doc updates. PDD invokes this automatically for large features.
---

# Best-Practices-Driven Development (BPDD)

## Overview

The baseline discipline for every code change, no matter how small. A bug fix, a refactor, a small feature — all of them follow these practices. The `plan-driven-development` skill invokes this automatically for large multi-milestone features, but you should use this directly for smaller work.

## When to Use

**Always.** Every code change should follow these practices. If the work is large enough for milestones and a plan file, use `plan-driven-development` instead (which includes everything here plus planning infrastructure).

## The Practices

### 1. Never Develop on Main

**Before writing any code, create a worktree or branch.** Ask the user which they prefer:

> "Should I create a git worktree (isolated copy, good for parallel work) or a new branch (simpler, single workspace)?"

- **Worktree** — `git worktree add ../project-feature feature/name` — use when the user works on multiple things in parallel, or when you're spawning subagents that need isolation
- **Branch** — `git checkout -b feature/name` — use for simple sequential work

**Never commit directly to main.** No exceptions.

### 2. Investigate Before Building

**Before writing code, understand what already exists.** Spawn an `Explore` subagent to check:

- Does similar code already exist? (DRY — see practice #5)
- Does existing infrastructure solve this problem? (Don't reinvent)
- What patterns does the codebase use for similar features?
- Do third-party dependencies offer unused capabilities that help?

**All investigation happens in subagents** to protect main context. The subagent returns a concise summary, not raw file contents.

**Subagent prompt template:**
> "Investigate the codebase for [feature/problem]. Check: (1) does similar code already exist, (2) do existing services or third-party deps already handle this, (3) what patterns are used for similar features. Return a concise summary under 30 lines."

### 3. Ask Before You Assume

**Use `AskUserQuestion` to clarify before building.** Don't guess at requirements, scope, or approach.

Ask about:
- **What they actually want** — don't infer, confirm
- **Who the user is** — developer, their customer, or end-user?
- **Scope** — specific to one case, or generic for future use?
- **Backwards compatibility** — keep the old code or delete it? (Most of the time: delete it)
- **Tradeoffs** — present the better option even if it's harder. Don't default to easy.

**Rules:**
- If the request is ambiguous, ask. Don't pick an interpretation.
- If there are multiple approaches, present them with tradeoffs. Recommend the better one.
- If you're about to make a product decision, surface it. The user's priorities may differ from yours.
- Batch related questions into one message.

### 4. Test-Driven Development

**Write failing tests first, then implement.** No exceptions. Use the `test-driven-development` skill.

The cycle:
1. **RED** — Write a test that describes what the code should do. Run it. Confirm it fails.
2. **GREEN** — Write the minimal code to make it pass.
3. **REFACTOR** — Clean up. Keep tests green.

No mocks. Tests hit real infrastructure.

### 5. DRY — Don't Repeat Yourself

**Before implementing anything, search for existing code that does the same or similar thing.** Spawn an `Explore` subagent to look:

> "Search the codebase for existing implementations of [what you're about to build]. Check utils, services, helpers, and similar features. Return file paths and a one-line summary of what each does."

**If similar code exists:**
- Extend or generalize the existing implementation
- Extract shared logic into a reusable function/class
- Don't create a second version of the same thing

**If you find duplication after writing code:**
- Refactor immediately — don't leave it for later
- Extract the common pattern into a shared utility

**Three similar lines of code is better than a premature abstraction** — but three similar *functions* should be consolidated.

### 6. Use Frontend-Design for UI Work

If the change involves any frontend/UI work, use the `frontend-design` skill. This applies to:
- New components or pages
- Modifying existing UI
- Adding visual indicators, loading states, error states
- Any user-facing change

### 7. Update Docs When Done

After the code is complete and tests pass, run the `update-docs` skill to sync all documentation:
- CLAUDE.md
- README
- Public skills/plugins
- Downstream project docs

Don't skip this. Stale docs cause more damage than missing docs.

### 8. Lint Before Committing

Run the project's linter before committing:
- Python: `ruff check` / `ruff format`
- JavaScript/TypeScript: `npm run lint`
- Fix issues in files you changed. Don't fix pre-existing issues in untouched files.

## Quick Reference

```
1. Branch or worktree (never main)
2. Investigate (subagent — what exists?)
3. Ask (clarify requirements with user)
4. TDD (red → green → refactor)
5. DRY (search before building, extract duplicates)
6. Frontend-design skill (if UI work)
7. Update docs (run /update-docs)
8. Lint (before committing)
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Commit to main | Create worktree or branch first |
| Start coding without checking what exists | Spawn Explore subagent first |
| Guess what the user wants | Ask with `AskUserQuestion` |
| Write tests after implementation | Write failing tests first (TDD) |
| Copy-paste similar code | Extract shared utility |
| Build custom infrastructure when a dependency handles it | Check third-party capabilities first |
| Default to the easier approach | Present options, recommend the better one |
| Keep old code "just in case" | Ask about backwards compat — usually delete |
| Skip docs because "it's a small change" | Run /update-docs — small changes cause drift too |
| Write UI code without frontend-design skill | Always use it for user-facing changes |
