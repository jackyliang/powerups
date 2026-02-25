---
name: test-driven-development
description: Use when building any feature (small or large), fixing bugs, or refactoring — always write failing tests first against real infrastructure
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write minimal code to pass. No exceptions.

If you didn't watch the test fail, you don't know if it tests the right thing. Tests written after implementation pass immediately — that proves nothing.

## When to Use

**Always:**
- New features (small or large)
- Bug fixes
- Refactoring
- Behavior changes
- When using plan-driven-development (TDD integrates into milestone tasks)

**Exceptions (ask the user first):**
- Throwaway prototypes or spike explorations
- Pure configuration changes (env vars, settings)
- Documentation-only changes

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Start over. Don't keep it as "reference" — you'll adapt it instead of writing from tests. Delete means delete.

## Red-Green-Refactor Cycle

### 1. RED — Write a Failing Test

Write one test that describes what the code **should** do.

**Run it. Confirm it fails.** The failure must be because the feature is missing, not because of a typo or import error.

```bash
pytest tests/test_{module}.py::TestClassName::test_method -v
```

If the test passes immediately, you're testing existing behavior. Fix the test.

### 2. GREEN — Write Minimal Code

Write the simplest code that makes the test pass. Don't add features, refactor, or "improve" beyond what the test requires.

```bash
pytest tests/test_{module}.py -v
```

All tests must pass — the new one and all existing ones.

### 3. REFACTOR — Clean Up

Only after green. Remove duplication, improve names, extract helpers. Keep all tests green. Don't add behavior.

### 4. REPEAT

Next failing test for the next behavior.

## What Makes a Good Test

### Test Real Behavior, Not Plumbing

Tests should verify **business outcomes**, not that frameworks work.

**Good — tests actual behavior:**
```python
async def test_upsert_updates_existing_record(writer, test_engine, test_schema):
    await writer.ensure_schema(test_schema)
    await writer.ensure_table(test_schema, "users", {"id": "1", "name": "Alice", "status": "new"})
    await writer.upsert_records(test_schema, "users", [{"id": "1", "name": "Alice", "status": "new"}])

    # Upsert with updated status
    count = await writer.upsert_records(
        test_schema, "users", [{"id": "1", "name": "Alice", "status": "active"}]
    )
    assert count == 1

    # Verify the actual data changed in the database
    async with test_engine.connect() as conn:
        result = await conn.execute(
            text(f'SELECT "status" FROM "{test_schema}"."users" WHERE "id" = \'1\'')
        )
        assert result.scalar() == "active"
```

**Bad — tests that the framework returns 200:**
```python
async def test_endpoint_works(client):
    response = await client.get("/v1/health")
    assert response.status_code == 200  # This tells you nothing useful
```

### Test Naming

Name tests so failures are self-documenting:

```python
# Good — describes the behavior
async def test_rejects_duplicate_sync_trigger_with_409(...)
async def test_expired_otp_returns_unauthorized(...)
async def test_upsert_sets_synced_at_timestamp(...)

# Bad — vague
async def test_sync_works(...)
async def test_auth(...)
async def test_api(...)
```

### One Behavior Per Test

If the test name has "and" in it, split it into two tests.

## No Mocks

**Do not use `unittest.mock`, `MagicMock`, `patch`, or any mocking library.**

Tests must hit real infrastructure:

| What | How to Test |
|------|-------------|
| **Database operations** | Real Postgres (Ghost DB fork if available, otherwise cleanup-based) |
| **API endpoints** | Full HTTP via FastAPI test client against real DB |
| **Service classes** | Instantiate real classes, call real methods |
| **Provider APIs (Zendesk, etc.)** | Real API with test credentials, or VCR cassettes as last resort |
| **Nango OAuth** | Nango sandbox/test environment |

**The only acceptable mock:** A third-party API that has no sandbox, no test environment, and charges per call. Document why with a comment above the mock:

```python
# Mock required: Stripe charges real money per API call and
# their sandbox is down. No viable alternative for CI.
```

"It's easier" and "it's faster" are not valid reasons to mock.

## Database Testing

Always test against a real database — the same engine as production (Postgres, not SQLite).

### Ghost DB Projects → Use database-branching Skill

If the project uses Ghost DB, follow the **database-branching** skill for fork-based test isolation. Tests run against the development fork — no cleanup code needed, the fork is disposable. If forking fails, **stop and tell the user**. Do not silently fall back to testing against production.

### Non-Ghost Projects → Cleanup-Based Isolation

When Ghost DB is not available, you need explicit cleanup. Use one or both of these patterns:

#### Transaction Rollback (Per-Test Isolation)

Each test runs in a transaction that rolls back afterward. Fast, but can't test DDL operations.

```python
@pytest.fixture
async def db_session(test_engine):
    async with test_engine.connect() as conn:
        trans = await conn.begin()
        session = AsyncSession(bind=conn)
        yield session
        await trans.rollback()  # Each test starts clean
```

#### Explicit Cleanup (For DDL / Schema Tests)

When tests create schemas, tables, or other DDL that can't be rolled back:

```python
@pytest.fixture(autouse=True)
async def _cleanup_schema(test_engine, test_schema):
    yield
    async with test_engine.begin() as conn:
        await conn.execute(text(f'DROP SCHEMA IF EXISTS "{test_schema}" CASCADE'))
```

**Rules for cleanup-based isolation:**
- Use unique names per test (e.g., `test_{uuid.uuid4().hex[:12]}`) to avoid collisions
- Always clean up in a `yield` fixture (runs even if test fails)
- Clean up schemas, tables, and test data — don't leave debris
- Consider a dedicated test database (not production) even without forking

### Running Tests

```bash
pytest tests/ -v                        # All tests
pytest tests/test_{module}.py -v        # Specific module
pytest tests/test_{module}.py -k "test_name" -v  # Specific test
```

## Integration with Plan-Driven Development

When using the `plan-driven-development` skill for large features, TDD integrates directly into the plan's milestones.

### How It Works

Each milestone should have test tasks **before** implementation tasks:

```markdown
### Milestone 2: Auth Endpoints
**Goal:** Email OTP login flow with JWT tokens.

- [ ] Write failing tests for `POST /v1/auth/login` (sends OTP)
- [ ] Write failing tests for `POST /v1/auth/verify` (validates OTP, returns JWT)
- [ ] Write failing tests for `POST /v1/auth/refresh` (refreshes JWT)
- [ ] Implement login endpoint to pass tests
- [ ] Implement verify endpoint to pass tests
- [ ] Implement refresh endpoint to pass tests

**Verification:**
- [ ] All tests pass against forked DB
- [ ] Fork deleted after verification
```

### Task Order Within Milestones

1. **Test tasks first** — `Write failing tests for X`
2. **Run tests** — confirm they fail (red)
3. **Implementation tasks** — `Implement X to pass tests`
4. **Run tests** — confirm they pass (green)
5. **Check off tasks** in the plan as completed

### Multi-Agent TDD

When spawning subagents for parallel milestone work, every agent prompt **must** include:

> "Write failing integration tests FIRST in `tests/test_{module}.py`. Tests must use real database (Ghost DB fork) — no mocks. Run them to confirm they fail. Then write implementation to make them pass."

The team lead must verify:
- Test files exist for every module
- Tests contain no mocks (search for `mock`, `patch`, `MagicMock`)
- Tests were run and failed before implementation was written

## What to Test

| Layer | Test Pattern |
|-------|--------------|
| **API endpoints** | Full HTTP request → verify response AND database state |
| **Service methods** | Call real methods → verify side effects (DB writes, state changes) |
| **Data models** | Create real instances → verify constraints, defaults, relationships |
| **Business logic** | Pure functions → verify input/output for normal cases AND edge cases |
| **Error handling** | Trigger real errors → verify correct error codes and messages |
| **Sync engine** | Run real syncs → verify data lands in correct schema/table |

### Edge Cases to Always Cover

- Empty inputs (empty list, empty string, None)
- Duplicate operations (idempotency)
- Invalid/malformed inputs
- Unauthorized access (missing or bad auth)
- Concurrent operations (if applicable)

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Need to explore first" | Fine. Throw away exploration. Start with TDD. |
| "Test is hard to write" | Listen to the test. Hard to test = hard to use. Simplify the design. |
| "Mocking is faster" | Mocks test mock behavior, not real behavior. You'll ship bugs. |
| "Just this once" | That's rationalization. Every time is "just this once." |
| "The plan doesn't mention tests" | Every plan implicitly requires TDD. Add test tasks. |

## Verification Checklist

Before marking any task or feature complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass (new and existing)
- [ ] Tests use real infrastructure (no mocks)
- [ ] Tests verify behavior, not plumbing
- [ ] Edge cases covered (empty, duplicate, invalid, unauthorized)
- [ ] Test database cleaned up (Ghost DB fork deleted, or cleanup fixtures ran)
- [ ] Plan file updated (if using plan-driven-development)
