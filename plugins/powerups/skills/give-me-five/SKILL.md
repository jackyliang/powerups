---
name: give-me-five
description: Use when the user wants to compare multiple UI/UX design directions side by side before choosing. Generates 5 meaningfully distinct variants of the same screen/component in parallel (one subagent per variant), each reachable via ?style=1...5 in the URL. Supports iteration — calling again on a chosen style produces 5 refined variants within that direction.
---

# Give Me Five

## Overview

The user is not a designer but knows good design when they see it. Instead of generating one design and asking "what do you think?", produce **five meaningfully distinct variants** at once so they can compare and pick. Each variant lives at the same URL with a different `?style=N` parameter (1–5).

This skill is an orchestration layer on top of `frontend-design:frontend-design`. The main agent brainstorms directions and dispatches; five parallel subagents each build one variant; the main agent assembles the result and hands off URLs.

## When to Use

- User asks for a UI/UX design and wants options before committing
- User says "give me five", "show me variants", "let me pick from a few", or similar
- After an initial design, user picks one and says "iterate" / "more like this" / "give me five in the style of #2"
- Any time picking among parallel designs is faster than describing what they want in words

Do NOT use when:
- The user has a clear, specific design in mind already
- The work is functional/backend with no visual surface
- A single iteration would be cheaper than five (e.g., a one-line copy change)

## How It Works

### 0. Create a feature branch

Defer to `powerups:best-practices` — branch before any work. Five experimental variants on `main` is risky; a branch lets you delete the four losers cleanly after the user picks, and reverts cleanly if you abandon the exploration.

```bash
git checkout -b feat/{description}-give-me-five
```

### 1. Brainstorm 5 distinct directions BEFORE dispatching

Generating 5 designs that are all the same vibe with different button colors is useless. Before launching any subagent, name the 5 directions on different axes. Good axes to vary on:

- **Layout** — single-column / multi-column / dashboard / full-bleed / card-grid
- **Density** — airy & minimal vs dense & data-rich
- **Aesthetic** — editorial / brutalist / glassmorphism / soft-neumorphic / terminal-monospace / magazine
- **Color** — monochrome / vibrant accent / gradient-led / dark-first / pastel
- **Typography** — serif-led editorial / sans-only utilitarian / display + body mixed / monospace-heavy
- **Hierarchy** — hero-led / list-led / grid-led / narrative-led
- **Motion** — static / hover-rich / animation-forward / micro-interactions

A strong set of 5 spans at least 3–4 of these axes — go **wide** on the first call. Name each direction in one phrase before dispatching:

> Style 1: Editorial magazine — serif display, generous whitespace, narrative hierarchy
> Style 2: Dense ops console — monospace, tight grid, terminal aesthetic, data-rich
> Style 3: Soft glassmorphism — frosted panels, gradient backdrops, hover motion
> Style 4: Brutalist — heavy borders, raw monospace + display, black/white + one accent
> Style 5: Playful — rounded shapes, big illustrations, pastel palette, bouncy micro-interactions

Output this list to the user before dispatching. (No approval needed unless they redirect.)

### 2. Dispatch 5 parallel subagents — one per variant

Each variant is built by its own `general-purpose` subagent. **All 5 launched in a single message with 5 Task tool calls in parallel** — sequential dispatch is 5× slower for no gain. The main agent's job is brainstorming, dispatch, and assembly; the subagents do the design work.

**The main agent does NOT design.** It writes `index.tsx` (the router) and orchestrates. Letting a subagent own the router risks two agents editing the same file.

**File layout:**

```
components/MyPage/
├── index.tsx            # router: reads ?style, dispatches to Style1..Style5  (main agent writes)
├── Style1.tsx           # subagent 1
├── Style2.tsx           # subagent 2
├── Style3.tsx           # subagent 3
├── Style4.tsx           # subagent 4
└── Style5.tsx           # subagent 5
```

Each subagent prompt must be **self-contained** — subagents don't see the main conversation. Include:

- The direction (one-phrase name + axes — e.g., "Style 3: Soft glassmorphism — frosted panels, gradient backdrops, hover motion")
- The exact file to write (e.g., `components/MyPage/Style3.tsx`)
- The props/data shape the variant must accept (identical across all 5 — variants vary on design only, not content)
- The content/copy to render (paste it in, don't reference)
- Explicit instruction to invoke `frontend-design:frontend-design` before writing code
- Hard constraint: produce **only** this one variant file; do not touch the router or other variants
- What to return: file path + 1-line summary of key design choices

**Example subagent prompt:**

```
Build Style 3 of a 5-variant comparison set for the user dashboard page.

Direction: Soft glassmorphism — frosted panels with backdrop-blur, subtle
gradient backdrops, generous hover motion, rounded-2xl, pastel accent palette.

Write to: components/UserDashboard/Style3.tsx
Props (same across all 5 variants):
  { user: User, stats: Stats, recentActivity: Activity[] }

Content to render (same across all 5): [paste exact copy + data here]

Quality requirements:
- Invoke `frontend-design:frontend-design` before writing code
- Production-grade — distinctive, not generic AI aesthetic
- Full, polished design — no half-built stubs
- Self-contained in Style3.tsx — do NOT modify other Style*.tsx or index.tsx

Return: the file path and a 1-line summary of the key design choices.
```

**Main agent's sequence:**

1. Write `index.tsx` (router that reads `?style` and dispatches to `Style1..Style5`, defaulting to `1`)
2. Launch all 5 subagents in **one message** (parallel)
3. Wait for all to complete
4. Verify each variant file actually exists on disk — don't trust summaries
5. Start the dev server
6. Hand off the numbered URLs (step 3 below)

### 3. Hand off the URLs

Present the URLs in a numbered list with the one-phrase name of each style:

```
Style 1 (Editorial magazine):   http://localhost:3000/page?style=1
Style 2 (Dense ops console):    http://localhost:3000/page?style=2
Style 3 (Soft glassmorphism):   http://localhost:3000/page?style=3
Style 4 (Brutalist):            http://localhost:3000/page?style=4
Style 5 (Playful):              http://localhost:3000/page?style=5
```

The user clicks through, compares, picks.

## Iteration Mode

When the user picks one and asks for more variants (e.g., "give me five in the style of #2"):

1. **Anchor** the chosen variant's design language: aesthetic, typography family, color palette, layout pattern. These are fixed for this iteration cycle and must appear verbatim in **every** subagent prompt this round so all 5 variants share the chosen DNA.
2. **Vary** within that anchor on smaller axes: density, accent shade, micro-interactions, hierarchy details, illustration vs. iconography, hover behaviors, spacing rhythm.
3. **Re-dispatch** 5 parallel subagents with the new narrower assignments. Same parallelization rule applies.
4. **Replace** `Style1.tsx..Style5.tsx` with the new variants — don't accumulate. The URL pattern stays `?style=1..5`. If the user wants to keep the previous winner around, save it as `StyleN-vN.tsx` or commit it on a git tag; otherwise let it go.
5. **Re-name each variant** with its differentiator. After 2–3 iteration cycles the names get specific: "Style 2 — denser table, no hover animation, bigger numerals".

Iteration is convergent — each cycle narrows the design space. The first call explores; subsequent calls refine.

## Quality Rules

- Every subagent must invoke `frontend-design:frontend-design` — variants need to be polished, not just varied.
- No filler variants. If you can't think of 5 strong directions, generate 3 or 4 and tell the user. Padding the set with weak options wastes their time.
- Variants should be obvious at a glance which is which — if the user can't tell two apart, they're not different enough.
- Keep the underlying data/content identical across variants — the comparison is about design, not content.
- All 5 variants must be reachable. A broken `style=4` defeats the purpose. Verify each file exists after subagents return.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generating 5 variants that are basically the same design with different colors | Vary on 3–4 design axes, not 1. Name the directions before dispatching. |
| Dispatching subagents sequentially instead of in parallel | All 5 Task tool calls go in a single message. Sequential is 5× slower and there's no dependency between variants. |
| Subagent prompt that says "see above" or "same approach as before" | Each subagent is fresh — paste the direction, file path, props, content, quality bar, and constraints into every prompt. No references to context they can't see. |
| Letting a subagent write the router | The router (`index.tsx`) is the main agent's job. Subagents only produce their assigned variant file. Two agents editing the router = merge conflicts. |
| Main agent doing design work | Main agent brainstorms directions and orchestrates; subagents design. If the main agent is writing CSS, something is wrong. |
| Skipping `frontend-design` in subagent prompts | Every subagent invokes it — variants need to be polished, not just varied. |
| Half-implementing some variants (e.g., only the hero) | Every variant is a full, polished design. Otherwise the comparison is unfair. |
| Trusting subagent summaries without verifying files exist | After all 5 return, check each file on disk. Summaries describe intent, not reality. |
| Not telling the user how to switch between them | Always hand off the numbered URLs with the variant names, and make sure the dev server is running. |
| Iterating without anchoring to the chosen style | In iteration mode, the aesthetic/typography/palette are FIXED. Paste the anchor into every subagent prompt this round. |
| Keeping previous variants around after iteration | Replace 1–5 each cycle. Past variants are noise unless the user explicitly asks to keep one. |
| Skipping the feature branch | Defer to `powerups:best-practices`. Five experimental variants on main is asking for a mess. |
