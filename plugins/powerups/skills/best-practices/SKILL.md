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

**Before writing any code, create a new branch.**

```bash
git checkout -b feature/name
```

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

**When working with 3rd party APIs or libraries:** Use `WebSearch` to look up the latest official documentation before writing any integration code. Your training data may be outdated — APIs change, deprecate endpoints, rename parameters, and introduce new best practices. A quick search confirms you're using the current API surface, not a stale version from memory.

- Search for the official docs (e.g., "Stripe API create payment intent latest docs")
- Check for recent breaking changes or migration guides
- Verify parameter names, required fields, and response shapes against the current docs
- If the library has a changelog or migration guide, skim it for recent changes

**Do NOT rely on training knowledge alone for 3rd party API calls.** Even if you "know" the API, verify it — the cost of a search is trivial compared to debugging a broken integration from a deprecated endpoint.

### 3. Impact Scan Before Changing Existing Code

**Before modifying any existing function, API, database schema, or shared utility, run 3 parallel subagents to exhaustively scan everything that depends on it.** This prevents incomplete changes that break existing code.

This is mandatory whenever you are:
- Changing a function signature (parameters, defaults, return type)
- Changing behavior of an existing function (parallelism, batch sizes, side effects)
- Adding/removing/renaming a database column or table
- Modifying a shared utility, helper, or base class
- Changing an API endpoint's request/response shape

**Run all 3 scans in parallel as `general-purpose` subagents:**

**Scan 1 — Callers:**
> "I'm modifying [function/module]. Find EVERY import and call site across the entire codebase. Check: (1) every file that imports it, including aliased imports, (2) every direct and indirect call site with file path and line number, (3) any hardcoded values matching current defaults I'm changing, (4) related functions in the same module with similar patterns, (5) scheduled jobs, cron handlers, background tasks, or webhooks that trigger this code path. For each: file path, line number, exact usage, whether it needs updating."

**Scan 2 — Data:**
> "I'm modifying [table/column/query]. Find EVERY database interaction across the entire codebase. Check: (1) every query that reads/writes the affected table(s), (2) every column reference in SELECTs, INSERTs, UPDATEs, WHERE clauses, JOINs, (3) every ORM model, typed dict, or Pydantic model mapping to this table, (4) every RPC/function call that touches this data, (5) every place that constructs rows or dicts matching the table schema. For each: file path, line number, exact usage, whether it needs updating."

**Scan 3 — Tests:**
> "I'm modifying [function/module]. Find EVERY test dependency across the entire codebase. Check: (1) every test file that imports or calls the changed function, (2) every fixture that sets up data for this code path, (3) every assertion that depends on current behavior (return values, side effects, batch sizes), (4) every mock or patch targeting the changed function, (5) integration tests exercising this code path end-to-end. For each: file path, test name, what it tests, whether it needs updating."

**What to do with the results:**
- Merge findings from all 3 scans into a single impact picture
- If using PDD, add a "Callers Impacted" section to the plan
- If not using a plan, verify each caller is handled before marking the work done
- Update any caller that passes explicit values matching old defaults you're changing

**This is NOT the same as practice #2 (Investigate Before Building).** Practice #2 asks "does similar code exist?" to avoid reinventing. This practice asks "what will break when I change this?" to avoid incomplete changes.

### 4. Ask Before You Assume

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

### 5. Test-Driven Development

**Write failing tests first, then implement.** No exceptions. Use the `test-driven-development` skill.

The cycle:
1. **RED** — Write a test that describes what the code should do. Run it. Confirm it fails.
2. **GREEN** — Write the minimal code to make it pass.
3. **REFACTOR** — Clean up. Keep tests green.

No mocks. Tests hit real infrastructure.

### 6. DRY — Don't Repeat Yourself

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

Use registry patterns for similar operations with different configurations — a dict mapping keys to functions/configs beats a chain of if/else blocks.

### 7. No Backward Compatibility by Default

**Do NOT implement backward compatibility or legacy methods unless explicitly asked.**

- When making breaking changes, ask: "Do you need backward compatibility for this change?"
- Most of the time, the answer is no — just update all usages directly
- Avoid: renamed variables with old aliases, deprecated function wrappers, legacy API endpoints, re-exports for old import paths
- If old code is unused after the change, delete it completely — no `# removed` comments, no `_unused` variables

### 8. Use Simple-Design-Principles for UI Work

If the change involves any user-facing text or UI, use the `simple-design-principles` skill. This covers:
- Copy and labels (plain language, no jargon)
- Component selection (consistent UI library usage)
- Toast messages, empty states, error messages
- Button labels and action text

### 9. Use Frontend-Design for UI Work

If the change involves any frontend/UI work, use the `frontend-design` skill. This applies to:
- New components or pages
- Modifying existing UI
- Adding visual indicators, loading states, error states
- Any user-facing change

### 10. Self-Documenting APIs

If the change involves API endpoints (new or modified), use the `self-documenting-apis` skill. This ensures:
- Endpoint docstrings (description, context, side effects)
- Typed response models with `Field(description=...)`
- Typed request models with field descriptions
- Proper status codes and error responses
- Router tags for grouping

Auto-generated docs (`/docs`, `/redoc`) should be the only API reference — no separate doc file to maintain.

### 11. Update Docs When Done

After the code is complete and tests pass, run the `update-docs` skill to sync all documentation:

- CLAUDE.md
- README
- Public skills/plugins
- Downstream project docs

Don't skip this. Stale docs cause more damage than missing docs.

### 12. Simplify After Implementation

After the code is working and tests pass, run `/simplify` to review changed code for reuse, quality, and efficiency. This catches:
- Duplicate code that should be extracted
- N+1 queries and missed batch operations
- React anti-patterns (components defined inside render)
- Stringly-typed code where types exist
- Copy-paste with slight variation

Fix issues found, then proceed to docs and lint.

### 13. Lint Before Committing

Run the project's linter before committing:
- Python: `ruff check` / `ruff format`
- JavaScript/TypeScript: `npm run lint`
- Fix issues in files you changed. Don't fix pre-existing issues in untouched files.

## Quick Reference

```
1.  Branch (never main)
2.  Investigate (subagent — what exists? WebSearch — latest 3rd party API docs)
3.  Impact scan (3 parallel subagents — what will break?)
4.  Ask (clarify requirements with user)
5.  TDD (red → green → refactor)
6.  DRY (search before building, extract duplicates)
7.  No backward compat (unless explicitly asked)
8.  Simple-design-principles (if UI/copy work)
9.  Frontend-design skill (if UI work)
10. Self-documenting APIs (if API work)
11. Update docs (run /update-docs)
12. Simplify (run /simplify after implementation)
13. Lint (before committing)
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Commit to main | Create a branch first |
| Start coding without checking what exists | Spawn Explore subagent first |
| Change a function without scanning for all callers | Run 3 parallel impact scan subagents first |
| Assume only the obvious files are affected | The scan always finds surprising callers — cron jobs, background tasks, shared utilities |
| Guess what the user wants | Ask with `AskUserQuestion` |
| Write tests after implementation | Write failing tests first (TDD) |
| Copy-paste similar code | Extract shared utility |
| Build custom infrastructure when a dependency handles it | Check third-party capabilities first |
| Assume your training data has the latest 3rd party API | WebSearch the official docs before writing integration code |
| Default to the easier approach | Present options, recommend the better one |
| Keep old code "just in case" | Delete it — no backward compat by default |
| Add backward compat shims without asking | Ask the user first — usually not needed |
| Write UI copy with technical jargon | Use simple-design-principles skill |
| Skip docs because "it's a small change" | Run /update-docs — small changes cause drift too |
| Write UI code without frontend-design skill | Always use it for user-facing changes |
| Maintain a separate api-reference.md | Use `self-documenting-apis` — code is the docs |
| Return raw dicts from API endpoints | Define typed response models |
