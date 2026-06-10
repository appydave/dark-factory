#!/usr/bin/env python3
"""Render-health check over rated designs: load each, flag broken renders
(console errors / 'Failed to load' / stuck 'Loading...' / parse errors) so we
don't mistake a data-wiring failure for a design verdict."""
import json, os, re, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

HERE=os.path.dirname(os.path.abspath(__file__))
def slug(root):
    r=re.sub(r"^.*/dev/","",root); r=re.sub(r"/(\.mochaccino|mochaccino)$","",r); return r.replace("/","-")
paths={}
for tsv in ["out/census-m4pro.tsv","out/census-mini-mirror.tsv"]:
    p=os.path.join(HERE,tsv)
    if not os.path.exists(p): continue
    for line in open(p,encoding="utf-8",errors="replace"):
        c=line.rstrip("\n").split("\t")
        if len(c)<7 or c[1]!="source": continue
        paths.setdefault((slug(c[2]),c[3]), c[4])
ratings=[r for r in json.load(open(os.path.join(HERE,"out/ratings/round-01.json"))) if r["rating"]]

def root_of(p): return re.sub(r"/designs/.+/index\.html$","",p)
def serve(d):
    h=functools.partial(SimpleHTTPRequestHandler,directory=d)
    s=ThreadingHTTPServer(("127.0.0.1",0),h)
    threading.Thread(target=s.serve_forever,daemon=True).start()
    return s,s.server_address[1]

BAD=re.compile(r"failed to load|unexpected token|is not defined|cannot read|NaN|undefined is not|error:",re.I)
by_root={}
for r in ratings:
    p=paths.get((r["repo"],r["design_id"]))
    if p: by_root.setdefault(root_of(p),[]).append((r,p))

out=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page()
    errs=[]; pg.on("console",lambda m:(errs.append(m.text) if m.type=="error" else None))
    for root,items in by_root.items():
        s,port=serve(root)
        sub=root.split("/")[-1]
        for r,p in items:
            did=re.sub(r".*/designs/(.+)/index\.html$",r"\1",p)
            errs.clear()
            try:
                pg.goto(f"http://127.0.0.1:{port}/designs/{did}/index.html",wait_until="networkidle",timeout=15000)
                pg.wait_for_timeout(300)
                body=pg.inner_text("body")
            except Exception as e:
                body=f"__nav_fail__ {e}"
            broken = bool(BAD.search(body)) or len([e for e in errs if "favicon" not in e])>0
            stuck = body.strip().lower().count("loading")>0 and len(body.strip())<400
            out.append(dict(repo=r["repo"],design_id=r["design_id"],rating=r["rating"],
                            broken=broken,stuck=stuck,console_errs=len([e for e in errs if "favicon" not in e])))
        s.shutdown()
    b.close()

json.dump(out,open(os.path.join(HERE,"out/ratings/health.json"),"w"),indent=2)
from collections import Counter
bad=[o for o in out if o["broken"] or o["stuck"]]
print(f"checked {len(out)}  broken/stuck {len(bad)}")
print("broken by rating:",dict(Counter(o["rating"] for o in bad)))
print("\nBROKEN/STUCK designs (rating | repo | id | consoleErrs):")
for o in sorted(bad,key=lambda x:x["rating"]):
    print(f"  {o['rating']:<5} {o['repo'].split('-')[-1]:<16} {o['design_id']:<32} errs={o['console_errs']} stuck={o['stuck']}")
