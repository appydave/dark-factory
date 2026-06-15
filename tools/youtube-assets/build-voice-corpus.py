#!/usr/bin/env python3
# build-voice-corpus.py — concatenate every per-video transcript in a catalog into ONE
# readable file: the channel's complete as-aired spoken voice, in chronological order.
# This is the single file to read to understand the creator's tone of voice.
#
# Usage:
#   python3 build-voice-corpus.py --cat <catalog> --out <file.md> [--channel "AppyDave"]
import argparse, glob, json, os, re


def words(s):
    return len(re.findall(r"\S+", s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cat", required=True, help="catalog dir (has videos/ and shorts/)")
    ap.add_argument("--out", required=True, help="output markdown file")
    ap.add_argument("--channel", default="")
    args = ap.parse_args()

    items = []
    for m in glob.glob(f"{args.cat}/**/meta.json", recursive=True):
        folder = os.path.dirname(m)
        tpath = os.path.join(folder, "transcript.txt")
        if not os.path.exists(tpath):
            continue
        meta = json.load(open(m))
        text = open(tpath, encoding="utf-8").read().strip()
        if not text:
            continue
        items.append((meta.get("published", ""), meta, text))

    items.sort(key=lambda x: x[0])  # chronological — oldest first, to show voice evolution

    total_words = sum(words(t) for _, _, t in items)
    head = [
        f"# {args.channel or 'Channel'} — Voice Corpus",
        "",
        f"Every as-aired transcript from the catalog, oldest first. This is the complete "
        f"spoken-voice record — read it to understand tone, phrasing, and delivery.",
        "",
        f"- Videos with transcripts: **{len(items)}**",
        f"- Total words: **{total_words:,}**",
        f"- Source: `{args.cat}`",
        "",
        "---",
        "",
    ]

    body = []
    for pub, meta, text in items:
        fmt = meta.get("format", "")
        body.append(f"## {pub} · {meta.get('title','(untitled)')}")
        body.append(f"_{fmt} · {meta.get('duration','')} · {meta.get('category','')} · "
                    f"https://youtu.be/{meta.get('youtubeId','')}_")
        body.append("")
        body.append(text)
        body.append("")
        body.append("---")
        body.append("")

    open(args.out, "w", encoding="utf-8").write("\n".join(head + body))
    print(f"WROTE {args.out}")
    print(f"  transcripts={len(items)}  words={total_words:,}  "
          f"bytes={os.path.getsize(args.out):,}")


if __name__ == "__main__":
    main()
