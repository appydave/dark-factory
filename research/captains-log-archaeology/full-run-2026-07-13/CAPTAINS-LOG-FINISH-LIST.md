# Captain's Log — finish list (from 6-month archaeology, deterministic)

## Open loops on Captain's Log (27)

- **Captain's Log UX overhaul** — first 2026-07-13, last 2026-07-13, seen 1×
- **actions and notes on captures** — first 2026-07-13, last 2026-07-13, seen 1×
- **temporal and thematic linking of captures** — first 2026-07-13, last 2026-07-13, seen 1×
- **Captain's Log Kybernesis extension build** — first 2026-07-12, last 2026-07-13, seen 2×
- **Plaud refresh-token automation** — first 2026-07-12, last 2026-07-12, seen 1×
- **ingestion data destinations and app config** — first 2026-07-12, last 2026-07-12, seen 1×
- **captains-log unified ingestion** — first 2026-07-11, last 2026-07-11, seen 1×
- **captains-log kyber extension hosting** — first 2026-07-09, last 2026-07-09, seen 1×
- **Captain's Log extension replaces OMI extension** — first 2026-07-06, last 2026-07-06, seen 2×
- **OMI vs Plaud transcription bake-off** — first 2026-07-06, last 2026-07-06, seen 2×
- **Unified ingestion controller for OMI+Plaud** — first 2026-07-05, last 2026-07-05, seen 1×
- **unify OMI+Plaud ingestion pipeline** — first 2026-07-05, last 2026-07-05, seen 1×
- **OMI list metadata + sequential item codes** — first 2026-07-04, last 2026-07-04, seen 1×
- **morning transcript routing** — first 2026-06-14, last 2026-06-14, seen 1×
- **omi brain release readiness** — first 2026-06-13, last 2026-06-13, seen 1×
- **multi-stream conversational inbox concept** — first 2026-04-12, last 2026-04-12, seen 1×
- **OMI scheduled daily processing** — first 2026-04-01, last 2026-04-01, seen 1×
- **OMI extraction backfill** — first 2026-03-30, last 2026-03-30, seen 1×
- **shared knowledge systems across machines** — first 2026-03-20, last 2026-03-20, seen 1×
- **loop-based ingestion automation** — first 2026-03-11, last 2026-03-11, seen 1×
- **upcoming videos and paid apps master list missing** — first 2026-03-09, last 2026-03-09, seen 1×
- **OMI ingestion pipeline design** — first 2026-03-05, last 2026-03-05, seen 2×
- **OMI ingestion + morning briefing system** — first 2026-03-04, last 2026-03-04, seen 2×
- **OMI transcript ingestion recipe** — first 2026-03-04, last 2026-03-04, seen 1×
- **OMI ingestion pipeline verification** — first 2026-03-04, last 2026-03-04, seen 1×
- **three recording blockers (OMI import, Stream Deck, Ecamm scenes)** — first 2026-03-03, last 2026-03-03, seen 1×
- **todo/journal micro-app design** — first 2026-03-01, last 2026-03-01, seen 1×

## Every action targeting Captain's Log (17), newest first

- [2026-07-13] Route all transcripts and synopses through a vocabulary correction system keyed to David's real product names
- [2026-07-13] Make OMI/Claude transcript ingestion a durable launchd-style job (30-min cadence, 07:00-22:00) with a manual trigger in the app
- [2026-07-13] Hide empty/noise captures by default behind a toggle and add semantic source coloring (OMI green, Plaud blue)
- [2026-07-13] Centralize tag storage/governance so missing tags (captains-log, kybernesis, lars) are fixed future-proof, possibly a dedicated tag-management app
- [2026-07-13] Automate the Plaud refresh-token refetch (currently a manual browser-console paste), likely via Playwright
- [2026-07-13] Add filter toggles for tags, timeframe, keyword search, and noise (hidden by default)
- [2026-07-13] Add a show-markdown/show-transcript button and a light theme to the capture view
- [2026-07-12] Mine prior Claude conversations on captains-log/OMI/Plaud into a detailed requirements doc and spec, then build the extension
- [2026-07-12] Build an easy refresh-token re-fetch plus storage against the Plaud ingestion provider
- [2026-07-12] Add ingestion-destination configuration for Plaud/OMI raw transcripts
- [2026-07-11] Extend Captain's Log ingestion beyond OMI/Plaud to email-forwarded YouTube links (transcript extraction) and articles (scraping), with analyze/summarize/ontology-tag pipeline
- [2026-07-09] Make the Captain's Log pulse configurable (daily window, ~10-minute cadence) through the extension system
- [2026-07-09] Host the Captain's Log viewer as a KyberAgent extension with LLM access via the daemon
- [2026-07-05] Suggest 3-4 names for the unified ingestion controller tool
- [2026-07-05] Research a Claude-based transcription pipeline that ingests OMI/Plaud audio+video and runs tagging/ontology
- [2026-07-05] Compare OMI vs Plaud transcript data structures for format quirks before unifying
- [2026-04-12] Pull OMI transcripts from the API endpoint into a central inbox and run a tagging ontology over them
