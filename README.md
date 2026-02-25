# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Tracks progress across context windows. |
| **database-branching** | Fork your database like a git branch. Develop on the fork, merge migrations back, delete the fork. (Ghost DB / TimescaleDB only) |

## Setup

Claude Code loads user-level skills from `~/.claude/skills/`. Each skill is a directory containing a `SKILL.md` file. The setup below clones this repo and symlinks the skills into that location so they stay in sync with `git pull`.

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- `git` available on `PATH`

### Install (copy-paste this entire block)

```bash
# Clone the repo (skip if already cloned)
[ -d "$HOME/Code/powerups" ] || git clone https://github.com/YOUR_USERNAME/powerups.git "$HOME/Code/powerups"

# Ensure the skills directory exists
mkdir -p "$HOME/.claude/skills"

# Symlink each skill — removes any existing file/directory at the target first
for skill in test-driven-development plan-driven-development database-branching; do
  rm -rf "$HOME/.claude/skills/$skill"
  ln -sf "$HOME/Code/powerups/skills/$skill" "$HOME/.claude/skills/$skill"
done
```

### Verify

After setup, confirm the symlinks point to the repo:

```bash
ls -la ~/.claude/skills/
```

Expected output (paths may differ):

```
test-driven-development -> /Users/you/Code/powerups/skills/test-driven-development
plan-driven-development -> /Users/you/Code/powerups/skills/plan-driven-development
database-branching      -> /Users/you/Code/powerups/skills/database-branching
```

Then open Claude Code. The skills should appear as slash commands:

```
/test-driven-development
/plan-driven-development
/database-branching
```

### Update

```bash
cd "$HOME/Code/powerups" && git pull
```

Symlinks mean the skills update in place — no re-linking needed.

### Uninstall

```bash
# Remove symlinks
for skill in test-driven-development plan-driven-development database-branching; do
  rm -f "$HOME/.claude/skills/$skill"
done

# Optionally remove the repo
rm -rf "$HOME/Code/powerups"
```

## License

MIT
