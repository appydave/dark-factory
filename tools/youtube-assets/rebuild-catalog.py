#!/usr/bin/env python3
# rebuild-catalog.py
# Re-aggregate v-aitldr/catalog/catalog.json from the per-folder meta.json files.
# meta.json is the SOURCE OF TRUTH (recat-writeback.py writes there). catalog.json
# is a derived index — this keeps it in sync so it never goes stale.
# Prints: CATALOG records=<n> by_format=<...> transcript_enriched=<n> corrected=<n>
import json, glob, os
from collections import Counter

CAT = "/Users/davidcruwys/dev/video-projects/v-aitldr/catalog"
SNAPSHOT_DATE = os.environ.get("SNAPSHOT_DATE", "2026-05-30")

metas = [json.load(open(m)) for m in glob.glob(f"{CAT}/**/meta.json", recursive=True)]
# stable order: newest first, then youtubeId
metas.sort(key=lambda m: (m.get("published", ""), m.get("youtubeId", "")), reverse=True)

fmt = Counter(m["format"] for m in metas)
enriched = sum(1 for m in metas if m.get("transcript_enriched"))
corrected = sum(1 for m in metas if m.get("transcript_changed"))

catalog = {
    "snapshot": {
        "source": "per-folder meta.json (rebuilt aggregate)",
        "snapshot_date": SNAPSHOT_DATE,
        "source_channel": "https://www.youtube.com/@AITLDR",
        "count": len(metas),
        "counts_by_format": {"video": fmt.get("video", 0), "short": fmt.get("short", 0)},
        "transcript_enriched": enriched,
        "categories_corrected": corrected,
    },
    # provenance of fields across the whole record set
    "verified":  ["title", "youtubeId", "format", "duration", "published"],
    "generated": ["slug", "category", "description", "tags", "featured"],
    "transcript_grounded": ["category_transcript", "description_transcript", "transcript_changed"],
    "count": len(metas),
    "records": metas,   # full per-video records, transcript fields included
}
json.dump(catalog, open(f"{CAT}/catalog.json", "w"), indent=2, ensure_ascii=False)
print(f"CATALOG records={len(metas)} by_format={dict(fmt)} transcript_enriched={enriched} corrected={corrected}")
