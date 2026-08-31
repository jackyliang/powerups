---
name: marketing-surfaces
description: Ship the public-facing side of a user-visible feature — docs/help page, blog or changelog post, screenshots, pricing tier line, landing copy, email, and social. Invoked by plan-driven-development's post-completion audit, and directly whenever asked to announce, document, or promote something that shipped.
---

# Marketing Surfaces

## Overview

In-repo docs (`docs/`, `CLAUDE.md`, `CHANGELOG.md`) are for whoever maintains the code. They do nothing for the person deciding whether to buy, or trying to turn the feature on. The public site is a separate repo with its own conventions, so it gets its own explicit steps — otherwise it is always the thing that never happens.

"Nobody outside the codebase knows this exists yet" is not a completed feature.

## When to Use

- A user-visible feature shipped (invoked by `powerups:plan-driven-development` — its last milestone and post-completion checklist)
- Asked to announce, document, or promote anything customers can see
- An existing surface is wrong: stale docs page, missing pricing tier line, a screenshot of a screen that has since changed

Skip for internal refactors, infra, and dev-only tooling. Say so in one line and move on.

## Before writing anything

1. **Find the marketing repo** — a sibling checkout, or the `../` paths in `CLAUDE.md`.
2. **Read its conventions** — front-matter schema, image directory and naming, generated directories, a required post pipeline or writing skill. Follow the repo's pipeline; never hand-edit generated output.
3. **Gate on the feature being live.** A docs page for something not yet deployed is worse than no page.
4. **Pick the audience per surface** (below) before drafting a word.

## Audience — decide per surface, not per feature

Default: **write for a non-technical reader** — a support lead or a store owner, not an engineer. Run `powerups:simple-design-principles` over every text surface and treat it as a gate, not a suggestion:

- Lead with the customer's job ("answer refund questions without a human"), not the mechanism ("a tool-calling server over JSON-RPC")
- No protocol or architecture jargon in the title, intro, or headings — MCP, endpoint, schema, webhook, payload, LLM, RAG, vector, embedding, middleware. If a term is unavoidable, explain it once in customer words on first use
- Say what they can now do, not how it works
- Short sentences, present tense, second person

**The exception: developer-reference surfaces.** When the reader is the person doing the implementation — API reference, MCP/integration setup docs, SDK or webhook guides — technical writing is correct. Don't dumb those down.

The split for a developer-facing feature:
- **Launch blog / changelog / email / social → non-technical.** The buyer reads these.
- **API / MCP / integration docs → technical.** The engineer reads these.
- **Bridge them:** the non-technical post links the technical page with an explicit hand-off line — "Send this to your engineer," or "If you're the engineer: the setup details are here."

**When the right level is not obvious for a surface, ask before writing.** One question, with your recommendation, is cheaper than a rewrite. Never split the difference into something half-technical that serves neither reader.

## The surfaces

Each is a separate step, done and verified on its own. Do the ones that apply; state in one line why any is N/A.

1. **Docs/help page** — the FULL installation and usage flow: how a customer turns the feature on, every step of using it, and its limits. Technical level per the rule above. Use the product's own name for its docs surface (check the marketing repo/CLAUDE.md). Only create a NEW article for large features; ask the user if unsure whether the feature warrants its own article or belongs in an existing one.
2. **Blog/changelog post** — the announcement, following the site repo's own writing pipeline or skill if it has one. Non-technical. Keep it SHORT: highlights only, and link the docs page for the full installation and usage flow — the blog never duplicates the docs.
3. **Screenshots** — the real feature, captured from the running app via `powerups:mockups`, embedded in both the post and the docs page.
4. **Pricing page** — only if the feature is plan-gated; name the tier it needs. The tier is a factual claim customers hold you to.
5. **Feature/landing copy** — only when the feature is a selling point, not for every change.
6. **Build and preview locally** — confirm generated files regenerated, and that links, images, and front matter render.
7. **Email announcement** — if the repo has a send pipeline (e.g. a broadcast script), draft it in `powerups:qq` style: short, one idea, one link to the live post. Send after the post is live.
8. **Social post** — if the repo/user has that pipeline: LinkedIn in broetry (one sentence per paragraph), X under 280 characters. Draft from the post, never from the PR description.

**Screenshots are not optional for anything with a UI.** A post describing a screen nobody can see reads like a press release; one showing the actual screen is the whole point. `powerups:mockups` owns how our images are made (raw CDP capture of the element, then the Shots.so recipe) — never hand-crop a desktop screenshot or invent a background. Commit exports where the site keeps its images, matching the existing naming and directory convention. Rules: real or realistically seeded data, never lorem and never an empty state pretending to be full; no secrets, keys, customer PII, or internal-only orgs in frame; capture the before/after pair when the feature changes an existing screen. If a step genuinely can't be shown (CLI/API-only), use a terminal capture or a fenced code block rather than skipping the visual.

## Output

The work lands as its own PR on the marketing repo. Report each surface with its status and evidence, and link the PR:

```
Marketing surfaces:
1. Docs page:       DONE — /docs/drive-connector (technical: engineer sets this up)
2. Blog post:       DONE — /blog/answer-from-your-drive-files (non-technical, links docs)
3. Screenshots:     DONE — 4 mockups, before/after of the Connectors page
4. Pricing page:    DONE — Drive listed under Growth
5. Landing copy:    N/A — not a headline selling point
6. Local preview:   DONE — built clean, generated blog/ regenerated
7. Email:           DONE — broadcast sent to 412 subscribers, links the post
8. Social:          DONE — LinkedIn + X drafts in the PR description
PR: ../answerhq-web #14
```
