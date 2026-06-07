#!/usr/bin/env bash
# retry.sh — retry-with-backoff for FAILED jobs (runs as Marshall's Monitor).
#
# Symphony §8.4: a failed job shouldn't just die. When a job lands in failed/
# (run-next-workflow step 5 moves failures there), re-queue it after an EXPONENTIAL
# backoff, up to RETRY_MAX attempts; after that, leave it terminal in failed/.
#
# Signal = failed/<queue_id>.json. Each ticket carries "attempt" (default 1).
#   eligible if: attempt < RETRY_MAX  AND  (now - failed_mtime) >= backoff(attempt)
#   backoff(attempt) = RETRY_BASE_SECONDS * 2^(attempt-1)   (e.g. 30s, 60s, 120s)
#   on retry: attempt++, write last_retry_at, move failed/<id> -> queue/<id>.
# A re-queued ticket is picked up by the next dispatch (auto-dispatch on re-queue
# is the queue-Monitor's job, C3c — separate). Idempotent-ish; safe to run repeatedly.
#
# Env: RETRY_MAX (default 3), RETRY_BASE_SECONDS (default 30),
#      RETRY_POLL_SECONDS (default 10), RETRY_ONCE=1 (single pass, for tests).
set -uo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
FAILED="$BASE/failed"; QUEUE="$BASE/queue"
MAX="${RETRY_MAX:-3}"; BASE_S="${RETRY_BASE_SECONDS:-30}"; POLL="${RETRY_POLL_SECONDS:-10}"
mkdir -p "$FAILED" "$QUEUE"
shopt -s nullglob

while true; do
  now=$(date +%s)
  for f in "$FAILED"/*.json; do
    qid=$(basename "$f" .json)
    attempt=$(node -e 'try{process.stdout.write(String(require(process.argv[1]).attempt||1))}catch{process.stdout.write("1")}' "$f" 2>/dev/null || echo 1)
    [ "$attempt" -ge "$MAX" ] && continue                       # terminal — give up, leave in failed/
    failed_at=$(stat -f %m "$f" 2>/dev/null || echo "$now")
    backoff=$(( BASE_S * (1 << (attempt - 1)) ))
    [ $(( now - failed_at )) -lt "$backoff" ] && continue       # backoff not elapsed yet
    next=$(( attempt + 1 ))
    # bump attempt + re-queue (write to queue/ first, then drop the failed/ copy)
    node -e 'const fs=require("fs");const t=require(process.argv[1]);t.attempt=Number(process.argv[2]);t.last_retry_at=new Date().toISOString();fs.writeFileSync(process.argv[3],JSON.stringify(t,null,2)+"\n")' "$f" "$next" "$QUEUE/$qid.json" \
      && rm -f "$f" \
      && echo "retrying $qid (attempt $next/$MAX, backoff was ${backoff}s)"
  done
  [ -n "${RETRY_ONCE:-}" ] && break
  sleep "$POLL"
done
