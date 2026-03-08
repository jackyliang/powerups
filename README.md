# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **best-practices** | The baseline for every code change. Worktrees/branches (never main), investigate before building, ask before assuming, TDD, DRY, frontend-design for UI, update-docs when done, lint before committing. |
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Builds on best-practices. Tracks progress across context windows with multi-agent coordination. |
| **database-branching** | Fork your database like a git branch. Develop on the fork, merge migrations back, delete the fork. (Ghost DB / TimescaleDB only) |
| **update-docs** | Sync all documentation after completing a feature. Finds stale content across CLAUDE.md, README, public skills/plugins, and downstream project docs. |

## Install

In Claude Code, run:

```
/plugin marketplace add jackyliang/powerups
/plugin install powerups@powerups
```

Skills will be available as:

```
/powerups:best-practices
/powerups:test-driven-development
/powerups:plan-driven-development
/powerups:database-branching
/powerups:update-docs
```

## License

MIT
