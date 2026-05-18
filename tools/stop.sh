#!/usr/bin/env bash
# Stop the Mochaccino HTTP server on port 7420.

PORT=7420
EXISTING=$(lsof -ti:$PORT 2>/dev/null || true)

if [ -n "$EXISTING" ]; then
  echo "→ killing pids: $EXISTING"
  echo "$EXISTING" | xargs kill -9 2>/dev/null || true
  sleep 0.3
  REMAINING=$(lsof -ti:$PORT 2>/dev/null || true)
  if [ -z "$REMAINING" ]; then
    echo "✓ port $PORT free"
  else
    echo "✗ pids still alive: $REMAINING"
    exit 1
  fi
else
  echo "no process on port $PORT — nothing to stop"
fi
