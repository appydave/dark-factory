#!/usr/bin/env bash
#
# claim-next.sh — atomically claim the oldest queue entry.
#
# The mutex is rename(2): moving a file from queue/ to running/ is atomic.
# If two claimers race for the same entry, exactly one `mv` succeeds; the
# loser gets ENOENT (source already gone) and moves on to the next entry.
#
# Usage:   claim-next.sh [claimant-id]
# Prints:  absolute path of the claimed entry in running/  (exit 0)
#          nothing                                          (exit 1 = queue empty)
#
# Override the engine dir with WT_ENGINE_DIR (used by the concurrency test).

set -euo pipefail

BASE="${WT_ENGINE_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
QUEUE="$BASE/queue"
RUNNING="$BASE/running"
CLAIMANT="${1:-session-$$}"

mkdir -p "$QUEUE" "$RUNNING"

# Oldest first. Entry filenames are timestamp-prefixed so lexical sort == time order.
for f in $(ls -1 "$QUEUE" 2>/dev/null | sort); do
  # The atomic claim. rename() either moves the file (we win) or fails
  # because another claimant already moved it (we lose, try next).
  if mv "$QUEUE/$f" "$RUNNING/$f" 2>/dev/null; then
    echo "$RUNNING/$f"
    exit 0
  fi
done

exit 1
