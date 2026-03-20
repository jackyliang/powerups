---
name: bug-fix
description: Use when fixing a bug — enforces reproduce-first-then-fix discipline with a strict step-by-step protocol. Prevents wrong-approach loops by gating each step on success criteria.
---

# Bug Fix Protocol

## Overview

A strict, sequential protocol for fixing bugs. Each step has a success criteria that MUST be met before proceeding to the next step. This prevents the common failure mode of guessing at fixes without understanding the bug, or breaking other things while fixing one thing.

**This skill invokes `powerups:best-practices`** — branching, investigation, TDD, and all other practices apply. This skill adds bug-specific discipline on top.

## When to Use

- User reports a bug or unexpected behavior
- A test is failing and needs investigation
- Something that used to work is now broken
- User pastes an error message or stack trace

## The Protocol

### Step 1: Create a branch

```bash
git checkout -b fix/{short-description}
```

Never fix bugs on `main`.

### Step 2: Read and understand

Read the relevant source files and understand the **current behavior**. Don't guess — read the actual code paths involved.

- Identify the entry point (endpoint, component, function) where the bug manifests
- Trace the code path from input to incorrect output
- Check recent git history for changes that may have introduced the bug: `git log --oneline -10 -- path/to/file.py`

**Success criteria:** You can explain what the code currently does and why it produces the wrong result.

### Step 3: Write a failing reproduction test

Write a **minimal** test that reproduces the exact bug. Run it and confirm it fails **for the right reason**.

- The test should fail because of the bug, not because of a typo or setup issue
- Keep the test minimal — don't test unrelated behavior
- Name the test descriptively: `test_returns_error_when_input_is_empty`, not `test_bug_fix`

```bash
# Run just the reproduction test
pytest tests/test_file.py::TestClass::test_name -v
```

**Success criteria:** The test fails, and the failure message clearly demonstrates the bug.

### Step 4: Investigate root cause

Now that you have a reproduction, investigate **why** it happens.

- Read the code paths identified in Step 2 more carefully
- Add temporary debug logging if needed (`logger.debug` or `print`) to narrow down the issue
- Check edge cases: null inputs, empty collections, type mismatches, race conditions

**Success criteria:** You can point to the exact line(s) of code causing the bug and explain the root cause.

### Step 5: Implement the smallest possible fix

Fix the root cause identified in Step 4. Keep the fix minimal — don't refactor, don't "improve" adjacent code, don't add features.

**Success criteria:** The fix addresses the root cause and nothing else.

### Step 6: Run the reproduction test

Run the test from Step 3. If it still fails, go back to Step 5.

```bash
pytest tests/test_file.py::TestClass::test_name -v
```

**Success criteria:** The reproduction test passes.

### Step 7: Run the full test suite

Run **all** tests to check for regressions.

```bash
# Python
pytest tests/

# JavaScript/TypeScript
npm test
```

If any other test broke, fix the regression **without breaking the original fix**. If fixing the regression requires changing the approach, go back to Step 5 with the new understanding.

**Success criteria:** All tests pass — both the new reproduction test and all existing tests.

### Step 8: Clean up

- Remove any temporary debug logging added in Step 4
- Remove any temporary `print` statements
- Verify the diff is clean: `git diff` should show only the fix and the test

**Success criteria:** No debug artifacts remain in the diff.

### Step 9: Simplify

**Run `/simplify`** — review changed code for reuse, quality, and efficiency. Fix issues found.

**Success criteria:** No duplicate code, N+1 queries, or anti-patterns in the diff.

### Step 10: Update change log

**Run `powerups:change-log`** — add an entry to `CHANGELOG.md` describing the fix in plain, business-user-friendly language. Skip this step only if the fix is purely internal (not user-facing).

**Success criteria:** `CHANGELOG.md` has a new entry for today's date.

### Step 11: Commit and PR

```bash
git add <specific files>
git commit -m "fix: <description of what was fixed and why>"
```

Create a PR. The PR description should include:
- What the bug was
- What caused it (root cause)
- How it was fixed
- The reproduction test that now passes

**Success criteria:** Commit is clean, PR is created.

## Rules

- **Do NOT skip steps.** Each step gates on the previous step's success criteria.
- **Do NOT proceed past a failing step.** If Step 6 fails, go back to Step 5. If Step 7 fails, fix the regression before moving on.
- **Do NOT expand scope.** A bug fix is not an opportunity to refactor, add features, or "improve" nearby code. Fix the bug, nothing more.
- **Do NOT remove the reproduction test.** It prevents the bug from recurring.

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Guess at the fix without reading the code | Read and trace the code path first (Step 2) |
| Fix without a reproduction test | Write a failing test first (Step 3) |
| Make a large fix that changes multiple behaviors | Make the smallest possible fix (Step 5) |
| Leave `print` or debug logging in the commit | Clean up before committing (Step 8) |
| Refactor adjacent code while fixing the bug | Only fix the bug — refactors are separate PRs |
| Skip the full test suite ("I only changed one file") | Always run all tests (Step 7) |
| Retry the same fix when the test still fails | Investigate deeper — re-read the root cause (Step 4) |
