#!/usr/bin/env python3
"""mocha-census screenshotter — full-page PNG of every design in a census TSV.
Serves each Mochaccino root over a throwaway local HTTP server (so relative
data/component fetches resolve), then Playwright-shoots each design under it.

Usage:
  python3 shoot.py --tsv out/census-m4pro.tsv [--filter dark-factory] [--out out/shots]
Writes PNGs to <out>/<repo-slug>__<design_id>.png and appends to <out>/shots.json
"""
import argparse, json, os, re, sys, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))

def repo_slug(root):
    r = re.sub(r"^.*/dev/", "", root)
    r = re.sub(r"/(\.mochaccino|mochaccino)$", "", r)
    return r.replace("/", "-")

def root_of(path):
    # <root>/designs/<id>/index.html  -> <root>
    return re.sub(r"/designs/[^/]+/index\.html$", "", path)

def load_rows(tsv, filt):
    rows = []
    for line in open(tsv, encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 7 or p[1] != "source":
            continue
        machine, kind, root, did, path, mt, title = p[:7]
        if filt and filt not in root:
            continue
        if not os.path.exists(path):
            continue
        rows.append(dict(machine=machine, root=root, design_id=did, path=path,
                         mtime=int(mt or 0), title=title.strip(), repo=repo_slug(root)))
    return rows

def serve(directory):
    handler = functools.partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--filter", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "out", "shots"))
    ap.add_argument("--width", type=int, default=1280)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    rows = load_rows(args.tsv, args.filter)
    # group by serving root
    by_root = {}
    for r in rows:
        by_root.setdefault(root_of(r["path"]), []).append(r)
    print(f"shooting {len(rows)} designs across {len(by_root)} roots -> {args.out}", flush=True)

    shots = []
    sidecar = os.path.join(args.out, "shots.json")
    if os.path.exists(sidecar):
        shots = json.load(open(sidecar))
    seen = {(s["repo"], s["design_id"]) for s in shots}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": 900},
                                device_scale_factor=1)
        for root, group in by_root.items():
            httpd, port = serve(root)
            rel = root.split("/")[-1]  # .mochaccino | mochaccino
            for r in group:
                key = (r["repo"], r["design_id"])
                if key in seen:
                    continue
                url = f"http://127.0.0.1:{port}/designs/{r['design_id']}/index.html"
                img = f"{r['repo']}__{r['design_id'].replace('/', '--')}.png"
                try:
                    page.goto(url, wait_until="networkidle", timeout=15000)
                    page.wait_for_timeout(350)
                    page.screenshot(path=os.path.join(args.out, img), full_page=True)
                    ok = True
                except Exception as e:
                    print(f"  FAIL {img}: {e}", flush=True)
                    ok = False
                if ok:
                    shots.append(dict(repo=r["repo"], design_id=r["design_id"],
                                      title=r["title"], machine=r["machine"],
                                      mtime=r["mtime"], img=img))
                    seen.add(key)
                    print(f"  ok  {img}", flush=True)
            httpd.shutdown()
        browser.close()

    shots.sort(key=lambda s: (s["repo"], s["design_id"]))
    json.dump(shots, open(sidecar, "w"), indent=2)
    print(f"\n{len(shots)} shots total -> {sidecar}", flush=True)

if __name__ == "__main__":
    main()
