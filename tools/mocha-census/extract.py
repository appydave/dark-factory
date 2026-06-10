#!/usr/bin/env python3
"""Lineage diff + pattern extraction over a ratings file.
For each rated design, read its index.html, extract structural features,
then aggregate by rating to surface what separates good from meh/shit.
Path map is built from the census TSVs (local + mini-mirror)."""
import json, os, re, glob
from collections import defaultdict

HERE=os.path.dirname(os.path.abspath(__file__))
def slug(root):
    r=re.sub(r"^.*/dev/","",root); r=re.sub(r"/(\.mochaccino|mochaccino)$","",r); return r.replace("/","-")

# path map (repo_slug, design_id) -> html path
paths={}
for tsv in ["out/census-m4pro.tsv","out/census-mini-mirror.tsv"]:
    p=os.path.join(HERE,tsv)
    if not os.path.exists(p): continue
    for line in open(p,encoding="utf-8",errors="replace"):
        c=line.rstrip("\n").split("\t")
        if len(c)<7 or c[1]!="source": continue
        paths.setdefault((slug(c[2]),c[3]), c[4])

ratings=json.load(open(os.path.join(HERE,"out/ratings/round-01.json")))

def feats(html):
    h=html; low=html.lower()
    def c(p): return len(re.findall(p,low))
    hexes=set(re.findall(r"#[0-9a-f]{6}",low))
    fonts=set(re.findall(r"font-family:\s*['\"]?([a-z0-9 \-]+)",low))
    return dict(
        lines=html.count("\n")+1,
        grid=c(r"display:\s*grid")+c(r"grid-template"),
        flex=c(r"display:\s*flex"),
        sidebar=c(r"sidebar"),
        chrome=c(r"status-badge")+c(r"item-icon")+c(r"sidebar-item"),  # app-chrome shell tell
        cards=c(r'class="[^"]*\bcard\b')+c(r'class="[^"]*panel\b'),
        svg=c(r"<svg"),
        table=c(r"<table")+c(r'role="grid"'),
        clamp=c(r"clamp\("),
        colormix=c(r"color-mix\(")+c(r"oklch\("),
        maxwidth=c(r"max-width"),
        ncolors=len(hexes),
        fonts=sorted(f.strip() for f in fonts if f.strip()),
    )

groups=defaultdict(list); perdesign=[]
miss=0
for r in ratings:
    if not r["rating"]: continue
    p=paths.get((r["repo"],r["design_id"]))
    if not p or not os.path.exists(p): miss+=1; continue
    f=feats(open(p,encoding="utf-8",errors="replace").read())
    perdesign.append({**r,**f})
    groups[r["rating"]].append(f)

num=["lines","grid","flex","sidebar","chrome","cards","svg","table","clamp","colormix","maxwidth","ncolors"]
print(f"rated-with-html: {len(perdesign)}   missing-html: {miss}\n")
print(f"{'feature':<10}"+"".join(f"{g:>9}" for g in ["good","meh","shit"]))
for k in num:
    row=f"{k:<10}"
    for g in ["good","meh","shit"]:
        vals=[x[k] for x in groups.get(g,[])]
        row+=f"{(sum(vals)/len(vals) if vals else 0):>9.1f}"
    print(row)

# font usage by rating
print("\nfonts by rating:")
for g in ["good","meh","shit"]:
    fc=defaultdict(int)
    for x in groups.get(g,[]):
        for fn in x["fonts"]: fc[fn]+=1
    top=sorted(fc.items(),key=lambda kv:-kv[1])[:6]
    print(f"  {g:<5}", ", ".join(f"{n}({c})" for n,c in top))

# exemplar pack: good designs ranked by "structural richness" (lines + svg + grid, low chrome)
print("\ncandidate exemplars (good, richest structure, lowest chrome):")
goods=[x for x in perdesign if x["rating"]=="good"]
goods.sort(key=lambda x:-(x["lines"]+x["svg"]*40+x["grid"]*10-x["chrome"]*30))
for x in goods[:15]:
    print(f"  {x['repo'].split('-')[-1]:<18} {x['design_id']:<34} lines={x['lines']:<4} svg={x['svg']} grid={x['grid']} chrome={x['chrome']}")

json.dump(perdesign,open(os.path.join(HERE,"out/ratings/features.json"),"w"),indent=2)
print("\n-> out/ratings/features.json")
