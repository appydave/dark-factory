#!/usr/bin/env bash
#
# test-atomic-claim.sh — prove the claim mutex under concurrency.
#
# Drops N entries into a sandbox queue, fires CLAIMERS parallel claimers
# (simulating the staggered sessions), and asserts every entry is claimed
# exactly once: no double-claims, no lost entries.
#
# This is THE spike test. If it passes, the 4-session model is safe.

set -euo pipefail

N="${1:-50}"
CLAIMERS="${2:-4}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SANDBOX="$ROOT/.test-sandbox"
LOG="$SANDBOX/claims.log"

# Fresh sandbox every run.
rm -rf "$SANDBOX"
mkdir -p "$SANDBOX/queue" "$SANDBOX/running"

# Seed N entries with sortable names.
for i in $(seq -w 1 "$N"); do
  echo "{\"queue_id\":\"test-$i\"}" > "$SANDBOX/queue/entry-$i.json"
done

# Each claimer loops, claiming until the queue is empty for it.
claimer() {
  local who="$1"
  local out
  while out=$(WT_ENGINE_DIR="$SANDBOX" "$ROOT/bin/claim-next.sh" "$who" 2>/dev/null); do
    [ -z "$out" ] && break
    echo "$who $(basename "$out")" >> "$LOG"
  done
}

for c in $(seq 1 "$CLAIMERS"); do
  claimer "claimer-$c" &
done
wait

# Assertions.
total_claims=$(wc -l < "$LOG" | tr -d ' ')
unique_claims=$(awk '{print $2}' "$LOG" | sort -u | wc -l | tr -d ' ')
in_running=$(ls -1 "$SANDBOX/running" | wc -l | tr -d ' ')
left_in_queue=$(ls -1 "$SANDBOX/queue" 2>/dev/null | wc -l | tr -d ' ')

echo "─────────────────────────────────────"
echo " entries seeded   : $N"
echo " parallel claimers : $CLAIMERS"
echo " total claims      : $total_claims"
echo " unique claims     : $unique_claims"
echo " moved to running/ : $in_running"
echo " left in queue/    : $left_in_queue"
echo " claims per claimer:"
awk '{print $1}' "$LOG" | sort | uniq -c | sed 's/^/   /'
echo "─────────────────────────────────────"

if [ "$total_claims" -eq "$N" ] && \
   [ "$unique_claims" -eq "$N" ] && \
   [ "$in_running" -eq "$N" ] && \
   [ "$left_in_queue" -eq 0 ]; then
  echo "PASS — every entry claimed exactly once, zero double-claims, zero lost."
  rm -rf "$SANDBOX"
  exit 0
else
  echo "FAIL — invariant violated (see $SANDBOX)."
  exit 1
fi
