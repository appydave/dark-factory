# Thread: captains-log

**Purpose**: 6-month timeline of the "captains-log" capture thread — from OMI unboxing to Captain's Log as a named Kybernesis extension under active dogfooding.

**For Agents**:
- Use this to understand how Captain's Log emerged from the OMI ingestion work — it is not a greenfield idea, it is the convergence point of six months of voice-capture plumbing.
- Superseded decisions are flagged inline; do not resurrect them.
- Records: 34, spanning 2026-01-09 → 2026-07-13.

---

## Arc at a glance

```
Jan 09        Mar 01–30            Apr 01–12         [DORMANT]      Jun 13–14      Jul 04–13
OMI unboxed → OMI ingestion       → scheduling +    ~2 months    → OMI brain    → Plaud arrives →
(origin)      design burst          Captain's Log     quiet         release +      unification →
              (skill? brain?        precursor seed                  transcript     NAMED Captain's Log →
              pipeline, routing)    (multi-stream                   routing        Kyber extension →
                                    inbox)                                         dogfooding fixes
```

---

## Phase 1 — Origin: the wearable arrives (2026-01-09)

- **2026-01-09** (personal): David unboxes the OMI wearable — magnetic-latch box, charging base, neckband — and onboards as a Chiang Mai-based YouTube creator. This single event seeds everything below: an always-on voice stream now exists and needs somewhere to go.

Then ~7 weeks of silence in this thread while the device presumably just records.

## Phase 2 — The March design burst: OMI ingestion becomes a system (2026-03-01 → 2026-03-30)

The thread wakes up hard in early March — 12 records in 30 days, mostly morning-monologue architecture.

- **2026-03-01** (idea): a lightweight to-do/journal micro-app for the todo brain — minimal fields, time-based daily grouping, roll-forward/drop mechanics — modelled as an **ongoing journal, not a historical log**. In hindsight this is the earliest "log of captures" framing.
- **2026-03-03 / 03-04** (direction, twice — near-duplicate morning monologues): the daily operating model is defined — morning briefing as heartbeat ritual, **30-minute OMI endpoint polling**, "on-the-sides" delegated-work protocol (requirements → plan → build → tests → Playwright/UAT). Three recording blockers named: **OMI import, Stream Deck, Ecamm scenes**. (Side decisions in the same captures — WUI→Agent Workflow Builder rename, Joy's shop cashflow — belong to other threads.)
- **2026-03-04** (questions ×2 + direction): should OMI ingestion be **its own brain or just a skill**? Should transcripts be processed as **a recipe in the API generation system**? A background agent is dispatched to verify the OMI login, research Krisp SDK + Ecamm HTTP API, and produce a flow graph/tests/UAT fact sheet on the ingestion/backup/routing pipeline. — *All three framings (brain, skill, API recipe) are eventually superseded by the extension model in July.*
- **2026-03-05** (direction, captured twice — duplicate): the OMI ingestion layer is architected — dedicated skill, context-quality/**prompt-injection checks**, observability with approval decision points, routing into the todo system, plus a **unified audit log across all apps** ("David is always the app-pipeline blocker").
- **2026-03-08** (question): David probes whether an AI session can actually reach OMI transcripts, from two angles — early dogfooding/verification instinct.
- **2026-03-09** (direction): first real **morning OMI inbox review** — read and route the morning's captures; flags wrong-looking timezones from Bangkok; notes no master list of upcoming videos/paid apps exists.
- **2026-03-11** (idea): the **/loop concept** — short in-session loops vs **standing ingestion loops** that continuously process incoming OMI/email/chat, route, file, summarize. The "always-running ingestion" idea that Captain's Log's pulse later fulfils.
- **2026-03-20** (decision): OMI conversations captured on one machine are **missing on the other** (same shared-knowledge gap as apps.json/locations.json — parked). Display standard set: **Bangkok time first, then UTC**.
- **2026-03-30** (decision): the OMI extraction **backfill** runs as a **single Python script writing markdown in place** (no sidecar), possibly wrapped as an appydave-plugin skill orchestrating omi-fetch + extraction; brain vocabulary from the provenance chain; **routing and automation explicitly deferred**. — *Superseded: the bespoke-script posture gives way to scheduled/daemon processing (Apr 1, then Jul 9/13).*

## Phase 3 — April: scheduling + the Captain's Log precursor (2026-04-01 → 2026-04-12)

- **2026-04-01** (idea): OMI-fetch output should be processed daily using **off-the-shelf schedulers** (Claude desktop scheduled tasks, `claude -p`, Agent SDK) rather than bespoke tooling; OMI + OMI scheduling added to the roadmap deck. — *Superseded in July by hosting the pulse inside a KyberAgent extension + launchd-style cron.*
- **2026-04-12** (idea) — **THE PRECURSOR RECORD**: a **multi-stream conversational inbox** — chain-of-consciousness streams (OMI first, later Krisp and YouTube, maybe email) flowing into a central inbox that auto-tags, labels, routes and summarizes via a tagging ontology. Noted: the existing **Gemini tagging software is flaky**. This is explicitly the Captain's Log seed, three months before the name exists.

## Phase 4 — Dormancy (2026-04-12 → 2026-06-13)

**~2 months with zero records.** The concept sits parked while (per surrounding context) the backfill/extraction tooling matured elsewhere (the omi-fetch pipeline reached 1041/1041 transcripts in early June). The thread itself is dormant.

## Phase 5 — June re-emergence: OMI brain maturity (2026-06-13 → 2026-06-14)

- **2026-06-13** (decision): late-night triage — ideas B and C get **documented, not built**; David asks where the **OMI brain release** stands (probe fixes vs more tests vs ship).
- **2026-06-14** (direction): the long ~7am morning transcript must be deeply reviewed and **split into three documentation streams without information loss** — the routing problem, still being done by hand. The pain that justifies Phase 6.

## Phase 6 — July convergence: Plaud arrives, Captain's Log is born (2026-07-04 → 2026-07-13)

Ten days, 15 records — the densest stretch of the whole thread. A second wearable (Plaud) forces generalization, and the precursor idea from April gets a name, a host, and a running build.

- **2026-07-04** (feedback): OMI list ingestion is **too thin** — wants ontology/tags/synopsis per item plus a **sequential A00-style primary key** so agents can be told "go get item A001".
- **2026-07-05** (decision + direction): the pivotal architecture call — **OMI and Plaud stay separate ingestion skills, but downstream processing is shared** (local Whisper/Groq transcription, tagging/ontology, source pinning) under **a single unified controller** — "the pre-naming seed of Captain's Log". Corollaries: omi-fetch's name/skill split is declared **wrong** (both devices are just voice-capture providers); pull raw audio locally instead of **paying $20/month per provider** for transcription; wants a feed structure comparison and 3–4 name suggestions before building. — *Supersedes the OMI-centric framing of all of Phase 2–3.*
- **2026-07-06** (direction ×2, duplicate captures): **the Captain's Log extension replaces the OMI-only extension** — it must show incoming conversations, **many-to-many project mapping**, and **machine-routing telemetry** (Roamy vs M4 Mini), since David has no field telemetry for that routing. Ticket to Dark Factory. — *Explicit supersession: OMI-only extension is dead.*
- **2026-07-06** (idea ×2, duplicate captures): **OMI vs Plaud transcription bake-off** — run the same micro-conversations through both wearables (David wears both) and compare quality.
- **2026-07-09** (decision): **officially named Captain's Log**, hosted as a **KyberAgent (Kybernesis) extension** so it reaches an LLM through the daemon for tagging/ontology without building its own API layer; **configurable pulse** polling Plaud and OMI within a daily window ~every 10 minutes. — *Resolves the March "brain vs skill vs API recipe" question and the flaky-Gemini-tagging problem (Apr 12) in one move.*
- **2026-07-11** (direction): scope widens — Captain's Log is a **unified intelligence hub**: OMI + Plaud + **self-sent emails** (YouTube links auto-extract transcripts, article links scraped), everything normalized to "transcripts" that get analyzed, summarized, ontology-tagged. The April multi-stream-inbox vision, fully restored.
- **2026-07-12** (direction + question + direction): build reality sets in.
  - **Plaud auth is brittle** — using Plaud from another client rotates the refresh token; needs an easy re-fetch flow storing the renewed token against the provider.
  - Open question: **where do raw transcripts land** (current folder vs second brain vs TIL-style process — exists for OMI, maybe not Plaud); the app needs its own ingestion-destination configuration.
  - Full **architecture pass** for the Kybernesis extension: server foundation (**AppyStack vs what Kybernesis provides** — undecided), vernacular normalization without changing context (AppyDave vs "Happy Dave"), list-view UX (hover metadata, markdown, clipboard, search), **per-provider cron configured in the extension but owned by the host daemon**, and tickets for missing SDK/host capabilities so extension-built functionality offloads to the platform later.
- **2026-07-13** (feedback + idea ×2 + direction): **extended dogfooding review** — the app exists and is being used:
  - Priority fixes: read-only markdown (needs a show button), dark-mode-only theme, vocabulary miscorrections ("Carbonetics" vs Kybernesis), **ungoverned/missing tags → needs a centralized future-proof tag store**, empty noise captures shown by default, and the **daily manual Plaud token repair** as the #1 pain.
  - Ideas: captures need **attachable actions, notes, done-marking** (possibly via a multi-conversational observation audit log); and — the meta-idea this very document embodies — ingestion items have **no connective tissue**: no temporal chain linking conversations on one topic, no **quest/side-quest thematic threads** (Dark Factory vocabulary).
  - Direction: ingestion must be **durable beyond the web server's lifetime** — launchd-style cron every 30 min, 07:00–22:00, plus in-app manual trigger; slice-and-dice filters (tags, timeframe, keyword, noise hidden by default); build verified against the soon-publishable **Kyber Extension SDK**.

---

## Splits and merges

- **Merged in**: the OMI ingestion thread (Phase 2–3), the multi-stream inbox idea (Apr 12), and the Plaud pipeline all **converge** into Captain's Log on 2026-07-05/09. The March /loop standing-ingestion idea is fulfilled by the pulse/cron design.
- **Split out** (mentioned here but living elsewhere): the todo/journal micro-app (Mar 1), WUI→AWB rename, Joy's shop cashflow, cross-machine shared-knowledge gap (Mar 20, parked), and machine-routing telemetry (feeds the AppyRadar/fleet domain even though Captain's Log surfaces it).

## Superseded decisions (do not resurrect)

| Superseded | By | When |
|---|---|---|
| OMI ingestion as its own brain / simple skill / API-recipe | Captain's Log as Kybernesis/KyberAgent extension | Jul 05–09 |
| OMI-only extension | Captain's Log extension (project mapping + machine routing) | Jul 06 |
| omi-fetch name + per-device skill split | OMI/Plaud as interchangeable "voice-capture providers", shared downstream | Jul 05 |
| Per-provider paid transcription (~$20/mo each) | Local Whisper (mlx-whisper) or Groq | Jul 05 |
| Single Python backfill script, routing/automation deferred | Daemon-hosted pulse + launchd-style cron 07:00–22:00 | Mar 30 → Jul 09/13 |
| Off-the-shelf Mac schedulers (Claude desktop tasks, claude -p) | Per-provider cron configured in extension, owned by host daemon | Apr 01 → Jul 12 |
| Flaky Gemini tagging tool | LLM tagging/ontology via KyberAgent daemon | Apr 12 → Jul 09 |

## Current status (as of 2026-07-13)

Captain's Log is a **named, running Kybernesis extension in active dogfooding** — ingesting OMI + Plaud, with email/YouTube/article ingestion directed but not confirmed built. Hot items: daily manual Plaud token repair (top pain), centralized tag store, read-only markdown/theme/noise-filter UX fixes, durable launchd-style ingestion, actions/notes/done on captures, and temporal + quest/side-quest linking of captures. Open decisions: server foundation (AppyStack vs Kybernesis-provided) and where raw transcripts land per provider. The thread is at peak activity and clearly the successor umbrella for all voice-capture processing.
