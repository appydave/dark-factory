#!/usr/bin/env bash
# reaper.sh — engine-state reaper (runs as Marshall's privileged Monitor).
#
# Closes the COMMON orphan: a Swagger whose handback landed in reports/ but whose
# tmux window is still open. PROCESS-INDEPENDENT — process-tree detection is dead
# (Claude Code reparents the session to its daemon; see proof/reaper-livefire-finding.md).
# Keys off the engine's OWN artifacts:
#   reports/<queue_id>.json  (handback; its mtime = when the job finished)
#   registry/<window>.json   ({"queue_id": "..."}; written by Marshall on dispatch)
# → once the handback is older than the grace period, if the window still exists,
#   tmux kill-window it and deregister. Idempotent: reaping an absent window is a no-op.
#
# Run via the Monitor tool in Marshall's session (Marshall alone holds tmux perms).
# Env: REAPER_GRACE_SECONDS (default 60), REAPER_POLL_SECONDS (default 5),
#      REAPER_ONCE=1 (run a single pass and exit — for testing).
set -uo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
REPORTS="$BASE/reports"; REG="$BASE/registry"
GRACE="${REAPER_GRACE_SECONDS:-60}"; POLL="${REAPER_POLL_SECONDS:-5}"
mkdir -p "$REG"
shopt -s nullglob

while true; do
  now=$(date +%s)
  for f in "$REPORTS"/*.json; do
    qid=$(basename "$f" .json)
    landed=$(stat -f %m "$f" 2>/dev/null || echo "$now")
    [ $(( now - landed )) -lt "$GRACE" ] && continue
    # Find the registry entry for this queue_id (the window that owns it).
    reg=""
    for r in "$REG"/*.json; do
      if grep -q "\"queue_id\"[[:space:]]*:[[:space:]]*\"$qid\"" "$r" 2>/dev/null; then reg="$r"; break; fi
    done
    [ -z "$reg" ] && continue            # untracked or already deregistered
    win=$(basename "$reg" .json)
    # tmux membership test WITHOUT `grep -q` in a pipe (that SIGPIPEs under pipefail).
    wins=$(tmux list-windows -a -F '#{window_name}' 2>/dev/null || true)
    if [[ $'\n'"$wins"$'\n' == *$'\n'"$win"$'\n'* ]]; then
      tmux kill-window -t "$win" 2>/dev/null && echo "reaped $win (job $qid done, grace ${GRACE}s)"
    fi
    rm -f "$reg"                         # deregister whether we killed it or it was already gone
  done
  [ -n "${REAPER_ONCE:-}" ] && break
  sleep "$POLL"
done
