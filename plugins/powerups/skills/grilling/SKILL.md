---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. Invoked by plan-driven-development with a 5-10 question cap.
---

# Grilling

Interview the user relentlessly about every aspect of the plan, decision, or idea until you reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

**Every question comes with suggested answers** — 2–4 plausible options, with the one you recommend marked and listed first. The user picks or overrides; they should never face a blank open-ended prompt. Prefer the `AskUserQuestion` tool when available (put the recommended option first, labeled "(Recommended)"); otherwise list the options inline.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking. The *decisions* are the user's — put each one to them and wait for their answer.

Do not act until the user confirms you have reached a shared understanding.

## Question budget

By default grilling is relentless — as many questions as the decision tree needs. When another skill invokes this with a cap (`powerups:plan-driven-development` caps it at 5–10 questions), ask only the highest-leverage questions: the ones whose answers change what gets built. Stop early once the open decisions are resolved, and state any remaining assumptions you're proceeding on.

## Credit

Adapted from [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) by Matt Pocock (MIT).
