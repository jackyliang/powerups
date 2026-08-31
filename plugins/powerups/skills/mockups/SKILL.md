---
name: mockups
description: Turn a product screenshot into a marketing mockup — capture the UI raw over CDP, then composite in Shots.so with the house recipe (Mystic gradient background, Glass Light rim, 4:3). Use for ANY customer-facing image (blog hero, landing page section, changelog, docs, launch or social post, deck) and whenever asked to take, retake, or restyle a marketing screenshot.
---

# Mockups

Two steps, always in this order: capture the UI raw over CDP, then run it through
[Shots](https://shots.so/) with the house recipe below. Never ship a raw capture, a
browser-chrome screenshot, or a flat crop.

**This skill needs a browser you control.** Step 1 needs a Chrome with a CDP port open;
step 2 is a GUI app, so it needs an agent that can click (Devin's computer tool, Claude in
Chrome, a human). Without one, do step 1, save the raw capture, and hand off step 2 — do
not substitute a hand-rolled gradient, a CSS frame or an AI-generated background.

## 1. Capture the source

`capture.py` ships next to this file.

```bash
python3 -m pip install "pillow>=11.0" "websockets>=14.0"
python3 <skill-dir>/capture.py <url> <selector> raw-<name>.png
```

It drives the Chrome already listening on `http://localhost:29229` (`--cdp` to change) and
clips to the element, so there is no browser chrome to crop off. `--click <text>` puts the
page in the state worth shooting, `--wait` covers pages that render skeletons first,
`--hide <selector>` drops banners and chat widgets, `--eval <js>` edits the DOM before the
shot (each `--eval` is followed by another `--wait`, so an evaluated action that fires a
request has time to render), and `--storage KEY=ENV_VAR` seeds an auth token read from the
environment before the page loads, for a signed-in page (never put the token itself on the
command line).

Defaults are the house settings, so don't pass them: `--scale 2` (retina), `--zoom 1.25`
(text stays readable once the image is scaled down in a post or a deck), and `--pad 4.5`,
the white margin that becomes the breathing room inside the glass rim — Shots has no
inner-padding control, so it has to be in the source.

Dashboard pages render real data. If the shot contains anything a customer wrote —
questions, topics, conversation threads, tickets, connected accounts, names, emails —
**ask whether to swap in generic placeholder text**, and default to swapping. Rewrite the
strings in the DOM with `--eval` before the capture, walking text nodes so nested markup
doesn't end up overlapping:

```js
const swap = new Map([["Wo ist meine Bestellung?", "Where is my order?"]]);
const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
nodes.forEach(n => { const t = n.nodeValue.trim(); if (swap.has(t)) n.nodeValue = swap.get(t); });
```

Keep counts, dates and labels plausible, and keep raw captures out of the repo's image
directory — they are inputs, not assets.

## 2. Compose in Shots

Open `https://shots.so/` and load the raw capture: CDP `DOM.setFileInputFiles` on the
media control's hidden `input[type=file]`, or `Input.dispatchDragEvent`
(`dragEnter`/`dragOver`/`drop` with `data.files`) onto the media control. Both work; both
sometimes need a second try before the editor swaps the active media, so **verify the
canvas actually shows the new image** before touching any setting.

The recipe, all of it free-tier:

| Setting | Value |
| --- | --- |
| Mockup → style | Glass Light |
| Mockup → border | Curved, radius 20 |
| Mockup → shadow | Spread, opacity 10 (the slider's floor) |
| Frame → ratio | Default 4:3 → exports 1920 × 1440 |
| Frame → background | **Mystic**, the number the requester asked for |
| Frame → Bg effects | Noise 84, Blur 0 |
| Canvas zoom | 114% |

Background: Mystic has 15 gradients, previewed at
`https://assets.shots.so/mystic-gradients/original/<1-15>.jpg`. **Ask which number** unless
the request names one — never pick one at random. Send the numbered contact sheet of all 15
with the question. #14 is the default when the requester has no preference. Stay inside the
Mystic family — that family *is* the house look.

Export downloads a watermark-free PNG to `~/Downloads/<n>_1x_shots_so.png` at 1920 × 1440.
2x/4K is a paid tier; don't buy it, 1920 is enough everywhere we ship images.

## 3. Check it before shipping

Open the export and look at it: one background, glass rim intact on all four sides, even
margin inside the rim, real product UI, nothing stale or private in frame. Then open the
page it lands on at real width and confirm nothing is cropped through a heading — the site
CSS has to be 4:3 too, or a 4:3 export gets sliced.

## Never

- Composite by hand in Python, CSS or Figma, or generate the background with an image
  model. Shots is the style.
- Re-composite an image out of the site's image directory — those already have a
  background, and a second pass through Shots stacks another one. Use a raw capture.
- Ship at a ratio other than 4:3.
- Leave lorem ipsum, test chats, personal emails, or old plan names in frame.
- Publish real customer text, or invented metrics.
