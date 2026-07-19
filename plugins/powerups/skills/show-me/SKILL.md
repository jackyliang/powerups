---
name: show-me
description: Use after implementing a change or opening a PR — proves the change works end-to-end by running the app, driving it in the browser, and recording an MP4 video as proof. The reviewer watches the recording and merges without pulling the branch.
---

# Show Me

## Overview

A post-implementation proof protocol. Instead of telling the reviewer "it works," show them: run the app, exercise exactly what changed, and capture a short recording (or terminal transcript for non-UI changes) that a reviewer watches and immediately thinks "yep, it works."

Inspired by Devin's testing-and-recordings workflow: Setup → Plan → Record → Deliver.

The proof is **scoped to the diff**. This is not a full regression pass — the test suite does that. This is a focused demonstration of the changed behavior.

## When to Use

- After completing a feature or bug fix, before or right after opening the PR
- User says "prove it works", "show me", "send me a recording", or "verify X works"
- As the final step of `powerups:plan-driven-development` or `powerups:bug-fix`, when the change is user-facing
- Any time a reviewer would otherwise have to pull the branch to verify behavior

**Not for:** pure refactors, dependency bumps, or changes with no observable behavior. Say so and skip instead of recording nothing meaningful.

## The Protocol

### Phase 1: Setup

Get the app running before any recording starts.

1. Read the diff to understand what needs demonstrating: `git diff main...HEAD` (or the PR diff via `gh pr diff`)
2. Start the app locally the way the project normally does (check README, `package.json` scripts, `Makefile`, docker-compose). Run it in the background and confirm it's serving before proceeding
3. If the flow needs credentials, seed data, or services that aren't available, ask the user for them **now** — never fake, stub, or screenshot around a login you can't complete
4. For UI proof, load the Chrome tools if deferred — one ToolSearch call for the full set including `gif_creator` — then call `tabs_context_mcp` and create a **new** tab

**Success criteria:** The app is running and you can reach the entry point of the changed behavior.

### Phase 2: Plan

Write a minimal test plan **derived from the diff** — 3–7 steps, one flow, only what changed.

- Each step is a concrete action with an expected observable result ("click Save → toast appears, row updates")
- Include the one edge case the diff exists to handle (the bug input, the new validation), not every edge case
- If the diff touches multiple independent flows, plan one recording per flow rather than one long meandering recording

State the plan in one short list before executing. Don't ask for approval — just record it so the deliverable can be checked against it.

**Success criteria:** A step list where every step maps to a line in the diff, and nothing in it is "general app smoke testing."

### Phase 3: Record

**UI changes** — record with `gif_creator`, deliver as MP4:

- Start capture **before** navigating to the flow; capture extra frames before and after each action so playback is smooth
- Execute the plan exactly. Pause briefly on the "proof moment" (the fixed output, the new element) so it's legible in playback
- Convert the captured GIF to MP4 before delivering — MP4 is far smaller and scrubs properly:
  ```bash
  ffmpeg -i flow.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" flow.mp4
  ```
  If `ffmpeg` isn't installed, deliver the GIF and say so — don't block the proof on a codec
- Name the file after the behavior, not the task: `login_error_message.mp4`, not `test.mp4`
- If a step fails, **stop recording and fix the app, not the plan**. Re-record from the top once fixed — a recording that skips the broken part is not proof

**Non-UI changes** (API, CLI, background job) — capture a terminal transcript instead:

- Run the demonstrating commands (`curl` the endpoint, invoke the CLI) and save the real input/output to a file
- Show the before-state where feasible (e.g. the error response on `main`, then the fix on the branch)

**Success criteria:** A recording or transcript where every planned step visibly succeeds.

### Phase 4: Deliver

1. Send the recording (or transcript) to the user with `SendUserFile`, captioned with a one-line pass/fail summary
2. Report the plan-vs-result: each step, what was expected, what the recording shows
3. If a PR exists, post the test plan and result as a PR comment (`gh pr comment`) so the reviewer has the summary next to the code
4. Stop the app and close the tab you created

**Success criteria:** The user has the file, and the summary honestly reflects what was and wasn't demonstrated.

## Rules

- **The diff defines the plan.** No drive-by exploration, no testing unrelated screens.
- **Never deliver a recording of a failure as if it passed.** If it fails, that's a finding — report it, fix it (via `powerups:bug-fix` if it's a real bug), then re-record.
- **Never fake the environment.** No hardcoded data, mocked endpoints, or commented-out auth to make the demo work. If the demo needs something you don't have, ask.
- **Keep it short.** A reviewer should get to "yep, it works" in under 30 seconds of playback. Cut setup and navigation dead time by starting recording close to the flow.
- **One flow per recording.** Multiple independent changes get multiple short recordings.

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Record the whole app "while you're at it" | Record only the flow the diff changed |
| Re-plan around a broken step mid-recording | Stop, fix the app, re-record from the top |
| Ship a recording where the key moment flashes by | Pause on the proof moment so it reads in playback |
| Mock the backend to make the UI demo work | Run the real stack; ask for missing credentials |
| Claim "verified" from a transcript that only shows the happy path you didn't change | Demonstrate the specific changed behavior, including its edge case |
| Skip proof on a non-UI change | Deliver a terminal transcript instead of a video |
