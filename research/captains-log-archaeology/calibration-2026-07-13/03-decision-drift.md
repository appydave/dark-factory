# Decision Drift — Beliefs That Changed Over the Fortnight (2026-06-29 → 2026-07-13)

**Purpose**: Trace where a plan or belief moved during the fortnight, and flag superseded decisions that may still look current in tickets, brains, or docs written before the drift.

**For Agents**:
- Before acting on any capture in this corpus, check this file — the earlier record may state a plan David has since reversed.
- "Still looks current in" = places likely to carry the stale version.

---

## Major drifts

### 1. Gling: replace → programmatically hijack
- **07-04 1240**: find an open-source agentic video-cutter to REPLACE Gling before the subscription renews "in days"; research + vetting actions issued.
- **07-11 1603**: pivot — don't recreate Gling; drive it programmatically from FliHub.
- **07-11 1627**: final form — Gling renewed anyway; inject an MCP server/API into its unobfuscated Electron codebase at startup and remote-control its internals.
- **Stale-risk**: the 07-04 "research open-source replacements" action, and anything in the `video-as-code` / `gling` brains written around 07-04. The subscription-cancellation decision was never made — it lapsed into renewal.

### 2. OMI extension: build it → it was built wrong → superseded by Captain's Log
- **07-03 0921**: OMI-fetch extension proposed as the simple proving-ground extension.
- **07-05 1831 / 2003**: verdict — the OMI extension was a "half-assed fork" that reinvented ingestion and bypassed the underlying skills; good ideas to be mined, artifact to be discarded.
- **07-06 → 07-13**: Captain's Log is the declared successor (skills-based, provider-agnostic).
- **Stale-risk**: any ticket/doc referring to "the OMI extension" as a live component; `omi-fetch` naming itself was declared conceptually obsolete on 07-05 ("rename/unify into provider-agnostic capture"). The `appydave:omi-fetch` skill and `apps/omi` docs still carry the old framing.

### 3. Thumbnail automation: build a generator → David keeps thumbnails manual
- **06-30 0801/0814**: build a thumbnail-generator micro-app + prompt-pacing TUI, multi-brand rollout.
- **07-03 0921**: explicit carve-out — "Do NOT automate thumbnail generation for David — he keeps personal control of that."
- Reconciliation: the *tooling* (shortlisting, pacing) may still be wanted as assistive, but full automation is off the table, and the whole arc has been dormant since 06-30 (externally marked PAUSED 07-10).
- **Stale-risk**: 06-30 build directives read as active orders; they are paused and scope-constrained.

### 4. Challenge DV retainer price: $5k → $3,300 → $2,750
- **07-07**: ~$5k/mo floated in the Linda call.
- **07-13 0633**: shaped to ~$3,300/mo inc GST.
- **07-13 0851**: settled at **$2,750 inc GST ($2,500 + GST)**, mid-month to mid-month from July 15.
- **Stale-risk**: any proposal draft or note using the earlier figures. Also: the contact's name (Lisa vs Lindy) is STILL unverified — a factual gap that must be closed before the proposal email.

### 5. Extension execution model: iframe-through-host → standalone web server surfaced in iframe
- **07-03 1401**: "iframe technique" decided — extensions external, dynamically loaded.
- **07-07 1953**: refinement/pushback — an extension is a standalone web server + daemon; the iframe client must NOT talk through the host to a backend.
- **07-05 2003 → 07-12/13**: but cron/scheduling and LLM/chat access SHOULD be host-provided (daemon executes extension-configured cron; LLM via agent daemon).
- Net current position: **UI isolation via iframe + own server; platform services (cron, LLM) via host daemon** — neither of the two earlier captures alone states this correctly.
- **Stale-risk**: reading only the 07-03 decision gives the wrong service topology.

### 6. Transcription economics: pay per-provider → self-host
- **Before 07-05**: implicit status quo — OMI and Plaud each with ~$20/mo transcription subscriptions.
- **07-05 0954**: decision direction — pull raw audio locally, transcribe with Whisper (or Groq per Ian), cancel both subscriptions.
- **Stale-risk**: budget/tooling notes assuming provider transcription; also the plaud-fetch skill already does local mlx-whisper, so the OMI side is the one still drifting.

### 7. Dark Factory vocabulary: lanes/stations → "war room" → revert
- **Pre-07-09**: established factory vocabulary (lanes, stations, workflow).
- **07-09 0642**: an unapproved "war room" namespace from a throwaway brainstorm displaced it; David's ruling — review and likely revert.
- **Stale-risk**: factory code/docs generated during the war-room window carry a namespace David considers unauthorized. Reversion not yet confirmed done.

### 8. Factory self-modification: allowed by default → gut says block
- **Pre-07-09**: no policy; the factory modified its own orchestrator code via a normal ticket.
- **07-09 0642**: David's position — self-modification tickets should be flagged/blocked, "open to debate".
- **Status**: policy proposed, not codified. Until written, the factory's default behaviour still contradicts David's stated intent.

## Minor drifts / soft reversals

- **Fable sprint framing** (07-02 "7 days" → 07-03 "~6 days" → post-window): the sprint's premise expired; captures issuing Fable-sprint directives are time-boxed orders that no longer apply as written.
- **Haiku → Sonnet 4.5** for factory workloads floated 07-04 — a consideration, never confirmed; don't treat as decided.
- **Affiliate triage**: 07-12 "batch-triage now, optionally draft responses" → 07-13 "defer, do together with Jan and Mary" — the solo-triage order is superseded.
- **Roadmap as document → roadmap as guided Q&A** (07-13): any agent presenting the Dark Factory roadmap as a wall of text is now violating an explicit preference.
- **Recipe-first vs app-management-first** (06-29): the "decide first build" question was never answered; events answered it implicitly — Captain's Log jumped the queue. The 06-29 framing of "recipe management vs app management" no longer reflects what's actually being built first.
