#!/usr/bin/env python3
"""Capture a retina screenshot of one element of a running page, over CDP.

    python3 <skill-dir>/capture.py URL SELECTOR OUT.png [options]

Marketing screenshots are worthless at 1x: the blog renders heroes around
1000 CSS px wide, so a 1x capture is already soft and a retina screen halves
it again. This drives Chrome with deviceScaleFactor 2 and clips to the
element, so the output is exactly the component at twice its CSS size, with
no browser chrome and no hand-cropping.

Options:
  --scale     device pixel ratio (default 2).
  --pad       white margin added around the capture, as a percent of its
              width (default 4.5). Shots has no inner-padding control, so
              the breathing room inside the glass rim has to be baked into
              the source. --pad 0 turns it off.
  --zoom      page zoom (default 1.25), the same knob as Chrome's ctrl+plus:
              the layout gets fewer CSS px so text and controls come out
              larger, which is what keeps a hero readable once the blog
              scales it down. Folded into the device pixel ratio, so the
              output stays --scale times its on-screen size.
  --width/--height
              viewport in CSS px before zoom (default 1440x900).
  --wait      extra ms after load, for fonts, charts and data (default 2500).
  --hide      CSS selector to hide before the shot; repeatable (cookie
              banners, dev overlays, anything that isn't the product).
  --click     click the first element whose text contains this string, before
              the shot; repeatable, in order. Use it to put the page in the
              state worth shooting (a tab, a row, a range).
  --eval      JavaScript to run before the shot; repeatable, in order, each
              followed by --wait ms so an answer or a fetch it kicked off has
              time to render. The escape hatch for anything --click and
              --hide can't express.
  --storage   KEY=ENV_VAR to seed into localStorage on the page's origin
              before loading it; repeatable. The value is read from that
              environment variable, never passed on the command line, so an
              auth token stays out of process listings and shell history.
              This is how you shoot an authenticated dashboard without
              typing a password into a script.
  --cdp       Chrome DevTools endpoint (default http://localhost:29229).

Needs a Chrome already listening on --cdp, plus pillow>=11 and
websockets>=14 (`python3 -m pip install "pillow>=11.0" "websockets>=14.0"`).
"""

import argparse
import asyncio
import base64
import io
import json
import os
from urllib.request import urlopen

import websockets
from PIL import Image

LOAD_TIMEOUT = 30


class Session:
    """Minimal CDP client: one websocket, awaited request/response pairs."""

    def __init__(self, ws):
        self.ws = ws
        self.next_id = 0
        self.events = []

    async def send(self, method, **params):
        self.next_id += 1
        call_id = self.next_id
        await self.ws.send(json.dumps({"id": call_id, "method": method, "params": params}))
        while True:
            message = json.loads(await self.ws.recv())
            if message.get("id") == call_id:
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message.get("result", {})
            if "method" in message:
                self.events.append(message)

    async def wait_for(self, method, matches, timeout):
        """Wait for one CDP event, including any already buffered by send()."""
        deadline = asyncio.get_running_loop().time() + timeout
        while True:
            for index, event in enumerate(self.events):
                if event["method"] == method and matches(event.get("params", {})):
                    del self.events[: index + 1]
                    return event["params"]
            self.events.clear()
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                raise SystemExit(f"timed out after {timeout}s waiting for {method}")
            try:
                message = json.loads(await asyncio.wait_for(self.ws.recv(), remaining))
            except asyncio.TimeoutError:
                raise SystemExit(f"timed out after {timeout}s waiting for {method}") from None
            if "method" in message:
                self.events.append(message)

    async def evaluate(self, expression):
        result = await self.send(
            "Runtime.evaluate", expression=expression, awaitPromise=True, returnByValue=True
        )
        if "exceptionDetails" in result:
            raise RuntimeError(result["exceptionDetails"].get("text", "evaluate failed"))
        return result["result"].get("value")

    async def goto(self, url, wait_ms):
        """Navigate and wait for *this* navigation to load, not the old page."""
        result = await self.send("Page.navigate", url=url)
        if result.get("errorText"):
            raise SystemExit(f"{url}: {result['errorText']}")
        loader_id = result.get("loaderId")
        if loader_id:
            await self.wait_for(
                "Page.lifecycleEvent",
                lambda params: params.get("name") == "load"
                and params.get("loaderId") == loader_id,
                LOAD_TIMEOUT,
            )
        elif await self.evaluate("document.readyState") != "complete":
            await self.wait_for(
                "Page.lifecycleEvent",
                lambda params: params.get("name") == "load",
                LOAD_TIMEOUT,
            )
        await asyncio.sleep(wait_ms / 1000)


def page_target(cdp):
    with urlopen(f"{cdp}/json") as response:
        targets = json.load(response)
    pages = [t for t in targets if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
    if not pages:
        raise SystemExit(f"no page target on {cdp}; is Chrome running?")
    return pages[0]["webSocketDebuggerUrl"]


async def capture(args):
    async with websockets.connect(
        page_target(args.cdp), max_size=None, ping_interval=None
    ) as ws:
        page = Session(ws)
        await page.send("Page.enable")
        await page.send("Runtime.enable")
        await page.send("Page.setLifecycleEventsEnabled", enabled=True)
        zoom = max(args.zoom, 0.1)
        await page.send(
            "Emulation.setDeviceMetricsOverride",
            width=round(args.width / zoom),
            height=round(args.height / zoom),
            deviceScaleFactor=args.scale * zoom,
            mobile=False,
        )

        if args.storage:
            items = []
            for item in args.storage:
                key, _, env_var = item.partition("=")
                if not env_var:
                    raise SystemExit(f"--storage takes KEY=ENV_VAR, got {item!r}")
                if env_var not in os.environ:
                    raise SystemExit(f"${env_var} is not set, needed for localStorage {key!r}")
                items.append((key, os.environ[env_var]))
            seed = ";".join(
                f"localStorage.setItem({json.dumps(key)}, {json.dumps(value)})"
                for key, value in items
            )
            await page.send(
                "Page.addScriptToEvaluateOnNewDocument",
                source=f"try{{{seed}}}catch(e){{}}",
            )

        await page.goto(args.url, args.wait)

        for label in args.click:
            clicked = await page.evaluate(
                "(() => { const want = " + json.dumps(label) + ".toLowerCase();"
                " const hit = [...document.querySelectorAll('button, a, [role=tab], [role=button], label')]"
                "   .find(n => n.offsetParent && n.textContent.trim().toLowerCase().includes(want));"
                " if (!hit) return false;"
                " for (const type of ['pointerdown', 'mousedown', 'pointerup', 'mouseup'])"
                "   hit.dispatchEvent(new PointerEvent(type, {bubbles: true}));"
                " hit.click(); return true; })()"
            )
            if not clicked:
                raise SystemExit(f"nothing clickable matched {label!r} on {args.url}")
            await asyncio.sleep(args.wait / 1000)

        for script in args.eval:
            await page.evaluate(f"({script}), 1")
            await asyncio.sleep(args.wait / 1000)

        for selector in args.hide:
            await page.evaluate(
                f"document.querySelectorAll({json.dumps(selector)})"
                ".forEach(n => n.style.setProperty('display', 'none', 'important')), 1"
            )

        box = await page.evaluate(
            "(() => { const n = document.querySelector(" + json.dumps(args.selector) + ");"
            " if (!n) return null;"
            " const r = n.getBoundingClientRect();"
            " return {x: r.x + window.scrollX, y: r.y + window.scrollY,"
            " width: r.width, height: r.height}; })()"
        )
        if not box:
            raise SystemExit(f"no element matched {args.selector!r} on {args.url}")
        if box["width"] < 2 or box["height"] < 2:
            raise SystemExit(f"{args.selector!r} has no size; is it collapsed or hidden?")

        shot = await page.send(
            "Page.captureScreenshot",
            format="png",
            captureBeyondViewport=True,
            clip={
                "x": box["x"],
                "y": box["y"],
                "width": box["width"],
                "height": box["height"],
                "scale": 1,
            },
        )
        await page.send("Emulation.clearDeviceMetricsOverride")

    image = Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
    margin = round(image.width * max(args.pad, 0) / 100)
    if margin:
        padded = Image.new(
            "RGB", (image.width + 2 * margin, image.height + 2 * margin), (255, 255, 255)
        )
        padded.paste(image, (margin, margin))
        image = padded
    image.save(args.out)
    print(
        f"{args.out}: {image.width}x{image.height} px"
        f" at {args.scale}x, zoom {zoom}, pad {args.pad}%"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url")
    parser.add_argument("selector")
    parser.add_argument("out")
    parser.add_argument("--scale", type=float, default=2)
    parser.add_argument("--pad", type=float, default=4.5)
    parser.add_argument("--zoom", type=float, default=1.25)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--wait", type=int, default=2500)
    parser.add_argument("--hide", action="append", default=[])
    parser.add_argument("--click", action="append", default=[])
    parser.add_argument("--eval", action="append", default=[])
    parser.add_argument("--storage", action="append", default=[])
    parser.add_argument("--cdp", default="http://localhost:29229")
    asyncio.run(capture(parser.parse_args()))


if __name__ == "__main__":
    main()
