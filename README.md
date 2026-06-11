# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **best-practices** | The baseline for every code change. Branching (never main), investigate before building, ask before assuming, TDD, DRY, simplify after implementation, update-docs when done, lint before committing. |
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Builds on best-practices. Skill audit before planning, scenario map for complex changes, plan-vs-reality audit before PR, multi-agent coordination across context windows. |
| **user-research** | Product-manager-grade discovery before building a user-facing feature — problem statement, jobs-to-be-done, core flow, and a decision matrix. Output is a short brief the requester approves, with open decisions surfaced as explicit questions. Invoked by plan-driven-development and give-me-five. |
| **bug-fix** | Strict 10-step protocol for fixing bugs. Reproduce first, then fix. Each step gates on success criteria. Supports Chrome browser debugging for UI bugs. |
| **change-log** | Log each feature or fix in `CHANGELOG.md` using plain, business-user-friendly language. Powers the product updates blog. |
| **simple-design-principles** | Rules for user-facing copy and UI components. Plain language, no jargon, consistent component usage. |
| **give-me-five** | Generate 5 meaningfully distinct UI/UX variants of the same screen in parallel — one subagent per variant — each reachable via `?style=1...5`. Iterate on a chosen style to refine within that direction. |
| **self-documenting-apis** | Ensure FastAPI endpoints have docstrings, typed response/request models, and proper status codes so auto-generated docs are the single source of truth. |
| **update-docs** | Sync all documentation after completing a feature. Finds stale content across CLAUDE.md, README, public skills/plugins, and downstream project docs. |
| **drift-audit** | Run before the PDD post-completion audit. Reconciles shipped code vs the plan in both directions — additive drift (unplanned things that landed) and subtractive drift (orphan files, completed Post-MVP items, stale TODOs, dead redirect stubs). |
| **qq** | Quick-question mode. Ultra-short answers and drafts. Drafted texts/messages and emails fit under 480 characters — no greetings, sign-offs, or preamble. |

## Install

In Claude Code, run:

```
/plugin marketplace add jackyliang/powerups
/plugin install powerups@powerups
```

## License

MIT
