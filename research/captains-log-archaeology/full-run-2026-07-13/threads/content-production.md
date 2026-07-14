# Thread: content-production

**Records**: 108 | **Span**: 2026-01-31 → 2026-07-09 | **Kinds**: research, direction, idea, feedback, decision, meeting, question

**Purpose**: 6-month archaeology of David's content-production thread — the arc from "fix the streaming rig" through "build the tooling" to "let agents make the videos".

**For Agents**:
- Use this to understand why current video work is agent-pipeline-shaped, not livestream-shaped
- Check "Superseded decisions" before reviving any old plan from this thread
- The YLO/FliLaunch and DeckHand/Ecamm sub-threads split off here; trace their origins in this file

---

## The one-paragraph arc

This thread started (Jan 31) as a **distribution ambition** — daily livestreams on a renamed "Coding Lab" channel — but the very same day collided with **infrastructure reality** (Ecamm/Twitter auth failures, mic hijacking). February–March became a deep tooling detour: reverse-engineering Ecamm Live, building DeckHand, wiring FliHub→AWB→YouTube-Launch-Optimizer, and producing "how I built the tooling" videos about the tooling itself. The thread peaked mid-March with the Digital Stage Summit, dictated a full YLO app spec in April, then went **dormant for ~7 weeks**. It re-emerged in June transformed: Media Studio, Remotion-vs-Hyperframes, and a voice-script-writer architecture — i.e. the goal shifted from *David streaming/recording content* to *agents generating content*, culminating (Jul 9) in the idea that every coding session should be automatically mined for marketing output.

---

## Phase 1 — Ignition: distribution ambition meets rig friction (2026-01-31)

Six captures on a single day set the whole thread in motion:

- **The big commitment**: cafe session where David commits to a **daily-livestream strategy** — rename the 2.5k-sub appydave-research channel to "the Coding Lab", stream every work session to YouTube/Twitter/Facebook/LinkedIn (paid X Premium), buy an M4 workstation, idle M2 as ClaudeBot machine, pay Guy monthly to cut streams with Jan polishing, and adopt NotebookLM-via-MCP "token offloading".
- **Coaching output**: David coaches Guy on fixing his 20 confidence videos (hook + scenario before body; ship, don't perfect).
- **Immediate friction**: Ecamm Live's Twitter/X destination fails with a silent spinner despite the new X Premium account (support email dictated); a live test reaches YouTube but Twitter status unknown; Ecamm hijacks the single HyperX QuadCast mic and kills his voice agents mid-demo.

The pattern of the next five months is visible on day one: ambition → tooling blocks → tooling becomes the work.

## Phase 2 — Compounding plan and early loops (Feb 2026)

- **Feb 12**: light touch — committing dependency-updated FliHub "opus" projects via voice agent.
- **Feb 22**: the **compounding plan**: client-funded Mac fleet, Mary's six-video Remotion series for AI-TLDR as a slow-burn asset, Remotion knowledge → $1000+ Skool course, agentic-OS "virtual employees" vision.
- **Feb 24**: first YLO friction — the workflow tool keeps launching YouTube Launch Optimizer as the wrong workflow after three corrections; plus an SRT raw-text-export micro-idea (a seed of later transcript-handling work).

## Phase 3 — The tooling detour: YLO/WAI, Ecamm, DeckHand (Mar 1–12)

This is the thread's densest stretch (~60 of 108 records). Three interleaved sub-loops:

### 3a. YouTube WAI / YLO / AWB (Mar 2 → Mar 12)
- Mar 2: three-pass YLO cleanup mandated; operating rule set (code via SupportSignal repo, workflow changes via Alex tool, shared data in git — never gitignored); the YouTube WAI system (IR compiler + HTML runner → n8n-style wizard UIs) reviewed with a ~15-test UAT plan.
- Mar 10–12: sustained AWB grind — prompt-template page regressions ("lost previously requested features while adding unrequested ones"), schema-template discrepancy audit, transcript-accuracy checker, FliHub-chapters→AWB ingestion mapping, FliHub→AWB JSON handoff. Recurring feedback theme: agents rearranging UI instead of doing what was asked.
- Mar 10: **chaptering decision** — manual chaptering (~2h per 1h video) replaced by a FliVideo JSON handover (timestamp + chapter name + first ~50 transcript words), with abridged transcripts and per-video SRTs **explicitly rejected** as inaccurate. Chapter values bind to the original recording transcript, not the edited video.
- Mar 12: UAT-vs-E2E naming "clusterfuck" unravelled by decree: UAT = human-run acceptance tests, never E2E.

### 3b. Ecamm reverse-engineering + DeckHand (Mar 3 → Mar 11)
- Mar 3–4: HyperX settings locked in (gain 2.5–3, mic angled up); central documentation home demanded for all Ecamm/Stream Deck automation knowledge; Ecamm brain harvest of Take One Tech transcripts ordered; discovery that Ecamm's internal HTTP server makes programmatic control feasible.
- Mar 5: the **pedal-recording saga** — ~9 captures in one day of Ecamm action-set buttons toggling states but never actually recording; pedal multi-actions planned; DeckHand conceived as a web app that pushes buttons into and reads config from Ecamm, exposing an API for skills.
- Mar 9–11: the saga becomes **content** — David records the Ecamm-skill video series (port scanning, plist diffing, Bitfocus as endpoint reference, 12-scene natural-language switching via a Python bridge), and hits hard limits: no programmatic crop panning (scene file only saves on app close), port changes every launch, Stream Deck SDK closed (state unreadable) → hacker-style reverse-engineering research requested. Public ask: Ecamm should ship official scene read/write APIs.
- Mar 10: DeckHand direction fixed — replicate Stream Deck's per-application profile model, starting with a single Ecamm Live profile.
- Camera fixed along the way (Mar 7–9): Blackmagic yellow cast (WB ~4550K), flicker solved at 25 fps + 50 Hz.

### 3c. Content planning proper (Mar 4–9, Mar 16)
- Tutorial-video backlog with named audiences (Angela, Lars, James Hicks); Nano Banana / Gemini infographic series (Chiang Mai weather episode, FFmpeg scroll-animation trick, NotebookLM slide-deck → 50s narrated video); four-video batch (Mar 7); Joy Juice bilingual NanoBanana menu series (Mar 10).
- Mar 12: **Nano Banana split into two tracks** — image generation (Jan's side) and a context-shaping skill (David's side), exchanged through FliHub via git.
- Mar 16: BMAD v6 enterprise rebuild video series intro recorded.

## Phase 4 — Digital Stage Summit spike (Mar 17)

Marathon David–Jan sessions: JSON→Markdown wrappers for NotebookLM→Nano Banana→ThumbRack slide generation, SyncThing relay over Tailscale, Skool pricing set at $14.95/month, YouTube editing backlog handed to Jan via Gling, summits brain created for the 11pm talk. This is where the team-production model (Jan/Mary as operators of the pipeline) gets real.

## Phase 5 — The YLO spec, then silence (Apr 11 → Jun 4)

- **Apr 11**: David dictates the **full YouTube Launch Optimizer app requirements** — transcript+SRT ingestion, 12 async AWB analysis prompts, title/thumbnail shortlist funnels (10-20 → 6 → 3), chapter playback validator, publish page. This consolidates six weeks of YLO/WAI/AWB fragments into one app spec (the lineage that becomes FliLaunch).
- Then **dormancy: ~7 weeks with zero captures** (Apr 12 – Jun 4). The thread's tooling energy visibly moved elsewhere (per surrounding context: dark-factory, knowledge systems).

## Phase 6 — Re-emergence, transformed: agent-generated video (Jun 5 → Jul 9)

The thread returns with a different premise — not David-on-camera with better rigging, but **agents producing the video**:

- **Jun 5**: Steve demos Media Studio creative presets (reference-image → reusable image-to-image preset; ~16c/storyboard, ~$2 per 15s video).
- **Jun 12**: David teaches Mary and Jan to reverse-engineer Capsules-style parallax storytelling and pushes them to drive Media Studio via Claude Code instead of manual prompting — 8 weeks of Vaz story videos as the driver.
- **Jun 13**: Remotion-vs-Hyperframes gap analysis commissioned (revisiting the Feb 22 Remotion bet); study of a video Claude Fable 5 one-shotted end-to-end (script → ElevenLabs clone → avatar renders → FFmpeg → HTML/GSAP motion graphics) with replication research queued; complaint that app requirements shouldn't live under brand-dave → dark-factory app-pipeline intake.
- **Jun 14**: **voice script writer architecture** — MVC mapped onto script generation (design/voice doc = View, ~170-video transcript corpus tone shape = Data, deep-research fact sheets = Model, LLM agent = Controller), then reframed toward a Mochaccino-style orchestrator + sub-agent team. Also: Hyperframes skills install **declined** — document subsystems into the brain first, decide later. Hunt for the lost AI-TLDR video-download workflow/catalogue.
- **Jul 9** (latest): **session-to-marketing extraction** — every coding session post-processed by a router-style pass extracting tweets, YouTube content, and lead magnets. The thread's endpoint: content production as an automatic byproduct of doing the work.

---

## Superseded decisions

| Decision (date) | Status | Superseded by |
|---|---|---|
| Daily-livestream "Coding Lab" strategy, multi-platform simulcast, paid X Premium (Jan 31) | **Abandoned in practice** — never resurfaces after Jan 31; Twitter/X destination never confirmed working | Recorded tutorial videos (Mar) → agent-generated pipelines (Jun) |
| Guy paid monthly to cut streams (Jan 31) | No follow-up in this thread | Jan takes YouTube editing via Gling (Mar 17) |
| Remotion as THE video-as-code bet + $1000 Skool Remotion course (Feb 22) | **Under challenge** | Remotion-vs-Hyperframes gap analysis (Jun 13); course never mentioned again |
| Abridged transcripts / per-video SRTs for chaptering (pre-Mar) | **Explicitly rejected** (Mar 10) | FliVideo JSON handover: timestamp + chapter name + first ~50 real-transcript words |
| Canva for thumbnails (implied pre-Mar) | **Lapsed, won't renew** (Mar 3) | Nano Banana / ThumbRack image pipeline |
| "FliHub chatgpt" feature name (Mar 12) | Renamed to "video" | — |
| UAT/E2E conflated naming (Mar) | **Decreed** UAT = human-run acceptance, never E2E (Mar 12) | — |
| YLO as workflow-engine runs inside AWB/WAI (Feb–Mar) | Consolidated | Standalone YLO app spec (Apr 11) → FliLaunch lineage |
| HTML screen generator work (Mar 10) | Paused for MVP focus; BMAD flagged as the better future system | BMAD v6 series (Mar 16) |
| Hyperframes skills install (Jun 14) | **Declined pending documentation** — brain-first, then decide | Open |

## Dormancy map

```
Jan31 ██ Feb ▂▂▂ Mar ██████████ Apr ▂ (Apr11 spec) —— 7-WEEK GAP —— Jun ████ Jul ▂ (Jul9)
```

## Current status (as of 2026-07-13)

- **Active frontier**: agent-generated video — voice script writer (orchestrator + sub-agents), Media Studio driven by Claude Code (Mary/Jan, 8-week Vaz series), Remotion-vs-Hyperframes verdict pending, session-to-marketing extraction as the newest idea (Jul 9).
- **Open loops**: Hyperframes install decision (blocked on brain documentation); AI-TLDR download workflow recovery; YLO/FliLaunch spec awaiting build (see ylo brain for lineage).
- **Quiet loops**: Ecamm/DeckHand automation (last touched ~Mar 11 in this thread); livestreaming entirely silent since Jan 31.
- **Direction of travel**: from *David produces content with better tools* → *the tools produce content from David's work*.
