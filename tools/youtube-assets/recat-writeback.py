#!/usr/bin/env python3
# recat-writeback.py — Stage 4: fold a transcript-recategorize workflow result back to disk.
#
# WHAT: reads a completed workflow task-output file and writes each record into its
#       meta.json NON-DESTRUCTIVELY:
#         adds category_transcript, description_transcript, transcript_changed,
#         transcript_enriched=true   — NEVER touches the title-based category/description.
#       Then auto-runs rebuild-catalog.py so catalog.json never goes stale.
#       Prints: WROTE=<n> CHANGED=<m>
#
#   (For the AppyDave-style transcript-grounded enrichment that writes the PRIMARY
#    category/description, see merge-ai-enrich.py instead — same role, ai.json sidecars.)
#
# CONFIG (env vars; defaults keep the original AITLDR behaviour):
#   CAT       catalog dir to write into   (default: v-aitldr/catalog)
#   CHANNEL   source channel URL, passed through to rebuild-catalog.py (optional)
# Arg 1 = the workflow task-output file (JSON).
#
# USAGE:
#   python3 recat-writeback.py <task_output_file>                      # AITLDR (default)
#   CAT=/Users/davidcruwys/dev/video-projects/v-appydave/catalog \
#     CHANNEL=https://www.youtube.com/@appydave \
#     python3 recat-writeback.py <task_output_file>
import json, glob, os, sys

CAT = os.environ.get("CAT", "/Users/davidcruwys/dev/video-projects/v-aitldr/catalog")
task_file = sys.argv[1]

raw = json.load(open(task_file))
data = raw.get("result", raw)            # task output is wrapped: {summary, result:{...}}
records = [r for r in data["records"] if r]

metas = {json.load(open(m))["youtubeId"]: m for m in glob.glob(f"{CAT}/**/meta.json", recursive=True)}

wrote = changed = 0
for r in records:
    path = metas.get(r["youtubeId"])
    if not path:
        continue
    meta = json.load(open(path))
    meta["category_transcript"]    = r["category_transcript"]
    meta["description_transcript"] = r["description_transcript"]
    meta["transcript_changed"]     = r["changed"]
    meta["transcript_enriched"]    = True
    json.dump(meta, open(path, "w"), indent=2, ensure_ascii=False)
    wrote += 1
    if r["changed"]:
        changed += 1

print(f"WROTE={wrote} CHANGED={changed}")

# Keep catalog.json in sync — it's a DERIVED aggregate of the meta.json files.
# Without this, catalog.json goes stale and silently drops the transcript work.
# Pass CAT (+ CHANNEL if set) through so the rebuild targets the same catalog.
import subprocess
subprocess.run(
    ["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rebuild-catalog.py")],
    env={**os.environ, "CAT": CAT},
)
