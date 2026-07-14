# Open Loops — Unfinished Business Register (2026-06-29 → 2026-07-13)

**Purpose**: Every record flagged `open_loop: true` (58 of 102), grouped by thread, oldest-first within each group — problems raised and seemingly never closed as of 2026-07-13.

**For Agents**:
- "Open" means no later capture in this corpus closes it; some may have been resolved in coding sessions the pendant didn't hear.
- ⚠ marks loops with a deadline, money, or explicit priority attached.

---

## kyber-extensions / kybernesis-extension-sdk (oldest loop in corpus)

| First raised | Loop |
|---|---|
| 06-29 | App/port registry vs locations.json untangling — micro-app registry with location + assigned port per app |
| 06-29 | Install/test AionUI + T3 as third-party extension hosts (decoupling hedge) |
| 06-29 | First-build decision: recipe management vs app management (overtaken by events — Captain's Log jumped the queue, but never explicitly closed) |
| 06-29 | Airtable-style relational-data extension as shared backend for other extensions |
| 07-03 | GitHub org name for extensions (appydave-kyber vs kybernesis vs kyber-extensions) |
| 07-03 | Dynamic external-extension loading likely missing from host — write up problem + proposed solution |
| 07-05 | ⚠ SDK requirements ticket: host chat-conversation access + scheduled-task/cron support — file it and report where |
| 07-07 | Architectural disconnect: confirm extensions run own web server + client, surfaced via iframe, NOT routed through host |
| 07-11 | Package Joy's bespoke micro-apps (till/POS, pricing catalog) as Kybernesis extensions |
| 07-13 | Extension SDK roadmap needed so extension-blocking gaps have somewhere to land as tickets |

## recipe-thumbnail-arc (dormant since 06-30)

| First raised | Loop |
|---|---|
| 06-30 | Scope the KyberAgent thumbnail-generator micro-app; per-brand field/rules configs |
| 06-30 | Locate the old image-prompt pacing TUI (appydave-tools / Ruby) |
| 06-30 | Shortlisting mechanism: 100+ thumbnail variants → 10–20 candidates |

## dark-factory-engine

| First raised | Loop |
|---|---|
| 07-02 | Architecture docs/visuals (events, hooks, pipelines) — mermaid → Mochaccino-generated diagrams |
| 07-02 | Separate/label the three codebases: canonical dark-factory vs PoC vs third-party reference |
| 07-02 | Lisa/KDD upgrade: extract *ideas* with provenance-chained speculative PRs |
| 07-02 | Morning-briefing surface for ~10–15 overnight projects (WatchTower) |
| 07-03 | Ranked build-options list from the agent for go/no-go; WatchTower + Switchboard comms-flow doc |
| 07-03 | Was a real server-backed Claude Agent SDK extension ever planned, or were the HTML pages only PoCs? |
| 07-03 | Builds must test the dark-factory harness itself (agent spin-up/down + bus), not inline Claude Code agents |
| 07-09 | ⚠ Governance: codify blocking of factory self-modification tickets |
| 07-09 | Revert unapproved "war room" namespace to lanes/stations vocabulary |
| 07-09 | Chaperone/observer for the main factory conversation (+ name/skill/agent for that role) |
| 07-09 | Consolidate 3 fragmented task-launch paths onto one sanctioned route (revive switchboard/watchtower?) |
| 07-09 | Repeatable bootstrap for a fresh context-rich main conversation (current one is "unresettable context spaghetti") |
| 07-09 | Deep-study KyberAgent SDK/control surfaces; ever-expanding "what Dark Factory needs to control Kybernesis" doc |
| 07-10 | ⚠ Cross-repo coding decision: reference folders vs MCP knowledge server vs centralize in Dark Factory |
| 07-13 | Roadmap reset: guided one-question-at-a-time Q&A; constellation apps as sequenced builds |

## kdd-lisa / dark-factory-kdd / kdd-librarians

| First raised | Loop |
|---|---|
| 07-03 | KDD-inspector extension (project decisions/lessons/patterns at a glance) |
| 07-03 | Locate where Lisa's machine-readable JSON processing files are landing (unknown) |
| 07-04 | Document what KDD bridge IS, why it exists, register it in the app registry |
| 07-04 | Deprecate broken Gemini integration |
| 07-04 | ⚠ **Structural**: wire KDD *reading* into SDLC checkpoints (PR validation, knowledge updates) — "the factory writes knowledge but nothing reads it" |
| 07-04 | Ticket triage: validate/close 176; hand 192 to new session; 191 waits for full-focus session |
| 07-04 | Lisa menuing/deterministic guardrails; investigate learning-became-a-branch failure |
| 07-07 | Strip per-repo customization from Lisa; KDD-folder-only scope |
| 07-07 | Teach tooling: refresh-context is for unknown projects only (recurring gripe) |

## captains-log-product (highest loop density: 11 open records)

| First raised | Loop |
|---|---|
| 07-04 *(omi-ingestion)* | OMI list: surface tags/synopsis, detail toggle, sequential ID scheme (partially absorbed into Captain's Log) |
| 07-05 | Local Whisper/Groq pipeline to kill both $20/mo transcription subscriptions |
| 07-05 | Compare OMI vs Plaud transcript data structures for provider-specific quirks |
| 07-06 | Transcription-quality bake-off verdict (dual-recorded conversations) — never scored |
| 07-06 | Cross-machine capture availability (injected conversations land on one machine only) |
| 07-12 | Data-destination config: where does ingested data land (raw / brain / TIL)? |
| 07-12 | ⚠ Plaud refresh-token brittleness → re-fetch + storage mechanism |
| 07-13 | Verify ingestion job durability; move to launchd (30-min, 7am–10pm) + manual trigger |
| 07-13 | ⚠ **Meta**: temporal/thematic linkage between captures — quest/side-quest threading (this calibration exercise is the prototype answer) |
| 07-13 | Actions/notes/done-marking attached to transcripts — mechanism undecided |
| 07-13 | ⚠ Full UX punch-list (A330–A339): show-markdown, light mode, DESIGN.md, vocabulary correction, semantic source colors, noise-hide default, tag governance/central store, chat-with-document, **automate daily Plaud token refresh (highest priority)** |

## kyberagent-learning / kybernesis-doc-watcher

| First raised | Loop |
|---|---|
| 07-06 | Doc-watcher agent on Roamy (planned for that weekend — didn't happen; re-planned 07-13 as the pilot, still not started) |
| 07-06 | ⚠ How to talk to / control a running KyberAgent from Claude Code (capability unknown — asked twice) |
| 07-13 | First agent on Roamy ($100 credits): Kybernesis-comprehension brain, KDD/commit reports on Ian & Martin's work |

## clients

| First raised | Loop |
|---|---|
| 07-07 | ⚠ Linda/Challenge DV: send engagement options — settled 07-13 at $2,750 inc GST from **July 15** (2 days away); confirm her name (Lisa/Lindy); answer Canva question; reply to unread email |
| 07-07 | Angela/Achieve: repo access, context load, 100 NDIS scripts, SupportSignal redeploy on Vercel+Supabase, $1000 invoice + Claude Max setup |
| 07-09 | Achieve MVP: SupportSignal/DSP AI analysis ("moments that matter"), JSON schemas → read-only micro-apps, synthetic-data agents, 30,000-ft gap map |
| 07-13 | Lars: prepare KyberAgent + Extension SDK + Captain's Log demo |

## meetups / peers / misc

| First raised | Loop |
|---|---|
| 07-03 | "Agent Burst" business name (coworking session) |
| 07-04 | July meetup dates → WhatsApp group; Angela docs by email; Angela+Stravan onboarding session |
| 07-04 | Skill registry design (staleness, learnings, taxonomy search, viewer) — dormant |
| 07-04 | Re-evaluate five "too thin" extensions for human+agent consumers — dormant |
| 07-04 | Gling/video: open-source cutter research → pivoted 07-11 to MCP injection into Gling's Electron app; gling brain review still pending |
| 07-04 | ⚠ Gling.ai subscription decision — lapsed into renewal by inaction (charge already hit 07-11) |
| 07-04 | OMI pendant wind-noise reliability doubt (is the device usable on the motorbike?) |
| 07-07 | Smart contracts + dual-loop explanation; contract/rubric verification step per unit of work |
| 07-07 | NordPass master-password verification without lockout |
| 07-07 | Frame extension: option-2 end-to-end tests; ~10 failing tests (integration vs unit?); panel-vs-mount terminology; refresh-context/screenshot pruning |
| 07-09 | Session-content-mining router skill (sessions → tweets/YouTube/lead magnets/Skool) |
| 07-11 | Plugin-on-plugin dependency investigation for modularising the AppyDave plugin suite |
| 07-11 | B-roll auto-tagging (~1000 videos) via Qwen + Whisper |
| 07-11 | Review-skill variant confusion (delivery vs dimensional); plugins on Thursday's agenda |
| 07-12 | Affiliate email triage — deferred 07-13 to do with Jan and Mary (still open, now scheduled-ish) |

---

## Shape of the backlog

- **58 open-loop records; ~70 distinct unclosed items** after merging duplicates.
- **Oldest loop**: the app/port registry untangling (06-29) — 15 days old, foundational, untouched.
- **Most at-risk**: Challenge DV proposal (July 15 start date, 2 days out) and the Plaud token automation (blocks Captain's Log's daily operation, explicitly "highest priority").
- **Most structural**: "factory writes knowledge but nothing reads it" (07-04) — every KDD/Lisa loop is a symptom of this one.
- **Most self-referential**: temporal/thematic capture linkage (07-06, 07-13) — the loop this document exists to close.
