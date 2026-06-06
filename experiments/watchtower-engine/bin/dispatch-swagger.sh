#!/usr/bin/env bash
# dispatch-swagger.sh — Marshall dispatches a Swagger AND registers it, so the
# engine-state reaper (bin/reaper.sh) can auto-close it. Registry-on-dispatch
# removes the "Marshall forgets to register/reap" failure mode.
#
# Run from repo root, inside tmux. Usage: dispatch-swagger.sh <window> <queue_id>
#
# NOTE (known limitation): the Swagger claims the OLDEST queue ticket, so the
# window↔queue_id binding here is only exact for SERIAL dispatch (one queued
# ticket at a time). Concurrent dispatch needs claim-by-id or self-reported
# window — a refinement the Symphony re-read may illuminate (claim/workspace).
set -euo pipefail
WIN="${1:?window name (e.g. swagger-foo)}"; QID="${2:?queue_id}"
BASE="experiments/watchtower-engine"
mkdir -p "$BASE/registry"
printf '{"window":"%s","queue_id":"%s","started_at":"%s"}\n' \
  "$WIN" "$QID" "$(date -u +%FT%TZ)" > "$BASE/registry/$WIN.json"
INSTR="You are a Swagger. Process the next ticket in $BASE/queue/ by following $BASE/skills/run-next-workflow/SKILL.md. Report ONE line and STOP. Do not ask questions. Follow the ticket prompt exactly; never call the date command."
tmux new-window -n "$WIN" "claude '$INSTR'"
echo "dispatched $WIN for $QID (registered for auto-reap)"
