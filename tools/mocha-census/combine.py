#!/usr/bin/env python3
"""Combine per-machine census TSVs into a deduped manifest + summary.
Dedup key = (logical_repo, design_id). Build copies (dist/public/client-dist)
collapse onto their source repo; cross-machine dupes collapse to one row,
keeping the most-recently-modified source. Flags cross-machine divergence."""
import json, os, sys, glob, re

HOME = os.path.expanduser("~")
rows = []
for tsv in glob.glob(os.path.join(os.path.dirname(__file__), "out", "census-*.tsv")):
    for line in open(tsv, encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 7:
            continue
        machine, kind, root, did, path, mt, title = p[:7]
        rows.append(dict(machine=machine, kind=kind, root=root, design_id=did,
                         path=path, mtime=int(mt or 0), title=title))

def logical_repo(root):
    r = re.sub(r"^.*/dev/", "", root)
    r = re.sub(r"/(\.mochaccino|mochaccino)$", "", r)
    for b in ("/apps/web/public", "/apps/web/dist", "/client/dist", "/dist", "/public"):
        r = r.replace(b, "")
    return r

groups = {}
for r in rows:
    repo = logical_repo(r["root"])
    key = (repo, r["design_id"])
    groups.setdefault(key, []).append({**r, "repo": repo})

manifest = []
for (repo, did), recs in sorted(groups.items()):
    machines = sorted({x["machine"] for x in recs})
    # prefer source over build, then newest mtime
    best = sorted(recs, key=lambda x: (x["kind"] != "source", -x["mtime"]))[0]
    # divergence: same key present on >1 machine with differing mtime among sources
    src_mtimes = {x["machine"]: x["mtime"] for x in recs if x["kind"] == "source"}
    diverged = len(set(src_mtimes.values())) > 1
    manifest.append(dict(repo=repo, design_id=did, title=best["title"].strip(),
                         machine=best["machine"], path=best["path"],
                         mtime=best["mtime"], machines=machines, diverged=diverged))

out = os.path.join(os.path.dirname(__file__), "out", "manifest.json")
json.dump(manifest, open(out, "w"), indent=2)

# summary
by_repo = {}
for m in manifest:
    s = by_repo.setdefault(m["repo"], dict(n=0, machines=set(), diverged=0))
    s["n"] += 1
    s["machines"].update(m["machines"])
    s["diverged"] += int(m["diverged"])

print(f"UNIQUE DESIGNS: {len(manifest)}   (raw rows: {len(rows)})")
both = sum(1 for m in manifest if len(m["machines"]) > 1)
div = sum(1 for m in manifest if m["diverged"])
print(f"on both machines: {both}    diverged (same id, different mtime): {div}")
print(f"\n{'designs':>7}  {'machines':<13} {'div':>3}  repo")
for repo, s in sorted(by_repo.items(), key=lambda kv: -kv[1]["n"]):
    print(f"{s['n']:>7}  {','.join(sorted(s['machines'])):<13} {s['diverged']:>3}  {repo}")
print(f"\nmanifest -> {out}")
