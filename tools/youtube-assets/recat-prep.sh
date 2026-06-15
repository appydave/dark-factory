#!/usr/bin/env bash
# recat-prep.sh — Stage 3 SELECTOR + BAKE for the transcript-recategorize loop.
#
# WHAT: finds pending videos (transcript.txt present, not yet transcript_enriched) and
#       bakes up to CAP of them into recat-run.js — a runnable copy of the workflow with
#       a fixed FOLDERS worklist injected. Deterministic, no LLM.
#       Prints:  PENDING=<n>  BATCH=<m>
#       Why a script writes JS: a Claude Workflow can't read disk, so it can't decide WHICH
#       videos still need work. This script makes that decision and hands it a fixed list.
#
# NEXT STEP: in Claude Code, run the baked file via the Workflow tool:
#       Workflow({ scriptPath: "<RUN>" })   # default RUN = ./recat-run.js
#   Then fold results back with recat-writeback.py. Re-run prep+workflow until PENDING=0.
#   Keep CAP under ~40 to stay below burst limits.
#
# CONFIG (env vars; defaults keep the original AITLDR behaviour):
#   CAT   catalog dir to scan   (default: v-aitldr/catalog)
#   WF    workflow template     (default: <repo>/.claude/workflows/transcript-recategorize.workflow.js)
#   RUN   baked output path     (default: <this-dir>/recat-run.js)
# Arg 1 = CAP (batch cap, default 30). REPO/TOOL self-derive from script location.
#
# USAGE:
#   bash recat-prep.sh 40                                              # AITLDR (default), batch 40
#   CAT=/Users/davidcruwys/dev/video-projects/v-appydave/catalog bash recat-prep.sh 30
set -uo pipefail
TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$TOOL/../.." && pwd)"
CAT="${CAT:-/Users/davidcruwys/dev/video-projects/v-aitldr/catalog}"
WF="${WF:-$REPO/.claude/workflows/transcript-recategorize.workflow.js}"
RUN="${RUN:-$TOOL/recat-run.js}"
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
