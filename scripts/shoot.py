#!/usr/bin/env python3
"""Screenshot a show-me-html page and report horizontal overflow.

Drives headless Chrome over the DevTools protocol (standard library only, no
PIL / Playwright). Viewport emulation sidesteps Chrome's minimum window width,
so 390px phone shots need no iframe wrapper; element shots are clipped by
Chrome itself, so there is no coordinate measuring or manual cropping.

  shoot.py page.html                          # light, 1440px, full page + overflow report
  shoot.py page.html --theme dark --width 390
  shoot.py page.html --select '#board' '#ranking figure'
  shoot.py page.html --matrix                 # light / dark / 390px phone / print
  shoot.py page.html --check                  # overflow report only, no PNG

Exit status: 0 = clean, 1 = overflow found (with --check or --strict), 2 = error.
"""

import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "msedge",
]

# variant name -> (theme, width, print)
MATRIX = {
    "light": ("light", 1440, False),
    "dark": ("dark", 1440, False),
    "phone": ("light", 390, False),
    "print": ("light", 794, True),  # A4 at 96dpi
}


def find_chrome():
    env = os.environ.get("CHROME")
    if env:
        return env
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        elif shutil.which(c):
            return shutil.which(c)
    sys.exit("shoot.py: Chrome not found; set CHROME=/path/to/chrome")


# ── minimal WebSocket client (RFC 6455, client side, text frames) ──


class WS:
    def __init__(self, url):
        m = re.match(r"ws://([^/:]+):(\d+)(/.*)", url)
        host, port, path = m.group(1), int(m.group(2)), m.group(3)
        self.sock = socket.create_connection((host, port), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall(
            (
                f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\n"
                f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            ).encode()
        )
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self.sock.recv(1024)
            if not chunk:
                raise ConnectionError("websocket handshake failed")
            head += chunk
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise ConnectionError(head.split(b"\r\n", 1)[0].decode())
        self.buf = head.split(b"\r\n\r\n", 1)[1]

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(max(65536, n - len(self.buf)))
            if not chunk:
                raise ConnectionError("websocket closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _send_frame(self, opcode, payload):
        n = len(payload)
        head = bytes([0x80 | opcode])
        if n < 126:
            head += bytes([0x80 | n])
        elif n < 65536:
            head += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            head += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        body = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(head + mask + body)

    def send(self, text):
        self._send_frame(0x1, text.encode())

    def recv(self):
        parts = []
        while True:
            b0, b1 = self._read(2)
            opcode, n = b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            payload = self._read(n)
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode == 0x8:
                raise ConnectionError("websocket closed by peer")
            if opcode in (0x0, 0x1, 0x2):
                parts.append(payload)
                if b0 & 0x80:
                    return b"".join(parts).decode()


class CDP:
    def __init__(self, ws):
        self.ws, self.next_id, self.events = ws, 0, []

    def call(self, method, **params):
        self.next_id += 1
        my_id = self.next_id
        self.ws.send(json.dumps({"id": my_id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == my_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg)

    def wait_event(self, name, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            for i, e in enumerate(self.events):
                if e["method"] == name:
                    return self.events.pop(i)
            msg = json.loads(self.ws.recv())
            if "method" in msg:
                self.events.append(msg)
        raise TimeoutError(name)

    def eval(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("text", "evaluate failed"))
        return r["result"].get("value")


def launch(chrome):
    profile = tempfile.mkdtemp(prefix="smh-shoot-")
    proc = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--remote-debugging-port=0",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    port_file = Path(profile) / "DevToolsActivePort"
    for _ in range(200):
        if port_file.exists() and port_file.read_text().strip():
            break
        time.sleep(0.05)
    else:
        proc.kill()
        sys.exit("shoot.py: Chrome did not start (no DevToolsActivePort)")
    port = port_file.read_text().split()[0]
    for _ in range(50):
        try:
            targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
            page = next(t for t in targets if t["type"] == "page")
            return proc, profile, CDP(WS(page["webSocketDebuggerUrl"]))
        except (OSError, StopIteration):
            time.sleep(0.1)
    proc.kill()
    sys.exit("shoot.py: no page target")


# Runs inside the page. Returns overflow findings for elements under `scope`.
OVERFLOW_JS = r"""
(scope) => {
  const root = document.querySelector(scope) || document.body;
  const sel = (el) => {
    const parts = [];
    for (let e = el; e && e.nodeType === 1 && e !== document.body; e = e.parentElement) {
      if (e.id) { parts.unshift('#' + CSS.escape(e.id)); break; }
      let s = e.localName;
      const cls = [...e.classList].filter(c => !/^(open|active|hot|focused)$/.test(c)).slice(0, 2);
      if (cls.length) s += '.' + cls.map(c => CSS.escape(c)).join('.');
      const sib = e.parentElement ? [...e.parentElement.children].filter(x => x.localName === e.localName) : [];
      if (sib.length > 1) s += `:nth-of-type(${sib.indexOf(e) + 1})`;
      parts.unshift(s);
    }
    return parts.join(' > ');
  };
  const vw = document.documentElement.clientWidth;
  const hits = [];
  for (const el of root.querySelectorAll('*')) {
    if (el.closest('svg') && el.localName !== 'svg') continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;  // display:none and everything inside it
    const ox = cs.overflowX;
    const scrolls = ox === 'auto' || ox === 'scroll';
    const spill = el.scrollWidth - el.clientWidth;
    // a line-end full-width "）" or "。" counts its blank half in scrollWidth; that half may hang past the edge
    // without anything visible spilling, so allow half an em when the text ends in CJK punctuation
    const ink = () => {
      const slack = /[）」』】〕》〉。，、；：！？]\s*$/.test(el.textContent) ? parseFloat(cs.fontSize) / 2 : 0;
      return spill > slack + 1;
    };
    if (!scrolls && spill > 1 && el.clientWidth > 0 && !/^(input|textarea|select|code|pre)$/.test(el.localName) && cs.display !== 'inline' && ink()) {
      hits.push({kind: ox === 'visible' ? 'spill' : 'clipped', sel: sel(el), el,
                 detail: `content ${el.scrollWidth}px in ${el.clientWidth}px box (overflow-x: ${ox})`});
    }
    if (r.right > vw + 1 && !el.closest('.table-container, .fig-scroll, pre') && getComputedStyle(el.parentElement).overflowX === 'visible') {
      hits.push({kind: 'offpage', sel: sel(el), el, detail: `right edge ${Math.round(r.right)}px > viewport ${vw}px`});
    }
    if (el.localName === 'svg' && el.viewBox && el.viewBox.baseVal && el.viewBox.baseVal.width) {
      const scale = r.width / el.viewBox.baseVal.width;
      if (scale < 0.6 && !el.classList.contains('lucide')) {
        hits.push({kind: 'svg-shrunk', sel: sel(el), el,
                   detail: `drawn at ${Math.round(scale * 100)}% (viewBox ${el.viewBox.baseVal.width} → ${Math.round(r.width)}px); 13px text reads as ${(13 * scale).toFixed(1)}px`});
      }
    }
  }
  // a collapsible inside a card: boxed-in-a-box, and in an equal-height row it never lines up with its neighbours
  for (const d of root.querySelectorAll(':is(.card, .lane) details')) {
    hits.push({kind: 'nested', sel: sel(d), el: d,
               detail: 'details inside a card; move it to one details.ev-more below the card group'});
  }
  // keep the innermost element of each spill chain: a long word overflowing an h4 also overflows its card
  const keep = hits.filter(h => h.kind === 'svg-shrunk' || h.kind === 'nested' ||
    !hits.some(o => o !== h && o.kind === h.kind && h.el.contains(o.el)));
  return {
    pageScroll: document.documentElement.scrollWidth > vw + 1 ? document.documentElement.scrollWidth : 0,
    viewport: vw,
    hits: keep.map(({kind, sel, detail}) => ({kind, sel, detail})),
  };
}
"""

RECTS_JS = r"""
(sels) => sels.map(s => [...document.querySelectorAll(s)].map(el => {
  const r = el.getBoundingClientRect();
  return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height};
}))
"""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "el"


def render(cdp, url, theme, width, printing, scale):
    # theme script in the skeleton reads localStorage before first paint
    cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900,
             deviceScaleFactor=scale, mobile=width < 600)
    cdp.call("Emulation.setEmulatedMedia", media="print" if printing else "", features=[
        {"name": "prefers-color-scheme", "value": theme},
        {"name": "prefers-reduced-motion", "value": "reduce"},
    ])
    cdp.events.clear()
    cdp.call("Page.navigate", url=url)
    cdp.wait_event("Page.loadEventFired")
    cdp.eval("document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300)))")
    cdp.eval("scrollTo(0, 0)")


def capture(cdp, path, clip, scale):
    clip = dict(clip, scale=1)
    data = cdp.call("Page.captureScreenshot", format="png", captureBeyondViewport=True, clip=clip)["data"]
    path.write_bytes(base64.b64decode(data))
    print(f"  {path}  ({int(clip['width'] * scale)}×{int(clip['height'] * scale)})")


def report(result, label):
    hits = result["hits"]
    if not hits and not result["pageScroll"]:
        print(f"  overflow[{label}]: none")
        return False
    print(f"  overflow[{label}]: {len(hits)} finding(s)")
    if result["pageScroll"]:
        print(f"    page scrolls sideways: document {result['pageScroll']}px > viewport {result['viewport']}px")
    for h in hits:
        print(f"    {h['kind']:<10} {h['sel']}\n               {h['detail']}")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", type=Path)
    ap.add_argument("--theme", choices=["light", "dark"], default="light")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--print", dest="printing", action="store_true", help="emulate print media (use with --width 794)")
    ap.add_argument("--matrix", action="store_true", help="shoot light, dark, 390px phone and print in one run")
    ap.add_argument("--select", nargs="+", default=[], metavar="CSS", help="shoot these elements instead of the full page")
    ap.add_argument("--pad", type=int, default=8, help="CSS px of margin around element shots (default 8 = 16 device px)")
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--scope", default="main", help="where to look for overflow (default: main)")
    ap.add_argument("--out", type=Path, help="output dir (default: $TMPDIR/show-me-html-shots/<page-stem>)")
    ap.add_argument("--check", action="store_true", help="overflow report only, no screenshots; exit 1 on findings")
    ap.add_argument("--strict", action="store_true", help="exit 1 when overflow is found")
    a = ap.parse_args()

    page = a.page.resolve()
    if not page.exists():
        sys.exit(f"shoot.py: {page} not found")
    out = a.out or Path(tempfile.gettempdir()) / "show-me-html-shots" / page.stem
    if not a.check:
        out.mkdir(parents=True, exist_ok=True)

    variants = MATRIX if a.matrix else {
        f"{a.theme}-{a.width}" + ("-print" if a.printing else ""): (a.theme, a.width, a.printing)
    }

    proc, profile, cdp = launch(find_chrome())
    found, init_id = False, None
    try:
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        for name, (theme, width, printing) in variants.items():
            if init_id:
                cdp.call("Page.removeScriptToEvaluateOnNewDocument", identifier=init_id)
            init_id = cdp.call("Page.addScriptToEvaluateOnNewDocument",
                               source=f"try{{localStorage.setItem('show-me-theme','{theme}')}}catch(e){{}}")["identifier"]
            render(cdp, page.as_uri(), theme, width, printing, a.scale)
            print(f"{name}:")
            if not a.check:
                if a.select:
                    groups = cdp.eval(f"({RECTS_JS})({json.dumps(a.select)})")
                    for s, rects in zip(a.select, groups):
                        if not rects:
                            print(f"  (no match) {s}")
                        for i, r in enumerate(rects):
                            p = a.pad
                            clip = {"x": max(r["x"] - p, 0), "y": max(r["y"] - p, 0),
                                    "width": r["w"] + 2 * p, "height": r["h"] + 2 * p}
                            suffix = f"-{i + 1}" if len(rects) > 1 else ""
                            capture(cdp, out / f"{page.stem}-{name}-{slug(s)}{suffix}.png", clip, a.scale)
                else:
                    h = cdp.eval("document.documentElement.scrollHeight")
                    capture(cdp, out / f"{page.stem}-{name}.png", {"x": 0, "y": 0, "width": width, "height": h}, a.scale)
            result = cdp.eval(f"({OVERFLOW_JS})({json.dumps(a.scope)})")
            found |= report(result, name)
    finally:
        try:
            cdp.call("Browser.close")
        except Exception:
            pass
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)
    return 1 if found and (a.check or a.strict) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError) as e:  # OSError covers a bad CHROME path, socket and timeout errors
        print(f"shoot.py: {e}", file=sys.stderr)
        sys.exit(2)
