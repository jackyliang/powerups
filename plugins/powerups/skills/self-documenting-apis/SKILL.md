---
name: self-documenting-apis
description: Use when building or refactoring FastAPI endpoints. Ensures endpoints have proper docstrings, response models, and request models so auto-generated docs (Swagger/ReDoc) are the single source of truth — no separate API reference file to maintain.
---

# Self-Documenting APIs

## Overview

FastAPI auto-generates OpenAPI docs at `/docs` (Swagger UI) and `/redoc` (ReDoc). When endpoints have proper docstrings and typed models, these docs are comprehensive enough to replace any hand-written API reference. The goal: **never maintain a separate api-reference.md** — the code IS the documentation.

## When to Use

**Apply this skill when:**
- Creating a new API endpoint
- Refactoring an existing endpoint (changing request/response shape)
- Adding a new router module
- Any milestone in a plan that involves API changes

**Skip when:**
- Internal helper functions (not exposed via HTTP)
- WebSocket endpoints (OpenAPI support is limited)

## The Practices

### 1. Every Endpoint Gets a Docstring

The docstring becomes the endpoint description in Swagger UI. Write it for the developer consuming your API.

```python
@router.post("/v1/connections/oauth")
async def create_oauth_session(
    body: OAuthSessionRequest,
    developer: CurrentDeveloper,
):
    """Start OAuth flow for an end user.

    Creates a Nango Connect Session and returns a URL to redirect the end user to.
    The end user completes OAuth in their browser, then call POST /v1/connections/confirm.
    """
```

**Rules:**
- First line: what the endpoint does (imperative mood)
- Additional lines: context a consumer needs — what happens next, side effects, prerequisites
- Don't document request/response fields in the docstring — that's what models are for

### 2. Typed Response Models (Not Raw Dicts)

Never return raw dicts. Define a Pydantic model so the response schema appears in docs.

```python
# Bad — docs show no response schema
@router.get("/v1/connections/{id}")
async def get_connection(...):
    return {"id": conn.id, "status": conn.status}

# Good — docs show full response schema with field descriptions
class ConnectionResponse(BaseModel):
    id: str
    end_user_id: str
    provider: str
    status: str = Field(description="Connection status: active, error, deleting")
    created_at: datetime

@router.get("/v1/connections/{id}", response_model=ConnectionResponse)
async def get_connection(...) -> ConnectionResponse:
    ...
```

**Key points:**
- Set `response_model=` on the decorator so FastAPI validates AND documents the response
- Use `Field(description=...)` for non-obvious fields
- For lists: `response_model=list[ConnectionResponse]`

### 3. Typed Request Models with Field Descriptions

```python
class SyncRequest(BaseModel):
    connection_id: str = Field(description="UUID of the connection to sync")
    resources: list[str] = Field(
        description="Resources to sync (e.g., ['tickets', 'articles'])"
    )
```

Use `Field` for:
- Non-obvious field names
- Fields with constraints (`ge=1`, `le=1000`)
- Fields with default values that need explanation
- Enum-like string fields (list the valid values)

### 4. Status Codes and Error Responses

Declare non-200 status codes so they appear in docs:

```python
@router.post(
    "/v1/syncs/{id}/trigger",
    status_code=202,
    responses={409: {"description": "Sync already running"}},
)
async def trigger_sync(...):
    """Trigger a sync run in the background."""
```

### 5. Router Tags for Grouping

Group related endpoints with tags so Swagger UI organizes them into sections:

```python
router = APIRouter(tags=["Connections"])
```

This replaces the need for section headers in a manual API reference.

### 6. Paginated List Responses

For list endpoints, use a consistent wrapper:

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
```

This documents the pagination contract once, consistently.

## Verification

After creating or modifying endpoints, check the auto-docs:

1. Start the server
2. Open `/docs` (Swagger UI) or `/redoc`
3. Verify:
   - Endpoint has a clear description (from docstring)
   - Request body schema shows all fields with descriptions
   - Response schema shows all fields with types
   - Status codes are documented
   - Endpoints are grouped logically (tags)

If a consumer can't understand the endpoint from `/docs` alone, the docstring or model is missing something.

## Quick Reference

```
1. Docstring   — what it does, context, side effects
2. Response    — Pydantic model with Field(description=...)
3. Request     — Pydantic model with Field(description=...)
4. Status      — response_model=, status_code=, responses={}
5. Tags        — APIRouter(tags=["Section"])
6. Verify      — check /docs after changes
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Return raw dicts | Define a response model |
| Write a separate api-reference.md | Let FastAPI generate docs from code |
| Document fields in the docstring | Use `Field(description=...)` on the model |
| Skip the docstring ("it's obvious") | Write it — `/docs` is your public contract |
| Use `Any` or `dict` as response type | Define a typed model, even for simple responses |
| Maintain two sources of truth | Code is the docs — update the code, docs update automatically |
