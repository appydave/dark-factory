#!/usr/bin/env python3
# sync-to-catalog.py — BRIDGE: turn a YouTube-API channel sync into a Dark Factory catalog.
#
# The Dark Factory pipeline (bulk-fetch.sh -> AI enrich -> rebuild-catalog.py) assumes the
# per-video `<slug>--<id>/meta.json` folders already exist. When you ALREADY have a
# `published/<channel>/` sync (channel.json + last-sync.json + videos/<id>/{metadata.json,
# thumbnail.jpg, transcript.txt}), there is no need to re-download anything from YouTube.
# This script adapts that sync into the catalog layout, locally, with zero YouTube calls.
#
# It REPLACES Stage 1 (build folders) AND Stage 2 (fetch assets) of the channel-catalog
# workflow. After running it, go straight to Stage 3 (AI enrich) and Stage 4 (rebuild).
#
# Idempotent: a target folder that already has meta.json + transcript is skipped.
#
# Usage:
#   sync-to-catalog.py --src <published/channel> --dst <catalog> [--shorts-file <ids.txt>]
#
# Example (AppyDave):
#   python3 sync-to-catalog.py \
#     --src /Users/davidcruwys/dev/video-projects/published/appydave \
#     --dst /Users/davidcruwys/dev/video-projects/v-appydave/catalog \
#     --shorts-file /tmp/appydave_shorts.txt
import argparse, glob, json, os, re, shutil, sys


def slugify(title: str) -> str:
    s = (title or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"


def parse_duration(iso: str):
    """ISO-8601 'PT1H2M3S' -> ('1:02:03', total_seconds). Returns ('', 0) on miss."""
    m = re.match(r"^P(?:T)?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m:
        return "", 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    total = h * 3600 + mi * 60 + s
    return (f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"), total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="published/<channel> sync dir")
    ap.add_argument("--dst", required=True, help="target catalog dir")
    ap.add_argument("--shorts-file", help="optional file of YouTube IDs known to be Shorts")
    ap.add_argument("--short-max-seconds", type=int, default=60,
                    help="duration <= this is treated as a Short when not in --shorts-file")
    args = ap.parse_args()

    src, dst = args.src.rstrip("/"), args.dst.rstrip("/")
    shorts_ids = set()
    if args.shorts_file and os.path.exists(args.shorts_file):
        shorts_ids = {l.strip() for l in open(args.shorts_file) if l.strip()}

    metas = sorted(glob.glob(f"{src}/videos/*/metadata.json"))
    if not metas:
        sys.exit(f"no metadata.json under {src}/videos/ — is --src correct?")

    n_video = n_short = n_txt = n_notxt = n_skip = 0
    for mpath in metas:
        vid_dir = os.path.dirname(mpath)
        md = json.load(open(mpath))
        yid = md.get("id") or os.path.basename(vid_dir)
        title = md.get("title", "")
        slug = slugify(title)
        dur_str, dur_secs = parse_duration(md.get("duration", ""))
        is_short = (yid in shorts_ids) or (0 < dur_secs <= args.short_max_seconds)
        fmt = "short" if is_short else "video"
        folder = f"{slug}--{yid}"
        out_dir = os.path.join(dst, "shorts" if is_short else "videos", folder)

        has_txt = os.path.exists(os.path.join(vid_dir, "transcript.txt"))

        # idempotent skip: already adapted with its transcript
        meta_out = os.path.join(out_dir, "meta.json")
        if os.path.exists(meta_out) and (os.path.exists(os.path.join(out_dir, "transcript.txt")) or not has_txt):
            n_skip += 1
            continue

        os.makedirs(out_dir, exist_ok=True)
        meta = {
            "title": title,
            "slug": slug,
            "youtubeId": yid,
            "format": fmt,
            "duration": dur_str,
            "published": (md.get("publishedAt") or "")[:10],
            "folder": folder,
        }
        json.dump(meta, open(meta_out, "w"), indent=2, ensure_ascii=False)

        # provenance: keep the original API record alongside
        shutil.copyfile(mpath, os.path.join(out_dir, "source.json"))

        th = os.path.join(vid_dir, "thumbnail.jpg")
        if os.path.exists(th):
            shutil.copyfile(th, os.path.join(out_dir, "thumb.jpg"))

        if has_txt:
            shutil.copyfile(os.path.join(vid_dir, "transcript.txt"),
                            os.path.join(out_dir, "transcript.txt"))
            n_txt += 1
        else:
            n_notxt += 1

        if is_short:
            n_short += 1
        else:
            n_video += 1

    total_new = n_video + n_short
    print(f"ADAPTED new={total_new} (video={n_video} short={n_short})  "
          f"transcripts={n_txt} missing_transcript={n_notxt}  skipped={n_skip}")
    print(f"  src: {src}")
    print(f"  dst: {dst}")


if __name__ == "__main__":
    main()
