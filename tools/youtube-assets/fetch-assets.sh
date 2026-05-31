#!/usr/bin/env bash
# fetch-assets.sh <youtubeId> <target_dir>
# Drops thumb.jpg + transcript.vtt + transcript.txt into target_dir. Idempotent.
set -uo pipefail
ID="$1"; DIR="$2"; URL="https://www.youtube.com/watch?v=$ID"
mkdir -p "$DIR"
got=""

# 1) THUMBNAIL — direct from i.ytimg.com (no yt-dlp; predictable URL). maxres, fallback hq.
if [ ! -f "$DIR/thumb.jpg" ]; then
  if curl -sfL "https://i.ytimg.com/vi/$ID/maxresdefault.jpg" -o "$DIR/thumb.jpg"; then got="${got}thumb(max) "
  elif curl -sfL "https://i.ytimg.com/vi/$ID/hqdefault.jpg" -o "$DIR/thumb.jpg"; then got="${got}thumb(hq) "
  else got="${got}thumb-FAIL "; fi
else got="${got}thumb(skip) "; fi

# 2) TRANSCRIPT VTT — yt-dlp auto-captions (proven to work)
if [ ! -f "$DIR/transcript.vtt" ]; then
  yt-dlp --no-update --skip-download --write-auto-subs --sub-langs en --sub-format vtt \
    -o "$DIR/.cap.%(ext)s" "$URL" >/dev/null 2>&1
  f=$(ls "$DIR"/.cap*.vtt 2>/dev/null | head -1)
  if [ -n "$f" ]; then mv "$f" "$DIR/transcript.vtt"; rm -f "$DIR"/.cap*.vtt 2>/dev/null; got="${got}vtt "
  else got="${got}vtt-FAIL "; fi
else got="${got}vtt(skip) "; fi

# 3) TRANSCRIPT TXT — clean text from the vtt
if [ -f "$DIR/transcript.vtt" ] && [ ! -f "$DIR/transcript.txt" ]; then
  python3 - "$DIR/transcript.vtt" "$DIR/transcript.txt" <<'PY'
import re,sys
src,dst=sys.argv[1],sys.argv[2]
out=[]
for l in open(src,encoding='utf-8'):
    l=l.rstrip('\n')
    if not l or l.startswith(('WEBVTT','Kind:','Language:')) or '-->' in l or re.match(r'^\d+$',l): continue
    l=re.sub(r'<[^>]+>','',l); l=re.sub(r'align:\S+|position:\S+','',l).strip()
    if l and (not out or out[-1]!=l): out.append(l)
open(dst,'w',encoding='utf-8').write(' '.join(out))
PY
  got="${got}txt "
fi
echo "$ID  ->  $got"
