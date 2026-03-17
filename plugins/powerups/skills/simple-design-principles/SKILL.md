---
name: simple-design-principles
description: Use when writing any user-facing text (UI labels, toasts, errors, empty states) or choosing UI components. Ensures plain language, consistent component usage, and human-first design.
---

# Simple Design Principles

## Overview

Rules for writing user-facing copy and choosing UI components. Apply these whenever a code change touches anything the user sees — labels, toasts, error messages, empty states, buttons, modals, tooltips.

`best-practices` and `plan-driven-development` invoke this automatically for UI work, but you can use it directly for copy-only changes.

## Copy & UI Text

Write for business users, not developers. A high schooler should understand every word.

### Language Rules

- **No technical jargon.** Never use: "disabled", "enabled", "configured", "integration", "endpoint", "triggered", "initialized", "synced", "deployed"
- **Plain human phrasing:**
  - "turned on/off" not "enabled/disabled"
  - "set up" not "configured"
  - "something went wrong" not "request failed"
  - "connected" not "integration active"
- **Focus on impact and outcomes.** "Save time" not "Execute batch process". Explain the *why* or benefit, not just the *what*.
- **Lead with what the user can do**, not what went wrong. "Try again" beats "Request timed out".
- **No implementation details in copy.** Users don't care about databases, tokens, or sync jobs — they care about their data and actions.

### Component-Specific Copy

| Component | Rule | Example |
|-----------|------|---------|
| **Toast messages** | Short and conversational. 1 short sentence max for the description. | "Website added" / "Changes saved" |
| **Button labels** | Action-oriented and specific. Say what clicking does. | "Add website" not "Submit". "Turn on tickets" not "Enable tickets". |
| **Empty states** | Encouraging. Tell the user what to do next, not describe system state. | "Add your first website to get started" not "No websites configured" |
| **Error messages** | Blame the system, not the user. Suggest a next step. | "Something went wrong. Try again." not "Invalid request payload" |
| **Tooltips** | One sentence explaining why this matters or what it does. | "Visitors will see this name in the chat window" |
| **Page titles** | Plain text, no icons in h1. Describe what the page is for. | "Knowledge vault" not "Knowledge vault" |
| **Descriptions** | One line under the title explaining what the user can do here. | "Add websites and articles your assistant can search" |

## UI Component Consistency

Use the project's UI library consistently. Don't mix custom implementations with library components.

### Component Selection

- **Tooltips** — for hover hints and explanations
- **Dialog** — for modals (confirmations, forms that block the page)
- **Sheet** — for slide-out panels (detail views, secondary forms)
- **AlertDialog** — for destructive action confirmations (delete, disconnect)
- **Follow existing patterns** in the project's component directory before creating custom components

### Visual Rules

- Action buttons: use the project's primary color (e.g., indigo-500)
- Destructive actions: use red with AlertDialog confirmation
- Loading states: spinner with muted color
- Section headings within cards: `text-lg font-semibold`
- No icons in page-level h1 titles

## Project-Specific Rules

This skill provides generic design principles. **Always check the project's CLAUDE.md for additional project-specific UI instructions** — these take precedence. Projects may define:
- Page layout conventions (e.g., specific Card/CardHeader patterns for dashboard pages)
- Color schemes (e.g., primary action color, destructive action color)
- Required footer components
- Loading state patterns
- Specific component library configurations

## Quick Reference

```
Copy:
- No jargon, no tech words
- Short sentences, one idea each
- Lead with what to do, not what went wrong
- Apple-like tone: confident, helpful, warm

Components:
- Use library components, not custom
- Dialog for modals, Sheet for panels
- AlertDialog for destructive actions
- Follow existing patterns in the codebase
```
