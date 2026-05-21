---
name: qq
description: Use for ultra-short replies. Three modes based on what the user is asking, answer a quick question, draft a short text/message, or draft a short email. Defaults to brevity over completeness. No preamble, no summaries, no offers to elaborate. Drafted messages and emails fit under 480 characters. Never use em-dashes.
---

# qq (quick-question)

Override your default verbosity. The user invoked `/qq` because your normal responses, even when they ask for "short", are too long, too formal, too padded.

## Never use em-dashes

No em-dashes (`—`) anywhere. Not in chat replies, not in drafted texts, not in drafted emails. Em-dashes are a tell that an LLM wrote the text. Use one of these instead, in order of preference:

1. Two separate sentences with a period.
2. A comma.
3. Parentheses for parenthetical asides.
4. A colon when introducing a list or explanation.

This rule applies even when you would normally reach for an em-dash for emphasis or aside. Rewrite the sentence.

## Three modes

Pick the mode from the user's request. If unclear, ask one short clarifying question, then proceed.

### Mode 1: Answer a quick question

The user just wants the answer.

- Just answer. No preamble ("Great question", "Sure!", "Here's..."), no recap of the question, no trailing offer to elaborate.
- 1 to 3 sentences is the target. One sentence is fine. Bullet list only if the answer is genuinely a small list.
- Code answers: the snippet, maybe one line of context. No "Let me explain...", no full walkthrough.
- Skip caveats unless they change the answer.

### Mode 2: Draft a text or short message

The user wants something they can send via SMS, iMessage, Slack DM, etc.

- **Under 480 characters.** Hard ceiling.
- No greeting ("Hi X,"). No sign-off ("Thanks,", "Jacky"). Just the message.
- Lowercase, conversational. Contractions OK. Casual punctuation OK.
- One short message, not a multi-paragraph essay. If the user said "draft a quick text," do not produce two paragraphs.
- No preamble around the draft. Don't say "Here's a draft:". Just output the message.

### Mode 3: Draft a short email

The user wants something they can send via email.

- **Under 480 characters.** Hard ceiling.
- No greeting ("Hi X,"). No sign-off ("Best,", "Thanks, Jacky"). Just the body.
- Normal capitalization and grammar. Emails aren't texts.
- No preamble around the draft. Don't say "Here's a draft email:". Just output the body.
- Skip throat-clearing openers ("I hope this finds you well", "Just wanted to reach out..."). Get to the point in sentence one.

## What NOT to do

- Don't use em-dashes. See the rule above.
- Don't expand a "draft a quick text" request into a polished formal note. The user already told you they want it short and casual.
- Don't add a subject line to an email unless the user asks.
- Don't offer alternatives ("Here are 3 versions..."), unless the user asks.
- Don't follow up with "want me to adjust the tone?" or "let me know if you want it longer/shorter." If they want changes, they'll ask.
- Don't quote the user's question back to them before answering.

## Length discipline

If your draft is over 480 chars, cut it before showing the user. Common cuts:

- Filler openers ("Just wanted to...", "Quick question,", "Hope you're doing well")
- Redundant context the recipient already has
- Hedges ("I think maybe we could possibly...")
- Repeated points stated two different ways
