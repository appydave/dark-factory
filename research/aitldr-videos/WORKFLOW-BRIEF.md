# WORKFLOW-BRIEF — AI-TLDR channel → business-data.json

> Turn the AI-TLDR YouTube channel into a verified business-data document (real rows)
> that the `astro-website` recipe can consume. Drops straight into Dark Factory's
> load → assess → store shape with a per-item contract.

## PATHS-DECLARED

**ASSUMED BASE:** `/Users/davidcruwys/dev/ad/apps/dark-factory` (verified real — no rebase needed)

### INPUTS
| path | exists | role |
|------|--------|------|
| `/Users/davidcruwys/dev/aitldr/aitldr-skool/recipes/astro-website/examples/aitldr/schema.md` | ✅ | category vocab (6 slugs) + `content_schema` (required fields per entry) |
| `research/aitldr-videos/config.yaml` | ✅ (stubbed) | run config — answers to the four open questions |

### OUTPUTS
| path | kind | role |
|------|------|------|
| `research/aitldr-videos/raw/videos.jsonl` | intermediate | raw yt-dlp dump, one record/line |
| `research/aitldr-videos/enriched/<slug>.json` | intermediate | one per video — the §5 contract |
| `research/aitldr-videos/business-data.json` | **DELIVERABLE** | feeds the recipe |
| `research/aitldr-videos/report.md` | summary | counts, category histogram, featured list, quarantine |

`research/aitldr-videos/` exists; `raw/` and `enriched/` are created by the workflow.

---

## 1. Intent

- **One sentence:** Turn the AI-TLDR YouTube channel into a verified business-data document (real rows) that the `astro-website` recipe can consume.
- **Trigger:** Before building/rebuilding ai-tldr.com, or to refresh data as the channel grows.
- **Success signal:** `business-data.json` contains one record per chosen video; every record has all required `content_schema` fields; every `category` ∈ the 6 schema slugs; `provenance.generated` contains only derived fields (`slug`, `category`, `description`) — never `title`/`youtubeId`/`duration`/`published`.

## 2. Inputs

- **schema.md** · md · provides `content_schema` (required fields per entry) + `categories[]` (6 slugs: `ai-tools`, `workflows`, `video-creation`, `content`, `automation`, `community`) · required: true
- **config.yaml** · yaml · `{ channel_url, subset, featured_rule, featured_count, description_policy, description_max_chars, category_slugs }` · required: true

## 3. Outputs

- `raw/videos.jsonl` · jsonl · one yt-dlp record/line (`id,title,duration,upload_date,description,…`) · overwrite · workflow creates `raw/`
- `enriched/<slug>.json` · json · the §5 contract · one-file-per-record · workflow creates `enriched/`
- `business-data.json` · json · `{ source, verified[], generated[], records:[ <content_schema record> … ] }` · overwrite
- `report.md` · md · counts, category histogram, featured list, rows quarantined for missing fields · overwrite

## 4. Phases

1. **fetch** — run `yt-dlp` on `config.channel_url`, dump every video (per `subset`) as JSON. `parallel: false`. reads `config.yaml`. writes `raw/videos.jsonl`.
2. **enrich** — one sub-agent per video row: derive `slug`, classify `category` into one of the 6 schema slugs, normalize `duration` (sec→`M:SS`) and `published` (`upload_date`→ISO), write `description` per `description_policy`, propose `featured_candidate`, extract `tags`, record provenance. `parallel: true` — fan-out unit: one agent per video. reads its row + `schema.md`. writes `enriched/<slug>.json`.
3. **assemble** — reduce: dedup, sort by `published` desc, apply `featured_rule`, validate (every `category` ∈ schema slugs, every required `content_schema` field present — quarantine failures to the report), build the `verified`/`generated` provenance block. `parallel: false`. reads `enriched/*.json` + `schema.md`. writes `business-data.json` + `report.md`.

> Optional Phase 4 "emit-standard" (business-data.json → markdown in the website's `src/content/videos/`) is **deliberately omitted** — that is the recipe's job. The clean seam is `business-data.json`.

## 5. Per-item contract (phase 2 fan-out)

Each sub-agent returns exactly (field names match `content_schema`):

```json
{
  "title":      "string",   // COPIED verbatim from source
  "slug":       "string",   // kebab-case, derived
  "youtubeId":  "string",   // COPIED (id, not full URL)
  "duration":   "string",   // "M:SS", normalized from source seconds
  "published":  "string",   // "YYYY-MM-DD", from upload_date
  "category":   "ai-tools|workflows|video-creation|content|automation|community",  // CLASSIFIED
  "description":"string",   // <=160 chars, fresh summary (GENERATED)
  "tags":       ["string"],
  "featured_candidate": false,
  "verified":   ["string"], // copied verbatim — MUST include title, youtubeId, duration, published
  "generated":  ["string"]  // derived — slug, category, description
}
```

## 6. Decisions (locked) & assumptions

**Locked answers:**
- **Subset:** `all` (~324 videos) — full channel dump, largest fan-out.
- **Featured rule:** `top_recent`, count 6 — mark the 6 newest videos featured.
- **Description policy:** `fresh_summary` — agent writes a clean ≤160-char summary; lands in `generated[]`.
- **Category:** derived/classified → recorded in `generated[]`, never `verified[]`. Accepted as honest provenance.

**Assumptions:** yt-dlp installed (✅ 2026.02.21) and channel public; `research/aitldr-videos/` is the workspace; `business-data.json` is the final deliverable (no markdown emit).
