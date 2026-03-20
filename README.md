# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **best-practices** | The baseline for every code change. Branching (never main), investigate before building, ask before assuming, TDD, DRY, simplify after implementation, update-docs when done, lint before committing. |
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Builds on best-practices. Skill audit before planning, tracks progress across context windows with multi-agent coordination. |
| **bug-fix** | Strict 10-step protocol for fixing bugs. Reproduce first, then fix. Each step gates on success criteria. Supports Chrome browser debugging for UI bugs. |
| **change-log** | Log each feature or fix in `CHANGELOG.md` using plain, business-user-friendly language. Powers the product updates blog. |
| **simple-design-principles** | Rules for user-facing copy and UI components. Plain language, no jargon, consistent component usage. |
| **self-documenting-apis** | Ensure FastAPI endpoints have docstrings, typed response/request models, and proper status codes so auto-generated docs are the single source of truth. |
| **database-branching** | Fork your database like a git branch. Develop on the fork, merge migrations back, delete the fork. (Ghost DB / TimescaleDB only) |
| **update-docs** | Sync all documentation after completing a feature. Finds stale content across CLAUDE.md, README, public skills/plugins, and downstream project docs. |

## Install

In Claude Code, run:

```
/plugin marketplace add jackyliang/powerups
/plugin install powerups@powerups
```

## License

MIT
