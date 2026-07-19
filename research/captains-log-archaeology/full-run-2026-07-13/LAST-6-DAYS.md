# Last 6 days (2026-07-08→2026-07-13) — 31 real captures (1250 total, noise excluded)

## By thread

### captains-log (9)
- 2026-07-09 — The combined Plaud+OMI viewer is officially named Captain's Log and will be hosted as a KyberAgent extension so it can reach an LLM through the daemon for tagging/ontology without building its own API layer, with a configurable pulse that polls Plaud and OMI within a daily window roughly every 10 minutes.
- 2026-07-11 — Captain's Log should be a unified intelligence hub ingesting OMI, Plaud, and self-sent emails (YouTube links auto-extract transcripts, article links get scraped), normalizing everything to 'transcripts' that get analyzed, summarized, and ontology-tagged.
- 2026-07-12 — Plaud auth is brittle — using Plaud from another client (Android/web) rotates the refresh token — so Captain's Log needs an easy re-fetch flow that stores the renewed token against the Plaud ingestion provider.
- 2026-07-12 — Open question: where should raw Plaud and OMI transcripts land (current folder vs the second brain vs a TIL-style process, which exists for OMI but maybe not Plaud) — and the Captain's Log app needs its own ingestion-destination configuration.
- 2026-07-12 — Architecture pass for the Captain's Log Kybernesis extension (Plaud+OMI): decide the server foundation (AppyStack vs what Kybernesis already provides), normalize David's vernacular in transcripts without changing context (AppyDave vs Happy Dave), list-view UX with hover metadata/markdown/clipboard/search, per-provider cron configured in the extension but owned by the host daemon, and spin tickets for missing SDK/host capabilities so extension-built functionality is offloaded to the platform later.
- 2026-07-13 — Extended dogfooding review of Captain's Log flags read-only markdown (needs a show button), dark-mode-only theme, transcript vocabulary miscorrections (Carbonetics vs Kybernesis), ungoverned/missing tags needing a centralized future-proof tag store, empty noise captures showing by default, and the daily manual Plaud token repair as the priority fixes.
- 2026-07-13 — Captures in Captain's Log need attachable actions, notes, and done-marking — possibly via a multi-conversational observation audit log collected while using the app and consolidated in one pass.
- 2026-07-13 — Ingestion items have no connective tissue — no linear temporal chain linking the many conversations on one topic, and no quest/side-quest thematic threads (Dark Factory vocabulary) for when one conversation forks into several idea chains.
- 2026-07-13 — Captain's Log ingestion must be durable beyond the web server's lifetime — launchd-style cron every 30 minutes from 07:00 to 22:00 plus an in-app manual trigger — with slice-and-dice filter toggles (tags, timeframe, keyword search, noise hidden by default) and the build verified against the soon-publishable Kyber Extension SDK.

### dark-factory (5)
- 2026-07-09 — Catch-up with Tony O'Connell: Joy Juice and Beauty & Joy self-provisioned as clients on Tony's one.ie platform (schemas now visualizable); David explains Dark Factory as a self-improving SDLC that builds observability/telemetry micro-apps (~50 tasks planned with Fable, executed on Opus) and shares the Taylor pattern (docs → UAT steps → Playwright automated acceptance runs) plus a Loom+FFmpeg screenshot-audit alternative; Tony's blockchain smart contracts flagged as a way to strengthen KDD rubrics/evals.
- 2026-07-09 — Dark Factory must gain deep understanding of KyberAgent and the Kyber Extension SDK so it can control the agent via MCP/API for direct deployment of built extensions into the local harness and integration testing over its communication channels, with escalated permissions and a dedicated ever-expanding document to track what control surfaces Dark Factory needs.
- 2026-07-09 — Governance critique of yesterday's Dark Factory session: changes to factory-running code should be blocked from running through the factory itself, the unapproved 'war room' namespace displaced the existing lanes/stations naming, the main conversation window lacks a chaperone/observer, task-launch has fragmented into three inconsistent paths (ad-hoc claude, orchestrator CLI, and the bypassed Switchboard/WatchTower web harness), and there is no clean way to bootstrap a new context-rich main conversation.
- 2026-07-10 — Open Dark Factory architecture decision: where does factory code run when documentation is split across two repos — Dark Factory holds the coding-agent/SDLC/KDD intelligence while KyberAgent holds requirements and code, but Claude Code runs in one folder; options are (a) run in KyberAgent with a reference folder back to Dark Factory, (b) an MCP server exposing Dark Factory knowledge, or (c) centralize all coding inside Dark Factory — needs a deliberate ultrathink pass.
- 2026-07-13 — Reset Dark Factory planning: replace the wall-of-text roadmap with a conversational one-question-at-a-time Q&A walkthrough, and elevate the complex constellation applications onto the roadmap as sequenced one-at-a-time builds instead of piecemeal tasks.

### ai-meetups (3)
- 2026-07-10 — Meetup lecture by Ishan (ex-HockeyStack GTM engineer) on agentic go-to-market: DeepLine as pay-as-you-go data/outreach infrastructure replacing Clay and UI tools, signal-based relevance targeting, lookalike campaigns, effort-as-proxy emails, reply-rate (not open-rate) as the metric, and Claude routines/connectors as the automation substrate.
- 2026-07-11 — Chiang Mai meetup talk on an AI-first multi-agent company stack — agent memory platform, desktop multi-agent orchestration, and a secure Agent Relationship Protocol (agent-to-agent handshake with scoped permissions) — demoing a research→design→deploy campaign workflow in minutes vs weeks, plus plugin dependency trees, evals/watch-don't-steer oversight, incremental rollout, and Claude certified-partner requirements.
- 2026-07-11 — Chiang Mai meetup session (Ian, Claude ambassador for Thailand/Kybernesis, plus Section 9 host) covering enterprise Claude ROI cases and a deep demo of Claude Tag as a multiplayer Slack team-member (own service account, isolated per-channel memory, sandboxing), Cowork desktop for long-running analysis (VC due-diligence in minutes vs six weeks), connectors, boring-secure-tools stack criteria, auto mode (~30% extra usage), and dispatch for phone-to-desktop local sessions.

### ai-research (2)
- 2026-07-10 — Peer report that platform version 5.6 regressed vs 5.5 — hour-long thread queues, slower and more expensive, poorly tested codex integration, and skills effectively unsupported (works okay only after removing all skills); vendor seen as pivoting to everyday users over developers, worth watching over the next few weeks.
- 2026-07-10 — Realization that a connector-first architecture beats in-app memory: if chat has connectors to your own specialized storage (a brain here, two brains there), you may not need the repos or the vendor's hidden memory at all — avoiding vendor lock-in and keeping data sovereignty.

### skills-tooling (2)
- 2026-07-10 — David will build a self-learning, context-aware formatting skill for ad-hoc executive-style reporting — like a CEO saying 'I need this as a table' without design details, adaptive turn-by-turn to conversation context and even time-of-day fatigue — extending his pattern of small utility skills (RN rename command, BTW prompt builder).
- 2026-07-11 — Amid heavy TV/background noise, a real fragment: David asking how delivery-review differs from other review skills, how to evaluate a skill-creator-built review skill run by a background agent, and flagging a plugins catch-up on Thursday.

### gling-automation (2)
- 2026-07-11 — Gling's Electron app is unobfuscated JavaScript, so instead of rebuilding it, inject an MCP server/API into its codebase at startup to remotely control the editor from Claude Code — and eventually have FliHub open Gling with recorded videos and keywords preloaded (subscription just renewed for a year, second-brain notes on Gling already exist).
- 2026-07-11 — With the Gling subscription renewing, David wants programmatic control over Gling (auto-open, add videos, remote device control, API into its codebase) and decides not to rebuild his own editor but to inject the needed features via a TypeScript/JavaScript library directly into the application, after reviewing his existing Gling second-brain notes.

### kyber-extensions (2)
- 2026-07-11 — David explains (at meetup) his Kybernesis extensions work: extensions are pre-baked micro-apps (agent + skills) living inside the KyberAgent desktop; Joy's juice/nail/eyebrow-tattoo configurable POS-and-pricing catalog is the archetype, feeding websites, AI-generated promo videos (Whisper transcript + Qwen visual tagging of B-roll, auto-assembly, Thai/English), and agents — while Martin builds the agent communication bus and David has finished the memory layer.
- 2026-07-13 — Two-agent feedback loop for the Kyber Extension SDK: an extension-builder agent (fed by the KyberAgent brain agent) develops extensions through the standard SDLC, and when it hits missing host/harness/daemon capabilities it prioritizes and files roadmap tickets for a second agent that extends the Kybernesis platform itself.

### client-achieve (1)
- 2026-07-09 — Working session with Angela on the Achieve MVP: $1.2–4M annual funding leakage traced to no single source of truth (service agreements as PDFs off spreadsheets), ~1,100 weekly rejected NDIS claims worked one-by-one with zero learning loops, siloed CI register and compliance-over-quality culture; plan is FDE-style incremental delivery — map the 30,000-ft process view into dependency-ordered project areas, derive JSON workflow/data schemas from SupportSignal (legacy/current/v2) and the DSP app under Supporting Potential, and spin up read-only micro-app visualizations (Mochaccino) fed by synthetic-data agents.

### content-production (1)
- 2026-07-09 — Every coding session should be post-processed for marketing: a router-style analysis pass over session transcripts extracting tweet material, YouTube video content, and lead magnets/knowledge packets (markdown/PDF), staged for refinement then routed to the right output channel — extending the in-progress recipe-extraction and handover skills.

### brand-strategy (1)
- 2026-07-12 — Batch-triage the weeks-long backlog of affiliate reach-outs (mostly AI-TLDR) in the david@ideasmen inbox — classify scammy vs real, check whether David had initiated contact and forgotten, and pre-draft responses; per a later note, to be done together with Jan and Mary.

### kyberagent-pilot (1)
- 2026-07-13 — Stand up a dedicated KyberAgent brain agent (covering the extension SDK, daemon, and harness) on Roamy using its $100 credits — it should read all KDD docs and commits and write David a recurring report on what Ian and Martin are adding across the whole Kybernesis system, mirroring Ian's multi-agent research→design→build→deploy workflow.

### client-challenge-dv (1)
- 2026-07-13 — Offer Challenge DV an FDE-style retainer — A$3,300/month incl GST for a weekly 90-minute Claude-centric training session plus roughly two custom micro-tools a month for marketing automation — opened with a KyberAgent demo (multi-agent orchestration, second brain, extensions, Captain's Log); first reply to her outstanding email (Canva question, contact name uncertain: Lisa or Lindy).

### client-lars (1)
- 2026-07-13 — Plan for the Lars call: cover KyberAgent, the KyberAgent brain, and the Kyber Extension SDK, with a quick 2-3 minute Captain's Log demo — Lars's key want is on-demand micro-application tools that plug into KyberAgent for himself.

