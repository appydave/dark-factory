#!/usr/bin/env bash
# bulk-fetch.sh — Stage 2 of the channel-catalog pipeline (careful pace).
#
# WHAT: walks every video folder under a catalog and fills it with thumb.jpg +
#       transcript.vtt + transcript.txt (via fetch-assets.sh). Paced, idempotent,
#       circuit-broken. bash 3.2 compatible (no mapfile).
#   - Idempotent: a folder that already has all three files is skipped.
#   - Polite: sleeps 30–60s between videos; STOPS itself after 6 consecutive caption
#     failures (assumes a YouTube rate-limit). Just re-run later to resume.
#   - For finishing a small remainder faster, use bulk-fetch-fast.sh (8–15s pacing).
#
# WHEN TO SKIP: if you already have a `published/<channel>/` API sync, run
#       sync-to-catalog.py instead — it builds the folders AND the assets locally with
#       no YouTube calls, replacing Stages 1+2 entirely.
#
# CONFIG (env vars; defaults keep the original AITLDR behaviour):
#   CAT   catalog dir to fill   (default: v-aitldr/catalog)
# Paths (TOOL/LOG/SINGLE) self-derive from this script's location — relocatable.
#
# USAGE:
#   bash bulk-fetch.sh                                    # AITLDR (default)
#   CAT=/Users/davidcruwys/dev/video-projects/v-appydave/catalog bash bulk-fetch.sh
set -uo pipefail
CAT="${CAT:-/Users/davidcruwys/dev/video-projects/v-aitldr/catalog}"
TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$TOOL/run.log"
SINGLE="$TOOL/fetch-assets.sh"

total=$(find "$CAT/videos" "$CAT/shorts" -maxdepth 2 -name meta.json | wc -l | tr -d ' ')
echo "$(date '+%H:%M:%S') START bulk-fetch: $total folders  (CAT=$CAT)" | tee -a "$LOG"

done_cnt=0; fetched=0; skipped=0; failed=0; consec_fail=0; i=0
while IFS= read -r meta; do
  d=$(dirname "$meta")
  i=$((i+1))
  id=$(python3 -c "import json;print(json.load(open('$meta'))['youtubeId'])")

  if [ -f "$d/thumb.jpg" ] && [ -f "$d/transcript.vtt" ] && [ -f "$d/transcript.txt" ]; then
    skipped=$((skipped+1)); done_cnt=$((done_cnt+1)); continue
  fi

  res=$("$SINGLE" "$id" "$d")
  echo "$(date '+%H:%M:%S') [$i/$total] $res" >> "$LOG"

  if echo "$res" | grep -q "vtt-FAIL"; then
    failed=$((failed+1)); consec_fail=$((consec_fail+1))
  else
    fetched=$((fetched+1)); done_cnt=$((done_cnt+1)); consec_fail=0
  fi

  if [ "$consec_fail" -ge 6 ]; then
    echo "$(date '+%H:%M:%S') CIRCUIT-BREAK: 6 consecutive caption failures — likely rate-limited. STOPPING. Re-run to resume." | tee -a "$LOG"
    break
  fi

  sleep $((30 + RANDOM % 31))
done < <(find "$CAT/videos" "$CAT/shorts" -maxdepth 2 -name meta.json | sort)

echo "$(date '+%H:%M:%S') END: done=$done_cnt fetched=$fetched skipped=$skipped failed=$failed of $total" | tee -a "$LOG"
