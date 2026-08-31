# powerups

Reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for disciplined software development.

## Skills

| Skill | Description |
|-------|-------------|
| **best-practices** | The baseline for every code change. Branching (never main), investigate before building, ask before assuming, TDD, DRY, simplify after implementation, update-docs when done, lint before committing. |
| **test-driven-development** | Write failing tests first against real infrastructure. No mocks. Red-green-refactor. |
| **plan-driven-development** | Versioned plan files in `plans/` for multi-milestone features. Builds on best-practices. Skill audit before planning, scenario map for complex changes, a marketing-surfaces milestone for user-visible features, plan-vs-reality audit before PR, multi-agent coordination across context windows. |
| **marketing-surfaces** | Ship the public side of a user-visible feature, one verified step per surface: docs/help page, blog or changelog post, `mockups` screenshots, pricing tier line, landing copy, local preview, email, social. Non-technical by default; technical only for developer-reference pages (API/MCP docs), which the launch post links with a "send this to your engineer" hand-off. Invoked by plan-driven-development's post-completion audit. |
| **user-research** | Product-manager-grade discovery before building a user-facing feature — problem statement, jobs-to-be-done, core flow, and a decision matrix. Output is a short brief the requester approves, with open decisions surfaced as explicit questions. Invoked by plan-driven-development and give-me-five. |
| **bug-fix** | Strict 10-step protocol for fixing bugs. Reproduce first, then fix. Each step gates on success criteria. Supports Chrome browser debugging for UI bugs. |
| **mockups** | The one way marketing images get made: capture the UI raw over CDP (`capture.py` ships with the skill), then composite in Shots.so with the house recipe — Mystic gradient, Glass Light rim, 4:3. Refuses to capture keys (even masked), emails or your own instance URLs, and rewrites the DOM to a generic example first. Needs an agent with a browser it can drive. Invoked by plan-driven-development for any screenshot. |
| **change-log** | Log each feature or fix in `CHANGELOG.md` using plain, business-user-friendly language. Powers the product updates blog. |
| **simple-design-principles** | Rules for user-facing copy and UI components. Plain language, no jargon, consistent component usage. |
| **give-me-five** | Generate 5 meaningfully distinct UI/UX variants of the same screen in parallel — one subagent per variant — each reachable via `?style=1...5`. Iterate on a chosen style to refine within that direction. |
| **self-documenting-apis** | Ensure FastAPI endpoints have docstrings, typed response/request models, and proper status codes so auto-generated docs are the single source of truth. |
| **update-docs** | Sync all documentation after completing a feature. Finds stale content across CLAUDE.md, README, the marketing/public site (docs, pricing, blog), public skills/plugins, and downstream project docs. |
| **drift-audit** | Run before the PDD post-completion audit. Reconciles shipped code vs the plan in both directions — additive drift (unplanned things that landed) and subtractive drift (orphan files, completed Post-MVP items, stale TODOs, dead redirect stubs). |
| **qq** | Quick-question mode. Ultra-short answers and drafts in ASD-STE100 Simplified Technical English. Texts, social posts, and emails under 480 characters (280 per tweet for X) — no greetings, sign-offs, preamble, or em-dashes. |

## Install

In Claude Code, run:

```
/plugin marketplace add jackyliang/powerups
/plugin install powerups@powerups
```

### Devin

Nothing to install. `.agents/skills/` in this repo is a generated mirror of
`plugins/powerups/skills/`, and Devin indexes `.agents/skills/<name>/SKILL.md`
across connected repos, so the skills are available in every Devin session
(`@skills:bug-fix`, `@skills:qq`, ...).

The mirror is regenerated and committed by the `Sync Devin skills` GitHub
Action on every push to `main` that touches the plugin skills. Run it by hand
with:

```
python3 scripts/sync-devin-skills.py
```

Edit skills only under `plugins/powerups/skills/` — `.agents/skills/` is
overwritten.

## License

MIT
