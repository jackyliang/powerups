# CLAUDE.md

## Version Bumping — MANDATORY

When ANY file under `plugins/powerups/skills/` or `plugins/powerups/.claude-plugin/` is changed, you MUST bump the version in BOTH of these files before committing:

1. `plugins/powerups/.claude-plugin/plugin.json` — the plugin version (controls local cache refresh)
2. `.claude-plugin/marketplace.json` — the marketplace version (controls marketplace discovery)

Both files must have the **exact same version string**. Use semver: bump patch for small changes, minor for new skills or significant behavior changes.

**Why:** Claude Code caches plugins by version. If the version doesn't change, projects using powerups will keep running the stale cached version even after you push updates. This has caused repeated issues where new/updated skills don't show up.

## Repo Structure

```
powerups/
├── .claude-plugin/
│   └── marketplace.json        ← marketplace manifest (has version)
├── plugins/powerups/
│   ├── .claude-plugin/
│   │   └── plugin.json         ← plugin manifest (has version)
│   └── skills/
│       ├── best-practices/
│       ├── bug-fix/
│       ├── change-log/
│       ├── database-branching/
│       ├── plan-driven-development/
│       ├── self-documenting-apis/
│       ├── simple-design-principles/
│       ├── test-driven-development/
│       └── update-docs/
└── README.md
```

## Updating README — MANDATORY

When adding, removing, or significantly changing a skill, you MUST update the skills table in `README.md` to match. This is part of every commit that changes skills, not a separate step.

**Why:** The README is the first thing users see on GitHub. If it lists outdated skills or missing descriptions, users won't know what's available. This has happened repeatedly — new skills were added but never listed in README.
