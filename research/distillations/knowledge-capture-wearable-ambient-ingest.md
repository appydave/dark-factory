---
distillation_id: knowledge-capture-wearable-ambient-ingest
stage: knowledge-capture
intent: "Fetch, classify, and route ambient audio transcripts (wearable, meeting, voice) into structured brain-ready content"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:omi
  - appydave-plugins:skill:omi-fetch
  - appydave-plugins:skill:omi-extract
  - appydave-plugins:skill:omi-extract-haiku
  - appydave-plugins:skill:omi-query
  - appydave-plugins:skill:omi-schedule
  - appydave-plugins:skill:krisp-fetch
  - appydave-plugins:skill:wistia-transcript
  - appydave-plugins:skill:youtube-transcript
  - gbrain:skill:voice-note-ingest
  - gbrain:skill:meeting-ingestion
  - gbrain:skill:meeting-sync
  - gbrain:skill:signal-detector
winner_mechanism: appydave-plugins:skill:omi
---

# Unified Skill: Wearable & Ambient Ingest

## Intent

Fetch transcripts from ambient/wearable devices (OMI pendant, Krisp meetings), video platforms (YouTube, Wistia), and voice notes; classify and tag them with structured frontmatter; and route brain-update candidates to a review queue.

## Winner's Mechanism

David's `omi` orchestrator is the winner: it chains sync (API fetch + git commit) → extract (Gemini classification + frontmatter write) → backlog-report (surface brain-update candidates) → discovery-query-refresh (keep random-queries.yml current). It's a full four-stage pipeline with model-tier awareness (flash-lite vs flash), quota handling, and a routing layer (`query_omi --routing brain-update`) that connects raw transcripts to downstream brain curation work. The five OMI sub-skills (`omi-fetch`, `omi-extract`, `omi-extract-haiku`, `omi-query`, `omi-schedule`) are already correctly factored — each does one thing.

The gap is the adjacent transcript sources (`krisp-fetch`, `wistia-transcript`, `youtube-transcript`) are siloed. Each fetches from a different API, but none routes into the same `brain-update` backlog that `omi-query` produces. The result: OMI conversations appear in the routing layer; Krisp meetings, YouTube research, and Wistia content do not.

## Existing-skill nesting (upgrading existing skills)

- **Existing mechanism (`omi` pipeline)**: Four-stage: fetch → classify → backlog-report → query-refresh. Runs against OMI wearable API. The extract stage writes YAML frontmatter with `routing` field. `omi-query` can filter by `routing: brain-update`.
- **Existing mechanisms (silo skills)**: `krisp-fetch` — meeting recordings/transcripts from Krisp API. `wistia-transcript` — video transcripts from Wistia. `youtube-transcript` — YouTube captions. Each produces raw text; none writes frontmatter.
- **New mechanism's grain**: Normalised frontmatter schema across all ambient transcript sources, so `query_omi --routing brain-update` (or a unified `query_transcripts`) can surface brain-update candidates from all sources, not just OMI.
- **Nesting rule**: Each silo skill (krisp-fetch, wistia-transcript, youtube-transcript) gains a post-fetch classification step — either by invoking the `omi-extract` classifier with a source-type hint, or by extending the extract script's `--source` flag. The `omi` orchestrator becomes a `transcript-pipeline` orchestrator that accepts `--source omi|krisp|youtube|wistia` and routes accordingly. The existing OMI-specific commands keep their names for ergonomics; the unified entry point is additive.

## Non-overlapping ideas folded in

- From `gbrain:meeting-ingestion`: **Attendee enrichment + entity extraction** — after meeting transcript ingest, enrich with attendee context from brain pages and extract decisions/action-items as structured entities — `complexity: medium | optional: true | prerequisite: "brain has attendee pages"`. David's Krisp transcripts currently land as raw text; this turns them into brain-searchable decisions.
- From `gbrain:meeting-sync`: **Circleback auto-import recipe** — meeting transcripts from Circleback (integration recipe: poll API, hash-deduplicate, write frontmatter) — `complexity: medium | optional: true | prerequisite: "Circleback account active"`. If David uses Circleback, this avoids the manual Krisp step.
- From `gbrain:signal-detector`: **Ambient signal-to-brain-update trigger** — always-on pattern: transcripts classified as containing knowledge signals (decisions, hypotheses, plans) auto-queue for brain review without manual invocation — `complexity: high | optional: true | prerequisite: "omi-schedule running"`. The `omi-schedule` launchd job already runs periodic sync; the signal-detector pattern adds a secondary classification that flags high-value transcripts for immediate attention rather than waiting for daily backlog review.
- From `gbrain:voice-note-ingest`: **Exact-phrasing preservation** — when ingesting voice notes (as opposed to ambient conversation transcripts), never paraphrase; preserve the speaker's exact phrasing because the wording often carries intent the LLM would otherwise normalise away — `complexity: low | optional: false | prerequisite: none"`. OMI's extract step currently summarises; voice-note mode should be a passthrough.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave:omi` | Full 4-stage pipeline orchestrator — the winner | — |
| `appydave:omi-fetch` | API fetch sub-skill | — |
| `appydave:omi-extract` | Gemini classification + frontmatter | — |
| `appydave:omi-extract-haiku` | Haiku model variant for Max plan | — |
| `appydave:omi-query` | Routing query layer | — |
| `appydave:omi-schedule` | launchd schedule management | — |
| `appydave:krisp-fetch` | Krisp API transcript fetch | Not yet integrated into routing layer |
| `appydave:wistia-transcript` | Wistia API transcript fetch | Not yet integrated into routing layer |
| `appydave:youtube-transcript` | YouTube caption fetch | Not yet integrated into routing layer |
| `gbrain:meeting-ingestion` | Attendee enrichment + decision extraction | GBrain's brain-linked attendee pages |
| `gbrain:meeting-sync` | Circleback auto-import recipe | Circleback-specific connector |
| `gbrain:signal-detector` | High-value signal auto-flagging | GBrain's always-on daemon model |
| `gbrain:voice-note-ingest` | Exact-phrasing preservation mode | GBrain's voice-note-as-brain-page pattern |

## Draft SKILL.md frontmatter

```yaml
name: omi
description: >
  OMI pipeline orchestrator — syncs new transcripts from the OMI API then extracts and
  classifies them with Gemini. Use when user says: "sync and extract OMI", "run omi pipeline",
  "omi sync", "process omi", "omi fetch and extract", "catch up on omi", "run omi",
  "update omi", "update discovery queries", "refresh random context", "update omi queries",
  "process krisp meetings", "classify youtube transcript", "route transcripts to brain".
argument-hint: "[--source omi|krisp|youtube|wistia] [--all] [--model gemini-2.5-flash]"
allowed-tools: Bash(python3:*), Bash(query_omi:*), Bash(git:*), Read, Write
```

## Open questions for David

1. **Unified query layer**: Should `query_omi` be renamed/extended to `query_transcripts` to cover all sources, or should it remain OMI-specific with separate `query_krisp`, `query_youtube` equivalents? The unified approach is more powerful but changes the CLI interface.

2. **Krisp classification model**: OMI uses Gemini for classification. Krisp transcripts are often longer (full meeting). Should meeting transcripts use a different prompt (structured meeting extraction: decisions, action-items, attendees) rather than the OMI conversation classifier?

3. **Signal detector automation**: The `omi-schedule` launchd job syncs on a timer. Should it also run the signal-detector pass automatically, or should that remain a manual step to control noise?
