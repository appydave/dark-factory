# Loop Registry — Calibration v2 (THE FIX-4 ARTIFACT)

**Purpose**: Replace run-1's flat `is_open` boolean with a real registry: records clustered by `loop.label` into distinct loops, each with a stable LOOP-ID, first/last seen, mention count, owning thread, and status. Oldest-open first.

**For Agents**:
- LOOP-IDs are stable — cite them (`LOOP-015`), don't re-derive clusters.
- Status vocabulary: `open` (active, evidence of motion), `stale` (open but no mention ≥5 days), `likely-resolved` (later evidence suggests done — verify before closing), `parked` (deliberately deferred).
- Near-duplicate labels were merged (merge notes inline); a loop's mentions may span threads — `owning thread` is where the loop is worked.

**Clustering notes**: 68 non-noise records carry 47 distinct non-empty labels → merged into **35 loops** (label variants merged: doc-watcher×2 wordings, Challenge DV×2, Gling×2, smart-contracts×2, Captain's Log build×4, Achieve×2, dark-factory visibility×1 label ×3 records).

---

## Registry (oldest-open first)

| LOOP-ID | Loop | Thread | First | Last | Mentions | Status |
|---------|------|--------|-------|------|----------|--------|
| LOOP-001 | Extension hosting + recipe monetization (sellable recipes, app/port registry, AionUI/T3 hosts) | kyber-extensions | 06-29 | 06-29 | 1 | **stale** (14d) — monetization framing echoed 07-11 (LOOP-027) but the registry/host-testing actions never resurfaced |
| LOOP-002 | Generalized self-improving recipe skill | recipe-thumbnail | 06-30 | 07-09 | 2 | **stale/parked** — mutated into marketing-router idea (LOOP-024), then thread paused |
| LOOP-003 | Thumbnail generator micro-app (+ prompt-batch TUI revival, shortlisting matrix) | recipe-thumbnail | 06-30 | 06-30 | 2 | **parked** — David reserved it for himself 07-03; known pause to ~late July |
| LOOP-004 | Dark Factory visibility & autonomy (arch docs, Mochaccino viz, morning briefing, build list) | dark-factory | 07-02 | 07-03 | 3 | **open** — partially superseded/absorbed by LOOP-025 governance cleanup + LOOP-034 roadmap reset; treat those as the live edge |
| LOOP-005 | KDD dedicated home location (.kdd interim) | kdd-lisa | 07-03 | 07-03 | 1 | **stale** — "within hours" never confirmed; .kdd-per-project is de-facto standing |
| LOOP-006 | Kyber extension GitHub org naming (appydave-kyber / kybernesis / kyber-extensions) | kyber-extensions | 07-03 | 07-03 | 1 | **stale** — explicitly deferred at creation, never revisited |
| LOOP-007 | Dark Factory harness untested (prototypes exercised Claude Code harness, not DF's) | dark-factory | 07-03 | 07-03 | 1 | **stale** — no record confirms a real server-backed SDK extension shipped; 07-09 governance record implies factory ran, but harness-exercise claim unverified |
| LOOP-008 | Skill registry design (~1100 investigating vs ~100 in-use, staleness, taxonomy search, viewer) | skills-tooling | 07-04 | 07-04 | 1 | **stale** (9d) |
| LOOP-009 | Extension usability enrichment (five thin extensions need search guidance/metadata/docs) | kyber-extensions | 07-04 | 07-07 | 2 | **open** — 07-07 doc-review session shows motion; unfinished |
| LOOP-010 | OMI list metadata + sequential IDs (A001-style) | captains-log | 07-04 | 07-04 | 1 | **likely-resolved** — 07-13 critique references items "A330–A339": sequential IDs shipped; metadata/synopsis partially (Show button still missing) |
| LOOP-011 | Angela + Stravan onboarding (email docs through, coordinate) | ai-meetups | 07-04 | 07-07 | 2 | **likely-resolved** for Angela (repo, invoice, Max plan by 07-07 → superseded by LOOP-020); Stravan never mentioned again |
| LOOP-012 | KDD bridge visibility + read-side wiring ("factory writes knowledge but nothing reads it"; register/document the bridge; OMI last-pulled visibility) | kdd-lisa | 07-04 | 07-04 | 1 | **stale** — high-leverage, no confirmation |
| LOOP-013 | Lisa workflow guardrails + scope (deterministic routing, pattern counting, KDD-folder-only, never per-repo customization) | kdd-lisa | 07-04 | 07-07 | 3 | **open** — repeated correction, no confirmed fix; dormant 6d, drifting to stale |
| LOOP-014 | Gling programmatic control (replace→inject pivot; Electron MCP/API injection; check gling brain) | gling-automation | 07-04 | 07-11 | 3 | **open** — direction settled 07-11, build not started |
| LOOP-015 | **Captain's Log build** (unified OMI+Plaud controller → KyberAgent-hosted extension → durable ingestion + filtering) — merges labels: unify pipeline / controller build / extension build / telemetry ticket / Kybernesis extension build / durable ingestion + filtering | captains-log | 07-05 | 07-13 | 8 | **open — ACTIVE, the corpus's center of gravity** |
| LOOP-016 | Extension SDK capability gaps (host-mediated LLM chat, daemon-owned cron/pulse, publishable SDK) | kyber-extensions | 07-05 | 07-13 | 3 | **open** — ticketed to Kybernesis; blocks LOOP-015's final form |
| LOOP-017 | OMI vs Plaud transcription bake-off (same micro-conversations, both devices) | captains-log | 07-06 | 07-06 | 1 | **stale** — dual-capture pairs from 07-06/07-07 exist as ready data; comparison never run |
| LOOP-018 | KyberAgent agent on Roamy (doc-watcher → whole-system learning agent; Claude Code↔KyberAgent comms; $100 credits; Ian/Martin change reports) | kyberagent-pilot | 07-06 | 07-13 | 3 | **open — stuck** (restated, not executed; weekend deadline missed) |
| LOOP-019 | Challenge DV retainer proposal (reply to Linda's Canva email; demo; $2,750 incl GST from 15 Jul) | client-challenge-dv | 07-07 | 07-13 | 4 | **open — URGENT** (start date 15 Jul = 2 days; proposal unsent since 07-07) |
| LOOP-020 | Achieve MVP (3-week visual demo → schema-driven read-only micro-apps, synthetic data, SupportSignal/DSP mining, dependency-ordered problem map) | client-achieve | 07-07 | 07-09 | 2 | **open** — demo clock ends ~07-28; heavy analysis actions outstanding |
| LOOP-021 | Smart contracts / dual-loop verification → eval rubrics for Dark Factory | agent-verification | 07-07 | 07-09 | 3 | **open** — evaluation action logged 07-09, no verdict |
| LOOP-022 | Frame extension e2e verification (merge to branch, option-2 closed-loop, ~10 failing tests: integration vs unit?) | kyber-extensions | 07-07 | 07-07 | 1 | **stale** — outcome never captured |
| LOOP-023 | Panel vs mount terminology (in-product vs iframe extension versions) | kyber-extensions | 07-07 | 07-07 | 1 | **stale** |
| LOOP-024 | Session→marketing asset router (tweets/YouTube/lead magnets → YouTube/X/Skool) | recipe-thumbnail | 07-09 | 07-09 | 1 | **stale/parked** with thread |
| LOOP-025 | Dark Factory governance & orchestration cleanup (self-approval block rule, war-room→lanes/stations, chaperone/observer, single launch path via Switchboard/WatchTower, main-conversation bootstrap) | dark-factory | 07-09 | 07-09 | 1 | **open — structural**; roadmap reset (LOOP-034) depends on it |
| LOOP-026 | Dark Factory control surface over KyberAgent (MCP/API control, deploy-into-local-harness, integration-test channels, permission escalation; ever-expanding doc) | dark-factory | 07-09 | 07-13 | 2 | **open** — 07-13 extension-builder loop (LOOP-033) is its agentified continuation |
| LOOP-027 | Kyber extensions build-out (pre-baked small-business micro-apps: till/pricing catalog etc.) | kyber-extensions | 07-11 | 07-11 | 1 | **open** — David's declared lane within Kybernesis (memory done, Martin on bus, David on extensions) |
| LOOP-028 | Review vs delivery-review skill distinction (+ Thursday plugins agenda) | skills-tooling | 07-11 | 07-11 | 1 | **open** — trivially answerable; Thursday catch-up pending |
| LOOP-029 | Captain's Log unified ingestion providers (self-sent email, article, YouTube-link → common transcript form) | captains-log | 07-11 | 07-11 | 1 | **open** — scope extension of LOOP-015 |
| LOOP-030 | Captain's Log output destinations (raw transcripts → folder vs second brain; TIL process for Plaud?) | captains-log | 07-12 | 07-12 | 1 | **open** — config decision needed |
| LOOP-031 | Plaud refresh-token brittleness (re-fetch flow, persist against provider, automate via Playwright) | captains-log | 07-12 | 07-13 | 2 | **open** — daily manual pain, escalating |
| LOOP-032 | Affiliate inbox triage (classify scam/real/follow-up, draft responses) | misc | 07-12 | 07-13 | 2 | **parked** — explicitly deferred to a session with Jan + Mary |
| LOOP-033 | Extension-builder two-agent feedback loop (builder agent ↔ platform-extender agent; needs SDK/host/harness/daemon roadmap) | kyber-extensions | 07-13 | 07-13 | 1 | **open — new** |
| LOOP-034 | Dark Factory roadmap walkthrough (one-question-at-a-time Q&A; constellation apps sequenced) | dark-factory | 07-13 | 07-13 | 1 | **open — new, gating** (defines what the factory does next) |
| LOOP-035 | Captain's Log connective tissue: temporal/quest linkage (LOOP-035a), action-tracking on transcripts (035b), UX overhaul incl. tag governance/light mode/vocabulary layer (035c) | captains-log | 07-13 | 07-13 | 3 | **open — new**; 035a is the feature this calibration exercise manually simulates |
| LOOP-036 | Lars demo plan (KyberAgent + Brain + Extension SDK walkthrough, 2–3 min Captain's Log demo) | client-lars | 07-13 | 07-13 | 1 | **open — time-critical** (call imminent) |

---

## Status rollup

| Status | Count | LOOP-IDs |
|--------|-------|----------|
| open | 20 | 004, 009, 013, 014, 015, 016, 018, 019, 020, 021, 025, 026, 027, 028, 029, 030, 031, 033, 034, 035, 036 (21 incl. sub-parts) |
| stale | 9 | 001, 005, 006, 007, 008, 012, 017, 022, 023, 024 (10) |
| likely-resolved | 2 | 010, 011 |
| parked | 3 | 002, 003, 032 |

## Priority read (age × importance)

1. **LOOP-019 Challenge DV proposal** — 6 days old, revenue-bearing, start date 15 July (2 days away), price finally settled. Highest urgency-to-effort ratio in the registry.
2. **LOOP-004/025/034 Dark Factory autonomy → governance → reset chain** — oldest big loop (07-02), escalated into a governance breakdown and now gates all factory throughput; the 07-13 roadmap walkthrough is the unblocking move.
3. **LOOP-018 KyberAgent on Roamy** — 7 days old, restated 3× without execution, and it is the prerequisite for LOOP-016/026/033 (SDK understanding, control surface, two-agent loop) plus the Lars and Challenge DV demos.

Honourable mentions: LOOP-012 (KDD read-side — oldest *systemic* gap, quiet but foundational), LOOP-015 (largest active build — healthy, doesn't need escalation, needs the SDK gaps in LOOP-016 resolved).

## Run-1 delta

Run-1 recorded only `is_open: true/false` per record — 68 disconnected flags. v2 collapses those into 35 identity-stable loops with lifecycle, exposing: 10 stale loops nobody restated, 2 silently-completed loops (010, 011), 4 stuck-recurrence loops (018, 019, 013, 003), and the merge structure (Captain's Log's 8 mentions were previously 8 unrelated booleans).
