#!/usr/bin/env bash
# Full census shoot: local m4pro designs, then mirror m4mini roots and shoot the rest.
# shoot.py dedupes by (repo,design_id) against shots.json, so shared designs shoot once.
set -uo pipefail
cd "$(dirname "$0")"
MINI=davidcruwys@100.82.235.39
MIRROR=/tmp/mocha-mini-mirror

echo "### 1/3  local m4pro shoot"
python3 shoot.py --tsv out/census-m4pro.tsv 2>&1 | grep -vE '^127\.0\.0\.1' | tail -40

echo "### 2/3  mirror m4mini source roots -> $MIRROR"
rm -rf "$MIRROR"; mkdir -p "$MIRROR"
awk -F'\t' '$2=="source"{print $3}' out/census-m4mini.tsv | sort -u | while read -r root; do
  dest="$MIRROR$root"
  mkdir -p "$dest"
  rsync -a --delete --exclude node_modules "$MINI:$root/" "$dest/" 2>/dev/null \
    && echo "  synced $root" || echo "  FAIL sync $root"
done

# rewrite mini tsv paths to mirror; keep machine label = m4mini
awk -F'\t' -v m="$MIRROR" 'BEGIN{OFS="\t"} $2=="source"{ $3=m $3; $5=m $5; print }' \
  out/census-m4mini.tsv > out/census-mini-mirror.tsv

echo "### 3/3  shoot mirrored m4mini designs (dedupe skips already-shot)"
python3 shoot.py --tsv out/census-mini-mirror.tsv 2>&1 | grep -vE '^127\.0\.0\.1' | tail -60

echo "### DONE  total shots:"
python3 -c "import json;print(len(json.load(open('out/shots/shots.json'))))"
