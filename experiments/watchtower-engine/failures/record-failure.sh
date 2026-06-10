#!/usr/bin/env bash
# record-failure.sh — append ONE structured failure record to the factory failure register.
#
# The register is the factory's failure ledger: one countable record per failure, so we
# focus energy by COUNTING categories and investigate a category once it hits the threshold
# (see audit.sh). Each record carries WHAT failed, WHEN, and what it's LINKED to (session /
# queue_id / component) so any past failure is reviewable. Append-only — never edit a record;
# to close one, append a status change or set status via a follow-up tool (kept simple here).
#
# Designed to be called BY HAND (Marshall) now, and WIRED into dispatch/reaper later (DF-3:
# the loop records its own failures externally, not the worker self-reporting — memory
# 'factory-operations-telemetry'). That is the whole point: harness-driven, not remembered.
#
# Usage:
#   record-failure.sh --category <slug> --severity <P1|P2|P3> --component <str> \
#       --what "<one line>" [--session <id>] [--queue-id <id>] [--ticket <DF-n>] [--linked k=v,k=v]
set -euo pipefail
BASE="$(cd "$(dirname "$0")" && pwd)"
REG="$BASE/register.jsonl"
CATEGORY="" SEVERITY="P2" COMPONENT="" WHAT="" SESSION="" QID="" TICKET="" LINKED=""
while [ $# -gt 0 ]; do
  case "$1" in
    --category) CATEGORY="$2"; shift 2;;
    --severity) SEVERITY="$2"; shift 2;;
    --component) COMPONENT="$2"; shift 2;;
    --what) WHAT="$2"; shift 2;;
    --session) SESSION="$2"; shift 2;;
    --queue-id) QID="$2"; shift 2;;
    --ticket) TICKET="$2"; shift 2;;
    --linked) LINKED="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$CATEGORY" ] && [ -n "$WHAT" ] || { echo "required: --category and --what" >&2; exit 2; }
TS="$(date -u +%FT%TZ)"
DAY="$(date -u +%Y%m%d)"
N=$(( $(grep -c "\"F-$DAY-" "$REG" 2>/dev/null || echo 0) + 1 ))
ID="F-$DAY-$(printf '%02d' "$N")"
python3 - "$ID" "$TS" "$CATEGORY" "$SEVERITY" "$COMPONENT" "$WHAT" "$SESSION" "$QID" "$TICKET" "$LINKED" >> "$REG" <<'PY'
import json,sys
id,ts,cat,sev,comp,what,sess,qid,ticket,linked=sys.argv[1:11]
rec={"id":id,"ts":ts,"category":cat,"severity":sev,"component":comp,"what":what,
     "session":sess or None,"queue_id":qid or None,"ticket":ticket or None,"status":"open"}
if linked:
    for kv in linked.split(","):
        if "=" in kv:
            k,v=kv.split("=",1); rec[k]=v
print(json.dumps(rec))
PY
echo "recorded $ID  [$CATEGORY/$SEVERITY]  $WHAT"
