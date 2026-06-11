---
name: user-research
description: Run PM-grade discovery before building any user-facing feature — problem statement, jobs-to-be-done, core flow, decision matrix. Output is a short brief with open decisions surfaced as explicit questions. Invoked by plan-driven-development and give-me-five.
---

# User Research

## Overview

Features fail more often from building the wrong thing than building the thing
wrong. This skill front-loads the thinking a good PM does before pixels or
code: who hires this feature, for what job, through what flow, with which
decisions locked and which deliberately deferred.

The output is a **discovery brief** the requester reads and reacts to. It is
short (one screen-ish), opinionated (every open decision has a recommended
default), and decision-forcing (ends with the 2–4 questions only the requester
can answer).

## When to Use

- A feature request arrives as a solution ("add a compare button") and the
  underlying problem hasn't been named
- Multiple plausible UX shapes exist and picking wrong is expensive to undo
- Before a design-variants round (each variant should embody the SAME
  job analysis, varying only on aesthetics/layout)

**Invoked by other powerups skills:**
- `powerups:plan-driven-development` runs this BEFORE writing the plan, whenever
  the feature is user-facing — the discovery brief feeds the Context and Design
  sections and surfaces the decisions that become plan questions.
- `powerups:give-me-five` runs this BEFORE brainstorming directions — all five
  variants must embody the same job analysis, so the research happens once up front.

Skip it when: the change is mechanical (rename, restyle, bugfix), the flow is
already industry-standard (login form), or the requester has already specified
the exact behavior and owns the consequences.

## The Method

Work through the four artifacts below IN ORDER — each feeds the next. Keep
every artifact table-shaped and scannable; prose only where a table can't
carry the nuance.

### 1. Problem statement (one sentence)

Name the user's problem without mentioning the feature. Test: a competitor
could read it and build a different solution to the same sentence.

> Weak: "Users want to compare models." (names the mechanism)
> Strong: "Users can't tell which model to trust for their task, so they're
> always guessing." (names the pain)

If you cannot write this sentence, stop and ask the requester what prompted
the request — usually there's a triggering incident that contains the answer.

### 2. Jobs-to-be-done table

Enumerate the distinct jobs a user would "hire" this feature for. 3–5 jobs is
typical; 1 means the feature may be a button not a feature; 7+ means scope
needs cutting.

| # | Job (verb phrase, user's voice) | Trigger moment | What "done" looks like | Frequency |
|---|---|---|---|---|
| J1 | "..." | the situation that makes them reach for it | the state where they stop | rare/periodic/constant |

Rules:
- Write jobs in the user's voice ("before I act on this, do others agree?"),
  not feature language ("run multi-model inference").
- **Trigger moment is the highest-leverage column.** Where the user is when
  the job arises dictates entry points: a job triggered mid-task needs an
  entry point in that task's context, not a new top-level screen.
- Frequency × stakes tells you what to optimize: frequent+low-stakes → speed;
  rare+high-stakes → confidence and legibility.

After the table, extract 1–3 **structural insights** — consequences the table
forces. ("J2 starts from an existing reply, so a message-level entry point
matters as much as a composer-level one.") These are the part the requester
actually remembers; don't skip them.

### 3. Core flow sketch

Draw the happy path as 3–4 stages, ASCII boxes, one line each. Annotate the
step that resolves the feature's hardest design tension — every feature has
one (for comparison UIs it's "what happens on the next turn?"; for wizards
it's "what if they leave halfway?"). If you can't name the tension, you
haven't found it yet — look at what happens AFTER the happy path ends.

```
entry (from JTBD triggers)  →  the work  →  the resolution
┌─────────────┐   ┌──────────────┐   ┌─────────────────────┐
│ ...         │ → │ ...          │ → │ the tension-resolver │
└─────────────┘   └──────────────┘   └─────────────────────┘
```

### 4. Decision matrix

Every axis where the design could plausibly go multiple ways gets a row.
This is the contract between you and the requester: silent assumptions are
the failure mode this artifact exists to kill.

| Decision | Options | v1 position | Why |
|---|---|---|---|
| ... | A / B / C | the recommendation | one line tying it to a JTBD row |

Rules:
- The "Why" column must reference the jobs ("J2 needs..."), not taste.
- Take a position on every row. A matrix of "it depends" is analysis theater.
- Mark rows where the requester might disagree — those become the questions
  in step 6.
- Typical axes: entry points, scale limits (how many / how much), what
  happens next-turn/next-visit, persistence, defaults, what's deliberately
  deferred to v2.

### 5. Hand off: force the decisions

End by asking the requester ONLY the decisions that genuinely change what
gets built (2–4 max), each with the recommended option marked. Everything
else proceeds on your stated defaults. If an interactive question tool is
available, use it; otherwise list the questions with defaults that apply
if unanswered.

Then STOP. Do not start designing or building until the requester answers —
the entire point of discovery is that these answers reshape the work.

## Quality Bar

- The whole brief fits in roughly one screen of reading; tables over prose
- Every recommendation traces to a JTBD row — if a decision cites no job,
  either the decision is arbitrary or a job is missing
- Ground claims in evidence available to you (codebase, APIs, prior user
  statements) rather than invented personas; when you assert a constraint
  (e.g. "4 columns is the readable max at min window width"), it should be
  checkable
- The requester should be able to disagree CHEAPLY: positions are explicit,
  one-line-justified, and reversible at this stage

## Common Mistakes

| Mistake | Fix |
|---|---|
| Starting from the requested mechanism ("add compare") | Rewrite as a problem statement first; the mechanism is one candidate solution |
| Personas instead of jobs | Jobs are situational ("when X happens, I need Y"), not demographic |
| Skipping the trigger-moment column | Entry points come from triggers; without them you'll default to a new top-level screen nobody finds |
| A decision matrix with no positions | Recommend on every row; the requester edits, not authors |
| Asking the requester every question | Only decisions that change the build; defaults for the rest |
| Sliding into implementation in the same breath | Discovery ends at the hand-off questions; building starts after answers |
| Analysis longer than the feature spec | One screen. If it's longer, the insights are diluted |
