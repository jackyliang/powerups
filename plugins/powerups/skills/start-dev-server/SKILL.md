---
name: start-dev-server
description: Use as a background subagent to start dev servers in a worktree. Handles symlinks, kills existing processes, starts servers, and verifies the correct code is running. Detects project (answerhq or sync_hq) from cwd automatically.
---

# Start Dev Server (Worktree)

## Overview

Start dev servers when working in a git worktree. Worktrees share dependencies (venv, node_modules, .env) with the main repo via symlinks. This skill handles creating those symlinks, killing any existing server on the port, starting the server, and verifying the cwd is correct.

**Run this skill as a background subagent** (`run_in_background: true`) so the main conversation is not blocked.

## When to Use

- Working in a git worktree and need to start dev servers
- After creating a new worktree (symlinks need to be set up)
- When switching between worktrees (need to kill old server and start new one)

## When NOT to Use

- Working in the main repo (not a worktree) — use the commands from the project's CLAUDE.md directly
- Production deployments

## Step 1: Detect Worktree and Project

```bash
git rev-parse --git-common-dir
```

If the result is `.git`, you are NOT in a worktree — abort and tell the user to use the CLAUDE.md commands directly.

The common dir path tells you which project you're in:
- Contains `answerhq` → answerhq project
- Contains `sync_hq` → sync_hq project

Extract the worktree path from cwd. Extract the main repo root by stripping `/.git` from the common dir.

## Step 2: Set Up Symlinks

Create symlinks with `ln -sf` (idempotent — safe to re-run).

**answerhq:**
```bash
ln -sf ~/Code/answerhq/chat-ui/.env.local <worktree>/chat-ui/.env.local
ln -sf ~/Code/answerhq/chat-ui/node_modules <worktree>/chat-ui/node_modules
```

**sync_hq:**
```bash
ln -sf ~/Code/sync_hq/.env <worktree>/.env
ln -sf ~/Code/sync_hq/.venv <worktree>/.venv
```

## Step 3: Kill Existing Processes

```bash
lsof -i :<port> -t | xargs kill 2>/dev/null; sleep 1
```

## Step 4: Start Servers

Use `run_in_background: true` with the Bash tool.

**answerhq** (two servers):

| Component | Port | Start Command |
|-----------|------|---------------|
| Backend | 8000 | `cd <worktree>/chat-ui && ~/Code/answerhq/chat-ui/venv/bin/python3 -m uvicorn api.index:app --reload` |
| Frontend | 3000 | `cd <worktree>/chat-ui && npm run next-dev` |

**sync_hq** (one server):

| Component | Port | Start Command |
|-----------|------|---------------|
| Backend | 8001 | `cd <worktree> && ~/Code/sync_hq/.venv/bin/uvicorn sync_hq.main:app --reload` |

## Step 5: Verify CWD

After the server starts, verify it is running from the worktree:

```bash
lsof -p $(lsof -i :<port> -t | head -1) | grep cwd
```

The cwd should show the worktree path, NOT the main repo. If it shows the main repo, kill and restart.

## Quick Reference

| Project | Servers | Ports | Symlinks |
|---------|---------|-------|----------|
| answerhq | Backend + Frontend | 8000, 3000 | `.env.local`, `node_modules` |
| sync_hq | Backend only | 8001 | `.env`, `.venv` |
