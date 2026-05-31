#!/usr/bin/env bash
# recat-prep.sh — SELECTOR + BAKE for the transcript-recategorize loop.
# Finds pending videos (transcript.txt present, not yet transcript_enriched),
# bakes up to CAP of them into recat-run.js (a runnable copy of the workflow).
# Prints:  PENDING=<n>  BATCH=<m>
# Deterministic — no LLM. The driver prompt runs this, then launches the workflow.
set -uo pipefail
CAT="/Users/davidcruwys/dev/video-projects/v-aitldr/catalog"
WF="/Users/davidcruwys/dev/ad/apps/dark-factory/.claude/workflows/transcript-recategorize.workflow.js"
RUN="/Users/davidcruwys/dev/ad/apps/dark-factory/tools/youtube-assets/recat-run.js"
CAP="${1:-30}"   # batch cap (stay under the ~40 burst-throttle)

python3 - "$CAT" "$WF" "$RUN" "$CAP" <<'PY'
import glob, json, os, sys
CAT, WF, RUN, CAP = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
pending=[os.path.dirname(m) for m in glob.glob(f"{CAT}/**/meta.json", recursive=True)
         if os.path.exists(os.path.dirname(m)+"/transcript.txt")
         and not json.load(open(m)).get("transcript_enriched")]
pending.sort()
batch=pending[:CAP]
if batch:
    src=open(WF).read()
    head=src[:src.index("const FOLDERS")]
    gen = head + f"const FOLDERS = {json.dumps(batch)}\nlog(`recat run: ${{FOLDERS.length}} folders`)\n\n" + src[src.index("const CATS"):]
    open(RUN,"w").write(gen)
print(f"PENDING={len(pending)} BATCH={len(batch)}")
PY
