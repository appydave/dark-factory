#!/usr/bin/env python3
"""shoot-slides — 16:9 PNG of every standalone HTML slide in a set of corpora.

Sibling to shoot.py, but for SLIDE DECKS rather than Mochaccino designs.
Each corpus is a directory of standalone *.html slides. We serve each corpus
root over a throwaway local HTTP server (so relative asset/data fetches resolve),
then Playwright-shoots each slide at a fixed 1600x900 16:9 viewport.

Corpora are declared in CORPORA below (reusable: add a dict to capture new decks).
Each corpus: name, root (dir), optional exclude-prefix list, optional single-file mode.

Usage:
  python3 shoot-slides.py                  # capture all corpora
  python3 shoot-slides.py --only poem      # capture one corpus
  python3 shoot-slides.py --width 1600 --height 900
Writes PNGs to out/slides/shots/<corpus>__<slug>.png and out/slides/shots.json
each entry: {corpus, slug, file, src_path}
"""
import argparse, json, os, re, sys, glob, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "slides")

# --- Corpus declarations (reusable: add an entry to capture a new deck root) ---
# kind:
#   "dir"  -> every *.html in `root` (minus excludes / exclude_prefix)
#   "file" -> a single html file at `root`
CORPORA = [
    dict(
        name="poem",
        kind="dir",
        root="/Users/davidcruwys/dev/ad/brand-artifacts/presentation-assets/bmad-poem",
        # exclude all navigation index pages (index-epic0.html, index-john.html, ...)
        exclude_prefix=["index"],
    ),
    dict(
        name="bmad-agents",
        kind="dir",
        root="/Users/davidcruwys/dev/ad/brand-artifacts/presentation-assets/bmad-agents",
        # bare index.html is nav-only
        exclude=["index.html"],
    ),
    dict(
        name="bmad-old",
        kind="file",
        root="/Users/davidcruwys/dev/ad/brains/bmad-method/bmad-agents-presentation.html",
    ),
]


def slug_of(path):
    base = os.path.basename(path)
    base = re.sub(r"\.html?$", "", base, flags=re.I)
    return re.sub(r"[^a-zA-Z0-9._-]", "-", base)


def slides_for(corpus):
    """Return list of (slug, src_path, serve_root, url_path) for a corpus."""
    out = []
    if corpus["kind"] == "file":
        path = corpus["root"]
        if not os.path.exists(path):
            return out
        root = os.path.dirname(path)
        out.append((slug_of(path), path, root, os.path.basename(path)))
        return out

    root = corpus["root"]
    if not os.path.isdir(root):
        return out
    excl = set(corpus.get("exclude", []))
    excl_pref = corpus.get("exclude_prefix", [])
    for path in sorted(glob.glob(os.path.join(root, "*.html"))):
        base = os.path.basename(path)
        if base in excl:
            continue
        if any(base.startswith(p) for p in excl_pref):
            continue
        out.append((slug_of(path), path, root, base))
    return out


def serve(directory):
    handler = functools.partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="capture only this corpus name")
    ap.add_argument("--out", default=os.path.join(OUT, "shots"))
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--fresh", action="store_true", help="ignore existing shots.json")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    corpora = [c for c in CORPORA if not args.only or c["name"] == args.only]
    if not corpora:
        print(f"no corpus named {args.only!r}", flush=True)
        sys.exit(1)

    sidecar = os.path.join(args.out, "shots.json")
    shots = []
    if os.path.exists(sidecar) and not args.fresh:
        try:
            shots = json.load(open(sidecar))
        except Exception:
            shots = []
    seen = {(s["corpus"], s["slug"]) for s in shots}
    failures = []

    plan = []
    for c in corpora:
        items = slides_for(c)
        plan.append((c, items))
        print(f"corpus {c['name']}: {len(items)} slides", flush=True)

    total = sum(len(items) for _, items in plan)
    print(f"shooting up to {total} slides @ {args.width}x{args.height} -> {args.out}", flush=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=1,
        )
        for c, items in plan:
            if not items:
                continue
            # group by serve root (file-mode each may differ; dir-mode shares one)
            roots = {}
            for slug, src, root, urlpath in items:
                roots.setdefault(root, []).append((slug, src, urlpath))
            for root, group in roots.items():
                httpd, port = serve(root)
                for slug, src, urlpath in group:
                    key = (c["name"], slug)
                    if key in seen:
                        continue
                    img = f"{c['name']}__{slug}.png"
                    url = f"http://127.0.0.1:{port}/{urlpath}"
                    try:
                        page.goto(url, wait_until="networkidle", timeout=20000)
                        page.wait_for_timeout(400)
                        # default: fixed 16:9 viewport shot (slide = one screen).
                        # Only fall back to full_page if content clearly overflows
                        # the viewport height by a large margin.
                        doc_h = page.evaluate("document.documentElement.scrollHeight")
                        full = doc_h > args.height * 1.6
                        page.screenshot(
                            path=os.path.join(args.out, img),
                            full_page=full,
                        )
                        shots.append(dict(
                            corpus=c["name"], slug=slug, file=img, src_path=src,
                            full_page=full,
                        ))
                        seen.add(key)
                        print(f"  ok  {img}{'  [full]' if full else ''}", flush=True)
                    except Exception as e:
                        msg = str(e).splitlines()[0] if str(e) else repr(e)
                        print(f"  FAIL {img}: {msg}", flush=True)
                        failures.append(dict(corpus=c["name"], slug=slug,
                                             src_path=src, error=msg))
                httpd.shutdown()
        browser.close()

    shots.sort(key=lambda s: (s["corpus"], s["slug"]))
    json.dump(shots, open(sidecar, "w"), indent=2)
    if failures:
        json.dump(failures, open(os.path.join(args.out, "failures.json"), "w"), indent=2)

    # summary by corpus
    by = {}
    for s in shots:
        by[s["corpus"]] = by.get(s["corpus"], 0) + 1
    print(f"\n{len(shots)} shots total -> {sidecar}", flush=True)
    for k in sorted(by):
        print(f"  {k}: {by[k]}", flush=True)
    if failures:
        print(f"  FAILURES: {len(failures)} (see failures.json)", flush=True)


if __name__ == "__main__":
    main()
