#!/usr/bin/env bash
# Start the Mochaccino HTTP server for the dark-factory workspace.
# Rooted at mochaccino/ so URLs look like /designs/, /data/...
#
# Idempotent: if a server is already on :7420 it is killed first.

set -e

PORT=7420
ROOT="$(cd "$(dirname "$0")/.." && pwd)/mochaccino"

# Kill anything already bound to the port
EXISTING=$(lsof -ti:$PORT 2>/dev/null || true)
if [ -n "$EXISTING" ]; then
  echo "→ killing existing server on :$PORT (pids: $EXISTING)"
  echo "$EXISTING" | xargs kill -9 2>/dev/null || true
  sleep 0.3
fi

cd "$ROOT"
nohup python3 -m http.server "$PORT" > .serve.log 2>&1 &
NEW_PID=$!
sleep 0.5

# Sanity check
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/designs/" | grep -q "200"; then
  echo "✓ server live"
  echo "  pid:               $NEW_PID"
  echo "  root:              $ROOT"
  echo "  log:               $ROOT/.serve.log"
  echo ""
  echo "  gallery:           http://localhost:$PORT/designs/"
  echo "  pipeline overview: http://localhost:$PORT/designs/01-pipeline-overview/"
  echo "  mining view:       http://localhost:$PORT/designs/02-mining-view/"
else
  echo "✗ server did not respond — check $ROOT/.serve.log"
  exit 1
fi
