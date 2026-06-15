#!/usr/bin/env python3
# merge-ai-enrich.py — fold AI enrichment sidecars (ai.json) back into each meta.json,
# then rebuild catalog.json. This is the "catch what the AI gives back" side of the
# scripts -> AI -> scripts sandwich.
#
# Each <folder>/ai.json (written by the enrichment workflow agents) looks like:
#   {"youtubeId": "...", "category": "<one of the taxonomy>", "description": "<=160 chars"}
#
# Merge is NON-DESTRUCTIVE for source-of-truth fields: it sets category + description +
# transcript_enriched=true, and never touches title/youtubeId/format/duration/published.
# Idempotent: re-running just re-applies the same values.
#
# Usage:
#   CAT=<catalog> CHANNEL=<channel-url> python3 merge-ai-enrich.py
import glob, json, os, subprocess, sys
from collections import Counter

CAT = os.environ.get("CAT", "/Users/davidcruwys/dev/video-projects/v-appydave/catalog")
ALLOWED = {"claude-code", "ai-coding", "prompt-engineering", "ai-media", "content-creation", "other"}

merged = 0
bad_cat = []
dist = Counter()
for ai_path in glob.glob(f"{CAT}/**/ai.json", recursive=True):
    folder = os.path.dirname(ai_path)
    meta_path = os.path.join(folder, "meta.json")
    if not os.path.exists(meta_path):
        continue
    ai = json.load(open(ai_path))
    meta = json.load(open(meta_path))
    cat = (ai.get("category") or "").strip()
    desc = (ai.get("description") or "").strip()
    if cat not in ALLOWED:
        bad_cat.append((meta.get("slug"), cat))
        cat = "other"
    meta["category"] = cat
    meta["description"] = desc
    meta["enriched_from"] = "transcript"
    meta["transcript_enriched"] = True
    json.dump(meta, open(meta_path, "w"), indent=2, ensure_ascii=False)
    merged += 1
    dist[cat] += 1

print(f"MERGED={merged}")
print("category distribution:")
for c, n in dist.most_common():
    print(f"   {c:18} {n}")
if bad_cat:
    print(f"\n!! {len(bad_cat)} out-of-taxonomy categories coerced to 'other':")
    for slug, c in bad_cat[:20]:
        print(f"   {slug}  (was: {c!r})")

# rebuild the master catalog.json from the per-folder meta.json (source of truth)
here = os.path.dirname(os.path.abspath(__file__))
print()
subprocess.run(["python3", os.path.join(here, "rebuild-catalog.py")],
               env={**os.environ, "CAT": CAT})
