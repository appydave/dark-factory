#!/usr/bin/env python3
"""design-lint screenshotter — PNG of one (or a few) rendered HTML page(s).

The mechanical half of the design-loop pass. Serves each page's directory over a
throwaway local HTTP server (so relative data/asset fetches resolve), then
Playwright-shoots it. The judgment half is the lint agent applying RUBRIC.md to
the PNG — that is NOT done here.

Usage:
  python3 shoot-one.py <html-path-or-url> [more...] [--out out/lint] [--width 1600] [--full]
Writes <out>/<stem>.png and prints one JSON line {src,img,ok} per page.
"""
import argparse, json, os, re, sys, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))

def serve(directory):
    handler = functools.partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]

def stem_for(src):
    s = re.sub(r"^https?://", "", src)
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return (s[-80:] or "page").rsplit(".html", 1)[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="HTML file path(s) or http(s) URL(s)")
    ap.add_argument("--out", default=os.path.join(HERE, "out", "lint"))
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--full", action="store_true", help="full-page capture (default: fixed viewport)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height},
                                device_scale_factor=1)
        for t in args.targets:
            img = os.path.join(args.out, stem_for(t) + ".png")
            ok, err = True, None
            try:
                if t.startswith("http://") or t.startswith("https://"):
                    url = t
                    httpd = None
                else:
                    path = os.path.abspath(t)
                    httpd, port = serve(os.path.dirname(path))
                    url = f"http://127.0.0.1:{port}/{os.path.basename(path)}"
                page.goto(url, wait_until="networkidle", timeout=20000)
                page.wait_for_timeout(350)
                page.screenshot(path=img, full_page=args.full)
                if httpd:
                    httpd.shutdown()
            except Exception as e:
                ok, err = False, str(e)
            print(json.dumps(dict(src=t, img=img if ok else None, ok=ok, err=err)), flush=True)
        browser.close()

if __name__ == "__main__":
    main()
