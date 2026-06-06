#!/usr/bin/env bash
# bulk-fetch.sh — paced, idempotent, circuit-broken fetch of thumb+transcript for ALL catalog videos.
# bash 3.2 compatible (no mapfile).
set -uo pipefail
CAT="/Users/davidcruwys/dev/video-projects/v-aitldr/catalog"
TOOL="/Users/davidcruwys/dev/ad/apps/dark-factory/tools/youtube-assets"
LOG="$TOOL/run.log"
SINGLE="$TOOL/fetch-assets.sh"

total=$(find "$CAT/videos" "$CAT/shorts" -maxdepth 2 -name meta.json | wc -l | tr -d ' ')
echo "$(date '+%H:%M:%S') START bulk-fetch: $total folders" | tee -a "$LOG"

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

  sleep $((8 + RANDOM % 8))
done < <(find "$CAT/videos" "$CAT/shorts" -maxdepth 2 -name meta.json | sort)

echo "$(date '+%H:%M:%S') END: done=$done_cnt fetched=$fetched skipped=$skipped failed=$failed of $total" | tee -a "$LOG"
