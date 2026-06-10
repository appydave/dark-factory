#!/usr/bin/env bash
# audit.sh — count factory failures by category; flag any category at/над the investigate
# threshold (default 3, i.e. at or above). The register is data; this is the "where do we focus" view.
# David's rule: when a category hits 3-4, stop and investigate THOROUGHLY (root-cause, not band-aid).
#
# Usage: audit.sh [threshold]   (default 3).  Reads register.jsonl next to this script.
set -euo pipefail
BASE="$(cd "$(dirname "$0")" && pwd)"
REG="$BASE/register.jsonl"
THRESH="${1:-3}"
[ -f "$REG" ] || { echo "no failures recorded yet ($REG)"; exit 0; }
python3 - "$REG" "$THRESH" <<'PY'
import json,sys,collections
reg,thresh=sys.argv[1],int(sys.argv[2])
recs=[json.loads(l) for l in open(reg) if l.strip()]
openr=[r for r in recs if r.get("status")!="closed"]
by_cat=collections.Counter(r["category"] for r in openr)
print(f"FACTORY FAILURE AUDIT — {len(openr)} open / {len(recs)} total  (investigate threshold: {thresh})")
print("-"*60)
for cat,n in by_cat.most_common():
    flag=" ⚠️ INVESTIGATE" if n>=thresh else ""
    sevs=collections.Counter(r["severity"] for r in openr if r["category"]==cat)
    print(f"  {n:3d}  {cat:28s} {dict(sevs)}{flag}")
print("-"*60)
hot=[c for c,n in by_cat.items() if n>=thresh]
if hot:
    print(f"→ {len(hot)} categor{'y' if len(hot)==1 else 'ies'} at threshold: {', '.join(hot)} — root-cause now.")
    for cat in hot:
        print(f"\n  {cat} instances:")
        for r in openr:
            if r["category"]==cat:
                link=r.get("queue_id") or r.get("session") or ""
                print(f"    {r['id']}  {r['ts'][:10]}  {r.get('component','')}  [{link}]  {r['what'][:70]}")
else:
    print("→ no category at threshold; keep counting.")
PY
