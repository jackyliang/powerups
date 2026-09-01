---
name: marketing-surfaces
description: Ship the public-facing side of a user-visible feature — docs/help page, blog or changelog post, screenshots, pricing tier line, landing copy, email, and social. Run the triage on EVERY feature, bug fix, or change (best-practices finishing sequence, bug-fix Step 9, plan-driven-development's post-completion audit), and directly whenever asked to announce, document, or promote something that shipped.
---

# Marketing Surfaces

## Overview

In-repo docs (`docs/`, `CLAUDE.md`, `CHANGELOG.md`) are for whoever maintains the code. They do nothing for the person deciding whether to buy, or trying to turn the feature on. The public site is a separate repo with its own conventions, so it gets its own explicit steps — otherwise it is always the thing that never happens.

"Nobody outside the codebase knows this exists yet" is not a completed feature.

## When to Use

- **Every feature, bug fix, or change** — the finishing sequence in `powerups:best-practices` (and `powerups:bug-fix` Step 9, `powerups:plan-driven-development`'s post-completion audit) runs the triage below. Most changes end at triage with "no public surface affected"; the point is that the question gets asked every time, not that every change ships a post.
- Asked to announce, document, or promote anything customers can see
- An existing surface is wrong: stale docs page, missing pricing tier line, a screenshot of a screen that has since changed

### Triage — run for every change

For each surface below, answer one of: **UPDATE** (say which page/post), **NEW** (say what), **N/A** (one-line reason), or **UNSURE**. Internal refactors, infra, and dev-only tooling are N/A across the board — say so in one line and move on.

If any surface is UNSURE — a fix that changes visible behavior a help article describes, a small feature that may or may not deserve a post, a limit that changed — **ask the user** with your recommendation instead of deciding silently. The cost of asking is one message; the cost of a stale public page is a customer who was told the wrong thing.

## Review and delivery rules

1. **Draft first, PR second.** Before opening any PR, share the proposed text inline with the user — the full docs/help article body, the post, the pricing line, the email, the in-app copy — plus the screenshots. Wait for approval or edits. Never open a marketing PR the user has not seen the words of.
2. **Separate PRs from the feature.** Marketing work never rides in the feature or bug-fix PR. Each lands as its own PR (on the marketing repo, or via the help-center API), so it can be reviewed and merged on its own schedule. The one exception is the `CHANGELOG.md` entry from `powerups:change-log`, which stays in the feature PR.
3. **Gate on live.** Do not merge or publish a surface before the feature is in production (see below).

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

1. **Docs/help page** — the FULL installation and usage flow: how a customer turns the feature on, every step of using it, and its limits. Technical level per the rule above. Use the product's own name for its docs surface (check the marketing repo/CLAUDE.md). Only create a NEW article for large features; ask the user if unsure whether the feature warrants its own article or belongs in an existing one. Bug fixes usually hit this surface, not a post: if an existing help/knowledge article describes the old behavior, it needs the UPDATE.
2. **Blog/changelog post** — the announcement, following the site repo's own writing pipeline or skill if it has one. Non-technical. Keep it SHORT: highlights only, and link the docs page for the full installation and usage flow — the blog never duplicates the docs.
3. **Screenshots** — the real feature, captured from the running app via `powerups:mockups`, embedded in both the post and the docs page.
4. **Pricing page** — only if the feature is plan-gated; name the tier it needs. The tier is a factual claim customers hold you to.
5. **Feature/landing copy** — only when the feature is a selling point, not for every change.
6. **Build and preview locally** — confirm generated files regenerated, and that links, images, and front matter render.
7. **Email announcement** — if the repo has a send pipeline (e.g. a broadcast script), draft it in `powerups:qq` style: short, one idea, one link to the live post. Send after the post is live.
8. **Social post** — if the repo/user has that pipeline: LinkedIn in broetry (one sentence per paragraph), X under 280 characters. Draft from the post, never from the PR description.
9. **In-app copy** — instructional text inside the product that describes the changed behavior: setup steps in a settings slide-out or integration panel (e.g. the Slack integration's setup instructions), onboarding hints, empty states, tooltips, help links. Grep the app for the feature name and the old wording. This is the surface bug fixes most often stale; it lives in the product repo, so it still ships as its own PR, not inside the fix.

**Screenshots are not optional for anything with a UI.** A post describing a screen nobody can see reads like a press release; one showing the actual screen is the whole point. `powerups:mockups` owns how our images are made (raw CDP capture of the element, then the Shots.so recipe) — never hand-crop a desktop screenshot or invent a background. Commit exports where the site keeps its images, matching the existing naming and directory convention. Rules: real or realistically seeded data, never lorem and never an empty state pretending to be full; no secrets, keys, customer PII, or internal-only orgs in frame; capture the before/after pair when the feature changes an existing screen. If a step genuinely can't be shown (CLI/API-only), use a terminal capture or a fenced code block rather than skipping the visual.

## Output

The work lands as its own PR on the marketing repo, separate from the feature PR, opened only after the user has approved the drafted text. Report each surface with its status and evidence, and link the PR. When triage found nothing, the report is the triage itself — one line per surface, all N/A with reasons:

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
9. In-app copy:     DONE — Connectors slide-out setup steps updated (answer-hq #NN)
PR: ../answerhq-web #14
```
