# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Tracks progress across context windows. |
| **database-branching** | Fork your database like a git branch. Develop on the fork, merge migrations back, delete the fork. (Ghost DB / TimescaleDB only) |

## Install

### As a plugin (recommended)

```bash
# Add the marketplace
/plugin marketplace add jackyliang/powerups

# Install
/plugin install powerups@powerups
```

Skills will be available as:

```
/powerups:test-driven-development
/powerups:plan-driven-development
/powerups:database-branching
```

### Manual (symlink)

If you prefer to manage it yourself:

```bash
git clone https://github.com/jackyliang/powerups.git "$HOME/Code/powerups"
mkdir -p "$HOME/.claude/skills"
for skill in test-driven-development plan-driven-development database-branching; do
  rm -rf "$HOME/.claude/skills/$skill"
  ln -sf "$HOME/Code/powerups/skills/$skill" "$HOME/.claude/skills/$skill"
done
```

## License

MIT
