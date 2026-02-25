# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Tracks progress across context windows. |
| **database-branching** | Fork your database like a git branch. Develop on the fork, merge migrations back, delete the fork. (Ghost DB / TimescaleDB only) |

## Install

In Claude Code, run:

```
/plugin marketplace add jackyliang/powerups
/plugin install powerups@powerups
```

Skills will be available as:

```
/powerups:test-driven-development
/powerups:plan-driven-development
/powerups:database-branching
```

## License

MIT
